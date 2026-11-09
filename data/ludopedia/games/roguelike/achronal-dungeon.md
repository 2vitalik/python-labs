---
title: Achronal Dungeon
slug: achronal-dungeon
aka: []
family: roguelike
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2022
platforms: [web (HTML5), Windows, macOS, Linux]
links:
  - {kind: itch, url: "https://patashu.itch.io/achronal-dungeon", best: true, note: "грати в браузері; суть «зелених» предметів, повне керування, 4 кінцівки, редактор після проходження"}
  - {kind: official, url: "https://github.com/Patashu/Achronal-Dungeon", note: "код на Godot (MIT): GameLogic.gd — формула бою, undo-буфери, зелені події, кінцівки"}
  - {kind: other, url: "https://raw.githubusercontent.com/Patashu/Achronal-Dungeon/main/GameLogic.gd", note: "уся логіка одним файлом"}
  - {kind: other, url: "https://patashu.itch.io/achronal-dungeon/devlog/469939/v13-secret-endings", note: "devlog v1.3: таємні кінцівки й умови"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=kRPn0sJHqZw", note: "проходження автора (спойлери), лінк з README"}
stage: v1
coverage: 65
mechanics: [move-4dir, keyboard-controls, cell-click, hover-highlight, key-and-door, hp-damage, item-pickup, impassable-cells, destructible-blocks, reach-exit, undo-unlimited, restart-level, state-string, replay, in-game-editor, editor-palette, level-exchange, level-metadata, save-progress, status-panel, message-log, sound-effects, keep-playing-after-win, +deterministic-combat, +damage-preview, +critical-value, +stat-gems, +multiple-endings, +undo-immune-objects, +undo-immune-avatar, +meta-restart, +undo-keeps-progress, +point-mirror-warp, +cell-value-multiplier, +no-losing-fight, +run-until-blocked, +auto-pathfind-command, +secret-endings]
proposes: ["+axis:undo=selective", "+feature:meta-restart", "+effect:fight(a, b)", "+effect:stat(a, name, ±n)", "+trigger:undo", "+ui:damage-preview", "+ui:action-preview", "+card:undo-immune-objects", "+card:undo-immune-avatar", "+card:point-mirror-warp", "+card:cell-value-multiplier", "+card:no-losing-fight"]
author: opus
date: 2026-11-09
---

# Achronal Dungeon — однокімнатна Magic Tower, де «зелені» речі переживають undo і рестарт

## Суть
Один екран, один рівень у традиції [magic-tower](magic-tower.md): герой з HP/ATK/DEF іде до виходу крізь стіни, замки й монстрів, бій детермінований і видно, скільки HP він коштує. Підземелля спершу непрохідне: ресурсів замало. Ключ — **Greenality**: заряд, яким можна зробити сусідню річ **зеленою**; взаємодія із зеленою річчю не відкочується ні undo, ні рестартом, тож можна «взяти» предмет у майбутньому й повернутися в минуле з ним. Гра з джему Confounding Calendar 2022 (Thinky Puzzle Games), натхнена Tower of the Sorcerer і Braid.

## Поле і час
- Одна фіксована кімната на квадратній сітці, видима повністю; у коді коментар «31 × 20» для максимальних індексів (тобто ~32×21 клітин (?)).
- Шари (Godot TileMap): підлога/обʼєкти (`FloorMap`), герой (`ActorMap`), **множники** (`MultiplierMap`: число на клітині), «осад» (`ResidueMap`: слід знищених зелених речей), інвентар.
- Хід = крок героя, застосування Greenality або Warp Wings; світ без вводу не змінюється, монстри не ходять.
- Два рівні часу: **turn** (кроки, відкочуються undo/рестартом) і **meta-turn** (усі натискання, включно з undo; рахуються для таємної кінцівки TIMERUN).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | HP 80, ATK 1, DEF 0 на старті (код); ключі, кирки, крила, пов'язки, заряди Greenality | крок 4 напрямки; вхід у клітину = взаємодія |
| Зелений герой | player | стан `green` | після Greenality в дзеркало: undo не повертає його позицію й HP/ATK/DEF |
| Слиз (Slime) | enemy | HP 10·m, ATK 1·m | стоїть; бій ініціює герой |
| Вартовий (Guard) | enemy | HP 5·m, ATK 2·m | те саме |
| Зуби (Teeth) | enemy | HP 3·m, ATK 3·m | те саме |
| Вогонь (Fire) | enemy | HP 2·m, ATK 5·m | те саме |
| Зілля (Potion) | pickup | +m HP | зникає при вході |
| Меч (Sword) | pickup | +m ATK | постійне посилення |
| Щит (Shield) | pickup | +m DEF | постійне посилення |
| Ключ (Key) | pickup | +m ключів | — |
| Замок (Lock) | gate | потрібно m ключів | відкривається, ключі витрачаються |
| Стіна (Wall) | static | потрібно m кирок | руйнується киркою при вході |
| Сталева стіна (Steel) | static | — | непробивна, не стає зеленою |
| Кирка (Pickaxe) | pickup | +m кирок | — |
| Крила (Warp Wings) | pickup | +m крил | X — стрибок у центрально-симетричну клітину |
| Пов'язка (Headband) | pickup | +m | після бою дає +ATK (+DEF), якщо бій був довгим |
| Greenality | pickup | +1 заряд (і назавжди +1 до максимуму) | X+напрям — зробити сусідню річ зеленою |
| Чарівне дзеркало (Magic Mirror) | static | — | непрохідне; Greenality в нього відбивається на героя |
| Ціль (Goal) | static | — | вхід = перемога; кінцівка залежить від відкритих сусідів |
| Зелена версія будь-чого (крім сталі, цілі, Greenality) | — | стан `green` | взаємодія з нею не відкочується undo/рестартом |
| Множник | zone | число m (2…5000) | масштабує значення предмета / стати ворога / вартість стіни чи замка |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell)` → ТО `move(hero, dir)`, `counter(turn, +1)`.
- КОЛИ `contact(hero, potion|sword|shield|key|pickaxe|wings|headband)` → ТО `pickup`, `disappear(item)`, `custom: «HP / ATK / DEF / запас += m»`, `move(hero, dir)`.
- КОЛИ `contact(hero, enemy)` → ЯКЩО `custom: «DEF героя ≥ ATK ворога»` → ТО `custom: «бій без втрат»`; інакше втрата = `(ATK_ворога − DEF) × (ceil(HP_ворога / ATK) − 1)` (герой б'є першим).
- КОЛИ `contact(hero, enemy)` → ЯКЩО `custom: «втрата ≥ поточне HP»` → ТО `block`, `message(«Fighting this … costs N HP»)` — програти бій неможливо.
- КОЛИ `contact(hero, enemy)` → ЯКЩО `custom: «втрата < HP»` → ТО `hp(hero, −втрата)`, `disappear(enemy)`, `move(hero, dir)`.
- КОЛИ `died(enemy)` → ЯКЩО `has(hero, headband)` and `custom: «ATK < HP ворога (бій довший за 1 удар)»` → ТО `custom: «ATK += кількість пов'язок»`; ЯКЩО ще й `custom: «DEF < ATK ворога»` → ТО `custom: «DEF += кількість пов'язок»`.
- КОЛИ `contact(hero, wall)` → ЯКЩО `counter(pickaxes, >=, m)` → ТО `take(hero, pickaxe×m)`, `set_cell(wall, floor)`, `move(hero, dir)`; інакше `block`.
- КОЛИ `contact(hero, steel)` → ТО `block`.
- КОЛИ `contact(hero, lock)` → ЯКЩО `counter(keys, >=, m)` → ТО `take(hero, key×m)`, `disappear(lock)`, `move(hero, dir)`; інакше `block`, `message(«You need m keys»)`.
- КОЛИ `contact(hero, greenality)` → ТО `disappear(greenality)`, `custom: «заряд +1, максимум +1; зберігається на диск, переживає навіть мета-рестарт»`.
- КОЛИ `input(X+dir)` → ЯКЩО `counter(greenality, >=, 1)` and `custom: «сусідня клітина в межах поля, не порожня підлога, не сталь, не Greenality, не ціль, ще не зелена»` → ТО `set_state(thing, green)`, `counter(greenality, −1)`, `counter(turn, +1)`.
- КОЛИ `input(X+dir)` → ЯКЩО `occupied(cell, mirror)` and `not state(hero, green)` → ТО `set_state(hero, green)` (зелене відбивається на героя).
- КОЛИ `input(undo)` → ТО `undo(1)`: відкочується останній хід — ЯКЩО `not state(event, green)`; події із зеленими речами (їхнє зникнення, здобуті HP/ATK/DEF/ключі) лишаються.
- Виняток: КОЛИ `died(green_enemy)` → ТО `custom: «рани від бою НЕ зелені»` — undo повертає HP, а ворог лишається мертвим.
- Виняток: витрачені на зелену стіну/замок кирки й ключі — звичайна подія, undo їх повертає, а стіна/замок лишаються знищеними.
- КОЛИ `input(undo)` → ЯКЩО `state(hero, green)` → ТО `custom: «світ відкочується, а позиція героя і HP/ATK/DEF — ні»` (предмети повертаються на поле, стати лишаються).
- КОЛИ `input(restart)` → ТО `custom: «undo до ходу 0»` (зелене лишається).
- КОЛИ `input(meta_restart)` → ТО `custom: «відкотити всі зелені події, стати й позицію — до старту; заряди Greenality = максимум»`.
- КОЛИ `input(X)` → ЯКЩО `has(hero, wings)` → ТО `take(hero, wings)`, `teleport(hero, (x_max − x, y_max − y))` — клітина призначення обробляється як звичайний вхід (стіна, ворог, предмет).
- КОЛИ `enter(hero, goal)` → ТО `win`; ЯКЩО `state(hero, green)` → GREEN ENDING; ЯКЩО `free(west_of_goal)` → HEROIC; ЯКЩО `free(north|south_of_goal)` → TUNNEL; інакше ASCENT.
- КОЛИ `level_end` → ТО `custom: «перевірити таємні кінцівки»`: SMUGGLER (рівно 2 використані Greenality), CATACLYSM (усі вороги мертві), TELEPORT (0 ходів), SPEEDRUN (< 38 ходів, не зелений), TIMERUN (< 163 мета-ходів), OUCH (1 HP), MAX HP/ATK/DEF (пороги, не зелений), INBOUNDS (без кирки з мета-рестарту), GROUNDED (жодного разу крила).
- Перемога: дійти до цілі. Поразки нема (смертельний бій заборонений, undo без ліміту). Рахунок: після повного проходження — змагання за максимум HP або мінімум ходів (README).

## Керування і ввід
- WASD / стрілки — крок; клік мишею — автошлях A* по порожніх клітинах до цілі (останній крок — вхід у ціль); Shift+напрям — біг до першої перешкоди (предмети підбирає, на стінах/ворогах/замках зупиняється).
- Наведення миші — інспекція клітини (назва, стати, «You would lose N HP», «+N ATK or +1 DEF would help!»).
- Z — undo ходу; Shift+Z — undo окремого кроку; R — рестарт; Esc — мета-рестарт (повертає заряди Greenality).
- X+напрям (або X + клік по сусідній клітині) — Greenality; X окремо — Warp Wings; поки X затиснуто, показано превʼю: зелені версії 4 сусідів і точка стрибка крил.
- Ctrl+C — копіювати реплей (рядок `wasd`/`WASD`/`x`/`z`/`r`); Ctrl+V — вставити реплей або рівень; Ctrl+Shift+C — копіювати рівень; Ctrl+Shift+L — редактор.
- M — звук, P — анімації (або кліки по іконках нотки й слизня).

## Вікна, меню, HUD
- `game-screen`: кімната + `stat-panel` (HP, ATK, DEF, Turn (натискання)) + `inventory-bar` (ключі, кирки, крила, пов'язки, заряди Greenality іконками) + рядок останнього повідомлення + дві колонки `tooltip` (інспекція/керування) + координати клітини + табличка «You are here» + іконки звуку й анімацій.
- `help-window` як частина HUD: список керування росте разом з навчанням (після першого зеленого предмета — Z/R, після Greenality — X/Esc, після крил — X).
- Після перемоги: титри + список здобутих таємних кінцівок у тій самій панелі (`end-screen` без окремого екрана).
- `confirm-dialog` на старті: «завантажити N збережених Greenality?».
- `editor-window` (Ctrl+Shift+L): палітра плиток (колесо миші), шари 1 — підлога / 2 — множники, ЛКМ/ПКМ — поставити/стерти; діалог Level Info (назва, автор); кнопка «New! Features».
- Переходи: старт → `confirm-dialog` (якщо є сейв) → `game-screen` ⇄ `editor-window`; перемога → панель кінцівок → undo/рестарт/мета-рестарт.

## Фічі поза полем
- `undo` без ліміту + `restart-level` + мета-рестарт — три рівні відкату з різною «глибиною» (`+axis:undo=selective`).
- `autosave` прогресу Greenality (v1.4) — зібрані заряди переживають закриття гри.
- `replay` / `share-code`: реплей і рівень як текстові рядки через буфер обміну; кастомні підземелля збирають на GitHub-вікі.
- `level-editor` (v1.5, після проходження) з метаданими рівня; кастомний рівень дає CUSTOM ENDING і не рахує таємних кінцівок.
- `animation-toggle`, `sound-toggle`; `achievements`-подібні таємні кінцівки (12, одна «???»).

## Варіації й родичі
- [magic-tower](magic-tower.md) — батько: стати, детермінований бій, ключі, кирки, крила; [tactical-nexus](tactical-nexus.md) і [towerbound](towerbound.md) — сучасні вежі; [h5mota](h5mota.md).
- Відмінності від Magic Tower: одна кімната замість вежі; ворог не має DEF; смертельний бій заборонений; множники на клітинах; головне — **вибіркова незворотність** (зелене).
- Braid — джерело ідеї «обʼєкти, що не підкоряються перемотуванню» (зелені ключі там світяться так само).
- Автор рекомендує Deep Rune (J.C. Bailey) як схожу гру.
- Осі варіацій: **що переживає undo** (нічого / окремі обʼєкти / аватар / метапрогрес) · **ціна бою** (кидки / формула / формула + заборона смертельного) · **рух** (крок / біг / автошлях / стрибок-дзеркало) · **кінцівки** (одна / за способом входу до цілі / таємні за рекордами).

## Цікавинки для курсу
- Два undo-буфери: звичайний стек ходів і «мета»-список зелених подій; restart = undo до нуля; meta-restart = ще й мета-список — 🥉 (event sourcing з двома журналами).
- Зелений аватар: undo відкочує світ, але не героя → дублювання предметів — 🥈 (тонкі інваріанти при частковому відкаті).
- Формула бою з прогнозом і підказкою «скільки ATK до меншої кількості ударів» — 🌱.
- Заборона бою, що вбив би: поразки нема, є лише софтлок, який лікує undo — 🌱.
- Warp Wings: точка `(x_max − x, y_max − y)` + звичайна обробка входу в клітину — 🌱.
- Кінцівка за тим, який сусід цілі відкритий (зі сходу, згори/знизу, жоден) — 🌱.
- Реплей як рядок символів з різними літерами для кроку / Greenality / undo / рестарту — 📎.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` · `cell-click` (автошлях) · `hover-highlight` (інспекція) · `key-and-door` (замки на m ключів) · `hp-damage` · `item-pickup` · `impassable-cells` (сталь, дзеркало) · `destructible-blocks` (стіна + кирка) · `reach-exit` · `undo-unlimited` + `restart-level` · `state-string` + `replay` (реплей і рівень рядком) · `in-game-editor` + `editor-palette` + `level-exchange` + `level-metadata` · `save-progress` (заряди) · `status-panel` · `message-log` (рядок повідомлення) · `sound-effects` · `keep-playing-after-win`.
- **Нема** → пропозиції карток:
  - `+undo-immune-objects` «Обʼєкти, взаємодія з якими переживає undo/рестарт» · game-logic/history · 🥈 · слот {що саме лишається: зникнення, ефект, рани}.
  - `+undo-immune-avatar` «Аватар поза undo: світ відкочується, герой ні» · game-logic/history · 🥈.
  - `+meta-restart` «Рестарт глибший за рестарт: скинути все, крім знань/зарядів» · game-logic/history · 🌱.
  - `+point-mirror-warp` «Стрибок у центрально-симетричну клітину» · entities/interact · 🌱.
  - `+cell-value-multiplier` «Множник на клітині масштабує обʼєкт» · entities/state · 🌱.
  - `+no-losing-fight` «Смертельний бій заборонено» · entities/combat · 🌱.
  - `+run-until-blocked` «Біг до першої перешкоди» · entities/move · 🌱.
  - `+secret-endings` «Таємні кінцівки за рекордами» · game-logic/win · 📎; повтори з корпусу: `+deterministic-combat`, `+damage-preview`, `+critical-value`, `+stat-gems`, `+multiple-endings`, `+undo-keeps-progress`, `+auto-pathfind-command`.

## Пропозиції до словників
- `+axis:undo=selective` — значення осі `undo`: частина стану (позначені обʼєкти) не відкочується.
- `+feature:meta-restart` — скидання глибше за рестарт з поверненням зарядів.
- `+effect:fight(a, b)`, `+effect:stat(a, name, ±n)` — повтор пропозицій сімʼї Magic Tower.
- `+trigger:undo` — подія «гравець скасував хід» (тут правила залежать від того, що саме відкочується).
- `+ui:damage-preview` — втрата HP при наведенні на ворога; `+ui:action-preview` — превʼю результату дії на сусідніх клітинах, поки затиснута клавіша.
- `+card:undo-immune-objects`, `+card:undo-immune-avatar`, `+card:point-mirror-warp`, `+card:cell-value-multiplier`, `+card:no-losing-fight` — див. «Мапу на каталог».

## Джерела
- ⭐ [itch.io: Achronal Dungeon](https://patashu.itch.io/achronal-dungeon) — гра в браузері, опис зелених предметів, усе керування, 4 кінцівки, редактор, сейви Greenality.
- [GitHub: Patashu/Achronal-Dungeon](https://github.com/Patashu/Achronal-Dungeon) — README (керування, рахунок за HP/ходами).
- [GameLogic.gd](https://raw.githubusercontent.com/Patashu/Achronal-Dungeon/main/GameLogic.gd) — стати ворогів, формула бою, заборона смертельного бою, пов'язка, крила, два undo-буфери, зелений герой, кінцівки й таємні кінцівки.
- [Devlog v1.3: Secret Endings](https://patashu.itch.io/achronal-dungeon/devlog/469939/v13-secret-endings) — 12 таємних кінцівок, їхні пороги й історія змін.
- [YouTube: проходження автора](https://www.youtube.com/watch?v=kRPn0sJHqZw) — лінк з README (спойлери; агент не дивився).

## Непевне
- (?) Розмір кімнати: у коді лише коментар «31 / 20» до максимальних індексів.
- (?) Пов'язка: підказка в грі каже «+1 ATK, якщо не вбив з одного удару, і +1 DEF, якщо отримав шкоду» (незалежно), а код дає +DEF лише всередині умови на ATK і додає кількість пов'язок, а не 1.
- (?) Пороги MAX HP / MAX DEF: devlog — 1796 / 73, код (правка 2026-05) — 1966 / 75; SMUGGLER LORD у коді — рівно 1 використана Greenality.
- (?) Скільки всього Greenality у кімнаті (у коментарях — «ще дві, добре охоронені»), і чи редактор справді відкривається лише після проходження (так каже itch; у коді — просто Ctrl+Shift+L).
