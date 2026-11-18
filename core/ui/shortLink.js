const VIDEO = /^(m\.)?(youtube\.com|youtu\.be|vimeo\.com|drive\.google\.com|loom\.com)(\/|$)/

// a link as one reads it: no scheme, no www; a long one keeps its host and its last step, a video gets «▶»
export function shortLink(url, max = 32) {
  let s = url.trim().replace(/^[a-z][\w+.-]*:\/\//i, '').replace(/^www\./, '').replace(/\/$/, '')
  const video = VIDEO.test(s)
  if (s.length > max) {
    const host = s.split('/')[0]
    const last = s.slice(s.lastIndexOf('/') + 1)
    s = host.length + last.length + 3 <= max ? `${host}/…/${last}` : `${s.slice(0, max - 13)}…${s.slice(-12)}`
  }
  return video ? `▶ ${s}` : s
}
