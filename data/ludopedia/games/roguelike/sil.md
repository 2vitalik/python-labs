---
title: Sil
slug: sil
aka: [Sil-Q]
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2012
platforms: [Windows, macOS, source, Android]
links:
  - {kind: other, url: "https://www.roguebasin.com/index.php/Sil", best: true, note: "RogueBasin: суть, релізи 1.0–1.3, форк Sil-Q, лінки на все"}
  - {kind: official, url: "http://www.amirrorclear.net/flowers/game/sil/", note: "сайт автора: завантаження, мануал, форум"}
  - {kind: other, url: "http://www.amirrorclear.net/flowers/game/sil/Sil-130-Manual.pdf", note: "мануал 1.3: кидки, бій, мораль, стелс, досвід, здібності, пісні"}
  - {kind: other, url: "https://github.com/sil-quirk/sil-q", note: "Sil-Q — живий форк (1.5.0): ребаланс, тайли"}
  - {kind: other, url: "http://angband.oook.cz/ladder-browse.php?v=Sil&s=1", note: "ладдер: дампи персонажів гравців"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Sil+roguelike+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-8dir, keyboard-controls, console-render, dungeon-generation, stairs-levels, fog-of-war, hp-damage, melee-vs-ranged, projectile-shot, status-effects, item-identification, hunger-clock, permadeath, inventory, inventory-items, inventory-limit, destructible-blocks, unit-xp-skills, message-log, tutorial-window, help-window, +xp-for-discovery, +stealth-alertness, +light-level, +opposed-skill-roll, +dice-protection, +surround-penalty, +morale-flee, +forced-descent, +reaction-attacks, +forge-crafting, +song-upkeep]
proposes: ["+trigger:noticed(monster, player)", "+cond:skill_check(skill, difficulty)", "+cond:lit(cell, op, n)", "+effect:free_attack(a, b)", "+effect:identify", "+role:stairs", "+window:character-sheet", "+window:smithing-window", "+ui:alertness-marker", "+feature:permadeath", "+card:forced-descent", "+card:xp-for-discovery"]
author: opus
date: 2026-11-09
---

# Sil — Angband за Толкіном: досвід за побачене, а не за вбите; стелс і світло важать як меч

## Суть
Ельф, гном чи людина пробирається в Ангбанд, спускається на 1000 футів до тронної зали Морґота, виколупує Сильмарил з його корони і тікає на поверхню. Від Angband лишився вигляд і інтерфейс, але майже вся механіка нова: нема класів і рівнів, досвід витрачають на 8 навичок і дерево здібностей. Головне: **досвід дають зустрічі, спуск і ідентифікація** не менше, ніж убивства, тож гру можна пройти, не вдаривши жодного разу. Бій прозорий (кидки d20/d10 проти навички суперника), магії майже нема — лише пісні.

## Поле і час
- Квадратна сітка, ASCII-символи (у Sil-Q — і тайли); 8 напрямків руху. Рівень — згенероване підземелля з кімнатами, коридорами, дверима, завалами.
- Глибина у футах: сходи ведуть на 50 ft нижче/вище, шахти — на 100 ft нижче; Морґот — на 1000 ft. Повернутись у покинуту зону не можна: кожні сходи — новий рівень.
- **Годинник спуску**: з часом росте «min depth» — мінімальна глибина, вище якої вже не піднятися (видно на листі персонажа). Лише із Сильмарилом можна йти вгору без обмеження.
- Хід = дія гравця; швидкість дискретна 1–4 (норма 2, +1 — на 50 % швидше).
- Видимість: туман, джерело світла з радіусом; рівень освітлення клітини впливає на бій (опір темряві, мораль світлобоязких). Ворога за межею освітленого не видно (здібність Keen Senses — видно трохи далі).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | раса/дім; Str, Dex, Con, Gra; 8 навичок; health (від Con), voice (від Gra); XP; їжа; вага ноші | хід/атака у 8 напрямках, стрільба, кидання, пісня, кування |
| Монстр | enemy | melee, evasion, perception, will, захист; **alertness** (сон / unwary / alert); **morale** | прокидається від шуму; за мораллю — нападає, хитрує або тікає |
| Безмозкий монстр | enemy | — | завжди Aggressive, не тікає |
| Територіальний (дракон) | enemy | лігво | повернувшись у лігво й не бачачи гравця — стає unwary або засинає |
| Невидимий монстр | enemy | — | видно лише за перевіркою Perception проти Will монстра |
| Морґот | boss | корона з трьома Сильмарилами | на 1000 ft у тронній залі |
| Сильмарил | pickup | — | ціль; виколупується з корони перевіркою Melee з великою шкодою |
| Сходи вниз / вгору | static | ±50 ft | новий рівень; вгору лише до min depth |
| Шахта | static | +100 ft | швидкий спуск |
| Двері | gate | зачинені / замкнені / таємні | зачинені глушать звук (−5 perception монстрам); замок — відмикати (Perception) або вибити (Str) |
| Завал (rubble) | static | — | не пропускає звук; прокопати лише лопатою/кайлом |
| Яма / шипована яма | hazard | складність 15 / 20 | падіння; вибратися — Evasion; у ямі melee і evasion ×½ |
| Павутина | hazard | — | тримає; вирватися — Str; у павутині melee і evasion ×½ |
| Пастки (дротики, уламки, кальтропи) | hazard | складність 10–20 | ухилитися — Evasion або Perception; знешкодити — Perception |
| Кузня | static | ресурс використань; зачарована — бонус до Smithing | кування зброї, броні, прикрас, артефактів |
| Зброя | pickup | (точність, NdM), вага | важча — більше кісток і стелі для Str; легша — більше критів |
| Броня | pickup | [evasion, NdM захисту], вага | кожні 10 lb — −1 до Stealth |
| Лук і стріли | pickup | дальність = 1.5 × сторін шкоди | постріл; поруч вороги — вільний удар по тобі |
| Метальна зброя | pickup | дальність від ваги й вантажопідйомності | кидок; не метальна — −5 до влучання, шкода ×½ сторін |
| Зілля, трави, кільця, амулети, роги, жезли | pickup | невідомі до ідентифікації | ефект при вжитку; роги й жезли — перевірка Will |
| Артефакт | pickup | {special} до ідентифікації | +200 XP за ідентифікацію |
| Мітрил | resource | — | для кування окремих речей |
| Їжа | pickup | — | поповнює лічильник їжі |
| Джерело світла | pickup | радіус | світло навколо гравця |

## Правила (КОЛИ → ЯКЩО → ТО)
Рух і бій:
- КОЛИ `input(dir)` → ЯКЩО `free(cell)` → ТО `move(player, dir)`; ЯКЩО `occupied(cell, enemy)` → ТО `custom: «атака: melee+1d20 проти evasion+1d20; більше — влучив»`.
- КОЛИ `after(attack hit)` → ТО `damage(n)`, де n = `custom: «кістки зброї (+1 сторона за пункт Str, не більше ваги зброї в lb) − кидок захисту броні»`; n ≤ 0 → шкоди нема.
- КОЛИ `after(attack hit)` → ЯКЩО `custom: «перевищив evasion на 7 + вага зброї»` → ТО `custom: «+1 кістка шкоди за кожне кратне перевищення (крит)»`.
- КОЛИ `adjacent(enemy, player)` → ЯКЩО `adjacent_count(player, enemy, >, 1)` → ТО `custom: «−1 до evasion за кожного сусіда, −2 — за тих, хто з протилежного боку від атакувальника»` (оточення).
- КОЛИ `input(attack)` → ЯКЩО `not line_of_sight(attacker, defender)` або `state(defender, unwary)` → ТО `custom: «melee атакувальника / evasion захисника ×½»`.
- КОЛИ `input(attack)` → ЯКЩО `state(target, asleep)` → ТО `custom: «evasion цілі = −5»`.
- КОЛИ `input(fire, target)` → ЯКЩО `line_of_sight(player, target)` і `in_range(player, target, 1.5×sides)` → ТО `custom: «archery+1d20 проти evasion/2; −1 за кожні 5 клітин»`; ЯКЩО `adjacent_count(player, enemy, >, 0)` → ТО `custom: «кожен сусідній ворог бʼє безкоштовно»`.
- КОЛИ `after(attack hit)` з вогнем/холодом/отрутою → ЯКЩО `not has(target, resistance)` → ТО `custom: «+1 кістка шкоди (уразливість — +2)»`.
- КОЛИ `hp_zero(player)` → ТО `lose` (одне життя).

Стелс і мораль:
- КОЛИ `tick` → ЯКЩО `custom: «perception монстра+1d10 − відстань звуку − 5 за кожні зачинені двері > stealth гравця+1d10»` → ТО `counter(alertness, +різниця)`.
- КОЛИ `counter(alertness, >=, 0)` → ТО `set_state(monster, alert)`; від −1 до −10 — `set_state(monster, unwary)`; ≤ −11 — сплячий.
- КОЛИ `input(attack)` або `contact(monster, player)` → ЯКЩО `state(monster, unwary)` → ТО `set_state(monster, alert)`.
- КОЛИ `input(stealth_mode)` → ТО `set_state(player, stealth)`, `speed(player, −1)`, `custom: «+5 до Stealth»`.
- КОЛИ `input(pass)` → ТО `custom: «+7 до Stealth наступного ходу»`.
- КОЛИ `tick` → ЯКЩО `not line_of_sight(monster, player)` і `custom: «монстр провалив perception на 25+»` → ТО `counter(alertness, −надлишок)` (з Vanish — поріг 15).
- КОЛИ `counter(morale, <=, 0)` → ТО `set_state(monster, fleeing)`; `counter(morale, >, 20)` → `set_state(monster, aggressive)`; між — confident (засідки, тактика).
- КОЛИ `died(monster)` → ЯКЩО `line_of_sight(similar_monster, monster)` → ТО `custom: «мораль подібних −4 (лідер −16)»`.
- КОЛИ `tick` → ЯКЩО `custom: «здоровʼя гравця ≤ 75 / 50 / 25 %»` → ТО `custom: «мораль монстрів +2 / +4 / +8»`.

Досвід (без рівнів):
- КОЛИ `line_of_sight(player, monster)` → ЯКЩО `first_time` → ТО `counter(xp, +depth/5)`; наступні того ж виду — спадна частка.
- КОЛИ `died(monster)` → ЯКЩО `first_time` (вид) → ТО `counter(xp, +depth/5)`; далі — так само спадає.
- КОЛИ `reach(player, depth d)` → ЯКЩО `first_time` → ТО `counter(xp, +d)`.
- КОЛИ `input(use item)` → ЯКЩО `first_time` (тип) → ТО `custom: «ідентифікувати тип»`, `counter(xp, +100)`; артефакт — +200.
- КОЛИ `input(buy skill)` → ЯКЩО `has(player, xp ≥ 100×n)` (n-й пункт) → ТО `custom: «навичка +1»`; здібність навички — 500, 1000, 1500… XP.

Глибина й час:
- КОЛИ `input(stairs_down)` → ЯКЩО `cell(under, stairs_down)` → ТО `next_level` (+50 ft); шахта — +100 ft.
- КОЛИ `input(stairs_up)` → ЯКЩО `custom: «глибина − 50 ≥ min depth»` або `has(player, silmaril)` → ТО `custom: «новий рівень на 50 ft вище»`; інакше `block`.
- КОЛИ `timer(…)` → ТО `custom: «min depth зростає»` (темп не перевірено).
- КОЛИ `input(stairs)` → ЯКЩО `custom: «багато сходів за короткий час»` → ТО `custom: «заблукав: може вивести не туди або в пастку»`.
- КОЛИ `reach(player, surface)` → ЯКЩО `has(player, silmaril)` → ТО `win`.

Тіло і середовище:
- КОЛИ `tick` → ТО `counter(food, −1)`; ЯКЩО `counter(food, <, 1000)` → ТО `custom: «Weak: Str −1»`; КОЛИ `counter(food, ==, 0)` → ТО `damage(1)` щоходу, регенерації нема.
- КОЛИ `tick` → ЯКЩО `state(player, poisoned X)` → ТО `damage(⌈0.2·X⌉)` і X зменшується; кровотеча — так само.
- КОЛИ `tick` → ЯКЩО `custom: «світло на клітині гравця > 2»` → ТО `custom: «+1 рівень опору темряві за кожен рівень надлишку»`; ЯКЩО > 3 → `custom: «мораль світлобоязких −1 за рівень»`.
- КОЛИ `enter(player, pit)` → ТО `set_state(player, in_pit)`; вибратися — `custom: «Evasion проти 15 / 20»`.
- КОЛИ `input(disarm)` → ЯКЩО `custom: «Perception проти складності пастки»` → ТО `disappear_b`; провал на 3+ → пастка спрацьовує.
- КОЛИ `input(smith item)` → ЯКЩО `has(player, ability)` і `has(player, mithril)` (якщо треба) і `custom: «Smithing ≥ складність»` → ТО `give(player, item)`; `custom: «10 ходів на пункт складності, шум 10; ціна — XP або злитий стат»`.
- КОЛИ `tick` → ЯКЩО `state(player, singing)` → ТО `counter(voice, −n)`, `custom: «шум = рівень пісні»`; Пісня Елберет — `custom: «Song проти Will: страх»`, Пісня Лорієн — `counter(alertness, −n)` до сну.

Реакції-здібності (вільний удар):
- КОЛИ `input(dir)` → ЯКЩО `has(player, Flanking)` і `custom: «стара і нова клітини обидві сусідні з ворогом»` → ТО `custom: «вільний удар»`.
- КОЛИ `input(dir)` → ЯКЩО `has(player, Controlled Retreat)` і `custom: «відійшов з сусідньої клітини, минулий хід стояв»` → ТО `custom: «вільний удар»`.
- КОЛИ `died(enemy)` → ЯКЩО `has(player, Follow-Through)` і `adjacent_count(player, enemy, >, 0)` → ТО `custom: «вільний удар по іншому сусіду (ланцюжиться)»`.
- КОЛИ `adjacent(enemy, player)` → ЯКЩО `has(player, Polearm Mastery)` і `custom: «гравець чекав минулий хід»` → ТО `custom: «вільний удар по тому, хто підійшов»`.
- КОЛИ `after(attack hit)` → ЯКЩО `has(player, Knock Back)` і `custom: «2×Str проти 2×Con»` → ТО `push(enemy)`.

## Керування і ввід
- Клавіатура (roguelike-розкладка в стилі Angband): цифри/стрілки — рух і атака; `5`/`z` — пропустити хід; `S` — стелс-режим; `@` — лист персонажа (витрата досвіду); `0` — планування кування; `x` — оглянути; `X` — помінятися місцем із ворогом (Exchange Places); `?` — довідка.
- Атака — рух у клітину ворога; постріл/кидок — вибір цілі.
- Undo нема; кожен хід — ризик.

## Вікна, меню, HUD
- `main-menu` / створення персонажа: раса → дім → 13 очок на стати (ціна 1, 3, 6, 10) → 5000 XP на навички й здібності.
- `game-screen`: ASCII-мапа, бокова панель статів і навичок, `hp-bar` (health), voice, світло; статуси кольоровим текстом під мапою; `message-log` вгорі.
- `character-sheet` (`@`): стати, 8 навичок з ціною наступного пункту, дерево здібностей на навичку, min depth.
- `smithing-window`: вибір бази, зачарувань, ціни (XP / стат / мітрил), складності.
- `inventory-window` і екіпірування; огляд предмета/монстра (monster recall).
- `help-window` (`?`): команди; `tutorial-window` — навчальний рівень.
- `end-screen`: смерть або перемога; дамп персонажа.

## Фічі поза полем
- `permadeath`: одне життя.
- `tutorial`; мануал PDF у комплекті.
- Раси як рівні складності: Noldor найлегші, Edain — «режим виклику»; доми в межах раси рівні.
- Дамп персонажа на ладдер (angband.oook.cz) — `leaderboard-online` поза грою.
- Відкритий код (C); форк Sil-Q (тайли, нові предмети, ребаланс навичок).

## Варіації й родичі
- Rogue → Moria → Angband → NPPAngband → Sil; порівняй з `rogue`, `nethack`, `dungeon-crawl-stone-soup` (DCSS теж стелс і світло), `brogue` (світло і стелс-радіус).
- Sil-Q — продовження спільноти.
- **Осі варіацій**: звідки досвід (вбивства / зустрічі й спуск / ідентифікація / нема досвіду — Cave Noire); що тисне час (голод / годинник min depth / таймер рівня); бій (детермінований — Desktop Dungeons / прозорі кістки — Sil / прихований шанс — NetHack); стелс (радіус шуму — Brogue / протиставлені кидки щохід — Sil).

## Цікавинки для курсу
- Протиставлені кидки «навичка+1d20 проти навички+1d20» + кістки шкоди мінус кістки захисту — 📎 (дві формули, але дуже прозора модель бою).
- Alertness як лічильник: щохід perception проти stealth з відстанню звуку й дверима — 🥉 (BFS звуку по мапі + стани сну/unwary/alert).
- Мораль монстрів з десятком модифікаторів і трьома стійками — 🥈 (таблиця + поведінка втечі «якнайдалі від гравця»).
- Досвід за перше побачене з затуханням для однотипних — 🌱.
- Годинник min depth: «назад не можна, з часом — і на рівень вище» — 📎.
- Реакції Flanking / Controlled Retreat / Zone of Control — 🥉 (перевірка геометрії «до і після ходу»).
- Штраф за оточення з різною вагою для протилежних боків — 📎.

## Мапа на каталог
- Є: `move-8dir` · `keyboard-controls` · `console-render` · `dungeon-generation` · `stairs-levels` (сходи/шахти) · `fog-of-war` · `hp-damage` · `melee-vs-ranged` · `projectile-shot` (стріли, кидки) · `status-effects` (отрута, кровотеча, оглушення 3 ступенів) · `item-identification` · `hunger-clock` · `permadeath` · `inventory`, `inventory-items`, `inventory-limit` (вага → повільність) · `destructible-blocks` (прокопати завал) · `unit-xp-skills` (XP → навички, без рівнів) · `message-log` · `tutorial-window` · `help-window`.
- **Нема** → пропозиції карток:
  - `+xp-for-discovery` «Досвід за перше побачене / глибину / ідентифікацію, а не лише вбивства» · game-logic/progression · 🌱 · слоти {sources, decay}.
  - `+stealth-alertness` «Лічильник пильності монстра: perception проти stealth щохід» · entities/ai · 🥉 · слоти {noise, distance, doors}.
  - `+light-level` «Рівень освітлення клітини як модифікатор правил» · entities/state · 📎.
  - `+opposed-skill-roll` «Протиставлений кидок навичка+кістка проти навичка+кістка» · game-logic/combat · 🌱.
  - `+dice-protection` «Броня кидає кістки захисту, віднімає від шкоди» · game-logic/combat · 🌱.
  - `+surround-penalty` «Штраф захисту за кількість сусідніх ворогів» · entities/combat · 📎.
  - `+morale-flee` «Мораль ворога: нападає / хитрує / тікає» · entities/ai · 🥈.
  - `+forced-descent` «Мінімальна глибина росте з часом» · levels · 📎.
  - `+reaction-attacks` «Вільний удар за геометрію руху (фланг, відступ, зона контролю)» · entities/combat · 🥉.
  - `+forge-crafting` «Кування з ціною в досвіді/статах на станції» · entities/items · 🥈.
  - `+song-upkeep` «Пісня-аура: щохід ціна в voice і шум» · entities/state · 📎.

## Пропозиції до словників
- `+trigger:noticed(monster, player)` — монстр перейшов у alert (зручніше за `counter(alertness, >=, 0)`).
- `+cond:skill_check(skill, difficulty)` — протиставлений кидок навички (Sil, Cave Noire-подібні RPG-перевірки).
- `+cond:lit(cell, op, n)` — рівень освітлення клітини.
- `+effect:free_attack(a, b)` — позачерговий удар-реакція.
- `+effect:identify` — розкрити тип предмета.
- `+role:stairs` — перехід між рівнями (зараз `static`).
- `+window:character-sheet` — витрата досвіду на навички/здібності.
- `+window:smithing-window` — конструктор предмета з ціною.
- `+ui:alertness-marker` — позначка сну/unwary/alert біля монстра (?).
- `+feature:permadeath`.
- `+card:forced-descent` · `+card:xp-for-discovery`.

## Джерела
- ⭐ [RogueBasin: Sil](https://www.roguebasin.com/index.php/Sil) — що це, релізи (1.0 — 3.01.2012, 1.3 — 2016), Sil-Q, лінки.
- [Сайт автора](http://www.amirrorclear.net/flowers/game/sil/) — завантаження, відгуки, лінки на мануал і форум.
- [Мануал Sil 1.3 (PDF)](http://www.amirrorclear.net/flowers/game/sil/Sil-130-Manual.pdf) — усі формули: навички, бій, крити, стихії, мораль, стелс, голод, статуси, досвід, здібності, пісні.
- [Sil-Q на GitHub](https://github.com/sil-quirk/sil-q) — форк, «dungeon heist».
- [Ладдер Sil](http://angband.oook.cz/ladder-browse.php?v=Sil&s=1) — дампи персонажів.
- YouTube: [пошук «Sil roguelike gameplay»](https://www.youtube.com/results?search_query=Sil+roguelike+gameplay).

## Непевне
- (?) Як саме дістати Сильмарил (чи треба приспати/обійти Морґота) — мануал каже лише «Melee, складність 0, але потрібна велика шкода».
- (?) Темп зростання min depth (у ходах) — у мануалі не знайшов.
- (?) Чи світло на клітині гравця збільшує шанс бути поміченим — мануал прямо цього не каже; опис RogueBasin «відступати в тіньові коридори» — радше про бій по одному.
- (?) Точна кількість рівнів: 1000 ft / 50 ft = 20 глибин — лише арифметика, рівні генеруються наново.
- (?) `alertness-marker` — чи показує гра стан монстра на мапі, не перевірено.
- (?) Розкладка клавіш, окрім названих у мануалі (`S`, `5`/`z`, `@`, `0`, `x`, `X`, `?`), — з памʼяті про Angband.
