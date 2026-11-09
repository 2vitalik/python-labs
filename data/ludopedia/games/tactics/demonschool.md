---
title: Demonschool
slug: demonschool
aka: []
family: tactics
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: partial
  random: none
  goal: state
year: 2025
platforms: [PC, macOS, Linux, Switch, PS4, PS5, Xbox One, Xbox Series]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Demonschool", best: true, note: "огляд: планування дій наперед і одночасне виконання, undo, вишикування атак, синергія загону, тижневий календар; Necrosoft / Ysbryd, 19.11.2025"}
  - {kind: steam, url: "https://store.steampowered.com/app/1900250/Demonschool/", note: "опис: «plan movements, execute them all at once», бафи/дебафи, комбо зі стихіями, 15 персонажів, ранок/полудень/ніч"}
  - {kind: other, url: "https://gameinformer.com/review/demonschool/class-is-in-session", note: "огляд: зростаюча ціна дій, рух по прямих і діагоналях, печатка → дальній край, прорив бар'єра = поразка, комбо-катсцени"}
  - {kind: other, url: "https://www.gamesmarket.global/demonschool/", note: "огляд: рух = дія, спільний пул AP на 4 персонажів, фаза планування / фаза дії"}
  - {kind: other, url: "https://www.mejoress.com/?p=293928", note: "гайд: класи Phaser/Ranger/Brawler/Modifier, Grunt-прорив, боси тижнів 0–10, статуси, ліміти ходів"}
  - {kind: other, url: "https://www.pockettactics.com/demonschool/review", note: "огляд (403 при fetch): перший хід персонажа — 1 AP, другий — 2…"}
  - {kind: steam, url: "https://store.steampowered.com/app/4820500/Demonschool_Puzzle_Killers/", note: "DLC Puzzle Killers: 50 бойових задач на один хід"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Demonschool+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [hp-damage, push-object, status-effects, telegraphed-intents, telegraph-marker, enemy-reached-base, spawner-entity, melee-vs-ranged, undo-unlimited, restart-level, sequential-levels, map-window, main-menu, pause-menu, game-screen, +move-attack, +action-points, +cost-escalation, +shared-action-pool, +plan-then-execute, +character-classes, +special-combos, +elemental-weakness, +seal-quota-then-exit, +turn-limit-objectives, +knockback, +calendar-social-sim, +relationship-levels, +puzzle-battles]
proposes: ["+card:shared-action-pool", "+card:plan-then-execute", "+card:seal-quota-then-exit", "+window:calendar-window", "+effect:combo_attack(units, target)"]
author: opus
date: 2026-11-09
---

# Demonschool — тактика, де рух і є удар: загін із спільним пулом очок планує хід з відкатом і виконує разом

## Суть
Студентка Фей і її друзі на острівному кампусі б'ються з демонами на сітці; поза боями — тижневий календар занять, дружби й побачень (sim-частина). У бою гравець **планує** дії всього загону, бачить, як відповідатимуть вороги, вільно відкочує й переставляє, а потім виконує все одним махом. Атака — це рух: персонаж біжить по прямій чи діагоналі й бʼє тих, у кого впирається, тож суть — вишикувати маршрути так, щоб один забіг зачепив кількох. Очки дій спільні на загін, а кожен наступний хід того самого персонажа дорожчий — гра штовхає грати всіма.

## Поле і час
- Ізометрична сітка (Games Market); рух по прямих і діагоналях (Game Informer); на деяких аренах — круглий майданчик, «арена, що звужується» (бос Tongue Circle).
- Хід: фаза планування (дії, undo, превʼю відповіді ворогів) → фаза дії (заплановане виконується разом) → вороги. Таймера нема.
- Типовий бій: убити досить демонів, щоб заповнити печатку, потім дійти до дальнього краю поля; демон, що дійшов до «нашого» краю і лишився там, ламає барʼєр — поразка.
- Інформація часткова: наміри ворогів і босів телеграфуються, але підкріплення (спавн) і фази боса — ні.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фей | piece | клас; SPECIAL | лідерка; SPECIAL для комбо-атак; навичка No Knockback прибирає відкидання з її атак |
| Namako | piece | — | Defense Down (ціль отримує ×2 шкоди), Burning Fist (опік) |
| Knute | piece | — | бафф Attack Up +1 союзнику |
| Ti | piece | — | SPECIAL відштовхує ворогів з HP ≥ 2 у кількох напрямках |
| Ocean | piece | — | пробивний SPECIAL по кількох цілях |
| Mercy, Henk та ін. | piece | — | Mercy — «звіролов»; Henk скидає обʼєкти на поле (Game Informer) |
| Phaser (клас) | piece | — | мобільний, проходить крізь ворогів (крізь босів — ні) |
| Ranger (клас) | piece | — | ворог на шляху блокує рух — дорого «пробиватися» |
| Brawler (клас) | piece | — | проштовхується крізь натовп |
| Modifier (клас) | piece | — | однакова шкода будь-якому босу |
| Grunt | enemy | — | іде до нашого краю; дійшов і лишився — прорив барʼєра |
| Polyp | spawner | — | якщо не вбити — породжує Grunt-ів |
| Tongue | enemy | 1 HP | гине з одного удару, але відштовхує загін |
| Meat Cube | enemy | 40 HP | слабкий до вогню |
| Міна | object | — | можна копнути (напр., у зону поїдання боса-краба) |
| Силове поле | static | — | перешкода, блокує рух |
| Бос тижня | boss | фази | телеграфує удари, змінює поле й правила (лінійні атаки, звуження арени, спавн, телепорт) |
| Зона поїдання | zone | — | ворог, що зайшов, зʼїдений — бос лікується |
| Печатка | resource | квота | наповнюється вбивствами демонів |
| Шкала SPECIAL | resource | — | повна — комбо-атака загону |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, piece, line)` → ЯКЩО `counter(ap_pool, >=, cost(piece))` → ТО `move(piece, line)`, `counter(ap_pool, -cost)`, `custom: «наступний хід цього персонажа дорожчий: 1 → 2 → 3…»`.
- КОЛИ `contact(piece, enemy)` (рух у ворога) → ТО `damage(enemy, atk)` — `custom: «рух = атака»`.
- КОЛИ `contact(phaser, enemy)` → ЯКЩО `not state(enemy, boss)` → ТО `custom: «проходить крізь, б'ючи»`; інакше `block`.
- КОЛИ `blocked(ranger)` → ЯКЩО `occupied(cell_ahead, enemy)` → ТО `block` (спершу треба прибрати того, хто на шляху).
- КОЛИ `contact(brawler, enemy)` → ТО `push(enemy)` і рух далі.
- КОЛИ `input(undo)` → ЯКЩО `custom: «фаза планування»` → ТО `undo(1)`.
- КОЛИ `input(confirm)` → ТО `custom: «усі заплановані дії виконуються разом»`, `end_turn`.
- КОЛИ `turn_start(player)` → ТО `custom: «вороги й бос показують, що зроблять»`.
- КОЛИ `custom: «атака Namako»` → ТО `set_state(enemy, defense_down)`; КОЛИ `after(damage(enemy))` → ЯКЩО `state(enemy, defense_down)` → ТО `damage(×2)`.
- КОЛИ `custom: «бафф Knute»` → ТО `set_state(ally, attack_up)` (+1 шкоди).
- КОЛИ `turn_end(enemy)` → ЯКЩО `state(unit, burn|poison)` → ТО `damage(unit, n)`.
- КОЛИ `after(damage(enemy, element))` → ЯКЩО `custom: «слабкість до стихії»` → ТО `custom: «підвищена шкода»` (Meat Cube ← вогонь).
- КОЛИ `counter(special, >=, full)` → ТО `custom: «комбо-атака кількох персонажів з катсценою»`, `damage(big)`; лінійні SPECIAL — нескінченна дальність по лінії.
- КОЛИ `destroyed(demon)` → ТО `counter(seal, +1)`, `counter(special, +n)` (?).
- КОЛИ `reach(party, far_edge)` → ЯКЩО `counter(seal, >=, quota)` → ТО `win`.
- КОЛИ `reach(grunt, our_edge)` → ЯКЩО `custom: «лишився там до кінця ходу»` → ТО `lose` (барʼєр прорвано).
- КОЛИ `turn_end(enemy)` → ЯКЩО `count(polyp, >, 0)` → ТО `spawn(grunt)`.
- КОЛИ `contact(tongue_attack, piece)` → ТО `push(piece)`; КОЛИ `contact(piece, tongue)` → ТО `disappear_b`.
- КОЛИ `custom: «атака боса»` → ТО `push(party, back)` (тижні 0, 2, 8 — до стін / назад).
- КОЛИ `enter(enemy, feeding_zone)` → ТО `disappear_a`, `heal(boss, n)`.
- КОЛИ `custom: «бій з босом»` → ЯКЩО `counter(turn, >, limit)` → ТО `custom: «втрачено досягнення»` (?).
- КОЛИ `input(reset_fight)` → ТО `restart`.
- Перемога: печатка + дальній край / знищити боса до ліміту ходів · Поразка: прорив барʼєра · Рахунок: —.

## Керування і ввід
- Курсор/геймпад: вибір персонажа → маршрут по прямій або діагоналі; гра одразу показує наслідки й відповідь ворогів; undo будь-якої запланованої дії.
- Порядок: можна «нитками» з'єднувати рухи кількох персонажів, перескакуючи від ворога до ворога, потім — підтвердити хід.
- Пауза-меню: миттєвий рестарт бою.

## Вікна, меню, HUD
- `main-menu`: нова гра, продовжити, налаштування (`settings-window`).
- `custom-window` «Календар»: тиждень з днями й слотами ранок / полудень / ніч; заняття, клуби, вихідні; кожна пʼятниця — бій з босом (тижні 0–10).
- `map-window` — кампус і острів: куди піти, з ким говорити, побічні квести.
- `dialogue-window` — розмови, побачення, дружби (15 персонажів).
- `upgrade-window` (?) — рівні, навички, Aspect Shifts (потрібні три персонажі).
- `game-screen`: ізометрична сітка; `action-points` (спільний пул); `progress-bar` (печатка); шкала SPECIAL; `telegraph-marker`; `hp-bar` ворогів; `undo-button`; `end-turn-button` (підтвердити); `turn-counter` (бос).
- `pause-menu`: рестарт бою, налаштування; `end-screen` бою.

## Фічі поза полем
- Календар семестру: дні можна пропускати; активності (караоке, риболовля, готування) підвищують звʼязки; звʼязки → рівні, навички, здібності.
- Побічні квести на острові; один відеокасетний «вечір» на вихідних (рецензія в газеті в понеділок).
- `restart-level` (рестарт бою з паузи); `achievements` (за ліміти ходів).
- DLC Puzzle Killers: 50 бойових задач «розв'яжи за один хід» фіксованим загоном; нові предмети-сфери (поповнити SPECIAL, дати техніку).

## Варіації й родичі
- Родичі: [Into the Breach](into-the-breach.md) (телеграф і задачі одного ходу), [Persona 5 Tactica](persona-5-tactica.md) (соціальна частина + тактика), [Yggdra Union](yggdra-union.md) (спільний ресурс ходів), [Frozen Synapse](frozen-synapse.md) (план → виконання), [Hoplite](hoplite.md) (атака рухом).
- **Осі варіацій**: атака — окрема дія / рух = атака (Demonschool, Hoplite) · очки дій — на юніта / спільний пул загону з наростаючою ціною · виконання — одразу / планування з відкатом і одночасне виконання.

## Цікавинки для курсу
- Рух як атака по прямій: персонаж біжить до першої перешкоди й бʼє все, у що впирається; класи міняють, що буде далі (крізь / зупинка / проштовхування) — 🥉.
- Спільний пул AP з наростаючою ціною (1, 2, 3… для того самого персонажа) — 📎, але дуже змінює рішення.
- Планування з відкатом і одночасне виконання — 🥈 (симуляція плану на копії стану, превʼю відповіді ворога).
- Печатка-квота → «тепер дійди до краю»: двофазна ціль бою — 🌱.
- Grunt дійшов до краю = поразка, Polyp множить Grunt-ів — 📎 (оборонна ціль у наступальній тактиці).

## Мапа на каталог
- Є: `hp-damage` · `push-object` (Brawler, Ti, Tongue) · `status-effects` (опік, отрута, Defense Down) · `telegraphed-intents` + `telegraph-marker` · `enemy-reached-base` (прорив барʼєра) · `spawner-entity` (Polyp) · `melee-vs-ranged` (лінійні SPECIAL) · `undo-unlimited` · `restart-level` · `map-window` · вікна.
- **Нема** → пропозиції карток:
  - `+shared-action-pool` «Спільний пул очок дій загону» · game-logic/opponent · 📎 · слот {cost: escalating}.
  - `+plan-then-execute` «Планування ходу з відкатом і одночасне виконання» · game-logic/history · 🥈.
  - `+seal-quota-then-exit` «Квота вбивств відкриває вихід» · game-logic/win · 🌱.
  - `+move-attack` «Атака рухом» (запропоновано Hoplite) · `+cost-escalation` · `+elemental-weakness` · `+calendar-social-sim` · `+puzzle-battles` (DLC).

## Пропозиції до словників
- `+card:shared-action-pool` — один пул AP на весь загін; ціна дії росте для персонажа, що вже ходив.
- `+card:plan-then-execute` — увесь хід плануєш з undo і превʼю, виконується разом.
- `+card:seal-quota-then-exit` — двофазна ціль: набрати квоту вбивств, потім дійти до краю.
- `+window:calendar-window` — календар днів/слотів часу між боями (Demonschool, Persona-подібні).
- `+effect:combo_attack(units, target)` — спільна атака кількох персонажів по одній цілі.

## Джерела
- ⭐ [Wikipedia: Demonschool](https://en.wikipedia.org/wiki/Demonschool) — бій: план наперед, одночасне виконання, undo, вишикування; календар; розробник, платформи, рецепція.
- [Steam](https://store.steampowered.com/app/1900250/Demonschool/) — опис бою, бафи/дебафи, комбо-стихії, персонажі.
- [Game Informer](https://gameinformer.com/review/demonschool/class-is-in-session) — наростаюча ціна дій, прямі й діагоналі, печатка й дальній край, прорив барʼєра.
- [Games Market](https://www.gamesmarket.global/demonschool/) — рух = дія, спільний пул AP на 4 персонажів, фази.
- [Mejoress: гайд](https://www.mejoress.com/?p=293928) — класи, вороги, боси тижнів 0–10, статуси, ліміти ходів.
- [Steam: Puzzle Killers](https://store.steampowered.com/app/4820500/Demonschool_Puzzle_Killers/) — DLC з задачами на один хід.

## Непевне
- (?) Точна механіка «рух = атака»: чи персонаж зупиняється перед ворогом, чи пробігає крізь і бʼє всіх по лінії (залежить від класу).
- (?) Ціна ходу 1 → 2 → … і розмір пулу AP — з цитати Pocket Tactics у пошуку (сторінка 403); «Ranger: 3 HP на шляху = 6 AP» з гайду — незрозумілий розрахунок.
- (?) Чи заплановані дії справді виконуються одночасно, чи послідовно після підтвердження (Wikipedia: simultaneously; Games Market: «executed immediately»).
- (?) Що дає загибель персонажа в бою; чи ліміт ходів боса — поразка, чи лише втрата досягнення (гайд суперечить сам собі).
- (?) Чи печатка наповнює й шкалу SPECIAL (Game Informer: «meter fills are tied to the seal objective»).
