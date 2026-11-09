---
title: Super Auto Pets
slug: super-auto-pets
aka: [SAP]
family: tower-lanes
also: []
klass: cursor
axes:
  field: 1d
  time: turn
  opponent: online
  info: partial
  random: runtime
  goal: collect
year: 2021
platforms: [PC, iOS, Android, Mac, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Super_Auto_Pets", best: true, note: "фази, 10 золота, порядок справа наліво, трофеї й життя, тири, режими, паки"}
  - {kind: fandom, url: "https://superautopets.wiki.gg/wiki/The_Basics", note: "wiki.gg: ціни 3/1, freeze, злиття дублікатів, досвід 2+3, бонус-пет за рівень, Hard Mode Toys"}
  - {kind: fandom, url: "https://superautopets.wiki.gg/", note: "wiki.gg: улюбленці, їжа, іграшки, мана, ailments"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=super+auto+pets+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [round-currency, shop-catalog, shop-buyback, shop-preview, tile-merge, drag-drop-piece, hp-damage, async-multiplayer, online-multiplayer, move-timer, status-effects, chain-reaction, achievements-window, mode-select, leaderboard, +auto-battle, +shop-reroll, +shop-freeze, +star-up-merge, +ability-triggers, +front-of-line-combat, +lives-and-trophies, +tier-by-turn, +level-up-bonus-pick, +handicap-toys, +pack-select]
proposes: ["+role:unit", "+trigger:faint", "+trigger:hurt", "+trigger:bought", "+trigger:sold", "+trigger:battle_start", "+trigger:level_up", "+effect:reroll", "+effect:sell", "+effect:freeze_slot", "+effect:summon", "+cond:position", "+ui:trophy-counter", "+ui:shop-bar", "+window:pack-select", "+axis:time"]
author: opus
date: 2026-11-09
---

# Super Auto Pets — автобатлер на одному ряду з 5 улюбленців: порядок і тригери «при купівлі / перед смертю»

## Суть
Асинхронний автобатлер: щоходу маєш 10 золота, купуєш у магазині улюбленців (3) і їжу, ставиш їх у **ряд з 5 слотів** і переставляєш. Бій — автоматичний: крайній правий твій бʼється з крайнім лівим чужим, обидва бʼють одночасно, загиблого заміняє наступний. Уся глибина — у **тригерах здібностей** (при купівлі, при продажу, на початку бою, при пораненні, при смерті…) і порядку в ряду, бо здібності зачіпають сусідів. Перемога — 10 трофеїв, поразка — кінець життів.

## Поле і час
- Поле — 1D-ряд з 5 слотів на сторону; у бою два ряди стоять лицем один до одного, контакт — лише «передні».
- Хід = **фаза магазину** (без ліміту часу в Arena; з таймером у Versus) → **бій** (авто, анімований) → результат. Тир магазину росте кожні два ходи до 6.
- Суперник — записана команда іншого гравця з того самого ходу (асинхронно) або AI-команда, якщо гравців нема.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Улюбленець (pet) | ally (`+role:unit`) | атака, HP, рівень 1–3, досвід, тир, здібність з тригером | стоїть у слоті; у бою бʼє переднього ворога; тригер → здібність |
| Слот ряду | zone | 5 | порядок важливий: перший — правий |
| Магазин | spawner | слоти улюбленців + їжі, тир | пропонує улюбленців і їжу поточного тиру й нижче |
| Замороження (freeze) | zone | на слоті магазину | заморожене не зникає при рероллі й між ходами |
| Їжа-стат | pickup | +атака/+HP | годують улюбленця з магазину |
| Їжа-перк | pickup | 1 перк на улюбленця | дає здібність у бою (щит, +шкода, повернення після смерті…) |
| Шоколад | pickup | +1 досвід | рівень без дубліката |
| Токен (призваний) | ally | — | зʼявляється від здібностей (напр., при смерті), займає слот |
| Золото | resource | 10 на хід | улюбленець 3, їжа 3 (деякі 1), реролл 1, перший реролл безкоштовний |
| Трофей | resource | 10 = перемога | +1 за виграний бій |
| Життя | resource | Arena 5 (Easy 7), Versus 6 | −1 за програний бій; +1 повертається на 3-му ході |
| Іграшка Hard Mode | hazard | — | з 3-го ходу обираєш 1 з 2, далі кожен непарний хід; шкодить тобі або допомагає суперникові |
| Мана (пак Unicorn) | resource | на улюбленцеві | пакова механіка |
| Ailment | hazard | — | негативний статус (пак Unicorn) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(player)` → ТО `currency(10)`, `custom: «магазин заповнюється, заморожене лишається»`; КОЛИ `custom: «непарний хід»` → ТО `custom: «тир магазину +1, до 6»`.
- КОЛИ `input(buy, pet, slot)` → ЯКЩО `has(gold, 3)` and `free(slot)` → ТО `currency(-3)`, `place(pet, slot)`, `custom: «trigger bought»`.
- КОЛИ `input(drag, pet, same_pet)` → ЯКЩО `same(a, b, kind)` → ТО `merge(a, b)`: `counter(exp, +1)`; рівень 2 — 2 досвіду, рівень 3 — ще 3.
- КОЛИ `counter(exp, >=, need)` → ТО `counter(level, +1)`, `custom: «+1 атака, +1 HP»`, `custom: «додати в магазин вибір з 2 улюбленців наступного тиру»` (не при злитті двох 2-рівневих у 3-й).
- КОЛИ `input(feed, food, pet)` → ЯКЩО `has(gold, price)` → ТО `custom: «+стати або перк»`; новий перк заміняє старий (1 на улюбленця).
- КОЛИ `input(roll)` → ЯКЩО `has(gold, 1)` or `first_time` → ТО `custom: «effect reroll: усі незаморожені слоти магазину»`.
- КОЛИ `input(freeze, shop_slot)` → ТО `set_state(slot, frozen)` (займає слот, переживає реролл і хід).
- КОЛИ `input(sell, pet)` → ТО `currency(+value)` (?), `disappear_a`, `custom: «trigger sold»`.
- КОЛИ `input(drag, pet, slot)` → ТО `swap(a, b)` або `move(a, slot)` (переставити порядок).
- КОЛИ `input(end_turn)` → ТО `custom: «trigger end_turn»` для здібностей, далі бій.
- КОЛИ `custom: «trigger battle_start»` → ТО `custom: «здібності «Start of battle» за порядком (?)»`.
- КОЛИ `custom: «раунд атаки»` → ТО `custom: «передній мій і передній чужий»` `damage` одне одному **одночасно**.
- КОЛИ `custom: «trigger hurt: улюбленець отримав шкоду»` → ТО здібність Hurt; КОЛИ `hp_zero(pet)` → ТО `custom: «trigger faint»`, `disappear_a`, `shift(row, front)` — наступний займає місце.
- КОЛИ `custom: «здібність призиває токен»` → ЯКЩО `count(row, <, 5)` → ТО `spawn_at(token, slot)`; інакше `block`.
- КОЛИ `all_gone(pets, side)` → ТО: тільки ворог — `counter(trophies, +1)`; тільки я — `lives(-1)`; обидва — `draw` (нічого не змінюється).
- КОЛИ `counter(trophies, ==, 10)` → ТО `win` (Arena); КОЛИ `counter(lives, ==, 0)` → ТО `lose`; Versus — `custom: «останній, хто вижив»`.
- КОЛИ `turn_start(player)` → ЯКЩО `custom: «хід 3 і втрачено життя»` → ТО `lives(+1)`.
- КОЛИ `custom: «Hard mode, непарний хід ≥3»` → ТО `choose(2 toys)`.
- Перемога: 10 трофеїв (Arena) / останній живий (Versus) · Поразка: життя = 0 · Рахунок: рейтинг Versus (старт 1500), стрічки за 3-рівневих у команді-переможці.

## Керування і ввід
- Миша/тач: drag улюбленця з магазину в слот; drag на однакового — злиття; drag їжі на улюбленця; drag між слотами — переставити.
- Кнопки Roll, Freeze (або клік по слоту магазину), Sell, End Turn; Arena без таймера, Versus — таймер ходу.

## Вікна, меню, HUD
- `main-menu`: Arena, Versus, With Friends, паки, налаштування.
- `mode-select` (Arena Easy/Normal/Hard · Versus · With Friends) і `+window:pack-select` (Turtle, Puppy, Star, Golden, Unicorn, Danger, Weekly, Custom).
- `game-screen` магазину: ряд з 5 слотів, вітрина `+ui:shop-bar` (улюбленці + їжа), `coins`, `lives`, `+ui:trophy-counter`, номер ходу/тир, кнопки Roll/Freeze/Sell/End Turn, `tooltip` здібності.
- `game-screen` бою: два ряди лицем один до одного, `popup-text` шкоди, `speed-slider`/пропуск (?).
- `choice-window` — Hard Mode Toys (1 з 2); `end-screen` — перемога/поразка, стрічки; `achievements-window` — досягнення «рівень 3»; `leaderboard` Versus (тижнева).
- With Friends: `lobby-window` / `match-setup` — пак, час підготовки, життя за поразку.

## Фічі поза полем
- `async-multiplayer` (Arena) і синхронний/асинхронний Versus 1v1 або 8; `leaderboard-online` тижневий.
- `custom-rules` — With Friends (пак, таймер, втрати життів); кастомні паки з лімітами на тир.
- `difficulty-presets` — Easy/Normal/Hard (Hard — іграшки-гандикапи); `achievements`; ribbons за перемоги.
- Платформи кросплей (Steam, мобільні, браузер); паки — DLC.

## Варіації й родичі
- Родичі в сімʼї: [dota-auto-chess](dota-auto-chess.md) і [teamfight-tactics](teamfight-tactics.md) (дошка 2D, злиття 3 копій), [inscryption](inscryption.md) (карти бʼють навпроти); поза сімʼєю — Hearthstone Battlegrounds (ряд юнітів, тригери Deathrattle/Battlecry), The Bazaar.
- **Осі варіацій**: поле — ряд (SAP) / дошка (DAC) · злиття — 2 копії → досвід (SAP) / 3 копії → зірка · суперник — записаний асинхронно / живий синхронно · економіка — фіксовані 10 золота / відсотки.

## Цікавинки для курсу
- Бій двох черг: передній проти переднього, одночасний удар, зсув черги — 🌱 (ідеально для deque).
- Подієва система тригерів (buy/sell/faint/hurt/start of battle) з ланцюгами: призов від смерті, що викликає «friend summoned» — 🥈.
- Магазин з рероллом і заморожуванням слотів — 📎.
- Досвід через дублікати + бонус-вибір наступного тиру — 📎.
- Асинхронний PvP: зберегти команду ходу N і віддати іншому гравцю на тому ж ході — 🥈.

## Мапа на каталог
- Є: `round-currency` ↔ 10 золота · `shop-catalog` + `shop-preview` ↔ вітрина з описом здібностей · `shop-buyback` ↔ продаж · `tile-merge` ↔ злиття дубліката · `drag-drop-piece` · `hp-damage` · `async-multiplayer` ↔ записані команди · `online-multiplayer` ↔ Versus · `move-timer` ↔ таймер Versus · `status-effects` ↔ перки/ailments · `chain-reaction` ↔ ланцюги тригерів · `achievements-window` · `mode-select` · `leaderboard`.
- **Нема** → пропозиції карток:
  - `+ability-triggers` «Здібності на подіях життєвого циклу (buy/sell/faint/hurt)» · entities/state · 🥈.
  - `+front-of-line-combat` «Бій двох черг передніми» · entities/combat · 🌱.
  - `+shop-freeze` «Заморозити слот вітрини» · game-logic/economy · 🌱.
  - `+lives-and-trophies` «Два лічильники: N перемог або M поразок» · game-logic/win · 🌱.
  - `+tier-by-turn` «Тир магазину росте з ходом» · game-logic/economy · 🌱.
  - `+level-up-bonus-pick` «Новий рівень дає вибір з наступного тиру» · game-logic/economy · 📎.
  - `+handicap-toys` «Обовʼязкові гандикапи на вибір» · game-logic/difficulty · 📎.
  - `+pack-select` «Набір контенту на партію» · game-logic/constraints · 🌱.

## Пропозиції до словників
- `+role:unit` — бойовий юніт загону.
- `+trigger:faint` (загинув свій юніт — ширше за `died` для здібностей), `+trigger:hurt`, `+trigger:bought`, `+trigger:sold`, `+trigger:battle_start`, `+trigger:level_up`.
- `+effect:reroll` · `+effect:sell` · `+effect:freeze_slot` (закріпити пропозицію магазину) · `+effect:summon` (призвати токен у ряд з перевіркою місця).
- `+cond:position` — місце в ряду (передній, сусід позаду).
- `+ui:trophy-counter` · `+ui:shop-bar`.
- `+window:pack-select` — вибір набору контенту.
- `+axis:time` — значення `phased`.

## Джерела
- ⭐ [Wikipedia: Super Auto Pets](https://en.wikipedia.org/wiki/Super_Auto_Pets) — підготовка/бій, 10 золота, правий проти лівого, трофей/життя/нічия, +1 життя на 3-му ході, 10 трофеїв, тири кожні 2 ходи до 6, Arena/Versus/With Friends, 7 паків; Team Wood Games, 2021.
- [Super Auto Pets Wiki: The Basics](https://superautopets.wiki.gg/wiki/The_Basics) — ціни 3/1, реролл 1 (+1 безкоштовний), freeze, 5 слотів, рівні 1–3, досвід 2+3, +1/+1 за рівень, бонус-вибір з наступного тиру, 1 перк, одночасний удар, життя за режимами, Hard Mode Toys, стрічки.
- [Super Auto Pets Wiki](https://superautopets.wiki.gg/) — улюбленці, їжа, іграшки, мана, ailments.

## Непевне
- (?) Повний список тригерів (Buy, Sell, Faint, Hurt, Start of battle, Before attack, End turn, Start of turn, Level-up, Friend summoned, Knock out) — з памʼяті; сторінку Pet Archetypes не відкривав.
- (?) Ціна продажу (1 золото за рівень (?)), кількість слотів магазину по тирах.
- (?) Порядок спрацювання Start of battle (за атакою?) — не перевірено.
- (?) Суперечність у The Basics: «на 1-му ході до 3 улюбленців» vs 5 слотів — ймовірно, це обмеження золота (10/3).
