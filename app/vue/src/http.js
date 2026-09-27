import { ref } from 'vue'

export const down = ref(false)  // the API does not answer: a restart on deploy, a crash, no network

const DOWN = 'Сайт тимчасово недоступний. Спробуй ще раз за хвилину.'
const BROKEN = 'Щось пішло не так на сервері. Викладач уже знає — спробуй ще раз трохи згодом.'
const TEXTS = { Forbidden: 'Нема доступу.', 'Not Found': 'Не знайдено.' }  // FastAPI's own words for a bare 403 and 404

// `status` tells a page «нема» (404) from «зламалось»; 0 = no answer at all
const fail = (message, status) => Object.assign(new Error(message), { status })

async function handle(res) {
  if (res.status === 401) {  // session gone mid-work: sign in and come back here
    location.assign(`/login?error=session&next=${encodeURIComponent(location.pathname + location.search)}`)
    throw fail('Потрібен вхід', 401)
  }
  const data = res.status === 204 ? null : await res.json().catch(() => undefined)
  if (res.status >= 500) {
    if (data !== undefined) throw fail(BROKEN, res.status)
    down.value = true  // the proxy in front of a dead API answers without JSON
    throw fail(DOWN, 0)
  }
  down.value = false
  const detail = typeof data?.detail === 'string' ? data.detail : ''  // a list — pydantic's validation report
  if (!res.ok) throw fail(TEXTS[detail] || detail || `Помилка ${res.status}`, res.status)
  return data
}

function send(url, options) {
  return fetch(url, options).then(handle, () => {
    down.value = true
    throw fail(DOWN, 0)
  })
}

export function request(url, method = 'GET', body) {
  return send(url, {
    method,
    headers: body ? { 'Content-Type': 'application/json' } : {},
    body: body ? JSON.stringify(body) : undefined,
  })
}

// `?a=1&b=2` out of an object; empty, false and undefined values are left out, 0 stays
export function query(params) {
  const q = new URLSearchParams(Object.entries(params).filter(([, v]) => v !== undefined && v !== '' && v !== false)).toString()
  return q && `?${q}`
}

export function upload(url, file) {
  const fd = new FormData()
  fd.append('file', file)
  return send(url, { method: 'POST', body: fd })
}
