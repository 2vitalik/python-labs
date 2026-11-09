---
title: Autonauts
slug: autonauts
aka: []
family: program-robots
also: [build-sim]
klass: hybrid
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: setup
  goal: state
year: 2019
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/979120/Autonauts/", best: true, note: "Denki / Curve, 17.10.2019: Scratch-подібне навчання ботів повтором дій, крафт, колоністи, Settlement Mode, Bot Database"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Autonauts", note: "історія: демо на itch.io 2017, TIGA, сиквел vs. Piratebots (2022)"}
  - {kind: itch, url: "https://denki.itch.io/autonauts", note: "прототип: керування, quickstart навчання бота, ланцюг крафту бота"}
  - {kind: other, url: "https://itch.io/t/118969/autonauts-faq?after=160", note: "FAQ форуму: Teach, Find Nearest у зоні маяка, Data Chip, крик між ботами, паливо Steam Bot"}
  - {kind: other, url: "https://denki.itch.io/autonauts/devlog/46572/scripts-too-shall-pass", note: "devlog: боти передають предмети один одному, пошук у зоні 1 клітини"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=autonauts+gameplay+bot+programming", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [command-program, step-execution, item-pickup, inventory, inventory-limit, cell-click, drag-drop-piece, keyboard-controls, save-game, game-pause, tutorial-window, in-game-editor, +teach-by-demonstration, +repeat-until-condition, +find-nearest-in-area, +work-area-beacon, +bot-crafting-chain, +bot-upgrade-parts, +program-copy-chip, +bot-shout-signal, +bot-to-bot-handoff, +bot-fuel, +colony-needs-tiers, +production-chain-automation, +code-sharing-database]
proposes: ["+feature:teach-by-demo", "+feature:bot-database", "+ui:teach-panel", "+ui:area-circle", "+cond:hands_full(a)", "+cond:hands_empty(a)", "+cond:heard(signal)", "+effect:shout(signal)", "+effect:find_nearest(kind, area)", "+effect:refuel(a)", "+trigger:recorded(action)", "+axis:control"]
author: opus
date: 2026-11-09
---

# Autonauts — покажи боту дію руками, гра запише її блоками, а ти додаси повтор і умову

## Суть
Колонія на клітинній мапі: гравець-автонавт рубає дерева, ставить верстати, робить ботів — і **навчає їх**: натискає Teach, виконує дію сам, а кожен крок записується в програму бота візуальними блоками (як у Scratch). Потім гравець обгортає запис у «Repeat» з умовою, натискає Go — і бот крутить роботу сам. Мета — автоматизувати ланцюги виробництва настільки, щоб колоністи (folk) мали їжу, житло й одяг і «трансцендували»; сила гри — у ланцюжках ботів, що передають ресурси один одному.

## Поле і час
- Квадратна клітинна мапа з деревами, камінням, водою, полями; будівлі ставляться на клітини, частина — лише на підлогу (Simple Flooring).
- Ізометричний 3D-вигляд камери над сіткою (?).
- Час `realtime`: гравець і десятки ботів діють паралельно; програма бота — послідовність блоків.
- Світ генерується (?) — `random: setup`.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Автонавт (гравець) | player | руки, рюкзак | ходить, бере, кладе, використовує інструменти, будує, навчає ботів |
| Робот-працівник (workerbot) | ally | програма, руки, інвентар, частини (голова/рама/привід (?)), паливо/завод | виконує записані блоки; потребує інструмент у руках |
| Steam Bot | ally | паливо — деревина | їде на дровах; сам дозаправляється деревом з інвентаря |
| Дерево / камінь / рослини | resource | — | рубаються/видобуваються інструментом; дерева ростуть знову (?) |
| Інструмент (сокира, кирка, лопата, мотика…) | pickup | знос (?) | без нього дія неможлива |
| Верстат (Crude Bench Saw, Workbench…) | container | рецепт | вкладене → продукт (колода → дошки й жердини; дошки → шестерня) |
| Worker Assembler | spawner | — | шестерня + дошки + жердини → новий бот |
| Сховище (storage) | container | тип, місткість | приймає/віддає один тип предметів (?) |
| Маяк (beacon) | switch | імʼя, радіус | центр і межа зони пошуку «Find Nearest» |
| Колоніст (folk) | neutral | енергія, потреби | сидить; потребує їжі, житла, одягу; рівні задоволення → «трансценденція» |
| Підлога | terrain | — | потрібна під частину будівель |
| Data Chip | pickup | збережена програма | Backup/Restore програми між ботами |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(teach, bot)` → ТО `set_state(bot, recording)`; КОЛИ `input(action)` гравця → ТО `custom: «дія дописується блоком у програму бота»`.
- КОЛИ `input(repeat)` → ТО `custom: «записані блоки обгортаються циклом Repeat»`; умова циклу — forever / N разів / поки руки чи інвентар не повні або не порожні (?).
- КОЛИ `input(go)` → ТО `custom: «бот виконує програму з першого блоку»`.
- КОЛИ `exec(find_nearest kind)` → ЯКЩО `in_range(bot, kind, beacon_area)` → ТО `custom: «ціль — найближчий обʼєкт виду в зоні»`; інакше `custom: «бот чекає / пропускає (?)»`.
- КОЛИ `exec(move_to target)` → ТО `move(bot, target)` (пошук шляху по сітці).
- КОЛИ `exec(use tool on target)` → ЯКЩО `has(bot, tool)` → ТО `custom: «дія інструмента: рубати, копати, косити…»`, `spawn(product)`; інакше `block`.
- КОЛИ `exec(pick_up)` → ЯКЩО `custom: «руки не повні»` → ТО `pickup(bot, item)`.
- КОЛИ `exec(add_to target)` → ЯКЩО `custom: «ціль приймає цей предмет»` → ТО `take(bot, item)`, `give(target, item)`.
- КОЛИ `exec(add_to bot)` → ЯКЩО `custom: «руки отримувача зайняті»` → ТО `custom: «шукати іншого бота, що прийме»`.
- КОЛИ `exec(stow)` / `exec(recall)` → ТО `custom: «предмет між руками й інвентарем»`.
- КОЛИ `exec(shout word)` → ТО `custom: «боти, що слухають word, реагують»` (зв'язок між ботами, напр. GoPlank / StopPlank) (?).
- КОЛИ `counter(fuel, <=, 0)` → ТО `stun(bot)` (зупиняється, «unwound»); КОЛИ `input(feed wood)` → ТО `custom: «дозаправка»` (?).
- КОЛИ `custom: «до верстата додано всі інгредієнти рецепта»` → ТО `spawn(product)`.
- КОЛИ `custom: «Worker Assembler отримав шестерню, дошки й жердини»` → ТО `spawn(workerbot)`.
- КОЛИ `custom: «потреби колоністів закрито на рівні»` → ТО `unlock(next_tier)`; найвищий рівень → `custom: «трансценденція»`.
- КОЛИ `input(backup, data_chip)` → ТО `custom: «записати програму бота на чип»`; `restore` → `custom: «завантажити в іншого бота»`.
- КОЛИ `input(put bot in storage)` → ТО `custom: «програма губилась (ранні версії)»` (?).
- Перемога: нема жорсткої — дерево цілей/планів і трансценденція колоністів · Поразка: нема · Рахунок: —; Settlement Mode — мегаполіс лише з 300 ботів.

## Керування і ввід
- ЛКМ — іти / діяти на клітині; ПКМ — кинути предмет; E — меню будівництва; I — інвентар (drag між руками, рюкзаком і ботами); Space — свисток (обрати ботів поруч).
- Teach / Repeat / Go / Stop — кнопки панелі бота; блоки з програми можна витягти мишею, щоб видалити.
- Маяк: взяти в руки й Z — назвати; область пошуку видно червоним колом.
- `control`: прямий для автонавта + `programmed` запис демонстрацією для ботів.

## Вікна, меню, HUD
- `main-menu` → `mode-select` (кампанія / Settlement Mode / пісочниця (?)) → `save-slots`.
- `game-screen`: мапа, гравець, боти, будівлі; HUD — руки/рюкзак (`inventory-bar`), цілі (`objective-text`).
- `teach-panel` (`code-editor`): список блоків бота, кнопки Teach/Repeat/Go/Stop, поля «Find nearest X in [area]», `instruction-highlight` під час виконання (?).
- `inventory-window` — передача між гравцем і ботами.
- Меню будівництва (`custom-window`): каталог будівель і креслень.
- Дерево цілей/креслень (`custom-window`, «plans»).
- `Bot Database` — обмін кодом ботів (Fully Automated update).
- `pause-menu`, `settings-window`.

## Фічі поза полем
- `teach-by-demo` — головна фіча; `bot-database` для обміну програмами; Data Chip Backup/Restore.
- Прогресія: креслення відкривають нові будівлі, інструменти, апгрейди ботів (більше памʼяті, дальність пошуку, швидкість (?)).
- Settlement Mode — обмеження 300 ботів.
- Збереження гри; туторіал перших кроків.

## Варіації й родичі
- Autonauts vs. Piratebots (2022) — той самий каркас + оборона від армії піратських ботів.
- [The Farmer Was Replaced](the-farmer-was-replaced.md) — ферма й автоматизація, але текстовий код; [Screeps](screeps.md) — колонія з кодом; Factorio-подібні (сімʼя `build-sim`) — автоматизація без програм.
- [Karel](karel.md) і [Lightbot](lightbot.md) — команди пишуться, а не записуються.
- Осі варіацій: **як зʼявляється програма** (написати / зібрати блоками / записати демонстрацією); **цикл** (forever / N / до умови); **координація** (кожен сам / передача з рук у руки / крики-сигнали); **цільова зона** (уся мапа / маяк / клітина).

## Цікавинки для курсу
- Запис дій гравця в програму бота й відтворення в циклі — 🥉.
- `Repeat until` з умовами «руки повні / інвентар порожній» — 📎.
- «Find nearest X у зоні маяка» — BFS/відстань до найближчого обʼєкта виду в радіусі — 🥉.
- Ланцюг ботів, що передають предмет із рук у руки, з пошуком іншого отримувача — 🥈.
- Крики-сигнали між ботами (подія → реакція слухачів) — 🥈.
- Дерево рецептів крафту й автоматичне виробництво до квоти — 🥈.

## Мапа на каталог
- Є: `command-program` ↔ програма бота; `step-execution` ↔ виконання блоків (?); `item-pickup`, `inventory`, `inventory-limit` ↔ руки й рюкзак; `cell-click` ↔ ЛКМ по клітині; `drag-drop-piece` ↔ drag в інвентарі; `keyboard-controls`; `save-game`; `game-pause`; `tutorial-window`; `in-game-editor` ↔ меню будівництва (наближено).
- **Нема** → пропозиції карток:
  - `+teach-by-demonstration` «Запис дій гравця в програму сутності» · game-logic/program · 🥉.
  - `+repeat-until-condition` «Цикл до умови стану (руки повні…)» · game-logic/program · 📎.
  - `+find-nearest-in-area` «Найближчий обʼєкт виду в зоні» · entities/move · 🥉.
  - `+work-area-beacon` «Маяк задає зону роботи» · entities/interact · 📎.
  - `+bot-crafting-chain` «Бот збирається з крафтових частин» · game-logic/economy · 🥉.
  - `+bot-upgrade-parts` «Апгрейд частин бота: памʼять, швидкість, дальність» · entities/state · 🥉.
  - `+program-copy-chip` «Копіювання програми між ботами» · game-logic/program · 🌱.
  - `+bot-shout-signal` «Сигнали-крики між ботами» · game-logic/program · 🥈.
  - `+bot-to-bot-handoff` «Передача предмета іншому боту» · entities/interact · 📎.
  - `+bot-fuel` «Паливо бота, дозаправка» · entities/state · 📎.
  - `+colony-needs-tiers` «Рівні потреб NPC-колоністів» · game-logic/win · 🥈.
  - `+production-chain-automation` «Ланцюг виробництва ресурсів» · game-logic/economy · 🥈.
  - `+code-sharing-database` «Онлайн-база програм гравців» · levels/bank · 🥈.

## Пропозиції до словників
- `+feature:teach-by-demo` — програма записується з дій гравця.
- `+feature:bot-database` — обмін програмами між гравцями.
- `+ui:teach-panel` — панель запису/циклу/запуску бота.
- `+ui:area-circle` — коло зони дії/пошуку на полі.
- `+cond:hands_full(a)` / `+cond:hands_empty(a)` — стан рук/інвентаря сутності (сусід `has`).
- `+cond:heard(signal)` — бот почув сигнал.
- `+effect:shout(signal)` — надіслати сигнал іншим ботам.
- `+effect:find_nearest(kind, area)` — обрати ціль: найближчий обʼєкт виду в зоні.
- `+effect:refuel(a)` — дозаправити сутність.
- `+trigger:recorded(action)` — дія гравця потрапила в запис.
- `+axis:control` — значення `taught` (запис демонстрацією).

## Джерела
- ⭐ [Steam: Autonauts](https://store.steampowered.com/app/979120/Autonauts/) — Scratch-подібне навчання «повтором дій», апгрейди «мозку», колоністи й трансценденція, Settlement Mode (300 ботів), Bot Database.
- [Wikipedia: Autonauts](https://en.wikipedia.org/wiki/Autonauts) — Denki (Данді), демо 2017, реліз 17.10.2019, сиквел vs. Piratebots.
- [itch.io: Autonauts](https://denki.itch.io/autonauts) — керування (ЛКМ/ПКМ/E/I/Space), quickstart Teach → Repeat → Go, ланцюг Bench Saw → Workbench → Worker Assembler.
- [itch.io FAQ](https://itch.io/t/118969/autonauts-faq?after=160) — Teach-вікно, Stow/Recall, Data Chip, крики GoPlank/StopPlank, Find Nearest у зоні маяка, Steam Bot на дровах.
- [Devlog «Scripts Too Shall Pass»](https://denki.itch.io/autonauts/devlog/46572/scripts-too-shall-pass) — передача предметів між ботами, зайняті руки → інший отримувач.

## Непевне
- (?) Повний набір блоків (Move To, Pick Up, Use, Add To, Take From, Drop) і умов Repeat (forever / N разів / руки або інвентар повні/порожні / почув сигнал) — частково з памʼяті; FAQ форуму 2017–2019 міг застаріти, умовні переходи там лише «в планах».
- (?) Енергія ботів: «unwound» згадано, механізм заводу/зарядки звичайних ботів не підтверджено; підтверджено лише паливо-деревину Steam Bot.
- (?) Частини бота (голова/рама/привід), ліміт памʼяті на кількість блоків і що дає кожен апгрейд.
- (?) Чи генерується мапа, ізометрія камери, режими в `mode-select`.
- (?) Консольні версії (PS4/Xbox/Switch) — не перевірено; TrueAchievements про ~250 ботів і програм для всіх планів — лише сніпет пошуку.
- Fandom і wiki.gg віддали 402/401 — у шапку не взято.
