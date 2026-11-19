---
title: Watchword
slug: watchword
aka: []
family: word-number
also: [roguelike]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: partial
  random: both
  goal: score
year: 2025
platforms: [PC, macOS, Linux]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2906730/Watchword/", best: true, note: "опис: мішок фігур (одинарні, подвійні, металеві, глючні, золоті), книги-реліквії, Watchword розширює дошку, Форум, Вартові; знімки"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=TaBdBq5k_PQ", note: "Watchword: Official Gameplay Trailer"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=8MtKC6k-SGs", note: "трейлер релізу (зі статті GamingOnLinux)"}
  - {kind: steam, url: "https://store.steampowered.com/app/3606170/", note: "безкоштовне демо: біграми QU / CH / EE, символи ! ? &, 8 Вартових, 15 апгрейдів забігу"}
  - {kind: other, url: "https://www.gamingonlinux.com/2025/05/watchword-gives-the-balatro-treatment-to-an-anagram-word-game/", note: "анонс: 120+ книг, 20+ Вартових (Greedy, Patient), 30+ апгрейдів доборів, скидань, руки"}
  - {kind: other, url: "https://www.gamingonlinux.com/2025/09/use-rule-bending-books-to-build-a-massive-score-in-anagram-roguelike-watchword-out-now/", note: "реліз: 80+ книг, редагування книг, вигадані слова через заборонені книги"}
  - {kind: other, url: "https://steamcommunity.com/stats/2906730/achievements", note: "досягнення: складності Normal / Hard / Challenge / Insane, Blackout — дошка без порожніх клітин"}
  - {kind: other, url: "https://steamcommunity.com/app/2906730/discussions/0/594030683912108524/", note: "гравці: дошка 4×4, 2 раунди, 2 добори, ціль 200+ на Hard; Watchword відкриває дошку"}
stage: v1
coverage: 50
mechanics: [word-validation, move-limit, run-relics, shop-between-levels, shop-catalog, shop-buyback, round-currency, permadeath, difficulty-levels, keep-playing-after-win, achievements-window, stats-window, game-screen, shop-window, +tile-bag-draw, +tile-rack, +tile-exchange, +target-score-rounds, +deck-builder, +special-letter-tiles, +multi-letter-face, +boss-fight, +growing-board, +shop-reroll, +meta-unlocks, +ascension-levels, +tile-retrigger, +base-times-mult, +score-board-at-round-end, +dictionary-bypass, +relic-edit, +boss-bribe, +symbol-tiles]
proposes: ["+effect:draw", "+effect:discard", "+effect:retrigger", "+effect:reroll", "+ui:target-score", "+ui:hand-slots", "+window:town-hub", "+window:loadout-select", "+axis:session=run"]
author: opus
date: 2026-11-19
---

# Watchword — анаграм-роглайк: тягни фігури-літери з мішка, клади слова кросвордом, раунд рахує всю дошку; слово-ключ розширює поле

## Суть
Роглайк-декбілдер про слова: з власного мішка фігур-літер тягнеш піддон (руку), викладаєш фігури на квадратну дошку так, щоб утворились слова, і в кінці раунду гра рахує кожне слово на дошці як «marks × amp». За кілька раундів треба набрати ціль випробування (trial), яке ускладнює Вартовий (Watchguard) зі своїм правилом. Між випробуваннями — Форум: магазин книг-реліквій (до 6), що ламають правила (наприклад, остання літера не перевіряється словником — так зʼявляються вигадані слова), і майстерні фігур. Особлива механіка — Watchword забігу: якщо скласти це слово на дошці, дошка росте для наступних випробувань.

## Поле і час
- Квадратна дошка: у гравців на Hard — 4×4, на знімках — 7×7; мішок Lettercase стартує з більшою дошкою; Watchword розширює її.
- Фігури лягають у клітини; слова читаються рядками й стовпцями, кросвордом (на знімках TABS / NINETY / DENTS / TALE перетинаються).
- Випробування = кілька раундів (на знімку Rounds 3); у раунді — добори піддона (Draws) і скидання (Discards); підрахунок у кінці раунду кнопкою «Scoring…» з анімацією, швидкість .75×–2×.
- Забіг: «Trial x/16» або «x/20» на знімках; після перемоги — Endless.
- Покроково, без таймера.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фігура-літера | tile | літера, marks | з піддона на клітину; назад у піддон не повертається |
| Подвійна фігура (біграм) | tile | QU, CH, EE … | дві літери на одній фігурі |
| Символ | tile | ! ? & | незвичні здібності (?) |
| Металева фігура | tile | — | дублікати міняються незалежно (?) |
| Глючна фігура | tile | символи | дають мішок Chip Bag і книга Spellbook |
| Золота фігура | tile | — | (?) |
| Постійна фігура | tile | — | не скидається |
| Мішок | supply | склад гравця | джерело добору; скинута фігура повертається в мішок |
| Піддон (рука) | supply | слоти, частина замкнена | розмір росте апгрейдами |
| Дошка | zone | N×N | слова кросвордом; росте від Watchword |
| Книга | pickup | Common … Mythic, ≤ 6, редагована | пасивна сила; часто ламає правило |
| Вартовий | boss | стратегія | Patient — 1 добір за хід; Greedy — можна відкупитися; Mercurial (?) |
| Watchword | mark | слово забігу (на знімках PURCHASE, GRUMES; у гравця — COCA) | складене на дошці — дошка більшає |
| Прокляття | hazard | duplicate / destroy | (?) |
| Ціль випробування | static | Goal to Pass | Trial Total ≥ ціль — пройдено |
| Золото | resource | — | валюта Форуму; хабар Вартовому |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(Draw Tray)` → ЯКЩО `counter(draws, >, 0)` → ТО `custom: «піддон поповнюється фігурами з мішка»`, `counter(draws, −1)`.
- КОЛИ `input(drag piece → cell)` → ЯКЩО `free(cell)` → ТО `place(player, piece)`; `custom: «фігура лишається на дошці»`.
- КОЛИ `input(Discard Piece | на мішок)` → ЯКЩО `counter(discards, >, 0)` і `not state(piece, permanent)` → ТО `custom: «фігура йде в мішок»`, `counter(discards, −1)`; скидань нема → `custom: «штраф скидання застосовується одразу»`.
- КОЛИ `input(Scoring)` → ЯКЩО `in_dictionary(кожне слово ряду / стовпця)` → ТО `score(marks × amp)` за кожне; нове для гравця слово → `message("New Word Found")`.
- КОЛИ `after(score)` → ЯКЩО `custom: «книга спрацьовує на цьому слові»` → ТО `counter(marks, +n)` / `multiplier(amp)` / `custom: «повторне спрацювання»`.
- КОЛИ `counter(trial_total, >=, goal)` → ТО `currency(+gold)`, `window(custom-window)` (Форум), наступне випробування.
- КОЛИ `counter(rounds, ==, 0)` → ЯКЩО `counter(trial_total, <, goal)` → ТО `lose`, `game_over` (забіг втрачено).
- КОЛИ `custom: «на дошці складено Watchword»` → ТО `grow(board, n)` для наступних випробувань.
- Вартові: Patient → `custom: «добір за хід = 1»`; Greedy → `custom: «відкупитися золотом»` (`currency(−n)`); хабар — меню з фігурами.
- Книги-приклади: The Finalist → `custom: «остання літера слова не перевіряється словником»`; The Sniper → `custom: «мінімальна довжина слова 4»`; Banana Brad → `custom: «повторна літера спрацьовує ще раз за кожну копію»`; Slot Machine Manual Mk2 → КОЛИ `custom: «зіграно фігуру з G-A-M-B-L-E»` → ЯКЩО `prob(1/3)` → ТО `currency(+2)` або `multiplier(+3 amp)` або нічого; Madam I'm Adam / Leafy House — спрацювання за паліндромом і орієнтацією слова.
- Перемога: пройти всі випробування забігу (далі Endless) · Поразка: ціль не набрано за раунди · Рахунок: Σ marks × amp по словах дошки; досягнення Blackout — дошка без порожніх клітин.

## Керування і ввід
- Миша: тягнути фігуру з піддона на клітину; кинути фігуру на мішок — скинути; кнопки Discard Piece, Draw Tray, Scoring…; перемикач швидкості підрахунку.
- Форум — нижня панель станцій-іконок; клік по станції; редагування книг; підказки (tooltip) фігур у мішку й у меню хабара.
- Геймпад — не перевірено (?).

## Вікна, меню, HUD
- `game-screen`: верх — ряд книг (6/6), золото, «Trial x/16», Watchword забігу; ліворуч — лічильники Discards / Draws / Rounds, піддон із замкненими слотами, кнопки; праворуч — слово, що рахується («TALE 9», «GRAILE 15 × 2!»), портрет і тип Вартового з `tooltip`, Trial Total, Goal to Pass, «Scoring…», швидкість; `toast` «New Word Found».
- Форум (`custom-window`, хаб зі станціями): Buybrary (`shop-window`: книги з цінами, «Reroll Stock» за 2 золота), пошта, майстерня заклинань («Unstable Spell — 50/50»), «Edit Books» («I'm Feeling Inspired by a Word»), різьбяр біграм-тегів, портал до наступного випробування (ціль і Вартовий).
- Старт забігу: вибір мішка (Lettercase, Handbag, Chip Bag, Pocket Dimension) і складності (Normal, Hard, Challenge, Insane; вищі відкриває перемога); `stats-window`; `achievements-window` (17); туторіал (демо); меню хабара Вартовому.
- Переходи: випробування → Форум → портал → наступне випробування; поразка → кінець забігу.

## Фічі поза полем
- `meta-progression` / `unlockables`: стартові мішки, рівні складності, книги, приховане.
- `difficulty-presets`, що відкриваються перемогами; `mode-endless` після перемоги (рахунки до сотень мільярдів).
- `stats`, `achievements` (17), `cloud-save`, `speed-control` підрахунку.
- Словник EN 100 000+ слів; форма пропозиції слова; фільтр лайки; заплановано власні словники й локалізацію.
- Демо з обмеженим набором книг і апгрейдів.

## Варіації й родичі
- Корпус: Wordatro (`wordatro.md` — Balatro зі словами без дошки), Beyond Words (`beyond-words.md` — дошка Scrabble з фігурними полями), Scrabble (`scrabble.md`), Bananagrams (`bananagrams.md` — кросворд з власних плиток), WordTactics (`wordtactics.md`), Bookworm Adventures (`bookworm-adventures.md`).
- Поза сімʼєю: Balatro (книги ≈ джокери, marks × amp ≈ chips × mult).
- **Осі варіацій:** коли рахується (за хід / уся дошка в кінці раунду) · дошка (фіксована / росте від слова-ключа) · словник (жорсткий / книги знімають перевірку) · фігури (одна літера / біграми / символи) · «суперник» (лише ціль / Вартовий-модифікатор).

## Цікавинки для курсу
- Підрахунок усієї дошки: знайти всі рядкові й стовпцеві слова, перевірити словником, скласти marks × amp — 🥉.
- Книги-реліквії як ланцюг модифікаторів, що можуть зняти перевірку словника чи змінити мінімальну довжину — 🥉.
- Дошка, що росте від спеціального слова забігу — 📎.
- Мішок + піддон + добори / скидання як ресурси раунду — 📎.
- Вартовий як модифікатор правил випробування (1 добір за хід, відкуп золотом) — 📎.
- Хаб між рівнями зі станціями (магазин з reroll, редагування книг, різьбяр) — 🥉.

## Мапа на каталог
- Є: `word-validation` · `move-limit` ↔ раунди випробування · `run-relics` ↔ книги · `shop-between-levels` + `shop-catalog` + `shop-buyback` (продаж книг за меншу ціну) + `round-currency` ↔ Форум і золото · `permadeath` · `difficulty-levels` · `keep-playing-after-win` ↔ Endless · `achievements-window` · `stats-window` · `game-screen` · `shop-window`.
- **Нема** → пропозиції карток:
  - Уже в корпусі: `+tile-bag-draw`, `+tile-rack` (піддон), `+tile-exchange` (скидання), `+target-score-rounds`, `+deck-builder` (мішок), `+special-letter-tiles`, `+multi-letter-face` (біграми), `+boss-fight` (Вартові), `+growing-board`, `+shop-reroll`, `+meta-unlocks`, `+ascension-levels`.
  - `+tile-retrigger`, `+base-times-mult` — див. `beyond-words.md` (тут marks × amp).
  - `+score-board-at-round-end` «Рахунок усієї дошки в кінці раунду» · game-logic/score · 🥉.
  - `+dictionary-bypass` «Реліквія знімає перевірку словника» · game-logic/constraints · 📎.
  - `+relic-edit` «Редагування значень реліквії» · game-logic/economy · 📎.
  - `+boss-bribe` «Відкуп від боса валютою» · game-logic/economy · 🌱.
  - `+symbol-tiles` «Плитки-символи зі здібностями» · entities/state · 📎.

## Пропозиції до словників
- `+effect:draw` — добір фігур з мішка в піддон.
- `+effect:discard` — скинути фігуру в мішок (лічильник скидань).
- `+effect:retrigger` — книга чи літера спрацьовує ще раз.
- `+effect:reroll` — оновити вітрину Buybrary.
- `+ui:target-score` — Goal to Pass поруч із Trial Total.
- `+ui:hand-slots` — піддон із замкненими слотами.
- `+window:town-hub` — Форум: хаб зі станціями між випробуваннями.
- `+window:loadout-select` — вибір стартового мішка.
- `+axis:session=run` — забіг з випробувань і permadeath.

## Джерела
- ⭐ [Steam: Watchword](https://store.steampowered.com/app/2906730/Watchword/) — опис, теги (Perma Death), Форум, книги, Watchword; знімки інтерфейсу випробування й Форуму.
- [Steam: демо](https://store.steampowered.com/app/3606170/) — біграми, символи, 8 Вартових, 15 апгрейдів.
- Новини Steam (патчі 0.6–1.1.3) — книги з числами (The Finalist, The Sniper, Banana Brad, Slot Machine Manual Mk2), Patient / Greedy Watchguard, хабар, скидання без запасу = штраф, мішки Lettercase / Handbag / Chip Bag, складність Challenge, 6 слотів книг і рідкості.
- [GamingOnLinux: анонс](https://www.gamingonlinux.com/2025/05/watchword-gives-the-balatro-treatment-to-an-anagram-word-game/) і [реліз](https://www.gamingonlinux.com/2025/09/use-rule-bending-books-to-build-a-massive-score-in-anagram-roguelike-watchword-out-now/) — кількості книг / Вартових / апгрейдів, трейлери.
- [Steam: обговорення](https://steamcommunity.com/app/2906730/discussions/0/594030683912108524/) — 4×4, 2 раунди, 2 добори, ціль 200+.
- [Steam: досягнення](https://steamcommunity.com/stats/2906730/achievements) — складності, Blackout, marks.
- YouTube: [Official Gameplay Trailer](https://www.youtube.com/watch?v=TaBdBq5k_PQ).

## Непевне
- (?) Чи мусить нове слово торкатися вже викладених фігур (звʼязний кросворд) — правило викладання не знайдено; на знімках слова перетинаються.
- (?) Як обирається Watchword (вибір на старті забігу прибрали в 0.10.0) і на скільки клітин росте дошка.
- (?) Що саме дають металеві, золоті, глючні фігури й символи ! ? &.
- (?) Скільки випробувань у забігу (на знімках 16 і 20) і від чого це залежить.
- (?) Вартовий Mercurial і прокляття duplicate / destroy — лише згадки.
- (?) Мінімальна довжина слова без книг (книга The Sniper піднімала її «з 3 до 4»).
