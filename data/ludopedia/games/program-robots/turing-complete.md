---
title: Turing Complete
slug: turing-complete
aka: [TC]
family: program-robots
also: [thinky]
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: setup
  goal: state
year: 2021
platforms: [PC, Mac, Linux]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1444480/Turing_Complete/", best: true, note: "від NAND до CPU і асемблера; власна мова асемблера; екрани, таймери, звук, клавіатура, мережа; 70+ рівнів у ранньому доступі"}
  - {kind: wiki, url: "https://turingcomplete.wiki.gg/wiki/Level_Guides", note: "усі рівні за розділами: Boolean Logic, Arithmetic and Memory, CPU Architecture 1–2, Programming 1–2, опційні"}
  - {kind: wiki, url: "https://turingcomplete.wiki.gg/wiki/Components", note: "повний список компонентів: Bit / Word / Misc / IO"}
  - {kind: wiki, url: "https://turingcomplete.wiki.gg/wiki/General_Guides", note: "гайди: схема зі слів, карти Карно, автомати станів (лабіринт двома вентилями)"}
  - {kind: other, url: "https://turingcomplete.game/leaderboard", note: "офіційний лідерборд (лінк з вікі, не відкрито)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=turing+complete+game+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [cell-click, drag-drop-piece, multi-select, sequential-levels, level-unlock, world-map, level-select, command-program, step-execution, code-editor-window, mode-indicator, in-game-editor, leaderboard, game-screen, end-screen, help-window, +logic-gates, +wire-drawing, +signal-propagation, +io-test-streams, +solution-metrics, +custom-component, +bit-word-buses, +custom-assembly-language, +truth-table-spec, +self-built-cpu-runs-program]
proposes: ["+trigger:signal(net)", "+cond:powered(net)", "+effect:power(net)", "+effect:halt", "+role:wire", "+role:pin", "+window:truth-table", "+window:assembly-editor", "+window:component-factory", "+ui:wire-probe", "+feature:custom-components", "+card:custom-assembly-language"]
author: opus
date: 2026-11-09
---

# Turing Complete — збери компʼютер з NAND: вентилі на сітці, потім АЛП, регістри, CPU і асемблер власного дизайну

## Суть
Пазл-кампанія з цифрової схемотехніки: гравець ставить компоненти на клітинне полотно й зʼєднує їх дротами, щоб вихідні піни дали очікувані значення на тестах рівня. Починається з одного NAND, з якого будують NOT, AND, OR, XOR, суматор, памʼять, лічильник; кожна побудована штука відкривається як компонент. Посередині кампанії гравець збирає власний процесор, потім пише для нього програми (спершу машинним кодом, далі асемблером, мнемоніки якого задає сам). Фінальні рівні — алгоритмічні задачі (лабіринт, Нім, ханойська вежа) на своєму ж CPU.

## Поле і час
- Полотно — квадратна сітка; компоненти — прямокутники на клітинах, дроти — лінії по клітинах (?); вхідні й вихідні піни рівня закріплені.
- Два типи сигналів: біт і слово (байт, ширші слова (?)); шини розгалужують і збирають Splitter/Maker.
- Час: схема без станів — обчислення за тест; з памʼяттю — потактово (`Delay Line`, `Register`): тік = такт (?).
- Тести: таблиця істинності або набір тактів із входами/очікуваними виходами; частина згенерована випадково (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Дріт | conduit | біт / слово | переносить значення від виходу до входів |
| Вентилі AND, NAND, NOR, NOT, OR, XNOR, XOR, 3-pin AND/OR | conduit | біт або слово (побітово) | булева функція |
| ON / OFF / Constant | source | 1 / 0 / число | постійне значення |
| Input Pin / Output Pin | source / sink | біт / слово | входи рівня / виходи, що перевіряються |
| Switch (bit/word) | switch | керуючий біт | пропускає значення або «нічого» (третій стан для шин) |
| Decoder 1/2/3 біти | conduit | — | вибирає один із 2^n виходів |
| Full Adder / Add / Increment / Negate | conduit | — | арифметика |
| Multiply / Divide / Modulo / Shift / Rotate / ASR / CLZ / CTZ | conduit | — | розширені операції (частина — опційні рівні) |
| Equal / Less (signed) / Less (unsigned) | conduit | — | порівняння → біт |
| Mux | conduit | — | вибір одного з входів |
| Delay Line (bit/word) | container | 1 такт | віддає значення з попереднього такту |
| Register (bit/word) | container | load / save | памʼять, що оновлюється за керуючим бітом |
| Counter | container | крок | наростає щотакту |
| RAM + Load/Store Port | container | адреса | памʼять з довільним доступом |
| Splitters / Makers / Concatenators | conduit | — | розбити слово на біти / зібрати |
| Program (ROM) | source | машинний код | подає інструкцію за адресою (?) |
| Halt | sink | біт | зупиняє симуляцію |
| 7-Segment Display, Screen, Keyboard, Push Button, Time | sink / source | IO | вивід/ввід користувача |
| Probes (wire, memory, disassembling) | mark | — | показують значення для дебагу |
| Власний компонент | container | схема гравця | побудована схема як один блок |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `custom: «змінився вхід вентиля»` → ТО `custom: «вихід = функція входів»`.
- КОЛИ `tick` → ТО `custom: «Delay Line/Register видають збережене; Register записує, якщо save = 1»`.
- КОЛИ `custom: «дріт має два активні джерела»` → ТО `custom: «помилка: конфлікт на шині»` (?).
- КОЛИ `custom: «вихід залежить сам від себе без затримки»` → ТО `custom: «помилка: цикл без Delay Line»` (рівень «Circular Dependency» на це вчить).
- КОЛИ `input(run)` → ТО `custom: «прогнати всі тести рівня»`; ЯКЩО `custom: «вихідний пін ≠ очікуваний»` → ТО `custom: «показати тест і різницю»`.
- КОЛИ `all_constraints_met` → ТО `win`, `custom: «розблокувати компонент/рівень»`, `window(end-screen)` з оцінкою.
- КОЛИ `custom: «побудовано компонент рівня (NOT, суматор, регістр…)»` → ТО `unlock(component)`.
- КОЛИ `exec(instruction)` → ТО `custom: «CPU гравця декодує байт і керує АЛП/регістрами/переходом»` — семантику задає схема гравця.
- КОЛИ `custom: «асемблер: мнемоніка»` → ТО `custom: «підставити байт, який гравець привʼязав до слова»`.
- КОЛИ `custom: «Halt = 1»` → ТО `custom: «зупинити симуляцію»`.
- Перемога: усі тести рівня пройдено · Поразка: нема — правиш схему · Рахунок: вартість вентилів і затримка (?), у програмних рівнях — кількість тактів (?).

## Керування і ввід
- Вибір компонента з палітри → клік на полотно; drag дротів між пінами; виділення рамкою, копіювання, обертання (?).
- Кнопки симуляції: крок такту / запуск / швидко (?); Probes на дротах показують значення.
- Програмні рівні: редактор коду з таблицею «мнемоніка → байт», що її визначає гравець.

## Вікна, меню, HUD
- `world-map` / `level-select`: дерево рівнів за розділами з залежностями (?).
- `game-screen`: полотно, палітра компонентів, `truth-table` (custom: очікувані входи/виходи, поточний тест), панель симуляції.
- `assembly-editor` (custom): текст програми + словник інструкцій гравця.
- `component-factory` (custom): створення власного компонента з піном-інтерфейсом (?).
- `end-screen`: оцінка схеми; `leaderboard` (онлайн).
- `help-window`: текстова теорія перед рівнем (?).

## Фічі поза полем
- `mode-sandbox`: вільне полотно для власних компʼютерів; власні компоненти; IO-компоненти (екран, клавіатура, мережа, звук).
- `leaderboard-online`, `achievements`, `cloud-save`; рання версія (з 2021), повний реліз планується на 2026.
- Verilog Input/Output-компоненти (?).

## Варіації й родичі
- NandGame (браузер), MHRD, Nand2Tetris (курс) — та сама драбина від NAND до CPU (?).
- У корпусі: [kohctpyktop](kohctpyktop.md) (транзистори на шарах), [robot-odyssey](robot-odyssey.md), [tis-100](tis-100.md) (асемблер готового CPU), [factorio-circuit-network](factorio-circuit-network.md), [minecraft-redstone](../build-sim/minecraft-redstone.md).
- **Осі варіацій:** рівень абстракції (транзистор / вентиль / блок) · сигнал (біт / слово / шина) · хто визначає ISA (гра / гравець) · оцінка (кількість вентилів / затримка / такти).

## Цікавинки для курсу
- Симулятор комбінаційної схеми на сітці з топологічним сортуванням — 🥉.
- Детектор циклу без затримки (пошук циклів у графі) — 📎.
- Послідовна логіка: Delay Line, Register, Counter по тактах — 🥈.
- Тест-раннер «таблиця істинності» з першою розбіжністю — 📎.
- Власний компонент: схема → блок із пінами (рекурсивна вкладеність) — 🥇.
- Асемблер з користувацькими мнемоніками → байти → виконання на схемі гравця — 🥇.
- Оцінка вартості схеми як сума NAND-еквівалентів — 📎.

## Мапа на каталог
- Є: `cell-click` · `drag-drop-piece` · `multi-select` · `sequential-levels` · `level-unlock` · `world-map` · `level-select` · `command-program` · `step-execution` · `code-editor-window` · `in-game-editor` (пісочниця) · `leaderboard` · `game-screen` · `end-screen` · `help-window`.
- **Нема** → пропозиції карток:
  - `+logic-gates` (як у редстоуні), `+signal-propagation` (Kohctpyktop), `+io-test-streams`, `+solution-metrics` (TIS-100) — підтвердження.
  - `+wire-drawing` «Дроти між пінами компонентів» · interface/input · 📎.
  - `+custom-component` «Схема гравця стає блоком палітри» · game-logic · 🥇.
  - `+bit-word-buses` «Біт і слово, сплітери/мейкери» · 🥉; `+truth-table-spec` · 📎.
  - `+custom-assembly-language` «Гравець задає мнемоніки своєї ISA» · 🥇; `+self-built-cpu-runs-program` · 👑.

## Пропозиції до словників
- `+trigger:signal(net)`, `+cond:powered(net)`, `+effect:power(net)` — як у Kohctpyktop (підтвердження).
- `+effect:halt` — схема зупиняє власну симуляцію.
- `+role:wire`, `+role:pin` — підтвердження.
- `+window:truth-table`, `+window:assembly-editor`, `+window:component-factory`.
- `+ui:wire-probe`, `+feature:custom-components`, `+card:custom-assembly-language`.

## Джерела
- ⭐ [Steam: Turing Complete](https://store.steampowered.com/app/1444480/Turing_Complete/) — драбина NAND → CPU → асемблер, власна мова асемблера, IO-компоненти, 70+ рівнів, ранній доступ з 2.10.2021.
- [Turing Complete Wiki: Level Guides](https://turingcomplete.wiki.gg/wiki/Level_Guides) — 92 рівні у 7 розділах.
- [Turing Complete Wiki: Components](https://turingcomplete.wiki.gg/wiki/Components) — повний список компонентів.
- [Turing Complete Wiki: General Guides](https://turingcomplete.wiki.gg/wiki/General_Guides) — схеми, карти Карно, автомати станів.
- [Лідерборд](https://turingcomplete.game/leaderboard) — лінк з вікі.
- YouTube: пошук «turing complete game gameplay».

## Непевне
- (?) Система оцінки (вартість вентилів + затримка, такти для програм) — з памʼяті; на відкритих сторінках не описано.
- (?) Як саме тягнуться дроти (по клітинах чи довільно), обертання, кнопки симуляції, редактор власних компонентів — з памʼяті.
- (?) Назви архітектур кампанії (OVERTURE, LEG) — OVERTURE видно лише як назву опційного рівня.
- (?) Чи тести генеруються випадково (`random: setup`).
