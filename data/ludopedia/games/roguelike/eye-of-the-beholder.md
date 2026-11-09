---
title: Eye of the Beholder
slug: eye-of-the-beholder
aka: [EOB, EoB, Око спостерігача]
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: hidden
  random: runtime
  goal: state
year: 1991
platforms: [PC (DOS), Amiga, PC-98, SNES, Mega-CD, GBA, C64 (фан-порт 2022)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Eye_of_the_Beholder_(video_game)", best: true, note: "суть: party-based кроулер у дусі Dungeon Master, 4 → 6 героїв, імпорт загону в сиквел"}
  - {kind: wiki, url: "https://de.wikipedia.org/wiki/Eye_of_the_Beholder_(Computerspiel)", note: "DE: 6 рас, 6 класів, 9 світоглядів, запамʼятовування заклинань після відпочинку, їжа, 12 рівнів, 7 камʼяних ключів-порталів, без автокарти в DOS"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=eye+of+the+beholder+1991+dos+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-4dir, orientation-state, impassable-cells, key-and-door, button-toggle, teleport-pair, hp-damage, inventory, inventory-items, inventory-limit, item-pickup, hunger-clock, status-effects, unit-xp-skills, melee-vs-ranged, projectile-shot, chase-player, stairs-levels, save-game, player-death, party-switch, character-select, drag-drop-piece, gui-render, player-camera, +first-person-grid, +party-formation, +two-hand-slots, +rule-system-import, +class-race-matrix, +spell-memorize-rest, +camp-menu, +stone-portal-keys, +party-import, +npc-recruit, +pressure-plate, +illusory-wall, +level-special-quest]
proposes: ["+trigger:rest(party)", "+cond:class(a, c)", "+effect:memorize(a, spell)", "+effect:recruit(npc)", "+window:camp-menu", "+window:spell-book", "+feature:party-import", "+card:spell-memorize-rest", "+card:stone-portal-keys"]
author: opus
date: 2026-11-09
---

# Eye of the Beholder — рушій Dungeon Master, але правила AD&D: класи, раси, рівні досвіду й заклинання, які заучують на привалі

## Суть
Загін із 4 героїв (до 6 з NPC) крокує клітинами підземель під містом Waterdeep від першої особи, бій іде в реальному часі. На відміну від [Dungeon Master](dungeon-master.md), персонажі зібрані за **Advanced Dungeons & Dragons**: раса, клас, світогляд, 6 атрибутів, рівні за досвід. Магія — не руни: маги й клірики **заучують заклинання** на привалі і витрачають їх. Головоломки рівнів — кнопки, плити, телепорти, камʼяні портали; 12 рівнів до фінального боса.

## Поле і час
- Квадратна сітка клітин, 12 рівнів-поверхів, сходи між ними; загін — одна фігура з орієнтацією, крок і поворот на 90°.
- Вид від першої особи кілька клітин углиб (`+first-person-grid`); в оригінальній DOS-версії **нема автокарти** — карту малюють самі (автокарта з'явилась у Mega-CD).
- Real-time: монстри ходять самі, бій без пауз; відпочинок прокручує час.
- Монстри блукають в межах своїх зон або переслідують загін.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Загін | player | 2×2 строї, орієнтація | рухається як одна фігура |
| Герой | ally | раса, клас, світогляд, 6 атрибутів, HP, рівень, 2 руки | атакує предметом у руці; кастер — заучені заклинання |
| NPC-супутник | ally | фіксовані риси | приєднується (5-й, 6-й член) або оживлений зі скелета |
| Стіна | static | — | непрохідна |
| Ілюзорна стіна | static | — | виглядає стіною, проходиться (?) |
| Двері (звичайні, замкнені) | gate | ключ / кнопка | відкриваються кнопкою, важелем або ключем |
| Кнопка / важіль | switch | — | перемикає двері, стіни, ями (?) |
| Плита тиску | switch | — | спрацьовує, коли на неї ступили або поклали предмет (?) |
| Телепорт | static | — | переносить загін у іншу клітину (?) |
| Камʼяний портал | static | 7 камʼяних ключів | ключ відповідного типу → телепорт в іншу частину підземелля |
| Яма / люк | hazard | — | падіння на рівень нижче (?) |
| Сходи | static | вгору/вниз | перехід між рівнями |
| Предмет (зброя, обладунок, сувій, зілля, їжа, ключ) | pickup | вага/слот | береться в інвентар, екіпірується |
| Монстр | enemy | HP, атака | блукає зоною або переслідує, бʼє в контакті, частина — здалеку |
| Бос (Xanathar, beholder) | boss | — | фінальний бій |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(step|strafe|turn)` → ЯКЩО `free(cell)` → ТО `move(party, dir)` / `face(party, dir)`; стіна, двері, монстр → `block`.
- КОЛИ `input(click_hand)` → ЯКЩО `custom: «герой у передньому ряду або зброя дистанційна»` `and not custom: «рука на перезарядці»` → ТО `custom: «атака предметом у руці»`, `damage(n)` за правилами AD&D (кидок на влучання) (?).
- КОЛИ `input(cast)` → ЯКЩО `custom: «заклинання заучене»` → ТО `custom: «ефект заклинання»`, `custom: «заклинання витрачене»`.
- КОЛИ `input(rest)` → ЯКЩО `not custom: «поруч ворог»` (?) → ТО `heal(heroes, n)`, `custom: «кастери заучують обрані заклинання»` (`+effect:memorize`), час іде.
- КОЛИ `timer(food_period)` → ТО `counter(food, -1)`; ЯКЩО `counter(food, ==, 0)` → `damage(n)` (`hunger-clock`).
- КОЛИ `contact(party, plate)` → ТО `custom: «перемикає повʼязані двері / стіни»` (?); КОЛИ `input(click_button)` → ТО той самий ефект.
- КОЛИ `input(use_key, door)` → ЯКЩО `has(party, key)` → ТО `custom: «двері відчинено»`, `take(party, key)`.
- КОЛИ `input(use_stone, portal)` → ЯКЩО `has(party, stone_key)` → ТО `teleport` в повʼязану частину підземелля.
- КОЛИ `enter(party, teleporter)` → ТО `teleport` (?).
- КОЛИ `enter(party, pit)` → ТО `custom: «падіння на рівень нижче»`, `damage(n)` (?).
- КОЛИ `died(monster)` → ТО `custom: «досвід ділиться між героями»`; КОЛИ `counter(xp, >=, threshold)` → ТО `custom: «рівень класу +1: HP, нові заклинання»`.
- КОЛИ `hp_zero(hero)` → ТО `custom: «герой мертвий, тіло — кістки-предмет»`; оживлення — заклинанням/жерцем (?).
- КОЛИ `custom: «усі герої мертві»` → ТО `game_over`.
- КОЛИ `custom: «знайдено особливий предмет / виконано квест рівня»` → ТО `custom: «бонус досвіду»` (?).
- КОЛИ `died(final_boss)` → ТО `win`.
- Перемога: знищити Xanathar-а на нижньому рівні. Поразка: загинув увесь загін. Рахунку нема — прогрес і досвід.

## Керування і ввід
- Мишею: екранні стрілки руху (крок, вбік, поворот), клік по руці героя — атака/використання, drag предметів між інвентарем, руками й світом.
- Клавіатура дублює рух; є підтримка геймпада у консольних версіях.
- Створення загону: кидок атрибутів з правкою, вибір раси/класу/світогляду, портрет.

## Вікна, меню, HUD
- `main-menu` — нова гра / завантажити / імпорт загону з іншої гри серії (?).
- `character-select` — створення 4 героїв: раса, клас (і мультиклас (?)), світогляд, атрибути, портрет.
- `game-screen` — 3D-вид, компас, стрілки руху, текстове вікно повідомлень; праворуч — 4–6 портретів з HP і двома руками кожен.
- `inventory-window` — «лялька» героя: слоти тіла, рюкзак, стати (сила, AC, рівень).
- `custom-window` — табір (`+window:camp-menu`): відпочинок, заучування заклинань, молитва, збереження/завантаження, налаштування.
- `custom-window` — книга заклинань (`+window:spell-book`) для вибору заклинання на касті.
- `end-screen` — фінал (у SNES/Mega-CD доданий повноцінний кінець).
- Переходи: створення → підземелля ↔ табір / інвентар → … → бос → фінал.

## Фічі поза полем
- `save-slots` — через табір.
- `feature: party-import` — загін переходить у сиквел Legend of Darkmoon, звідти — в Assault on Myth Drannor.
- Секрети: на кожному рівні — бонусна знахідка (промо 1991 року пропонувало її шукати).
- Mega-CD — автокарта, кат-сцени, озвучення; SNES — інший саундтрек.

## Варіації й родичі
- [Dungeon Master](dungeon-master.md) — той самий формат (загін 2×2, real-time на сітці, дві руки). Відмінності: у DM навички ростуть від вживання й нема класів, магія — руни з маною; у EOB — класи/раси AD&D, рівні за досвід, заучування на привалі, NPC-рекрути, табір замість окремих кнопок сну/збереження.
- [Legend of Grimrock](legend-of-grimrock.md) — сучасний нащадок з плитами, важелями й алкавами.
- Eye of the Beholder II: The Legend of Darkmoon (1991) — поверхнева частина, більше рольових елементів; EOB III (1993); GBA-ремейк (2002) — покроковий бій.
- [Rogue](rogue.md), [Brogue](brogue.md) — покрокові роглайки з одним героєм і генерацією; EOB — ручні рівні, загін, real-time.
- **Осі варіацій:** правила героя (навички від вживання / класи і рівні); магія (руни / заучування / мана); карта (малювати самому / автокарта); бій (real-time / покроковий у GBA).

## Цікавинки для курсу
- Перенесення настільних правил (раса × клас × атрибути) у дані — 📎 (таблиці обмежень і модифікаторів).
- Заучування заклинань на привалі: слоти за рівнем, витрата при касті — 📎.
- Камʼяні ключі-портали: 7 типів ключа, кожен відкриває свій портал — 🌱.
- Загін 2×2: передній ряд бʼє впритул, задній — заклинання і дальня зброя — 📎.
- Плити, кнопки й ілюзорні стіни як «скриптовані» перемикачі рівня — 📎.
- Імпорт загону в наступну гру — 🥉 (серіалізація стану героїв між програмами).

## Мапа на каталог
- Є: `move-4dir` · `orientation-state` · `impassable-cells` · `key-and-door` · `button-toggle` (кнопки, плити) · `teleport-pair` (портали) · `hp-damage` · `inventory` · `inventory-items` · `inventory-limit` · `item-pickup` · `hunger-clock` · `status-effects` (отрута, параліч (?)) · `unit-xp-skills` · `melee-vs-ranged` · `projectile-shot` · `chase-player` · `stairs-levels` · `save-game` · `player-death` · `party-switch` (вибір героя для дії) · `character-select` · `drag-drop-piece` · `gui-render` · `player-camera`.
- **Нема** → пропозиції карток (частина вже з DM/Grimrock):
  - `+first-person-grid`, `+party-formation`, `+two-hand-slots`, `+pressure-plate` — як у DM/Grimrock.
  - `+rule-system-import` «Правила настільної RPG як дані» · game-logic/rules · 📎.
  - `+class-race-matrix` «Дозволені пари раса × клас, мультиклас» · entities/state · 📎.
  - `+spell-memorize-rest` «Заклинання заучуються на привалі, витрачаються на касті» · entities/state · 📎 · слоти {slots_per_level}.
  - `+camp-menu` «Табір: відпочинок, заучування, збереження» · interface/menus · 🌱.
  - `+stone-portal-keys` «Типізовані ключі до порталів-телепортів» · entities/interaction · 🌱.
  - `+party-import` «Перенесення загону в наступну гру» · persistence/save · 🥉.
  - `+npc-recruit` «NPC приєднується до загону» · entities/party · 📎.
  - `+illusory-wall` «Стіна, що проходиться» · entities/collision · 🌱.
  - `+level-special-quest` «Прихований квест рівня з бонусом досвіду» · levels/progression · 🌱.

## Пропозиції до словників
- `+trigger:rest(party)` — загін відпочиває (відновлення, заучування).
- `+cond:class(a, c)` — герой має клас (хто може касти, носити обладунок).
- `+effect:memorize(a, spell)` — заучити заклинання у слот.
- `+effect:recruit(npc)` — NPC стає членом загону.
- `+window:camp-menu` — меню табору; `+window:spell-book` — книга заклинань для касту.
- `+feature:party-import` — імпорт персонажів з іншої гри серії.
- `+card:spell-memorize-rest`, `+card:stone-portal-keys` — див. вище.

## Джерела
- ⭐ [Wikipedia: Eye of the Beholder](https://en.wikipedia.org/wiki/Eye_of_the_Beholder_(video_game)) — party-based кроулер від першої особи, схожий на Dungeon Master; 4 героїв → до 6 (NPC, оживлені скелети); point-and-click бій; імпорт загону в сиквели; промо з бонусом на кожному рівні.
- [Wikipedia DE](https://de.wikipedia.org/wiki/Eye_of_the_Beholder_(Computerspiel)) — 6 рас, 6 класів (Fighter, Thief, Mage, Cleric, Paladin, Ranger), 9 світоглядів, 6 атрибутів з правкою, real-time, заклинання після сну, їжа, 12 рівнів, 7 камʼяних ключів до порталів, без автокарти в DOS, порти.
- YouTube: пошук «eye of the beholder 1991 dos gameplay».

## Непевне
- (?) THAC0, AC і кидки на влучання — «правила AD&D» у джерелах без деталей; механіку кидка не перевірено.
- (?) Плити тиску, ілюзорні стіни, телепорти, ями — з памʼяті; відкриті джерела згадують лише камʼяні портали й секрети.
- (?) Мультиклас для напівлюдей, обмеження раса × клас.
- (?) Чи можна відпочивати поруч з ворогами; як оживлюються мертві герої.
- (?) Квести рівнів з бонусом досвіду — з памʼяті, підтверджено лише «бонусна знахідка» в промо.
- (?) Пункти головного меню й табору.
- (?) Фінальний бос Xanathar (beholder) і місто Waterdeep — з памʼяті; відкриті джерела боса не називають.
