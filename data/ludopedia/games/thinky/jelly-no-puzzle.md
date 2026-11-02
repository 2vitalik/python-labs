---
title: Jelly no Puzzle (ゼリーのパズル)
slug: jelly-no-puzzle
family: thinky
also: [push-slide, falling-match]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2013
platforms: [PC (Windows), Android]
links:
  - {kind: other, url: "https://arxiv.org/html/2501.12282v2", best: true, note: "Crabtree & Mitsou 2025: розділ 1 — правила Jelly-No коротко (рух на 1, гравітація, злиття того самого кольору, чорні желе, желе на стінах), картинки рівнів"}
  - {kind: official, url: "https://qrostar.net/jelly/", note: "офіційна сторінка (EN): безкоштовна збірка для Windows, jelly1000.zip"}
  - {kind: official, url: "https://qrostar.jp/jelly/", note: "японська сторінка автора (Tatsunami/Qrostar): 250 000+ завантажень"}
  - {kind: other, url: "https://play.google.com/store/apps/details?id=com.jellycrew.jellynopuzzle", note: "Android-версія від JellyCrew"}
  - {kind: other, url: "https://arxiv.org/html/2601.08057v2", note: "«Carrying is Hard»: порівняння Jelly і Hanano, чому в Jelly нема «перенесення» і каскадів"}
  - {kind: youtube, url: "https://www.youtube.com/channel/UCknBUJvp8CESgEp2pG5s-Dw", note: "YouTube-канал Qrostar"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Jelly+no+Puzzle+gameplay", note: "пошук; проходження рівнів"}
stage: v1
coverage: 75
mechanics: [cell-click, gravity-fall, push-object, stick-together, tile-merge, multi-cell-size, impassable-cells, completion-detection, sequential-levels, level-select, save-progress, movement-animation, level-solver, +undo-redo, +merge-into-body, +anchored-piece, +connectivity-goal, +settle-then-merge]
proposes: ["+trigger:input", "+trigger:after", "+cond:same", "+cond:free", "+cond:supported", "+effect:move", "+effect:fall", "+effect:merge", "+effect:attach", "+role:tile", "+feature:undo", "+card:connectivity-goal", "+axis:undo"]
author: opus
date: 2026-11-02
---

# Jelly no Puzzle — зсувай желе ліворуч/праворуч, гравітація їх кидає, однакові кольори злипаються назавжди; зліпи кожен колір в одне тіло

## Суть
Поле збоку (вид-профіль) зі стінами й кольоровими желе різних форм. Гравець клацає по желе і зсуває його на одну клітину ліворуч або праворуч; після ходу все без опори падає. Коли два желе одного кольору торкаються боком, вони **зливаються назавжди** в одне тіло (можливо неопукле), яке далі рухається й падає як ціле. Мета — щоб кожен колір став одним желе. Ядро — незворотне злиття: кожне злипання робить тіло більшим і незграбнішим, тож порядок зʼєднань важливіший за самі ходи.

## Поле і час
- Квадратна сітка «збоку» (гравітація вниз), невеликі рівні (типово ~10–14 × 6–10 (?)). Стіни/платформи — нерухоме тло.
- Хід = один зсув одного тіла на 1 клітину по горизонталі → далі детерміновано: падіння всього без опори → злиття дотичних однакових → знову падіння, доки стан не стабілізується.
- Ні часу, ні випадковості, ні ворогів; повна інформація. Складність — PSPACE-повна (Crabtree & Mitsou 2025), одноколірні рівні — NP-повні (Yang 2018).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кольорове желе | tile | колір; форма (1×1 або багатоклітинна) | зсувається на 1 ліворуч/праворуч кліком; падає без опори; зливається з дотичним того ж кольору |
| Злите тіло | tile | множина клітин одного кольору | рухається й падає як ціле; роз'єднатися не може |
| Чорне желе | object | довільна (неопукла) форма | рухається й падає як звичайне; **не зливається** й не потребує злиття — вантаж, опора, клин |
| Желе, прикріплене до стіни | tile | колір; позначка кріплення (?) | не рухається й не падає; зливаючись із ним, рухоме тіло теж стає нерухомим (?) |
| Стіна / платформа | static | — | непрохідна, опора для падіння |
| Порожнеча | — | — | желе падає крізь неї до опори |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, jelly, dir∈{left,right})` → ЯКЩО `free(cells_beside)` для всього тіла (з урахуванням штовхання) → ТО `move(jelly, dir)`; інакше `block`.
- КОЛИ `contact(jelly, other_jelly)` при зсуві → ЯКЩО `free(cell_behind)` для всього ланцюга → ТО `push` (сусідні тіла зсуваються разом) (?); якщо хоч одне впирається в стіну — `block`.
- КОЛИ `after(move)` → ЯКЩО `not supported(body)` → ТО `fall(body)` до опори (тіла падають цілком, не поклітинно).
- КОЛИ `adjacent(a, b)` (спільне ребро, не кут) → ЯКЩО `same(a, b, color)` і колір ≠ чорний → ТО `merge(a, b → body)` / `attach(a, b)` назавжди.
- КОЛИ `after(merge)` → ТО повторити `fall` (нове тіло може втратити або знайти опору) → повторити перевірку злиття — каскад до стабільного стану.
- КОЛИ тіло, що стоїть на іншому, зсувають знизу → ТО верхнє **не їде** разом (нема «перенесення»), а падає, якщо втратило опору (Crabtree & Mitsou: «Jelly does not have a carrying feature»).
- КОЛИ `merge(a, anchored)` → ТО `set_state(body, anchored)` (?).
- КОЛИ `pattern(each_color_single_body)` → ТО `win` — `custom: «кожен колір утворює одну звʼязну компоненту»`.
- Поразки нема: глухий кут (розʼєднані однакові кольори, які вже не зійдуться) лікується undo/restart. Рахунку нема.

## Керування і ввід
- Миша: клік по желе — зсув на 1 клітину; напрямок задається кнопкою миші або стороною кліку (?) — точну схему не перевірено.
- Undo останнього ходу й рестарт рівня — клавішами/кнопками (?).
- Android: дотик/свайп по желе (?).

## Вікна, меню, HUD
- `level-select` — сітка рівнів з позначками пройдених (?).
- `game-screen` — поле збоку; номер рівня; кнопки `undo-button`, `restart-button` (?); `movement-animation` падіння/злиття.
- `end-screen` — коротке «Clear» і перехід далі (?).
- Переходи: level-select → game-screen → (усі кольори зʼєднані) → наступний рівень / level-select.

## Фічі поза полем
- `undo` (кроків ∞ (?)) + `restart-level`; `levels-sequential` (~40 рівнів (?)) з `level-select`; `autosave` прогресу (?).
- Безкоштовна гра для Windows (zip без інсталятора), мови EN/JA; Android-порт JellyCrew.
- Нема редактора, підказок, рахунку.

## Варіації й родичі
- Hanano Puzzle / Hanano Puzzle 2 (той самий автор): та сама фізика «збоку + гравітація + зсув», але замість злиття — розквіт квітів, і блоки лишаються окремими ([hanano-puzzle.md](hanano-puzzle.md)).
- Yugo Puzzle (ユウゴウパズル, Qrostar) — варіант Jelly, PSPACE-повний при необмеженій кількості кольорів (Kano, Yamanaka, Hirayama).
- Sokobond — злипання при контакті, але на площині без гравітації і за валентністю; 2048/Threes — злиття однакових, але з новим значенням, а не форма.
- **Осі варіацій:** коли зливаються — одразу при дотику / за дією гравця; що зливається — колір / значення / валентність; тіла — розʼєднувані / назавжди; чи несе нижнє тіло верхнє — ні (Jelly) / так; є нейтральні нерухомі обʼєкти (чорні желе) — так/ні.

## Цікавинки для курсу
- Злиття в одне тіло як union-find по клітинах: желе = множина клітин, рух/падіння тіла цілком — 🥉 (структура даних + перевірка колізії всього тіла).
- Каскад «падіння → злиття → падіння» до фіксованої точки — 🥉 (цикл до стабільності, порядок обробки).
- Умова перемоги «кожен колір звʼязний» — 📎 (flood fill по кольорах).
- Штовхання ланцюга тіл довільної форми з гравітацією — 🥈 (рекурсивна перевірка «чи всі можуть зсунутись»).
- Розвʼязувач BFS по станах + канонічний хеш стану — 🥇 (гра PSPACE-повна, але малі рівні вирішуються перебором).
- Желе на стінах «заражає» нерухомістю — 🌱 як прапорець на тілі.

## Мапа на каталог
- Є: `cell-click` ↔ клік по желе; `gravity-fall` ↔ падіння; `push-object` ↔ штовхання сусідніх тіл (?); `stick-together` ↔ злипання при контакті й спільний рух; `tile-merge` ↔ злиття однакових; `multi-cell-size` ↔ желе-форми; `impassable-cells` ↔ стіни; `completion-detection` ↔ перевірка «колір звʼязний»; `sequential-levels` + `level-select` + `save-progress`; `movement-animation`; `level-solver` ↔ BFS-розвʼязувач як завдання.
- **Нема** → пропозиції карток:
  - `+undo-redo` «Undo ходів у грі» · game-logic/flow · 📎 (вже пропоновано з Parabox/Snakebird).
  - `+merge-into-body` «Злиття в одне багатоклітинне тіло назавжди» · entities/state · 🥉 · слот {by: color|value} — дитина `stick-together`.
  - `+anchored-piece` «Закріплений шматок, що передає нерухомість при злитті» · entities/legality · 🌱.
  - `+connectivity-goal` «Перемога: кожна група однакових звʼязна» · game-logic/win · 📎 — також Flow-подібні.
  - `+settle-then-merge` «Каскад падіння і злиття до стабільного стану» · entities/move · 🥉 — родич `after`-каскадів match-3.

## Пропозиції до словників
- `+trigger:input`; `+trigger:after` — після ефекту (каскад падіння ↔ злиття).
- `+cond:same(a, b, color)`; `+cond:free`; `+cond:supported(body)` — під хоча б однією клітиною тіла є опора.
- `+effect:move`, `+effect:fall` (тіло цілком), `+effect:merge(a, b → c)` — тут злиття форм, не значень; `+effect:attach`.
- `+role:tile` — желе як плитка з кольором і формою.
- `+feature:undo`; `+axis:undo` — `unlimited` (?).
- `+card:connectivity-goal` — умова перемоги «звʼязність кожного кольору» не лягає ні в `all-on-targets`, ні в `satisfy-constraints`.

## Джерела
- ⭐ [Crabtree & Mitsou, arXiv 2501.12282](https://arxiv.org/html/2501.12282v2) — стислі правила Jelly-No (рух на 1, гравітація, злиття, чорні желе неопуклої форми, желе на стінах), історія складності.
- [Qrostar: Jelly no Puzzle (EN)](https://qrostar.net/jelly/) · [JP-сторінка](https://qrostar.jp/jelly/) — завантаження Windows, Android-посилання, 250 000+ завантажень.
- [Google Play: JellyCrew](https://play.google.com/store/apps/details?id=com.jellycrew.jellynopuzzle) — мобільна версія.
- [«Carrying is Hard», arXiv 2601.08057](https://arxiv.org/html/2601.08057v2) — у Jelly нема перенесення; злиття вбиває каскади, що є в Hanano; рік гри 2013.
- [YouTube-канал Qrostar](https://www.youtube.com/channel/UCknBUJvp8CESgEp2pG5s-Dw) · [пошук «Jelly no Puzzle gameplay»](https://www.youtube.com/results?search_query=Jelly+no+Puzzle+gameplay).

## Непевне
- (?) Чи може зсунуте желе штовхати сусідні тіла ланцюгом — з памʼяті про гру; статті правило штовхання для Jelly не описують.
- (?) Як саме задається напрямок (ліва/права кнопка миші, сторона кліку чи drag) і клавіші undo/restart.
- (?) Кількість рівнів (~40) і наявність екрана вибору рівнів у Windows-версії.
- (?) Поведінка желе, прикріпленого до стіни, при злитті (чи стає все тіло нерухомим) — логічно з «cannot move», але не перевірено.
- (?) Чи бувають різноколірні желе, зчеплені між собою від початку (у пізніх рівнях) — памʼять розмита.
- (?) Розмір поля рівнів.
