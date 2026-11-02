---
title: Kara (Кара — сонечко)
slug: kara
family: program-robots
also: []
klass: avatar
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: none
  goal: state
year: 2000
platforms: [PC (Java), web (KaraWeb)]
links:
  - {kind: official, url: "https://www.swisseduc.ch/informatik/karatojava/kara/index.html", best: true, note: "Kara: сонечко, програма — скінченний автомат у графічному редакторі; посібник, завдання з розвʼязками"}
  - {kind: official, url: "https://www.swisseduc.ch/informatik/karatojava/", note: "уся родина: Kara, JavaKara, PythonKara, RubyKara, JavaScriptKara, MultiKara, TuringKara"}
  - {kind: other, url: "https://www.swisseduc.ch/informatik/karatojava/kara/screenshots.html", note: "скриншоти: редактор світу, редактор програми, сенсори, завдання"}
  - {kind: other, url: "https://www.swisseduc.ch/informatik/karatojava/turingkara/index.html", note: "TuringKara — машина Тюрінга на 2D-аркуші"}
  - {kind: other, url: "https://www.swisseduc.ch/informatik/karatojava/multikara/index.html", note: "MultiKara — до 4 сонечок, критична секція, монітор, барʼєр"}
  - {kind: other, url: "https://www.swisseduc.ch/informatik/karatojava/javakara/index.html", note: "JavaKara — той самий світ, програма на Java"}
  - {kind: play, url: "https://karaweb.classinteractives.co.uk/", note: "KaraWeb — вебверсія англійською"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=kara+marienk%C3%A4fer+endlicher+automat", note: "пошук; уроки"}
stage: v1
coverage: 75
mechanics: [move-4dir, impassable-cells, push-object, item-pickup, in-game-editor, editor-palette, editor-erase, editor-playtest, level-exchange, state-as-data, game-screen, help-window, +command-program, +sensor-predicates, +fsm-program, +transition-table, +runtime-error-stop, +step-execution, +code-editor-window, +torus-wrap, +put-item, +tape-2d-turing, +multi-agent-sync]
proposes: ["+trigger:exec(cmd)", "+trigger:program_end", "+trigger:state_enter(s)", "+cond:sensor(name)", "+cond:dont_care", "+effect:goto_state(s)", "+effect:place", "+effect:crash", "+effect:wrap", "+window:code-editor", "+window:fsm-editor", "+window:world-editor", "+window:task-list", "+ui:state-diagram", "+ui:transition-table", "+ui:sensor-selector", "+ui:instruction-highlight", "+feature:sensor-config", "+axis:control"]
author: opus
date: 2026-11-02
---

# Kara — сонечко, яким керує скінченний автомат: стан × сенсори → дії й наступний стан

## Суть
Kara — навчальне середовище SwissEduc (ETH Zürich): сонечко на клітинному світі з деревами, грибами й листочками конюшини. Програма — не текст, а **скінченний автомат**, який збирають мишкою: для кожного стану обирають сенсори, а в таблиці переходів для кожної комбінації їхніх значень задають послідовність команд і наступний стан. Задачі — «збери всі листочки», «обійди дерево», «штовхай гриб до стіни», «намалюй шаховий візерунок». Варіанти родини ведуть від автоматів до справжніх мов (JavaKara, PythonKara…), паралельності (MultiKara) і машини Тюрінга (TuringKara).

## Поле і час
- Квадратна сітка довільного розміру; клітина — порожня, дерево, гриб, листок (листок може лежати під сонечком або грибом (?)).
- Світ — тор: вихід за край переносить на протилежний (?).
- Сонечко має напрямок; сенсори відносні до напрямку (спереду/ліворуч/праворуч).
- Час `programmed`: крок = виконання однієї команди (move/turn/put/remove); автомат переходить у наступний стан після послідовності дій рядка (?).
- Повна видимість, детермінізм.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Kara (сонечко) | player | позиція, напрямок | виконує автомат: рух, поворот, кладе/забирає листок |
| Дерево | static | — | непрохідне, нерухоме |
| Гриб | object | — | штовхається на 1, якщо за ним вільно (не дерево й не гриб) |
| Листок конюшини | pickup | 0/1 на клітині | Kara стає на нього; `removeLeaf` забирає, `putLeaf` кладе (запас нескінченний) |
| Стан автомата | mark | імʼя, сенсори стану | вузол діаграми; є старт і спеціальний `stop` |
| Перехід | mark | значення сенсорів (так/ні/байдуже), дії, наступний стан | рядок таблиці переходів |
| Сенсори | mark | `treeFront`, `treeLeft`, `treeRight`, `mushroomFront`, `onLeaf` | булеві «датчики» оточення |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `state_enter(s)` → ТО зчитати сенсори, обрані для стану s.
- КОЛИ сенсори прочитано → ЯКЩО рядок таблиці стану s збігається (`sensor(x)` = так/ні; «байдуже» — будь-що) → ТО виконати дії рядка по черзі, `goto_state(next)`.
- КОЛИ `exec(move)` → ЯКЩО `cell(ahead, empty|leaf)` → ТО `move(kara, dir)`; ЯКЩО `cell(ahead, mushroom)` і `free(cell_behind_mushroom)` → ТО `push`; ЯКЩО дерево або гриб упирається → ТО `crash` («Kara не може рухатись») (?).
- КОЛИ `exec(turnLeft|turnRight)` → ТО `face(kara, ±90°)`.
- КОЛИ `exec(putLeaf)` → ЯКЩО `not occupied(here, leaf)` → ТО `place(leaf)`; інакше `crash` (?).
- КОЛИ `exec(removeLeaf)` → ЯКЩО `occupied(here, leaf)` → ТО `pickup`; інакше `crash` (?).
- КОЛИ `edge(kara)` → ТО `wrap(kara)` (тор) (?).
- КОЛИ `goto_state(stop)` → ТО `program_end`.
- КОЛИ `custom: «жоден рядок таблиці не підходить»` → ТО `crash` (?) — автомат неповний.
- Перемога: задача вважається розвʼязаною, коли світ у потрібному стані й автомат зупинився; автоперевірки нема — завдання з розвʼязками для порівняння (?) · Поразка: помилка виконання · Рахунок: нема.

## Керування і ввід
- Редактор світу: палітра (Kara, дерево, гриб, листок), клік — поставити, повторний клік/гумка — прибрати; поворот Kara; розмір світу; зберегти/відкрити світ у файл.
- Ручне керування Kara кнопками (крок, поворот, листок) — для дослідження світу перед програмуванням.
- Редактор програми (верх): діаграма станів — додати/перейменувати/видалити стан, позначити старт; вибрати сенсори стану.
- Редактор програми (низ): таблиця переходів — колонки сенсорів (✓ / ✗ / байдуже), колонка дій (перетягнути іконки команд), колонка наступного стану.
- Виконання: Play, Step, Pause, Stop, повзунок швидкості; підсвічується поточний стан і рядок.

## Вікна, меню, HUD
- `game-screen` = `world-editor`: поле світу з Kara, палітра обʼєктів, кнопки керування Kara, кнопки Play/Step/Stop, `speed-slider`.
- `fsm-editor` (`code-editor`): `state-diagram` (кружки-стани, стрілки-переходи) + `transition-table` поточного стану + `sensor-selector`.
- `task-list` (custom): вбудовані завдання з описом і світом; розвʼязки (у версії без суфікса `-x`).
- `help-window`: посібник (Bedienungsanleitung) і пояснення сенсорів.
- `confirm-dialog` / повідомлення про помилку виконання.
- Файлові діалоги: світ і програма зберігаються окремо.
- Переходи: світ ↔ редактор програми (окремі вікна поруч); завдання → завантажує світ → програмування → Play.

## Фічі поза полем
- `level-editor` (редактор світу) + `export-import` (файли світу й програми).
- `puzzle-bank`: завдання різної складності з розвʼязками; версія без розвʼязків для учнів.
- `step-mode`, `speed-control`.
- `custom-rules` (сенсорна конфігурація): у задачі можна обмежити набір сенсорів.
- Навчальні матеріали й курс «програмування на основі Kara»; нагорода European Academic Software Award 2002.

## Варіації й родичі
- **JavaKara / PythonKara / RubyKara / JavaScriptKara** — той самий світ, програма текстом (`move()`, `turnLeft()`, `treeFront()`, `onLeaf()`, `removeLeaf()` …).
- **MultiKara** — до 4 сонечок одночасно; синхронізація: критична секція, монітор, барʼєр (rendez-vous).
- **TuringKara** — машина Тюрінга на **двовимірному аркуші**: голова читає/пише символ клітини й рухається в 4 сторони; задачі від інверсії бітів і двійкового додавання до універсальної машини Тюрінга.
- GreenfootKara, GameGridKara, ScratchKara, KaraWeb.
- Родичі: Karel the Robot (процедури замість автомата), RoboZZle (умова-колір на кожній команді), Lightbot.
- Осі варіацій: **модель програми** (автомат / процедури / текст); **сенсори** (фіксовані / конфігуровані в задачі); **кількість акторів** (1 / 4 з синхронізацією); **памʼять** (лише світ / 2D-стрічка Тюрінга).

## Цікавинки для курсу
- Інтерпретатор скінченного автомата з таблицею «стан × сенсори → дії + стан» і «байдуже» — 🥈.
- Графічний редактор автомата (діаграма + таблиця) — 🥇.
- Штовхання гриба як обмеження на рух — 📎 (картка `push-object` є).
- Світ-тор — 🌱.
- TuringKara: 2D-машина Тюрінга, виконання і перевірка — 🥈.
- MultiKara: кілька акторів і барʼєр/монітор — 🥇.
- Окремі файли світу й програми (рівень ≠ розвʼязок) — 📎.

## Мапа на каталог
- Є: `move-4dir` (рух + повороти) · `impassable-cells` (дерева) · `push-object` (гриби) · `item-pickup` (листки) · `in-game-editor` + `editor-palette` + `editor-erase` + `editor-playtest` (редактор світу) · `level-exchange` (файли) · `state-as-data` · `game-screen` · `help-window`.
- **Нема** → пропозиції карток:
  - `+command-program`, `+sensor-predicates`, `+runtime-error-stop`, `+step-execution`, `+code-editor-window` — спільні з Karel.
  - `+fsm-program` «Програма як скінченний автомат» · game-logic · 🥈 · слоти {states, sensors}.
  - `+transition-table` «Таблиця переходів з “байдуже”» · interface/input · 🥉.
  - `+torus-wrap` (спільна з The Farmer Was Replaced) · entities/move · 🌱.
  - `+put-item` «Актор кладе предмет на клітину» · entities/interact · 🌱.
  - `+tape-2d-turing` «Машина Тюрінга на 2D-аркуші» · game-logic · 🥈.
  - `+multi-agent-sync` «Синхронізація кількох акторів (барʼєр, монітор)» · game-logic · 🥇.

## Пропозиції до словників
- `+trigger:exec(cmd)`, `+trigger:program_end`; `+trigger:state_enter(s)` — вхід автомата в стан.
- `+cond:sensor(name)` — булевий сенсор актора (точніший за `cell`); `+cond:dont_care` — «байдуже» в таблиці.
- `+effect:goto_state(s)` — перехід автомата; `+effect:place` — покласти предмет; `+effect:crash`; `+effect:wrap` (⏳ є).
- `+window:fsm-editor`, `+window:world-editor`, `+window:task-list`; `+window:code-editor`.
- `+ui:state-diagram`, `+ui:transition-table`, `+ui:sensor-selector`, `+ui:instruction-highlight`.
- `+feature:sensor-config` — набір доступних сенсорів як параметр задачі.
- `+axis:control` = `programmed`.

## Джерела
- ⭐ [SwissEduc: Kara](https://www.swisseduc.ch/informatik/karatojava/kara/index.html) — сонечко, скінченні автомати, графічне середовище, посібник, завдання.
- [SwissEduc: Kara → Java](https://www.swisseduc.ch/informatik/karatojava/) — уся родина, автори (Nievergelt, Hartmann, Reichert, Brändle, Schlatter), нагорода 2002.
- [Скриншоти Kara](https://www.swisseduc.ch/informatik/karatojava/kara/screenshots.html) — редактор світу («збирати листки, штовхати гриби, ходити між деревами»), редактор програми (автомат угорі, дії за сенсорами внизу).
- [TuringKara](https://www.swisseduc.ch/informatik/karatojava/turingkara/index.html) — 2D-аркуш замість стрічки, від інверсії бітів до УМТ.
- [MultiKara](https://www.swisseduc.ch/informatik/karatojava/multikara/index.html) — до 4 сонечок, критична секція, монітор, барʼєр.
- [JavaKara](https://www.swisseduc.ch/informatik/karatojava/javakara/index.html) — світ ідентичний Kara; приклад з `treeFront()`, `onLeaf()`, `move()`, `removeLeaf()`.
- [KaraWeb](https://karaweb.classinteractives.co.uk/) — «Code your ladybird».

## Непевне
- (?) Імена сенсорів `treeLeft`, `treeRight`, `mushroomFront` і команд `turnLeft`, `turnRight`, `putLeaf` — з памʼяті (на сторінках бачив лише `treeFront`, `onLeaf`, `move`, `removeLeaf`; `mushroomFront` — у саксонських матеріалах за пошуком).
- (?) Тор-світ, помилки виконання (крок у дерево, подвійний листок, «нема рядка»), автоперевірка задач — з памʼяті; посібник PDF не відкрився.
- (?) Рік першої версії (≈2000) — непевно; точно відомо лише нагороду 2002.
- (?) Символи TuringKara (0, 1, #, порожньо, стрілки) — з памʼяті.
