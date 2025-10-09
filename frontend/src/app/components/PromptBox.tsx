'use client'

import { useEffect, useRef, useState } from 'react'

type OrgItem = { name?: string; rationale?: string; url?: string }
type ChatMsg = { role: 'user' | 'assistant'; content: string }

export default function PromptBox() {
  const [prompt, setPrompt] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [messages, setMessages] = useState<ChatMsg[]>([])
  // Always use fast mode and Top K = 3 (no UI controls needed)

  // Decide endpoint: use proxy route if NEXT_PUBLIC_API_BASE is not set
  const apiBaseEnv = process.env.NEXT_PUBLIC_API_BASE as string | undefined
  const resultRef = useRef<HTMLDivElement | null>(null)
  const errorRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    if (error && errorRef.current) errorRef.current.focus()
  }, [error])

  // Auto-scroll the transcript container when new messages arrive (without focusing it)
  useEffect(() => {
    const el = resultRef.current
    if (el) {
      try {
        el.scrollTo({ top: el.scrollHeight, behavior: 'smooth' })
      } catch {
        el.scrollTop = el.scrollHeight
      }
    }
  }, [messages])

  // Persist session id across reloads for a smoother chat experience
  useEffect(() => {
    const saved = typeof window !== 'undefined' ? window.localStorage.getItem('terplink_session_id') : null
    if (saved) setSessionId(saved)
  }, [])
  useEffect(() => {
    if (sessionId && typeof window !== 'undefined') {
      window.localStorage.setItem('terplink_session_id', sessionId)
    }
  }, [sessionId])

  const handleSubmit = async (e?: React.FormEvent<HTMLFormElement> | React.MouseEvent<HTMLButtonElement>) => {
    e?.preventDefault?.()
    if (!prompt.trim()) return
    setLoading(true)
    setError(null)
    try {
      // optimistic update of chat transcript
      setMessages((m) => [...m, { role: 'user', content: prompt }])

      const body = new URLSearchParams()
      body.append('data', prompt)
    if (sessionId) body.append('session_id', sessionId)
    body.append('top_k', '3')
    body.append('fast', 'true')

      const url = apiBaseEnv ? `${apiBaseEnv.replace(/\/$/, '')}/run-rag` : '/api/run-rag'
      const res = await fetch(url, { method: 'POST', body, mode: 'cors' })

      if (!res.ok) {
        const rawErr = await res.text().catch(() => '')
        if (res.status === 404) throw new Error(`404 from ${url} — backend route not found. Is the Flask server running?`)
        throw new Error(rawErr || `Request failed: ${res.status}`)
      }

      const raw = await res.text()
      // Try JSON first (preferred), otherwise treat raw as plain text
      try {
        const parsed = JSON.parse(raw)
        if (parsed && typeof parsed === 'object') {
          if (parsed.session_id && !sessionId) setSessionId(String(parsed.session_id))
          const replyText = parsed.reply ? String(parsed.reply) : String(raw)
          setMessages((m) => [...m, { role: 'assistant', content: replyText }])
        } else {
          setMessages((m) => [...m, { role: 'assistant', content: String(raw) }])
        }
      } catch {
        setMessages((m) => [...m, { role: 'assistant', content: String(raw) }])
      }
      setPrompt('')
    } catch (err: any) {
      setError(err?.message ?? String(err))
    } finally {
      setLoading(false)
    }
  }

  const handleReset = async () => {
    setMessages([])
    setError(null)
    try {
      const body = new URLSearchParams()
      if (sessionId) body.append('session_id', sessionId)
      body.append('reset', 'true')
      const url = apiBaseEnv ? `${apiBaseEnv.replace(/\/$/, '')}/run-rag` : '/api/run-rag'
      await fetch(url, { method: 'POST', body, mode: 'cors' }).catch(() => {})
    } catch {}
  }

  // quick suggestions to improve usability
  const suggestions = [
    'robotics and hardware projects',
    'community service and volunteering',
    'cultural organizations and events',
    'entrepreneurship and startups',
    'music and performing arts'
  ]

  // No JSON rendering; we only show the chat transcript for a clean look

  return (
    <section className="relative mx-auto max-w-3xl min-h-screen flex flex-col">
      <header className="px-4 pt-6 pb-4">
        <h1 className="text-center text-4xl md:text-5xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-red-800 to-red-500">
          terpBot
        </h1>
      </header>

      {/* Messages area */}
  <main className="flex-1 overflow-y-auto px-4 pb-36 focus:outline-none focus-visible:outline-none" ref={resultRef} aria-live="polite" id="results">
        {error && (
          <div
            ref={errorRef}
            role="alert"
            id="error-message"
            tabIndex={-1}
            className="mb-3 rounded-md border border-red-200 bg-red-50 px-3 py-2 text-red-700"
          >
            {error}
          </div>
        )}

        {messages.length > 0 && (
          <ul className="space-y-2">
            {messages.map((m, i) => (
              <li key={i} className={m.role === 'user' ? 'text-right' : 'text-left'}>
                <div className={`inline-block max-w-[85%] rounded-lg px-3 py-2 text-sm ${m.role === 'user' ? 'bg-red-600 text-white' : 'bg-gray-100 text-gray-900'}`}>
                  {m.content}
                </div>
              </li>
            ))}
          </ul>
        )}

        {loading && (
          <div role="status" aria-live="polite" className="mt-3 text-sm text-gray-600">
            Searching…
          </div>
        )}
      </main>

      {/* Fixed bottom prompt bar */}
      <div className="fixed inset-x-0 bottom-0 z-50 w-full backdrop-blur-md bg-gradient-to-t from-white/95 via-white/90 to-transparent" style={{ paddingBottom: 'calc(env(safe-area-inset-bottom) + 0.5rem)' }}>
        <div className="mx-auto max-w-3xl px-4 pt-2">
        <form
          onSubmit={handleSubmit}
          aria-busy={loading}
          className="rounded-xl border border-gray-200 bg-white shadow-lg p-2 flex items-center gap-2"
        >
          <input
            id="prompt"
            name="prompt"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Describe yourself to find matching student organizations"
            aria-describedby={error ? 'error-message' : undefined}
            aria-invalid={!!error}
            aria-controls="results"
            required
            autoFocus
            className="flex-1 rounded-md border-0 bg-transparent px-3 py-2 text-gray-900 placeholder:text-gray-400 focus:outline-none focus-visible:ring-2 focus-visible:ring-red-300"
          />
          {/* Reset button: clears chat history */}
          <button
            type="button"
            onClick={handleReset}
            className="hidden sm:inline-flex rounded-md border border-gray-300 px-3 py-2 text-gray-700 hover:bg-gray-100 focus-visible:ring-2 focus-visible:ring-red-300"
          >
            Reset
          </button>
          {/* Search button: submits your prompt */}
          <button
            type="submit"
            disabled={loading || !prompt.trim()}
            className="inline-flex items-center rounded-md bg-red-600 px-4 py-2 text-white shadow-sm hover:bg-red-700 disabled:opacity-50 focus-visible:ring-2 focus-visible:ring-red-300"
          >
            {loading ? 'Searching…' : 'Search'}
          </button>
        </form>
        </div>
      </div>
    </section>
  )
}