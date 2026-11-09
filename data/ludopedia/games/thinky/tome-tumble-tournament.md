---
title: Tome Tumble Tournament
slug: tome-tumble-tournament
aka: [TTT]
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2024
platforms: [web, PC]
links:
  - {kind: itch, url: "https://terzalo.itch.io/tome-tumble-tournament", best: true, note: "джем-версія в браузері (HTML5), коментарі гравців"}
  - {kind: steam, url: "https://store.steampowered.com/app/3596820/Tome_Tumble_Tournament/", note: "повна версія (TBA): опис твісту, заклинання"}
  - {kind: other, url: "https://terzalo.itch.io/tome-tumble-tournament/devlog/928284/tome-tumble-tournament-has-a-steam-page-and-a-trailer", note: "девлог 2025-04-19: замерзання води, ідоли, порожнисті блоки, драбини, ями"}
  - {kind: other, url: "https://itch.io/jam/thinky-puzzle-game-jam-4/rate/2806792", note: "сторінка в Thinky Puzzle Game Jam 4"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Tome+Tumble+Tournament+gameplay", note: "пошук; геймплей і трейлер"}
stage: v1
coverage: 40
mechanics: [move-4dir, keyboard-controls, push-object, multi-cell-size, orientation-state, environment-death, floor-types, inertia-slide, level-select, undo-unlimited, restart-level, +roll-block, +orientation-goal, +mirrored-second-move, +player-only-passable, +spell-on-open]
proposes: ["+card:orientation-goal", "+card:player-only-passable", "+card:spell-on-open"]
author: opus
date: 2026-11-09
---

# Tome Tumble Tournament — Sokoban з книгою-блоком, що розкривається, коли ляже на корінець

## Суть
Джем-гра Dito Seregin (terzalo, Thinky Puzzle Game Jam 4), що росте в комерційну. Чарівник штовхає величезну книгу-фоліант: вона не ковзає, а **перекочується з грані на грань**, як блок у Bloxorz. Книга розкривається, коли ляже на корінець; покласти її обкладинкою донизу — дискваліфікація (бруд псує сторінки). Деякі книги, розкриваючись, кидають заклинання, що тимчасово міняє правила рівня.

## Поле і час
- Квадратна сітка, вид згори в 3D; у повній версії — вертикальний рух (драбини, ями), тобто висоти.
- Покроково; хід = крок героя, книга перекочується на поштовх.
- Розміри книги в клітинах і поля — не зʼясовано (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Чарівник | player | — | крок у 4 напрямки; штовхає книгу; проходить крізь порожнисті блоки |
| Книга-фоліант | object | орієнтація (на яку грань лежить) | від поштовху перекочується на сусідню грань; на корінці — розкрита |
| Книга з чарами | object | заклинання | як книга; розкриття запускає заклинання |
| Вода (калюжі) | terrain | рідка / замерзла | після чар заморозки — тверда й слизька |
| Порожнистий блок | static | — | зупиняє книги й великі обʼєкти, гравця пропускає |
| Деревʼяний ідол | object | великий | після чар повторює рухи гравця |
| Драбина / яма | terrain | висота | вертикальний рух (повна версія) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(player, dir)`.
- КОЛИ `contact(player, book)` → ЯКЩО `custom: «клітини, куди перекотиться книга, вільні»` → ТО `custom: «книга перекочується на наступну грань»`, `face(book, new_orientation)`; інакше `block`.
- КОЛИ `state_on(book, spine_down)` → ТО `set_state(book, open)` — книга розкрита.
- КОЛИ `state_on(book, cover_down)` → ТО `lose` — дискваліфікація («бруд псує сторінки»).
- КОЛИ `state_on(book, open)` → ЯКЩО `has(book, spell)` → ТО `custom: «заклинання тимчасово міняє правила світу»`.
- Заморозка: КОЛИ `state_on(book, open)` → ЯКЩО `same(spell, freeze)` → ТО `set_cell(water, ice)` на всьому рівні — вода тверда й слизька (ковзання — `slide`).
- Ідоли: КОЛИ `input(dir)` → ЯКЩО `state(idols, awake)` → ТО `move(idol, dir)` — повтор руху гравця.
- КОЛИ `contact(book, hollow_block)` → ТО `block`; КОЛИ `contact(player, hollow_block)` → ТО `move(player, dir)`.
- Перемога: `custom: «відкрити книгу(и) в потрібному місці / стані»` (?).

## Керування і ввід
- Клавіатура (крок, undo, restart — є за нотатками оновлень); Esc — вибір рівня («застряг — Esc, обери інший»). Точні клавіші не зʼясовано (?).

## Вікна, меню, HUD
- `level-select` (Esc).
- `game-screen`: 3D-поле; коли книга стоїть на корінці, гравцеві видно розворот сторінки.
- `custom-window` «Run Game» — стартовий екран браузерної версії; сюжетні вставки про турнір (ведучий Tom Lumber) — `dialogue-window` (?).

## Фічі поза полем
- `undo`, `restart-level` (згадані в нотатках оновлень 09.07), `level-select`.
- Повна версія (Steam, TBA): досягнення Steam, хмарні збереження.

## Варіації й родичі
- `games/push-slide/bloxorz.md` — перекочування блоку з орієнтацією як станом; тут блок котить не сам гравець, а аватар поштовхом, і мета — орієнтація («на корінець»).
- `games/thinky/stephens-sausage-roll.md` — штовхання/перекочування довгого обʼєкта з «заборонною» гранню (не підсмажити двічі ↔ не класти обкладинкою вниз).
- Ідоли-повторювачі — як дзеркальні двійники в інших thinky-іграх; замерзла вода — ковзання з `games/push-slide/ice-sliding-puzzles.md`.
- **Осі варіацій:** що котиться — сам аватар / обʼєкт від поштовху; що означає орієнтація — нічого / мета (корінець) / поразка (обкладинка); ефект досягнення стану — нічого / заклинання, що міняє правила.

## Цікавинки для курсу
- Орієнтація кубоїда (6 граней) як стан і перекочування поштовхом — 📎.
- «Стан-мета і стан-поразка» на одному обʼєкті (корінець / обкладинка) — 🌱.
- Глобальне заклинання, що міняє тип клітин рівня (вода → лід), — 🌱; ідоли, що повторюють ввід гравця, — 📎.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls`; `push-object` ↔ поштовх книги; `multi-cell-size` ↔ велика книга (?); `orientation-state` ↔ грань, на якій лежить книга; `environment-death` ↔ дискваліфікація; `floor-types` + `inertia-slide` ↔ лід; `level-select`, `undo-unlimited`, `restart-level`.
- **Нема** → пропозиції карток:
  - `+roll-block` «Блок перекочується з грані на грань» · entities/move · 📎 (уже запропоновано в `bloxorz.md`).
  - `+orientation-goal` «Мета/поразка — орієнтація обʼєкта» · game-logic/win · 🌱.
  - `+mirrored-second-move` «Двійник повторює хід гравця» · entities/move · 📎 (уже пропонувалась).
  - `+player-only-passable` «Клітина пропускає гравця, але не обʼєкти» · entities/legality · 🌱.
  - `+spell-on-open` «Досягнення стану запускає глобальну зміну правил» · game-logic/constraints · 🥉.

## Пропозиції до словників
- `+card:orientation-goal`, `+card:player-only-passable`, `+card:spell-on-open` — механік нема в каталозі.

## Джерела
- ⭐ [itch.io](https://terzalo.itch.io/tome-tumble-tournament) — джем-версія, підказка про Esc, нотатки оновлень (undo/restart), коментарі (зокрема increpare).
- [Steam](https://store.steampowered.com/app/3596820/Tome_Tumble_Tournament/) — «книга розкривається, коли лягає на корінець», «обкладинкою вниз — дискваліфікація», заклинання.
- [Девлог 2025-04-19](https://terzalo.itch.io/tome-tumble-tournament/devlog/928284/tome-tumble-tournament-has-a-steam-page-and-a-trailer) — заморозка води, ідоли, порожнисті блоки, драбини й ями.
- [Сторінка джему](https://itch.io/jam/thinky-puzzle-game-jam-4/rate/2806792) — «A block-rolling puzzle game with a twist».

## Непевне
- (?) Механіку бачив лише в описах: розмір книги в клітинах, чи перекочується вона саме як Bloxorz-блок 1×2, умова перемоги і точні клавіші не перевірено грою (рушій — raylib/WASM, коду для читання нема).
- (?) Рік: джем TPGJ4 і оновлення 07–24.07 — 2024 (черга давала 2025); Steam-версія — дата TBA.
- (?) Чи зупиняє замерзла вода книгу, чи книга теж ковзає по льоду, — невідомо.
- (?) Свисток (коментар increpare «whistle shrill») — звук гри чи дія героя, не зʼясовано.
