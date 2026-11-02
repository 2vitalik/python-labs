---
title: Plants vs. Zombies (Рослини проти зомбі)
slug: plants-vs-zombies
family: tower-lanes
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: runtime
  goal: survive
year: 2009
platforms: [PC, Mac, iOS, Android, Xbox 360, PS3, DS, PS Vita, Windows Phone, BlackBerry 10]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Plants_vs._Zombies_(video_game)", best: true, note: "геймплей: смуги, сонце, газонокосарки, хвилі, режими"}
  - {kind: official, url: "https://www.ea.com/ea-studios/popcap/plants-vs-zombies"}
  - {kind: steam, url: "https://store.steampowered.com/app/3590/Plants_vs_Zombies_GOTY_Edition/", note: "GOTY Edition: 49 рослин, 26 зомбі, 50 рівнів Adventure, 5 режимів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=plants+vs+zombies+2009+gameplay", note: "пошук; геймплей"}
stage: v2
coverage: 70
mechanics: [round-currency, enemy-waves, enemy-reached-base, projectile-shot, shoot-forward, shoot-spread, shoot-cooldown, blast-wave, hp-damage, temporary-modes, speed-per-type, melee-vs-ranged, spawn-schedule, spawn-points, item-pickup, shop-between-levels, shop-catalog, sequential-levels, game-pause, +lane-grid, +placement-cooldown, +loadout-select, +last-line-defense, +upgrade-on-top, +seed-conveyor]
proposes: ["+trigger:lane_enter", "+cond:lane_has", "+effect:jump_over", "+effect:steal", "+effect:lane_clear", "+role:lane", "+window:loadout-select", "+window:garden-window", "+ui:seed-bar", "+ui:wave-progress-flags", "+ui:shovel", "+feature:minigames", "+feature:loadout", "+card:lane-grid", "+card:placement-cooldown"]
author: opus
date: 2026-11-02
---

# Plants vs. Zombies — смуговий tower defense: висаджуй рослини за сонце, тримай 5 рядів проти зомбі

## Суть
Гравець «рукою» садить рослини на газон 5×9 (басейн/туман — 6×9), платячи сонцем, яке падає з неба або виробляють соняшники. Зомбі йдуть справа наліво кожен **своєю смугою** й їдять рослини на шляху; рослина бʼє лише свою смугу (або сусідні, якщо має особливий патерн). Ядро — економіка «сонце → виробники → стрілки» + підбір 6–10 насінин перед рівнем під відомий склад зомбі. Незвичне: смуга як головна одиниця простору, газонокосарка — разова «остання лінія» кожної смуги.

## Поле і час
- Газон — сітка 5 рядів × 9 колонок (день, ніч, дах); «задній двір» (басейн, туман) — 6 рядів, з них два середні (3–4) — вода (садити лише на Lily Pad або водні рослини).
- Ліворуч — будинок і газонокосарки (по одній на ряд; у басейні — pool cleaner, на даху — roof cleaner); праворуч за краєм — точка входу зомбі.
- Варіанти поля: **день** (сонце падає з неба) · **ніч** (сонця з неба нема, гриби дешевші й не сплять, з землі ростуть надгробки, з яких лізуть зомбі) · **басейн** · **туман** (праві колонки закриті, видно лише при Plantern/Blover/спалахах) · **дах** (похилий: прямі стрілки бʼють об схил, потрібні катапульти; садити лише в Flower Pot).
- Real-time: тік — кадр, рослини стріляють своїм періодом, зомбі мають власну швидкість. Рівень = послідовність хвиль; прогрес-бар із прапорцями, перед прапорцем — «великий наступ».
- Камера статична; перед рівнем — проїзд праворуч, де видно склад зомбі (вибір насіння).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Курсор-рука | — | вибрана насінина / лопата | садить, збирає сонце й монети, викопує |
| Сонце | resource | 25 (мале 15) | падає з неба (день) або від виробника; клік → +сонце; зникає за часом |
| Монета (срібна/золота/діамант) | pickup | 10 / 50 / 1000 (?) | випадає зі зомбі; клік → гроші для крамниці |
| Газонокосарка | static | 1 на ряд, разова | зомбі дійшов до будинку → їде вздовж ряду, знищує всіх зомбі в ряду, зникає |
| Надгробок | spawner | ніч | з нього вилазять зомбі у фінальній хвилі; Grave Buster зʼїдає |
| Peashooter | ally | 100 сонця | раз на ~1.4 с горошина вперед по своєму ряду |
| Repeater · Gatling Pea | ally | 200 · апгрейд | 2 · 4 горошини за постріл |
| Snow Pea | ally | 175 | горошина + сповільнення цілі |
| Threepeater | ally | 325 | стріляє у свій і два сусідні ряди |
| Split Pea | ally | 125 | вперед і назад (проти Digger) |
| Starfruit | ally | 125 | 5 зірок у 5 напрямках (точний набір — див. «Непевне») |
| Cactus · Cattail | ally | 125 · апгрейд на Lily Pad | збиває кулі Balloon; Cattail — самонавідні шипи по всьому полю |
| Puff-shroom · Scaredy-shroom | ally | 0 · 25, гриби | Puff — короткий радіус 3 клітини; Scaredy ховається, коли зомбі поруч |
| Fume-shroom · Gloom-shroom | ally | 75 · апгрейд | пробивний дим на 4 клітини (крізь щит); Gloom — довкола 3×3 |
| Kernel/Cabbage/Melon-pult · Winter Melon | ally | 100–300 | навісний постріл (через щит, на даху); кукурудза — масло стопорить; кавун — сплеск по сусідах |
| Cob Cannon | ally | апгрейд на 2 Kernel-pult, 2 клітини | клік → клік по полю: ракета в будь-яку точку, довге перезаряджання |
| Torchwood | ally | 175 | горошина, що пролітає крізь, стає вогняною (×2 шкода); снігову — розморожує |
| Sunflower · Twin Sunflower | ally | 50 · апгрейд 150 | виробник: 25 · 50 сонця раз на ~24 с |
| Sun-shroom | ally | 25, гриб | спершу мале сонце 15, згодом 25 |
| Sea-shroom | ally | 0, гриб, вода | як Puff-shroom, але садиться на воду без Lily Pad (?) |
| Marigold · Gold Magnet | ally | 50 · апгрейд | виробляє монети · притягує монети |
| Wall-nut · Tall-nut | ally | 50 · 125 | блокер з великим HP; Tall-nut ще й не дає перестрибнути |
| Pumpkin | ally | 125 | оболонка поверх іншої рослини: зомбі їсть спершу її |
| Spikeweed · Spikerock | ally | 100 · апгрейд | на землі, не їдять; шкодить усім, хто проходить; пробиває Zomboni |
| Cherry Bomb · Jalapeno | ally | 150 · 125, миттєві | вибух 3×3 · вогонь по всьому ряду |
| Potato Mine | ally | 25 | ~15 с озброюється, потім вибух при контакті |
| Squash · Chomper | ally | 50 · 150 | розчавлює сусіднього · ковтає одного і довго жує |
| Ice-shroom · Doom-shroom | ally | 75 · 125, гриби | заморожує всіх на полі · великий вибух, лишає кратер (не садити) |
| Tangle Kelp | ally | 25, вода | тягне першого зомбі під воду |
| Hypno-shroom | ally | 75, гриб | хто зʼїв — переходить на бік рослин і йде назад |
| Magnet-shroom | ally | 100, гриб | забирає метал: відро, шолом, двері, кирку, драбину, джек-ін-бокс |
| Garlic | ally | 50 | хто вкусив — переходить у сусідній ряд |
| Umbrella Leaf | ally | 100 | захищає сусідні рослини від Bungee і катапульт |
| Plantern · Blover | ally | 25 · 100 | освітлює туман довкола · здуває туман і всі кулі Balloon |
| Lily Pad · Flower Pot | ally | 25 | основа: дозволяє садити на воді / на даху |
| Coffee Bean | ally | 75 | будить гриб удень |
| Grave Buster | ally | 75 | зʼїдає надгробок |
| Imitater | ally | вартість копії | копіює іншу насінину (дві однакові в наборі) |
| Zombie · Flag Zombie | enemy | базове HP (?≈10 горошин) | іде вліво, їсть рослину перед собою; Flag — вістун великої хвилі |
| Conehead · Buckethead | enemy | броня-конус · відро | броня поглинає шкоду; відро — метал (Magnet) |
| Pole Vaulting | enemy | швидкий | перестрибує першу рослину одноразово (Tall-nut зупиняє), далі повільний |
| Newspaper | enemy | газета-щит | газету знищено → лютує, прискорюється |
| Screen Door | enemy | двері-щит | прямі постріли поглинає щит; навісні й дим — ні |
| Football | enemy | шолом (метал), швидкий | дуже міцний і швидкий |
| Dancing · Backup Dancer | enemy · spawner | — | кличе 4 танцюристів на сусідні клітини (зверху, знизу, спереду, ззаду) |
| Ducky Tube · Snorkel · Dolphin Rider | enemy | вода | Snorkel пірнає — прямі постріли пролітають; Dolphin перестрибує першу рослину |
| Zomboni | enemy | машина | розчавлює рослини, лишає льодовий слід (садити не можна); Spikeweed пробиває |
| Zombie Bobsled Team | enemy | 4 зомбі | їде лише по льодовому сліду |
| Jack-in-the-Box | enemy | — | випадково вибухає, знищуючи рослини 3×3 |
| Balloon | enemy | летить | пролітає над рослинами; Cactus/Cattail/Blover збивають кулю |
| Digger | enemy | кирка | риє під землею до будинку, вилазить у 1-й колонці й іде **праворуч** |
| Pogo | enemy | жердина | стрибає через кожну рослину; Tall-nut/Magnet зупиняє |
| Bungee | enemy | з неба | падає на клітину, після паузи краде рослину |
| Ladder | enemy | драбина | ставить драбину на блокер — інші зомбі перелазять |
| Catapult | enemy | дах | закидає баскетбольні мʼячі на рослини ззаду ряду |
| Gargantuar · Imp | enemy | дуже багато HP | розбиває рослину одним ударом; на половині HP кидає Imp-а вглиб поля |
| Zombie Yeti | enemy | рідкісний | іде і, якщо вижив, тікає назад (?) |
| Dr. Zomboss | boss | Zombot | фінал: спавнить зомбі, давить рослини, кидає вогняні/крижані кулі (Ice-shroom/Jalapeno гасять) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `timer(sky_sun)` → ЯКЩО `mode(day)` → ТО `spawn_at(sun, random_col)`; сонце падає і лежить, доки `timed-despawn`.
- КОЛИ `timer(producer.period)` → ТО `spawn_at(sun, near(producer))`; Marigold — `spawn_at(coin)`.
- КОЛИ `input(click, sun|coin)` → ТО `currency(+value)` / `pickup`.
- КОЛИ `input(place, seed, cell)` → ЯКЩО `has(sun, cost)` and `free(cell)` and `custom: «насінина відкатилась»` and `cell(x, suitable)` → ТО `spawn(plant)`, `currency(-cost)`, `custom: «запустити відкат насінини (fast 7.5 с / slow 30 с / very slow 50 с)»`.
- КОЛИ `input(place, upgrade, cell)` → ЯКЩО `occupied(cell, base_plant)` → ТО `transform(upgrade_plant)` (Gatling на Repeater, Twin на Sunflower, Cob Cannon на дві Kernel-pult).
- КОЛИ `input(shovel, cell)` → ТО `disappear_b` (без повернення сонця).
- КОЛИ `timer(plant.fire_rate)` → ЯКЩО `custom: «lane_has(zombie, ahead)»` → ТО `spawn(projectile)` за патерном рослини (вперед / 3 ряди / назад / 5 напрямків / навісом).
- КОЛИ `contact(pea, zombie)` → ТО `damage(n)`, `disappear_a`; снігова — `speed(zombie, ×0.5, duration)`; КОЛИ `contact(pea, torchwood)` → ТО `transform(fire_pea)`.
- КОЛИ `adjacent(zombie, plant)` → ТО `custom: «зомбі зупиняється і їсть: damage щотік»`; КОЛИ `hp_zero(plant)` → ТО `disappear_b`, зомбі йде далі.
- КОЛИ `hp_zero(armor)` → ТО `transform(zombie_without_armor)`; Newspaper — `speed(×k)`.
- КОЛИ `contact(pole_vaulter, first_plant)` → ЯКЩО `not occupied(cell, tall_nut)` → ТО `custom: «effect jump_over»`, `set_state(no_pole)`.
- КОЛИ `contact(magnet_range, metal_item)` → ТО `take(zombie, metal_item)`.
- КОЛИ `spawned(dancing)` / `timer` → ТО `spawn_at(backup_dancer, 4 neighbours)`.
- КОЛИ `enter(zomboni, cell)` → ТО `disappear_b` (рослина), `set_cell(ice)`; КОЛИ `contact(zomboni, spikeweed)` → ТО `disappear_a`.
- КОЛИ `reach(digger, col_1)` → ТО `face(digger, right)`, виходить з-під землі.
- КОЛИ `custom: «HP Gargantuar < 50%»` → ТО `spawn_at(imp, back_of_field)` одноразово.
- КОЛИ `timer(bungee_delay)` → ЯКЩО `not adjacent(umbrella_leaf)` → ТО `custom: «effect steal(plant)»`.
- КОЛИ `contact(zombie, hypno_shroom)` → ТО `set_side(zombie, plants)`, `face(reverse)`.
- КОЛИ `contact(zombie, garlic)` → ТО `move(zombie, adjacent_lane)`.
- КОЛИ `reach(zombie, house_col)` → ЯКЩО `has(lane, mower)` → ТО `custom: «effect lane_clear»`, `take(lane, mower)`; інакше `lose` («THE ZOMBIES ATE YOUR BRAINS!» (?)), рівень перезапускається.
- КОЛИ `schedule(waves)` → ТО `spawn_at(zombies, right_edge, random_lane)`, хвилі щільнішають; КОЛИ `wave_start(flag)` (великий наступ із Flag Zombie — у кінці рівня й часто посередині) → ТО `message(«A huge wave of zombies is approaching!» (?))`; останній — «FINAL WAVE» (?).
- КОЛИ `all_gone(zombie)` and `custom: «остання хвиля вийшла»` → ТО `win`, `spawn(reward)` (нова насінина/лист/гроші), `next_level`.
- Ніч: `wave_start(final)` → `spawn_at(zombie, gravestones)`; гриби вдень — `set_state(sleep)` доки Coffee Bean.
- Туман: `custom: «колонки 6–9 приховані; Plantern reveal(radius), Blover reveal(all, n с)»`.
- Перемога: пережити всі хвилі рівня · Поразка: зомбі увійшов у будинок у смузі без косарки · Рахунок: нема очок; гроші накопичуються для крамниці; у Survival — кількість прапорців.

## Керування і ввід
- Тільки миша (тач на мобільних): клік по насінині в `seed-bar` → клік по клітині = посадити; перетягування теж працює (?).
- Клік по сонцю/монеті — збирання (на мобільних — тап); лопата — викопати.
- Cob Cannon — двокроковий ввід: клік по гарматі → клік по цілі.
- Перед рівнем — вибір насінин у слоти (6, докуповуються до 10) із сітки відкритих рослин.
- Пауза — кнопка Menu або втрата фокусу вікна.

## Вікна, меню, HUD
- `splash-screen` — PopCap; «завантаження» з дорогою-повзунком.
- `main-menu` — надгробок: Adventure · Mini-games · Puzzle · Survival; Zen Garden · Almanac · Store; Options · Help · Quit (розклад пунктів — з памʼяті (?)).
- `custom-window` «Choose Your Seeds» (`+window:loadout-select`): сітка відкритих рослин, слоти набору, праворуч — газон зі складом зомбі цього рівня («Let's Rock!»).
- `game-screen`: газон, `seed-bar` угорі (лічильник сонця + насінини з ціною й затемненням-відкатом), лопата, кнопка Menu, `wave-counter` у вигляді прогрес-бару з прапорцями внизу праворуч, назва рівня.
- `codex-window` «Suburban Almanac» — дві сторінки: рослини (ціна, відкат, шкода, опис) і зомбі (міцність, швидкість, особливість).
- `shop-window` Crazy Dave's Twiddydinkies (відкривається після 3-4) — слоти насіння, апгрейд-рослини, граблі, косарки для басейну/даху, Imitater, товари для саду.
- `custom-window` Zen Garden (`+window:garden-window`, після 5-4): горщики, лійка, добриво, спрей від жуків, програвач; підвиди — гриб-сад, акваріум, Дерево мудрості.
- `pause-menu` — Resume, Restart, Main Menu, Almanac (?), налаштування гучності.
- `settings-window` — музика, звук, 3D-прискорення, повний екран.
- `end-screen` — нагорода (нова насінина, записка) → «Next level»; поразка — «The zombies ate your brains!» → Try again / Main Menu.
- `level-select` для міні-ігор/Puzzle/Survival: сітка рівнів з трофеями.
- Переходи: main-menu → (Adventure) loadout → game-screen → end-screen → наступний loadout; main-menu → Almanac/Store/Zen Garden і назад.

## Фічі поза полем
- `levels-sequential` 5 світів × 10 рівнів (день, ніч, басейн, туман, дах; останній рівень даху — нічний, бос Dr. Zomboss); рівень 5 — міні-гра/конвеєр, рівень 10 — конвеєр насінин замість сонця (`+seed-conveyor`).
- `unlockables`: кожен рівень відкриває рослину; після Adventure — режими Mini-games (20), Puzzle (Vasebreaker, I, Zombie), Survival (normal/hard/endless (?)); повторне Adventure з трьома випадковими стартовими рослинами.
- `shop-window` + гроші з монет — `meta-progression` (слоти насіння, апгрейди, граблі — разова пастка на першого зомбі).
- `codex` (Almanac) — довідник усіх сутностей у грі.
- Zen Garden — пасивна мініферма: рослини просять воду/добриво/музику, щасливі — дають монети; Stinky the Snail збирає монети.
- `save-progress`, `autosave` посеред рівня (?), `pause`, `volume-sliders`, `fullscreen`, `achievements` (GOTY).
- Міні-ігри як `custom-rules` над тим самим двіжком: Wall-nut Bowling (горіхи котяться і рикошетять між рядами), Whack a Zombie, Beghouled (match-3 рослинами), Zombiquarium, Slot Machine, It's Raining Seeds, Invisi-ghoul, Portal Combat, Last Stand (фіксоване сонце, кілька підходів).
- Puzzle: **Vasebreaker** (вази з рослиною/зомбі; розбий усі і переможи всіх) · **I, Zombie** (ролі навпаки: купуєш зомбі за сонце й ставиш праворуч проти розставлених рослин; мета — зʼїсти мозок у кожному ряду).

## Варіації й родичі
- Сиквели: Plants vs. Zombies 2 (світи-епохи, Plant Food — разовий супер-ефект), Heroes (карткова), Garden Warfare (шутер).
- Родичі «смугових» TD: Kingdom Rush (шлях, не смуги), Fieldrunners (лабіринт), Inscryption (смуги як колонки карт), Defenders of the Kingdom; аркадна предтеча — Space Invaders-смуги.
- **Осі варіацій**: простір ворога — смуга / шлях / вільний лабіринт · звідки ресурс — небо+виробники / вбивства / хвиля · подача юнітів — вибір набору / конвеєр / випадкова ваза · остання лінія — косарка / життя / HP бази · ролі: оборона / атака (I, Zombie).

## Цікавинки для курсу
- Смугова модель: кожен зомбі й снаряд знають свій ряд, колізії лише в межах ряду — 🥉 (просте поле, багато сутностей).
- Насінини з відкатом і ціною + сонце від виробників — 🥉 (таймери, економіка, ввід «вибрав → поставив»).
- Таблиця «зомбі × рослина» з винятками (Pole Vault ↔ Tall-nut, Balloon ↔ Cactus, Digger ↔ Split Pea, метал ↔ Magnet) — 🥈 (`interaction-table` як дані).
- Апгрейд «поверх базової рослини» і Cob Cannon на 2 клітини — 📎 + 🥉.
- Газонокосарка: разова очистка ряду як «друге життя смуги» — 🌱.
- I, Zombie — той самий двіжок з інверсією ролей — 🥈 (архітектурна перевірка `logic-render-split`).
- Wall-nut Bowling: рикошет між рядами — 📎.

## Мапа на каталог
- Є: `round-currency` ↔ сонце · `enemy-waves` + `spawn-schedule` ↔ хвилі з прапорцями · `enemy-reached-base` ↔ зомбі в будинку · `projectile-shot` + `shoot-forward` / `shoot-spread` (Threepeater, Starfruit) / `shoot-cooldown` · `blast-wave` (Cherry Bomb, Jalapeno як ряд) · `hp-damage` ↔ HP рослин і броня · `temporary-modes` ↔ сповільнення/заморожування/сон грибів · `speed-per-type` · `melee-vs-ranged` ↔ хто чим бʼється · `spawn-points` ↔ надгробки · `item-pickup` ↔ сонце/монети · `shop-between-levels` + `shop-catalog` ↔ Crazy Dave · `goal-counter` ↔ прогрес хвиль · `sequential-levels` · `level-select` · `save-progress` · `game-pause` · `volume-control`.
- **Нема** → пропозиції карток:
  - `+lane-grid` «Смугове поле» · entities/legality · 🥉 · слот {lanes: n} — ворог і снаряди живуть у ряду.
  - `+placement-cooldown` «Відкат розміщення юніта» · game-logic/economy · 📎 · слот {cooldown: s}.
  - `+loadout-select` «Вибір набору перед рівнем» · interface/menus (#window) · 🥉 · слот {slots: n}.
  - `+last-line-defense` «Разова очистка смуги» · game-logic/lose · 🌱.
  - `+upgrade-on-top` «Апгрейд поверх юніта» · game-logic/economy · 📎.
  - `+seed-conveyor` «Конвеєр юнітів замість ресурсу» · game-logic/economy · 📎.

## Пропозиції до словників
- `+trigger:lane_enter` — сутність увійшла в смугу/ряд (зомбі в ряд — рослини ряду активуються).
- `+cond:lane_has` — у смузі попереду є сутність виду (рослина стріляє, лише якщо в ряду є зомбі).
- `+effect:jump_over` — перестрибнути першу перешкоду (Pole Vault, Dolphin, Pogo).
- `+effect:steal` — забрати сутність з поля (Bungee краде рослину).
- `+effect:lane_clear` — знищити всіх ворогів у смузі (газонокосарка, Jalapeno).
- `+role:lane` — смуга як сутність зі станом (косарка є/нема, вода/земля/лід).
- `+window:loadout-select` — вибір набору юнітів перед рівнем із превʼю ворогів.
- Вжито наявний `codex-window`: Almanac — еталон (сторінки рослин і зомбі зі статами).
- `+window:garden-window` — пасивна мініферма між рівнями (Zen Garden).
- `+ui:seed-bar` — панель юнітів з ціною й затемненням-відкатом; `+ui:wave-progress-flags` — прогрес хвиль з прапорцями великих наступів; `+ui:shovel` — інструмент видалення свого юніта.
- `+feature:minigames` — набір варіантів правил над тим самим двіжком; `+feature:loadout` — обмежений набір інструментів на рівень.
- `+card:lane-grid`, `+card:placement-cooldown` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Plants vs. Zombies](https://en.wikipedia.org/wiki/Plants_vs._Zombies_(video_game)) — смуги 5/6, сонце, відкат, косарки, хвилі й прапорці, 5×10 рівнів Adventure, 20 міні-ігор, Vasebreaker, I Zombie, Survival, Almanac, Zen Garden, Dr. Zomboss, 49 рослин / 26 зомбі, платформи з датами.
- [EA: Plants vs. Zombies](https://www.ea.com/ea-studios/popcap/plants-vs-zombies) — офіційна сторінка серії.
- [Steam: PvZ GOTY Edition](https://store.steampowered.com/app/3590/Plants_vs_Zombies_GOTY_Edition/) — актуальна PC-версія, 49 рослин, 26 зомбі, 5 режимів.
- YouTube: пошук «plants vs zombies 2009 gameplay».

## Непевне
- (?) Ціни й відкати рослин, HP зомбі, номінал сонця (25/15), період сонця (~24 с), постріл Peashooter (~1.4 с), озброєння Potato Mine (~15 с) — з памʼяті; Wikipedia їх не дає, фан-вікі (fandom) віддає 402.
- (?) Поведінка рослин і зомбі, яких Wikipedia не називає (Digger, Zomboni, Gargantuar/Imp, Yeti, Coffee Bean, сон грибів удень, Sea-shroom), — з памʼяті; перелік 49/26 звірено з Wikipedia і Steam.
- (?) Напрямки Starfruit: імовірно назад, вгору, вниз і дві діагоналі вперед (без прямо вперед) — не звірено.
- (?) Тексти «THE ZOMBIES ATE YOUR BRAINS!», «A huge wave…», «FINAL WAVE» — з памʼяті; Wikipedia каже лише, що рівень перезапускається.
- (?) Номінали монет (10/50/1000) і поведінка Zombie Yeti.
- (?) Чи можна садити перетягуванням у PC-версії; чи є Almanac у меню паузи.
- (?) Точне число стартових слотів (6) і максимум після крамниці (10).
