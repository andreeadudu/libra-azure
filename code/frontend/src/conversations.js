// Client-side chat history — the backend's /ask is stateless (no threads, no
// server-side memory), so "conversations" are a browser-local grouping of
// Q&A pairs, persisted to localStorage like a ChatGPT/Claude sidebar.

const LIST_KEY = 'libra-assist:conversations'
const ACTIVE_KEY = 'libra-assist:active-conversation'

function newId() {
  return (crypto.randomUUID?.() || `${Date.now()}-${Math.random().toString(16).slice(2)}`)
}

export function emptyConversation() {
  return { id: newId(), title: 'New chat', messages: [], createdAt: Date.now() }
}

export function loadConversations() {
  try {
    const raw = localStorage.getItem(LIST_KEY)
    const list = raw ? JSON.parse(raw) : []
    if (Array.isArray(list) && list.length > 0) return list
  } catch { /* corrupt or blocked storage — start fresh */ }
  return [emptyConversation()]
}

export function loadActiveId(conversations) {
  const saved = localStorage.getItem(ACTIVE_KEY)
  return conversations.some((c) => c.id === saved) ? saved : conversations[0].id
}

export function saveConversations(list) {
  try { localStorage.setItem(LIST_KEY, JSON.stringify(list)) } catch { /* storage full/blocked */ }
}

export function saveActiveId(id) {
  try { localStorage.setItem(ACTIVE_KEY, id) } catch { /* storage full/blocked */ }
}

export function titleFrom(text) {
  const trimmed = text.trim().replace(/\s+/g, ' ')
  return trimmed.length > 42 ? `${trimmed.slice(0, 42)}…` : trimmed
}
