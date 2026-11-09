---
title: Pokémon Trozei! (Pokémon Link!)
slug: pokemon-trozei
aka: [Pokémon Link!, ポケモントローゼ, Pokemon Trozei]
family: falling-match
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: collect
year: 2005
platforms: [Nintendo DS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pok%C3%A9mon_Trozei!", best: true, note: "рух рядів із загортанням, стовпці вниз/вгору, 4 в ряд, Trozei Chance 3 → 2 з вікном ~2 с, Ditto, Jammer, режими Adventure/Endless/Forever/Mr. Who's Den"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ポケモントローゼ", note: "стилусом зсув рядка/стовпця в 4 боки, 4+ сусідніх, メタモン-джокер, режими Battle (versus) і Pair (кооп), обмін через бездротовий звʼязок"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pok%C3%A9mon_Battle_Trozei", note: "сиквел 3DS 2014: 3+ і бойова система типів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=pokemon+trozei+ds+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [wrap-edges, gravity-fall, line-match-clear, swipe-gestures, chain-reaction, combo-multiplier, collect-quota, goal-counter, sequential-levels, level-unlock, progress-acceleration, codex-window, time-out, simultaneous-versus, online-multiplayer, mode-select, +row-col-slide-wrap, +wildcard-tile, +shrinking-match-window, +jammer-attack, +boss-disruption, +quota-penalty, +stylus-drag]
proposes: ["+cond:match_len", "+ui:chance-timer", "+card:shrinking-match-window", "+card:boss-disruption"]
author: opus
date: 2026-11-09
---

# Pokémon Trozei! — тягни стилусом цілий рядок або стовпець з загортанням; після четвірки на ~2 секунди вистачає трійки, далі — пари

## Суть
Іконки покемонів падають згори через обидва екрани DS; рухати й складати можна лише ті, що на нижньому. Хід — зсунути стилусом **цілий рядок** ліворуч/праворуч (що виїхало за край, заходить з іншого боку) або **стовпець** униз (нижній переходить нагору); підняти стовпець можна, але без збігу він одразу осідає. Чотири однакових у ряд — **Trozei**: вони зникають і «рятуються» до лічильника рівня. Після Trozei вмикається **Trozei Chance**: ~2 секунди вистачає трійки, а якщо встигнути — далі пари, доки ти встигаєш у кожне вікно; так одна четвірка розкручується в довгий ланцюг.

## Поле і час
- Два екрани: верхній — зона, де покемони падають (недосяжна), нижній — ігрове поле, де зсуваються ряди й стовпці. Ширина/висота — (?); у Mr. Who's Den і Forever поле на 2 стовпці ширше.
- Горизонталь — тор: рядок загортається через бічні краї; стовпець униз загортається знизу нагору; вгору — лише тимчасово.
- Real-time: нові покемони безперервно падають згори; рівень пройдено за квотою врятованих, темп і склад покемонів міняються з рівнем.
- Боси (Phobos Mobiles) можуть «знебарвити» поле до силуетів — інформація тимчасово неповна.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Іконка покемона | tile | вид (386 видів; Unown — 28 форм як окремі) | зсувається разом з рядком/стовпцем; 4+ однакових у ряд → зникає |
| Рядок | zone | — | зсув ліворуч/праворуч на клітину з загортанням |
| Стовпець | zone | — | зсув униз із загортанням нижньої клітини нагору; вгору — осідає назад без збігу |
| Ditto (Метамон) | tile | джокер | збігається з будь-яким видом, навіть з кількома різними одночасно; випадає бонусом за надлишкове зчищення |
| Jammer-кулька (камінь) | hazard | — | не збігається ні з чим, крім Ditto; підкидають боси |
| Іконка Trozei Chance | static | ~2 с | зʼявляється після Trozei; поки горить — поріг збігу знижено |
| Бос (Phobos Mobile: Train, Jet, Drill, Sub, Walker) | boss | — | кидає Jammer, знебарвлює поле, +50 до лишку квоти, коли гравцю лишилось ≤10 |
| Лічильник квоти | resource | N покемонів | падає з кожним врятованим; 0 → рівень пройдено |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag_row, left|right)` → ТО `shift(row, dir)`, `wrap(icon_at_edge)`.
- КОЛИ `input(drag_col, down)` → ТО `shift(col, down)`, `wrap(bottom_icon)` — нижня іконка йде нагору стовпця.
- КОЛИ `input(drag_col, up)` → ТО `shift(col, up)`; ЯКЩО `not pattern(line(…))` → ТО `fall(icons)` — стовпець одразу осідає назад.
- КОЛИ `tick` → ТО `spawn_at(icon, top_screen)`, `fall(icon)` до нижнього екрана й стеку.
- КОЛИ `pattern(line(4+, same_kind))` → ЯКЩО `not state(player, trozei_chance)` → ТО `clear(line)`, `counter(quota, −n)`, `set_state(player, trozei_chance, ~2s)`.
- КОЛИ `pattern(line(3+, same_kind))` → ЯКЩО `state(player, trozei_chance)` → ТО `clear(line)`, `counter(quota, −n)`, `combo(+1)`, `set_state(player, trozei_chance_2, ~2s)`.
- КОЛИ `pattern(line(2+, same_kind))` → ЯКЩО `state(player, trozei_chance_2)` → ТО `clear(line)`, `counter(quota, −n)`, `combo(+1)`, `set_state(player, trozei_chance_2, ~2s)` — оновлює вікно.
- КОЛИ `state_off(player, trozei_chance)` → ТО `reset_combo` — поріг знову 4.
- КОЛИ `pattern(line(n, includes ditto))` → ТО `custom: «Ditto рахується як будь-який вид, може замкнути кілька видів одночасно»`.
- КОЛИ `after(clear)` → ЯКЩО `custom: «зчищено більше за потрібне (5 замість 4)»` → ТО `spawn(ditto)`.
- КОЛИ `pattern(line(…, includes jammer))` → ЯКЩО `not occupied(line, ditto)` → ТО `block` — Jammer збігається лише з Ditto.
- КОЛИ `after(clear)` → ТО `fall(icons_above)`; `custom: «новий вид у Покедексі, якщо врятовано вперше»`.
- КОЛИ `counter(quota, ==, 0)` → ТО `win`, `next_level`.
- КОЛИ `custom: «поле заповнене іконками»` → ТО `game_over`.
- Бос: КОЛИ `timer(interval)` → ТО `spawn_at(jammer, …)` або `custom: «силуети замість кольорів»`; КОЛИ `counter(quota, ≤, 10)` → ТО `counter(quota, +50)`.
- Mr. Who's Den: КОЛИ `level_start` → ТО `take(player, prize_coin)`, `timer(start, 2:00)`; КОЛИ `counter(time_left, ==, 0)` → ЯКЩО `not state(player, trozei_chance)` → ТО `window(end-screen)` (поточний Chance дограється).
- Forever: КОЛИ `level_start` → ТО `custom: «поріг першого збігу 5, далі 4 і менше»`, `speed(fall, +)`.
- Endless: КОЛИ `counter(quota, ==, 0)` → ТО `next_level`, `speed(fall, +)`; рівні нескінченні (>145).

## Керування і ввід
- Стилус: потягнути рядок убік або стовпець униз/угору — зсув на стільки клітин, на скільки потягнув (?).
- D-pad і кнопки як альтернатива стилусу — (?).
- Бездротовий звʼязок: Trozei Battle (versus), Pair Trozei (кооп), «Secret Operations» — обмін картками гравців і злиття таблиць рекордів; обмін з Mystery Dungeon: Blue Rescue Team дає Prize Coins.

## Вікна, меню, HUD
- `main-menu` / `mode-select`: Trozei Adventure · Endless · (Hard Adventure, Forever — розблоковуються) · Battle / Pair (бездротово) · Pokédex · Mr. Who's Den.
- `map-window` (?) — вибір етапу пригоди: Research (навчання), Storage (Secret/Huge), Phobos Mobiles (боси), Mr. Who's Den.
- `tutorial-window` — Research: навчальні етапи з прийомами.
- `level-select` — Endless: старт з будь-якого пройденого рівня, кратного 5 (до 25 — 1, 5, 10, 15, 20).
- `codex-window` — Pokédex: запис відкривається, коли покемона врятовано в будь-якому режимі.
- `game-screen`: верхній екран — падіння + портрети/бос, нижній — поле; `remaining-counter` (лишок квоти), `custom: «іконка Trozei Chance з відліком»` (`+ui:chance-timer`), `popup-text` ланцюга, `timer-countdown` (Mr. Who's Den), `level-number` (Endless), `score` (?).
- `dialogue-window` — сюжет Lucy Fleetfoot / SOL проти Phobos.
- `lobby-window` — бездротове лобі Battle / Pair (?).
- `end-screen` — рівень пройдено / поле заповнено; `leaderboard` — рекорди (зливаються через обмін).

## Фічі поза полем
- Режими: пригода (`levels-sequential`, боси), Hard Adventure (більша квота, частіше падіння), `mode-endless`, Forever (ширше поле, поріг 5→4, швидше), Mr. Who's Den (2 хв, рідкісні покемони, вхід за Prize Coin), `mode-versus` і `mode-coop` бездротово.
- `level-unlock` — Hard Adventure після пригоди, Forever після Hard.
- `codex` — Покедекс як колекція; `collectibles` — рідкісні покемони, яких легше зустріти з картками інших гравців.
- `leaderboard-local` зі злиттям через обмін; `currency` — Prize Coins за звʼязок з іншою грою.

## Варіації й родичі
- Pokémon Trozei! (DS, 2005; Genius Sonority) → Pokémon Battle Trozei / Link Battle (3DS eShop, 2014): збіги 3+, бій на верхньому екрані з таблицею ефективності типів, кооп до 4.
- Родичі в корпусі: `chuzzle` (зсув рядка/стовпця з загортанням як хід), `yoshis-cookie` (зсув рядів, поле росте), `puzzle-and-dragons` (вільне перетягування й комбо), `panel-de-pon` (ланцюг під час анімацій), `meteos` (стилус).
- **Осі варіацій**: чим рухати (обмін сусідів / зсув ряду з загортанням / дірка) · поріг збігу (фіксований / спадний у вікні часу — Trozei / зростаючий — Forever) · хто шкодить (нема / бос-скрипт / живий суперник) · мета (виживання / квота врятованих / колекція).

## Цікавинки для курсу
- Зсув рядка й стовпця з загортанням + «підняти стовпець можна, але без збігу осідає» — 📎.
- Trozei Chance: поріг збігу 4 → 3 → 2 у вікні ~2 с, що оновлюється кожним збігом — 🥉 (таймер-стан + змінний поріг перевірки ліній).
- Ditto-джокер, що замикає кілька видів одразу, і Jammer, що збігається лише з Ditto — 📎.
- Бос-диверсії як скрипт (кинути Jammer, знебарвити, +50 до квоти біля фінішу) — 📎.
- Квота рівня + Покедекс як мета-колекція — 🌱.
- Два екрани: недосяжна зона падіння над ігровим полем — 🌱.

## Мапа на каталог
- Є: `wrap-edges` ↔ рядок через край; `gravity-fall` ↔ падіння згори й осідання; `line-match-clear` ↔ 4/3/2 в ряд; `swipe-gestures` ↔ тягнення стилусом; `chain-reaction` + `combo-multiplier` ↔ ланцюг у Trozei Chance; `collect-quota` + `goal-counter` ↔ квота врятованих; `sequential-levels`, `level-unlock`, `progress-acceleration`; `codex-window` ↔ Покедекс; `time-out` ↔ 2 хв у Mr. Who's Den; `simultaneous-versus` + `online-multiplayer` ↔ бездротові Battle/Pair (найближче); `mode-select`.
- **Нема** → пропозиції карток:
  - `+row-col-slide-wrap` (спільна з Chuzzle) — хід = зсув ряду/стовпця з загортанням.
  - `+wildcard-tile` (спільна) — Ditto.
  - `+shrinking-match-window` «Після збігу поріг знижується у вікні часу» · game-logic/score · 🥉 · слоти {thresholds: 4→3→2, window: 2s}.
  - `+jammer-attack` (спільна з Pac-Man sequels) — Jammer-кульки від боса (дитина `garbage-attack`).
  - `+boss-disruption` «Скриптові диверсії боса на полі гравця» · game-logic/opponent · 📎 · слоти {jammer, blind, quota_penalty}.
  - `+quota-penalty` «Квота зростає біля фінішу» · game-logic/win · 🌱.
  - `+stylus-drag` — тягнення стилусом як основний ввід (родич `drag-drop-piece`, `swipe-gestures`).

## Пропозиції до словників
- `+cond:match_len` — довжина лінії, що вважається збігом зараз (4 / 3 / 2) як параметр, а не константа шаблону.
- `+ui:chance-timer` — іконка-відлік вікна знижених умов.
- `+card:shrinking-match-window`, `+card:boss-disruption` — див. мапу.

## Джерела
- ⭐ [Wikipedia: Pokémon Trozei!](https://en.wikipedia.org/wiki/Pok%C3%A9mon_Trozei!) — рух рядків із загортанням і стовпців униз/вгору, падіння через два екрани, 4 в ряд, Trozei Chance (~2 с, 3 → 2), Ditto, Jammer, етапи пригоди, боси (+50 до квоти), Mr. Who's Den, Endless, Forever, Покедекс, розробник і дати.
- [Wikipedia JA: ポケモントローゼ](https://ja.wikipedia.org/wiki/ポケモントローゼ) — зсув рядка/стовпця стилусом у 4 боки, 4+ поруч, Ditto, Trozei Chance до кінця ланцюга, Hard Adventure, Trozei Battle, Pair Trozei, Forever (5 у ряд, ширше), обмін картками, звʼязок з Mystery Dungeon.
- [Wikipedia: Pokémon Battle Trozei](https://en.wikipedia.org/wiki/Pok%C3%A9mon_Battle_Trozei) — сиквел 3DS: 3+, типи, кооп до 4.
- YouTube: пошук «pokemon trozei ds gameplay».

## Непевне
- (?) Розмір поля, чи зсув на кілька клітин за один жест, чи є керування кнопками — не знайдено.
- (?) Форма збігу: EN — «у ряд», JA — «4+ сусідніх» (隣接); чи рахуються L/T-фігури — не перевірено, беру лінії.
- (?) Forever: EN — «спершу 5, потім 4 і так далі», JA — «потрібно 5 у ряд» — розходяться.
- (?) Поразка в пригоді — так само заповнення поля, як в Endless (?).
- (?) Очки й рекорди: JA згадує злиття «рейтингів рекордів», таблиці очок не знайдено.
