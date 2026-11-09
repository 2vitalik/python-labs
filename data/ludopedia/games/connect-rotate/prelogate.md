---
title: Prelogate
slug: prelogate
aka: []
family: connect-rotate
also: [program-robots]
klass: cursor
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2014
platforms: [PC (Windows), Linux]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/332830/Prelogate/", best: true, note: "опис і трейлер: лазери, змішування, логічні вентилі; 64 рівні в 10 розділах"}
  - {kind: other, url: "https://www.gamingonlinux.com/2014/12/laser-beam-puzzle-game-prelogate-released-on-steam-demo-is-available/page=1/", note: "огляд: дзеркало, сплітер, міксер, приймачі кольору, багатокрокові рівні"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=367434974", note: "проходження: назви 10 розділів і 64 рівнів, текстові коди розвʼязків"}
  - {kind: other, url: "https://steamcommunity.com/stats/332830/achievements", note: "16 досягнень: кількість пристроїв, логічні тіки, довжина лазера, чисті розвʼязки"}
  - {kind: other, url: "https://steamcommunity.com/app/332830/discussions/0/490125103630946434/", note: "поради до багатокрокових рівнів: IF/XOR/AND, дифузор проти міксера"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Prelogate+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [beam-tracing, mirror-reflect, impassable-cells, cell-click, keyboard-controls, undo-redo, redo, restart-level, satisfy-constraints, completion-detection, sequential-levels, level-unlock, level-select, state-string, save-progress, leaderboard, in-game-editor, game-screen, main-menu, pause-menu, end-screen, achievements-window, +beam-splitter, +beam-color-mix, +beam-logic-gate, +multi-step-truth-table, +solution-metrics, +solution-slots, +oscillation-detect, +view-toggle]
proposes: ["+trigger:beam_hit", "+cond:beam_present", "+effect:emit_beam", "+effect:split_beam", "+ui:step-selector", "+ui:solution-stats", "+window:solution-slots", "+feature:solution-code", "+card:beam-logic-gate", "+card:multi-step-truth-table", "+card:oscillation-detect"]
author: opus
date: 2026-11-09
---

# Prelogate — розстав дзеркала, міксери й логічні вентилі, щоб кожен приймач на кожному кроці отримав свій колір

## Суть
Пазл про лазерні схеми: на полі стоять емітери кольорових променів і приймачі, що чекають певного кольору. Гравець ставить із набору пристрої — дзеркала, сплітери, міксери, дифузори, призми й логічні вентилі (OR, AND, XOR, IF). Головна ідея — **багатокрокові рівні**: емітери на різних кроках вмикаються по-різному, і одна схема має дати правильний результат на всіх кроках, тобто реалізувати таблицю істинності. Проміні тут і «дроти», і сигнали: вентиль ставлять на перетин двох променів, і один керує іншим.

## Поле і час
- Поле — прямокутна сітка з клітинами для пристроїв; промені йдуть ортогонально, довжину рахують в одиницях (досягнення «понад 270 одиниць»). Є стіни й тверді обʼєкти; з розділу VII — перешкоди, з VIII — «плаваючі платформи».
- 3D-сцена з режимом 2D: гравці пишуть, що грають «у 2D-режимі», бо так краще видно пристрої.
- Редагування без часу (`static`); всередині схема рахується **логічними тіками**: вентилі перераховують стан, доки схема не осяде. Схема, що не осідає (вентиль вмикається й вимикається без кінця), рівня не розвʼязує.
- Крок — це окремий набір увімкнених емітерів, тобто тест-кейс. Кроки можна гортати в будь-якому порядку; емітери «пульсують» відповідно до кроку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Емітер (лазер) | source | колір, напрям, розклад увімк/вимк по кроках | випускає промінь свого кольору на тих кроках, де увімкнений |
| Приймач | sink | потрібний колір на кожному кроці (або «нічого») | крок зараховано, коли кожен приймач отримує свій колір; промінь не того кольору чи не на тому кроці — провал |
| Промінь | projectile | колір, довжина | летить по прямій до пристрою, стіни або краю; за край — довжина «нескінченна» |
| Стіна / твердий обʼєкт | static | — | зупиняє промінь |
| Дзеркало (Mirror) | object | орієнтація | повертає промінь на 90° |
| Сплітер (Splitter) | object | орієнтація | повертає промінь на 90° і водночас пропускає його прямо — два промені |
| Міксер (Mixer) | object | орієнтація | приймає два промені з протилежних боків, видає змішаний колір перпендикулярно до обох |
| Дифузор (Diffuser) | object | — | змішує промені, що через нього йдуть; легко «забруднює» первинні кольори (?) |
| Призма (Prism) | object | — | є в наборі (картка, рівень IX.4 «Prisms»); поведінка не підтверджена (?) |
| IF-вентиль | switch | лінія проходу, керівний вхід збоку | пропускає промінь, лише коли його під прямим кутом перетинає активний керівний промінь; колір керівного неважливий |
| AND-вентиль | switch | два входи | дає вихід, коли входи з обох боків є й однакові (?) |
| OR / XOR-вентилі | switch | два входи | вихід за відповідною булевою функцією входів (?) точна геометрія входів |
| Плаваюча платформа (розд. VIII) | terrain | — | особливе місце для пристроїв (?) |
| Клітина поля | terrain | вільна / зайнята | сюди ставлять пристрої з набору; набір необмежений |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, device, cell)` → ЯКЩО `free(cell)` → ТО `place(player, device)`, `counter(devices, +1)`.
- КОЛИ `input(delete, device)` (клавіша Delete, також під курсором) → ТО `disappear(device)`, `counter(devices, -1)`.
- КОЛИ `phase_start(step_k)` → ЯКЩО `state(emitter, on_at_step_k)` → ТО `custom: «емітер випускає промінь свого кольору»`.
- КОЛИ `contact(beam, wall)` → ТО `block` (промінь закінчується, довжина скінченна).
- КОЛИ `edge(beam)` → ТО `custom: «довжина лазера стає нескінченною»` (важить для метрик і досягнень).
- КОЛИ `contact(beam, mirror)` → ТО `bounce(beam)` (поворот на 90°).
- КОЛИ `contact(beam, splitter)` → ТО `bounce(beam)`, `clone(beam)` (копія йде прямо).
- КОЛИ `contact(beam_a, mixer)` → ЯКЩО `custom: «з протилежного боку входить другий промінь»` → ТО `merge(beam_a, beam_b, beam_mix)`, `custom: «вихід перпендикулярно до обох входів»`.
- КОЛИ `contact(beam, diffuser)` → ТО `custom: «колір змішується з іншими променями дифузора»` (?).
- КОЛИ `contact(control_beam, if_gate)` під прямим кутом → ТО `set_state(if_gate, open)`; КОЛИ керівний промінь зник → ТО `clear_state(if_gate, open)`.
- КОЛИ `contact(beam, if_gate)` уздовж лінії проходу → ЯКЩО `state(if_gate, open)` → ТО `custom: «промінь проходить далі»`; інакше `block`.
- КОЛИ `tick` → ТО `custom: «AND/OR/XOR перераховують вихід за станом входів»`, `counter(logic_ticks, +1)`.
- КОЛИ `repetition` (стан вентилів повторюється, схема не осідає) → ТО `custom: «нескінченна логічна петля — розвʼязок не зараховано»` (досягнення Infinity).
- КОЛИ `settled` → ЯКЩО `same(beam_at_receiver, receiver, color)` для кожного приймача → ТО `custom: «крок k зараховано»`; інакше `custom: «крок k провалено»`.
- КОЛИ `all_constraints_met` (зараховано всі кроки) → ТО `win`, `window(end-screen)`, `unlock(next_level)` (лише в режимі PLAY).
- Перемога: усі кроки рівня дають правильні кольори на всіх приймачах однією схемою. · Поразки нема: схему правлять, доки не спрацює. · Рахунок: три метрики розвʼязку — кількість пристроїв, сумарна довжина лазера, логічні тіки; плюс «чистий» розвʼязок (?) — у таблицях Steam і досягненнях.

## Керування і ввід
- Миша: вибрати пристрій у наборі (toolbox) і поставити на клітину; пристрої мають гарячі клавіші, вони підписані в наборі (оновлення 1.3.1).
- Delete — прибрати пристрій (у т. ч. під курсором); undo/redo (з 1.3.0); перегляд кроків по одному.
- B (натиснути) або V (утримувати) — посилення для дальтоніків; перемикання 3D/2D.
- Рестарт рівня — через паузу (гравці просили винести його в основний інтерфейс).
- Пасхалка — Konami-код ↑↑↓↓←→←→BA.

## Вікна, меню, HUD
- `main-menu`: PLAY (сюжетний режим, рівні відкриваються по черзі) · LEVELS (вільний вибір, але нових не відкриває) · налаштування · вихід.
- `chapter-select` / `level-select`: 10 розділів — Tutorial, Managing colours, Complex Mixing, Redefining logic, Constructing gates, All together, Obstacles, Floating platforms, Minimalism, Conclusion.
- `game-screen`: поле; `tool-palette` пристроїв із гарячими клавішами; `step-selector` (гортати кроки); `solution-stats` (порядок «пристрої, довжина лазера, логічні тіки»); `onboarding-hints` — поради про вентилі.
- `end-screen`: рівень пройдено; кнопка Save зберігає розвʼязок у слот разом з позначкою «чистий», тіками й довжиною.
- `solution-slots` (custom-window): 5 додаткових слотів розвʼязків на рівень плюс останній.
- `leaderboard` — таблиці Steam за метриками; `achievements-window` — оверлей Steam.
- `pause-menu`: рестарт, вихід до меню.
- `editor-window` — прихований розробницький редактор рівнів, «не user-friendly»; гравці знаходили його, шукаючи пасхалку.
- Переходи: main-menu → PLAY → game-screen → end-screen → наступний рівень; LEVELS → level-select → game-screen.

## Фічі поза полем
- `levels-sequential` + `level-unlock` (лише PLAY) і вільний `level-select` (LEVELS).
- `undo`, `redo`, `restart-level`; `save-slots` розвʼязків (5 + останній); `cloud-save` (Steam Cloud).
- Розвʼязки як текстові коди (рядок на кшталт base64 у гайдах) — `share-code` (?), як саме їх вводять у гру.
- `leaderboard-online`, `achievements` (16), `stats` по метриках; `colorblind-palette` (гаряча клавіша); `view-toggle` 3D/2D.
- `level-editor` прихований, без обміну рівнями; Workshop нема.

## Варіації й родичі
- Родичі: Octopticom (промені як сигнали, вентилі-перемикачі, метрики розвʼязку), Chromatron (змішування кольорів), Deflektor і Laser Tank (класичне трасування), Aargon Deluxe (гравець порівнює з ним).
- Осі варіацій:
  - **як промінь керує променем**: ніяк (Deflektor) / вентиль на перетині (Prelogate) / перемикач-дзеркало (Octopticom);
  - **скільки входів перевіряє рівень**: один стан (Chromatron) / кілька кроків-тестів (Prelogate) / потік даних (Octopticom);
  - **як змішується колір**: міксер з двох боків / дифузор / фільтр;
  - **оцінка розвʼязку**: лише «пройдено» / метрики пристроїв, довжини, тіків з таблицями.

## Цікавинки для курсу
- Трасування променя по сітці з дзеркалами й сплітерами плюс захист від нескінченного циклу променя — 🥉 (BFS по станах «клітина × напрям»).
- Адитивне змішування кольорів як OR трьох бітів RGB — 🌱.
- Вентиль на перетині двох променів і ітерація до нерухомої точки, лічильник тіків і виявлення осциляції — 🥈 (симуляція схеми зі зворотними звʼязками).
- Багатокроковий рівень як прогін таблиці істинності: одна схема на всі кроки — 🥉.
- Три метрики розвʼязку (пристрої, довжина, «∞», якщо промінь вилітає за край, тіки) і таблиця рекордів — 📎.
- Розвʼязок як текстовий код для обміну — 📎 (картка `state-string`).

## Мапа на каталог
- Є: `beam-tracing` ↔ промені; `mirror-reflect` ↔ дзеркало; `impassable-cells` ↔ стіни; `cell-click` + `keyboard-controls` ↔ розстановка й гарячі клавіші; `undo-redo` + `redo` + `restart-level`; `satisfy-constraints` + `completion-detection` ↔ усі кроки; `sequential-levels` + `level-unlock` + `level-select` ↔ PLAY / LEVELS; `state-string` ↔ коди розвʼязків; `save-progress`; `leaderboard` ↔ таблиці Steam; `in-game-editor` ↔ прихований редактор; `game-screen`, `main-menu`, `pause-menu`, `end-screen`, `achievements-window`.
- **Нема** → пропозиції карток:
  - `+beam-splitter` «Сплітер: поворот + прохід» · entities/interact · 📎 (уже пропонувався в сімʼї).
  - `+beam-color-mix` «Змішування кольорів променів» · entities/interact · 🌱 (є в сімʼї).
  - `+beam-logic-gate` «Вентиль на перетині променів» · entities/interact · 🥈 · слот {op: if|and|or|xor}.
  - `+multi-step-truth-table` «Рівень із кількома кроками-тестами» · game-logic/win · 🥉 · слот {steps}.
  - `+solution-metrics` «Метрики розвʼязку» · interface/results · 📎 (є в Octopticom).
  - `+solution-slots` «Кілька збережених розвʼязків рівня» · game-logic/save · 🌱.
  - `+oscillation-detect` «Схема не осідає → не зараховано» · game-logic/constraints · 🥉.
  - `+view-toggle` «Перемикання 3D/2D без зміни логіки» · interface/render · 🌱.

## Пропозиції до словників
- `+trigger:beam_hit` — промінь влучив у пристрій чи приймач (тут записано через `contact(beam, …)`).
- `+cond:beam_present` — на вході вентиля є промінь (керування IF/AND/OR/XOR).
- `+effect:emit_beam` — емітер випускає промінь; `+effect:split_beam` — сплітер дає два промені (тут — `bounce` + `clone`).
- `+ui:step-selector` — перемикач кроків багатокрокового рівня; `+ui:solution-stats` — панель «пристрої / довжина / тіки».
- `+window:solution-slots` — слоти збережених розвʼязків рівня.
- `+feature:solution-code` — розвʼязок як текстовий код.
- `+card:beam-logic-gate`, `+card:multi-step-truth-table`, `+card:oscillation-detect`.

## Джерела
- ⭐ [Steam: Prelogate](https://store.steampowered.com/app/332830/Prelogate/) — опис: перенаправлення, змішування, логічні вентилі; 64 рівні, 10 розділів; рецензії Very Positive.
- [GamingOnLinux (2014)](https://www.gamingonlinux.com/2014/12/laser-beam-puzzle-game-prelogate-released-on-steam-demo-is-available/page=1/) — дзеркало 90°, сплітер, міксер з протилежних боків і виходом перпендикулярно, приймачі кольору, кроки з пульсацією емітерів.
- [Steam-гайд: проходження](https://steamcommunity.com/sharedfiles/filedetails/?id=367434974) — назви розділів і рівнів (OR gate, AND gate, XOR gate, IF gate, Prisms…), коди розвʼязків.
- [Досягнення Steam](https://steamcommunity.com/stats/332830/achievements) — Infinity (нескінченна логічна петля), «Optimization» (тіки), «Wastage» / «270 Degrees» (скінченна довжина лазера), «Cleanliness» (без міксера).
- [Steam-форум: поради до багатокрокових](https://steamcommunity.com/app/332830/discussions/0/490125103630946434/) — IF-вентиль на перетині під прямим кутом, колір керівного неважливий; дифузори проти міксерів. Інші гілки: набір карток (Mirror, Splitter, Diffuser, Mixer, Prism, OR/AND/XOR/IF), PLAY проти LEVELS, прихований редактор, рестарт у паузі.
- Новини Steam (оновлення 1.3.0–1.3.2): undo/redo, 5 слотів розвʼязків, Delete, поради про вентилі, режим для дальтоніків B/V.
- YouTube: пошук «Prelogate gameplay».

## Непевне
- (?) Поведінка призми й дифузора; точна логіка AND/OR/XOR — з якого боку входи й що виходить (на форумі: «AND вимагає, щоб обидва боки були однакові»).
- (?) Що таке «чистий» (clean) розвʼязок — імовірно, без зайвих променів, що не доходять до приймачів.
- (?) Роль «плаваючих платформ» (розділ VIII) і перешкод розділу VII.
- (?) Чи поле — справжня сітка клітин, чи вільне розміщення на решітці; одиниця довжини лазера.
- (?) Чи рахуються таблиці Steam за всіма трьома метриками окремо; як вводять текстові коди розвʼязків.
