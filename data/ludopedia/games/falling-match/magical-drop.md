---
title: Magical Drop (Chain Reaction)
slug: magical-drop
family: falling-match
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: survive
year: 1995
platforms: [arcade (Neo Geo MVS), Super Famicom, Saturn, PlayStation, WonderSwan, Neo Geo Pocket Color, Game Boy Color, Wii VC, iOS, Android, PC, Switch, PS4, Xbox One]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Magical_Drop_III", best: true, note: "найповніший опис правил серії: витягти/кинути, 3 у стовпці, ланцюги, кнопка додавання ряду"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Magical_Drop", note: "серія, походження від Drop-Drop (Russ Ltd), versus-атаки за персонажем"}
  - {kind: fandom, url: "https://strategywiki.org/wiki/Magical_Drop_III/Gameplay", note: "StrategyWiki: геймплей і спец-кульки (WebFetch — 403, бачено в пошуку)"}
  - {kind: official, url: "https://www.nintendo.com/games/detail/aca-neogeo-magical-drop-3-switch", note: "ACA NeoGeo Magical Drop III (Switch)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=magical+drop+iii+gameplay", note: "пошук; геймплей MD III"}
stage: v1
coverage: 65
mechanics: [keyboard-controls, move-by-input, progress-acceleration, ai-opponent, hot-seat, event-points, combo-multiplier, score-records, game-pause, end-screen, +column-grab-throw, +line-match-clear, +chain-reaction, +cascade-gravity, +garbage-attack, +ceiling-push, +wildcard-tile, +color-clear-special, +manual-row-add]
proposes: ["+trigger:input", "+trigger:pattern", "+trigger:settled", "+trigger:timer", "+cond:same", "+cond:has", "+effect:pickup", "+effect:clear", "+effect:shift", "+effect:send_garbage", "+role:tile", "+ui:action-text", "+ui:held-stack", "+window:character-select", "+feature:mode-puzzle", "+axis:gravity", "+axis:control"]
author: opus
date: 2026-11-02
---

# Magical Drop — витягни кульки з низу стовпця й кинь в інший; 3 однакові в стовпці лопаються

## Суть
Стовпці кольорових кульок звисають зі стелі й повільно опускаються. Персонаж-клоун унизу ходить між стовпцями: одна кнопка **витягує** нижній ряд однакових кульок стовпця «в руки», друга **кидає** їх назад угору в стовпець, під яким він стоїть. Якщо в стовпці виходить 3+ однакових підряд по вертикалі — вони лопаються, кульки нижче піднімаються вгору, і можуть зібратись нові збіги (ланцюг). Гра — дуель на виживання: ланцюги прискорюють опускання стеку суперника.

## Поле і час
- Поле — сітка стовпців (≈ 6–7 у versus, більше у соло (?)) × висота до лінії клоуна; кульки «висять» від стелі, тобто **гравітація вгору**: дірки закриваються підйомом нижніх кульок.
- Real-time: стек періодично зсувається вниз на ряд (новий ряд додається зверху), темп росте. Поразка — коли кулька досягає нижньої межі.
- Ланцюг рахується і як каскад (підйом → новий збіг), і як швидка серія окремих збігів за короткий час (?).
- Versus: два поля поруч; суперник — CPU-персонаж або другий гравець.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клоун (персонаж) | player | стовпець, «руки»: колір + кількість | ходить ←/→ по стовпцях; тримає довільну кількість кульок одного кольору |
| Кулька (drop) | tile | колір (4 базові) | висить у стовпці; витягується разом з однаковими під нею; 3+ вертикально → лопається |
| Спец-кулька (зірка/special) | tile | колір | при лопанні знищує всі кульки свого кольору на полі (?) |
| Райдужна кулька | tile | wildcard | підходить до будь-якого кольору (versus) (?) |
| Лід-кулька | hazard | — | заморожена; розморожується, коли поруч лопається група (?) |
| «Масть» (suit) кулька | tile | символ карти | особлива поведінка у versus (?) |
| Бомба | hazard | — | у пазл/соло-режимах (?) |
| Стеля-генератор | spawner | темп | щоперіоду штовхає новий ряд зверху — весь стек опускається |
| Лінія поразки | static | нижній ряд | кулька тут → програш |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ТО `move(clown, column±1)`.
- КОЛИ `input(grab)` → ЯКЩО руки порожні або `same(hand, bottom_drop, color)` → ТО `pickup(run)` — нижня кулька стовпця і всі однакові підряд над нею; інакше `block`. Можна набрати з кількох стовпців.
- КОЛИ `input(throw)` → ЯКЩО `has(clown, drops)` → ТО `custom: «push — усі кульки з рук кладуться під низ поточного стовпця»`.
- КОЛИ `after(throw)` → ЯКЩО `pattern(line(3+, same_color, vertical))`, що включає кинуті → ТО `clear(line)`; разом лопаються й звʼязані з групою однакові кульки (?) — `score(+n)`.
- КОЛИ `after(clear)` → ТО `custom: «fall up — кульки нижче піднімаються до стелі/опори»`; ЯКЩО новий `pattern(line(3+))` → ТО `clear`, `combo(+1)` (ланцюг).
- КОЛИ `custom: «кілька збігів швидко підряд»` → ТО `combo(+1)` — ланцюг за темпом (?).
- КОЛИ `timer(push_interval)` → ТО `custom: «shift(all, down) — новий ряд зверху»`; інтервал скорочується з часом (`progress-acceleration`).
- КОЛИ `input(add_row)` (3-тя кнопка, MD III) → ТО одразу `custom: «shift(all, down)»` — гравець сам прискорює стек (більше кульок для ланцюгів).
- Versus: КОЛИ `after(chain)` → ТО `custom: «send_garbage — стек суперника опускається швидше; кожен персонаж надсилає ряди своїм нерівним візерунком»` — перемішує кольори суперника.
- КОЛИ `custom: «кулька в лінії поразки»` → ТО `lose`; суперник — `win` раунду.
- Перемога: versus — суперник програв (матч з кількох раундів (?)); соло-Endless — рахунок до поразки; Puzzle — очистити задане поле (?).
- Рахунок: за кожну лопнуту кульку, множник за довжину ланцюга і за великі групи.

## Керування і ввід
- ←/→ — клоун між стовпцями; кнопка A — витягти (pull), B — кинути (push); C (MD III) — додати ряд.
- Ввід принципово інший, ніж у Tetris/Puyo: гравець не керує падаючою фігурою, а **переносить** вже наявні кульки між стовпцями; «рука» — стек одного кольору довільної висоти.
- Швидкість — ключ: досвідчені гравці роблять серії pull/push за долі секунди.

## Вікна, меню, HUD
- `splash-screen` → `main-menu`: 1P (проти CPU, «таро»-персонажі) · VS · Endless · Puzzle · Options (?).
- `+window:character-select` — вибір персонажа (у кожного свій візерунок атаки); у MD III — 24–26 персонажів-арканів таро.
- `game-screen`: два поля (versus) або одне; клоун під полем; `score`; лічильник ланцюга (`+ui:action-text` «N Chain!»); що в руках (`+ui:held-stack`) видно над клоуном; `danger-line`.
- `end-screen` раунду (Win/Lose, анімація персонажів) → наступний суперник; `game-over-continue` в аркаді.
- MD III: «Magical Journey» — настільна гра-мапа з мініграми (`custom-window`).
- Переходи: main-menu → character-select → game-screen → end-screen → наступний / continue.

## Фічі поза полем
- `mode-versus` (`local-multiplayer`, `ai-opponent-levels`), `mode-endless`, `mode-puzzle` (задані поля), `difficulty-presets` (?).
- MD III + Wonderful / Magical Journey — мета-режим на мапі.
- `leaderboard-local` (аркада), `game-over-continue`.
- Magical Drop V (PC, 2012) — `online-multiplayer` (?).

## Варіації й родичі
- Походить від Drop-Drop (Russ Ltd). Серія: MD (1995), MD II, MD III (1997), MD F, MD Touch (2009), MD V (2012), MD VI (2023).
- Родичі: Puyo (звʼязані групи, сміття), Panel de Pon (swap у стеку, що росте знизу), Puzzle Bobble (кидати кульки вгору). Тут унікально — «витягни/кинь стовпець» і гравітація до стелі.
- **Осі варіацій**: напрям гравітації (вниз / вгору до стелі) · ввід (керувати фігурою / swap / витягти-кинути / стріляти) · збіг (лінія 3 у стовпці / група) · тиск (стеля опускається / стек росте знизу) · атака (ряди сміття / прискорення стеку суперника).

## Цікавинки для курсу
- Ввід «витягти нижню серію однакових / кинути в стовпець» з «рукою»-стеком одного кольору — 📎.
- Гравітація до стелі (дзеркальна) + перевірка вертикальної лінії 3+ — 🌱.
- Ланцюг: підйом після зникнення → новий збіг; плюс ланцюг за таймінгом — 🥉.
- Стеля, що опускається з прискоренням, і кнопка «додати ряд сам» — 📎.
- Versus з атакою візерунком персонажа — 🥉; CPU-суперник, що шукає 3-збіги — 🥈.
- Спец-кульки: зірка (знищити колір), райдуга (джокер) — 🌱 кожна.

## Мапа на каталог
- Є: `keyboard-controls` · `move-by-input` (клоун по стовпцях) · `progress-acceleration` (темп стелі) · `ai-opponent` · `hot-seat` (тут одночасно, найближча) · `event-points` · `combo-multiplier` (ланцюг) · `score-records` · `game-pause` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+column-grab-throw` «Витягти серію з низу стовпця й кинути в інший» · interface/input · 📎 · слоти {hand: one_color|any}.
  - `+line-match-clear` — ⏳ підтверджую (Dr. Mario), тут {min: 3, dir: vertical}.
  - `+chain-reaction` · `+cascade-gravity` — ⏳ підтверджую; тут гравітація вгору.
  - `+garbage-attack` — ⏳ підтверджую (Tetris, Puyo): прискорений стек суперника.
  - `+ceiling-push` «Стеля штовхає новий ряд» · game-logic/waves · 🌱 (≈ Panel de Pon, але згори).
  - `+wildcard-tile` — спільна з Triple Town (райдужна кулька).
  - `+color-clear-special` «Спец-плитка знищує весь колір» · entities/interact · 🌱 (також Bejeweled hypercube (?)).
  - `+manual-row-add` «Гравець сам прискорює подачу» · game-logic/waves · 🌱.

## Пропозиції до словників
- `+trigger:input` · `+trigger:pattern` · `+trigger:settled` · `+trigger:timer`.
- `+cond:same` (колір у руках = колір серії) · `+cond:has` (у руках є кульки).
- `+effect:pickup` ✅ як «взяти в руку»; `+effect:clear` · `+effect:shift` (стек униз) · `+effect:send_garbage`.
- `+role:tile`.
- `+ui:action-text` («Chain!») · `+ui:held-stack` — що і скільки в руках персонажа.
- `+window:character-select` — ⏳ підтверджую.
- `+feature:mode-puzzle` — ⏳ підтверджую.
- `+axis:gravity` — новий варіант `up` (до стелі); `+axis:control` — `grab-throw`.

## Джерела
- ⭐ [Wikipedia: Magical Drop III](https://en.wikipedia.org/wiki/Magical_Drop_III) — правила (витягти/кинути, 3 у стовпці, ланцюги, кнопка ряду, поразка), режими, платформи.
- [Wikipedia: Magical Drop](https://en.wikipedia.org/wiki/Magical_Drop) — серія, Drop-Drop, атаки 24 персонажів.
- [StrategyWiki: Magical Drop III/Gameplay](https://strategywiki.org/wiki/Magical_Drop_III/Gameplay) — спец-кульки (suit, ice, rainbow у versus) — бачено в пошуку, сторінка не відкрилась (403).
- [Nintendo: ACA NeoGeo Magical Drop III](https://www.nintendo.com/games/detail/aca-neogeo-magical-drop-3-switch) — сучасне перевидання.
- YouTube: пошук «magical drop iii gameplay».

## Непевне
- (?) Ширина поля (6/7 стовпців) і висота — не підтверджено.
- (?) Чи лопаються разом звʼязані по горизонталі однакові кульки — з памʼяті.
- (?) Ефекти спец-кульок: зірка/special — знищити колір; лід, «масть», бомба — пошук підтвердив лише назви (suit, ice, rainbow у versus).
- (?) Ланцюг «за темпом» (швидка серія) — Wikipedia: «several groups cleared in quick succession», але вікно часу невідоме.
- (?) Набір режимів першої гри (1995) vs MD III — описано переважно за MD III.
