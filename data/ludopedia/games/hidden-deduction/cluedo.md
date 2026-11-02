---
title: Cluedo (Clue; «Клуедо»)
slug: cluedo
family: hidden-deduction
also: [board-digital]
klass: hybrid
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 1949
platforms: [board (Waddingtons 1949, Parker Brothers / Hasbro), PC (1989, 1992, 1998…), CD-i, iOS, Android, Steam (Marmalade 2018, 2023), Nintendo Switch]
links:
  - {kind: other, url: "https://www.hasbro.com/common/instruct/Clue_(2002).pdf", best: true, note: "офіційні правила Parker Brothers/Hasbro 2002: рух, двері, таємні ходи, припущення, спростування, обвинувачення"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Cluedo", note: "історія, 324 розвʼязки, правила, видання й цифрові версії"}
  - {kind: steam, url: "https://store.steampowered.com/app/794800/ClueCluedo_Classic_Edition/", note: "Marmalade 2018: віртуальний Cluesheet сам відмічає показані карти"}
  - {kind: steam, url: "https://store.steampowered.com/app/2506480/ClueCluedo/", note: "Marmalade 2023: Classic / Clue Cards / Ultimate Detective (одночасні таємні відповіді)"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Clue_(1992_video_game)", note: "список відеоігор Clue 1985–2009"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=clue+cluedo+how+to+play+rules", note: "пошук; правила"}
stage: v1
coverage: 70
mechanics: [move-4dir, impassable-cells, teleport-pair, cell-click, legal-move-highlight, hover-highlight, hot-seat, turn-enforcement, ai-opponent, ai-random, ai-greedy, pencil-marks, game-screen, main-menu, end-screen, settings-window, help-window, confirm-dialog, leaderboard, sound-effects, event-effects, +dice-move-steps, +room-zone-entry, +solution-envelope, +hidden-hand-cards, +suggestion-disprove, +summon-to-room, +one-shot-accusation, +eliminated-still-answers, +auto-notebook, +door-blocking, +simultaneous-secret-answer, +constraint-deduction-ai]
proposes: ["+trigger:suggest", "+trigger:accuse", "+cond:holds", "+effect:show_card", "+effect:eliminate", "+role:card", "+ui:dice-result", "+ui:notebook-grid", "+window:detective-notebook", "+window:suggestion-dialog", "+window:disprove-dialog", "+window:envelope-reveal", "+window:pass-device", "+feature:auto-notebook", "+axis:info-asymmetry", "+card:dice-move-steps", "+card:room-zone-entry", "+card:solution-envelope", "+card:hidden-hand-cards", "+card:suggestion-disprove", "+card:summon-to-room", "+card:one-shot-accusation", "+card:eliminated-still-answers", "+card:auto-notebook", "+card:door-blocking", "+card:simultaneous-secret-answer", "+card:constraint-deduction-ai"]
author: opus
date: 2026-11-02
---

# Cluedo — ходи кубиками по особняку, у кімнатах роби припущення, викреслюй карти: хто, де і чим

## Суть
У конверті лежать три приховані карти — підозрюваний, кімната, зброя (6 × 9 × 6 = 324 варіанти). Решту карт роздано гравцям. Гравець кидає кубики, веде свою фішку коридором до кімнати і там робить **припущення** «X у цій кімнаті з Y»; суперники по колу намагаються його спростувати, таємно показуючи одну карту. Хто першим правильно **обвинуватить** — виграє; помилка вибиває з гри. `klass: hybrid`: **avatar** (одна фішка, рух за кубиком по сітці — обмежує, *де* можна питати) + **cursor-дедукція** (блокнот-таблиця, яку гравець розмічає) — друга лінія і є ядром.

## Поле і час
- Квадратна сітка коридорів (класична дошка ≈24×25 клітин (?)), 9 кімнат по периметру (Hall, Lounge, Dining Room, Kitchen, Ballroom, Conservatory, Billiard Room, Library, Study); центр (сходи/«підвал») — недоступний, там лежить конверт.
- Кімната — **зона** без клітин усередині: вхід через двері зупиняє рух; у кімнаті може бути скільки завгодно фішок і зброї.
- Чотири кутові кімнати зʼєднані **таємними ходами** по діагоналі (Study↔Kitchen, Lounge↔Conservatory (?)).
- 6 стартових клітин на краю дошки — по одній на підозрюваного.
- Покроково, за годинниковою стрілкою; Miss Scarlet ходить першою (новіші правила — хто більше викинув). Хід: рух (кубики або таємний хід) → можливе припущення → можливе обвинувачення.
- Два шари інформації: **поле** (публічне: де фішки і зброя) і **карти** (рука — приватна; конверт — нічий; показана карта — відома двом).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фішка підозрюваного ×6 | player / piece | колір, стартова клітина | рух на результат кубиків ортогонально; фішки без гравця теж стоять на полі — їх тягають припущеннями |
| Клітина коридору | terrain | — | 1 крок; зайнята фішкою — непрохідна |
| Стіна | static | — | непрохідна |
| Кімната ×9 | zone | двері (1–4), таємний хід (кути) | вхід зупиняє рух; лише тут можна робити припущення |
| Двері | gate | кімната | прохід у кімнату; сам проріз не рахується кроком; заблокований фішкою суперника — закритий |
| Таємний хід ×2 | static | пара кутових кімнат | замість кидка: перейти в протилежну кутову кімнату |
| Центр / сходи | static | — | недоступний; тримає конверт |
| Зброя ×6 | object | Rope, Lead Pipe, Knife, Wrench, Candlestick, Pistol (видання 2002) | лежить у кімнаті; переноситься припущенням |
| Карта ×21 | card / supply | тип: suspect ×6 · weapon ×6 · room ×9 | у руці (приватно), у конверті (приховано від усіх) |
| Конверт «Case File» | container | 3 карти, по одній кожного типу | відкривається лише при обвинуваченні, таємно |
| Кубики ×2 | — | 2d6 | кількість кроків |
| Блокнот детектива | mark | таблиця 21 рядок × гравці | приватні позначки; у цифровій версії — автоматичні |

## Правила (КОЛИ → ЯКЩО → ТО)
- Підготовка: `custom: «з кожної колоди одна випадкова карта — у конверт»`; решту перемішати і роздати по колу (комусь може дістатись більше); свої карти — одразу відмітити в блокноті.
- КОЛИ `turn_start(p)` → ЯКЩО `cell(p, corner_room)` → ТО на вибір `teleport(p, opposite_corner)` замість кидка; інакше `input(roll)` → `custom: «кроків = сума 2d6»`.
- Рух: КОЛИ `input(step, dir)` → ЯКЩО ортогонально і `free(cell)` і клітина ще не відвідана цього ходу → ТО `move(p, cell)`; інакше `block`. Не можна стати на / пройти крізь клітину з іншою фішкою.
- КОЛИ `enter(p, room)` (через двері) → ТО `custom: «рух закінчено, решта кроків згорає»`; повторно в ту саму кімнату того ж ходу — `block`.
- КОЛИ `contact(p, door)` → ЯКЩО `occupied(door_square, opponent)` → ТО `block`. Усі двері кімнати заблоковано → гравець чекає всередині.
- КОЛИ `input(suggest, suspect, weapon)` → ЯКЩО `cell(p, room)` і `custom: «увійшов у кімнату цього ходу або його фішку перенесли сюди припущенням»` → ТО `move(suspect_pawn, room)`, `move(weapon, room)`; кімната припущення = поточна.
- Повторне припущення в тій самій кімнаті — лише після виходу й повернення наступним ходом (US-правила); «пропустити хід, сидячи в кімнаті» не можна.
- Спростування: КОЛИ `after(suggest)` → для q = ліворуч, далі по колу: ЯКЩО `holds(q, any of 3)` → ТО `choose(q: one card)`, `show_card(q → p)` таємно, кінець; інакше перехід до наступного. Ніхто не спростував → `custom: «у конверті — ці три, крім карт із руки самого p»`.
- Можна називати карти зі своєї руки — блеф або перевірка.
- КОЛИ `input(accuse, s, r, w)` (будь-яка кімната) → ТО `custom: «таємно глянути в конверт»`: збіг усіх трьох → `win`, `reveal(envelope)`; інакше `eliminate(p)`, карти назад у конверт.
- КОЛИ `eliminate(p)` → ТО p не ходить і не обвинувачує, **але далі спростовує** чужі припущення; якщо фішка p блокує двері — переноситься в кімнату.
- КОЛИ лишився один невибулий → ТО `win` (Wikipedia; у правилах 2002 не описано (?)).
- Цифрова версія: КОЛИ `show_card(q → p)` → ТО `mark(notebook_p, card, q)` автоматично; свої карти відмічено на старті.
- Ultimate Detective (Marmalade 2023): усі гравці відповідають на припущення **одночасно і таємно** — `custom: «спростування не зупиняється на першому»` (?).
- Перемога: правильне обвинувачення · Поразка: хибне обвинувачення (вибування) або хтось інший розвʼязав першим · Рахунку нема.

## Керування і ввід
- Настолка: кинути кубики, порахувати кроки, переставити фішку; вголос назвати припущення; карту показати «під столом».
- Цифрова версія: кнопка «Кинути» → підсвітка досяжних клітин і кімнат (`legal-move-highlight`, BFS на N кроків) → клік по цілі, фішка йде сама; кнопка «Таємний хід» у кутовій кімнаті.
- Припущення — діалог із двох рядів портретів (підозрюваний, зброя); кімната підставлена автоматично.
- Спростування — якщо маєш кілька збігів, вибираєш, яку карту показати (тактичний вибір: показувати ту, що вже бачив цей гравець).
- Блокнот — клік по клітинці таблиці: ✗ / ✓ / «?» / ініціали; Marmalade — «ticks and crosses» поверх автопозначок.

## Вікна, меню, HUD
- `main-menu`: Грати (AI) · Онлайн · Локально · Правила/навчання · Налаштування · Магазин тем.
- `mode-select` (Marmalade 2023): Classic · Clue Cards · Ultimate Detective.
- `match-setup` / `character-select`: кількість гравців 2–6, хто AI, вибір підозрюваного, складність AI.
- `game-screen`: дошка (3D-особняк), фішки, зброя в кімнатах; HUD — `turn-indicator`, `dice-result`, `pocket` (своя рука карт), кнопки Roll / Secret Passage / Suggest / Accuse.
- `detective-notebook` (цифрова версія): таблиця 21 карта × гравці; автопозначки показаних карт; ручні ✗/✓; може бути бічною панеллю або окремим вікном.
- `suggestion-dialog`: вибір підозрюваного і зброї → анімація перенесення фішки й зброї в кімнату.
- `disprove-dialog`: гравцю, що спростовує, — його збіги на вибір; іншим — лише «Гравець N показав карту» / «ніхто не спростував».
- `confirm-dialog` перед обвинуваченням («Ви впевнені? Помилка — вибування»).
- `envelope-reveal` / `end-screen`: відкриття конверта, переможець; хибне обвинувачення — приватне «Ви вибули» і далі режим спостерігача-спростовувача.
- `pass-device` (локальна гра на одному екрані): завіса між ходами, бо рука і блокнот приватні.
- `leaderboard` (Marmalade: тижневі онлайн-таблиці), `help-window` (How to Play), `settings-window`.
- Переходи: main-menu → match-setup → game-screen ⇄ (suggestion-dialog → disprove-dialog → notebook) → confirm → envelope-reveal → end-screen.

## Фічі поза полем
- `auto-notebook`: своя рука і всі показані тобі карти відмічаються автоматично; гравець лише робить висновки (Marmalade 2018: «Cluesheet will automatically keep track of the cards you've been shown»). Дизайнерське питання: автоматизувати лише факти чи й висновки.
- `ai-opponent-levels` (Marmalade: «customisable AI suspects», «AI that adapts to your skill»), `online-multiplayer` (до 6, кросплатформа), `local-multiplayer` (shared screen), `leaderboard-online`.
- `custom-rules`: Classic / Clue Cards (швидкий режим) / Ultimate Detective; теми-дошки (Black Adder Resort, Polar Research Station, Noir Mansion…) змінюють підозрюваних, зброю, кімнати.
- `tutorial`, `rules-page`.

## Варіації й родичі
- Clue Master Detective (1988): 12 кімнат, 10 підозрюваних, 8 зброй, до 10 гравців. Cluedo: Discover the Secrets (2008): обвинувачення лише з центрального басейну, колода інтриг з картами-«годинниками» (8-й годинник вибиває). Cluedo Junior — «хто зʼїв торт».
- Родичі за дедукцією: Mastermind (відгук на спробу), Black Box, Battleship; «таблиця виключень» як у логічних пазлах Einstein-типу.
- **Осі варіацій**: спростування «перший, хто може (класика) / усі одночасно таємно (Ultimate Detective)»; рух «кубики по сітці / телепорт між кімнатами (Clue Cards) (?)»; обвинувачення «будь-де / лише з центру (2008)»; блокнот «паперовий / автоматичні факти / автоматичні висновки».

## Цікавинки для курсу
- Конверт + роздача + приватні руки: три видимості однієї колоди (нічий / мій / показаний мені) — 📎.
- Хід за кубиком по сітці з забороною повторних клітин і зайнятих — BFS на N кроків для підсвітки досяжного — 🥉.
- Цикл «припущення → спростування по колу → таємний показ» як машина станів із приватними повідомленнями — 🥉.
- Автоблокнот: таблиця 21×N із фактами; рівень вище — **виводи** (якщо q не спростував — у q немає жодної з трьох карт; якщо показав — у q є хоч одна з трьох) — 🥈.
- AI-детектив, що розвʼязує обмеження «у гравця q є одна з {a, b, c}» перебором розподілів карт — 🥇.
- Hotseat із приватною рукою і блокнотом (завіса) — 📎.
- Вибулий гравець, що лишається в грі як джерело відповідей — 🌱, але гарний приклад «ролі після поразки».

## Мапа на каталог
- Є: `move-4dir` (крок фішки) · `impassable-cells` (стіни, центр) · `teleport-pair` (таємні ходи) · `cell-click` + `legal-move-highlight` + `hover-highlight` · `hot-seat` + `turn-enforcement` · `ai-opponent` / `ai-random` / `ai-greedy` · `pencil-marks` (позначки в блокноті) · `game-screen` / `main-menu` / `end-screen` / `settings-window` / `help-window` / `confirm-dialog` / `leaderboard` · `sound-effects` · `event-effects`.
- **Нема** → пропозиції карток:
  - `+dice-move-steps` «Рух на результат кубиків» · entities/move · 📎 · слот {dice: 2d6, revisit: false}.
  - `+room-zone-entry` «Кімната-зона: вхід через двері зупиняє рух» · entities/legality · 📎.
  - `+solution-envelope` «Прихована відповідь із кількох категорій» · levels/generation · 🌱 · слот {categories}.
  - `+hidden-hand-cards` «Приватна рука карт» · entities/state · 📎.
  - `+suggestion-disprove` «Припущення і спростування по колу» · game-logic/opponent · 🥉.
  - `+summon-to-room` «Припущення переносить фігуру суперника» · entities/interact · 🌱.
  - `+one-shot-accusation` «Одна спроба відповіді, помилка — вибування» · game-logic/lose · 🌱.
  - `+eliminated-still-answers` «Вибулий лишається відповідачем» · game-logic/opponent · 🌱.
  - `+auto-notebook` «Автоблокнот дедукції» · interface/hud · 🥈 · слот {level: facts|inferences}.
  - `+door-blocking` «Фішка блокує двері» · entities/legality · 🌱.
  - `+simultaneous-secret-answer` «Усі відповідають одночасно і таємно» · game-logic/opponent · 📎.
  - `+constraint-deduction-ai` «AI-дедукція за обмеженнями на руки» · game-logic/opponent · 🥇.

## Пропозиції до словників
- `+trigger:suggest` — гравець зробив припущення (запускає ланцюг спростування); `+trigger:accuse` — обвинувачення.
- `+cond:holds(player, card)` — у руці гравця є карта (приватне `has` для карт).
- `+effect:show_card(from → to)` — таємно показати карту одному гравцю; `+effect:eliminate(p)` — вибування гравця без кінця гри.
- `+role:card` — карта як сутність поза полем (в руці, в конверті); близьке до 🔥 `supply`.
- `+ui:dice-result` — показ кидка; `+ui:notebook-grid` — таблиця «карта × гравець» з позначками.
- `+window:detective-notebook` — блокнот дедукції як окреме вікно/панель; `+window:suggestion-dialog`; `+window:disprove-dialog` — вибір карти для показу; `+window:envelope-reveal` — розкриття відповіді.
- `+window:pass-device` — див. Battleship/Stratego.
- `+feature:auto-notebook` — автоматичні позначки фактів.
- `+axis:info-asymmetry` — див. Geister; тут — найскладніший випадок: кожна карта має свою множину «хто знає».

## Джерела
- ⭐ [Clue rules (Hasbro, 2002, PDF)](https://www.hasbro.com/common/instruct/Clue_(2002).pdf) — підготовка, рух (не діагонально, без повторних клітин, не крізь фішки), двері й блокування, таємні ходи, припущення, спростування, одне обвинувачення, наслідки помилки.
- [Wikipedia: Cluedo](https://en.wikipedia.org/wiki/Cluedo) — історія (Pratt 1943, Waddingtons 1949), 324 розвʼязки, правила, Master Detective, Discover the Secrets, Junior, цифрові версії.
- [Steam: Clue/Cluedo Classic Edition](https://store.steampowered.com/app/794800/ClueCluedo_Classic_Edition/) — автоматичний Cluesheet, онлайн, shared screen, теми.
- [Steam: Clue/Cluedo (2023)](https://store.steampowered.com/app/2506480/ClueCluedo/) — режими Classic / Clue Cards / Ultimate Detective, AI, онлайн.
- [Wikipedia: Clue (1992 video game)](https://en.wikipedia.org/wiki/Clue_(1992_video_game)) — перелік відеоігор Clue.
- YouTube: пошук «clue cluedo how to play rules».

## Непевне
- (?) Розмір сітки 24×25 і точні пари таємних ходів (Study↔Kitchen, Lounge↔Conservatory) — з памʼяті; правила 2002 кажуть лише «кімнати в протилежних кутах».
- (?) «Останній невибулий перемагає» — Wikipedia; у правилах 2002 прямо не сказано.
- (?) Як саме працює Ultimate Detective (чи бачить той, хто питає, усі показані карти) і Clue Cards mode — лише рядки зі Steam.
- (?) Кількість дверей у кожній кімнаті — не перевірено.
