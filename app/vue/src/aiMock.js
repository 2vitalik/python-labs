// «?ai=mock» in a dev build (ai.js): the panel of «Описати словами» without the backend and the key. One draft is the maze
// of app/api/ai/examples.json laid out by hand in the contract's Item form, another an older round already sorted out;
// «Розібрати» answers the maze again (a text with «помилка» — the error of a spent limit), apply and state change it here
const item = (key, group, data, quote, more = {}) => ({ key, group, data, quote, hint: '', needs: [], state: 'open', made: '', ...more })
const rule = (when, then, more = {}) => ({ when, then, ...more })
const TEXT = 'Гра — лабіринт. Гравець ходить стрілками на одну клітинку за раз. Є стіни, через них не пройти. По лабіринту лежать ключі: '
  + 'наступив на ключ — він зникає, і відчиняються двері. Коли зібрав усі ключі, відкривається вихід; зайшов у вихід — перемога, '
  + 'показується вікно «Перемога». На старті головне меню: «Грати» і «Вийти». Поле 17 на 7, лабіринт один, малював сам. '
  + 'Збоку показую, скільки ключів зібрано. Потім ще хочу зробити туман війни і, може, збереження.'

const maze = (id, text = TEXT) => ({ id, at: new Date().toISOString(), text, model: 'mock', cost: 0.012, error: '', items: [
  item('f', 'field', { control: ['direct'], size: '17×7' }, 'Поле 17 на 7'),
  item('e1', 'entity', { title: 'Гравець', role: 'player', description: 'Ходить стрілками на одну клітинку за раз' }, 'Гравець ходить стрілками на одну клітинку за раз'),
  item('e2', 'entity', { title: 'Стіна', role: 'static', description: 'Через неї не пройти' }, 'Є стіни, через них не пройти', { state: 'exists' }),
  item('e3', 'entity', { title: 'Ключ', role: 'pickup', description: 'Зникає, коли на нього наступити; відчиняє двері' }, 'По лабіринту лежать ключі'),
  item('e4', 'entity', { title: 'Двері', role: 'gate', description: 'Відчиняються, коли зібрано ключ', states: ['зачинені', 'відчинені'] }, 'він зникає, і відчиняються двері'),
  item('e5', 'entity', { title: 'Вихід', role: 'gate', description: 'Відкривається, коли зібрано всі ключі', states: ['зачинений', 'відчинений'] }, 'Коли зібрав усі ключі, відкривається вихід'),
  item('r1', 'rule', rule({ kind: 'input', action: '↑', a: 'Гравець' }, [{ kind: 'move', a: '@a', dir: 'up' }], { note: 'так само ↓ ← →', claims: ['move-4dir'] }),
    'Гравець ходить стрілками на одну клітинку за раз', { needs: ['e1'] }),
  item('r2', 'rule', rule({ kind: 'contact', a: 'Гравець', b: 'Стіна' }, [{ kind: 'block' }], { claims: ['impassable-cells'] }), 'Є стіни, через них не пройти', { needs: ['e1'] }),
  item('r3', 'rule', rule({ kind: 'enter', a: 'Гравець', b: 'Ключ' }, [{ kind: 'disappear', a: '@b' }, { kind: 'counter', name: 'ключів', n: 1 },
    { kind: 'set_state', a: 'Двері', s: 'відчинені' }], { claims: ['key-and-door'] }), 'наступив на ключ — він зникає, і відчиняються двері', { needs: ['e1', 'e3', 'e4'] }),
  item('r4', 'rule', rule({ kind: 'all_gone', a: 'Ключ' }, [{ kind: 'set_state', a: 'Вихід', s: 'відчинений' }]), 'Коли зібрав усі ключі, відкривається вихід', { needs: ['e3', 'e5'] }),
  item('r5', 'rule', rule({ kind: 'enter', a: 'Гравець', b: 'Вихід' }, [{ kind: 'win' }, { kind: 'window', window: 'Перемога' }],
    { cond: [{ kind: 'state', a: '@b', s: 'відчинений' }], claims: ['reach-exit'] }), 'зайшов у вихід — перемога, показується вікно «Перемога»', { needs: ['e1', 'e5', 'w3'] }),
  item('w1', 'window', { title: 'Головне меню', task: 'main-menu', items: [{ title: 'Грати', window: 'Гра' }, { title: 'Вийти' }] }, 'На старті головне меню: «Грати» і «Вийти»', { needs: ['w2'] }),
  item('w2', 'window', { title: 'Гра', task: 'game-screen', description: 'Лабіринт; збоку — скільки ключів зібрано', claims: ['goal-counter'] }, 'Збоку показую, скільки ключів зібрано'),
  item('w3', 'window', { title: 'Перемога', task: 'end-screen' }, 'показується вікно «Перемога»'),
  item('l1', 'level', { title: 'Лабіринт', description: 'Один лабіринт, намальований вручну', mode: 'hand', count: '1', size: '17×7' }, 'лабіринт один, малював сам'),
  item('u1', 'unknown', { why: 'це план, а не те, що вже є в грі, — додай, коли зробиш', candidates: ['fog-of-war', 'save-game'] },
    'Потім ще хочу зробити туман війни і, може, збереження'),
] })
const older = { id: 'm0', at: new Date(Date.now() - 864e5).toISOString(), text: 'Лабіринт зі стінами, підлога звичайна.', model: 'mock', cost: 0.004, error: '', items: [
  item('e1', 'entity', { title: 'Стіна', role: 'static' }, 'Лабіринт зі стінами', { state: 'added', made: 'entities' }),
  item('e2', 'entity', { title: 'Підлога', role: 'terrain' }, 'підлога звичайна', { state: 'rejected' }),
] }

const db = { mode: 'on', why: '', left_today: 8, left_total: 52, max_chars: 4000, drafts: [maze('m1'), older] }
let n = 1
const copy = (x) => JSON.parse(JSON.stringify(x))
const wait = (ms) => new Promise((r) => setTimeout(r, ms))
const draft = (id) => db.drafts.find((d) => d.id === id)
const fail = (message, status) => Object.assign(new Error(message), { status })
const SECTION = { field: 'field', entity: 'entities', rule: 'rules', window: 'windows', level: 'levels', claim: 'zone-game-logic' }  // «показати →» without real ids

export const mockApi = {
  get: async () => copy(db),
  async ask(text) {
    await wait(1500)
    if (/помилк/i.test(text)) throw fail('На сьогодні запити вичерпано — лишилось 0 з 10', 429)
    const d = maze(`m${++n}`, text)
    db.drafts.unshift(d)
    db.left_today--
    db.left_total--
    return copy(d)
  },
  async apply(id, keys) {  // the named ones and what they need, as the server does
    await wait(400)
    const d = draft(id)
    const all = new Set(keys.flatMap((k) => [k, ...(d.items.find((x) => x.key === k)?.needs || [])]))
    for (const it of d.items) if (all.has(it.key) && it.state !== 'exists') Object.assign(it, { state: 'added', made: SECTION[it.group] })
    return { draft: copy(d), added: {}, skipped: [] }
  },
  async state(id, keys, state) {
    await wait(200)
    for (const it of draft(id).items) if (keys.includes(it.key)) it.state = state
    return copy(draft(id))
  },
}
