---
title: Walking Dots (てんてん虫)
slug: walking-dots
aka: [Tenten-mushi, てんてん虫, Тентен-муші]
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
  - {kind: itch, url: "https://nebu-soku.itch.io/walking-dots", best: true, note: "грати в браузері; опис «eat, digest, grow and think», коментарі (ключ X, рівні до 27, діагональний трюк), devlog"}
  - {kind: other, url: "https://www.puzzlescript.net/editor.html?hack=7994d9b1bf4dafee95b5b3ff5357b2da", note: "сирець PuzzleScript: обʼєкти, шари, правила digest/slide/block/lost/fix, 27 рівнів"}
  - {kind: other, url: "https://api.github.com/gists/7994d9b1bf4dafee95b5b3ff5357b2da", note: "той самий сирець як gist JSON (2024-10-04)"}
  - {kind: other, url: "https://nebu-soku.itch.io/walking-dots/devlog", note: "devlog: прибрано ненавмисний розвʼязок рівня 8 (2024-10-05)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Walking+Dots+puzzlescript+nebu+soku", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-4dir, keyboard-controls, body-queue, push-object, multi-cell-size, environment-death, all-on-targets, undo-unlimited, restart-level, sequential-levels, level-from-txt, save-progress, +grow-on-eat, +digest-step, +food-capacity, +segment-support, +fix-on-target, +cut-tail-to-block, +grow-recoil]
proposes: ["+effect:digest", "+window:message-screen", "+axis:undo", "+axis:control", "+card:digest-step", "+card:food-capacity", "+card:fix-on-target", "+card:cut-tail-to-block", "+card:grow-recoil"]
author: opus
date: 2026-11-19
---

# Walking Dots — черв'як із крапок їсть, перетравлює й росте, щоб викласти себе на цілі

## Суть
Покрокова PuzzleScript-головоломка nebu soku (2024): ти — черв'як-ланцюжок крапок. Голова їсть їжу й стає «повною» крапкою; клавіша X **перетравлює** — кожна порція їжі зсувається тілом на одну крапку до хвоста, а повний хвіст вирощує нову крапку позаду себе. Мета — вкрити цілі: мала ціль приймає порожню крапку, велика — повну; крапка, що стала на свою ціль, **застигає** стіною, а тіло за нею відривається й стає штовхальним блоком. Рівні — острівці над прірвою: черв'як не падає, поки хоч одна крапка на підлозі; ріст у стіну відштовхує весь черв'як уперед.

## Поле і час
- Квадратна сітка; рівні шириною 9–23 і висотою 7–21 клітина разом із прірвою довкола (сирець). Більшість рівнів — острівці підлоги посеред прірви, частина обнесена стінами.
- Шари сирця: тло/прірва → ціль → тіло → їжа/блок → голова/стіна/застигла крапка. Тіло і блок можуть на мить ділити клітину: новий хвіст, що виріс «на» блоці, виштовхує його.
- Хід = крок голови або перетравлення. Рушій має `realtime_interval 0.03`: відкладені наслідки (поїдання, застигання, падіння) спрацьовують наступним тіком, тобто майже одразу.
- Камера статична, рівень видно цілим; 24 основні рівні + 3 «Extra»; тіло — до 20 крапок (обʼєкти `body1…body20`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Голова | player | порожня / повна; напрям погляду | крок у 4 напрямки; заходить на їжу — їсть; штовхає блоки, а коли черв'як повний — і їжу; не йде в шию й у тіло, крім хвоста |
| Крапка тіла | segment | порожня / повна; номер 1–20 | стає на місце попередньої (`body-queue`); зберігає їжу; тримає черв'яка над прірвою |
| Хвіст | segment | остання крапка | у його клітину голова зайти може (хвіст звільняє); повний хвіст при перетравленні вирощує нову крапку |
| Їжа | pickup | — | зʼїдена → повною стає голова або найближча порожня крапка; поки черв'як повний — тверда й штовхається; над прірвою падає |
| Мала ціль | terrain | — | порожня крапка чи малий блок на ній застигає |
| Велика ціль | terrain | іноді з їжею на старті | застигає лише повна крапка чи великий блок |
| Застигла крапка (мала / велика) | static | на своїй цілі | стіна: блокує рух, від неї відштовхується ріст; зараховується в перемогу |
| Блок (малий / великий) | object | ланцюжок-фігура з відірваних крапок | штовхається цілим; падає, лише коли жодна клітина не на підлозі; на своїй цілі застигає |
| Стіна | static | — | непрохідна; ріст у неї відштовхує весь черв'як |
| Прірва | hazard | — | черв'як, блок чи їжа, що цілком над нею, падає й зникає |
| Підлога | terrain | — | опора |

## Правила (КОЛИ → ЯКЩО → ТО)
Рух і поїдання:
- КОЛИ `input(dir)` → ЯКЩО `free(head+dir)` → ТО `move(head, dir)`; тіло — `custom: «кожна крапка стає на місце попередньої»`.
- КОЛИ `input(dir)` → ЯКЩО `occupied(head+dir, neck)` або `occupied(head+dir, body)` і `not custom: «це хвіст»` → ТО `block`.
- КОЛИ `input(dir)` → ЯКЩО `occupied(head+dir, block)` → ТО `push` (увесь ланцюжок блока й те, що за ним), `move(head, dir)`; ЯКЩО `custom: «ланцюжок упирається в стіну чи в тіло»` → ТО `block`.
- КОЛИ `enter(head, food)` → ЯКЩО `not state(head, full)` → ТО `pickup`, `set_state(head, full)`.
- КОЛИ `enter(head, food)` → ЯКЩО `state(head, full)` → ТО `pickup`, `set_state(custom: «найближча до голови порожня крапка», full)`.
- КОЛИ `input(dir)` → ЯКЩО `occupied(head+dir, food)` і `count(empty_dot, ==, 0)` (голова й усі крапки повні) → ТО `push` (їжа як блок).

Перетравлення:
- КОЛИ `input(action)` → ТО `custom: «кожна порція їжі зсувається на одну крапку до хвоста»` (обробка з хвоста).
- КОЛИ `input(action)` → ЯКЩО `state(tail, full)` → ТО `clear_state(tail, full)`, `grow(worm, 1)`, `spawn_at(dot, «позаду хвоста на продовженні останньої ланки»)`.
- Черв'як із самої голови: КОЛИ `input(action)` → ЯКЩО `state(head, full)` → ТО `clear_state(head, full)`, `spawn_at(dot, «позаду голови, проти погляду»)`.
- Нова крапка: ЯКЩО `occupied(behind_tail, worm)` або `custom: «там блок чи їжа, які не зрушити»` → ТО `block` (перетравлення скасовано).
- Нова крапка: ЯКЩО `occupied(behind_tail, block)` або `occupied(behind_tail, food)` і `free(cell_behind_it)` → ТО `push` (виштовхує назад).
- Нова крапка: ЯКЩО `cell(behind_tail, wall)` або `cell(behind_tail, fixed)` → ТО `custom: «увесь черв'як жорстко зсувається на 1 від стіни (у бік передньої сусідки хвоста), штовхаючи все перед собою»`; ЯКЩО зсув неможливий → ТО `undo` (їжа вертається, нової крапки нема).

Прірва:
- КОЛИ `tick` → ЯКЩО `not supported(worm)` (жодна крапка не на підлозі) → ТО `fall(worm)`, `disappear_a` — гравця більше нема, лишаються `undo` / `restart`.
- КОЛИ `tick` → ЯКЩО `not supported(block)` (жодна клітина ланцюжка не на підлозі) → ТО `fall(block)`, `disappear_a`; їжа над прірвою — так само.

Цілі й відрив:
- КОЛИ `tick` → ЯКЩО `occupied(small_target, empty_dot)` і `custom: «крапка стоїть тут з минулого тіку»` → ТО `transform(dot, fixed_small)`.
- КОЛИ `tick` → ЯКЩО `occupied(big_target, full_dot)` і `custom: «крапка стоїть тут з минулого тіку»` → ТО `transform(dot, fixed_big)`; повна крапка через малу ціль і порожня через велику проходять.
- КОЛИ `enter(block, target)` → ЯКЩО `same(block, target, size)` → ТО `transform(block_cell, fixed)`; ланцюжок блока рветься в цьому місці.
- КОЛИ `after(transform(segment, fixed))` → ТО `detach(worm, tail_part)`, `transform(tail_part, block)` — порожні крапки → малі блоки, повні → великі, форма ланцюжка зберігається; передня частина грає далі коротшим черв'яком.
- КОЛИ `after(transform(head, fixed))` → ТО `custom: «тіло без голови завмирає»` — це або останній крок рівня, або глухий кут.

Перемога і підказка:
- КОЛИ `all_on(fixed_dot, target)` → ЯКЩО `not custom: «щось ще падає»` → ТО `win`, `next_level`.
- Рівень 2: КОЛИ `custom: «повна голова без тіла стоїть кілька тіків»` → ТО `message("X to digest.")`.
- Перемога: на кожній цілі застигла крапка свого розміру. · Поразка: формальної нема — падіння в прірву чи передчасне застигання голови = глухий кут, вихід через undo/restart. · Рахунку нема.

## Керування і ввід
- Стрілки / WASD — крок голови; X — дія PuzzleScript = перетравити (так і пише гра: «X to digest.»).
- Z — undo без ліміту; R — рестарт рівня; Esc — меню (стандарт PuzzleScript; у сирці не вимкнено `noundo` / `norestart`).
- Швидкий ввід через realtime-тік дає трюки: горизонталь і вертикаль в одному тіку проводять голову крізь діагональну щілину (коментар-спойлер на itch).

## Вікна, меню, HUD
- `main-menu` (титульний екран PuzzleScript): «Tenten-mushi / Walking Dots», nebu soku; start game / continue (?).
- `game-screen`: лише поле, без HUD; темно-синій фон, фіолетовий текст повідомлень (сирець).
- `custom-window` (повідомлення PuzzleScript): «X to digest.» на рівні 2, «Extra 1/3 … 3/3» перед додатковими рівнями, «Thanks for playing!» у кінці.
- `pause-menu` (Esc): повернення на титул (?).
- Переходи: main-menu → game-screen → (усі цілі) наступний рівень → … → «Extra 1/3» → … → «Thanks for playing!».

## Фічі поза полем
- `undo` без ліміту й `restart-level` — стандарт PuzzleScript; автовідкату після падіння нема.
- `levels-sequential`: 24 рівні + 3 Extra; вибору рівня в сирці нема; `continue` — PuzzleScript памʼятає рівень у браузері (?).
- Звук — лише кінець рівня (`endlevel` у SOUNDS).
- Безкоштовна браузерна гра на itch; devlog латав ненавмисний розвʼязок рівня 8.

## Варіації й родичі
- У корпусі: [Snakebird](snakebird.md) (опора будь-яким сегментом, ріст від фрукта), [Can of Wormholes](can-of-wormholes.md), [Would You Love Me If I Was A Snake](would-you-love-me-if-i-was-a-snake.md), [Temple of Snek](temple-of-snek.md), [The Snake That Eats Puzzle Game Mechanics](the-snake-that-eats-puzzle-game-mechanics.md); того ж автора — [Magicube](../grid-platformer/magicube.md).
- **Осі варіацій:**
  - коли їжа стає тілом — одразу (Snake, Snakebird) / зберігається й просувається командою, ріст біля хвоста (Walking Dots);
  - де зʼявляється нова клітина — на місці хвоста (Snake) / позаду хвоста по прямій, з виштовхуванням або відштовхуванням (Walking Dots);
  - опора — гравітація вниз (Snakebird) / прірва при вигляді згори: падає лише те, що цілком над порожнечею (Walking Dots);
  - мета — дійти до виходу / вкрити цілі власним тілом, яке застигає (Walking Dots);
  - відрізане тіло — зникає / стає штовхальним блоком-ланцюжком (Walking Dots).

## Цікавинки для курсу
- Перетравлення: стани «порожня/повна» вздовж `body-queue`, зсув на 1 до хвоста й ріст із хвоста — 🥉 (обробляти з хвоста, щоб не затерти).
- Ріст у стіну → жорсткий зсув усього черв'яка з ланцюговим штовханням і відкатом, якщо не вийшло — 🥈.
- Застигання за розміром + відрив хвоста в блок-ланцюжок, що зберігає форму й штовхається цілим — 🥈 (розщеплення ланцюга, рух поліоміно).
- Прірва з опорою «хоч одна клітина на підлозі» для черв'яка і блоків — 📎.
- Повний черв'як не їсть: їжа стає твердою — 🌱.
- Розвʼязувач: BFS по станах (крапки, вміст їжі в кожній, блоки, застиглі) — 🥇.
- Те саме як система правил-перезаписів PuzzleScript (`late`, `rigid`, шари) — 🥇.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ крок голови; `body-queue` ↔ тіло; `push-object` + `multi-cell-size` ↔ блоки-ланцюжки й тверда їжа; `environment-death` ↔ прірва; `all-on-targets` ↔ цілі; `undo-unlimited` + `restart-level` ↔ Z / R; `sequential-levels` ↔ 24 + 3 рівні; `level-from-txt` ↔ ASCII-рівні PuzzleScript; `save-progress` ↔ continue (?).
- **Нема** → пропозиції карток:
  - `+grow-on-eat` (Snakebird) — тут відкладений · слот {when: instant|digest}.
  - `+digest-step` «Їжа просувається тілом за командою; з хвоста — нова клітина» · entities/state · 🥉.
  - `+food-capacity` «Повний не їсть: їжа стає штовхальною» · entities/interact · 🌱.
  - `+segment-support` (Snakebird) — слот {support: any, view: top-down-abyss}.
  - `+fix-on-target` «Сутність на своїй цілі застигає стіною» · entities/state · 📎 · слот {match: size}.
  - `+cut-tail-to-block` «Відрізане тіло стає блоком-ланцюжком» · entities/interact · 🥈.
  - `+grow-recoil` «Ріст у стіну відштовхує все тіло» · entities/move · 🥈.

## Пропозиції до словників
- `+effect:digest` — уся їжа в тілі зсувається на 1 крапку до хвоста, з повного хвоста — нова крапка (родич `grow`).
- `+window:message-screen` — повноекранне повідомлення PuzzleScript між рівнями (тут — підказка й «Extra»).
- `+axis:undo` — `unlimited`; `+axis:control` — `direct`.
- `+card:digest-step`, `+card:food-capacity`, `+card:fix-on-target`, `+card:cut-tail-to-block`, `+card:grow-recoil` — див. «Мапа на каталог».

## Джерела
- ⭐ [itch.io: Walking Dots](https://nebu-soku.itch.io/walking-dots) — опис «eat, digest, grow and think», PuzzleScript, HTML5, коментарі: ключ X, рівні до 27, діагональний трюк, розʼєднане тіло.
- [PuzzleScript: сирець](https://www.puzzlescript.net/editor.html?hack=7994d9b1bf4dafee95b5b3ff5357b2da) і [gist API](https://api.github.com/gists/7994d9b1bf4dafee95b5b3ff5357b2da) — повні правила (рух, digest, slide, block, lost, fix), умова перемоги `all Target on winnable`, 24 + 3 рівні, повідомлення.
- [Devlog](https://nebu-soku.itch.io/walking-dots/devlog) — виправлення рівня 8.
- YouTube: [пошук «Walking Dots puzzlescript»](https://www.youtube.com/results?search_query=Walking+Dots+puzzlescript+nebu+soku).

## Непевне
- (?) Клавіші Z / R / Esc і тач — стандарт PuzzleScript; у сирці не вимкнені, у грі не перевірено.
- (?) «2nd page» рівнів 21–27 у коментарях — у сирці вибору рівнів нема; можливо, itch-збірка відрізняється від gist від 2024-10-04.
- (?) Тайминг застигання (наступний realtime-тік) і діагональний прохід — висновок із сирця й коментаря, не з гри.
- (?) Рядок сирця `late [ canteat Targetbig … ] -> [ prefixedbig Targetsmall … ]` міняє велику ціль на малу — схоже на описку; на гру може не впливати.
- (?) Як гра поводиться, коли голова застигла раніше за тіло (решта завмирає), — висновок із правил.
