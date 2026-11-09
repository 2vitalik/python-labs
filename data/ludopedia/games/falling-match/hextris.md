---
title: Hextris (Гекстріс)
slug: hextris
aka: [Hextris.io]
family: falling-match
also: []
klass: cursor
axes:
  field: graph
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: survive
year: 2014
platforms: [web, iOS, Android]
links:
  - {kind: other, url: "https://github.com/Hextris/hextris", best: true, note: "відкритий код (GPLv3, JS): checking.js — збіги й очки, wavegen.js — патерни хвиль, Hex.js — обертання"}
  - {kind: other, url: "https://raw.githubusercontent.com/Hextris/hextris/gh-pages/js/initialization.js", note: "налаштування: рядів 8/7, 4 кольори, comboTime, рекорди top-3"}
  - {kind: play, url: "https://hextris.io/", note: "грати в браузері"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=hextris+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [gravity-fall, line-match-clear, chain-reaction, combo-multiplier, event-points, progress-acceleration, spawn-schedule, keyboard-controls, game-pause, end-screen, help-window, save-autosave, score-records, popup-text, game-loop, state-as-data, +radial-lanes, +rotate-field-not-piece, +spawn-wave-patterns, +combo-time-window, +colorblind-palette, +lane-overflow-lose]
proposes: ["+cond:since(event, op, t)", "+axis:field=radial", "+ui:combo-timer-ring", "+card:radial-lanes", "+card:spawn-wave-patterns"]
author: opus
date: 2026-11-09
---

# Hextris — шестикутник у центрі обертається, блоки летять до нього з 6 сторін; 3+ однакових зникають

## Суть
У центрі — шестикутник; з шести напрямків до нього повільно летять кольорові блоки й прилипають до його граней, утворюючи шість стовпців-«лан». Гравець не керує блоками — лише обертає центральний шестикутник на 60°, підставляючи потрібну грань. 3+ звʼязаних блоків одного кольору зникають, решта осідає до центру; серія швидких очищень дає множник. Програш — будь-яка лана переросла зовнішній сірий шестикутник.

## Поле і час
- Поле — 6 лан навколо центру (полярна сітка): лана = грань, позиція в лані = відстань від центру. Сусідство 4: попередній/наступний у тій самій лані і той самий рівень у сусідніх ланах (циклічно, 6 → 1).
- Ліміт — `rows`: 8 на десктопі, 7 на мобільних; блоки поза ним → кінець гри. Межу видно як зовнішній сірий шестикутник.
- Real-time: тік ≈16.7 мс (мобільні 14 мс); блоки летять безперервно до центру зі швидкістю, що росте зі складністю.
- Обертання не переносить блоки між ланами в даних: змінюється лише `position` шестикутника, і падаючий блок мапиться на лану з урахуванням повороту. Анімація повороту — кутова швидкість до цільового кута.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Шестикутник | player | position 0–5 | обертається на ±60° за ввід; до граней прилипають блоки |
| Падаючий блок | tile | колір (1 з 4), сторона, швидкість | летить від краю до центру; зіткнувся з гранню/верхнім блоком лани → прилипає |
| Блок у лані | tile | колір, індекс у лані | частина стека; після видалення нижчих — знову «падає» до центру |
| Генератор хвиль | spawner | nextGen (мс), складність 1–35 | породжує блоки за патернами: random, double, crosswise, spiral, circle, half-circle |
| Зовнішній шестикутник | static | rows | межа: блоків у лані > rows → поразка |
| Таймер комбо | zone | comboTime | кольорові лінії на зовнішньому шестикутнику; очищення в межах вікна → множник +1 |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(rotate_left|rotate_right)` → ЯКЩО `custom: «минуло ≥75 мс від попереднього повороту (не на мобільних)»` → ТО `rotate(hex, ±60)`.
- КОЛИ `input(hold_down)` → ТО `speed(falling_blocks, ×4)`; відпустив → `speed(falling_blocks, ÷4)`.
- КОЛИ `tick` → ТО `move(falling_block, to_center)` на `iter × dt`.
- КОЛИ `contact(falling_block, hex|top_block)` → ТО `custom: «прилипає в лану = (сторона, position) mod 6»`, `shake` у бік лани.
- КОЛИ `locked(block)` → ЯКЩО `pattern(group, 3)` and `same(a, b, color)` (сусідство: лана ±1 індекс, сусідні лани той самий індекс) → ТО `clear(group)`.
- КОЛИ `after(clear)` → ТО `fall(blocks_above)` до центру; приземлені знову перевіряються на групу — `chain-reaction`.
- КОЛИ `after(clear)` → ЯКЩО `custom: «від останнього очищення минуло < comboTime»` → ТО `combo(+1)`, `message(«x N»)`; інакше → `reset_combo` (comboTime = 240).
- Рахунок: `score(n² × m)` — n очищених блоків, m — множник комбо; `custom: «+score спливає в центрі кольором групи»`.
- КОЛИ `timer(nextGen)` → ТО `spawn_at(block, random_side)` за поточним патерном; після >5 одиночних — `rng` → інший патерн (double, crosswise — 2 протилежні того ж кольору, spiral по колу, circle — усі 6, half-circle — 3 поспіль).
- КОЛИ `destroyed(block)` → ТО `custom: «складність +0.085×speedModifier (≤35), nextGen −30/−8 (≥600 мс)»`; також складність росте з часом.
- КОЛИ `tick` → ЯКЩО `count(blocks_in_lane, >, rows)` → ТО `lose`; `custom: «рекорд у top-3, збереження стерто»`.
- КОЛИ `custom: «вікно втратило фокус»` → ТО `custom: «пауза»`.
- КОЛИ `custom: «закриття сторінки»` → ТО `custom: «стан гри (блоки, рахунок, хвиля, комбо) → localStorage»`; при відкритті — продовження.

## Керування і ввід
- Клавіатура: ←/A та →/D — поворот на 60° у різні боки; ↓/S (утримання) — прискорення падіння ×4; P/пробіл — пауза; Enter — старт/рестарт/продовжити.
- Тач/миша: тап у ліву / праву половину екрана — поворот; прискорення на тачі нема.
- Кнопки: пауза, рестарт, перемикач палітри для дальтоніків.

## Вікна, меню, HUD
- `main-menu` (стартовий екран): кнопка Start; якщо є збережений стан — продовження.
- `game-screen`: центральний шестикутник, ланці блоків, зовнішня межа (`danger-line`), `score` у центрі, `custom: «combo-timer-ring — кольорові лінії по зовнішньому шестикутнику»`, `popup-text` (+N, «x N»), `pause-button`.
- `help-window`: ціль (тримати блоки в сірому шестикутнику), керування, «3+ однакових — очки», пояснення таймера комбо.
- `pause-menu`: продовжити, рестарт.
- `end-screen`: рахунок, `hi-score` (top-3), рестарт, поділитися (?).
- Переходи: main-menu → game-screen ⇄ pause/help → end-screen → game-screen.

## Фічі поза полем
- `autosave` при закритті сторінки й `continue` після відкриття; `leaderboard-local` — top-3 у localStorage.
- `colorblind-palette` — кнопка альтернативних кольорів.
- `touch-controls` / `mouse-and-keyboard`; `pause` автоматично при втраті фокусу.
- Історія повороту по тіках (`history`) — заготовка під `replay` (?).

## Варіації й родичі
- Натхнення — Tetris (у README «inspired by Tetris»); ближча механіка — Puyo/Columns (група ≥3 по сусідству) і Tetrisphere (обертання поля).
- Клони/наступники — численні браузерні «hex/circle match» ігри (Hexagon-подібні; `(?)`).
- **Осі варіацій**: топологія (стовпці / радіальні лани / сфера Tetrisphere) · що обертає гравець (фігуру / поле) · джерело падіння (зверху / з усіх сторін) · умова очищення (група ≥3 / ряд) · комбо (каскад / часове вікно).

## Цікавинки для курсу
- Радіальна сітка «6 лан × рядів» з циклічним сусідством і flood-fill групи ≥3 — 📎.
- Обертання поля без перекладання даних: зсув індексу `position` замість переміщення масивів — 🌱.
- Генератор хвиль з патернами (spiral, circle, crosswise) і перемиканням за ймовірністю — 📎.
- Комбо як часове вікно між очищеннями, а не довжина каскаду — 🌱.
- Плавне обертання з кутовою швидкістю і «трусінням» лани при прилипанні — 📎 (GUI-анімація).
- Збереження/відновлення повного стану в localStorage — 🌱 (`state-as-data`).

## Мапа на каталог
- Є: `gravity-fall` (до центру) · `line-match-clear` (група ≥3; найближча) · `chain-reaction` · `combo-multiplier` · `event-points` · `progress-acceleration` · `spawn-schedule` · `keyboard-controls` · `game-pause` · `end-screen` · `help-window` · `save-autosave` · `score-records` · `popup-text` · `game-loop` · `state-as-data`.
- **Нема** → пропозиції карток:
  - `+radial-lanes` «Радіальні лани навколо центру» · interface/render · 📎 · слоти {lanes: 6, rows}.
  - `+rotate-field-not-piece` «Гравець обертає поле, а не фігуру» · entities/move · 🌱.
  - `+spawn-wave-patterns` «Патерни спавну хвиль» · entities/spawn · 📎 · слоти {patterns, switch_p}.
  - `+combo-time-window` «Комбо за часове вікно» · game-logic/score · 🌱 · слоти {window}.
  - `+colorblind-palette` «Палітра для дальтоніків» · interface/settings · 🌱.
  - `+lane-overflow-lose` «Програш: стовпець перевищив ліміт» · game-logic/lose · 🌱.

## Пропозиції до словників
- `+cond:since(event, op, t)` — від останньої події минуло порівняно з t (вікно комбо Hextris; затримка повороту).
- `+axis:field=radial` — полярна сітка: лани від центру з циклічним сусідством (Hextris; гравітація `toward-center` уже в коді).
- `+ui:combo-timer-ring` — таймер комбо, намальований по межі поля.
- `+card:radial-lanes`, `+card:spawn-wave-patterns` — див. «Мапа на каталог».

## Джерела
- ⭐ [GitHub: Hextris/hextris](https://github.com/Hextris/hextris) — код гри (GPLv3); файли js/: checking.js (група ≥3, очки n²×m, комбо), wavegen.js (патерни, складність 1–35, nextGen 2700→600), Hex.js (обертання, прилипання, shake), input.js (клавіші, тап-половини), main.js (поразка: блоків у лані > rows; довідка), initialization.js (rows 8/7, 4 кольори, top-3 рекордів, сейв при unload), update.js (порядок тіку, осідання після видалення).
- [hextris.io](https://hextris.io/) — грати (сертифікат при WebFetch не пройшов; сторінку не відкрив).

## Непевне
- (?) Сторінка hextris.io не відкрилась (помилка сертифіката) — опис лише з коду; версії для App Store / Google Play — з памʼяті.
- (?) Чи осідання після очищення запускає нові збіги автоматично — тіло `consolidateBlocks` не бачив; у `update.js` видно лише скидання `settled` для блоків вище.
- (?) Кнопка «поділитися» на end-screen і `replay` через `history` — у коді є натяки (`tweetblock`, `history`), функціональність не перевірена.
- (?) Рік 2014 — з рядка черги; у LICENSE — copyright 2018.
