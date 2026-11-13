// what a catalog card asks a claim to show (Task.proof, T284 §7): a hint, never a must.
// `link` — shown by a link, not a picture: the claim's panel points at its link field (ClaimShots.vue)
export const PROOFS = {
  shot: { icon: '📷', label: 'скриншот', ask: 'покажи скриншотом' },
  gif: { icon: '🎞️', label: 'гіфка', ask: 'покажи гіфкою чи коротким відео' },
  video: { icon: '🎬', label: 'відео з поясненням', ask: 'поясни у відео — посилання в заявці', link: 'поясни у відео — посилання на нього в полі вище' },
  code: { icon: '🔗', label: 'посилання на код', ask: 'дай посилання на код: файл або коміт', link: 'дай посилання на код у полі вище: файл або коміт' },
}
