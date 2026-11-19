# Черга: build-sim — будування, ферми, автоматизація, автомати

Сид куратора (Fable, 2026-11-02), розширено пошуковим агентом 2026-11-02. Пріоритет 1 — обовʼязково описати, 2 — бажано, 3 — коли дійдуть руки. Лінки — лише ті, що агент бачив (Wikipedia перевірено через API, Steam — через appdetails); де точної сторінки не бачив — пошуковий шаблон. Ліміт вебпошуку сесії вичерпано на середині — частина нових знахідок має лише Wikipedia/Steam-лінки, механіки з позначкою `(?)` перевірити описовому агенту.

Для великих ігор у «чим нова» — **одна** клітинна механіка, яку корпус має витягти (решту гри не описувати).

## Клітинні автомати (гра без гравця або з редактором)

| Назва | рік | чим нова для корпусу | лінк-⭐ | інші лінки | пріоритет |
|---|---|---|---|---|---|
| Conway's Game of Life | 1970 | еталон: правило B3/S23 за 8 сусідами, патерни, редактор, крок/швидкість | https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life | https://en.wikipedia.org/wiki/Life-like_cellular_automaton · https://en.wikipedia.org/wiki/Golly_(program) | 1 |
| Langton's Ant (+ turmites) | 1986 | агент-мураха фарбує клітину й повертає; «шосе» після хаосу | https://en.wikipedia.org/wiki/Langton%27s_ant | https://en.wikipedia.org/wiki/Turmite · https://esolangs.org/wiki/Langton%27s_ant | 1 |
| Wireworld | 1987 | 4 стани (порожньо/голова/хвіст/провідник) — електроніка й логічні вентилі на клітинах | https://en.wikipedia.org/wiki/Wireworld | https://conwaylife.com/wiki/WireWorld · https://celestial.itch.io/wireworld-1k | 1 |
| Brian's Brain | 1990-ті (?) | 3 стани з рефрактерним «вмирає» — вічні рухомі структури | https://en.wikipedia.org/wiki/Brian%27s_Brain | https://en.wikipedia.org/wiki/Seeds_(cellular_automaton) | 2 |
| Rule 110 (елементарні 1D автомати) | 1983 | одновимірний ряд, час — вниз; правило як 8-бітний номер; Тюрінг-повний | https://en.wikipedia.org/wiki/Rule_110 | https://en.wikipedia.org/wiki/Elementary_cellular_automaton | 2 |
| Lenia | 2018 | неперервні стани й ядро-сусідство замість 8 клітин — межа «клітинності» | https://en.wikipedia.org/wiki/Lenia | — | 3 |
| Cell Machine | 2020 | гравець розставляє клітини-рушії/генератори/обертачі, далі автомат крутиться сам | https://samhogan.itch.io/cell-machine/comments?after=468 | https://rawg.io/games/cell-machine · https://omay238.itch.io/sprig-machine | 1 |
| Falling sand (→ dig-gravity) | 1990-ті | матеріали-клітини падають/течуть/горять; тут лише згадка, опис — у dig-gravity | https://en.wikipedia.org/wiki/Falling-sand_game | https://en.wikipedia.org/wiki/The_Powder_Toy | 3 |

## Автоматизація й конвеєри

| Назва | рік | чим нова для корпусу | лінк-⭐ | інші лінки | пріоритет |
|---|---|---|---|---|---|
| Factorio | 2020 | **витягти:** конвеєр на 2 доріжки + інсертер між клітинами; будівлі 1×1/2×2/3×3 | https://store.steampowered.com/app/427520 | https://en.wikipedia.org/wiki/Factorio · https://forums.factorio.com/viewtopic.php?p=168203 | 1 |
| Mindustry | 2019 | конвеєри підвозять набої до турелей — фабрика як TD | https://store.steampowered.com/app/1127400 | https://en.wikipedia.org/wiki/Mindustry · https://mindustry.fandom.com/wiki/Mindustry_Wiki?oldid=929 | 1 |
| shapez | 2020 | безкоштовні будівлі, ресурс — геометрична форма з 4 чвертей, різання/фарбування/стек | https://store.steampowered.com/app/1318690 | https://gigazine.net/gsc_news/en/20201103-game-shapez | 1 |
| ~~shapez 2~~ | 2024 | шари поверхів, форми до 4 шарів × 4 чверті, модульні острови | https://store.steampowered.com/app/2162800 | https://en.wikipedia.org/wiki/Shapez_2 · https://thinkygames.com/games/shapez-2/ · ⊘ 2026-11-19: покрито `build-sim/shapez` | 2 |
| Dyson Sphere Program | 2021 | **витягти:** сітка на кулі планети — клітини стискаються до полюсів | https://store.steampowered.com/app/1366540 | https://en.wikipedia.org/wiki/Dyson_Sphere_Program | 2 |
| Big Pharma | 2015 | машини зсувають «концентрацію» інгредієнта 0–20 — стан предмета на конвеєрі | https://en.wikipedia.org/wiki/Big_Pharma_(video_game) | https://store.steampowered.com/search/?term=Big+Pharma | 1 |
| Automachef | 2019 | кухня-конвеєр на сітці, рецепт = маршрут інгредієнтів | https://store.steampowered.com/search/?term=Automachef | https://www.youtube.com/results?search_query=Automachef+gameplay | 3 |
| Production Line | 2017 | зміна-слоти конвеєра авто, швидкість станцій (?) | https://store.steampowered.com/search/?term=Production+Line | https://www.youtube.com/results?search_query=Production+Line+car+factory+gameplay | 3 |
| PlateUp! | 2022 | ресторан на клітинах: прилади-сусіди, конвеєри й авто-руки між тайлами (?) | https://store.steampowered.com/app/1599600 | https://www.youtube.com/results?search_query=PlateUp+gameplay | 2 |
| OpenTTD (Transport Tycoon) | 2004 / 1994 | **витягти:** блокові й шляхові семафори на тайлових рейках | https://wiki.openttd.org/en/Manual/Signals | https://en.wikipedia.org/wiki/OpenTTD · https://en.wikipedia.org/wiki/Transport_Tycoon · https://dpk.land/io/ttd/signals | 1 |
| Mini Motorways | 2021 | дороги малюються по квадратній сітці, будинок↔будівля одного кольору, таймер переповнення | https://en.wikipedia.org/wiki/Mini_Motorways | https://store.steampowered.com/app/1127500 | 1 |

## Ферми й ріст

| Назва | рік | чим нова для корпусу | лінк-⭐ | інші лінки | пріоритет |
|---|---|---|---|---|---|
| Stardew Valley | 2016 | **витягти:** грядка (зорано/полито/росте за дні) + спринклери 4/8/24 клітини | https://stardewvalleywiki.com/Sprinkler | https://en.wikipedia.org/wiki/Stardew_Valley · https://stardewvalleywiki.com/Iridium_Sprinkler · https://store.steampowered.com/app/413150 | 1 |
| Harvest Moon | 1996 | первинна петля «плуг → насіння → полив → день»; сезон губить посіви | https://en.wikipedia.org/wiki/Harvest_Moon_(video_game) | https://en.wikipedia.org/wiki/Rune_Factory | 2 |
| Animal Crossing: New Horizons | 2020 | **витягти:** схрещування квітів-сусідів за прихованими генами (менделівськи) | https://github.com/joeyparrish/acnh-flowers | https://en.wikipedia.org/wiki/Animal_Crossing:_New_Horizons · https://www.gamespot.com/amp-articles/animal-crossing-new-horizons-hybrid-flowers-guide-/1100-6475346/ | 1 |
| FarmVille | 2009 | посів у реальному часі, посіви в'януть без збору — таймер клітини | https://en.wikipedia.org/wiki/FarmVille | — | 3 |
| Hay Day | 2012 | мобільна ферма: грядки + виробничі черги будівель | https://en.wikipedia.org/wiki/Hay_Day | — | 3 |
| Viva Piñata | 2006 | сад-екосистема: умови появи тварин від складу клітин саду (?) | https://en.wikipedia.org/wiki/Viva_Pi%C3%B1ata_(video_game) | https://www.youtube.com/results?search_query=Viva+Pinata+gameplay · ✔ виправлено 2026-11-09 | 3 |

## Тайлові пісочниці (великі ігри — по одній механіці)

| Назва | рік | чим нова для корпусу | лінк-⭐ | інші лінки | пріоритет |
|---|---|---|---|---|---|
| Minecraft | 2011 | **витягти:** редстоун — сигнал 0–15, згасає на 1 за блок, репітер/компаратор | https://minecraft.wiki/w/Redstone_circuits/Advanced_circuits | https://en.wikipedia.org/wiki/Minecraft · https://esolangs.org/wiki/Minecraft_(game) | 1 |
| Terraria | 2011 | **витягти:** рідини (вода/лава/мед) течуть між тайлами, змішування → нові блоки | https://en.wikipedia.org/wiki/Terraria | https://store.steampowered.com/search/?term=Terraria | 2 |
| Core Keeper | 2022 | **витягти:** копання тайлів зверху + ферма й автоматизація в тому ж світі | https://en.wikipedia.org/wiki/Core_Keeper | https://store.steampowered.com/search/?term=Core+Keeper | 3 |
| Forager | 2019 | **витягти:** купівля нових острівних ділянок сітки світу | https://en.wikipedia.org/wiki/Forager_(video_game) | https://store.steampowered.com/search/?term=Forager | 3 |
| Graveyard Keeper | 2018 | **витягти:** якість могили як сума предметів на ділянці (?) | https://en.wikipedia.org/wiki/Graveyard_Keeper | https://store.steampowered.com/search/?term=Graveyard+Keeper | 3 |

## Укладання тайлів і процедурні сітки

| Назва | рік | чим нова для корпусу | лінк-⭐ | інші лінки | пріоритет |
|---|---|---|---|---|---|
| Townscaper | 2021 | нерегулярна квадова сітка; вигляд клітини — правило від сусідів, гравець лише ставить колір | https://www.gamedeveloper.com/game-platforms/how-townscaper-works-a-story-four-games-in-the-making | https://en.wikipedia.org/wiki/Townscaper · https://store.steampowered.com/app/1291340 · https://sketchpunklabs.github.io/irregular_grid | 1 |
| Dorfromantik | 2022 | гекс-тайли з 6 краями, бонус за повний збіг, квести дають нові тайли | https://store.steampowered.com/app/1455840 | https://en.wikipedia.org/wiki/Dorfromantik · https://www.vice.com/en/article/dorfromantik-turns-city-building-into-a-beautiful-series-of-puzzles | 1 |
| Loop Hero | 2021 | тайли біля петлі-дороги спавнять ворогів; суміжність і 3×3 скелі дають нові тайли | https://pcgamer.com/loop-hero-combos-cards-tile | https://en.wikipedia.org/wiki/Loop_Hero · https://store.steampowered.com/app/1282730 · https://minmax.wiki/loop-hero/gameplay-tips | 1 |
| Islanders | 2019 | очки за сусідство в радіусі будівлі, прев'ю очок до розміщення (вільна позиція — межа) | https://en.wikipedia.org/wiki/Islanders_(video_game) | https://store.steampowered.com/app/1046030 | 2 |
| Block'hood | 2017 | блоки-воксели з входами/виходами ресурсів; без входу блок гниє й заражає сусідів | https://en.wikipedia.org/wiki/Block%27hood | https://store.steampowered.com/app/416210 · https://www.devolverdigital.com/games/blockhood | 1 |

## Сітковий інвентар і слот-сітки

| Назва | рік | чим нова для корпусу | лінк-⭐ | інші лінки | пріоритет |
|---|---|---|---|---|---|
| Backpack Hero | 2023 | рюкзак-сітка як бій: позиція й сусідство предметів визначають ефект | https://store.steampowered.com/app/1970580 | https://en.wikipedia.org/wiki/Backpack_Hero · https://www.pcgamer.com/heres-a-whole-roguelike-about-inventory-management | 1 |
| Backpack Battles | 2024 | PvP-автобатлер рюкзаків: синергії «поруч з їжею/темним» | https://en.wikipedia.org/wiki/Backpack_Battles | https://store.steampowered.com/app/2427700 | 1 |
| Save Room | 2022 | чисте пакування поліміно-предметів у кейс RE4-стилю як пазл | https://store.steampowered.com/search/?term=Save+Room | https://www.youtube.com/results?search_query=Save+Room+Organization+Puzzle+gameplay | 2 |
| Resident Evil 4 (attaché case) | 2005 | сітковий кейс з обертанням предметів — прообраз жанру | https://en.wikipedia.org/wiki/Resident_Evil_4 | — | 3 |
| Diablo II (inventory) | 2000 | інвентар з прямокутними предметами 1×1…2×4, Horadric Cube | https://en.wikipedia.org/wiki/Diablo_II | — | 3 |
| Dredge | 2023 | трюм-сітка: улов різної форми, пошкоджені клітини корпусу | https://en.wikipedia.org/wiki/Dredge_(video_game) | https://store.steampowered.com/search/?term=Dredge | 2 |
| Luck be a Landlord | 2023 | слот-сітка 5×4: символи взаємодіють із сусідами після кожного спіну | https://en.wikipedia.org/wiki/Luck_Be_a_Landlord | https://store.steampowered.com/app/1404850 · https://gamepretty.com/luck-be-a-landlord-symbol-item-guide/ | 1 |

## Містобудування, парки, лікарні

| Назва | рік | чим нова для корпусу | лінк-⭐ | інші лінки | пріоритет |
|---|---|---|---|---|---|
| SimCity (Micropolis) | 1989 | зони R/C/I 3×3, вартість землі й злочинність як поля-карти | https://en.wikipedia.org/wiki/SimCity_(1989_video_game) | https://store.steampowered.com/search/?term=SimCity | 1 |
| Cities: Skylines | 2015 | **витягти:** зонні клітинки народжуються вздовж дороги (?) | https://en.wikipedia.org/wiki/Cities:_Skylines | — | 3 |
| Caesar III | 1998 | ходоки-служби з будівель: покриття — пройдений шлях, не радіус | https://en.wikipedia.org/wiki/Caesar_III | https://store.steampowered.com/search/?term=Caesar+3 | 1 |
| Pharaoh | 1999 | та сама модель ходоків + еволюція будинку від набору послуг, розлив Нілу | https://en.wikipedia.org/wiki/Pharaoh_(video_game) | https://store.steampowered.com/search/?term=Pharaoh | 2 |
| Anno 1800 | 2019 | **витягти:** радіус впливу будівлі сервісу по дорогах (?) | https://en.wikipedia.org/wiki/Anno_1800 | — | 3 |
| Civilization VI | 2016 | **витягти:** бонус суміжності районів на гексах (+2/+1/+0.5) | https://civilization.fandom.com/wiki/List_of_districts_in_Civ6 | https://en.wikipedia.org/wiki/Civilization_VI · https://pcgamesn.com/civilization-vi/civ-6-district-guide | 1 |
| Frostpunk | 2018 | кругова (полярна) сітка навколо генератора, тепло радіусом | https://en.wikipedia.org/wiki/Frostpunk | https://store.steampowered.com/app/323190 | 1 |
| Populous | 1989 | підняття/опускання землі у вершинах сітки; пласка площа = розмір будинку | https://en.wikipedia.org/wiki/Populous_(video_game) | https://www.youtube.com/results?search_query=Populous+1989+gameplay | 1 |
| RollerCoaster Tycoon | 1999 | доріжки й колії по тайлах з висотою, черга до атракціону | https://en.wikipedia.org/wiki/RollerCoaster_Tycoon_(video_game) | — | 2 |
| Parkitect | 2018 | службові доріжки окремо від гостьових, видимість зі шляху | https://en.wikipedia.org/wiki/Parkitect | https://store.steampowered.com/search/?term=Parkitect | 3 |
| Theme Hospital | 1997 | кімната = прямокутник мін. розміру + обов'язкові предмети всередині | https://en.wikipedia.org/wiki/Theme_Hospital | — | 2 |
| Two Point Hospital | 2018 | те ж + престиж кімнати від предметів у ній | https://en.wikipedia.org/wiki/Two_Point_Hospital | — | 3 |
| Fallout Shelter | 2015 | однакові кімнати-сусіди зливаються до 3 ширини; сітка поверхів у скелі | https://fallout.wiki/wiki/Fallout_Shelter_rooms | https://en.wikipedia.org/wiki/Fallout_Shelter · https://store.steampowered.com/search/?term=Fallout+Shelter | 1 |
| Tiny Tower / SimTower | 2011 / 1994 | одновимірна вежа поверхів, ліфт як вузьке місце | https://en.wikipedia.org/wiki/Tiny_Tower | https://en.wikipedia.org/wiki/SimTower | 2 |

## Колонії й підземелля

| Назва | рік | чим нова для корпусу | лінк-⭐ | інші лінки | пріоритет |
|---|---|---|---|---|---|
| Prison Architect | 2015 | кімнати-зони за вимогами + графік; стіни й двері задають доступ | https://en.wikipedia.org/wiki/Prison_Architect | https://store.steampowered.com/search/?term=Prison+Architect | 2 |
| RimWorld | 2018 | **витягти:** кімната = замкнений стінами регіон; температура й «враження» кімнати | https://en.wikipedia.org/wiki/RimWorld | https://store.steampowered.com/app/294100 | 2 |
| Dwarf Fortress | 2006 | **витягти:** призначення клітин (зони, склади) + рідини 1–7 рівнів у клітині | https://en.wikipedia.org/wiki/Dwarf_Fortress | https://store.steampowered.com/search/?term=Dwarf+Fortress | 2 |
| Oxygen Not Included | 2019 | **витягти:** кожна клітина — один газ/рідина з масою й температурою, дифузія | https://en.wikipedia.org/wiki/Oxygen_Not_Included | https://store.steampowered.com/app/457140 | 1 |
| Dungeon Keeper | 1997 | копання тайлів слугами за позначкою + кімнати, що приваблюють істот | https://en.wikipedia.org/wiki/Dungeon_Keeper | — | 2 |
| SimAnt | 1991 | мурахи + феромонні сліди на клітинах; бокова мапа нори | https://en.wikipedia.org/wiki/SimAnt | — | 2 |
| Space Haven | 2020 | корабель з тайлів, кисень/температура по клітинах (?) | https://store.steampowered.com/app/979110 | — | 3 |
| Timberborn | 2021 | вода як рівень у клітині, дамби й посухи; вертикальні шари | https://en.wikipedia.org/wiki/Timberborn | https://store.steampowered.com/app/1062090 | 1 |
| Against the Storm | 2023 | галявини в лісі, розчищення; клітинна сітка (не гекс, перевірити) (?) | https://store.steampowered.com/app/1336490 | https://en.wikipedia.org/wiki/Against_the_Storm_(video_game) | 3 |
| Kingdoms and Castles | 2017 | вікінги/дракони атакують мапу з клітин, родючість ґрунту для ферм | https://en.wikipedia.org/wiki/Kingdoms_and_Castles | https://store.steampowered.com/search/?term=Kingdoms+and+Castles | 3 |

## Бази й розкладання

| Назва | рік | чим нова для корпусу | лінк-⭐ | інші лінки | пріоритет |
|---|---|---|---|---|---|
| Clash of Clans | 2012 | розкладка бази на сітці для чужих атак, стіни з тайлів | https://en.wikipedia.org/wiki/Clash_of_Clans | — | 2 |
| Boom Beach | 2014 | та сама модель, острів-база + рух десанту | https://en.wikipedia.org/wiki/Boom_Beach | — | 3 |
| Unpacking | 2021 | розкладання предметів по полицях-клітинах, правильне місце = правило | https://en.wikipedia.org/wiki/Unpacking_(video_game) | https://store.steampowered.com/app/1135690 | 2 |
| A Little to the Left | 2022 | впорядкування за прихованим правилом, кілька правильних розв'язків | https://en.wikipedia.org/wiki/A_Little_to_the_Left | — | 2 |
| Wilmot's Warehouse | 2019 | склад-сітка: власна класифікація ящиків, потім вибірка на час | https://en.wikipedia.org/wiki/Wilmot%27s_Warehouse | https://store.steampowered.com/app/839870 | 2 |

## Відновлення й екосистеми

| Назва | рік | чим нова для корпусу | лінк-⭐ | інші лінки | пріоритет |
|---|---|---|---|---|---|
| Terra Nil | 2023 | тайли пустки → біоми; турбіни лише на камені, радіуси машин, потім прибирання | https://en.wikipedia.org/wiki/Terra_Nil | https://store.steampowered.com/app/1593030 | 1 |
| Cloud Gardens | 2021 | рослини ростуть від розкиданого сміття поблизу (?) | https://store.steampowered.com/app/1372320 | https://www.youtube.com/results?search_query=Cloud+Gardens+gameplay | 3 |

## Межові випадки

- **Falling sand · The Powder Toy · Noita** → `dig-gravity` (клітинна фізика матеріалів).
- **Carcassonne · Kingdomino · Isle of Skye · Cascadia · Kingdom Builder · Tiny Towns · Patchwork** → `board-digital` (тут лише згадка; Kingdomino/Cascadia — найближчі до Dorfromantik). Лінки: https://en.wikipedia.org/wiki/Carcassonne_(board_game) · https://en.wikipedia.org/wiki/Kingdomino · https://en.wikipedia.org/wiki/Isle_of_Skye:_From_Chieftain_to_King · https://en.wikipedia.org/wiki/Cascadia_(board_game) · https://en.wikipedia.org/wiki/Kingdom_Builder
- **Autonauts** → `program-robots` (ботам пишуть програми).
- **Infinifactory · Opus Magnum · Manufactoria** → `program-robots` (фабрика як програма, а не логістика).
- **Mindustry** — можна і в `tower-lanes`; лишаю тут, бо 80 % часу — логістика.
- **Stacklands** — картки складаються в стоси без сітки; не клітинна, максимум згадка. https://en.wikipedia.org/wiki/Stacklands
- **Tiny Glade** — навмисно без сітки; не брати. https://store.steampowered.com/app/2198150/
- **Satisfactory** — фундаменти 8 м як 3D-сітка, але гра від першої особи; радше пропустити.
- **Islanders** — вільне розміщення, не сітка: описувати лише модель «очки сусідства в радіусі», якщо куратор вирішить, що радіус замість клітин теж наш.
- **Lenia** — неперервний автомат; брати лише як «межу класу», без повного опису.
- **Loop Hero · Backpack Hero · Backpack Battles** — тайл/інвентарна механіка обслуговує бій; можливе `also: roguelike`.
- **Clash of Clans · Boom Beach** — атака бази ближче до `tactics`/`tower-lanes`; тут — лише розкладка.

## Хвиля 3 — 2026-11-09: нові кандидати (пошукові агенти Opus)

Джерела: Wikipedia API (`Category:Cellular_automata`, `Category:Cellular_automaton_rules`, `Category:City-building_games`, extracts 20 статей автоматів), статті ігор EN-Wikipedia, Steam search + сторінки ігор, itch `tag-cellular-automata`, earslap.com · Не відкрилось: `Category:Agricultural_video_games` (порожня), wiki.gg/fandom (не пробував — правило) · WebSearch: 9.

| Назва | рік | чим нова для корпусу | лінк-⭐ | інші лінки | пріоритет |
|---|---|---|---|---|---|
| Abelian sandpile model (Bak–Tang–Wiesenfeld) | 1987 | клітина з ≥4 зернами осипається на 4 сусідів; лавини; порядок осипань не важить | W:Abelian_sandpile_model | https://www.youtube.com/results?search_query=abelian+sandpile+model | 1 |
| Wa-Tor | 1984 | тор: риби й акули ходять, розмножуються за таймером, акули гинуть без їжі | W:Wa-Tor | https://www.youtube.com/results?search_query=Wa-Tor+simulation | 1 |
| Forest-fire model (Drossel–Schwabl) | 1992 | порожньо/дерево/вогонь: ріст з імовірністю p, блискавка f, вогонь до сусідів | W:Forest-fire_model | https://www.youtube.com/results?search_query=forest+fire+cellular+automaton | 1 |
| Cyclic cellular automaton (Griffeath) | 1989 (?) | n станів по колу: клітина бере стан сусіда, рівно на 1 більший — спіралі | W:Cyclic_cellular_automaton | https://www.youtube.com/results?search_query=cyclic+cellular+automaton | 1 |
| Langton's loops (+ Byl's loop) | 1984 / 1989 | петля зі «стрічкою генів» самовідтворюється через рукав; 8 станів, у Била 7 | W:Langton's_loops | W:Byl's_loop | 1 |
| Critters (block cellular automaton, Margolus) | 1987 | правило діє на блоки 2×2, розбиття зсувається щокроку; оборотний автомат | W:Critters_(cellular_automaton) | W:Block_cellular_automaton | 1 |
| Biham–Middleton–Levine traffic model | 1992 | червоні авто вправо, сині вниз, ходять по черзі; різкий перехід у глобальний затор | W:Biham–Middleton–Levine_traffic_model | https://www.youtube.com/results?search_query=Biham+Middleton+Levine+traffic+model | 1 |
| Nagel–Schreckenberg model | 1992 | 1D дорога: швидкість авто 0..vmax, розгін, гальмування до просвіту, випадкове гальмування | W:Nagel–Schreckenberg_model | https://www.youtube.com/results?search_query=Nagel+Schreckenberg+model | 1 |
| Schelling's model of segregation | 1971 | агент переїжджає в порожню клітину, коли частка схожих сусідів нижче порогу | W:Schelling's_model_of_segregation | https://www.youtube.com/results?search_query=Schelling+segregation+model | 1 |
| Sugarscape | 1996 | агенти із зором і метаболізмом збирають цукор, що відростає на клітинах | W:Sugarscape | https://www.youtube.com/results?search_query=Sugarscape+simulation | 1 |
| Otomata | 2011 | клітини-стрілки рухаються; удар об стіну — нота за позицією, зіткнення — поворот за годинниковою | http://earslap.com/page/otomata.html | https://elanarko.itch.io/otomata-dx | 1 |
| Sleeper Cells | 2024 (?) | камінь-ножиці-папір клітин: оточена ≥2 ворогами переходить; ліміт заражень і стінки | https://thesquaregroot.itch.io/sleeper-cells | https://itch.io/games/tag-cellular-automata | 1 |
| The Settlers II | 1996 | дороги між прапорцями, один носій на відрізок; частіші прапорці — коротші переноси | W:The_Settlers_II | https://www.youtube.com/results?search_query=The+Settlers+II+gameplay | 1 |
| M.U.L.E. | 1983 | ділянки колонії під ресурс; бонус за групу сусідніх однотипних; аукціон у реальному часі | W:M.U.L.E. | https://www.youtube.com/results?search_query=M.U.L.E.+1983+gameplay | 1 |
| The King Is Watching | 2025 | замок 5×5: працюють лише клітини під рухомою фігурою погляду короля | https://store.steampowered.com/app/2753900/The_King_is_Watching/ | W:The_King_Is_Watching | 1 |
| Urbek City Builder | 2022 | будівля перетворюється на іншу залежно від сусідів; забруднення знецінює житло поруч | https://store.steampowered.com/app/1411740/Urbek_City_Builder/ | W:Urbek_City_Builder | 1 |
| Before We Leave | 2020 | гекс-сітка на кулі планети з 12 пʼятикутниками; бонуси сусідства будівель | https://pcgamer.com/before-we-leave-review | https://store.steampowered.com/app/1073910 · W:Before_We_Leave | 1 |
| Greenberg–Hastings automaton | 1978 | збудливе середовище спокій → збудження → рефрактерність; хвилі й спіралі з порогом | W:Greenberg–Hastings_cellular_automaton | https://www.youtube.com/results?search_query=Greenberg+Hastings+cellular+automaton | 2 |
| Von Neumann cellular automaton (+ Codd) | 1966 / 1968 | 29 станів, універсальний конструктор будує копію за стрічкою; Codd — 8 станів | W:Von_Neumann_cellular_automaton | W:Codd's_cellular_automaton | 2 |
| Lattice gas automaton (HPP / FHP) | 1973 / 1986 | частинки-напрямки в клітині, зіткнення за таблицею; квадратна HPP і гексова FHP | W:Lattice_gas_automaton | https://www.youtube.com/results?search_query=lattice+gas+automaton | 2 |
| Ulam–Warburton automaton | 1962 (?) | клітина вмикається, якщо рівно один сусід по ребру увімкнений; фрактальний ріст | W:Ulam–Warburton_automaton | — | 2 |
| Firing squad synchronization problem | 1957 | 1D-задача-конструктор: скласти правило, щоб усі клітини «вистрілили» в один тік | W:Firing_squad_synchronization_problem | https://www.youtube.com/results?search_query=firing+squad+synchronization+problem | 2 |
| 3D Life (Carter Bays) | 1987 | Life у кубічній сітці: 26 сусідів, правила народження/виживання для 3D | W:3D_Life | https://store.steampowered.com/app/1089890/3D_Life/ | 2 |
| Patternsight | 2026 | фігури Life як будівлі й юніти з ціною; планер — снаряд; передбачити еволюцію | https://programersi.itch.io/patternsight | — | 2 |
| Offworld Trading Company | 2016 | екстрактори лише на гексах поруч зі штабом; ціни ресурсів від попиту й пропозиції | W:Offworld_Trading_Company | https://www.youtube.com/results?search_query=Offworld+Trading+Company+gameplay | 2 |
| Afterlife | 1996 | 14 зон гріхів і чеснот у Раю й Пеклі; споруди ростуть лише під своїми vibes | W:Afterlife_(video_game) | https://www.youtube.com/results?search_query=Afterlife+1996+LucasArts+gameplay | 2 |
| Minami Lane | 2024 | місто з однієї вулиці: магазини, будинки, парки, меню й ціни крамниць | W:Minami_Lane | https://store.steampowered.com/search/?term=Minami+Lane | 2 |
| SteamWorld Build | 2023 | два шари: місто на поверхні й шахта під ним, тунелі копають робітники | W:SteamWorld_Build | https://store.steampowered.com/search/?term=SteamWorld+Build | 2 |
| Rebuild 3: Gangs of Deadsville | 2015 | місто з кварталів-клітин; база росте лише на очищені від зомбі сусідні квартали | W:Rebuild_3:_Gangs_of_Deadsville | https://store.steampowered.com/search/?term=Rebuild+3 | 2 |
| Reus | 2013 | ділянка = один обʼєкт; симбіоз-бонус від певних сусідів у радіусі; межі селищ | W:Reus_(video_game) | https://guides.gamepressure.com/reus/segments/zf4fc2 | 2 |
| SimCity 2000 | 1993 | сиквел SimCity: висоти рельєфу й підземний шар (водогін, метро, тунелі) | W:SimCity_2000 | https://www.youtube.com/results?search_query=SimCity+2000+gameplay | 2 |
| Factory Town | 2021 | жолоби везуть лише вниз схилом, вагонетки — повільно вгору; логіка воріт і фільтрів | https://store.steampowered.com/app/860890/Factory_Town/ | https://pcgamer.com/factory-town-reimagines-factorio-as-a-colourful-magical-city-builder | 2 |
| Escape from Tarkov | 2017 / 2025 | витягти: форма сітки інвентаря залежить від спорядження; захищений контейнер переживає смерть | W:Escape_from_Tarkov | https://www.youtube.com/results?search_query=Escape+from+Tarkov+inventory+tetris | 2 |
| Cosmoteer | 2022 | план корабля з модулів; екіпаж носить снаряди; модулі руйнуються окремо, корабель розпадається | https://store.steampowered.com/app/799600/Cosmoteer_Starship_Architect_Commander/ | https://www.youtube.com/results?search_query=Cosmoteer+gameplay | 2 |
| Hot Springs Story (Kairosoft) | 2010 (?) | сумісні кімнати поруч дають бонус; декор діє в радіусі 2 клітин зі спадом | https://www.pocketgamer.co.uk/articles/027950/r/ | https://kairosoft.wiki.gg/wiki/Hot_Springs_Story · https://kairosoft.wiki.gg/wiki/Combos_(Dream_Town_Story) | 2 |
| Dragon Quest Builders | 2016 | витягти: кімната = стіни ≥2 блоки + двері + світло; набір меблів задає тип | https://dragon-quest.org/wiki/Room_Recipes_(Dragon_Quest_Builders) | W:Dragon_Quest_Builders · https://dragon-quest.org/wiki/List_of_room_recipes_in_Dragon_Quest_Builders_2 | 2 |
| Niche – a genetics survival game | 2017 | гекс-карта; розведення тварин з домінантними й рецесивними генами; 3 ходи на тварину | https://www.pcgamer.com/niche-blends-turn-based-strategy-roguelike-survival-and-genetic-mutations | https://www.gog.com/game/niche | 2 |
| Atomicrops | 2020 | витягти: 4 однакові культури квадратом 2×2 + добриво → велетенський плід; нічні хвилі | W:Atomicrops | https://www.youtube.com/results?search_query=Atomicrops+gameplay | 2 |
| A-Train | 1985 | залізниця везе будматеріали — місто росте біля станцій; пасажири як дохід | W:A-Train | https://www.youtube.com/results?search_query=Take+the+A-Train+III+gameplay | 2 |
| Toom's rule | 1978 | голос більшості: сама клітина, північний і східний сусід; виправляє шум | W:Toom's_rule | — | 3 |
| Yawnoc | 2024 | вороги-машини живуть за Life / Brian's Brain / LowDeath, правило змінюється з рівнем | https://store.steampowered.com/app/2824730/Yawnoc/ | https://dafluffypotato.itch.io/yawnoc | 3 |
| ActRaiser (режим симуляції) | 1990 | ангел вказує напрям забудови; лігва спавнять монстрів, доки їх не запечатано | W:ActRaiser | https://www.youtube.com/results?search_query=ActRaiser+simulation+mode | 3 |
| SimEarth | 1990 | витягти: режим Daisyworld — ромашки змінюють колір від температури; тераформінг клітинами (?) | W:SimEarth | https://www.youtube.com/results?search_query=SimEarth+gameplay | 3 |
| Startopia | 2001 | станція-тор з 3 палуб; біопалуба тераформується (температура, вологість, вода, висота) | W:Startopia | https://www.youtube.com/results?search_query=Startopia+gameplay | 3 |
