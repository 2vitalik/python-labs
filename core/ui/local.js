// localStorage that may be absent (private mode, blocked storage): reads fall back, writes just don't remember
export const load = (key) => { try { return localStorage.getItem(key) } catch { return null } }
export const save = (key, value) => { try { localStorage.setItem(key, value) } catch { /* not remembered */ } }
