---
title: Loophole
slug: loophole
aka: []
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: partial
  random: none
  goal: state
year: 2025
platforms: [PC, Mac]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3629400/Loophole/", best: true, note: "суть: машини часу, минулі «я» повторюють щойно зроблене, вибухи за кілька клітин; редактор, Workshop, Cloud, 11 мов"}
  - {kind: other, url: "https://github.com/loophole-game/community-levels-guide/blob/main/README.md", note: "гайд спільноти: онлайн-редактор, JSON-рівень, шлях у меню Community Levels"}
  - {kind: other, url: "https://github.com/loophole-game/community-levels-guide", note: "levelSchema.ts — офіційна схема рівня: усі типи сутностей, вибухи, правила накладання"}
  - {kind: other, url: "https://github.com/loophole-game/loophole-level-editor", note: "відкритий веб-редактор (React + canvas); описи сутностей і пікапів"}
  - {kind: play, url: "https://loophole-game.github.io/loophole-level-editor/", note: "онлайн-редактор рівнів"}
  - {kind: other, url: "https://itch.io/post/15431530", note: "коментар до Chrono Break (джем-клон Loophole): «не можна дати минулому собі побачити тебе — парадокс»"}
  - {kind: steam, url: "https://store.steampowered.com/app/4051150/Chronigma/", note: "Chronigma (2025) — сестра-механіка: запис дій і співпраця з минулим собою"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Loophole+time+travel+puzzle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-4dir, move-by-input, keyboard-controls, push-object, impassable-cells, one-way-cell, button-toggle, item-pickup, status-effects, fog-of-war, reach-exit, restart-level, sequential-levels, level-select, level-exchange, state-as-data, achievements-window, save-progress, +time-clone-replay, +paradox-sighting, +edge-walls, +advancing-hazard-front, +zone-time-stop, +vision-blockers, +replay-solved-levels, +external-level-editor, +level-json-schema]
proposes: ["+trigger:sighted", "+trigger:paradox", "+effect:time_travel", "+role:echo", "+card:time-clone-replay", "+card:paradox-sighting", "+card:edge-walls", "+card:advancing-hazard-front", "+card:vision-blockers", "+card:external-level-editor", "+card:level-json-schema", "+feature:workshop"]
author: opus
date: 2026-11-09
---

# Loophole — Sokoban про подорожі в часі: проходиш крізь машину часу, і твої щойно зроблені ходи повторює минулий «ти»

## Суть
Лабіринт на квадратній сітці от-от знищать вибухи, що насуваються з країв. Машина часу повертає героя в минуле, де на нього вже чекають **минулі «я»** — копії, що точно повторюють щойно виконані дії. Вони можуть допомогти (тримати кнопку, нести посох) або заважати (стати на шляху, побачити тебе й спричинити парадокс). Гравець планує одну «петлю» так, щоб майбутня копія зробила потрібне, а сам — дійшов до виходу. Поруч — стіни на ребрах клітин, що по-різному блокують рух і погляд, туман невідкритого, гриби-статуси й клітина, де час стоїть.

## Поле і час
- Квадратна сітка з координатами до ±192 × ±104 у схемі рівня; стіни лежать **на ребрах** між клітинами (позиція ребра = клітина + `RIGHT`/`TOP`).
- Глобальний час — лічильник ходів; вибухи — функція часу: фронт у напрямку `RIGHT/UP/LEFT/DOWN`, у момент `startTime` досягає координати `startPosition`, просувається на клітину раз на `period` ходів (може бути дробовим — два кроки за хід). На рівень — не більше одного фронту в кожному напрямку.
- Видимість: стіни, штори, односторонні ребра й двері закривають погляд; невідкриті ділянки — туман; рівень може відкрити все одразу (`automaticallyDiscoverVision`).
- Покроково; ізометрична 2.5D-камера; 7 палітр підлога/стіни.
- Рівні згруповані в регіони; спільнотні рівні — з другого регіону.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | статуси від грибів | крок 4 напрямки; бере посох; з червоним грибом штовхає обʼєкти |
| Минулий «я» (echo) | ally | записана послідовність дій | повторює дії, зроблені до стрибка в часі; може допомогти або заважати |
| Машина часу | static | напрям проходу; має власні стіни й двері | вхід рівня (герой зʼявляється в ній); прохід крізь іншу — повернення в минуле |
| Вихід | static | — | мета рівня |
| Стіна (ребро) | static | ребро | блокує рух і погляд |
| Штора (ребро) | static | ребро | блокує погляд, пропускає рух |
| Скло (ребро) | static | ребро | блокує рух, пропускає погляд |
| Одностороннє ребро | static | напрям | блокує погляд; рух — лише в один бік |
| Двері (ребро) | gate | канал | блокують рух і погляд, доки канал не активний |
| Кнопка | switch | канал | активує канал, поки на ній герой, минулий «я» або посох |
| Дріт | mark | канал, прямий/кут | декор, що показує звʼязок кнопка → двері; світиться, коли канал активний |
| Посох (staff) | object | — | герой піднімає й переносить; тримає кнопку |
| «Соус» (sauce) | terrain | — | клітина, у якій час не йде |
| Синій гриб | pickup | статус | робить героя невидимим |
| Зелений гриб | pickup | статус | герой «інакше сприймає час» (?) |
| Червоний гриб | pickup | статус | герой може штовхати обʼєкти |
| Очисна купіль | terrain | — | знімає всі статуси грибів |
| Фронт вибухів | hazard | напрям, startTime, startPosition, period | насувається з часом; повернення в минуле відсуває його назад |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `custom: «на ребрі в напрямку руху нема стіни/скла/зачинених дверей/зустрічного одностороннього»` → ТО `move(hero, dir)`; інакше `block`.
- КОЛИ `tick` → ТО `counter(time, +1)`; ЯКЩО `occupied(cell, hero)` and `cell(cell, sauce)` → ТО `custom: «час для героя не йде»` (?).
- КОЛИ `tick` → ТО `custom: «кожен фронт вибухів стає на позицію startPosition + (time − startTime) / period»`.
- КОЛИ `contact(explosion, hero)` → ТО `lose` (?).
- КОЛИ `enter(hero, time_machine)` → ТО `custom: «герой повертається в минуле; щойно зроблені дії стають минулим «я»»`, `spawn(echo)`.
- КОЛИ `tick` → ТО `custom: «кожен минулий «я» виконує свою записану дію цього моменту»`.
- КОЛИ `line_of_sight(echo, hero)` → ЯКЩО not `state(hero, invisible)` → ТО `custom: «парадокс»`, `restart` (?).
- КОЛИ `custom: «минулий «я» не може повторити записану дію (шлях перекрито)»` → ТО `custom: «парадокс»` (?).
- КОЛИ `enter(hero|echo|staff, button[c])` → ТО `set_state(channel_c, active)`, `set_state(door_c, open)`; КОЛИ `leave(...)` останнього → ТО `clear_state(door_c, open)`.
- КОЛИ `input(action)` → ЯКЩО `occupied(cell, staff)` → ТО `pickup(hero, staff)`; повторно — `place(hero, staff)` (?).
- КОЛИ `picked(hero, mushroom_blue)` → ТО `set_state(hero, invisible)`.
- КОЛИ `picked(hero, mushroom_red)` → ТО `set_state(hero, can_push)`.
- КОЛИ `picked(hero, mushroom_green)` → ТО `set_state(hero, time_shifted)` (?).
- КОЛИ `contact(hero, object)` → ЯКЩО `state(hero, can_push)` and `free(cell_behind)` → ТО `push(object)`.
- КОЛИ `enter(hero, cleansing_pool)` → ТО `clear_state(hero, all)`.
- КОЛИ `enter(hero, exit)` → ТО `win`, `next_level`.
- Перемога: герой на виході · Поразка: вибух або парадокс → рестарт пазла · Рахунку нема.

## Керування і ввід
- Клавіатура (повністю «Keyboard Only») або геймпад (Xbox, DualShock, DualSense).
- `R` / `Y` на геймпаді — рестарт пазла (додано в патчі 2).
- Undo — не підтверджено (?).

## Вікна, меню, HUD
- `game-screen` — ізометричний лабіринт з туманом, героєм, минулими «я», фронтами вибухів.
- `pause-menu` → «Community Levels» → «Play Workshop Levels» · «Play Local Files» · «Upload to Workshop» → «Upload New Level».
- `level-select` — повтор пройдених рівнів (відкривається після 100 % регіону; нове розвʼязання не зберігається).
- `settings-window` — гучність окремих каналів, мова (11) (?).
- `editor-window` — окремий **веб**-редактор: палітра сутностей, інспектор, метадані (назва, опис, палітра), «Test Level» вивантажує JSON.
- `achievements-window` (Steam Achievements).

## Фічі поза полем
- `restart-level`; `replay` пройдених рівнів після 100 % регіону.
- `level-editor` (відкритий, у браузері) + `level-sharing` через Steam Workshop + `user-levels-browser`; рівень — JSON за опублікованою схемою (≤ 1 МБ, ≤ 4000 сутностей), можна писати власні редактори.
- `achievements`, `cloud-save`, `localization` (11 мов), `gamepad-support`, `volume-sliders`.

## Варіації й родичі
- **Chronigma** (C3BGames, 2025, безкоштовна) — сестра-механіка: Sokoban, з 6-го рівня — запис власних дій, стрибок назад і співпраця з минулим собою; 60+ рівнів, підказки в грі, пропуск рівня, «відкрити все», режим мінімального сюжету.
- Chrono Break (джем-гра) — real-time-клон Loophole з тим самим правилом «минулий я не має тебе бачити».
- Родичі за часовими копіями: Braid (рівень з тінню-копією), The Misadventures of P.B. Winterbottom, Cursor*10; за тінями-повторювачами в корпусі — [Void Stranger](void-stranger.md) (`mimic-copy`).
- **Осі варіацій** часових копій: скільки копій — одна / кілька петель; що повторюють — рухи / усі дії; парадокс — погляд / неможливість повторити / нема; що «відкочується» — лише герой / увесь світ (вибухи).

## Цікавинки для курсу
- Запис ходів і відтворення копією синхронно з новими ходами — 🥉 (список дій + індекс часу).
- Парадокс «копія побачила тебе»: лінія погляду з урахуванням стін, штор і скла — 🥈 (два різні шари блокування: рух і погляд).
- Стіни на ребрах клітин замість клітин-стін — 📎 (модель поля «клітини + ребра»).
- Фронт вибухів як чиста функція часу (`startTime`, `period`) — 🌱; разом із відкатом часу — 📎.
- Кнопки/двері/дроти через канали — 📎 (один словник `channel → active`).
- Рівень як JSON за опублікованою схемою + валідатор — 🥉 (той самий формат, що в реальному редакторі).

## Мапа на каталог
- Є: `move-4dir`, `move-by-input`, `keyboard-controls` · `push-object` ↔ з червоним грибом · `impassable-cells` ↔ стіни/скло · `one-way-cell` ↔ одностороннє ребро · `button-toggle` ↔ канали кнопка → двері · `item-pickup` ↔ гриби, посох · `status-effects` ↔ статуси грибів і купіль · `fog-of-war` ↔ туман і погляд · `reach-exit` · `restart-level` · `sequential-levels`, `level-select` ↔ регіони й повтор рівнів · `level-exchange`, `state-as-data` ↔ JSON-рівні у Workshop · `achievements-window`, `save-progress`.
- **Нема** → пропозиції карток:
  - `+time-clone-replay` «Минулий я повторює записані дії» · entities/spawn · 🥈 · слоти {max_clones, what: moves|actions}.
  - `+paradox-sighting` «Копія бачить оригінал — парадокс» · game-logic/lose · 🥉.
  - `+edge-walls` «Стіни на ребрах клітин» · entities/legality · 📎 · слоти {blocks: move|sight|both}.
  - `+advancing-hazard-front` «Фронт загрози, що просувається з часом» · entities/death · 🌱 · слоти {dir, period}.
  - `+zone-time-stop` (уже пропонована) ↔ клітина «соус».
  - `+vision-blockers` «Окремо: що блокує рух, що — погляд» · entities/legality · 📎.
  - `+replay-solved-levels` «Повтор пройдених рівнів після 100 %» · levels/progression · 🌱.
  - `+external-level-editor` «Редактор рівнів окремим веб-застосунком» · levels/editor · 🥈 — на відміну від `in-game-editor`.
  - `+level-json-schema` «Рівень як JSON за опублікованою схемою з валідацією» · levels/format · 🥉 — родич `level-from-txt` і `map-validation`.

## Пропозиції до словників
- `+trigger:sighted` — сутність потрапила в поле зору іншої (підтверджую; у `vocab/` ще нема).
- `+trigger:paradox` — порушено часову узгодженість (у Parabox — інший зміст; тут — копія бачить оригінал або не може повторити дію).
- `+effect:time_travel(a, t)` — повернути сутність у момент t, перетворивши її історію на копію.
- `+role:echo` — копія-повторювач минулих дій (не `ally`: не має волі, лише запис).
- `+card:time-clone-replay`, `+card:paradox-sighting`, `+card:edge-walls`, `+card:advancing-hazard-front`, `+card:vision-blockers`, `+card:external-level-editor`, `+card:level-json-schema` — див. вище.
- `+feature:workshop` — публікація й завантаження рівнів через Steam Workshop (окремо від `level-sharing` кодом).

## Джерела
- ⭐ [Steam](https://store.steampowered.com/app/3629400/Loophole/) — опис: машини часу, минулі «я», вибухи; категорії (Workshop, редактор, Cloud, Keyboard Only); новини: редактор і Workshop, патч 2 з кнопкою рестарту (R/Y) і повтором рівнів, патч 1 (туман війни).
- [Community Levels Guide](https://github.com/loophole-game/community-levels-guide/blob/main/README.md) + `levelSchema.ts` — повний перелік сутностей (машина часу, стіна, штора, одностороннє ребро, скло, посох, соус, гриби, купіль, кнопка, двері, дріт), вибухи з `startTime/startPosition/period`, правила накладання, ліміти.
- [Loophole Level Editor](https://github.com/loophole-game/loophole-level-editor) — описи пікапів (синій — невидимість, зелений — інше сприйняття часу, червоний — штовхати), купіль знімає статуси; [онлайн-версія](https://loophole-game.github.io/loophole-level-editor/).
- [Коментар до Chrono Break](https://itch.io/post/15431530) — розробник джем-клону підтверджує, що копіював Loophole; правило «минулий я не має тебе бачити».
- [Steam: Chronigma](https://store.steampowered.com/app/4051150/Chronigma/) — сестра-механіка, C3BGames.
- YouTube: [пошук «Loophole time travel puzzle gameplay»](https://www.youtube.com/results?search_query=Loophole+time+travel+puzzle+gameplay).

## Непевне
- Рецензій і вікі не знайдено; правила часу — з опису Steam, схеми рівня й коментарів, не з власної гри.
- (?) Куди саме повертає машина часу (на старт рівня? на N ходів?) і чи можна мати кілька минулих «я» одночасно.
- (?) Парадокс: погляд копії на героя — з клону Chrono Break; синій гриб (невидимість) і шари «рух/погляд» узгоджуються з цим, але офіційного опису нема. Чи парадокс — і коли копія не може повторити дію.
- (?) Що робить зелений гриб («perceive time differently») і «соус» для копій.
- (?) Вибух — поразка чи відкат; undo — не підтверджено; підбір/скидання посоха — окрема дія чи автоматично.
