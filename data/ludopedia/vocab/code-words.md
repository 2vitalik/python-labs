# Слова коду сайту (автоген)

`scripts/code_vocab.py` з `app/api/models/vocab.py` і карток `data/catalog/tasks.yaml` з `opt` · ролей 22 · тригерів 38 · умов 33 · ефектів 65. Це словник форм «Моєї гри» (T259, T270): у корпусі ці слова — ✅ нарівні зі словниками `vocab/*.md`; аргументи — як у шаблоні речення.

## Ролі

| slug | назва | група |
|---|---|---|
| `player` | Гравець 🧍 | Живі |
| `ally` | Союзник 🤝 | Живі |
| `enemy` | Ворог 👾 | Живі |
| `boss` | Бос 👹 | Живі |
| `neutral` | Нейтральний персонаж 🐾 | Живі |
| `segment` | Хвіст / сегмент 🐍 | Живі |
| `object` | Обʼєкт / ящик 📦 | Речі |
| `pickup` | Предмет / бонус 💎 | Речі |
| `projectile` | Снаряд 🔸 | Речі |
| `container` | Контейнер / скриня 🎁 | Речі |
| `resource` | Ресурс 🪙 | Речі |
| `supply` | Запас поза полем 🗃️ | Речі |
| `static` | Стіна / статика 🧱 | Клітини поля |
| `terrain` | Підлога з властивістю 🟫 | Клітини поля |
| `hazard` | Пастка / стихія 🔥 | Клітини поля |
| `gate` | Двері / барʼєр 🚪 | Клітини поля |
| `switch` | Кнопка / важіль 🔘 | Клітини поля |
| `spawner` | Спавнер / генератор 🌀 | Клітини поля |
| `zone` | Зона / область 🟦 | Клітини поля |
| `piece` | Фігура ♟️ | Фігури й розмітка |
| `tile` | Плитка 🔷 | Фігури й розмітка |
| `mark` | Розмітка ✏️ | Фігури й розмітка |

## Тригери — КОЛИ

| slug | речення | аргументи | група |
|---|---|---|---|
| `contact` | контакт А × Б | a:entity, b:entity | контакт |
| `enter` | А стає на клітину Б | a:entity, b:entity | контакт |
| `leave` | А сходить з Б | a:entity, b:entity | контакт |
| `adjacent` | А поруч із Б | a:entity, b:entity | контакт |
| `line_of_sight` | А бачить Б по прямій | a:entity, b:entity | контакт |
| `in_range` | Б у радіусі від А | a:entity, b:entity, n:int | контакт |
| `blocked` | А вперся в перешкоду | a:entity | контакт |
| `reach` | А досяг місця | a:entity, where:text | контакт |
| `edge` | А вийшов за край поля | a:entity | контакт |
| `input` | гравець зробив дію | action:text, a:entity | ввід і час |
| `timer` | кожні N тіків | every:int | ввід і час |
| `tick` | кожен тік |  | ввід і час |
| `idle` | гравець не діє N тіків | n:int | ввід і час |
| `schedule` | за розкладом | list:text | ввід і час |
| `rng` | випадково з ймовірністю | p:int | ввід і час |
| `phase_start` | почалась фаза тіку | phase:text | ввід і час |
| `turn_start` | початок ходу сторони | a:entity | ввід і час |
| `turn_end` | кінець ходу сторони | a:entity | ввід і час |
| `counter` | лічильник досяг | name:text, op:choice:op, n:int | стан і лічильники |
| `hp_zero` | HP А вичерпано | a:entity | стан і лічильники |
| `state_on` | А увійшов у стан | a:entity, s:text | стан і лічильники |
| `state_off` | А вийшов зі стану | a:entity, s:text | стан і лічильники |
| `all_gone` | зникли всі А | a:entity | стан і лічильники |
| `all_on` | усі А на Б | a:entity, b:entity | стан і лічильники |
| `no_moves` | нема легальних ходів | a:entity | стан і лічильники |
| `pattern` | на полі склався шаблон | shape:choice:shape, n:int | стан і лічильники |
| `settled` | поле осіло після падінь |  | стан і лічильники |
| `level_start` | старт рівня |  | життєвий цикл |
| `level_end` | кінець рівня |  | життєвий цикл |
| `wave_start` | старт хвилі |  | життєвий цикл |
| `wave_cleared` | хвилю знищено |  | життєвий цикл |
| `spawned` | зʼявився А | a:entity | життєвий цикл |
| `died` | загинув А | a:entity | життєвий цикл |
| `picked` | А підібрав Б | a:entity, b:entity | життєвий цикл |
| `destroyed` | А знищено | a:entity | життєвий цикл |
| `all_constraints_met` | усі обмеження виконано (пазл) |  | пазли |
| `constraint_broken` | порушено обмеження (пазл) | text:text | пазли |
| `custom` | інше (словами) | text:text | інше |

## Умови — ЯКЩО

| slug | речення | аргументи | група |
|---|---|---|---|
| `free` | клітина вільна | cell:choice:cell | поле |
| `occupied` | у клітині сутність | cell:choice:cell, what:entity | поле |
| `adjacent_count` | кількість сусідів виду | what:entity, op:choice:op, n:int | поле |
| `count` | кількість сутностей на полі | what:entity, op:choice:op, n:int | поле |
| `path_exists` | існує шлях | a:entity, b:entity | поле |
| `connected` | множина звʼязна | what:entity | поле |
| `in_check` | А під ударом | a:entity | хід гри |
| `fits` | фігура вміщується | a:entity, cell:choice:cell | поле |
| `state` | А у стані | a:entity, s:text | стан |
| `has` | у А є предмет | a:entity, item:entity | стан |
| `counter` | лічильник порівняно з N | name:text, op:choice:op, n:int | стан |
| `same` | А і Б однакові за… | a:entity, b:entity, prop:text | стан |
| `facing` | А дивиться у напрямку | a:entity, dir:choice:dir | стан |
| `moving` | А рухається у напрямку | a:entity, dir:choice:dir | стан |
| `in_range` | Б у радіусі від А | a:entity, b:entity, n:int | стан |
| `line_of_sight` | А бачить Б | a:entity, b:entity | стан |
| `turn_of` | зараз ходить сторона | a:entity | хід гри |
| `legal` | хід легальний | text:text | хід гри |
| `level` | номер рівня | op:choice:op, n:int | хід гри |
| `timer` | часу лишилось | op:choice:op, n:int | хід гри |
| `mode` | режим гри | text:text | хід гри |
| `first_time` | вперше за рівень |  | хід гри |
| `chain` | каскад уже N кроків | n:int | хід гри |
| `prob` | з ймовірністю | p:int | хід гри |
| `unique` | усі значення різні | where:choice:where | обмеження пазла |
| `sum` | сума дорівнює | where:choice:where, n:int | обмеження пазла |
| `no_adjacent` | не сусідять | what:entity | обмеження пазла |
| `no_2x2` | нема квадрата 2×2 | what:entity | обмеження пазла |
| `region_size` | розмір області | what:entity, n:int | обмеження пазла |
| `single_loop` | рівно одна петля |  | обмеження пазла |
| `cover_all` | покрито всі клітини | what:entity | обмеження пазла |
| `run_lengths` | довжини блоків за підказкою | where:choice:where | обмеження пазла |
| `custom` | інше (словами) | text:text | інше |

## Ефекти — ТО

| slug | речення | аргументи | група |
|---|---|---|---|
| `disappear` | зникає | a:entity | поява і зникнення |
| `spawn` | зʼявляється | entity:entity, cell:choice:cell | поява і зникнення |
| `spawn_at` | зʼявляється у місці | entity:entity, where:text | поява і зникнення |
| `transform` | перетворюється на | a:entity, into:entity | поява і зникнення |
| `respawn` | відроджується | a:entity, where:text | поява і зникнення |
| `clone` | клонується | a:entity | поява і зникнення |
| `block` | рух не відбувається |  | рух |
| `push` | штовхається | a:entity | рух |
| `pull` | тягнеться | a:entity | рух |
| `move` | рухається на 1 | a:entity, dir:choice:dir | рух |
| `slide` | ковзає до упору | a:entity, dir:choice:dir | рух |
| `teleport` | телепортується | a:entity, where:text | рух |
| `wrap` | переходить через край (тор) | a:entity | рух |
| `swap` | міняються місцями | a:entity, b:entity | рух |
| `rotate` | повертається | a:entity, deg:choice:deg | рух |
| `fall` | падає | a:entity | рух |
| `bounce` | відбивається | a:entity | рух |
| `face` | розвертається | a:entity, dir:choice:dir | рух |
| `shift` | зсув ряду / поля | axis:choice:axis, dir:choice:dir | рух |
| `stun` | завмирає на N тіків | a:entity, n:int | рух |
| `speed` | змінює швидкість | a:entity, n:int | рух |
| `attach` | зчіплюється | a:entity, b:entity | рух |
| `damage` | шкода | a:entity, n:int | стан і числа |
| `heal` | лікування | a:entity, n:int | стан і числа |
| `lives` | ± життя | n:int | стан і числа |
| `score` | ± очки | n:int | стан і числа |
| `currency` | ± валюта | n:int | стан і числа |
| `counter` | ± лічильник | name:text, n:int | стан і числа |
| `set_value` | встановити значення | a:entity, v:text | стан і числа |
| `multiplier` | множник очок | k:int | стан і числа |
| `set_state` | увімкнути стан | a:entity, s:text, dur:int | стан і числа |
| `clear_state` | зняти стан | a:entity, s:text | стан і числа |
| `grow` | росте / зменшується | a:entity, n:int | стан і числа |
| `set_side` | змінює сторону / власника | a:entity, side:text | стан і числа |
| `pickup` | підбирає в інвентар | a:entity, item:entity | інвентар |
| `take` | втрачає предмет | a:entity, item:entity | інвентар |
| `give` | отримує предмет | a:entity, item:entity | інвентар |
| `use` | використовує предмет | a:entity, item:entity | інвентар |
| `place` | ставить із запасу на поле | a:entity, entity:entity | інвентар |
| `set_cell` | клітина стає іншою | cell:choice:cell, type:entity | клітини й поле |
| `mark` | розмітка клітини | cell:choice:cell, v:text | клітини й поле |
| `unmark` | стерти розмітку | cell:choice:cell | клітини й поле |
| `reveal` | відкрити клітини | cell:choice:cell | клітини й поле |
| `hide` | сховати клітини | cell:choice:cell | клітини й поле |
| `paint` | зафарбувати | cell:choice:cell, color:text | клітини й поле |
| `fill` | заливка області | cell:choice:cell | клітини й поле |
| `clear` | очистити лінію / групу | shape:choice:shape | клітини й поле |
| `merge` | злиття двох в одну | a:entity, b:entity, into:entity | клітини й поле |
| `explode` | вибух із формою | shape:choice:shape, n:int, into:entity | клітини й поле |
| `win` | перемога 🏆 |  | хід гри |
| `lose` | поразка 💀 |  | хід гри |
| `draw` | нічия |  | хід гри |
| `next_level` | наступний рівень |  | хід гри |
| `restart` | рестарт рівня |  | хід гри |
| `undo` | скасувати хід (undo) | n:int | хід гри |
| `game_over` | кінець гри |  | хід гри |
| `end_turn` | хід переходить |  | хід гри |
| `pass_turn` | пас |  | хід гри |
| `extra_move` | додатковий хід |  | хід гри |
| `choose` | гравець обирає | options:text | хід гри |
| `window` | відкрити вікно | window:window | хід гри |
| `message` | повідомлення | text:text | хід гри |
| `sound` | звук / ефект | text:text | хід гри |
| `timer` | таймер | clock:choice:clock, n:int | хід гри |
| `custom` | інше (словами) | text:text | інше |

## Поле (`Part kind=field`)

- `topology` — Сітка: square, hex, graph, iso, layers, 1d, 3d, nested
- `view` — Вид: top-down, side, first-person
- `time` — Час: turn, realtime, static, programmed, wego, rhythm
- `control` — Керування: direct, indirect, click-cell, drag-piece, swipe-all, drag-path, mark, programmed
- `gravity` — Гравітація: down, up, per-type, toward-center
- `wrap` — Замкнене поле: вийшов за край — зʼявився з протилежного боку: on
- `size` — Розмір за замовчуванням
- `layers` — Шари клітини

## Характеристики сутності

- `hp` — HP (здоровʼя) ❤️
- `lives` — Життя 💗
- `speed` — Швидкість ⚡ (кл/тік)
- `damage` — Шкода ⚔️ (HP)
- `armor` — Броня 🛡️ (HP)
- `range` — Дальність дії 🎯 (кл)
- `capacity` — Місткість 🎒 (предм.)
- `cooldown` — Перезарядка ⏱️ (тіків)
- `value` — Очки / цінність ⭐
- `count` — Кількість на полі #️⃣ (шт.)
- `duration` — Тривалість ⏳ (тіків)
- `size` — Розмір 📐 (кл)
- `ammo` — Патрони 🔫 (шт.)
- `cost` — Ціна 🏷️
- `vision` — Огляд 👁️ (кл)
- `side` — Сторона / колір 🏳️
- `energy` — Енергія / паливо 🔋
- `rank` — Рівень прокачки 🎖️
