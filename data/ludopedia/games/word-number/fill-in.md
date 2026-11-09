---
title: Fill-In (Kriss Kross, Word Fit)
slug: fill-in
aka: [Kriss Kross, Criss Cross, Word Fit, Fill-It-In, Word Fill-In, Skeleton, Kreuzgitter, кросворд-скелет]
family: word-number
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
platforms: [paper (журнали головоломок), mobile (Astraware Kriss Kross), web (AmuseLabs)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Fill-In_(puzzle)", best: true, note: "правила, список за довжиною й алфавітом, стартове слово, стратегія спроб, варіанти (cross numbers, diagramless, відома група слів)"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Kriss_Kross", note: "сторінка-неоднозначність: Kriss Kross — варіація Fill-In"}
  - {kind: other, url: "https://astraware.freshdesk.com/support/solutions/articles/1000226159-how-to-play-kriss-kross", note: "цифрова версія: drag слова на прогалину, конфлікт червоним, вибивання слова, складності, daily 17×17, Weekender 21×21, штрафи"}
  - {kind: other, url: "https://astraware.freshdesk.com/support/solutions/articles/1000226161-kriss-kross-extra-features", note: "тап по слову підсвічує місця; тап по прогалині гортає список; слоти незавершених ігор; годинник; опції"}
  - {kind: other, url: "https://amuselabs.com/docs/puzzles/krisskross/overview/", note: "веб-конструктор: кожне слово рівно раз, усі слоти заповнені, Check / Reveal вмикає автор"}
  - {kind: other, url: "https://apps.apple.com/app/id592693877", note: "Astraware Kriss Kross (iOS) — з результатів пошуку, сторінку не відкривав"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=kriss+kross+fill+in+puzzle+how+to+solve", note: "пошук; розвʼязування"}
stage: v1
coverage: 65
mechanics: [drag-drop-piece, cell-click, legal-move-highlight, conflict-highlight, markup-validity, satisfy-constraints, completion-detection, difficulty-levels, daily-puzzle, leaderboard, save-multi-slot, game-pause, unique-puzzle-generation, level-solver, sound-warnings, particles, game-screen, help-window, about-window, settings-window, +word-list-checkoff, +entry-run-detection, +skeleton-fill, +knock-out-replace, +incidental-entry, +hint-penalty, +clock-toggle]
proposes: ["+cond:in_list", "+cond:length_fits", "+trigger:slot_filled", "+effect:return_to_list", "+ui:fill-list", "+feature:hint-penalty", "+feature:clock-toggle", "+card:skeleton-fill", "+card:knock-out-replace", "+card:incidental-entry"]
author: opus
date: 2026-11-09
---

# Fill-In — кросворд без визначень: дано список слів за довжиною, впиши всі в скелет так, щоб зійшлися перетини

## Суть
Дано сітку-скелет (білі й чорні клітини, як у кросворді) і список слів, згрупований за кількістю літер, усередині групи — за алфавітом. Треба вписати всі слова, кожне рівно раз, так, щоб літери на перетинах збіглися. Визначень нема: уся інформація — довжини слотів і спільні літери. Часто одне слово вже вписане як точка входу. Числовий двійник цієї ж механіки — [nansuke.md](nansuke.md); тут — словесна класика журналів головоломок і її цифрова версія Kriss Kross (Astraware).

## Поле і час
- Прямокутна сітка: слот = максимальний відрізок білих клітин уздовж рядка (→) або стовпця (↓); перетин — спільна клітина двох слотів.
- Поза полем — список слів, згрупований за довжиною; у цифровій версії список гортається вбік і показує групу, що відповідає вибраній прогалині.
- Статичний пазл без ходів-тіків; розвʼязок має бути єдиний (AmuseLabs: тісно переплетена сітка).
- Розміри (цифрова версія Astraware): щоденні — 17×17, щотижневий Weekender — 21×21; паперові — довільні.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Біла клітина | terrain | порожня / літера | приймає одну літеру, спільну для обох слотів, що через неї проходять |
| Чорна клітина | static | — | розділяє слоти, нічого не приймає |
| Слот | zone | довжина, напрям → / ↓, перетини | має прийняти рівно одне слово тієї ж довжини |
| Слово списку | supply | літери, довжина, вписане / ні | ставиться в слот один раз; вписане викреслюється зі списку |
| Група довжини | zone | довжина n, слова за алфавітом | звужує кандидатів слота до слів довжини n |
| Стартове слово | static | позиція | уже вписане на старті (легкі пазли), дає перші літери перетинів |
| Літера | mark | символ | належить двом словам на перетині; конфлікт — різні літери в одній клітині |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «показати скелет і список слів, згрупований за довжиною, далі за алфавітом»`.
- КОЛИ `level_start` → ЯКЩО `difficulty(easy)` → ТО `custom: «одне слово списку вже вписане як стартове»`.
- Слот: `custom: «кожен максимальний відрізок білих клітин уздовж рядка чи стовпця — один запис»`.
- КОЛИ `input(tap word)` → ТО `custom: «підсвітити всі прогалини довжини слова»` (цифрова версія).
- КОЛИ `input(tap slot)` → ТО `custom: «прокрутити список до групи цієї довжини»` (цифрова версія).
- КОЛИ `input(drag word, slot)` → ЯКЩО `custom: «довжина слова = довжина слота»` → ТО `place(word, slot)`, `custom: «слово примагнічується до прогалини»`; інакше `block`.
- КОЛИ `input(drag word, slot)` → ЯКЩО `occupied(slot, word)` → ТО `custom: «старе слово вибивається й повертається до списку»`, `place(word, slot)`.
- КОЛИ `input(drag word, slot)` → ЯКЩО `custom: «літера на перетині не збігається з уже вписаним перехресним словом»` → ТО `sound(warning)`, `custom: «перехресне слово червоніє»`.
- КОЛИ `input(drop word)` → ЯКЩО `custom: «є конфлікт перетинів»` → ТО `place(word, slot)`, `custom: «усі конфліктні слова повертаються до списку; штрафу нема»`.
- КОЛИ `input(drag word off grid)` → ТО `custom: «слово знімається з сітки й повертається до списку»`.
- Папір: КОЛИ `input(write word)` → ТО `mark(cells, letters)`, `custom: «викреслити слово в списку»`.
- КОЛИ `after(mark)` → ЯКЩО `custom: «перехресний слот заповнився цілком літерами перетинів»` → ТО `custom: «це слово теж вписане — викреслити його, інакше лишиться зайве слово»` (пастка з трилітерними словами).
- КОЛИ `input(hint)` → ТО `reveal(one cell)`, `timer(+penalty)` (цифрова версія).
- Обмеження: `cover_all(white cells)` і `custom: «кожне слово списку вписане рівно один раз»`.
- КОЛИ `all_constraints_met` → ТО `win`, `window(end-screen)`.
- Daily: КОЛИ `all_constraints_met` → ЯКЩО `mode(daily)` → ТО `timer(stop)`, `custom: «час + штрафи за підказки й незавершені слова → місце в рейтингу»`.
- Перемога: усі слова вписані без конфліктів · Поразка: нема · Рахунок: на папері нема; у daily — час зі штрафами.

## Керування і ввід
- Папір: вписати слово олівцем, викреслити його в списку; на сумнівних місцях — пробне вписування і відкат (рекомендована тактика спроб і помилок).
- Цифрова версія (Astraware): drag слова зі списку на прогалину; тап по слову — підсвітка місць, де воно може стати; тап по прогалині — список стрибає до слів цієї довжини; drag із сітки на список — зняти слово; свайп по списку — гортання.
- Веб (AmuseLabs): адаптивний інтерфейс з екранною клавіатурою на малих екранах; кнопки Check і Reveal — якщо автор пазла їх увімкнув.

## Вікна, меню, HUD
- `main-menu` (титульний екран Astraware): слоти незавершених ігор — продовжити / почати нову / видалити (з показом повного розвʼязку перед видаленням); `?` → `about-window`.
- `save-slots`: обмежена кількість ігор у процесі; щоб почати нову, треба завершити або видалити стару.
- `game-screen`: сітка, `fill-list` (список за довжиною з гортанням), `legal-move-highlight` (куди стане вибране слово), `conflict-highlight` (червоне перехресне слово), годинник у правому верхньому куті (час доби ↔ час гри з підказками), `hint-button`.
- `settings-window` (внизу `about-window`): моноширинний шрифт, ефекти частинок, показ годинника, бокове гортання списку.
- `difficulty-select`: Easy (стартове слово) / Medium (є слово з єдиною прогалиною своєї довжини) / Hard (нема очевидних входів, рідші слова).
- `daily-window`: щоденні пазли однакові для всіх (потрібна мережа), Weekender по пʼятницях; після розвʼязання — надіслати час і побачити місце (`leaderboard`).
- `end-screen`: розвʼязано + час.
- Переходи: титульний → `game-screen` (нова / продовжити) → `end-screen`; `game-screen` → пауза → титульний.

## Фічі поза полем
- `difficulty-presets` — Easy / Medium / Hard за наявністю «входу».
- `daily-puzzle` + `leaderboard-online` — однаковий пазл для всіх, рейтинг за часом.
- `hint` з `hint-penalty`: підказка відкриває одну літеру, додає час.
- `save-slots`, `pause`, `show-solution` (лише при видаленні гри).
- Веб-конструктор: автор вмикає/вимикає `auto-check` і reveal, задає тематичний список; мультиплеєр показує, хто знайшов яке слово.

## Варіації й родичі
- **Cross numbers / числовий Fill-In** — замість слів числа, вирази, роки; японська форма — [nansuke.md](nansuke.md).
- **Diagramless** — сітка на старті порожня (форму скелета теж треба вивести) (?).
- **Відома група слів** — списку нема, слова з відомої множини (напр. 50 штатів США).
- Родичі корпусу: [codeword.md](codeword.md) (кросворд без визначень, але з шифром), [knotwords.md](knotwords.md) (літери регіонів замість списку), [word-search.md](word-search.md) (список слів, які треба знайти, а не вписати), [dropquote.md](dropquote.md), [cryptic-crossword.md](cryptic-crossword.md) і [arrowword.md](arrowword.md) (кросворди з визначеннями), [crossmath.md](crossmath.md).
- **Осі варіацій:** що вписується (слова / числа / вирази) · підказка (список / визначення / нічого) · вхід (стартове слово / слово з унікальною довжиною / нема) · сітка (дана / diagramless) · список (за довжиною / суцільний / тематичний / відомий набір).

## Цікавинки для курсу
- Виділення слотів з маски сітки (максимальні відрізки по рядках і стовпцях) + індекс «довжина → слоти» — 🌱.
- Drag-n-drop слова з примагнічуванням, перевіркою перетинів, вибиванням старого слова і поверненням конфліктних до списку — 📎.
- Детектор «випадково заповненого» перехресного слота (усі клітини вже мають літери) з автоматичним викресленням — 🌱.
- Розвʼязувач: CSP з бектрекінгом, спочатку найбільш обмежений слот (унікальна довжина, найбільше відомих літер) — 🥉.
- Генератор: заповнити скелет словами словника так, щоб розвʼязок був єдиний, і оцінити складність за наявністю «входів» — 🥇.
- Daily-рейтинг за часом зі штрафами за підказки й незавершені слова — 📎.

## Мапа на каталог
- Є: `drag-drop-piece` ↔ перетягнути слово на прогалину · `cell-click` ↔ тап по прогалині · `legal-move-highlight` ↔ підсвітка місць для слова · `conflict-highlight` + `markup-validity` ↔ червоне конфліктне слово · `satisfy-constraints` + `completion-detection` ↔ усі слова вписані · `difficulty-levels` · `daily-puzzle` · `leaderboard` · `save-multi-slot` ↔ кілька ігор у процесі · `game-pause` · `unique-puzzle-generation` · `level-solver` · `sound-warnings` ↔ звук конфлікту · `particles` · `game-screen` · `help-window` · `about-window` · `settings-window`.
- **Нема** → пропозиції карток:
  - `+skeleton-fill` «Вписати всі елементи списку в скелет за довжинами й перетинами» · game-logic/constraints · 🌱 · слоти {items: words|numbers} — узагальнює `+number-list-fill` з nansuke.
  - `+word-list-checkoff` (є в корпусі, word-search) — список, що викреслюється.
  - `+entry-run-detection` (є в корпусі, nansuke) — записи як максимальні відрізки.
  - `+knock-out-replace` «Нове слово вибиває старе й конфліктні назад у список» · interface/input · 🌱.
  - `+incidental-entry` «Запис, заповнений перетинами, зараховується сам» · game-logic/constraints · 🌱.
  - `+hint-penalty` (є в корпусі) — підказка додає час.
  - `+clock-toggle` «Годинник: час доби ↔ час гри» · interface/hud · 🌱.

## Пропозиції до словників
- `+cond:in_list` — слово є у списку й ще не використане (Fill-In, Nansuke, Word Search).
- `+cond:length_fits` — довжина елемента = довжина слота (Fill-In, Nansuke, Scrabble-подібні).
- `+trigger:slot_filled` — запис став повністю заповненим, навіть без прямого вписування.
- `+effect:return_to_list` — елемент знімається з поля й повертається в запас/список.
- `+ui:fill-list` — список для вписування з групами й викресленням.
- `+feature:hint-penalty` — підказка штрафує час/очки; `+feature:clock-toggle`.
- `+card:skeleton-fill`, `+card:knock-out-replace`, `+card:incidental-entry`.

## Джерела
- ⭐ [Wikipedia: Fill-In (puzzle)](https://en.wikipedia.org/wiki/Fill-In_(puzzle)) — правила, порядок списку (довжина → алфавіт), стартове слово, тактика спроб, пастка «зайвих слів», варіанти cross numbers / diagramless / відома група.
- [Wikipedia: Kriss Kross](https://en.wikipedia.org/wiki/Kriss_Kross) — неоднозначність: Kriss Kross як варіація Fill-In.
- [Astraware: How to play Kriss Kross](https://astraware.freshdesk.com/support/solutions/articles/1000226159-how-to-play-kriss-kross) — drag, примагнічування, конфлікти червоним, вибивання, складності Easy/Medium/Hard, daily 17×17, Weekender 21×21, штрафи.
- [Astraware: Kriss Kross extra features](https://astraware.freshdesk.com/support/solutions/articles/1000226161-kriss-kross-extra-features) — підсвітка місць, гортання списку, слоти ігор, годинник, опції.
- [AmuseLabs: Kriss Kross overview](https://amuselabs.com/docs/puzzles/krisskross/overview/) — кожне слово рівно раз, усі слоти заповнені, Check/Reveal, групування за довжиною чи темою.
- YouTube: пошук «kriss kross fill in puzzle how to solve».

## Непевне
- (?) Diagramless-варіант: Wikipedia каже лише «сітка на старті порожня»; чи треба виводити й чорні клітини — не перевірено.
- (?) Мінімальна довжина слота (2 чи 3 літери) у журнальних Fill-In — джерела не називають.
- (?) Вікно `end-screen` і окреме вікно daily в Astraware — з опису функцій, не з побаченого інтерфейсу; кількість щоденних пазлів (згадано «другий… третій і четвертий») — точно не названа.
- (?) Рік появи жанру невідомий; назви Skeleton / Kreuzgitter — з сусіднього файла nansuke, не з відкритого джерела.
