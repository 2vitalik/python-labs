---
title: Forever Wonder Colour
slug: forever-wonder-colour
aka: [FWC]
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
year: 2025
platforms: [web, Windows, macOS, Linux]
links:
  - {kind: itch, url: "https://patashu.itch.io/forever-wonder-colour", best: true, note: "грати в браузері; «one screen time manipulation Sokoban», Gain Insight, Author's Replay, редактор після проходження, Confounding Calendar 2025"}
  - {kind: other, url: "https://github.com/Patashu/Forever-Wonder-Colour", note: "сирці Godot 3.5 (MIT): GameLogic.gd — історія ходів, пересимуляція, глибина, Splice Flower; тексти Rules Overview і підказки редактора"}
  - {kind: other, url: "https://github.com/Patashu/Forever-Wonder-Colour/wiki", note: "кастомні пазли спільноти у форматі FWCPuzzleStart … FWCPuzzleEnd"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=azBgC0Wkri4", note: "проходження + показ кастомних пазлів (посилання зі сторінки itch)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Forever+Wonder+Colour+Patashu", note: "пошук; геймплей"}
stage: v1
coverage: 85
mechanics: [move-4dir, keyboard-controls, push-object, one-way-cell, impassable-cells, reach-exit, touch-death, fill-hole, undo-unlimited, redo, restart-level, replay, replay-window, in-game-editor, editor-palette, editor-playtest, level-exchange, state-string, controls-remap, volume-control, settings-window, pause-menu, help-window, game-screen, movement-animation, sound-effects, background-music, save-progress, +history-resimulation, +resim-depth, +depth-door, +history-splice-point, +undo-immune-objects, +reset-overlap-priority, +infinite-loop-loss, +divergence-emotes, +meta-undo, +insight-level, +authors-replay, +block-goal]
proposes: ["+effect:resimulate", "+effect:truncate_history", "+effect:record_move", "+effect:return_home", "+cond:depth", "+ui:resim-label", "+ui:emote-bubble", "+feature:insight-level", "+feature:solution-replay", "+feature:undo-restart", "+axis:undo", "+card:history-resimulation", "+card:depth-door"]
author: opus
date: 2026-11-19
---

# Forever Wonder Colour — однокімнатний Sokoban, де поштовх помаранчевого блока переписує минуле: уся історія твоїх ходів програється наново

## Суть
Вояль прийшов у Печеру Дива по секрети Часу. Це звичайний Sokoban на одному екрані (мета — дійти до Goal), але кожен успішний хід записується в **історію**, а штовхнутий **Wonder Block** (помаранчевий) запускає пересимуляцію: усі, крім таких блоків, повертаються на стартові («домашні») клітини, і вся історія програється наново так, ніби блок завжди стояв на новому місці. Колись успішний хід тепер може впертися чи штовхнути щось інше; якщо під час пересимуляції знову зсувається Wonder Block — історія обрізається й починається глибша пересимуляція (Depth 2, 3…), а двері в печері відчиняються залежно від глибини. Splice Flower стирає історію й робить поточний стан новим ходом 0.

## Поле і час
- Основний пазл — одна кімната 14×13 клітин (стіни по периметру): 7 Stone Block, 4 Wonder Block, 2 Splice Flower, 4 Depth Door (глибини 2, −1, 1, 1), 3 one-way, 1 Goal. Пазл «Gain Insight» — 11×7. Авторський розвʼязок — 90 вводів.
- Шари: кілька TileMap-шарів рельєфу (стіни, one-way, квітки, ями, дошки) + актори (гравець, блоки, двері) + Goal. Під дошками (редактор) — окремий нижній шар: актори над і під дошками одне одного не бачать.
- Два «часи»: **історія** — рядок успішних ходів `w/a/s/d` від ходу 0 (велика літера = хід із поштовхом) і **мета-ходи** — вводи гравця, які скасовує undo (разом з усіма пересимуляціями).
- Покроково; пересимуляція анімується хід за ходом з написом «Resimulating: t/T · Current Depth: d» (колір глибини: помаранчевий / кремовий / синій по колу).
- До першої Splice Flower лічильник показує «Turn: N + 1 000 000» — за сюжетом печера відчинилась на мільйонний хід Всесвіту, і перша пересимуляція «програє Всесвіт» від початку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Вояль | player | сила LIGHT, вага IRON; цілий / зламаний | крок у 4 напрямки; штовхає один блок; зламаний не ходить (лише undo) |
| Stone Block | object | вага IRON | звичайний блок Sokoban; при пересимуляції повертається на домашню клітину |
| Wonder Block (помаранчевий) | object | вага IRON; імунний до скидання | штовхнутий — нова клітина стає домашньою й запускає пересимуляцію |
| White Block (редактор) | object | імунний до скидання | як Wonder, але пересимуляції не запускає |
| Splice Flower | pickup | — | гравець ступив → квітка зникає, історія стерта, поточний стан = хід 0; зламаного гравця оживляє |
| Depth Door | gate | число N (буває відʼємним) | N > 0: прохідні, коли поточна глибина ≥ N; N < 0: прохідні, доки глибина < |N| |
| One-Way ×4 | terrain | напрям | «Solid to moves entering its tile» з одного боку |
| Стіна | static | — | непрохідна |
| Goal | static | — | перемога, якщо цілий гравець на ній; під час пересимуляції не спрацьовує |
| Block Goal (редактор) | zone | — | перемога заблокована, доки на ній нема блока (закрита дошками — не рахується) |
| No Player / No Stone / No Wonder / No White (редактор) | terrain | — | непрохідні лише для одного виду акторів |
| Spikes (редактор) | hazard | — | ламають гравця |
| Orange Spikes (редактор) | hazard | — | ламають гравця й запускають пересимуляцію («зазвичай нескінченний цикл») |
| Hole (редактор) | hazard | — | гравець чи блок падає й засипає яму |
| Floorboards: Blue / White / Orange (редактор) | terrain | — | ховають рельєф і акторів під собою; ламаються, коли гравець сходить; White — імунні до скидання; Orange — ще й запускають пересимуляцію |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(player, dir)`, `custom: «літера ходу дописується в історію; велика — якщо був поштовх»`.
- КОЛИ `contact(player, block)` → ЯКЩО `free(cell_behind)` → ТО `push`; два блоки поспіль не зсуваються (сила гравця LIGHT ≥ вага IRON, сила блока WOODEN < IRON).
- КОЛИ `input(dir)` → ЯКЩО `cell(next_cell, wall|one_way_against_move)` або `not state(depth_door, open)` → ТО `block`; невдалий хід не потрапляє в історію й не забирає часу.
- КОЛИ `contact(player, depth_door)` → ЯКЩО `not state(depth_door, open)` → ТО `block`, `message(«Opens at Depth N+.»)`.
- КОЛИ `after(push)` → ЯКЩО `custom: «зсунуто Wonder Block»` → ТО `custom: «нова клітина блока стає домашньою»`, `counter(depth, +1)`, `custom: «пересимуляція: усі, крім Wonder/White-блоків і дверей, повертаються на домашні клітини; історія програється з ходу 0»`.
- Під час пересимуляції КОЛИ `custom: «програється хід з історії»` → ЯКЩО `not free(next_cell)` → ТО `block`, `message(«!!»)`; був поштовх, а тепер нема — `message(«?»)`; поштовху не було, а тепер є — `message(«!»)`; поштовх зірвався — `message(«?!»)`.
- КОЛИ `custom: «Wonder Block зсунувся під час пересимуляції»` → ТО `custom: «історію обрізано на цьому ході»`, `counter(depth, +1)`, `custom: «нова, глибша пересимуляція»`.
- КОЛИ `counter(depth, >=, 16)` → ТО `lose` («Infinite loop.»), `custom: «історію обрізано»`.
- КОЛИ `custom: «пересимуляцію завершено»` → ТО `counter(depth, -1)` — після всіх вкладених рівнів глибина знову 0.
- КОЛИ `counter(depth, >=, N)` → ТО `set_state(depth_door_N, open)` для N > 0; для N < 0 навпаки — `clear_state(depth_door, open)`, щойно глибина ≥ |N|.
- КОЛИ `custom: «на початку історії два актори в одній клітині»` → ТО `set_state(loser, broken)` — «Player beats Wonder Block beats Stone Block»; розбитий блок розлітається й більше ні з чим не взаємодіє.
- КОЛИ `enter(player, splice_flower)` → ТО `disappear_b`, `custom: «історію стерто (пересимуляція зупиняється); поточні клітини всіх акторів стають домашніми — це новий хід 0»`, `clear_state(player, broken)`.
- КОЛИ `enter(player, goal)` → ЯКЩО `not state(player, broken)` і `custom: «кожен Block Goal зайнятий блоком»` → ТО `win`.
- Редактор: КОЛИ `enter(player, spikes)` → ТО `set_state(player, broken)`; Orange Spikes — плюс `custom: «пересимуляція»`.
- Редактор: КОЛИ `enter(actor, hole)` → ТО `set_state(actor, broken)`, `set_cell(hole, floor)`; яму, засипану гравцем чи Stone Block, пересимуляція відновлює, засипану Wonder/White — ні; Wonder у ямі запускає пересимуляцію.
- Редактор: КОЛИ `leave(player, floorboards)` → ТО `set_cell(floorboards, floor)`; Blue — відновлюються при пересимуляції, White — ні, Orange — ні й запускають пересимуляцію.
- Редактор: КОЛИ `contact(actor, no_tile)` → ЯКЩО `custom: «тип плитки забороняє саме цей вид»` → ТО `block`.
- Перемога: цілий гравець на Goal, усі Block Goal зайняті. · Поразка: «Infinite loop.» на глибині 16 → Undo або Restart; зламаний гравець — лише undo. · Рахунку нема; зберігається найкращий власний реплей (менше вводів, при рівності — коротший рядок).

## Керування і ввід
- Стрілки / WASD — крок; утримання — повтор.
- Z або C — undo (мета-undo: скасовує останній ввід разом з усією пересимуляцією); Y — redo; R — рестарт (теж скасовується undo, якщо так обрано в налаштуваннях); Esc — меню.
- Enter / Space / X — прискорити пересимуляцію; будь-який напрям — пропустити її; після перемоги — дивитися реплей.
- M — вимкнути звук; F5 / F6 / F7 — реплей: крок назад / пауза / крок уперед; F9 / F10 — повільніше / швидше; Ctrl+C / Ctrl+V — копіювати / вставити реплей чи рівень.
- Геймпад з перепризначенням, екранні кнопки для тачу (undo, redo, напрямки, Enter, кнопки реплею).

## Вікна, меню, HUD
- `dialogue-window` — вступ «On the 1,000,000th turn of the Universe... The entrance to the Wonder Cave opens!»; після першої квітки — думки героя «That orange block I walked past was super pretty...~» з кнопкою «Maybe this flower will help»; після перемоги — «Well, the Wonder Cave was a bust…».
- `game-screen`: кімната; HUD — назва рівня (зірка, якщо пройдено), `turn-counter` «Turn», «Iterations» (скільки було пересимуляцій), `move-counter` «Inputs», напис пересимуляції (`+ui:resim-label`), `popup-text` («Opens at Depth N+.»), бульбашки-реакції над героєм (`+ui:emote-bubble`: !!, ?!, ?, !), екранні кнопки.
- `pause-menu` (Menu): Continue · Your Replay · Author's Replay · Save Replay · Copy Replay · Paste Replay · Level Editor · Controls · Settings · Restart · Quit Game · «Stuck? Try these:» Gain Insight · Rules Overview.
- `help-window` — Rules Overview: 8 правил (Sokoban, one-way, Wonder Block і Depth 1, обрізання історії, Depth Door, Splice Flower, хто кого бʼє на старті історії).
- `confirm-dialog` — перед Gain Insight («shows you a simpler or remixed puzzle») і перед Author's Replay («this puzzle's official solution»).
- `replay-window` — режим реплею: «Input i/N», повзунок ходу, швидкість, пауза.
- `settings-window`: VSync, Puzzle Checkerboard, Resolution, FPS, Animation Speed, Full Screen, гучності Master / SFX / Music / Fanfare, Mute In Background, екранні кнопки, Reset Progress, Copy / Paste Save File, «Undo a Restart?».
- `options-controls` — клавіатура й контролер, перепризначення, Deadzone, Debounce.
- `editor-window` — палітра плиток із підказкою-описом кожної, метадані рівня (назва, автор, глибини дверей), тест-режим записує реплей.
- `end-screen` — «You have won! Made by Patashu / Graphics by Teal Knight / [Enter]: Watch Replay / Or try custom puzzles!»; поразка — «Infinite loop. Undo or Restart to continue.»
- Переходи: вступ → game-screen ↔ pause-menu → (Gain Insight) пазл-підказка ↔ основний; перемога → end-screen → реплей; Level Editor → editor-window → тест → game-screen.

## Фічі поза полем
- `undo` без ліміту на рівні вводів + `redo`; `restart-level`, який сам скасовується undo (`+feature:undo-restart`, налаштування «Undo a Restart?»).
- `replay`: власний найкращий реплей, `show-solution` — Author's Replay з повзунком і швидкістю (`+feature:solution-replay`).
- `+feature:insight-level` — «Gain Insight»: простіший пазл з тією самою ключовою ідеєю, «Lose Insight» — назад.
- `level-editor` (після проходження) + `level-sharing`: рівень — текст `FWCPuzzleStart: назва by автор` … шари … `FWCPuzzleEnd`, вставляється Ctrl+V; спільнота збирає пазли у вікі GitHub; `share-code` для реплеїв.
- `autosave` з копіюванням / вставкою файла збереження; `remap-controls`, `gamepad-support`, `touch-controls`, `volume-sliders`, `fullscreen`, `window-size`, швидкість анімації; на itch — «Color-blind friendly».

## Варіації й родичі
- Той самий автор і рушій: [Entwined Time](entwined-time.md) (окремі таймлайни, «зелений» колір часу, Gain Insight), Unwin (згаданий у коді й коментарях гравців).
- [The Observer's Paradox](the-observers-paradox.md) — блок повертається на місце; [Achronal Dungeon](../roguelike/achronal-dungeon.md) і [Tres Undos](tres-undos.md) — обʼєкти, імунні до скидання; [Meet me at NooN](meet-me-at-noon.md) — повтор ходів з початку.
- Натхнення — блог knexator «Puzzles About Time Travel»; кастомні варіанти спільноти: «Featureless Wonder Colour» (без one-way), «Desync Kindergarten», «Room 2 [Hard Mode]» тощо.
- **Осі варіацій:** що переживає скидання — нічого / окремі «чарівні» обʼєкти (тут Wonder і White) / гравець · що запускає скидання — кнопка / поштовх обʼєкта (тут) / смерть · що програється — нічого (Sokoban) / власна історія ходів (тут) / записи клонів · глибина — один рівень / вкладені з лімітом (тут 16) · точка нуля часу — початок рівня / квітка, що переносить нуль.

## Цікавинки для курсу
- Історія як рядок ходів і пересимуляція від домашніх позицій: детермінований реплей, велика літера = «тут був поштовх» — 🥉.
- Вкладені пересимуляції з обрізанням історії й лімітом глибини 16 → «Infinite loop», і все це скасовується одним undo — 🥇.
- Реакції на розбіжність «тоді / тепер» (!!, ?!, ?, !) — 📎 (порівняння очікуваного й фактичного результату ходу).
- Двері, що залежать від поточної глибини пересимуляції (додатні й відʼємні N) — 📎.
- Splice Flower: перенести нуль часу — перезаписати домашні позиції й очистити історію — 🌱.
- Пріоритет на старті історії «Player > Wonder > Stone»: хто з двох в одній клітині розбивається — 📎.
- Текстовий формат рівня з шарами, метаданими й реплеєм; вставка з буфера — 🥉.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ крок; `push-object` ↔ блоки; `one-way-cell` ↔ One-Way; `impassable-cells` ↔ стіни, No-плитки, зачинені двері; `reach-exit` ↔ Goal; `touch-death` ↔ Spikes (редактор); `fill-hole` ↔ Hole (редактор); `undo-unlimited` + `redo` + `restart-level`; `replay` + `replay-window` ↔ свій і авторський реплей; `in-game-editor` + `editor-palette` + `editor-playtest` ↔ редактор і тест-режим; `level-exchange` + `state-string` ↔ текст FWCPuzzleStart…End; `controls-remap`, `volume-control`, `settings-window`, `pause-menu`, `help-window` (Rules Overview), `game-screen`, `movement-animation`, `sound-effects`, `background-music`, `save-progress`; поза тегами лишились `confirm-dialog`, `popup-text`, `field-scaling` (кімната масштабується ×0.5 / ×1 / ×2).
- **Нема** → пропозиції карток:
  - `+history-resimulation` «Пересимуляція історії ходів після зміни світу» · game-logic/history · 🥇 · слоти {trigger: push_of_kind, max_depth: 16}.
  - `+resim-depth` «Вкладені пересимуляції з глибиною» · game-logic/history · 🥈.
  - `+depth-door` «Двері, відчинені на певній глибині пересимуляції» · entities/legality · 📎 · слот {depth: ±N}.
  - `+history-splice-point` «Квітка: новий нуль часу» · game-logic/history · 🌱.
  - `+undo-immune-objects` (вже пропонована Achronal Dungeon / Tres Undos) — тут імунітет до скидання, не до undo.
  - `+reset-overlap-priority` «Хто кого розбиває, коли скидання ставить двох в одну клітину» · entities/interact · 📎.
  - `+infinite-loop-loss` «Поразка за нескінченну рекурсію» · game-logic/lose · 📎.
  - `+divergence-emotes` «Реакція героя на розбіжність повтору» · interface/hud · 🌱.
  - `+meta-undo` (вже пропонована Entwined Time) — undo скасовує ввід разом з його наслідками й рестарт.
  - `+insight-level` (вже пропонована Entwined Time) — простіший пазл-підказка.
  - `+authors-replay` «Авторський розвʼязок із повзунком» · interface/results · 🌱.
  - `+block-goal` «Плитка, що блокує перемогу без блока на ній» · game-logic/win · 🌱.

## Пропозиції до словників
- `+effect:resimulate` — повернути всіх на домашні позиції й програти історію ходів наново.
- `+effect:truncate_history` — обрізати історію на поточному ході (наступні ходи зникають).
- `+effect:record_move` — дописати хід в історію (тут літерою; велика — з поштовхом).
- `+effect:return_home` — актор повертається на домашню клітину.
- `+cond:depth` — поточна глибина пересимуляції порівняно з N (Depth Door).
- `+ui:resim-label` — напис «Resimulating t/T · Current Depth d» поверх поля.
- `+ui:emote-bubble` — значок-реакція над героєм (!!, ?!, ?, !).
- `+feature:insight-level` — пазл-підказка з тією самою ідеєю; `+feature:solution-replay` — авторський розвʼязок у плеєрі; `+feature:undo-restart` — рестарт, який скасовує undo.
- `+axis:undo` — `meta` (скасовує ввід з усією пересимуляцією), без ліміту.
- `+card:history-resimulation`, `+card:depth-door` — див. «Мапа на каталог».

## Джерела
- ⭐ [itch: Forever Wonder Colour](https://patashu.itch.io/forever-wonder-colour) — опис (one screen time manipulation Sokoban, Confounding Calendar 2025), Gain Insight, Author's Replay, редактор після проходження, Godot 3.53, кольоросліпий режим, девлог про реліз 10.12.2025.
- [GitHub: Patashu/Forever-Wonder-Colour](https://github.com/Patashu/Forever-Wonder-Colour) — `GameLogic.gd` (історія, `increment_iteration`, `splice_flower`, `adjust_depth`, «Infinite loop.» на глибині 16, сила й вага), `Hint.tscn` (Rules Overview), `LevelEditor.gd` (описи всіх плиток), `Menu.tscn`, `Settings.tscn`, `project.godot` (клавіші), рівень `levels/ForeverWonderColour.tscn` (90-вводовий авторський реплей, глибини дверей 2, −1, 1, 1).
- [GitHub wiki](https://github.com/Patashu/Forever-Wonder-Colour/wiki) — кастомні пазли спільноти й формат рівня.
- [YouTube: проходження + кастомні пазли](https://www.youtube.com/watch?v=azBgC0Wkri4).

## Непевне
- (?) Плитки Spikes, Orange Spikes, White Block, Hole, Floorboards, No-плитки й Block Goal є в коді й палітрі редактора, але ні в основному пазлі, ні в пазлі Gain Insight не стоять; які з них уживають кастомні пазли спільноти — не перевіряв.
- (?) Як саме поводяться актори під дошками (шар під Floorboards) — описано лише за кодом `actor_tangible`, у грі не перевірено.
- (?) Статус сторінки itch — «In development», хоча девлог 10.12.2025 оголошує реліз; рік 2025 — за девлогом.
