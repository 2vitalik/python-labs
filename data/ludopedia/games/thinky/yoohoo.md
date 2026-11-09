---
title: Yoohoo
slug: yoohoo
aka: []
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
platforms: [web]
links:
  - {kind: itch, url: "https://competor.itch.io/yoohoo", best: true, note: "сторінка гри: керування, 9 рівнів, вибір рівня; грати в браузері"}
  - {kind: play, url: "https://puzzlescriptnext.polyomino.com//play.html?p=af9bedc71b5d4db0e86214c4b77bddc4", note: "грати (PuzzleScript Next)"}
  - {kind: other, url: "https://api.github.com/gists/af9bedc71b5d4db0e86214c4b77bddc4", note: "вихідний код PuzzleScript (gist, JSON)"}
  - {kind: other, url: "https://itch.io/jam/thinky-puzzle-game-jam-4", note: "Thinky Puzzle Game Jam 4"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Yoohoo+puzzlescript+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-4dir, keyboard-controls, push-object, impassable-cells, projectile-shot, turn-when-blocked, fill-hole, environment-death, orientation-state, facing-icon, all-on-targets, reach-exit, sequential-levels, level-select, save-progress, undo-unlimited, restart-level, level-from-txt, sound-effects, +fan-blow, +gust-carry-over-pit, +gust-reverse-in-dead-end, +shout-action]
proposes: ["+card:gust-carry-over-pit", "+card:gust-reverse-in-dead-end", "+card:shout-action"]
author: opus
date: 2026-11-09
---

# Yoohoo — Sokoban, де ящики й себе рухаєш не руками, а вигуком-поривом

## Суть
Маленька PuzzleScript-гра competor (Thinky Puzzle Game Jam 4): герой ходить по острівцях підлоги над порожнечею, штовхає камені й може крикнути «Yoohoo!» — у клітині попереду народжується порив повітря. Порив летить по прямій, штовхає камені й самого героя, у коридорі повертає за стіною, а в глухому куті розвертається назад. Мета — поставити камені на свої цілі, а героя — на свою. Головна ідея: обʼєкти, яких несе порив, не падають у прірву, тож порив — це міст і «транспорт».

## Поле і час
- Квадратна сітка; клітина — підлога або порожнеча (провалля). Рівень обрамлено рамкою: обʼєкт, винесений на рамку, зникає з поля.
- Шари: фон → підлога/цілі → {гравець, стіна, камінь, порив} → службові мітки.
- Покроково: хід = натискання. Після вигуку порив рухається сам — PuzzleScript `again` дає серію авто-тіків (0,05 с) без вводу, доки порив живий.
- Псевдо-3D вигляд (тіні, бічні грані) — лише графіка, логіка пласка.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | напрям погляду | крок на 1 у 4 напрямки, погляд = напрям останнього кроку; штовхає один камінь; сам у провалля не ступає |
| Порив (wind) | projectile | напрям | щотіку летить на 1; штовхає камінь/гравця; при упорі повертає або розвертається; зник, якщо не зрушив |
| Камінь | object | штовхуваний | рух на 1 від поштовху; над проваллям без пориву — падає й стає підлогою |
| Стіна | static | — | непрохідна, не штовхається |
| Підлога | terrain | — | опора для гравця і каменя |
| Порожнеча | hazard | — | гравець падає й гине; камінь засипає її |
| Ціль гравця | zone | — | має стояти гравець |
| Ціль каменя | zone | — | має стояти камінь |
| Рамка | static | край мапи | штовхуваний обʼєкт на ній зникає |
| Підказка-плитка | zone | — | на 1-му рівні показує «press X to breathe out» |

## Правила (КОЛИ → ЯКЩО → ТО)
Гравець:
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` і `cell(next_cell, floor)` → ТО `move(player, dir)`, `face(player, dir)`.
- КОЛИ `input(dir)` → ЯКЩО `cell(next_cell, void)` → ТО `block` (сам у провалля не йде).
- КОЛИ `contact(player, rock)` → ЯКЩО `free(cell_behind)` → ТО `push(rock)`; інакше `block`. Ланцюгового поштовху нема.
- КОЛИ `input(action)` → ЯКЩО `free(cell_ahead)` (нема стіни, каменя, гравця; провалля можна) → ТО `spawn(wind, cell_ahead)` з напрямом погляду, `sound(shout)`.

Порив (кожен авто-тік):
- КОЛИ `tick` → ЯКЩО `free(cell_ahead)` → ТО `move(wind, dir)`.
- КОЛИ `tick` → ЯКЩО `occupied(cell_ahead, rock|player)` і `free(cell_behind_it)` → ТО `push` обʼєкта й `move(wind, dir)`.
- КОЛИ `tick` → ЯКЩО `occupied(cell_ahead, player)` і `occupied(cell_ahead_of_player, rock)` і `free(next)` → ТО `push` обох (герой у поштовху штовхає камінь перед собою).
- КОЛИ `blocked(wind)` → ЯКЩО `free(left)` і `not free(right)` → ТО `face(wind, left)`; дзеркально для правого боку (`turn-when-blocked`).
- КОЛИ `blocked(wind)` → ЯКЩО `not free(left)` і `not free(right)` → ТО `bounce(wind)` — розворот на 180°, `sound(turnback)`.
- КОЛИ `blocked(wind)` → ЯКЩО `free(left)` і `free(right)` → ТО `custom: «порив не обирає бік — лишається на місці»`.
- КОЛИ `custom: «порив за тік не зрушив»` → ТО `disappear(wind)`, `sound(end)`.

Падіння і край:
- КОЛИ `after(move)` → ЯКЩО `cell(under, void)` і `not state(rock, carried)` → ТО `set_cell(under, floor)`, `disappear(rock)` — камінь засипає провалля.
- КОЛИ `after(move)` → ЯКЩО `cell(under, void)` і `not state(player, carried)` → ТО `custom: «гравець падає — стає «мертвим» спрайтом»`; далі лише undo/restart.
- КОЛИ `enter(rock|player|wind, frame)` → ТО `disappear` — винесено за межі мапи.
- Стан `carried` = обʼєкт у цьому тіку підхоплений поривом; поки порив несе, порожнеча під ним не діє.

Перемога / поразка:
- КОЛИ `all_on(player, player_target)` і `all_on(rock, rock_target)` → ТО `win`, `message(«N/9 · назва»)`, `next_level`.
- Поразка — падіння героя (не автоматична: гра чекає undo/restart). Рахунку нема.

## Керування і ввід
- Стрілки / WASD — крок і поворот; X / пробіл / Enter — «Yoohoo!» (вигук у бік погляду); Z — undo; R — рестарт; Esc — меню вибору рівня.
- Лише клавіатура; мікрофона нема — «голос» тут сюжетний (вигук = клавіша дії).

## Вікна, меню, HUD
- `main-menu` (титул PuzzleScript Next): назва, автор, старт / продовжити.
- `level-select` (Esc): 9 рівнів-секцій із позначкою `*` для розвʼязаних.
- `game-screen`: поле, без HUD; звук на крок каменя, вигук, поворот, розворот, зникнення пориву, падіння.
- `custom-window` повідомлення між рівнями: «1/9 Breathe in», «2/9 I'm Yoohoo», «3/9 Change an opinion», «4/9 Gives You Wings», «5/9 Soko», «6/9 Echo chamber», «7/9 Portal», «8/9 Looping», «9/9 Crevasse»; фінал — «Congratulations!».
- Переходи: main-menu → game-screen → повідомлення → наступний рівень; Esc → level-select.

## Фічі поза полем
- `levels-sequential` + `level-select` (рушій PuzzleScript Next), прогрес зберігається в браузері.
- `undo` ∞ і `restart-level`.
- Вихідний код відкритий (PuzzleScript Next, «hack»).

## Варіації й родичі
- Батько — Sokoban (`games/push-slide/sokoban.md`); засипання дірки каменем — як у Kwirk і `games/thinky/a-monsters-expedition.md`.
- Рух обʼєкта на відстані без дотику — родич `games/thinky/increpare-micro-puzzles.md` (ящики їдуть від кроку) і `increpare-sokoban-variants.md` (Explodoban штовхає вибухом).
- **Осі варіацій:** чим рухати обʼєкти — тілом / снарядом-поривом; що робить снаряд при упорі — зникає / повертає / розвертається; чи переносить через провалля — так / ні; чи штовхає самого гравця — так (ключ до «Gives You Wings»).

## Цікавинки для курсу
- Порив-снаряд з авто-тіками після одного вводу (цикл `again` до стабілізації) — 📎.
- Поворот пориву: упор → перевірка двох боків → поворот / розворот / зникнення — 🥉 (маленький автомат станів руху).
- «Несомий не падає»: гравітація-в-провалля перевіряється лише для обʼєктів без мітки поштовху цього тіку — 🥉.
- Камінь засипає провалля й стає підлогою — 🌱.
- Петлі й «ехо»: порив, що ходить по замкнутому коридору (рівні Looping, Echo chamber), — тест на нескінченний цикл, потрібен ліміт тіків — 🥈.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls`; `push-object` ↔ поштовх каменя; `projectile-shot` ↔ порив; `turn-when-blocked` ↔ поворот пориву; `fill-hole` ↔ камінь у проваллі; `environment-death` ↔ падіння героя; `orientation-state` + `facing-icon` ↔ погляд визначає напрям вигуку; `all-on-targets` + `reach-exit` ↔ дві цілі; `sequential-levels`, `level-select`, `save-progress`, `undo-unlimited`, `restart-level`, `level-from-txt`, `sound-effects`.
- **Нема** → пропозиції карток:
  - `+fan-blow` «Порив/вентилятор штовхає обʼєкти» · entities/move · 📎 (уже пропонувалась іншими файлами).
  - `+gust-carry-over-pit` «Несений поривом не падає в провалля» · entities/move · 🥉.
  - `+gust-reverse-in-dead-end` «Снаряд розвертається в глухому куті» · entities/move · 🌱 · слот {on_block: vanish|turn|reverse}.
  - `+shout-action` «Дія гравця породжує сутність перед собою» · entities/spawn · 🌱.

## Пропозиції до словників
- `+card:gust-carry-over-pit`, `+card:gust-reverse-in-dead-end`, `+card:shout-action` — механік нема в каталозі.

## Джерела
- ⭐ [Yoohoo на itch.io](https://competor.itch.io/yoohoo) — керування (WASD, X/Space/Enter, Z, R, Esc), 9 рівнів, вибір рівня, PuzzleScript, TPGJ4; коментар про рівень 9 («камені не мають падати до останнього моменту»).
- [Грати (PuzzleScript Next)](https://puzzlescriptnext.polyomino.com//play.html?p=af9bedc71b5d4db0e86214c4b77bddc4).
- [Вихідний код (gist API)](https://api.github.com/gists/af9bedc71b5d4db0e86214c4b77bddc4) — правила пориву (`WindChk*`, `pushNext*`, `again`), падіння (`deadrock`), рамка, умови перемоги `all Target on Player` / `all rocktarget on rock`, назви рівнів; gist створено 2024-07-04.
- [Thinky Puzzle Game Jam 4](https://itch.io/jam/thinky-puzzle-game-jam-4).

## Непевне
- (?) Черга описувала гру як «Sokoban з голосовим вводом» і рік 2025 — у джерелах вигук — клавіша, мікрофона нема; рік — 2024 (gist і devlog — липень 2024).
- (?) Поведінка пориву, коли попереду стіна, а обидва боки вільні: з коду порив лишається на місці й зникає наступного тіку — грою не перевірено.
- (?) Гравець теж штовхуваний для пориву, а `pushable` у коді включає й сам порив — чи може гравець штовхнути порив кроком, не перевірено.
- (?) Падіння героя — спрайт «dead» без вікна поразки; що саме бачить гравець, не перевірено.
