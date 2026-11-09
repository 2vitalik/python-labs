---
title: Maze War
slug: maze-war
aka: [Maze, Mazewar, MazeWar, Maze Wars]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: online
  info: hidden
  random: none
  goal: score
year: 1973
platforms: [Imlac PDS-1, PDP-10 (MIT), Xerox Alto, X Window, Macintosh, NeXTSTEP, Palm OS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Maze_(1973_video_game)", best: true, note: "рух клітинами, повороти на 90°, підглядання, +10/−5, 2 с захисту, роботи, редактор, версії"}
  - {kind: other, url: "https://digibarn.com/collections/games/xerox-maze-war/", note: "DigiBarn: Xerox-версія, очі-аватари, карта знизу, стріляти в спину, «Maze Lords»"}
  - {kind: other, url: "https://digibarn.com/collections/games/xerox-maze-war/maze-documentation/index.htm", note: "фото й підписи до Imlac-версії, апаратна версія 1976"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=maze+war+xerox+alto+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-by-input, orientation-state, impassable-cells, projectile-shot, shoot-forward, line-of-sight-attack, event-points, respawn, minimap-radar, fog-of-war, online-multiplayer, ai-opponent, realtime-ai, cheat-codes, level-from-txt, player-camera, +first-person-grid-view, +peek-around-corner, +hit-invulnerability-window, +hit-penalty-score, +bot-slows-after-score, +spectator-overview, +text-message-to-player]
proposes: ["+effect:peek", "+ui:first-person-view", "+feature:spectator-overview", "+axis:view", "+card:peek-around-corner", "+card:hit-invulnerability-window"]
author: opus
date: 2026-11-09
---

# Maze War — перший мережевий шутер від першої особи: кроки клітинами, повороти на 90°, постріл у спину

## Суть
Кожен гравець — око в клітинному лабіринті, яке бачить коридор від першої особи. Хід — крок на клітину вперед/назад або поворот на 90°, постріл летить по коридору й влучає в першого гравця на шляху. Влучання дає +10, пропущений постріл −5; після влучання жертва має дві секунди, щоб утекти. Гра 1973 року, з якої виросли мережеві FPS, боти, редактор рівнів і перші читери.

## Поле і час
- Пласка сітка клітин «порожньо / стіна», стіни однакової висоти; є дефолтний лабіринт і власні (MIT-версія — 16×32).
- Камера — від першої особи в напрямку погляду; поруч чи знизу — вид згори з **лише своєю** позицією (суперників на карті не видно). Ранні версії накладали карту поверх виду.
- Real-time: усі гравці діють одночасно, кожне натискання — один крок або поворот. Спільний стан тримав сервер PDP-10 (MIT) або машини обмінювались напряму по Ethernet (Xerox Alto).
- Апаратна версія 1976 — куб 16×16×16 без гравітації (рух угору/вниз); у корпусі не описується окремо.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець (око / 3-літерний ID зі стрілкою) | player | очки, напрямок погляду | крок уперед/назад, поворот ліворуч/праворуч/назад, підглядання, постріл |
| Суперник-людина | enemy | очки | те саме з іншого термінала; видно, лише коли в одному коридорі |
| Робот (бот) | enemy | поріг очок | простий алгоритм руху й стрільби; після порогу очок сповільнюється |
| Куля | projectile | швидка | летить прямо від стрільця, влучає в першого гравця на шляху |
| Стіна | static | — | непрохідна; обмежує видимість і кулі |
| Підлога (порожня клітина) | static | — | прохідна |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(forward|back)` → ЯКЩО `free(cell_ahead|cell_behind)` → ТО `move(player, dir)`; інакше `block`.
- КОЛИ `input(turn_left|turn_right)` → ТО `face(player, ±90)`; КОЛИ `input(about_face)` → ТО `face(player, 180)`.
- КОЛИ `input(peek_left|peek_right)` → ТО `custom: «показати вид, ніби гравець ступив і повернув, але він лишається на місці»` (`+effect:peek`); ЯКЩО `state(player, peeking)` → `input(fire)` не діє.
- КОЛИ `input(fire)` → ТО `spawn(bullet)` у напрямку погляду.
- КОЛИ `tick` → ЯКЩО `free(cell_ahead_of_bullet)` → ТО `move(bullet, dir)`; інакше `disappear(bullet)`.
- КОЛИ `contact(bullet, player_b)` → ЯКЩО `not state(player_b, invulnerable)` → ТО `disappear(bullet)`, `score(+10)` стрільцю, `custom: «жертві −5 очок»`, `set_state(player_b, invulnerable, 2 s)`.
- КОЛИ `line_of_sight(player_a, player_b)` → ТО `reveal(player_b)` у виді від першої особи (око видно і видно, куди воно дивиться).
- КОЛИ `line_of_sight(player_a, player_b)` → ЯКЩО `not facing(player_b, player_a)` → ТО `custom: «B не бачить A — можна стріляти безпечно»` (засідка, постріл у спину).
- КОЛИ `counter(score_bot, >=, limit)` → ТО `speed(bot, −)` (боти MIT-версії були надто сильні).
- КОЛИ `input(message)` → ТО `message(text)` на екрані іншого гравця.
- КОЛИ `input(cheat_command)` → ТО `custom: «гравець проходить крізь стіни»` (чит Thompson-а).
- Перемога: формальної нема — гра триває, рахунок порівнюється на табло. Поразка: нема, лише −5. Рахунок: +10 за влучання, −5 за отримане.

## Керування і ввід
- Клавіші: крок уперед, крок назад, поворот ліворуч/праворуч, розворот, підглядання ліворуч/праворуч, постріл (точні клавіші залежать від версії).
- Xerox Alto: ліва рука — 5-клавішний keyset акордами, права — миша.
- Текстове повідомлення іншому гравцю — зі свого термінала.

## Вікна, меню, HUD
- `game-screen` — вид від першої особи (`+ui:first-person-view`) згори, карта-лабіринт знизу з власною позицією (`minimap`), табло `score` усіх гравців збоку/знизу.
- Maze Watcher (окрема програма на терміналі LDS-1) — вид згори на всю гру для глядачів (`+feature:spectator-overview`).
- Вибір лабіринту / резерв терміналу — поза грою (адміністрування лабораторії).
- Переходи: вхід у гру з термінала → game-screen; вихід — закрити програму.

## Фічі поза полем
- `online-multiplayer` — 2 гравці (серійний кабель), до 8 (MIT, сервер PDP-10), далі ARPANET між інститутами (MIT ↔ UC Santa Cruz) з поправкою на мережеву затримку; Alto — peer-to-peer по Ethernet; Maze Wars+ — до 30 гравців по AppleTalk.
- `ai-opponent-levels` — роботи замість відсутніх людей; в апаратній версії складність ботів регулювалась швидкістю заліза.
- `level-editor` — програма Lebling-а для власних лабіринтів, названа першим редактором рівнів.
- `chat` — текст на екран суперника.
- `spectator` — Maze Watcher.
- Анти-фічі історії: «Maze Guncher» (адміністратор вбивав ігри), читерські збірки «Maze Lords» з показом усіх позицій → автори зашифрували вихідний код.

## Варіації й родичі
- X MazeWars (1986, X Window), **Maze Wars+** (1987, Mac: 4 типи роботів, телепорти, тонкі стіни-лінії, 5 аватарів), **MIDI Maze** (1987, Atari ST, мережа по MIDI) → Faceball 2000, Super MazeWars (1992), Oracle Maze (1992), MazeWars для NeXT і Palm.
- Родичі в корпусі: `3d-monster-maze` (той самий вид від першої особи в клітинному лабіринті, але один ворог-AI), `combat` / `battle-city` (стрілянина в лабіринті згори), `wizard-of-wor` (стрілянина в лабіринті з радаром).
- **Осі варіацій:** вид (від першої особи / згори / обидва); що видно на карті (лише себе / усіх — чит); рух (дискретні клітини / вільний); стіни (клітини / лінії-ребра); суперники (люди / боти / мікс); топологія мережі (сервер / peer-to-peer).

## Цікавинки для курсу
- Вид від першої особи з клітинної карти: коридор малюється як 2–3 рамки вглиб, доки нема стіни — 🥉 (класичний «псевдо-3D» рендер на сітці).
- Підглядання за ріг без ризику і без права стріляти — 📎 (стан, що блокує дію).
- 2 секунди невразливості після влучання — 🌱 (таймер стану).
- Постріл у спину: видимість залежить від напрямку погляду суперника — 📎.
- Мережева гра на двох з одним станом (сервер або peer-to-peer) — 🥇 (синхронізація стану, затримка).
- Бот, який сповільнюється після порогу очок — 📎 (динамічна складність).

## Мапа на каталог
- Є: `move-by-input` · `orientation-state` (напрямок погляду) · `impassable-cells` · `projectile-shot` + `shoot-forward` · `line-of-sight-attack` · `event-points` (+10/−5) · `respawn` (?) · `minimap-radar` (лише своя позиція) · `fog-of-war` (бачиш лише свій коридор) · `online-multiplayer` · `ai-opponent` + `realtime-ai` · `cheat-codes` · `level-from-txt` (власні лабіринти) · `player-camera`.
- **Нема** → пропозиції карток:
  - `+first-person-grid-view` «Вид від першої особи на клітинній карті» · interface/render · 🥉 · слот {depth}.
  - `+peek-around-corner` «Підглянути без руху» · entities/state · 📎.
  - `+hit-invulnerability-window` «Невразливість після влучання» · entities/state · 🌱 · слот {duration}.
  - `+hit-penalty-score` «Мінус очки за отримане влучання» · game-logic/score · 🌱.
  - `+bot-slows-after-score` «Бот слабшає після порогу очок» · game-logic/difficulty · 📎.
  - `+spectator-overview` «Глядач бачить усю карту згори» · interface/render · 🥉.
  - `+text-message-to-player` «Текст на екран іншого гравця» · game-logic/opponent · 🌱.

## Пропозиції до словників
- `+effect:peek` — показати вид з сусідньої позиції без зміни положення сутності.
- `+ui:first-person-view` — вікно виду від першої особи поряд із картою.
- `+feature:spectator-overview` — окремий вид згори для глядачів (Maze Watcher).
- `+axis:view` — `top-down` · `side` · `first-person` (у `code-words.md` є поле `view`, але не вісь шапки).
- `+card:peek-around-corner`, `+card:hit-invulnerability-window` — див. вище.

## Джерела
- ⭐ [Wikipedia: Maze (1973)](https://en.wikipedia.org/wiki/Maze_(1973_video_game)) — сітка, рух і повороти, підглядання, кулі, +10/−5, 2 с, до 8 гравців, ARPANET, Alto, роботи, Maze Guncher, Maze Watcher, редактор, варіанти.
- [DigiBarn: Xerox Maze War](https://digibarn.com/collections/games/xerox-maze-war/) — скриншот (вид згори + карта знизу + рахунок), очі-аватари, засідки, підглядання за ріг, «Maze Lords».
- [DigiBarn: документація Imlac](https://digibarn.com/collections/games/xerox-maze-war/maze-documentation/index.htm) — підписи до фото, апаратна версія.
- YouTube: пошук «maze war xerox alto gameplay».

## Непевне
- (?) Чи переносить влучання жертву у випадкову клітину (респавн) — у джерелах лише «2 секунди, щоб відійти».
- (?) Точні клавіші і чи є окрема клавіша розвороту в усіх версіях («look behind» — у Wikipedia).
- (?) Формат файла лабіринту і як працював редактор Lebling-а.
- (?) Алгоритм руху роботів («простий») і чи вони бачать карту.
