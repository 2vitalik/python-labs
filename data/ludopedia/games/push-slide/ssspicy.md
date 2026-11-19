---
title: "SSSPICY!"
slug: ssspicy
aka: [Ssspicy]
family: push-slide
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: collect
year: 2022
platforms: [web (HTML5), Windows, mobile browser]
links:
  - {kind: itch, url: "https://torcado.itch.io/ssspicy", best: true, note: "грати в браузері; «eat all the food and get back to its home»; керування Z/R/Esc/Shift+T і тач; Grand Prize Kajam 2022; v1.1.2 HTML і Windows"}
  - {kind: play, url: "https://html-classic.itch.zone/html/6192812/index.html", note: "HTML5-збірка (Stencyl/OpenFL); у kajam22b.js — типи плиток, рух, поштовх, віддача перцю, привид, нора, сипучий пісок, падіння"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=SSSPICY+torcado+snake+puzzle", note: "пошук; геймплей"}
stage: v1
coverage: 80
mechanics: [move-4dir, keyboard-controls, swipe-gestures, body-queue, self-collision, push-object, destructible-blocks, collect-all, reach-exit, environment-death, player-death, undo-unlimited, restart-level, skip-level, sequential-levels, save-progress, settings-window, volume-control, movement-animation, particles, sound-effects, +push-chain, +grow-on-eat, +segment-support, +ghost-phase, +cut-body, +eat-when-blocked, +recoil-slide, +exit-opens-when-cleared]
proposes: ["+effect:recoil", "+effect:burn", "+card:eat-when-blocked", "+card:recoil-slide", "+card:exit-opens-when-cleared", "+feature:clear-save-hold"]
author: opus
date: 2026-11-19
---

# SSSPICY! — змійка-сокобан: зʼїж усю їжу й заповзи в нору, а перець вистрілює тебе назад, як ракету

## Суть
Змійка торкадо (torcado, Kajam 2022 — головний приз) ходить по маленькому острову 9×9 і має зʼїсти всю їжу, щоб відкрилась нора. Їжа — не точки Snake, а сокобан-обʼєкти: змійка **штовхає** банан чи перець, доки той не впреться, і лише тоді зʼїдає. Банан подовжує тіло, перець дає вогняне дихання з віддачею — уся змійка зʼїжджає назад до упору, пропалюючи дерево й лід перед пащею, а привидний перець на 10 ходів робить її безтілесною.

Поразки — падіння з острова, сипучий пісок, загублена їжа; undo без ліміту, тож гра — чистий пазл.

## Поле і час
- Поле 9×9 клітин; острів — клітини землі, решта — прірва. Під кожною клітиною — шар землі (земля / пісок / сипучий пісок / нора), над ним — шар предметів і змійки.
- Хід = натискання; без вводу нічого не рухається. Віддача перцю — анімована серія кроків (клітина за ~0,1 с), під час неї ввід заблоковано.
- Камера статична, увесь острів на екрані; перед рівнем предмети «падають» на свої місця.
- 23 рівні (сцени s1–s23) і титульна сцена s0; нове вводиться поступово: s1 перці й каміння, s3 банани, s7 дерево й пісок, s10 лід, s13 сипучий пісок, s19 привидні перці.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Голова змійки | player | напрям | рух 4 боки; штовхає штовхальне; їсть їжу, яку не може штовхнути |
| Тіло | segment | довжина | повторює шлях голови; голові непрохідне, крім кінчика хвоста |
| Банан | pickup | їжа | штовхається; зʼїдений → +1 сегмент |
| Перець | pickup | їжа | штовхається; зʼїдений → вогонь уперед і віддача змійки назад до упору |
| Привидний перець | pickup | їжа, 10 ходів | зʼїдений → змійка-привид: проходить крізь предмети, не їсть |
| Камінь | static | — | непрохідний, не горить |
| Дерево | static | горить | непрохідне; вогонь перед пащею його спалює |
| Лід | object | тане | штовхається; вогонь перед пащею його розтоплює |
| Відрізаний шматок | object | група | частина тіла, відрізана після привида; штовхається цілою групою |
| Нора | static | закрита / відкрита | відкрита, коли на полі нема їжі; голова в ній → перемога |
| Земля, пісок | terrain | — | опора для змійки й предметів |
| Сипучий пісок | hazard | — | голова на ньому → змійка тоне |
| Прірва | hazard | — | предмет без опори падає; змійка падає, якщо жоден сегмент не на землі |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(head, dir)`, `custom: «кожен сегмент стає на місце попереднього»`.
- КОЛИ `input(dir)` → ЯКЩО `occupied(next, body|stone|wood)` → ТО `block`; клітина кінчика хвоста вважається вільною, бо хвіст іде далі (окрім змійки з 2 сегментів, що розвертається назад).
- КОЛИ `contact(head, food|ice|piece)` → ЯКЩО `free(cell_behind)` → ТО `push`, `move(head, dir)` — ряд штовхальних предметів їде весь.
- КОЛИ `contact(head, food)` → ЯКЩО `not free(cell_behind)` → ТО `move(head, dir)`, `disappear(food)` — їжу зʼїдено лише тоді, коли її нема куди штовхнути.
- КОЛИ `picked(head, banana)` → ТО `grow(snake, 1)` — новий сегмент на місці, звідки щойно пішов хвіст.
- КОЛИ `picked(head, pepper)` → ТО `set_state(head, fire_breath)`, `slide(snake, back)` — уся змійка жорстко зсувається проти погляду голови по клітині, доки якийсь сегмент не впреться; дорогою штовхає штовхальне.
- КОЛИ `tick` → ЯКЩО `state(head, fire_breath)` and `occupied(ahead_of_head, wood|ice)` → ТО `disappear(wood|ice)` — дерево згорає, лід тане.
- КОЛИ `edge(snake)` → ТО `lose` — віддача винесла змійку (чи штовхнуте нею) за край поля, змійка вилітає.
- КОЛИ `picked(head, ghost_pepper)` → ТО `set_state(snake, ghost, 10)` — 10 ходів напівпрозора: блокує лише власне тіло, їсти не може.
- КОЛИ `state_off(snake, ghost)` → ЯКЩО `occupied(segment_cell, stone|wood|ice|piece)` → ТО `detach(tail_part, snake)`, `transform(tail_part, piece)` — сегмент у предметі й хвіст за ним стають мертвим шматком; якщо так зріже голову → `lose`.
- КОЛИ `state_off(snake, ghost)` → ЯКЩО `occupied(segment_cell, food)` → ТО `disappear(food)`, `lose` — їжу розчавлено.
- КОЛИ `all_gone(food)` → ТО `set_state(hole, open)`.
- КОЛИ `enter(head, hole)` → ЯКЩО `state(hole, open)` → ТО `custom: «змійка по сегменту заповзає в нору»`, `win`, `next_level`.
- КОЛИ `enter(head, quicksand)` → ТО `custom: «змійка тоне по сегменту»`, `lose`.
- КОЛИ `after(move)` → ЯКЩО `not supported(snake)` → ТО `fall(snake)`, `lose` — достатньо, щоб на землі був хоч один сегмент.
- КОЛИ `after(move)` → ЯКЩО `not supported(item)` → ТО `fall(item)`; якщо впала їжа → `lose`.
- КОЛИ `input(z)` → ТО `undo`; КОЛИ `input(r)` → ТО `restart`.
- Перемога: уся їжа зʼїдена й голова в норі. · Поразка: змійка впала чи вилетіла за край, голова в сипучому піску, їжа впала чи вилетіла, привид розчавив їжу або зрізав голову — далі undo. · Рахунку нема.

## Керування і ввід
- Стрілки — крок голови (поштовх і їжа — тим самим кроком).
- Z — undo без ліміту; R — рестарт; Esc або Space — меню налаштувань (звідти можна пропустити будь-який рівень); утримати Shift+T — стерти збереження.
- Мобільний браузер: торкнутись і провести в напрямку руху; кнопки undo й рестарт на екрані.

## Вікна, меню, HUD
- `splash-screen` / титул — сцена s0 з назвою (?).
- `game-screen`: острів на весь екран, HUD нема; кнопки undo й рестарт — лише на тачі.
- `settings-window` (Esc/Space): гучність звуку, тряска екрана, пропуск рівня.
- `end-screen`: змійка заповзає в нору → перехід до наступного рівня; у кінці — фінальна сцена.
- Поразка: «сльоза» в змійки й підказка про undo/рестарт.
- Переходи: титул → рівень → (нора) наступний рівень → … → фінал.

## Фічі поза полем
- `undo` без ліміту, `restart-level`, пропуск будь-якого рівня з меню (`skip-level` без ліміту).
- `autosave` прогресу; Shift+T — стерти збереження.
- `screen-shake-toggle`, `volume-sliders`; `touch-controls` (свайп).
- Вибору рівнів нема (гравці просили в коментарях); редактора нема.

## Варіації й родичі
- [snakebird](../thinky/snakebird.md) — змійка з гравітацією і їжею-ростом; [would-you-love-me-if-i-was-a-snake](../thinky/would-you-love-me-if-i-was-a-snake.md) — опора будь-яким сегментом; [snake](../maze-arcade/snake.md) — класичне тіло-черга; [the-snake-that-eats-puzzle-game-mechanics](../thinky/the-snake-that-eats-puzzle-game-mechanics.md).
- [sokoban](sokoban.md) — штовхання; [bonfire-peaks](../thinky/bonfire-peaks.md) — вогонь як спосіб прибрати перешкоду.
- Осі варіацій:
  - **їжа**: зʼїдається при дотику (Snake) / лише коли впирається (тут);
  - **що дає їжа**: ріст / віддача з вогнем / безтілесність на N ходів;
  - **опора**: гравітація вниз (Snakebird) / хоч один сегмент на землі згори (тут);
  - **ціль**: зібрати все → відкривається вихід (нора).

## Цікавинки для курсу
- Поштовх перед поїданням: їжа — штовхальний обʼєкт, зʼїсти можна лише притиснувши — 🌱.
- Тіло-черга з ростом у клітину, звідки пішов хвіст — 🌱.
- Віддача: жорстке зсування всієї змійки назад до упору з поштовхом предметів і перевіркою краю поля — 📎.
- Вогонь перед пащею під час віддачі: на кожному кроці спалити дерево / розтопити лід — 🌱.
- Привид на 10 ходів і розріз тіла на виході з нього (мертві шматки стають штовхальною групою) — 🥉.
- Опора хоч одним сегментом + падіння предметів у прірву — 📎.
- Розвʼязувач рівня 9×9 (BFS по позиції змійки, предметах і стані привида) — 🥈.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` + `swipe-gestures` ↔ стрілки й тач; `body-queue` ↔ тіло; `self-collision` ↔ голова не входить у тіло; `push-object` ↔ їжа, лід, шматки; `destructible-blocks` ↔ дерево й лід під вогнем; `collect-all` + `reach-exit` ↔ уся їжа → нора; `environment-death` + `player-death` ↔ прірва, сипучий пісок; `undo-unlimited` + `restart-level` + `skip-level` ↔ Z, R, меню; `sequential-levels` + `save-progress` ↔ 23 рівні й автозбереження; `settings-window` + `volume-control` ↔ Esc; `movement-animation` + `particles` + `sound-effects` ↔ анімації, вогонь, хрумкіт.
- **Нема** → пропозиції карток:
  - `+push-chain` (є в корпусі) — ряд предметів штовхається весь.
  - `+grow-on-eat` (є в корпусі) — банан додає сегмент.
  - `+segment-support` (є в корпусі) — опора будь-яким сегментом.
  - `+ghost-phase` (є в корпусі) — тут проходить крізь предмети сам гравець, 10 ходів.
  - `+cut-body` (є в корпусі) — розріз тіла, відрізане стає штовхальним шматком.
  - `+eat-when-blocked` «Їжа штовхається, зʼїдається лише впершись» · entities/interact · 🌱.
  - `+recoil-slide` «Віддача: аватар ковзає назад до упору» · entities/move · 📎 · слот {trigger: pickup}.
  - `+exit-opens-when-cleared` «Вихід відкривається, коли зібрано все» · game-logic/win · 🌱 (родич `collect-quota`).

## Пропозиції до словників
- `+effect:recoil` — зсув назад до упору як наслідок дії (перець); `slide(snake, back)` не каже, що причина — власна дія.
- `+effect:burn` — спалити / розтопити клітину перед джерелом вогню (повтор: кандидат у корпусі).
- `+card:eat-when-blocked`, `+card:recoil-slide`, `+card:exit-opens-when-cleared` — див. «Мапу на каталог».
- `+feature:clear-save-hold` — стерти збереження утриманням комбінації (Shift+T), без меню.

## Джерела
- ⭐ [itch.io: SSSPICY!](https://torcado.itch.io/ssspicy) — гра в браузері, опис, керування (Z/R/Esc/Space/Shift+T, тач), Kajam 2022, коментарі (виштовхнута за край їжа → «сльоза» й підказка undo).
- [HTML5-збірка](https://html-classic.itch.zone/html/6192812/index.html) — `kajam22b.js`: типи плиток і їхні властивості (`pepper`, `banana`, `ghostPepper`, `stone`, `wood`, `ice`, `hole`, `sand`, `quicksand`), функції `slideAndEatTile`, `slideBody`, `handleFire`, `ghost`/`endGhost`, `cutBody`, `checkHole`, `checkFall`, `checkItemFall`, `checkQuicksand`; `lib/default.pak` — список сцен s0–s23 і їхній склад.
- YouTube: пошук «SSSPICY torcado snake puzzle».

## Непевне
- (?) Титульна сцена s0 (змійка, перець, камінь, без нори): схоже, гра стартує, коли змійка зʼїдає перець і вилітає з поля, — з коду, не перевірено в грі.
- (?) Пісок поводиться як звичайна земля — у коді для нього бачу лише інший вигляд.
- (?) Пауза перед віддачею (довжина звуку) і темп 0,1 с на клітину — з коду; на швидкості гри не перевіряв.
- (?) Як саме поводиться тач-керування (свайп чи утримання) — зі слів сторінки «touch and drag».
