---
title: Goishi Hiroi (Збирання каменів го)
slug: goishi-hiroi
aka: [碁石拾い, 碁石ひろい, Hiroimono, ひろいもの, 拾い物, Rock Collection, Goishi]
family: pencil-logic
also: []
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: collect
year: 1727
platforms: [paper, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Goishi_Hiroi", best: true, note: "правила, історія (бар-парі XIV ст., книга 1727), NP-повнота, розібраний приклад"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/碁石拾い", note: "правила JA, Wakoku Chie Kurabe 1727 і Kanja Otogi Zōshi 1743, перша назва ひろいもの"}
  - {kind: official, url: "https://www.nikoli.co.jp/ja/puzzles/goishi_hiroi/", note: "Nikoli: 4 правила, приклад і розвʼязок"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/goishi.js", note: "puzz.link: правила EN/JA, коди помилок, тести вводу кліками"}
  - {kind: play, url: "https://puzz.link/rules.html?goishi", note: "puzz.link: сторінка правил і вхід у плеєр/редактор"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Hiroimono/index.htm", note: "Janko: 30 пазлів 5×5…12×12, назви, WPC 1999, варіант «чорний-білий»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Goishi+Hiroi+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 70
mechanics: [cell-click, collect-all, no-reverse-turn, no-moves-left, completion-detection, satisfy-constraints, remaining-counter, undo-redo, in-game-editor, import-open-formats, level-bank, level-solver, unique-puzzle-generation, +nearest-in-direction-move, +hamiltonian-path-check, +alternating-color-order]
proposes: ["+effect:find_nearest", "+cond:passed_over", "+card:nearest-in-direction-move", "+card:hamiltonian-path-check", "+card:alternating-color-order"]
author: opus
date: 2026-11-09
---

# Goishi Hiroi — збери всі камені го одним ланцюгом: щоразу до найближчого по лінії, повертати можна лише на камені й ніколи назад

## Суть
На перетинах дошки го лежать камені. Гравець починає з будь-якого каменя і рухається по лініях дошки вертикально чи горизонтально: дійшовши до каменя, мусить його підняти, і лише там може повернути на 90° або йти далі прямо, але не назад. Мета — підняти всі камені. По суті це гамільтонів шлях у графі «камінь → найближчий камінь у кожному з 4 напрямків», де граф змінюється: піднятий камінь зникає, і його сусіди «бачать» далі.

## Поле і час
- Решітка дошки го: камені на перетинах ліній (puzz.link малює клітинками); банк Janko — від 5×5 до 12×12.
- Стан: множина каменів, що лишились · поточний камінь · напрямок, яким до нього прийшли.
- Крок — від поточного каменя до найближчого каменя в обраному напрямку; порожні перетини й місця вже знятих каменів проходяться наскрізь.
- Час статичний; хід = наступний номер у ланцюжку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Камінь | pickup | номер підняття k | обовʼязково піднімається, щойно шлях до нього доходить; потім зникає |
| Перший камінь | pickup | k = 1 | будь-який (у варіанті — заданий) |
| Порожній перетин | terrain | — | шлях іде крізь прямо; повернути тут не можна |
| Місце знятого каменя | terrain | — | як порожній: прохід крізь, без повороту (Nikoli, правило 4) |
| Шлях (поточна позиція) | player | камінь, напрямок приходу | наступний камінь — найближчий у напрямку «прямо, ліворуч, праворуч» |
| Межа дошки | static | — | у напрямку без каменів до краю ходу нема |
| Камінь (варіант «чорний-білий») | pickup | колір | кольори мають чергуватись |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, stone)` → ЯКЩО `first_time` → ТО `pickup(player, stone)`, `mark(stone, 1)`, `disappear(stone)`.
- КОЛИ `input(click, stone)` → ЯКЩО `line_of_sight(current, stone)` and `not moving(player, back)` → ТО `pickup(player, stone)`, `mark(stone, k+1)`, `disappear(stone)`, `face(player, dir)`.
- КОЛИ `input(click, stone)` → ЯКЩО `not line_of_sight(current, stone)` → ТО `block` (інший ряд/стовпець або між ними є камінь; puzz.link не ставить номер).
- КОЛИ `input(click, stone)` → ЯКЩО `moving(player, back)` → ТО `block`: розворот на 180° заборонено.
- КОЛИ `contact(player, stone)` → ТО `pickup(player, stone)`: камінь на шляху не можна перескочити (`+effect:find_nearest`).
- КОЛИ `custom: «шлях проходить місце знятого каменя»` → ТО `custom: «іде далі прямо, повернути тут не можна»` (`+cond:passed_over`).
- КОЛИ `edge(player)` → ТО `block`.
- КОЛИ `all_gone(stone)` → ТО `win`.
- КОЛИ `no_moves(player)` → ЯКЩО `count(stone, >, 0)` → ТО `constraint_broken(stones_remain)` (puzz.link `goishiRemains`).
- КОЛИ `custom: «на полі нема каменів»` → ТО `constraint_broken(no_stones)` (puzz.link `brNoStone`, перевірка редактора).
- Варіант «чорний-білий» (Wei-Hwa Huang, 2006): КОЛИ `input(click, stone)` → ЯКЩО `same(stone, last, color)` → ТО `block`.
- Варіант «фіксований старт»: перший камінь заданий умовою (Wikipedia).
- Перемога: підняті всі камені одним ланцюгом. · Поразка: глухий кут — камені лишились, а ходу нема (переграти). · Рахунку нема.

## Керування і ввід
- Папір: пронумерувати камені 1…N у порядку підняття (Janko, puzz.link).
- puzz.link (play): клік по каменю — наступний номер, лише якщо крок легальний; нелегальний клік ігнорується. Edit: курсор + клавіша (`q`) або клік ставить камінь, подвійний клік — інше значення (?).
- Wikipedia: класично — фізичні камені на дошці, гравець знімає їх руками.

## Вікна, меню, HUD
- `game-screen` (puzz.link): решітка, камені, номери в піднятих; `check-button`, `undo-button`, `redo-button`; `remaining-counter` каменів — цифрова версія (?).
- `editor-window` (puzz.link edit mode): розмір дошки, розстановка каменів, експорт у URL.
- `help-window`: правила (Nikoli, puzz.link, Janko, Wikipedia).
- `puzzle-select` (Janko): 30 пазлів за розміром і складністю.
- Переходи: puzz.link rules → URL пазла → game-screen → Check → «розвʼязано» (?).

## Фічі поза полем
- `auto-check` за кнопкою: «лишились камені» / «нема каменів» (puzz.link).
- `undo` / `redo` (puzz.link) (?).
- `level-editor` + `share-code` — пазл як URL puzz.link.
- `puzzle-bank` (Janko: 30 пазлів 5×5…12×12; більшість розвʼязні логікою без проб).

## Варіації й родичі
- Назви: Hiroimono (ひろいもの, перша) → Goishi Hiroi; Rock Collection (Kim Scott, Suomi Go, Wei-Hwa Huang). Задача була на чемпіонаті світу з пазлів 1999 (Janko).
- Історія: бар-парі в Японії XIV ст. (Costello 1988, через Wikipedia); збірки Wakoku Chie Kurabe (Tagaya Kanchūsen, 1727) і Kanja Otogi Zōshi (Nakane Hikotate, 1743).
- Складність: розвʼязність NP-повна (Andersson 2007, з 3-SAT; Fukui–Suetsugu–Suzuki 2017, з гамільтонового шляху).
- Родичі: [hitori-ribashi](hitori-ribashi.md) — Janko називає схожим; [hashiwokakero](hashiwokakero.md) — теж «до найближчого острова по прямій»; [n-queens-knights-tour](n-queens-knights-tour.md) — гамільтонів обхід; [masyu](masyu.md) — поворот лише в позначених місцях.
- Змійка/Tron-подібні з `no-reverse-turn` — та сама заборона розвороту, але в реальному часі.
- **Осі варіацій**: старт вільний / заданий · кольори (один / чергування) · напрямки (4 / 8 (?)) · де можна повертати (лише на камені / будь-де).

## Цікавинки для курсу
- «Найближчий камінь у напрямку» — 🌱: цикл по лінії до першого каменя або краю.
- Генерація легальних ходів з урахуванням напрямку приходу (без розвороту) — 🌱.
- Ввід кліками з валідацією кроку й нумерацією — 📎.
- Розвʼязувач: DFS по станах (лишені камені, поточний, напрямок) з відсіканням ізольованих каменів — 🥈; NP-повнота як тема для розмови.
- Генератор: випадковий «обхід», що кладе камені в точках поворотів, потім перевірка єдиності — 🥇.
- Варіант «чорний-білий» — один додатковий предикат — 🌱.

## Мапа на каталог
- Є: `cell-click` ↔ клік по каменю · `collect-all` ↔ підняти всі · `no-reverse-turn` ↔ заборона 180° · `no-moves-left` ↔ глухий кут · `completion-detection`, `satisfy-constraints`, `remaining-counter` · `undo-redo` · `in-game-editor`, `import-open-formats` ↔ puzz.link URL · `level-bank` ↔ Janko · `level-solver`, `unique-puzzle-generation`.
- **Нема** → пропозиції карток:
  - `+nearest-in-direction-move` «Хід до найближчого обʼєкта в обраному напрямку, проміжні порожні проходяться» · entities/move · 🌱.
  - `+hamiltonian-path-check` «Шлях проходить кожен вузол рівно раз» · game-logic/constraints · 📎 (повтор із Knight's tour).
  - `+alternating-color-order` «Кольори в ланцюжку чергуються» · game-logic/constraints · 🌱.

## Пропозиції до словників
- `+effect:find_nearest` — знайти найближчий обʼєкт у напрямку (повтор із корпусу).
- `+cond:passed_over` — клітинку вже пройдено / обʼєкт тут уже знято (поворот заборонено).
- `+card:nearest-in-direction-move`, `+card:hamiltonian-path-check`, `+card:alternating-color-order` — див. мапу.

## Джерела
- ⭐ [Wikipedia: Goishi Hiroi](https://en.wikipedia.org/wiki/Goishi_Hiroi) — правила (по горизонталі/вертикалі, без розвороту, прямо або під прямим кутом), фіксований/вільний старт, історія, NP-повнота з двома доведеннями.
- [Wikipedia JA: 碁石拾い](https://ja.wikipedia.org/wiki/碁石拾い) — правила, книги 1727 і 1743, перша назва ひろいもの.
- [Nikoli: 碁石ひろい](https://www.nikoli.co.jp/ja/puzzles/goishi_hiroi/) — 4 правила: старт з будь-якого; без каменя — прямо; камінь обовʼязково підняти, тут можна повернути, але не назад; на місці знятого каменя повертати не можна.
- [puzz.link goishi.js](https://puzz.link/js/pzpr-samples/goishi.js) — правила EN/JA, коди `brNoStone`, `goishiRemains`, тести: нелегальний клік не отримує номера.
- [puzz.link rules](https://puzz.link/rules.html?goishi) — сторінка правил (рендериться JS).
- [Janko: Hiroimono](https://www.janko.at/Raetsel/Hiroimono/index.htm) — правила DE/EN («не пропускати непіднятий камінь»), назви, WPC 1999, Andersson 2007, варіант «чорний-білий», 30 пазлів.
- YouTube: пошук «Goishi Hiroi puzzle».

## Непевне
- (?) Значення подвійного кліку в редакторі puzz.link — з тестових послідовностей, не з документації.
- (?) Наявність undo/redo і повідомлення «розвʼязано» саме для goishi в puzz.link — загальна поведінка pzpr, не перевірена.
- (?) Бар-парі XIV ст. — переказ Wikipedia з Costello (1988), первинного джерела не бачив.
- (?) Варіанти з 8 напрямками — лише як вісь варіацій, у джерелах не бачив.
- Janko каже «можливо, вперше в Nikoli», Wikipedia — книга 1727: у шапці взято 1727 як найранішу задокументовану публікацію.
