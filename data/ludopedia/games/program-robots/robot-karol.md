---
title: Robot Karol
slug: robot-karol
aka: [Karol, Robot Karol Online, Java Karol, Robot Karol++]
family: program-robots
also: []
klass: avatar
axes:
  field: layers
  time: programmed
  opponent: none
  info: full
  random: none
  goal: state
year: 2001
platforms: [PC, web]
links:
  - {kind: play, url: "https://karol.arrrg.de/", best: true, note: "Robot Karol Online — блоки, текст, Python, Java; збірка задач з перевіркою"}
  - {kind: wiki, url: "https://de.wikipedia.org/wiki/Robot_Karol", note: "історія: Karel → Robot Karol++ (Krško) → Freiberger 2001; v3.0.4 (2019); Online з 2022"}
  - {kind: other, url: "https://github.com/Entkenntnis/robot-karol-online", note: "README: команди, умови, режими блок/текст/Python/Java, редактор задач"}
  - {kind: other, url: "https://de.wikibooks.org/wiki/Mini-Languages:_Programmierung_von_Robot_Karol", note: "Ziegel / Quader / Marke, висота стопки, клавіші, повідомлення помилок"}
  - {kind: other, url: "http://cgd.zum.de/wiki/Programmieren_lernen_mit_Robot_Karol", note: "умови IstZiegel(n), IstMarke, IstNorden…; Anweisung … *Anweisung; кольори з v3.0"}
  - {kind: play, url: "https://entkenntnis.github.io/rk3.0/", note: "оригінальний Robot Karol 3.0 у браузері"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=robot+karol", note: "пошук; уроки"}
stage: v1
coverage: 70
mechanics: [command-program, user-procedures, sensor-predicates, step-execution, code-editor-window, height-levels, impassable-cells, inventory-items, in-game-editor, editor-palette, editor-playtest, level-exchange, puzzle-select, keyboard-controls, sound-effects, game-screen, help-window, +runtime-error-stop, +goal-state-check, +stack-height-limit, +blocks-text-switch, +structogram-view, +view-2d-3d-toggle]
proposes: ["+cond:height_diff(a, b, op, n)", "+cond:stack_height(cell, op, n)", "+window:structogram-view", "+ui:view-2d-3d-toggle", "+feature:blocks-text-switch"]
author: opus
date: 2026-11-09
---

# Robot Karol — Karel з третім виміром: робот кладе цеглини стопками й лізе на них

## Суть
Німецька шкільна гілка Karel: робот Karol на клітинному полі виконує програму з `Schritt`, `LinksDrehen`, `Hinlegen`, `Aufheben`, `MarkeSetzen`. Головна відмінність від [karel](karel.md) — **висота**: цеглини (Ziegel) кладуться в клітину перед роботом стопкою, а сам робот може ступити на стопку, лише якщо перепад висот ≤ 1, тож вищу стопку треба обійти або збудувати «сходи». Світ показується в ізометричному 3D (і 2D-плані). Robot Karol Online (2022+) додає блоковий режим, Python/Java і збірку задач з перевіркою цілі.

## Поле і час
- Квадратна сітка (ширина × довжина задаються при створенні світу) + **висота**: кожна клітина — стопка цеглин 0…N, звичайна межа 6, максимум 10 при створенні світу.
- Шари клітини: висота стопки (Ziegel, у v3.0 — кольорові) + марка (Marke) на «підлозі» стопки + Quader (суцільний блок-перешкода) або нічого + робот.
- Стіни — межа світу; Quader працює як внутрішня стіна.
- Вид — ізометричне 3D або 2D-план зверху; Північ — угорі.
- Час `programmed`: тік = одна команда; `Warten(ms)` — пауза; є покроковий режим і ручне керування стрілками.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Karol | player | позиція, висота стояння, напрям N/E/S/W | виконує програму; ступає вперед на клітину з перепадом ≤ 1 |
| Ziegel (цеглина) | object | висота стопки, колір (v3.0: червоний/жовтий/синій/зелений) | кладеться/знімається в клітині **перед** роботом; стопка росте вгору |
| Quader (блок) | static | — | непрохідний; не стопкується; на нього не стати; не кладеться на марку |
| Marke (марка) | mark | колір (v3.0) | ставиться/знімається **під** роботом; лишається під цеглиною, якщо на неї покласти Ziegel |
| Межа світу (Wand) | static | — | `IstWand` = true; `Schritt` у неї → помилка |
| Цільовий світ (Online) | mark | стан цеглин, марок, позиції | задача вважається розвʼязаною, коли світ збігся з ціллю |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `exec(Schritt)` → ЯКЩО `free(front)` and `custom: «|висота(front) − висота(here)| ≤ 1»` → ТО `move(karol, facing)`.
- КОЛИ `exec(Schritt)` → ЯКЩО `not free(front)` → ТО `crash` («Karol ist an die Wand angestoßen» з номером рядка).
- КОЛИ `exec(Schritt)` → ЯКЩО `custom: «перепад висот > 1»` → ТО `crash` (?).
- КОЛИ `exec(LinksDrehen|RechtsDrehen)` → ТО `face(karol, ±90°)`; з параметром — n поворотів.
- КОЛИ `exec(Hinlegen(n))` → ЯКЩО `free(front)` → ТО `place(ziegel, front)` n разів (`custom: «висота стопки +n»`).
- КОЛИ `exec(Hinlegen)` → ЯКЩО `custom: «стопка вже максимальної висоти»` → ТО `crash` («Maximale Stapelhöhe erreicht»).
- КОЛИ `exec(Aufheben(n))` → ЯКЩО `occupied(front, ziegel)` → ТО `custom: «зняти n цеглин зі стопки перед собою»`; інакше `crash` (?).
- КОЛИ `exec(MarkeSetzen|MarkeLöschen)` → ТО `mark(here, marke)` / `unmark(here)`.
- КОЛИ `exec(Quader setzen)` (лише в редакторі/вручну: Q / E) → ТО `set_cell(front, quader)` / `set_cell(front, empty)`.
- КОЛИ `exec(Ton)` → ТО `sound(ton)`; `exec(Warten(ms))` → ТО `custom: «пауза»`.
- КОЛИ `exec(Beenden)` → ТО `custom: «негайно зупинити програму»`.
- Умови (чисті): `IstWand` ↔ `not free(front)`; `IstZiegel` / `IstZiegel(n)` ↔ `occupied(front, ziegel)` / `custom: «у стопці перед собою рівно n»`; `IstMarke` ↔ `cell(here, marke)`; `IstNorden|Osten|Süden|Westen` ↔ `facing(karol, dir)`; кожна має `Nicht…`-заперечення.
- Потік: `wiederhole n mal`, `wiederhole solange <cond>`, `wiederhole … *wiederhole solange|bis` (з постумовою), `wiederhole immer`, `wenn … dann … sonst … *wenn`; свої `Anweisung name … *Anweisung` і `Bedingung name … wahr/falsch … *Bedingung`; лише один параметр, рекурсія без параметрів; змінних і операторів нема.
- КОЛИ `program_end` → ЯКЩО `custom: «світ = цільовий (Online-задача)»` → ТО `win`; інакше `message(«ще не збігається»)`.
- Перемога: світ збігся з ціллю (Online) / учитель перевіряє на око (класична версія) · Поразка: помилка виконання · Рахунок: нема.

## Керування і ввід
- Програма — текст німецькою (`Schritt`, `wiederhole 4 mal`…), регістр не важливий, параметри в дужках; у v3.0 стара синтаксис-форма `*wiederhole`, у Online — ще ООП-форма `karol.Schritt(4)`.
- Online: блоковий редактор (Blockly-подібний) ⇄ текст, перемикання будь-коли; плюс Python- і Java-режими; Struktogramm-вид програми.
- Запуск F9, крок F7, «Abbrechen» для нескінченного циклу; кнопка «L» / «Welt löschen» — повернути початковий світ.
- Ручне керування: стрілки рухають/повертають, H — покласти цеглину, A — підняти, M — марка, Q/E — поставити/прибрати Quader.

## Вікна, меню, HUD
- `game-screen` (v3.0) = редактор програми (ліворуч угорі) + світ 2D/3D (праворуч) + довідник команд (ліворуч унизу) + інформаційна панель з помилками (праворуч унизу).
- HUD: `instruction-highlight`, позначка «великий палець униз» на рядку з помилкою, `view-2d-3d-toggle`, `step-button`, `speed-slider` (?).
- `editor-window`: «Welt → Neue Welt» (ширина, довжина, висота), розставлення вручну, збереження `.kdw`.
- Online: `puzzle-select` — огляд задач (від туторіалів до вкладених алгоритмів); `editor-window` задач з ціллю й посиланням для розсилки.
- `structogram-view` — програма як діаграма Насі–Шнейдермана.
- `help-window` — вбудований довідник команд.

## Фічі поза полем
- `level-editor` + `level-sharing`: світ `.kdw` (v3.0), задача за посиланням (Online).
- `goal-check` в Online-задачах.
- `blocks-text-switch` — та сама програма блоками і текстом.
- `step-mode`, ручне керування для дослідження світу.
- Бібліотеки користувачів (Karollign, KarolAlphabet — малювання літер цеглинами).
- Java Karol (2008) — ті самі методи як Java-бібліотека для переходу до «справжньої» мови.

## Варіації й родичі
- [karel](karel.md) — предок (Pattis); Robot Karol++ (Ондрей Кршко, Словаччина) → Robot Karol (Ульлі Фрайбергер, 2001+) → Java Karol → Robot Karol Online (Девід Лі, 2022).
- [lightbot](lightbot.md) — теж висота ±1 і стрибок, але без будування стопок; [kara](kara.md) — швейцарський сусід.
- Niki der Roboter, Turtle-графіка — шкільні альтернативи в Баварії.
- Осі варіацій: **поле** (2D / з висотою, яку робот змінює сам); **що кладе робот** (біпер у свою клітину / цеглину перед собою стопкою); **перешкоди** (стіни на ребрах / Quader у клітині); **мова** (німецька міні-мова / блоки / Python / Java).

## Цікавинки для курсу
- Висотна мапа зі стопками і правилом кроку «перепад ≤ 1» — 📎.
- Робот змінює рельєф (кладе цеглину перед собою), а потім сам по ньому лізе: «збудуй сходи» — 🥉.
- Ізометричний рендер стопок + перемикач 2D/3D над тією самою моделлю — 🥈.
- Міні-мова з `wiederhole … *wiederhole` і власними `Bedingung` (умова з `wahr/falsch`) — 🥇.
- Перемикання блоки ⇄ текст однієї програми (round-trip AST) — 🥇.
- Перевірка цілі як порівняння стопок і марок з цільовим світом — 📎.

## Мапа на каталог
- Є: `command-program` · `user-procedures` · `sensor-predicates` · `step-execution` · `code-editor-window` · `height-levels` (стопки, крок ±1) · `impassable-cells` (Quader) · `inventory-items` (цеглини з «необмеженого запасу» (?)) · `in-game-editor` / `editor-palette` / `editor-playtest` · `level-exchange` (`.kdw`, посилання) · `puzzle-select` · `keyboard-controls` (ручне керування) · `sound-effects` (`Ton`) · `game-screen` · `help-window`.
- **Нема** → пропозиції карток:
  - `+runtime-error-stop`, `+goal-state-check` (вже пропоновано в Karel).
  - `+stack-height-limit` «Ліміт висоти стопки, перевищення — помилка» · entities/legality · 🌱.
  - `+blocks-text-switch` «Програма блоками й текстом з перемиканням» · interface/input · 🥇.
  - `+structogram-view` «Програма як структурограма» · interface/render · 🥈.
  - `+view-2d-3d-toggle` «Те саме поле в 2D-плані та ізометрії» · interface/render · 🥈.

## Пропозиції до словників
- `+cond:height_diff(a, b, op, n)` — перепад висот між клітинами (крок на стопку, Lightbot-стрибок).
- `+cond:stack_height(cell, op, n)` — висота стопки в клітині (`IstZiegel(n)`).
- `+window:structogram-view` — вікно-вид програми як діаграми.
- `+ui:view-2d-3d-toggle` — перемикач виду поля.
- `+feature:blocks-text-switch` — двостороннє перетворення блоки ⇄ текст.

## Джерела
- ⭐ [Robot Karol Online](https://karol.arrrg.de/) — грати одразу (сторінка — SPA, зміст підтверджено через README).
- [GitHub: robot-karol-online](https://github.com/Entkenntnis/robot-karol-online) — команди (Schritt, Links/RechtsDrehen, Hinlegen/Aufheben з кількістю, MarkeSetzen/Löschen, Beenden), умови (IstWand, IstZiegel(n), IstMarke, IstNorden…), режими блок/текст/Python/Java, Struktogramm, редактор задач.
- [Wikipedia (de): Robot Karol](https://de.wikipedia.org/wiki/Robot_Karol) — походження від Karel, Krško → Freiberger (2001), v3.0.4 (2019), Java Karol (2008), Online (2022), власні Anweisung/Bedingung з одним параметром, без змінних.
- [Wikibooks: Programmierung von Robot Karol](https://de.wikibooks.org/wiki/Mini-Languages:_Programmierung_von_Robot_Karol) — Ziegel/Quader/Marke, висота 6 (до 10), «Maximale Stapelhöhe erreicht», клавіші H/A/Q/E/M, F7/F9, помилка «an die Wand angestoßen».
- [ZUM: Programmieren lernen mit Robot Karol](http://cgd.zum.de/wiki/Programmieren_lernen_mit_Robot_Karol) — умови, `Anweisung … *Anweisung`, `.kdw`, кольори цеглин і марок з v3.0.
- [Robot Karol 3.0 у браузері](https://entkenntnis.github.io/rk3.0/) — оригінальний інтерфейс.

## Непевне
- (?) Що буде при кроці на стопку з перепадом > 1 — помилка чи просто відмова; Wikibooks каже лише «на дві й більше — будуй сходи».
- (?) Рюкзак цеглин (`HatZiegel`, `IstVoll`, `IstLeer`) і обмежений запас — у джерелах не знайшов; з памʼяті є опція в налаштуваннях v3.0.
- (?) Умови `IstZiegelLinks/Rechts` — з памʼяті, у відкритих джерелах нема.
- (?) Рік першої версії: Freiberger почав у 2001; точна дата релізу 1.0 невідома.
- (?) Як саме Online-задачі перевіряють ціль (порівняння зі світом-ціллю) — з README видно лише «інтерактивні задачі».
