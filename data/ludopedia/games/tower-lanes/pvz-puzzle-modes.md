---
title: "Plants vs. Zombies: Vasebreaker і I, Zombie (режим Puzzle)"
slug: pvz-puzzle-modes
aka: [Vasebreaker, "I, Zombie", PvZ Puzzle Mode, Розбивач ваз, "Я, зомбі"]
family: tower-lanes
also: [hidden-deduction]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: hidden
  random: setup
  goal: state
year: 2009
platforms: [PC, Mac, iOS, Android, Xbox 360, PS3, DS]
links:
  - {kind: fandom, url: "https://plantsvszombies.wiki.gg/wiki/Vasebreaker", best: true, note: "Vasebreaker: типи ваз, Plantern, 10 рівнів, Endless і серії"}
  - {kind: fandom, url: "https://plantsvszombies.wiki.gg/wiki/Vasebreaker_(level)", note: "перший рівень: вміст ваз, пакети насінин зникають, без косарок"}
  - {kind: fandom, url: "https://plantsvszombies.wiki.gg/wiki/Vasebreaker_Endless", note: "35 ваз, склад рослин/зомбі, сонце у вазі, ріст складності за серією"}
  - {kind: fandom, url: "https://plantsvszombies.wiki.gg/wiki/I,_Zombie", note: "I, Zombie: ціни зомбі, 200 сонця за соняшник, умови перемоги/поразки"}
  - {kind: fandom, url: "https://plantsvszombies.wiki.gg/wiki/I,_Zombie_(level)", note: "перший рівень: набір рослин, макс. 1400 сонця"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Plants_vs._Zombies_(video_game)", note: "загальний контекст гри"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=plants+vs+zombies+vasebreaker+i+zombie+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [enemy-reached-base, hp-damage, projectile-shot, shoot-forward, shoot-cooldown, timed-despawn, interaction-table, speed-per-type, melee-vs-ranged, explode-area, destroy-all-enemies, round-currency, cell-click, puzzle-select, level-unlock, streak-stats, achievements-window, progress-acceleration, logic-render-split, +lane-grid, +hidden-container, +reverse-td, +placement-line, +endless-streak]
proposes: ["+trigger:lane_enter", "+cond:lane_has", "+effect:break_open", "+effect:lane_clear", "+role:lane", "+ui:streak-counter", "+ui:seed-bar", "+feature:endless-streak", "+card:hidden-container", "+card:reverse-td", "+card:placement-line"]
author: opus
date: 2026-11-09
---

# PvZ Puzzle: Vasebreaker і I, Zombie — два пазли на двіжку смугового TD: розбий вази з невідомим вмістом / атакуй зомбі готову оборону

## Суть
Режим Puzzle з Plants vs. Zombies ([plants-vs-zombies](plants-vs-zombies.md)) — два набори пазлів на тому самому газоні 5 рядів × 9 колонок. **Vasebreaker**: праву частину газону заставлено вазами, у кожній — рослина або зомбі; гравець молотком розбиває вази в обраному порядку, сам задаючи темп, і має встигнути посадити знайдені рослини, перш ніж випущені зомбі дійдуть до будинку. **I, Zombie**: ролі навпаки — рослини вже розставлені («картонні»), гравець купує зомбі за сонце й ставить їх праворуч від лінії, щоб зʼїсти мозок у кінці кожного ряду. Обидва — «пазли поверх TD»: менше реакції, більше порядку дій і бюджету.

## Поле і час
- Газон як у PvZ: 5 рядів-смуг × 9 колонок, будинок ліворуч; обидва режими — нічні (Night) (рівень 4-5 Adventure — теж Vasebreaker на Night).
- Vasebreaker: вази займають праві колонки газону (скільки колонок — див. «Непевне»); ліві колонки вільні під посадку. У першому рівні й Endless газонокосарок нема.
- I, Zombie: рослини стоять на лівій частині; лінія, правіше від якої можна ставити зомбі, — приблизно посередині газону; за рослинами в кінці кожного ряду — мозок.
- Real-time як в оригіналі: зомбі йдуть своєю швидкістю, рослини стріляють своїм періодом. Темп Vasebreaker задає сам гравець — нічого не відбувається, доки не розбив вазу (крім уже випущених зомбі).
- Інформація: Vasebreaker — вміст ваз прихований (крім зелених «листяних»), Plantern показує вміст у 3×3; I, Zombie — повна інформація.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Ваза звичайна | container | вміст: рослина / зомбі / сонце (Endless) | клік молотком → розбивається, вміст зʼявляється в цій клітині |
| Ваза зелена (з листям) | container | завжди рослина | видно, що всередині рослина; розбивати першою |
| Молоток (курсор) | — | — | клік по вазі = розбити |
| Пакет насінини з вази | pickup | lifetime | зʼявляється на панелі; посадити безкоштовно до зникнення, інакше втрачено |
| Сонце у вазі (Endless) | resource | 25–75 | лише з ваз; можна тримати на Cherry Bomb |
| Plantern | ally | — | освітлює 3×3: показує вміст ваз навколо |
| Peashooter · Snow Pea · Repeater (назад) · Threepeater | ally | з вази | стріляють як у PvZ; у Endless Repeater-и розвернуті назад |
| Squash · Potato Mine · Wall-nut · Cherry Bomb | ally | з вази | миттєві / блокер; Squash розчавлює зомбі, що виходить з вази поруч |
| Зомбі з вази (Zombie, Buckethead, Jack-in-the-Box, Gargantuar+Imp) | enemy | як у PvZ | зʼявляється в клітині вази, іде вліво своїм рядом, їсть рослини |
| Будинок | static | — | зомбі дійшов → `lose` |
| Картонні рослини (I, Zombie) | enemy | розстановка рівня | стріляють/бʼють зомбі гравця як у PvZ |
| Соняшник (I, Zombie) | resource | 200 сонця | зʼїдений звичайним зомбі (або вкрадений Bungee) → +200 сонця |
| Мозок (I, Zombie) | static | 1 на ряд | зомбі дійшов до нього → мозок зʼїдено |
| Зомбі гравця (I, Zombie) | ally | ціна в сонці | ставиться за лінією, далі сам іде вліво; забрати назад не можна |
| Лінія розміщення | zone | ~середина газону | правіше — можна ставити зомбі |

Ціни зомбі в I, Zombie (wiki.gg): Zombie 50 · Imp 50 · Conehead 75 · Pole Vaulting 75 · Screen Door 100 · Buckethead 125 · Digger 125 · Bungee 125 · Balloon 150 · Ladder 150 · Football 175 · Gargantuar 300 · Dancing 350.

## Правила (КОЛИ → ЯКЩО → ТО)
Vasebreaker:
- КОЛИ `input(click, vase)` → ТО `custom: «break_open: ваза зникає, вміст зʼявляється в її клітині»`, `reveal(vase)`.
- КОЛИ `destroyed(vase)` → ЯКЩО `occupied(vase, plant)` → ТО `give(player, seed_packet)`; пакет зникає за часом (`timed-despawn`).
- КОЛИ `destroyed(vase)` → ЯКЩО `occupied(vase, zombie)` → ТО `spawn_at(zombie, vase_cell)`, зомбі `move(a, left)` своїм рядом.
- КОЛИ `destroyed(vase)` → ЯКЩО `occupied(vase, sun)` → ТО `currency(+n)` (Endless, 25–75).
- КОЛИ `input(place, seed_packet, cell)` → ЯКЩО `free(cell)` → ТО `place(plant)`, `take(player, seed_packet)` (без сонця).
- КОЛИ `timer(seed_packet.lifetime)` → ЯКЩО `custom: «пакет не використано»` → ТО `disappear_a`.
- КОЛИ `in_range(plantern, vase, 1)` → ТО `reveal(vase)` (3×3 навколо Plantern).
- КОЛИ `timer(plant.fire_rate)` → ЯКЩО `custom: «lane_has(zombie, ahead)»` → ТО `spawn(projectile)` — як у PvZ.
- КОЛИ `adjacent(zombie, plant)` → ТО `custom: «зупиняється і їсть: damage щотік»`; КОЛИ `hp_zero(plant)` → ТО `disappear_b`.
- КОЛИ `reach(zombie, house_col)` → ЯКЩО `not has(lane, mower)` → ТО `lose` (у Endless — кінець серії).
- КОЛИ `all_gone(vase)` and `all_gone(zombie)` → ТО `win` (Endless — `counter(streak, +1)` і новий газон з вазами).
- Endless: КОЛИ `counter(streak, %, 10)` → ТО `spawn(reward)` (подарунок / шоколад / мішок золота / діамант); `custom: «кожні 10 серій одного звичайного зомбі в наборі замінює Gargantuar, до 9»`.

I, Zombie:
- КОЛИ `input(place, zombie_type, cell)` → ЯКЩО `has(sun, cost)` and `custom: «клітина правіше лінії розміщення»` → ТО `place(zombie)`, `currency(-cost)`.
- КОЛИ `custom: «зомбі гравця вже на газоні»` → ТО `custom: «забрати назад не можна; іде вліво сам»`.
- КОЛИ `hp_zero(sunflower)` → ЯКЩО `custom: «зʼїв зомбі гравця»` → ТО `currency(+200)`; Bungee: КОЛИ `contact(bungee, sunflower)` → ТО `take(field, sunflower)`, `currency(+200)`.
- КОЛИ `contact(player_zombie, brain)` → ТО `disappear_b`, `counter(brains, -1)`.
- КОЛИ `counter(brains, =, 0)` → ТО `win` (Endless — `counter(streak, +1)` і нова розстановка).
- КОЛИ `no_moves(player)` → ЯКЩО `count(player_zombie, =, 0)` and `not has(sun, 50)` → ТО `lose`.
- Endless: КОЛИ `counter(streak, %, 3)` → ТО `spawn(reward)` (рослина Zen Garden / шоколад / мішок золота / діамант).
- Взаємодії «зомбі × рослина» — як у PvZ (Pole Vault перестрибує, Digger обходить знизу, Ladder ставить драбину на блокер, Balloon летить над прямими стрілками, Squash чекає на першого).

- Перемога: Vasebreaker — усі вази розбито й усіх зомбі знищено (?) · I, Zombie — зʼїдено мозок у кожному ряду.
- Поразка: Vasebreaker — зомбі в будинку · I, Zombie — зомбі на газоні нема, а сонця < 50.
- Рахунок: нема очок; у Endless — довжина серії («You made it to a streak of N»); у I, Zombie — залишок сонця (досягнення за 1000 на першому рівні).

## Керування і ввід
- Лише миша/тач: Vasebreaker — клік молотком по вазі; клік по пакету на панелі → клік по клітині = посадити.
- I, Zombie — клік по картці зомбі з ціною → клік по клітині правіше лінії.
- Ключове рішення Vasebreaker — **порядок розбивання** (рекомендовано праворуч наліво, зелені вази — першими, щоб мати рослини до появи зомбі); I, Zombie — **розподіл бюджету по рядах** (який тип куди).

## Вікна, меню, HUD
- `main-menu` → Puzzle → `puzzle-select` з двома вкладками/наборами: Vasebreaker (9 рівнів + Endless) і I, Zombie (9 + Endless); трофей на пройденому рівні.
- `game-screen` Vasebreaker: газон з вазами, панель пакетів насінин (`+ui:seed-bar`) із затемненням-зникненням, лічильник сонця (Endless), `+ui:streak-counter`, кнопка Menu.
- `game-screen` I, Zombie: газон з картонними рослинами й мозками, панель зомбі з цінами, лічильник сонця, лінія розміщення на полі.
- `pause-menu`, `end-screen` (трофей / мішок грошей при повторі; у Endless — «You made it to a streak of N»).
- `shop-window` (iOS): решту рівнів купують у Crazy Dave за 150 000 монет — перший безкоштовний.
- `achievements-window` (GOTY): Smashing! (9 трофеїв Vasebreaker), China Shop (серія 15), I, Win (9 трофеїв I, Zombie), Where the Sun Don't Shine, Think Hard.

## Фічі поза полем
- Рівні Vasebreaker: Vasebreaker · To the Left · Third Vase · Chain Reaction · M is for Metal · Scary Potter · Hokey Pokey · Another Chain Reaction · Ace of Vase · Vasebreaker Endless (китайські видання — ще 6).
- Рівні I, Zombie: I, Zombie · I, Zombie Too · Can You Dig It? · Totally Nuts · Dead Zeppelin · Me Smash! · ZomBoogie · Three Hit Wonder · All your brainz r belong to us · I, Zombie Endless.
- `mode-endless` з серією (`+feature:endless-streak`): складність росте з кожною серією, нагорода кожні 10 (Vasebreaker) / 3 (I, Zombie) серій.
- `level-unlock`, `achievements`, нагороди: трофей за перше проходження, мішок монет за повтор.

## Варіації й родичі
- Основна гра — [plants-vs-zombies](plants-vs-zombies.md); тим самим двіжком зроблені міні-ігри (Wall-nut Bowling, Beghouled тощо).
- Реверс-TD: [anomaly-warzone-earth](anomaly-warzone-earth.md) (маршрут конвою), [mechabellum](mechabellum.md) (армія проти армії), PvZ 2 «Zombies vs. Zombies» (?).
- Приховане поле: Minesweeper/Dragonsweeper (сімʼя hidden-deduction) — але тут «міни» не вбивають, а випускають ворога, якого ще можна зупинити.
- **Осі варіацій**: роль гравця — оборона / напад · подача юнітів — купівля / вміст контейнера / конвеєр · інформація — повна / приховані контейнери / часткове освітлення · темп — хвилі за розкладом / темп гравця (розбивання).

## Цікавинки для курсу
- Vasebreaker як «сапер на смугах»: відкриття клітини випускає або ресурс, або загрозу; темп задає гравець — 🥉 (сутність-контейнер + спавн з її клітини).
- Пакет насінини з таймером зникнення — 🌱.
- Plantern: розкриття вмісту в радіусі — 📎.
- I, Zombie — інверсія ролей на тому самому двіжку: зомбі стають юнітами гравця, рослини — ворогами без економіки — 🥈 (перевірка `logic-render-split` і даних-сторін).
- Поразка «нема юнітів і нема грошей» — 🌱; соняшник як «гаманець» ворога (+200 за зʼїдений) — 📎.
- Endless-серія з ростом складності (Gargantuar замість звичайного кожні 10) — 📎.

## Мапа на каталог
- Є: `enemy-reached-base` ↔ зомбі в будинку · `hp-damage` · `projectile-shot` + `shoot-forward` + `shoot-cooldown` · `timed-despawn` ↔ пакети насінин · `interaction-table` ↔ «зомбі × рослина» · `speed-per-type` · `melee-vs-ranged` · `explode-area` (Jack-in-the-Box, Cherry Bomb) · `destroy-all-enemies` (Vasebreaker) · `round-currency` (I, Zombie: сонце) · `cell-click` · `puzzle-select` · `level-unlock` · `streak-stats` · `achievements-window` · `progress-acceleration` (Endless) · `logic-render-split` (інверсія ролей).
- **Нема** → пропозиції карток:
  - `+lane-grid` — див. plants-vs-zombies.
  - `+hidden-container` «Контейнер з прихованим вмістом» · entities/spawn · 🥉 · слот {contents: [plant, zombie, sun], hint: green} — відкриття клітини дає ресурс або ворога.
  - `+reverse-td` «Реверс-TD: атака проти готової оборони» · game-logic/opponent · 🥈 — гравець купує атакувальників, AI — статична оборона.
  - `+placement-line` «Лінія розміщення юнітів» · entities/legality · 🌱 · слот {col} — ставити можна лише за лінією.
  - `+endless-streak` «Нескінченна серія з ростом складності» · game-logic/waves · 📎 · слот {reward_every: n}.

## Пропозиції до словників
- `+trigger:lane_enter` · `+cond:lane_has` · `+effect:lane_clear` · `+role:lane` · `+ui:seed-bar` — повтор із plants-vs-zombies (для правила трьох).
- `+effect:break_open` — розбити контейнер: він зникає, вміст зʼявляється в його клітині (ваза, скриня, яйце); відмінність від `disappear_b` + `spawn_at` — одна атомарна дія.
- `+ui:streak-counter` — лічильник поточної серії в нескінченному режимі.
- `+feature:endless-streak` — нескінченний режим, де одиниця прогресу — пройдена серія, з нагородою кожні N.
- `+card:hidden-container`, `+card:reverse-td`, `+card:placement-line` — див. «Мапа на каталог».

## Джерела
- ⭐ [PvZ wiki.gg: Vasebreaker](https://plantsvszombies.wiki.gg/wiki/Vasebreaker) — звичайні й зелені вази, молоток, Plantern 3×3, порада «праворуч наліво», 10 рівнів, Endless-нагороди кожні 10 серій, досягнення.
- [PvZ wiki.gg: Vasebreaker (level)](https://plantsvszombies.wiki.gg/wiki/Vasebreaker_(level)) — вміст ваз першого рівня (5 Peashooter, 5 Snow Pea, 5 Squash; 6 Zombie, 3 Buckethead, 1 Jack-in-the-Box), пакети зникають, косарок нема.
- [PvZ wiki.gg: Vasebreaker Endless](https://plantsvszombies.wiki.gg/wiki/Vasebreaker_Endless) — 35 ваз, 2 зелені, склад рослин і зомбі, 25–75 сонця у вазі, Gargantuar кожні 10 серій до 9, кінець — зомбі в будинку.
- [PvZ wiki.gg: I, Zombie](https://plantsvszombies.wiki.gg/wiki/I,_Zombie) — лінія розміщення ~посередині, ціни 13 зомбі, 200 сонця за соняшник, перемога/поразка, Endless-подарунок кожні 3 серії.
- [PvZ wiki.gg: I, Zombie (level)](https://plantsvszombies.wiki.gg/wiki/I,_Zombie_(level)) — розстановка першого рівня, доступні зомбі, макс. 1400 сонця.
- [Wikipedia: Plants vs. Zombies](https://en.wikipedia.org/wiki/Plants_vs._Zombies_(video_game)) — загальний контекст режиму Puzzle.
- YouTube: пошук «plants vs zombies vasebreaker i zombie gameplay».

## Непевне
- (?) Скільки колонок займають вази у Vasebreaker і чи стоять вони суцільно; у якій колонці лінія розміщення I, Zombie (wiki.gg: «приблизно посередині»).
- (?) Формальна умова перемоги Vasebreaker («усі вази розбито і всі зомбі мертві») — сторінки її не формулюють, лише натякають.
- (?) Стартове сонце в I, Zombie; чи є сонце у звичайних рівнях Vasebreaker (Endless — лише з ваз).
- (?) Чи розставлення рослин в I, Zombie фіксоване для рівня, чи з випадковими варіантами (перший рівень: «іноді ряд без стрілків, натомість 4 соняшники» — отже, є випадковість).
- (?) Чи бувають косарки в окремих рівнях Vasebreaker (перший і Endless — без них).
- (?) Розбіжність wiki.gg: «35 ваз, 19 рослин, 15 зомбі» не сходиться (34); можливо, одна ваза — сонце.
