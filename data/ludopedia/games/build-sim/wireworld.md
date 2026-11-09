---
title: Wireworld
slug: wireworld
aka: [WireWorld, Вайрворлд, «Світ дротів»]
family: build-sim
also: [connect-rotate]
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: none
  goal: none
year: 1987
platforms: [web, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Wireworld", best: true, note: "4 стани, правило, Мур-8, діоди, годинники, XOR, Wireworld-компʼютер"}
  - {kind: itch, url: "https://celestial.itch.io/wireworld-1k", note: "PICO-8 демо: послідовний двійковий суматор 7-бітних чисел"}
  - {kind: official, url: "https://golly.sourceforge.io/", note: "Golly — WireWorld серед вбудованих типів КА"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=wireworld+cellular+automaton+computer", note: "пошук; логічні вентилі й компʼютер"}
stage: v1
coverage: 80
mechanics: [cell-click, editor-palette, editor-draw-tools, editor-erase, in-game-editor, game-loop, game-pause, state-as-data, level-from-txt, import-open-formats, field-scaling, logic-render-split, unit-tests, fixture-level-tests, +cellular-automaton-rule, +multi-state-cell, +step-run-speed, +pattern-library, +logic-circuit-wiring, +signal-visualization]
proposes: ["+card:multi-state-cell", "+card:signal-gate-library", "+ui:generation-counter", "+cond:adjacent_count_in"]
author: opus
date: 2026-11-09
---

# Wireworld — клітинний автомат-електроніка: 4 стани, електрони біжать провідником і складаються у вентилі

## Суть
Автомат Брайана Сільвермана (1987, програма Phantom Fish Tank), відомий з колонки Дьюдні в Scientific American (січень 1990). Клітина — порожнеча, провідник, голова або хвіст електрона; електрон («голова + хвіст») біжить провідником, бо голова стає хвостом, хвіст — провідником, а провідник поруч з 1–2 головами — головою. Гравець малює схему (дроти, діоди, годинники, вентилі) і запускає; з цього збирають суматори, дисплеї й Тюрінг-повний компʼютер Марка Оуена. Ядро — **багатостанова клітина з циклом станів** і поріг «1 або 2 сусіди», що робить діоди можливими.

## Поле і час
- Квадратна сітка; сусідство Мура радіусу 1 (8 сусідів, включно з діагональними) — тому дріт може йти по діагоналі.
- 4 стани: 0 — порожньо (чорний), 1 — голова (синій), 2 — хвіст (червоний), 3 — провідник (жовтий). Інші реалізації: дріт золотий, хвіст білий (Wireworld 1K).
- Тік = покоління, синхронне оновлення з повного старого стану (подвійний буфер).
- Порожні клітини ніколи не змінюються — поле «живе» лише вздовж провідників, тож розріджене зберігання дуже ефективне.
- Темп — від користувача: крок, запуск, швидкість.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Порожня клітина | static | стан 0 | завжди лишається порожньою (ізолятор) |
| Провідник | conduit | стан 3 | стає головою, якщо серед 8 сусідів рівно 1 або 2 голови; інакше лишається провідником |
| Голова електрона | tile | стан 1 | наступного тіку стає хвостом |
| Хвіст електрона | tile | стан 2 | наступного тіку стає провідником (не дає сигналу піти назад) |
| Електрон | object | голова + хвіст | емерджентний: рухається провідником на 1 клітину за тік у бік від хвоста |
| Діод | object | форма з провідника | пропускає електрон в один бік; у зворотному — блокує |
| Годинник (clock) | spawner | петля з електроном, довжина = період | випускає електрон у вихідний дріт раз на оберт |
| Вентиль (OR, XOR, AND, NOT…) | object | 2 входи, 1 вихід | емерджентна схема з провідника; XOR — класичний приклад Wikipedia |
| Дисплей / декодер | object | 7 сегментів | Wikipedia показує семисегментний дисплей з декодером |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ЯКЩО `cell(x, empty)` → ТО лишається `empty`.
- КОЛИ `tick` → ЯКЩО `cell(x, head)` → ТО `set_cell(x, tail)`.
- КОЛИ `tick` → ЯКЩО `cell(x, tail)` → ТО `set_cell(x, conductor)`.
- КОЛИ `tick` → ЯКЩО `cell(x, conductor)` and `adjacent_count(x, head, in, {1,2})` → ТО `set_cell(x, head)`; інакше лишається `conductor`.
- Усі переходи рахуються з **старого** стану і застосовуються разом.
- Наслідок 1 (рух): хвіст за головою — провідник позаду ще не «вільний», тож голова може народитись лише попереду → електрон біжить в один бік.
- Наслідок 2 (діод/вентиль): КОЛИ `tick` → ЯКЩО `adjacent_count(x, head, >=, 3)` → ТО провідник не збуджується — так конструкції «гасять» сигнал (зворотний бік діода, частина XOR).
- Наслідок 3 (розгалуження): дріт, що ділиться, копіює електрон в обидві гілки — `custom: «сигнал дублюється без втрат»`.
- КОЛИ `input(click, cell)` → ТО `set_cell(cell, selected_state)` (палітра: порожньо / провідник / голова / хвіст).
- Перемоги/поразки/рахунку нема; «ціль» задає людина (зібрати суматор, лічильник, дисплей).

## Керування і ввід
- Типовий редактор (Golly, web-версії): вибір стану з палітри, клік/drag малює, гумка; Run/Pause, Step, швидкість; зум і пан.
- Wireworld 1K (PICO-8): Z, X або стрілка — наступний крок демо; демо ділиться на фази «кинути кості» (два випадкові числа A, B) → обчислення → вивід суми.
- Читання результату 1K: вхід/вихід послідовні, little-endian — сумуєш ваги розрядів, де стоїть електрон.

## Вікна, меню, HUD
- `game-screen` (типова цифрова версія): поле з `zoom-control`, `grid-lines`, `element-picker` чотирьох станів, кнопки Run/Pause, `step-button`, `speed-slider`, Clear.
- HUD: `generation-counter`, координати під курсором.
- `custom-window` «Бібліотека» (Golly: патерни Wireworld, зокрема компʼютер) — вставити готову схему.
- Import/Export (`custom-window`): RLE-файл або вставлення з буфера.
- Wireworld 1K: один екран-демо з підписами фаз і пояснювальними діаграмами на сторінці itch.

## Фічі поза полем
- `step-mode`, `speed-control`, `pause`; `export-import` патернів; `level-editor` = сама гра.
- Бібліотека схем (діоди, годинники, вентилі, компʼютер) — аналог `puzzle-bank` без прогресу.
- Нема рахунку, збережень прогресу, режимів.

## Варіації й родичі
- **Осі варіацій:** кількість станів (Life — 2, Wireworld — 4, Brian's Brain — 3) · поріг збудження (тут {1,2}) · сусідство (Мур-8 / фон Нейман-4) · «чи порожнеча змінюється» (тут ніколи — схема статична, рухається лише сигнал).
- Родичі в корпусі: [game-of-life](game-of-life.md) (лічильник сусідів, але без каналів), [cell-machine](cell-machine.md), [langtons-ant](langtons-ant.md) (Wikipedia: мураху можна побудувати у Wireworld), [factorio-belts](factorio-belts.md) і [mindustry](mindustry.md) (логіка-сигнали поверх логістики), [oxygen-not-included-cells](oxygen-not-included-cells.md) (автоматика-дроти).
- Ігри-нащадки: «схемотехнічні» пазли (логічні вентилі з дротів) — ідея «сигнал = рухомий стан клітини».

## Цікавинки для курсу
- Крок Wireworld з 4 станами і порогом {1,2} — 🌱 (класика після Life; той самий подвійний буфер).
- Редактор з палітрою станів + збереження/завантаження схеми — 📎.
- Бібліотека перевірених схем (діод, годинник, XOR) як тести-фікстури: «через N тіків на виході електрон» — 📎 (`fixture-level-tests`).
- Розріджене оновлення: зберігати лише провідники й голови, рахувати тільки сусідів голів — 🥉 (оптимізація під великі схеми).
- Зібрати суматор/лічильник на Wireworld — 🥈 (дизайн схеми + синхронізація годинників).
- Компілятор «вентилі → клітини» (розкласти схему з AND/OR/NOT по сітці) — 👑.

## Мапа на каталог
- Є: `cell-click` · `editor-palette` (4 стани) · `editor-draw-tools` · `editor-erase` · `in-game-editor` · `game-loop` + `game-pause` · `state-as-data` · `level-from-txt` + `import-open-formats` (RLE) · `field-scaling` · `logic-render-split` · `unit-tests` + `fixture-level-tests`.
- **Нема** → пропозиції карток:
  - `+multi-state-cell` «Клітина з циклом станів (голова → хвіст → провідник)» · game-logic · 📎 · слоти {states, transitions} — узагальнює Life/Brian's Brain/Wireworld.
  - `+signal-gate-library` «Бібліотека вентилів-патернів з тестами» · levels/bank · 📎.
  - Перевикористано: `+cellular-automaton-rule`, `+step-run-speed`, `+pattern-library`, `+logic-circuit-wiring`, `+signal-visualization`.

## Пропозиції до словників
- `+card:multi-state-cell`, `+card:signal-gate-library` — див. «Мапа на каталог».
- `+ui:generation-counter` — номер покоління (Life, Langton, Wireworld).
- `+cond:adjacent_count_in` — кількість сусідів у множині значень ({1,2}); зараз пишеться `adjacent_count(x, head, in, {1,2})`, але `in` не описано в словнику операторів.

## Джерела
- ⭐ [Wikipedia: Wireworld](https://en.wikipedia.org/wiki/Wireworld) — 4 стани і кольори, правило 1–2 голови, Мур-8, Сільверман 1987, Дьюдні 1990, діоди, годинники + XOR, семисегментний дисплей, компʼютер.
- [Wireworld 1K на itch.io](https://celestial.itch.io/wireworld-1k) — PICO-8 демо суматора (7 біт, little-endian), діаграми розгалуження й діодів.
- [Golly](https://golly.sourceforge.io/) — WireWorld серед вбудованих типів КА.
- YouTube: пошук «wireworld cellular automaton computer».

## Непевне
- (?) Що саме обчислює Wireworld-компʼютер Марка Оуена (поширено — прості числа) — Wikipedia цього не каже; сторінка Оуена (quinapalus.com) і LifeWiki віддали 403.
- (?) Точні форми діода й вентилів (кількість клітин) — не перемальовано з джерела; механізм «≥3 голови → не збуджується» виведено з правила.
- (?) Набір кнопок «типового редактора» — узагальнення; Wireworld 1K редагування не має.
