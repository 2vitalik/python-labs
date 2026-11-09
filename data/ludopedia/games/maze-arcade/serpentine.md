---
title: Serpentine
slug: serpentine
aka: []
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: score
year: 1982
platforms: [Apple II, Atari 8-bit, C64, IBM PC, VIC-20]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Serpentine_(video_game)", best: true, note: "кольори змій, лобові удари, хвости, яйця й загін, жаби, швидкості по рівнях, 20 лабіринтів"}
  - {kind: other, url: "https://archive.org/details/Serpentine_1982_Creative", note: "мануал VIC-20: мета, 3 змії в запасі, яйця, таблиця очок"}
  - {kind: other, url: "https://www.atarimagazines.com/cva/v1n2/apple2games.php", note: "огляд Apple II 1982: загін справа, клітка злих змій зліва, плямисті й білі яйця"}
  - {kind: wiki, url: "https://fr.wikipedia.org/wiki/Serpentine_(jeu_vid%C3%A9o)", note: "FR: кожна змія періодично кладе яйце"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Serpentine+Broderbund", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-4dir, move-auto, body-queue, impassable-cells, touch-death, player-death, item-pickup, destroy-all-enemies, event-points, spawn-points, sequential-levels, progress-acceleration, speed-per-type, realtime-ai, game-pause, +length-duel, +length-color-cue, +bite-tail, +egg-extra-life, +egg-hatch-spawn, +egg-hunter, +autopilot-return, +level-score-multiplier]
proposes: ["+card:bite-tail", "+card:egg-extra-life", "+card:egg-hatch-spawn", "+card:egg-hunter", "+card:autopilot-return", "+cond:compare", "+feature:screen-adjust"]
author: opus
date: 2026-11-09
---

# Serpentine — змія проти змій у лабіринті: кусай хвости, доки ворог не стане коротшим, і бережи яйця

## Суть
Гравець веде синю «добру» змію лабіринтом і має зʼїсти всіх «злих» змій. Довший перемагає: червоного (довшого) ворога бʼють лише ззаду, відкушуючи хвіст, доки він не стане коротшим за тебе й не позеленіє — тоді його можна взяти в лоб. Яйця — головна економіка: змії відкладають їх ціною сегмента; твоє яйце, що вціліло до кінця рівня, вилуплюється в нову змію (життя), вороже — у нового ворога; жаби полюють на яйця. Близький родич [`jungler`](jungler.md) (Konami, 1981), але без пострілів і з яйцями.

## Поле і час
- Лабіринт на один екран (у більшості версій 20 лабіринтів, на картриджі Atari — 5). Справа — **загін** (захищена зона), звідки виходить змія гравця; зліва — **клітка**, з якої виходять злі змії.
- Real-time, змії рухаються безперервно, тіло повторює шлях голови.
- З рівнем вороги довшають і швидшають, а змія гравця — **повільнішає**; нова змія після смерті отримує стартову швидкість, але без набутих сегментів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Синя змія | player | довжина; 3 у запасі на старт | рух 4 напрямки; кусає хвости; бʼє головою зелених |
| Червона / помаранчева змія | enemy | довша за гравця | лобовий удар → гравець гине; укус у хвіст коротшає її |
| Зелена змія | enemy | коротша за гравця | лобовий удар → гравець її зʼїдає й росте на 1 |
| Хвіст змії | object | — | гравець відкушує сегмент: ворог −1, гравець не росте |
| Біле яйце (гравця) | container | — | доживе до повернення в загін — вилупиться нова змія гравця; ворог, що зʼїв, +1 сегмент |
| Плямисте яйце (вороже) | container | — | вилуплюється у нового ворога з 2 сегментів; гравець, що зʼїв, +1 сегмент |
| Жаба | neutral | зʼявляється у випадкові моменти | стрибає лабіринтом і йде до яйця, щоб зʼїсти; будь-яка змія, що зʼїла жабу, +1 сегмент |
| Загін (справа) | zone | — | старт і фініш гравця; тут вилуплюються збережені яйця |
| Клітка (зліва) | spawner | — | звідси виходять злі змії |
| Стіна лабіринту | static | — | непрохідна |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `move(serpent, facing)`, `custom: «тіло повторює шлях голови»`.
- КОЛИ `input(dir)` → ТО `face(player, dir)`.
- КОЛИ `contact(player_head, enemy_tail)` → ТО `grow(enemy, -1)`, `score(tail_points)`.
- КОЛИ `contact(player_head, enemy_tail)` → ЯКЩО `custom: «ворог тепер коротший за гравця»` → ТО `transform(enemy, green_serpent)`.
- КОЛИ `contact(player_head, enemy_head)` → ЯКЩО `state(enemy, green)` → ТО `disappear(enemy)`, `grow(player, +1)`, `score(head_points × segments)`; інакше `lives(-1)`.
- КОЛИ `rng(p)` → ТО `spawn(frog)`.
- КОЛИ `contact(serpent, frog)` → ТО `disappear_b`, `grow(a, +1)`; гравцю ще `score(500)`.
- КОЛИ `tick` → ЯКЩО `count(egg, >, 0)` → ТО `custom: «жаба йде до найближчого яйця»` — навіть під час автопілота в кінці рівня.
- КОЛИ `contact(frog, egg)` → ТО `disappear_b`.
- КОЛИ `custom: «змія відкладає яйце»` → ЯКЩО `counter(length, >, 2)` → ТО `spawn(egg)`, `grow(a, -1)`; інакше (змія гравця з 2 сегментів) `lives(-1)`.
- КОЛИ `timer(hatch)` → ЯКЩО `custom: «яйце вороже»` → ТО `transform(egg, enemy_serpent)` — новий ворог з 2 сегментів.
- КОЛИ `contact(player_head, enemy_egg)` → ТО `disappear_b`, `grow(player, +1)`, `score(150 × level)`.
- КОЛИ `contact(enemy_head, player_egg)` → ТО `disappear_b`, `grow(enemy, +1)`.
- КОЛИ `all_gone(enemy_serpent)` → ТО `custom: «автопілот веде змію гравця до загону»`.
- КОЛИ `reach(player, pen)` → ЯКЩО `count(player_egg, >, 0)` → ТО `lives(+1)` за кожне яйце, `next_level`.
- КОЛИ `level_start` → ТО `speed(enemies, +n)`, `grow(enemies, +n)`, `speed(player, -n)`.
- КОЛИ `died(player)` → ЯКЩО `counter(lives, >, 0)` → ТО `respawn(player, pen)` — стартова швидкість, без набутих сегментів; інакше `game_over`.
- Перемога рівня: зʼїдено всіх злих змій. Поразка: запас змій вичерпано. Рахунок (VIC-20): жаба 500 · вороже яйце 150 × рівень · хвіст 100 на рівнях 1–2, +100 кожен другий рівень · голова 200 за сегмент на рівнях 1–2, +200 кожен другий рівень.

## Керування і ввід
- Джойстик 4 напрямки — поворот змії; змія не зупиняється.
- Кнопка джойстика (VIC-20) — пауза/продовження; старт — кнопкою під час вступної музики.
- VIC-20: під час заставки джойстиком центрують зображення; утримання вправо ~20 с перемикає режим interlace.

## Вікна, меню, HUD
- `splash-screen` — вступна музика; тут же налаштування екрана (VIC-20).
- `game-screen`: лабіринт, загін справа, клітка зліва; `score`, запас змій (`lives`) (?) щодо точного складу HUD.
- `pause-menu` — кнопкою, без меню.
- Переходи: заставка → (кнопка) рівень → (усі вороги) автопілот у загін → вилуплення яєць → наступний лабіринт; запас 0 → кінець гри.

## Фічі поза полем
- `levels-sequential` — 20 лабіринтів (Atari-картридж — 5); складність росте через довжину й швидкість ворогів і сповільнення гравця.
- `pause`; `+feature:screen-adjust` — центрування й interlace у заставці (VIC-20).
- Один гравець; таблиці рекордів у джерелах нема.

## Варіації й родичі
- [`jungler`](jungler.md) — той самий бій «довший виграє» з кольором-індикатором; там постріл зрізає хвіст і тіло прохідне, тут хвіст відкушують головою, а замість пострілів — яйця й жаби.
- [`snake`](snake.md), [`nibbler`](nibbler.md) — довжина як рахунок/загроза собі; [`slither-io`](slither-io.md) — сучасна дуель змій.
- [`nimble-quest`](nimble-quest.md) — змійка, де кожен сегмент — окремий юніт.
- **Осі варіацій**: шкода ворогу — «постріл у хвіст (Jungler) / укус у хвіст (Serpentine) / лише таран»; додаткові життя — «за очки / за запас довжини (Jungler) / з яєць, що вціліли (Serpentine)»; темп — «гравець швидшає / сповільнюється з рівнем».

## Цікавинки для курсу
- Лобовий удар за порівнянням довжин + перефарбування ворога, щойно він коротший — 🌱.
- Укус у хвіст укорочує ворога, але не годує гравця (розвести «шкоду» і «ріст») — 🌱.
- Яйця: відкласти сегмент зараз → життя пізніше, якщо вціліє; вороже яйце → новий ворог — 📎.
- Жаба як нейтральний мисливець на яйця (ціль — предмет, а не гравець) — 📎.
- Автопілот у загін після перемоги (пошук шляху для аватара) — 🥉.
- Очки, що ростуть кожен другий рівень (таблиця від номера рівня) — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `move-auto` · `body-queue` · `impassable-cells` · `touch-death` · `player-death` · `item-pickup` (жаба, яйце) · `destroy-all-enemies` · `event-points` · `spawn-points` (клітка, загін) · `sequential-levels` · `progress-acceleration` · `speed-per-type` · `realtime-ai` · `game-pause`.
- **Нема** → пропозиції карток:
  - `+bite-tail` «Укус у хвіст: ворог −1, гравець не росте» · entities/combat · 🌱 (сімʼя з `+shoot-off-segment`).
  - `+egg-extra-life` «Відкладене яйце → життя, якщо вціліло до кінця рівня» · game-logic/score · 📎.
  - `+egg-hatch-spawn` «Яйце ворога вилуплюється в нового ворога» · entities/spawn · 🌱.
  - `+egg-hunter` «Нейтрал полює на предмети» · entities/move · 📎.
  - `+autopilot-return` «Після перемоги аватар сам іде на базу» · entities/move · 🥉.
  - Повтори: `+length-duel`, `+length-color-cue` (`jungler`), `+level-score-multiplier` (`nibbler`).

## Пропозиції до словників
- `+cond:compare` — порівняння властивості двох сутностей (`compare(enemy, player, length, <)`); `same` покриває лише рівність (повтор з `jungler`).
- `+feature:screen-adjust` — центрування зображення й interlace в налаштуваннях заставки (VIC-20, ранні ТВ-виходи).

## Джерела
- ⭐ [Wikipedia: Serpentine](https://en.wikipedia.org/wiki/Serpentine_(video_game)) — кольори, лобові удари, хвости, яйця й загін, жаби, швидкості по рівнях, 20/5 лабіринтів, порти.
- [Мануал VIC-20 (archive.org)](https://archive.org/details/Serpentine_1982_Creative) — «великі змії ковтають малих», атака ззаду до позеленіння, 3 змії на старт, яйце коштує сегмент, смерть при спробі відкласти з 2 сегментів, таблиця очок, пауза кнопкою, interlace.
- [Creative Computing Video & Arcade Games (1982)](https://www.atarimagazines.com/cva/v1n2/apple2games.php) — загін справа, клітка зліва, плямисті злі й білі добрі яйця, жаби.
- [Wikipedia FR](https://fr.wikipedia.org/wiki/Serpentine_(jeu_vid%C3%A9o)) — кожна змія періодично кладе яйце.
- YouTube: пошук «Serpentine Broderbund».

## Непевне
- (?) Як гравець кладе яйце — сам (кнопкою?) чи автоматично періодично; у VIC-20 кнопка — пауза, FR-вікі каже «періодично».
- (?) Чи можуть злі змії кусати хвіст гравця; чи гравець розвертається на 180°.
- (?) Скільки часу яйце до вилуплення; чи вилуплюється яйце гравця, якщо його не встигли донести (EN: лише при поверненні в загін).
- (?) Кольори відрізняються між версіями (VIC-20 — червоні, Apple — помаранчеві); EN-вікі в одному місці каже, що вороги з рівнем повільнішають — суперечить решті.
- (?) Склад HUD і чи є таблиця рекордів.
