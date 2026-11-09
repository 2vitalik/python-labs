---
title: Castle Wolfenstein
slug: castle-wolfenstein
aka: [Замок Вольфенштайн]
family: maze-arcade
also: []
klass: avatar
axes:
  field: free
  time: realtime
  opponent: ai
  info: hidden
  random: setup
  goal: state
year: 1981
platforms: [Apple II, Atari 8-bit, Commodore 64, MS-DOS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Castle_Wolfenstein", best: true, note: "процедурний замок ~60 кімнат, вартові й SS, скрині, уніформа, капітуляція, вибух скрині, перезапуск за причиною смерті, звання"}
  - {kind: other, url: "https://archive.org/details/Castle_Wolfenstein_1989_MUSE_Software", note: "мануал Muse: керування для всіх платформ, обшук, відмикання, ліміти запасу, звання, збереження"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Castle+Wolfenstein+1981", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-8dir, orientation-state, projectile-shot, shoot-forward, explode-area, line-of-sight-attack, key-and-door, item-pickup, inventory-items, inventory-limit, player-death, dungeon-generation, stairs-levels, reach-exit, difficulty-levels, save-game, save-single-slot, keyboard-controls, game-pause, +room-exits, +disguise-uniform, +surrender-on-aim, +search-action, +timed-unlock, +noise-alert, +explosive-chest, +armored-enemy, +rank-promotion, +death-keeps-layout, +aim-separate-from-move, +taunt-speech]
proposes: ["+trigger:room_exit", "+effect:alert(a)", "+trigger:aimed_at(a, b)", "+card:disguise-uniform", "+card:surrender-on-aim", "+card:explosive-chest", "+card:rank-promotion", "+card:death-keeps-layout", "+card:aim-separate-from-move"]
author: opus
date: 2026-11-09
---

# Castle Wolfenstein — втеча з процедурного замку: обшукуй вартових, відмикай скрині, не стріляй у скриню з гранатами

## Суть
Втікач-шпигун починає в підземеллі замку з пістолетом, 10 набоями й 3 гранатами від помираючого вʼязня; мета — знайти воєнні плани й вибратися живим. Замок з ~60 кімнат генерується на старті, кімнати з'єднані проходами й сходами між поверхами. Вартових можна застрелити або змусити здатись прицілом (навіть без набоїв), обшукати й забрати їхнє; SS у бронежилетах беруть лише гранати, а уніформа проводить повз звичайну охорону. Межова гра сімʼї: рух вільний у кімнаті, як у [Berzerk](berzerk.md), сітковий лише граф кімнат — цей файл короткий.

## Поле і час
- Замок ≈ 60 кімнат, складених з 64 взаємозамінних планів, перетасованих при генерації (35–60 с до старту); старт — найнижчий поверх.
- Кожна кімната має щонайменше один прохід у сусідню або сходи на інший поверх; ті самі кімнати лишаються, доки не втечеш або не згенеруєш новий замок.
- Вид згори на одну кімнату (екран); рух вільний, не клітинний (`field: free`); що в скринях — невідомо до відкриття (`info: hidden`).
- Real-time; відмикання скрині триває помітний час — саме це «вікно ризику».

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Шпигун | player | набої, ≤ 3 гранати, ключі, жилет, уніформа, плани | рух 8 напрямків, окремо — приціл; стрільба, граната, обшук, відмикання |
| Вартовий | enemy | — | помічає й стріляє; під прицілом може здатись; кулі вбивають |
| SS-штурмовик | enemy | бронежилет | кулі не беруть — потрібна граната; уніформа його не обманює |
| Мертвий / полонений вартовий | container | його запас | обшук → потрібне в запас; обойма міняється, якщо в нього більше куль |
| Скриня | container | замкнена, вміст | відмикання з часом; постріл пришвидшує, але кличе охорону |
| Скриня з вибухівкою | hazard | набої / гранати | відкрита пострілом вибухає — гравець гине |
| Двері | gate | замкнені | приціл + пробіл — відмикання, або вистрелити |
| Прохід | static | — | перехід у сусідню кімнату |
| Сходи | static | — | перехід на інший поверх |
| Уніформа | pickup | — | звичайні вартові не помічають |
| Бронежилет | pickup | — | захист (деталі — (?)) |
| Воєнні плани | pickup | — | з ними втеча = гарантоване підвищення |
| Їжа й напої (капуста, ковбаски, шнапс) | pickup | — | без ефекту |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move_dir)` → ТО `move(player, dir)`; КОЛИ `input(aim_dir)` → ТО `face(player, dir)` — рух і приціл незалежні; клавіша S — стоп.
- КОЛИ `input(fire)` → ЯКЩО `has(player, bullets)` → ТО `spawn(bullet)`, `counter(bullets, -1)`.
- КОЛИ `contact(bullet, guard)` → ЯКЩО `not has(guard, vest)` → ТО `transform(guard, dead_guard)`; ЯКЩО SS → ТО `custom: «куля не бере»`.
- КОЛИ `custom: «гравець цілиться у вартового»` (`+trigger:aimed_at`) → ЯКЩО `prob(p)` → ТО `set_state(guard, surrendered)` — навіть з порожнім пістолетом.
- КОЛИ `input(space)` → ЯКЩО `occupied(target, dead_guard)` `or state(guard, surrendered)` → ТО `give(player, needed_items)`; обойму — лише ЯКЩО `custom: «у вартового більше куль»`.
- КОЛИ `input(space)` → ЯКЩО `cell(aim, door|chest)` → ТО `custom: «відмикання триває кілька секунд»`, `unlock(x)`.
- КОЛИ `contact(bullet, door|chest)` → ТО `unlock(x)` (швидше), `custom: «вартові в кімнаті йдуть на постріл»` (`+effect:alert`).
- КОЛИ `contact(bullet, chest)` → ЯКЩО `custom: «у скрині набої й гранати»` → ТО `explode(area)`, `lose`, `custom: «новий замок»`.
- КОЛИ `input(use_chest)` → ЯКЩО `custom: «скриня відчинена»` → ТО `pickup(player, item)` у межах лімітів.
- КОЛИ `input(grenade)` → ЯКЩО `has(player, grenade)` → ТО `custom: «граната летить у напрямку прицілу»`, `explode(area)`, `take(player, grenade)`; гине й SS.
- КОЛИ `line_of_sight(guard, player)` → ЯКЩО `has(player, uniform)` `and not same(guard, ss, type)` → ТО `custom: «не помічає»`; інакше `custom: «окрик "Halt!" і вогонь»`.
- КОЛИ `custom: «влучання ворожої кулі»` → ТО `lose`, `restart` — той самий замок, скрині й вартові.
- КОЛИ `custom: «гравець у вибуху власної гранати»` → ТО `lose`, `custom: «новий замок»`.
- КОЛИ `reach(player, doorway)` → ТО `custom: «сусідня кімната»` (`+trigger:room_exit`); КОЛИ `enter(player, stairs)` → ТО `custom: «інший поверх»`.
- КОЛИ `reach(player, castle_exit)` → ЯКЩО `has(player, war_plans)` → ТО `win`, `custom: «підвищення звання; новий, складніший замок»`; без планів — підвищення лише можливе.
- Перемога: втеча з планами. · Поразка: куля (той самий замок) або власний вибух (новий замок). · Рахунок: очок нема — прогрес = звання (8 рівнів складності).

## Керування і ввід
- Клавіатура: клавіші руху (8 напрямків) і окремі клавіші прицілу; S — стоп; L — вогонь (Apple, IBM) / сховати пістолет (Atari, C64).
- Джойстик: «натиснути — цілитись, відпустити — йти»; Atari — режим двох джойстиків (рух і приціл окремо, кнопка гранати); падли — напрям руху, прицілу й постріл.
- Пробіл — обшук, відмикання дверей і скринь; окремі клавіші — кинути гранату, взяти вміст відчиненої скрині, показати запас.
- ESC (Apple, IBM) / RUN/STOP (C64) — зберегти позицію й вийти; Atari — клавіша паузи; IBM — CTRL-R міняє керування.

## Вікна, меню, HUD
- `splash-screen` — титул; Atari: START → екран вибору.
- `custom-window` — екран вибору: продовжити, новий замок зі збереженням звання, скинути звання до Private.
- `game-screen` — кімната згори: проходи, двері, сходи, скрині, вартові, SS, мертві вартові; репліки німецькою («Achtung!», «Halt!», «Kamerad»).
- `inventory-window` — список запасу (клавіша).
- `end-screen` (?) — повідомлення про втечу й нове звання.
- Переходи: титул → вибір → (генерація) кімната → … → втеча → звання → новий замок.

## Фічі поза полем
- `difficulty-presets` за званням: Private → Corporal → Sergeant → Lieutenant → Captain → Colonel → General → «???????».
- `save-slots`: один слот — вихід зберігає позицію, повернення — у неї.
- Генерація замку на старті; новий замок — за бажанням або після смерті від вибуху.
- Оцифрований голос вартових (вісім фраз).

## Варіації й родичі
- [Berzerk](berzerk.md) — та сама кімнатна real-time стрілянина (Warner надихався нею), але без скринь, обшуку й стелсу.
- [Wolfenstein 3D](wolfenstein-3d.md) — гра id Software за мотивами: втеча із замку, але від першої особи на сітці 64×64, без стелсу й обшуку.
- Beyond Castle Wolfenstein (1984) — сиквел із перепустками (Wikipedia); [Atari Adventure](atari-adventure.md) — кімнати-екрани з предметами.
- **Осі варіацій:** стелс (нема / уніформа / перепустки); вороги (лише вбити / ще й здатися); ціна смерті (той самий світ / новий світ за причиною); прогрес (рівні / звання → складність).

## Цікавинки для курсу
- Генерація замку з набору планів кімнат і перевірка, що вихід досяжний, — 🥇.
- Відмикання на час з альтернативою «постріл = швидко, але шумно» — 🌱 (ризик vs час).
- Уніформа як маска: умова в AI вартового за типом ворога — 🌱.
- Капітуляція під прицілом без набоїв + обшук тіла з правилом «обойма, лише якщо більша» — 📎.
- Причина смерті визначає, що перегенерувати — 🌱.
- Розділення напрямку руху й прицілу (twin-stick 1981 року) — 📎.

## Мапа на каталог
- Є: `move-8dir` · `orientation-state` (приціл) · `projectile-shot` + `shoot-forward` · `explode-area` (граната) · `line-of-sight-attack` · `key-and-door` · `item-pickup` + `inventory-items` + `inventory-limit` (3 гранати) · `player-death` · `dungeon-generation` · `stairs-levels` · `reach-exit` · `difficulty-levels` (звання) · `save-game` + `save-single-slot` · `keyboard-controls` · `game-pause`.
- **Нема** → пропозиції карток:
  - `+room-exits` (`berzerk`, `atari-adventure`); `+search-action` (`spy-vs-spy`); `+taunt-speech` (`berzerk`).
  - `+disguise-uniform` «Предмет-маска: частина ворогів не помічає» · entities/ai · 🌱.
  - `+surrender-on-aim` «Ворог здається під прицілом» · entities/ai · 📎.
  - `+timed-unlock` «Відмикання триває N тіків, можна пришвидшити» · entities/interact · 🌱.
  - `+noise-alert` «Постріл кличе ворогів кімнати» · entities/ai · 🌱.
  - `+explosive-chest` «Скриня з вибухівкою вибухає від пострілу» · entities/interact · 🌱.
  - `+armored-enemy` «Ворог, якого не бере звичайна зброя» · entities/combat · 🌱.
  - `+rank-promotion` «Перемога підвищує звання = складність» · levels/progression · 🌱.
  - `+death-keeps-layout` «Смерть: той самий світ чи новий — за причиною» · entities/death · 🌱.
  - `+aim-separate-from-move` «Приціл окремо від руху» · interface/input · 📎.

## Пропозиції до словників
- `+trigger:room_exit` — підтверджую з `berzerk` / `atari-adventure`.
- `+effect:alert(a)` — підтверджую з `wolfenstein-3d`: ворог переходить у бойовий режим на шум.
- `+trigger:aimed_at(a, b)` — A тримає B на прицілі (капітуляція, реакція на загрозу).
- `+card:*` — шість карток вище.

## Джерела
- ⭐ [Wikipedia: Castle Wolfenstein](https://en.wikipedia.org/wiki/Castle_Wolfenstein) — замок ~60 кімнат з 64 планів, генерація 35–60 с, стартовий набір, ключі й скрині, уніформа, капітуляція без набоїв, SS і гранати, вибух скрині, перезапуск за причиною смерті, звання й 8 рівнів складності, оцифрована мова.
- [Мануал Muse, archive.org](https://archive.org/details/Castle_Wolfenstein_1989_MUSE_Software) — керування для Apple / Atari / C64 / IBM, пробіл для обшуку й відмикання, правило обойми, ліміти запасу, список звань, збереження, екран вибору, легенда екрана.
- YouTube: пошук «Castle Wolfenstein 1981».

## Непевне
- (?) Ліміт набоїв: у скані мануалу число зіпсоване («maximum of 1 bullets»).
- (?) Що дає бронежилет гравцеві (витримати влучання?) — джерела лише називають його.
- (?) Імовірність капітуляції і чи SS теж здаються; чи вартові переслідують між кімнатами.
- (?) Чи граната руйнує стіни або двері — мануал каже лише «в напрямку прицілу».
- (?) Літери клавіш гранати, скрині й запасу — розкладка в скані нечитабельна.
- (?) Як кімнати укладені на поверхах (сітка екранів чи довільний граф) — у джерелах не сказано.
