---
title: WOIM
slug: woim
aka: [If I Was A Worm]
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
year: 2026
platforms: [PC (Windows, macOS, Linux), Steam Deck, web (демо If I Was A Worm)]
links:
  - {kind: play, url: "https://arussellsaw.itch.io/if-i-was-a-worm", best: true, note: "безкоштовне браузерне демо (Godot): керування WASD/стрілки, Q/Backspace undo, E — інша черв'ячка, Esc — вибір рівня; коментарі про яйця"}
  - {kind: steam, url: "https://store.steampowered.com/app/4272020/WOIM/", note: "опис: каміння, яйця, двері, кнопки, земля, яблука, пазли-джигсо, капелюхи; 4 світи, 50+ пазлів"}
  - {kind: itch, url: "https://arussellsaw.itch.io/woim", note: "повна версія на itch, «Snip yourself in half to get a helping hand»"}
  - {kind: other, url: "https://kotaku.com/woim-puzzle-game-logic-sokoban-indie-game-pc-steam-review-2000754137", note: "огляд: Snake + Sokoban, ріст від яблук, кнопка тримає ворота, швидка перемотка ходів, 50 пазлів"}
  - {kind: other, url: "https://80.lv/articles/check-out-this-wip-puzzle-game-where-you-play-as-a-worm", note: "WIP-стаття: розрізати себе навпіл, крихке яйце"}
  - {kind: other, url: "https://reddit.sentinel-team.org/posts/1qqgg6z/snapshots/2026-01-29T18%3A21%3A14.676814Z", note: "дзеркало девлогу r/gamedev: розріз — «головна механіка», інверсія черв'ячок після розрізу, гравітація яйця, жуки"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=WOIM+worm+puzzle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [move-by-input, move-4dir, body-queue, push-object, impassable-cells, dig-terrain, item-pickup, party-switch, undo-unlimited, restart-level, world-map, level-select, keyboard-controls, save-progress, +grow-by-eating, +cut-body, +pressure-plate, +egg-hatch, +fragile-egg, +invert-worm, +jigsaw-collectible, +cosmetic-hats, +collectible-secrets]
proposes: ["+effect:reverse_body", "+card:fragile-egg", "+card:invert-worm", "+card:jigsaw-collectible", "+card:cosmetic-hats"]
author: opus
date: 2026-11-09
---

# WOIM — Snake + Sokoban під землею: черв'як росте від яблук і розрізає себе навпіл, щоб мати помічника

## Суть
Покрокова головоломка з видом згори: гравець — черв'як, тіло якого тягнеться за головою, як у Snake. Він штовхає каміння, їсть землю й яблука (росте), тисне кнопки, що відкривають ворота, і обережно возиться з крихкими яйцями. Головна механіка — **розріз**: черв'як ділиться навпіл, і друга половина стає окремою підконтрольною черв'ячкою-помічником (перемикання клавішею). Рівні — вузли підземної мапи, яка веде «глибше й глибше»; 4 світи, 50+ пазлів, секрети, капелюхи й пазли-джигсо.

## Поле і час
- Квадратна сітка, вид згори (Kotaku: «top-down 2D underworld»); кімнати-тунелі в ґрунті, рівні сполучені на спільній мапі-світі.
- Хід = один крок активної черв'ячки; світ без вводу не змінюється.
- Тіло займає ланцюжок клітин; на тілі видно темніший пояс (поясок черв'яка) — роль у механіці (?).
- Камера показує кімнату рівня цілком (скриншоти); на мапі-світі — частину мапи.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Черв'як (Woim) | player | довжина N, голова, хвіст | голова крокує в 4 напрямки, тіло-черга йде слідом; штовхає, їсть, тисне |
| Половинка-помічник | player | довжина | зʼявляється після розрізу; керується окремо після перемикання; неактивна — перешкода |
| Яблуко | pickup | — | зʼїдене — черв'як довшає |
| Земля | terrain | — | черв'як «їсть» її — клітина стає прохідною |
| Камінь | object | — | штовхається на 1, якщо за ним вільно |
| Яйце | object | крихке | переноситься/штовхається; розбивається за неправильного руху (?); має «гравітацію» (?) |
| Ножиці | switch | — | розрізають тіло, що через них проходить (?) |
| Кнопка (кругла плита) | switch | колір | натиснута, поки на ній лежить сегмент тіла |
| Ворота | gate | колір кнопки | відкриті, лише поки кнопку тиснуть |
| Ціль рівня (золоте яблуко?) | static | — | досягти — рівень пройдено (?) |
| Стіна / ґрунт | static | — | непрохідні |
| Пазл-джигсо, капелюх | pickup | — | секрети: шматки бічного пазла, косметика |
| Жуки (bugs) | neutral | прості правила руху | з девлогу: їх треба загнати барʼєрами з каміння й тіла (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(head, dir)`, `custom: «кожен сегмент стає на місце попереднього (тіло-черга)»`.
- КОЛИ `input(dir)` → ЯКЩО `cell(next_cell, wall)` або `occupied(next_cell, body)` → ТО `block` (?) — у себе не заходить.
- КОЛИ `contact(head, apple)` → ТО `disappear(apple)`, `grow(worm, 1)`.
- КОЛИ `contact(head, dirt)` → ТО `set_cell(dirt, floor)`.
- КОЛИ `contact(head, rock)` → ЯКЩО `free(cell_behind)` → ТО `push(rock)`; інакше `block`.
- КОЛИ `contact(worm, egg)` → ЯКЩО `free(cell_behind)` → ТО `push(egg)` / `carry(worm, egg)` (?).
- КОЛИ `custom: «яйце вдарилось або впало не так» (?)` → ТО `disappear(egg)` — розбите яйце робить пазл нерозвʼязним, лише undo.
- КОЛИ `custom: «яйце доставлено» (?)` → ТО `spawn(hatchling)` (Kotaku: «hatch eggs»).
- КОЛИ `enter(body, button)` → ТО `set_state(gate[color], open)`; КОЛИ `leave(body, button)` → ТО `clear_state(gate[color], open)`.
- КОЛИ `contact(head, gate)` → ЯКЩО `not state(gate, open)` → ТО `block`.
- Наслідок: щоб пройти ворота, черв'як має бути досить довгим, аби хвіст тиснув кнопку, поки голова проходить (Kotaku), або кнопку тримає друга половинка.
- КОЛИ `contact(body, scissors)` → ТО `split(worm)` — дві черв'ячки, друга — помічник (?) механізм розрізу.
- КОЛИ `input(switch)` → ТО `custom: «активною стає інша черв'ячка»` (клавіша E).
- КОЛИ `input(invert)` → ТО `custom: «голова й хвіст половинки міняються ролями»` (девлог: «inverting worms post-snip») (?).
- КОЛИ `contact(head, goal)` → ТО `win`, `next_level` (?) — мета рівня; іноді треба вирости, щоб дотягнутись.
- КОЛИ `contact(head, jigsaw_piece|hat)` → ТО `pickup`.
- КОЛИ `input(undo)` → ТО `undo(1)`; утримання — швидка перемотка всіх ходів рівня.
- КОЛИ `input(esc)` → ТО `window(level-select)`.
- Перемога: дійти до цілі рівня. · Поразка: нема (розбите яйце / глухий кут → undo). · Рахунку й лічильника ходів нема.

## Керування і ввід
- WASD / стрілки — крок голови; E — перемкнути черв'ячку; Q / Backspace — undo (утримання — перемотка); Esc — до вибору рівня (браузерне демо).
- Геймпад підтримується («Flawless with gamepad»); Steam Deck.
- Ввід двох напрямків одночасно в демо давав баги (коментарі) — рух строго по одній клітині.

## Вікна, меню, HUD
- `main-menu` (?): старт / продовжити / налаштування.
- `map-window`: підземна мапа-світ, рівні — світні кулі в тунелях, переходи між світами (порівняння з Baba Is You).
- `game-screen`: кімната рівня; HUD нема (скриншоти без лічильників).
- `level-select` (Esc) — повернення на мапу/вибір рівня.
- `custom-window`: бічний пазл-джигсо зі знайдених шматків; вибір капелюха (?).
- Переходи: мапа → рівень → (ціль) мапа; Esc → мапа.

## Фічі поза полем
- `world-map` з 4 світами, `level-unlock`, опційні челендж-рівні («extra gimmicks with the existing mechanics»).
- `undo` ∞ + `rewind`-подібна швидка перемотка; рестарт — утриманням undo (демо) (?).
- `collectibles`: секрети, шматки джигсо; `custom-skins` — капелюхи.
- `cloud-save`, досягнення Steam, `localization` (8 мов), `gamepad-support`.

## Варіації й родичі
- If I Was A Worm (2025, безкоштовне браузерне демо на itch) → WOIM (2026, Steam/itch); між ними — переробка рівнів («teamwork»), нові механіки (яйця, жуки).
- Родичі: `games/thinky/snakebird.md` (ріст від фруктів, кілька змій), `games/thinky/can-of-wormholes.md` (черв'як, розріз тіла), `games/maze-arcade/` Snake; ворота-кнопки — як у `games/thinky/heroes-of-sokoban.md`.
- **Осі варіацій:** розріз — нема / за ножицями (WOIM) / будь-де (Can of Wormholes); половинки — обидві підконтрольні / одна стає обʼєктом; гравітація — нема (WOIM, вид згори) / є (Snakebird); кнопка — тримає / перемикає.

## Цікавинки для курсу
- Тіло-черга + ріст від яблука — 🌱 (класика Snake, `deque`).
- Розріз тіла: одна черга → дві, друга стає окремим аватаром, перемикання — 🥉.
- Інверсія половинки (хвіст стає головою) — 📎 (`reverse` черги).
- Кнопка, що тримає ворота лише під вагою, і тіло як «довгий палець» — 📎.
- Крихке яйце: правило руйнування за способом руху — 🥉 (умова на напрям/падіння).
- Розвʼязувач BFS по станах (кілька черв'ячок, каміння, яйця, ворота) — 🥇 (стан швидко росте).

## Мапа на каталог
- Є: `move-by-input` + `move-4dir` ↔ крок голови; `body-queue` ↔ тіло; `push-object` ↔ каміння; `impassable-cells`; `dig-terrain` ↔ земля → прохід; `item-pickup` ↔ яблука, секрети; `party-switch` ↔ E; `undo-unlimited` + `restart-level`; `world-map` + `level-select`; `keyboard-controls`; `save-progress`.
- Уже пропоновані іншими файлами: `+grow-by-eating` (Can of Wormholes), `+cut-body` (Can of Wormholes), `+pressure-plate` (Grimrock), `+egg-hatch`, `+collectible-secrets`.
- **Нема** → пропозиції карток:
  - `+fragile-egg` «Крихкий обʼєкт: ламається від неправильного руху» · entities/state · 🥉 · слот {break_on: fall|side_push}.
  - `+invert-worm` «Перевернути черв'яка: хвіст стає головою» · entities/move · 📎.
  - `+jigsaw-collectible` «Шматки бічного пазла як секрети» · levels/progression · 🌱.
  - `+cosmetic-hats` «Косметика на аватарі» · interface/graphics · 🌱.

## Пропозиції до словників
- `+effect:reverse_body` — голова й хвіст тіла-черги міняються місцями (інверсія після розрізу).
- `+card:fragile-egg`, `+card:invert-worm`, `+card:jigsaw-collectible`, `+card:cosmetic-hats` — механік нема в каталозі.

## Джерела
- ⭐ [If I Was A Worm (itch, браузер)](https://arussellsaw.itch.io/if-i-was-a-worm) — грати; клавіші; коментарі гравців (яйце в отворі, яйце б'ється від поштовху збоку, нема лічильника ходів, рестарт — утримання Q).
- [Steam: WOIM](https://store.steampowered.com/app/4272020/WOIM/) — перелік механік, 4 світи, 50+ пазлів, секрети, 8 мов; відгуки (ріст, щоб дотягнутись до цілі; «Centipede element»; мапа як у Baba Is You; капелюхи).
- [itch: WOIM](https://arussellsaw.itch.io/woim) — опис повної версії і скриншоти (ножиці, кнопки-диски, ворота, яблука, яйце).
- [Kotaku](https://kotaku.com/woim-puzzle-game-logic-sokoban-indie-game-pc-steam-review-2000754137) — Snake + Sokoban, яблука → ріст, кнопка й ворота, розріз без пояснень, швидка перемотка, 50 пазлів, $10.
- [80.lv](https://80.lv/articles/check-out-this-wip-puzzle-game-where-you-play-as-a-worm) — WIP: розділити черв'яка навпіл заради помічників, крихке яйце.
- [Девлог r/gamedev (дзеркало)](https://reddit.sentinel-team.org/posts/1qqgg6z/snapshots/2026-01-29T18%3A21%3A14.676814Z) — розріз як головна механіка, інверсія після розрізу, «гравітація яйця», жуки й барʼєри, розриви в ґрунті (ідея з Can of Wormholes).

## Непевне
- (?) Як саме працює розріз: ножиці як клітина, через яку проходить тіло, чи предмет-дія; хто стає «головою» відрізаної половинки; чи можна злити половинки назад.
- (?) Яйце: що означає його «гравітація» у грі з видом згори, коли воно б'ється, як «вилуплюється» (Kotaku: «hatch eggs») і чи несе його черв'як на собі.
- (?) Ціль рівня — золоте яблуко чи вихід; скільки сегментів дає яблуко; чи можна заходити у власне тіло.
- (?) Жуки, вода/фонтан (скриншот), «Centipede element» — у повній версії є, але правила не описані.
- (?) Рік: демо If I Was A Worm — 2025, реліз WOIM у Steam — 21.10.2026.
