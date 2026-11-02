# 04 · Як системи класифікації витримали корпус

`2026-11-02` · корпус: **~230 ігор** у 17 сімʼях · живі матриці — [index/harvest.md](../index/harvest.md) («Таксономія»).

## Сімʼї-теки (17) — витримали, з трьома уточненнями

- Жодна тека не виявилась порожньою чи «смітником»: від 7 (grid-platformer) до 25+ (pencil-logic, chess-abstract) ігор. `also:` вжито у 150+ файлах — гібридність нормальна і фіксується, як задумано.
- Найчастіші другі домівки: `push-slide` ×19, `thinky` ×17, `pencil-logic` ×16, `board-digital` ×13, `maze-arcade` ×13, `roguelike` ×12. Тобто **push-slide і thinky — не дві сімʼї, а дві осі** (класична механіка штовхання ↔ «відкриття правила»): межу «якщо ядро — відкриття правила → thinky» агенти застосовували, але 5 ігор (Jelly, Hanano, Puddle Knights, Helltaker, Kwirk) опинились на межі. Пропозиція: лишити теки, але в `families.md` записати правило явно: *thinky = гра з 2015+ з авторськими правилами, що відкриваються; все, що є варіацією Sokoban-механіки без «відкриття», — push-slide*.
- Спірні призначення, зроблені куратором (агенти заперечили): **Theseus and the Minotaur** → roguelike (черга радила thinky; це логічний лабіринт — правильніше `push-slide`/`thinky`); **Quoridor** → chess-abstract (черга: board-digital; `also` є); **Hoplite** → `klass: figure` (агент: за суттю `avatar` — один герой на гексах; правильно `avatar`); **Recursed** → thinky (черга: grid-platformer — платформер з гравітацією; правильно `also: grid-platformer`, зроблено). Правки — одним проходом по шапках після сесії.
- **Межові випадки корпусу** (описані, але не «клітинні» в строгому сенсі): Frozen Synapse (вільний простір, WEGO), Gorogoa (панелі), Kula World (3D), Townscaper (нерегулярна сітка), Powder Toy/ONI (клітинна фізика без гри). Їх варто тримати як «край мапи» — вони показують, де закінчується мова клітинного поля.

## Класи за актором (`klass`) — витримали, але просять пʼятого

Розподіл (169 ігор на момент матриці): avatar 65 · cursor 46 · figure 28 · puzzle 26 · hybrid 4. Кореляція з сімʼями очікувана: maze/platformer/roguelike/thinky/dig → avatar; tower/falling/build/board → cursor; chess/tactics → figure; pencil → puzzle; hidden-deduction і word — навпіл cursor/puzzle.

Проблеми:
1. **Tetris / Puyo / Dr. Mario / Columns** — агенти поставили `avatar` (керуєш однією активною фігурою, щоразу новою), тоді як 2048 за T49 — `cursor`. Корпус показує третій тип дієслова: «керую активним обʼєктом, який змінюється». Варіанти: (a) лишити `avatar` з приміткою в `_classes.md`; (b) ввести значення `piece` — «активна фігура без постійного аватара»; (c) `cursor`. Рекомендую **(a)**: для студента скелет коду той самий, що в аватарних (вхід рухає одну сутність), а різниця — у спавні нової фігури після фіксації — це картка `next-queue`/`spawn-schedule`, не клас. → Q-тікет.
2. **Програмовані ігри** (program-robots: 14 файлів) не лягають у жоден з чотирьох класів: гравець не рухає аватар, не клікає клітини, не ходить фігурами й не розмічає — він **пише програму**, яка потім рухає сутність. Усі агенти писали `avatar` + `axes.time: programmed` + `+axis:control=programmed`. Пропозиція: пʼятий клас **`programmed`** («програмні»: Karel, Lightbot, RoboRally, 7 Billion Humans, The Farmer Was Replaced, Opus Magnum) — для курсу Python це найприродніший клас взагалі (студент пише інтерпретатор команд над своїм же полем), і він дає окрему підзону карток (03 §2). → Q-тікет.
3. **hybrid** вжито 4 рази (Backpack Hero, Dungeon of the Endless, Mindustry, Townscaper) — рідко, бо `also` і осі покривають гібридність; значення можна лишити як запобіжник.

## Осі (`axes`) — витримали; значення ⏳ підтвердились

- `field`: square ×148 · hex ×8 · graph ×5 · layers ×4 · iso ×3 · 3d ×1 — усі ⏳-значення вжиті; агенти просять ще `irregular-quad` (Townscaper), `hyperbolic` (HyperRogue), `nested` (Parabox, Recursed — поле всередині поля), `side-view` (ONI, платформери — ортогональна сітка з гравітацією вниз). Пропозиція: `nested` і `hyperbolic` — як екзотика в `_classes.md`; `side-view` — **не вісь поля, а значення нової осі `gravity`** (див. нижче).
- `time`: turn ×79 · realtime ×52 · static ×29 · programmed ×8 · rhythm ×1 — `programmed` і `rhythm` підтверджені; просять `wego` (одночасне планування + виконання: Frozen Synapse, RoboRally, Diplomacy-подібне) — додати.
- `opponent`: none ×96 · ai ×39 · hotseat ×20 · online ×10 · coop ×4 — ок; у настолках часто кілька значень (hotseat+online+ai) — шапка бере домінантне; варто дозволити список.
- `info`: full ×118 · hidden ×26 · partial ×25 — `partial` (Into the Breach, туман) виявився потрібним — підтверджено.
- `random`: none ×71 · runtime ×45 · setup ×35 · both ×18 — 4 значення працюють.
- `goal`: state ×69 · score ×30 · collect ×21 · constraints ×20 · survive ×19 · territory ×7 · race ×3 — усі 7 вжиті; просять `none` (Townscaper, Powder Toy — іграшки без мети) — додати як легальне.

Нові осі, підтверджені правилом трьох (детально — 01): `control` (direct / indirect / programmed / swipe-all / drag-path / grab-throw) ×16 · `session` (level / endless / daily / match / run) ×14 · `undo` (none / limited / unlimited / rewind) ×13 · `actors` (single / party / swarm) ×7 · `gravity` (none / down / up / per-type / toward-center) ×5 · `turn-structure` (sequential / time-track / simultaneous / wego) ×4. Ще поодинокі, але змістовні: `guess-policy` (random / punished / forgiven / impossible — сапер і родичі), `view` (top-down / side / first-person / iso), `markup-layers` (пазли з двома шарами розмітки), `win-condition` (для фігурних: capture / reach / majority / connect / eliminate / last-mover), `stop-rule` (ковзання: до упору / на 1 / до обʼєкта).

Рекомендація для шапки корпусу й для `BaseGame.axes`: додати `control`, `session`, `undo`, `gravity`, `turn-structure`; решту тримати як теги-пропозиції. Для **курсу** найцінніша `control` — вона напряму визначає, який ввід студент реалізує (клавіші напрямку / клік по клітині / свайп усього поля / drag шляху / список команд).

## Дієслова гравця (система 4 у systems.md)

З тегів `mechanics` виводяться стабільно: push ×(Sokoban-лінія ~30) · dig ×8 · match/merge ×20 · mark ×30 · reveal ×15 · place ×40+ · move-piece ×30 · program ×14 · connect/rotate ×20 · guess ×10 · command (indirect: клік-ціль) ×15. Дієслово `place` (покласти з запасу) виявилось найпоширенішим у настільних і TD-іграх і **відсутнє в каталозі як окрема дія** — пара до `move`. Висновок: дієслова — хороша навігація по корпусу («покажи всі ігри, де ставлять»), але окремого поля в шапці не потребують — виводяться з тегів.

## Зовнішні таксономії

Steam-теги й BGG-механіки корисні лише для пошуку кандидатів; Thinky Games і puzz.link — як канонічні назви жанрів (пазли). Для системи опису вони не додають вимірів, яких нема в осях + тегах.

## Що змінити в документах корпусу (зроблю/зроблено)

- `taxonomy/families.md`: правило thinky vs push-slide явно; Kwirk/Fire 'n Ice виправлено.
- `vocab/classes.md`: додати `wego`, `goal: none`, `field: nested|hyperbolic`, нові осі з 🔥 — зроблено частково (секція 🔥).
- Шапки: Hoplite → avatar; Theseus → push-slide. Масове перепризначення не роблю — рішення Vitalik у Q-тікеті.
