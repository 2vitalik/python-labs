---
title: "Descent: Journeys in the Dark"
slug: descent-journeys-in-the-dark
aka: [Descent, "Descent 2nd Edition", "Descent: Road to Legend", "Descent: Legends of the Dark"]
family: tactics
also: [board-digital, roguelike]
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: hidden
  random: runtime
  goal: state
year: 2005
platforms: [board, "Road to Legend app (iOS/Android/PC, 2016)"]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Descent:_Journeys_in_the_Dark", best: true, note: "оверлорд, загроза, колода як таймер, герої й навички, кубики з символами, доповнення, 2-га редакція"}
  - {kind: other, url: "https://lehi-innovation.github.io/boardgame-rules/rules/descent-journeys-in-the-dark-second-edition/", note: "конспект правил 2-ї ред.: 2 дії героя, втома, кубики, сплески, хід оверлорда, LOS, нокаут, пошук, кампанія"}
  - {kind: official, url: "https://fantasyflightgames.com/en/products/descent-journeys-in-the-dark-second-edition", note: "сторінка FFG (бачив у пошуку): 2-га ред., Road to Legend"}
  - {kind: other, url: "https://fgbradleys.com/wp-content/uploads/rules/DescentRules.pdf", note: "правила 1-ї ред. PDF (бачив у пошуку)"}
  - {kind: other, url: "https://www.orderofgamers.com/?p=2756", note: "конспект правил (бачив у пошуку)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Descent+Journeys+in+the+Dark+how+to+play", note: "пошук; правила"}
stage: v1
coverage: 70
mechanics: [move-8dir, impassable-cells, hp-damage, melee-vs-ranged, status-effects, multi-cell-size, item-pickup, inventory-items, spawn-points, reinforcements, shop-between-levels, unit-xp-skills, hot-seat, ai-opponent, sequential-levels, save-progress, world-map, character-select, game-screen, end-screen, +game-master, +asymmetric-sides, +modular-board, +combat-dice-symbols, +dice-range-check, +surge-spend, +fatigue-pool, +knockout-standup, +threat-economy, +deck-as-timer, +monster-groups, +lieutenant-boss, +search-tokens, +branching-campaign, +companion-app-overlord, +corner-los]
proposes: ["+trigger:knocked_out", "+cond:range_total", "+effect:fatigue", "+effect:draw_card", "+effect:activate_group", "+role:minion", "+ui:surge-count", "+ui:fatigue-bar", "+window:quest-guide", "+window:campaign-sheet", "+feature:app-overlord"]
author: opus
date: 2026-11-09
---

# Descent: Journeys in the Dark — 1 проти всіх: оверлорд копить загрозу й розігрує пастки, герої витрачають дії, втому й «сплески» на кубиках

## Суть
До 4 героїв проходять квест на дошці з плиток-кімнат, оверлорд (окремий гравець) керує групами монстрів і грає картки пасток, подій і посилень. Ядро — **економіка двох сторін**: у героя 2 дії за хід і запас втоми, яку можна «спалити» на зайві кроки чи вміння; оверлорд у 1-й ред. накопичує загрозу від дій героїв і витрачає її на монстрів, а його колода тикає як таймер. Бій — кубики з символами: синій кубик атаки дає дальність, шкоду, сплеск або промах, кольорові кубики захисту — щити.

## Поле і час
- Поле — модульні плитки (кімнати, коридори, двері), складені за мапою квесту; клітини квадратні; великі монстри займають кілька клітин.
- Хід 2-ї ред.: усі герої по черзі (по 2 дії), потім оверлорд: тягне 1 картку, активує кожну групу монстрів (по 2 дії на монстра, з них лише 1 атака).
- 1-ша ред.: оверлорд отримує загрозу у відповідь на дії героїв; герої мають спільний пул очок перемоги, які тануть із загибеллю героїв.
- Видимість: лінія з кута клітини атакувальника до будь-якого кута клітини цілі; блокують стіни, непрохідна місцевість, двері.
- Випадковість: кубики атаки/сили/захисту, колода оверлорда, картки пошуку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | piece | швидкість, здоровʼя, витривалість (stamina), захист (кубик), риси (?) | 2 дії за хід: рух / атака / пошук / відпочинок / встати / підняти союзника / спецдія |
| Оверлорд | — | рука карток, загроза (1-ша ред.), XP (кампанія) | грає пастки й події, активує монстрів |
| Міньйон (рядовий монстр) | enemy | бежева фігура | слабша версія в групі |
| Майстер (ватажок групи) | enemy | червона фігура, кращі статки й уміння | ходить разом з групою |
| Великий монстр | enemy | кілька клітин | «стискається» до 1 клітини для руху, «розгортається» на зупинці |
| Лейтенант оверлорда | boss | окрема фігура (кампанія) | сюжетний ворог між квестами |
| Плитка-кімната / коридор | terrain | — | складають поле за мапою квесту |
| Двері | gate | — | блокують рух і видимість, відчиняються (?) |
| Вода / лава / яма / брила | terrain | — | особливі ефекти й обмеження руху (?) |
| Жетон пошуку | pickup | 9 жетонів, 12 карток пошуку | сусідній герой перевертає → картка предмета |
| Ціль квесту (жетон) | static | за квестом | артефакт, важіль, бранець тощо |
| Картка оверлорда | supply | пастка / посилення / подія | тягнеться щоходу й при нокауті героя |
| Картка стану | — | отрута, хвороба, знерухомлення, оглушення | одна такого типу на фігуру |
| Магазин | — | 20 предметів Акту I, 14 Акту II | між квестами за золото |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(hero)` → ТО `custom: «2 дії; дію можна повторити, рух можна перервати іншою дією»`.
- КОЛИ `input(move, hero)` → ТО `move` до значення швидкості; ЯКЩО `custom: «втома < витривалості»` → ТО можна `custom: «+1 клітина за 1 втому»`.
- КОЛИ `custom: «зовнішня втома перевищила витривалість»` → ТО `damage(hero, надлишок)`; у монстрів витривалості нема — вся втома стає шкодою.
- КОЛИ `input(rest, hero)` → ТО `custom: «у кінці ходу скинути всю втому»`.
- КОЛИ `input(attack, figure, target)` → ЯКЩО `line_of_sight(figure, target)` → ТО атакувальник кидає синій кубик + кубики сили, захисник — кубики захисту одночасно.
- КОЛИ `custom: «на синьому кубику X»` → ТО промах, решта ігнорується.
- КОЛИ дальня атака → ЯКЩО `custom: «сума дальності на кубиках < відстань до цілі»` → ТО промах (сплеск може додати дальності).
- КОЛИ `custom: «випав сплеск»` → ТО `choose(ефект зброї/вміння)`; невитрачений сплеск героя → `custom: «−1 втома»`.
- КОЛИ влучання → ТО `damage(target, серця − щити)` (мінімум 0); ЯКЩО шкода ≥ 1 → ТО `set_state(target, condition)` від зброї.
- КОЛИ `custom: «шкода ≥ здоровʼя героя»` → ТО нокаут: `transform(hero, hero_token)`, скинути стани, оверлорд `custom: «тягне картку»`; жетон імунний до атак, клітина вважається порожньою.
- КОЛИ `turn_start(knocked_hero)` → ЯКЩО не підняли → ТО лише дія «встати»: 2 червоні кубики, `heal(hero, серця)`, `custom: «зняти втому = сплески»`, хід закінчено.
- КОЛИ `input(revive, hero, knocked_hero)` → ЯКЩО `adjacent(hero, knocked_hero)` → ТО той самий кидок «встати» для пораненого.
- КОЛИ `input(search, hero)` → ЯКЩО `adjacent(hero, search_token)` → ТО `reveal(token)` + `give(hero, search_card)`.
- КОЛИ `turn_start(overlord)` → ТО `custom: «тягне 1 картку оверлорда»`, потім `custom: «кожна група активується раз; усі її монстри — до 2 дій, лише 1 атака; група закінчує до наступної»`.
- КОЛИ `input(play, overlord_card)` → ТО пастка (`damage`/`set_state` герою), посилення монстра або подія; `spawn_at(monsters, entry)` — за квестом.
- КОЛИ (1-ша ред.) `custom: «герой діє / оверлорд тягне картку»` → ТО `counter(threat, +n)`; КОЛИ оверлорд купує монстра або карту → `counter(threat, −cost)`.
- КОЛИ (1-ша ред.) `died(hero)` → ТО `custom: «герой воскресає в місті, команда втрачає очки перемоги»`; ЯКЩО `counter(conquest, <=, 0)` → ТО `win` оверлорда.
- Перемога (2-га ред.): кожен квест задає ціль героїв і ціль оверлорда; виконав першим — `win`. 1-ша ред.: герої — убити фінального боса, оверлорд — вичерпати очки перемоги героїв.
- Кампанія: `custom: «результат квесту відкриває наступні; герої — золото на магазин і XP на картки класу; оверлорд — XP на нові картки; після Акту I — інтерлюдія, Акт II з сильнішими монстрами»`.

## Керування і ввід
- Настільно: фігурки, кубики, картки героїв (статки, класи, навички), жетони втоми/шкоди/станів; оверлорд тримає руку карток закритою.
- Застосунок Road to Legend (цифрова версія): застосунок бере роль оверлорда — гравці всі герої (кооп); застосунок показує мапу, які плитки викласти, активації монстрів і події (?). Ввід — тап по героях, дії й результати кидків вводять гравці (?).
- Legends of the Dark (2021) — 3-тя гра серії, повністю через застосунок (?).

## Вікна, меню, HUD
- `main-menu` (застосунок): кампанія / новий квест / продовжити (?).
- `character-select` — вибір героя й класу (воїн, лікар, маг, розвідник).
- `custom-window` «Книга квестів» (`quest-guide`) — опис квесту, мапа, цілі обох сторін.
- `game-screen`: поле з плиток, фігури, `hp-bar` і `ui:fatigue-bar` героя, `ui:dice-result` (серця, щити, сплески, дальність), `ui:surge-count`, рука оверлорда (на руках у гравця).
- `shop-window` — магазин між квестами; `custom-window` «Аркуш кампанії» (`campaign-sheet`) — золото, XP, пройдені квести, лейтенанти.
- `map-window` — мапа світу кампанії (Road to Legend, 1-ша ред.).
- `end-screen` — підсумок квесту.

## Фічі поза полем
- Кампанія (`save-progress`): 2-га ред. — акти, гілки квестів, XP і золото; 1-ша ред. Road to Legend — рівні срібло/золото/діамант для героїв і монстрів.
- Режими: оверлорд-людина (hotseat за столом) / застосунок-оверлорд (`mode-coop`); доповнення-кооператив Nature's Ire (з сплесками монстрів).
- Доповнення: нові плитки, герої, монстри, пастки; Tomb of Ice — кубик невидимості і приховані від оверлорда картки подвигів; Sea of Blood — кораблі.

## Варіації й родичі
- Предки: [heroquest-space-hulk](heroquest-space-hulk.md) (HeroQuest — майстер за ширмою), [space-crusade](space-crusade.md).
- Сусіди: [gloomhaven](gloomhaven.md) (без оверлорда, картки замість кубиків), [kingdom-death-monster](kingdom-death-monster.md), Imperial Assault (та сама рушійна база від FFG, (?)).
- **Осі варіацій**: противник — людина-оверлорд / застосунок / колода AI (Gloomhaven) · ресурс оверлорда — загроза (1-ша) / рука карток (2-га) · мета — убити боса (1-ша) / цілі квесту для обох сторін (2-га) · смерть — воскресіння з мінусом очок / нокаут і «встати».

## Цікавинки для курсу
- Синій кубик з промахом X і дальністю: одна кидка вирішує влучання, дальність і шкоду — 📎.
- Сплески як валюта: «купити» ефект зброї або зняти втому — 🥉 (вибір після кидка).
- Втома: добровільні бонус-кроки до межі, примусова втома понад межу → шкода — 📎.
- Нокаут → жетон, «встати» кидком або союзник піднімає — 📎.
- Активація груп монстрів (міньйони + майстер), «2 дії, одна атака» — 🥉.
- Великий монстр, що «стискається» для руху й «розгортається» — 🥈 (пошук розміщення).
- Застосунок-оверлорд замість гравця — 🥇 (AI сторони-майстра).

## Мапа на каталог
- Є: `move-8dir` (?) · `impassable-cells` · `hp-damage` · `melee-vs-ranged` · `status-effects` (отрута, хвороба, оглушення, знерухомлення) · `multi-cell-size` (великі монстри) · `item-pickup` / `inventory-items` (картки пошуку, спорядження) · `spawn-points` / `reinforcements` · `shop-between-levels` · `unit-xp-skills` (XP на картки класу) · `hot-seat` · `ai-opponent` (застосунок) · `sequential-levels` · `save-progress` · `world-map` · `character-select` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+game-master` · `+asymmetric-sides` · `+modular-board` · `+combat-dice-symbols` · `+fatigue-pool` · `+branching-campaign` — наявні пропозиції корпусу.
  - `+dice-range-check` «Дальність на кубиках проти відстані» · entities/combat · 📎.
  - `+surge-spend` «Сплески на кубиках як валюта ефектів» · entities/combat · 🥉.
  - `+knockout-standup` «Нокаут і підйом кидком» · entities/state · 📎.
  - `+threat-economy` «Загроза оверлорда від дій героїв» · game-logic/economy · 📎.
  - `+deck-as-timer` «Колода ворога як таймер» · game-logic/turns · 📎.
  - `+monster-groups` «Групи монстрів з ватажком, активація групою» · game-logic/opponent · 🥉.
  - `+lieutenant-boss` «Сюжетний бос між квестами» · levels/progression · 🌱.
  - `+search-tokens` «Жетон пошуку → картка» · entities/interact · 🌱.
  - `+companion-app-overlord` «Застосунок грає майстра» · game-logic/opponent · 🥇.
  - `+corner-los` «Видимість від кута до кута клітини» · entities/combat · 🥉.

## Пропозиції до словників
- `+trigger:knocked_out` — герой нокаутований (відмінно від `hp_zero`/`died`: лишається жетоном).
- `+cond:range_total` — сума дальності на кубиках ≥ відстані.
- `+effect:fatigue` — ±втома (окремий від HP ресурс з межею).
- `+effect:draw_card` — потягнути картку (оверлорд, пошук).
- `+effect:activate_group` — активувати групу ворогів.
- `+role:minion` — рядовий член групи з ватажком.
- `+ui:surge-count` — сплески кидка; `+ui:fatigue-bar` — втома / витривалість.
- `+window:quest-guide` — книга квесту з цілями сторін; `+window:campaign-sheet` — аркуш кампанії.
- `+feature:app-overlord` — застосунок замість гравця-ведучого.

## Джерела
- ⭐ [Wikipedia: Descent: Journeys in the Dark](https://en.wikipedia.org/wiki/Descent:_Journeys_in_the_Dark) — оверлорд, загроза, колода-таймер, герої з навичками, кубики з символами (3–5, до 10), доповнення, 2-га ред. 2012.
- [Конспект правил 2-ї ред.](https://lehi-innovation.github.io/boardgame-rules/rules/descent-journeys-in-the-dark-second-edition/) — 2 дії, втома й витривалість, синій кубик з X, кубики сили й захисту, сплески, хід оверлорда, LOS «від кута», нокаут, 9 жетонів пошуку / 12 карток, магазин 20/14.
- [FFG: Descent 2nd Edition](https://fantasyflightgames.com/en/products/descent-journeys-in-the-dark-second-edition) — сторінка видавця (у пошуку, з розділом Road to Legend).
- [Правила 1-ї ред. (PDF)](https://fgbradleys.com/wp-content/uploads/rules/DescentRules.pdf), [Order of Gamers](https://www.orderofgamers.com/?p=2756) — бачив у пошуку, не відкривав.

## Непевне
- (?) Діагональний рух (`move-8dir`) — у 2-й ред., наскільки пам'ятаю, так; джерело не каже.
- (?) Road to Legend (застосунок 2016) і Legends of the Dark (2021) — з памʼяті: застосунок як оверлорд, повний кооп; Wikipedia-статті не відкрились (404).
- (?) Двері, вода, лава, ями — дія і вартість з памʼяті.
- (?) Деталі загрози й «очок перемоги/conquest» 1-ї ред. — Wikipedia дає лише загальну формулу.
- (?) Imperial Assault як «та сама рушійна база» — з памʼяті.
