# T265 · Лудопедія: хвиля 3 — нові кандидати й описи — звіт

`2026-11-09` · ⚙️ задача · [план](plan.md) · запит Vitalik у чаті (нічна автономна сесія, max-ефорт) · попередня хвиля — [T260](../T260--ludopedia-wave2/report.md) · вибори — [T266](../T266-Q--ludopedia-wave3-choices.md) (нові) і [T264](../T264-Q--ludopedia-wave2-choices.md) (Q5a і Q7a прийнято як «a» і виконано) · **хвиля не завершена** — зупинена тижневим лімітом Opus; точка продовження нижче і в `data/ludopedia/analysis/07-wave3-curator-notes.md`

## Що зроблено

- **Інструменти** (крок 1): `scripts/known_names.py` → `index/known-names.txt` (усі назви корпусу й черг, 4780 → 8187 рядків — дедуп для пошукових агентів); `scripts/queue_merge.py` (злиття `queue/<хвиля>/*.md` у черги сімей з відкиданням дублів; для нього `queue_status.described()` віддає ще `full`-назви); інструкція пошукового агента (`queue/_search-brief.md`) і агента дампу Thinky; бриф описувача — `AGENT-BRIEF.md` v1.3; батчер `scripts/make_batches.py` (у репо після хвилі — з `maybe`-рядками).
- **Пошук** (крок 2): 17 Opus-агентів по сімʼях → 7-колонкові файли `queue/wave3/*.md` → `queue_merge.py wave3 --apply` **+733 рядки** (4 відкинуто хибно через колізії alias — повернуто руками: Zoo Keeper Taito, [the Sequence], Ice path; Lights Out не був у чергах — додано). Thinky Games (агентам 403) знято через Chrome: сайтмап 1290 ігор → 445 невідомих → 5 агентів дампу перевірили кожну у Steam/itch/PuzzleScript → **+308 рядків**. Разом черги 1150 → **2265 (+1041)**. Найпродуктивніші джерела: Wikipedia API `categorymembers`, JA-Wikipedia, RogueTemple, Steam-теги, itch-джеми, puzz.link/Janko.
- **Описи** (крок 4): **956 → 1663 ігор (+707)** — 148 пачок по ≤5 (D 12 · E 7 · F 65 · G 53 · H 11), до 20 Opus-агентів одночасно, лінт 0 після кожної; два огляди доповнені підрозділами (Renban; Sandwich + Miracle), нові огляди для сиквелів і родин (`fairy-chess-conditions`, `shogi-rule-twists`, `tetris-worlds`…). **Зупинено о 08:46**: усі 20 пачок у роботі (G052, G053, G056–G061, G063–G074) впали з HTTP 429 «weekly limit · resets 1pm» — встигли записати 10 повних файлів (paklyx, temple-of-snek, wildfire-swap, wormspell, sprouts, pipeline-capstone, railway-islands, sunken-stones, below-the-crown, myth-bearer; лінт 0, 13 секцій, 8–20 правил), решта їхніх рядків і 56 незапущених пачок лишились у чергах.
- **Прогалина конвеєра закрита**: `queue_status.py` позначає `maybe` рядки зі схожою назвою (65 у хвилі 3 — майже всі хибні збіги: Battle Sheep ≈ battleship, Loopz ≈ slitherlink…), а батчер їх не брав — зроблено префікс H з ⚠-підказкою (11 пачок виконано, збіги хибні крім 4 покритих), і `make_batches.py` у репо тепер включає `maybe` завжди.
- **T264 Q5a**: 21 рядок черг виправлено (роки, описи, лінки з нотаток хвилі 2) з позначкою `✔ виправлено 2026-11-09`.
- **Після зупинки** (кроки 5–6): лінт 0 на 1663; індекси (`build_index`, `harvest`, `card_examples` — 333 картки × 26 168 прикладів, `rule_words` — КОЛИ 2,5 % · ЯКЩО 6,3 % · ТО 8,4 %, `queue_status`, `known_names`); імпорт у локальну базу й смоук; доки — README корпусу («Стан», «Структура»), `analysis/07-wave3-curator-notes.md` + рядок в `analysis/README.md`, `.dev/games/README.md`, CHANGELOG, Q-тікет [T266](../T266-Q--ludopedia-wave3-choices.md), STATUS (жест агента), памʼять (тижневий ліміт Opus посеред хвилі); коміти локально, без push.

## Що перевірено

- `scripts/lint.py` — 1663 файлів · 0 проблем; усі скрипти `scripts/` відпрацювали на повному корпусі; `make_batches.py` з репо генерує пачки з `remaining` і `maybe`.
- Файли зірваних агентів: mtime і лінт — записані одним Write і повні; часткових або битих файлів нема (агенти пишуть файл одним заходом, лінт — після).
- `ludopedia_io.py import --prune` і `smoke_ludopedia.py` — результат у секції нижче (числа — у STATUS і CHANGELOG).
- Сервер не чіпався; GitHub — нічого не пушено.

## Де зупинились і як продовжити

- Лишилось **308 рядків (п1 9 · п2 163 · п3 136) + 23 `maybe`** — `data/ludopedia/index/queue-status.md`; найбільше push-slide 100 · thinky 83 · pencil-logic 45 · program-robots 19 · word-number 18. З девʼяти п1 реально нових сім (Лабиринт, Croquet Conundrum, Vext Edit, Tres Undos, 0PLAYER, Triga, Балда); «Шашки» покриті `checkers*.md`, Thiruthamizh — без джерела правил.
- Рецепт: `queue_status.py` → `make_batches.py 1 20 --prefix I --out <скретчпад>` → кожен промпт у `Agent(general-purpose, model=opus)`, ≤20 одночасно, наступна пачка — на нотифікації; після кожних ~30 пачок лінт → індекси → коміт; у кінці `import --prune` + смоук. Оцінка: 73 пачки / 327 рядків (перевірено батчером) ≈ 13 млн токенів агентів ≈ 1,5 год при 20 паралельних. Повний список команд — `analysis/07-wave3-curator-notes.md`, секція «Де зупинились».
- Перед стартом — глянути залишок тижневого ліміту Opus; хвилю різати порціями.

## Рішення і спостереження

- Thinky Games через Chrome (Claude in Chrome + `get_page_text`/JS у вкладці) — єдиний спосіб дістати цей каталог; 1290 ігор, ≈ 25 хв дампу з паузами. Слім-список ще не перевірених назв — `queue/_thinky-dump-2026-11-09.tsv`.
- Пошук по сімʼях з дедупом через `known-names.txt` дав 733 рядки майже без дублів (злиття відкинуло 4, і ті хибно); каталоги через Wikipedia API вигідніші за точкові WebSearch у десятки разів.
- Тижневий ліміт Opus вичерпується масовою хвилею за кілька годин; падіння не псує файли, але губить пачки. Нотифікації обіцяють продовження агента через `SendMessage` — лише в тій самій сесії, тому леджер і батчер тепер у репо, а не в скретчпаді.
- Агенти без підказки переносять гру в правильну сімʼю, пишуть огляди для сиквелів і коротко — для межових ігор без сітки (`field: free/graph/1d/nested`); ≈ 20 нових межових файлів і 5 пропозицій нових значень осей — [T266](../T266-Q--ludopedia-wave3-choices.md) Q4.
- Шість сторінок tcrf.net містять prompt-injection — агенти проігнорували; правило в брифі v1.3.

## Чекає Vitalik

- Відповіді [T266](../T266-Q--ludopedia-wave3-choices.md) Q1–Q9 (мовчання = a) і далі [T264](../T264-Q--ludopedia-wave2-choices.md) / [T258](../T258-Q--ludopedia-corpus-choices.md).
- Погляд на `/ludopedia` у деві (admin) і 2–3 файли хвилі 3 на якість.
- Push і деплой з перезапуском API; на сервері — `ludopedia_io.py import --prune`.
- У `.dev/STATUS.md` у «Зараз» лишився артефакт «--help» від `dev status --help` — рядок користувача, я не чіпав (T266 Q9).
