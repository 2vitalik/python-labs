export async function getMe() {
  const res = await fetch('/api/me')
  return res.json()
}
