---
title: "La Pucelle: Tactics"
slug: la-pucelle-tactics
aka: [La Pucelle, "La Pucelle: Ragnarok", ラ・ピュセル 光の聖女伝説]
family: tactics
also: [connect-rotate]
klass: figure
axes:
  field: iso
  time: turn
  opponent: ai
  info: full
  random: both
  goal: state
year: 2002
platforms: [PS2, PSP, PC, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/La_Pucelle:_Tactics", best: true, note: "Dark Portals, потік до перешкоди, поворот фасингом, очищення, Miracle при самоперетині >15 панелей, індекс темряви"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ラ・ピュセル_光の聖女伝説", note: "JA: петля від 15 клітин, ланцюг Miracle, атаки підтримки зліва/справа/ззаду, рівні предметів до 99, Dark World 10 поверхів"}
  - {kind: other, url: "https://www.supercheats.com/playstation2/walkthroughs/lapucelletactics-walkthrough01.txt", note: "FAQ: 7 кольорів потоків, правила фасингу, Change Up, потоки рівня 2, бонус і множник петель"}
  - {kind: other, url: "https://www.rpgfan.com/review/la-pucelle-tactics/", note: "огляд PS2: стихія потоку, Miracle навколо ворогів, вербування монстрів, Dark World"}
  - {kind: steam, url: "https://store.steampowered.com/app/1866420/La_Pucelle_Ragnarok/", note: "PC-версія Ragnarok: поворот камери, сценарій Overlord Prier"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=La+Pucelle+Tactics+purification", note: "пошук; очищення порталів і Miracle"}
stage: v1
coverage: 65
mechanics: [beam-tracing, mirror-reflect, chain-reaction, combo-multiplier, event-points, spawner-entity, spawn-random-cell, hp-damage, ai-opponent, status-effects, shop-between-levels, shop-window, dungeon-generation, sequential-levels, game-screen, +beam-color-mix, +crossing-detection, +facing-redirect, +loop-area-attack, +beam-merge-level, +purify-portal, +recruit-ally, +corruption-index, +support-adjacent, +item-leveling, +item-synthesis, +shop-survey, +monster-training, +multiple-endings]
proposes: ["+effect:emit_beam", "+trigger:beam_hit", "+effect:hit_enclosed", "+cond:loop_length", "+ui:dark-index", "+ui:stream-overlay", "+window:shop-survey", "+window:training"]
author: opus
date: 2026-11-09
---

# La Pucelle: Tactics — портали пускають кольорові потоки темряви, юніти повертають їх своїм фасингом, а самоперетин петлі від 15 панелей — «Miracle»

## Суть
Ізометрична тактика Nippon Ichi (до Disgaea): загін Прієр бʼється з монстрами, але головна гра — **Dark Portals**, що випускають потік темної енергії прямо до першої перешкоди. Юніт у потоці **повертає його фасингом** (вліво/вправо — поворот на 90°, проти — зупинка), як рухоме дзеркало. Очищення порталу силою більшою за його HP пускає атаку вздовж усього потоку; якщо потік довжиною від 15 панелей **перетинає сам себе**, спрацьовує **Miracle** — удар по всіх ворогах усередині петлі, що очищає портали в ній і запускає ланцюг. Монстрів очищують і вербують, а неочищена темрява піднімає індекс, що відкриває Dark World.

## Поле і час
- Ізометрична мапа різної форми й розміру з базовою панеллю; портали розкидані випадково на старті.
- Хід — фаза гравця (юніти в будь-якому порядку) → фаза ворога. Потоки — шар поверх клітин: їхній шлях перераховується, коли юніт чи Change Up стає в потік або повертається.
- Бій — окремий екран: атакувальник, ціль і сусідні союзники; кожен бʼє один раз.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Прієр і люди загону | piece | HP, стати, сила очищення, фасинг | ходять, бʼють, очищають; фасингом повертають потік |
| Монстр-союзник | piece | рівень, щастя | завербований; від щастя 10 теж очищає |
| Ворог-людина | enemy | — | ШІ |
| Ворог-монстр | enemy | HP, рівень очищення | очищений і переможений — може приєднатися |
| Dark Portal | spawner | HP, колір, напрям | випускає потік; неочищений кілька раундів → новий ворог |
| Панель потоку | terrain | колір, рівень 1–2 | шкодить ворогам на ній; блакитна лікує союзників |
| Перешкода | static | — | зупиняє потік |
| Change Up | object | напрям; 50 prica | повертає потік як юніт; його можна обертати |
| Базова панель | spawner | — | вихід загону на мапу |
| Подарунок | container | — | відкрити → індекс темряви ↑ |
| Брама Dark World | gate | — | відкривається при індексі ≈ 100 |

Кольори потоків: червоний (вогонь), зелений (вітер), синій (лід), жовтий (блискавка = Ч + З), блакитний (лікування = З + С), пурпуровий (допомога = Ч + С), білий (святість = Ч + З + С).

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `spawn_at(portal, random)`; `custom: «кожен портал пускає потік у свій бік»`.
- КОЛИ `custom: «потік іде клітиною»` → ЯКЩО `occupied(cell, obstacle)` → ТО `block`.
- КОЛИ `custom: «потік входить у клітину з юнітом»` → ЯКЩО `facing(unit, against_flow)` → ТО `block`; ЯКЩО `facing(unit, along_flow)` → ТО `custom: «без змін»`; ЯКЩО `facing(unit, left|right)` → ТО `rotate(flow, ±90)`.
- КОЛИ `custom: «потік входить у клітину з Change Up»` → ТО `rotate(flow, change_up_dir)`.
- КОЛИ `input(face, unit, dir)` → ТО `face(unit, dir)` — потік перераховується.
- КОЛИ `custom: «зустрілись два потоки одного кольору»` → ТО `merge(flow, flow → flow_level2)`; рівень ≤ 2; коротший потік завжди йде далі своїм напрямом.
- КОЛИ `input(purify, portal)` → ЯКЩО `custom: «сила очищення > HP порталу»` → ТО `disappear(portal)`, `custom: «атака йде вздовж усього потоку»`; інакше `damage(portal, power)`.
- КОЛИ `custom: «атака йде потоком»` → ЯКЩО `occupied(flow_panel, enemy)` → ТО `damage(enemy, n)`; блакитний потік → `heal(ally, n)`, ворогів не чіпає.
- КОЛИ `custom: «атака пройшла панель»` → ТО `counter(bonus, +1)` (рівень 2 — +2); поранений ворог і вбитий (+10, +20…) теж додають бонус.
- КОЛИ `pattern(loop_closed)` (потік перетнув сам себе) → ЯКЩО `counter(flow_len, ≥, 15)` (з порталом) і `custom: «у петлі є ворог; для блакитного — союзник»` → ТО `custom: «Miracle»`: `damage(all_enemies_inside_loop, big)`.
- Стихія Miracle = колір останньої панелі перед перетином: Armageddon (Ч), Requiem (З), Gospel (С), Testament (Ж), Ultimate Insanity (П: шкода + статуси), Evangel (Б: лікує союзників), Ragnarok (білий).
- КОЛИ `after(miracle)` → ЯКЩО `occupied(loop_inside, portal)` → ТО `disappear(portal)` незалежно від HP, `trigger(next_miracle)` — ланцюг до шести; n-та петля рахує ×n за панель.
- КОЛИ `custom: «очищення / Miracle»` → ТО `counter(item_xp, +bonus×3)`; зброя стихії Miracle — більше; рівень предмета ≤ 99.
- КОЛИ `custom: «портал неочищений кілька раундів»` → ТО `spawn(enemy)` біля порталу (?).
- КОЛИ `input(purify, monster)` → ТО `counter(monster_purity, +power)`; КОЛИ `hp_zero(monster)` → ЯКЩО `prob(p ~ purity)` → ТО `set_side(monster, player)`, одразу доступний для розгортання.
- КОЛИ `input(attack, target)` → ЯКЩО `occupied(left|right|behind_attacker, ally)` → ТО `custom: «атака підтримки»` (менша шкода, союзник ще може діяти).
- КОЛИ `custom: «портал лишився, атака по союзнику, відкрито подарунок»` → ТО `counter(dark_index, +n)`; КОЛИ `custom: «очищення мапи»` → ТО `counter(dark_index, -n)`.
- КОЛИ `counter(dark_index, ≥, 100)` → ТО `spawn(dark_world_gate)` — генеровані рівні; вищий індекс — сильніші вороги.
- КОЛИ `level_end` → ТО `currency(+n)` за розмір очищення; усі портали очищено — другий такий самий бонус; `choose(training)` з випадкового списку.
- Перемога: умова мапи (?) · Поразка: (?) · Рахунок: бонус очищення → гроші й досвід предметів; кінцівка епізоду (Special / Good / Normal / Bad).

## Керування і ввід
- Курсор по ізосітці; юніт → Move · Attack · Purify · Item · кінець ходу.
- Фасинг: курсор на юніті, утримати Square + напрям на хрестовині — повернути без руху.
- Change Up: розмістити й обертати; FAQ описує трюк — навести Change Up на портал і змінити напрям самого порталу (ймовірно, баг).
- PC/Switch (Ragnarok): поворот камери, пропуск сцен.

## Вікна, меню, HUD
- `game-screen`: ізомапа, кольорові доріжки потоків (`+ui:stream-overlay`), HP порталів, лічильник бонусу, `+ui:dark-index`.
- `custom-window` «бій»: атакувальник, ціль і союзники підтримки.
- `shop-window` Rosenqueen + `+window:shop-survey` (опитування після покупок: ранг товару, бажання «Triple Money» / «Triple Purification Experience»); `custom-window` синтезу предметів (монстр поглинається).
- `+window:training` — вибір тренування монстрів після мапи; відправка монстрів у Dark World.
- `dialogue-window` — сюжет 12 епізодів; `end-screen` — кінцівка епізоду; `save-slots` (?).

## Фічі поза полем
- `levels-sequential`: 12 епізодів, у кожного до 4 кінцівок (впливають на нагороди, фінал один).
- Dark World — `dungeon-generation`: генеровані рівні (JA: 10 поверхів), бос на дні; монстри ходять туди на «Demon Wars» і приносять предмети.
- Прокачка предметів очищенням замість Item World з Disgaea; синтез у Rosenqueen; до 4 пар взуття для руху.
- PSP/PC Ragnarok: персонажі Disgaea, перенесення загону при перепроходженні, сценарій Overlord Prier, до 149 предметів.

## Варіації й родичі
- [disgaea](disgaea.md) — наступник NIS: Geo Panels («колір клітини + символ») замість потоків; Прієр — прихований бос там.
- [knights-in-the-nightmare](knights-in-the-nightmare.md) — La Pucelle як гостьовий клас (PSP).
- У корпусі `connect-rotate`: Deflektor, Laser Tank, Khet — промінь і дзеркала; тут дзеркалами є юніти з фасингом. [hoshigami](hoshigami.md) — фасинг перенаправляє відкинутого ворога.
- **Осі варіацій**: хто повертає промінь — дзеркала / юніти фасингом / предмети · що дає петля — нічого / удар по лінії / удар по всьому всередині · змішування — нема / рівень за однаковим кольором / адитивні кольори.

## Цікавинки для курсу
- Трасування потоку від порталу до перешкоди з поворотом фасингом юнітів — 🥉 (beam tracing з рухливими дзеркалами).
- Самоперетин потоку від 15 панелей + «усе всередині петлі» — 🥈 (детекція перетину + заливка області).
- Ланцюг Miracle через портали в петлі з множником n-ї петлі — 🥈.
- Злиття однакових потоків у рівень 2 і адитивні кольори — 🥉.
- Очищення порталу: сила проти HP, інакше часткова шкода — 🌱.
- Індекс темряви від «поганих» дій → секретний генерований світ — 📎.

## Мапа на каталог
- Є: `beam-tracing` · `mirror-reflect` (юніти й Change Up) · `chain-reaction` (ланцюг Miracle) · `combo-multiplier` (n-та петля) · `event-points` (бонус) · `spawner-entity` (портал) · `spawn-random-cell` · `hp-damage` · `ai-opponent` · `status-effects` · `shop-between-levels` · `shop-window` · `dungeon-generation` · `sequential-levels` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+beam-color-mix` · `+crossing-detection` · `+recruit-ally` · `+support-adjacent` — уже в корпусі.
  - `+facing-redirect` «Фасинг юніта повертає потік» · entities/move · 🥉 — спільне з [hoshigami](hoshigami.md).
  - `+loop-area-attack` «Удар по всьому всередині петлі» · entities/combat · 🥈 · слот {min_len: 15}.
  - `+beam-merge-level` «Злиття однакових променів у рівень» · entities/interact · 📎.
  - `+purify-portal` «Закрити джерело силою проти HP» · entities/combat · 🌱.
  - `+corruption-index` «Індекс поганих дій відкриває секрет» · game-logic/score · 📎.
  - `+item-leveling` «Предмет росте від дій» · entities/state · 📎.
  - `+item-synthesis` «Синтез предметів» · game-logic/economy · 📎.
  - `+shop-survey` «Опитування магазину змінює асортимент» · game-logic/economy · 📎.
  - `+monster-training` «Тренування завербованих між мапами» · entities/state · 📎.
  - `+multiple-endings` «Кілька кінцівок епізоду» · levels/progression · 🌱.

## Пропозиції до словників
- `+effect:emit_beam` — джерело пускає промінь до перешкоди (уже пропоновано).
- `+trigger:beam_hit` — промінь дійшов до клітини/сутності (уже пропоновано); тут — до юніта з фасингом.
- `+effect:hit_enclosed` — подія по всіх сутностях усередині замкненої лінії.
- `+cond:loop_length` — довжина петлі/лінії ≥ N.
- `+ui:dark-index` — шкала прихованого лічильника «поганих» дій; `+ui:stream-overlay` — кольорові доріжки потоків на сітці.
- `+window:shop-survey` — опитування після покупки; `+window:training` — вибір тренування з випадкового списку.

## Джерела
- ⭐ [Wikipedia: La Pucelle: Tactics](https://en.wikipedia.org/wiki/La_Pucelle:_Tactics) — портали, потік, фасинг, очищення, Miracle (>15 панелей), вербування, індекс темряви, Dark World, версії.
- [Wikipedia JA](https://ja.wikipedia.org/wiki/ラ・ピュセル_光の聖女伝説) — петля від 15, ланцюг Miracle, атаки підтримки, рівні предметів, синтез, опитування, 12 епізодів × 4 кінцівки.
- [Supercheats FAQ](https://www.supercheats.com/playstation2/walkthroughs/lapucelletactics-walkthrough01.txt) — кольори, правила фасингу, Change Up, рівень 2, стихія Miracle, бонуси, ланцюг до 6.
- [RPGFan](https://www.rpgfan.com/review/la-pucelle-tactics/) — Miracle навколо ворогів, вербування, Dark World, магазин.
- [Steam: La Pucelle: Ragnarok](https://store.steampowered.com/app/1866420/La_Pucelle_Ragnarok/) — PC-доповнення.
- YouTube: пошук «La Pucelle Tactics purification».

## Непевне
- (?) Мінімум петлі: EN — «більше 15 панелей», JA — «15 і більше», FAQ — «щонайменше 15 з порталом», і згадує 14 (перетин рахується двічі).
- (?) Поріг Dark World: EN — 100, JA — понад 101.
- (?) Скільки раундів неочищений портал чекає до появи ворога; де саме зʼявляється ворог.
- (?) Змішування різних кольорів при зустрічі потоків — FAQ лише називає кольори-суміші, механізм не описано.
- (?) Умови перемоги й поразки мап — джерела не описують; FAQ дає бонус за ворога то 5, то 10.
- (?) Чи Change Up — предмет, що кладеться на поле, чи вміння — з FAQ неясно.
