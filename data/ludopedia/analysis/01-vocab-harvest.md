# 01 · Жнива словників — перший прохід

`2026-11-02` · корпус на момент проходу: **114 ігор** (фінально — 275; усі пороги лише зросли, живі числа — в індексі), 1500+ рядків `proposes` · джерело чисел — [index/proposals.md](../index/proposals.md) і [index/mechanics.md](../index/mechanics.md) (автоген, свіжіші за цей файл). Поріг — правило трьох (T98): слово підтверджене, якщо його незалежно попросили ≥3 ігри. 🔥 = підтверджено корпусом; рішення «в код» — за Vitalik.

## Висновок одним абзацом

Граматика КОЛИ→ЯКЩО→ТО витримала сотню різнорідних ігор: середнє покриття структурою 70 % (від 55 % у TD з бідними джерелами до 90 % у Sokoban-подібних). Словник у коді (2 тригери · 0 умов · 15 ефектів · 5 ролей) замалий приблизно втричі: корпус стабільно просить **~15 тригерів, ~12 умов, ~35 ефектів, ~15 ролей**, і майже все це — слова, які були в ⏳-кандидатах від початку. Нових, непередбачених слів небагато й вони купчасті: вибух із формою, котіння, «поле осіло», «покласти з запасу», «відгук на спробу», аварія програми. Окремо корпус показав три **структури, яких у граматиці нема**: фази тіку, таблиця станів сутності, декларативні обмеження пазлів — про них у `05-rules-system.md`.

## Тригери — КОЛИ

| 🔥 слово | ігор | що означає | у код? |
|---|---|---|---|
| `input(action)` | 33 | гравець зробив дію (клавіша, клік, свайп, drag) | **так** — без нього не описати жоден хід гравця |
| `counter(name, op, n)` | 12 | лічильник досяг | так |
| `pattern(shape)` | 9 | на полі склався шаблон: лінія N, група N, повний ряд, замкнена область, форма будівлі | так, з підсловником форм |
| `enter(a, cell_type)` | 6 | став на клітину типу (лід, вода, конвеєр) | так — пара до `contact`, друга сторона — шар підлоги |
| `settled` | 6 | поле стабілізувалось після падінь/каскадів — кінець ланцюга, момент сміття | так (сімʼя падаючих) |
| `all_constraints_met` / `constraint_broken(c)` | 6 / 4 | пазл розвʼязано / порушено обмеження | так — єдиний спосіб описати клас `puzzle` |
| `turn_end(side)` | 4 | кінець ходу сторони | так |
| `repetition(n)` | 4 | позиція повторилась N разів (нічия, ко) | ⏳ — фігурні |
| `line_of_sight(a, b)` | 4 | бачить по прямій без перешкод | так |
| `blocked(a)` | 4 | рух неможливий (упор) — вісь «що робить ворог, впершись» | так |
| `exec(cmd)` · `program_end` | 4 / 3 | програма виконує команду / завершилась | ⏳ — лише `program-robots` |
| `locked` | 3 | фігура зафіксувалась (Tetris lock) | ⏳ — дитина `settled` |
| `check(side)` | 3 | король під ударом | ⏳ — фігурні |
| `phase_start(phase)` | 3 | почалась фаза тіку (вогонь → середовище → вороги) | так — див. структура «фази» в 05 |

## Умови — ЯКЩО (словник у коді порожній)

| 🔥 слово | ігор | у код? |
|---|---|---|
| `free(cell)` | 13 | **так** — умова штовхання/руху |
| `state(a, s)` | 11 | так |
| `same(a, b, prop)` | 11 | так — злиття/збіг за кольором чи значенням |
| `has(a, item)` | 8 | так — ключі, черевики, ресурси |
| `facing(a, dir)` | 8 | так |
| `in_range(a, b, n)` | 6 | так |
| `adjacent_count(cell, kind, op, n)` | 5 | так — Life, сапер, Letterpress |
| `count(kind, op, n)` | 4 | так — макс. на полі |
| `path_exists(a, b)` | 4 | так — Lines 98, Quoridor, TD-лабіринти |
| `connected(set)` | 4 | так — усі острови/труби звʼязані |
| `in_dictionary(word)` | 4 | ⏳ — словесні |
| `in_check(side)` · `supported(a)` | 3 / 3 | ⏳ |

Рекомендований стартовий словник умов у коді: `free · state · same · has · facing · in_range · count · adjacent_count · path_exists · connected` (10) + `not`/`and`.

## Ефекти — ТО (у коді 15)

| 🔥 слово | ігор | примітка |
|---|---|---|
| `set_state(a, s, dur?)` | 15 | режими, стани toggle-стін, щит |
| `move(a, dir|to)` | 13 | найчастіший «ТО» руху |
| `set_cell(cell, type)` | 12 | земля → підлога, popup → стіна |
| `place(entity, cell)` | 10 | **нове**: гравець кладе з запасу/руки (го, Hive, Blokus, дроп у шогі); відрізняти від `spawn_at` (система) |
| `rotate(a, deg)` | 10 | плитки, дзеркала, фігури |
| `fall(a)` · `roll(a)` | 9 / 5 | гравітація; `roll` **нове** — скочується з округлого |
| `counter(name, ±n)` | 8 | ходи, поштовхи, ресурси |
| `slide(a, dir)` | 8 | ковзання до упору |
| `spawn_at(entity, where)` | 8 | уточнення `spawn` — де саме |
| `reveal(cells)` · `mark(cell, v)` | 7 / 5 | приховані поля й пазли |
| `take(a, item)` · `give(a, item)` | 6 / 3 | інвентар у обидва боки |
| `explode(area, into?)` | 5 | **нове**: вибух з формою (хрест N, 3×3) і продуктом (діаманти, порожнеча) |
| `speed(a, ±n)` · `stun(a, n)` | 5 / 3 | темп |
| `shift(row|col|all, dir)` · `wrap(a)` | 4 / 4 | зсув рядів, тор |
| `face(a, dir)` · `lives(±n)` · `hp(a, ±n)` · `heal` | 4 / 4 / 3 / 3 | |
| `send_garbage(n)` | 4 | **нове**: versus-пазли — сміття супернику |
| `clear(cells)` · `merge(a, b→c)` · `swap(a, b)` | 4 / 3 / 3 | match/merge |
| `feedback(guess)` | 4 | **нове**: відгук на спробу (кольори Wordle, чорні/білі Mastermind) — дані для дедукції, не `message` |
| `choose(options)` | 3 | гравець обирає (апгрейд, промоція) |
| `throw(a, n)` · `carry(a, b)` · `pull(b)` | 3 / 3 / 3 | кинути через перешкоди; везти на собі (колода, платформа); тягнути |
| `set_value(a, v)` · `timer(start|stop)` · `message(text)` · `crash(text)` | 3 кожен | `crash` **нове** — аварія програми, не `lose` |

Рекомендований набір у код (другий ешелон після наявних 15): `set_state · move · set_cell · place · rotate · fall · slide · counter · spawn_at · reveal · mark · take · give · explode · speed · shift · wrap · face · lives · hp · clear · merge · swap · feedback · choose` (25). `roll · send_garbage · throw · carry · pull · stun · crash · set_value` лишаються ⏳ до реальних робіт студентів.

## Ролі сутностей (у коді 5)

`terrain` ×18 · `zone` ×13 · `tile` ×12 · `hazard` ×9 · `container` ×7 · `boss` ×7 · `projectile` ×7 · `gate` ×7 · `mark` ×5 · `resource` ×4 · `spawner` ×4 · `switch` ×3 · `neutral` ×3 · **нові**: `supply` ×3 (запас/рука/резерв поза полем — го, Blokus, Crazyhouse), `source`/`sink`/`conduit` ×3 (джерело, приймач, провідник — connect-rotate).

Рекомендація: `terrain · tile · zone · hazard · gate · switch · container · spawner · projectile · boss · mark · resource · supply` — 13 нових ролей у код; `source/sink/conduit · neutral · ally · piece` — ⏳. Зауваження: `tile` і `mark` — ролі для класів `cursor`/`puzzle`, де «сутність» — плитка чи розмітка; без них таблиця сутностей цих класів не заповнюється.

## Вікна, HUD, фічі

- Вікна 🔥: `map-window` ×10 · `mode-select` ×6 · `character-select` ×5 · `inventory-window` ×4 · `level-password` ×4 · `code-editor` ×4 · `stats-window` ×3 · **нове** `attract-demo` ×4 (аркадний demo-екран «гра сама грає» — гарний приклад вікна без вводу).
- HUD 🔥: `move-counter` ×6 · `conflict-highlight` ×4 · `energy-bar` · `inventory-bar` · `next-tile-preview` · `path-preview` ×3 · **нові** `pocket` ×3 (рука/взяті фігури: шогі, Crazyhouse), `instruction-highlight` ×3 (поточна команда програми), `action-text` ×3.
- Фічі 🔥: `undo` ×6 · `world-map` ×5 · `custom-rules` ×4 · `meta-progression` · `mode-coop` · `auto-check` · `stars-rating` · `streaks` ×3 · **нові** `skip-level` ×3, `operator-settings` ×3 (DIP-перемикачі автомата: життя, пороги — «налаштування власника», не гравця), `share-result` ×3 (поділитись результатом емодзі-сіткою).
- Осі 🔥: `control` ×16 (direct / indirect / programmed / swipe-all / drag-path / grab-throw) · `session` ×14 · `undo` ×13 · `actors` ×7 · **нові** `gravity` ×5 (none / down / up / per-type / toward-center) · `turn-structure` ×4 (по черзі / трек часу / одночасно / WEGO).

## Картки каталогу — найчастіші прогалини

| `+картка` | ігор | зона | коментар |
|---|---|---|---|
| `undo-redo` | **21** | game-logic/save або interface/input | у каталозі лише `editor-undo`; це найбільша прогалина корпусу |
| `chain-reaction` | 7 | game-logic/score | каскади match-3, ланцюги Puyo, детонації |
| `wrap-edges` | 7 | entities/legality | тор: Pac-Man тунель, Life, Labyrinth |
| `move-notation` · `seed-share` · `world-map` | 5 | interface / levels | запис ходів; поділитись seed; мапа світу як прогресія |
| `cascade-gravity` · `garbage-attack` · `line-match-clear` · `next-queue` · `connected-group-pop` | 3–4 | entities/state, game-logic/opponent | сімʼя падаючих блоків майже не представлена в каталозі |
| `dig-terrain` · `roll-off-rounded` · `wall-follower` · `one-way-cell` · `carrier-platform` | 3–4 | entities/* | Boulder Dash-лінія і типи клітин |
| `code-editor-window` · `command-program` · `step-execution` · `sensor-predicates` · `user-procedures` | 3–4 | нова підзона? | program-robots — цілий клас, якого в таксономії нема |
| `edge-marking` · `single-loop-check` · `multi-select` · `line-sum-clue` · `neighbor-count-clue` · `no-guess-generation` | 3–4 | game-logic/constraints, interface/input | пазли: розмітка ребер, перевірка однієї петлі, підказки-суми |
| `move-limit` · `extra-life-threshold` · `leftover-penalty` · `pass-turn` · `pawn-promotion` · `piece-drop` · `piece-rotate-flip` · `tile-rotate` · `simultaneous-versus` · `share-result` · `streak-stats` · `word-validation` · `level-password` | 3 | різні | дрібніші, але стабільні |

Повний список з іграми — [index/mechanics.md](../index/mechanics.md) (секція «Нові»). Пропозиції карток з зоною/монеткою/слотами — у секції «Мапа на каталог» кожної гри; зведення в картки — `03-catalog-gaps.md`.

## Що це означає для коду (пропозиція порядку)

1. Умови: завести словник `CONDITIONS` (10 слів) і UI «ЯКЩО» у `RuleRow` — найбільша віддача, бо без умов половина правил корпусу пишеться як `custom`.
2. Тригери: +8 (`input · enter · counter · pattern · settled · turn_end · blocked · line_of_sight`) + пара для пазлів.
3. Ефекти: +25 другого ешелону; `spawn`/`transform` отримують аргумент `where`.
4. Ролі: +13.
5. Картка `undo-redo` в каталог одразу (21 гра).
6. Структури поза граматикою (фази, стани, обмеження) — окреме рішення, `05-rules-system.md`.
