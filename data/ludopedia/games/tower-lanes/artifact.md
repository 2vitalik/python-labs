---
title: Artifact
slug: artifact
aka: [Artifact Classic, Artifact Foundry, Artifact 2.0]
family: tower-lanes
also: []
klass: cursor
axes:
  field: 1d
  time: turn
  opponent: online
  info: hidden
  random: both
  goal: state
year: 2018
platforms: [PC, macOS, Linux]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Artifact_(video_game)", best: true, note: "три окремі дошки-смуги з вежами, Ancient, мана кожної смуги, ініціатива за карту, крипи, крамниця, кольори, Artifact 2.0 → Foundry"}
  - {kind: steam, url: "https://store.steampowered.com/app/583950/Artifact/", note: "Classic і Foundry; у Foundry — усі смуги одночасно, спільна мана, менше випадковості, Hero Draft, PvE"}
  - {kind: other, url: "https://steelseries.com/en-hk/blog/artifact-blog-77", note: "гайд: вежа 40 HP, Ancient 80, фази Deployment/Action/Shopping, 2 крипи у випадкові смуги, ініціатива, 3 крамниці, +5/+1 золота"}
  - {kind: other, url: "https://destructoid.com/?p=236990", note: "кольори й класи, до 2 героїв за раунд наосліп, сигнатурні закляття ×3, Siege/Piercing, ≤3 копії, 44 героя"}
  - {kind: other, url: "https://www.shacknews.com/article/108730/artifact-review-the-moba-of-card-games", note: "огляд: 2 з 3 веж, Ancient 80, респавн героя, режими (драфти, гантлети)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Artifact+Valve+card+game+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [hp-damage, respawn, round-currency, shop-catalog, shop-window, spawn-random-cell, pocket, move-timer, online-multiplayer, ai-opponent, mode-select, tutorial-window, +lane-grid, +deck-draw, +deck-builder, +three-boards, +per-lane-mana, +initiative-pass, +pass-pass-resolve, +combat-arrows, +tower-then-ancient, +two-of-three-lanes, +color-requirement, +hero-fountain-respawn, +item-deck, +secret-shop-hold, +signature-spell, +siege-overflow, +piercing-armor, +blind-deployment, +draft-mode, +card-collection, +card-market]
proposes: ["+trigger:pass", "+cond:color_in_lane", "+effect:draw_cards", "+ui:initiative-marker", "+ui:lane-overview", "+card:combat-arrows", "+card:initiative-pass"]
author: opus
date: 2026-11-09
---

# Artifact — карткова Dota: три окремі дошки-смуги з вежами, своя мана в кожній, ініціатива переходить за кожну карту

## Суть
Карткова гра Valve за дизайном Річарда Гарфілда (Magic: The Gathering): поле — **три смуги**, як три лінії карти Dota 2, кожна — окрема дошка з вежею, своєю маною й своїм боєм. Гравці по черзі грають карти в поточній смузі; кожна зіграна карта **передає ініціативу** супернику, два паси поспіль запускають бій смуги. Герої дають «колір», без якого карти цього кольору в смузі не зіграти; між раундами — крамниця за золото з убивств. Перемога — дві вежі з трьох або Ancient.

## Поле і час
- Поле — **3 дошки-смуги** (ліва, центр, права), кожна — два протилежні ряди позицій юнітів (свій/суперника) і вежа кожного гравця. У Classic смуги розігруються **по черзі** зліва направо, на екрані — одна смуга зблизька.
- Раунд: **Action** в смузі 1 → бій смуги 1 → Action/бій смуги 2 → смуги 3 → **Shopping** → **Deployment** (на першому раунді розстановка своя).
- Хід — покроковий з обміном ініціативою; кожен гравець має обмежений загальний запас часу на бездіяльність.
- Artifact Foundry (2.0): **усі три смуги видно одночасно**, одна спільна мана, випадковість суттєво зменшено.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Смуга-дошка ×3 | zone | своя мана, вежі, ряди позицій | окремий бій; розігрується в черзі |
| Вежа | static | 40 HP | одна на смугу на гравця; незаблокований юніт бʼє вежу |
| Ancient | static | 80 HP | зʼявляється в смузі після знищення вежі; знищено — перемога |
| Герой | piece | атака, броня, HP, колір, 3 слоти | «відкриває» свій колір у смузі; гине → фонтан → знову в будь-яку смугу |
| Мілі-крип | piece | слабкий | по 2 на сторону щорозстановки у випадкові смуги; не керується |
| Карта крипа | piece | мана, колір | призиває юніта в смугу |
| Закляття | — | мана, колір | одноразовий ефект (шкода, лікування, переміщення, видалення) |
| Покращення (improvement) | zone | мана, колір | постійний ефект смуги (?) |
| Сигнатурне закляття | — | 3 копії | у колоді разом зі своїм героєм |
| Зброя / броня / аксесуар | object | ціна в золоті | екіпірується на героя (1 на слот), лишається після його смерті |
| Розхідник | pickup | дешевий | одноразово: лікування, добір карт, переміщення героя |
| Золото | resource | +5 за героя, +1 за крипа | у крамниці; можна копити |
| Мана смуги | resource | +1 щораунду | поповнюється до максимуму; окрема в кожній смузі (Classic) |
| Ініціатива | — | — | хто діє зараз; перший пас у смузі — перший хід у наступній |
| Стрілка атаки | mark | навпроти / діагональ | показує ціль юніта в бою |
| Рука | zone | без ліміту | — |
| Фонтан | zone | — | загиблі герої чекають на повернення |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «по 3 вежі по 40 HP; перші герої в смуги; draw_cards стартова рука»`.
- КОЛИ `turn_start(round)` → ТО `custom: «мана кожної смуги +1 і поповнюється»`, `custom: «draw_cards»` (?).
- КОЛИ `input(play, card, lane)` → ЯКЩО `counter(lane_mana, >=, cost)` and `custom: «у цій смузі є ваш герой кольору карти»` → ТО `custom: «ефект карти»`, `counter(lane_mana, -cost)`, `end_turn`; інакше `block`.
- КОЛИ `input(play, item, hero)` → ЯКЩО `custom: «слот цього виду вільний»` → ТО `attach(item, hero)`, `end_turn`; предмети — у будь-якій смузі.
- КОЛИ `input(pass)` → ЯКЩО `custom: «суперник спасував щойно перед цим»` → ТО `custom: «бій у смузі»`; інакше `pass_turn`.
- КОЛИ `custom: «перший пас у смузі»` → ТО `custom: «цей гравець отримує ініціативу в наступній смузі»`.
- КОЛИ `custom: «бій у смузі»` → ТО `damage(arrow_target, attack)` — усі юніти одночасно; ціль — куди вказує стрілка, зазвичай юніт навпроти.
- КОЛИ `custom: «бій у смузі»` → ЯКЩО `custom: «стрілка юніта вказує на порожнє місце навпроти»` → ТО `damage(tower, attack)`.
- КОЛИ `custom: «бій; атакер має Siege»` → ТО `custom: «надлишок шкоди по блокеру переходить у вежу»`; Piercing → `custom: «ігнорує броню»`.
- КОЛИ `hp_zero(hero)` → ТО `disappear(hero)`, `currency(+5)` суперникові, `custom: «герой — у фонтан, пропускає розстановку»`.
- КОЛИ `hp_zero(creep)` → ТО `disappear(creep)`, `currency(+1)` суперникові.
- КОЛИ `hp_zero(tower)` → ТО `spawn(ancient)` у цій смузі (80 HP).
- КОЛИ `counter(destroyed_enemy_towers, >=, 2)` → ТО `win`.
- КОЛИ `hp_zero(ancient)` → ТО `win`.
- КОЛИ `phase_start(shopping)` → ТО `custom: «таємна крамниця — випадковий предмет усієї гри; основна — з вашої колоди предметів, поповнюється одразу після купівлі; бічна — дешеві розхідники»`.
- КОЛИ `input(buy, item)` → ЯКЩО `counter(gold, >=, price)` → ТО `give(player, item)`, `currency(-price)`.
- КОЛИ `input(hold, secret_item)` → ЯКЩО `counter(gold, >=, 1)` → ТО `currency(-1)`, `custom: «предмет лишається в таємній крамниці до наступної фази»`.
- КОЛИ `phase_start(deployment)` → ТО `spawn_at(melee_creep, random_lane)` × 2 кожній стороні; `custom: «позиції в смузі випадкові»`.
- КОЛИ `input(deploy, hero, lane)` → ЯКЩО `custom: «герой готовий (новий або з фонтану)»` → ТО `place(player, hero)`; обидва розставляють наосліп одночасно.
- КОЛИ `custom: «загальний час бездіяльності гравця вичерпано»` → ТО `lose`.
- КОЛИ `input(concede)` → ТО `lose`; суперник `win`.
- Перемога: 2 ворожі вежі або 1 Ancient · Поразка: те саме проти вас, вичерпаний час, здача · Рахунок: нема; у режимах — серії перемог і нагороди.

## Керування і ввід
- Миша: вибрати карту руки → смугу/ціль; кнопка пасу; клік по предмету в крамниці; розстановка героїв у смуги на фазі Deployment (?) деталі drag/клік не перевірені.
- Перемикання між смугами — по черзі гри (Classic); у Foundry — одна дошка з трьома смугами.
- Колоди можна імпортувати кодом із зовнішніх сайтів.

## Вікна, меню, HUD
- `game-screen`: поточна смуга зблизька, огляд трьох смуг, HP веж/Ancient (`hp-bar`), мана смуги (`energy-bar`), золото (`coins`), рука (`pocket`), маркер ініціативи, кнопка пасу (`end-turn-button`), запас часу (`player-clock`), стрілки атаки.
- `shop-window`: три крамниці (таємна · основна · бічна), «притримати» за 1 золото.
- `placement-screen`: розстановка героїв у смуги (наосліп).
- `deck-builder` (`custom-window`): 5 героїв, основна колода (≥ 40 карт, ≤ 3 копії), колода предметів; `codex-window` колекції.
- `mode-select`: бот-режими, Featured Events, Global Matchmaking, Casual Arena (до 5 перемог), Phantom Draft, Keeper Draft, Expert-гантлети за квиток; Foundry: Hero Draft, Beginner-кампанія, челенджі.
- `tutorial-window`: навчання проти AI (у Foundry — розширене + демо-сценарій кожного героя).
- `end-screen`: перемога/поразка; `main-menu`.
- Переходи: `main-menu` → `mode-select` → (`deck-builder`) → `game-screen` ⇄ `shop-window` / `placement-screen` → `end-screen`.

## Фічі поза полем
- `online-multiplayer` 1×1; `ai-opponent-levels` (боти різної складності); драфт-режими (`+draft-mode`).
- Колекція й ринок: на старті карти купувались і продавались на Steam Marketplace (пакети по 12, 1 рідкісна гарантована); згодом усе безкоштовне, карти власників стали Collector's Edition.
- Foundry: карти заробляються грою, PvE-кампанія, Hero Draft; розробку зупинено в 2021, обидві версії безкоштовні.

## Варіації й родичі
- **Classic vs Foundry**: три смуги по черзі → **одночасно**; мана кожної смуги → **спільний пул**; багато випадковості (крипи, стрілки, позиції) → **мало**.
- Родичі в корпусі: [marvel-snap](marvel-snap.md) (3 локації, 2 з 3), [gwent](gwent.md) (ряди й раунди), [plants-vs-zombies-heroes](plants-vs-zombies-heroes.md) (смуги з картами), [hearthstone-battlegrounds](hearthstone-battlegrounds.md) (крамниця між боями), [inscryption](inscryption.md) (атака навпроти по смузі), [clash-royale](clash-royale.md) (вежі на смугах, ancient-подібна головна вежа).
- **Осі варіацій**: смуги — одна дошка / **три окремі дошки з окремою маною** / спільна мана; черговість — хід цілком / **ініціатива за кожну карту, бій за два паси**; ціль атаки — навпроти / **стрілка (навпроти чи діагональ)**.

## Цікавинки для курсу
- Обмін ініціативою за кожну дію і бій на «пас-пас» — 🥉 (машина станів пріоритету, як у MTG).
- Три незалежні дошки з окремими лічильниками мани й ресурсом героїв-кольорів — 🥉.
- Вежа → Ancient: друга фаза цілі в тій самій смузі, дві умови перемоги — 📎.
- Таємна / основна / бічна крамниці з колодою предметів і «притримати за 1 золото» — 📎.
- Стрілки атаки й випадкове розміщення крипів — 🌱 (і причина, чому Foundry їх прибрав).
- Siege (надлишок у вежу) і Piercing (ігнор броні) — 🌱.

## Мапа на каталог
- Є: `hp-damage` · `respawn` (фонтан) · `round-currency` (золото, мана) · `shop-catalog` · `shop-window` · `spawn-random-cell` (крипи) · `pocket` (рука) · `move-timer` (запас часу) · `online-multiplayer` · `ai-opponent` · `mode-select` · `tutorial-window`.
- **Нема** → пропозиції карток:
  - `+initiative-pass` «Ініціатива переходить за кожну дію» · game-logic/opponent · 🥉 — з `+pass-pass-resolve` (два паси поспіль → розвʼязка).
  - `+combat-arrows` «Стрілка цілі атаки» · entities/combat · 📎 · слот {dir: across|diagonal}.
  - `+three-boards` «Кілька незалежних дошок у партії» · entities/legality · 🥉 · слот {boards: 3}.
  - `+per-lane-mana`, `+tower-then-ancient`, `+two-of-three-lanes`, `+color-requirement`, `+hero-fountain-respawn`, `+item-deck`, `+secret-shop-hold`, `+signature-spell`, `+siege-overflow`, `+piercing-armor`, `+blind-deployment`, `+card-market` — 🌱–📎.
  - `+lane-grid`, `+deck-draw`, `+deck-builder`, `+draft-mode`, `+card-collection` — як у сусідніх файлах сімʼї.

## Пропозиції до словників
- `+trigger:pass(side)` — сторона спасувала (у парі з попереднім пасом суперника — розвʼязка смуги).
- `+cond:color_in_lane(color)` — у смузі є свій герой цього кольору (вимога для карти).
- `+effect:draw_cards(n)` — узяти N карт (у словнику `draw` = нічия).
- `+ui:initiative-marker` — позначка, хто ходить першим/зараз.
- `+ui:lane-overview` — мініатюра трьох смуг поруч із поточною.
- `+card:combat-arrows` · `+card:initiative-pass` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/Artifact_(video_game)) — три дошки, вежі й Ancient, мана смуг, ініціатива, крипи, крамниця, слоти, кольори, колода ≥ 40, 2.0/Foundry, дати.
- [Steam](https://store.steampowered.com/app/583950/Artifact/) — Classic і Foundry, відмінності Foundry.
- [SteelSeries, гайд](https://steelseries.com/en-hk/blog/artifact-blog-77) — 40/80 HP, фази, крипи, ініціатива, 3 крамниці, золото 5/1.
- [Destructoid](https://destructoid.com/?p=236990) — кольори й класи, розстановка наосліп, сигнатурні закляття, Siege/Piercing, ліміт копій, запас часу.
- [Shacknews, огляд](https://www.shacknews.com/article/108730/artifact-review-the-moba-of-card-games) — умови перемоги, респавн, режими.

## Непевне
- (?) Респавн героя: «пропускає один раунд» (Destructoid, Shacknews) vs «через два повні раунди» (SteelSeries).
- (?) Правило стрілок: коли навпроти порожньо, стрілка йде прямо чи по діагоналі — із якою ймовірністю; стартова мана смуги й добір карт за раунд — не бачив у джерелах.
- (?) Стартова розстановка героїв (скільки й куди на першому раунді) і скільки героїв за раунд далі (Destructoid: «до двох»).
- (?) Колода предметів: мінімум чи максимум 9; чи improvement — постійна карта смуги (так у Destructoid як «upgrades»); чи шкода юнітів зберігається між раундами.
