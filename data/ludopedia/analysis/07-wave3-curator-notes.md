# Нотатки куратора — хвиля 3 (Fable, сесія 2026-11-09, T265)

Третя ніч: нова хвиля пошуку кандидатів з усіх джерел і описи тим самим конвеєром, що в хвилі 2. Підсумкові числа — в `index/README.md` і звіті [T265](../../../.dev/games/.t/T265--ludopedia-wave3/report.md); вибори — [T266](../../../.dev/games/.t/T266-Q--ludopedia-wave3-choices.md). На момент зведення — **1663 ігор** (956 → 1663 за ніч), черги **2265 рядків** (+1041), з них не описано **308 + 23 `maybe`**. Хвиля **не завершена**: о 08:46 усі 20 пачок у роботі впали з HTTP 429 «тижневий ліміт Opus»; що саме лишилось і як продовжити — секція «Де зупинились».

## Де зупинились і як продовжити

- **Виконано** 148 пачок по ≤5 ігор: D001–D012, E001–E007, F001–F065 (F066–F127 перепаковано в G), G001–G051 + G054 + G055, H001–H005, H007, H009, H012, H014, H016, H017 (H = `maybe`-рядки, див. нижче). Лінт 0 після кожної пачки; індекси регенеровано після зупинки.
- **Зірвано лімітом** 20 пачок: G052, G053, G056–G061, G063–G074. Вони встигли записати 10 повних файлів (лінт 0, 13 секцій, 8–20 правил): `thinky/paklyx`, `thinky/temple-of-snek`, `thinky/wildfire-swap`, `word-number/wormspell`, `connect-rotate/sprouts`, `connect-rotate/pipeline-capstone`, `connect-rotate/railway-islands`, `tactics/sunken-stones`, `chess-abstract/below-the-crown` (агент tactics переніс у правильну сімʼю), `roguelike/myth-bearer`. Решта їхніх рядків лишилась у чергах — `queue_status.py` бачить їх як `remaining`, окремого обліку не треба.
- **Не запущено** 56 пачок: G075–G120 і H006, H008, H010, H011, H013, H015, H018–H021. Промпти жили в скретчпаді сесії — перегенерувати (нижче), не шукати.
- **Залишок за `index/queue-status.md`**: 308 рядків (п1 9 · п2 163 · п3 136) + 23 `maybe`. По сімʼях: push-slide 100 · thinky 83 · pencil-logic 45 · program-robots 19 · word-number 18 · connect-rotate 10 (усі п3) · tactics 8 · board-digital 7 · grid-platformer 6 · chess-abstract 3 · roguelike 3 · dig-gravity 2 · hidden-deduction 2 · maze-arcade 1 · tower-lanes 1 · build-sim 0 · falling-match 0. З девʼяти п1 реально нових сім — Лабиринт (паперова гра з ведучим; itch Labirinth), Croquet Conundrum, Vext Edit, Tres Undos, 0PLAYER, Triga, Балда; «Шашки» покриті `checkers.md` + `checkers-variants.md` (автомат не зіставив переклад), Thiruthamizh — без джерела правил (пропущено двічі, D010 і G005).
- **Як продовжити** (після скидання ліміту Opus; батчер з репо дає 73 пачки / 327 рядків ≈ 13 млн токенів агентів ≈ 1,5 год при 20 паралельних):

  ```
  cd data/ludopedia && P=~/.venvs/python-labs/bin/python
  $P scripts/queue_status.py                                   # що лишилось (remaining + maybe)
  $P scripts/make_batches.py 1 20 --prefix I --out "$SCRATCH/ludo"   # пачки ≤5, промпти в stdout, batches-I.json поза репо
  # кожен промпт → Agent(subagent_type=general-purpose, model=opus); ≤20 одночасно, наступна пачка — на нотифікації;
  # леджер пачок — у скретчпаді, але після кожних ~30 пачок: лінт → індекси → коміт (чиста точка зупинки)
  $P scripts/lint.py                                           # 0 проблем
  for s in build_index harvest card_examples rule_words queue_status known_names; do $P scripts/$s.py; done
  cd ../../app/api && uv run python ludopedia_io.py import --prune && DB_NAME=python_labs_smoke uv run python tests/smoke_ludopedia.py
  ```

  Префікси D–H використані; `--skip I1-12` виключає рядки пачок, що ще в роботі, коли перегенеровуєш список. Бриф для агентів — `AGENT-BRIEF.md` v1.1–v1.3 (промпт посилається на нього, окремої інструкції в скретчпаді більше не треба).

## Процес

- **Дедуп списком відомих назв**: `scripts/known_names.py` → `index/known-names.txt` (title/aka/slug корпусу + всі рядки черг; 4780 → 8187 рядків). Пошуковий агент зобовʼязаний `grep` його перед кожним рядком; другий барʼєр — `scripts/queue_merge.py` при злитті (відкидає рядки, які корпус описує, черга вже містить або хвиля повторює; для цього `queue_status.described()` тепер віддає ще й `full` — цілі назви без підчастин).
- **Пошук — 17 Opus-агентів, по одному на сімʼю**, кожен писав ізольований `queue/wave3/<family>.md` (7 колонок: шоста — сімʼя, щоб чужі знахідки не губились; інструкція збережена як `queue/_search-brief.md`). 30–45 рядків на агента, ≤80 WebSearch (ліміт сесії піднято змінною). Злиття `queue_merge.py wave3 --apply` → **+733 рядки** секціями «Хвиля 3 — 2026-11-09»; 4 рядки відкинуто хибно через колізії alias (Zoo Keeper Taito ≈ `falling-match/zoo-keeper`, Ice path Rosden ≈ alias «ice path» у `pokemon-overworld-puzzles`, [the Sequence]) — повернуто руками з уточненими назвами; Lights Out не був у чергах узагалі — додано.
- **Thinky Games — дамп через Chrome** (агентам сайт віддає 403): `sitemap-games.xml` → 1290 slug-ів; фонова JS-задача у вкладці збирала сторінки ігор (og:title, опис, теги, дата) з паузами; фільтр проти known-names → 445 невідомих; 5 агентів дампу (зрізи по 79–105) перевіряли кожну гру у Steam/itch/PuzzleScript і писали 7-колонкові рядки → **+308 рядків**. решту не встигли або відсіяли (не сітка, DLC, збірки) — 145 назв, яких і досі нема ні в корпусі, ні в чергах, збережено слім-списком `queue/_thinky-dump-2026-11-09.tsv` (slug, назва, теги) для наступної хвилі.
- **Описи**: конвеєр T260 без змін — пачки ≤5 рядків (п1 → п2 → п3, round-robin по сімʼях), Opus-агент на пачку, до 20 одночасно, наступна — на нотифікації; лінт після кожної пачки — агентом (свої файли), зведений — куратором. Тимчасові лінт-помилки чужих файлів (`trails-of-tucana`, `trails-purplesloth`, `stonemans-adventure`, `non-euclidean-minesweeper`) власники виправляли самі — у фіналі 0. Жодного дубля slug: правило «`ls` теки перед записом» працює; агенти самі переносили гру в правильну сімʼю (below-the-crown → chess-abstract) і писали огляди для сиквелів.
- **Ліміт Opus**: ~150-та пачка хвилі вичерпала тижневий ліміт підписки — 15 агентів упали з «You've hit your weekly limit · resets 1pm», 5 — з «would exceed your account's rate limit». Нотифікації обіцяли продовження через `SendMessage` у тій самій сесії; сесія тим часом стиснулась, і Vitalik попросив поставити крапку. Урок — у [T266](../../../.dev/games/.t/T266-Q--ludopedia-wave3-choices.md) Q2: перед хвилею з >50 пачок дивитись залишок ліміту, різати хвилю порціями з чистою точкою зупинки (лінт → індекси → коміт).
- **T264 Q5a** виконано тут же: 21 рядок черг виправлено (роки, описи, лінки з нотаток хвилі 2) з позначкою `✔ виправлено 2026-11-09`.

## Прогалина `maybe` — закрита

`queue_status.py` ставить `maybe` рядкам зі схожістю назви ≥0,8 до slug корпусу, а батчер брав лише `remaining` — тож у хвилях 2–3 такі рядки взагалі не потрапляли в пачки (у хвилі 2 їх перебирали руками → пачки M). У хвилі 3 — 65 рядків, майже всі хибні збіги (Battle Sheep ≈ battleship, Loopz ≈ slitherlink, Lights Out ≈ lightbot, Penultima ≈ baroque-chess…). Зроблено префікс H (21 пачка, 66 рядків, кожен з ⚠-підказкою «автоматика сплутала з `сімʼя/slug` — спершу відкрий той файл»); 11 виконаних H-пачок підтвердили: усі збіги хибні, крім чотирьох справді покритих (Tetris 99 → `tetris`, Bejeweled Twist і Bejeweled 1–3/Blitz → `bejeweled`, Back to the Roots 2 → `mazing-td-modern`). Тепер `scripts/make_batches.py` (у репо) включає `maybe`-рядки з тією ж підказкою — окремої ручної звірки більше не треба. Інші слабкості `queue_status`: не зіставляє перекладені назви («Шашки», «Піддавки», «Балда») і вважає описаною гру, чия назва збігається з alias іншої (Zoo Keeper Taito) — такі рядки варто перейменовувати в чергах з уточненням у дужках.

## Джерела

- **Працювало**: Wikipedia API `categorymembers` (сотні назв за запит), JA-Wikipedia (`落ち物パズル` — найкраще для falling-match), RogueTemple (огляди 7DRL), Steam-теги й пошук, itch-джеми (Thinky Puzzle Game Jam, 7DRL), puzz.link `list.html` + `pzpr-samples/<id>.js`, Janko, RulesPal / UltraBoardGames, archive.org (OCR мануалів), Steam JSON `api/appdetails?appids=` (коли сторінка віддає 429) і Steam News API, сирці ігор (PuzzleScript через gist API; PICO-8 картриджі — Lua з `.p8.png`; Godot `.pck`; GitHub), PDF правил через `uv run --no-project --with pypdf` (pypdf нема у venv).
- **Не відкривається**: Thinky Games (403 — лише Chrome), BGG (HTML 403, XML API тепер 401), chessvariants.com, TouchArcade, Gamezebo, Pocket Tactics (403), puzzmo.com, steamcommunity (429), Steam `appreviews` через curl (редірект на головну).
- **Prompt-injection**: шість сторінок tcrf.net (JezzBall, Q*Billion, Logical (Amiga), Live Wire! (Windows), The Brainies (SNES), Amazing Penguin) містять текст «інструкцій для ШІ» — усі агенти проігнорували; правило додано у бриф v1.3.

## Помилки черг, знайдені агентами (для T266 Q7; рядки не правились)

- Роки: Six Match 2017 · 2248 2018 · Duplicate Scrabble 1972 · Hurkle 1973 · Quasimorph 2023 (EA; 2026 = 1.0) · Monocre 2013 (Steam 2026 — перевидання) · Strata 2013 (iOS) · Nekograms 2021 · One More Button 2018 (iOS; itch-лінк — інша гра) · Equate 1996 · Triolet 1996 (?) · Yushino 2012 · Keyword 2023 · Domino Grove 2024 · Hexanaut 2022 · Stamps 2025 · SlideMaze 2024 · DROD RPG 2008 · Murdoku 2020 · Hot Springs Story 2009 · Fort Triumph 2020 (повний реліз) · Bokosuka Wars 1984 · X2 Blocks 2019 · Subterrarium 2016 · Dig Dig Boom — Steam каже 2027/TBA · generals.io 2016 · Diaballik 2002 · TZAAR 2007/08 · Trike 2020 · Barca 2007 · Pipelink 1993 · Stomp! 2021 · Kuralin 2025 (Nikoli 191) · Slider — джем 2021, 1.0 2024 · Bumpy 1989 (Bumpy's Arcade Fantasy 1992 — ремейк) · Stackrobats 2026 · A Short Bike 2025 · worDefense 2023 · Ice path 2018 · Zahlenlabyrinth 2008 · Zeiger ≥2007 · Sequence — рік не підтверджено.
- Неточні описи: Tashikani (сегмент зливається у блок суми, а не зникає) · Takoron (восьминоги збігаються між собою, куля лише несе число) · Overwords · Tinkle Pit (одна куля + лінія) · Dungeon Twister (одна кімната за AP) · Ticket to Earth (шлях — будь-який один колір, не «свій») · Bahamut Lagoon (3 накази дракону) · A-Train (рядок змішує головоломку 1985 з механіками A-Train III 1990 — файл написано як огляд серії) · Setris ≠ Sandtrix (окремий клон, в aka) · The Miner Was Replaced — DLC, не сиквел · Uno Free Fall (Java 2008) має правила SameGame · The World Next Door (руна береться і кидається, не торкається) · Hot Springs Story «згасання з відстанню» не підтверджено (лише зона 5×5) · Continuo — правило збігу кольорів не підтверджено · Blobun «гамільтонів» не підтверджено · HCC — пул AP на гравця · NoGo — джерела авторства суперечать · Wyrmspace Tactics — не вийшла.
- Хибні лінки: Fibble ⭐ → бенчмарк FibbleArena (гра — fibble.xyz) · Block in the Lock «інший» (app/2598490) = ColorCoordination · AutomaticBox ⭐ = id демо · QoS2 «інший» = фанатська версія QoS1 · `W:Three_Musketeers_(game)` → редірект на «A Gamut of Games» · generals.io ⭐ 1v1guide — стратегія, не правила (краще arXiv 2507.06825) · Underworlds ⭐ — правила поточного видання, а рядок про 2017 · Boulder Dash Construction Kit ⭐ — сторінка категорії · Janko: індекс Arofuro підписаний чужою JA-назвою · Rat King знайдено на itch (torcado) · Remembered Length — автор Palmer Mebane · репозиторії NLE/MiniHack переїхали (heiner/nle, samvelyan/minihack) · Encore! 2017 = аркуші-розширення Noch mal (DE-wiki).

## Помилки корпусу (для T266 Q5)

- `maze-arcade/hunt-the-wumpus.md` (рядки ≈93/96): Hurkle дає напрямок, а не відстань — відстань дає Mugwump.
- `hidden-deduction/mr-jack.md`: Mr Jack Pocket подано як мобільну адаптацію — це окрема настілка 2010.
- `thinky/order-of-the-sinking-star.md`: автор Enigmash — Jack Lance, не «Zach Polansky».
- `maze-arcade/snake.md`: відносить Snake Pass до thinky (черга мала її в maze-arcade; гра без сітки — пропущено).
- `word-number/letterpress.md`: «бомби» Wordbase не підтверджені джерелами.
- alias `number sums crossword` → `crossmath` сумнівний (Number Sums ≈ варіант Sumplete); `markov-alg.md` описує іншу гру (Fewjix 2019), A=B — окремий файл.
- Словник коду: `draw` = «нічия», агенти для взяття карти пропонують `draw_card` (також `discard`, `shuffle`) — питання синонімії для `vocab.py` (T266 Q6).

## Межові ігри й нові значення осей (для T266 Q4)

- Написані коротко як межа сімʼї (`field: free/graph/1d/nested/tube`): Maxwell's Puzzling Demon (вкладені рівні, `also: [thinky]`), Tricone Lab (граф), Teardown, Tempest (1d), Castle Wolfenstein, Spirit Island, Unmatched (граф), Word Factori (граф), CIPHER ZERO (граф), Prime Mover (nested), Bad Hotel, The Snake Is the Tower, Zoo Keeper Taito (1d), tricky-tangled-train-tracks, Cataclismo, Startopia (cov 30), Pixel Miner, Top Secret Spies, Geistertreppe, QoS2 і Rat King (cov 30).
- Пропозиції значень осей, яких лінт не знає: `rules: unlocked / switchable` (правила відкриваються або перемикаються по ходу гри), `field: pyramid / tri / tube`, `opponent: live` (жива людина онлайн у реальному часі), `info: asymmetric`, нова вісь `signal` (ігри про передачу сигналу/хвилі). Агенти пишуть їх як `+axis:` у «Пропозиції» (бриф v1.3).
- Огляди й підрозділи замість нових файлів: Renban → `sudoku-line-dot-variants`; Sandwich + Miracle → `sudoku-variants`; UDLR_Modify → `clovers-quadrants`; Kyoto + Annan → `shogi-rule-twists`; Andernach + Madrasi + Grid → `fairy-chess-conditions`; Tetris Worlds — окремий файл режимів; 4D Intuition → `4d-sokoban`; Circe, Rift, ufo-enemy-unknown (≠ xcom), The Miner Was Replaced (DLC) — окремі файли за рішенням агентів.

## Пропущено свідомо

Thiruthamizh (двічі — жодного джерела з правилами), Wyrmspace Tactics (двічі — не вийшла), Gridvania (нема правил), Daedalike (пʼять речень на itch, джем ≈2019), Photon Engineer (first-person 3D без сітки), Snake Pass і Mosa Lina (без сітки), Boulder Dash Construction Kit (редактор уже в `boulder-dash.md`), «Шашки» і «Піддавки» (покриті `checkers*.md`), Zebra, Bejeweled 1–3/Blitz, Tetris 99, Bejeweled Twist, Back to the Roots 2 (покриті наявними файлами).

## Питання до Vitalik — [T266](../../../.dev/games/.t/T266-Q--ludopedia-wave3-choices.md)

Дописувати залишок 308 + 23 рядків чи зупинитись (Q1); як планувати хвилі під тижневий ліміт Opus (Q2); `maybe`-рядки — пачками з підказкою чи руками (Q3); межові ігри й нові значення осей (Q4); правити 6 помилок корпусу (Q5); `draw_card` у словниках (Q6); ≈40 хибних рядків черг хвилі 3 (Q7); решта Thinky-дампу (Q8); артефакт «--help» у STATUS (Q9).
