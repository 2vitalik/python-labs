---
title: BoxUp (Clickmazes BoxUp)
slug: boxup
aka: [Clickmazes BoxUp, Original BoxUp, Boxup]
family: push-slide
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2003
platforms: [web (Java applet, 2003), web (PuzzleScript Plus, 2022), iOS]
links:
  - {kind: itch, url: "https://clickmazes.itch.io/original-boxup", best: true, note: "грати: 29 пазлів, клавіші й тач, кредити, «tiny inside-out Sokoban»"}
  - {kind: official, url: "https://www.clickmazes.com/boxup/new-boxup.htm", note: "clickmazes: правила, набори 12 + 5 + 12, довжини розвʼязків, порти"}
  - {kind: other, url: "https://gist.github.com/angilbert/192b7403618c6c10eccb83986283053b", note: "код PuzzleScript: шари, правила входу, поштовху зсередини й вкладення, 29 рівнів"}
  - {kind: play, url: "https://auroriax.github.io/PuzzleScript/play.html?p=192b7403618c6c10eccb83986283053b", note: "hackable-версія в PuzzleScript Plus"}
  - {kind: other, url: "https://apps.apple.com/us/app/clickmazes-boxup/id512061618", note: "iOS-застосунок (110 пазлів з даних Bob Henderson)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=clickmazes+BoxUp", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [move-4dir, keyboard-controls, swipe-gestures, push-object, impassable-cells, orientation-state, level-select, sequential-levels, undo-unlimited, restart-level, sound-effects, +enter-box, +push-from-inside, +nest-boxes, +open-side-box]
proposes: ["+card:open-side-box", "+card:push-from-inside", "+card:nest-boxes", "+card:enter-box", "+window:title-screen", "+window:message-screen"]
author: opus
date: 2026-11-09
---

# BoxUp — «Sokoban навиворіт»: коробки відкриті з одного боку, штовхаєш лише зсередини, малу треба загнати у велику

## Суть
На крихітному полі (3×3, N×2, 4×3) стоять порожнисті коробки двох розмірів, кожна відкрита з одного боку. Гравець заходить у коробку лише через відкритий бік і рухає її, лише штовхаючи зсередини її закриту стінку; ззовні коробку не зрушити. Мала коробка може заїхати у велику (разом із гравцем усередині) і далі їздить у ній. Мета — малу червону коробку поставити у велику синю; чорні коробки допомагають або заважають.

## Поле і час
- Квадратна сітка в стінах; ігрові поля дуже малі: оригінальні 3×3, набір Don O'Brien — N×2 (найбільший 6×2, розвʼязок 108 ходів), Bob Henderson — 4×3 (найдовший розвʼязок 153).
- Шари однієї клітини (PuzzleScript): підлога → стіна → **велика коробка** → **гравець** → **мала коробка**. Отже, в одній клітині можуть бути велика, гравець і мала одночасно: гравець — у малій, мала — у великій.
- Орієнтація коробки = відкритий бік (N / E / S / W); вона не змінюється.
- Хід = крок гравця, можливо з коробкою; без вводу нічого не рухається. Невдалий хід скасовується повністю (звук Cancel).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | — | ходить по підлозі; входить і виходить з коробки лише через відкритий бік; рухає коробку, штовхаючи закриту стінку зсередини |
| Мала червона коробка | container | відкритий бік | ціль гри: має опинитися у великій синій |
| Велика синя коробка | container | відкритий бік | приймає малу; везе її всередині |
| Чорні коробки (малі й великі) | container | відкритий бік | нейтральні: ті самі правила, служать «ключами» або перешкодами |
| Стіна | static | — | непрохідна для гравця й коробок |
| Старт у стіні (`q`) | static | позначка рівня | на старті гравець переходить зі стіни в сусідню коробку — рівень починається «всередині» |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `cell(next_cell, wall)` → ТО `block`.
- КОЛИ `input(dir)` → ЯКЩО `occupied(next_cell, box)` і `not facing(box, -dir)` (бік, з якого заходиш, закритий — у будь-якої коробки клітини) → ТО `block`.
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` або всі коробки там `facing(box, -dir)` → ТО `move(player, dir)` (гравець усередині найменшої).
- КОЛИ `input(dir)` → ЯКЩО `occupied(here, box)` і `facing(box, dir)` → ТО `custom: «коробка лишається, гравець виходить через відкритий бік»`.
- КОЛИ `input(dir)` → ЯКЩО `occupied(here, box)` і `not facing(box, dir)` → ТО `push`: `move(box, dir)`, `move(player, dir)` — штовхання зсередини.
- КОЛИ `input(dir)` → ЯКЩО `occupied(here, small)` і `occupied(here, big)` і `facing(big, dir)` і `not facing(small, dir)` → ТО `move(small, dir)`, `move(player, dir)` — мала виїжджає з великої через її відкритий бік.
- КОЛИ `after(move(big, dir))` → ЯКЩО `occupied(big_cell, small)` → ТО `carry(big, small)` — мала їде всередині.
- КОЛИ `custom: «коробка заходить у клітину з іншою коробкою»` → ЯКЩО велика → мала, велика → велика або мала → мала → ТО `block` (скасовується весь хід); мала → велика дозволено, але лише через відкритий бік великої (туди мусить пройти гравець).
- Штовхнути ряд коробок не можна: поштовх рухає лише ту коробку, в якій стоїш.
- КОЛИ `enter(red_small, blue_big)` → ТО `win`, `next_level` (у коді: `some redX on blueX`).
- КОЛИ `level_start` → ЯКЩО `occupied(player_cell, wall)` → ТО `move(player, adjacent_box)`.
- КОЛИ `input(undo)` → ТО `undo(1)`; КОЛИ `input(restart)` → ТО `restart`.
- Перемога: червона мала у синій великій. · Поразка: нема; глухий кут → undo/рестарт. · Рахунок: нема (на сторінці — довжини оптимальних розвʼязків як міра складності).

## Керування і ввід
- Клавіатура: стрілки / WASD — крок; `Z` — undo; `R` — рестарт.
- Тач: тап у головному меню, свайп — рух, меню-вкладка вгорі ліворуч — undo / рестарт.
- Повтор клавіші при утриманні — раз на 0,5 с (`key_repeat_interval`).

## Вікна, меню, HUD
- `title-screen` (custom, PuzzleScript Plus): «Clickmazes BoxUp», Andrea Gilbert.
- `level-select` (PuzzleScript Plus `level_select`): розділи «Andrea: 3x3 #1…», набори Original [12], Nx2 [5], 4x3 [12].
- `message-screen` (custom): правило на старті («Push the small red box into the large blue box. You can only push a box from the inside.»), заставка кожного набору з автором і роком, фінал «Thank you for playing :)».
- `game-screen`: поле без HUD; на тачі — меню-вкладка з undo / restart.
- Переходи: title → level-select або наступний рівень → набір → фінал.

## Фічі поза полем
- `puzzle-bank` з трьох наборів (29 пазлів), `level-select` по розділах, `levels-sequential`.
- `undo` ∞, `restart-level`, `touch-controls`.
- iOS-застосунок: 110 пазлів, відібраних з даних Bob Henderson, саундтрек Robert Adams.
- Відкритий код (hackable у PuzzleScript Plus).

## Варіації й родичі
- Історія: концепція й 12 пазлів Andrea Gilbert (2003, Java-аплети) → Don O'Brien, 5 пазлів N×2 (2003) → Bob Henderson, вичерпний пошук простору і 12 пазлів 4×3 (2012) → PuzzleScript-версія (2022) → iOS; порти Boxup (SVG, Henri Manson), Boxup (JS, Graham Rogers).
- Родичі в корпусі: [sokoban](sokoban.md) (той самий поштовх, але ззовні); [patricks-parabox](../thinky/patricks-parabox.md) (вхід у коробку, вкладеність — рекурсивна); [kwirk](kwirk.md) (орієнтовані турнікети); [lock-and-pin](../thinky/lock-and-pin.md) (замок насаджується лише зі свого боку — той самий clickmazes-автор).
- Осі варіацій:
  - **звідки штовхаєш**: ззовні (Sokoban) / лише зсередини (BoxUp) / зсередини рекурсивно (Parabox);
  - **хто може бути всередині**: нікого / гравець / гравець і менша коробка (BoxUp) / цілий рівень (Parabox);
  - **розміри**: один / два вкладені (BoxUp) / нескінченна вкладеність;
  - **орієнтація**: нема / відкритий бік як стан, що не змінюється (BoxUp) / змінюється поворотом.

## Цікавинки для курсу
- Клітина з кількома шарами (велика — гравець — мала) і правилами «хто в кому» — 📎.
- Вхід лише з відкритого боку: перевірка орієнтації всіх коробок цільової клітини — 🌱.
- Штовхання зсередини і перенесення вкладеної малої разом із великою — 📎.
- Атомарний хід: будь-яке порушення скасовує весь хід — 🌱.
- Розвʼязувач BFS для 3×3 / 4×3 (стан = позиції й вкладеність коробок + гравець) і пошук найдовших розвʼязків, як у Bob Henderson, — 🥈.
- Генератор «найважчих пазлів» вичерпним перебором малих полів — 🥇.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` + `swipe-gestures`; `push-object` ↔ поштовх коробки (лише зсередини); `impassable-cells` ↔ стіни; `orientation-state` ↔ відкритий бік — сторони коробки різні; `level-select` + `sequential-levels`; `undo-unlimited` + `restart-level`; `sound-effects` ↔ EndLevel, Cancel.
- **Нема** → пропозиції карток:
  - `+enter-box` (вже пропонована, Parabox) — гравець заходить у коробку.
  - `+open-side-box` «Коробка, відкрита з одного боку: вхід і вихід лише через нього» · entities/legality · 🌱 · слот {open: N|E|S|W}.
  - `+push-from-inside` «Обʼєкт рухається лише поштовхом зсередини» · entities/legality · 📎.
  - `+nest-boxes` «Мала коробка заходить у велику й їде в ній» · entities/interact · 🥉 · слот {sizes: 2}.

## Пропозиції до словників
- `+card:open-side-box`, `+card:push-from-inside`, `+card:nest-boxes`; повтор `+card:enter-box`.
- `+window:title-screen`, `+window:message-screen` — повтор.
- ⏳-слова, вжиті тут: `input`, `cell`, `occupied`, `free`, `facing` (відкритий бік = орієнтація), `move`, `carry`, `after`, `enter`, `level_start`, `undo`; роль `container` — для коробок.

## Джерела
- ⭐ [Original BoxUp на itch.io](https://clickmazes.itch.io/original-boxup) — гра, 29 пазлів, клавіші й тач, кредити (Andrea Gilbert, Don O'Brien, Bob Henderson, Auroriax), реліз червня 2022, лінки на hackable-версію й App Store.
- [clickmazes: BoxUp](https://www.clickmazes.com/boxup/new-boxup.htm) — правило («hollow and open on one side … pushing from the inside only»), мала червона у велику синю, чорні коробки, набори й довжини розвʼязків, iOS, порти.
- [Gist з кодом](https://gist.github.com/angilbert/192b7403618c6c10eccb83986283053b) — шари `wall / bigX / player / smallX`, `blockedN…`, `pushableN…`, перенесення малої у великій, заборони big→small, big→big, small→small, `some redX on blueX`, `level_select`, повідомлення; [те саме в PuzzleScript Plus](https://auroriax.github.io/PuzzleScript/play.html?p=192b7403618c6c10eccb83986283053b).
- [App Store](https://apps.apple.com/us/app/clickmazes-boxup/id512061618) — iOS-версія.
- YouTube: пошук «clickmazes BoxUp».

## Непевне
- (?) Інтерфейс Java-аплетів 2003 року (миша чи клавіші, undo) — не перевірено.
- (?) Вхід у клітину, де велика коробка відкрита до гравця, а мала всередині — ні: за кодом заборонено (перевіряються всі коробки клітини), грою не перевірено.
- (?) Чи показує `level-select` позначки «розвʼязано» — у коді лише прапорець `level_select`.
