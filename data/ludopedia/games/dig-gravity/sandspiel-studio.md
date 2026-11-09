---
title: Sandspiel Studio
slug: sandspiel-studio
aka: [studio.sandspiel.club]
family: dig-gravity
also: [thinky]
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: runtime
  goal: none
year: 2022
platforms: [web]
links:
  - {kind: official, url: "https://github.com/MaxBittker/sandspiel-studio", best: true, note: "README: блоковий конструктор елементів Sandspiel, «Cellular Autonoma Playground», MIT"}
  - {kind: other, url: "https://github.com/MaxBittker/sandspiel-studio/blob/main/docs/blocks.md", note: "довідник усіх блоків: Cells, Logic, Direction, Number, Data, Experimental"}
  - {kind: other, url: "https://raw.githubusercontent.com/MaxBittker/sandspiel-studio/main/prisma/schema.prisma", note: "схема галереї: пости з кодом, ремікс-дерево parentId, зірки, featured"}
  - {kind: play, url: "https://studio.sandspiel.club/", note: "грати й програмувати в браузері (бета)"}
  - {kind: other, url: "https://maxbittker.com/making-sandspiel", note: "двіжок оригінальної Sandspiel, на якому стоїть Studio"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Sandspiel+Studio+tutorial", note: "пошук; автор веде плейлист туторіалів"}
stage: v1
coverage: 55
mechanics: [interaction-table, cell-transform, game-loop, state-as-data, in-game-editor, editor-palette, editor-erase, level-exchange, level-rating, sensor-predicates, code-editor-window, rule-variants, keyboard-controls, +falling-sand-cell, +relative-neighbor-api, +cell-registers, +block-programming, +symmetry-expansion, +remix-tree, +end-of-frame-queue, +user-defined-elements]
proposes: ["+trigger:end_of_frame", "+cond:key_held", "+role:material", "+window:save-browser", "+feature:remix", "+card:block-programming", "+card:symmetry-expansion", "+card:remix-tree"]
author: opus
date: 2026-11-09
---

# Sandspiel Studio — falling sand, де кожен елемент гравець сам програмує блоками і публікує як ремікс

## Суть
Надбудова над [Sandspiel](sandspiel.md): замість фіксованих 19 елементів кожен вид частинки — **програма з блоків** (як у Scratch), яку гравець пише сам: «якщо знизу порожньо — поміняйся з ним». Програма виконується для кожної клітини виду щокадру, тобто гравець пише функцію `update` клітинного автомата, не знаючи цього слова. Готові «світи» (набір елементів + поле) публікуються в галерею, де їх зірочкують і реміксують — кожен ремікс памʼятає батька. Блок «Keyboard» дає змогу зробити керовану частинку, тож Studio — ще й конструктор маленьких ігор.

## Поле і час
- Квадратна сітка частинок, як у Sandspiel; розмір — не перевірено (?).
- Кожна клітина має 4 поля даних: Type, Color Fade (0–100, за замовчуванням випадкове), Hue Rotate (0–100, циклічно), Extra Data (0–100, «нічого не робить» — вільний регістр гравця).
- Тік = кадр: кожна клітина виконує програму свого Type; блок «End of Frame» відкладає дію, доки не діятимуть усі інші клітини.
- `time: programmed` — гравець задає правила, двіжок їх виконує в real-time; паралельно можна малювати по полю.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Елемент користувача (Type) | object | програма з блоків, колір | на кожному кадрі виконує свою програму відносно «me» |
| Empty | terrain | — | порожнеча; цільова клітина для swap/copy |
| Керований елемент (можливість) | player | блоки Keyboard + Arrow Keys Direction | програма міняється з клітиною в напрямку стрілок — з автомата виходить аватар |
| Поля клітини | mark | Color Fade, Hue Rotate, Extra Data | регістри 0–100 для стану й кольору; Change скидає їх |

## Правила (КОЛИ → ЯКЩО → ТО)
Правила тут — не правила гри, а **словник блоків**, з яких гравець їх складає:
- КОЛИ `tick` → ТО `custom: «виконати програму свого Type для кожної клітини»`.
- КОЛИ `tick` → ЯКЩО `cell(down, empty)` → ТО `swap(me, down)` — типова «падаюча» програма з довідника блоків.
- Блок Swap: `swap(me, v)` — помінятися з клітиною за вектором.
- Блок Copy: `clone(me → v)` — скопіювати себе в іншу клітину.
- Блок Change: `transform(v → type)` — змінити тип клітини; скидає Hue Rotate, Extra Data і Color Fade.
- Блок Check: умова `cell(v, type)` або `cell(v, type1|type2…)`.
- Блок Touching: умова `custom: «є сусід виду серед 8 клітин»`; Number Touching — `adjacent_count(me, type, op, n)`.
- Блок Chance: `prob(p)`; Random Number — випадкове між min і max.
- Блок Keyboard: умова `custom: «клавіша (пробіл, стрілки) затиснута»`; вектор Arrow Keys Direction — напрям стрілок.
- Блоки If / And / Or / Not / Compare / True / False — логіка для умов.
- Вектори: me, right, left, up, down, NE, SE, SW, NW, «? Neighbor» (випадковий сусід), Arrow Keys.
- Random Transformation: `custom: «виконати дію у випадковому повороті/віддзеркаленні»`; For Each Transformation — для кожного повороту/віддзеркалення; Rotated — повернути на N кроків по 45°.
- Operation: + − × ÷ % і різниця; Vector + Number повертає вектор за годинниковою.
- Get / Set / Modify Data: `set_value(me|v, field, n)` — регістри клітини.
- Repeat: повторити N разів · Every: `timer(every)` — «кожні три кадри» · End of Frame: `custom: «у чергу після всіх клітин»`.
- Перемоги, поразки й рахунку нема; мета — придумати поведінку й поділитися.

## Керування і ввід
- Поле: малювати обраним елементом і стирати (?) — як у Sandspiel.
- Редактор: перетягування блоків у програму елемента; кнопки додати/вибрати елемент (?) щодо точного UI.
- У грі: пробіл і стрілки — вхід для програм із блоками Keyboard / Arrow Keys Direction.

## Вікна, меню, HUD
- `game-screen`: полотно + `element-picker` (елементи поточного світу).
- `code-editor` — блоковий редактор програми обраного елемента поруч із полем (?) щодо компонування.
- `save-browser` — галерея творінь: зірки, перегляди, featured, публічні/приватні пости.
- `custom-window` дерево реміксів — батько і діти поста (`parent` / `children`) (?) щодо того, як показано.
- `profile-window` — вхід через OAuth (NextAuth: Account, Session); автор поста.
- Переходи: галерея → відкрити пост → поле з його елементами → змінити → опублікувати як ремікс.

## Фічі поза полем
- `mode-sandbox` + `custom-rules`: увесь набір правил — дані користувача.
- `level-sharing`, `user-levels-browser`, `level-rating` (зірки, featured), перегляди.
- Ремікс: новий пост з `parentId` старого — історія походження творінь.
- Акаунти, бан (`bannedAt`), мʼяке видалення (`deletedAt`), публічність поста (`public`).
- Туторіали — YouTube-плейлист і довідник блоків (`tutorial` поза грою).

## Варіації й родичі
- Батько: [sandspiel](sandspiel.md) — той самий двіжок і формат клітини, елементи жорстко в Rust.
- [sandboxels](sandboxels.md) — поведінка як текстова 3×3-сітка правил (DSL, моди JS); [the-powder-toy](the-powder-toy.md) — Lua-скрипти й таблиця властивостей.
- Ширше: SandPond (SpaceTode — візуальна мова правил «що бачу → що роблю»), Scratch, Baba Is You (правила як обʼєкти на полі).
- **Осі варіацій**: хто пише правила — «автор гри / модер на JS / гравець блоками»; одиниця правила — «функція на вид / 3×3-шаблон / блоки з симетріями»; спільнота — «файл / галерея / галерея з ремікс-деревом».

## Цікавинки для курсу
- Двіжок, що виконує правила-дані: інтерпретатор дерева блоків на кожну клітину — 🥈.
- Симетрії: For Each / Random Transformation розгортає одне правило в 4–8 поворотів — 📎: прибирає дублювання «вліво/вправо».
- Регістри клітини 0–100 (Color Fade, Hue Rotate, Extra Data) і скидання при Change — 🌱.
- End of Frame — відкладена черга дій після проходу всіх клітин — 📎.
- Керована частинка через Keyboard + Arrow Keys — 📎: з автомата виростає гра.
- Галерея з ремікс-деревом (`parentId`) і зірками — 🥈 як вебчастина.
- Довідник блоків як «паспорт гри» для студентів (Check/Touching/Swap — готові тригери й ефекти) — 🌱.

## Мапа на каталог
- Є: `interaction-table` (правила елементів як дані) · `cell-transform` (Change) · `sensor-predicates` (Check, Touching, Keyboard) · `code-editor-window` · `rule-variants` (гравець конструює правила) · `game-loop` · `state-as-data` · `in-game-editor` + `editor-palette` + `editor-erase` · `level-exchange` + `level-rating` · `keyboard-controls`.
- **Нема** → пропозиції карток:
  - `+block-programming` «Правила елемента блоками» · game-logic/program · 🥈 · слоти {cells, logic, direction, number, data}.
  - `+symmetry-expansion` «Одне правило в усіх поворотах і віддзеркаленнях» · entities/interact · 📎.
  - `+remix-tree` «Ремікс памʼятає батька» · levels/editor · 📎.
  - `+end-of-frame-queue` «Дії після проходу всіх клітин» · code/python · 📎.
  - `+user-defined-elements` «Гравець додає нові види клітин» · levels/editor · 🥈.
  - `+falling-sand-cell` · `+relative-neighbor-api` · `+cell-registers` — повтори з Sandspiel.

## Пропозиції до словників
- `+trigger:end_of_frame` — дія після того, як діяли всі клітини тіку.
- `+cond:key_held(key)` — клавіша затиснута (умова в правилі, а не тригер `input`).
- `+role:material` — повтор TPT/Sandspiel.
- `+window:save-browser` — повтор (галерея з зірками).
- `+feature:remix` — опублікувати змінену копію чужого творіння з посиланням на батька.
- `+card:block-programming` · `+card:symmetry-expansion` · `+card:remix-tree` — див. «Мапа на каталог».

## Джерела
- ⭐ [GitHub: sandspiel-studio](https://github.com/MaxBittker/sandspiel-studio) — README: блоковий конструктор, бета, буде безкоштовним, автори Max & Lu.
- [docs/blocks.md](https://github.com/MaxBittker/sandspiel-studio/blob/main/docs/blocks.md) — повний довідник блоків і 4 поля даних клітини.
- [schema.prisma](https://raw.githubusercontent.com/MaxBittker/sandspiel-studio/main/prisma/schema.prisma) — Post (code, parentId, public, views, featuredAt), Star, User, OAuth.
- [studio.sandspiel.club](https://studio.sandspiel.club/) — бета (сторінка без тексту для читача).
- [Making Sandspiel](https://maxbittker.com/making-sandspiel) — двіжок-основа.

## Непевне
- (?) Рік 2022 — з черги; ні README, ні схема дати не показують.
- (?) Розмір поля, компонування редактора й галереї, як саме показано ремікс-дерево — UI не відкрився (SPA без тексту).
- (?) Чи Studio — окрема гра чи вже «нова Sandspiel»: тримаю окремим файлом, бо програмування елементів — окрема механіка (у Sandspiel елементи фіксовані).
- (?) ⭐ HN-тред з черги (brianlovin.com/hn/35999835) — про Orb Farm, Studio там не описано; у шапку не взято.
