---
title: hexceed
slug: hexceed
aka: [Hexceed]
family: hidden-deduction
also: []
klass: cursor
axes:
  field: hex
  time: static
  opponent: none
  info: hidden
  random: none
  goal: state
year: 2021
platforms: [PC (Windows, macOS, Linux / Steam), Switch]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1463920/", best: true, note: "ToastieLabs, 15.01.2021, free to play; числа, лінії-напрямки, стіни, без вгадувань, сотні рівнів, мапа світу з milestone і side-рівнями, 42 DLC"}
  - {kind: other, url: "https://ec.nintendo.com/AU/en/titles/70010000041334", note: "Nintendo eShop (Switch): той самий опис, тач, 39 DLC"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=hexceed+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [cell-click, neighbor-count-clue, no-guess-generation, world-map, level-unlock, level-bank, completion-detection, save-progress, game-screen, achievements-window, +directional-line-clue, +wall-cell, +level-pack-dlc]
proposes: ["+cond:in_direction", "+card:directional-line-clue", "+card:wall-cell", "+card:level-pack-dlc", "+feature:dlc-level-packs"]
author: opus
date: 2026-11-09
---

# hexceed — гекс-сапер без вгадувань: сотні ручних рівнів на мапі світу, спецплитки-лінії й стіни

## Суть
Гексагональний сапер у стилі [Hexcells](hexcells.md): число на гексі показує, скільки «небезпек» серед сусідів, гравець кліками відкриває безпечні гекси. Кожна клітина має логічно виведену відповідь, вгадувати не треба; клік по небезпечному гексу «має наслідки». Головна відмінність від Hexcells — **спецплитки** з ціною: кожна дає нову інформацію й водночас щось забирає (лінія-напрямок, стіна…), і **мапа світу** з основною й побічними гілками рівнів. Гра безкоштовна, гроші — за пакети рівнів (DLC).

## Поле і час
- Гексагональна сітка, кожен рівень — своя унікальна розкладка (форма поля ручна (?)).
- Статичний пазл, без таймера (?).
- Шари: прихований вміст (безпечно / небезпека) + відкриті числа + спецплитки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Закритий гекс | static | прихований вміст | відкривається кліком |
| Число | mark | n = небезпеки серед 6 сусідів | підказка |
| Небезпека | hazard | — | клік по ній — «наслідки» (помилка / провал рівня (?)) |
| Лінія-напрямок | mark | напрям | вказує напрям; ймовірно, рахує небезпеки вздовж лінії (?) |
| Стіна | static | — | блокує «шлях» — розриває лінію/сусідство (?) |
| Інші спецплитки | mark | — | зʼявляються поступово, правила не документовано (?) |
| Milestone-рівень | zone | — | вузол основного маршруту на мапі світу |
| Side-рівень | zone | — | необовʼязковий вузол, «домальовує» мапу |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(open, c)` → ЯКЩО `not cell(c, danger)` → ТО `reveal(c)` зі значенням `adjacent_count(c, danger)` по 6 сусідах.
- КОЛИ `input(open, c)` → ЯКЩО `cell(c, danger)` → ТО `custom: «наслідок помилки — не описано»` (?).
- Лінія: `custom: «підказка вздовж напрямку (кількість небезпек на промені)»` (?).
- Стіна: `custom: «стіна обриває лінію / шлях»` (?).
- КОЛИ `custom: «усі безпечні гекси відкрито»` → ТО `win`, `unlock(next_node)` на мапі світу.
- Гарантія дизайну: кожна клітина має виведену відповідь — вгадування не потрібне.
- Перемога: розвʼязати рівень. · Поразка: (?) · Рахунок: — (прогрес мапи).

## Керування і ввід
- Лише миша (Steam: «mouse only»); тач на Switch.
- Позначки небезпеки (прапорці) — не згадано (?).

## Вікна, меню, HUD
- `game-screen`: гекс-поле з числами й спецплитками.
- `map-window` / `world-map`: вузли рівнів — основний маршрут через milestone, побічні side-рівні.
- `shop-window` (?) — DLC-пакети через магазин платформи, не в грі.
- `achievements-window` (Steam Achievements).

## Фічі поза полем
- `world-map` з основною й побічною гілкою, `level-unlock`.
- `cloud-save` (Steam Cloud, Switch Online), `achievements`, `localization` (13 мов на Steam, 11 на Switch).
- Модель free-to-play + `+feature:dlc-level-packs`: Year 1–5 Passes, тематичні пакети рівнів, саундтрек (42 add-on на Steam).

## Варіації й родичі
- [hexcells](hexcells.md) — прямий попередник жанру: гекс, без вгадувань, лінійні підказки, `{n}`/`-n-`; [tametsi](tametsi.md) і [patterna](patterna.md) — інші no-guess наступники; [globesweeper](globesweeper.md) (Hex Puzzler) — гекси на сфері з новими підказками.
- Осі варіацій: **підказки** сусіди / лінії / топологія / стіни як модифікатор · **подача рівнів** список / мапа світу з гілками · **модель** платна гра / F2P + пакети рівнів.

## Цікавинки для курсу
- Гекс-сапер із числами сусідів (axial-координати) — 🥉 (як у Hexcells).
- Стіна як модифікатор сусідства й ліній — 📎.
- Мапа світу з основним маршрутом і побічними вузлами — 🥉.
- Пакети рівнів як контент поза ядром (завантаження набору рівнів з файла) — 📎.

## Мапа на каталог
- Є: `cell-click` · `neighbor-count-clue` ↔ числа 6 сусідів · `no-guess-generation` ↔ «without the element of guesswork» (ручні рівні, перевірені на логіку) · `world-map` + `level-unlock` ↔ milestone/side · `level-bank` · `completion-detection` · `save-progress` ↔ Cloud · `game-screen` · `achievements-window`.
- **Нема** → пропозиції карток:
  - `+directional-line-clue` «Плитка-стрілка: підказка вздовж напрямку» · game-logic/constraints · 📎 (родич `line-sum-clue`, але на полі, а не за краєм).
  - `+wall-cell` «Стіна рве сусідство й лінії підказок» · game-logic/constraints · 🌱.
  - `+level-pack-dlc` «Пакети рівнів як окремий контент» · levels/bank · 📎.

## Пропозиції до словників
- `+cond:in_direction` — клітина лежить на промені від підказки в заданому напрямку (до стіни/краю).
- `+feature:dlc-level-packs` — додаткові набори рівнів поза базовою грою.

## Джерела
- ⭐ [Steam: hexceed](https://store.steampowered.com/app/1463920/) — ToastieLabs, 15.01.2021, F2P; «numbers show how many dangers», лінії-напрямки, стіни, «each mechanic gives you information while taking something away», без вгадувань, «100s of levels», milestone/side-рівні, 42 DLC.
- [Nintendo eShop](https://ec.nintendo.com/AU/en/titles/70010000041334) — той самий опис, тач, © 2020 ToastieLabs, 39 DLC.
- Огляди (voicemag.uk — 403; зміст лише з пошукової видачі): нові механіки вводяться поступово й не документовані.

## Непевне
- (?) Точна семантика лінії-напрямку й стіни — Steam лише називає їх; моє прочитання — промінь-підказка і розрив.
- (?) Наслідок кліку по небезпеці: лічильник помилок, як у Hexcells, чи провал рівня.
- (?) Решта спецплиток не названа в жодному відкритому джерелі; сайт toastielabs.com припаркований.
- (?) Чи є прапорці, підказки, undo, таймер.
- (?) «Сотні рівнів» — точної кількості нема.
