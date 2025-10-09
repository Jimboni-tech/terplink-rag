import { NextResponse } from 'next/server'

// Proxies POST /api/run-rag to the Flask backend to avoid CORS from the browser.
export async function POST(req: Request) {
  try {
    const contentType = req.headers.get('content-type') || ''

    // Normalize incoming body into URLSearchParams including chat fields
    let payload = new URLSearchParams()
    if (contentType.includes('application/json')) {
      const body = await req.json().catch(() => ({} as any))
      const q = (body?.question ?? body?.data ?? '').toString()
      payload.set('data', q)
      if (body?.session_id) payload.set('session_id', String(body.session_id))
      if (typeof body?.reset !== 'undefined') payload.set('reset', String(body.reset))
      if (typeof body?.top_k !== 'undefined') payload.set('top_k', String(body.top_k))
      if (body?.history) payload.set('history', JSON.stringify(body.history))
    } else {
      const form = await req.formData()
      const q = (form.get('data') || form.get('question') || '').toString()
      payload.set('data', q)
      const sessionId = form.get('session_id')
      if (sessionId) payload.set('session_id', sessionId.toString())
      const reset = form.get('reset')
      if (reset !== null && reset !== undefined) payload.set('reset', String(reset))
      const topk = form.get('top_k')
      if (topk !== null && topk !== undefined) payload.set('top_k', String(topk))
      const history = form.get('history')
      if (history) payload.set('history', history.toString())
    }

    const configured = process.env.API_BASE || process.env.NEXT_PUBLIC_API_BASE || ''
    const candidates = configured
      ? [configured]
      : ['http://127.0.0.1:5000', 'http://localhost:5000']

    const attempted: string[] = []
    let lastErr: any = null
    for (const base of candidates) {
      const url = `${base.replace(/\/$/, '')}/run-rag`
      attempted.push(url)
      try {
        const res = await fetch(url, {
          method: 'POST',
          body: payload,
          headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' },
        })
        const text = await res.text()
        const headers: Record<string, string> = {}
        const ct = res.headers.get('content-type')
        headers['Content-Type'] = ct || 'text/plain; charset=utf-8'
        return new NextResponse(text, { status: res.status, headers })
      } catch (e: any) {
        lastErr = e
        continue
      }
    }
    return NextResponse.json({ error: lastErr?.message || 'Proxy error', attempted }, { status: 500 })
  } catch (e: any) {
    return NextResponse.json({ error: e?.message || 'Proxy error' }, { status: 500 })
  }
}
