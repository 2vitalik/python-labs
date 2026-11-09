---
title: Epaminondas (Епамінонд)
slug: epaminondas
aka: [Епамінонд, Crossings, Кросінгз]
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
year: 1975
platforms: [board, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Epaminondas_(game)", best: true, note: "фаланга, рух на довжину, правило взяття «коротша лінія», перемога на задньому ряду, правило симетрії"}
  - {kind: other, url: "https://jpneto.github.io/world_abstract_games/epaminondas.htm", note: "World of Abstract Games: 12×14, 28 каменів, рух уздовж фаланги, варіанти Heximondas / Force / Abanondas"}
  - {kind: play, url: "http://www.gamerz.net/pbmserv/epaminondas.html", note: "гра поштою (pbmserv), лінк з World of Abstract Games; не відкривав"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=Epaminondas", note: "пошук BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Epaminondas+board+game+Robert+Abbott", note: "пошук; як грати"}
stage: v1
coverage: 70
mechanics: [piece-move-patterns, piece-capture, move-8dir, legal-move-highlight, selection-highlight, last-move-highlight, multi-select, hot-seat, turn-enforcement, move-timer, ai-opponent, ai-minimax, cell-click, hover-highlight, drag-drop-piece, move-notation, replay, game-screen, main-menu, end-screen, help-window, settings-window, state-as-data, unit-tests, +group-move, +phalanx-length-move, +outnumber-line-capture, +back-row-majority-win, +delayed-win-check, +symmetry-rule]
proposes: ["+cond:outnumbers", "+cond:phalanx", "+effect:move_group", "+effect:capture_line", "+trigger:back_row_majority", "+cond:mirror_symmetric", "+ui:phalanx-selection", "+ui:back-row-counter", "+card:phalanx-length-move", "+card:outnumber-line-capture", "+card:back-row-majority-win", "+card:delayed-win-check"]
author: opus
date: 2026-11-09
---

# Epaminondas — фаланга каменів іде вздовж себе на свою довжину і бʼє коротшу ворожу лінію

## Суть
Двоє з великими арміями однакових каменів намагаються прорватись на задній ряд суперника. Камені в лінію (фаланга) рухаються разом уздовж цієї лінії на відстань до своєї довжини; голова фаланги може вдарити ворожу лінію на тому ж напрямку, якщо та коротша, — і вся вона знята. Перемога — коли на початку твого ходу на задньому ряду суперника твоїх каменів більше, ніж його на твоєму: тобто прорив треба втримати один хід. Robert Abbott, 1975; перше видання — «Crossings» у Sid Sackson «A Gamut of Games».

## Поле і час
- Квадратна дошка 12×14 (`field: square`), 8 напрямків (ортогоналі й діагоналі).
- Ряд, найближчий до гравця, — його «домашній»; ціль — домашній ряд суперника.
- Покроково, білі першими; один хід = рух одного каменя або однієї фаланги (чи її частини). Без випадковості.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Камінь | piece | сторона white/black; по 28 | одиночний — фаланга довжини 1: крок на 1 у 8 напрямках, як король |
| Фаланга | piece | довжина n ≥ 2, напрямок (горизонталь / вертикаль / діагональ) | суцільна лінія своїх без проміжків; рухається вздовж своєї лінії вперед/назад на 1..n |
| Частина фаланги | piece | k ≤ n суміжних каменів з кінця | може рушити окремо, не далі ніж на k |
| Голова фаланги | piece | перший камінь у напрямку руху | бʼє: стає на клітину першого взятого |
| Ворожа лінія | zone | m суміжних ворожих від точки удару | знімається цілком, якщо m < n |
| Домашній ряд | zone | крайній ряд кожного | «фініш» для суперника |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(select, stones)` → ЯКЩО `custom: «суцільна лінія своїх у одному з 4 напрямків»` (`+cond:phalanx`) → ТО фаланга обрана; камінь може входити в різні фаланги за різними напрямками.
- КОЛИ `input(move, phalanx, dist)` → ЯКЩО `custom: «рух уздовж лінії фаланги, вперед або назад, dist ≤ довжини»` → ТО `custom: «зсунути всю фалангу на dist»` (`+effect:move_group`); боком — `block`.
- КОЛИ `input(move, stone, dir)` (одиночний) → ЯКЩО `free(next)` → ТО `move(stone, dir)`.
- КОЛИ `input(move, phalanx, dist)` → ЯКЩО `occupied(path, own)` → ТО `block` — крізь свої не ходять.
- КОЛИ `input(move, phalanx, dist)` → ЯКЩО голова влучає в ворожий камінь і `custom: «ворожих підряд на цій лінії від точки удару менше, ніж каменів у фаланзі»` (`+cond:outnumbers`) → ТО `custom: «зняти всю цю ворожу лінію, голова стає на місце першого взятого»` (`+effect:capture_line`); рівні чи довші — `block`.
- Фаланга з n каменів бере не більше n−1; одиночний камінь не бʼє ніколи; взяття не обовʼязкове.
- КОЛИ `input(move, phalanx, dist)` → ЯКЩО на шляху ворожий камінь до кінця дистанції → ТО рух закінчується ударом або `block` (крізь ворожі теж не проходять) (?).
- КОЛИ `input(move, stone, home_row_opponent)` → ЯКЩО `custom: «після ходу позиція дзеркально-симетрична зліва направо»` (`+cond:mirror_symmetric`) → ТО `block` (правило симетрії, за Wikipedia).
- КОЛИ `turn_start(side)` → ЯКЩО `custom: «моїх на домашньому ряду суперника строго більше, ніж його — на моєму»` (`+trigger:back_row_majority`) → ТО `win`.
- Перевірка — на **початку** свого ходу: суперник має один хід, щоб збити прорив або прорватися сам.
- Перемога: більшість на чужому задньому ряду на початку свого ходу · Поразка: дзеркально · Рахунок: нема.

## Керування і ввід
- Настільна: пересунути один камінь або кілька в лінію разом.
- (цифрова версія) Клік по каменю → вибір напрямку лінії (фаланга підсвічується за напрямком) → розширити/звузити виділення з кінця (частина фаланги) → клік по цільовій клітині на лінії; ціль удару підсвічена червоним із числом взятих.
- Неоднозначність «який із 4 напрямків фаланги» — головна задача інтерфейсу: drag від хвоста до цілі задає і фалангу, і напрямок.

## Вікна, меню, HUD
- `main-menu` (цифрова версія): Грати проти людини / AI → `match-setup` (колір, годинник, правило симетрії увімк/вимк).
- `game-screen`: дошка 12×14, `turn-indicator`, `phalanx-selection`, `legal-move-highlight` (клітини 1..n уздовж лінії), `threat-range` (ворожі лінії, які можна взяти), `back-row-counter` (мої на чужому ряду vs його на моєму), `captured-pieces`, `last-move-highlight`, `move-list`.
- `end-screen`: прорив задніх рядів.
- `help-window`: правила фаланги з діаграмами.
- Переходи: main-menu → match-setup → game-screen → end-screen.

## Фічі поза полем
- Гра поштою (pbmserv на gamerz.net), ZRF для Zillions of Games — за World of Abstract Games.
- `custom-rules`: правило симетрії, розмір дошки (Crossings 8×8).
- Сучасної популярної цифрової версії не знайдено (?).

## Варіації й родичі
- **Crossings** — перша версія на 8×8 з іншими правилами взяття.
- **Heximondas** (Keith Carter, 2002) — гекс-поле.
- **Force** (Chris Huntoon, 2000) — камені промотуються на останньому ряду; мета — лишити суперника з менш ніж 2 каменями або промотувати 2 свої.
- **Abanondas** (João Neto, Bill Taylor, 2006) — суміш з [abalone](abalone.md): фаланга може зробити бічний крок на 1 у порожні.
- Родичі в корпусі: [abalone](abalone.md) (колона + перевага сил «3>2»), [breakthrough-loa](breakthrough-loa.md) (прорив на задній ряд; LOA — дальність = кількість на лінії), [dvonn](dvonn.md) (дальність = висота стосу).
- Осі варіацій: **дальність** (до довжини / рівно довжина) · **взяття** (коротша лінія / одна фішка / виштовхування) · **ціль** (більшість на ряду з затримкою / перший, хто дійшов) · **рух** (лише вздовж / ще й боком).

## Цікавинки для курсу
- Перелік фаланг: для кожного каменя 4 напрямки, суцільні відрізки, частини з кінця — 📎.
- Генерація ходів «уздовж на 1..n, крізь свої не можна» + удар з підрахунком ворожої лінії — 🥉.
- Перемога з затримкою на один хід (перевірка на початку ходу) — 🌱, але вчить різниці «стан після ходу» vs «стан перед ходом».
- Правило симетрії (дзеркальна позиція заборонена) — 📎.
- UI вибору фаланги й частини (drag хвіст → ціль) — 🥉.
- AI: великий фактор розгалуження (28 каменів × 4 лінії × довжини) — minimax з відсіканням — 🥇.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ рух каменя/фаланги · `piece-capture` ↔ удар голови · `move-8dir` ↔ одиночний камінь · `multi-select` ↔ вибір фаланги · `legal-move-highlight`, `selection-highlight`, `last-move-highlight` · `hot-seat`, `turn-enforcement`, `move-timer` · `ai-opponent`, `ai-minimax` · `cell-click`, `hover-highlight`, `drag-drop-piece` · `move-notation`, `replay`, `state-as-data`, `unit-tests` · `game-screen`, `main-menu`, `end-screen`, `help-window`, `settings-window`.
- **Нема** → пропозиції карток:
  - `+group-move` (див. abalone.md) — хід групою.
  - `+phalanx-length-move` «Лінія рухається вздовж себе на свою довжину» · entities/move · 📎 — дитина `group-move`.
  - `+outnumber-line-capture` «Взяття коротшої ворожої лінії» · entities/combat · 📎 — родич `majority-push` (abalone.md).
  - `+back-row-majority-win` «Більшість на задньому ряду суперника» · game-logic/win · 🌱.
  - `+delayed-win-check` «Перемога перевіряється на початку свого ходу» · game-logic/win · 🌱.
  - `+symmetry-rule` «Заборона дзеркальної позиції» · entities/legality · 📎.

## Пропозиції до словників
- `+cond:outnumbers` — своїх у лінії більше, ніж ворожих підряд (див. abalone.md).
- `+cond:phalanx` — обрані камені — суцільна лінія в одному напрямку.
- `+effect:move_group` — зсунути групу одним ходом (див. abalone.md).
- `+effect:capture_line` — зняти суцільну лінію ворожих від точки удару.
- `+trigger:back_row_majority` — на початку ходу більшість на чужому домашньому ряду.
- `+cond:mirror_symmetric` — позиція дзеркально-симетрична.
- `+ui:phalanx-selection` — виділення фаланги з напрямком; `+ui:back-row-counter` — лічильник проривів.
- `+card:phalanx-length-move`, `+card:outnumber-line-capture`, `+card:back-row-majority-win`, `+card:delayed-win-check` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Epaminondas](https://en.wikipedia.org/wiki/Epaminondas_(game)) — фаланга, рух частини, взяття «ворожих від точки удару менше», n−1, правило симетрії, перемога на початку ходу, Crossings, Games 100 (1980).
- [World of Abstract Games: Epaminondas](https://jpneto.github.io/world_abstract_games/epaminondas.htm) — 12×14, 28+28 (плюс запасні), рух уздовж лінії вперед/назад, варіанти і лінки на ZRF/pbmserv.

## Непевне
- (?) Орієнтація 12×14 і стартова розстановка: 28 каменів = мабуть, два крайні ряди по 14, тобто ряд має 14 клітин; діаграми не бачив.
- (?) Чи може фаланга пройти крізь ворожий камінь без удару — прямо не сказано; логічно — ні (удар або `block`).
- (?) Правило симетрії є у Wikipedia, але не згадане в World of Abstract Games — можливо, необовʼязкове.
- (?) Як саме виглядала версія Crossings (правила взяття) — лише «інші правила взяття».
- (?) Лінк pbmserv не відкривав; чи живий — невідомо.
