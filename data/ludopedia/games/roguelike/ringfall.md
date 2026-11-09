---
title: Ringfall
slug: ringfall
aka: []
family: roguelike
also: []
klass: avatar
axes:
  field: graph
  time: turn
  opponent: ai
  info: full
  random: setup
  goal: score
year: 2026
platforms: [web (HTML5), touch]
links:
  - {kind: itch, url: "https://helmworkshop.itch.io/ringfall", best: true, note: "грати в браузері: правила кілець, обвал, боса, керування, онлайн-рахунки"}
  - {kind: other, url: "https://helmworkshop.itch.io/ringfall/devlog/1748626/020-released", note: "devlog 0.2.0: класи Warrior/Mage, ранги, сімʼї монстрів (дракони, нежить, гай), предмети, інтерфейс"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Ringfall+helm+workshop+roguelike", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-by-input, impassable-cells, telegraph-marker, telegraphed-intents, drop-on-death, sequential-levels, restart-level, leaderboard, game-pause, keyboard-controls, message-log, +ring-board, +shrinking-arena, +boss-fight, +boss-absorb-growth, +bump-attack, +wait-turn, +fire-breath, +revive-remains, +snare-roots, +class-skill-timer, +rank-up-skill]
proposes: ["+effect:absorb(boss, a)", "+ui:ringfall-gauge", "+ui:inspect-panel", "+ui:glint-marker", "+axis:field=ring", "+card:boss-absorb-growth"]
author: opus
date: 2026-11-09
---

# Ringfall — броуглайк на арені з концентричних кілець: зовнішнє кільце обвалюється, а вороги на ньому годують боса в центрі

## Суть
Коротка «кавова» покрокова гра: герой стартує на зовнішньому кільці, бос чекає в центрі. Кожні кілька ходів **найзовнішнє кільце обвалюється**, і вороги, що на ньому лишились, **поглинаються босом — він сильнішає**. Тож гравець пробивається всередину, вирішуючи, кого встигнути вбити, а кого лишити босові; вбив боса — спуск на наступну глибину. Чим глибше, тим швидше росте бос, тож лишені вороги коштують дедалі дорожче.

## Поле і час
- Полярна сітка: концентричні кільця, поділені на клітини; сусідство — вздовж кільця (вліво/вправо) і по «спиці» (всередину/назовні). Кількість кілець і клітин (?).
- На кільцях бувають стіни (вогняна смуга дракона крізь них проходить).
- Покроково: хід героя → хід ворогів; обвал зовнішнього кільця за таймером у ходах («ringfall gauge»).
- Дошка генерується; `R` переграє **ту саму** дошку з глибини 1, `Shift+R` — нову; онлайн-рахунки окремо для кожної дошки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | клас, ранг, щит (Warrior) | крок на сусідню клітину; вхід у ворога = удар |
| Warrior: Ward | player | лічильник | періодично дає щит; лічильник стоїть, поки щит є; під Ward удар лише «щербить» ворога, а щит бере наступний удар |
| Mage: Nova | player | лічильник | періодично вибух по всіх сусідніх клітинах; сильніший, що більше ворогів поруч |
| Бос (Lich, Warlord, Ent, Wyrm) | boss | сила | у центрі; поглинає ворогів з обваленого кільця й сильнішає |
| Дракони (зокрема Fire Drake, Wyrm) | enemy | — | позначають вогняну смугу, що спалахує наступного ходу; стіни не захищають |
| Нежить | enemy | — | гинучи, лишає купку решток, що підводиться знову |
| Купка решток | object | — | стати на неї — розвіяти, поки не встала |
| Гай (Grove) | enemy | — | накидає пута: герой не може ступити |
| Капітан сімʼї | enemy | — | посилений представник сімʼї (детально не описано) |
| Ворог-носій (блищить) | enemy | дроп: зілля / щит / пісочний годинник | убити — забрати дроп; поглинув бос — дроп втрачено |
| Вогняна смуга | hazard | лінія | позначена за хід до спалаху; зникає, якщо вбити дракона |
| Стіна | static | — | перешкода руху |
| Кільце | zone | номер | зовнішнє обвалюється за таймером |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(up)` → ЯКЩО `free(cell_inward)` → ТО `move(hero, inward)`; `input(down)` → назовні; `input(left|right)` → вздовж кільця.
- КОЛИ `input(dir)` → ЯКЩО `occupied(cell, enemy)` → ТО `custom: «удар (bump)»` — ворог гине (?), під Ward — `damage(enemy, chip)`.
- КОЛИ `input(wait)` (Space або тап по собі) → ТО `pass_turn`.
- КОЛИ `timer(ringfall)` → ТО `set_cell(outer_ring, void)`; для кожного ворога на ньому — `custom: «бос поглинає»`, `counter(boss_power, +n)`; дроп носія `disappear`.
- КОЛИ `died(boss)` → ТО `next_level` (глибина +1); ЯКЩО `level(op, n)` глибше → ТО `custom: «бос росте від поглинання швидше»`.
- КОЛИ `died(carrier)` → ТО `spawn_at(drop, cell)`; `picked(hero, drop)` → ефект зілля / щита / годинника (?).
- КОЛИ `custom: «дракон цілиться»` → ТО `mark(lane, fire)`; КОЛИ `turn_end` наступного ходу → ТО `damage(all in lane)`; ЯКЩО `died(dragon)` раніше → ТО `unmark(lane)`.
- КОЛИ `died(fire_drake)` → ТО `custom: «вогонь заповнює все його кільце»`; Wyrm — `custom: «дихає вздовж твоєї спиці»`.
- КОЛИ `died(undead)` → ТО `spawn_at(remains, cell)`; КОЛИ `timer(rise)` → ТО `transform(remains, undead)`; КОЛИ `enter(hero, remains)` → ТО `disappear(remains)`.
- КОЛИ `custom: «пута гаю»` → ТО `set_state(hero, snared, roots)`; ЯКЩО `state(hero, snared)` → ТО `block` для кроку; КОЛИ `input(any)` (удар або очікування теж) → ТО `custom: «один корінь рветься»`; щит пута не блокує.
- КОЛИ `timer(ward)` → ЯКЩО `not has(hero, shield)` → ТО `give(hero, shield)`; КОЛИ `contact(enemy_attack, hero)` → ЯКЩО `has(hero, shield)` → ТО `take(hero, shield)` замість шкоди.
- КОЛИ `timer(nova)` → ТО `damage(adjacent cells, n)`, `custom: «n росте з кількістю ворогів поруч»`; пасив — `custom: «спис за кожен каст»`.
- КОЛИ `custom: «ранг +1»` → ТО перший ранг — `give(hero, class_skill)`; далі — пасиви; останній — фінальна форма навички.
- КОЛИ `input(R)` → ТО `restart` (та сама дошка, глибина 1); `input(Shift+R)` → нова дошка.
- КОЛИ `custom: «забіг завершено»` → ТО `window(leaderboard)` за `L`; `M` — меню.
- Перемога: нема — «How deep can you go?». Поразка: смерть героя (?). Рахунок: глибина/результат на онлайн-таблиці дошки (?).

## Керування і ввід
- Стрілки або WASD: вгору — всередину, вниз — назовні, вліво/вправо — по кільцю; рух у ворога — атака.
- Space — чекати (на тачі — тап по герою); `X` — оглянути героя й ворогів глибини; `Tab` — перебір вмісту дошки.
- `Esc` / `P` — пауза; `R` — та сама дошка з початку; `Shift+R` — нова дошка; після забігу `L` — рахунки, `M` — меню.

## Вікна, меню, HUD
- `game-screen` у «термінальному» стилі: дошка-кільця, панелі PLAYER · ENEMIES · INSPECT, `message-log`, `ringfall-gauge` під дошкою, `glint-marker` на носіях дропу, `telegraph-marker` вогняних смуг; на малих екранах — компактний макет із вкладками.
- `pause-menu` (Esc/P), `main-menu` (M), `leaderboard` (L) — онлайн-рахунки цієї дошки.
- `character-select` — Warrior / Mage; анонсовані Acolyte і Apprentice (?).

## Фічі поза полем
- `leaderboard-online` для кожної дошки; бета-примітка: оновлення можуть скидати таблиці.
- `restart-level` тієї самої дошки й «нова дошка» — фактично відкритий seed без показу.
- `touch-controls` (тап), `mouse-and-keyboard`; сесія — кілька хвилин.
- Прогресія: класи з гілками; нові персонажі в розробці.

## Варіації й родичі
- Броуглайки корпусу: [magpie-broughlike](magpie-broughlike.md), [mosaic-broughlike](mosaic-broughlike.md), [868-hack](868-hack.md) — малі поля, удар рухом, телеграфовані загрози.
- [hyperrogue](hyperrogue.md) — теж нестандартна геометрія поля.
- Звуження арени — як у Bomberman (`+shrinking-arena` у корпусі); тут звуження ще й **годує боса**.
- Осі варіацій: **арена** (квадрат / кільця / гекс) · **що робить звуження** (просто вбиває / переносить ворогів до боса) · **клас** (захисний таймер / таймер-вибух).

## Цікавинки для курсу
- Полярна сітка кілець і спиць: сусідство, рух «всередину/назовні/по колу» — 📎.
- Обвал зовнішнього кільця за таймером із поглинанням ворогів босом — 🥉 (ресурс, який ти «віддаєш» ворогові).
- Телеграфована вогняна смуга, що гасне зі смертю дракона — 📎.
- Нежить: рештки, які треба розтоптати до відродження — 🌱.
- Пута з «коренями», що рвуться від будь-якої дії — 🌱.
- Та сама дошка за `R` і окремі рахунки для дошки — 📎 (seed + таблиця за seed).

## Мапа на каталог
- Є: `move-by-input` · `impassable-cells` (стіни) · `telegraph-marker` / `telegraphed-intents` (вогняна смуга) · `drop-on-death` (носії) · `sequential-levels` (глибини) · `restart-level` · `leaderboard` · `game-pause` · `keyboard-controls` · `message-log`.
- **Нема** → пропозиції карток:
  - `+ring-board` (як у корпусі) — поле-кільця × сектори.
  - `+shrinking-arena` (як у корпусі) — край поля зникає за таймером.
  - `+boss-absorb-growth` «Бос поглинає ворогів з обваленого краю й росте» · game-logic/waves · 🥉.
  - `+bump-attack` «Атака рухом у ворога» · entities/combat · 🌱.
  - `+wait-turn`, `+fire-breath`, `+boss-fight` — уже в корпусі.
  - `+revive-remains` «Рештки встають, якщо не розтоптати» · entities/spawn · 🌱.
  - `+snare-roots` «Пута: N дій до звільнення» · entities/state · 🌱.
  - `+class-skill-timer` «Навичка класу спрацьовує за власним таймером» · entities/state · 📎.
  - `+rank-up-skill` «Ранги: навичка → пасиви → фінальна форма» · entities/state · 🌱.

## Пропозиції до словників
- `+effect:absorb(boss, a)` — бос поглинає сутність і сильнішає (уже пропонували в корпусі); обвал — ✅ `timer` + `set_cell`, спуск — ✅ `next_level`, пута — ✅ `state(hero, snared)`.
- `+ui:ringfall-gauge` — шкала до наступного обвалу; `+ui:inspect-panel` — панель огляду клітини; `+ui:glint-marker` — блиск на ворогах із дропом.
- `+axis:field=ring` (як у корпусі) — полярна сітка.
- `+card:boss-absorb-growth`.

## Джерела
- ⭐ [itch.io: Ringfall](https://helmworkshop.itch.io/ringfall) — опис арени, обвалу й поглинання, керування, рестарт дошки, онлайн-рахунки, статус (HTML5, Godot, безкоштовно, бета).
- [Devlog 0.2.0](https://helmworkshop.itch.io/ringfall/devlog/1748626/020-released) — ранги, Ward і Nova, Space-очікування, дракони / нежить / гай, носії дропу, швидший ріст боса вглиб, термінальний інтерфейс.
- YouTube: [пошук](https://www.youtube.com/results?search_query=Ringfall+helm+workshop+roguelike).

## Непевне
- (?) Розмір арени (кількість кілець і секторів) і період обвалу «кожні кілька ходів».
- (?) Чи звичайний удар убиває ворога одразу — devlog лише каже, що під Ward удар «щербить замість вбити».
- (?) Що буде з героєм на кільці, що обвалюється; HP героя і як він гине.
- (?) Ефекти зілля й пісочного годинника; як герой набирає ранг (за вбивства?).
- (?) «Спиця» = радіальна лінія клітин — моє тлумачення слова spoke.
- (?) Рік 2026 і статус «In development» — за сторінкою itch на 2026-11; опубліковано ~13 днів тому.
