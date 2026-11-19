---
title: ilomilo
slug: ilomilo
aka: [ilomilo plus, "ilomilo: Autumn Tale"]
family: thinky
also: []
klass: avatar
axes:
  field: 3d
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2010
platforms: [Windows Phone 7, Xbox 360 (XBLA), Windows 8 (ilomilo plus), Xbox One (BC)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Ilomilo", best: true, note: "мета — звести Іло й Міло, 49 рівнів, перемикання, кубики-мости, провал на інший бік, килимки, перемикачі, safka й спогади, кооператив із вказівником"}
  - {kind: other, url: "https://www.pocketgamer.com/ilomilo/review/", note: "рецензія WP7: килимки повертають на 90° поверхнею фігури, висувний кубик на 3 клітини, без падінь і стрибків, свиня й jack-in-the-box"}
  - {kind: other, url: "https://www.hookedgamers.com/x360/ilomilo/review/article-658-2.html", note: "кубики-рюкзаки з «характером»: ліфт, міст, люк; істота-блокатор; яблука й свиня; safka, спогади, фото й платівки"}
  - {kind: other, url: "https://www.engadget.com/2011-01-05-ilomilo-review-thumbs-upside-down.html", note: "люк на протилежний бік кубика, кубик, що котиться, передача предметів між героями"}
  - {kind: other, url: "https://kotaku.com/review-ilomilos-surprising-depth-is-a-matter-of-percep-5727987", note: "49 рівнів у 4 главах, блоки, що повертаються, герої на різних боках, кооператив із мухою-вказівником"}
  - {kind: other, url: "https://gamerant.com/ilomilo-reviews/", note: "B — перемикання, кубики-ліфти, мапа глави 3×4, по три safka"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=ilomilo+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [party-switch, move-4dir, button-toggle, carrier-platform, world-map, level-unlock, level-select, item-pickup, leaderboard, movement-animation, background-music, +meet-partner, +carry-one-block, +place-bridge, +extending-bridge, +surface-walk, +trapdoor-flip, +pass-item-to-partner, +blocker-creature, +eater-clears-obstacle, +local-coop, +collectible-unlocks-bonus]
proposes: ["+effect:set_gravity", "+cond:surface_of", "+ui:helper-pointer", "+window:gallery", "+card:meet-partner", "+card:trapdoor-flip", "+card:extending-bridge", "+card:pass-item-to-partner"]
author: opus
date: 2026-11-19
---

# ilomilo — двоє друзів на різних кінцях кубічного лабіринту: переносиш кубики, доки вони не зустрінуться

## Суть
3D-головоломка SouthEnd Interactive і Microsoft: Іло (червоний) і Міло (синій) починають у різних місцях конструкції з кубиків 1×1 і мають зустрітися лицем до лиця. Гравець перемикається між ними; кожен уміє лише ходити кубиками, брати один переносний кубик «рюкзаком» і ставити його, а поставлений кубик виконує свою дію: латає розрив, висувається мостом, їздить ліфтом, провалює героя на протилежний бік. Килимки дають перейти на бічну чи нижню грань, тож герої часто ходять різними боками й «догори ногами»; падінь, стрибків і смерті нема — лише маршрут і порядок дій.

## Поле і час
- Рівень — 3D-конструкція з кубиків 1×1 (доріжки й споруди), що висить у просторі; ходять по гранях кубиків. З країв не падають і не стрибають (Pocket Gamer).
- «Низ» у кожного героя свій: килимок переводить на перпендикулярну грань, люк — на протилежний бік; Іло й Міло можуть бути на зовсім різних боках (Kotaku).
- Камера показує конструкцію під кутом, із зумом; крива геометрія часто заслоняє героїв (Game Rant).
- Час: світ змінюється лише від дій активного героя (`time: turn`); таймера й поразки нема.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Іло (червоний) | player | активний / ні, свій «низ» | ходить гранями кубиків; бере й ставить один кубик; неактивний стоїть |
| Міло (синій) | player | те саме | те саме |
| Кубик доріжки | static | — | поверхня ходу |
| Простий переносний кубик | object | — | узятий — «рюкзак» на спині; поставлений у розрив стає доріжкою |
| Висувний кубик | object | довжина 3 | поставлений висувається на три клітини, утворюючи міст |
| Кубик-ліфт | platform | — | поставлений їздить угору-вниз (?), везе героя |
| Кубик-люк (trap door) | object | — | один із «характерів» переносних кубиків (Hooked Gamers) (?); герой, що став на нього, провалюється крізь кубик на протилежний бік конструкції |
| Килимок (червоний) | terrain | — | дозволяє перейти через ребро на сусідню грань (поворот на 90°) |
| Кубик, що котиться | object | — | відпущений котиться рівнем (Engadget); правила — (?) |
| Блоки, що повертаються | object | кут | «ratchet-like blocks that twist» (Kotaku); правила — (?) |
| Перемикач | switch | → міст | вмикає міст |
| Істота-блокатор | neutral | — | перекриває шлях, з якої б грані не підійти |
| Яблуко | static | — | перекриває шлях; його зʼїдає свиня |
| Свиня | neutral | — | зʼїдає яблуко, якщо змусити її пройти повз |
| Jack-in-the-box | static | — | кубик-перешкода (Pocket Gamer); поведінка — (?) |
| Safka | pickup | 3 на рівень | малюки-істоти; відкривають бонусні рівні |
| Уламок спогаду | pickup | — | заповнює шкалу; 4 повні шкали за главу — цілий спогад-листівка |
| Фото / платівка | pickup | — | відкривають картинки й пісні галереї |
| Яйце | pickup | — | лише в мультиплеєрі |

## Правила (КОЛИ → ЯКЩО → ТО)
Хода й перемикання:
- КОЛИ `input(dir)` → ЯКЩО `custom: «попереду кубик доріжки, гранню до героя»` and `not occupied(next_cell, creature)` → ТО `move(active, dir)`; інакше `block` — з краю не падають.
- КОЛИ `input(switch)` → ТО `custom: «активним стає інший герой»`.
- КОЛИ `input(action)` → ЯКЩО `occupied(next_cell, cube)` and `not has(active, cube)` → ТО `pickup(active, cube)` — кубик стає рюкзаком.
- КОЛИ `input(action)` → ЯКЩО `has(active, cube)` and `free(next_cell)` → ТО `place(active, cube)`; кубик виконує дію свого типу.
- КОЛИ `input(action)` → ЯКЩО `custom: «другий герой поруч»` and `has(active, cube)` → ТО `give(partner, cube)`, `take(active, cube)` (Engadget: «when proximity allows»).

Кубики й килимки:
- КОЛИ `custom: «простий кубик поставлено в розрив»` → ТО `set_cell(gap, path)` — по ньому можна йти.
- КОЛИ `custom: «поставлено висувний кубик»` → ТО `grow(extender, 3)` — міст на три клітини вперед.
- КОЛИ `custom: «поставлено кубик-ліфт»` → ТО `custom: «їздить угору-вниз»`.
- КОЛИ `enter(active, lift)` → ТО `carry(lift, active)` (?).
- КОЛИ `enter(active, trapdoor)` → ТО `custom: «провалитися крізь кубик на протилежну грань, низ перевертається»`.
- КОЛИ `enter(active, carpet)` → ЯКЩО `custom: «попереду ребро кубика»` → ТО `custom: «перейти на сусідню грань, низ повертається на 90°»`.
- КОЛИ `enter(active, switch)` → ТО `set_state(bridge, on)`.

Істоти:
- КОЛИ `contact(active, blocker)` → ТО `block` — з будь-якої грані (Hooked Gamers).
- КОЛИ `contact(active, apple)` → ТО `block`.
- КОЛИ `contact(pig, apple)` → ТО `disappear(apple)` — свиню треба змусити пройти повз.

Збирання й мета:
- КОЛИ `contact(active, safka)` → ТО `pickup(active, safka)`, `counter(safkas, +1)`.
- КОЛИ `counter(safkas, ==, 3)` → ТО `unlock(bonus_level)` (?).
- КОЛИ `contact(active, memory_shard)` → ТО `counter(memory, +1)`; чотири повні шкали за главу — `unlock(memory_postcard)`.
- КОЛИ `adjacent(ilo, milo)` → ЯКЩО `facing(ilo, toward_milo)` and `facing(milo, toward_ilo)` → ТО `win`, `custom: «танець героїв і оркестр двох істот»`, `next_level`.
- Перемога: Іло й Міло зустрілись лицем до лиця (Kotaku). · Поразки нема: «no way of killing», нерозвʼязних позицій нема (Pocket Gamer). · Рахунок: нема; є таблиці друзів XBL (WP7) — що в них рахується, (?).

## Керування і ввід
- Стик — хода активного героя; кнопка дії — взяти / поставити кубик.
- B — перемкнути героя (Game Rant); за Engadget B ще дає помахати й побачити, де другий (?).
- Кооператив: кожен гравець — свій герой, активний лише один; другий тим часом водить муху-вказівник, показуючи маршрут і предмети (Wikipedia, Kotaku).
- Windows Phone — тач (?).

## Вікна, меню, HUD
- `chapter-select` / `map-window`: глава — квадрат 3×4 рівнів; рівень відкривається, коли пройдено сусідній (Game Rant).
- `game-screen`: конструкція, обидва герої, кубик-рюкзак на спині активного; HUD — лічильники safka й спогадів (?).
- `custom-window` галерея: фото, концепт-арт, платівки-пісні, листи друзів, спогади-листівки.
- `end-screen`: танець героїв і оркестр із двох істот (барабан і туба).
- Міні-гра «ilomilo shuffle» у стилі NES — `custom-window`, що відкривається.
- Переходи: chapter-select → game-screen → (зустріч) end-screen → chapter-select (сусідні рівні відкрито).

## Фічі поза полем
- `world-map` по главах (3×4) + `level-unlock` сусідством; 49 рівнів у 4 главах (Wikipedia, Kotaku).
- `collectibles`: safka (по 3), уламки спогадів, фото, платівки; `unlockables`: бонусні рівні (частина байки Себастьяна, кросовери з іншими іграми, переодягнені рівні), галерея, міні-гра.
- `mode-coop` / `local-multiplayer`: двоє, кожен — свій герой; яйця — лише в мультиплеєрі.
- `leaderboard-online`: таблиці друзів XBL (WP7, Pocket Gamer).
- DLC Autumn Tale (Xbox 360, 2011); ilomilo plus (Windows 8, 2012) — набори «berry story» і «playroom escapade», 6 нових треків.
- Undo — (?); нерозвʼязних позицій нема, тож він і не потрібен.

## Варіації й родичі
- Версії: WP7 (32 рівні + 6 бонусних, 3 глави — Pocket Gamer), XBLA (49 рівнів, 4 глави), Windows 8 «plus».
- У корпусі: `games/grid-platformer/kula-world.md` (за ребром блока гравітація повертається на 90°), `games/thinky/orakyubu.md` (Sokoban на гранях кубів), `games/thinky/english-country-tune.md` (аватар прилипає до будь-якої грані), `games/grid-platformer/captain-toad-treasure-tracker.md` (кубічні діорами, герой не стрибає), `games/thinky/toodee-and-topdee.md` (двоє героїв з перемиканням), `games/grid-platformer/block-dude.md` (несе один блок).
- **Осі варіацій:** мета кількох аватарів — зустрітися (ilomilo) / усім вийти (Kwirk) / кожному на свою ціль; що робить поставлений блок — латає / висувається мостом / ліфт / люк; гравітація — одна на всіх / своя в героя, міняється килимком і люком; кооп — одночасний / по черзі з вказівником.

## Цікавинки для курсу
- Мета «зустрітися лицем до лиця»: перевірка сусідства й орієнтації двох аватарів — 🌱.
- Два аватари з перемиканням і передачею предмета між ними — 📎.
- Кубик-рюкзак з «характером»: одна дія «поставити» запускає різну поведінку за типом (латка / міст на 3 / ліфт / люк) — 🥉.
- Хода гранями кубиків: свій «низ» у кожного героя, перехід через ребро килимком — 🥈.
- Люк: провал крізь конструкцію на протилежну грань (пошук першої клітини вздовж осі + переворот низу) — 📎.
- Мапа глави 3×4 з відкриттям сусідніх рівнів — 📎.

## Мапа на каталог
- Є: `party-switch` ↔ Іло / Міло кнопкою; `move-4dir` ↔ хода гранями; `button-toggle` ↔ перемикач мосту; `carrier-platform` ↔ кубик-ліфт (?); `world-map` + `level-unlock` + `level-select` ↔ мапа глави 3×4; `item-pickup` ↔ safka, спогади, платівки; `leaderboard` ↔ таблиці друзів XBL; `movement-animation`; `background-music` ↔ платівки-пісні.
- **Нема** → пропозиції карток:
  - `+meet-partner` «Перемога, коли два аватари зустрілись» · game-logic/win · 🌱 · слот {facing: bool}.
  - `+carry-one-block` (уже в корпусі: Block Dude) — кубик-рюкзак.
  - `+place-bridge` (уже в корпусі: Lemmings, Toki Tori) — кубик у розрив.
  - `+extending-bridge` «Поставлений блок висувається мостом на N» · entities/interact · 📎 · слот {n: 3}.
  - `+surface-walk` (уже в корпусі: English Country Tune) — килимки.
  - `+trapdoor-flip` «Люк: провал на протилежний бік конструкції» · entities/move · 📎.
  - `+pass-item-to-partner` «Передати предмет іншому аватару поруч» · entities/interact · 🌱.
  - `+blocker-creature` «Істота, що лише перекриває шлях» · entities/legality · 🌱.
  - `+eater-clears-obstacle` «Істота зʼїдає перешкоду, якщо її провести повз» · entities/interact · 📎 (?).
  - `+local-coop` (уже в корпусі) — тут по черзі, з вказівником.
  - `+collectible-unlocks-bonus` «Зібрані скарби відкривають бонусні рівні» · levels/progress · 🌱.

## Пропозиції до словників
- `+effect:set_gravity` — змінити «низ» окремої сутності: килимок — на 90°, люк — на 180° (уже пропонував English Country Tune).
- `+cond:surface_of` — на якій грані стоїть сутність (уже пропонував English Country Tune).
- `+ui:helper-pointer` — вказівник другого гравця, що показує маршрут (муха в ilomilo).
- `+window:gallery` — галерея відкритих картинок, пісень і листів.
- `+card:meet-partner`, `+card:trapdoor-flip`, `+card:extending-bridge`, `+card:pass-item-to-partner` — механік нема в каталозі.

## Джерела
- ⭐ [Wikipedia: Ilomilo](https://en.wikipedia.org/wiki/Ilomilo) — «unite Ilo and Milo», 49 рівнів, перемикання героїв, переносні кубики, кубики-мости й провал на інший бік, килимки, перемикачі, safka, спогади, яйця в мультиплеєрі, вказівник у кооперативі, платформи й DLC.
- [Pocket Gamer: review](https://www.pocketgamer.com/ilomilo/review/) — «flip 90 degrees along the surface», висувний кубик на 3 клітини, без падінь і стрибків, свиня й jack-in-the-box, без смерті, 32 + 6 рівнів (WP7), таблиці друзів.
- [Hooked Gamers, с. 2](https://www.hookedgamers.com/x360/ilomilo/review/article-658-2.html) — кубики-рюкзаки з «personalities»: ліфт, міст, люк; килимок; істота-блокатор; яблука й свиня; фото, платівки, спогади, по три safka; 36 + 12 рівнів.
- [Engadget](https://www.engadget.com/2011-01-05-ilomilo-review-thumbs-upside-down.html) — червоний Іло й синій Міло, «backpacks», люк на протилежний бік кубика, кубик, що котиться, передача предметів поруч.
- [Kotaku](https://kotaku.com/review-ilomilos-surprising-depth-is-a-matter-of-percep-5727987) — 49 рівнів у 4 главах, блоки, що повертаються, герої на різних боках, «meet face-to-face», муха-вказівник.
- [Game Rant](https://gamerant.com/ilomilo-reviews/) — B перемикає, кубики-ліфти, мапа 3×4 з відкриттям сусідніх, три safka, «ilomilo shuffle».
- YouTube: [пошук «ilomilo gameplay»](https://www.youtube.com/results?search_query=ilomilo+gameplay).

## Непевне
- (?) Офіційних назв кубиків не знайдено (fandom-вікі віддає 402); опис — з рецензій. Темний кубик і висувна коробка (сніпет гайду Gameyum до фінального пазла) — поведінка невідома.
- (?) Кубик-ліфт: чи везе героя і як керується; блоки, що повертаються (Kotaku), і кубик, що котиться (Engadget), — механіка не описана.
- (?) Свиня й яблука: як саме «змусити» свиню пройти; що робить jack-in-the-box.
- (?) Передача кубика між героями: досить сусідства чи треба стояти лицем до лиця.
- (?) Кількість рівнів різниться: 49 (Wikipedia, Kotaku) / 36 + 12 бонусних (Hooked Gamers) / 32 + 6 і 3 глави (WP7, Pocket Gamer); Game Rant пише про «six worlds».
- (?) Умова відкриття бонусних рівнів: три safka в рівні чи всі safka глави.
- (?) Кнопки: B — перемикання (Game Rant) чи «помахати» (Engadget); що рахують таблиці друзів XBL.
