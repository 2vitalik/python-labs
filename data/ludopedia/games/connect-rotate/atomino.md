---
title: Atomino
slug: atomino
aka: []
family: connect-rotate
also: [falling-match]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: collect
year: 1990
platforms: [Amiga, Atari ST, DOS, C64]
links:
  - {kind: other, url: "https://www.atarimania.com/game-atari-st-atomino_11129.html", best: true, note: "скани мануалу Psygnosis (EN/FR/IT): поле 7×8, яма на 6 атомів, курсор і SPACE, обмін, джокер, Extra Round, режими A/B, очки"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Atomino", note: "ядро: валентність 1–4, обмін, молекула зникає, цілі рівнів, переповнення"}
  - {kind: wiki, url: "https://de.wikipedia.org/wiki/Atomino_(Computerspiel)", note: "джокер стає атомом з потрібною валентністю, перешкоди, бонус-рівні, паролі"}
  - {kind: other, url: "https://www.c64-wiki.com/wiki/Atomino", note: "C64: кольори валентностей, очки, паролі рівнів 1–100, керування"}
  - {kind: other, url: "https://everygamegoing.com/larticle/power-test-atomino/82474", note: "огляд C64: курсор показує можливі звʼязки, обмін «з'їдає» яму, пазл-раунди"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Atomino+Psygnosis+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [cursor-place, next-queue, connectivity-check, collect-quota, impassable-cells, progress-acceleration, event-points, sequential-levels, level-password, mode-select, score-records, leaderboard, main-menu, game-screen, status-panel, goal-counter, help-window, music-toggle, sound-effects, theme-select, game-pause, +valence-bonds, +wildcard-tile, +swap-with-queue, +queue-overflow, +pinned-piece, +clear-all-goal, +bonus-stage, +copy-protection-code]
proposes: ["+ui:bond-preview", "+window:bonus-round", "+window:protection-code", "+card:valence-bonds", "+card:swap-with-queue", "+card:queue-overflow", "+card:pinned-piece", "+feature:copy-protection"]
author: opus
date: 2026-11-09
---

# Atomino — клади атоми з 1–4 вільними звʼязками поруч; молекула без вільних звʼязків зникає, а яма не має переповнитись

## Суть
Атоми випадкової валентності (1–4 «руки») падають у вузьку яму праворуч від поля; нижній — поточний. Гравець ставить його курсором у вільну клітину поля 7×8: з сусідами зліва, справа, згори чи знизу утворюються звʼязки, і кожен звʼязок забирає по одній вільній «руці» в обох атомів. Звʼязна структура, у якої не лишилось жодної вільної руки, — завершена молекула: вона зникає й дає очки. Якщо у яму впаде сьомий атом — кінець гри, тож ставити треба швидко, а атом-«четвірку» біля краю чи «трійку» в куті вже не закрити.

## Поле і час
- Поле 7 × 8 = 56 клітин, квадратна сітка, 4-сусідство; звʼязки лише по ортогоналях.
- Яма-черга праворуч на 6 атомів; атоми падають у неї за таймером — спершу повільно, з рівнями (і з часом у режимі B) швидше.
- Real-time: тиск часу задає лише темп появи атомів; поле між ходами нерухоме, нічого не падає.
- На вищих рівнях режиму A — клітини-блоки, куди не можна ставити; рівні-контури з «бульбашками»; прикручені атоми.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Атом 1 | tile | валентність 1 (C64: синій) | 1 вільна рука; звʼязується з одним сусідом |
| Атом 2 | tile | валентність 2 (C64: червоний) | 2 руки |
| Атом 3 | tile | валентність 3 | 3 руки; у куті — завжди лишиться вільна рука |
| Атом 4 | tile | валентність 4 (C64: жовтий) | 4 руки; на краю — завжди лишиться вільна рука |
| Джокер | tile | без валентності | ставиться будь-куди й «підлаштовується»: валентність = кількість звʼязків, які він утворив; без жодного звʼязку одразу зникає без очок |
| Яма (pit) | supply | місткість 6 | черга атомів; поточний — нижній; 7-й атом = кінець гри |
| Молекула | zone | кількість атомів | звʼязна група; без вільних рук — зникає |
| Блок | static | — | клітина, куди не можна ставити; переходить і в Extra Round |
| Бульбашка (контур) | static | — | обмежує фігуру, яку треба заповнити (рівні «Complete the given pattern») |
| Прикручений атом | tile | screwed | стоїть від початку рівня; не обмінюється; його треба вбудувати в молекулу |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `timer(drop_interval)` → ТО `spawn_at(random_atom, pit_top)`; інтервал скорочується з рівнем (A) або з часом (B).
- КОЛИ `counter(pit, ==, 7)` → ТО `game_over`, `window(leaderboard)` (імʼя в таблицю рекордів, запис на диск).
- КОЛИ `input(fire, cell)` → ЯКЩО `free(cell)` і `not cell(cell, block)` → ТО `place(player, current_atom)`, `score(+10)` (лише режим B).
- КОЛИ `after(place)` → ТО `attach(atom, neighbour)` для кожного обраного напрямку, `counter(free_bonds, -1)` в обох атомів.
- КОЛИ `input(space)` → ЯКЩО `custom: «курсор поруч з кількома атомами, а рук на всіх не вистачає»` → ТО `custom: «змінити, з якими сусідами утвориться звʼязок»`.
- КОЛИ `input(fire, cell)` → ЯКЩО `occupied(cell, atom)` і `not state(atom, screwed)` → ТО `swap(current_atom, atom)` — знятий атом повертається на дно ями.
- КОЛИ `input(fire, cell)` → ЯКЩО `custom: «поточний атом — джокер»` і `adjacent_count(cell, free_bond, >=, 1)` → ТО `place(player, joker)`, `set_value(joker, bonds_formed)`; інакше `disappear(joker)` без очок.
- КОЛИ `counter(free_bonds_of_group, ==, 0)` → ТО `clear(molecule)`, `score(+size²)`.
- Режим A, ціль «x молекул ≥ y атомів»: КОЛИ `after(clear)` → ЯКЩО `count(molecule_atoms, >=, SIZE)` → ТО `counter(LEFT, -1)`; на перших рівнях будь-яка молекула рахується.
- Режим A: КОЛИ `counter(LEFT, ==, 0)` → ЯКЩО `count(atom, ==, 0)` → ТО `next_level`; інакше `message(«очисти поле»)` — і подальші молекули вже без очок.
- Ціль «заповни контур»: КОЛИ `input(fire, cell)` → ЯКЩО `not cell(cell, inside_outline)` → ТО `block`; атоми в яму йдуть не випадково, а під контур (якщо збудувати з першої спроби); очки — лише після повного контуру.
- Ціль «прибери задані атоми»: КОЛИ `custom: «усі прикручені атоми вбудовано в молекули й зникли»` → ТО `custom: «рівень можна завершити»`, ймовірно бонус-очки (?).
- КОЛИ `after(clear)` → ЯКЩО `count(molecule_atoms, >=, EXTR)` і `count(atom, ==, 0)` → ТО `message(«EXTRA ROUND?»)`.
- КОЛИ `input(fire)` → ЯКЩО `timer(<=, 2)` (після питання) → ТО `window(bonus-round)`; інакше гра йде далі.
- Extra Round: КОЛИ `level_start` → ТО `custom: «усе поле заповнене атомами; часу не обмежено; ходи — лише обмін»`.
- Extra Round: КОЛИ `after(clear)` → ТО `score(+2×size²)`, `custom: «раунд скінчено; атоми поза молекулою лишаються на полі, нові падають лише після молекули»`.
- Перемога: нема фінальної — рівні йдуть далі (паролі до 100-го). · Поразка: сьомий атом у ямі. · Рахунок: режим B — 10 за атом + (атомів у молекулі)²; режим A — лише за молекули цілі; Extra Round — подвійні очки (C64: повна молекула з 56 атомів = 2 × 56² = 6272).

## Керування і ввід
- Джойстик (або миша на 16-біт (?)): рух курсора по полі; FIRE — поставити поточний атом або обміняти з поставленим; FIRE — прийняти «EXTRA ROUND?» за 2 секунди.
- SPACE — перебрати напрямки звʼязку, коли можливих кілька.
- C64: P — пауза, RUN/STOP — на титульний екран, H на титулі — довідка з короткими анімаціями.
- Курсор сам показує валентність поточного атома, а поруч із поставленими — лініями, з ким він звʼяжеться.

## Вікна, меню, HUD
- `main-menu`: Music ON/OFF · FX ON/OFF · Colour 1/2 (лише C64) · Mode A/B · Password · Start · Quit.
- `level-password`: ввести пароль, щоб почати з вищого рівня (C64 — кожні 10 рівнів).
- `custom-window` захист від копіювання: гра питає код із таблиць на сторінках мануалу (C64: після першого рівня).
- `game-screen`: поле 7×8; ліворуч угорі `score`, під ним статус — SIZE (мін. розмір молекули), LEFT (`remaining-counter` молекул), SET (атомів на полі), EXTR (поріг Extra Round); праворуч яма — `next-piece-preview` на 6; курсор з `+ui:bond-preview`.
- `confirm-dialog` «EXTRA ROUND?» з відліком 2 с → `custom-window` Extra Round.
- `help-window` (C64, H на титулі): анімовані пояснення.
- `end-screen` Game Over з власною мелодією → `leaderboard` з введенням імені.
- Переходи: титул → main-menu → (пароль) → game-screen → (рівень) game-screen → (EXTR) Extra Round → game-screen → (7-й атом) Game Over → leaderboard → титул.

## Фічі поза полем
- `mode-select`: A — рівні із завданнями (3 типи цілей); B «right down to K.O.» — без цілей, блоків і гвинтів, лише очки, темп росте.
- `levels-sequential` + `level-password`; `leaderboard-local` (зберігається на диск).
- `music-toggle`, `sound-toggle`, `theme-select` (набір кольорів атомів 1/2, C64), `pause`, `rules-page` (анімована довідка).
- Захист від копіювання кодом з мануалу — приклад «вікна поза грою».

## Варіації й родичі
- **Осі варіацій**:
  - звідки атом: випадкова черга з переповненням (Atomino) / задані атоми на полі, які штовхаєш (`thinky/sokobond`) / ковзання до упору до цільової молекули (`push-slide/atomix`);
  - мета: будь-яка закрита молекула зникає (Atomino) / точна цільова молекула (Atomix, Sokobond);
  - вибір звʼязку: автоматично з усіма сусідами / гравець обирає напрямки SPACE, коли рук менше, ніж сусідів (Atomino).
- Спільне ядро «закрита структура зникає, черга тисне»: `loopz` (замкнена петля), `pipe-mania` (черга труб); Tetris — переповнення як програш.
- Не плутати з `board-digital/ubongo` (викладання поліоміно в контур на час) — інша гра; контурні рівні Atomino лише нагадують її.

## Цікавинки для курсу
- Валентність як лічильник вільних рук + звʼязки з сусідами + перевірка «у звʼязної компоненти 0 вільних рук» (BFS) — 📎.
- Вибір напрямків звʼязку, коли рук менше за сусідів (перебір комбінацій SPACE) — 🥉.
- Обмін поставленого атома з поточним із поверненням на дно ями (черга як стек з обох боків) — 📎.
- Джокер, що набуває валентності за кількістю сусідів із вільними руками — 🌱.
- Три типи цілей рівня (квота розміру, контур, прикручені атоми) + умова «поле порожнє» — 🥉.
- Extra Round: поле, повне атомів, лише обміни, мета — одна молекула з усіх 56 (пошук перестановки) — 🥇.
- Темп падіння в яму, що росте з рівнем, і переповнення на 7-му атомі — 🌱.

## Мапа на каталог
- Є: `cursor-place` ↔ поставити атом · `next-queue` ↔ яма на 6 · `connectivity-check` ↔ молекула = звʼязна група · `collect-quota` ↔ «x молекул ≥ y» · `impassable-cells` ↔ блоки й бульбашки · `progress-acceleration` ↔ швидше падіння · `event-points` · `sequential-levels` + `level-password` · `mode-select` · `score-records` + `leaderboard` · `goal-counter` ↔ LEFT · `status-panel` ↔ SIZE/LEFT/SET/EXTR · `help-window`, `music-toggle`, `sound-effects`, `theme-select`, `game-pause`, `main-menu`, `game-screen`.
- **Нема** → пропозиції карток:
  - `+valence-bonds` (є в корпусі, Sokobond) — ліміт звʼязків на атомі.
  - `+wildcard-tile` (є в корпусі) — джокер-атом.
  - `+swap-with-queue` «Обмін поставленої фігури з поточною, стара — назад у чергу» · entities/legality · 📎.
  - `+queue-overflow` «Переповнення черги надходження — програш» · game-logic/lose · 🌱 · слот {capacity: 6}.
  - `+pinned-piece` «Закріплена фігура: не обмінюється, лише прибирається» · entities/legality · 🌱.
  - `+clear-all-goal`, `+bonus-stage` (є в корпусі) — порожнє поле для рівня; Extra Round.
  - `+copy-protection-code` «Код із мануалу як вхід у гру» · interface/menus · 🌱.

## Пропозиції до словників
- `+ui:bond-preview` — лінії від курсора до сусідів, з якими утвориться звʼязок.
- `+window:bonus-round` (повтор корпусу) — Extra Round з іншими правилами.
- `+window:protection-code` — запит коду з мануалу.
- `+feature:copy-protection` — перевірка оригіналу кодом із друкованих матеріалів.
- `+card:valence-bonds`, `+card:swap-with-queue`, `+card:queue-overflow`, `+card:pinned-piece` — див. «Мапа на каталог».

## Джерела
- ⭐ [Atarimania: Atomino (ST), скани мануалу](https://www.atarimania.com/game-atari-st-atomino_11129.html) — англійський мануал Psygnosis: 4.1–4.6 (поле 7×8, статус SIZE/LEFT/SET/EXTR, яма на 6, 7-й атом = Game Over, побудова молекули, курсор і SPACE, обмін, джокер), 5 (Extra Round), 6 (режими A і B, три типи цілей), 7 (очки), 8 (поради), таблиці кодів захисту.
- [Wikipedia EN: Atomino](https://en.wikipedia.org/wiki/Atomino) — Blue Byte / Psygnosis 1990, валентність 1–4, обмін, цілі рівнів, переповнення ями.
- [Wikipedia DE: Atomino (Computerspiel)](https://de.wikipedia.org/wiki/Atomino_(Computerspiel)) — джокер, перешкоди, прикручені атоми, бонус-рівні, режими «K.-o.» і «Spielstufen», паролі й рекорди.
- [C64-Wiki: Atomino](https://www.c64-wiki.com/wiki/Atomino) — кольори 1/2/4, очки режимів, 6272 за повний Extra Round, керування C64, паролі рівнів 1–100, тактика.
- [Everygamegoing: Power Test Atomino](https://everygamegoing.com/larticle/power-test-atomino/82474) — огляд C64: курсор-превʼю звʼязків, обмін забиває яму, пазл-раунди, палітри.
- YouTube: пошук «Atomino Psygnosis gameplay».

## Непевне
- (?) Колір атома-«трійки» і кольори на Amiga/ST — у джерелах нема (C64: 1 синій, 2 червоний, 4 жовтий).
- (?) Миша на Amiga/ST/DOS — мануал у прочитаних розділах говорить лише про джойстик і FIRE.
- (?) Бонус за вбудовані прикручені атоми — мануал: «you'll probably get some extra points»; C64-Wiki пише про множення очок на кількість прикручених.
- (?) Точні інтервали падіння, кількість рівнів на ПК; «близько 600 000 рівнів» з огляду — сумнівне.
- (?) Чи звʼязки утворюються з усіма сусідами автоматично, коли рук вистачає на всіх (так видно з прикладів мануалу), і як джокер обирає звʼязки за кількох сусідів.
- Плутанина черги: автоматика звʼязала Atomino з `board-digital/ubongo` — це різні ігри.
