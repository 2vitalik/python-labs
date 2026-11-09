---
title: Triangle Strategy
slug: triangle-strategy
aka: [Project Triangle Strategy, TS]
family: tactics
also: []
klass: figure
axes:
  field: layers
  time: turn
  opponent: ai
  info: full
  random: none
  goal: state
year: 2022
platforms: [Switch, PC, PS5, Xbox Series, Meta Quest]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Triangle_Strategy", best: true, note: "бій на сітці, TP, затиск з двох боків, удар зі спини і згори, Kudos/Quietus, стихії на терені, ваги переконань"}
  - {kind: steam, url: "https://store.steampowered.com/app/1850510/", note: "офіційний опис: висота, follow-up при фланзі, переконання Utility/Morality/Liberty, табір, Mental Mock Battles"}
  - {kind: official, url: "https://www.nintendo.com/en-ca/whatsnew/tips-for-getting-started-with-triangle-strategy/", note: "поради Nintendo: черга ходів унизу, кольори клітин небезпеки, ланцюг стихій лід→вода→блискавка, драбини"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Triangle+Strategy+battle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [hp-damage, melee-vs-ranged, height-levels, orientation-state, legal-move-highlight, threat-range, hover-highlight, cell-transform, floor-types, push-object, environment-death, chain-reaction, status-effects, unit-xp-skills, inventory-items, shop-between-levels, destroy-all-enemies, player-death, ai-opponent, difficulty-levels, save-multi-slot, placement-screen, character-select, world-map, +pincer-follow-up, +back-attack-bonus, +height-attack-bonus, +speed-turn-order, +tactical-points, +quietus-team-skill, +elemental-terrain-combo, +party-vote, +branching-campaign, +ladder-build]
proposes: ["+cond:behind", "+cond:higher", "+cond:pincer", "+effect:follow_up", "+effect:delay_turn", "+trigger:attacked", "+ui:turn-order-bar", "+ui:follow-up-marker", "+ui:damage-forecast", "+window:vote-window", "+window:exploration-screen", "+window:camp-screen", "+feature:new-game-plus", "+axis:turn-structure=speed-queue"]
author: opus
date: 2026-11-09
---

# Triangle Strategy — тактика-діорама: затисни ворога з двох боків, бий згори й зі спини, поєднуй стихії на терені

## Суть
Загін героїв воює на тривимірних клітинних мапах з перепадами висоти проти AI. Ядро — **позиція відносно цілі**: двоє союзників з протилежних боків ворога дають безкоштовну додаткову атаку (follow-up), удар зі спини або згори сильніший. Друге ядро — стихії, що змінюють клітини: вогонь підпалює підлогу, лід тане у воду, блискавка по воді бʼє всіх, хто в ній стоїть, вітер зіштовхує з урвищ. Між боями — голосування загону на «вагах переконань», яке гілкує кампанію.

## Поле і час
- Поле — квадратна сітка з **висотами** (`layers`): дахи, схили, скелі, мости; рух угору обмежений параметром стрибка (?); подекуди можна поставити драбину, щоб залізти вище.
- Камера обертається навколо діорами; клітини підсвічуються кольорами небезпеки.
- Час — покроковий, але **черга ходів за Speed** окремих юнітів обох сторін (не фаза «всі мої → всі ворожі»); черга показана внизу екрана. Хід юніта: рух + одна дія (більшість), напрям погляду в кінці (?).
- Випадковості в бою мало: шкода детермінована до прогнозу, криті й ухилення — (?). Мапи фіксовані.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой (Serenoa та ін.) | piece | HP, TP, Move, Jump (?), Speed, Atk/Def/Mag, клас, рівень | рух у межах Move, атака/навичка, після бою — досвід і рівень |
| Лучник / маг / цілитель | piece | дальність, стихія | атаки на відстані, дальність лучника росте з висотою (?) |
| Ворожий солдат | enemy | ті самі параметри | AI: іде до найвигіднішої цілі, теж використовує фланг і висоту |
| Ворожий командир | boss | більше HP, навички | ціль місії «перемогти ватажка» |
| Клітина висоти / урвище | terrain | рівень висоти | дає бонус атакувальнику згори; падіння вниз при зіштовхуванні (?) |
| Палаюча клітина | hazard | тривалість | шкодить тому, хто стоїть / заходить; заважає руху |
| Крижана клітина | terrain | — | створює маг льоду; тане від вогню у воду |
| Вода / калюжа | terrain | — | проводить блискавку на всіх у звʼязній воді |
| Драбина | object | — | ставиться спецнавичкою, відкриває підйом |
| Руйнівна споруда (будинок, вагонетка) | object | HP (?) | можна зруйнувати / пустити, щоб замкнути чи вдарити ворога |
| Предмет-витратник | supply | спільний запас на бій (?) | лікує / знімає стан, витрачає дію |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(unit)` → ТО `counter(TP, +1)` (до максимуму, ?) — TP накопичується між ходами.
- КОЛИ `input(move, unit, cell)` → ЯКЩО `path_exists(unit, cell)` and `custom: «у межах Move і Jump»` → ТО `move(unit, cell)`.
- КОЛИ `input(attack, unit, target)` → ЯКЩО `in_range(unit, target, range)` → ТО `damage(target, n)`; звичайна атака TP не коштує.
- КОЛИ `input(skill, unit, target)` → ЯКЩО `counter(TP, >=, cost)` → ТО `counter(TP, −cost)`, `custom: «ефект навички»`.
- Фланг: КОЛИ `after(attack)` → ЯКЩО `custom: «союзник стоїть з протилежного боку цілі (pincer)»` and `custom: «атака фізична»` → ТО `custom: «союзник робить безкоштовну додаткову атаку (follow-up)»`.
- КОЛИ `input(attack, unit, target)` → ЯКЩО `custom: «атакувальник за спиною цілі»` → ТО `custom: «шкода більша (back attack)»`.
- КОЛИ `input(attack, unit, target)` → ЯКЩО `custom: «атакувальник вище за ціль»` → ТО `custom: «шкода більша»`; нижче — менша (?).
- КОЛИ `input(skill(fire), unit, cell)` → ТО `damage(area, n)`, `set_cell(cell, burning)`; ЯКЩО `cell(cell, ice)` → ТО `set_cell(cell, water)`.
- КОЛИ `enter(unit, burning)` або `turn_start(unit)` → ЯКЩО `cell(under, burning)` → ТО `damage(unit, n)`.
- КОЛИ `input(skill(lightning), unit, cell)` → ЯКЩО `cell(cell, water)` → ТО `custom: «уражено всіх у звʼязній воді»`, `set_state(target, paralysis, dur)` (?).
- КОЛИ `input(skill(wind), unit, target)` → ТО `push(target)`; ЯКЩО `custom: «за ціллю урвище / край»` → ТО `fall(target)`, `damage(target, n)` (?).
- КОЛИ `input(skill(ice), unit, cell)` → ТО `set_cell(cell, ice)`, `custom: «сповільнює / заважає рухові»` (?).
- КОЛИ `input(wait, unit)` → ТО `end_turn`, `custom: «наступний хід юніта настане раніше»` (?).
- КОЛИ `input(item, unit, ally)` → ЯКЩО `has(party, item)` → ТО `use(unit, item)`, `heal(ally, n)` / `clear_state(ally, s)`.
- Kudos: КОЛИ `custom: «follow-up, удар зі спини, вбивство, стихійне комбо»` → ТО `counter(kudos, +n)`.
- КОЛИ `input(quietus, q)` → ЯКЩО `counter(kudos, >=, cost)` → ТО `custom: «разова дія на весь загін: воскресити, +Move усім, …»`.
- КОЛИ `hp_zero(unit)` → ТО `disappear(unit)` з бою — без перманентної смерті.
- КОЛИ `hp_zero(serenoa)` → ТО `lose` (?).
- Перемога: `all_gone(enemy)` або `destroyed(boss)` чи спеціальна ціль мапи → ТО `win`, `window(end-screen)` з досвідом і грошима.
- Ваги переконань: КОЛИ `custom: «ключове рішення»` → ТО `window(vote-window)`; кожен член ради голосує; переконати можна аргументами, знайденими під час дослідження → `choose(branch)`.

## Керування і ввід
- Курсор по клітинах (геймпад або миша): вибір юніта в його хід → синя зона руху → клітина → меню дій (Attack, Skills, Items, Wait).
- Наведення на ціль показує прогноз шкоди й маркер follow-up; навести на порожню клітину й натиснути кнопку — номери черги ходів (?).
- Обертання камери, перемикання на огляд мапи, перегляд параметрів ворога та його зони атаки.
- Перед боєм — розстановка: вибір юнітів і стартових клітин.

## Вікна, меню, HUD
- `main-menu`: New Game, Continue, Load, Settings; New Game+ після проходження.
- `game-screen`: діорама; `legal-move-highlight` (сині клітини), `threat-range` (фіолетові — досягає ворог, червоні лінії — хто саме може атакувати), червоні клітини — куди атакує поточний юніт; `turn-order-bar` унизу; `hp-bar`, TP-піпси; `follow-up-marker`, `damage-forecast`; Kudos-лічильник.
- `placement-screen` — розстановка й вибір загону (`character-select`).
- `exploration-screen` — вільне дослідження локації: розмови з NPC, предмети, гроші, аргументи для голосування.
- `vote-window` — ваги переконань: варіанти, голоси членів ради, спроби переконати.
- `camp-screen` — табір: крамниця, кузня (поліпшення зброї), таверна з Mental Mock Battles, розмови.
- `map-window` — мапа світу з вузлами подій.
- `end-screen` — підсумок бою; `pause-menu`; `settings-window` (складність, камера, текст).

## Фічі поза полем
- Кампанія з гілками за голосуванням; накопичення переконання Utility / Morality / Liberty визначає, хто з героїв приєднається; 4 кінцівки.
- `new-game-plus` — вища складність і нові гілки; `difficulty-presets`; `save-slots`.
- Mental Mock Battles — тренувальні бої для досвіду, включно з боями з особливими умовами перемоги.
- Поліпшення зброї й класів героїв (кузня), Quietus-уміння купуються за Kudos.

## Варіації й родичі
- Родичі: Final Fantasy Tactics і Tactics Ogre (висота, удар зі спини, черга за швидкістю — див. [final-fantasy-tactics](final-fantasy-tactics.md)), Fire Emblem (табір, підтримки — [fire-emblem](fire-emblem.md)), Into the Breach (зіштовхування з урвищ — [into-the-breach](into-the-breach.md)), Divinity: Original Sin (стихійні поверхні — поза корпусом).
- Осі варіацій:
  - **фланг**: бонус від напряму погляду цілі (FFT) / pincer з двох боків дає безкоштовну атаку (TS) / фланг ламає укриття ([xcom](xcom.md));
  - **черга ходів**: фази сторін (FE) / черга за Speed по юнітах (FFT, TS) / почергово сторони ([banner-saga](banner-saga.md));
  - **стихії на клітинах**: нема / клітина змінює тип і реагує на іншу стихію (TS, DOS).

## Цікавинки для курсу
- Pincer + follow-up: перевірити, чи союзник на протилежній від атакувальника клітині відносно цілі, і запустити його атаку — 📎.
- Бонус удару зі спини й згори (напрям погляду + висота) — 📎.
- Ланцюг стихій: лід → (вогонь) → вода → (блискавка) уражує всю звʼязну водойму — 🥉 (заливка BFS по типу клітини).
- Вітер-поштовх з падінням з урвища — 🥉.
- Черга ходів за Speed з показом майбутнього порядку — 🥉 (симуляція черги наперед).
- Голосування з вагами й переконанням радників — 🥉 (вікно поза полем зі станом).

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` ↔ лучники й маги · `height-levels` ↔ висоти діорами · `orientation-state` ↔ напрям погляду · `legal-move-highlight` / `threat-range` / `hover-highlight` · `cell-transform` + `floor-types` ↔ вогонь/лід/вода · `push-object` + `environment-death` ↔ вітер з урвища · `chain-reaction` ↔ стихійне комбо · `status-effects` · `unit-xp-skills` · `inventory-items` · `shop-between-levels` ↔ табір · `destroy-all-enemies` · `player-death` ↔ падіння Serenoa (?) · `placement-screen` · `character-select` · `world-map` · `difficulty-levels` · `save-multi-slot`.
- **Нема** → пропозиції карток:
  - `+pincer-follow-up` «Затиск з двох боків → додаткова атака» · entities/combat · 📎 · слот {needs: physical}.
  - `+back-attack-bonus` «Удар зі спини» · entities/combat · 📎 (родич `+facing-hit-bonus` з FFT).
  - `+height-attack-bonus` «Бонус атаки згори» · entities/combat · 🌱.
  - `+speed-turn-order` «Черга ходів юнітів за швидкістю» · game-logic/opponent · 🥉.
  - `+tactical-points` «Очки на навички, що накопичуються щоходу» · entities/combat · 📎.
  - `+quietus-team-skill` «Разова командна дія за очки стилю» · entities/combat · 📎.
  - `+elemental-terrain-combo` «Стихії міняють клітини і реагують між собою» · entities/legality · 🥉.
  - `+party-vote` «Голосування загону з переконанням» · interface/menus · 🥉.
  - `+branching-campaign` «Кампанія з гілками за рішеннями» · progression · 📎.
  - `+ladder-build` «Поставити драбину на висоту» · entities/legality · 🌱.

## Пропозиції до словників
- `+cond:behind(a, b)` — A стоїть за спиною B (з напряму погляду B).
- `+cond:higher(a, b)` — A на вищому рівні висоти, ніж B.
- `+cond:pincer(a, t, b)` — A і B на протилежних клітинах відносно T.
- `+effect:follow_up(a, t)` — A робить безкоштовну додаткову атаку по T.
- `+effect:delay_turn(a, n)` — зсунути юніта в черзі ходів (Wait, навички).
- `+trigger:attacked(a, b)` — A атакував B (ланцюг: follow-up, контратака).
- `+ui:turn-order-bar` — смуга майбутньої черги ходів; `+ui:follow-up-marker` — значок «буде додаткова атака»; `+ui:damage-forecast` — прогноз шкоди на полосці HP.
- `+window:vote-window` — голосування ради; `+window:exploration-screen` — вільна локація з NPC між боями; `+window:camp-screen` — табір з крамницями й тренуваннями.
- `+feature:new-game-plus` — повтор кампанії зі збереженим прогресом.
- `+axis:turn-structure=speed-queue` — черга окремих юнітів за швидкістю (TS, FFT).

## Джерела
- ⭐ [Wikipedia: Triangle Strategy](https://en.wikipedia.org/wiki/Triangle_Strategy) — сітка, TP, затиск з двох боків, бонус зі спини й згори, Kudos/Quietus, вогонь на землі, мокрий терен і блискавка, вітер з урвищ, голосування, без permadeath.
- [Steam: Triangle Strategy](https://store.steampowered.com/app/1850510/) — висота, follow-up при фланзі, Utility/Morality/Liberty, табір, Mental Mock Battles.
- [Nintendo: поради для початку](https://www.nintendo.com/en-ca/whatsnew/tips-for-getting-started-with-triangle-strategy/) — черга ходів унизу, кольори клітин небезпеки, лід→вода→блискавка, драбини.
- YouTube: пошук «Triangle Strategy battle gameplay».

## Непевне
- (?) Точний приріст і максимум TP (у пошукових поясненнях — «1 на старті, +1 щоходу»), і чи Wait дає додатковий TP.
- (?) Чи можна рухатись після дії, і як задається напрям погляду наприкінці ходу.
- (?) Розмір бонусу зі спини (гарантований крит чи множник) і штраф атаки знизу.
- (?) Шкода від падіння з урвища, параліч від блискавки, сповільнення на льоду.
- (?) Чи падіння Serenoa — поразка в усіх боях; ліміт предметів на бій.
- (?) Дальність лучника залежно від висоти; параметр Jump.
