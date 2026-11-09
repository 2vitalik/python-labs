---
title: HeroClix
slug: heroclix
aka: [Хероклікс, Clix, "Marvel HeroClix", "DC HeroClix"]
family: tactics
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: runtime
  goal: score
year: 2002
platforms: [board]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/HeroClix", best: true, note: "бойовий диск у підставці, стати й клацання, сітка 35 мм, мапи, бюджет команди кратний 100, історія WizKids/NECA"}
  - {kind: other, url: "https://rulespal.com/heroclix/rulebook", note: "правила: фази ходу, ліміт дій = бюджет/100, маркери дій і pushing, рух на 8 напрямків, breakaway, лінія вогню, кольори терену, 2d6, крити, knockback, обʼєкти, перемога за очками KO"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=HeroClix+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 65
mechanics: [hp-damage, melee-vs-ranged, line-of-sight-attack, impassable-cells, floor-types, height-levels, move-8dir, item-pickup, inventory-items, hot-seat, turn-enforcement, destroy-all-enemies, time-out, match-setup, reachable-highlight, threat-range, selection-highlight, +combat-dial, +wound-track-stats, +army-points-draft, +action-total-budget, +action-tokens-push, +breakaway-roll, +zone-of-control, +two-d6-vs-defense, +critical-hit-miss, +knockback, +multi-target-bolts, +color-coded-powers, +keyword-themed-team, +team-abilities, +throwable-objects, +ko-points-victory, +tiebreak-chain, +initiative-roll, +sideline-reserve]
proposes: ["+effect:roll_dice", "+effect:knockback", "+trigger:attacked", "+trigger:round_end", "+cond:adjacent8", "+cond:elevation(a, op, b)", "+effect:click(a, n)", "+role:dial", "+ui:combat-dial-view", "+ui:action-tokens", "+ui:action-total", "+ui:dice-tray", "+window:team-builder", "+feature:build-total", "+axis:damage-model:dial", "+card:combat-dial"]
author: opus
date: 2026-11-09
---

# HeroClix — мініатюри супергероїв, у підставці яких бойовий диск: кожне поранення клацає диск і показує нові стати й сили

## Суть
Гравці збирають команду фігурок за бюджетом очок (зазвичай 300) і бʼються на квадратній сітці мапи. Під кожною фігуркою — **бойовий диск (combat dial)**: у віконці видно поточні Speed, Attack, Defense і Damage з кольоровими квадратиками сил; кожна одиниця шкоди повертає диск на «клік», і з'являється новий рядок — зазвичай слабший, але буває й сильніший; KO — коли у віконці зʼявляється символ KO. Темп задає **ліміт дій** на хід (1 на кожні 100 очок), а повторна дія тим самим героєм два ходи поспіль коштує шкоди (pushing).

## Поле і час
- Мапа з сіткою квадратів 35 × 35 мм; стандартні мапи 3 × 3 фути або 2 × 3 фути; стартова мапа Marvel Universe — 13 × 13 клітин. Терен позначено кольоровими контурами.
- Терен: clear — без ефекту · hindering (зелений) — сповільнює рух і заважає лінії вогню · blocking (коричневий) і стіни (чорні лінії) — непрохідні й блокують лінію вогню · elevated (червоний) — пронумеровані рівні висоти · water (синій) — заважає лише рухові · obscuring (білий) — заважає лише лінії вогню · indoor (жовтий) — приміщення на змішаних мапах · special terrain — перекриває терен назавжди.
- Сусідство — 8 клітин (бік або діагональ); блокуючий терен, стіни й різна висота сусідство розривають.
- Хід гравця — 4 фази: Beginning of Turn → Action → End of Turn → Clear; гравці ходять по черзі.
- Гра йде до перемоги однієї сторони або до ліміту часу (найчастіше 50 хвилин).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Персонаж | piece | диск: Speed, Attack, Defense, Damage, Range + блискавки (кількість цілей), очки, ключові слова, символ команди | 1 платна дія за хід; клацає диском від шкоди й лікування |
| Бойовий диск | mark | позиції-кліки, стартова лінія, KO-кліки | поточний клік визначає всі стати й кольорові сили |
| Сила (power) | mark | кольоровий квадрат біля значення на диску; спецсила — білий з чорною рамкою | ефект за картою сил (PAC); напр. рожевий у Speed — Sidestep, коричневий у Damage — Perplex |
| Символ на значенні | mark | крило / дельфін у Speed; Auto в Attack; смуга в Defense; Tiny / Giant / Colossal у Damage | Flight · Swim · Autonomous · Indomitable · розмір (Giant Reach:2, Colossal Reach:3) |
| Перехожий (bystander) | piece | стати без диска | не лікується; будь-яка шкода → KO |
| Легкий обʼєкт | object | жовте кільце | підняти, нести, покласти; кілька в одній клітині |
| Важкий обʼєкт | object | червоне кільце | як легкий; у клітині цілі заважає лінії вогню |
| Особливий обʼєкт | object | ≥5 клітин від стартових зон | власний ефект (?) |
| Маркер дії | mark | 0–2 на персонажі | другий = pushed і 1 шкоди; знімається, якщо цього ходу дії не було |
| Hindering-терен | terrain | зелений | вхід зупиняє рух; старт у ньому — половина швидкості |
| Blocking-терен / стіна | static | коричневий / чорна лінія | не пройти, не бачити крізь; обʼєкти руйнуються дією Destroy (шкода ≥3) |
| Висота | terrain | рівень | розриває сусідство, впливає на лінію вогню; падіння при knockback — 2 шкоди |
| Вода | terrain | синій | заважає рухові |
| Obscuring | terrain | білий | заважає лише лінії вогню |
| Стартова зона | zone | край мапи | розстановка на початку |
| Sideline | supply | до 3 елементів на 100 очок, макс. 15 | запас поза полем для ефектів |
| KO-зона | zone | — | вибулі персонажі; їхні очки йдуть супернику |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `custom: «початок гри»` → ТО `custom: «відкрити команди, кидок за першого гравця (+1 за кожного персонажа тематичної команди)»`, вибір мапи й стартових зон, розстановка персонажів, потім обʼєктів.
- КОЛИ `turn_start(player)` → ТО `set_value(actions_left, build_total / 100)` — від 2 до 10.
- КОЛИ `input(action, c, MOVE | CLOSE | RANGE | POWER)` → ЯКЩО `counter(actions_left, >, 0)` and `counter(tokens(c), <=, 1)` and `custom: «c ще не отримав платної дії цього ходу»` → ТО `custom: «виконати дію»`, `mark(c, action_token)`, `counter(actions_left, -1)`.
- КОЛИ `input(action, c, DOUBLE_POWER)` → ЯКЩО `counter(tokens(c), ==, 0)` → ТО `custom: «два маркери одразу»`.
- КОЛИ `input(action, c, FREE)` → ТО `custom: «без ліміту й маркера, той самий FREE-ефект раз за хід»`.
- КОЛИ `custom: «персонаж отримав другий маркер»` → ТО `set_state(c, pushed)`, `damage(c, 1)` — pushing damage, зменшити його можуть лише ефекти, що прямо про це кажуть.
- КОЛИ `phase_start(clear)` → ЯКЩО `custom: «c не отримав маркера цього ходу»` → ТО `unmark(c, action_tokens)`.
- КОЛИ `input(move, c)` → ЯКЩО `adjacent(c, enemy)` → ТО `custom: «breakaway: d6, 4–6 — відрив; інакше рух не відбувається, дію витрачено»`.
- КОЛИ `input(move, c, path)` → ЯКЩО `custom: «кроків ≤ Speed, 8 напрямків»` → ТО `move(c, cell)` покроково; крізь своїх можна, зупинитися на зайнятій — ні.
- КОЛИ `enter(c, cell)` → ЯКЩО `custom: «клітина поруч із ворогом»` → ТО `custom: «рух закінчується»`.
- КОЛИ `enter(c, hindering)` → ТО `custom: «рух закінчується»`; КОЛИ `input(move, c)` → ЯКЩО `cell(start, hindering)` → ТО `speed(c, ×0.5)`.
- КОЛИ `input(move, c, cell)` → ЯКЩО `cell(cell, blocking)` → ТО `block`.
- КОЛИ `input(close, a, b)` → ЯКЩО `adjacent(a, b)` → ТО атака (нижче).
- КОЛИ `input(range, a, targets)` → ЯКЩО `in_range(a, b, Range)` and `line_of_sight(a, b)` and `custom: «цілей ≤ кількості блискавок»` → ТО атака.
- КОЛИ `custom: «лінія вогню перетинає blocking-терен, персонажа в проміжній клітині або перепад висоти»` → ТО `block`; через hindering або важкий обʼєкт у клітині цілі — `custom: «лінія вогню hindered»`.
- КОЛИ `custom: «атака»` → ТО `custom: «2d6 + Attack(a) ≥ Defense(b) — влучання в кожну таку ціль»`, `damage(b, Damage(a))`.
- КОЛИ `custom: «дубль 6»` → ТО `custom: «влучання в усі цілі»`, `damage(b, +1)`.
- КОЛИ `custom: «дубль 1»` → ТО `custom: «промах усім»`, `damage(a, 1)` — незменшувана.
- КОЛИ `custom: «b отримав n шкоди»` → ТО `rotate(dial(b), +n clicks)` — у віконці новий рядок статів і сил.
- КОЛИ `custom: «b лікують на n»` → ТО `heal(b, n)`, `rotate(dial(b), -n clicks)`; не вище стартової лінії й не на KO-клік.
- КОЛИ `custom: «у віконці KO-клік або KO-символ замість значення»` → ТО `disappear(b)` у KO-зону; суперник `score(+point_value(b))`.
- КОЛИ `custom: «перехожий отримав будь-яку шкоду»` → ТО `disappear(b)`.
- КОЛИ `custom: «влучання з дублем або KNOCKBACK»` → ТО `custom: «b відлітає на кількість клітин = кліків шкоди, прямо від атакувальника»`.
- КОЛИ `blocked(b)` → ЯКЩО `custom: «під час knockback — персонаж, blocking, край мапи або вища висота»` → ТО `damage(b, 1)`; КОЛИ `custom: «knockback з висоти вниз»` → ТО `damage(b, 2)`.
- КОЛИ `input(pickup, c, object)` → ЯКЩО `occupied(cell, object)` → ТО `pickup(c, object)`; покласти — `place(c, object)`.
- КОЛИ `input(destroy, c, object|blocking)` → ЯКЩО `custom: «Damage(c) ≥ 3»` → ТО `disappear(object)` або `set_cell(cell, clear)`.
- КОЛИ `custom: «у гравця нема персонажів вартістю ≥1 очка»` → ТО `lose` (для нього).
- КОЛИ `all_gone(enemy_characters)` → ТО `win`; КОЛИ `counter(time_left, <=, 0)` → ТО `custom: «підрахунок: очки стартової лінії кожного ворожого KO + очки знищених ворожих обʼєктів»`; нічия — `custom: «кидок 2d6»`.
- Перемога: остання непереможена сторона або більше очок на кінець часу · Поразка: нема персонажів вартістю ≥1 · Рахунок: сума очок KO-нутих суперників.

## Керування і ввід
- Настільна: гравець вказує персонажа й дію, рахує клітини, кидає 2d6, сам повертає диск у підставці на потрібну кількість кліків; маркери дій кладе біля підставки.
- (цифрова версія) клік по фігурці → `reachable-highlight` на Speed (з урахуванням hindering і зупинки поруч із ворогом) → клік по клітині; атака — клік по цілі в радіусі з перевіркою лінії вогню; анімація клацання диска з показом нового рядка.
- Ліміт дій на хід — видно лічильником; FREE-дії не рахуються.

## Вікна, меню, HUD
- (цифрова версія) `main-menu` → `+window:team-builder` (бюджет 300 / кратний 100, унікальні й Prime — по одному, до 3 обʼєктів, Sideline, тематична команда за ключовим словом) → `match-setup` (мапа, ліміт часу, кількість гравців 2–4) → `game-screen`.
- `game-screen`: сітка мапи з кольоровими контурами терену; на виділеному персонажі `+ui:combat-dial-view` (поточний клік: значення з кольоровими квадратами сил), `tooltip` сили з картки PAC; `+ui:action-tokens` біля фігурок; `+ui:action-total` (лишилось дій); `turn-indicator`; `timer-countdown` 50 хв; `threat-range` / дальність; `+ui:dice-tray` 2d6; KO-зона з очками (`captured-pieces`).
- `codex-window` — картка персонажа (здібності, що не влазять на диск) і карта сил/здібностей.
- `end-screen` — переможець і підрахунок очок.

## Фічі поза полем
- Командобудування за бюджетом очок: **build total** кратний 100, ліміт дій з нього; унікальні персонажі — по одному; тематичні команди дають бонус ініціативи й Probability Control (X = кількість, макс. 5).
- Команди-здібності за символом на підставці; ключові слова на картці.
- Серії фігурок (колекційні бустери): Marvel, DC та інші ліцензії; Feats і Battlefield Conditions — карти пізніших правил; Team Bases (2013) — командна гра.
- Досвід колись показувала кольорова облямівка (Rookie / Experienced / Veteran) — тепер не використовується.
- Ліміт часу й турнірний підрахунок очок.

## Варіації й родичі
- Родичі в корпусі: [Heroscape](heroscape.md) (мініатюри, кубики, висота), [Tannhäuser](tannhauser.md) (трек здоровʼя знижує стати), [D&D grid combat](dnd-grid-combat.md) (квадрати, зупинка біля ворога), [Mage Knight (настільна)](mage-knight.md) — інша гра WizKids-лінії (?).
- **Осі варіацій**:
  - **модель шкоди**: HP-лічильник / маркери ран / **диск, де шкода міняє стати й сили** / трек рядків ([Tannhäuser](tannhauser.md));
  - **хто ходить**: увесь загін / **N дій на хід, кожен персонаж раз** / маркери наказів ([Heroscape](heroscape.md));
  - **втома**: нема / **pushing — повтор дії два ходи поспіль коштує шкоди**;
  - **зупинка руху**: нема / біля ворога (zone of control) + кидок на відрив;
  - **кубики**: сума 2d6 проти порогу + крити на дублях / пул з успіхами / символи.

## Цікавинки для курсу
- Бойовий диск: стан персонажа = індекс у списку рядків статів, шкода й лікування рухають індекс — 🌱 (і чудово показує «стан як дані»).
- Pushing: другий маркер дії поспіль → 1 шкоди; маркери знімаються лише після ходу без дії — 📎 (таймер відпочинку на сутності).
- Ліміт дій = бюджет/100 (2–10) — темп залежить від розміру армії — 🌱.
- Breakaway + зупинка руху біля ворога (zone of control на 8 сусідів) — 📎.
- Лінія вогню з 3 причинами блокування і 2 причинами hindered — 🥉 (Брезенгем + висота).
- Knockback: відкидання на кількість кліків з шкодою від упору й падіння — 📎.
- Перемога за очками KO на кінець таймера + 2d6-тайбрейк — 🌱.

## Мапа на каталог
- Є: `hp-damage` ↔ кліки диска · `melee-vs-ranged` ↔ CLOSE / RANGE · `line-of-sight-attack` ↔ лінія вогню · `impassable-cells` ↔ blocking і стіни · `floor-types` ↔ hindering / water / obscuring · `height-levels` ↔ elevated · `move-8dir` · `item-pickup` + `inventory-items` ↔ обʼєкти · `hot-seat`, `turn-enforcement` · `destroy-all-enemies` + `time-out` ↔ дві умови кінця · `match-setup`, `reachable-highlight`, `threat-range`, `selection-highlight`.
- **Нема** → пропозиції карток:
  - `+combat-dial` «Бойовий диск: стати за кліком» · entities/state · 🌱 · слот {clicks, ko_marker} — HP як індекс у таблиці станів.
  - `+wound-track-stats` «Шкода міняє всі стати» · entities/state · 🌱 (спільна з Tannhäuser).
  - `+army-points-draft` «Команда за бюджетом очок» · interface/menus · 📎 · слот {budget, uniques}.
  - `+action-total-budget` «Ліміт дій на хід з бюджету» · game-logic/opponent · 🌱 · слот {per_points: 100, min: 2, max: 10}.
  - `+action-tokens-push` «Маркери дій і шкода за повтор» · entities/state · 📎 · слот {max_tokens: 2, push_damage: 1}.
  - `+breakaway-roll` «Кидок на відрив від ворога» · entities/move · 🌱 · слот {success: 4-6}.
  - `+zone-of-control` «Рух зупиняється біля ворога» · entities/move · 🌱.
  - `+two-d6-vs-defense` «2d6 + атака ≥ захист» · entities/combat · 🌱; `+critical-hit-miss` «дубль 6 / дубль 1» · 🌱.
  - `+knockback` «Відкидання з шкодою від упору» · entities/combat · 📎.
  - `+multi-target-bolts` «Кількість цілей атаки» · entities/combat · 🌱.
  - `+color-coded-powers` «Кольоровий код сили біля стату» · entities/state · 📎 · слот {legend}.
  - `+keyword-themed-team` · `+team-abilities` · `+throwable-objects` · `+ko-points-victory` · `+tiebreak-chain` · `+initiative-roll` · `+sideline-reserve`.

## Пропозиції до словників
- `+effect:roll_dice` — кинути кубики як ефект (2d6 атаки, breakaway d6, тайбрейк).
- `+effect:knockback` — відкинути ціль на N клітин від атакувальника з перевіркою упору.
- `+trigger:attacked` — ціль атаки (реактивні сили); `+trigger:round_end` — кінець ходу гравця (фаза Clear).
- `+cond:adjacent8` — сусідство на 8 напрямків з розривом стінами й висотою (у словнику лише варіант тригера).
- `+cond:elevation(a, op, b)` — порівняння висоти (лінія вогню, knockback-падіння).
- `+effect:click(a, n)` — повернути диск стану на n позицій (альтернатива `rotate` для «стану як індексу»).
- `+role:dial` — сутність-таблиця станів, привʼязана до фігури.
- `+ui:combat-dial-view` — віконце диска з поточними значеннями й кольоровими силами; `+ui:action-tokens` — маркери дій біля фігур; `+ui:action-total` — лишилось дій на хід; `+ui:dice-tray`.
- `+window:team-builder` — бюджет, унікальні, Sideline, тематична команда; `+feature:build-total` — розмір гри як число очок, що масштабує ліміт дій.
- `+axis:damage-model:dial` — нова вісь «модель шкоди»: hp · wounds · dial · track.
- `+card:combat-dial` — диск як навчальний приклад таблиці станів.

## Джерела
- ⭐ [Wikipedia: HeroClix](https://en.wikipedia.org/wiki/HeroClix) — диск і клацання, перелік статів, кольори досвіду, сітка 35 мм і розміри мап, бюджет кратний 100, 2d6, історія (WizKids 2002, Topps, NECA 2009), Feats, Team Bases.
- [RulesPal: HeroClix rulebook](https://rulespal.com/heroclix/rulebook) — повні правила: фази, ліміт дій, маркери і pushing, рух і breakaway, сусідство й лінія вогню, кольори терену, атака й крити, кліки й KO, knockback, обʼєкти, перемога й таймер; другий шматок — символи на значеннях, тематичні команди, перехожі.
- YouTube: пошук «HeroClix how to play».

## Непевне
- (?) Що саме дає «hindered» лінія вогню (за памʼяттю — +1 до Defense цілі) — у прочитаному уривку не сказано.
- (?) Повний список стандартних сил і кольорів (карта PAC) — у прочитаних уривках лише приклади Sidestep і Perplex.
- (?) Метання обʼєктів як атака — за памʼяттю; RulesPal підтверджує лише «підняти, нести, покласти, знищити».
- (?) Онлайн-версія (HeroClix Online) — за памʼяттю, сторінку не відкривав; вікна — як «цифрова версія».
- (?) Походження диска від Mage Knight: Rebellion (2000, WizKids) — за памʼяттю; файл [mage-knight](mage-knight.md) описує іншу гру (2011).
