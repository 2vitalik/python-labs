---
title: Hat-tricks
slug: hat-tricks
aka: [Hat tricks]
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
year: 2022
platforms: [web]
links:
  - {kind: official, url: "https://www.clickmazes.com/hattricks/hattricks.htm", best: true, note: "clickmazes: механіка від авторки — паличка з двома станами, капелюх-портал, hat-trick як єдиний спосіб змінити орієнтацію; історія, Pattern:Script"}
  - {kind: itch, url: "https://clickmazes.itch.io/hat-tricks", note: "грати в браузері; 16 пазлів, вересень 2022; стрілки/WASD, Z, R, свайпи"}
  - {kind: other, url: "https://gist.github.com/b81a790a66fda61d8192888ca2da072d", note: "вихідний код Pattern:Script: штовхання, трюк, віддача, розворот, 16 рівнів"}
  - {kind: other, url: "https://clementsparrow.github.io/Pattern-Script/src/editor.html?hack=b81a790a66fda61d8192888ca2da072d", note: "код у редакторі Pattern:Script"}
  - {kind: other, url: "https://itch.io/jam/thinky-puzzle-game-jam-2", note: "Thinky Puzzle Game Jam 2 (липень 2022), для якого гру задумано"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Hat-tricks+clickmazes+puzzlescript", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-4dir, move-by-input, keyboard-controls, swipe-gestures, multi-cell-size, orientation-state, push-object, impassable-cells, teleport, teleport-pair, reach-exit, undo-unlimited, restart-level, sequential-levels, sound-effects, event-effects, +rigid-stick-pusher, +portal-on-object, +push-chain, +open-side-box, +rule-discovery, +portal-sets-orientation, +portal-recoil, +portal-reverse-on-block, +pushable-exit]
proposes: ["+cond:axis", "+ui:in-field-level-number", "+window:title-screen", "+window:message-screen", "+card:portal-sets-orientation", "+card:portal-recoil", "+card:portal-reverse-on-block", "+card:pushable-exit"]
author: opus
date: 2026-11-19
---

# Hat-tricks — паличка 2×1 штовхає капелюхи-портали; повернутись можна, лише пройшовши крізь капелюх

## Суть
Логічний лабіринт Andrea Gilbert (clickmazes) на Pattern:Script — форку PuzzleScript; авторка зве його «Sokoban… of sorts». Гравець — чарівна паличка з двох клітин, горизонтальна або вертикальна: вона ходить у 4 боки, не повертаючись, і штовхає капелюхи. Кожен капелюх має один відкритий бік і пару того самого кольору; паличка, що входить в отвір кінцем уперед, «перетікає» в парний капелюх і виходить з його отвору — уже в його орієнтації. Це **єдиний спосіб змінити орієнтацію**; мету гра не називає — треба здогадатись завести паличку в білий капелюх-вихід.

## Поле і час
- Квадратна сітка; 16 кімнат від 7 до 13 клітин завширшки й від 6 до 9 заввишки разом зі стінами (код рівнів).
- Хід = зсув палички на 1. Трюк розгортається серією автоматичних кроків (`again_interval 0.1`): спершу передня половинка, потім задня.
- Шари: підлога й стіни · паличка (дві половинки, кожна «дивиться» назовні) · капелюхи з кольором і позначками вход/вихід · ефекти (пил при ударі, фінальний спалах).
- Номер рівня намальований крапками в нижній стіні: групи по 1–4 крапки, сума = номер (на рівнях 3 і 4 переплутані — авторка підтвердила на itch).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Паличка | player | 2 клітини; орієнтація H/V | зсув на 1 у 4 боки цілою; штовхає капелюхи; входить у капелюх кінцем уперед |
| Капелюх | object | колір пари (червоний, зелений, помаранчевий, фіолетовий; 5-й блакитний — лише в тестах); відкритий бік N/E/S/W | штовхається, ряд капелюхів їде разом; отвір — вхід порталу до пари |
| Білий капелюх-вихід | object | відкритий бік; без пари | штовхається як інші; паличка в ньому — перемога |
| Стіна | static | — | непрохідна для всього; удар — пил, хід скасовано |
| Крапки номера | static | 1–4 крапки | декор нижньої стіни: номер рівня |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cells_ahead)` → ТО `move(wand, dir)` — обидві половинки, орієнтація не змінюється.
- КОЛИ `input(dir)` → ЯКЩО `cell(cell_ahead, wall)` → ТО `block`, `sound(sfx2)` — хід скасовано повністю.
- КОЛИ `contact(wand, hat)` → ЯКЩО `custom: «паличка рухається поперек своєї осі»` → ТО `push(hat)` — байдуже, куди дивиться отвір; дві половинки можуть штовхнути два капелюхи разом.
- КОЛИ `contact(wand, hat)` → ЯКЩО `custom: «рух уздовж осі палички»` і `not facing(hat, toward_wand)` → ТО `push(hat)`.
- КОЛИ `custom: «капелюх, що рухається, впирається в капелюх»` → ТО `push(hat)` — ряд капелюхів зсувається цілим.
- КОЛИ `blocked(hat)` → ТО `block` — будь-що впирається в стіну, і скасовується весь хід, з паличкою.
- КОЛИ `contact(wand, hat)` → ЯКЩО `facing(hat, toward_wand)` і `custom: «рух уздовж осі палички»` → ТО `teleport(wand, pair_hat)`, `face(wand, pair_opening)`, `move(wand, pair_opening)` — трюк: пара — капелюх того самого кольору; передня половинка зʼявляється в парному капелюсі, задня входить у вхідний і теж переходить; паличка виходить з отвору пари й лягає вздовж його осі.
- Під час виходу паличка штовхає капелюхи (і ряди) на шляху так само, як звичайним ходом.
- КОЛИ `blocked(wand)` під час виходу → ТО `push(pair_hat, back)` — віддача: парний капелюх разом із рядом капелюхів позаду відʼїжджає проти свого отвору, а паличка лишається на звільненому місці.
- КОЛИ `blocked(pair_hat)` (віддачу теж заблоковано) → ТО `custom: «трюк іде назад: вхід і вихід міняються ролями, паличка виходить з отвору вхідного капелюха»`, `sound(sfx1)`.
- Капелюх, що рухається, везе свій колір і половинку палички всередині, крім руху проти отвору (тоді капелюх зʼїжджає з неї).
- КОЛИ `contact(wand, exit_hat)` → ЯКЩО `facing(exit_hat, toward_wand)` → ТО `animate(finale)`, `sound(sfx3)`, `win`, `next_level`.
- Перемога: паличка в білому капелюсі. · Поразки нема (глухий кут → undo або рестарт). · Рахунку нема.

## Керування і ввід
- Стрілки / WASD — зсув палички; Z — undo; R — рестарт (itch).
- Тач: тап у головному меню, свайп — рух, меню-вкладка вгорі ліворуч — undo / restart.
- Дії X нема: у коді лише закоментований налагоджувальний «fast forward».

## Вікна, меню, HUD
- `title-screen` (custom, стандарт PuzzleScript): назва «Hat tricks», автор, старт.
- `game-screen`: кімната; `level-number` крапками в стіні, іншого HUD нема; на мобільному — вкладка з `undo-button` і `restart-button`.
- Фінал рівня — спалах у білому капелюсі (4 кадри), далі наступна кімната.
- `message-screen` (custom): «Thank you for playing! :)» після 16-го рівня.
- Переходи: title → 16 кімнат підряд → фінальне повідомлення.

## Фічі поза полем
- `undo` ∞, `restart-level`, `levels-sequential`: 16 пазлів, «1h+» гри за itch.
- `touch-controls` (свайпи) поруч із клавіатурою.
- Відкритий код: Pattern:Script скоротив код (16 спрайтів капелюхів з 30 рядків замість 300+); у коді лишились закоментовані рівні-«юніт-тести» механіки й мітки режиму редагування, що задають, куди дивляться отвори.
- Нема підказок, вибору рівня, редактора.

## Варіації й родичі
- Інші ігри clickmazes у корпусі: `thinky/lock-and-pin.md`, `push-slide/boxup.md` (коробка з одним відкритим боком), `push-slide/wriggle.md`; `push-slide/punt-mazes.md` — чужа концепція, але сторінка й частина рівнів на clickmazes.
- Паличка-штовхач — `thinky/elephant-in-a-bottle.md`; орієнтація як стан — `thinky/stephens-sausage-roll.md`, `push-slide/bloxorz.md`; вхід у штовхуваний обʼєкт — `thinky/patricks-parabox.md`; портал на ящику — ScaleBox.
- Задумано для Thinky Puzzle Game Jam 2 (липень 2022); вийшло у вересні 2022 як «late non-entry».
- **Осі варіацій**: портал — нерухомий / на штовхуваному обʼєкті (тут); вихід — зберігає напрям / задає орієнтацію за отвором (тут); заблокований вихід — нічого / віддача порталу / розворот трюку (тут обидва, по черзі); вхід — з будь-якого боку / лише крізь отвір і лише кінцем уперед.

## Цікавинки для курсу
- Обʼєкт 2×1 з орієнтацією, що зсувається без повороту, з перевіркою обох клітин фронту — 📎.
- Штовхання рядом зі скасуванням усього ходу, якщо хоч щось упирається в стіну — 📎.
- Капелюх-портал: вхід лише в отвір і лише кінцем, вихід з отвору пари з новою орієнтацією — 🥉.
- Каскад «вперед → віддача порталу → розворот трюку» зі станом вход/вихід (`m1`/`m2`) — 🥈.
- Трюк як послідовність автоматичних тіків, поки ввід чекає — 📎.
- BFS-розвʼязувач: стан = позиція й орієнтація палички + до 9 капелюхів; віддача й розворот ускладнюють функцію переходу — 🥇.

## Мапа на каталог
- Є: `move-4dir` + `move-by-input` ↔ зсув; `multi-cell-size` ↔ паличка 2×1; `orientation-state` ↔ H/V; `push-object` ↔ капелюхи; `teleport` + `teleport-pair` ↔ пара капелюхів одного кольору; `impassable-cells` ↔ стіни; `reach-exit` ↔ білий капелюх; `undo-unlimited` + `restart-level`; `sequential-levels`; `keyboard-controls` + `swipe-gestures`; `sound-effects` + `event-effects` (пил, спалах).
- Уже пропоновані іншими: `+rigid-stick-pusher` (Elephant in a Bottle) ↔ паличка; `+portal-on-object` (ScaleBox) ↔ капелюх-портал, що штовхається; `+push-chain` ↔ ряд капелюхів; `+open-side-box` (Boxup) ↔ вхід лише з боку отвору; `+rule-discovery` ↔ мету й механіку треба відкрити.
- **Нема** → пропозиції карток:
  - `+portal-sets-orientation` «Вихід із порталу задає орієнтацію за його отвором» · entities/interact · 🥉.
  - `+portal-recoil` «Заблокований вихід відштовхує сам портал назад» · entities/interact · 📎.
  - `+portal-reverse-on-block` «Вихід і віддача заблоковані — повернення крізь вхідний портал» · entities/interact · 📎.
  - `+pushable-exit` «Вихід — рухомий обʼєкт» · game-logic/win · 🌱.

## Пропозиції до словників
- `+cond:axis` — рух уздовж / поперек осі довгого обʼєкта (уже пропонувала Elephant in a Bottle); тут вирішує «штовхнути чи увійти».
- `+ui:in-field-level-number` — номер рівня, намальований на самому полі (крапки в стіні).
- `+window:title-screen`, `+window:message-screen` — стандартні екрани PuzzleScript.
- `+card:portal-sets-orientation`, `+card:portal-recoil`, `+card:portal-reverse-on-block`, `+card:pushable-exit` — механік нема в каталозі.

## Джерела
- ⭐ [clickmazes: Hat-tricks](https://www.clickmazes.com/hattricks/hattricks.htm) — паличка з двома станами, капелюх з одним отвором як портал до пари, hat-trick кінцем уперед — єдина зміна орієнтації, «цікаві взаємодії», коли вихід частково заблоковано; історія й Pattern:Script.
- [itch: Hat-tricks](https://clickmazes.itch.io/hat-tricks) — грати; вересень 2022, 16 пазлів, клавіші й тач, коментарі (переплутані крапки рівнів 3–4).
- [Код у gist](https://gist.github.com/b81a790a66fda61d8192888ca2da072d) — повні правила: штовхання боком і кінцем, ряди, трюк, віддача, розворот, фінал, 16 рівнів і тестові рівні.
- [Редактор Pattern:Script](https://clementsparrow.github.io/Pattern-Script/src/editor.html?hack=b81a790a66fda61d8192888ca2da072d) — той самий код, запуск у редакторі.
- [Thinky Puzzle Game Jam 2](https://itch.io/jam/thinky-puzzle-game-jam-2) — джем, на який гру не встигли подати.
- YouTube: пошук «Hat-tricks clickmazes puzzlescript».

## Непевне
- (?) Чи паличка на виході з трюку може одразу ввійти в наступний капелюх, що стоїть до неї отвором (ланцюг трюків), — з коду не певно, у грі не перевірено.
- (?) Титул, Esc-меню й пункт continue — стандарт рушія PuzzleScript; Pattern:Script як форк, найпевніше, такий самий.
- (?) Чи віддача може зсунути капелюх-вихід на клітину, де стоїть інша половинка палички, — крайній випадок, не перевірено.
