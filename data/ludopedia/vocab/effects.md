# Ефекти — ТО

Словник `EFFECTS` у коді (`models/rule.py`): ✅ є · ⏳ кандидат. У правилі може бути кілька ефектів; `custom: «текст»` — легально, але дублюй у «Пропозиції до словників».

## ✅ У коді (15)

- `disappear_a` · `disappear_b` · `disappear_both` — зникає.
- `block` — рух не відбувається.
- `push` — B зсувається у напрямку руху A.
- `pickup` — B переходить в інвентар/лічильник A.
- `teleport` — A переноситься (на пару/випадково).
- `damage(n)` — шкода N HP.
- `score(n)` — ±N очок.
- `spawn(entity)` — зʼявляється сутність.
- `transform(entity)` — перетворюється на іншу сутність.
- `window(window)` — відкрити вікно.
- `win` · `lose`.
- `custom(text)`.

## ⏳ Кандидати

Рух і положення:
- `move(a, dir|to)` — перемістити на 1 / у клітину.
- `slide(a, dir)` — ковзати до упору (Inertia, Pengo).
- `pull(b)` — B тягнеться за A.
- `swap(a, b)` — обмінятись місцями/значеннями.
- `rotate(a, deg)` — повернути сутність/плитку/поле.
- `fall(a)` — падає, доки є порожнє під.
- `bounce(a)` — відбивається (змінює напрямок на протилежний/дзеркальний).
- `wrap(a)` — переходить на протилежний край (тор).
- `shift(row|col|all, dir)` — зсунути ряд/стовпець/усе поле (2048, Sixteen).
- `drop_rows` / `collapse` — осідання після зникнення.
- `attach(a, b)` / `detach(a, b)` — зчепити/розчепити (Sokobond, тіло змійки).
- `face(a, dir)` — змінити орієнтацію без руху.

Стан сутності:
- `hp(a, ±n)` · `lives(±n)` · `heal(a, n)`.
- `set_state(a, s, duration?)` / `clear_state(a, s)` — увімкнути/зняти стан (щит, переляк, стан на N тіків).
- `speed(a, ±n|×k)` · `freeze(a, n)` · `stun(a, n)`.
- `grow(a, n)` / `shrink(a, n)` — довжина/розмір (змійка, сніжка).
- `set_value(a, v)` / `merge(a, b → c)` — значення плитки, злиття двох в одну.
- `clone(a)` / `split(a)`.
- `set_side(a, side)` — зміна власника (Reversi-перевертання, захват).
- `invert_controls(n)` · `mirror_input`.

Клітини і поле:
- `set_cell(cell, type)` — змінити тип клітини (дірка → підлога, трава → земля).
- `mark(cell, value)` / `unmark(cell)` — розмітка (пазли, прапорці).
- `reveal(cells)` / `hide(cells)` — відкрити/закрити (туман, сапер, каскад нулів).
- `paint(cell, color)` — зафарбувати (Q*bert, Xonix, територія).
- `fill(region)` — заливка замкненої області.
- `clear(cells)` — очистити лінію/групу (Tetris, match-3).
- `spawn_at(entity, where)` — спавн у вказаному місці (край, точка спавну, випадково).
- `shake` / `flash` / `sound(x)` / `message(text)` / `animate(x)` — зворотний звʼязок.
- `camera(x)` — рух/зум камери.

Економіка, лічильники, час:
- `currency(±n)` · `give(a, item)` · `take(a, item)` · `counter(name, ±n)`.
- `multiplier(×k)` · `combo(+1)` · `reset_combo`.
- `timer(start|stop|±n)` · `extra_move` · `end_turn` · `pass_turn` · `skip_turn(a)`.
- `unlock(x)` · `checkpoint` · `undo_point`.

Хід гри:
- `next_level` · `restart` · `respawn(a, where)` · `game_over` · `draw` (нічия).
- `trigger(rule)` — запустити інше правило (ланцюг).
- `choose(options)` — гравець обирає з варіантів (вікно вибору апгрейда).

## 🔥 Підтверджено корпусом (2026-11-02, 114 ігор)

`set_state` ×15 · `move` ×13 · `set_cell` ×12 · `place` ×10 (нове: гравець кладе з запасу/руки — не `spawn_at`) · `rotate` ×10 · `fall` ×9 · `counter` ×8 · `slide` ×8 · `spawn_at` ×8 · `reveal` ×7 · `take` ×6 · `transform` ×6 · `speed` ×5 · `explode(area, into?)` ×5 (нове: вибух з формою й продуктом) · `roll` ×5 (нове: скочується з округлого) · `mark` ×5 · `shift` ×4 · `wrap` ×4 · `face` ×4 · `lives` ×4 · `send_garbage` ×4 (нове: сміття супернику) · `clear` ×4 · `feedback(guess)` ×4 (нове: відгук на спробу — Wordle/Mastermind) · `hp` · `heal` · `choose` · `give` · `stun` · `timer` · `merge` · `swap` · `throw` · `message` · `carry` (нове: везти на собі) · `set_value` · `crash` (нове: аварія програми) · `pull` ×3. Рішення — [analysis/01-vocab-harvest.md](../analysis/01-vocab-harvest.md).
