---
title: KaitoRamma (快刀乱麻)
slug: kaitoramma
aka: [快刀乱麻, Kaitoramma, Kaito Ranma, kramma]
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
  - {kind: other, url: "https://puzz.link/rules.html?kramma", best: true, note: "puzz.link: правила EN/JP з прикладом (сторінка рендериться JS)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/kramma.js", note: "текст правил EN/JP, Puzzle Communication Nikoli vol. 123, приклад 5×5, тест-коди bkNoNum і bkPlNum"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/kramma.js", note: "код kramma / kramman / shwolf: кружки в клітинках, межі по ребрах, протяжка до вузла з підказкою, перевірки"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json", note: "тексти помилок: «An area has no marks», «An area has both white and black circles»"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/kramman.js", note: "New Kaitoramma (Nikoli vol. 124): поворот лише на чорних точках, без глухих кінців"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/shwolf.js", note: "Goats and Wolves: кози й вовки замість кружків, лінії гнуться на точках"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=kaitoramma+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 70
mechanics: [satisfy-constraints, markup-validity, completion-detection, edge-marking, conflict-highlight, undo-redo, in-game-editor, level-solver, unique-puzzle-generation, help-window, +full-span-cuts, +mono-color-regions, +whole-line-toggle, +fail-code-checklist, +url-puzzle-encoding]
proposes: ["+card:full-span-cuts", "+card:mono-color-regions", "+card:whole-line-toggle"]
author: opus
date: 2026-11-19
---

# KaitoRamma — розріж поле прямими від краю до краю так, щоб білі й чорні кружки опинились у різних шматках

## Суть
Сітка з білими й чорними кружками в деяких клітинках; гравець проводить по пунктиру лінії — кожна пряма й тягнеться від одного краю поля до протилежного, лінії можуть перетинатися. Розрізи ділять поле на блоки: у кожному має бути хоча б один кружок, і жоден блок не може містити і білі, і чорні. Назва — японська ідіома «гострим ножем розрубати сплутане прядиво»; жанр зʼявився в Puzzle Communication Nikoli vol. 123.

## Поле і час
- Прямокутна сітка клітинок з пунктирними межами; кружки стоять у клітинках (у pzprjs — значення 1 / 2 клітинки), приклад puzz.link — 5×5.
- Розріз іде по межах клітинок прямо від краю до протилежного краю; горизонтальні й вертикальні розрізи перетинаються.
- Наслідок: кожен розріз — уся внутрішня лінія сітки, тож блоки завжди прямокутники між сусідніми вибраними лініями.
- Розвʼязок — це лише вибір, які з R − 1 горизонталей і C − 1 вертикалей різати.
- Час статичний; хід — поставити або зняти розріз.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | static | — | належить рівно одному блоку |
| Білий кружок | static | колір white | блок з ним — лише з білими |
| Чорний кружок | static | колір black | блок з ним — лише з чорними |
| Внутрішня лінія сітки | mark | розріз / нема | розріз — уся пряма від краю до краю |
| Допоміжна лінія | mark | — | нотатка гравця «тут не ріжемо» (права кнопка puzz.link) |
| Блок | zone | прямокутник | ≥ 1 кружок, кольори не змішані |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, edge)` → ТО `mark(line, cut)` — `custom: «зміна поширюється по прямій до вузла з підказкою; у kramma таких нема, тож — уся лінія від краю до краю»`; повтор — `unmark(line)` (puzz.link, з коду).
- КОЛИ `input(right_drag, edge)` → ТО `mark(edge, aux)` (допоміжна лінія-нотатка).
- КОЛИ `constraint_broken(block)` → ЯКЩО `count(circle_in_block, ==, 0)` → ТО `custom: «блок без кружка»` (puzz.link: An area has no marks).
- КОЛИ `constraint_broken(block)` → ЯКЩО `not same(circles_in_block, color)` → ТО `custom: «у блоці і білі, і чорні кружки»` (An area has both white and black circles).
- КОЛИ `constraint_broken(line)` → ЯКЩО `custom: «лінія ламається або не доходить до краю»` → ТО `custom: «розріз недійсний»` (папір; у puzz.link kramma ввід такого не дозволяє).
- КОЛИ `input(check)` → ТО `custom: «назвати перше порушене правило й підсвітити блок»` (puzz.link Check).
- КОЛИ `all_constraints_met` → ТО `win`, `message(solved)`.
- Наслідок: варіантів розрізу 2^(R−1) · 2^(C−1) — для 5×5 це 256, для 8×8 — 16 384.
- Дедукція «один рядок»: різнокольорові кружки в одному рядку розділить лише вертикаль між їхніми стовпцями — хоча б одна мусить бути; так само для стовпця.
- Дедукція «будь-яка пара»: різнокольорові кружки в різних рядках і стовпцях → потрібна горизонталь між рядками або вертикаль між стовпцями.
- Дедукція «порожня смуга»: рядок (стовпець) без кружків не можна відрізати з обох боків — вийдуть блоки без кружків.
- Дедукція «надлишок»: розріз, після якого якийсь прямокутник лишається без кружка, заборонений, навіть якщо він розділяє кольори.
- Перемога: у кожному блоці ≥ 1 кружок, кольори не змішані. Поразки й рахунку нема.

## Керування і ввід
- puzz.link, play: ліва кнопка — протягнути по пунктиру, щоб поставити чи зняти розріз; стан задає перше зачеплене ребро.
- Права кнопка — допоміжні лінії-нотатки.
- Edit-режим: розставити білі й чорні кружки; поле кодується в URL (див. [puzz.link](puzz-link.md)).
- Папір (Nikoli): провести лінії по пунктиру поверх сітки.

## Вікна, меню, HUD
- `game-screen` (puzz.link): поле з кружками й пунктиром, розрізи синім, панель: Check · Undo · Redo · Erase answer; меню File / Edit / Display / Setting / Help — як у всіх жанрах [puzz.link](puzz-link.md).
- `conflict-highlight`: Check підсвічує блок і пише текст першої помилки.
- `help-window`: rules.html?kramma — правила EN/JP з прикладом.
- `+window:game-id-dialog` (URL input / output) — обмін пазлом посиланням.
- Переходи: посилання p?kramma/… → game-screen (play) → Check → повідомлення «розвʼязано» або текст помилки.

## Фічі поза полем
- `undo` / `redo` без ліміту, `auto-check` за кнопкою з текстом першого порушеного правила.
- Редактор умови й обмін через URL; trial-режим і таймер — спільні для puzz.link (див. [puzz.link](puzz-link.md)).
- Генератора нема: пазли складають люди (Nikoli, автори puzz.link).

## Варіації й родичі
- **New Kaitoramma** (新・快刀乱麻, kramman; Nikoli vol. 124): на вузлах сітки — чорні точки; повернути на 90° лінія може лише на точці, через кожну точку проходять рівно дві лінії; поза точками лінії перетинаються й ідуть прямо; глухих кінців нема.
- **Goats and Wolves** (ヤギとオオカミ, shwolf): кози й вовки замість кружків; лінії доходять до рамки, гнуться лише на точках (не на кожній), до точки — не більше двох ліній, без петель через точки.
- [Shikaku](shikaku.md) — теж прямокутні блоки, але за числами-площами; [Double Choco](double-choco.md), [Palisade](palisade.md) — межі по ребрах з іншими умовами.
- **Осі варіацій**: форма розрізу (повна пряма / пряма з поворотами на точках / вільна межа) · що розділяють (кольори кружків / кози й вовки / числа) · чи дозволені перетини (так / не на точках) · чи мусить блок мати обʼєкт (так).

## Цікавинки для курсу
- Перебір підмножин горизонталей і вертикалей (2^(R+C−2)) з перевіркою прямокутників — 🌱: рідкісний пазл, який чесно розвʼязується повним перебором.
- Перевірка блоків: прямокутники решітки, у кожному ≥ 1 кружок і один колір — 🌱.
- Зведення до SAT: для кожної різнокольорової пари — «є лінія між ними», для кожного прямокутника — «не порожній» — 🥉.
- Ввід «протяжка ставить усю пряму»: правило вбудоване у ввід, перевіряти лишається тільки блоки — 📎.
- Генератор з єдиним розвʼязком: обрати лінії → розкидати кружки → прибирати зайві, перевіряючи перебором — 🥈.
- New Kaitoramma: лінії з поворотами лише на точках, без глухих кінців — 🥉.

## Мапа на каталог
- Є: `satisfy-constraints` · `markup-validity` · `completion-detection` · `edge-marking` ↔ лінії по пунктиру · `conflict-highlight` · `undo-redo` · `in-game-editor` ↔ Edit-режим · `level-solver` · `unique-puzzle-generation` · `help-window`.
- Перевикористано: `+fail-code-checklist`, `+url-puzzle-encoding` (puzz.link).
- **Нема** → пропозиції карток:
  - `+full-span-cuts` «Розрізи — лише повні прямі від краю до краю» · game-logic/constraints · 🌱 · слот {turns: none|at-dots}.
  - `+mono-color-regions` «У кожній області ≥ 1 обʼєкт і лише одного виду» · game-logic/constraints · 🌱 · слот {kinds: 2}.
  - `+whole-line-toggle` «Протяжка по ребру перемикає всю пряму до вузла-зупинки» · interface/input · 📎.

## Пропозиції до словників
- `+card:full-span-cuts` — розріз поля повними прямими (KaitoRamma; New Kaitoramma — з поворотами на точках).
- `+card:mono-color-regions` — області розділяють обʼєкти двох видів, порожніх областей нема (KaitoRamma, Goats and Wolves).
- `+card:whole-line-toggle` — ввід, який сам тримає правило «пряма від краю до краю».

## Джерела
- ⭐ [puzz.link: правила kramma](https://puzz.link/rules.html?kramma) — правила й приклад у браузері (рендер JS).
- [pzpr-samples/kramma.js](https://puzz.link/js/pzpr-samples/kramma.js) — правила EN/JP: прямі від краю до краю, можуть перетинатись, ≥ 1 кружок у блоці, без змішування; Nikoli vol. 123; приклад 5×5.
- [pzprjs: src/variety/kramma.js](https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/kramma.js) — модель поля, ввід, порядок перевірок для трьох жанрів.
- [pzprjs: failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json) — тексти помилок kramma і shwolf.
- [kramman.js](https://puzz.link/js/pzpr-samples/kramman.js), [shwolf.js](https://puzz.link/js/pzpr-samples/shwolf.js) — правила варіантів.
- YouTube: [пошук «kaitoramma puzzle»](https://www.youtube.com/results?search_query=kaitoramma+puzzle).

## Непевне
- (?) Рік: vol. 123 за квартальною нумерацією Nikoli (100 — осінь 2002, 130 — весна 2010) припадає приблизно на літо 2008; прямої дати не бачив, у шапці порожньо.
- (?) Що протяжка в kramma одразу ставить усю лінію — висновок з коду pzprjs (поширення через вузли без підказок), у браузері не перевіряв.
- (?) Типові розміри пазлів Nikoli не бачив; сторінку Nikoli для жанру не знайшов (вгадана адреса /ja/puzzles/kaitoramma/ віддала 404).
- (?) Переклад назви — загальне значення ідіоми 快刀乱麻, не з джерела про пазл.
