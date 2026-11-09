---
title: Beneath Apple Manor
slug: beneath-apple-manor
aka: [BAM, "Beneath Apple Manor: The Special Edition"]
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
year: 1978
platforms: [Apple II, Atari 8-bit, IBM PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Beneath_Apple_Manor", best: true, note: "контекст: прото-роглайк 1978 (Don Worth), Golden Apple, 10/5 кімнат на поверх, процедурна генерація, Special Edition"}
  - {kind: other, url: "https://crpgadventures.blogspot.com/2015/11/beneath-apple-manor-1978-victory.html", note: "CRPG Adventures: 4 стати-пули, відпочинок, вартість досвіду 10:1, команди, монстри, смерть і brain scan, фальшиві яблука"}
  - {kind: other, url: "https://crpgaddict.blogspot.com/2012/12/game-79-beneath-apple-manor-1978.html", note: "CRPG Addict: налаштування rooms/difficulty, двері, заклинання, магазин, предмети; коментарі Don Worth"}
  - {kind: other, url: "https://www.roguebasin.com/index.php/Beneath_Apple_Manor", note: "RogueBasin: стати S/I/D/B як пули по 20, версії"}
  - {kind: other, url: "https://www.mobygames.com/game/8610", note: "MobyGames (403 для WebFetch; посилання з Wikipedia)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=beneath+apple+manor+apple+ii+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-4dir, dungeon-generation, stairs-levels, fog-of-war, hp-damage, key-and-door, one-way-cell, inventory-items, item-pickup, round-currency, shop-catalog, shop-between-levels, unit-xp-skills, status-effects, teleport-random-exit, difficulty-levels, field-size-picker, game-settings, respawn, save-game, keyboard-controls, gui-render, +stat-pools, +rest-regen, +search-hidden, +listen-at-door, +bash-door, +decoy-goal, +brain-scan-save, +fixed-xp-per-level, +gold-as-xp]
proposes: ["+cond:stat(a, s, op, n)", "+effect:spend_stat(a, s, n)", "+effect:rest(a, n)", "+effect:convert_stat(a, from, to)", "+effect:forget_map", "+effect:identify", "+role:chest", "+ui:stat-pools", "+window:town-hub", "+window:setup-dialog", "+feature:brain-scan", "+feature:reincarnate-on-stairs", "+card:stat-pools", "+card:decoy-goal"]
author: opus
date: 2026-11-09
---

# Beneath Apple Manor — прото-роглайк 1978: кожна дія витрачає свій стат-пул, відпочинок його повертає

## Суть
Один герой спускається процедурними поверхами підвалу під маєтком, щоб знайти Золоте Яблуко в скрині на нижньому поверсі. Головна ідея — **чотири стати як витратні пули**: рух витрачає спритність, удар і вибивання дверей — силу, магія — інтелект, а тіло — це HP. Відпочинок відновлює все, крім тіла, але чим довше відпочиваєш, тим імовірніше напад. Досвід (переважно із золота) витрачають нагорі, підіймаючи максимум статів; загибель не остаточна — герой переселяється на вхідні сходи поверху.

## Поле і час
- Квадратна сітка; поверх — набір кімнат, зʼєднаних дверима; гравець сам задає кількість кімнат на поверх (у lo-res-версії 10, у hi-res Special Edition — 5).
- Поверхи генеруються випадково з урахуванням сили героя й далі незмінні; глибші — важчі.
- Туман війни: спершу видно лише довкола героя, мапа відкривається дослідженням; клітини кольорово кодовані (герой, монстр, двері, скриня).
- Покроково: крок або дія = хід; блукаючі монстри зʼявляються з часом.
- Вхідна клітина поверху — непозначені сходи вгору, до «міста» з магазином.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | Strength, Intelligence, Dexterity, Body — по 20 на старті (поточне/макс), золото, досвід | рух 4 напрямками; кожна дія витрачає свій стат |
| Слиз (Slime) | enemy | мало HP, мала шкода | кислота може зіпсувати куплену броню |
| Привид (Ghost) | enemy | — | лише чарівний меч або Zap; удар назавжди знімає 1–2 сили |
| Троль | enemy | багато HP | регенерує |
| Пурпуровий черв (Worm) | enemy | багато HP | сильний ближній бій |
| Дракон | enemy | мало Body, сильна атака | стереже скриню з яблуком (?) |
| Вампір, Сталкер (невидимий) | enemy | — | у пізніших версіях (?) |
| Двері | gate | зачинені; більшість поверхів має таємні | вибити силою; за героєм зачиняються; монстри крізь двері не ходять |
| Таємні двері | gate | приховані | знайти оглядом стін |
| Скриня | container | золото / жезл / зілля / пастка | відкрити; зілля пʼється одразу; може бути пастка |
| Золоте Яблуко | pickup | справжнє / фальшиве | справжнє — перемога; фальшиве вибухає й убиває |
| Жезли й зілля | pickup | одиничні на гру | подвоїти стат, Zap без витрат, відчинити двері; прокляті — половинять стат, отрута, забуття мапи |
| Магічні меч і броня | pickup | — | меч бʼє привидів; знаходять у скринях |
| Сходи вгору (вхід) | static | — | у місто: магазин, витрата досвіду |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(N|S|E|W)` → ЯКЩО `free(target)` і `custom: «Dexterity > 0»` → ТО `move(hero, dir)`, `counter(dexterity, −)`.
- КОЛИ `input(bash)` → ЯКЩО `cell(ahead, door)` → ТО `counter(strength, −)`, `custom: «двері відчинено»` (шанс від сили (?)).
- КОЛИ `custom: «герой пройшов двері»` → ТО `custom: «двері зачиняються за ним»`; монстри — `block` біля дверей.
- КОЛИ `input(listen)` → ЯКЩО `cell(ahead, door)` → ТО `message(«за дверима є/нема монстра»)`.
- КОЛИ `input(inspect)` → ЯКЩО `custom: «поруч таємні двері»` → ТО `reveal(secret door)`.
- КОЛИ `input(attack)` → ЯКЩО `custom: «Strength > 0»` → ТО `counter(strength, −)`, `damage(monster, від сили)`; влучання — від Dexterity.
- КОЛИ `input(zap)` → ЯКЩО `custom: «Intelligence достатньо»` → ТО `damage(monster)`, `counter(intelligence, −cost)` (від 1 до половини поточного).
- КОЛИ `input(heal)` → ТО `custom: «Intelligence → Body»`.
- КОЛИ `input(x-ray)` → ТО `reveal(r3)` (видно й крізь двері).
- КОЛИ `input(teleport)` → ТО `teleport(hero, random)`, `take(hero, carried gold)`.
- КОЛИ `input(run)` у бою → ТО `custom: «втеча; золото повертається в скриню»`.
- КОЛИ `input(rest n)` → ТО `custom: «відновити n раундів усі стати, крім Body»`; ЯКЩО `rng(p ~ n)` → ТО `spawn(monster)` (напад).
- КОЛИ `input(rest 0)` → ТО `custom: «відновити до максимуму, крім Body»` з тим самим ризиком.
- КОЛИ `contact(monster, hero)` → ТО `damage(hero, n)` (зменшує Body); привид — `custom: «−1–2 Strength назавжди»`; слиз — `custom: «може зіпсувати броню»`.
- КОЛИ `contact(ghost attack, hero weapon)` → ЯКЩО `not has(hero, magic sword)` → ТО `block` (лише Zap або чарівний меч).
- КОЛИ `tick` → ЯКЩО `custom: «троль поранений»` → ТО `heal(troll, n)`.
- КОЛИ `input(open chest)` → ТО `pickup(gold | wand)`, зілля — `custom: «випити одразу»`; ЯКЩО `custom: «пастка»` → ТО `damage(hero)`.
- КОЛИ `custom: «зілля забуття»` → ТО `hide(level map)`; `custom: «зілля отрути»` → `lose` (до переселення).
- КОЛИ `counter(body, ≤, 0)` → ТО `custom: «переселення на вхідні сходи поверху»`, `custom: «стати = останній brain scan або по 20»`.
- КОЛИ `input(spend xp)` у місті → ТО `custom: «+1 до максимуму стату за 10 досвіду»`.
- КОЛИ `input(buy brain scan)` → ТО `currency(−price)`, `custom: «зберегти стати; ціна росте зі статами»`.
- КОЛИ `custom: «знайдено золото»` → ТО `currency(+n)`, `custom: «золото конвертується в досвід»`.
- КОЛИ `input(open apple chest)` → ЯКЩО `custom: «яблуко фальшиве»` → ТО `explode`, `custom: «смерть»`; ЯКЩО справжнє → ТО `win`.
- КОЛИ `level_start` → ТО `message(«досвіду на поверсі: N»)` — кожен поверх має фіксований запас.
- Перемога: відкрити скриню зі справжнім Золотим Яблуком. Поразка: остаточної нема — переселення з відкатом статів. Рахунку нема.

## Керування і ввід
- Клавіатура: `N` `S` `E` `W` — рух (у DOS-версії — стрілки).
- `B` вибити двері · `L` слухати біля дверей · `I` оглянути (таємні двері) · `O` відкрити скриню.
- У бою: `A` атака · `Z` Zap · `H` Heal · `X` X-ray · `R` втеча; телепорт — заклинання-втеча.
- Відпочинок: цифра `1–9` — стільки раундів; `0` — до максимуму.
- Перед стартом — питання про кількість кімнат на поверх і складність 1–10.

## Вікна, меню, HUD
- `setup-dialog`: кількість кімнат на поверх і складність («a pushover» … «you're nuts!!!»).
- `game-screen`: поле (lo-res блоками або hi-res тайлами), `stat-pools` (S I D B поточне/макс), золото, досвід, рядок повідомлень.
- `town-hub` (сходи вгору): `shop-window` (сокира, меч; шкіряна, кольчуга, латна броня; brain scan), витрата досвіду на стати.
- `end-screen`: справжнє яблуко веде до командного рядка (гра закінчується).
- Переходи: `setup-dialog` → поверх 1 → сходи → `town-hub` → назад; смерть → вхідні сходи поверху.

## Фічі поза полем
- Налаштування генерації: кімнат на поверх (`field-size-picker`) і складність 1–10 (`difficulty-levels`).
- «Brain scan» — платне збереження статів; дорожчає, а повторні скани «зношуються».
- Special Edition (1982–83): hi-res графіка, різні складності, збереження прогресу.
- Кожен предмет — один на гру й не витрачається.

## Варіації й родичі
- Нащадок за ідеєю: [rogue](rogue.md) (1980) — без стат-пулів, з голодом і ідентифікацією; далі [nethack](nethack.md), [angband](angband.md).
- Сучасники-кроулери: [dungeons-of-daggorath](dungeons-of-daggorath.md) (втома як ресурс у real-time), [wizardry](wizardry.md) (загін, фіксований лабіринт).
- Осі варіацій: **ресурс дій** (окремий стат на тип дії / одна витривалість / нема) · **смерть** (переселення з відкатом / permadeath) · **досвід** (за вбивства / за золото) · **поверх** (генерується від сили героя / фіксований).

## Цікавинки для курсу
- Стати-пули: кожна дія має «ціну» в одному з чотирьох лічильників, відпочинок повертає — 🌱.
- Відпочинок як ставка: довжина відпочинку × ризик блукаючого монстра — 🌱.
- Генерація поверху «N кімнат з дверима» з параметром від гравця — 🥉.
- Двері, що зачиняються за героєм і не пропускають монстрів: двері як щит — 🌱.
- Фальшиві Золоті Яблука: ціль-приманка, що вбиває — 🌱.
- Brain scan: збереження як платний предмет із ціною, що росте — 📎.

## Мапа на каталог
- Є: `move-4dir` · `dungeon-generation` · `stairs-levels` · `fog-of-war` · `hp-damage` (Body) · `key-and-door` (жезл відкривання) · `one-way-cell` (двері зачиняються за героєм) · `inventory-items` · `item-pickup` · `round-currency` (золото) · `shop-catalog` / `shop-between-levels` · `unit-xp-skills` (досвід → стати) · `status-effects` (отрута, подвоєння/половина) · `teleport-random-exit` · `difficulty-levels` · `field-size-picker` · `game-settings` · `respawn` (на вхідних сходах) · `save-game` · `keyboard-controls` · `gui-render`.
- **Нема** → пропозиції карток:
  - `+stat-pools` «Кожна дія витрачає свій стат-пул» · entities/state · 🌱.
  - `+rest-regen` «Відпочинок N ходів відновлює пули з ризиком нападу» · entities/state · 🌱.
  - `+search-hidden` (як у Rogue) — таємні двері.
  - `+listen-at-door` «Послухати, чи є хтось за дверима» · entities/interact · 🌱.
  - `+bash-door` «Вибити двері коштом сили» · entities/interact · 🌱.
  - `+decoy-goal` «Фальшива ціль, що вбиває» · game-logic/win · 🌱.
  - `+brain-scan-save` «Збереження як покупка з ціною, що росте» · game-logic/save · 📎.
  - `+fixed-xp-per-level` «Кожен поверх має відомий запас досвіду» · game-logic/score · 🌱.
  - `+gold-as-xp` «Золото конвертується в досвід» · game-logic/economy · 🌱.

## Пропозиції до словників
- `+cond:stat(a, s, op, n)` — значення стату-пулу (Dexterity > 0 для кроку).
- `+effect:spend_stat(a, s, n)` — дія витрачає пул; `+effect:rest(a, n)` — відпочинок N раундів; `+effect:convert_stat(a, from, to)` — Heal: інтелект → тіло; `+effect:forget_map` — стерти запамʼятовану мапу; `+effect:identify` (як у Rogue).
- `+role:chest` — скриня з випадковим вмістом і можливою пасткою.
- `+ui:stat-pools` — кілька пулів поточне/макс у рядок.
- `+window:town-hub` (як у EO) · `+window:setup-dialog` — параметри генерації перед партією.
- `+feature:brain-scan` — платне збереження · `+feature:reincarnate-on-stairs` — смерть = повернення на вхід поверху з відкатом.
- `+card:stat-pools` · `+card:decoy-goal`.

## Джерела
- ⭐ [Wikipedia: Beneath Apple Manor](https://en.wikipedia.org/wiki/Beneath_Apple_Manor) — 1978, Don Worth, мета (Golden Apple), 10/5 кімнат на поверх у lo-/hi-res, процедурна генерація, Special Edition 1982–83, платформи.
- [CRPG Adventures: Victory](https://crpgadventures.blogspot.com/2015/11/beneath-apple-manor-1978-victory.html) — стати 20 і що їх витрачає, відпочинок цифрами, 10 досвіду = +1, кімнати й складність 1–10, двері B/L/I, 5 монстрів, A/Z/R, заклинання, магазин, переселення й brain scan, фальшиві яблука.
- [CRPG Addict: Game 79](https://crpgaddict.blogspot.com/2012/12/game-79-beneath-apple-manor-1978.html) — шкала складності словами, двері зачиняються за героєм, фіксований досвід на поверх, предмети зі скринь, Zap-ціна, коментарі Don Worth (DF, кислота слизу, дракон).
- [RogueBasin: Beneath Apple Manor](https://www.roguebasin.com/index.php/Beneath_Apple_Manor) — S/I/D/B як пули по 20, версії.

## Непевне
- (?) Вампіри й невидимі сталкери — у CRPG Addict (ймовірно Special Edition/DOS), в оригіналі за CRPG Adventures — 5 монстрів.
- (?) Яблуко «завжди в скрині дракона» — з коментаря читача; фальшиві яблука на поверхах 36 і ~40, справжнє на ~43 — досвід одного блогера, глибина залежить від налаштувань.
- (?) «Яблуко зʼявляється при статах ~120» — спостереження блогера, не правило.
- (?) Шанс вибити двері й формула шкоди від сили — не знайшов.
- (?) Psittacine Labs і сайт Don Worth (лінки Wikipedia) не відкрились (DNS), Wayback недоступний.
