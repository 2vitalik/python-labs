---
title: Sokobond
slug: sokobond
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2013
platforms: [PC, Mac, Linux, iOS, Android, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Sokobond", best: true, note: "атоми й валентності, злипання в молекулу, обʼєкти що рвуть/посилюють/переставляють звʼязки"}
  - {kind: official, url: "https://www.sokobond.com/", note: "сайт гри, магазини"}
  - {kind: official, url: "https://www.sokobond.com/presskit", note: "історія (джем-гра з GDC 2012), автори, трейлери"}
  - {kind: steam, url: "https://store.steampowered.com/app/290260/"}
  - {kind: other, url: "https://draknek.itch.io/sokobond", note: "itch.io"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=pGisbr65cWk", note: "трейлер 2021 (з прескіту)"}
  - {kind: other, url: "https://killscreen.com/review-sokobond-fun-we-promise-game-about-chemistry", note: "рецензія: bond splitters, подвійні звʼязки, інертні гази, факти після рівня"}
  - {kind: other, url: "https://sokobond.express/", note: "Sokobond Express (2024) — продовження-мешап із Cosmic Express"}
stage: v1
coverage: 70
mechanics: [move-4dir, push-object, stick-together, multi-cell-size, impassable-cells, satisfy-constraints, completion-detection, sequential-levels, level-select, level-unlock, keyboard-controls, swipe-gestures, movement-animation, save-progress, +valence-bonds, +bond-cutter, +bond-upgrade, +pivot-rotate, +undo-redo, +level-fact-card]
proposes: ["+trigger:input", "+trigger:adjacent", "+trigger:cross", "+cond:free", "+cond:free_electrons", "+effect:attach", "+effect:detach", "+effect:bond_order", "+effect:rotate", "+effect:move", "+role:atom", "+window:puzzle-select", "+window:fact-card", "+card:edge-objects", "+axis:actors"]
author: opus
date: 2026-11-02
---

# Sokobond — штовхай атоми, доки всі вільні електрони не стануть звʼязками

## Суть
Sokoban, де «ящики» — атоми з вільними електронами (валентністю). Гравець веде один атом; коли він опиняється поруч з іншим атомом і в обох є вільні електрони, вони **злипаються звʼязком**, і далі молекула рухається як одне тверде тіло. Мета — скласти молекулу, у якій не лишилось вільних електронів. Хімія тут — не тема-обгортка, а сама таблиця правил: валентність H=1, O=2, N=3, C=4, He=0 визначає, що з чим і скільки разів може злипнутися.

## Поле і час
- Невелика квадратна сітка зі стінами (кімната на один екран); кількість атомів — 2…~12.
- Покроково: тік = один крок молекули гравця; після кроку перевіряються нові сусідства й утворюються звʼязки.
- Спецобʼєкти лежать **на ребрах/вузлах сітки**, а не в клітинах: вони діють на звʼязок (відрізок між центрами двох атомів), коли той проходить крізь них.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Атом гравця | player | елемент, вільні електрони | рух 4 напрямки разом з усією своєю молекулою |
| Водень H | object | валентність 1 | штовхається; утворює 1 звʼязок |
| Кисень O | object | валентність 2 | 2 звʼязки |
| Азот N | object | валентність 3 | 3 звʼязки |
| Вуглець C | object | валентність 4 | 4 звʼязки (максимум по одному на кожного з 4 сусідів, або кратні) |
| Гелій He | object | валентність 0 | інертний: ніколи не злипається, лише штовхається як ящик |
| Молекула | object | форма (набір клітин), звʼязки | тверде тіло: рухається/штовхається цілком, якщо всі клітини попереду вільні |
| Звʼязок | — | кратність 1/2/3 | зʼєднує два сусідні атоми; кожна одиниця кратності витрачає по 1 електрону з обох |
| Стіна | static | — | непрохідна для всіх атомів |
| Розрізувач (splitter, червоний) | static | на ребрі сітки | звʼязок, що проходить крізь нього, рветься — молекула ділиться на дві |
| Підсилювач (bonder, зелений «+») | static | на ребрі сітки | звʼязок, що проходить крізь нього, отримує +1 кратність, якщо в обох атомах є вільні електрони |
| Півот (pivot, синій) | static | у вузлі сітки | молекула, зачепившись, «обгортається» навколо нього — частина повертається на 90° |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cells_ahead_of_molecule)` → ТО `move(molecule, dir)`; клітини попереду зайняті атомом → ТО `push(that_molecule)` рекурсивно, якщо за ним вільно; інакше `block`.
- КОЛИ `adjacent(atom_a, atom_b)` після кроку → ЯКЩО `free_electrons(a) > 0 and free_electrons(b) > 0` → ТО `attach(a, b)`, `counter(electrons(a), -1)`, `counter(electrons(b), -1)`; нова молекула = обʼєднання.
- Кілька нових сусідств за один крок → усі звʼязки утворюються одночасно (порядок, якщо електронів не вистачає на всі, — (?)).
- КОЛИ `cross(bond, splitter)` → ТО `detach(a, b)`, електрони повертаються обом; частина без атома гравця лишається на місці як окрема молекула (?).
- КОЛИ `cross(bond, bonder)` → ЯКЩО `free_electrons(a) > 0 and free_electrons(b) > 0` → ТО `bond_order(bond, +1)`.
- КОЛИ `contact(molecule, pivot)` → ТО `rotate(part, 90°)` навколо вузла (?).
- КОЛИ `count(free_electrons, ==, 0)` → ТО `win` (джерела: «кожен електрон задіяний у звʼязку»).
- Гелій: КОЛИ `adjacent(any, He)` → ТО нічого; лише `push`.
- Поразки нема; глухий кут (небажаний звʼязок, атом у куті) знімається undo/restart.

## Керування і ввід
- Стрілки/WASD або свайпи — крок молекули; штовхання = крок у атом.
- Undo (Z) — покроково; Restart (R) — рівень з початку (?).
- Мишею/тачем — вибір рівня на карті.

## Вікна, меню, HUD
- `main-menu` → `puzzle-select`: рівні як вузли, згруповані в тематичні секції; пройдені позначені, нові відкриваються після попередніх.
- `game-screen`: поле, атоми з точками-електронами навколо (кількість вільних видно прямо на спрайті — HUD не потрібен), назва рівня.
- `fact-card` (custom): після рівня — назва зібраної молекули й факт про її застосування в реальному світі.
- `settings-window`: звук, музика, мова (11 мов у Steam).
- Переходи: main-menu → puzzle-select → game-screen → (молекула завершена) fact-card → puzzle-select.

## Фічі поза полем
- `levels-sequential` у секціях + `level-unlock`; 105 рівнів (Wikipedia; рецензії дають інші числа).
- `undo` ∞ і `restart-level`; `save-progress` (Steam Cloud), `achievements` (Steam).
- `localization` 11 мов; `touch-controls` (iOS/Android), Switch.
- Нема редактора, підказок, рахунку ходів (?).

## Варіації й родичі
- Sokobond Express (2024, José Hernández × Draknek) — атом-локомотив і колія з Cosmic Express; поле не обмежене краями сітки.
- Родичі: Sokoban (штовхання), Atomix (збір молекули з атомів, але без злипання), Snakebird (тіло як група клітин), A Monster's Expedition (той самий автор, Alan Hazelden).
- Осі варіацій **злипання**: коли злипаються — при будь-якому дотику / лише при вільних «гачках» (валентність) / лише за кольором; що рухається — один атом / уся молекула / молекула тягне за собою; як розʼєднати — ніяк / об спецобʼєкт / undo.

## Цікавинки для курсу
- Валентність як лічильник на сутності + автоматичне злипання при сусідстві — 🥉.
- Молекула як тверде тіло з довільною формою: рух і штовхання ланцюгом молекул — 🥈 (рекурсивна перевірка всіх клітин).
- Обʼєкти на ребрах сітки, що діють на звʼязок при перетині (розрізувач, підсилювач) — 🥈 (нова геометрія: ребра, а не клітини).
- Півот, навколо якого частина молекули повертається — 🥇 (обертання підграфа з перевіркою колізій).
- Умова перемоги «нуль вільних електронів» — 🌱; картка-факт про молекулу — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `push-object` · `stick-together` (ядро гри, картка прямо згадує Sokobond) · `multi-cell-size` (молекула) · `impassable-cells` · `satisfy-constraints` + `completion-detection` · `sequential-levels` · `level-select` · `level-unlock` · `keyboard-controls` · `swipe-gestures` · `movement-animation` · `save-progress`.
- **Нема** → пропозиції карток:
  - `+valence-bonds` «Валентність: ліміт звʼязків на сутності» · entities/interact · 🥉 · слот {valences} (дитина `stick-together`).
  - `+bond-cutter` «Розрізувач звʼязків» · entities/interact · 🥈 — обʼєкт на ребрі сітки.
  - `+bond-upgrade` «Підсилювач кратності звʼязку» · entities/interact · 🥉.
  - `+pivot-rotate` «Обертання навколо півота» · entities/move · 🥇.
  - `+undo-redo` «Undo/redo ходів» · game-logic · 🥉 (є з Sokoban).
  - `+level-fact-card` «Картка-факт після рівня» · interface/menus · 🌱.

## Пропозиції до словників
- `+trigger:adjacent` (⏳ вже є, тут — головний тригер злипання); `+trigger:cross` — звʼязок/відрізок перетнув обʼєкт на ребрі сітки.
- `+cond:free_electrons` — у атома лишились вільні «гачки» (узагальнення: лічильник валентності).
- `+effect:bond_order` — змінити кратність звʼязку; ⏳ `attach`/`detach`/`rotate` вжиті як є.
- `+role:atom` — сутність з валентністю, що злипається (або вважати `object` з параметром).
- `+window:fact-card` — картка-факт після рівня; ⏳ `puzzle-select` вжито.
- `+card:edge-objects` — сутності на ребрах/вузлах сітки, а не в клітинах (Sokobond, тонкі стіни Chip's Challenge).
- `+axis:actors` — тут «одна сутність, що росте в групу» (single → party як тіло).

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/Sokobond) — атоми C/N/O/H/He з 4/3/2/1/0 звʼязками, злипання в молекулу, 105 рівнів, пізні обʼєкти (рвуть/посилюють/переставляють звʼязки).
- [Прескіт](https://www.sokobond.com/presskit) — історія з GDC-джему, автори (Alan Hazelden, Lee Shang Lun), [трейлер 2021](https://www.youtube.com/watch?v=pGisbr65cWk).
- [Kill Screen review](https://killscreen.com/review-sokobond-fun-we-promise-game-about-chemistry) — bond splitters, подвійні звʼязки, інертні гази, факти після рівнів.
- [Steam](https://store.steampowered.com/app/290260/) · [itch.io](https://draknek.itch.io/sokobond) · [сайт](https://www.sokobond.com/) · [Sokobond Express](https://sokobond.express/).

## Непевне
- (?) Умова перемоги: «усі електрони рівня звʼязані» (так у результатах пошуку) vs «у молекулі гравця нема вільних електронів» — перевірити, чи можуть лишатися зайві атоми.
- (?) Точна поведінка півота (кут, що саме повертається) — є лише опис рецензента «ланцюг обгортається навколо синіх точок».
- (?) Що стається з відрізаною частиною молекули після розрізувача (лишається на місці?).
- (?) Порядок утворення звʼязків, коли нових сусідств більше, ніж вільних електронів.
- (?) Розміщення спецобʼєктів (ребро vs вузол сітки) — з памʼяті.
- (?) Клавіші undo/restart.
