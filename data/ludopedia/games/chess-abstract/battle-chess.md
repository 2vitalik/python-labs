---
title: Battle Chess
slug: battle-chess
aka: [Battle Chess Enhanced, Battle Chess 4000, "Battle Chess: Game of Kings"]
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: none
  goal: state
year: 1988
platforms: [Amiga, MS-DOS, C64, NES, Mac, Apple IIGS, Atari ST, 3DO, CDTV, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Battle_Chess", best: true, note: "стандартні правила, 35 анімацій взяття, 2D-режим, бібліотека дебютів, режими гри, сиквели"}
  - {kind: steam, url: "https://store.steampowered.com/app/622830/Battle_Chess/", note: "перевидання: 10 рівнів AI, гра компʼютера з собою, split-screen PvP"}
  - {kind: steam, url: "https://store.steampowered.com/app/200150/Battle_Chess_Game_of_Kings/", note: "Battle Chess: Game of Kings (2015)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Battle+Chess+1988+all+captures", note: "пошук; усі анімації взять"}
stage: v1
coverage: 60
mechanics: [piece-move-patterns, piece-capture, checkmate, check-stalemate, movement-animation, death-animation, event-effects, sound-effects, gui-render, dual-frontends, logic-render-split, ai-opponent, difficulty-levels, hot-seat, online-multiplayer, attract-demo, game-screen, main-menu, settings-window, tutorial-window, +capture-cutscene, +opening-book]
proposes: ["+effect:play_cutscene", "+feature:render-mode-toggle", "+feature:ai-vs-ai", "+card:capture-cutscene", "+card:opening-book"]
author: opus
date: 2026-11-09
---

# Battle Chess — звичайні шахи, де кожне взяття — анімована сутичка двох фігур

## Суть
Правила — стандартні шахи (`chess.md`), без жодної зміни. Новизна — подача: фігури — живі воїни, що ходять полем, а взяття розігрується як короткий бій, у якому атакуючий **завжди** перемагає (35 різних анімацій на пари «хто кого»). Межовий приклад «шкурки»: та сама логіка, інший рендер; є навіть 2D-режим без анімацій — той самий двіжок з іншим фронтендом.

## Поле і час
- Дошка 8×8 у ізометричній проекції; фігури — анімовані спрайти. Альтернативний 2D-вид згори без анімацій.
- Покроково; час на хід визначає рівень AI; анімація ходу/бою — неінтерактивна вставка між ходами.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фігури (король, ферзь, тура, слон, кінь, пішак) | piece | як у `chess.md` | ходи стандартні; рух анімовано кроками воїна |
| Пара «атакуючий × жертва» | — | 35 анімацій | при взятті програється бій, жертва гине (напр., тура стає камʼяним монстром і розчавлює пішака) |
| Король під матом | piece | — | фігура, що оголосила мат, бʼється з королем і перемагає |

## Правила (КОЛИ → ЯКЩО → ТО)
- Правила ходу, взяття, рокіровки, перетворення, мату, нічиїх — як у `chess.md`.
- КОЛИ `input(move(piece, to))` → ЯКЩО `legal(move)` → ТО `animate(walk(piece, to))`, `move(piece, to)`, `end_turn`.
- КОЛИ `contact(piece, enemy_piece)` (взяття) → ЯКЩО `mode(3d)` → ТО `custom: «програти анімацію бою пари (attacker, victim)»` (`+effect:play_cutscene`) → `disappear(enemy_piece)`.
- КОЛИ `contact(piece, enemy_piece)` → ЯКЩО `mode(2d)` → ТО `disappear(enemy_piece)` без анімації.
- КОЛИ `custom: «мат»` → ТО `custom: «фігура, що матує, бʼється з королем»`, `win`.
- Перемога: мат · Нічия: як у шахах · Рахунок: 1 / ½ / 0.

## Керування і ввід
- Вибір фігури і клітини курсором (миша / джойстик / стрілки на консолях) (?).
- Під час анімації ввід неактивний; 2D-режим прибирає паузи анімацій.

## Вікна, меню, HUD
- `game-screen`: ізометрична дошка з анімованими фігурами; перемикання в 2D-вид згори.
- `main-menu` / `settings-window` (?): сторони (людина / компʼютер), рівень AI, вид 2D/3D, звук.
- `tutorial-window` (версія CDTV): озвучений вступ, що пояснює ходи фігур для новачків.
- `end-screen`: анімація мату як фінальна сцена (?).
- Переходи: main-menu → game-screen → (мат) фінальна сцена → main-menu.

## Фічі поза полем
- `ai-opponent-levels` — 10 рівнів (перевидання на Steam); бібліотека дебютів понад 30 000 ходів (крім версій C64 і Apple II) (`+opening-book`).
- `hotseat`; null-modem і LAN у частині портів; перевидання — shared/split-screen PvP і Remote Play Together.
- Режим «компʼютер грає сам із собою» (`+feature:ai-vs-ai`, близько до `attract-demo`).
- `animation-toggle` через 2D-режим (`+feature:render-mode-toggle`); цифрові звуки (на MS-DOS — через PC speaker).

## Варіації й родичі
- Сиквели: Battle Chess II: Chinese Chess (1990, на основі сянці — `xiangqi.md`); Battle Chess 4000 (1992, науково-фантастична пародія, пластилінова анімація); Battle Chess Enhanced (1991, VGA і CD-музика); Battle Chess: Game of Kings (2015, Steam); Battle Chess 3 скасовано.
- Протилежна вісь — Archon (Steam-пошук показує Archon Classic): там взяття не гарантоване, а вирішується бойовою аркадою (?).
- Інші «шкурки» з тими ж правилами — шахи з тематичними фігурами (`theme-select` у `chess.md`).
- **Осі варіацій**: взяття (миттєве / анімація-вставка / бій, що вирішує результат) · рендер (2D / ізометрія / 3D) · хто перемагає в сутичці (завжди атакуючий / за статами — сімʼя `tactics`).

## Цікавинки для курсу
- Розділення логіки й рендеру: той самий шаховий двіжок, два фронтенди (2D і анімований) — 🥈 (картка `dual-frontends`).
- Таблиця анімацій взяття за парою типів (6×6 → лише наявні пари, решта — загальна) — 📎.
- Черга подій двіжка → програвач анімацій, ввід блокується до кінця вставки — 🥉.
- Бібліотека дебютів як словник «позиція → хід» перед пошуком AI — 🥉.
- Режим AI проти AI як демо — 🌱.

## Мапа на каталог
- Є: `piece-move-patterns`, `piece-capture`, `checkmate`, `check-stalemate` ↔ стандартні шахи · `movement-animation` ↔ кроки воїна · `death-animation` ↔ загибель жертви · `event-effects`, `sound-effects` · `gui-render`, `dual-frontends`, `logic-render-split` ↔ 2D/ізометрія · `ai-opponent`, `difficulty-levels` ↔ 10 рівнів · `hot-seat`, `online-multiplayer` ↔ null modem / LAN · `attract-demo` ↔ AI проти AI · `game-screen`, `main-menu`, `settings-window`, `tutorial-window`.
- **Нема** → пропозиції карток:
  - `+capture-cutscene` «Анімація-вставка на подію» · interface/graphics · 📎 · слоти {by_pair} — неінтерактивна сцена за типом подій, ввід заблоковано.
  - `+opening-book` «Бібліотека дебютів AI» · game-logic/opponent · 🥉 — ходи з книги до початку пошуку.

## Пропозиції до словників
- `+effect:play_cutscene` — програти неінтерактивну вставку (анімацію бою) і лише потім продовжити.
- `+feature:render-mode-toggle` — перемикання виду (2D / анімований) без зміни логіки.
- `+feature:ai-vs-ai` — компʼютер грає сам із собою (перегляд).
- `+card:capture-cutscene` · `+card:opening-book` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Battle Chess](https://en.wikipedia.org/wiki/Battle_Chess) — Interplay, 1988 (Amiga), порти до 1994; стандартні правила; 35 анімацій бою; мат — бій з королем; 2D-режим; CDTV-вступ; hotseat, null modem, LAN; дебютна база >30 000 ходів; сиквели; 250 000 копій до лютого 1993.
- [Steam: Battle Chess](https://store.steampowered.com/app/622830/Battle_Chess/) — 10 рівнів, компʼютер проти себе, split-screen PvP.
- [Steam: Battle Chess: Game of Kings](https://store.steampowered.com/app/200150/Battle_Chess_Game_of_Kings/) — сучасний перезапуск 2015.
- YouTube: пошук «Battle Chess 1988 all captures».

## Непевне
- (?) Склад меню, налаштувань, наявність take back і setup board — Wikipedia не описує, MobyGames віддав 403, WebSearch вичерпано.
- (?) Чи 10 рівнів AI — лише в перевиданні чи й в оригіналі.
- (?) Archon як протилежність (взяття вирішується боєм) — з памʼяті, сторінку не відкривав.
- (?) Фінальна сцена мату як окремий `end-screen` — припущення.
