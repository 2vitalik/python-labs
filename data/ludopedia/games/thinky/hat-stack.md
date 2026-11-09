---
title: Hat Stack
slug: hat-stack
aka: []
family: thinky
also: [program-robots]
klass: cursor
axes:
  field: 1d
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2022
platforms: [web]
links:
  - {kind: itch, url: "https://knexator.itch.io/hat-stack", best: true, note: "грати в браузері; в описі — правила всіх предметів у rot13 для тих, хто хоче пропустити відкриття"}
  - {kind: play, url: "https://html-classic.itch.zone/html/6126283/index.html", note: "сама збірка (один HTML): 13 рівнів і вся логіка паличок у відкритому JS"}
  - {kind: other, url: "https://itch.io/jam/thinky-puzzle-game-jam-2", note: "Thinky Puzzle Game Jam 2, для якого зроблено гру"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Hat+Stack+knexator", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [drag-drop-piece, interaction-table, cell-transform, completion-detection, sequential-levels, restart-level, movement-animation, event-effects, +stack-spells, +triplicate-next, +swap-next-two, +move-to-stack-end, +type-cycle-transform, +pop-order-goal, +prep-then-show-phases, +rule-discovery]
proposes: ["+effect:reorder", "+cond:top_of_stack", "+cond:stack_height", "+ui:goal-sequence", "+ui:stack-view", "+feature:rules-spoiler", "+axis:rules", "+card:stack-spells"]
author: opus
date: 2026-11-09
---

# Hat Stack — склади тварин у капелюх фокусника так, щоб помахи палички переписали стос у потрібний порядок виходу

## Суть
Гра knexator для Thinky Puzzle Game Jam 2: фокусник готує номер. Тварин і предмети зі сцени перетягують у капелюх — це **стек** (верхній — останній покладений). Помах палички «читає» верхній предмет: він зникає й діє на те, що під ним — потроює, міняє два місця, перетворює, переносить на дно чи з дна нагору. Потім «Go!»: предмети виходять з капелюха згори вниз і мають скласти задану послідовність. Правила предметів не пояснено — їх відкривають дослідом (у описі itch — підказки в rot13).

## Поле і час
- Поле — **одновимірний стек** у капелюсі; навколо — сцена 800×600 px із розкиданими тваринами (вільні координати, лише для drag-вводу) і рядок цілей угорі.
- Дві фази рівня: **підготовка** (кладемо, викидаємо, махаємо паличкою) → **шоу** (кожен клік виймає верхній предмет у наступний слот цілі).
- Хід = одна дія мишею; без вводу нічого не змінюється. Анімації (завіса, політ предмета) — косметика.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Капелюх | container | стек предметів | приймає перетягнутий предмет нагору; клік у підготовці — верхній зникає назавжди; клік у шоу — верхній іде в ціль |
| Паличка | switch | вимкнена на рівні 1 | клік — застосувати чари верхнього предмета; у шоу — те саме, що клік по капелюху |
| Кролик | object | потрібно ≥2 у стеку | зникає; наступний предмет утричі (додаються 2 копії зверху) |
| Голуб («chicken» в описі itch, `dove` у коді) | object | — | зникає; нижній предмет стеку переходить нагору |
| Слон | object | — | зникає; верхній (наступний) предмет іде на дно |
| Джокер | object | потрібно ≥3 | зникає; два наступні міняються місцями |
| Квітка | object | потрібно ≥2 | зникає; наступний перетворюється по колу квітка→джокер→дзеркало→слон→кролик→голуб→квітка |
| Дзеркало | object | потрібно ≥2 | зникає; наступний перетворюється на пару: голуб↔слон, квітка↔дзеркало, кролик↔джокер |
| Слот цілі | mark | тип, стан ✓/✗/порожній | i-й вийнятий предмет порівнюється з i-м слотом |
| Тварина на сцені | object | позиція x,y | до шоу — перетягується; на «Go!» невикористані йдуть за лаштунки |

## Правила (КОЛИ → ЯКЩО → ТО)
Підготовка:
- КОЛИ `input(drag, animal)` → ЯКЩО `custom: «відпущено в радіусі ~100 px від капелюха»` і `not state(level, show)` → ТО `place(hat, animal)` (нагору стеку).
- КОЛИ `input(click, hat)` → ЯКЩО `not state(level, show)` і `count(hat_item, >, 0)` → ТО `disappear(top)` — предмет не повертається на сцену.
- КОЛИ `input(click, wand)` → ЯКЩО `level(=, 1)` → ТО `block` (перший рівень — лише порядок).
- КОЛИ `input(click, wand)` → ЯКЩО `custom: «верхній — кролик»` і `count(hat_item, >=, 2)` → ТО `disappear(rabbit)`, `clone(next)`, `clone(next)`.
- КОЛИ `input(click, wand)` → ЯКЩО `custom: «верхній — голуб»` → ТО `disappear(dove)`, `custom: «нижній предмет — нагору»` (`+effect:reorder`); на порожньому під ним — просто зникає.
- КОЛИ `input(click, wand)` → ЯКЩО `custom: «верхній — слон»` → ТО `disappear(elephant)`, `custom: «наступний — на дно»` (`+effect:reorder`).
- КОЛИ `input(click, wand)` → ЯКЩО `custom: «верхній — джокер»` і `count(hat_item, >=, 3)` → ТО `disappear(joker)`, `swap(next1, next2)`.
- КОЛИ `input(click, wand)` → ЯКЩО `custom: «верхній — квітка»` і `count(hat_item, >=, 2)` → ТО `disappear(flower)`, `transform(next, cycle[next])`.
- КОЛИ `input(click, wand)` → ЯКЩО `custom: «верхній — дзеркало»` і `count(hat_item, >=, 2)` → ТО `disappear(mirror)`, `transform(next, pair[next])`.
- КОЛИ `input(click, wand)` → ЯКЩО `custom: «капелюх порожній або під верхнім замало предметів»` → ТО `block`, `custom: «паличка сіпається — чари не спрацювали»`.

Шоу:
- КОЛИ `input(click, go)` → ТО `set_state(level, show)`, `custom: «завіса відкривається, невикористані тварини йдуть зі сцени»`.
- КОЛИ `input(click, hat|wand)` → ЯКЩО `state(level, show)` і `same(top, goal_slot_i, type)` → ТО `custom: «верхній летить у слот i»`, `mark(goal_slot_i, ✓)`, `counter(i, +1)`.
- КОЛИ `input(click, hat|wand)` → ЯКЩО `state(level, show)` і `not same(top, goal_slot_i, type)` → ТО `mark(goal_slot_i, ✗)`, `set_state(level, failed)`, `counter(i, +1)`.
- КОЛИ `counter(hat_item, =, 0)` → ЯКЩО `state(level, show)` і `counter(i, =, goal_len)` і `not state(level, failed)` → ТО `win`, `custom: «оплески»`.
- КОЛИ `input(click, reset)` → ТО `restart`. КОЛИ `input(click, prev|next)` → ТО `custom: «сусідній рівень, без замків»`.
- Перемога: послідовність виходу з капелюха **точно** дорівнює рядку цілей (жодного зайвого предмета). · Поразка: окремої нема — ✗ у слоті або залишок, далі лише рестарт. · Рахунку нема.

## Керування і ввід
- Лише миша: drag тварини на капелюх; клік по капелюху (викинути верхній / у шоу — вийняти); клік по паличці (чари / у шоу — вийняти); кнопка «Go!».
- Кнопки внизу: «prev» · «Reset the N-th show» · «next». Undo нема — лише рестарт рівня.

## Вікна, меню, HUD
- `game-screen` (єдиний екран, без головного меню): сцена з завісою й публікою, капелюх, паличка з зірочкою-ефектом, тварини, рядок цілей угорі.
- HUD: `+ui:goal-sequence` — рядок сірих іконок цілей, що фарбуються й отримують ✓/✗ при виході предмета; `level-number` — у тексті кнопки «Reset the 3rd show».
- Переходи: підготовка → «Go!» (завіса відкривається) → шоу → оплески (перемога) → «next» вручну.
- Сторінка itch — фактично `help-window`: опис + правила предметів у rot13.

## Фічі поза полем
- `levels-sequential` — 13 рівнів; prev/next без замків, збереження прогресу нема.
- `restart-level` (кнопка Reset); undo нема.
- `+feature:rules-spoiler` — правила в rot13 на сторінці гри: хто хоче, пропускає відкриття й іде одразу до складних пазлів.
- За коментарями в коді рівні 10–13 — «autogen»: згенеровані пошуком, а не намальовані вручну.

## Варіації й родичі
- [Magiciban](magiciban.md) — той самий образ фокусника з кроликами й капелюхами, але просторовий (зсуви сцени).
- [Stack Machines](../program-robots/stack-machines.md) — стек як основа програми; у Hat Stack «програма» записана в самих даних: кожен елемент стеку — команда для наступного.
- Інші роботи knexator у корпусі (обидві просторові): варіант [4D Sokoban](4d-sokoban.md) і рівень «Bubble Pond» у [The Snake That Eats…](the-snake-that-eats-puzzle-game-mechanics.md).
- **Осі варіацій:** звідки беруться команди (окремий список / самі елементи стеку) · область дії (наступний / два наступні / дно) · вид зміни (копія / обмін / перенесення / перетворення за таблицею) · ціль (точна послідовність / множина / лише верхній).

## Цікавинки для курсу
- Стек + шість операцій-чарів як інтерпретатор із перевіркою «вистачає предметів» — 🌱.
- Таблиці перетворень (цикл квітки і пари дзеркала) як словники — 🌱.
- Дві фази рівня (підготовка → шоу) з порівнянням послідовності й ✓/✗ — 📎.
- Розвʼязувач BFS по станах стеку (кролик роздуває стан — потрібна межа довжини) — 🥉.
- Генератор рівнів «від цілі назад» або перебором, як «autogen»-рівні автора — 🥈.

## Мапа на каталог
- Є: `drag-drop-piece` ↔ тварина в капелюх; `interaction-table` ↔ шість предметів × дія на наступний; `cell-transform` ↔ квітка/дзеркало міняють тип предмета (не клітини — найближча картка); `completion-detection` ↔ звірка послідовності; `sequential-levels`, `restart-level`; `movement-animation`, `event-effects` ↔ політ у слот, завіса, оплески.
- **Нема** → пропозиції карток:
  - `+stack-spells` «Елемент стеку діє на наступні» · game-logic/program · 🥉 · слоти {ops: triple|swap|to_bottom|to_top|cycle|pair}.
  - `+triplicate-next` · `+swap-next-two` · `+move-to-stack-end` · `+type-cycle-transform` — окремі операції, 🌱 кожна.
  - `+pop-order-goal` «Порядок виходу = ціль» · game-logic/win · 🌱.
  - `+prep-then-show-phases` «Підготовка, потім виконання без втручання» · game-logic · 📎.
  - `+rule-discovery` (уже пропонувалась) — правила предметів не пояснені.

## Пропозиції до словників
- `+effect:reorder` — перенести елемент на інший кінець стеку/черги (голуб: дно → верх; слон: верх → дно); повтор з інших файлів.
- `+cond:top_of_stack(a)` — A — верхній у стеку (повтор).
- `+cond:stack_height(op, n)` — у стеку ≥N предметів (кролик ≥2, джокер ≥3).
- `+ui:goal-sequence` — рядок цільових іконок, що заповнюється ✓/✗ у порядку виходу.
- `+ui:stack-view` — видно вміст стеку (тут лише верхній виглядає з капелюха) (повтор).
- `+feature:rules-spoiler` — пояснення прихованих правил, закодоване (rot13), щоб пропустити фазу відкриття.
- `+axis:rules` — значення `discovered` (повтор).
- `+card:stack-spells` — див. «Мапа на каталог».

## Джерела
- ⭐ [itch: Hat Stack](https://knexator.itch.io/hat-stack) — опис («Discover the rules behind the strange spells»), rot13-пояснення шести предметів, теги jam / non-spatial / thinky, коментар про рівень 7.
- [Збірка гри (itch.zone)](https://html-classic.itch.zone/html/6126283/index.html) — відкритий JS: `doWandLogic` (умови ≥2/≥3, `flowerMapping`, `mirrorMapping`), `popDuringShow` (звірка зі слотом, ✓/✗, оплески), `loadLevel` (13 рівнів, коментарі «autogen»), радіус drop ~100 px, вимкнена паличка на рівні 1.
- [Thinky Puzzle Game Jam 2](https://itch.io/jam/thinky-puzzle-game-jam-2) — джем (посилання зі сторінки гри; файли збірки — липень 2022).
- YouTube: пошук «Hat Stack knexator».

## Непевне
- (?) Курка чи голуб: опис itch каже «chicken», у коді й картинках — `dove`; дію (дно → верх) підтверджено кодом.
- (?) Сторінка itch має статус «In development» — чи буде повніша версія, невідомо.
- (?) Рік 2022 — за датами файлів сторінки (07.2022) і номером джему; точну дату публікації не бачив.
