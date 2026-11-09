---
title: Clover's Quadrants
slug: clovers-quadrants
aka: [UDLR_Modify]
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: collect
year: 2026
platforms: [PC, Linux, web (прототип)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3191170/Clovers_Quadrants/", best: true, note: "повна гра Two-Headed Deer: опис ядра, 90+ пазлів, функції допомоги; відгуки з описом предметів"}
  - {kind: itch, url: "https://deertwoheads.itch.io/udlr-modify", note: "прототип UDLR_Modify (Acerola Jam 0, 2024): 20 рівнів, керування, джерельний код CC BY-NC-SA"}
  - {kind: play, url: "https://html-classic.itch.zone/html/9906281/index.html", note: "збірка прототипу (Godot 3.5.3); з неї прочитано Level.gd і формат рівнів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Clover%27s+Quadrants+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-4dir, move-by-input, keyboard-controls, inventory, inventory-items, item-pickup, push-object, collect-all, reach-exit, impassable-cells, undo-unlimited, restart-level, skip-level, level-select, save-progress, level-from-txt, sound-effects, movement-animation, idle-animation, +direction-slots, +jump-over, +eraser-token, +swap-slot, +eat-or-push, +move-helper, +multi-exit-cost]
proposes: ["+effect:jump", "+ui:direction-slots", "+feature:move-helper", "+card:direction-slots", "+card:eat-or-push"]
author: opus
date: 2026-11-09
---

# Clover's Quadrants — чотири напрями руху = чотири слоти інвентаря: зʼїдений символ змінює крок у той бік

## Суть
Sokoban-подібна головоломка Ian Spadin (Two-Headed Deer). Героїня Clover — кругле личко з чотирма секторами: вгору, вниз, ліворуч, праворуч. Символ, зʼїдений рухом у якийсь бік, займає сектор цього боку і відтоді змінює **кожен рух у той бік**: наприклад, крок стає стрибком через стіну. Мета — зʼїсти всі символи і дійти до виходу. Порядок поїдання вирішує все: «предмети шкодять так само часто, як допомагають» (Steam). Прототип — джемова UDLR_Modify (Acerola Jam 0, березень 2024, 20 рівнів). Повна гра (26.06.2026) має 90+ пазлів, нові типи предметів і змінені базові правила.

## Поле і час
- Квадратна сітка зі стінами; у прототипі рівень — текстова мапа: `#` стіна, `-` невидима стіна поза полем, `0`–`3` і `S` символи, `@` героїня, `$` вихід.
- Межі поля — найдальші обʼєкти мапи; вихід за них — «бонк».
- Хід = один ввід; стрибок на 2–3 клітини відбувається за один хід. Часу й ворогів нема.
- Повна гра: мальований фон і власний арт на кожному пазлі; кілька світів з «challenge»-рівнями.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Clover | player | 4 слоти: up/down/left/right | рух на k клітин у бік; k задає слот цього боку; їсть або штовхає символи |
| Символ «0» (порожній) | pickup | тип NONE | зʼїдається лише заповненим слотом і очищує його; інакше штовхається |
| Символ «1» | pickup | крок 1 | зʼїдається порожнім слотом; рух у той бік — на 1 |
| Символ «2» | pickup | стрибок 2 | рух у той бік — на 2, проміжна клітина ігнорується |
| Символ «3» | pickup | стрибок 3 | рух у той бік — на 3 |
| Символ «Swap» | pickup | — | у слоті: наступний зʼїдений символ кладеться на місце Swap, а не в слот руху |
| Стіна | static | видима / невидима | непрохідна; через неї можна перестрибнути |
| Вихід | static | активний / ні | активується, коли символів не лишилось; вхід в активний — перемога |
| Нові предмети повної гри | pickup | — | «рух лише на 1», «пропустити клітину», «заборона руху в бік» (з відгуків) |

## Правила (КОЛИ → ЯКЩО → ТО)
Рух (прототип, з коду):
- КОЛИ `input(dir)` → ТО `custom: «k = 1 для порожнього слота й «1», 2 для «2», 3 для «3»»`; ціль = позиція + k·dir; проміжні клітини не перевіряються (`+effect:jump`).
- КОЛИ `input(dir)` → ЯКЩО `free(target)` → ТО `move(clover, target)`.
- КОЛИ `input(dir)` → ЯКЩО `occupied(target, wall)` або `custom: «ціль поза межами поля»` → ТО `block`, `sound(bonk)`, струс.

Поїдання або поштовх:
- КОЛИ `contact(clover, token)` → ЯКЩО `state(slot[dir], empty)` і `not same(token, zero, type)` → ТО `pickup(clover, token)`, `set_value(clover, slot[dir] = token.type)`, `move(clover, target)`.
- КОЛИ `contact(clover, token_zero)` → ЯКЩО `not state(slot[dir], empty)` → ТО `pickup(clover, token_zero)`, `set_value(clover, slot[dir] = empty)`.
- КОЛИ `contact(clover, token)` → ЯКЩО `has(clover, swap)` і `not same(token, swap, type)` → ТО `pickup(clover, token)`, `set_value(clover, slot[swap_dir] = token.type)` — Swap витрачається.
- КОЛИ `contact(clover, token)` → ЯКЩО `custom: «зʼїсти не можна»` і `free(cell_behind)` → ТО `push(token)` рівно на 1 клітину (навіть після стрибка), `move(clover, target)`; інакше `block` і струс обох.

Мета:
- КОЛИ `all_gone(token)` → ТО `set_state(goal, active)` (шахова клітинка проявляється).
- КОЛИ `enter(clover, goal)` → ЯКЩО `state(goal, active)` → ТО `win`, `sound(win)`, `next_level`; у неактивний вихід можна просто стати.
- Повна гра: КОЛИ `enter(clover, exit)` → ТО `custom: «кожен із кількох виходів забирає по одному символу»` (з відгуку).

Сервіс:
- КОЛИ `input(undo)` → ТО `undo(1)` (стек станів без ліміту). КОЛИ `input(restart)` → ТО `restart`.
- Перемога: усі символи зʼїдено й досягнуто активного виходу. Поразки нема; глухий кут — undo.

## Керування і ввід
- Прототип: стрілки — рух; Z — undo; R — рестарт; O/P — попередній/наступний рівень; M — звук.
- Повна гра: клавіатура (і, ймовірно, геймпад (?)); пропустити будь-який рівень можна будь-коли.
- Рух у стіну нічого не змінює, лише трясе; гравці «спамлять» це, коли думають.

## Вікна, меню, HUD
- `game-screen`: поле; HUD — чотири стрілки-слоти навколо поля з поточним символом кожного боку (`+ui:direction-slots`), «підстрибують» при зміні; сектори на самій Clover; кільце, коли в слоті Swap.
- Повна гра: кружечки показують, куди можна рушити; клітини, що стали недосяжними після поїдання, візуально блокуються (помічники руху й парності).
- `hints-window`: візуальна підказка до кожного пазла (Steam).
- `level-select` / `world-map`: світи з рівнями й challenge-рівнями; «Free Play» відкриває все (`mode-practice`).
- `settings-window`: опція вимкнути личко Clover (відгук), мова (EN, JA, 简/繁 中文), допомога.
- Переходи: перемога → рівень відлітає вгору → наступний рівень.

## Фічі поза полем
- `undo` ∞, `restart-level`, `skip-level` без обмежень, `mode-practice` (Free Play).
- `hint` (візуальні підказки), `+feature:move-helper` (досяжні клітини й парність).
- `colorblind-palette` увімкнено за замовчуванням; `localization` на 4 мови.
- `save-progress`: прототип зберігає прогрес у cookies браузера.

## Варіації й родичі
- UDLR_Modify → Clover's Quadrants: ті самі слоти напрямів; у повній грі нові предмети, кілька виходів, що забирають символи, і змінені базові правила (які саме — (?)).
- `games/thinky/baba-is-you.md` — змінювати власні правила руху; тут правило належить окремому напряму.
- `games/thinky/heroes-of-sokoban.md` — різні дієслова в різних героїв; тут різні дієслова в різних напрямах одного героя.
- **Осі варіацій:** де живе модифікатор — у персонажа / у напрямку (тут) / у клітині; що робить предмет — довжина кроку / стрибок / заборона / обмін слотів; символ, який не можна зʼїсти, — блок / ящик (тут).

### UDLR_Modify (2024)
- Джемовий прототип для Acerola Jam 0 (зроблено 3–10 березня 2024), автор Ian Spadin (Two-Headed Deer): ті самі чотири слоти напрямів, символи 0–3 і Swap, стрілки + Z/R/O/P/M. Правила цього файла прочитано саме з коду прототипу, тож окремого файла нема. [itch.io: UDLR_Modify](https://deertwoheads.itch.io/udlr-modify)

## Цікавинки для курсу
- Чотири слоти напрямів і таблиця «тип → довжина кроку» — 🌱.
- Правило «зʼїсти чи штовхнути» залежно від стану слота й типу символу — 📎.
- Swap: перенаправлення результату в інший слот — 📎.
- Стрибок, що ігнорує проміжні клітини, плюс поштовх на 1 після стрибка — 🌱.
- Помічник досяжності: позначити клітини, недосяжні з поточного набору слотів (BFS за станами) — 🥈.
- Розвʼязувач: стан = позиція + 4 слоти + множина символів — 🥈.

## Мапа на каталог
- Є: `move-4dir`, `move-by-input`, `keyboard-controls`; `inventory` + `inventory-items` ↔ слоти; `item-pickup` ↔ поїдання; `push-object` ↔ символ, який не можна зʼїсти; `collect-all` + `reach-exit` ↔ мета; `impassable-cells`; `undo-unlimited`, `restart-level`, `skip-level`, `level-select`, `save-progress`; `level-from-txt` ↔ текстові мапи прототипу; `sound-effects`, `movement-animation`, `idle-animation` (символи погойдуються).
- **Нема** → пропозиції карток:
  - `+direction-slots` «Слот предмета на кожен напрямок руху» · entities/state · 🥉.
  - `+jump-over` «Крок на N клітин через перешкоди» · entities/move · 🌱.
  - `+eraser-token` «Символ, що очищує слот» · entities/interact · 🌱.
  - `+swap-slot` «Предмет перенаправляє наступний підбір в інший слот» · entities/state · 📎.
  - `+eat-or-push` «Предмет або підбирається, або штовхається» · entities/interact · 📎.
  - `+move-helper` «Підсвітка досяжних клітин і парності» · interface/hud · 🥈.
  - `+multi-exit-cost` «Кілька виходів, кожен забирає предмет» · game-logic/win · 📎.

## Пропозиції до словників
- `+effect:jump(a, n)` — переміститися на n клітин у напрямку, ігноруючи проміжні (Clover's Quadrants, шаховий кінь).
- `+ui:direction-slots` — чотири індикатори предметів напрямів навколо поля.
- `+feature:move-helper` — підсвітка досяжних клітин і попередження про парність.
- `+card:direction-slots`, `+card:eat-or-push` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Clover's Quadrants](https://store.steampowered.com/app/3191170/Clovers_Quadrants/) — «your four directions of movement correspond with four different inventory slots»; 90+ пазлів, помічники, підказки, пропуск, Free Play, colorblind; про UDLR_Modify; відгуки: збирати символи → вихід, кілька виходів, що забирають символ, кружечки-помічники.
- [itch.io: UDLR_Modify](https://deertwoheads.itch.io/udlr-modify) — керування (стрілки, Z, R, O/P, M), Godot 3.5.3, автор Ian Spadin, джерельний код; коментарі («even (red) movement», назви рівнів).
- [Збірка прототипу](https://html-classic.itch.zone/html/9906281/index.html) — розібрано `Level.gd`, `Player.gd`, `Token.gd`, `HUDArrow.gd`, мапи `levels/*.tres` і список з 21 рівня.
- Steam-кліпи (3) — Clover із секторами, шаховий вихід, символи «X», сон Clover.

## Непевне
- (?) Правила кроку, поїдання й Swap — з коду прототипу. Steam прямо каже, що в повній грі «modifying some of the base mechanics»; які саме — не перевірено.
- (?) Предмети повної гри «лише 1 клітина», «пропустити клітину», «заборона напрямку» і «вихід забирає символ» — лише з одного відгуку.
- (?) Підтримка геймпада в повній грі не перевірена.
- (?) Колір «червоного» (парного) руху з коментаря — ймовірно, символ «2».
