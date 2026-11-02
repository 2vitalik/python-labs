---
title: Arknights
slug: arknights
family: tower-lanes
also: [tactics]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: none
  goal: survive
year: 2019
platforms: [Android, iOS, PC]
links:
  - {kind: fandom, url: "https://arknights.wiki.gg/wiki/Operation", best: true, note: "Terra Wiki: екран операції — LP, DP, ліміт юнітів, розгортання з напрямком, redeploy, навички, 1×/2×, рейтинги"}
  - {kind: fandom, url: "https://arknights.wiki.gg/wiki/Block", note: "блокування: Block N, вороги на 2–4 Block, неблоковані"}
  - {kind: fandom, url: "https://arknights.wiki.gg/wiki/Cost", note: "ціна DP: повернення 50 % при відступі, ×1.5/×2 при повторному розгортанні"}
  - {kind: fandom, url: "https://arknights.wiki.gg/wiki/Deployment_Point", note: "DP: 1/с, межа 99, генерація авангардами"}
  - {kind: fandom, url: "https://arknights.wiki.gg/wiki/Terrain", note: "усі типи клітин: Protection Objective, Incursion Point, Hole, руни, лава, вода…"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Arknights", note: "огляд: класи, клітини ближні/дальні, режими, дати"}
  - {kind: official, url: "https://www.arknights.global/", note: "офіційний сайт (Yostar)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=arknights+gameplay+stage+clear", note: "пошук; проходження етапів"}
stage: v1
coverage: 65
mechanics: [enemy-waves, spawn-schedule, spawn-points, enemy-reached-base, round-currency, hp-damage, melee-vs-ranged, projectile-shot, blast-wave, temporary-modes, speed-per-type, impassable-cells, floor-types, teleport-one-way, game-pause, drag-drop-piece, legal-move-highlight, telegraphed-intents, level-select, level-unlock, replay, save-progress, dungeon-generation, shop-between-levels, +tower-placement, +tower-range, +placement-cooldown, +tile-class-placement, +block-count, +facing-range, +cost-escalation, +unit-limit, +skill-charge, +retreat-refund, +shift-push-pull, +auto-deploy, +run-relics, +loadout-select]
proposes: ["+trigger:blocked_by", "+trigger:sp_full", "+cond:cell", "+cond:block_free", "+effect:sell", "+effect:shift", "+effect:retreat", "+role:tower", "+role:unit", "+ui:deploy-bar", "+ui:skill-charge-ring", "+ui:range-circle", "+ui:enemy-route-preview", "+ui:dp-counter", "+window:loadout-select", "+window:squad-window", "+window:base-window", "+feature:auto-deploy", "+feature:gacha", "+feature:stamina", "+axis:control"]
author: opus
date: 2026-11-02
---

# Arknights — tower defense, де вежі — оператори: ближні тримають ворогів своїм тілом, дальні стріляють з висоти

## Суть
Ворожі загони йдуть фіксованими маршрутами від точок вторгнення до цілей захисту; кожен, хто дійшов, забирає Life Point. Гравець за **очки розгортання (DP)**, що капають щосекунди, ставить операторів з колоди-загону: ближніх — на низькі клітини дороги, дальніх — на високі. Ближній оператор **блокує** N ворогів на своїй клітині — вони зупиняються і бʼються з ним. Оператора можна відкликати (повернення половини DP), але повторне розгортання дорожче й чекає кулдаун.

## Поле і час
- Квадратна сітка (зазвичай ~10×7…12×9 (?)), камера під кутом. Клітини двох базових класів: **низькі** (дорога, по ній ходять вороги; сюди — ближні) і **високі** (платформи; сюди — дальні); плюс непридатні для розгортання клітини й декоративні стіни.
- Спецклітини: руни лікування/захисту/ППО, ями (Hole — зіштовхнутий ворог гине), кущі (невидимість), лава, вода, лід (ковзання), тунелі (вхід → вихід із затримкою), паркани (ближні можуть стояти, вороги не пройдуть).
- Real-time з паузою і 1×/2×; вибір оператора сповільнює час до ½. Хвилі за розкладом; маршрут наступного ворога показується пунктиром перед появою.
- Інформація часткова: загальний склад хвиль невідомий, вороги «відкриваються» в момент спавну.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Incursion Point (червона брама) | spawner | наземна / повітряна | вороги зʼявляються за розкладом |
| Protection Objective (синя брама) | static | — | ворог увійшов → −1 LP (боси — більше) |
| Низька клітина | terrain | — | маршрут ворогів; розгортання ближніх |
| Висока клітина | terrain | — | розгортання дальніх; вороги не ходять |
| Непридатна клітина / стіна | static | — | не можна розгорнути, ворог не йде |
| Hole (яма) | hazard | — | наземний ворог, зіштовхнутий сюди, гине |
| Руни (лікування, захист, ППО) | terrain | бонус | баф операторові на клітині |
| Тунель | terrain | пара вхід/вихід, затримка | ворог зникає і виходить з іншого місця |
| Vanguard (авангард) | tower | низька, Block 1–2, дешевий | генерує DP (навичка або за вбивство) |
| Guard (гвардієць) | tower | низька, Block 1–2 | основна шкода впритул |
| Defender (захисник) | tower | низька, Block 3 | тримає лінію, висока DEF |
| Specialist (спеціаліст) | tower | низька, Block 0–2 | штовхає/тягне, швидкий redeploy, пастки |
| Sniper (снайпер) | tower | висока, Block 0 | фізична шкода на відстані, пріоритет повітря |
| Caster (маг) | tower | висока | Arts-шкода (крізь броню), часто по площі |
| Medic (медик) | tower | висока | лікує союзників у радіусі |
| Supporter (підтримка) | tower | висока | сповільнення, дебафи, виклики |
| Виклик / пристрій | ally | Block, без повернення DP | дрон, стіна-барикада, пастка |
| Звичайний ворог | enemy | HP, ATK, DEF, RES, швидкість, Weight | іде маршрутом; блокований — бʼє блокувальника |
| Дальній ворог | enemy | дальність | стріляє в операторів, поки йде |
| Великий ворог | enemy | займає 2–4 Block | зупиняється лише тим, у кого вистачає Block |
| Неблокований / повітряний | enemy | — | ігнорує блок, летить/йде до цілі |
| Бос | boss | фази, кілька LP | змінює поведінку за HP/часом |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `timer(1 s)` → ТО `currency(dp, +1)` до межі 99; авангарди — `currency(dp, +n)` навичкою/за вбивство.
- КОЛИ `input(deploy, op, cell, facing)` → ЯКЩО `has(dp, cost)` and `custom: «cond cell(cell, low|high) відповідає класу»` and `free(cell)` and `count(deployed, <, unit_limit)` and `not state(op, redeploy_cd)` → ТО `spawn(op)`, `face(op, facing)`, `currency(dp, -cost)`; інакше `block`.
- КОЛИ `input(retreat, op)` → ТО `custom: «effect retreat: прибрати, повернути ⌊cost/2⌋ DP»`, `set_state(op, redeploy_cd, t)`.
- КОЛИ `hp_zero(op)` → ТО `disappear_a` без повернення DP, `set_state(op, redeploy_cd, t)`.
- КОЛИ `custom: «повторне розгортання»` → ТО `custom: «cost ×1.5 (вдруге), ×2 (далі), ≤ 99»`.
- КОЛИ `schedule(waves)` → ТО `spawn_at(enemy, incursion_point)`; наземний ворог `move(a, route)` по низьких клітинах; повітряний — своїм маршрутом над усім.
- КОЛИ `contact(enemy, op_cell)` → ЯКЩО `custom: «cond block_free(op) ≥ enemy.block_size»` and `not state(enemy, unblockable)` → ТО `custom: «блок: ворог зупинився, бʼє оператора»`; інакше ворог проходить далі.
- КОЛИ `custom: «ворог блокований»` → ТО він вважається в радіусі блокувальника незалежно від форми дальності.
- КОЛИ `in_range(op, enemy)` → ЯКЩО `custom: «клітина ворога у формі дальності, повернутій за facing»` → ТО `damage(type: physical|arts|true)` з періодом attack interval; медик — `heal(ally)` у радіусі.
- КОЛИ `custom: «фізична шкода»` → ТО `damage(max(ATK − DEF, 5 % ATK))`; Arts — `damage(ATK × (1 − RES%))` (?).
- КОЛИ `custom: «SP повний» (auto/offensive/defensive заряд — щосекунди / за атаку / за отриманий удар)` → ТО навичка доступна: ручна — `input(skill)`, автоматична — сама; `set_state(op, skill, duration)`.
- КОЛИ `input(skill)` спеціаліста-штовхача → ТО `custom: «effect shift: штовхнути/тягнути ворога з силою vs Weight»`; ЯКЩО `enter(enemy, hole)` → `disappear_a`.
- КОЛИ `enter(enemy, protection_objective)` → ТО `lives(-1)` (бос −2…), `disappear_a`.
- КОЛИ `counter(lp, ==, 0)` → ТО `lose`.
- КОЛИ `all_gone(enemy)` і хвилі скінчились → ТО `win`; рейтинг: 3★ без втрати LP, 2★ — з втратою, 4★ — Challenge Mode.
- Перемога: знищити/пропустити всіх ворогів, не втративши всі LP · Поразка: LP = 0 · Рахунок: зірки етапу.

## Керування і ввід
- Тач/миша: перетягнути портрет з панелі розгортання на клітину (легальні підсвічені) → свайпом обрати напрямок (4 сторони) — форма дальності повертається; відпустити поза індикатором — скасувати.
- Тап по оператору — коло навички (активувати), кнопка відступу, показ дальності; час сповільнюється до ½.
- Кнопки: пауза, 1×/2×, вихід; під час паузи можна розгортати (тактична пауза).
- Auto Deploy: записане ручне проходження на 3★ відтворюється автоматично.

## Вікна, меню, HUD
- `main-menu` (головний термінал) → кампанія, події, база, найм, загін, магазин, Integrated Strategies.
- `level-select` (етапи розділу, зірки) → `+window:loadout-select` (вибір загону з 12 операторів + підтримка друга) → `game-screen`.
- `game-screen`: поле, `+ui:dp-counter`, `lives` (LP), лічильник ворогів «знищено/всього», ліміт юнітів, `+ui:deploy-bar` (портрети з ціною DP; червоний таймер — redeploy, напівпрозорий — бракує DP), `+ui:skill-charge-ring` (SP), `+ui:range-circle` (сітка дальності), `+ui:enemy-route-preview` (пунктир маршруту), кнопки паузи/швидкості.
- `end-screen` — рейтинг зірками, нагороди; повтор/далі.
- `+window:squad-window` — загони й прокачка (рівні, Elite-підвищення, навички, модулі); `+window:base-window` — база (RIIC): кімнати-виробництва з призначеними операторами.
- `shop-window`, найм (gacha) з банерами, `codex-window` (архів ворогів/операторів), `achievements-window`.
- Переходи: main-menu → level-select → loadout → game-screen → end-screen → level-select.

## Фічі поза полем
- `levels-sequential` + `level-unlock` (розділи кампанії), `stars-rating` (2★/3★/4★), `mode-practice` (Practice Plan — безкоштовна спроба).
- `+feature:auto-deploy` — повтор записаної послідовності дій (той самий детермінований етап).
- `+feature:stamina` — Sanity: вхід в етап коштує ресурс, що відновлюється в часі.
- `+feature:gacha` — найм операторів за валюту; рідкість 1–6★.
- Режими: Integrated Strategies (роглайк: мапа, реліквії-колекційні, загін з нуля — `+run-relics`), Contingency Contract (ручні модифікатори складності), Reclamation Algorithm (виживання з будівництвом), Stationary Security Service (декбілдинг), кооп Icebreaker Games.
- `meta-progression`: рівні операторів, Elite, Potential (знижує ціну DP), Trust; база-інкремент.
- `cloud-save` (акаунт), щоденні нагороди.

## Варіації й родичі
- Родичі: Kingdom Rush (бараки блокують ворогів), Plants vs. Zombies (юніти-вежі з ціною і кулдауном), Defense Grid; спадкоємці — Girls' Frontline 2 (?), Arknights: Endfield (інший жанр).
- **Осі варіацій**: вежа — статична / оператор з HP, що може померти · блок — немає / N ворогів за вагою · клітина — будь-яка / типізована (ближні vs дальні) · ресурс — за вбивства / що тече в часі · дальність — коло / форма, повернута за напрямком.
- Модифікатори етапу (Contingency Contract) як окремий шар правил над тим самим етапом.

## Цікавинки для курсу
- Блокування: оператор тримає до N ворогів, великі займають 2–4 «місця», неблоковані проходять — 🥈 (ресурс на клітині + розподіл черги ворогів).
- Форма дальності (шаблон клітин), повернута за напрямком розгортання — 🥉 (поворот матриці-шаблону навколо клітини).
- Типізовані клітини (низька/висока) як обмеження розстановки — 🌱, але одразу дає «гру в розстановку».
- Економіка DP: тече 1/с, відступ повертає половину, повторне розгортання ×1.5/×2, кулдаун — 📎 за кожне правило, разом 🥉.
- Штовхання ворога в яму з силою проти ваги — 🥉.
- Auto Deploy — запис і відтворення дій на детермінованому рівні — 🥈 (`replay` як механіка, а не відео).
- Навички з SP трьох типів заряду (час / атаки / отримані удари) — 🥉.

## Мапа на каталог
- Є: `enemy-waves` + `spawn-schedule` + `spawn-points` · `enemy-reached-base` ↔ Protection Objective і LP · `round-currency` ↔ DP · `hp-damage` (оператори теж гинуть) · `melee-vs-ranged` ↔ класи й клітини · `projectile-shot` · `blast-wave` ↔ AoE-маги · `temporary-modes` ↔ навички, сповільнення · `speed-per-type` · `impassable-cells` · `floor-types` ↔ руни, лава, вода, лід · `teleport-one-way` ↔ тунелі · `game-pause` · `drag-drop-piece` ↔ розгортання · `legal-move-highlight` ↔ підсвітка легальних клітин · `telegraphed-intents` ↔ маршрут ворога пунктиром · `level-select` + `level-unlock` · `replay` ↔ Auto Deploy · `save-progress` · `dungeon-generation` ↔ мапа IS · `shop-between-levels` ↔ магазин IS.
- **Нема** → пропозиції карток:
  - `+tower-placement`, `+tower-range` — див. fieldrunners; `+placement-cooldown`, `+loadout-select` — див. plants-vs-zombies (redeploy, загін 12); `+run-relics` — див. isle-of-arrows.
  - `+tile-class-placement` «Клітини за класом юніта» · entities/legality · 🌱 · слот {classes: low|high}.
  - `+block-count` «Блокування N ворогів» · entities/combat · 🥈 · слоти {block, enemy_size}.
  - `+facing-range` «Дальність-шаблон за напрямком» · entities/combat · 🥉 · слот {pattern}.
  - `+cost-escalation` «Ціна росте з повторами» · game-logic/economy · 🌱 · слот {steps: [1, 1.5, 2]}.
  - `+retreat-refund` «Відступ із частковим поверненням» · game-logic/economy · 🌱 (≈ `shop-buyback` на полі).
  - `+unit-limit` «Ліміт юнітів на полі» · game-logic/economy · 🌱.
  - `+skill-charge` «Навичка з зарядом» · entities/state · 🥉 · слот {charge: time|attack|hit}.
  - `+shift-push-pull` «Штовхнути/потягнути з силою проти ваги» · entities/combat · 🥉.
  - `+auto-deploy` «Автоповтор записаних дій» · interface/results · 🥈.

## Пропозиції до словників
- `+trigger:blocked_by` — ворог зупинений блокувальником; `+trigger:sp_full` — навичка заряджена.
- `+cond:cell` ⏳ — підтвердження (тип клітини для розгортання); `+cond:block_free` — у блокувальника є вільні «місця» ≥ розміру ворога.
- `+effect:sell` — тут «відступ із поверненням»; `+effect:retreat` — прибрати юніт із кулдауном повернення; `+effect:shift` — примусово зсунути сутність з силою (vs вага).
- `+role:tower` — підтвердження (але з HP і смертю); `+role:unit` — з TFT.
- `+ui:deploy-bar` — панель портретів з ціною й таймером кулдауну; `+ui:skill-charge-ring`; `+ui:range-circle` (тут сітка клітин); `+ui:enemy-route-preview` (≈ ⏳ `path-preview` для ворога); `+ui:dp-counter`.
- `+window:loadout-select` — підтвердження (загін); `+window:squad-window` — прокачка юнітів; `+window:base-window` — база-інкремент.
- `+feature:auto-deploy`, `+feature:gacha`, `+feature:stamina`.
- `+axis:control` — `indirect`: гравець лише ставить і активує, юніти діють самі.

## Джерела
- ⭐ [Arknights Terra Wiki: Operation](https://arknights.wiki.gg/wiki/Operation) — увесь HUD етапу: LP, DP, ліміт юнітів, розгортання з напрямком, redeploy-таймер, SP, 1×/2×, сповільнення при виборі, рейтинги.
- [Terra Wiki: Block](https://arknights.wiki.gg/wiki/Block) — правило блоку, вороги на 2/3/4 Block, неблоковані, «блокований = в радіусі».
- [Terra Wiki: Cost](https://arknights.wiki.gg/wiki/Cost) — відступ = ⌊cost/2⌋, повторне розгортання ×1.5 → ×2, ≤ 99.
- [Terra Wiki: Deployment Point](https://arknights.wiki.gg/wiki/Deployment_Point) — 1 DP/с, межа 99, від’ємні DP.
- [Terra Wiki: Terrain](https://arknights.wiki.gg/wiki/Terrain) — каталог спецклітин.
- [Wikipedia: Arknights](https://en.wikipedia.org/wiki/Arknights) — 8 класів, ближні на землі / дальні на висоті, режими, дати.
- [Офіційний сайт](https://www.arknights.global/) · YouTube: пошук «arknights gameplay stage clear».

## Непевне
- (?) Типові Block по класах (Defender 3, Vanguard/Guard 1–2) і тривалість redeploy (~70 с, спеціалісти швидкого redeploy ~18 с) — з памʼяті.
- (?) Формули шкоди (мінімум 5 % ATK для фізичної; RES у % для Arts).
- (?) Типовий розмір поля і стартові LP (зазвичай 3? на Challenge — 1).
- (?) Ліміт загону (12 + підтримка) і типовий Unit Limit (8?) — з памʼяті.
- (?) Як саме повітряні вороги прокладають маршрут (вікі лише каже про Aerial Incursion Points).
