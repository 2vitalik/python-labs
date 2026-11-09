---
title: Soulestination (魂之归宿)
slug: soulestination
aka: [魂之归宿]
family: roguelike
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: none
  goal: state
year: 2021
platforms: [PC (Windows)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1477330/Soulestination/", best: true, note: "Zaxiquej, 05.01.2021; «magic tower (fixed-value strategy RPG)» з мета-елементами: 300+ мап, 200+ ворогів зі скілами, ~30 босів, 3 складності; демо — 1-й розділ"}
  - {kind: other, url: "https://steamcommunity.com/app/1477330/reviews/?browsefilter=toprated&l=english", note: "відгуки EN: детермінований бій, скінченні HP і ключі, механіка душі, відкат до 100 рішень, мета-загадки"}
  - {kind: other, url: "https://steamcommunity.com/app/1477330/reviews/?browsefilter=toprated&l=schinese", note: "відгуки CN: 集气爆发 → 疲软, 魂缚 босів, RPG Maker, підказка у файлі"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=3489515806", note: "гайд: бос Blood Doctor з мінімумом боїв"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Soulestination+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [key-and-door, hp-damage, item-pickup, undo-redo, save-game, difficulty-levels, difficulty-select, +deterministic-combat, +soul-charge-burst, +post-burst-weakness, +boss-rule-constraint, +equip-loadout, +attribute-points, +undo-limited, +fourth-wall-puzzle, +branching-campaign, +secret-area]
proposes: ["+effect:fight(a, b)", "+effect:stat(a, name, ±n)", "+trigger:burst_end", "+effect:burst(a, dur)", "+cond:boss_rule(rule)", "+feature:undo-limited", "+feature:meta-files", "+ui:soul-gauge"]
author: opus
date: 2026-11-09
---

# Soulestination (魂之归宿) — Magic Tower з «душею»: накопичуєш заряд, вибухаєш силою на великого ворога, потім слабнеш

## Суть
Китайська інді-гра Zaxiquej на RPG Maker — «magic tower (fixed-value strategy RPG)» (див. [magic-tower](magic-tower.md)): героїня Ровія йде крізь 300+ ручних мап, бій детермінований, HP і ключі скінченні, кожен бій — торг ресурсом. Головна відмінність від ядра — **механіка душі**: у боях накопичується заряд, його розряд дає тимчасовий сплеск статів проти великого ворога, після чого героїня ослаблена. Друга — **боси «Злі Душі» з правилами** (не просто «пробий HP»), третя — **мета-загадки** в дусі Undertale/OneShot, що виходять за межі ігрового вікна.

## Поле і час
- Понад 300 ручних мап у 20+ стилях областей; секретні проходи, необовʼязкові випробування.
- Покроково; рішення (кроки/бої) можна відкотити — до 100 рішень назад.
- `random: none` — дроп «повністю невипадковий», результат бою видно наперед (відгуки).
- Деякі боси мають таймер: «стеж за пісочним годинником праворуч» (відгук CN).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Ровія | player | HP, ATK, DEF (?), атрибути, заряд душі, зброя, артефакти | ходить мапою; бій «наступанням» |
| Ворог | enemy | стати + скіли (200+ видів, десятки скілів) | під кожен скіл — своя тактика |
| Бос «Зла Душа» | boss | ~30; 魂缚 (душевні путі) — особливе правило | напр. «не вбивай інших ворогів, бо бос посилиться» |
| Двері / ключ | gate / pickup | — | ключі скінченні: відкрити баф зараз чи зберегти |
| Баф / предмет статів | pickup | — | посилення героїні |
| Зброя | pickup | десятки; можуть мати явні вади | змінює стиль (вампіризм/регенерація, підсилене закляття на кімнату) |
| Артефакт душі (Soul Artifact) | pickup | — | пасивний ефект білду |
| Секретний прохід | zone | — | веде до необовʼязкового випробування |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell)` → ТО `move(hero, dir)`.
- КОЛИ `contact(hero, enemy)` → ТО `custom: «детермінований бій за статами й скілами ворога»`, `damage(hero, n)`; ЯКЩО `hp_zero(hero)` → `lose`.
- КОЛИ `contact(hero, enemy)` → ЯКЩО `custom: «у ворога скіл»` → ТО `custom: «скіл змінює розрахунок бою»`.
- КОЛИ `died(enemy)` → ТО `counter(soul, +n)` (集气 — накопичення заряду).
- КОЛИ `input(burst)` → ЯКЩО `counter(soul, >=, n)` → ТО `set_state(hero, burst, dur)` — тимчасовий сплеск статів.
- КОЛИ `state_off(hero, burst)` → ТО `set_state(hero, weakened, dur)` (疲软 — спад після розряду).
- КОЛИ `died(enemy)` → ЯКЩО `custom: «правило боса: не вбивати зайвих»` → ТО `custom: «бос посилюється»`.
- КОЛИ `contact(hero, door)` → ЯКЩО `has(hero, key)` → ТО `take(hero, key)`, `disappear(door)`; інакше `block`.
- КОЛИ `input(undo)` → ТО `undo(n)` (n ≤ 100 рішень).
- КОЛИ `custom: «сюжетна розвилка»` → ТО `choose(options)` — наслідки постійні.
- КОЛИ `custom: «мета-загадка»` → ТО `custom: «підказка зʼявляється файлом у теці гри»`.
- КОЛИ `custom: «таймер боса вичерпано»` → ТО `custom: «наслідок бою з таймером»` (?).
- КОЛИ `died(evil_soul_boss)` → ТО `custom: «відкрито наступну область / розділ»`.
- Перемога: дійти до Святого Місця (фінал розділів). Поразка: HP = 0 → відкат або завантаження. Рахунок: нема.

## Керування і ввід
- Клавіатура RPG Maker: крок, взаємодія, меню (?); відкат рішень; збереження «частіше» (порада гравців).
- Розподіл атрибутів і вибір зброї/артефактів — у меню між боями.

## Вікна, меню, HUD
- `game-screen` — мапа, стати, заряд душі (`+ui:soul-gauge`) (?), пісочний годинник на бос-бою.
- `inventory-window` — зброя й артефакти душі (з описом вад).
- `difficulty-select` — три складності (у т. ч. Easy/Normal); у відгуках — тонке налаштування чисел.
- `save-slots` — збереження; `dialogue-window` — сюжет і розвилки.
- `main-menu`, `end-screen`, `settings-window` (?).

## Фічі поза полем
- `undo` до 100 рішень + ручні сейви.
- `difficulty-presets` (3) і числове налаштування складності.
- Мета: підказки й загадки поза вікном гри (файли в теці) — `+feature:meta-files`.
- `achievements`, `cloud-save`, картки Steam; `localization` (EN, CN; переклад EN нерівний).

## Варіації й родичі
- [magic-tower](magic-tower.md) — ядро; [requiem-of-reuinis](requiem-of-reuinis.md) — наступна гра Zaxiquej (добовий цикл, алхімія); [tactical-nexus](tactical-nexus.md), [h5mota](h5mota.md) — сучасні вежі; [desktop-dungeons](desktop-dungeons.md) — порівнюють за духом.
- Відмінність від класики: заряд душі як ресурс таймінгу, боси з правилами замість «стіни статів», мета-загадки, сюжетні розвилки.
- Осі варіацій: **сплеск сили** (нема / розряд душі зі спадом) · **бос** (стати / правило-обмеження) · **відкат** (сейви / N рішень) · **загадки** (у грі / поза вікном).

## Цікавинки для курсу
- Заряд → розряд → спад: тимчасовий стан із «відкатом» після — 📎 (дві фази `set_state`).
- Бос із правилом «не вбивай зайвих» — обмеження на маршрут, а не на стати — 🌱.
- Відкат до 100 рішень (кільцевий буфер станів) — 📎.
- Мета-загадка: гра пише файл-підказку в теку — 🌱 (файловий ввід/вивід як механіка).
- Мінімізація кількості боїв на мапі боса (гайд Blood Doctor) — 🥈 (пошук шляху з обмеженням на бої).

## Мапа на каталог
- Є: `key-and-door` · `hp-damage` · `item-pickup` · `undo-redo` (до 100 рішень) · `save-game` · `difficulty-levels` + `difficulty-select`.
- **Нема** → пропозиції карток:
  - `+soul-charge-burst` «Заряд від боїв → тимчасовий сплеск сили» · entities/state · 📎.
  - `+post-burst-weakness` «Після сплеску — спад» · entities/state · 🌱.
  - `+boss-rule-constraint` «Бос з умовою на маршрут/бої» · entities/combat · 🌱.
  - `+attribute-points` «Розподіл очок атрибутів» · entities/state · 🌱.
  - `+undo-limited` «Undo на N кроків (кільцевий буфер)» · game-logic/history · 📎 (дитина `undo-redo`).
  - `+fourth-wall-puzzle` «Загадка поза вікном гри (файли, назва вікна)» · interface/meta · 🥉.
  - `+deterministic-combat`, `+equip-loadout`, `+branching-campaign`, `+secret-area` — уже пропоновані корпусом.

## Пропозиції до словників
- `+effect:fight(a, b)` — атомарний детермінований бій.
- `+effect:stat(a, name, ±n)` — змінити стат.
- `+effect:burst(a, dur)` — розрядити накопичений заряд у тимчасові стати (зараз — `set_state` + `counter`).
- `+trigger:burst_end` — сплеск закінчився (зараз — `state_off`).
- `+cond:boss_rule(rule)` — діє обмеження боса.
- `+feature:undo-limited` — undo з глибиною N.
- `+feature:meta-files` — гра пише/читає файли поза вікном як частину загадок.
- `+ui:soul-gauge` — шкала заряду.

## Джерела
- ⭐ [Steam: Soulestination](https://store.steampowered.com/app/1477330/Soulestination/) — жанр, 300+ мап, 200+ ворогів зі скілами, ~30 босів, зброя й артефакти, 3 складності, мета-загадки, постійні наслідки вибору.
- [Steam: відгуки EN](https://steamcommunity.com/app/1477330/reviews/?browsefilter=toprated&l=english) — детермінізм, скінченні HP/ключі, механіка душі, боси з правилами, відкат до 100 рішень, Easy/Normal.
- [Steam: відгуки CN](https://steamcommunity.com/app/1477330/reviews/?browsefilter=toprated&l=schinese) — 集气爆发/疲软, 魂缚, пісочний годинник, підказка у теці, RPG Maker.
- [Steam-гайд: Blood Doctor minimal fights](https://steamcommunity.com/sharedfiles/filedetails/?id=3489515806) — маршрут боса з мінімумом боїв.

## Непевне
- (?) Точна формула бою й чи це класичне «ceil(HP/(ATK−DEF))» — у джерелах лише «фіксовані значення».
- (?) Як саме накопичується й розряджається душа (за вбивство чи за бій; вручну чи автоматично) — відгуки описують загально.
- (?) Пісочний годинник і «каратель» (punisher) у бою Blood Doctor — механіка таймера не описана.
- (?) Розміри мап, рухливість ворогів (`opponent: ai` поставлено через скіли й боси з таймером).
- (?) Чи є прогноз втрат на іконках ворогів, як у H5-веж.
