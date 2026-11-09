---
title: Lup Salad (Rupupu Cube)
slug: lup-salad
aka: [るぷぷキューブ ルプ★さらだ, "Rupupu Cube: Lup Salad", Lupupu Cube, ルプ★さらだ, "Lup★Salad DS"]
family: grid-platformer
also: [falling-match]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 1996
platforms: [PlayStation, Nintendo DS (2008), PSP (2010), PlayStation Archives / PSN (2010)]
links:
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/%E3%83%AB%E3%83%97%E2%98%85%E3%81%95%E3%82%89%E3%81%A0", best: true, note: "Salad штовхає блоки, ≥3 однакових суміжних зникають; порти DS/PSP/Archives; Famitsu: підказки після невдач"}
  - {kind: other, url: "https://gametyrant.com/news/rupupu-cube-lup-salad-review-a-challenging-ps1-puzzle-gem", note: "огляд: лише вліво-вправо, стрибок тільки вперед, блоки падають і чавлять, 10 світів × 10, Reset Puzzle з лічильником, 2P Line Clear"}
  - {kind: other, url: "https://www.vgdb.co/games/rupupu-cube-lup-salad", note: "довідка: Fupac, Datam Polystar, PSN Import"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Lup+Salad+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [move-by-input, push-object, gravity-fall, line-match-clear, environment-death, impassable-cells, restart-level, sequential-levels, game-pause, pause-menu, game-screen, +push-only-sideways, +forward-only-jump, +wildcard-block, +color-bomb-block, +reset-counter, +hint-after-fails, +clear-all-colored, +glued-block-group]
proposes: ["+trigger:crushed", "+cond:same_or_wild", "+effect:clear_color", "+ui:reset-counter", "+card:wildcard-block", "+card:color-bomb-block", "+card:clear-all-colored"]
author: opus
date: 2026-11-09
---

# Lup Salad — дівчинка Salad штовхає кольорові блоки, вони падають, і три однакових поряд зникають; мета — прибрати всі

## Суть
Пазл-платформер з видом збоку за мангою Ідзумі Такемото: на одному екрані — Salad і купи кольорових блоків. Вона ходить лише вліво-вправо, штовхає блок перед собою, стрибає тільки вперед; блоки без опори падають, а три й більше однакових суміжних зникають. Мета стадії — прибрати всі кольорові блоки; необережний поштовх знизу стосу може обвалити блок на саму Salad. Родич [puzznic](../falling-match/puzznic.md), але з аватаром замість курсора.

## Поле і час
- Один екран-стадія, вид збоку, клітинна сітка блоків (?), гравітація для блоків.
- Real-time рух героїні; таймера в джерелах нема (?).
- 10 світів × 10 стадій = 100 (огляд); кожен світ — історія, яку тато розповідає Salad; між стадіями — сюжетні сцени (JA-вікі).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Salad | player | напрям погляду | ходить вліво-вправо; швидкий розворот легким натиском назад; стрибок лише вперед («push-jump»); штовхає блок збоку |
| Кольоровий блок | tile | колір | зсувається поштовхом; без опори падає; ≥3 однакових суміжних зникають |
| Райдужний блок | tile | — | підходить до будь-якого кольору (?) |
| Блок-бомба | tile | — | з'єднаний зі звичайним — зникають усі блоки цього кольору (?) |
| Фіксований блок | static | — | не рухається (?) |
| Блок зі стрічкою | object | група | склеєні: зсунув один — їдуть усі (?) |
| Сталевий блок | static | — | не руйнується; для перемоги прибирати не треба (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ЯКЩО `free(next)` → ТО `move(salad, dir)`; ЯКЩО `not facing(salad, dir)` → ТО `face(salad, dir)` (швидкий розворот).
- КОЛИ `input(dir)` → ЯКЩО `occupied(next, block)` і `free(behind_block)` → ТО `push(block)`; штовхати можна лише сусіда зліва або справа.
- КОЛИ `input(jump)` → ТО `custom: «стрибок уперед за поглядом; на місці не стрибає»`.
- КОЛИ `tick` → ЯКЩО `not supported(block)` → ТО `fall(block)`.
- КОЛИ `custom: «блок падає в клітину Salad»` → ТО `lose`, `restart` (?) — штовхнув низ стосу, верхній блок розчавив.
- КОЛИ `pattern(match(color, 3))` → ТО `clear(group)` — три й більше однакових суміжних (JA-вікі).
- КОЛИ `settled` → ТО `custom: «нові збіги після осідання теж зникають»` (?).
- КОЛИ `pattern(match(color, 3))` → ЯКЩО `custom: «у групі райдужний блок»` → ТО `clear(group)` — райдужний рахується за будь-який колір (?).
- КОЛИ `adjacent(bomb_block, block)` → ТО `custom: «зникають усі блоки цього кольору»` (?).
- КОЛИ `input(dir)` → ЯКЩО `occupied(next, fixed_block)` → ТО `block`.
- КОЛИ `contact(salad, tape_block)` → ЯКЩО `custom: «вся група може зсунутись»` → ТО `custom: «зсувається вся склеєна група»` (?).
- КОЛИ `all_gone(colored_block)` → ТО `win`, `next_level` — сталеві блоки не враховуються (?).
- КОЛИ `input(reset_puzzle)` → ТО `restart`, `counter(resets, +1)` — пункт меню паузи для стадій, що стали нерозв'язними.
- КОЛИ `counter(fails, >=, n)` → ТО `custom: «показати підказку»` (Famitsu: підказки після невдач; n — (?)).
- Перемога: прибрано всі кольорові блоки · Поразка: розчавлення блоком (?) або тупик → Reset · Рахунок — (?).

## Керування і ввід
- Хрестовина: вліво/вправо — хід і поштовх; легкий натиск у протилежний бік — розворот на місці.
- Кнопка стрибка — завжди вперед; Start — пауза з Reset Puzzle (?).

## Вікна, меню, HUD
- `main-menu` → історія (світи) · Line Clear Mode на двох (`mode-select`) (?).
- `dialogue-window` — сюжетні сцени між стадіями.
- `game-screen`: стадія на весь екран; праворуч угорі — лічильник ресетів (`+ui:reset-counter`).
- `pause-menu`: Reset Puzzle (?) і вихід.
- `hints-window` / підказка після невдач (?).

## Фічі поза полем
- `levels-sequential`: 10 світів по 10 стадій.
- `restart-level` з лічильником ресетів; `hint` після невдалих спроб.
- Line Clear Mode на 2 гравців — схожий на Panel de Pon / Columns, але за правилами Lup Salad (огляд); деталі (?).
- Порти: DS (Dimple, 2008), PSP (2010), PlayStation Archives (2010), PSN Import Classic у США (2012, огляд).

## Варіації й родичі
- Родичі: [puzznic](../falling-match/puzznic.md) (блоки зсуваються вбік, падають, однакові зникають — курсором), [block-dude](block-dude.md) (аватар і блоки з гравітацією), [samegame-flood](../falling-match/samegame-flood.md), [columns](../falling-match/columns.md), [panel-de-pon](../falling-match/panel-de-pon.md) (режим Line Clear).
- Осі варіацій: **хто рухає блоки** (курсор — Puzznic / аватар — Lup Salad); **скільки однакових для зникнення** (2 — Puzznic / 3 — Lup Salad); **спецблоки** (джокер / бомба кольору / склеєна група / незнищенний).

## Цікавинки для курсу
- Аватар штовхає блоки на сітці з гравітацією й небезпекою обвалу на себе — 🥉.
- Зникнення груп ≥3 одного кольору (flood fill) і повторна перевірка після осідання — 🥉.
- Блок-джокер і блок-бомба кольору — 📎 кожен.
- Склеєна група блоків, що рухається тільки цілою, — 🥉 (перевірка фронту всієї групи).
- Reset з лічильником + підказка після N невдач — 🌱.
- Розв'язувач стадії (BFS по позиції Salad і розкладці блоків з гравітацією) — 🥇.

## Мапа на каталог
- Є: `move-by-input` · `push-object` · `gravity-fall` · `line-match-clear` (групи ≥3; картка про лінії — найближча) · `environment-death` (розчавлення) · `impassable-cells` (сталь, фіксовані) · `restart-level` · `sequential-levels` · `game-pause` + `pause-menu` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+push-only-sideways` «Штовхати лише сусіда збоку» · entities/legality · 🌱.
  - `+forward-only-jump` «Стрибок лише вперед, не на місці» · entities/move · 🌱.
  - `+wildcard-block` «Блок-джокер до будь-якого кольору» · entities/interact · 📎.
  - `+color-bomb-block` «Бомба прибирає весь колір» · entities/interact · 📎.
  - `+reset-counter` «Лічильник рестартів на екрані» · interface/hud · 🌱.
  - `+hint-after-fails` «Підказка після кількох невдач» · game-logic/difficulty · 📎.
  - `+clear-all-colored` «Прибрати всі блоки, крім незнищенних» · game-logic/win · 🌱.
  - `+glued-block-group` «Наперед склеєна група блоків рухається цілою» · entities/legality · 🥉 (`stick-together` — злипання при контакті, тут склеєно з початку).

## Пропозиції до словників
- `+trigger:crushed(a)` — сутність розчавлено падінням зверху.
- `+cond:same_or_wild(a, b, prop)` — однакові або один із них джокер.
- `+effect:clear_color(color)` — прибрати з поля всі блоки кольору.
- `+ui:reset-counter` — лічильник рестартів стадії.
- `+card:wildcard-block`, `+card:color-bomb-block`, `+card:clear-all-colored` — див. вище.

## Джерела
- ⭐ [Wikipedia JA: ルプ★さらだ](https://ja.wikipedia.org/wiki/%E3%83%AB%E3%83%97%E2%98%85%E3%81%95%E3%82%89%E3%81%A0) — манга і гра: Salad штовхає блоки, ≥3 однакових зникають, головоломки між сюжетом; PS 30.08.1996 (Datam Polystar), DS 31.01.2008 (Dimple), PSP 28.01.2010, Archives 22.09.2010; Famitsu 26/40 — прості правила, підказки після невдач.
- [GameTyrant: огляд](https://gametyrant.com/news/rupupu-cube-lup-salad-review-a-challenging-ps1-puzzle-gem) — рух лише вбік, розворот, стрибок уперед, push-only, блоки падають і чавлять, 10 × 10 стадій, Reset Puzzle і лічильник, нові блоки в пізніх світах, Line Clear Mode на двох.
- [VGDB: Rupupu Cube: Lup Salad](https://www.vgdb.co/games/rupupu-cube-lup-salad) — Fupac, Datam Polystar / GungHo, PSN Import.
- Giant Bomb / MobyGames (бачив лише фрагменти в пошуку, сторінки 403) — спецблоки: райдужний, бомба, фіксований, стрічка, сталь; «зникають від 2 однакових».
- YouTube: пошук «Lup Salad gameplay».

## Непевне
- (?) Скільки однакових треба для зникнення: JA-вікі — «три й більше», пошуковий фрагмент Giant Bomb/MobyGames — «два й більше»; суміжність — по сторонах чи лише в лінію.
- (?) Усі спецблоки — лише з пошукових фрагментів; поведінка не перевірена.
- (?) Чи падає сама Salad, чи може залазити на блок і як далеко стрибає.
- (?) Розчавлення — програш стадії чи життя; чи є каскади після осідання.
- (?) Дата PS: JA-вікі — 30.08.1996, VGDB — 30.10.1996.
- (?) Правила Line Clear Mode, меню й екран підказки — не описані.
- Черга пише «Lupupu Cube»; японська назва るぷぷ читається «Rupupu» (так у VGDB/Giant Bomb).
