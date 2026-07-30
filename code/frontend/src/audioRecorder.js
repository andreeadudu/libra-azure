// Records the microphone and encodes it as 16 kHz mono PCM WAV — the exact
// format /tools/transcribe expects (see backend/app/services/speech.py). The
// browser has no built-in encoder for that (MediaRecorder only gives
// compressed webm/opus), so this resamples and writes the WAV by hand.

const TARGET_SAMPLE_RATE = 16000

function writeString(view, offset, str) {
  for (let i = 0; i < str.length; i++) view.setUint8(offset + i, str.charCodeAt(i))
}

function encodeWav(samples, sampleRate) {
  const buffer = new ArrayBuffer(44 + samples.length * 2)
  const view = new DataView(buffer)
  writeString(view, 0, 'RIFF')
  view.setUint32(4, 36 + samples.length * 2, true)
  writeString(view, 8, 'WAVE')
  writeString(view, 12, 'fmt ')
  view.setUint32(16, 16, true)
  view.setUint16(20, 1, true)          // PCM
  view.setUint16(22, 1, true)          // mono
  view.setUint32(24, sampleRate, true)
  view.setUint32(28, sampleRate * 2, true)
  view.setUint16(32, 2, true)
  view.setUint16(34, 16, true)
  writeString(view, 36, 'data')
  view.setUint32(40, samples.length * 2, true)
  let offset = 44
  for (let i = 0; i < samples.length; i++, offset += 2) {
    const s = Math.max(-1, Math.min(1, samples[i]))
    view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7fff, true)
  }
  return new Blob([buffer], { type: 'audio/wav' })
}

// Mic input rarely arrives at exactly 16 kHz (Safari especially ignores the
// AudioContext sampleRate hint), so average consecutive samples down to it.
function downsample(buffer, inRate, outRate) {
  if (outRate === inRate) return buffer
  const ratio = inRate / outRate
  const newLength = Math.round(buffer.length / ratio)
  const result = new Float32Array(newLength)
  let offsetBuffer = 0
  for (let i = 0; i < newLength; i++) {
    const next = Math.round((i + 1) * ratio)
    let sum = 0, count = 0
    for (let j = offsetBuffer; j < next && j < buffer.length; j++) { sum += buffer[j]; count++ }
    result[i] = count > 0 ? sum / count : 0
    offsetBuffer = next
  }
  return result
}

export const micSupported = typeof navigator !== 'undefined' && !!navigator.mediaDevices?.getUserMedia

/** Starts capturing the microphone. Returns a controller: stop() resolves to a WAV Blob, cancel() discards it. */
export async function startMicRecording() {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
  const AudioCtx = window.AudioContext || window.webkitAudioContext
  const ctx = new AudioCtx()
  const source = ctx.createMediaStreamSource(stream)
  // ScriptProcessorNode is deprecated but universally supported and needs no
  // separate worklet module to be served — the simplest correct choice here.
  const processor = ctx.createScriptProcessor(4096, 1, 1)
  const chunks = []

  processor.onaudioprocess = (e) => chunks.push(new Float32Array(e.inputBuffer.getChannelData(0)))
  source.connect(processor)
  processor.connect(ctx.destination) // some browsers only fire onaudioprocess once connected to a sink

  const teardown = () => {
    processor.disconnect()
    source.disconnect()
    stream.getTracks().forEach((t) => t.stop())
  }

  return {
    stop() {
      teardown()
      const total = chunks.reduce((n, c) => n + c.length, 0)
      const merged = new Float32Array(total)
      let offset = 0
      for (const c of chunks) { merged.set(c, offset); offset += c.length }
      const wav = encodeWav(downsample(merged, ctx.sampleRate, TARGET_SAMPLE_RATE), TARGET_SAMPLE_RATE)
      ctx.close()
      return wav
    },
    cancel() {
      teardown()
      ctx.close()
    },
  }
}
