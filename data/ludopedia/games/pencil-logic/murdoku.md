---
title: Murdoku
slug: murdoku
aka: [Мердоку, murder mystery puzzle, Family Murdoku]
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
year: 2020
platforms: [paper, web]
links:
  - {kind: other, url: "https://allthings.how/murdoku-explained-how-the-murder-mystery-sudoku-puzzle-works/", best: true, note: "пояснення: кімнати, предмети, «beside», убивця сам на сам з жертвою, приклади підказок, правила складних справ"}
  - {kind: official, url: "https://murdoku.com/", note: "автор Manuel Garand, книжки, онлайн-версія, конкурс"}
  - {kind: play, url: "https://murdoku.com/play", note: "грати в браузері"}
  - {kind: official, url: "https://murdoku.com/print", note: "безкоштовні PDF-справи 6×6…16×16 з розвʼязками, Family Murdoku"}
  - {kind: other, url: "https://murdoku.com/pdf/car-repair-bw.pdf", note: "аркуш справи: блок правил, легенда «можна / не можна стати», підказки"}
  - {kind: other, url: "https://murdokufans.pages.dev/en/strategy/", note: "фанатський гайд: виключення рядків/стовпців, зонування за напрямком, інтерфейс з підсвіткою ключових слів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Murdoku+gameplay", note: "пошук; розвʼязання"}
stage: v1
coverage: 65
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, impassable-cells, dot-mark, hover-highlight, puzzle-select, level-bank, difficulty-levels, +relation-clues, +occupiable-objects, +one-per-line, +isolation-culprit]
proposes: ["+cond:count_in(line, kind, op, n)", "+cond:next_to", "+cond:alone_in(area)", "+cond:on_object(kind)", "+role:suspect", "+ui:clue-cards", "+ui:keyword-highlight", "+card:relation-clues", "+card:occupiable-objects", "+card:isolation-culprit"]
author: opus
date: 2026-11-09
---

# Murdoku — розстав підозрюваних по кімнатах, по одному на рядок і стовпець; убивця — той, хто сам на сам із жертвою

## Суть
Логічний пазл Manuel Garand (Монреаль, 2020; книжки з 2025): план місця злочину N×N поділено на кімнати й заставлено меблями. Гравець розставляє N людей — підозрюваних і жертву — так, щоб у кожному рядку й стовпці була рівно одна людина і справджувалась письмова підказка кожного («вона була поруч зі статуєю», «він сидів на килимі»). Коли всі на місцях, убивця — єдиний, хто опинився **наодинці з жертвою в одній зоні**. Ядро — розстановка в дусі N-ферзів / Star Battle, але обмеження задані реченнями, а не числами.

## Поле і час
- Квадратна сітка з координатами R1…RN, C1…CN; розміри справ: 6×6 (Car Repair, Family) · 7×7 · 9×9 (книжка 1) · 11×11 · 12×12 · 16×16 (Expert).
- Шари: кімнати-зони з назвами (Gallery, Garage, Waiting Area…) · клітинка-обʼєкт або підлога · людина.
- Обʼєкти на клітинках двох класів (легенда аркуша): **можна зайняти** — килим, стілець, авто; **не можна** — полиця, стіл, телевізор, рослина. Інші предмети (мольберт, статуя, картина в рамі, масляна пляма) — орієнтири для підказок; на деякі можна стати («на його клітинці була картина в рамі»).
- Великі предмети можуть займати кілька клітинок; у Volume 3 одна справа може охоплювати кілька сіток-локацій.
- Час статичний; хід = поставити людину або закреслити клітинку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка підлоги | mark | рядок, стовпець, зона | може містити одну людину |
| Кімната / зона | zone | назва; межі | «beside» і «alone» рахуються лише в межах зони |
| Займаний обʼєкт (килим, стілець, авто) | terrain | тип | людина може стояти/сидіти; підказки «on a carpet», «sitting in a chair», «in a car» |
| Блокуючий обʼєкт (полиця, стіл, ТБ, рослина) | static | тип; 1+ клітинок | людина не може зайняти; орієнтир для «beside» |
| Орієнтир (мольберт, статуя, картина, пляма) | static | тип | ціль підказок «beside» / «on» |
| Підозрюваний | piece | імʼя, стать, ініціал, підказка | ставиться на одну клітинку |
| Жертва (V) | piece | імʼя, підказка «була наодинці з убивцею» | ставиться так само, як підозрювані |
| Хрестик / закреслення | mark | — | клітинка виключена для всіх |
| Підказка | mark | речення | обмежує клітинку людини: зона, обʼєкт, рядок/стовпець, відносно іншої людини |

### Типи підказок (з аркушів і пояснення)
| Тип | Приклад |
|---|---|
| зона | «She was alone in the Waiting Area» |
| на обʼєкті | «He was on a carpet» · «He was on an oil slick» · «There was a framed painting on his square» |
| поруч з обʼєктом | «He was beside a shelf» · «She was beside an easel, directly south of it» |
| лінія | «He was in the last column» |
| відносно людини | «He was exactly one row north of Gemma» · «There was a woman alone in the Gallery one row north of her» |
| самотність | «He was alone» · «She was the only person sitting in a chair» |
| жертва | «She was alone with the murderer» |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place person, cell)` → ЯКЩО `not free(cell)` (блокуючий обʼєкт або вже зайнято) → ТО `block`.
- КОЛИ `input(place person, cell)` → ТО `place(person)`, `mark(row ∪ col, X)` — «щойно поставив — закресли весь рядок і стовпець».
- КОЛИ `input(place)` → ЯКЩО `custom: «у рядку чи стовпці вже є людина»` → ТО `constraint_broken(one_per_line)`.
- «Beside»: ЯКЩО `custom: «ціль праворуч/ліворуч/вище/нижче»` and `custom: «та сама зона»` → підказка справджена; діагональ і сусід через стіну зони — не «beside».
- «Alone»: ЯКЩО `count(person in area, ==, 1)` → підказка «alone in …» справджена; «alone with X» — у зоні рівно двоє.
- КОЛИ `custom: «підказка людини хибна при поточній розстановці»` → ТО `constraint_broken(clue)`.
- Спецправила складних справ: Zoo — `custom: «у вольєрах лише доглядачі, у кожному ≥ 1»`; Horse Track — `custom: «ahead/behind задають порядок жокеїв»`; Preppers — ящики й приховані кімнати; Solitary Confinement — ролі охоронців, порожні клітинки, кути.
- КОЛИ `all_constraints_met` (N людей, по одній у рядку/стовпці, усі підказки справджені) → ТО `custom: «знайти зону, де лише жертва + 1 людина»` → убивця, `win`.
- Перемога: назвати вбивцю (рядок «The murderer is…» на аркуші). Поразки й рахунку нема; правильність — за PDF розвʼязку.

## Керування і ввід
- Папір: вписати ініціал у клітинку, закреслити рядок і стовпець (крок з блоку правил аркуша).
- Онлайн (murdoku.com/play): розстановка підозрюваних на плані; за фан-гайдом наведення на картку підозрюваного підсвічує ключові слова підказки на полі, наведення на клітинку — назву обʼєкта (напр. Carpet).
- Порядок розвʼязання: прочитати жертву й усі підказки → поставити найобмеженіших → закреслити їхні лінії → «beside»/меблі → наприкінці знайти пару «наодинці».

## Вікна, меню, HUD
- `game-screen` (онлайн): план із кімнатами й предметами, `cell-coordinates` (R/C), `+ui:clue-cards` — картки підозрюваних з портретом-ініціалом і реченням, `+ui:keyword-highlight`, `tooltip` назви обʼєкта, поле «The murderer is…».
- `puzzle-select` — список справ із рівнем (Very Easy … Expert) і розміром; Family Murdoku окремо.
- `end-screen` (цифрова версія) — хто вбивця + покрокове пояснення, як на PDF-розвʼязку.
- `help-window` — блок правил аркуша: «One person per Row and Column», «What does beside mean?», легенда «Can be occupied / Cannot be occupied».

## Фічі поза полем
- `puzzle-bank` онлайн і PDF-справи (кольорові й ч/б) з окремими аркушами розвʼязків; нові справи — щотижня (сайт) або двічі на тиждень (стаття) (?).
- `difficulty-presets` за справою (Very Easy … Expert), Family Murdoku для дітей; переклади (`localization`, 15 мов книжки).
- Книжки: Murdoku (80 справ, 9×9), Back in Time, Around the World (багатосіткові справи), Beyond the Grave (анонс).
- Конкурс «The Treasure Hunt»; спільнота Reddit/Discord; сторінка errata.

## Варіації й родичі
- [n-queens-knights-tour](n-queens-knights-tour.md), [star-battle](star-battle.md) — «по одному на рядок/стовпець» без слів; [zebra-puzzle](zebra-puzzle.md) — підказки-речення й відношення «поруч / ліворуч».
- [tents](tents.md) — розстановка з привʼязкою до обʼєкта-орієнтира.
- Dedoku (Deduction Detective) — клон із тими ж ідеями: свідки, «стояти можна / не можна» (бачив лише в пошуку).
- Осі варіацій: **хто на полі** (лише підозрювані / + жертва / + ролі) · **кількість сіток** (одна / кілька локацій) · **фінальне питання** (хто сам на сам з жертвою / порядок / ролі) · **тип обʼєкта** (займаний / блокуючий / орієнтир).

## Цікавинки для курсу
- Розстановка N людей «по одному на лінію» з перевіркою — 📎 (як N-ферзі без діагоналей).
- Підказки як предикати над розстановкою (зона, обʼєкт, сусідство в межах зони, відносний рядок) — 🥉 (мовні шаблони → функції).
- «Beside» лише в межах зони: сусідство, обрізане межами кімнат — 📎.
- Висновок «убивця = єдиний наодинці з жертвою» як ціль після розвʼязку — 🌱.
- Генерація справи з єдиним розвʼязком і підбором підказок-речень — 👑.

## Мапа на каталог
- Є: `markup-validity` · `completion-detection` · `satisfy-constraints` · `cell-click` · `impassable-cells` (полиці, столи, рослини) · `dot-mark` (хрестики-закреслення) · `hover-highlight` (підсвітка ключових слів, назви обʼєктів) · `puzzle-select` · `level-bank` · `difficulty-levels`.
- **Нема** → пропозиції карток:
  - `+relation-clues` «Підказки-відношення словами» (повтор із zebra-puzzle).
  - `+occupiable-objects` «Обʼєкти: можна / не можна стати» · entities/legality · 🌱 · слот {kinds}.
  - `+one-per-line` «Рівно один на рядок і стовпець» · game-logic/constraints · 🌱.
  - `+isolation-culprit` «Відповідь — хто наодинці з жертвою в зоні» · game-logic/win · 🌱.

## Пропозиції до словників
- `+cond:count_in(line, kind, op, n)` — кількість сутностей у рядку/стовпці (повтор із tents).
- `+cond:next_to` — сусідство (повтор із zebra-puzzle); тут з обрізанням межею зони.
- `+cond:alone_in(area)` — у зоні рівно одна людина (або рівно двоє для «alone with»).
- `+cond:on_object(kind)` — клітинка людини містить обʼєкт виду.
- `+role:suspect` — фігура з підказкою-реченням.
- `+ui:clue-cards` — картки підказок поруч з полем; `+ui:keyword-highlight` — підсвітка на полі слів з підказки.
- `+card:relation-clues` · `+card:occupiable-objects` · `+card:isolation-culprit` — див. мапу.

## Джерела
- ⭐ [All Things How: Murdoku explained](https://allthings.how/murdoku-explained-how-the-murder-mystery-sudoku-puzzle-works/) — правила, «beside», убивця, приклади підказок, спецправила Zoo/Horse Track/Preppers/Solitary.
- [murdoku.com](https://murdoku.com/) · [About](https://murdoku.com/about) · [Books](https://murdoku.com/book) — автор, 2020, книжки (80 справ, 9×9), багатосіткові справи Vol. 3.
- [Print](https://murdoku.com/print) — справи й розміри; [Car Repair PDF](https://murdoku.com/pdf/car-repair-bw.pdf), [The Art School PDF](https://murdoku.com/pdf/the-art-school-bw.pdf) і [розвʼязок](https://murdoku.com/pdf/the-art-school-solution.pdf) — блок правил, легенда обʼєктів, хід розвʼязання.
- [Murdoku Fans: Solving guide](https://murdokufans.pages.dev/en/strategy/) — техніки й підсвітка в онлайн-версії.
- YouTube: [пошук](https://www.youtube.com/results?search_query=Murdoku+gameplay).

## Непевне
- (?) Інтерфейс murdoku.com/play (кнопки, перевірка, undo) — сторінка не віддала тексту; опис — з фан-гайду.
- (?) Частота нових справ: «щотижня» (сайт) проти «двічі на тиждень» (стаття).
- (?) Рік: концепт і перші PDF — 2020 (сторінка About), книжка — 2025; черга вказує 2025.
- (?) Чи завжди людей рівно N на сітці N×N — так на двох перевірених аркушах (6 і 9).
