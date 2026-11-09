---
title: Jungle (Dou Shou Qi, «Джунглі», звірині шахи)
slug: jungle
aka: [Dou Shou Qi, Dou Shou Ch'i, 斗兽棋, 鬥獸棋, Animal chess, Jungle King, Джунглі, Звірині шахи]
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: state
year: 1950
platforms: [board, web, mobile]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Jungle_(board_game)", best: true, note: "дошка 7×9, барліг, пастки, річки, 8 тварин за рангом, щур і слон, стрибки лева/тигра, варіанти"}
  - {kind: other, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=jungle+dou+shou+qi", note: "пошук BGG (не відкривав)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=jungle+dou+shou+qi+rules", note: "пошук; правила"}
stage: v1
coverage: 70
mechanics: [piece-move-patterns, piece-capture, legal-move-highlight, floor-types, hot-seat, turn-enforcement, ai-opponent, ai-minimax, cell-click, drag-drop-piece, last-move-highlight, game-screen, main-menu, end-screen, help-window, rule-variants, state-as-data, unit-tests, +reach-row-win, +trap-squares, +rank-capture, +weakest-beats-strongest, +terrain-restricted-piece, +river-jump, +own-den-forbidden, +capture-count-win]
proposes: ["+cond:stronger", "+cond:in_zone", "+effect:jump_capture", "+card:rank-capture", "+card:weakest-beats-strongest", "+card:terrain-restricted-piece", "+card:river-jump", "+card:own-den-forbidden", "+ui:rank-badge", "+ui:trap-marker", "+window:variant-select"]
author: opus
date: 2026-11-09
---

# Jungle — шахи з тваринами, де сильніший їсть слабшого, а щур — слона

## Суть
Двоє гравців мають по вісім тварин з рангами 1–8 (щур → слон) і ходять ними на одну клітину ортогонально. Тварина бʼє рівну або слабшу — **крім пари щур/слон**: найслабший щур бʼє найсильнішого слона. Поле не однорідне: дві **річки** (лише щур плаває, лев і тигр перестрибують), **пастки** біля барлогу (у ворожій пастці будь-яка тварина стає рангу 0) і **барліг** — мета: зайти туди будь-якою твариною.

## Поле і час
- Дошка 7 стовпців × 9 рядів, ходять по клітинах.
- У центрі першого ряду кожної сторони — **барліг** (den); три клітини довкола нього — **пастки**.
- У центрі дошки — дві **річки** 2×3 (вода), розділені сушею.
- Покроково; синій ходить першим; пропускати хід не можна.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Слон | piece | ранг 8 | бʼє будь-кого рангом ≤ 8; у поширеному варіанті — не бʼє щура (див. «Непевне») |
| Лев | piece | ранг 7 | крок 1; стрибок через річку вертикально й горизонтально |
| Тигр | piece | ранг 6 | крок 1; стрибок через річку вертикально (у багатьох правилах — і горизонтально) |
| Леопард | piece | ранг 5 | крок 1 |
| Вовк | piece | ранг 4 | крок 1 (у варіанті — лисиця) |
| Пес | piece | ранг 3 | крок 1 |
| Кіт | piece | ранг 2 | крок 1 |
| Щур | piece | ранг 1 | крок 1; єдиний заходить у воду; бʼє слона з суші; у воді недосяжний для сухопутних |
| Річка | terrain | 2 області 2×3 | вхід лише щуру; блокує стрибки, якщо в ній будь-який щур на лінії |
| Пастка | terrain | 3 біля кожного барлогу | ворожа тварина в ній має ранг 0; власник ходить через неї вільно |
| Барліг | zone | 1 на сторону | свій — заборонений; ворожий — вхід = перемога |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, animal, to)` → ЯКЩО `turn_of(side)` і `custom: «to — сусідня ортогональна клітина»` → ТО `move(animal, to)`, `end_turn`; хід обовʼязковий.
- КОЛИ `input(move, animal, to)` → ЯКЩО `cell(to, water)` і `not same(animal, rat, kind)` → ТО `block`.
- КОЛИ `input(move, animal, to)` → ЯКЩО `cell(to, own_den)` → ТО `block`.
- КОЛИ `input(move, animal, to)` → ЯКЩО `occupied(to, enemy)` і `custom: «ранг animal ≥ рангу ворога»` (`+cond:stronger`) → ТО `move`, `disappear_b`; інакше `block`.
- КОЛИ `input(move, rat, to)` → ЯКЩО `occupied(to, enemy_elephant)` і `not cell(from, water)` → ТО `disappear_b` — щур бʼє слона лише з суші.
- КОЛИ `input(move, elephant, to)` → ЯКЩО `occupied(to, enemy_rat)` → ТО `block` у поширеному варіанті (див. «Непевне»).
- КОЛИ `input(move, land_animal, to)` → ЯКЩО `occupied(to, enemy_rat)` і `cell(to, water)` → ТО `block`; щура у воді бʼє лише інший щур у воді.
- КОЛИ `input(jump, lion|tiger, across_river)` → ЯКЩО `custom: «на шляху у воді нема жодного щура»` → ТО `move(animal, first_land_cell)`; ЯКЩО там ворог з рангом ≤ → `disappear_b` (`+effect:jump_capture`); інакше `block`.
- КОЛИ `enter(animal, enemy_trap)` → ТО `set_state(animal, rank_0)` — будь-який ворог може її взяти.
- КОЛИ `leave(animal, enemy_trap)` → ТО `clear_state(animal, rank_0)`.
- КОЛИ `enter(animal, enemy_den)` → ТО `win`.
- КОЛИ `all_gone(enemy_animals)` → ТО `win`.
- Перемога: зайти у ворожий барліг · зʼїсти всіх тварин. Поразка — те саме навпаки. Рахунку нема.

## Керування і ввід
- (цифрова версія) Клік по тварині → підсвітка легальних клітин (з урахуванням води, барлогу, рангу на цілі, стрибків) → клік по цілі; або drag.
- Рангові цифри або піктограми на фішках; у паперових наборах — малюнок тварини з числом.

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Проти AI · З другом (hot-seat) · Правила → `help-window` · Налаштування (варіанти правил).
- `game-screen`: дошка з водою, пастками й барлогами, `turn-indicator`, `rank-badge` на кожній фігурі, `captured-pieces`, `last-move-highlight`, `legal-move-highlight`, `trap-marker` (пастка + знижений ранг).
- `settings-window` / `variant-select`: слон бʼє щура чи ні · тигр стрибає горизонтально · рівні лев і тигр · універсальні пастки · пес у воді · приховані фішки.
- `end-screen`: «барліг захоплено» / «усі тварини зʼїдені».
- Переходи: main-menu → game-screen → end-screen → реванш.

## Фічі поза полем
- `custom-rules` — перемикачі численних регіональних варіантів (див. нижче).
- `ai-opponent-levels`, `hotseat`, `rules-page`.
- Режим з прихованими фішками (ранги не видно супернику) — гра стає з частковою інформацією.

## Варіації й родичі
- **Варіанти** (Wikipedia): слон не бʼє щура · лев і тигр рівні або тигр сильніший · леопард стрибає лише горизонтально · пастки універсальні (свої теж) · лисиця замість вовка · без горизонтального стрибка лева · обмеження, хто з малих заходить у пастки · пес плаває · фішки приховані.
- **Animal checkers** — спрощена версія без пасток і річок, 4 фігури.
- **Jungle King** (Waddington, Британія, 1960-ті) — комерційне видання.
- Родичі: Stratego-подібні ігри з рангами й «слабкий бʼє найсильнішого» (шпигун/маршал) — прихований варіант Jungle майже Stratego; ієрархія рангів у [arimaa](arimaa.md) (сильніший штовхає слабшого); стрибуни-генерали за рангом у [large-shogi-variants](large-shogi-variants.md); мета «зайти в клітину» — як у [breakthrough-loa](breakthrough-loa.md).
- **Осі варіацій**: ієрархія (лінійна / циклічна щур>слон) · рельєф (вода / пастки / нема) · стрибки (хто, у яких напрямках) · видимість (відкрито / приховані фішки) · мета (барліг / усіх зʼїсти).

## Цікавинки для курсу
- Ранг як число + виняток-цикл «1 бʼє 8» — 🌱 (класична задача на `if` з винятками).
- Тип клітини змінює можливості фігури: вода лише щуру, пастка обнуляє ранг, свій барліг заборонений — 📎.
- Стрибок через річку, що блокується щуром у воді (перевірка всіх клітин шляху) — 📎.
- Щур у воді невразливий для сухопутних, але не для щура у воді — 🌱.
- Конструктор варіантів правил з 8–10 перемикачами — 🥉.
- AI minimax для невеликої дошки 7×9 — 🥈.

## Мапа на каталог
- Є: `piece-move-patterns` · `piece-capture` · `legal-move-highlight` · `floor-types` ↔ вода/пастка/барліг · `hot-seat`, `turn-enforcement`, `ai-opponent`, `ai-minimax` · `cell-click`, `drag-drop-piece`, `last-move-highlight` · `game-screen`, `main-menu`, `end-screen`, `help-window` · `rule-variants` ↔ варіанти · `state-as-data`, `unit-tests`.
- **Нема** → пропозиції карток:
  - `+reach-row-win` (є в сімʼї) — тут клітина-барліг.
  - `+trap-squares` (є в сімʼї, Arimaa) — тут не знищує, а обнуляє ранг.
  - `+capture-count-win` (є в сімʼї) — зʼїсти всіх.
  - `+rank-capture` «Бити рівного чи слабшого за рангом» · entities/combat · 🌱 · слоти {ranks, ties}.
  - `+weakest-beats-strongest` «Циклічний виняток ієрархії» · entities/combat · 🌱 · слоти {pair, condition}.
  - `+terrain-restricted-piece` «Клітини, доступні лише певному типу фігур» · entities/legality · 🌱.
  - `+river-jump` «Стрибок через область, який блокує фігура в ній» · entities/move · 📎.
  - `+own-den-forbidden` «Своя клітина-ціль заборонена для власних фігур» · entities/legality · 🌱.

## Пропозиції до словників
- `+cond:stronger` — ранг A ≥ рангу B (підтверджую arimaa.md; тут з винятком щур/слон і рангом 0 у пастці).
- `+cond:in_zone` — підтверджую (у ворожій пастці / барлозі).
- `+effect:jump_capture` — стрибок із взяттям на клітині приземлення (є в пропозиціях сімʼї; тут — стрибок через річку).
- `+ui:rank-badge` — число рангу на фігурі (Jungle, Stratego).
- `+ui:trap-marker`, `+window:variant-select` — підтверджую (arimaa.md, lichess-variants.md).
- `+card:rank-capture`, `+card:weakest-beats-strongest`, `+card:terrain-restricted-piece`, `+card:river-jump`, `+card:own-den-forbidden` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Jungle (board game)](https://en.wikipedia.org/wiki/Jungle_(board_game)) — дошка 7×9, барліг і три пастки, дві річки 2×3, ранги 8…1, ходи, взяття, щур/слон, стрибки лева й тигра, блок щуром, ранг 0 у пастці, дві умови перемоги, варіанти, Animal checkers, Jungle King.
- BGG / YouTube — пошукові сторінки.

## Непевне
- (?) Чи слон у класичних правилах бʼє щура: стаття подає «слон не бʼє щура» як поширений варіант, а базове правило (рівний чи слабший) формально дозволяє; у таблиці лишаю обидва.
- (?) Правила нічиєї і що робити, коли нема легальних ходів, — стаття не описує.
- (?) `year: 1950` — умовно: китайське походження погано задокументоване, Jungle King — 1950-ті/1960-ті.
- (?) Чи може щур виходити з води прямо на взяття іншої фігури (не слона) — за загальним правилом так, окремо не підтверджено.
- (?) Онлайн-сервери та застосунки — не відкривав.
