---
title: Double Choco (Дабл-чоко)
slug: double-choco
aka: [Daburu Choko, ダブルチョコ, dbchoco]
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
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/double_choco/", best: true, note: "Nikoli: 3 правила, Sample → Progressing → Solution"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/dbchoco.js", note: "puzz.link dbchoco: правила, коди помилок, Puzzle Communication Nikoli vol. 163"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=double+choco+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 65
mechanics: [satisfy-constraints, markup-validity, completion-detection, edge-marking, connectivity-check, piece-rotate-flip, conflict-highlight, in-game-editor, undo-redo, +congruent-halves, +shape-identity-check, +no-dead-end-border, +two-color-block]
proposes: ["+cond:same_shape(a, b)", "+cond:no_dead_end(borders)", "+cond:one_area_per_color(block)", "+card:congruent-halves", "+card:two-color-block", "+card:shape-identity-check"]
author: opus
date: 2026-11-09
---

# Double Choco — розріж «шоколадку» на блоки: у кожному біла й сіра частини однакові за формою

## Суть
Сітка, де клітинки заздалегідь пофарбовані в білий і сірий, з числами в деяких клітинках. Гравець малює межі по пунктирних лініях і ділить сітку на блоки. Кожен блок складається рівно з двох звʼязних частин — білої й сірої — однакових за розміром і формою (одна може бути поворотом або дзеркалом іншої). Число каже, скільки клітинок свого кольору в блоці, тобто половину розміру блоку. Незвичне: обмеження **конгруентності двох половин** — блок «склеєний» з фігури і її копії. Nikoli, Puzzle Communication Nikoli vol. 163.

## Поле і час
- Прямокутна сітка; колір кожної клітинки (білий / сірий) — дана умова, гравець його не змінює.
- Розвʼязок — межі по ребрах; блоки довільного розміру (рівного 2·N для блоку з числом N).
- Сусідство ортогональне для звʼязності частин і блоків.
- Час статичний; хід = змінити стан одного ребра.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Біла клітинка | static | колір white | належить білій частині свого блоку |
| Сіра клітинка | static | колір grey | належить сірій частині свого блоку |
| Клітинка з числом | static | N; колір | частина її кольору в блоці має рівно N клітинок; блок = 2N |
| Ребро | mark | невідомо / межа / «не межа» | межі ріжуть сітку на блоки |
| Блок | zone | розмір 2N | рівно одна біла й одна сіра звʼязна частина; може мати кілька однакових чисел або жодного |
| Частина блоку | zone | колір, форма | звʼязна група одного кольору всередині блоку; конгруентна частині іншого кольору |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, edge)` → ТО `mark(edge, border)`; повтор → `unmark(edge)`; права кнопка → `mark(edge, no_border)` (?).
- КОЛИ `constraint_broken(parts)` → ЯКЩО `custom: «у блоці менше двох кольорових частин (один колір відсутній)»` → ТО конфлікт (`bkSubLt2`) (?).
- КОЛИ `constraint_broken(parts)` → ЯКЩО `custom: «у блоці більше двох частин — колір розірваний»` → ТО конфлікт (`bkSubGt2`) (?).
- КОЛИ `constraint_broken(shape)` → ЯКЩО `not same(white_part, grey_part, shape)` (з точністю до поворотів і відбиттів) → ТО конфлікт (`bkDifferentShape`).
- КОЛИ `constraint_broken(size)` → ЯКЩО `region_size(part_with_N, < N)` → ТО конфлікт (`bkSizeLt`); `> N` → `bkSizeGt`.
- КОЛИ `constraint_broken(border)` → ЯКЩО `custom: «межа обривається всередині блоку»` → ТО конфлікт (`bdDeadEnd`).
- КОЛИ `all_constraints_met` → ТО `win`.
- Наслідки: розмір блоку завжди парний; ізольована пара біла+сіра сусідніх клітинок — найменший блок (доміно 1+1); два різні числа в одній частині неможливі.
- Дедукції: число N у частині, де одноколірна звʼязна пляма вже рівно N, — пляма закривається межею від решти свого кольору; частина, чия форма не вміщається в жодну сусідню пляму протилежного кольору, мусить бути меншою; межа ставиться між однаковими кольорами, якщо їх обʼєднання перевищило б N.
- Перемога: усі блоки з двох конгруентних частин, числа виконані, нема обірваних меж. Поразки й рахунку нема.

## Керування і ввід
- puzz.link (цифрова версія): протягування лівою по пунктирних лініях — межі, права — «не межа»; Edit: колір клітинок і числа (?).
- Папір (Nikoli): тверді лінії поверх пунктирних.

## Вікна, меню, HUD
- `game-screen` (puzz.link): сітка з білими/сірими клітинками, числа, межі, `conflict-highlight` за Check.
- Кнопки: Check · Undo · Redo · Erase answer; Edit / Play (див. puzz-link).
- `help-window` — правила Nikoli (Sample / Progressing / Solution).
- `puzzle-select` — книги й журнал Nikoli (цифрова версія — банк пазлів).
- `end-screen` — розвʼязано.

## Фічі поза полем
- `undo`/`redo`, `auto-check` за кнопкою (puzz.link).
- `level-editor` + `share-code` — пазл у URL.

## Варіації й родичі
- **Choco Banana** (Nikoli) — інший «шоколадний» жанр: фарбування на прямокутні й непрямокутні області (?).
- **Tentai Show** — блоки з симетрією відносно точки; тут замість симетрії — копія іншого кольору.
- **Tachiawase Block** — теж конгруентність, але між двома сітками.
- **Pentominous**, **LITS** — порівняння форм фігур між сусідами.
- **Осі варіацій**: що спільне в частинах (форма / розмір / симетрія) · скільки частин у блоці (2 / більше) · чи задані кольори (так — Double Choco; ні — гравець фарбує).

## Цікавинки для курсу
- Перевірка конгруентності двох поліоміно за 8 симетріями (нормалізація зсувом) — 🥉.
- Розклад блоку на одноколірні компоненти і перевірка «рівно 2» — 📎.
- Межі-відрізки без глухих кінців (кожна межа розділяє різні блоки) — 🥉.
- Розвʼязувач з перебором розміщень частини і її копії поруч — 🥇.

## Мапа на каталог
- Є: `satisfy-constraints` · `markup-validity` · `completion-detection` · `edge-marking` · `connectivity-check` (частини звʼязні) · `piece-rotate-flip` (копія може бути повернута/віддзеркалена) · `conflict-highlight` · `in-game-editor` · `undo-redo`.
- **Нема** → пропозиції карток:
  - `+congruent-halves` «Блок з двох конгруентних частин» · game-logic/constraints · 🥉.
  - `+two-color-block` «Рівно одна частина кожного кольору в блоці» · game-logic/constraints · 📎.
  - `+shape-identity-check` (пропоновано в LITS).
  - `+no-dead-end-border` (пропоновано в Palisade).

## Пропозиції до словників
- `+cond:same_shape(a, b)` — однакова форма з поворотами й відбиттями.
- `+cond:no_dead_end(borders)` — межа не обривається всередині області.
- `+cond:one_area_per_color(block)` — у блоці кожен колір утворює рівно одну звʼязну частину.

## Джерела
- ⭐ [Nikoli: Double Choco](https://www.nikoli.co.jp/en/puzzles/double_choco/) — правила (блок = пара білої й сірої областей однакової форми, поворот/дзеркало дозволено; число = клітинки свого кольору = половина блоку).
- [puzz.link dbchoco.js](https://puzz.link/js/pzpr-samples/dbchoco.js) — правила англійською, vol. 163, коди `bkSubLt2`, `bkSubGt2`, `bdDeadEnd`, `bkSizeLt`, `bkSizeGt`, `bkDifferentShape`.
- YouTube: [пошук](https://www.youtube.com/results?search_query=double+choco+puzzle).

## Непевне
- (?) Рік: джерела дають лише vol. 163 Puzzle Communication Nikoli.
- (?) Значення `bkSubLt2` / `bkSubGt2` — виведено з назв кодів, не з тексту джерела.
- (?) Ввід у puzz.link для цього жанру — за загальною схемою, тестів вводу у файлі нема.
- (?) Опис Choco Banana — з памʼяті, сторінку не відкривав.
- Стаття Atlas Obscura про Double Choco віддала 403 — не використана.
