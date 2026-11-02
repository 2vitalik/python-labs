---
title: Cell Machine
slug: cell-machine
family: build-sim
also: [thinky, program-robots]
klass: puzzle
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: none
  goal: state
year: 2020
platforms: [web, PC]
links:
  - {kind: official, url: "https://samhogan.itch.io/cell-machine", best: true, note: "оригінал Sam Hogan (GMTK Game Jam 2020), грати в браузері, список клітин"}
  - {kind: play, url: "https://traloc-dheckoa.itch.io/cmmm", note: "Cell Machine Mystic Mod Plus — фанатський ремейк із пісочницею й кодами рівнів"}
  - {kind: other, url: "https://traloc-dheckoa.itch.io/cmmm/devlog/342984/big-update", note: "девлог моду: десятки нових клітин, формати кодів V1/V3/MP1"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=cell+machine+sam+hogan+gameplay", note: "пошук; геймплей і розбір механік"}
stage: v1
coverage: 75
mechanics: [push-object, destroy-all-enemies, cell-click, drag-drop-piece, level-select, game-loop, state-as-data, level-from-txt, in-game-editor, editor-palette, editor-playtest, +step-run-speed, +push-chain, +generator-clone, +rotate-neighbours, +axis-pushable, +build-zone, +update-order, +level-code-string, +entity-rotate]
proposes: ["+trigger:tick", "+trigger:phase_start", "+cond:free", "+cond:facing", "+effect:move", "+effect:rotate", "+effect:clone", "+effect:place", "+role:spawner", "+role:hazard", "+ui:step-button", "+ui:tool-palette", "+feature:step-mode", "+feature:mode-sandbox", "+feature:share-code", "+window:code-editor", "+axis:control", "+card:push-chain"]
author: opus
date: 2026-11-02
---

# Cell Machine — розстав клітини в зоні збірки, натисни Play: автомат сам штовхає, копіює й крутить, доки не знищить ворогів

## Суть
Пазл-автомат: на полі вже стоять клітини з власною поведінкою (рушій, генератор, ротатор, блоки), гравець може лише **переставити** ті, що лежать у підсвіченій зоні збірки, а потім натискає Play — і далі не керує нічим. Кожне покоління всі клітини діють за своїми правилами; мета — щоб якась клітина влетіла у ворога. Тема джему «Out of Control» буквально: гравець програмує початковий стан, решту робить клітинний автомат із напрямленими клітинами. Від Game of Life відрізняється тим, що правило не «рахує сусідів», а **рухає й копіює**: це автомат-конструктор.

## Поле і час
- Невелика прямокутна сітка рівня (оригінал — ручні рівні, у моді — довільний розмір, напр. 100×100 у пісочниці); один шар: клітина або порожньо. Край поля поводиться як нерухома стіна (?).
- **Зона збірки** (build zone) — підсвічена область; лише клітини в ній можна брати й ставити, і лише в її межах.
- Два режими часу: **редагування** (статика) → **симуляція** покоління за поколінням (`time: programmed`). Кнопки Play / Step / Reset; після Reset поле повертається до розстановки гравця.
- Покоління обробляється **фазами за типом** (спершу генератори, потім ротатори, потім рушії), а всередині фази — у фіксованому порядку напрямків (?) — від порядку залежить результат зіткнень.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Рушій (Mover) | object | напрям | щопокоління крок у свій напрям, штовхаючи ланцюг клітин попереду; ланцюг уперся — стоїть |
| Генератор (Generator) | spawner | напрям | копіює клітину **позаду** себе в клітину **попереду**, зсуваючи ланцюг попереду; позаду порожньо — нічого |
| Ротатор за год. стрілкою | object | CW | щопокоління повертає 4 ортогональних сусідів на 90° (змінює їхній напрям) |
| Ротатор проти год. стрілки | object | CCW | те саме, −90° |
| Push-клітина | object | — | пасивна; зсувається, коли штовхають з будь-якого боку |
| Slide-клітина | object | вісь H або V | штовхається лише вздовж своєї осі; поперек — як стіна |
| Нерухома (Immobile) | static | — | не штовхається, зупиняє ланцюг; генератор може її **скопіювати** |
| Ворог (Enemy) | enemy | — | клітина, що в нього входить, знищується разом із ним |
| Смітник (Trash) | hazard | — | поглинає все, що в нього заштовхнули, сам лишається (?) |
| Зона збірки | zone | прямокутник/маска | де гравцеві дозволено брати й ставити клітини |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(play)` → ТО `custom: «зафіксувати розстановку, запустити покоління»`; `input(step)` → одне покоління; `input(reset)` → повернути стан до Play.
- КОЛИ `input(drag, cell)` → ЯКЩО `cell(from, build_zone)` і `cell(to, build_zone)` і `free(to)` → ТО `move(cell, to)`; інакше `block`.
- КОЛИ `phase_start(generators)` → ДЛЯ кожного генератора: ЯКЩО `not free(behind)` → ТО `clone(behind)` у клітину `ahead`; ЯКЩО `ahead` зайнята → ТО `push` ланцюга у напрямку генератора; ланцюг упирається в нерухоме → `block` (копії нема).
- КОЛИ `phase_start(rotators)` → ТО `rotate(neighbour4, ±90)` для кожного сусіда, що має напрям; ненапрямлені (push, enemy) не змінюються.
- КОЛИ `phase_start(movers)` → ТО `move(mover, facing)`; ЯКЩО попереду ланцюг → `push` усього ланцюга на 1, доки за останнім `free`; інакше `block` — рушій стоїть.
- КОЛИ `push(chain)` → ЯКЩО в ланцюгу `slide` поперек осі або `immobile` → ТО `block` весь ланцюг.
- КОЛИ рушії штовхають один одного зустрічно → ТО `custom: «сили складаються: кожен рушій у бік руху +1, проти −1; рух, лише якщо сума > 0»` (?).
- КОЛИ `contact(any, enemy)` → ТО `disappear_both`; КОЛИ `contact(any, trash)` → ТО `disappear_a`.
- КОЛИ `all_gone(enemy)` → ТО `win`, `next_level`.
- Поразки нема: якщо автомат зациклився чи ворог уцілів — гравець натискає Reset і переставляє.
- Рахунку нема; єдина метрика — рівень пройдено/ні.

## Керування і ввід
- Миша: перетягнути клітину в межах зони збірки (`drag-drop-piece`); у моді — вибір клітини з палітри й клік для розміщення, поворот перед установкою клавішами (?).
- Кнопки Play / Step / Reset — керування часом автомата; під час симуляції редагування заблоковане.
- Мод: пісочниця (вільний редактор будь-якої клітини), імпорт/експорт рівня рядком-кодом (`V1;ширина;висота;...`).

## Вікна, меню, HUD
- `main-menu` → `level-select` (оригінал: рівні-кнопки, проходити можна в будь-якому порядку).
- `game-screen`: поле, підсвічена зона збірки, кнопки Play / Step / Reset (`step-button`, `restart-button`), кнопка назад до меню.
- Мод: `editor-window` пісочниці з `tool-palette` клітин; `custom-window` «Import/Export level code» — текстове поле для коду (+window:code-editor найближчий); `settings-window` (швидкість симуляції — `speed-slider`).
- Переходи: main-menu → level-select → game-screen (edit) → Play → game-screen (run) → (вороги знищені) → наступний рівень / level-select.

## Фічі поза полем
- `step-mode` і `speed-control` (мод) — ядро «дебагу» автомата.
- `puzzle-bank`: оригінал — кілька десятків ручних рівнів (?), незалежних.
- Мод (CMMM/CMMM+): `mode-sandbox`, `level-editor`, `share-code` (коди V1 → V3 → MP1), величезний словник нових клітин (телепорт, конвертер, nudge, puller, лічильник тощо) — приклад `custom-rules` через розширення таблиці клітин.

## Варіації й родичі
- Мод-сімʼя: Cell Machine Mystic Mod (ремейк із пісочницею й кодами) → CMMM+ та інші форки; кожен додає клітини, не змінюючи ядра «фаза × тип».
- Родичі: Game of Life (автомат, але за кількістю сусідів), Opus Magnum / SpaceChem (програма = розстановка, потім виконання), Baba Is You (правила як клітини), Wireworld, Factorio (рух предметів сусідством).
- **Осі варіацій**: що робить клітина (рух / копія / поворот / поглинання) · як визначається порядок оновлення (за типом / за напрямком / одночасно з конфліктами) · що може гравець (лише переставити / додати з палітри / повернути) · де дозволено ставити (зона збірки / все поле).

## Цікавинки для курсу
- Штовхання **ланцюга** клітин до упору з перевіркою «чи весь ланцюг може зсунутись» — 📎 (цикл уздовж напрямку).
- Генератор: копія «позаду» → «попереду» зі зсувом ланцюга і збереженням орієнтації копії — 🥉 (поєднує clone + push + напрям).
- Фазове оновлення за типами з фіксованим порядком напрямків: детермінований автомат з конфліктами — 🥈 (порядок змінює результат; треба буферизувати «вже рухався»).
- Slide-клітина: прохідність залежить від осі руху — 🌱.
- Зона збірки як маска редагування + Reset до розстановки — 📎 (`state-as-data` двічі: «план» і «прогін»).
- Код рівня рядком (ширина;висота;клітини) — 📎, експорт/імпорт.
- Сили рушіїв (сума за напрямком) — 🥉 (?), якщо реалізувати як у моді.

## Мапа на каталог
- Є: `push-object` (базове штовхання) · `destroy-all-enemies` · `cell-click` / `drag-drop-piece` (розстановка) · `level-select` · `game-loop` · `state-as-data` (Reset) · `level-from-txt` (коди моду) · `in-game-editor` + `editor-palette` + `editor-playtest` (пісочниця моду).
- **Нема** → пропозиції карток:
  - `+push-chain` «Штовхання ланцюга до упору» · entities/legality · 📎 · слот {max_len} — дитина `push-object`.
  - `+generator-clone` «Генератор: копія позаду → вперед» · entities/spawn · 🥉.
  - `+rotate-neighbours` «Ротатор крутить сусідів» · entities/interact · 📎 · слоти {deg, neighbourhood}.
  - `+axis-pushable` «Обʼєкт штовхається лише вздовж осі» · entities/legality · 🌱.
  - `+build-zone` «Зона, де дозволено ставити» · levels/editor · 🌱 · слот {mask} (також Opus Magnum, Into the Breach-деплой, CoC).
  - `+update-order` «Порядок оновлення сутностей у тіку» · code/architecture · 🥈 · слоти {by_type, by_dir}.
  - `+level-code-string` «Рівень одним рядком-кодом» · levels/format · 📎 (близько до `level-from-txt`, але для обміну в чаті).
  - `+step-run-speed` (з Game of Life) · `+entity-rotate` (з Factorio) — повторно вжиті.

## Пропозиції до словників
- `+trigger:tick`, `+trigger:phase_start` (фаза генераторів/ротаторів/рушіїв у межах покоління).
- `+cond:free` (кінець ланцюга вільний), `+cond:facing` (напрям рушія/генератора).
- `+effect:move`, `+effect:rotate` (повернути сусіда), `+effect:clone` (копія сутності в іншу клітину — тут головне дієслово), `+effect:place` (розстановка гравцем).
- `+role:spawner` (генератор), `+role:hazard` (смітник).
- `+ui:step-button`, `+ui:tool-palette` (пісочниця).
- `+feature:step-mode`, `+feature:mode-sandbox`, `+feature:share-code` (код рівня).
- `+window:code-editor` — тут не програма, а поле коду рівня; можливо, окремий `+window:level-code` (поки `custom-window`).
- `+axis:control` = `programmed` (розстановка → прогін без втручання).
- `+card:push-chain` — див. вище.

## Джерела
- ⭐ [Cell Machine на itch.io](https://samhogan.itch.io/cell-machine) — оригінал у браузері, офіційний опис 7 типів клітин, Play/Step/Restart, коментарі гравців.
- [Cell Machine Mystic Mod Plus](https://traloc-dheckoa.itch.io/cmmm) — фанатський ремейк із пісочницею.
- [Девлог CMMM+ «Big Update»](https://traloc-dheckoa.itch.io/cmmm/devlog/342984/big-update) — нові клітини, формати кодів V1/V3/MP1.
- YouTube: пошук «cell machine sam hogan gameplay».

## Непевне
- (?) Рік: оригінал зроблено на GMTK Game Jam 2020 (не 2021, як у черзі); точну дату релізу сторінка не дає.
- (?) Смітник (Trash) і ротатор CCW — є в моді, у первісному списку itch-сторінки не названі; чи були в оригіналі, не перевірено.
- (?) Порядок фаз (генератори → ротатори → рушії) і порядок напрямків у фазі — з памʼяті про мод, не з документації.
- (?) «Сили» рушіїв (сума зустрічних) — механіка моду, за оригінал не ручаюсь.
- (?) Чи можна в оригіналі повертати клітини перед Play, і що робить край поля (стіна чи знищення) — не перевірено (WebSearch вичерпано, фан-вікі 402).
