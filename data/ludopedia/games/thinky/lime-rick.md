---
title: Lime Rick
slug: lime-rick
aka: []
family: thinky
also: [grid-platformer]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2013
platforms: [web]
links:
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=6841210", best: true, note: "PuzzleScript-порт: 11 рівнів, грати в браузері"}
  - {kind: other, url: "https://api.github.com/gists/6841210", note: "вихідний код порту (gist, JSON): уся механіка в ~10 правилах"}
  - {kind: other, url: "https://www.kongregate.com/games/KissMaj7/lime-rick", note: "оригінал Tommi Tuovinen (KissMaj7) на Kongregate, 2013-08-25"}
  - {kind: other, url: "https://www.puzzlescript.net/Gallery/index.html", note: "галерея PuzzleScript, де є порт"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Lime+Rick+puzzlescript", note: "пошук; геймплей"}
stage: v1
coverage: 80
mechanics: [move-by-input, gravity-fall, push-object, impassable-cells, visited-trail, item-pickup, reach-exit, keyboard-controls, sequential-levels, save-progress, undo-unlimited, restart-level, level-from-txt, sound-effects, +trail-wall, +climb-limit, +trail-eraser-pickup]
proposes: ["+effect:leave_trail", "+card:trail-eraser-pickup"]
author: opus
date: 2026-11-09
---

# Lime Rick — черв'як, що лазить по власному сліду: кожен крок лишає тверде тіло

## Суть
Гра Tommi Tuovinen (KissMaj7), відома за PuzzleScript-портом. Голова-черв'як ходить вбік, підіймається вгору не більше ніж на 3 клітини поспіль і падає під гравітацією; **кожна клітина, з якої пішла голова, назавжди стає твердим тілом**. Тіло — опора й стіна водночас: щоб вилізти, треба «побудувати» собі драбину, але власний слід швидко закриває шляхи. Яблуко стирає все тіло. Мета — дійти головою до виходу.

## Поле і час
- Квадратна сітка, вид збоку, гравітація вниз. Рівні з порту — 19×15, нижні ряди — декоративний «ґрунт» зі стін.
- Шари: фон → {вихід, яблуко} → тіло → {голова, стіна, ящик}.
- Покроково: хід = натискання; падіння голови й ящиків завершується в тому самому ході (правила повторюються до стабілізації).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Голова (Rick) | player | лічильник підйому 1–4 | вбік — крок, лічильник → 1; вгору — крок, лічильник +1 (до 4); падає, якщо під нею порожньо |
| Тіло (горизонтальне / вертикальне) | static | — | лишається в клітині, звідки пішла голова; непрохідне, тримає голову; не падає |
| Ящик | object | — | штовхається вбік на 1, якщо за ним вільно; падає до опори |
| Стіна | static | — | непрохідна |
| Яблуко | pickup | — | голова входить → усе тіло на полі зникає, яблуко зʼїдено |
| Вихід | static | — | голова на виході → рівень пройдено |

## Правила (КОЛИ → ЯКЩО → ТО)
Рух:
- КОЛИ `input(left|right)` → ЯКЩО `free(cell_ahead)` → ТО `move(head, dir)`, `custom: «стара клітина стає тілом»` (`+effect:leave_trail`), `set_value(head, climb=1)`.
- КОЛИ `input(left|right)` → ЯКЩО `occupied(cell_ahead, crate)` і `free(cell_behind_crate)` → ТО `push(crate)`, `move(head, dir)`, тіло в старій клітині.
- КОЛИ `input(up)` → ЯКЩО `counter(climb, <, 4)` і `free(cell_above)` → ТО `move(head, up)`, тіло в старій клітині, `counter(climb, +1)`, `sound(jump)`.
- КОЛИ `input(up)` → ЯКЩО `counter(climb, =, 4)` → ТО `block` (3 підйоми поспіль — межа).
- КОЛИ `input(down)` → ТО `block` (вниз — лише падінням).

Гравітація:
- КОЛИ `after(move)` → ЯКЩО `free(cell_under_head)` → ТО `fall(head)` і тіло в кожній покинутій клітині — падіння лишає вертикальний стовп тіла; `set_value(head, climb=1)`.
- КОЛИ `after(move)` → ЯКЩО `free(cell_under_crate)` → ТО `fall(crate)` (без сліду).
- Тіло й стіни гравітації не підкоряються; тіло — опора для голови та ящиків.

Яблуко і вихід:
- КОЛИ `contact(head, apple)` → ТО `disappear(all body)`, `disappear(apple)`; далі голова може впасти, бо опори-тіла вже нема.
- КОЛИ `contact(head, exit)` → ТО `win`, `message(«level N of 11»)`, `next_level`.
- Поразки нема: глухий кут — undo/restart. Рахунку нема.

## Керування і ввід
- Стрілки ← → ↑ (↓ не діє); Z — undo; R — рестарт; Esc — меню. Ті самі клавіші в оригіналі на Kongregate (там Esc — вибір рівня).

## Вікна, меню, HUD
- `main-menu` (титул PuzzleScript): назва, автор, start / continue.
- `game-screen`: поле без HUD; кольором голови показано лічильник підйому (світло-зелена → жовта → помаранчева → червона).
- `custom-window` повідомлення «level N of 11», фінал «congratulations!».
- Оригінал (Kongregate): `level-select` за Esc.

## Фічі поза полем
- `levels-sequential` (11 рівнів порту), `continue` у браузері.
- `undo` ∞, `restart-level`.
- Порт відкритий у редакторі PuzzleScript; автор порту пише, що повна версія має механіки, яких нема в 11 рівнях, але рушій їх підтримує.

## Варіації й родичі
- `games/thinky/snakebird.md` — головна відмінність: у Snakebird тіло — черга фіксованої довжини, що йде за головою й падає разом із птахом; у Lime Rick тіло не рухається, не падає й росте з кожним кроком, а ліміт — висота підйому (3), не довжина.
- Слід-стіна — як у Tron / `games/maze-arcade/snake.md` без хвоста; «зʼїж, щоб стерти слід» — інверсія Snake (там їжа подовжує).
- **Осі варіацій:** тіло — черга за головою / нерухомий слід; гравітація — на все тіло / лише на голову; ліміт — довжина / висота підйому / нема; їжа — подовжує / стирає тіло.

## Цікавинки для курсу
- Слід-стіна + гравітація голови з повтором правила до опори (падіння лишає стовп) — 🌱.
- Лічильник підйому з кольором голови як індикатором — 🌱.
- Яблуко, що стирає все тіло, і повторне падіння — 📎.
- Розвʼязувач BFS: стан = голова + множина клітин тіла + ящики + лічильник; росте швидко, бо тіло лише додається — 🥈 (гарний приклад вибуху простору станів).

## Мапа на каталог
- Є: `move-by-input` + `keyboard-controls`; `gravity-fall` ↔ голова і ящики; `push-object` ↔ ящик вбік; `impassable-cells` ↔ стіни й тіло; `visited-trail` ↔ слід; `item-pickup` ↔ яблуко; `reach-exit`; `sequential-levels`, `save-progress`, `undo-unlimited`, `restart-level`, `level-from-txt`, `sound-effects`.
- **Нема** → пропозиції карток:
  - `+trail-wall` «Слід стає стіною» · entities/move · 🌱 (уже пропонувалась).
  - `+climb-limit` «Ліміт підйому поспіль» · entities/move · 🌱 · слот {n: 3} (уже пропонувалась).
  - `+trail-eraser-pickup` «Предмет стирає весь слід» · entities/interact · 🌱.

## Пропозиції до словників
- `+effect:leave_trail(a, kind)` — клітина, яку покинула сутність, стає сутністю виду (Lime Rick, Tron).
- `+card:trail-eraser-pickup` — нема в каталозі.

## Джерела
- ⭐ [Lime Rick — PuzzleScript-порт](https://www.puzzlescript.net/play.html?p=6841210) — 11 рівнів.
- [Вихідний код порту (gist API)](https://api.github.com/gists/6841210) — правила підйому (`PlayerHead1..4`), сліду (`PlayerBodyH/V`), яблука, гравітації, `some player on exit`; gist 2013-10-05.
- [Kongregate](https://www.kongregate.com/games/KissMaj7/lime-rick) — оригінал: керування (стрілки, Z, R, Esc), «sliding, jumping, sticking to surfaces», дата 2013-08-25.
- [Галерея PuzzleScript](https://www.puzzlescript.net/Gallery/index.html) — запис «Lime Rick · Tommi Tuovinen».

## Непевне
- (?) Лінк черги `play.html?p=6994394` веде на іншу гру — «Atlas Shrank» (James Noeckel); правильний порт — `p=6841210`. Рік у черзі 2014 — джерела дають 2013.
- (?) Оригінал на Kongregate за FAQ ставить мету «дійти до яблука/виходу» і згадує «ковзання» та «прилипання до поверхонь» — у порті цього нема; механіки повної версії не перевірено.
- (?) Чи падіння справді лишає стовп тіла в кожній клітині — виведено з правила `DOWN [ Player | No Obstacle ] -> [ PlayerBodyV | PlayerHead1 ]`, грою не перевірено.
- (?) Хто зробив порт (у gist автор — Tuovinen, коментар «ported with permission») — найімовірніше Stephen Lavelle.
