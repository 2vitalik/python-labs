---
title: Shakashaka (シャカシャカ)
slug: shakashaka
aka: [シャカシャカ, Шакашака]
family: pencil-logic
also: []
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: null
platforms: [paper, web]
links:
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/shakashaka/", best: true, note: "Nikoli: 4 правила, картинка чотирьох трикутників, Sample → Progressing → Solution"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Shakashaka", note: "правила, NP-повнота й #P-повнота (Demaine та ін., 2014)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/shakashaka.js", note: "puzz.link: правила EN/JP, «Nikoli vol. 123», режими вводу use_tri 1/2/3, коди помилок"}
  - {kind: other, url: "https://puzz.link/rules.html?shakashaka", note: "puzz.link: сторінка правил (рендериться JS)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=shakashaka+puzzle+how+to+solve", note: "пошук; розвʼязання"}
stage: v1
coverage: 60
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, keyboard-controls, neighbor-count-clue, in-game-editor, import-open-formats, undo-redo, dot-mark, +half-cell-triangles, +rect-shape-check, +input-scheme-toggle]
proposes: ["+cond:is_rectangle", "+effect:place_triangle", "+card:half-cell-triangles", "+card:rect-shape-check", "+ui:triangle-input-mode"]
author: opus
date: 2026-11-09
---

# Shakashaka — розстав чорні трикутники-половинки так, щоб усе біле стало прямокутниками (і під 45°)

## Суть
Сітка з білих і чорних клітинок; частина чорних має число 0–4. Гравець ставить у білі клітинки чорні прямокутні трикутники, кожен займає рівно половину клітинки (розріз по діагоналі, 4 орієнтації). Усе, що лишилось білим, має розпадатися на прямокутники — звичайні або повернуті на 45°. Число на чорній клітинці — скільки з її 4 ортогональних сусідів містять трикутник. Незвичне: розмітка не по клітинках, а по **половинках клітинки**, і форма перевіряється в геометрії з діагоналями.

## Поле і час
- Прямокутна сітка; типи клітинок: біла (порожня), чорна, чорна з числом 0–4.
- Шари: тип клітинки (незмінний) · стан білої: порожньо / трикутник у куті NE / NW / SE / SW / (мітка «тут біле» (?)).
- Похідна геометрія: біла область = обʼєднання білих клітинок і білих половинок; її межі — сторони клітинок і діагоналі трикутників.
- Час статичний; хід = поставити/зняти/змінити трикутник.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Біла клітинка | mark | стан empty / tri(corner) | приймає трикутник або лишається білою |
| Чорний трикутник | mark | кут: NE, NW, SE, SW | зафарбовує половину клітинки по діагоналі |
| Чорна клітинка | static | — | трикутник у неї ставити не можна; межа для білих областей |
| Чорна клітинка з числом | static | N 0–4 | рівно N з 4 ортогональних сусідів містять трикутник |
| Біла область | zone | форма | має бути прямокутником: прямим або повернутим на 45° |
| Мітка «біле» (крапка) | mark | — | позначка гравця, без впливу на перевірку (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, cell)` → ЯКЩО `cell(x, white)` → ТО `custom: «поставити трикутник у куті за схемою вводу»` (`+effect:place_triangle`); повтор — інша орієнтація або `unmark(cell)` (?).
- КОЛИ `input(click, cell)` → ЯКЩО `cell(x, black)` → ТО `block` (Nikoli: у чорні клітинки трикутників не ставлять).
- КОЛИ `constraint_broken(clue)` → ЯКЩО `adjacent_count(clue, triangle, >, N)` → ТО число конфліктне (puzz.link `nmTriangleGt`).
- КОЛИ `constraint_broken(clue)` → ЯКЩО `adjacent_count(clue, triangle, <, N)` і поле заповнене → ТО число конфліктне (puzz.link `nmTriangleLt`).
- КОЛИ `constraint_broken(shape)` → ЯКЩО `custom: «біла область не прямокутник ні прямо, ні під 45°»` (`+cond:is_rectangle`) → ТО область конфліктна (puzz.link `cuNotRectx`).
- КОЛИ `all_constraints_met` → ТО `win`.
- Дедукція «0»: усі 4 сусіди числа 0 — білі цілком.
- Дедукція «кут»: біла клітинка у куті між двома чорними (або чорною і рамкою) не може лишатись «зубцем» — або трикутник, що зрізає кут, або біле продовження прямокутника.
- Дедукція «нема 270°»: біла область з увігнутим кутом (270°) чи гострим кутом (45°) — не прямокутник; тому навколо кожної вершини сітки дозволені лише кілька локальних конфігурацій.
- Перемога: усі числа виконані, кожна біла область — прямокутник (прямий чи діагональний). Поразки й рахунку нема.

## Керування і ввід
- puzz.link: ліва/права кнопка й drag ставлять або знімають трикутник; налаштування `use_tri` з трьома схемами вводу (`setconfig,use_tri,1/2/3`) — як саме кожна обирає кут, з тестів не видно (?).
- puzz.link edit mode: курсор, клавіші `0–4` і `-` ставлять числа/чорні клітинки.
- Папір: гравець малює діагональ і заштриховує половину.
- Цифрова версія: undo/redo, перевірка за кнопкою (як у puzz.link).

## Вікна, меню, HUD
- `game-screen`: сітка, трикутники, `conflict-highlight` (числа/області з помилкою), кнопка перевірки.
- puzz.link: панель режимів (play/edit), меню налаштувань з вибором схеми вводу трикутників → `settings-window` + `+ui:triangle-input-mode`.
- `help-window` — правила (Nikoli, puzz.link rules).
- (цифрова версія) `puzzle-select` — банк пазлів Nikoli/збірок.
- Переходи: edit → play; check → повідомлення з кодом першої помилки.

## Фічі поза полем
- `auto-check` за кнопкою (puzz.link: код першої помилки).
- `undo` / `redo`; `level-editor` + `share-code` (puzz.link URL пазла).
- `custom-rules` ↔ вибір схеми вводу трикутників.
- Генератора в puzz.link нема (банк — книги й журнал Nikoli) (?).

## Варіації й родичі
- Родичі: [Light Up](light-up.md) (число на чорній = кількість обʼєктів поруч), [Shikaku](shikaku.md) (поле ділиться на прямокутники), [Nurikabe](nurikabe.md) (форма білих областей), Gokigen/Slant (діагоналі в клітинках, Tatham Slant у [Tatham Collection](tatham-collection.md)).
- Diagonal-пазли загалом: розмітка «половинкою» — рідкість серед Nikoli-жанрів.
- **Осі варіацій**: дозволені кути білих областей (лише 90° / також 45°-прямокутники) · що рахує число (сусіди з трикутником / площу) · форма-ціль (прямокутник / квадрат / будь-який опуклий) · сітка (квадратна / трикутна).

## Цікавинки для курсу
- Модель клітинки з 5 станами (порожня + 4 кути) і малювання трикутника — 🌱.
- Число = кількість сусідів з трикутником — 🌱 (`adjacent_count`).
- Перевірка «біла область — прямокутник» для прямих і 45°-прямокутників: розбиття на половинки клітинок, flood fill, перевірка кутів (лише 90°, без 45°/135°/270°) — 🥈.
- Локальна перевірка через таблицю допустимих конфігурацій навколо вершини замість глобальної геометрії — 🥉.
- Розвʼязувач з пропагацією локальних шаблонів — 🥇; NP-повнота (Demaine та ін.) — привід поговорити про складність — 👑.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `cell-click`, `keyboard-controls` · `neighbor-count-clue` ↔ числа · `in-game-editor`, `import-open-formats` ↔ puzz.link edit/URL · `undo-redo` · `dot-mark` (?).
- Перевикористано: `+rect-shape-check` (з Shikaku), `+input-scheme-toggle` (з Hitori) ↔ `use_tri`.
- **Нема** → пропозиції карток:
  - `+half-cell-triangles` «Діагональна половинка клітинки як стан» · entities/state · 📎 · слот {orientations: 2|4} — Shakashaka, Slant, дзеркала.
  - `+rect-shape-check` розширити слотом {rot: 0|45} — 45°-прямокутники Shakashaka.

## Пропозиції до словників
- `+cond:is_rectangle` — область має форму прямокутника (слот: дозволений поворот 45°); повтор з Shikaku.
- `+effect:place_triangle` — поставити в клітинку половинку з вибраним кутом.
- `+ui:triangle-input-mode` — перемикач схеми вводу орієнтації (клік-цикл / за квадрантом / drag) (?).
- `+card:half-cell-triangles`, `+card:rect-shape-check` — див. мапу.

## Джерела
- ⭐ [Nikoli: Shakashaka](https://www.nikoli.co.jp/en/puzzles/shakashaka/) — 4 правила, «four kinds» трикутників, приклади Sample/Progressing/Solution.
- [Wikipedia: Shakashaka](https://en.wikipedia.org/wiki/Shakashaka) — правила, «білі прямокутники не мають спільної сторони», NP-повнота і #P-повнота (Demaine, Okamoto, Uehara, Uno, IEICE 2014).
- [puzz.link shakashaka.js](https://puzz.link/js/pzpr-samples/shakashaka.js) — «rectangle can be upright, or rotated at a 45° angle», Nikoli vol. 123, `use_tri`, коди `brNoTriangle`, `nmTriangleGt`, `nmTriangleLt`, `cuNotRectx`.
- [puzz.link rules](https://puzz.link/rules.html?shakashaka) — сторінка правил (через WebFetch текст не рендериться).
- YouTube: пошук «shakashaka puzzle how to solve».

## Непевне
- (?) Рік: перша поява — Puzzle Communication Nikoli vol. 123; рік номера не перевірено (`year: null`).
- (?) Що означає `brNoTriangle` у puzz.link (можливо, трикутник у чорній клітинці або на рамці) — опису кодів у файлі нема.
- (?) Як працюють три схеми `use_tri` і чи є мітка-крапка для «білої» клітинки.
- (?) Чи має генератор будь-яка поширена цифрова версія.
- (?) Локальні дедукції «кут» і «нема 270°» — мій висновок з правила прямокутника, не цитата джерела.
