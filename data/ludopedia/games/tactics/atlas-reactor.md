---
title: Atlas Reactor
slug: atlas-reactor
aka: [AR]
family: tactics
also: []
klass: avatar
axes:
  field: square
  time: wego
  opponent: online
  info: hidden
  random: none
  goal: score
year: 2016
platforms: [Windows]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Atlas_Reactor", best: true, note: "4×4, 20 с на рішення, розвʼязка фазами Prep→Dash→Blast→Move, відкинутий не рухається, до 5 вбивств або 20 ходів, овертайм, ролі, закриття 2019"}
  - {kind: other, url: "https://atlasreactor.blogspot.com/p/getting-started-in-ar.html", note: "фан-блог: тайм-банк, lock in, що в якій фазі, спринт, перший раунд лише рух, каталізатори 3 × раз за матч, free actions"}
  - {kind: other, url: "https://atlasreactor.blogspot.com/p/tips.html", note: "фан-блог: низькі стіни, смугаста зона AoE, спільний огляд, маркер останнього місця, камуфляж-клітини, енергія, моди (бюджет 10), 4 пауер-апи"}
  - {kind: other, url: "https://atlasreactor.blogspot.com/p/what-is-ar.html", note: "фан-блог: режими, ранкед з драфтом і банами, без прокачки в матчі"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Atlas+Reactor+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [online-multiplayer, ai-opponent, lobby-window, match-setup, rating-system, character-select, fog-of-war, line-of-sight-attack, path-preview, threat-range, move-timer, respawn, hp-damage, status-effects, item-pickup, spawn-points, shop-window, end-screen, +simultaneous-turns, +phase-resolution-order, +knockback, +knockback-cancels-move, +dash-dodge, +sprint-no-action, +cover-system, +camouflage-brush, +last-seen-ghost, +shared-vision, +energy-ultimate, +catalyst-once-per-match, +ability-mods-budget, +free-actions, +trap-delayed, +body-block, +cooldown-ability, +kill-race-win, +overtime-sudden-death, +time-bank, +draft-mode, +teammate-plan-preview]
proposes: ["+trigger:lock_in", "+trigger:knocked_back", "+cond:revealed", "+cond:aoe_safe_zone", "+effect:knockback", "+effect:dash", "+effect:sprint", "+effect:root", "+effect:invisible", "+ui:lock-in-button", "+ui:time-bank", "+ui:plan-lines", "+ui:last-seen-marker", "+window:loadout", "+window:season-window", "+feature:free-rotation", "+feature:daily-missions"]
author: opus
date: 2026-11-09
---

# Atlas Reactor — XCOM з одночасними ходами: 20 секунд на план, потім усі дії розвʼязуються фазами Prep → Dash → Blast → Move

## Суть
Командна PvP-тактика 4 на 4 (Trion Worlds, 2016–2019): кожен гравець керує одним «фрилансером» на клітинній арені. Хід — це **одночасне планування за 20 секунд** і розвʼязка всіх наказів обох команд у фіксованому порядку фаз: спершу підготовка (щити, пастки), потім ривки, потім постріли й відкидання, і лише в кінці — рух. Тому вгадують, **де ворог буде**, а не де він є: можна ухилитися ривком, а відкинутий ворог уже не встигне втекти. Мета — перша команда з 5 вбивствами.

## Поле і час
- Квадратна сітка арени: низькі стіни (укриття), високі обʼєкти (блокують атаки й огляд), камуфляж-клітини, пади пауер-апів.
- Раунд = Decision (20 с, тайм-банк +5 с двічі за матч; проти ботів таймер без штрафу) → Resolution: **Prep → Dash → Blast → Move**.
- Усередині фази дії рахуються одночасно, а показуються по черзі: персонаж, якого «вбили» раніше в показі, доживає до кінця своєї дії.
- Огляд спільний на команду, у кожного обмежений радіус; поза оглядом ворог — маркер останнього відомого місця, його дії — «hidden action».
- Безкінечні респавни; матч — до 5 вбивств або 20 раундів + овертайм із раптовою смертю.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фрилансер Firepower | player | HP, енергія, 4–5 здібностей, кулдауни | основна шкода |
| Фрилансер Frontline | player | HP, енергія | танк, ривки, відкидання, контроль |
| Фрилансер Support | player | HP, енергія | лікування, щити, бафи у Prep |
| Союзник / ворог | ally / enemy | те саме | такі ж фрилансери інших гравців або ботів |
| Пастка | hazard | відкладена шкода | ставиться в Prep, шкодить тому, хто зайде пізніше |
| Щит / баф | object | на раунд (?) | ставиться в Prep, до будь-якої шкоди |
| Низька стіна | terrain | — | зменшує шкоду від більшості дальніх атак |
| Висока стіна | static | — | блокує атаки й лінію огляду |
| Камуфляж-клітини («блискучі») | terrain | група клітин | на них невидимий, якщо нема статусу Revealed; червоні — тимчасово вимкнені; вороги в одній групі бачать одне одного |
| Пауер-ап здоровʼя (зелений) | pickup | — | лікує |
| Пауер-ап Haste (синій) | pickup | — | прискорення руху |
| Пауер-ап Might (червоний) | pickup | — | підсилення шкоди |
| Пауер-ап енергії (жовтий) | pickup | — | енергія для ультимейта |
| Пад пауер-апу | spawner | 3 позначки | показує, коли зʼявиться бонус; з трьома позначками — спавн на початку наступного раунду |
| Каталізатор | object | 3 на матч: Prep, Dash, Blast | одноразовий бонусний ефект |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(decision)` → ТО `timer(start, 20)`.
- КОЛИ `custom: «20 с вичерпано»` → ЯКЩО `custom: «тайм-банк не витрачено (2 × 5 с)»` → ТО `timer(+5)`.
- КОЛИ `input(lock_in)` → ТО `custom: «план прийнято»`; без lock-in наказ не зараховується.
- КОЛИ `input(order, freelancer)` → ТО `custom: «за раунд: одна активна здібність + наказ руху, вільні дії — додатково, каталізатор — не більше одного за раунд»`.
- КОЛИ `custom: «перший раунд матчу або перший після респавну»` → ТО `custom: «дозволено лише рух/спринт»`.
- КОЛИ `phase_start(prep)` → ТО `custom: «лікування, щити, бафи, частина дебафів, пастки»` — до будь-якого руху й шкоди.
- КОЛИ `phase_start(dash)` → ТО `move(freelancer, dash_target)` — ухилення або ривок з шкодою; ЯКЩО `custom: «зробив ривок»` → ТО `custom: «у фазі Move не рухається»` (крім окремих героїв, напр. Kaigin).
- КОЛИ `phase_start(blast)` → ТО `damage(targets, n)` усіх пострілів одночасно, потім `push(targets)` відкиданням.
- КОЛИ `custom: «ціль відкинуто в Blast»` → ТО `set_state(target, no_move, 1)` — її рух цього раунду скасовано.
- КОЛИ `phase_start(move)` → ТО `move(freelancer, planned_path)`; ЯКЩО `custom: «не використав активної здібності»` → ТО `custom: «спринт: більша дальність»`.
- КОЛИ `custom: «на шляху руху інший персонаж / корінь / сповільнення»` → ТО `block` або `speed(freelancer, -n)`.
- КОЛИ `enter(enemy, trap)` → ТО `damage(enemy, n)` (відкладена шкода).
- КОЛИ `custom: «дальня атака через низьку стіну»` → ТО `custom: «шкода зменшена»`.
- КОЛИ `custom: «між стрільцем і ціллю висока стіна»` → ТО `block`.
- КОЛИ `custom: «ціль у смугастій частині зони AoE»` → ТО `custom: «шкоди нема»`.
- КОЛИ `enter(freelancer, camo_cell)` → ЯКЩО `not state(freelancer, revealed)` → ТО `set_state(freelancer, invisible)`.
- КОЛИ `leave(freelancer, camo_cell)` → ТО `clear_state(freelancer, invisible)`.
- КОЛИ `custom: «ворог вийшов з огляду команди»` → ТО `custom: «маркер останнього відомого місця»`; його наказ показано як «hidden action».
- КОЛИ `custom: «здібність влучила»` → ТО `counter(energy, +n)` (більше цілей — більше енергії).
- КОЛИ `turn_start` → ТО `counter(energy, +small)`.
- КОЛИ `input(ultimate, freelancer)` → ЯКЩО `counter(energy, ≥, cost)` → ТО `custom: «ультимейт (часто у фазі Blast)»`, `counter(energy, -cost)`.
- КОЛИ `input(ability)` → ЯКЩО `custom: «кулдаун минув»` → ТО `custom: «здібність»`, `timer(start, cooldown)`.
- КОЛИ `input(catalyst, type)` → ЯКЩО `custom: «цього типу ще не використано за матч»` і `custom: «цього раунду каталізатора не було»` → ТО `custom: «ефект каталізатора»`.
- КОЛИ `enter(freelancer, power_up)` → ТО `pickup`, `heal|set_state(haste|might)|counter(energy, +n)`.
- КОЛИ `counter(pad_pips, ==, 3)` → ТО `spawn(power_up)` на початку наступного раунду.
- КОЛИ `hp_zero(freelancer)` → ТО `disappear(freelancer)`, `counter(enemy_kills, +1)`, `respawn(freelancer)` пізніше (?).
- КОЛИ `counter(kills, ==, 5)` → ТО `win` команди.
- КОЛИ `counter(round, ==, 20)` → ЯКЩО `custom: «у команди більше вбивств»` → ТО `win`; інакше `custom: «овертайм з раптовою смертю»`.
- Перемога: 5 вбивств або більше вбивств після 20 раундів · Поразка: навпаки · Рахунок: вбивства команди.

## Керування і ввід
- Миша: вибір здібності → клік по клітині/напрямку → превʼю дуги атаки, ривка (жовта лінія), відкидання (червоні лінії можливих місць); правий клік — точка руху (суцільна лінія — повний рух, пунктир — спринт), вейпоінти в обхід пасток.
- Правий клік по персонажу — «слідувати»; ще раз — іти на його поточну клітину.
- Видно плани союзників: дуги, білі лінії руху, енергію; Alt — кулдауни й каталізатори ворогів.
- Кнопка Lock in; таймер раунду; тайм-банк.

## Вікна, меню, HUD
- `lobby-window` / `mode-select`: ранкед (соло/дуо, драфт, бани, обмін героями з тіммейтом), анранкед PvP, проти ботів, кастомні ігри (власник повної гри — кілька персонажів).
- `character-select` + `custom-window` лоадаут (`+window:loadout`): моди здібностей (бюджет 10, один мод на здібність, ціна 1–3), каталізатори за категоріями, скіни.
- `game-screen`: сітка, `hp-bar` і жовтий `energy-bar` під ним, `skill-bar` з кулдаунами, `+ui:lock-in-button`, `timer-countdown` і `+ui:time-bank`, `+ui:plan-lines` (рух/ривок/відкидання), `+ui:last-seen-marker`, лічильник вбивств і раундів, `fog-overlay`.
- `end-screen` — результат і нагороди; `custom-window` сезону (`+window:season-window`): рівні сезону, глави місій, щоденна місія на вибір; `shop-window` — фрилансери за гроші або ігрову валюту; `settings-window`.

## Фічі поза полем
- `online-multiplayer` 4×4, ранкед з рейтингом, `ai-opponent-levels` (боти), кастомні ігри.
- Модель: спершу «спробуй до покупки» з ротацією фрилансерів, з 17.01.2017 — free-to-play (`+feature:free-rotation`).
- Сезони з рівнями (обнуляються, сумуються в Reactor Level), `+feature:daily-missions`, GG-бусти досвіду; без прокачки й магазину всередині матчу.
- Закрито 28.06.2019.

## Варіації й родичі
- Родичі в корпусі: [Frozen Synapse](frozen-synapse.md) (WEGO, але вільне поле й 5 с симуляції), [XCOM](xcom.md) (укриття, огляд), [Into the Breach](into-the-breach.md) (фіксований порядок розвʼязки й відкидання), [Duelyst](duelyst.md) (PvP на сітці).
- **Осі варіацій**: структура ходу — по черзі / WEGO з фазами за типом дії (AR) / WEGO із симуляцією часу ([Frozen Synapse](frozen-synapse.md)) · відкидання — зсув (AR: ще й скасовує рух) / шкода об стіну ([Into the Breach](into-the-breach.md)) · огляд — повний / спільний туман із маркерами останнього місця (AR).

## Цікавинки для курсу
- Фазова розвʼязка одночасних наказів: зібрати накази, відсортувати за фазою, у фазі застосувати всі разом — 🥈.
- Відкидання скасовує запланований рух — один прапорець, що змінює всю тактику — 🌱.
- «Мертвий доживає до кінця своєї дії» — розділення розрахунку і показу (логіка vs анімація) — 📎.
- Таймер планування з тайм-банком — 🌱.
- Камуфляж-клітини з групами (вороги в одній групі бачать одне одного) і статус Revealed — 📎.
- Бюджет модів (≤10, ≤1 на здібність) як валідація лоадауту — 🌱.

## Мапа на каталог
- Є: `online-multiplayer` · `ai-opponent` (боти) · `lobby-window` · `match-setup` (кастом) · `rating-system` (ранкед) · `character-select` · `fog-of-war` (спільний огляд) · `line-of-sight-attack` · `path-preview` · `threat-range` (дуги атак) · `move-timer` (20 с) · `respawn` · `hp-damage` · `status-effects` · `item-pickup` + `spawn-points` (пади пауер-апів) · `shop-window` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+phase-resolution-order` «Розвʼязка одночасних наказів фазами за типом дії» · game-logic/turns · 🥈 · слот {phases: list}.
  - `+knockback-cancels-move` «Відкинутий втрачає рух цього ходу» · entities/move · 🌱.
  - `+dash-dodge` «Ривок до фази атаки як ухилення» · entities/move · 📎.
  - `+sprint-no-action` «Без дії — довший рух» · game-logic/turns · 🌱.
  - `+camouflage-brush` «Клітини-невидимки з групами огляду» · interface/render · 📎.
  - `+shared-vision` / `+last-seen-ghost` «Спільний огляд команди і маркер останнього місця» · interface/render · 📎.
  - `+energy-ultimate` «Ультимейт за енергію від влучань» · entities/state · 🌱.
  - `+catalyst-once-per-match` «Три одноразові бонуси на матч, ≤1 за раунд» · game-logic/economy · 🌱.
  - `+ability-mods-budget` «Моди здібностей з бюджетом» · interface/menus · 📎.
  - `+kill-race-win` / `+overtime-sudden-death` «До N вбивств, ліміт раундів, овертайм» · game-logic/win · 🌱.
  - `+time-bank` «Тайм-банк понад таймер ходу» · game-logic/opponent · 🌱.
  - `+teammate-plan-preview` «Видно плани тіммейтів до розвʼязки» · interface/hud · 📎.
  - `+simultaneous-turns` / `+knockback` / `+cover-system` / `+free-actions` / `+trap-delayed` / `+body-block` / `+cooldown-ability` / `+draft-mode` — уже в корпусі або дрібні.

## Пропозиції до словників
- `+trigger:lock_in` — гравець підтвердив план раунду.
- `+trigger:knocked_back` — сутність відкинуто (скасування руху).
- `+cond:revealed` — сутність має статус Revealed (не ховається в камуфляжі).
- `+cond:aoe_safe_zone` — ціль у безпечній (смугастій) частині зони ураження.
- `+effect:knockback` — відкинути ціль від джерела; `+effect:dash` — ривок до фази атак; `+effect:sprint` — рух з більшою дальністю без дії.
- `+effect:root` — сутність не може рухатися (корінь); `+effect:invisible` — сховати сутність від ворожого огляду.
- `+ui:lock-in-button` · `+ui:time-bank` · `+ui:plan-lines` (лінії руху/ривка/відкидання) · `+ui:last-seen-marker`.
- `+window:loadout` — моди й каталізатори перед матчем; `+window:season-window` — сезонний прогрес.
- `+feature:free-rotation` — тижнева ротація безкоштовних персонажів; `+feature:daily-missions` — щоденна місія на вибір.

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/Atlas_Reactor) — формат 4×4, Decision 20 с, порядок фаз і що в кожній, відкинутий не рухається, одночасність усередині фази, 5 вбивств / 20 ходів / овертайм, ролі, сезони, модель, закриття 28.06.2019.
- [The Reactor Core: Getting Started](https://atlasreactor.blogspot.com/p/getting-started-in-ar.html) — тайм-банк, lock in, плани союзників, вміст фаз, ривок без руху, спринт, перший раунд, каталізатори, free actions.
- [The Reactor Core: Tips](https://atlasreactor.blogspot.com/p/tips.html) — низькі й високі стіни, смугаста зона AoE, спільний огляд, «hidden action», камуфляж і Revealed, енергія, моди, 4 пауер-апи і пади.
- [The Reactor Core: What is AR](https://atlasreactor.blogspot.com/p/what-is-ar.html) — режими, ранкед із драфтом і банами, без прокачки в матчі.

## Непевне
- (?) Чи є в бою випадковість (крити, шанс) — не бачив; `random: none` за описами детермінованої розвʼязки.
- (?) Скільки енергії треба на ультимейт і скільки дає пасивно — числа не знайдені.
- (?) Затримка респавну і де саме відроджуються.
- (?) Наскільки низька стіна зменшує шкоду і чи залежить від напрямку.
- (?) Режим Extraction — лише згадка в блозі.
- (?) Тривалість щитів і бафів з Prep.
