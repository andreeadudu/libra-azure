import { useEffect, useRef, useState } from 'react'
import { api } from '../api'
import { micSupported, startMicRecording } from '../audioRecorder'
import { Err, RunsOnBadge } from '../components'

export default function Chat({ conversation, onMessagesChange, agents, hostedOnly = [], foundry }) {
  const messages = conversation.messages
  const setMessages = onMessagesChange // same updater-fn-or-value signature as React's setState
  const [question, setQuestion] = useState('')
  const [agent, setAgent] = useState('default')
  const [useRag, setUseRag] = useState(true)
  const [factCheck, setFactCheck] = useState(false)
  const [mode, setMode] = useState('local')
  const [topK, setTopK] = useState(3)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState(null)
  const [showOptions, setShowOptions] = useState(false)
  const [copied, setCopied] = useState(null)
  const [speech, setSpeech] = useState({}) // message index -> { busy, url, error }
  const [recording, setRecording] = useState(false)
  const [transcribing, setTranscribing] = useState(false)
  const endRef = useRef(null)
  const taRef = useRef(null)
  const recorderRef = useRef(null)

  useEffect(() => { endRef.current?.scrollIntoView({ behavior: 'smooth' }) }, [messages, busy])
  // Blob URLs are per-conversation (Chat remounts on switch, see App.jsx's `key`) — release them on unmount.
  useEffect(() => () => { Object.values(speech).forEach((s) => s?.url && URL.revokeObjectURL(s.url)) }, []) // eslint-disable-line react-hooks/exhaustive-deps
  // Switching conversations remounts Chat (see App.jsx's `key`) — don't leave the mic hot.
  useEffect(() => () => recorderRef.current?.cancel?.(), [])

  function autoGrow(el) {
    if (!el) return
    el.style.height = 'auto'
    el.style.height = `${Math.min(el.scrollHeight, 200)}px`
  }

  async function listen(i, text) {
    setSpeech((s) => ({ ...s, [i]: { busy: true, url: s[i]?.url, error: null } }))
    try {
      const blob = await api.speak({ text })
      setSpeech((s) => {
        if (s[i]?.url) URL.revokeObjectURL(s[i].url)
        return { ...s, [i]: { busy: false, url: URL.createObjectURL(blob), error: null } }
      })
    } catch (e) {
      setSpeech((s) => ({ ...s, [i]: { busy: false, url: s[i]?.url, error: e.message } }))
    }
  }

  async function copy(i, text) {
    try {
      await navigator.clipboard.writeText(text)
      setCopied(i)
      setTimeout(() => setCopied((c) => (c === i ? null : c)), 1500)
    } catch { /* clipboard unavailable — silently ignore */ }
  }

  async function toggleMic() {
    if (recording) {
      setRecording(false)
      const controller = recorderRef.current
      recorderRef.current = null
      if (!controller) return
      setTranscribing(true); setError(null)
      try {
        const blob = controller.stop()
        const file = new File([blob], 'dictation.wav', { type: 'audio/wav' })
        const result = await api.transcribe(file)
        setQuestion((q) => {
          const next = q.trim() ? `${q.trim()} ${result.text}` : result.text
          requestAnimationFrame(() => autoGrow(taRef.current))
          return next
        })
        taRef.current?.focus()
      } catch (e) { setError(e.message) } finally { setTranscribing(false) }
      return
    }
    setError(null)
    try {
      recorderRef.current = await startMicRecording()
      setRecording(true)
    } catch (e) { setError(e.message || 'Microphone unavailable') }
  }

  async function send() {
    const text = question.trim()
    if (!text || busy) return
    setQuestion(''); setError(null); setBusy(true)
    if (taRef.current) taRef.current.style.height = 'auto'
    setMessages((m) => [...m, { role: 'user', text }])
    try {
      const data = await api.ask({ question: text, use_rag: useRag, top_k: Number(topK),
                                  agent, agent_mode: mode, fact_check: factCheck })
      setMessages((m) => [...m, { role: 'bot', data }])
    } catch (e) {
      setMessages((m) => [...m, { role: 'err', text: e.message }])
      setError(e.message)
    } finally { setBusy(false) }
  }

  const all = [...agents, ...hostedOnly]
  const current = all.find((a) => a.name === agent)

  // Three states, not two. `available === false` is not "we don't know" — it is a
  // definite no: the Agent Service cannot be reached from here at all, whichever agent
  // you pick, because a key was used where Entra is required. Offering the lane anyway
  // is how you get a 503 in the chat window instead of a greyed-out option.
  const foundryReachable = foundry?.available                 // true | false | undefined
  const isHosted = current?.runs_on === 'both' || current?.runs_on === 'foundry'
  const localImpossible = current?.runs_on === 'foundry'      // no JSON file to run here
  const foundryBlocked =
    foundryReachable === false ||                             // no identity — nothing can
    (foundryReachable === true && !isHosted)                  // reachable, but not deployed
  const foundryWhy =
    foundryReachable === false
      ? (foundry?.reason || 'The Agent Service cannot be reached from here.')
      : 'Not deployed to Foundry — deploy it from the Agents view'

  // Keep the mode legal whenever the selected agent changes.
  useEffect(() => {
    if (foundryBlocked && mode === 'foundry') setMode('local')
    else if (localImpossible && mode !== 'foundry') setMode('foundry')
  }, [agent, localImpossible, foundryBlocked])   // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div className="chat-wrap">
      <div className="chat-top">
        <div className="chat-top-left">
          <select className="pill-select" value={agent} onChange={(e) => setAgent(e.target.value)}
                  title="Which persona answers">
            {agents.map((a) => <option key={a.name} value={a.name}>{a.display_name}</option>)}
            {hostedOnly.length > 0 && (
              <optgroup label="hosted in Foundry only">
                {hostedOnly.map((a) => <option key={a.name} value={a.name}>{a.display_name}</option>)}
              </optgroup>
            )}
          </select>
          {current && <RunsOnBadge runsOn={current.runs_on} reason={foundry?.reason} />}
          {foundryReachable === false && (
            <span className="badge muted" title={foundryWhy}>hosted agents off — key auth</span>
          )}
        </div>
        <div className="chat-top-right">
          <button className="icon-btn" onClick={() => setShowOptions((v) => !v)} title="Chat options"
                  aria-expanded={showOptions}>⚙</button>
        </div>
        {showOptions && (
          <div className="options-panel">
            <label className="check" title="Retrieve from your documents and ground the answer">
              <input type="checkbox" checked={useRag} onChange={(e) => setUseRag(e.target.checked)} />
              use RAG
            </label>
            <label className="check" title="After answering, verify the answer against the open web and attach a verdict">
              <input type="checkbox" checked={factCheck} onChange={(e) => setFactCheck(e.target.checked)} />
              fact-check
            </label>
            <div>
              <label htmlFor="chat-mode">where the loop executes</label>
              <select id="chat-mode" value={mode} onChange={(e) => setMode(e.target.value)}>
                <option value="local" disabled={localImpossible}
                        title={localImpossible ? 'This agent has no local JSON file' : ''}>
                  local agent
                </option>
                <option value="foundry" disabled={foundryBlocked} title={foundryBlocked ? foundryWhy : ''}>
                  Foundry agent{foundryReachable === false ? ' — no identity'
                                : foundryBlocked ? ' — not deployed' : ''}
                </option>
              </select>
            </div>
            <div>
              <label htmlFor="chat-topk">passages to retrieve</label>
              <input id="chat-topk" type="number" min="1" max="10" value={topK}
                     onChange={(e) => setTopK(e.target.value)} />
            </div>
            {current && <span className="badge muted" title={current.description}>temp {current.temperature ?? '—'}</span>}
            <button className="btn btn-outline btn-sm" onClick={() => setMessages([])}>clear this chat</button>
          </div>
        )}
      </div>

      <div className="msgs">
        <div className="msgs-inner">
          {messages.length === 0 && (
            <div className="empty-state">
              <span className="brand-mark" style={{ margin: '0 auto .8rem' }}>
                {(current?.display_name || 'L').charAt(0)}
              </span>
              <h3 style={{ margin: '0 0 .4rem' }}>{current?.display_name || 'Libra Assist'}</h3>
              <p className="muted" style={{ margin: 0 }}>
                {current?.description
                  || 'Ask a question about the documents you have ingested. Switch the persona to change how '
                     + 'it answers, or turn RAG off to see the model answer without grounding.'}
              </p>
            </div>
          )}

          {messages.map((m, i) => {
            if (m.role === 'user') return (
              <div className="msg-row user" key={i}><div className="msg user">{m.text}</div></div>
            )
            if (m.role === 'err') return (
              <div className="msg-row bot" key={i}>
                <div className="msg-avatar err">!</div>
                <div className="msg err"><strong>Request failed:</strong> {m.text}</div>
              </div>
            )
            const d = m.data
            const sp = speech[i]
            return (
              <div className="msg-row bot" key={i}>
                <div className="msg-avatar">{(d.agent?.display_name || 'L').charAt(0)}</div>
                <div className="msg bot">
                  {d.answer}
                  <div className="msg-meta">
                    <span className="badge">{d.agent?.display_name || 'agent'}</span>
                    <span className={`badge ${d.augmented ? 'gold' : 'muted'}`}>{d.augmented ? 'grounded' : 'no retrieval'}</span>
                    <span className="badge muted">{d.agent?.mode}</span>
                    <span className="badge muted">{d.model}</span>
                    {d.usage && <span className="badge muted">{d.usage.prompt_tokens}↑ {d.usage.completion_tokens}↓ tokens</span>}
                    <button className="btn btn-outline btn-sm" onClick={() => copy(i, d.answer)}
                            title="Copy this answer">
                      {copied === i ? '✓ copied' : '⧉ copy'}
                    </button>
                    <button className="btn btn-outline btn-sm" onClick={() => listen(i, d.answer)} disabled={sp?.busy}
                            title="Read this answer aloud (Azure AI Speech)">
                      {sp?.busy ? <><span className="spin" /> synthesizing…</> : '🔊 listen'}
                    </button>
                  </div>
                  {sp?.error && <div className="err" style={{ marginTop: '.4rem' }}>{sp.error}</div>}
                  {sp?.url && <audio controls autoPlay src={sp.url} style={{ marginTop: '.5rem', width: '100%' }} />}
                  {d.fact_check && (
                    <div className="src" style={{ marginTop: '.55rem',
                         borderLeftColor: d.fact_check.verdict === 'supported' ? 'var(--c-teal)'
                           : d.fact_check.verdict === 'contradicted' ? 'var(--c-crimson)' : 'var(--c-gold)' }}>
                      <span className={`badge ${d.fact_check.verdict === 'contradicted' ? 'crimson'
                        : d.fact_check.verdict === 'supported' ? '' : 'gold'}`}>
                        fact-check: {d.fact_check.verdict}
                      </span>{' '}
                      <span className="faint">{d.fact_check.confidence} confidence · {d.fact_check.evidence_from}</span>
                      {d.fact_check.error
                        ? <div className="faint" style={{ marginTop: '.3rem' }}>{d.fact_check.error}</div>
                        : <div style={{ marginTop: '.3rem' }}>{d.fact_check.reasoning}</div>}
                      {d.fact_check.sources?.length > 0 && (
                        <ul className="faint" style={{ margin: '.35rem 0 0', paddingLeft: '1.1rem' }}>
                          {d.fact_check.sources.map((sc) => (
                            <li key={sc.rank}>
                              <a href={sc.url} target="_blank" rel="noreferrer">{sc.title || sc.url}</a>
                              {' '}{sc.used ? `(${sc.chars_read} chars read)` : '(could not be read)'}
                            </li>
                          ))}
                        </ul>
                      )}
                    </div>
                  )}
                  {d.retrieved?.length > 0 && (
                    <details className="sources">
                      <summary>{d.retrieved.length} retrieved passage{d.retrieved.length > 1 ? 's' : ''}</summary>
                      {d.retrieved.map((h, j) => (
                        <div className="src" key={h.id}>
                          <span className="score">[{j + 1}] score {h.score.toFixed(4)}</span>
                          <div>{h.text}</div>
                        </div>
                      ))}
                    </details>
                  )}
                  <details className="sources">
                    <summary>the exact prompt that was sent</summary>
                    <pre className="out" style={{ marginTop: '.4rem' }}>{`SYSTEM:\n${d.system_prompt}\n\nUSER:\n${d.prompt_sent}`}</pre>
                  </details>
                </div>
              </div>
            )
          })}
          {busy && (
            <div className="msg-row bot">
              <div className="msg-avatar">{(current?.display_name || 'L').charAt(0)}</div>
              <div className="msg bot"><span className="spin" /> thinking…</div>
            </div>
          )}
          <div ref={endRef} />
        </div>
      </div>

      <Err error={error} />
      <div className="composer-wrap">
        <div className="composer">
          {micSupported && (
            <button className={`composer-mic ${recording ? 'recording' : ''}`} onClick={toggleMic}
                    disabled={busy || (transcribing && !recording)}
                    title={recording ? 'Stop and transcribe' : 'Dictate with your microphone'}>
              {transcribing ? <span className="spin" /> : recording ? '■' : '🎤'}
            </button>
          )}
          <textarea ref={taRef} value={question} rows={1}
                    placeholder={recording ? 'Listening…' : 'Ask Libra Assist…  (Enter to send, Shift+Enter for a new line)'}
                    onChange={(e) => { setQuestion(e.target.value); autoGrow(e.target) }}
                    onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send() } }} />
          <button className="composer-send" onClick={send} disabled={busy || !question.trim()} title="Send">↑</button>
        </div>
        <p className="composer-note">Libra Assist can make mistakes. Check important information.</p>
      </div>
    </div>
  )
}
