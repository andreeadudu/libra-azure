import { useCallback, useEffect, useState } from 'react'
import { api } from './api'
import { emptyConversation, loadActiveId, loadConversations, saveActiveId, saveConversations, titleFrom }
  from './conversations'
import Agents from './views/Agents'
import Chat from './views/Chat'
import Knowledge from './views/Knowledge'
import Search from './views/Search'
import Status from './views/Status'
import Tools from './views/Tools'

const TOOL_VIEWS = [
  { id: 'knowledge', label: 'Knowledge', group: 'Pipeline' },
  { id: 'search', label: 'Retrieval', group: 'Pipeline' },
  { id: 'agents', label: 'Agents', group: 'Platform' },
  { id: 'tools', label: 'Tools', group: 'Platform' },
  { id: 'status', label: 'Status', group: 'Platform' },
]

export default function App() {
  const [view, setView] = useState('chat')
  const [agents, setAgents] = useState([])
  const [hostedOnly, setHostedOnly] = useState([])
  const [foundry, setFoundry] = useState(null)
  const [health, setHealth] = useState(null)
  const [azure, setAzure] = useState(null)
  const [theme, setTheme] = useState('light')

  const [conversations, setConversations] = useState(() => loadConversations())
  const [activeId, setActiveId] = useState(() => loadActiveId(conversations))

  const loadAgents = useCallback(() => {
    api.agents()
      .then((d) => { setAgents(d.personas || []); setHostedOnly(d.hosted_only || []); setFoundry(d.foundry) })
      .catch(() => { setAgents([]); setHostedOnly([]); setFoundry(null) })
  }, [])
  const loadHealth = useCallback(() => {
    api.health().then(setHealth).catch(() => setHealth(null))
  }, [])
  const loadAzure = useCallback(() => {
    api.azure().then(setAzure).catch(() => setAzure(null))
  }, [])

  useEffect(() => { loadAgents(); loadHealth(); loadAzure() }, [loadAgents, loadHealth, loadAzure])
  useEffect(() => { document.documentElement.dataset.theme = theme }, [theme])
  useEffect(() => { saveConversations(conversations) }, [conversations])
  useEffect(() => { saveActiveId(activeId) }, [activeId])
  // A conversation can vanish (deleted) out from under the saved active id.
  useEffect(() => {
    if (!conversations.some((c) => c.id === activeId)) setActiveId(conversations[0]?.id)
  }, [conversations, activeId])

  const groups = [...new Set(TOOL_VIEWS.map((v) => v.group))]
  const online = health?.status === 'ok'
  const activeConversation = conversations.find((c) => c.id === activeId) || conversations[0]

  function newConversation() {
    const c = emptyConversation()
    setConversations((cs) => [c, ...cs])
    setActiveId(c.id)
    setView('chat')
  }

  function openConversation(id) {
    setActiveId(id)
    setView('chat')
  }

  function deleteConversation(id) {
    setConversations((cs) => {
      const next = cs.filter((c) => c.id !== id)
      return next.length > 0 ? next : [emptyConversation()]
    })
  }

  function updateMessages(id, updater) {
    setConversations((cs) => cs.map((c) => {
      if (c.id !== id) return c
      const messages = typeof updater === 'function' ? updater(c.messages) : updater
      const title = c.title === 'New chat' && messages[0]?.role === 'user' ? titleFrom(messages[0].text) : c.title
      return { ...c, messages, title }
    }))
  }

  return (
    <div className="app">
      <aside className="side">
        <div className="brand">
          <span className="brand-mark">L</span>
          <p className="brand-text">Libra Assist<small>console</small></p>
        </div>

        <button className="btn-newchat" onClick={newConversation}>
          <span aria-hidden="true">+</span> New chat
        </button>

        <div className="conv-list">
          {conversations.map((c) => (
            <div key={c.id} className={`conv-item ${view === 'chat' && c.id === activeId ? 'active' : ''}`}
                 onClick={() => openConversation(c.id)}>
              <span className="conv-title">{c.title}</span>
              {conversations.length > 1 && (
                <button className="conv-del" title="Delete chat"
                        onClick={(e) => { e.stopPropagation(); deleteConversation(c.id) }}>×</button>
              )}
            </div>
          ))}
        </div>

        <div className="nav-tools">
          {groups.map((g) => (
            <div key={g}>
              <div className="nav-group">{g}</div>
              {TOOL_VIEWS.filter((v) => v.group === g).map((v) => (
                <button key={v.id} className={`nav-item ${view === v.id ? 'active' : ''}`} onClick={() => setView(v.id)}>
                  <span className="dot" />{v.label}
                </button>
              ))}
            </div>
          ))}
        </div>

        <div className="side-foot">
          <div style={{ display: 'flex', alignItems: 'center', gap: '.4rem', marginBottom: '.4rem' }}>
            <span className="dot" style={{ width: 7, height: 7, borderRadius: '50%',
              background: online ? 'var(--c-teal)' : 'var(--c-crimson)', display: 'inline-block' }} />
            {online ? `${health.llm.provider} · ${health.llm.model}` : 'backend offline'}
          </div>
          {azure?.configured && (
            <div style={{ marginBottom: '.5rem' }} title={azure.auth === 'identity'
              ? 'Signed in with Microsoft Entra — the Agent Service and control plane are available'
              : 'Key authentication — the Agent Service and control plane cannot be queried'}>
              <span className={`badge ${azure.auth === 'identity' ? '' : 'gold'}`}>
                {azure.auth === 'identity' ? 'Entra identity' : 'key auth'}
              </span>
            </div>
          )}
          <button className="btn btn-outline btn-sm" onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}>
            ◐ {theme === 'dark' ? 'light' : 'dark'}
          </button>
        </div>
      </aside>

      <main className="main">
        {view === 'chat' && activeConversation && (
          <Chat key={activeConversation.id} conversation={activeConversation}
                onMessagesChange={(updater) => updateMessages(activeConversation.id, updater)}
                agents={agents} hostedOnly={hostedOnly} foundry={foundry} />
        )}
        {view === 'knowledge' && <Knowledge />}
        {view === 'search' && <Search />}
        {view === 'agents' && <Agents agents={agents} hostedOnly={hostedOnly} foundry={foundry}
                                      reload={loadAgents} azure={azure} />}
        {view === 'tools' && <Tools />}
        {view === 'status' && <Status health={health} reload={loadHealth}
                                      azure={azure} reloadAzure={loadAzure} />}
      </main>
    </div>
  )
}
