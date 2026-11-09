---
title: Spiral puzzle (Спіральний кросворд)
slug: spiral-puzzle
aka: [Spiral crossword, Spiral, Bull's-Eye Spiral, Спіраль, Спіральний кросворд]
family: word-number
also: []
klass: puzzle
axes:
  field: 1d
  time: static
  opponent: none
  info: hidden
  random: none
  goal: constraints
year: null
platforms: [paper, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Spiral_puzzle", best: true, note: "ланцюг клітин спіраллю, відповіді 1→100 і 100→1, мітки a-b, складність без нумерації, варіант в один бік, кольорові ряди з фінальним розвʼязком"}
  - {kind: play, url: "https://amuselabs.com/docs/puzzles/spiral/overview/", note: "PuzzleMe: mini spiral (25 клітин) і full (100), живий приклад для розвʼязування"}
  - {kind: other, url: "https://amuselabs.com/docs/puzzles/spiral/upload/", note: "формат .txt: відповідь + підказка, inward від зовнішнього кільця до центру, роздільник ---, outward назад"}
  - {kind: other, url: "https://amuselabs.com/docs/puzzles/spiral/magic-fill-for-spiral/", note: "генератор спіралей: розміри 20–25 / 95–100 літер, довжини слів 4–12, обовʼязкові слова, blocklist, оцінки"}
  - {kind: other, url: "https://www.pennydellpuzzles.com/wp-content/uploads/2026/04/Print-n-Solve-Magazines-Approved-Variety-Puzzles-AXFL-sample-puz.pdf", note: "Penny Dell: Bull's-Eye Spiral — кругла мішень на 80 клітин, Outward 1-4… і Inward 80-77…"}
  - {kind: other, url: "https://crosswordnexus.com/blog/2025/10/03/puzzle-140-crushword-spiral", note: "ребус-спіраль: inward 1→49, outward 49→1, у кожній клітині 2+ літери"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=spiral+crossword+puzzle+how+to+solve", note: "пошук; розвʼязування"}
stage: v1
coverage: 55
mechanics: [cell-click, keyboard-controls, selection-highlight, completion-detection, satisfy-constraints, game-screen, help-window, +clue-list, +inward-outward-chain, +clue-range-label, +numberless-chain, +word-chain-overlap, +rebus-cells, +hidden-message-cells, +spiral-fill-generator, +print-version]
proposes: ["+cond:chain_segment", "+cond:fits_enumeration", "+ui:clue-list", "+ui:direction-toggle", "+feature:rebus-entry", "+card:inward-outward-chain"]
author: opus
date: 2026-11-09
---

# Spiral puzzle — один ланцюг літер, згорнутий спіраллю: одні відповіді читаються від краю до центру, інші — від центру назад

## Суть
Усі клітини пазла — одна довга стрічка, згорнута в квадратну (або круглу) спіраль, у кожній клітині одна літера. Є два списки підказок: **Inward** (відповіді вписуються з клітини 1 до центру) і **Outward** (відповіді з центру назад до 1). Межі слів в обох списках різні, тож кожна клітина належить рівно одному inward- і одному outward-слову — це єдиний «перетин» у пазлі. Звичайних перетинів, як у кросворді, нема, тому пазл важчий, ніж виглядає.

## Поле і час
- Поле — **ланцюг** клітин 1…N (`field: 1d`), намальований спіраллю; сусідство лише по ланцюгу. Типові довжини: 100 (Wikipedia, PuzzleMe full), 25 (PuzzleMe mini), 80 (Penny Dell Bull's-Eye — круглі кільця), 97 і 49 (окремі видання).
- Нумерація: у клітинах стоять номери лише там, де починається якась відповідь; підказка «20-26» = відповідь із клітини 20 по 26, тобто 7 літер.
- Напрям: класика — inward від зовнішнього кільця до центру, outward — назад; у Bull's-Eye Spiral навпаки: номер 1 у центрі, Outward 1-4, 5-9… йде назовні, Inward 80-77… — усередину.
- Шари: клітина (літера / порожньо), номер, кольорове підсвічування клітин фінального розвʼязку (деякі видання).
- Часу нема.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітина ланцюга | tile | індекс 1…N, літера | приймає одну літеру (у ребус-спіралі — 2+); входить в одне inward- і одне outward-слово |
| Номер | mark | 1…N | ставиться в клітину, де починається відповідь; у «важкій» версії відсутній |
| Inward-відповідь | zone | мітка a-b (a < b), підказка | відрізок ланцюга a…b, читається за зростанням індексу |
| Outward-відповідь | zone | мітка b-a (b > a), підказка | відрізок b…a, читається за спаданням індексу |
| Підказка | static | текст, мітка | у списку Inward або Outward |
| Кольорова клітина | mark | колір / ряд | частина фінального розвʼязку, що читається горизонтально, вертикально чи по діагоналі |

## Правила (КОЛИ → ЯКЩО → ТО)
Модель і обмеження:
- КОЛИ `custom: «підказка з міткою a-b»` → ТО `custom: «довжина відповіді = |b − a| + 1; наступна відповідь того ж списку починається з клітини b+1 (або b−1 для outward)»`.
- КОЛИ `custom: «inward-відповіді вписано поспіль»` → ЯКЩО `custom: «їхня склейка 1…N = ланцюг»` and `custom: «склейка outward-відповідей N…1 = той самий ланцюг навспак»` → ТО `custom: «обидва набори узгоджені»`.
- КОЛИ `constraint_broken(клітина дає різні літери для inward і outward)` → ТО `custom: «одна з двох відповідей хибна»`.
- КОЛИ `all_constraints_met` → ЯКЩО `custom: «усі клітини заповнені й кожна відповідь пасує до своєї підказки»` → ТО `win`.
- Приклад з Wikipedia: ланцюг I M P U G N I N G I S в один бік дає IMPUGNING + IS…(ISLE), у зворотний — SIGNING UP + …MI(LE).

Ввід (цифрова версія):
- КОЛИ `input(click cell)` → ТО `custom: «виділити inward- або outward-слово, що містить клітину»`; повторний клік — `custom: «перемкнути напрям»`.
- КОЛИ `input(type letter)` → ЯКЩО `state(cell, selected)` → ТО `set_value(cell, letter)`, `custom: «курсор на сусідню клітину ланцюга за напрямом слова (+1 inward / −1 outward)»`.
- КОЛИ `input(click clue)` → ТО `custom: «виділити відрізок a…b»`.

Варіанти правил:
- Без нумерації: КОЛИ `level_start` → ЯКЩО `mode(numberless)` → ТО `custom: «межі слів не дано; їх виводять із довжин відповідей»`.
- В один бік: КОЛИ `custom: «слово i закінчилось»` → ТО `custom: «остання літера слова i = перша літера слова i+1»` (без зворотного списку — «майже вікторина»).
- Ребус-спіраль: КОЛИ `input(type)` → ТО `custom: «у клітину вписується 2+ літери»`.
- Фінальний розвʼязок: КОЛИ `all_constraints_met` → ТО `custom: «прочитати літери кольорових клітин у рядку/стовпці/діагоналі»`.
- Перемога: ланцюг заповнено й обидва набори відповідей правильні · Поразки нема · Рахунку нема (у застосунках — час (?)).

## Керування і ввід
- Папір: вписати літери ручкою; стратегія Penny Dell — застряг на outward-слові → переходь на inward.
- (цифрова версія) клік по клітині/підказці, набір з клавіатури, перемикання Inward ↔ Outward повторним кліком (?); у ребус-спіралі Crossword Nexus — Escape відкриває меню вводу кількох літер.

## Вікна, меню, HUD
- (цифрова версія) `game-screen`: спіраль клітин, два `clue-list` (Inward / Outward), `selection-highlight` поточного відрізка, номери.
- (цифрова версія) `help-window`: пояснення міток a-b і двох напрямів.
- (цифрова версія) `end-screen`: «розвʼязано» (?).
- Друк: паперова сторінка з розвʼязком на наступній сторінці (Penny Dell).

## Фічі поза полем
- Генератор (PuzzleMe Magic Fill for Spiral): розмір Small 20–25 або Large 95–100 літер, словники + власний blocklist, мінімальна оцінка слова й сітки, обовʼязкові слова, довжини слів 4–12 за замовчуванням; видає кілька кандидатів «чипами» inward/outward, їх можна позначати зірочкою й фільтрувати.
- Імпорт: `.txt` — рядок відповіді + рядок підказки, inward-блок, `---`, outward-блок.
- Перевірка / розкриття в онлайн-розвʼязувачі — (?).

## Варіації й родичі
- **Bull's-Eye Spiral** (Penny Dell) — кругла мішень, нумерація від центру.
- **Ребус-спіраль** (Crossword Nexus «Crushword») — кілька літер у клітині.
- **Однонапрямна спіраль** — слова через спільну літеру (word chain); родич Dropquote (`dropquote.md`) і Acrostic (`acrostic.md`) за «прочитай фінальне повідомлення».
- Rows Garden / Marching Bands — інші «варіетні» сітки з двома наборами відповідей (?).
- Не плутати з механічними спіральними головоломками (jigsaw-спіраль, 3D-спіраль, що розбирається) — Wikipedia згадує їх у тій самій статті.
- **Осі варіацій:** форма (квадратна / кругла спіраль) · нумерація (є / нема) · напрям (двосторонній / один бік з перекриттям літери) · вміст клітини (1 літера / ребус) · фінальний меседж (нема / кольорові ряди).

## Цікавинки для курсу
- Модель ланцюга: два розбиття одного рядка на відрізки, перевірка «inward-склейка == reverse(outward-склейка)» — 🌱.
- Малювання квадратної спіралі з N клітин (координати клітини i) і круглої мішені — 📎.
- Ввід зі зміною напряму курсора (+1 / −1) і підсвіткою відрізка — 📎.
- Помічник: за довжинами з міток і вписаними літерами — кандидати зі словника для обох напрямів — 🥉.
- Генератор спіралі (Magic Fill): пошук ланцюга, що розбивається на слова з обох кінців, з backtracking і оцінкою слів — 🥇.
- Варіант без нумерації: вивести межі слів перебором довжин — 🥈.

## Мапа на каталог
- Є: `cell-click` + `keyboard-controls` ↔ ввід; `selection-highlight` ↔ поточний відрізок; `completion-detection` + `satisfy-constraints` ↔ перевірка обох наборів; `game-screen`, `help-window`.
- **Нема** → пропозиції карток:
  - `+inward-outward-chain` «Ланцюг, що читається в обидва боки двома наборами слів» · game-logic/constraints · 📎.
  - `+clue-range-label` «Підказка з міткою клітин a-b замість номера й напрямку» · interface/hud · 🌱.
  - `+numberless-chain` «Межі слів не дано» · game-logic/constraints · 🥈.
  - `+word-chain-overlap` «Остання літера = перша наступного» · game-logic/constraints · 🌱.
  - `+rebus-cells` «Кілька літер у клітині» · interface/input · 📎.
  - `+hidden-message-cells` «Кольорові клітини складають фінальну фразу» · game-logic/win · 🌱.
  - `+spiral-fill-generator` «Генерація спіралі зі словника» · levels/generation · 🥇.
  - `+clue-list`, `+print-version` — уже пропоновані іншими файлами сімʼї.

## Пропозиції до словників
- `+cond:chain_segment` — відрізок a…b ланцюга (у заданому напрямі) збігається з відповіддю (Spiral; також Dropquote).
- `+cond:fits_enumeration` — довжина відповіді з мітки/enumeration (уже з `cryptic-crossword.md`).
- `+ui:clue-list` — списки Inward/Outward.
- `+ui:direction-toggle` — перемикач напряму вводу (Inward/Outward, Across/Down).
- `+feature:rebus-entry` — кілька літер у клітині.
- `+card:inward-outward-chain` — механіка, якої в каталозі нема.

## Джерела
- ⭐ [Wikipedia: Spiral puzzle](https://en.wikipedia.org/wiki/Spiral_puzzle) — будова (1→100 і 100→1), мітки 20-26, приклад IMPUGNING / SIGNING UP, складність без нумерації, однонапрямний варіант, кольорові ряди, механічні «спіральні» пазли.
- [PuzzleMe: Spiral overview](https://amuselabs.com/docs/puzzles/spiral/overview/) — mini 25 / full 100, живий приклад.
- [PuzzleMe: Spiral upload](https://amuselabs.com/docs/puzzles/spiral/upload/) — inward від зовнішнього кільця до центру, outward назад, роздільник `---`.
- [PuzzleMe: Magic Fill for Spiral](https://amuselabs.com/docs/puzzles/spiral/magic-fill-for-spiral/) — параметри генератора.
- [Penny Dell: Bull's-Eye Spiral (PDF-зразок)](https://www.pennydellpuzzles.com/wp-content/uploads/2026/04/Print-n-Solve-Magazines-Approved-Variety-Puzzles-AXFL-sample-puz.pdf) — кругла версія на 80 клітин, інструкція «працюй в обидва боки».
- [Crossword Nexus: Crushword Spiral](https://crosswordnexus.com/blog/2025/10/03/puzzle-140-crushword-spiral) — ребус-спіраль 1→49.
- Пошук (WebSearch): за описами видань, кожна відповідь закінчується в клітині перед номером наступної, inward за годинниковою стрілкою, outward — проти, кожна клітина використовується двічі.

## Непевне
- (?) Напрям обходу (за / проти годинникової стрілки) і де стоїть клітина 1 (зовні чи в центрі) — залежить від видання; «за годинниковою» бачив лише в описі пошуку.
- (?) Як онлайн-розвʼязувачі перемикають напрям, чи мають check/reveal — не бачив.
- (?) Rows Garden / Marching Bands як родичі — з памʼяті, не перевірено.
- (?) Рік появи і перші видання — Wikipedia посилається на NYT (2017, Will Shortz) і Games World of Puzzles (2016), але не дає історії.
