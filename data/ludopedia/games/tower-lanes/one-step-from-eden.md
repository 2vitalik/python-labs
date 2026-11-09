---
title: One Step From Eden
slug: one-step-from-eden
aka: [OSFE]
family: tower-lanes
also: [roguelike]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: both
  goal: state
year: 2020
platforms: [PC, Switch, PS4, Xbox One]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/One_Step_From_Eden", best: true, note: "сітка 4×4 гравця + окрема 4×4 ворогів, мана, колода, артефакти, розгалужена мапа, co-op/PvP, натхнення MMBN"}
  - {kind: steam, url: "https://store.steampowered.com/app/960690/", note: "200+ закляттів, 100+ предметів, 9 персонажів, локальні co-op і PvP, Workshop"}
  - {kind: other, url: "https://steamah.com/one-step-from-eden-useful-tips-for-beginners/", note: "гайд: Focus і Luck, час перетасування, статы, заручники, Spare/Execute і кінцівки, Angel mode"}
  - {kind: other, url: "https://localindieverse.blogspot.com/2023/06/one-step-from-eden-beginner-tips-and.html", note: "2 заклинання одночасно, кулдаун і ціна в мані, шафл кнопкою, правка колоди після бою"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=One+Step+From+Eden+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, move-by-input, hp-damage, impassable-cells, status-effects, run-relics, shop-catalog, world-map, map-window, character-select, permadeath, enemy-waves, game-screen, game-pause, pause-menu, end-screen, achievements-window, +split-field-halves, +deck-draw, +draft-pick, +spell-slots-two, +mana-regen-cost, +reshuffle-delay, +manual-reshuffle, +deck-focus-weights, +spare-or-execute, +hostage-npc, +meta-progression, +local-coop, +shared-field-versus, +assist-mode, +mod-workshop]
proposes: ["+role:card", "+trigger:deck_empty", "+effect:draw_card", "+effect:shuffle_deck", "+ui:spell-slots", "+ui:shuffle-timer", "+window:deck-builder", "+axis:field=split-halves"]
author: opus
date: 2026-11-09
---

# One Step From Eden — ядро Mega Man Battle Network як роглайк-декбілдер: дві половини 4×4, мана, два заклинання над головою й перетасування колоди на час

## Суть
Гравець бігає своєю половиною поля 4×4 у реальному часі, бʼє зброєю персонажа й кидає заклинання з колоди на ворогів на сусідній половині 4×4. Відмінність від [mega-man-battle-network](mega-man-battle-network.md): замість Custom Gauge з паузою — **мана**, що безперервно відновлюється; одночасно «в руці» лише 2 заклинання, колода йде по черзі, а перетасування коштує секунд, які ростуть із розміром колоди. Між боями — роглайк: розгалужена мапа, нове заклинання після кожного бою, артефакти за рівні, вибір «пощадити чи стратити» боса.

## Поле і час
- Бій — дві сітки 4×4: своя (гравець) і окрема ворожа; ступати на ворожі клітини не можна.
- Real-time без пауз на вибір карт: мана тече постійно, кожне заклинання має ціну й кулдаун; «bullet hell» атаки ворогів по клітинах.
- Перед кастом гра показує на сітці значок, куди влучить заклинання (Spell preview, можна вимкнути).
- Клітини ворожої половини можна тимчасово ламати (Terra-пощада «ламає 6 випадкових ворожих клітин»).
- Поза боєм — розгалужена мапа вузлів (бій, скарб, крамниця, мінібос/бос); 4 біоми (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Персонаж (Saffron та ін., 9) | player | HP, мана (max, regen), сила зброї, Spell Power, Shield, Luck | рух на 1 клітину своєї 4×4; зброя персонажа незмінна; 2 заклинання в слотах |
| Заклинання (spell) | card (`+role:card`) | ціна мани, кулдаун, ефект, рідкість, Focus-категорія (10) | одноразово з колоди; апгрейд у меню колоди; деякі — «consume» (?) |
| Колода | supply | розмір = час перетасування | по черзі подає заклинання в 2 слоти |
| Артефакт | pickup | позитивний і негативний пасив | діє до кінця забігу |
| Ворог | enemy | HP, патерн атак | на ворожій 4×4; атакує клітини гравця |
| Яйце | spawner | — | з нього вилуплюється ворог (за нього більше EXP) |
| Структура | object | HP | займає ворожу клітину; на Hazard — більше EXP за знищення |
| Бос | boss | HP, атаки | наприкінці зони; переможений — вибір Spare / Execute |
| Заручник (hostage) | neutral | колір: червоний / зелений / чорний з капелюхом | порятунок — лікування / вибір артефакту / гроші; іде геть за часом |
| Клітина поля | terrain | ціла / зламана (тимчасово) | зламана — непрохідна |
| Sera | resource | — | гроші: крамниці; більше за бій без влучань |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, dir)` → ЯКЩО `free(target)` and `custom: «клітина своєї половини»` → ТО `move(player, dir)`; інакше `block`.
- КОЛИ `input(weapon)` → ТО `custom: «атака зброєю персонажа, без мани»`.
- КОЛИ `tick` → ТО `counter(mana, +regen)` до max.
- КОЛИ `input(cast, slot)` → ЯКЩО `counter(mana, >=, cost)` and `custom: «кулдаун минув»` → ТО `counter(mana, -cost)`, `custom: «ефект заклинання по клітинах»`, `custom: «effect draw_card: слот займає наступне заклинання колоди»`.
- КОЛИ `custom: «trigger deck_empty: заклинання в колоді скінчились»` → ТО `custom: «effect shuffle_deck: перетасування триває N с, N росте з розміром колоди»`.
- КОЛИ `input(shuffle)` → ТО `custom: «примусове перетасування будь-коли, навіть посеред бою»`.
- КОЛИ `contact(enemy_attack, player)` → ТО `damage(player, n)` мінус Shield.
- КОЛИ `custom: «ефект ламає клітину»` → ТО `set_cell(tile, broken)`; КОЛИ `custom: «минув час»` → ТО `set_cell(tile, normal)`.
- КОЛИ `all_gone(enemy)` → ТО `win` бою, `choose(new_spell)` (з урахуванням до 2 Focus), `counter(exp, +n)`; Hazard і бій без влучань — більше EXP і Sera.
- КОЛИ `counter(exp, >=, level_up)` → ТО `choose(artifact)`.
- КОЛИ `custom: «заручника врятовано»` → ТО `heal(player, n)` / `choose(artifact)` / `currency(+n)` за кольором; вбити заручника перед відходом — EXP.
- КОЛИ `hp_zero(boss)` → ТО `choose(spare|execute)`: Execute → `counter(exp, +n)`, `choose(epic_spell)`, `choose(artifact)`; Spare → без цих нагород, `custom: «бос потім допомагає в бою своїм ефектом»` (Terra ламає клітини, Hazel — турель, Selicy — Fragile трьом ворогам…).
- КОЛИ `custom: «фінал забігу»` → ЯКЩО `custom: «пощаджено всіх / частину / нікого»` → ТО `custom: «кінцівка Pacifist / Neutral / Genocide»`.
- КОЛИ `hp_zero(player)` → ТО `lose`, `custom: «заклинання й артефакти скидаються; шкала завершення лишається і відкриває персонажів і заклинання»`.
- Перемога: дійти до Eden через усіх босів зони · Поразка: HP 0 → новий забіг · Рахунок: —.

## Керування і ввід
- Клавіатура/геймпад: 4 напрямки руху на 1 клітину (опція Hold Movement — повільний автоповтор), кнопка зброї, 2 кнопки заклинань (лівий/правий слот), кнопка шафлу.
- `I` — меню колоди (Focus, апгрейд, видалення, порядок); `Tab` — мапа; `Esc` — меню; утримання `E` — превʼю заклинання (коли автопревʼю вимкнено).
- Після бою — вибір нового заклинання, утримання кнопки, щоб пропустити.

## Вікна, меню, HUD
- `main-menu` → `character-select` (9 персонажів) → `map-window` (розгалужена мапа з легендою вузлів) → бій.
- `game-screen` (бій): дві сітки 4×4, `hp-bar`, `energy-bar` мани, `+ui:spell-slots` (2 карти над головою персонажа з ціною), `+ui:shuffle-timer` (секунди перетасування), значок цілі заклинання на сітці.
- `+window:deck-builder` (клавіша I): колода, Focus (до 2), апгрейд / видалення / порядок, статы (зброя, Spell Power, Shield, Luck).
- `upgrade-window` після бою — вибір нового заклинання; після рівня — артефакт; після боса — Spare / Execute.
- `shop-window` (вузол крамниці: заклинання, max mana, regen); `pause-menu`; `settings-window` (Spell preview, Hold Movement, Angel mode); `end-screen` забігу; `achievements-window` (Steam).

## Фічі поза полем
- `meta-progression`: шкала завершення після кожного забігу відкриває персонажів і заклинання.
- `assist-mode` — Angel mode: полегшення, що не блокує досягнення.
- `mode-coop` і `mode-versus` — локальні (shared/split screen); у co-op двоє ділять одну колоду, у PvP — наперед задані колоди.
- `mod-support` — Steam Workshop; `cloud-save`, `achievements`; 13 мов.
- Luck підвищує рідкість закляттів/артефактів і складність (до 30); Focus (2 Luck за вибір) зсуває, які заклинання випадають.

## Варіації й родичі
- Базове ядро — [mega-man-battle-network](mega-man-battle-network.md) (поле на дві половини, бій карток у real-time); у Star Force — [mega-man-star-force](mega-man-star-force.md) — поле з-за спини і рух лише рядом.
- Колодо-роглайки в корпусі: [cobalt-core](cobalt-core.md), [monster-train](monster-train.md), [wildfrost](wildfrost.md).
- Duelists of Eden (2024) — PvP-спадкоємець того ж автора.
- **Осі варіацій**: доступ до карт — пауза-вибір 5 (MMBN) / 2 слоти + мана без паузи (OSFE) · «вартість» колоди — ліміт розміру / час перетасування · нагорода за боса — сила зараз (Execute) / союзник потім (Spare).

## Цікавинки для курсу
- Дві сітки 4×4 з забороною входу на чужу і превʼю цілі заклинання — 🌱.
- Два слоти + колода по черзі + мана з регеном і кулдауном — 📎 (стан руки як черга, а не множина).
- Перетасування, тривалість якого = f(розмір колоди): велика колода — довша «дірка» без заклинань — 🌱 (баланс розміру колоди одним числом).
- Spare / Execute: вибір нагороди «зараз» чи «союзник у наступних боях» + кінцівка за підсумком вибору — 📎.
- Заручники з таймером відходу й нагородою за кольором — 🌱.
- Розгалужена мапа вузлів з легендою типів — 🥉 (генерація DAG + вибір шляху).

## Мапа на каталог
- Є: `move-4dir` + `move-by-input` ↔ рух на 1 клітину · `hp-damage` · `impassable-cells` ↔ ворожа половина, зламані клітини · `status-effects` ↔ Fragile, Shield · `run-relics` ↔ артефакти · `shop-catalog` ↔ крамниці · `world-map` + `map-window` ↔ розгалужена мапа · `character-select` · `permadeath` ↔ смерть скидає забіг · `enemy-waves` · `game-screen` · `game-pause` + `pause-menu` · `end-screen` · `achievements-window`.
- **Нема** → пропозиції карток:
  - `+split-field-halves` · `+deck-draw` · `+draft-pick` · `+local-coop` · `+shared-field-versus` — уже пропонувались корпусом; тут: дві 4×4, колода по черзі, вибір заклинання після бою, кооп і PvP на одному екрані.
  - `+spell-slots-two` «Рука з 2 слотів, що поповнюються з колоди по черзі» · entities/state · 🌱 · слот {slots: 2}.
  - `+mana-regen-cost` «Мана з регеном, ціна і кулдаун заклинання» · game-logic/economy · 🌱 · слоти {max, regen}.
  - `+reshuffle-delay` «Перетасування колоди займає час ∝ розміру» · game-logic/turns · 🌱 · слот {sec_per_card}.
  - `+manual-reshuffle` «Скинути руку й перетасувати будь-коли» · interface/input · 🌱.
  - `+deck-focus-weights` «Вибір категорій, що частіше випадають у нагородах» · game-logic/economy · 🌱 · слот {focus: 2}.
  - `+spare-or-execute` «Пощадити боса (союзник потім) чи стратити (нагорода зараз)» · game-logic/score · 📎.
  - `+hostage-npc` «NPC на полі бою: врятуй до відходу — нагорода» · entities/interact · 🌱.
  - `+meta-progression` «Відкриття між забігами» · levels/progression · 🥉.
  - `+assist-mode` «Режим полегшення без штрафу» · game-logic/difficulty · 🌱.
  - `+mod-workshop` «Моди й Workshop» · levels/editor · 🥈.

## Пропозиції до словників
- `+role:card` — заклинання-карта як сутність поза полем (підтвердження корпусу).
- `+trigger:deck_empty` — колода скінчилась (старт перетасування); у корпусі вже пропонувалось.
- `+effect:draw_card` — слот руки поповнюється з колоди; `+effect:shuffle_deck` — перетасувати колоду з тривалістю.
- `+ui:spell-slots` — 2 карти над персонажем з ціною в мані; `+ui:shuffle-timer` — відлік до кінця перетасування.
- `+window:deck-builder` — меню колоди з Focus, апгрейдом і видаленням (підтвердження MMBN).
- `+axis:field=split-halves` — поле з двох половин зі своїм власником (підтвердження MMBN).

## Джерела
- ⭐ [Wikipedia: One Step From Eden](https://en.wikipedia.org/wiki/One_Step_From_Eden) — сітка 4×4 і окрема 4×4 ворогів, рух на клітину, мана, нове заклинання за бій, артефакти, розгалужена мапа, шкала відкриттів, co-op/PvP, натхнення MMBN, автор Thomas Moon Kang, видавець Humble, дати виходу.
- [Steam](https://store.steampowered.com/app/960690/) — 200+ заклинань, 100+ предметів, 9 персонажів, shared/split screen co-op і PvP, Workshop, 13 мов.
- [Steamah: Useful Tips for Beginners](https://steamah.com/one-step-from-eden-useful-tips-for-beginners/) — клавіші, Focus і Luck, час шафлу, стати, Hazard, заручники, Spare/Execute і кінцівки, Angel mode.
- [Local Indieverse: Beginner Tips](https://localindieverse.blogspot.com/2023/06/one-step-from-eden-beginner-tips-and.html) — 2 заклинання одночасно, ціна й кулдаун, шафл кнопкою, правка колоди після кімнати, артефакт за рівень.
- YouTube: [пошук «One Step From Eden gameplay»](https://www.youtube.com/results?search_query=One+Step+From+Eden+gameplay).

## Непевне
- (?) Статуси (Frost, Flow, Poison, Trinity, Flame) і що таке «consume»-заклинання — у відкритих джерелах не розписано; підтверджено лише Fragile і Shield.
- (?) 4 біоми — з однієї рецензії (JumpDashRoll), не перевірено.
- (?) Що саме і куди бʼє зброя кожного персонажа (гайд згадує маркер атаки на 4-й клітині попереду) — не розібрано.
- (?) Конкретні клавіші заклинань і шафлу за замовчуванням; підтверджено лише I, Tab, Esc, E.
- (?) Spare «дає 400 HP» у гайді — незрозуміле формулювання, у правила не взято.
