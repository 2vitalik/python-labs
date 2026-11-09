---
title: Money Puzzle Exchanger
slug: money-puzzle-exchanger
aka: [Money Idol Exchanger, マネーアイドルエクスチェンジャー, MPE]
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
year: 1997
platforms: [arcade (Neo Geo MVS), Game Boy, Windows, PlayStation, PS4, Xbox One, Switch, PS Vita]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Money_Puzzle_Exchanger", best: true, note: "суть: монети зливаються 1→5→10…, RU/ER, режими, порти"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/マネーアイドルエクスチェンジャー", note: "JA: поле 7×12 (GB 7×9), точні правила злиття 5/2, ER/RU, draw, порти"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Magical_Drop_III", note: "родич: той самий ввід витягти/кинути"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=money+puzzle+exchanger+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [keyboard-controls, move-by-input, tile-merge, chain-reaction, garbage-attack, simultaneous-versus, ai-opponent, event-points, combo-multiplier, progress-acceleration, character-select, game-over-continue, score-records, game-pause, end-screen, +column-grab-throw, +ceiling-push, +manual-row-add, +denomination-merge, +rank-up-special, +color-clear-special, +late-chain]
proposes: ["+effect:rank_up", "+effect:clear_color", "+effect:raise_stack", "+cond:min_group", "+ui:held-stack", "+card:denomination-merge", "+card:rank-up-special", "+card:late-chain"]
author: opus
date: 2026-11-09
---

# Money Puzzle Exchanger — витягни монети з низу стовпця й кинь назад: 5 однакових «копійок» розмінюються на одну старшу

## Суть
Клон-гібрид Magical Drop і Fujitsu-гри Moujiya: поле монет-номіналів єни звисає зі стелі й опускається, персонаж унизу **витягує** нижні однакові монети стовпця і **кидає** їх в інший стовпець. Збіг — не «зникнення трьох», а **розмін**: 5 монет по 1 стають однією 5, дві 5 — однією 10, далі 50, 100, 500; лише дві 500 зникають. Тож кожен збіг переважно **не звільняє**, а стискає поле і народжує нову монету, яка може дати наступний розмін (ланцюг). Плюс спецблоки RU (підвищити номінал усіх монет виду) і ER (стерти всі монети виду).

## Поле і час
- Сітка **7 стовпців × 12 рядів** (Game Boy — 7 × 9); у клітині одна монета або спецблок.
- Гравітація **до стелі** (як у Magical Drop): монети висять зверху, дірки закриваються підйомом нижніх монет — кинуті монети «влітають» угору й лягають під стовпець.
- Real-time: через фіксовані проміжки згори виходить новий повний ряд монет — увесь стек зсувається вниз; гравець може викликати ряд сам.
- Поразка — монета перейшла нижній ряд (або гравець сам поставив туди монету без злиття).
- Versus: два поля поруч, ланцюги одного «досипають» монети іншому.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Персонаж-обмінник | player | стовпець; «руки»: номінал + кількість | ходить ←/→ під полем; витягує й кидає монети |
| Монета 1 | tile | номінал 1 | 5+ дотичних → одна монета 5 |
| Монета 5 | tile | номінал 5 | 2+ дотичних → одна монета 10 |
| Монета 10 | tile | номінал 10 | 5+ → одна 50 |
| Монета 50 | tile | номінал 50 | 2+ → одна 100 |
| Монета 100 | tile | номінал 100 | 5+ → одна 500 |
| Монета 500 | tile | номінал 500 | 2+ дотичних → зникають (вершина ланцюга номіналів) |
| RU (Rank Up, зелений) | tile | — | 2+ дотичних RU зникають → усі монети номіналу, що безпосередньо над ними, по всьому полю підвищуються на ранг |
| ER (Erase, синій) | tile | — | 2+ дотичних ER зникають → усі монети номіналу над ними зникають з поля |
| Стеля-генератор | spawner | темп | періодично видає повний ряд монет зверху, стек опускається |
| Нижня межа | static | ряд персонажа | монета за нею → поразка |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ТО `move(player, column±1)`.
- КОЛИ `input(grab)` → ЯКЩО руки порожні або `same(hand, bottom_coin, value)` → ТО `pickup(run)` — нижня монета стовпця і **всі однакові підряд** над нею, без ліміту кількості.
- КОЛИ `input(throw)` → ЯКЩО `has(player, coins)` → ТО `throw(hand, column)` — монети з рук летять угору й лягають під низ стовпця.
- КОЛИ `after(throw)` → ЯКЩО `same(group, 1|10|100, value) and custom: «min_group ≥ 5, звʼязні по горизонталі/вертикалі»` → ТО `merge(group → next_rank)` — одна монета наступного рангу, `score(n)`.
- КОЛИ `after(throw)` → ЯКЩО `same(group, 5|50, value) and custom: «min_group ≥ 2»` → ТО `merge(group → next_rank)`, `score(n)`.
- КОЛИ `after(throw)` → ЯКЩО `same(group, 500, value) and custom: «min_group ≥ 2»` → ТО `clear(group)`, `score(n)`.
- КОЛИ `after(throw)` → ЯКЩО `same(group, ER) and custom: «min_group ≥ 2»` → ТО `clear(group)`, `custom: «clear_color — усі монети номіналу, що лежить безпосередньо над ER, зникають з поля»`; очок за сам спецблок нема.
- КОЛИ `after(throw)` → ЯКЩО `same(group, RU) and custom: «min_group ≥ 2»` → ТО `clear(group)`, `custom: «rank_up — усі монети номіналу над RU по полю стають наступним рангом (1 → 5)»`.
- КОЛИ `after(merge|clear)` → ТО `fall(coins_below)` угору до стелі; КОЛИ `settled` → ЯКЩО новий збіг → ТО повторити злиття з `combo(+1)` (ланцюг; більше очок).
- КОЛИ `input(grab|throw)` під час анімації ланцюга → ЯКЩО новий збіг стався до `settled` → ТО `custom: «late_chain — збіг зараховано як продовження ланцюга»` (аналог «後付け連鎖» Magical Drop).
- КОЛИ `timer(every)` → ТО `custom: «raise_stack — новий повний ряд монет зверху, стек униз на 1»`.
- КОЛИ `input(add_row)` → ТО `custom: «raise_stack — ряд одразу»`.
- КОЛИ `reach(coin, below_bottom)` → ЯКЩО `not custom: «на полі йде злиття/зникнення»` → ТО `lose`.
- КОЛИ `input(throw)` у нижній ряд → ЯКЩО кидок не дав злиття → ТО `lose`.
- Versus: КОЛИ `counter(chain, ≥, n)` → ТО `send_garbage(coins)` — кількість монет супернику росте з довжиною ланцюга.
- Versus: КОЛИ обидва програли одночасно → ТО `draw` (обидва вважаються переможцями); у фінальному бою з CPU нічия = перемога CPU.
- Перемога: суперник програв · Поразка: монета нижче межі · Рахунок: очки за злиття, множник ланцюга.

## Керування і ввід
- Джойстик ←/→ — персонаж по 7 стовпцях; одна кнопка — витягти (grab), друга — кинути (throw) (?); окрема дія — додати ряд (?).
- Руки тримають монети лише одного номіналу; витягнути інший номінал, поки руки не порожні, не можна.
- Темп: досвідчений гравець робить серії grab/throw дуже швидко, будуючи ланцюг поки попередній ще «розмінюється».

## Вікна, меню, HUD
- `splash-screen` / `attract-demo` (аркада) → `main-menu`: 1P проти CPU · VS 2P · «Один на практиці» (solo) · Story (лише Windows/PS).
- `character-select` — 8 персонажів-«валют» (Sakura Mitsukoshi / Exchanger, Asahi Takashima, Bill Bank, Lulula Franc, Ena Arashizaki, Seshil Pound, Blibov Sakata, Note Bank); в аркадному 1P обираєш з двох; прихований персонаж Haniwa у solo.
- `game-screen`: два поля 7×12 (versus) або одне; персонаж під полем з монетами в руках (`+ui:held-stack`); `score`; `popup-text` «N Chain»; `danger-line`.
- `end-screen` раунду (Win/Lose/DRAW) → наступний суперник; `game-over-continue` в аркаді.
- `dialogue-window` між боями (story-версії).
- Переходи: main-menu → character-select → game-screen → end-screen → наступний бій / continue.

## Фічі поза полем
- `mode-versus` (`local-multiplayer`), 1P-кампанія проти 7 суперників, `mode-endless` (solo: виживати якомога довше).
- Story mode — додано в Windows 95 і PlayStation; на Game Boy нема, і в CPU-боях там лише Sakura.
- `leaderboard-local` (аркада), `game-over-continue`.
- ACA NeoGeo (Hamster): онлайн-рекорди перевидання (?).

## Варіації й родичі
- Прямий родич — [magical-drop](magical-drop.md) (ввід витягти/кинути, стеля, що опускається; Data East судилась із Face 1997 р.). Механіка злиття — від Moujiya (Fujitsu, 1995).
- Злиття номіналів з порогом, що чергується (5 / 2) — родич [2048](2048.md) і [triple-town](triple-town.md) (злиття в старший тип), але в real-time стеку.
- Спецблок «знищити колір» — як у [columns](columns.md) і Magical Drop.
- **Осі варіацій**: результат збігу (зникнення / злиття в старший тип / злиття з порогом за рангом) · поріг групи (фіксований 3 / залежить від типу 5-2-5-2) · спецблоки (по кольору поля / по типу під собою) · ввід (керувати фігурою / swap / витягти-кинути).

## Цікавинки для курсу
- Злиття номіналів із чергуванням порогу 5/2 (як справжні монети) і «зникненням» лише на вершині — 📎: таблиця правил замість одного числа.
- Ланцюг, де продукт злиття — нова монета у клітині групи, що може злитися далі — 🥉: треба вирішити, де саме зʼявляється старша монета.
- RU/ER, що дивляться на тип «над собою» і діють на все поле — 🌱 кожен.
- Гравітація до стелі + кидок угору під стовпець — 🌱 (дзеркальна гравітація).
- «Late chain» — ланцюг продовжується вводом під час анімації — 🥈 (стан анімації в логіці).
- Versus з нічиєю та особливим правилом нічиєї проти CPU — 📎.

## Мапа на каталог
- Є: `keyboard-controls` · `move-by-input` (персонаж по стовпцях) · `tile-merge` (розмін) · `chain-reaction` · `garbage-attack` · `simultaneous-versus` · `ai-opponent` · `event-points` · `combo-multiplier` · `progress-acceleration` · `character-select` · `game-over-continue` · `score-records` · `game-pause` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+column-grab-throw` — ⏳ підтверджую (Magical Drop).
  - `+ceiling-push` · `+manual-row-add` — ⏳ підтверджую (Magical Drop).
  - `+denomination-merge` «Злиття N однакових у старший тип за таблицею порогів» · entities/legality · 📎 · слоти {thresholds: [5,2,5,2,5,2], top: vanish}.
  - `+rank-up-special` «Спецблок підвищує всі плитки типу» · entities/interact · 🌱 · слоти {target: above|chosen}.
  - `+color-clear-special` — ⏳ підтверджую (ER).
  - `+late-chain` «Ланцюг продовжується збігом, зробленим під час анімації» · game-logic/score · 🥈.

## Пропозиції до словників
- `+effect:rank_up` — усі сутності типу стають наступним рангом (RU; також підвищення плиток у merge-іграх).
- `+effect:clear_color` — прибрати з поля всі сутності типу/кольору (ER; Columns, Magical Drop).
- `+effect:raise_stack` — ⏳ підтверджую (Panel de Pon): тут стек опускається від стелі.
- `+cond:min_group` — розмір звʼязної групи ≥ N, де N залежить від типу (5 для 1/10/100, 2 для 5/50/500).
- `+ui:held-stack` — ⏳ підтверджую (Magical Drop): номінал і кількість у руках.
- `+card:denomination-merge` · `+card:rank-up-special` · `+card:late-chain`.

## Джерела
- ⭐ [Wikipedia: Money Puzzle Exchanger](https://en.wikipedia.org/wiki/Money_Puzzle_Exchanger) — суть розміну, RU/ER, режими, персонажі, дати й платформи, Moujiya/Magical Drop.
- [Wikipedia JA: マネーアイドルエクスチェンジャー](https://ja.wikipedia.org/wiki/マネーアイドルエクスチェンジャー) — поле 7×12 / 7×9, пороги 5/2, ER/RU «тип над собою», late chain, умови поразки, DRAW, відмінності портів.
- [Wikipedia: Magical Drop III](https://en.wikipedia.org/wiki/Magical_Drop_III) — базова схема вводу.
- YouTube: пошук «money puzzle exchanger gameplay».

## Непевне
- (?) Де саме зʼявляється нова монета після злиття (у клітині кинутої монети чи найвищої в групі) — джерела не кажуть.
- (?) Чи є окрема кнопка «додати ряд» на аркадному пульті (JA-вікі: «можна підняти вручну», без кнопки).
- (?) Чи монети в руках обмежені (JA: «без ліміту» для однакових над нижньою).
- (?) Формула монет-сміття за ланцюг і візерунки атак персонажів — не описано.
- (?) Темп появи рядів і прискорення — чисел нема.
- (?) EN-вікі: у 1P «один із двох персонажів» проти до 7 суперників; JA уточнює лише GB (тільки Sakura).
