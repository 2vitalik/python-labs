---
title: "Stitches (Стібки)"
slug: stitches
aka: [Стібки]
family: pencil-logic
also: []
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: null
platforms: [paper, web]
links:
  - {kind: play, url: "https://www.puzzle-stitches.com/", best: true, note: "правила в 4 пункти й гра одразу: 5×5…15×15, 1–3 стібки на пару (÷), Daily/Weekly 4÷, Monthly 1÷, 16 налаштувань, ID пазла"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Stitches/index.htm", note: "Janko: правила DE/EN, «латки ковдри», автор жанру невідомий, 110 пазлів 5×5…15×15"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Bedienung.htm", note: "Janko: загальна інструкція аплетів — миша, тач, клавіатура, F3 підказка, F4 розвʼязок, F6 перевірка, undo/redo, 9 слотів"}
  - {kind: youtube, url: "https://www.youtube.com/embed/videoseries?list=PLH_elo2OIwaCRA3lmEsYsvCO63c8blDlP", note: "Video Tutorial з puzzle-stitches.com (плейліст)"}
stage: v1
coverage: 70
mechanics: [satisfy-constraints, markup-validity, completion-detection, edge-marking, cell-click, dot-mark, line-sum-clue, conflict-highlight, rule-variants, field-size-picker, difficulty-levels, daily-puzzle, level-bank, level-rating, game-settings, theme-select, leaderboard, seed-share, state-string, restart-level, undo-redo, save-multi-slot, field-scaling, keyboard-controls, +irregular-regions, +region-pair-stitches, +print-version, +elapsed-timer, +hint-reveal, +reveal-solution]
proposes: ["+cond:count_in", "+cond:links_between(region_a, region_b, n)", "+ui:edge-cross", "+window:game-id-dialog", "+window:hall-of-fame", "+window:puzzle-info", "+feature:print", "+card:region-pair-stitches"]
author: opus
date: 2026-11-19
---

# Stitches — зший кожну пару сусідніх латок рівно одним стібком; числа на краях рахують отвори

## Суть
Сітка поділена на неправильні регіони — «латки» ковдри, які треба зшити (Janko). Гравець ставить стібки: стібок — відрізок довжини 1 між двома ортогонально сусідніми клітинками **різних** регіонів. Кожна пара сусідніх регіонів зшита рівно одним стібком (у варіантах ÷2, ÷3, ÷4 — рівно K), клітинка-«отвір» належить щонайбільше одному стібку, а числа біля рядків і стовпців кажуть, скільки в них отворів. Незвичне: обмеження стоїть на **ребрі графа сусідства регіонів** — кожне таке ребро треба «реалізувати» доміно через спільну межу.

## Поле і час
- Квадратна сітка N×N: Janko 5×5…15×15 (більшість 7×7 і 10×10); puzzle-stitches 5×5, 7×7, 10×10, 15×15.
- Товсті межі ділять сітку на регіони неправильної форми; сусідство регіонів — через спільний відрізок межі.
- Підказки — поза полем: число біля кожного рядка й стовпця = кількість отворів у лінії.
- Шари: регіони (незмінні) · стібки на межах регіонів · стан клітинки (порожньо / отвір / X «отвору нема») · червона межа «тут стібка нема» (puzzle-stitches).
- Стібок лише горизонтальний або вертикальний; діагональних нема.
- Час статичний; хід = поставити чи зняти стібок або позначку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Регіон (латка) | zone | форма, список сусідів | з кожним ортогонально сусіднім регіоном зшитий рівно K стібками |
| Пара сусідніх регіонів | zone | K = 1…4 (позначка ÷K) | ребро графа сусідства; стібків між ними рівно K |
| Стібок | mark | дві клітинки по різні боки межі | відрізок довжини 1; дає 2 отвори |
| Отвір (hole) | mark | — | кінець стібка; у клітинці щонайбільше один |
| X у клітинці | mark | — | помітка гравця «отвору нема», не перевіряється |
| Червона межа | mark | — | помітка гравця «тут стібка нема» (puzzle-stitches) |
| Межа регіонів | static | товста лінія | шити можна лише через неї |
| Підказка рядка / стовпця | static | N | отворів у лінії рівно N |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, border)` (між двома клітинками) → ТО `mark(border, stitch)`: обидві клітинки стають отворами (puzzle-stitches).
- КОЛИ `input(right_click, border)` → ТО `mark(border, red)` — «тут стібка нема».
- КОЛИ `input(click, cell)` → ТО `mark(cell, hole)`.
- КОЛИ `input(right_click, cell)` → ТО `mark(cell, x)`.
- КОЛИ `input(drag, cell_to_neighbor)` (Janko) → ТО `mark(pair, stitch)`; Ctrl + протягування — `unmark(pair)` (загальна схема аплетів).
- КОЛИ `constraint_broken(pair)` → ЯКЩО `custom: «між двома сусідніми регіонами стібків ≠ K»` (`+cond:links_between`) → ТО `custom: «пазл не розвʼязано»`.
- КОЛИ `constraint_broken(stitch)` → ЯКЩО `custom: «обидва кінці стібка в одному регіоні»` → ТО `custom: «пазл не розвʼязано»`.
- КОЛИ `constraint_broken(hole)` → ЯКЩО `custom: «клітинка — отвір двох стібків»` → ТО `custom: «пазл не розвʼязано»` («2 stitches cannot share a hole»).
- КОЛИ `constraint_broken(line_count)` → ЯКЩО `custom: «отворів у рядку чи стовпці ≠ числу на краю»` (`+cond:count_in`) → ТО `custom: «пазл не розвʼязано»`.
- КОЛИ `input(f6)` (Janko, «перевірити») → ТО `custom: «порушення позначено червоним»`; puzzle-stitches — налаштування Highlight errors.
- КОЛИ `all_constraints_met` → ТО `win`; puzzle-stitches — кнопка Done або налаштування Auto submit, Janko — рамка діаграми зеленіє.
- Облік: кожен стібок дає 2 отвори; горизонтальний — обидва в одному рядку й по одному у двох стовпцях, вертикальний — навпаки. Сума чисел рядків = сума чисел стовпців = 2 × K × (кількість пар сусідніх регіонів).
- Дедукції: число 0 — лінію не торкається жоден стібок; два регіони, що межують лише одним відрізком довжини 1, при K = 1 зшиті саме там; пара, що вже має K стібків, — решта її межі червона; отвір забирає клітинку, тож сусідні стібки «конкурують» за спільні клітинки.
- Перемога: усі пари зшиті рівно K стібками, отвори не спільні, числа рядків і стовпців виконані. Поразки нема. Рахунку нема; puzzle-stitches міряє час (Hall of Fame (?)).

## Керування і ввід
- puzzle-stitches: клік між двома клітинками — стібок; правий клік по межі — червона межа; клік у клітинці — отвір; правий клік у клітинці — X. Стиль стібків Normal / Thin.
- Janko (загальна схема аплетів): лінію тягнуть лівою кнопкою, Ctrl + протягування стирає; клавіатура — стрілки рухають рамку, Shift + стрілки малюють лінію, Ctrl + стрілки стирають; на тачі — перемикач «клітинка / лінія», два пальці — прокрутка, щипок — зум.
- Janko, функції: F3 — режим підказки (клік відкриває правильне значення), F4 — розвʼязок, F6 — перевірка, PgUp / PgDn — undo / redo, Home / End — усе назад / вперед; Ctrl+S / Ctrl+L — зберегти / завантажити.
- Помітки Janko: 9 символів (коло, квадрат, крапка, хрестик…) і 10 кольорів; значення помітки вирішує гравець.

## Вікна, меню, HUD
- `game-screen` (puzzle-stitches): сітка, числа рядків і стовпців (`line-clue`), «Puzzle ID» над полем, кнопки Done · Start Over · Print… · Share · New Puzzle, поля Progress Permalink і Progress Screenshot, `timer-elapsed` (можна сховати), Hide / Show the rules.
- Перелік варіантів: 5×5/1÷ … 15×15/3÷ у Normal / Hard + Special Daily 4÷, Weekly 4÷, Monthly 1÷ — як `mode-select` списком посилань.
- `settings-window`: Hide game controls, Sticky toolbar, Auto submit, Show checkpoints, Show board coordinates, Hide the timer, Non-competitive (personal) timer, Night mode, Highlight errors, Use blue for errors, Highlight completed, Show counters, Count remaining, Thicker block borders, Auto place red borders, Colored blocks.
- `+window:game-id-dialog` (Specific puzzle — ввести ID) · `+window:hall-of-fame` (hall.php) · `stats-window` (stats.php, вміст не відкривав) · `custom-window` Mass Print.
- Janko: `game-screen` з панеллю іконок (undo/redo, перевірка, підказка, розвʼязок, зум, кандидати); розгортні «Regeln» і «Bedienungsanleitung» (`help-window`); `puzzle-select` «Rätsel wählen» (110 пазлів, сортування за датою, розміром, складністю); `+window:puzzle-info` (F1: версія скрипта, дані пазла, час, розвʼязок, список ходів, форма відгуку); `save-slots` («сервер» на 10 днів + 8 локальних).
- HUD Janko: `timer-elapsed` у двох видах — Brutto (з відкриття сторінки) і Netto (оцінка активного часу без пауз).
- Переходи: список варіантів → `game-screen` → Done → (?) результат; Janko: `puzzle-select` → пазл → Zurück / Weiter.

## Фічі поза полем
- `difficulty-presets` (Normal / Hard) і вибір розміру та K (÷1–÷4) — набір варіантів правил як параметр.
- `daily-puzzle` + щотижневий і щомісячний спецпазл.
- `share-code`: Progress Permalink (стан за посиланням), Share, Specific puzzle за ID (`seed-input`).
- Друк: Print… і Mass Print (`+feature:print`); у Janko — окрема сторінка допомоги з друку.
- `auto-check`-подібні налаштування: Highlight errors, Highlight completed, Auto place red borders, Count remaining; `theme-select`: Night mode, Colored blocks, Thicker block borders.
- `leaderboard-online` — Hall of Fame (?); `stats` — Statistics (?).
- Janko: `undo` ∞ і `redo` (лише одразу після undo), `hint` (одна клітинка), `show-solution`, `save-slots`, таймер Netto / Brutto.

## Варіації й родичі
- **÷K** (puzzle-stitches): кожна пара регіонів зшита рівно 2, 3 чи 4 стібками — та сама логіка, щільніше поле отворів.
- [one-room-one-door](one-room-one-door.md) — теж обмеження на **пару регіонів** (щонайбільше одні «двері»); у Stitches — рівно K «дверей»-стібків, і вони не ділять клітинок.
- [tents](tents.md), [star-battle](star-battle.md) — ті самі лічильники рядків і стовпців; [hashiwokakero](hashiwokakero.md) — звʼязки між «островами», але мости довгі й перетинаються з правилами кількості.
- [dominosa](dominosa.md) — інший пазл про доміно на сітці (там покриття, тут розріджені стібки).
- Осі варіацій: скільки звʼязків на пару (рівно 1 / рівно K / щонайбільше 1) · що рахують підказки (отвори / стібки / нічого) · довжина звʼязку (1 / будь-яка, як мости) · чи можна ділити клітинку між звʼязками.

## Цікавинки для курсу
- Граф сусідства регіонів: обхід сітки → множина пар (A, B) і їхні спільні відрізки межі — 📎.
- Перевірка «рівно K стібків на кожну пару» + «отвір не спільний» + лічильники ліній — 🥉 (три різні обмеження над однією розміткою).
- Стібок як сутність на ребрі (пара сусідніх клітинок), а не на клітинці — 📎 (поруч із `edge-marking`).
- Авто-червоні межі: пара досягла K → решта її межі закривається — 🌱.
- Стан за посиланням (Progress Permalink): серіалізувати стібки й позначки в рядок і назад — 📎.
- Генератор з єдиним розвʼязком і параметром K — 🥇.

## Мапа на каталог
- Є: `satisfy-constraints` · `markup-validity` · `completion-detection` · `edge-marking` (стібки, червоні межі) · `cell-click` + `dot-mark` (отвір, X) · `line-sum-clue` (числа рядків і стовпців) · `conflict-highlight` (Highlight errors, F6) · `rule-variants` (÷K) · `field-size-picker` · `difficulty-levels` · `daily-puzzle` · `level-bank` + `level-rating` (Janko, складність за часом) · `game-settings` + `theme-select` (Night mode) · `leaderboard` (Hall of Fame) · `seed-share` (Specific puzzle) · `state-string` (Progress Permalink) · `restart-level` (Start Over) · `undo-redo` · `save-multi-slot` · `field-scaling` · `keyboard-controls` (Janko).
- **Нема** → пропозиції карток:
  - `+region-pair-stitches` «Рівно K звʼязків між кожною парою сусідніх регіонів» · game-logic/constraints · 🥉 · слот {per_pair: 1..4} — родич `+door-limit-per-region-pair` (One Room One Door).
  - `+irregular-regions` (повтор, 🔥) — поле з неправильних регіонів.
  - `+print-version` (повтор, 🔥) — Print / Mass Print.
  - `+elapsed-timer` · `+hint-reveal` · `+reveal-solution` — повтори (таймер, F3, F4 Janko).

## Пропозиції до словників
- `+cond:count_in` — кількість розміток виду в рядку чи стовпці (тут отвори); повтор, 🔥 у корпусі.
- `+cond:links_between(region_a, region_b, n)` — кількість звʼязків між двома регіонами (стібки тут, двері в One Room One Door).
- `+ui:edge-cross` — помітка «тут нема» на межі (червона межа); повтор Palisade.
- `+window:game-id-dialog` — ввести ID пазла (Specific puzzle); повтор Tatham.
- `+window:hall-of-fame` — таблиця найкращих розвʼязувачів сайту.
- `+window:puzzle-info` — інфо-вікно пазла: версія, дані, час, розвʼязок, ходи, відгук (Janko F1).
- `+feature:print` — друк пазла чи пакета пазлів.
- `+card:region-pair-stitches` — див. мапу.

## Джерела
- ⭐ [puzzle-stitches.com](https://www.puzzle-stitches.com/) — правила 4 пунктами, ÷-варіанти, керування мишею, 16 налаштувань, кнопки, Daily / Weekly / Monthly, ID пазла, Video Tutorial, Hall of Fame, Statistics, Mass Print.
- [Janko: Stitches](https://www.janko.at/Raetsel/Stitches/index.htm) — правила DE/EN, «латки ковдри» (Masche, Knoten), автор і перша публікація невідомі, 110 пазлів 5×5…15×15, складність за часом розвʼязання.
- [Janko: Bedienung](https://www.janko.at/Raetsel/Bedienung.htm) — загальна інструкція аплетів: миша, тач, клавіатура, F-клавіші, undo/redo, 9 слотів збереження, Netto / Brutto.
- [Video Tutorial](https://www.youtube.com/embed/videoseries?list=PLH_elo2OIwaCRA3lmEsYsvCO63c8blDlP) — плейліст YouTube з кнопки на puzzle-stitches.

## Непевне
- (?) Рік і автор жанру: Janko — «невідомо, можливо з турніру»; puzzle-stitches не каже.
- (?) Аплет Janko саме для Stitches — за загальною інструкцією; які кнопки (кандидати, кольори) є в цьому жанрі, не перевіряв.
- (?) Що робить Done при помилці, як працюють Auto place red borders і Show checkpoints — бачив лише назви.
- (?) Hall of Fame і Statistics — сторінки не відкривав; чи пазли генеруються (ID ~12 млн), чи це банк — не перевіряв.
- (?) Розмір поля Special Daily / Weekly 4÷ на сторінці не вказаний.
- (?) Повторний клік по стібку знімає його — за звичною схемою сайтів puzzle-*.com, не перевірено.
