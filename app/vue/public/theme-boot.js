// plain script in <head>: the theme is set before the first paint, so a dark page never flashes white
// (a file, not an inline script — a Content-Security-Policy with script-src 'self' lets it through)
{
  let theme
  try { theme = localStorage.getItem('theme') } catch { /* storage blocked */ }
  theme ||= matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  document.documentElement.dataset.bsTheme = theme
}
