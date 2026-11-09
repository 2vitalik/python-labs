---
title: "Paper Mario: The Origami King — бойова кільцева сітка"
slug: paper-mario-the-origami-king
aka: [Paper Mario Origami King, PMTOK, ペーパーマリオ オリガミキング]
family: push-slide
also: [tactics]
klass: cursor
axes:
  field: graph
  time: turn
  opponent: ai
  info: partial
  random: both
  goal: state
year: 2020
platforms: [Switch]
links:
  - {kind: wiki, url: "https://www.mariowiki.com/Paper_Mario:_The_Origami_King", best: true, note: "Super Mario Wiki: арена 4 кільця × 12 клітин, Rotate/Slide на L/R, бонус 1,5× за лінію чи 2×2, форми атак, таймер і ліміт ходів з undo, Buy Time, Cheer, бос-бої зі стрілками, панелі, бонуси монет, прихований Miss Points"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Paper_Mario:_The_Origami_King", note: "огляд бою: кільця, ліміт часу й обертань, hammer 2×2 біля центру, boots 1×4, тоадів кличуть монетами; бос-бій навпаки — Маріо зовні йде стрілками"}
  - {kind: other, url: "https://gamewith.net/paper-mario-the-origami-king/article/show/20190", note: "бос Earth Vellumental: 60 с на хід, 2 зсуви кілець, панель з кулаком у кінці шляху"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Paper+Mario+Origami+King+ring+battle", note: "пошук; кільцеві бої"}
stage: v1
coverage: 60
mechanics: [row-conveyor, wrap-edges, move-timer, move-limit, undo-redo, hp-damage, inventory-items, round-currency, item-pickup, enemy-waves, path-preview, button-toggle, +ring-board, +ring-rotate, +lineup-bonus, +attack-shape, +arrow-path-panels, +weapon-durability, +timing-judgement-bonus, +timing-window, +hint-move, +buy-time, +pity-discount]
proposes: ["+axis:field=polar", "+effect:damage_area", "+cond:timing_window", "+trigger:lineup_end", "+feature:buy-time", "+feature:pity-discount", "+window:battle-command", "+card:lineup-bonus", "+card:attack-shape", "+card:arrow-path-panels"]
author: opus
date: 2026-11-09
---

# Paper Mario: The Origami King — бойова кільцева сітка: за обмежені ходи й секунди крути кільця й зсувай промені, щоб вишикувати ворогів під удар

## Суть
Пригодницька RPG Intelligent Systems (Switch, 2020), де світ — паперовий, а Маріо з Олівією розплутує стрічки короля Оллі; поза боєм — дослідження, «1000-Fold Arms» і конфетті для дірок у світі (тут не описано). Описано лише **бій**: арена — полярна сітка з 4 кілець по 12 клітин, Маріо в центрі, вороги розкидані по клітинах. Перед атакою гравець за ліміт ходів і таймер **обертає кільця** і **зсуває промені**, щоб зібрати ворогів у лінію (під стрибок) або квадрат 2×2 (під молот) — правильна розстановка дає ×1,5 до шкоди. У бос-боях ролі навпаки: бос у центрі, Маріо зовні, і гравець тими самими зсувами прокладає йому шлях зі стрілок.

## Поле і час
- Поле — полярна сітка: 4 концентричні кільця × 12 секторів = 48 клітин (`field: graph`, кільця замкнені по колу; промінь проходить крізь центр на протилежний бік (?)).
- Два ходи-генератори: **Rotate** — кільце повертається на крок, усі вороги на ньому їдуть по колу; **Slide** — промінь (сектор + протилежний сектор) зсувається до/від центру.
- Хід бою: фаза розстановки (таймер у секундах + ліміт ходів) → фаза атаки → хід ворогів і партнерів → вороги розбігаються на нові клітини → знову розстановка.
- Інформація: усе видно, крім ворогів, що ховаються (Piranha Plant закопується, Boo стає невидимим під час розстановки) — `info: partial`.
- Випадковість: стартова розкладка ворогів і їхнє розбігання; промах партнерів (`random: both`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Маріо | player | HP 50 → 200; Jump 3 → 11, Hammer 4 → 12 | стоїть у центрі; атакує формою зброї; бос-бій — іде стрілками по кільцях |
| Ворог | enemy | HP, тип | займає клітину; їде з кільцем/променем; атакує в хід ворогів |
| Piranha Plant / Boo | enemy | ховається | закопується / невидимий під час розстановки |
| Ворог-панцир | enemy | — | після стрибка ховається в панцир; стрибок по панциру запускає його в інших |
| Mechakoopa | enemy | випадкова заміна | дає більше монет |
| Ворог з Magic Circle | enemy | wave-бій | знищений після розстановки лишає коло під ногами Маріо |
| Партнер | ally | шанс промаху | бʼє наприкінці ходу фіксованою формою |
| Тоади на трибунах | neutral | монети | Cheer: кидають сміття у ворогів, підкручують кільця до розвʼязку, лікують, дають предмети |
| Boots / Hammer | pickup | вічні | стрибок — лінія 1×4; молот — квадрат 2×2 біля центру |
| Сильніша зброя | pickup | міцність | ламається після кількох ударів |
| Бойовий предмет | pickup | одноразовий | Fire/Ice Flower — лінія; POW Block — усі наземні, оглушення |
| Стрілка (бос) | terrain | напрям | Маріо йде за нею до наступної стрілки / панелі / кола |
| Action Panel (бос) | switch | — | зупинка: вибір зброї чи предмета для атаки |
| Extra Action / ×2 Striking Power (бос) | switch | — | додаткова дія / подвоєна сила наступної атаки |
| ON-перемикач і Magic Circle (бос) | switch / gate | стан on | коло спрацьовує лише після ON; дає 1000-Fold Arms чи силу Велюменталу |
| Скриня, серце, монета, Hint Envelope (бос) | pickup | — | лежать на вільних клітинах; підказка замість Олівії |
| Стрічка / діркопробивач / ножиці / лід (бос) | hazard | — | склеює панелі (не зсуваються, кільця крутяться разом) / дірки, у які падає Маріо / вирізає панелі / заморожує панелі |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(rotate, ring, dir)` → ЯКЩО `counter(moves_left, >, 0)` → ТО `shift(ring, dir)`, `counter(moves_left, -1)`.
- КОЛИ `input(slide, ray, dir)` → ЯКЩО `counter(moves_left, >, 0)` → ТО `shift(diameter, dir)`, `counter(moves_left, -1)`.
- КОЛИ `input(undo)` → ЯКЩО `counter(moves_left, >, 0)` і `timer(>, 0)` → ТО `undo(1)`.
- КОЛИ `input(buy_time)` → ЯКЩО `has(mario, coins)` → ТО `currency(-n)`, `timer(+n)`.
- КОЛИ `input(cheer)` → ЯКЩО `first_time` (раз за хід) → ТО `currency(-n)` (до 999), `custom: «тоади бʼють сміттям / наближають кільця до розвʼязку / лікують / дають предмети — що більше монет, то сильніше»`.
- КОЛИ `custom: «ходи вичерпано або таймер = 0, або гравець підтвердив»` → ТО `custom: «фаза атаки з поточною розстановкою»`.
- КОЛИ `pattern(line(4))` або `pattern(square_2x2)` → ЯКЩО `custom: «усі вороги в лініях/квадратах»` → ТО `multiplier(1.5)`, `extra_move` (кожна вишикувана група — окрема дія).
- КОЛИ `input(jump)` → ТО `damage(n)` по лінії 1×4 від центру.
- КОЛИ `input(hammer)` → ТО `damage(n)` по квадрату 2×2 на двох внутрішніх кільцях.
- КОЛИ `input(action_command)` → ЯКЩО `custom: «натиснуто в правильний момент»` → ТО `damage(+n)`, `message(Nice|Excellent)`.
- КОЛИ `custom: «удар зброєю з міцністю»` → ЯКЩО `counter(durability, ==, 0)` → ТО `disappear_a` (зброя ламається).
- КОЛИ `turn_start(mario)` → ЯКЩО `count(enemy, <=, few)` → ТО `custom: «фазу розстановки пропущено»`, `multiplier(boost)`.
- КОЛИ `turn_start(enemies)` → ТО `damage(mario, n)` (по одному або командним прийомом), `custom: «вороги перебігають на нові клітини»`.
- КОЛИ `custom: «ворог атакує»` → ЯКЩО `custom: «гравець натиснув захист у такт»` → ТО `custom: «шкоду зменшено»`.
- КОЛИ `turn_end(mario)` → ТО `custom: «партнер бʼє фіксованою формою, можливий промах»`.
- КОЛИ `died(circle_holder)` → ЯКЩО `custom: «вороги були вишикувані»` → ТО `spawn_at(magic_circle, mario)`; наступного ходу — `disappear(all_enemies)`.
- Бос: КОЛИ `enter(mario, arrow)` → ТО `face(mario, arrow_dir)`, `move(mario, dir)` до наступної стрілки, Action Panel чи кола.
- Бос: КОЛИ `enter(mario, action_panel)` → ТО `choose(weapon|item)`; ЯКЩО `custom: «Маріо на двох зовнішніх кільцях»` → ТО молот і хвіст не дістають боса.
- Бос: КОЛИ `custom: «Маріо вдруге проходить ту саму панель»` → ТО `end_turn` (спотикається).
- Бос: КОЛИ `enter(mario, on_switch)` → ТО `set_state(magic_circle, on)`.
- Бос: КОЛИ `enter(mario, magic_circle)` → ЯКЩО `state(magic_circle, on)` → ТО `custom: «1000-Fold Arms / сила Велюменталу»`.
- КОЛИ `input(flee)` → ЯКЩО `mode(boss)` → ТО `block`; інакше `custom: «спроба втекти»`.
- КОЛИ `all_gone(enemy)` → ТО `win`, `currency(+clear_bonus)`; бонуси: за ефективність розстановки (до 100 % Clear Bonus), без шкоди, фініш 1000-Fold Arms, wave-бій (по 50 %).
- КОЛИ `hp_zero(mario)` → ТО `game_over`.
- Прихований лічильник Miss Points: КОЛИ `custom: «не захистився / провалив розстановку / Game Over»` → ТО `counter(miss_points, +n)`; пороги → знижки на аксесуари, на 10 000 — відкривається Puzzle Solver.

## Керування і ввід
- Розстановка: курсор-кільце / курсор-промінь стіком, L/R — перемкнути Rotate ↔ Slide, підтвердження — кнопкою; Minus — Buy Time; окремі пункти — підказка Олівії, Cheer, втеча.
- Атака: меню зброї й предметів, потім Action Command у такт (стрибок — натиснути перед приземленням, молот — тримати й відпустити (?)).
- Захист: A перед ударом ворога.
- Бос-бій: ті самі Rotate/Slide, але мета — шлях зі стрілок від Маріо до Action Panel.

## Вікна, меню, HUD
- `game-screen` бою: кільцева арена, `timer-countdown`, `move-counter` (лишилось зсувів), `hp-bar` Маріо, `coins`, `hint-marker` — кружечки O від Puzzle Solver, `path-preview` — підсвічений шлях стрілок (після Cheer у бос-бою).
- `battle-command` (custom-window): Jump · Hammer · Items · Accessories (?) · Flee; вибір цілі/форми.
- `inventory-window` — бойові предмети й зброя з міцністю.
- `end-screen` — монети за бій з розбивкою бонусів (Clear, Puzzle, No-Damage, Finisher, Wave).
- Переходи: дослідження → (дотик ворога) бій → розстановка → атака → хід ворогів → … → екран нагороди → дослідження.

## Фічі поза полем
- `hint` — підказка Олівії (не в бос-боях) і Hint Envelope на полі боса; Puzzle Solver — аксесуар, що позначає цільові клітини.
- Аксесуари на старт бою: Time Plus (більше часу), Timer Extender (сам купує час раз за хід), Heart Plus, Guard Plus; обмеження — по одному кожного виду, ще два інших.
- `assist-mode`-подібне: прихований Miss Points дає знижки на аксесуари гравцеві, що часто помиляється.
- `undo` — у межах фази розстановки, доки є ходи й час.
- Решта гри (світ, збереження Save Block, 1000-Fold Arms у світі) — поза шаром.

## Варіації й родичі
- Осі варіацій:
  - **топологія поля**: квадрат (`mazezam`, Loopover у `sliding-tile-permutation`) / тор (Loopover) / **полярна сітка з центром** (Origami King, Unstoppable Gorg);
  - **хід-генератор**: зсув ряду по колу / поворот кільця / зсув променя крізь центр;
  - **навіщо зсувати**: зібрати картинку (пʼятнашки) / пройти (`mazezam`) / **вишикувати ворогів під форму атаки** (Origami King) / прокласти шлях стрілок (бос-бій).
- Родичі: `sliding-tile-permutation` (Sixteen, Loopover), `mazezam`, `arranger` (зсув свого ряду світу), `unstoppable-gorg` (кільця орбіт у TD).

## Цікавинки для курсу
- Полярна сітка 4×12: Rotate як циклічний зсув рядка масиву, Slide як зсув «діаметра» з 8 клітин — 📎.
- Перевірка «усі вороги в лініях 1×4 або квадратах 2×2» і бонус ×1,5 — 🥉 (покриття множини фігурами).
- Розвʼязувач: BFS за ≤ N зсувів до розкладки, де всі вороги покриті фігурами атаки (та сама задача, що в Puzzle Solver) — 🥇.
- Таймер фази + ліміт ходів + undo в межах фази + Buy Time за монети — 📎.
- Бос-бій: шлях зі стрілок, що міняється зсувами кілець; «двічі на ту саму панель — кінець ходу» — 🥈.
- Прихована динамічна складність Miss Points → знижки — 🌱.

## Мапа на каталог
- Є: `row-conveyor` ↔ Slide (зсув цілого променя); `wrap-edges` ↔ кільце замкнене по колу; `move-timer` ↔ таймер розстановки; `move-limit` ↔ ліміт зсувів; `undo-redo` ↔ undo в межах фази; `hp-damage` ↔ HP Маріо й ворогів; `inventory-items` ↔ предмети й зброя; `round-currency` ↔ монети на Buy Time і Cheer; `item-pickup` ↔ серця й монети на полі боса; `enemy-waves` ↔ wave-бої; `path-preview` ↔ підсвічений шлях стрілок; `button-toggle` ↔ ON-перемикач Magic Circle.
- **Нема** → пропозиції карток:
  - `+ring-board` (вже пропонована Oware, Ringfall) · слоти {rings: 4, sectors: 12}; `+ring-rotate` (вже пропонована Unstoppable Gorg).
  - `+lineup-bonus` «Розстановка ворогів під форму атаки дає множник» · game-logic/score · 🥉 · слот {mult: 1.5}.
  - `+attack-shape` «Зброя бʼє фіксованою формою клітин (1×4, 2×2)» · entities/combat · 📎 · слот {shape}.
  - `+arrow-path-panels` «Шлях зі стрілок, що веде аватара; змінюється зсувами поля» · entities/move · 🥈.
  - `+weapon-durability` (вже пропонована Fire Emblem); `+timing-judgement-bonus` (Magical Beat) ↔ Action Command; `+timing-window` ↔ захист; `+hint-move` ↔ підказка розстановки.
  - `+buy-time` «Купити секунди за валюту» · game-logic/economy · 🌱.
  - `+pity-discount` «Прихований лічильник помилок → знижки/допомога» · game-logic/difficulty · 🌱.

## Пропозиції до словників
- `+axis:field=polar` — полярна сітка «кільця × сектори» з центром (Origami King, Castle Panic, Frostpunk).
- `+effect:damage_area` — шкода по фігурі клітин (лінія 1×4, квадрат 2×2), а не одній цілі.
- `+cond:timing_window` — натискання потрапило у вікно такту (Action Command, захист).
- `+trigger:lineup_end` — кінець фази розстановки (ходи / таймер / підтвердження).
- `+feature:buy-time` — докупити час фази за валюту; `+feature:pity-discount` — прихована допомога гравцеві за помилки.
- `+window:battle-command` — меню бойових команд (зброя, предмети, втеча).
- `+card:lineup-bonus`, `+card:attack-shape`, `+card:arrow-path-panels` — див. «Мапа на каталог».

## Джерела
- ⭐ [Super Mario Wiki: Paper Mario: The Origami King](https://www.mariowiki.com/Paper_Mario:_The_Origami_King) — 4 кільця × 12, Rotate/Slide на L/R, 1,5× за лінію чи 2×2, пропуск розстановки, таймер і ліміт з undo, Buy Time (Minus), Cheer до 999 монет, форми атак, міцність зброї, Action Command, захист, партнери, Mechakoopa, wave-бої, бонуси монет, Miss Points, бос-бої (стрілки, Action Panel, двічі ту саму панель, зовнішні кільця, ON-коло, Hint Envelope), стрічка/діркопробивач/ножиці/лід, аксесуари, HP і сила атак.
- [Wikipedia](https://en.wikipedia.org/wiki/Paper_Mario:_The_Origami_King) — огляд бою, hammer 2×2 біля центру, boots 1×4, тоадів кличуть монетами, бос-бій навпаки.
- [GameWith: Earth Vellumental](https://gamewith.net/paper-mario-the-origami-king/article/show/20190) — 60 с на хід і 2 зсуви в бос-бою, кулак-панель у кінці шляху.
- YouTube: пошук «Paper Mario Origami King ring battle».

## Непевне
- (?) Геометрія Slide: промінь з 8 клітин (4 + 4 протилежні) зсувається крізь центр по колу — з памʼяті; Wikipedia каже лише «horizontally or vertically».
- (?) Скільки ходів і секунд дається у звичайному бою (у бос-бою на GameWith — 60 с і 2 зсуви; «Ring Moves 2~3» без пояснень).
- (?) Чи бонус 1,5× вимагає, щоб **усі** вороги були вишикувані, і як рахується «додаткова дія» за кожну групу.
- (?) Точні назви й порядок пунктів бойового меню та кнопки Action Command для молота.
- (?) Як саме промені зсуваються в бос-бою (там зсуваються панелі зі стрілками, а не вороги) і що робить коло без ON.
