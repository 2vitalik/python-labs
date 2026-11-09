---
title: Chocolate Fix (ThinkFun)
slug: chocolate-fix
aka: [Шоколадна коробка, ThinkFun Chocolate Fix]
family: board-digital
also: [pencil-logic]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: null
platforms: [board, iOS, Android]
links:
  - {kind: official, url: "https://legacy.thinkfun.com/products/chocolate-fix/", best: true, note: "офіційна сторінка (бачив у видачі пошуку; при відкритті 503)"}
  - {kind: other, url: "https://legacy.thinkfun.com/wp-content/uploads/2015/09/Choco-1530-IN03.pdf", note: "офіційні правила PDF (бачив у видачі; при відкритті 503)"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/ThinkFun", note: "ThinkFun: Chocolate Fix серед основних продуктів, мобільні версії"}
  - {kind: other, url: "https://jrmf.org/puzzle/chocolate-fix/", note: "JRMF: шкільна активність за мотивом (спрощена 2×2), веб-версія"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=ThinkFun+Chocolate+Fix", note: "пошук; як грати"}
stage: v1
coverage: 55
mechanics: [drag-drop-piece, satisfy-constraints, completion-detection, markup-validity, pencil-marks, level-bank, puzzle-select, difficulty-levels, sequential-levels, unique-puzzle-generation, difficulty-rating, level-solver, +partial-pattern-clue, +floating-clue-fragment, +shape-color-attributes, +each-combo-once, +solution-on-back]
proposes: ["+cond:matches_fragment(clue, offset)", "+cond:attr(cell, shape|color)", "+role:clue-fragment", "+ui:clue-cards", "+ui:attribute-placeholder", "+card:floating-clue-fragment", "+card:partial-pattern-clue"]
author: opus
date: 2026-11-09
---

# Chocolate Fix — розкласти 9 цукерок у коробку 3×3 за уривками-підказками, де відомий то колір, то форма

## Суть
Одиночна дедуктивна головоломка ThinkFun: 9 цукерок трьох смаків (ваніль, шоколад, полуниця) треба розкласти в лоток 3×3 так, щоб виконались усі підказки картки. Кожна підказка — уривок майбутнього розкладу, де частина клітин показує цукерку повністю, частина — лише форму або лише колір. Розвʼязок єдиний; перевірка — розворотом картки. Близько до `pencil-logic` (статична розмітка за обмеженнями), але фізична настолка з фішками.

## Поле і час
- Поле — лоток 3×3; кожна клітина приймає одну цукерку.
- Шари: лоток (цукерки) + картка завдання (набір підказок-уривків) + необовʼязкові фішки-заглушки «форма» / «колір» для часткових знань.
- Час статичний: без ходів і лічильника; пазл розвʼязано, коли всі 9 клітин заповнені й усі підказки справджуються.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітина лотка | terrain | 3×3 | порожня або з цукеркою |
| Цукерка | piece | смак white/brown/pink × форма | кладеться в клітину; 9 штук, по 3 кожного смаку |
| Заглушка форми | mark | форма без кольору | позначка «тут ця форма, смак невідомий» |
| Заглушка кольору | mark | колір без форми | позначка «тут цей смак, форма невідома» |
| Підказка-уривок | zone | k×m клітин | клітини: повна цукерка / лише форма / лише колір / невідомо |
| Повна підказка 3×3 | zone | фіксована | накладається на лоток без зсуву |
| Картка завдання | supply | рівень складності | набір підказок; розвʼязок на звороті |

## Правила (КОЛИ → ЯКЩО → ТО)
- Хід: КОЛИ `input(place(candy, cell))` → ЯКЩО `free(cell)` → ТО `place(candy)`; інакше `swap(candy, other)` або `block`.
- Заглушка: КОЛИ `input(place(placeholder, cell))` → ТО `mark(cell, shape|color)` — допоміжна розмітка, на перевірку не впливає.
- Повна клітина підказки: ЯКЩО `custom: «клітина підказки показує цукерку»` → ТО у відповідній клітині лотка `same(candy, clue, shape)` and `same(candy, clue, color)`.
- Клітина «форма»: ЯКЩО `custom: «клітина підказки — лише контур форми»` → ТО `same(candy, clue, shape)`; смак — будь-який.
- Клітина «колір»: ЯКЩО `custom: «клітина підказки — лише пляма кольору»` → ТО `same(candy, clue, color)`; форма — будь-яка.
- Порожня клітина підказки: ТО `custom: «обмеження нема»`.
- Повна підказка: ЯКЩО `custom: «підказка розміром 3×3»` → ТО накладається на лоток рівно.
- Уривок: ЯКЩО `custom: «підказка менша за 3×3»` → ТО `custom: «має справджуватися хоча б при одному зсуві в межах лотка»` (див. «Непевне»).
- Унікальність: ЯКЩО `custom: «кожне поєднання смак × форма лише один раз»` → ТО обмеження діє на весь лоток (див. «Непевне»).
- Перемога: КОЛИ `all_constraints_met` and `count(empty_cell, =, 0)` → ТО `win`.
- Перевірка: КОЛИ `input(custom: «перевернути картку»)` → ТО `feedback(guess)` — збіг з розвʼязком на звороті.
- Порушення: КОЛИ `constraint_broken(clue)` → ТО `custom: «у цифровій версії — підсвітити підказку»`.

## Керування і ввід
- Фізично: взяти цукерку → покласти в клітину; переставити; поставити заглушку форми/кольору як «олівцеву» позначку.
- Цифрова версія: drag цукерки з запасу на клітину, drag між клітинами = обмін; окремий режим заглушок (аналог `pencil-marks`); кнопка «перевірити».

## Вікна, меню, HUD
(цифрова версія; мобільні версії згадані у Wikipedia, екрани не перевіряв)
- `main-menu`: Грати → `puzzle-select` · Правила → `help-window`.
- `puzzle-select`: картки за рівнями (від початкового до експертного) з позначками «розвʼязано».
- `game-screen`: лоток 3×3, запас 9 цукерок, `clue-cards` (кандидат: уривки підказок), `attribute-placeholder` (кандидат), `check-button`, `restart-button`.
- `end-screen`: «замовлення виконано», наступна картка.

## Фічі поза полем
- `puzzle-bank`: 40 карток завдань з розвʼязками, від Beginner до Expert.
- `levels-sequential` · `stars-rating` або позначки — лише цифрова версія (?).
- `show-solution` — розвʼязок на звороті картки.

## Варіації й родичі
- Родичі ThinkFun «картка-завдання + фізичні фішки»: [thinkfun-logic-mazes](thinkfun-logic-mazes.md), [code-master](code-master.md); також [quarto](quarto.md) (фігури з кількома атрибутами).
- Паперові родичі: [zebra-puzzle](../pencil-logic/zebra-puzzle.md) (дедукція за частковими твердженнями), [sudoku](../pencil-logic/sudoku.md) (кожне значення один раз).
- JRMF-варіант 2×2 з двома смаками й двома формами — шкільна активність.
- **Осі варіацій**: розмір лотка (2×2 / 3×3) · атрибути цукерки (смак, форма, (?) третій) · тип підказки (повна / форма / колір / заборона) · уривок фіксований чи «плаваючий».

## Цікавинки для курсу
- Модель цукерки як пари атрибутів і клітина підказки з маскою «форма/колір/обидва/нічого» — 🌱.
- Перевірка плаваючого уривку: перебір зсувів у межах 3×3 — 📎.
- Розвʼязувач перебором 9! перестановок із відсіканням — 📎; через пропагацію обмежень — 🥉.
- Генерація завдання з єдиним розвʼязком і мінімальним набором уривків — 🥇.
- Оцінка складності картки за технікою, потрібною розвʼязувачу — 🥇.
- Цифрові заглушки форми/кольору як pencil-marks — 🌱.

## Мапа на каталог
- Є: `drag-drop-piece` · `satisfy-constraints` · `completion-detection` · `markup-validity` · `pencil-marks` (заглушки) · `level-bank` · `puzzle-select` · `difficulty-levels` · `sequential-levels` · `unique-puzzle-generation` · `difficulty-rating` · `level-solver`.
- **Нема** → пропозиції карток:
  - `+partial-pattern-clue` «Підказка — частковий шаблон з масками атрибутів» · game-logic/constraints · 📎 · слоти {mask: [full, shape, color, none]}.
  - `+floating-clue-fragment` «Уривок без координат: справджується при якомусь зсуві» · game-logic/constraints · 📎.
  - `+shape-color-attributes` «Фігура з двома незалежними атрибутами» · entities/state · 🌱.
  - `+each-combo-once` «Кожне поєднання атрибутів — рівно один раз» · game-logic/constraints · 🌱.
  - `+solution-on-back` «Розвʼязок поруч із завданням (перевірка розворотом)» · levels/bank · 🌱.

## Пропозиції до словників
- `+cond:matches_fragment(clue, offset)` — уривок підказки збігається з лотком при зсуві.
- `+cond:attr(cell, shape|color)` — у клітині фігура з атрибутом (точніше за `same` для маски).
- `+role:clue-fragment` — підказка-уривок як сутність поза полем.
- `+ui:clue-cards` · `+ui:attribute-placeholder`.
- `+card:floating-clue-fragment` · `+card:partial-pattern-clue`.

## Джерела
- ⭐ [ThinkFun: Chocolate Fix](https://legacy.thinkfun.com/products/chocolate-fix/) — офіційна сторінка (у видачі пошуку; при відкритті 503).
- [Правила PDF](https://legacy.thinkfun.com/wp-content/uploads/2015/09/Choco-1530-IN03.pdf) — у видачі пошуку; при відкритті 503. З уривків видачі: мета — заповнити лоток 9 цукерками за підказками; кожне завдання має єдиний розвʼязок; перевірка розворотом картки; 40 карток Beginner → Expert; 9 цукерок (по 3 ваніль/шоколад/полуниця); 18 заглушок форми й кольору; 1 гравець, 8+.
- [Wikipedia: ThinkFun](https://en.wikipedia.org/wiki/ThinkFun) — Chocolate Fix серед основних продуктів; мобільні версії (iPhone, Android); згадка в дослідженні когнітивних навичок.
- [JRMF: Chocolate Fix](https://jrmf.org/puzzle/chocolate-fix/) — активність за мотивом, веб-версія (спрощена).

## Непевне
- (?) Форми цукерок (кругла, квадратна, трикутна) і правило «кожне поєднання смак × форма один раз» — з памʼяті; джерела підтверджують лише 3 смаки по 3 штуки.
- (?) Правило «уривок менший за 3×3 можна зсувати по лотку, повна 3×3 — фіксована» — з памʼяті, офіційний PDF не відкрився.
- (?) Рік (близько 2008) і автор (Mark Engelberg) — з памʼяті, не перевірено; у шапці `year: null`.
- (?) Чи бувають у картках підказки-заборони або «порожня клітина» як обмеження — не перевірено.
- (?) Склад екранів мобільних версій — не бачив; вікна гіпотетичні.
