---
title: A Little to the Left
slug: a-little-to-the-left
aka: [ALTTL, Трохи лівіше]
family: build-sim
also: [thinky]
klass: cursor
axes:
  field: free
  time: static
  opponent: none
  info: hidden
  random: none
  goal: constraints
year: 2022
platforms: [PC, macOS, Switch, PS4, PS5, Xbox One, Xbox Series, Android]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1629520/", best: true, note: "100+ пазлів, кілька розвʼязків, регульовані підказки, кіт, Daily Tidy, Let It Be, DLC"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/A_Little_to_the_Left", note: "drag-n-drop прибирання, зірки (неповні на багаторозвʼязкових), GMTK Jam 2020, дати"}
  - {kind: other, url: "https://www.siliconera.com/review-a-little-to-the-left-can-be-an-obtuse-puzzle-game/", note: "огляд: дзвіночок «можливо правильно», кіт, підказки-малюнки, сміття за край екрана, порядок розділів"}
  - {kind: other, url: "https://www.cgmagonline.com/review/a-little-to-the-left-pc-review/", note: "огляд (бачив у пошуку): підказка — закреслений розвʼязок, який стираєш гумкою"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=a+little+to+the+left+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [drag-drop-piece, hover-highlight, completion-detection, satisfy-constraints, skip-level, daily-puzzle, sequential-levels, level-select, sound-effects, +hidden-order-rule, +multi-solution-stars, +near-correct-chime, +eraser-hint, +disruptor-cat, +drag-offscreen-discard, +snap-tolerance, +wordless-ui]
proposes: ["+trigger:arrangement", "+cond:sorted_by", "+cond:aligned", "+cond:allowed_spot", "+effect:sweep", "+ui:star-slots", "+ui:hint-eraser", "+window:hint-page", "+feature:let-it-be", "+feature:solution-stars", "+card:hidden-order-rule", "+card:multi-solution-stars"]
author: opus
date: 2026-11-09
---

# A Little to the Left — розклади речі «як треба», не знаючи правила: перевіряльник приймає кілька порядків, а кіт усе змітає

## Суть
Пазли-прибирання: на кожному екрані невпорядкований набір домашніх речей (олівці, рамки, ящики, наліпки), треба перетягнути їх у «правильний» стан — посортувати за розміром, згрупувати, вирівняти, скласти за візерунком. Правило **не пояснюється**: гра без тексту, гравець вгадує, що «правильно», а перевіряльник сам помічає, коли стан задовольняє одне з кількох прийнятих правил. Частина пазлів має 2–3 розвʼязки — за кожен окрема зірка; повернутись і знайти решту — окрема мета. Ядро для курсу — **перевірка невідомого правила з кількома розвʼязками** і «допуск» для неточного розміщення.

## Поле і час
- Вид згори на поверхню (стіл, шухляда, полиця), речі мають вільні координати й форму (`field: free`); часто є «гнізда» — комірки ящика, контур, де річ має стати.
- Часу нема: без таймерів, рахунку й штрафів; пазл статичний, доки не зайде кіт.
- Кожен рівень — окремий екран; рівні згруповані в розділи, проходяться по порядку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Річ (олівець, рамка, книжка…) | object | розмір, колір, орієнтація, тип | перетягується; іноді обертається (?) |
| Гніздо / комірка (ячейка коробки, контур) | zone | форма | приймає річ, у якої форма/місце збігається |
| Ціль-правило | mark | набір прийнятних станів | приховане; задоволене → зірка |
| Сміття (стружка, папірці) | object | — | рухоме; прибирається перетягуванням за край екрана |
| Кіт | enemy | лише в частині рівнів | змітає розкладене; часом відкриває сховане (марка під стосом) |
| Прихована річ | object | — | лежить під іншими, відкривається, коли їх зсунути |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag item)` → ТО `move(item, to)` (вільне переміщення).
- КОЛИ `input(drop item)` → ЯКЩО `custom: «річ близько до прийнятного місця/порядку»` → ТО `sound(chime)` — тихий сигнал «можливо, правильно».
- КОЛИ `input(drop item)` → ЯКЩО `custom: «відхилення в межах допуску»` → ТО `custom: «зараховано»`; інакше (точні пазли) — не зараховано.
- КОЛИ `input(drag clutter off-screen)` → ТО `disappear(clutter)`.
- КОЛИ `all_constraints_met` → ТО `custom: «зірка за цей варіант розвʼязку»` → `win` (рівень пройдено).
- КОЛИ `all_constraints_met` → ЯКЩО `custom: «у рівня кілька розвʼязків»` → ТО `custom: «зірка частково заповнена; інші варіанти можна знайти, переграючи»`.
- КОЛИ `custom: «на рівні є кіт»` → ТО `custom: «кіт приходить і змітає речі»` → `custom: «розкладене зіпсовано; іноді відкрито сховану річ»`.
- КОЛИ `input(hint)` → ТО `window(hint-page)`: `custom: «малюнок-розвʼязок під каракулями; стираєш гумкою, скільки треба»`.
- КОЛИ `input(Let it be)` → ТО `next_level` без штрафу.
- Типи прихованих правил (зі спостережень оглядів): сортування за розміром / кольором, групування «що до чого», вирівнювання по лінії, візерунок, заповнення гнізд формами.
- Перемога: стан задовольняє одне з прийнятних правил · Поразки нема · Рахунок — зірки за знайдені варіанти.

## Керування і ввід
- Миша/тач/геймпад: drag-n-drop речі; можливо, обертання (?).
- Кнопки меню: підказка, Let it be (пропуск), вихід до вибору рівня.
- Без тексту в інтерфейсі.

## Вікна, меню, HUD
- `main-menu`: Грати → `level-select` (розділи з рівнями та зірками), Daily Tidy, Налаштування, Вихід (?).
- `game-screen`: поверхня з речами; HUD — мінімум (кнопки меню).
- `+window:hint-page` — аркуш із закресленим розвʼязком і гумкою (`+ui:hint-eraser`).
- `daily-window` — Daily Tidy Delivery: новий пазл щодня, варіації улюблених пазлів.
- `end-screen` рівня — зірки (`+ui:star-slots`, по слоту на розвʼязок).
- `settings-window` — гучність (сигнал важливий для гри), керування (?).

## Фічі поза полем
- `levels-sequential` — розділи по порядку (далі не перескочиш, навіть із пропуском).
- `skip-level` ≈ `+feature:let-it-be` (без ліміту, без штрафу).
- `hint` — регульована (стерти мало чи багато); `+feature:solution-stars` — переграти рівень заради інших розвʼязків.
- `daily-puzzle` (Daily Tidy Delivery).
- DLC: Cupboards & Drawers (27.06.2023, організація дому), Seeing Stars.
- Без таймерів, рахунку, штрафів; без тексту.

## Варіації й родичі
- Unpacking (`unpacking.md`) — правило місця явне й одне; тут — приховане й кілька.
- Wilmot's Warehouse (`wilmots-warehouse.md`) — правило розкладу вигадує гравець, гра не перевіряє.
- Thinky-гілка «вгадай правило» (Baba Is You, Stephen's Sausage Roll — інше ядро).
- Осі варіацій: **правило** (явне / приховане / вигадане гравцем) · **кількість розвʼязків** (1 / кілька зі зірками) · **допуск** (точне гніздо / наближення / порядок без координат) · **збурення** (нема / кіт).

## Цікавинки для курсу
- Перевіряльник «чи список речей посортовано за ключем» з кількома ключами (розмір ↑, ↓, колір) — 🌱.
- Кілька прийнятних розвʼязків + зірка за кожен знайдений, збережено між сесіями — 📎.
- Допуск для неточного розміщення (вирівнювання з похибкою ε, кутом) — 📎.
- Підказка-гумка: зображення розвʼязку під шаром каракуль, стирання маскою — 🥉.
- Кіт-збурювач: подія, що зсуває речі випадково, і відкриття схованої — 📎.
- Daily: пазл дня як варіація шаблону з фіксованим seed — 🥉.

## Мапа на каталог
- Є: `drag-drop-piece` · `hover-highlight` · `completion-detection` + `satisfy-constraints` · `skip-level` (Let it be) · `daily-puzzle` · `sequential-levels` + `level-select` · `sound-effects` (дзвіночок як підказка).
- **Нема** → пропозиції карток:
  - `+hidden-order-rule` «Приховане правило порядку» · game-logic/constraints · 📎 · слоти {keys} — перевірка «посортовано за одним із ключів».
  - `+multi-solution-stars` «Зірка за кожен розвʼязок» · game-logic/win · 📎.
  - `+near-correct-chime` «Сигнал близькості» · interface/sound · 🌱.
  - `+eraser-hint` «Підказка-гумка» · interface/hud · 🥉.
  - `+disruptor-cat` «Збурювач стану» · entities · 📎.
  - `+drag-offscreen-discard` «Викинути за край» · interface/input · 🌱.
  - `+snap-tolerance` «Допуск розміщення» · entities/legality · 📎.
  - `+wordless-ui` «Інтерфейс без тексту» · interface · 🌱.

## Пропозиції до словників
- `+trigger:arrangement` — розклад речей змінився й набув одного з прийнятних станів (точніше за `all_constraints_met` для кількох розвʼязків).
- `+cond:sorted_by` — набір посортовано за ключем (розмір, колір, кількість).
- `+cond:aligned` — речі на одній лінії з допуском.
- `+cond:allowed_spot` — річ у дозволеній зоні (також Unpacking).
- `+effect:sweep` — подія розкидає/зсуває речі (кіт).
- `+ui:star-slots` — слоти зірок по кількості розвʼязків; `+ui:hint-eraser` — стирання маски підказки.
- `+window:hint-page` — сторінка з візуальною підказкою.
- `+feature:let-it-be` — пропуск без ліміту й штрафу; `+feature:solution-stars` — пошук альтернативних розвʼязків.
- `+card:hidden-order-rule`, `+card:multi-solution-stars` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam](https://store.steampowered.com/app/1629520/) — «Over 100 unique logical puzzles», кілька розвʼязків, регульовані підказки, кіт, Daily Tidy Delivery, Let It Be, DLC.
- [Wikipedia](https://en.wikipedia.org/wiki/A_Little_to_the_Left) — drag-and-drop прибирання, зірки (частково заповнені для багаторозвʼязкових), Let it Be після статті RPS, GMTK Jam 2020, Max Inferno, дати.
- [Siliconera, огляд](https://www.siliconera.com/review-a-little-to-the-left-can-be-an-obtuse-puzzle-game/) — дзвіночок, точні пазли, кіт відкриває сховане, сміття за край, розділи по порядку, без тексту.
- [CGMagazine, огляд](https://www.cgmagonline.com/review/a-little-to-the-left-pc-review/) — підказка-гумка (з пошукового фрагмента; сторінку не відкривав).

## Непевне
- (?) Кількість пазлів: Steam — «100+» (з DLC/Daily?), огляд — «75+»; кількість розділів — 4 чи 5.
- (?) Обертання речей і точний механізм «допуску».
- (?) Пункти головного меню й налаштувань — не перевірено.
- (?) Чи кіт — випадкова подія, чи скриптова в конкретних рівнях («у деяких рівнях» — з огляду).
