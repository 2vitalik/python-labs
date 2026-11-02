---
title: Kaboom (+ LuckSweeper, Pure Skill Minesweeper, Tatham Mines — сапер, що карає або прощає вгадування)
slug: kaboom
family: hidden-deduction
also: [pencil-logic]
klass: cursor
axes:
  field: square
  time: static
  opponent: ai
  info: hidden
  random: runtime
  goal: state
year: 2019
platforms: [web]
links:
  - {kind: play, url: "https://pwmarcz.pl/kaboom/", best: true, note: "грати; пресети, опції Debug / Allow guessing anywhere / Safe mode / Countdown, Hint, Undo"}
  - {kind: other, url: "https://pwmarcz.pl/blog/kaboom/", note: "блог автора: ідея «cruel, but fair», класифікація клітин, SAT-розвʼязувач (MiniSat у JS)"}
  - {kind: official, url: "https://github.com/pwmarcz/kaboom", note: "код, MIT, 2019"}
  - {kind: play, url: "https://www.vidarholen.net/contents/lucksweeper/", note: "LuckSweeper: вимушене вгадування завжди щасливе"}
  - {kind: other, url: "https://github.andrewt.net/mines/", note: "Pure Skill Minesweeper: та сама ідея незалежно; опис «unnecessary guess backfires»"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/mines.html", note: "Tatham Mines: Ensure solubility (без вгадувань), Undo після вибуху з лічильником смертей"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=kaboom+minesweeper+cruel+but+fair", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [cell-click, chord-click, mines-after-first-click, difficulty-levels, game-settings, field-size-picker, completion-detection, level-solver, game-screen, end-screen, settings-window, +flood-reveal, +neighbor-count-clue, +no-guess-generation, +adversarial-placement, +forced-guess-safe, +lazy-hidden-state, +sat-cell-classifier, +debug-overlay, +undo-after-death]
proposes: ["+cond:provably_safe", "+cond:forced_guess", "+cond:flags_match", "+effect:flood_reveal", "+effect:resolve_hidden", "+effect:mark_safe", "+ui:mine-counter", "+ui:certainty-overlay", "+ui:death-counter", "+feature:guess-policy", "+feature:no-guess", "+feature:debug-overlay", "+feature:undo-after-death", "+axis:guess-policy", "+card:adversarial-placement", "+card:forced-guess-safe", "+card:lazy-hidden-state", "+card:sat-cell-classifier", "+card:debug-overlay", "+card:undo-after-death"]
author: opus
date: 2026-11-02
---

# Kaboom — сапер без прихованого стану: міни вирішуються в момент кліку, вгадування карається, вимушене — безпечне

## Суть
Kaboom (Paweł Marczewski, 2019) — сапер «cruel, but fair»: міни не розкидано на старті, гра визначає їх у момент кліку. Якщо клітина доведено безпечна — вона порожня; якщо можна було знайти безпечну клітину, а ти вгадував — гра обирає найгірший сценарій і ставить міну; якщо доведено безпечних клітин нема (вимушене вгадування) — вгадування безпечне. Файл описує цілу **вісь дизайну «вгадування: карається / безпечне / неможливе»**: LuckSweeper робить вимушене вгадування щасливим, але не карає зайве; Tatham Mines генерує поле, де вгадувати не доведеться; класичний Windows-сапер — вгадування чесно випадкове.

## Поле і час
- Прямокутна сітка W×H, сусідство 8; ширина, висота, кількість мін — поля вводу + 4 пресети з назвами рівнів Doom («I'm too young to die» … «Ultra-Violence»).
- Шари клітини: стан (закрита / відкрита з числом / прапорець) + **немає прихованого шару** — є лише множина розміщень мін, сумісних з усіма відкритими числами («Only the labels will be binding»).
- Межа (boundary) — закриті клітини поруч з відкритими числами; моделюються точно. Решта закритих — «океан», де міни розподіляються випадково з урахуванням загальної кількості.
- Статично, без часу; Countdown mode — режим з відліком (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Закрита клітина | object | клас: safe / mine / uncertain (обчислюється) | при відкритті вирішується за політикою вгадування |
| Відкрита клітина-число | mark | 0–8 | кількість мін серед 8 сусідів; 0 — каскадне відкриття |
| Міна | hazard | — | існує лише як наслідок: зʼявляється, коли гра «вирішує» клітину проти тебе |
| Прапорець | mark | — | позначка гравця; не впливає на розвʼязувач |
| Клітина межі | zone | — | закрита, поруч із числом; кодується в SAT-формулу |
| Океан (поза межею) | zone | — | закриті клітини без сусідніх чисел; клік туди за замовчуванням карається |
| Debug-позначка | mark | safe / mine / uncertain | (Debug mode) показує класифікацію кожної клітини |
| Tatham: відкрита стартова область | mark | — | гарантований вхід, з якого все поле виводиться логікою |

## Правила (КОЛИ → ЯКЩО → ТО)
- Класифікація (перед кожним кліком): для закритої клітини c — `custom: «SAT: чи існує розміщення, сумісне з усіма числами і загальною кількістю мін, де c = міна? де c = порожньо?»`; лише «порожньо» можливе → safe; лише «міна» → mine; обидва → uncertain.
- КОЛИ `input(reveal, c)` → ЯКЩО `provably_safe(c)` → ТО `reveal(c)` як порожню, число = `adjacent_count(c, mine)` у новому розміщенні; 0 → `flood_reveal`.
- КОЛИ `input(reveal, c)` → ЯКЩО `custom: «c доведено міна»` → ТО `lose` (Kaboom!).
- КОЛИ `input(reveal, c)` → ЯКЩО c uncertain і `custom: «на полі є хоч одна доведено безпечна клітина»` → ТО `custom: «обрати розміщення, де c — міна»`, `lose` («cruel»).
- КОЛИ `input(reveal, c)` → ЯКЩО c uncertain і `forced_guess` (доведено безпечних нема) → ЯКЩО c на межі (або ввімкнено «Allow guessing anywhere») → ТО `custom: «обрати розміщення, де c порожня»`, `reveal(c)` («fair»).
- Поза межею: КОЛИ `input(reveal, ocean_cell)` → ЯКЩО не (нічого ще не відкрито / усі міни доведено на межі / уся межа доведено міни) → ТО карається як зайве вгадування; перемикач «Allow guessing anywhere» знімає обмеження.
- Перший клік: нічого не відкрито → безпечний (вимушене вгадування за визначенням).
- КОЛИ `input(chord, n)` → ЯКЩО `flags_match(n)` → ТО відкрити незапрапорованих сусідів (кожного — за правилами вище).
- Safe mode: КОЛИ `input(click)` → ТО `block`; відкриття — лише подвійним кліком (захист від випадкового).
- КОЛИ `input(hint)` → ТО `custom: «підсвітити одну доведено безпечну клітину»` (?); Debug mode — показати класи всіх клітин.
- КОЛИ `input(undo)` → ТО повернути стан до останнього кліку (зокрема після вибуху (?)).
- КОЛИ `custom: «усі не-мінні клітини відкрито»` → ТО `win`.
- LuckSweeper: КОЛИ відкриття → ЯКЩО `forced_guess` між рівноймовірними розміщеннями → ТО вгадування «випадково» щасливе; але біля «8» — `lose` (там немає шансу). Зайве вгадування не карається явно (?) — звичайна ймовірність.
- Pure Skill Minesweeper (andrewt): вимушене → тихо переставляє міни на користь гравця; зайве → переставляє так, щоб вгадування програло (та сама ідея, що Kaboom; автор радить Kaboom).
- Tatham Mines: КОЛИ генерація → ЯКЩО `Ensure solubility` → ТО `custom: «поле виводиться логікою зі стартової області»`; КОЛИ вибух → ТО відкривається лише ця міна, Undo дозволено, `counter(deaths, +1)` (Undo лічильник не зменшує).
- Перемога: відкрити всі безпечні клітини · Поразка: відкрити міну · Рахунок: нема (час/кліки — не основне).

## Керування і ввід
- Лівий клік — відкрити (у Safe mode — подвійний клік); правий — прапорець; акорд по числу — як у класичному сапері.
- Кнопки «Give me a hint», «Undo», «New game»; поля «width / height / mines»; 4 пресет-кнопки.
- Чекбокси: Debug mode · Allow guessing anywhere · Safe mode (double-click to reveal) · Countdown mode.
- LuckSweeper: правий клік — позначка, середній — відкрити область (акорд). Tatham: Space — прапорець, лівий клік по прапорцю не відкриває.

## Вікна, меню, HUD
- `game-screen` (одна вебсторінка): поле; над ним — налаштування розміру й мін, пресети, чекбокси опцій, кнопки Hint/Undo/New game; посилання на блог, GitHub, LuckSweeper-подібні проєкти.
- HUD: `mine-counter` (?), `certainty-overlay` у Debug mode (кольорові позначки safe / mine / uncertain), `hint-marker`.
- `end-screen`: стан вибуху або перемоги на тому ж полі (без окремого вікна) (?).
- Tatham Mines: стандартне меню колекції (Game / Type / Help → `help-window`), `death-counter` у статус-рядку, `settings-window` Custom (розмір, кількість або % мін, Ensure solubility).
- Переходи: game-screen → New game / пресет → game-screen; вибух → Undo → game-screen того ж стану.

## Фічі поза полем
- `guess-policy` (нова вісь): карати зайве (Kaboom, Pure Skill) · прощати вимушене (Kaboom, LuckSweeper) · унеможливити (Tatham `Ensure solubility`, no-guess режими онлайн-саперів) · чесна випадковість (класика).
- `custom-difficulty` + `difficulty-presets` (4 рівні), `undo`, `hint`, `debug-overlay` (навчальний режим: видно, як міркує розвʼязувач), `mouse-and-keyboard`.
- Tatham: `undo-after-death` з лічильником смертей — «прощення» не через генерацію, а через відкат.
- Відкритий код (MIT) і детальний блог — готовий навчальний розбір.

## Варіації й родичі
- Класичний Minesweeper (міни на старті, перший клік безпечний у Windows), Tatham Mines (генерація без вгадувань), онлайн «No guessing» режими (minesweeper.online), Kaboom і Pure Skill Minesweeper (адверсарна ліниве розміщення), LuckSweeper (вимушене — щасливе).
- Ідейні родичі «адверсарного прихованого стану»: Absurdle (Wordle, де слово обирається найгірше) (?), адверсарний шифрувальник у Mastermind.
- **Осі варіацій**: момент фіксації мін «до гри / після першого кліку / ніколи (ліниво)»; політика вгадування «випадково / карається / вимушене безпечне / неможливе»; що вважається вимушеним «нема безпечних на межі / нема безпечних ніде / лише сусідні до відкритих»; прощення «undo після вибуху / лічильник смертей / нема».

## Цікавинки для курсу
- Класифікатор клітин safe / mine / uncertain перебором розміщень межі (бектрекінг) — 🥇 (автор упирався в 18 млн варіантів на великих полях).
- Те саме через SAT (CNF, кодування «сума сусідів = n», totalizer для загальної кількості мін) — 👑.
- Ліниве розміщення: міна стає фактом лише в момент кліку, правила «cruel, but fair» — 🥇 поверх класифікатора.
- Debug-оверлей «що гра знає про клітину» — 🥉 (добре пояснює студентам дедукцію).
- LuckSweeper-політика (вимушене — щасливе) — 🥈: потрібне лише розпізнати вимушене вгадування.
- Tatham «Undo після вибуху + лічильник смертей» — 📎: найдешевший спосіб прибрати біль вгадування.
- Генерація без вгадувань: генеруй і перевіряй розвʼязувачем, перестав міни до успіху — 🥇 (картка `+no-guess-generation`).

## Мапа на каталог
- Є: `cell-click` · `chord-click` · `mines-after-first-click` (тут — граничний випадок: міни після *кожного* кліку) · `difficulty-levels` + `game-settings` + `field-size-picker` · `completion-detection` · `level-solver` (класифікатор) · `game-screen` / `end-screen` / `settings-window`.
- **Нема** → пропозиції карток:
  - `+flood-reveal` · `+neighbor-count-clue` · `+no-guess-generation` — див. Minesweeper.
  - `+adversarial-placement` «Адверсарне розміщення прихованого» · levels/generation · 🥇 — гра обирає найгірше сумісне.
  - `+forced-guess-safe` «Вимушене вгадування безпечне» · levels/generation · 🥈 (LuckSweeper, Kaboom).
  - `+lazy-hidden-state` «Прихований стан без фіксації» · code/architecture · 🥇 — зберігати лише відкриті факти, а не розміщення.
  - `+sat-cell-classifier` «Класифікація клітин розвʼязувачем» · levels/solvability · 👑 · слот {engine: backtrack|sat}.
  - `+debug-overlay` «Оверлей знань розвʼязувача» · interface/hud · 🥉.
  - `+undo-after-death` «Відкат після програшу з лічильником смертей» · game-logic/lose · 📎.

## Пропозиції до словників
- `+cond:provably_safe` — клітина безпечна в усіх сумісних розміщеннях.
- `+cond:forced_guess` — на полі нема жодної доведено безпечної клітини (вгадування вимушене).
- `+cond:flags_match` — див. Minesweeper (акорд).
- `+effect:flood_reveal` — див. Minesweeper; `+effect:mark_safe` — див. 14 Minesweeper Variants (Debug-позначка safe).
- `+effect:resolve_hidden` — зафіксувати прихований вміст клітини в момент взаємодії за політикою (найгірше / найкраще / випадкове).
- `+ui:mine-counter` — див. Minesweeper; `+ui:certainty-overlay` — позначки safe/mine/uncertain поверх закритих клітин; `+ui:death-counter` — скільки разів вибухнув (Tatham).
- `+feature:guess-policy` — налаштування, як гра реагує на вгадування; `+feature:no-guess` — див. Minesweeper; `+feature:debug-overlay`; `+feature:undo-after-death`.
- `+axis:guess-policy` — нова вісь для hidden-deduction: `random` (класика) · `punished` (Kaboom) · `forgiven` (LuckSweeper) · `impossible` (Tatham, Hexcells) · `undoable` (Tatham Undo).

## Джерела
- ⭐ [Kaboom](https://pwmarcz.pl/kaboom/) — гра в браузері з усіма опціями.
- [Блог: Kaboom](https://pwmarcz.pl/blog/kaboom/) — ідея, класифікація клітин, бектрекінг → SAT (MiniSat, totalizer Bailleux–Boufkhad), правила кліків поза межею, Debug mode.
- [GitHub pwmarcz/kaboom](https://github.com/pwmarcz/kaboom) — код (є `sat.js`), MIT 2019.
- [LuckSweeper](https://www.vidarholen.net/contents/lucksweeper/) — вимушене вгадування щасливе, біля «8» — ні.
- [Pure Skill Minesweeper](https://github.andrewt.net/mines/) — незалежна реалізація ідеї, «unnecessary guess backfires».
- [Tatham Mines](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/mines.html) — Ensure solubility, Undo після вибуху, лічильник смертей, % мін.
- YouTube: пошук «kaboom minesweeper cruel but fair».

## Непевне
- (?) Що саме робить «Give me a hint» і «Countdown mode» — на сторінці лише назви з «(?)», блог не описує.
- (?) Розміри/кількість мін для 4 пресетів Kaboom — не показані в тексті сторінки.
- (?) Чи LuckSweeper карає зайве вгадування — сторінка мовчить; ймовірно, ні (звичайна ймовірність).
- (?) Undo в Kaboom після вибуху — кнопка є, поведінку не перевірено.
- (?) Absurdle як адверсарний Wordle — з памʼяті.
