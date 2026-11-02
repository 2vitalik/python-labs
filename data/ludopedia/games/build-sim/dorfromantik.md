---
title: Dorfromantik
slug: dorfromantik
family: build-sim
also: [board-digital, connect-rotate]
klass: cursor
axes:
  field: hex
  time: turn
  opponent: none
  info: partial
  random: runtime
  goal: score
year: 2022
platforms: [PC, Switch, PS5, Xbox Series, macOS]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1455840/Dorfromantik/", best: true, note: "офіційний опис: стос, поворот, квести (вітряк, локомотив, олень), режими Quick/Hard/Custom/Monthly/Creative"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dorfromantik", note: "6 типів країв, видно 3 верхні плитки, ідеальна плитка, історія, настільна версія"}
  - {kind: fandom, url: "https://dorfromantik.fandom.com/wiki/Dorfromantik_Wiki", note: "фан-вікі (фетчеру 402)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=dorfromantik+gameplay+guide", note: "пошук; геймплей"}
  - {kind: wiki, url: "https://en.wikipedia.org/w/index.php?search=Dorfromantik+The+Board+Game&ns0=1", note: "пошук; настільна версія (Spiel des Jahres 2023)"}
stage: v1
coverage: 70
mechanics: [cell-click, hover-highlight, drag-drop-piece, event-points, score-records, leaderboard, daily-puzzle, level-unlock, save-game, save-autosave, game-settings, field-scaling, goal-counter, +edge-matching, +tile-rotate, +tile-stack-resource, +group-quest, +perfect-placement-bonus, +hard-edge-constraint, +tile-preview-queue]
proposes: ["+trigger:input", "+trigger:counter", "+trigger:pattern", "+cond:legal", "+cond:same", "+cond:count", "+effect:rotate", "+effect:score", "+effect:counter", "+effect:unlock", "+role:tile", "+role:zone", "+ui:next-piece-preview", "+ui:remaining-counter", "+ui:legal-move-highlight", "+ui:score", "+ui:popup-text", "+ui:quest-marker", "+window:mode-select", "+window:unlocks", "+feature:custom-rules", "+feature:mode-sandbox", "+feature:leaderboard-online", "+feature:unlockables", "+card:edge-matching", "+cond:edge_match"]
author: opus
date: 2026-11-02
---

# Dorfromantik — викладай гекс-плитки зі стосу, зводь краї, виконуй квести, щоб стос не скінчився

## Суть
Пасьянс на гексах: зі стосу береш верхню плитку, повертаєш і кладеш поруч із уже викладеними. Кожна плитка має 6 країв ландшафту (ліс, село, поле, вода, рейки, пустир); збіг країв дає очки, а **стос плиток — це ресурс-життя**: гра закінчується, коли плитки скінчились. Нові плитки дають квести (групи «досягни N») і ідеальні розміщення (усі 6 країв збіглись). Ядро — локальне обмеження сусідства + глобальні групи-компоненти.

## Поле і час
- Гексагональна нескінченна сітка; стартова плитка в центрі. Плитку можна класти в будь-яку порожню клітину, суміжну з викладеними.
- Шар: лише плитки (кожна — 6 ребер типу) + обʼєкти-квести на них; групи — звʼязні компоненти країв одного типу через межі плиток.
- Хід = одна плитка; часу нема (`turn`, без таймера). Видно 3 верхні плитки стосу (Wikipedia) — `info: partial`, випадковий порядок генерації (`random: runtime`).
- Камера: вільне обертання/зум над 3D-ландшафтом; підсвітка доступних клітин.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка | tile | 6 ребер: forest / village / field / water / rail / barren | кладеться поруч з викладеними, повертається на 60° |
| Край «ліс/село/поле» | zone | тип | «мʼякий»: невідповідність дозволена, але без очок |
| Край «вода» (річка) | zone | тип | «жорсткий»: має стикатися з водою (?) |
| Край «рейки» | zone | тип | «жорсткий»: має стикатися з рейками (?) |
| Озеро / станція | tile | спецребра | станція зʼєднує воду й рейки; озеро — вода без продовження (?) |
| Група (ліс, село, поле, річка, колія) | zone | розмір у плитках / довжина | звʼязна компонента однотипних країв |
| Квест-плитка | tile | тип групи, ціль N | квест належить групі, де лежить; виконання → +плитки, +очки |
| Прапорець «замкни» (?) | tile | тип групи | виконано, коли група повністю замкнена (без відкритих країв) (?) |
| Довгий квест (вітряк, локомотив, олень) | pickup | умова | приклади Steam: вітряк — облямуй 6 полів; локомотив — зʼєднай 10 рейок; олень — ліс із ≥50 деревами |
| Стос плиток | resource | кількість (старт 40) | −1 за хід, + за квести і ідеальні плитки; 0 → кінець гри |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, cell)` → ЯКЩО `custom: «клітина порожня і має ≥1 викладеного сусіда»` and `legal(edges)` → ТО `spawn(tile)`, `counter(stack, -1)`.
- КОЛИ `input(rotate)` → ТО `rotate(tile, 60)` (до розміщення).
- `legal(edges)`: для кожного сусіда — ЯКЩО край water/rail → `edge_match` (той самий тип або станція/озеро) (?); інші краї — завжди дозволені.
- КОЛИ плитку покладено → для кожного ребра з сусідом: ЯКЩО `same(edge_a, edge_b, type)` → ТО `score(+n)` (?).
- КОЛИ плитку покладено → ЯКЩО `custom: «усі 6 сусідів є й усі 6 ребер збіглися»` → ТО **ідеальна плитка**: `counter(stack, +1)` (?), `score(+bonus)`, `popup-text`.
- КОЛИ плитку покладено → `custom: «перерахувати звʼязні групи (union-find за ребрами)»`.
- КОЛИ `counter(group_size, ==, N)` для квесту групи → ТО `counter(stack, +k)`, `score(+q)`, `disappear(quest_marker)`.
- КОЛИ `counter(group_size, >, N)` (перебір) → ТО квест провалено (?) — `disappear(quest_marker)` без нагороди.
- КОЛИ `pattern(region_closed)` для прапорця → ТО квест виконано (?).
- КОЛИ спрацювала довга умова (вітряк, олень…) → ТО `unlock(tile_set|biome)` між партіями.
- КОЛИ `counter(stack, ==, 0)` → ТО `game_over`, `window(end-screen)` з рахунком.
- Поразки як такої нема; мета — максимальний рахунок; «смерть» — порожній стос.

## Керування і ввід
- Миша: наведення на клітину показує привид плитки і підсвітку збігів ребер (зелене/червоне); колесо або клавіші — поворот плитки на 60°; ЛКМ — покласти.
- ПКМ-drag — обертання камери, колесо/зум — масштаб; клік по квесту — підсвітка групи (?).
- Геймпад (Switch/консолі): курсор по гексах, бампери — поворот.

## Вікна, меню, HUD
- `game-screen`: 3D-ландшафт, привид плитки, `next-piece-preview` (3 верхні плитки), `remaining-counter` (плиток у стосі), `score`, `quest-marker` на плитках (тип + число, прогрес групи), `popup-text` (+очки, +плитки, «Perfect»).
- `mode-select`: Classic, Quick, Hard, Custom (свої правила, поширення), Monthly (місячний виклик), Creative (без ліміту плиток).
- `end-screen`: підсумок партії — рахунок, кількість плиток, рекорди.
- `custom-window` «Unlocks/Progress»: довгі задачі, відкриті біоми й плитки.
- `leaderboard` для Monthly (?); `settings-window`: графіка, звук, керування.
- `main-menu`: Continue, New game → `mode-select`, Unlocks, Settings, Quit.
- Переходи: main-menu → mode-select → game-screen → (стос 0) end-screen → main-menu.

## Фічі поза полем
- `unlockables`/`meta-progression`: виконання довгих умов відкриває нові плитки, біоми, квести.
- Режими: `mode-classic`, `mode-zen`/`mode-sandbox` (Creative), `mode-hardcore`-подібний Hard, Quick, `custom-rules` (Custom — правила-набір із кодом поширення (?)), Monthly ≈ `mode-daily` з місячним циклом.
- `save-game`: продовжити партію; `score-records`.
- Undo останньої плитки (?) — не підтверджено.

## Варіації й родичі
- Dorfromantik: The Board Game (2023, кооп, Spiel des Jahres 2023) — та сама механіка на столі (→ `board-digital`).
- Carcassonne (квадратні плитки зі збігом країв, мейпли), Kingdomino, Cascadia, Isle of Skye; Townscaper (без цілей, автотайлінг), Islanders.
- Осі варіацій «збіг країв»: обовʼязковий для всіх / лише для «жорстких» країв / лише за очки · сітка: квадрат / гекс · стос: фіксований / поповнюваний квестами.
- Осі «квест групи»: досягти ≥N / рівно N / замкнути область.

## Цікавинки для курсу
- Гекс-сітка з осьовими координатами, поворот плитки на 60° як циклічний зсув 6 ребер — 📎.
- Перевірка легальності ребер (мʼякі/жорсткі типи) + підсвітка під курсором — 📎.
- Групи через union-find по ребрах, квест «група досягла N» — 🥉.
- Стос як ресурс-таймер: +плитки за квести й ідеальні розміщення — 🌱 (економіка «живеш, поки заробляєш ходи»).
- Ідеальна плитка: всі 6 сусідів існують і збіглися — 🌱.
- Генерація стосу, щоб квести були здійсненні (рандом із «підкрученими» ймовірностями) — 🥈 (?).
- «Monthly»/seed-режим: однаковий стос для всіх + таблиця — 📎.

## Мапа на каталог
- Є: `cell-click` + `hover-highlight` + `drag-drop-piece` (привид плитки) · `event-points` (очки за ребра й квести) · `score-records` + `leaderboard` · `daily-puzzle` (≈ Monthly) · `level-unlock` (біоми) · `save-game` + `save-autosave` · `game-settings` · `field-scaling` (зум) · `goal-counter` (прогрес квесту).
- **Нема** → пропозиції карток:
  - `+edge-matching` «Збіг країв плиток» · entities/legality · 📎 · слоти {edge_types, hard_types} — Carcassonne, Dorfromantik.
  - `+tile-rotate` «Поворот плитки перед розміщенням» · interface/input · 🌱 · слот {step: 90|60}.
  - `+tile-stack-resource` «Стос плиток як ресурс» · game-logic/economy · 🌱.
  - `+group-quest` «Квест на розмір групи» · game-logic/win · 🥉 · слоти {op: >=|==|closed} — union-find.
  - `+perfect-placement-bonus` «Бонус за повний збіг» · game-logic/score · 🌱.
  - `+hard-edge-constraint` «Жорсткі краї мусять зʼєднатися» · entities/legality · 📎.
  - `+tile-preview-queue` «Видно N наступних плиток» · interface/hud · 🌱 (близько до `next-piece-preview`).

## Пропозиції до словників
- `+trigger:input`, `+trigger:counter` (група = N, стос = 0), `+trigger:pattern` (`region_closed`).
- `+cond:legal`, `+cond:same`, `+cond:count`; новий `+cond:edge_match` — ребро плитки збігається з ребром сусіда (тип/сумісність); ширше за `same`, бо є таблиця сумісності (станція = вода + рейки).
- `+effect:rotate`, `+effect:score`, `+effect:counter`, `+effect:unlock`.
- `+role:tile`, `+role:zone` (групи).
- `+ui:next-piece-preview`, `+ui:remaining-counter`, `+ui:legal-move-highlight`, `+ui:score`, `+ui:popup-text`; новий `+ui:quest-marker` — маркер квесту на клітині з числом/прогресом.
- `+window:mode-select`; `+window:unlocks` — екран довгих задач і відкритого (поки що `custom-window`).
- `+feature:custom-rules`, `+feature:mode-sandbox`, `+feature:leaderboard-online`, `+feature:unlockables`.
- `+card:edge-matching` — див. вище.

## Джерела
- ⭐ [Steam: Dorfromantik](https://store.steampowered.com/app/1455840/Dorfromantik/) — суть циклу (бери, повертай, клади), квести з прикладами, режими Quick/Hard/Custom/Monthly/Creative, розблокування біомів.
- [Wikipedia](https://en.wikipedia.org/wiki/Dorfromantik) — стос 40, видно 3 верхні, 6 типів країв, очки за збіги, +плитки за квести й повний збіг 6 сусідів, настільна версія.
- [Dorfromantik Fandom](https://dorfromantik.fandom.com/wiki/Dorfromantik_Wiki) — фан-вікі (фетчеру недоступна).
- YouTube: пошук «dorfromantik gameplay guide».

## Непевне
- (?) Точна формула очок за ребро/квест/ідеальну плитку і скільки плиток дає квест — не знайдено.
- (?) Квест «рівно N» з провалом при переборі vs «щонайменше N»; прапорці «замкни область» — з памʼяті.
- (?) Жорсткість країв води й рейок (заборона ставити невідповідно) і роль станцій/озер — з памʼяті, Wikipedia не підтверджує.
- (?) Undo останньої плитки, leaderboard для Monthly, код поширення Custom-правил — не перевірено.
- WebSearch вичерпано, fandom недоступна (402).
