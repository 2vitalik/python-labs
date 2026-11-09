# Інструкція пошукового агента (хвиля 3, 2026-11-09 — зразок для наступних хвиль)

Збережена інструкція хвилі 3 ([T265](../../../.dev/games/.t/T265--ludopedia-wave3/report.md)): один Opus-агент на сімʼю, кожен пише ізольований файл `queue/<хвиля>/<family>.md`, куратор зливає їх у черги сімей скриптом `scripts/queue_merge.py <хвиля> [--apply]`. Для нової хвилі: замінити номер і дату, створити теку `queue/<хвиля>/`, перегенерувати `index/known-names.txt` (`scripts/known_names.py`) і `index/queue-status.md` (`scripts/queue_status.py`). Хаби джерел — [_sources.md](_sources.md); спільні правила — [AGENT-BRIEF.md](../AGENT-BRIEF.md), секція «Пошуковий агент». Усі шляхи нижче — відносно `data/ludopedia/`.

## Мета

Корпус уже має сотні описаних ігор і тисячі рядків черг — усе очевидне вже є. Задача агента: знайти **30–45 нових ігор на клітинному полі** для своєї сімʼї, яких немає ні в корпусі, ні в чергах. Цінність — **розмаїття механік** (нова взаємодія, незвичне поле, незвичний ввід, цікаве вікно/налаштування), старі й нові ігри однаково; не популярність і не кількість. Краще 30 чесних рядків із джерелами, ніж 60 з вигаданими.

## Крок 0 — прочитай (у цьому порядку)

1. `AGENT-BRIEF.md` — спільні правила, секція «Пошуковий агент», доповнення v1.1–v1.3.
2. `taxonomy/families.md` — межа своєї сімʼї із сусідами.
3. `queue/<family>.md` — що вже в черзі; `index/queue-status.md` — що з черг описано.
4. `queue/_sources.md` — хаби пошуку.
5. `index/known-names.txt` — **усі відомі назви** (title/aka/slug корпусу + рядки черг), рядок `назва | нормалізована | game:сімʼя/slug або queue:файл`.
6. `ls games/<family>/` — slug-и вже описаних у сімʼї (і сусідніх, якщо гра на межі).

## Дедуп — залізне правило

Перед тим як записати рядок: `grep -i "<ключове слово назви>" index/known-names.txt` (і для альтернативних назв: оригінальна JA/DE, регіональна, абревіатура, назва ремейку). Є збіг — **не додавай**. Сиквел або клон уже описаної гри з тими самими механіками — не додавай; сиквел із **новою** механікою — додай з приміткою «сиквел X: що нового». Назви, яких нема у `known-names.txt`, але ти не певен — перевір ще `grep -ril "<назва>" games/*/*.md`.

## Джерела (працюють для агентів)

- **Wikipedia через API** (дешево, сотні назв за один WebFetch): `https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:<Назва_категорії>&cmlimit=500&format=json` — підкатегорії теж (`cmtype=subcat`). Старт: `Category:Puzzle_video_games`, `Tile-matching_video_games`, `Roguelike_video_games`, `Turn-based_tactics_video_games`, `Tower_defense_video_games`, `Maze_games`, `Snake_video_games`, `Programming_games`, `Chess_variants`, `Abstract_strategy_games`, `Tile-based_board_games`, `Logic_puzzles`, `Word_games`, `City-building_games`, `Puzzle-platform_games`, `Sliding_puzzles`, `Pac-Man_clones` — і підкатегорії за роками/платформами. Списки: `List_of_puzzle_video_games`, `List_of_roguelikes`, `List_of_chess_variants`, `List_of_Nikoli_puzzle_types`, `List_of_tower_defense_games`, `List_of_maze_video_games`. Стаття гри — `https://en.wikipedia.org/wiki/<Назва_з_підкресленнями>`; JA/DE Wikipedia — для японських/німецьких ігор (JA `Category:落ち物パズル` — найпродуктивніша для falling-match).
- **Steam**: пошук `https://store.steampowered.com/search/?term=<слова>`, теги `https://store.steampowered.com/tags/en/<Tag%20Name>/` (Grid-Based Movement, Sokoban, Traditional Roguelike, Turn-Based Tactics, Tower Defense, Match 3, Programming, Logic, Minesweeper, Hex Grid, Tile-Matching, Automation). Сторінка гри — `https://store.steampowered.com/app/<id>/`; при 429 — JSON `…/api/appdetails?appids=<id>`.
- **itch.io**: `https://itch.io/games/tag-<tag>` (sokoban, puzzlescript, grid-based, roguelike, minesweeper, match-3, tower-defense, word-game, 7drl, chess, hex); джеми — `https://itch.io/jam/<slug>/entries` (Thinky Puzzle Game Jam 1–4, 7DRL за роками); деякі джеми віддають `…/entries.json`.
- **PuzzleScript**: галерея `https://www.puzzlescript.net/Gallery/index.html` (або `raw.githubusercontent.com/increpare/PuzzleScript/master/src/Gallery/index.html`), гра — `play.html?p=<gist-id>`, сирець — `https://api.github.com/gists/<gist-id>`.
- **Паперові**: `https://puzz.link/list.html` (244 жанри; правила — `js/pzpr-samples/<id>.js`), Nikoli, Janko `https://www.janko.at/Raetsel/index.htm` (300+ жанрів), Logic Masters Germany, GM Puzzles, Conceptis, Tatham, Cracking the Cryptic (варіанти судоку).
- **Настільні й абстрактні**: Ludii `https://ludii.games/library.php`, BoardSpace, Yucata, Mindsports, Board Game Arena (інколи 500), правила — UltraBoardGames `…/<slug>/game-rules.php`, RulesPal `…/<slug>/rulebook`. BGG — і HTML, і XML API віддають 401/403.
- **Роглайки**: RogueBasin `List_of_roguelikes`, `Category:Roguelike_games`, 7DRL `https://7drl.com/`, RogueTemple (огляди 7DRL — найпродуктивніше).
- **Thinky Games** віддає агентам 403 — не ходи туди; куратор знімає його через Chrome (див. нижче) і кладе дамп у теку, шлях до якої буде в промпті.
- **Стабільно не відкриваються**: fandom (402), wiki.gg (401), StrategyWiki / Giant Bomb / TV Tropes / MobyGames / GameFAQs / chessvariants / Sensei's Library (403), BGG (401/403). Обхід через сторонні рідери, проксі чи пошукові сервіси у WebFetch **заборонено**.
- **WebSearch**: ліміт спільний на ~20 агентів — до 80 запитів на агента; каталоги через WebFetch (сотні назв за запит) завжди вигідніші за точкові пошуки. На помилку бюджету не повторюй — далі лише WebFetch.

## Що таке «гра на клітинному полі» для корпусу

Поле з дискретних клітин (квадрат, гекс, граф, 1D-ряд, шари, 3D-воксель) і сутності, що живуть у клітинах; хід/тік — дискретний або real-time на сітці. Підходять також ігри, де сітковий шар — лише частина (інвентар-сітка, бойова сітка RPG, сітка ферми): у колонці «чим нова» пиши «витягти: <шар>». **Не підходять**: вільна фізика без сітки (платформери з пікселями, шутери, гонки), карткові без поля, текстові.

## Формат файла (Write одним заходом; перезаписувати можна)

Шлях: `queue/<хвиля>/<family>.md`. Інших файлів не чіпати.

```
# Хвиля N: <family> — <дата>

Джерела: <що читав, 1–3 рядки> · Не відкрилось: <…> · WebSearch: <N>.

| Назва | рік | чим нова для корпусу | лінк-⭐ | інші лінки | пріоритет | сімʼя |
|---|---|---|---|---|---|---|
| Emberward | 2025 | стіни-тетроміно будують лабіринт для ворогів TD | https://store.steampowered.com/app/2356790/Emberward/ | https://www.youtube.com/results?search_query=Emberward+gameplay | 1 | tower-lanes |
```

- У клітинках — без символу `|`. «Чим нова» — ≤15 слів, конкретна механіка, не маркетинг.
- `лінк-⭐` — URL, який агент **реально відкрив або бачив у результатах**; скорочення `W:Назва_статті` дозволене. Нема лінка — `—` і пріоритет 3. YouTube-ID з памʼяті заборонено; пошуковий URL `https://www.youtube.com/results?search_query=…` — дозволено.
- `рік` — з джерела; трад. гра — `трад.`; не знайшов — `?`.
- `пріоритет`: 1 — нова для корпусу механіка, чисто клітинна, є джерело правил; 2 — бажано; 3 — межова («витягти», слабке джерело).
- `сімʼя` — своя за замовчуванням; гра, що явно належить іншій сімʼї за `families.md`, — її тека (до 10 таких рядків на агента).
- Після таблиці — `## Нотатки` (3–6 рядків): найпродуктивніші джерела, що в чергах/корпусі здалося помилковим, чого свідомо не додав і чому.

## Звіт куратору (≤10 рядків)

Скільки рядків (п1/п2/п3), з них чужих сімей; найпродуктивніші джерела; що не відкрилось; скільки WebSearch; 3 найцікавіші знахідки одним рядком; сумніви щодо дублів.

## Підказки джерел за сімʼями (кожну назву перевіряти у `known-names.txt` і в джерелі)

- **push-slide**: Sokoban Wiki (варіанти правил), ThinkFun-каталог (Rush Hour-родина, Gravity Maze), `Category:Sliding_puzzles`, Pengo-подібні аркади, PuzzleScript-галерея, itch `tag-sokoban`, Steam тег Sokoban; Thinky-теги sokoban / sliding-tile / maneuvering.
- **dig-gravity**: `Category:Rocks-and-diamonds_games`, копальні (Dome Keeper, Wall World, Motherload — «витягти»), falling-sand (межа), ідл-шахти; Steam-пошук dig / mining / boulder dash / falling sand.
- **maze-arcade**: `Category:Maze_games`, `Pac-Man_clones`, `Snake_video_games`, `Bomberman`, Frogger/Qix-клони, arcade-history.com, MAME-списки лабіринтних аркад 1980–85, io-ігри на сітці (`iogames.space`); Thinky-тег snake.
- **grid-platformer**: `Category:Puzzle-platform_games` (лише клітинні), клони Lode Runner / Boxboy / Toki Tori / Solomon's Key / Kickle Cubicle / Fire 'n Ice / Lolo, HAL і Taito головоломки-платформери NES/SNES, Steam тег Grid-Based Movement + Platformer, PuzzleScript платформери з гравітацією.
- **falling-match**: `Category:Tile-matching_video_games`, JA-Wikipedia `Category:落ち物パズル`, японські аркадні пазли (Compile, Taito, Data East, SNK), мобільні match-3 з новим поворотом, merge-ігри, 1010!/Woodoku-подібні, Threes-подібні; Steam тег Match 3.
- **thinky**: itch-джеми Thinky Puzzle Game Jam 1–4, Draknek, increpare, PuzzleScript-галерея, itch `tag-puzzlescript`, Steam новинки Puzzle + Sokoban + Grid-Based Movement; Thinky-теги sokoban / rule-discovery / limited-moves / stepping / maneuvering / record-and-replay.
- **pencil-logic**: puzz.link `list.html` (244 жанри — звіряти кожен), Janko (300+ жанрів з правилами), Logic Masters Germany, Nikoli, Conceptis, GM Puzzles, Cracking the Cryptic / `Glossary_of_Sudoku`, KrazyDad, Puzzle Baron, `Category:Logic_puzzles`.
- **hidden-deduction**: варіанти сапера (14 Minesweeper Variants, Hexcells-подібні, Tametsi, itch `tag-minesweeper`), Battleship/Mastermind на сітці, Voltorb Flip-подібні, `Category:Deduction_board_games`, memory-ігри на сітці, Steam тег Minesweeper.
- **chess-abstract**: `List_of_chess_variants`, `Category:Chess_variants`, `Shogi_variants`, `Abstract_strategy_games`, `Connection_games`, `Tafl_games`, `Mancala`, `Go_variants`; Ludii, BoardSpace, Mindsports, iggamecenter, nestorgames, Project GIPF; Steam-пошук chess roguelike / chess variant.
- **tactics**: `Category:Turn-based_tactics_video_games`, `Tactical_role-playing_video_games` (клітинні/гексові), гекс-варгейми, SRPG консолей, інді-тактики, настільні тактики (Heroscape, Memoir '44, Summoner Wars, Neuroshima Hex), Steam теги Turn-Based Tactics + Hex Grid / Grid-Based Movement.
- **roguelike**: RogueBasin, 7DRL за роками (itch `7drl-challenge-20xx/entries`), `Category:Roguelike_video_games`, Steam тег Traditional Roguelike, broughlikes, `Category:Mystery_Dungeon`, Magic Tower-родина, Pixel Dungeon-форки (`github.com/topics/pixel-dungeon`), coffee-break роглайки, японські.
- **tower-lanes**: `Category:Tower_defense_video_games`, Steam тег Tower Defense + Grid-Based (mazing), `Category:Plants_vs._Zombies` і клони, автобатлери (гекс / 1D), карткові з полем (Duelyst, Faeria, Clash of Heroes, Marvel Snap), lane-бійки.
- **build-sim**: `Category:City-building_games`, `Construction_and_management_simulation_games`, `Agricultural_simulation_video_games`, `Cellular_automata`; Steam теги Automation / Base Building / Colony Sim на сітці; ферми; інвентар-сітки «витягти».
- **program-robots**: `Category:Programming_games`, Steam тег Programming, Zachtronics каталог, змагання ботів на сітці (Screeps, Battlesnake, Halite, Battlecode, CodinGame), Robozzle, Manufactoria, Cargo-Bot, Turing Complete, Logic World, Robo Instructus, Untrusted, Carnage Heart, Robot Odyssey, ComputerCraft; Thinky-теги programming / zachlike / engineering.
- **connect-rotate**: клони Pipe Mania і Flow Free, Infinity Loop-родина, лазери й дзеркала, шляхові плитки (Tsuro, Indigo, Tantrix, Trax, Metro), залізниці на сітці, шестерні й обертання, схеми (Wired, Electric Box, Circuit Scramble); Thinky-теги line-drawing / beam-reflection / sequencing.
- **board-digital**: `Category:Tile-based_board_games`, `Board_games_introduced_in_<рік>` (фільтрувати сіткові), roll-and-write на сітці, поліоміно, гекс-викладання, сіткові абстракти (двобої → chess-abstract), каталоги BGA, Yucata, UltraBoardGames.
- **word-number**: `Category:Word_games`, `Word_puzzle_video_games`, клони Wordle, NYT Games, `Category:Crosswords` (cryptic, codeword, arrowword, crossnumber), Scrabble-подібні, LinkedIn-ігри, Puzzmo (сайт блокує агентів), Apple Quartiles, числові (Mathler, Nerdle, Number Match, Cross Sums); Thinky-теги word / daily.

## Thinky Games — дамп через Chrome і агенти дампу

Thinky Games (`thinkygames.com`) — найбагатший каталог сучасних головоломок, але агентам віддає 403; відкривається в Chrome користувача (Claude in Chrome). Процес хвилі 3: `sitemap-games.xml` → 1290 slug-ів; фонова JS-задача в сторінці сайту збирає сторінки ігор (og:title, опис, теги `(@tag)`, дата) з паузами, щоб не ловити 429; куратор фільтрує дамп проти `index/known-names.txt` і ріже на зрізи по ~90 рядків (TSV: `сімʼя-підказка · slug · назва · рік · теги · опис · ≈можливий дубль`) для 3–5 агентів дампу.

Агент дампу працює за цією ж інструкцією з відмінностями: (1) дедуп ще раз через `known-names.txt` і `grep -ril` по корпусу — сиквели й DLC часто вже лежать підрозділами; (2) відсіює не-сіткові ігри (first-person 3D, фізичні, карткові без поля, сортувальні без сітки, текстові, DLC/перевидання/збірки, книжки головоломок без цифрової версії); (3) для кожної гри знаходить і **відкриває** сторінку Steam / itch / PuzzleScript (сирець — gist API) / Wikipedia — без відкритої сторінки рядок не пише, URL Thinky в рядок не кладе; (4) темп ≈1–2 хв на гру, ≤2 WebFetch на гру, WebSearch ≤30 на агента, ліміт 90 хв на зріз — що не встиг, перелічує у звіті назвами; (5) файл `queue/<хвиля>/thinky-dump-N.md` того самого 7-колонкового формату + секція `## Пропущено` (`назва — причина`).
