// Lightweight CTA tracking. Captures clicks/leads locally, mirrors them to
// window.dataLayer (GTM-ready) and ships a sendBeacon to a configurable
// endpoint. Default endpoint is a stub — wire it to a real collector
// before running marketing.

const ENDPOINT = import.meta.env.VITE_TRACK_ENDPOINT || ''
const STORAGE_KEY = 'omnia_landing_events_v1'

function readLog() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]')
  } catch {
    return []
  }
}

function writeLog(events) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(events.slice(-200)))
  } catch {
    /* quota exceeded — drop silently */
  }
}

function getOrCreateAnonId() {
  let id = localStorage.getItem('omnia_anon_id')
  if (!id) {
    id =
      'a-' +
      Math.random().toString(36).slice(2, 10) +
      Date.now().toString(36)
    localStorage.setItem('omnia_anon_id', id)
  }
  return id
}

export function track(event, payload = {}) {
  const record = {
    event,
    ts: Date.now(),
    href: typeof location !== 'undefined' ? location.href : '',
    ref: typeof document !== 'undefined' ? document.referrer : '',
    anon_id: getOrCreateAnonId(),
    ...payload,
  }

  const log = readLog()
  log.push(record)
  writeLog(log)

  if (typeof window !== 'undefined') {
    window.dataLayer = window.dataLayer || []
    window.dataLayer.push({ event: 'omnia_' + event, ...payload })
  }

  if (ENDPOINT && typeof navigator !== 'undefined' && navigator.sendBeacon) {
    try {
      const blob = new Blob([JSON.stringify(record)], { type: 'application/json' })
      navigator.sendBeacon(ENDPOINT, blob)
    } catch {
      /* ignore */
    }
  }

  if (import.meta.env.DEV) {
    // eslint-disable-next-line no-console
    console.log('[track]', event, payload)
  }
}

export function trackedHandler(event, payload = {}, handler) {
  return (...args) => {
    track(event, payload)
    return handler ? handler(...args) : undefined
  }
}
