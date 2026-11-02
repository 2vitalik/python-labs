# Тригери — КОЛИ

Словник `TRIGGERS` у коді (`models/rule.py`): ✅ є · ⏳ кандидат. Запис у правилі: `name(args)`. Правило трьох: ⏳ стає ✅, коли зустрілось у ≥3 іграх корпусу (див. `index/proposals.md`).

## ✅ У коді

- `contact(a, b)` — A наступає на / стикається з B (клітина спільна або A входить у клітину B).
- `timer(every)` — кожні N тіків / секунд.

## ⏳ Кандидати

Ввід і хід:
- `input(action)` — гравець виконав дію (клавіша, клік по клітині, свайп, drag).
- `turn_start(side)` / `turn_end(side)` — початок/кінець ходу сторони.
- `tick` — кожен тік (для real-time правил без періоду).
- `idle(n)` — гравець не діє N тіків.

Простір:
- `enter(a, cell_type)` / `leave(a, cell_type)` — сутність стала на / зійшла з клітини типу.
- `adjacent(a, b)` — опинились у сусідніх клітинах (без спільної клітини); варіант `adjacent8`.
- `line_of_sight(a, b)` — B на одній лінії з A без перешкод (стріляє, коли бачить).
- `in_range(a, b, n)` — відстань ≤ N.
- `reach(a, where)` — A досяг краю / рядка / зони / точки.
- `edge(a)` — вихід за межу поля.
- `blocked(a)` — рух неможливий (упор у стіну).

Стан і лічильники:
- `counter(name, op, n)` — лічильник досяг (очки ≥ N, зібрано = квота, довжина = N).
- `hp_zero(a)` — HP сутності вичерпано.
- `state_on(a, s)` / `state_off(a, s)` — сутність увійшла в / вийшла зі стану (переляк, щит).
- `all_gone(kind)` — зникли всі сутності виду (усі вороги, усі точки).
- `all_on(kind, target)` — усі сутності виду на цілях.
- `no_moves(side)` — нема легальних ходів.
- `pattern(shape)` — на полі склався шаблон: `line(n)`, `group(n)`, `row_full`, `region_closed`, `loop_closed`, `match(color, n)`.
- `constraint_broken(c)` / `all_constraints_met` — порушено / виконано обмеження (пазли).

Життєвий цикл:
- `level_start` / `level_end` · `wave_start` / `wave_cleared` · `game_start` / `game_over`.
- `spawned(a)` / `died(a)` / `picked(a, item)` / `destroyed(a)` — подія іншої сутності (ланцюги правил).
- `after(rule|effect)` — одразу після іншого ефекту (каскад).
- `rng(p)` — випадково з ймовірністю p (на тік / на подію).
- `schedule(list)` — за розкладом (хвилі: тік 100, 250, 400…).

## 🔥 Підтверджено корпусом (2026-11-02, 114 ігор)

`input` ×33 · `counter` ×12 · `pattern` ×9 · `enter` ×6 · `all_constraints_met` ×6 · `settled` ×6 (нове: поле стабілізувалось) · `turn_end` ×4 · `repetition` ×4 (нове: позиція повторилась) · `line_of_sight` ×4 · `blocked` ×4 · `constraint_broken` ×4 · `exec(cmd)` ×4 (нове: програма виконує команду) · `check` ×3 (нове: король під ударом) · `locked` ×3 (нове: фігура зафіксувалась) · `program_end` ×3 · `phase_start` ×3 (нове: фаза тіку). Рішення — [analysis/01-vocab-harvest.md](../analysis/01-vocab-harvest.md).
