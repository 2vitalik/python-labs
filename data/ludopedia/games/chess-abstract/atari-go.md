---
title: Atari Go (Capture Go, го до першого взяття)
slug: atari-go
aka: [Capture Go, First Capture Go, Capture Game, Атарі-ґо]
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: race
year: —
platforms: [board, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Capture_Go", best: true, note: "правила: го, але перемога першим взяттям (або N камінців); автор Ясуда Ясутосі"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Go_variants", note: "розділ Capture Go: «most capture» Ясуди, малі дошки"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=atari+go+capture+go+beginners", note: "пошук; навчальні партії"}
stage: v1
coverage: 60
mechanics: [piece-capture, turn-enforcement, hot-seat, ai-opponent, cell-click, hover-highlight, last-move-highlight, pass-turn, field-size-picker, game-screen, end-screen, +liberty-capture, +first-capture-win, +capture-quota]
proposes: ["+cond:liberties", "+effect:capture_group", "+card:first-capture-win", "+card:capture-quota"]
author: opus
date: 2026-11-09
---

# Atari Go — го, де виграє той, хто першим зняв камінь

## Суть
Навчальна варіація [го](go.md): усі правила ставлення каменів і захоплення груп без дихань ті самі, але партія закінчується **першим взяттям** (або коли хтось зняв заздалегідь домовлену кількість каменів). Нема підрахунку території, мертвих каменів, комі й ко-тонкощів наприкінці — лишається чисте ядро «дихання → атарі → взяття». Запропонував Ясуда Ясутосі (8 дан), який викладає го дітям; на Заході відома як Atari Go.

## Поле і час
- Та сама сітка ліній, камені на перетинах, 4-сусідство; для навчання — мала дошка (9×9 і менше (?)).
- Хід = поставити камінь на порожній пункт; чорні першими.
- Партія коротка: від кількох до кількох десятків ходів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Камінь чорний/білий | piece | колір | ставиться на порожній перетин, не рухається |
| Група | zone | звʼязні камені одного кольору | спільні дихання; 0 дихань → знімається |
| Дихання | — | лічильник групи | 1 → атарі (загроза взяття) |
| Лічильник взять | resource | на сторону | досяг квоти (типово 1) → перемога |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place(cell))` → ЯКЩО `turn_of(side)` and `free(cell)` → ТО `place(side, stone)`, `end_turn`.
- КОЛИ `after(place)` → для кожної ворожої групи-сусіда ЯКЩО `custom: «0 дихань»` (`+cond:liberties`) → ТО `custom: «зняти групу»` (`+effect:capture_group`), `counter(captures[side], +size)`.
- КОЛИ `counter(captures[side], >=, quota)` → ТО `win` (quota = 1 у класичному варіанті; 2–3 — наступний крок навчання).
- Самогубство: свій камінь без дихань, що нічого не бере, — за правилами го (?) — у більшості навчальних наборів заборонено.
- Ко на практиці не виникає: перше взяття вже закінчує партію.
- «Most capture» (порада Ясуди): наступний етап — виграє той, хто зняв більше каменів (?) до кінця партії.
- Перемога: перше взяття / квота взять. Поразки за часом і нічиєї нема (?).

## Керування і ввід
- Клік по перетину — камінь; `hover-highlight` — привид каменя; `last-move-highlight` — маркер останнього каменя.

## Вікна, меню, HUD
- (цифрова версія)
- `match-setup`: розмір дошки, квота взять (1/2/3/N), людина/AI.
- `game-screen`: дошка, `turn-indicator`, лічильник взять обох сторін, підсвітка груп в атарі (навчальна підказка).
- `end-screen`: «чорні взяли першими», кнопка «ще партію» / «квота +1».

## Фічі поза полем
- `ai-opponent-levels`, `hotseat`, `custom-rules` (квота взять), `tutorial` (дихання, атарі, драбина, сітка).

## Варіації й родичі
- Батько — [го](go.md): Atari Go відрізає підрахунок і лишає лише захоплення.
- **Осі варіацій**: квота (1 / 2–3 / most capture) · розмір дошки · стартова позиція (порожня / хрест з 4 каменів у центрі (?)).
- Інші навчальні сходинки го: малі дошки 9×9 / 13×13, далі повні правила. Схожий «спрощувальний» прийом — [Hexapawn](hexapawn.md) для шахів.

## Цікавинки для курсу
- Ядро го без підрахунку: flood fill групи й дихань, зняття — 🥉 (той самий код, що для го, але гра закінчена).
- Підсвітка «група в атарі» як навчальний HUD — 📎.
- AI, що бачить драбину (ladder) на кілька ходів — 🥈.
- Розвʼязувач малих дошок (5×5 і менше) повним перебором — 🥇.

## Мапа на каталог
- Є: `piece-capture` (частково: тут оточенням) · `turn-enforcement`, `hot-seat`, `ai-opponent` · `cell-click`, `hover-highlight`, `last-move-highlight` · `pass-turn` (?) · `field-size-picker` · `game-screen`, `end-screen`.
- **Нема** → пропозиції карток:
  - `+liberty-capture` — див. go.md.
  - `+first-capture-win` «Перемога першим взяттям» · game-logic/win · 🌱.
  - `+capture-quota` «Перемога за квотою взять» · game-logic/win · 🌱 · слоти {quota}.

## Пропозиції до словників
- `+cond:liberties`, `+effect:capture_group` — підтверджую з go.md (у `vocab/` ще нема).
- `+card:first-capture-win`, `+card:capture-quota` — див. вище.

## Джерела
- ⭐ [Wikipedia: Capture Go](https://en.wikipedia.org/wiki/Capture_Go) — правила го, перемога «capturing one or more stones», квота домовлена наперед, 1 → 2–3 камені для новачків, Ясуда Ясутосі.
- [Wikipedia: Go variants](https://en.wikipedia.org/wiki/Go_variants) — «The first player to capture a stone wins»; «most capture» як наступний крок; 9×9 і 13×13 для новачків.
- Sensei's Library — 403; YouTube — пошук.

## Непевне
- (?) Розмір дошки для Atari Go (9×9 і менші) і стартова позиція «хрест» у центрі — з памʼяті; у відкритих джерелах не названі.
- (?) Чи пас дозволений і що, якщо ніхто не може взяти (на малій дошці — рідко).
- (?) Правило самогубства в навчальних наборах.
- (?) Як саме визначається переможець у «most capture» (до кінця партії? до N ходів?).
- Веб-пошук сесії вичерпано.
