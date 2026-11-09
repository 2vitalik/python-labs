---
title: Theta and Paralldox on Worldlines
slug: theta-and-paralldox-on-worldlines
aka: [Paralldox]
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
year: 2026
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3219580/", best: true, note: "опис: Тета повертає ліворуч біля стін, виделка розщеплює її на копії; 6 розділів, 240+ пазлів, підказки й Notebook"}
  - {kind: itch, url: "https://xexlax.itch.io/paralldox", note: "сторінка XXela: керуєш однією чи кількома героїнями, 250+ пазлів, мета-пазли"}
  - {kind: other, url: "https://steamcommunity.com/app/3219580/reviews/?browsefilter=toprated&l=english", note: "відгуки: спільний ввід для всіх копій, поворот проти годинникової, злиття копій, Gain Insight"}
  - {kind: other, url: "https://steamcommunity.com/app/3219580/reviews/?browsefilter=toprated&l=schinese", note: "китайські відгуки: конфлікт дій → розщеплення світу, суперпозиція, заплутаність, годинник у розділі 6"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Theta+and+Paralldox+on+Worldlines+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [move-4dir, keyboard-controls, push-object, impassable-cells, turn-when-blocked, key-and-door, button-toggle, undo-redo, world-map, level-unlock, codex-window, achievements-window, save-progress, +multi-agent-sync, +fork-split, +merge-on-contact, +world-split-on-conflict, +measurement-collapse, +hint-ministage, +meta-puzzles, +collectible-secrets, +view-to-unlock]
proposes: ["+trigger:conflict", "+effect:split_world", "+window:hint-stage", "+card:world-split-on-conflict", "+card:merge-on-contact", "+card:view-to-unlock"]
author: opus
date: 2026-11-09
---

# Theta and Paralldox on Worldlines — дівчинка, що завжди повертає ліворуч, розщеплюється на копії, а суперечливі ходи розщеплюють сам світ

## Суть
Тета ходить сіткою за вводом гравця, але, впершись у стіну чи нерухомий обʼєкт, не зупиняється, а повертає до наступного вільного напрямку проти годинникової стрілки. Знайдена виделка розщеплює її на кілька копій, і всі копії отримують **один і той самий ввід** — окремо однією не походиш; копії, що зіткнулись, зливаються в одну. Коли дві дії суперечать (дві Тети штовхають один ящик у різні боки), гра не обирає переможця, а розщеплює світ на паралельні гілки, по одній на кожен результат. На цьому ядрі — ящики, ключі, замки, перемикачі, суперпозиція, заплутаність і, з 6-го розділу, час.

## Поле і час
- Квадратна сітка в 3D-діорамі, вигляд згори (Steam-теги 3D, Top-Down, Sokoban); камера на оверворлді пасивна, не обертається.
- Покроково: один ввід рухає всі копії одночасно; поворот біля стіни — частина того ж кроку.
- Кілька паралельних світів одночасно — копії рівня з різними станами; з 6-го розділу годинник у правому нижньому куті стає елементом пазлів («world-line»).
- 6 основних розділів, 240+ пазлів (Steam; itch — 250+), мета-пазли й приховані колекційні.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Тета (копія) | player | напрям руху | крок за вводом; впершись — поворот проти годинникової до вільного напрямку |
| Виделка | pickup | — | розщеплює Тету на кілька копій |
| Паралельний світ | zone | гілка | окрема версія рівня, що виникла при конфлікті дій |
| Ящик | object | — | штовхається; конфліктні поштовхи → розщеплення світу |
| Ключ | pickup | — | відмикає замок (?) |
| Замок / двері | gate | — | відкривається ключем або перемикачем (?) |
| Перемикач / кнопка | switch | належить стану світу | відчиняє «двері під тиском»; у суперпозиції неочевидно, якому стану належить |
| Шипи | hazard | — | небезпека; можуть ховатися під накритою плиткою |
| Стіна | static | — | непрохідна; причина повороту ліворуч |
| Годинник | static | на екрані | з розділу 6 — частина правил часу (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО `move(theta, dir)` для кожної копії одночасно.
- КОЛИ `blocked(theta)` → ТО `face(theta, ccw)`, `custom: «іде в наступний вільний напрям проти годинникової стрілки»`.
- КОЛИ `contact(theta, box)` → ЯКЩО `free(cell_behind)` → ТО `push(box)`; інакше — як `blocked(theta)`.
- КОЛИ `contact(theta, theta)` → ТО `merge(theta, theta, theta)` — копій стає менше.
- КОЛИ `picked(theta, fork)` → ТО `clone(theta)` — Тета розщеплюється (?: скільки копій і де зʼявляються).
- КОЛИ `custom: «два ефекти одного кроку суперечать (ящик штовхають у різні боки)»` → ТО `custom: «світ розщеплюється на паралельні гілки, у кожній — один результат»`.
- КОЛИ `contact(theta, lock)` → ЯКЩО `has(theta, key)` → ТО `disappear(lock)` (?).
- КОЛИ `enter(theta|box, switch)` → ТО `set_state(door, open)` (?).
- КОЛИ `enter(theta, spike)` → ТО `custom: «ця копія / гілка програє»` (?).
- КОЛИ `custom: «спостереження»` → ТО `custom: «суперпозиція колапсує в одну гілку»` (?).
- КОЛИ `custom: «ціль рівня досягнуто»` → ТО `win`, `next_level` (?).
- Перемога: умова рівня (?). Поразка: глухий кут → undo. Рахунку нема; колекційні зірки й стрічки — за мета-пазли.

## Керування і ввід
- Напрямок руху — клавіші (Steam-сторінка не уточнює розкладку) (?).
- Окремої копії не вибрати: усі поділяють ввід (відгук «can't move just one of them»).
- Undo — основний інструмент після небажаного злиття копій (відгуки; у версії є баги undo).

## Вікна, меню, HUD
- `game-screen`: діорама рівня; кілька світів-гілок; годинник у правому нижньому куті (розд. 6).
- `map-window` / оверворлд розділів з рівнями; рівень відкривається вже за **перегляд** попереднього, «контрольні» треба пройти.
- `hints-window` — «Gain Insight»: окремий міні-пазл, що моделює спосіб мислення, а не дає відповідь.
- `codex-window` — Notebook: що вже вивчено, суть поточного рівня «у сні Тети».
- `achievements-window` (Steam Achievements); мета-пазли й колекції (зірки, стрічки).

## Фічі поза полем
- `undo`, `restart-level`.
- `hint` у формі міні-рівнів (є лише в перших світах, автор додає), `codex` (Notebook).
- `level-unlock` за перегляд, `skip-level` фактично (пропускати можна, крім контрольних).
- `collectibles`, мета-пазли, `achievements`, `cloud-save`; `localization` (EN, 简体, 日本語).

## Варіації й родичі
- Від того ж видавця (Delta Theta) — [Maxwell's Puzzling Demon](../push-slide/maxwells-puzzling-demon.md) (бандл «Entropy and Multiverse»).
- Родичі: [Order of the Sinking Star](order-of-the-sinking-star.md) і [Recopy](recopy.md) (спільний ввід кількох агентів), [Can of Wormholes](can-of-wormholes.md) (міні-рівні-підказки), [Stephen's Sausage Roll](stephens-sausage-roll.md), [Bean and Nothingness](bean-and-nothingness.md), [Patrick's Parabox](patricks-parabox.md).
- **Осі варіацій**: що робить агент, впершись — стоїть / повертає ліворуч (тут) / праворуч · копії при зіткненні — блокують / зливаються (тут) · конфлікт ефектів — пріоритет / скасування / розщеплення світу (тут).

## Цікавинки для курсу
- Поворот проти годинникової до першого вільного напрямку — 🌱 (картка `turn-when-blocked`, але для гравця).
- Кілька аватарів зі спільним вводом і злиттям при зіткненні — 📎 (порядок обробки ходів).
- Детектор конфлікту двох поштовхів одного ящика — 🥉.
- Розщеплення світу: множина станів замість одного, кожна гілка живе далі — 🥇 (стан гри як множина світів, undo по всіх).
- Розвʼязувач над множиною світів — 👑.

## Мапа на каталог
- Є: `move-4dir`, `keyboard-controls` · `push-object` · `impassable-cells` · `turn-when-blocked` ↔ Тета біля стіни · `key-and-door`, `button-toggle` · `undo-redo` · `world-map`, `level-unlock` · `codex-window` ↔ Notebook · `achievements-window`, `save-progress`.
- **Нема** → пропозиції карток:
  - `+world-split-on-conflict` «Конфлікт ефектів розщеплює світ на гілки» · game-logic/history · 🥇.
  - `+merge-on-contact` «Копії гравця, зіткнувшись, зливаються в одну» · entities/interact · 🌱.
  - `+fork-split` «Предмет розщеплює аватара на копії» · entities/state · 📎.
  - `+view-to-unlock` «Наступний рівень відкривається за перегляд попереднього» · levels/progression · 🌱.
  - `+multi-agent-sync`, `+measurement-collapse`, `+hint-ministage`, `+meta-puzzles`, `+collectible-secrets` — є в інших файлах корпусу.

## Пропозиції до словників
- `+trigger:conflict` — два ефекти одного тіку суперечать один одному.
- `+effect:split_world` — стан гри розгалужується на паралельні світи.
- `+window:hint-stage` — підказка як окремий міні-рівень (підтверджую з can-of-wormholes.md).
- `+card:world-split-on-conflict`, `+card:merge-on-contact`, `+card:view-to-unlock` — див. вище.

## Джерела
- ⭐ [Steam](https://store.steampowered.com/app/3219580/) — «turns left every time she hits a wall», виделка розщеплює на копії, 6 розділів, 240+ пазлів, мета-пазли, підказки й Notebook; реліз 03.02.2026.
- [itch.io](https://xexlax.itch.io/paralldox) — одна чи кілька героїнь, 250+ пазлів, мета-пазли, колекційні.
- [Відгуки Steam (EN)](https://steamcommunity.com/app/3219580/reviews/?browsefilter=toprated&l=english) — спільний ввід, поворот проти годинникової, злиття копій, Gain Insight, відкриття рівнів за перегляд.
- [Відгуки Steam (中文)](https://steamcommunity.com/app/3219580/reviews/?browsefilter=toprated&l=schinese) — конфлікт дій → паралельні світи, суперпозиція, заплутаність, спостереження, годинник у розділі 6, ключі/замки/перемикачі/двері.
- YouTube: пошук «Theta and Paralldox on Worldlines gameplay».

## Непевне
- (?) Як саме виделка розщеплює Тету: при підбиранні, на розвилці коридору чи як дія гравця; скільки копій виникає.
- (?) Умова перемоги рівня (вихід, ціль, усі копії?) — у джерелах не названа.
- (?) Правила суперпозиції, заплутаності, спостереження й часу (розділи 3, 5, 6) — лише назви з відгуків.
- (?) Чи гинуть копії на шипах, чи «програє» вся гілка світу.
- (?) Розкладка клавіш і підтримка геймпада.
- Кількість пазлів: Steam — 240+, itch — 250+.
