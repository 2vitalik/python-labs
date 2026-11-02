---
title: Lady Bug
slug: lady-bug
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: both
  goal: collect
year: 1981
platforms: [arcade, ColecoVision, Intellivision, Nintendo Switch (Arcade Archives)]
links:
  - {kind: play, url: "https://archive.org/details/arcade_ladybug", best: true, note: "Internet Arcade — грати аркаду; опис літер, сердець-множників, черепів, овоча"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Lady_Bug_(video_game)", note: "турнікети, рамка-таймер, 8 видів комах, порти"}
  - {kind: official, url: "https://www.nintendo.com/en-ca/store/products/arcade-archives-lady-bug-switch/", note: "Arcade Archives — офіційне перевидання"}
  - {kind: wiki, url: "https://pixelatedarcade.com/games/lady-bug", note: "опис механік: поворотні стінки, кольори літер, черепи"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=lady+bug+1981+arcade+gameplay", note: "пошук; геймплей аркади"}
stage: v1
coverage: 70
mechanics: [move-4dir, collect-all, touch-death, player-death, chase-player, spawn-points, spawn-schedule, temporary-modes, combo-multiplier, event-points, impassable-cells, sequential-levels, progress-acceleration, status-panel, mode-indicator, score-records, leaderboard, game-screen, +turnstile-gate, +color-cycling-items, +word-spelling-bonus, +border-timer, +lethal-to-all-hazard, +center-bonus-item]
proposes: ["+effect:rotate_gate", "+effect:cycle_color", "+trigger:timer_lap", "+cond:color", "+effect:add_letter", "+ui:border-timer", "+ui:word-slots", "+card:turnstile-gate"]
author: opus
date: 2026-11-02
---

# Lady Bug — Pac-Man з турнікетами: перекручуй стінки лабіринту, лови літери потрібного кольору

## Суть
Сонечко їсть усі квіти, серця й літери в лабіринті, тікаючи від комах, що виходять із центру. Головна відмінність від Pac-Man — **20 зелених турнікетів**: проходячи крізь них, гравець повертає стінку на 90° і перебудовує лабіринт, відрізаючи переслідувачів. Друга вісь — **предмети, що мерехтять кольорами**: синє серце підвищує множник очок, червона/жовта літера додається у слово SPECIAL/EXTRA. Черепи вбивають і гравця, і комах.

## Поле і час
- Квадратний лабіринт (клітинний, як у Pac-Man) з центральною «кліткою» комах; у ній же пізніше зʼявляється овоч.
- **Рамка лабіринту — таймер**: по периметру біжить кольорова смуга; кожне повне коло випускає одну комаху з центру (до 4 на рівні). Швидкість кола зростає на рівнях 2 і 5.
- Турнікети — частина стін зі станом (горизонтальне/вертикальне положення); лабіринт змінюється під час гри, але повністю ізолювати ділянку неможливо.
- Real-time; кольори предметів перемикаються за власним циклом.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Сонечко | player | життя | рух 4 напрямки; проходячи турнікет, повертає його |
| Стіна | static | — | непрохідна |
| Турнікет (green gate) | gate | положення ┃/━ | поворот на 90° у бік руху сонечка |
| Квітка (dot) | pickup | — | очки; потрібна для завершення |
| Серце | pickup | колір синій/червоний/жовтий | синє → множник ×2 → ×3 → ×5; інші — лише очки |
| Літера | pickup | буква; колір | червона → слово SPECIAL, жовта → EXTRA, синя — очки |
| Череп | hazard | випадкове місце | смерть сонечку; комаха на черепі теж гине |
| Комаха | enemy | вид за рівнем (8 видів) | виходить із центру за таймером, переслідує |
| Овоч | pickup | вид і ціна за рівнем | у центрі після виходу 4-ї комахи; бонус + заморожує комах |
| Рамка-таймер | static (HUD у полі) | швидкість | повне коло → випуск комахи |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(ladybug, dir)`.
- КОЛИ `contact(ladybug, gate)` → ТО `rotate(gate, 90)` у бік руху; сонечко проходить. `custom: «комахи турнікет не повертають»` (?).
- КОЛИ `contact(ladybug, flower)` → ТО `pickup`, `score(10 × mult)` (?).
- КОЛИ `contact(ladybug, heart)` → ЯКЩО `custom: «колір = синій»` → ТО `multiplier(×2→×3→×5)`; інакше `score(n × mult)`.
- КОЛИ `contact(ladybug, letter)` → ЯКЩО `custom: «колір = червоний»` і буква є в SPECIAL → ТО `custom: «підсвітити букву в SPECIAL»`; ЯКЩО жовтий і буква в EXTRA → ТО так само для EXTRA; завжди `score(n × mult)`.
- КОЛИ `custom: «слово EXTRA зібране»` → ТО `lives(+1)`.
- КОЛИ `custom: «слово SPECIAL зібране»` → ТО `custom: «безкоштовна гра (кредит)»` (аркада); ColecoVision — бонус-рівень «Vegetable Harvest».
- КОЛИ `timer(border_lap)` → ЯКЩО `count(insect, <, 4)` → ТО `spawn(insect)` з центру.
- КОЛИ `counter(insects_released, ==, 4)` → ТО `spawn_at(vegetable, center)`.
- КОЛИ `contact(ladybug, vegetable)` → ТО `pickup`, `score(veg_value)` (до 9500 на пізніх рівнях, без множника), `freeze(insects, кілька секунд)`; дотик до замороженої комахи все одно вбиває.
- КОЛИ `contact(ladybug, insect|skull)` → ТО `lose` (життя −1).
- КОЛИ `contact(insect, skull)` → ТО `disappear_both` (?) — череп смертельний і для комах.
- Комахи: `chase-player` по поточному лабіринту; турнікети для них — стіни.
- КОЛИ `all_gone(flower, heart, letter)` → ТО `win` рівня, `next_level`.
- Перемога: нема (нескінченна аркада). Поразка: 0 життів. Рахунок: квіти/серця/літери × множник (до ×5), овоч окремо.

## Керування і ввід
- 4-позиційний джойстик; кнопок дії нема. Турнікет крутиться самим проходом — без окремої дії.
- Тактика — «перекрити» турнікетами коридори позаду себе; комахи губляться.
- 1–2 гравці по черзі.

## Вікна, меню, HUD
- `splash-screen` / атракт: демо, ціни предметів.
- `game-screen` — лабіринт у рамці-таймері; HUD: `score`, `hi-score`, `lives`, `level-number`, **слова SPECIAL і EXTRA з підсвіченими зібраними буквами** (`custom: «word-slots»`), індикатор множника ×2/×3/×5 (`multiplier`), наступний овоч / комаха (?).
- `end-screen` рівня (коротко), екран вводу ініціалів → `leaderboard`.
- Переходи: атракт → (монета) game-screen → (усе зʼїдено) наступний рівень → (0 життів) ініціали → атракт.

## Фічі поза полем
- `levels-sequential`, `progress-acceleration` (рамка швидшає, нові комахи щорівня до 8-го).
- `leaderboard-local`; `hotseat` — 2 гравці по черзі.
- Нема паузи, збережень, налаштувань у грі (лише DIP оператора).

## Варіації й родичі
- Порти: ColecoVision (бонус-рівень Vegetable Harvest за SPECIAL), Intellivision (без SPECIAL). Arcade Archives — точне перевидання.
- Родичі: Pac-Man (лабіринт + переслідувачі), Mr. Do! (букви EXTRA від ворогів), Kwirk і Chip's Challenge (турнікети в головоломках).
- Осі: **хто може повернути турнікет** (лише гравець / усі); **що дає колір предмета** (множник / слово / очки); **таймер як елемент поля** (рамка) vs окремий лічильник.

## Цікавинки для курсу
- Турнікет: стінка-стан, що повертається від руху аватара, і лабіринт змінюється для AI ворогів — 🥉: перерахунок шляху після зміни поля.
- Предмети з циклом кольорів і різний ефект залежно від моменту взяття — 📎.
- Слова-колекції SPECIAL/EXTRA як прогрес між рівнями — 📎 (+ `ui` слоти букв).
- Рамка-таймер: таймер, вбудований у поле, що керує спавном — 🌱 логіка + 📎 рендер.
- Череп, смертельний для всіх: пастка, якою можна вбити ворога — 🌱.
- Множник ×2→×3→×5 від синіх сердець — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `collect-all` · `touch-death` · `player-death` · `chase-player` · `spawn-points` (центр) · `spawn-schedule` (коло рамки) · `temporary-modes` (заморожені комахи після овоча) · `combo-multiplier` (найближче до множника від сердець) · `event-points` · `impassable-cells` · `sequential-levels` · `progress-acceleration` · `status-panel` · `mode-indicator` (множник) · `score-records` · `leaderboard` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+turnstile-gate` «Турнікет, що повертається проходом» · entities/legality · 🥉 · слот {who: player|all}.
  - `+color-cycling-items` «Предмет зі змінним кольором-ефектом» · entities/interact · 📎.
  - `+word-spelling-bonus` «Зібрати слово з букв» · game-logic/score · 📎 · слот {words: text}.
  - `+border-timer` «Таймер-рамка навколо поля» · interface/hud · 📎.
  - `+lethal-to-all-hazard` «Пастка для всіх» · entities/death · 🌱.
  - `+center-bonus-item` «Бонус у точці спавну після події» · entities/spawn · 🌱 (овоч, фрукт Pac-Man).

## Пропозиції до словників
- `+effect:rotate_gate` — повернути стінку-турнікет на 90° у бік проходу (`rotate(a, deg)` є, але не про стіну між клітинами).
- `+effect:cycle_color` — предмет періодично змінює колір (і ефект).
- `+trigger:timer_lap` — завершено коло таймера-рамки (спавн).
- `+cond:color(a, c)` — колір предмета в момент взяття.
- `+effect:add_letter(word, ch)` — додати букву у слово-колекцію.
- `+ui:border-timer` — таймер як рамка поля; `+ui:word-slots` — слово з підсвіченими зібраними буквами.
- `+card:turnstile-gate` — див. вище.

## Джерела
- ⭐ [Internet Arcade: Lady Bug](https://archive.org/details/arcade_ladybug) — грати в браузері; опис кольорів літер, синіх сердець ×2/×3/×5, черепів, овоча.
- [Wikipedia: Lady Bug](https://en.wikipedia.org/wiki/Lady_Bug_(video_game)) — 20 турнікетів, рамка-таймер (швидшає на 2 і 5), 8 видів комах, порти.
- [Pixelated Arcade: Lady Bug](https://pixelatedarcade.com/games/lady-bug) — поворот секцій стіни, ролі кольорів літер, черепи проти комах, овоч після всіх комах.
- [Arcade Archives Lady Bug (Nintendo)](https://www.nintendo.com/en-ca/store/products/arcade-archives-lady-bug-switch/) — офіційне перевидання.
- YouTube: пошук «lady bug 1981 arcade gameplay».

## Непевне
- (?) Точні очки (квітка 10, серця/літери 100–800, овочі 1000–9500) — у джерелах лише фрагменти.
- (?) Чи можуть комахи повертати турнікети — описи згадують лише сонечко.
- (?) Порядок і період зміни кольорів літер/сердець; чи синя літера щось дає, крім очок.
- (?) Чи завершення EXTRA одразу закінчує рівень (Pixelated Arcade) — не підтверджено іншим джерелом.
- (?) Розмір лабіринту в клітинах.
