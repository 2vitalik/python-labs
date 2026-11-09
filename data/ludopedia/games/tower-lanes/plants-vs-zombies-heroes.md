---
title: Plants vs. Zombies Heroes
slug: plants-vs-zombies-heroes
aka: [PvZ Heroes, PvZH, "Рослини проти зомбі: Герої"]
family: tower-lanes
also: []
klass: cursor
axes:
  field: square
  time: turn
  opponent: online
  info: hidden
  random: both
  goal: state
year: 2016
platforms: [iOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Plants_vs._Zombies_Heroes", best: true, note: "5 смуг (висота й вода в ranked), Team-Up, ліміт 2 карти на смугу, 4 фази ходу, сонце/мізки, блок-метр 8 поділок, суперсили, колода 40, сети"}
  - {kind: fandom, url: "https://plantsvszombies.wiki.gg/wiki/Plants_vs._Zombies_Heroes", note: "PvZ Wiki (wiki.gg): 20 HP героя, +1 ресурс щоходу, бій зліва направо, зомбі б'є першим, рука 10, 4 копії, трейти, класи"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=plants+vs+zombies+heroes+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [hp-damage, round-currency, cursor-place, drag-drop-piece, pocket, inventory-limit, piece-capture, status-effects, explode-area, ai-opponent, online-multiplayer, rating-system, mode-select, match-setup, character-select, tutorial-window, end-screen, shop-window, +lane-grid, +deck-draw, +ramping-energy, +lane-types, +amphibious-lane, +team-up-stack, +lane-capacity, +asymmetric-phases, +hidden-play-reveal, +left-to-right-resolve, +block-meter, +superpower-cards, +card-traits, +class-pair-hero, +deck-builder, +card-collection, +card-rarity, +daily-challenge]
proposes: ["+trigger:card_played", "+trigger:blocked_hit", "+cond:lane_type", "+cond:lane_has", "+cond:trait", "+effect:draw_card", "+effect:block_hit", "+effect:bounce_card", "+effect:reveal_gravestone", "+role:card", "+role:hero", "+role:lane", "+ui:block-meter", "+ui:lane-badge", "+ui:phase-banner", "+window:deck-builder", "+window:collection-window", "+feature:card-collection", "+axis:turn-structure=phased-asymmetric", "+card:team-up-stack", "+card:block-meter"]
author: opus
date: 2026-11-09
---

# Plants vs. Zombies Heroes — карткова дуель на п'яти смугах, де зомбі ходять першими, а рослини відповідають

## Суть
Колекційна карткова гра у світі [plants-vs-zombies](plants-vs-zombies.md): двоє гравців — герой рослин і герой зомбі — по черзі викладають бійців у **5 смуг** між героями. Фази ходу **асиметричні**: зомбі ставлять бійців першими, рослини бачать це й відповідають, потім зомбі грають трюки, і лише тоді бій. Смуги мають типи — **висота** (Heights), **вода** (лише Amphibious) і земля; рослини-**Team-Up** можуть стати вдвох в одну смугу. Мета — звести 20 HP ворожого героя до нуля; герой час від часу **блокує** удар і отримує суперсилу.

## Поле і час
- Поле — 5 смуг, кожна з клітиною зомбі й клітиною рослин; герої — по краях смуг (рослинний герой ліворуч поля (?)). Фактично сітка 2×5 зі слотами.
- Типи смуг (ranked): крайня ліва — **висота** (Heights), три середні — земля, крайня права — **вода**. У воду грають лише бійці з Amphibious.
- Місткість: до 2 карт на смугу на бік, з яких щонайбільше 1 — Team-Up; Team-Up є лише в рослин.
- Хід (раунд) — 4 фази: **Zombies Play** → **Plants Play** (рослини, трюки, середовища) → **Zombie Tricks** (трюки й середовища зомбі) → **Fight!**.
- Бій розвʼязується смугами зліва направо; у кожній смузі **зомбі б'є першим**.
- Ресурс: сонце (рослини) і мізки (зомбі) — +1 до максимуму щоходу, ресурс відновлюється щоходу.
- Інформація прихована (рука, колода, Gravestone); випадковість — у колоді, блок-метрі й ефектах карт.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой рослин / зомбі | player (`+role:hero`) | 20 HP, блок-метр 8 поділок, 2 класи, 4 суперсили | отримує шкоду від незаблокованих бійців; блокує до 3 разів за гру |
| Боєць (Fighter) | ally (`+role:card`) | ціна, сила, здоров'я, трейти, клас | стоїть у смузі до знищення; б'є бійця навпроти або героя |
| Трюк (Trick) | supply (`+role:card`) | ціна | одноразовий ефект (шкода, бафф, переміщення, знищення) |
| Середовище (Environment) | terrain (`+role:card`) | ціна | кладеться на смугу, змінює правила в ній; нове замінює старе (?) |
| Суперсила | supply | ціна 1 | особливий трюк героя; 1 на старті, решта — за блок |
| Смуга землі | zone (`+role:lane`) | — | звичайна |
| Смуга висоти (Heights) | zone | — | окремі карти мають бонус/обмеження «на висоті» (?) |
| Смуга води | zone | — | лише Amphibious |
| Gravestone-зомбі | enemy | прихований | грається «надгробком»; розкривається у фазі трюків зомбі (?) |
| Team-Up-рослина | ally | — | може стати у смугу, де вже є рослина |
| Сонце / мізки | resource | макс. +1 щоходу | плата за карти |
| Рука | supply | ліміт 10 | понад ліміт — лише через Bounce |
| Колода | supply | рівно 40 + 4 суперсили, ≤4 копії | добір щоходу (?) |

Трейти бійців: Amphibious, Anti-Hero, Armored, Bullseye, Deadly, Double Strike, Frenzy, Gravestone, Hunt, Overshoot, Splash Damage, Strikethrough, Team-Up, Untrickable.

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(both)` → ТО `custom: «макс. сонця/мізків +1, ресурс поповнено»`, `custom: «добір карти»` (?).
- КОЛИ `phase_start(zombies_play)` → ТО гравець-зомбі `input(play, fighter, lane)`; рослини ще не діють.
- КОЛИ `phase_start(plants_play)` → ТО гравець-рослини грає бійців, трюки й середовища — вже бачачи зомбі.
- КОЛИ `phase_start(zombie_tricks)` → ТО гравець-зомбі грає трюки й середовища; `custom: «Gravestone-зомбі розкриваються»` (?).
- КОЛИ `input(play, card, lane)` → ЯКЩО `has(sun|brains, cost)` → ТО `currency(−cost)`, `place(card, lane)`.
- КОЛИ `input(play, fighter, lane)` → ЯКЩО `cell(lane, water)` and `custom: «боєць без Amphibious»` → ТО `block`.
- КОЛИ `input(play, plant, lane)` → ЯКЩО `occupied(lane, plant)` → ТО ЯКЩО `custom: «одна з двох рослин Team-Up і в смузі ще нема двох»` → ТО `place`, інакше `block`.
- КОЛИ `phase_start(fight)` → ТО для смуг зліва направо: `custom: «зомбі бʼє першим, потім рослина»`; ціль — боєць навпроти, а якщо його нема — ворожий герой.
- КОЛИ `custom: «боєць б'є бійця»` → ТО `damage(strength)`; КОЛИ `hp_zero(fighter)` → ТО `disappear_b`.
- КОЛИ `custom: «удар по герою»` → ЯКЩО `custom: «атакувальник без Bullseye»` → ТО `counter(block_meter, +rng(1..3))`; ЯКЩО `counter(block_meter, ≥, 8)` and `custom: «блоків < 3»` → ТО `custom: «шкоду ігноровано»`, `give(hero, superpower)`, `counter(block_meter, =0)`.
- КОЛИ `custom: «удар по герою не заблоковано»` → ТО `damage(hero, strength)`.
- КОЛИ `input(play, superpower)` → ЯКЩО `has(sun|brains, 1)` → ТО ефект суперсили.
- Трейти: Strikethrough — `damage` усім у смузі, включно з героєм; Deadly — знищує будь-якого бійця, якому завдав шкоди; Frenzy — `extra_move` атаки після знищення бійця; Double Strike — бʼє двічі; Splash Damage — шкода і сусіднім смугам/цілям; Overshoot — бʼє героя до бою; Anti-Hero — більше шкоди герою; Armored N — `custom: «шкода −N»`; Untrickable — трюки суперника не діють; Hunt — `custom: «переходить у смугу, куди суперник щойно зіграв бійця»` (?).
- КОЛИ `input(play, environment, lane)` → ТО `custom: «середовище змінює правила смуги для обох сторін»`.
- КОЛИ `custom: «Bounce»` → ТО `custom: «боєць повертається в руку»` — так рука може перевищити 10.
- КОЛИ `hp_zero(hero)` → ТО `lose` для власника, `win` супернику.
- Перемога: звести HP ворожого героя з 20 до 0 · Поразка: власний герой на 0 · Рахунок: рейтинг у ranked.

## Керування і ввід
- Тач: drag карти з руки на смугу (`drag-drop-piece`), підсвічуються легальні смуги; tap по карті — збільшений перегляд з трейтами.
- Кнопка «Готово» завершує свою фазу; суперсили — окремі карти в руці.
- Між боями — редактор колоди: фільтр за класом героя, рідкістю, ціною.

## Вікна, меню, HUD
- `main-menu` → `mode-select`: місії рослин/зомбі (кампанія), multiplayer (casual, ranked), Today's Challenge (щоденний), Random Battle.
- `character-select` — 11 героїв на бік, кожен з двома класами.
- `+window:deck-builder` — колода рівно 40, ≤4 копії, лише класи героя; `+window:collection-window` — колекція карт, рідкість, сети.
- `shop-window` — паки карт; нагороди-квитки за перемоги.
- `game-screen`: 5 смуг з `+ui:lane-badge` (висота/вода/земля), портрети героїв з HP і `+ui:block-meter`, лічильник сонця/мізків, рука (`pocket`), `+ui:phase-banner` (чия фаза), кнопка завершення фази.
- `end-screen`: перемога/поразка, рейтинг, нагороди.
- `tutorial-window` — навчальні бої на старті кампанії.

## Фічі поза полем
- `card-collection`: сети Premium (190), Galactic Gardens (100), Colossal Fossils (50), Triassic Triumph (50); рідкості; базові карти відкриваються з класом.
- Герої як «двокласні» колоди: клас визначає, які карти дозволено.
- Ranked з сезонами, casual, бої з AI, щоденний виклик, події з квитками (15 за онлайн-перемогу, 10 — офлайн).
- Кампанія місій рослин і зомбі з особливими умовами боїв (?).

## Варіації й родичі
- У корпусі: [plants-vs-zombies](plants-vs-zombies.md) (смуги, Amphibious/вода, той самий бестіарій), [pvz-puzzle-modes](pvz-puzzle-modes.md) (I, Zombie — гра за зомбі), [inscryption](inscryption.md) (карти в колонках-смугах, удар у порожнє — по шкалі), [marvel-snap](marvel-snap.md) (локації з модифікаторами), [clash-royale](clash-royale.md) (ресурс, що росте, колода).
- Hearthstone — найближчий карткове-структурний родич (герой з HP, мана +1 щоходу, суперсила-hero power), але без смуг.
- Осі варіацій:
  - **поле карткової гри**: без позицій (Hearthstone) / смуги «один на один» (PvZH, Inscryption) / локації з потужністю (Marvel Snap);
  - **порядок ходу**: сторони по черзі / одночасне розкриття (Snap) / **асиметричні фази**: зомбі ставлять → рослини відповідають → зомбі трюки → бій (PvZH);
  - **тип смуги**: однакові / вода з дозволом за трейтом / висота / середовище, що кладе гравець;
  - **захист героя**: нема / броня / **випадковий блок-метр з нагородою** (PvZH).

## Цікавинки для курсу
- Асиметричні фази ходу (одна сторона ставить наосліп, інша відповідає, потім трюки) — 📎 (машина станів фаз).
- Смуги з типами + місткість (2 на смугу, 1 Team-Up, вода лише Amphibious) як правило легальності ходу — 🌱.
- Бій зліва направо, зомбі першим у смузі; удар у порожню смугу — по героєві — 🌱.
- Блок-метр: випадковий приріст 1–3 з 8, макс. 3 блоки, нагорода-суперсила — 🌱.
- Трейти як прапорці бійця (Strikethrough, Deadly, Frenzy, Armored…) і порядок їх обробки — 🥉.
- Редактор колоди з обмеженнями (40 карт, ≤4 копії, класи героя) — 📎.

## Мапа на каталог
- Є: `hp-damage` · `round-currency` ↔ сонце/мізки · `cursor-place` + `drag-drop-piece` ↔ карта на смугу · `pocket` ↔ рука · `inventory-limit` ↔ рука 10 · `piece-capture` ↔ знищення бійця · `status-effects` ↔ трейти-стани · `explode-area` ↔ Splash · `ai-opponent` · `online-multiplayer` · `rating-system` · `mode-select` · `character-select` ↔ вибір героя · `tutorial-window` · `shop-window` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+lane-grid` (з PvZ), `+deck-draw` (з Clash Royale), `+ramping-energy` (з Marvel Snap), `+deck-builder`, `+card-collection`.
  - `+lane-types` «Смуги з типами (висота/вода/земля)» · entities/legality · 🌱.
  - `+amphibious-lane` «Смуга лише для бійців з трейтом» · entities/legality · 🌱.
  - `+team-up-stack` «Дві карти в одній смузі за трейтом» · entities/legality · 🌱 · слоти {capacity: 2, team_up_max: 1}.
  - `+asymmetric-phases` «Фази ходу різні для сторін» · game-logic/opponent · 📎.
  - `+hidden-play-reveal` «Gravestone: карта лежить прихованою до фази» · entities/state · 📎.
  - `+left-to-right-resolve` «Бій смугами зліва направо, атакувальник першим» · entities/combat · 🌱.
  - `+block-meter` «Випадковий блок-метр героя з нагородою» · entities/state · 🌱 · слоти {size: 8, step: 1..3, max_blocks: 3}.
  - `+superpower-cards`, `+card-traits`, `+class-pair-hero`, `+card-rarity`, `+daily-challenge`.

## Пропозиції до словників
- `+trigger:card_played(card, lane)` — зіграно карту (для Hunt і реакцій); `+trigger:blocked_hit(hero)` — герой заблокував удар.
- `+cond:lane_type(lane, type)` — тип смуги (висота/вода/земля); `+cond:lane_has(lane, kind)` — у смузі вже є карта; `+cond:trait(a, t)` — у бійця трейт.
- `+effect:draw_card` — добір; `+effect:block_hit(hero)` — ігнорувати шкоду й дати суперсилу; `+effect:bounce_card(a)` — повернути бійця в руку; `+effect:reveal_gravestone` — відкрити приховані карти.
- `+role:card` · `+role:hero` (герой поза смугами з HP) · `+role:lane`.
- `+ui:block-meter` — 8 поділок під портретом; `+ui:lane-badge` — значок типу смуги; `+ui:phase-banner` — банер поточної фази.
- `+window:deck-builder` · `+window:collection-window` (вибір героя — наявний `character-select`).
- `+feature:card-collection` — колекція карт з рідкістю й сетами; щоденний виклик — наявний `mode-daily`.
- `+axis:turn-structure=phased-asymmetric` — фази ходу різні для сторін.
- `+trigger:phase_start` вже ✅ (🔥) — використано без пропозиції.
- `+card:team-up-stack`, `+card:block-meter`.

## Джерела
- ⭐ [Wikipedia: Plants vs. Zombies Heroes](https://en.wikipedia.org/wiki/Plants_vs._Zombies_Heroes) — 5 смуг, ліва — висота, права — вода (ranked), Amphibious, ліміт 2 карти/смугу з 1 Team-Up (лише рослини), 4 фази, сонце/мізки, колода 40, блок-метр 8 поділок (+1/2/3, крім Bullseye, до 3 разів), 4 суперсили, 11 героїв на бік, сети, квитки.
- [PvZ Wiki (wiki.gg)](https://plantsvszombies.wiki.gg/wiki/Plants_vs._Zombies_Heroes) — 20 HP героя, суперсила за 1, +1 ресурс щоходу, бій зліва направо й зомбі першим, рука 10 і Bounce, ≤4 копії, трейти, класи, режими.
- YouTube: пошук «plants vs zombies heroes gameplay».

## Непевне
- (?) Правила смуги Heights (чим вона відрізняється, крім того, що окремі карти посилаються на неї) — сторінки вікі про висоту/Gravestone не знайшлись (404).
- (?) Gravestone: момент розкриття (початок фази Zombie Tricks) і недоступність для трюків рослин — з памʼяті.
- (?) Добір карти щоходу, Hunt, Overshoot (на вікі позначено «unused icon»), Splash — формулювання з памʼяті.
- (?) Що саме відбувається з рештою бою в смузі після блоку героя.
- (?) Хто з героїв ліворуч/праворуч на екрані.
