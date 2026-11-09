---
title: Ironclad Tactics
slug: ironclad-tactics
aka: []
family: tower-lanes
also: [tactics]
klass: cursor
axes:
  field: square
  time: wego
  opponent: ai
  info: hidden
  random: runtime
  goal: race
year: 2013
platforms: [PC, macOS, Linux, Android, PS4]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Ironclad_Tactics", best: true, note: "смуги сітки, автохід загонів, 4 види карт, рука 5 / старт 3 / +1, карта згорає за 5 ходів, AP, одночасні ходи, VP за перетин, мортири, колода 20, режими"}
  - {kind: official, url: "https://www.zachtronics.com/ironclad-tactics/", note: "режими: кооп-кампанія, Skirmish, Nemesis, онлайн quick-skirmish, WAR!; кампанії Rise of Dmitry і Blood and Ironclads"}
  - {kind: steam, url: "https://store.steampowered.com/app/226960/Ironclad_Tactics/", note: "опис, режими, доповнення"}
  - {kind: other, url: "https://www.playstationlifestyle.net/2015/01/26/ironclad-tactics-review-pick-card-ps4/", note: "огляд PS4: фази Play/Act/Kill/Move, зазвичай 8 VP, мортирні клітини, +AP суперникові, керування"}
  - {kind: other, url: "https://www.gamegrin.com/reviews/ironclad-tactics-review/", note: "огляд: 1 клітина за хід, бульдозер і джетпак, зброя-частини, колода 20 карт / 2 фракції"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Ironclad+Tactics+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [hp-damage, line-of-sight-attack, push-object, cursor-place, pocket, inventory-limit, move-timer, ai-opponent, online-multiplayer, mode-select, level-unlock, +lane-grid, +deck-draw, +deck-builder, +auto-march-units, +simultaneous-turns, +action-points, +reach-row-win, +hold-zone-points, +comeback-ap, +card-expiry, +card-upgrade-by-use, +unit-parts-equip, +halt-toggle, +phase-cycle, +faction-deck-limit, +coop-campaign]
proposes: ["+effect:draw_cards", "+ui:vp-track", "+ui:phase-indicator", "+card:comeback-ap", "+card:card-expiry"]
author: opus
date: 2026-11-09
---

# Ironclad Tactics — карткові загони самі сунуть смугами; одночасні короткі ходи й очки за перетин поля

## Суть
Гра Zachtronics: два гравці (або гравець і AI) одночасно викладають карти загонів на свій край сітки, а загони **самі** йдуть смугою вперед по клітині за хід, доки не впруться. Механічні ironclad-и, що перетнули поле, приносять очки перемоги (VP); хто першим набрав ціль — виграв. Гравець керує не рухом, а **що й куди викласти**, чим обладнати ironclad і коли зупинити загін.

## Поле і час
- Поле — прямокутна сітка, поділена на **смуги**; кожна сторона розгортає загони на своєму краї, мета — протилежний край. Є клітини-мортири (утримання → VP) і перешкоди.
- Хід поділено на 4 фази: **Play** (гравці таємно й одночасно кладуть карти; приблизно половина ходу) → **Act** (загони стріляють/діють) → **Kill** (знищені зникають) → **Move** (рухомі незупинені йдуть щонайменше на клітину вперед).
- Ходи короткі й за таймером — відчуття RTS; рішення треба ухвалювати швидко.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Ironclad (базовий) | piece | HP, ціна в AP, слоти частин | автохід 1 кл/хід смугою; перетнув поле — VP за типом |
| Бульдозер-ironclad | piece | — | відштовхує інші ironclad-и назад |
| Джетпак-ironclad | piece | — | перелітає мапу |
| Важкий автоматон | piece | багато HP | вбирає шкоду, «танк» смуги |
| Трансформер-ironclad (Дмитро) | piece | — | доповнення Rise of Dmitry (?) |
| Піхота (стрільці, ветерани-стрільці) | piece | ціна в AP | люди; так само йдуть уперед, діють раз за хід |
| Частина: рушниця | object | — | стріляє по прямій уперед |
| Частина: меч | object | — | бʼє всіх навколо |
| Частина: ракети · цвяхомет · бур · броня · «капелюх» | object | — | зброя/тактика/захист для ironclad-а |
| Тактична карта | — | ціна в AP | одноразово: перевести загін на іншу смугу, полагодити ironclad тощо |
| Мортирна клітина | zone | — | зайняти й утримати хід → +1 VP |
| Перешкода | static | — | зупиняє рух загону |
| Зона розгортання | zone | свій край | лише тут кладуться загони |
| Action Points (AP) | resource | ≈ +1 за хід | ціна карт; накопичуються; більше — коли суперник набрав VP |
| Victory Points (VP) | resource | ціль зазвичай 8 | за перетин поля, за мортири |
| Рука | zone | ≤ 5 карт | старт 3, +1 за хід; карта без розіграшу 5 ходів — у скид |
| Колода | zone | 20 карт, ≤ 2 фракції | скінчилась — скид замішується наново |
| Суперник | enemy | AI / людина | ті самі правила, одночасний хід |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «перемішати колоду; draw_cards 3»`.
- КОЛИ `turn_start(both)` → ТО `counter(ap, +1)`; ЯКЩО `count(hand, <, 5)` → ТО `custom: «draw_cards 1»`.
- КОЛИ `custom: «карта пролежала в руці 5 ходів»` → ТО `custom: «discard»`.
- КОЛИ `custom: «колода порожня»` → ТО `custom: «скид і зіграні карти замішуються в нову колоду»`.
- КОЛИ `phase_start(play)` → ТО `timer(start)`; обидві сторони планують таємно й одночасно.
- КОЛИ `input(play, unit_card, cell)` → ЯКЩО `counter(ap, >=, cost)` and `free(cell)` and `custom: «клітина у своїй зоні розгортання»` → ТО `place(player, unit)`, `counter(ap, -cost)`; інакше `block`.
- КОЛИ `input(play, part_card, ironclad)` → ЯКЩО `counter(ap, >=, cost)` and `custom: «у ironclad-а вільний слот цього виду»` → ТО `attach(part, ironclad)`, `counter(ap, -cost)`.
- КОЛИ `input(play, tactic_card, target)` → ЯКЩО `counter(ap, >=, cost)` → ТО `custom: «ефект карти»` — напр. `move(unit, other_lane)` або `heal(ironclad, n)`.
- КОЛИ `input(toggle, unit)` → ЯКЩО `state(unit, halted)` → ТО `clear_state(unit, halted)`; інакше `set_state(unit, halted)`.
- КОЛИ `phase_start(act)` → ЯКЩО `line_of_sight(rifle_unit, enemy)` → ТО `damage(enemy, n)`.
- КОЛИ `phase_start(act)` → ЯКЩО `adjacent(sword_unit, enemy)` → ТО `damage(enemy, n)` кожному сусідньому.
- КОЛИ `phase_start(kill)` → ЯКЩО `custom: «HP загону ≤ 0»` → ТО `disappear(unit)` — усі одночасно, тож обидва загони можуть знищити одне одного.
- КОЛИ `phase_start(move)` → ЯКЩО `free(cell_ahead)` and `not state(unit, halted)` → ТО `move(unit, forward)`; інакше `block`.
- КОЛИ `blocked(bulldozer)` → ЯКЩО `occupied(cell_ahead, ironclad)` → ТО `push(ironclad)` назад.
- КОЛИ `phase_start(move)` → ЯКЩО `state(unit, jetpack)` → ТО `custom: «перелітає загони на шляху»`.
- КОЛИ `reach(ironclad, far_edge)` → ТО `counter(vp, +n)` (n — за типом), `custom: «суперник отримує додаткові AP»`.
- КОЛИ `turn_end(both)` → ЯКЩО `occupied(mortar_cell, own_unit)` → ТО `counter(vp, +1)`.
- КОЛИ `counter(vp, >=, target)` → ТО `win`; суперник `lose`.
- КОЛИ `counter(turns, >=, n)` → ЯКЩО `mode(survive_barrage)` → ТО `win`; варіант: не дати супернику набрати VP.
- КОЛИ `counter(deployed_riflemen, >=, n)` → ТО `unlock(veteran_riflemen)` (кампанійна ціль покращує карту).
- Перемога: першим набрати VP-ціль (зазвичай 8) або виконати умову мапи · Поразка: суперник першим · Рахунок: VP.

## Керування і ввід
- Вибрати карту в руці → вказати клітину свого краю (загін) або свій ironclad (частина) або ціль тактики.
- Перемикач «йти / стояти» на загоні (іконка play/pause; на PS4 — кнопка X).
- PS4: хрестовина — вибір карт і курсор по полю клітина за клітиною; гарячих клавіш на типи нема.
- Хід не чекає гравця: таймер фази Play іде, потім фази Act/Kill/Move відтворюються самі.

## Вікна, меню, HUD
- `game-screen`: сітка зі смугами, `pocket` (рука ≤ 5), лічильник AP (`action-points`), VP обох сторін до цілі, індикатор фази, `timer-countdown` ходу, HP загонів.
- `deck-builder` (`custom-window`): колода 20 карт, ≤ 2 фракції, кілька збережених колод; на перше проходження місії ворог невідомий — колода «наосліп».
- `level-select`: місії кампаній; кожна має челенджі, що відкривають карти.
- `dialogue-window`: сюжет — ілюстрований графічний роман між місіями.
- `mode-select`: кампанія (соло / кооп), Skirmish і Nemesis проти друзів, онлайн quick-skirmish, WAR!; `lobby-window` для онлайну.
- `end-screen`: перемога/поразка, виконані челенджі, нові карти.
- Переходи: `main-menu` → `mode-select` → `level-select` → `deck-builder` → `game-screen` → `end-screen`.

## Фічі поза полем
- `unlockables`: карти — за сюжет, челенджі рівнів і перемоги онлайн (частина карт — лише за онлайн); без мікротранзакцій.
- Апгрейд карти використанням: розіграв N стрільців → відкрито ветеранів.
- Головоломкові місії: фіксований набір карт, треба знайти виграшне рішення (`mode-puzzle`).
- `mode-coop` (кампанія вдвох; AP-темп залежить від напарника), `online-multiplayer`, `mode-versus` (Skirmish — однакові колоди).
- Доповнення: Rise of Dmitry (8 місій, гантлет Fort Phantom Ridge з 6 етапів, ~18 карт) і Blood and Ironclads (8 місій, Франція й Німеччина, режим WAR!, ~24 карти).

## Варіації й родичі
- Родичі в корпусі: [plants-vs-zombies](plants-vs-zombies.md) (смуги, зустрічний рух), [plants-vs-zombies-heroes](plants-vs-zombies-heroes.md) (карти на смуги), [swords-and-soldiers](swords-and-soldiers.md) і [age-of-war-stick-war](age-of-war-stick-war.md) (юніти самі сунуть до бази суперника), [the-battle-cats](the-battle-cats.md), [mechabellum](mechabellum.md) (план → автобій), [marvel-snap](marvel-snap.md) (одночасні таємні ходи).
- **Осі варіацій**: рух загону — керований / **автохід із перемикачем стоп**; хід — по черзі / **одночасний із таймером**; ціль — знищити базу / **провести загін за край (VP-гонка)**; ресурс — фіксований / **з наздоганяльним бонусом програючому**.

## Цікавинки для курсу
- Чотирифазний хід Play → Act → Kill → Move з одночасним знищенням — 🥉 (порядок фаз прибирає перевагу ініціативи).
- Автохід смугою + перемикач «стояти» + бульдозер, що штовхає назад — 📎.
- VP за перетин поля й за утримання мортири — дві умови рахунку на одній мапі — 📎.
- Наздоганяльний AP: суперник, проти якого набрали VP, отримує більше — 🌱.
- Карта, що згорає після 5 ходів у руці, і замішування скиду — 🌱.
- Ironclad як каркас зі слотами частин (зброя визначає форму атаки: пряма / навколо) — 📎.

## Мапа на каталог
- Є: `hp-damage` · `line-of-sight-attack` (рушниця) · `push-object` (бульдозер) · `cursor-place` · `pocket` (рука) · `inventory-limit` (≤ 5) · `move-timer` · `ai-opponent` · `online-multiplayer` · `mode-select` · `level-unlock`.
- **Нема** → пропозиції карток:
  - `+comeback-ap` «Наздоганяльний ресурс» · game-logic/economy · 🌱 — суперник, проти якого набрали очки, отримує більше AP.
  - `+card-expiry` «Карта згорає за N ходів у руці» · entities/state · 🌱 · слот {turns: 5}.
  - `+halt-toggle` «Стоп/йти для автоматичного загону» · interface/input · 🌱.
  - `+phase-cycle` (Play/Act/Kill/Move), `+hold-zone-points` (мортира), `+unit-parts-equip`, `+card-upgrade-by-use`, `+faction-deck-limit`, `+coop-campaign` — 🌱–📎.
  - `+lane-grid`, `+deck-draw`, `+deck-builder`, `+auto-march-units`, `+simultaneous-turns`, `+action-points`, `+reach-row-win` — як у сусідніх файлах сімʼї.

## Пропозиції до словників
- `+effect:draw_cards(n)` — узяти N карт із колоди (у словнику `draw` = нічия, тож потрібне окреме слово).
- `+ui:vp-track` — лічильник очок перемоги обох сторін до цілі.
- `+ui:phase-indicator` — поточна фаза ходу (Play/Act/Kill/Move).
- `+card:comeback-ap` · `+card:card-expiry` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/Ironclad_Tactics) — смуги, автохід, 4 види карт, рука, згоряння карт, AP, одночасні ходи, VP, мортири, колода 20, режими, платформи.
- [Zachtronics](https://www.zachtronics.com/ironclad-tactics/) — режими й доповнення.
- [Steam](https://store.steampowered.com/app/226960/Ironclad_Tactics/) — опис і доповнення.
- [PlayStation LifeStyle, огляд](https://www.playstationlifestyle.net/2015/01/26/ironclad-tactics-review-pick-card-ps4/) — фази ходу, ціль 8 VP, мортири, +AP за VP суперника, керування PS4.
- [GameGrin, огляд](https://www.gamegrin.com/reviews/ironclad-tactics-review/) — 1 клітина за хід, бульдозер/джетпак/автоматон, частини-зброя, обмеження колоди.

## Непевне
- (?) Тривалість таймера ходу, розмір сітки й кількість смуг; чи піхота теж дає VP за перетин (джерела кажуть «головно ironclad-и»).
- (?) Дальність і точна форма ракет, цвяхомета й бура; що дає «капелюх»; деталі трансформерів Дмитра.
- (?) Розбіжність: один огляд пише, що +AP отримує сам гравець, коли суперник набрав VP, — так і записано; Wikipedia лише каже, що темп AP змінюють напарники й утримання точок.
- (?) Чи доповнення безкоштовні (так на сайті Zachtronics) для всіх платформ.
