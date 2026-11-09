---
title: Island of Kesmai
slug: island-of-kesmai
aka: [IoK, Kesmai, "Legends of Kesmai (1996)", "Dungeons of Kesmai (1980)"]
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: online
  info: hidden
  random: runtime
  goal: score
year: 1985
platforms: [CompuServe (термінал), AOL і GameStorm (Legends of Kesmai, 1996)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Island_of_Kesmai", best: true, note: "до 100 гравців, 62 000 клітин, ASCII-сітка, одна команда на 10 секунд, ціни CompuServe"}
  - {kind: other, url: "https://www.filfre.net/2017/12/games-on-the-net-before-the-web-part-3-the-persistent-multiplayer-crpg/", note: "Digital Antiquarian: екран у 4 чвертях, символи мапи, карма, шериф, PvP лише в зонах, дракон"}
  - {kind: other, url: "https://www.engadget.com/2012/03/06/the-game-archaeologist-discovers-the-island-of-kesmai/", note: "Game Archaeologist: 7 класів, старт на 3-му з 21 рівня, черга з трьох кроків, вік у ходах"}
  - {kind: other, url: "https://discmaster.textfiles.com/file/24006/1997-02_Disc_2.13.iso/legends/legends.z/legends.hlp/legends.pdf", note: "довідка Legends of Kesmai (1996, графічний наступник): мапа 7×7, рух до 3 клітин, смерть-привид, воскресіння, карма, закляття"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Island+of+Kesmai+CompuServe", note: "пошук"}
stage: v1
coverage: 40
mechanics: [move-8dir, impassable-cells, fog-of-war, hp-damage, status-effects, inventory, inventory-items, item-pickup, unit-xp-skills, melee-vs-ranged, round-currency, shop-catalog, online-multiplayer, lobby-window, console-render, message-log, status-panel, keyboard-controls, respawn, +shared-world-mmo, +round-clock, +command-queue, +typed-commands, +karma-alignment, +invincible-guard, +pvp-zones, +ghost-corpse-wait, +corpse-recovery, +aging-retirement, +boss-respawn-days, +level-cap-portal, +quest-ladder, +stamina-energy, +weapon-fumble, +town-hub]
proposes: ["+trigger:round_start", "+cond:alignment(a, x)", "+cond:karma(op, n)", "+cond:zone(a, pvp)", "+effect:set_alignment(a, x)", "+effect:resurrect(a)", "+effect:fumble(a)", "+role:guard", "+window:chat-lobby", "+ui:command-line", "+ui:area-description", "+feature:pay-per-hour", "+feature:gm-punish", "+axis:opponent=mmo", "+card:round-clock", "+card:karma-alignment"]
author: opus
date: 2026-11-09
---

# Island of Kesmai — роглайк на 100 гравців: спільна ASCII-сітка острова, одна команда раз на 10 секунд

## Суть
Ранній онлайн-рольовий світ CompuServe (1985): до 100 гравців одночасно ходять одним островом із пʼяти регіонів (≈62 000 клітин, ≈2500 істот), бʼються з монстрами в підземеллях під храмом, виконують квести, торгують у місті. Подача — роглайкова: огляд згори ASCII-символами, короткі текстові команди. Темп задає сервер: **одна команда обробляється раз на 10 секунд**, тому в команду пакують до трьох кроків («n nw n»). Соціальні правила вбудовані в механіку: карма за вбивства й крадіжки псує світогляд, злим не можна в місто, у «цивілізованих» місцях на агресора приходить невразливий шериф.

## Поле і час
- Острів — клітинна сітка (≈62 000 клітин, Engadget називає їх «hexes»; у довідці наступника «hex» — це квадрат 10 футів на мапі 7×7 навколо героя).
- Екран у чотирьох зонах: статус персонажа, огляд згори навколо героя, текст опису місцевості, командний рядок; камера центрована на героєві й прокручується.
- Видимість: стіни й двері затуляють; темрява (вночі чи від закляття) ховає далекі клітини (Legends).
- Час: глобальний такт — **команда раз на 10 с**; одна команда руху — до трьох кроків (ходьба / біг / спринт у Legends).
- Персистентний світ: дракон, убитий кимось, повертається за кілька днів; персонаж старіє в ходах і може померти від старості.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Персонаж гравця `>` | player | клас (7, з них 5 магічних), світогляд, стать, край походження, кидки статів, рівень (старт 3 з 21), HP, витривалість, мана, вік, карма | виконує одну команду за такт |
| Інший гравець `B` | ally | — | союзник у полюванні або загроза в PvP-зонах |
| Монстр `A` | enemy | — | бʼється з позицією, ініціативою, втомою |
| Дракон | boss | — | найсильніший; убивство дає славу; респавн через кілька днів |
| Шериф (і заступники) | neutral | невразливий | у місті нападає на агресорів; злих атакує одразу (Legends) |
| Місто | zone | крамниці, бари, тренери | злим вхід заборонено |
| Храм | zone | — | веде в підземелля; жрець воскрешає (Legends) |
| Стіна `[ ]` | static | — | непрохідна, затуляє огляд |
| Двері `–` / `/` | gate | зачинені / відчинені | відчиняються командою або входом |
| Павутина `@@` | hazard | — | затримує (?) |
| Скарб `$` | pickup | предмет або золото | взяти в руку / мішок |
| Вода | terrain | — | плисти лише по 1 клітині; без закляття — тонути (Legends) |
| Тіло загиблого | container | кілька хвилин | інші можуть нести його до храму; лут лишається на місці (Legends) |
| Портал у Torii / Annwn | gate | рівень = максимум | у розширення 1988 р., назад шляху нема |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `timer(10 s)` → ТО `custom: «сервер виконує по одній команді кожного гравця»` (`+trigger:round_start`).
- КОЛИ `input("n nw n")` → ЯКЩО `free(cells on path)` → ТО `move(char, ≤3 cells)`; стіна → `block`; біг у стіну → `stun(char, n)` (Legends).
- КОЛИ `custom: «біг або спринт з вантажем»` → ТО `counter(stamina, −n)`; КОЛИ `counter(stamina, ==, 0)` → ТО `custom: «лише 1 клітина за команду»` (Legends).
- КОЛИ `input(open door dir)` → ЯКЩО `cell(dir, door)` → ТО `custom: «двері відчинено»`.
- КОЛИ `input(fight target)` → ТО `custom: «кидок влучання: позиція, ініціатива, втома, навичка зброї»`; влучило → `damage(n)`; інакше — блок щитом/зброєю.
- КОЛИ `custom: «удар у бою»` → ЯКЩО `prob(fumble)` → ТО `custom: «зброя падає на клітину — підняти командою take»`.
- КОЛИ `contact(attack, char)` → ЯКЩО `prob(n)` → ТО `stun(char, n)` або `set_state(char, poisoned)`.
- КОЛИ `died(monster)` → ТО `counter(xp, +n)`, `custom: «лут — переможцю»`.
- КОЛИ `counter(xp, >=, threshold)` → ТО `custom: «рівень +1»`; ЯКЩО `level(==, cap)` → ТО `unlock(portal to Torii/Annwn)`.
- КОЛИ `enter(char, portal)` → ТО `teleport(char, Torii|Annwn)`, `custom: «повернення неможливе»`.
- КОЛИ `custom: «напад або крадіжка проти мирного»` → ТО `counter(karma, +1)`, `set_state(char, neutral → evil)`.
- КОЛИ `enter(char, town)` → ЯКЩО `state(char, evil)` → ТО `block`.
- КОЛИ `custom: «напад на персонажа в цивілізованій зоні»` → ТО `spawn_at(sheriff, near attacker)`, `custom: «невразливий шериф атакує агресора»`.
- КОЛИ `input(attack player)` → ЯКЩО `not custom: «зона дозволяє PvP»` → ТО `block`.
- КОЛИ `custom: «скарги на грифера»` → ТО `custom: «адміністратори-ghods забирають досвід, предмети або вбивають»`.
- КОЛИ `died(dragon)` → ТО `custom: «вічна слава»`; КОЛИ `timer(кілька днів)` → ТО `respawn(dragon)`.
- КОЛИ `counter(age_turns, >=, lifespan)` → ТО `custom: «смерть від старості, без воскресіння»`.
- КОЛИ `hp_zero(char)` → ТО `set_state(char, ghost)`, `custom: «тіло лежить; привид не рухається, може говорити»` (Legends).
- КОЛИ `custom: «тіло принесено до жерця храму»` → ТО `custom: «воскресіння з найменшими втратами»`; інакше через час — `respawn(char, temple)`, `custom: «мінус конституція, сила, навички»` (Legends).
- КОЛИ `custom: «загинув у вогні»` → ТО `custom: «тіла нема, речі на землі»`; КОЛИ `custom: «зʼїдений або злий»` → ТО `teleport(char, underworld)` (Legends).
- КОЛИ `input(warm spell)` → ТО `custom: «закляття готове»`; КОЛИ `input(cast)` → ЯКЩО `custom: «мана достатня»` → ТО `custom: «ефект»`; ЯКЩО `custom: «отримав шкоду ≥ 1/6 HP»` → ТО `custom: «закляття згасає»` (Legends).
- КОЛИ `custom: «квест виконано першим»` → ТО `give(char, unique item)`.
- Перемога: нема — рівень, слава, квести. Поразка: смерть (воскресіння з втратами) або старість. Рахунок: досвід і рівень (до 21).

## Керування і ввід
- Командний рядок: короткі фрази й скорочення, напрямки `n`, `nw`, `e` …, до трьох у команді; дії — `fight`, `take`, `open door n`, закляття, розмова (чат у тому ж рядку).
- Ранні версії — однолітерні команди; потім — квазіприродний парсер.
- Темп: команда лягає в чергу й виконується на наступному 10-секундному такті; кожна команда коштувала ≈1⅔ цента (тариф CompuServe за годину).
- Користувацькі фронтенди (Mac) замінювали ASCII на кольорові бітмапи.

## Вікна, меню, HUD
- Вхід у CompuServe → вибір гри → `character-create` (кидки статів, перекидання до 17–18; клас, світогляд Lawful/Neutral, стать, край) → `lobby-window` (конференц-кімната, чат) → світ.
- `game-screen` у чотирьох зонах: `status-panel` (HP, стан), огляд мапи ASCII, `+ui:area-description` (опис місцевості й подій), `+ui:command-line`.
- Легенда символів: `>` — ти, `A` — монстр, `B` — інший гравець, `@@` — павутина, `$` — скарб, `[ ]` — стіни, `–` / `/` — зачинені / відчинені двері.
- Legends of Kesmai (1996): мапа 7×7, іконки, шкали HP (червона), витривалості (зелена), мани (синя), список істот з кольором світогляду, стійки заклинань.

## Фічі поза полем
- `online-multiplayer` на 100 гравців у спільному персистентному світі; чат-кімната.
- `+feature:pay-per-hour`: $6/год (300 бод) або $12/год (1200 бод); мануал на 181 сторінку за $16.50.
- `+feature:gm-punish`: адміністратори карають грифінг.
- Advanced Game — після достатнього досвіду; розширення 1988 р. (Torii, Annwn) — після максимального рівня.
- Церемонії наступника в Legends: передати досвід «нащадку» замість гри побитим персонажем.

## Варіації й родичі
- Dungeons of Kesmai (1980, 6 гравців; на CompuServe — однокористувацька, 1982) → Island of Kesmai (1985) → Legends of Kesmai (1996, графіка, AOL/GameStorm); закрито 2000 р. після купівлі EA.
- Родичі в корпусі: [rogue](rogue.md) і [nethack](nethack.md) (ASCII-огляд, той самий словник символів), [larn](larn.md) (місто + підземелля), [wizardry](wizardry.md) (карма-подібний світогляд і воскресіння в храмі).
- Осі варіацій: **гравці** (один / кілька в одному світі / сотня) · **темп** (хід гравця / глобальний такт / real-time) · **смерть** (остаточна / воскресіння з втратами / привид, що чекає допомоги) · **PvP** (заборонено / лише в зонах / скрізь з кармою).

## Цікавинки для курсу
- Глобальний такт: команди всіх гравців збираються й виконуються раз на 10 с — 🥉 (черга, синхронізація).
- Черга з кількох кроків у одній команді («n nw n») з перевіркою шляху — 🌱.
- Карма й світогляд як автомат станів Lawful → Neutral → Evil, що закриває місто — 🌱.
- Невразливий охоронець-NPC, що зʼявляється на агресію в безпечній зоні — 📎.
- Смерть-привид: тіло лежить кілька хвилин, інший гравець несе його до храму — 📎.
- Спільний персистентний світ з респавном боса «через кілька днів» — 🥈.

## Мапа на каталог
- Є: `move-8dir` · `impassable-cells` · `fog-of-war` (огляд, ніч, темрява) · `hp-damage` · `status-effects` (оглушення, отрута) · `inventory` / `inventory-items` / `item-pickup` · `unit-xp-skills` · `melee-vs-ranged` · `round-currency` (золото) · `shop-catalog` · `online-multiplayer` · `lobby-window` · `console-render` (ASCII) · `message-log` · `status-panel` · `keyboard-controls` · `respawn` (дракон).
- Вже пропоновані: `+typed-commands` (як у Daggorath) · `+corpse-recovery` (як у Wizardry) · `+aging-retirement` · `+stamina-energy` · `+town-hub`.
- **Нема** → пропозиції карток:
  - `+shared-world-mmo` «Спільний персистентний світ для багатьох гравців» · game-logic/opponent · 👑.
  - `+round-clock` «Глобальний такт: команда кожного гравця раз на N секунд» · game-logic/opponent · 🥉.
  - `+command-queue` «Кілька кроків в одній команді» · interface/input · 🌱.
  - `+karma-alignment` «Карма за вбивства мирних змінює світогляд і доступ до місць» · entities/state · 🌱.
  - `+invincible-guard` «Невразливий NPC карає агресію в безпечній зоні» · entities/move · 📎.
  - `+pvp-zones` «PvP дозволено лише в окремих зонах» · game-logic/opponent · 🌱.
  - `+ghost-corpse-wait` «Загиблий — привид біля тіла, чекає воскресіння» · game-logic/lose · 📎.
  - `+boss-respawn-days` «Бос повертається через реальний час» · entities/spawn · 🌱.
  - `+level-cap-portal` «Портал у нові землі після максимального рівня, без повернення» · levels/progression · 🌱.
  - `+quest-ladder` «Сходи квестів з ростом нагород» · levels/progression · 📎.
  - `+weapon-fumble` «Невдалий удар — зброя падає на клітину» · entities/combat · 🌱.

## Пропозиції до словників
- `+trigger:round_start` — почався глобальний такт сервера.
- `+cond:alignment(a, x)` (як у Wizardry) · `+cond:karma(op, n)` — карма персонажа · `+cond:zone(a, pvp)` — зона дозволяє PvP.
- `+effect:set_alignment(a, x)` — зміна світогляду · `+effect:resurrect(a)` (як у Wizardry) · `+effect:fumble(a)` — випустити зброю.
- `+role:guard` — невразливий охоронець порядку.
- `+window:chat-lobby` — чат-кімната перед входом у світ.
- `+ui:command-line` — рядок текстових команд · `+ui:area-description` — текст опису місцевості.
- `+feature:pay-per-hour` — погодинна оплата сесії · `+feature:gm-punish` — модерація гравців адміністраторами.
- `+axis:opponent=mmo` — масовий онлайн-світ (відмінний від `online`-партії).
- `+card:round-clock` · `+card:karma-alignment`.

## Джерела
- ⭐ [Wikipedia: Island of Kesmai](https://en.wikipedia.org/wiki/Island_of_Kesmai) — до 100 гравців (у попередника — 6), 5 регіонів, 62 000 локацій, 2500 істот, ASCII-сітка, рух клітинами короткими командами, одна команда на 10 с, ціни CompuServe, мануал 181 с., Torii й Annwn після максимального рівня без повернення.
- [Digital Antiquarian: The Persistent Multiplayer CRPG](https://www.filfre.net/2017/12/games-on-the-net-before-the-web-part-3-the-persistent-multiplayer-crpg/) — екран у 4 чвертях, легенда символів, бій (позиція, ініціатива, втома, оглушення, отрута, fumble), карма good → neutral → evil, місто для злих закрите, невразливий шериф, PvP лише в зонах, ghods, дракон з респавном.
- [Engadget: The Game Archaeologist discovers the Island of Kesmai](https://www.engadget.com/2012/03/06/the-game-archaeologist-discovers-the-island-of-kesmai/) — 7 класів (5 магічних), 2 світогляди, кидки статів, старт 3 з 21 рівня, вік у ходах і смерть від старості, черга «n nw n», команда раз на 10 с.
- [Довідка Legends of Kesmai (PDF)](https://discmaster.textfiles.com/file/24006/1997-02_Disc_2.13.iso/legends/legends.z/legends.hlp/legends.pdf) — наступник 1996 р.: мапа 7×7 «hexes» по 10 футів, рух до 3 клітин (ходьба/біг/спринт), витривалість, плавання, fumble, привид і 3 способи воскресіння, карма й 4 світогляди, закляття «розігріти → скастувати».

## Непевне
- (?) Правила смерті й воскресіння в самому Island of Kesmai — описано за довідкою Legends of Kesmai (1996); оригінал міг відрізнятися.
- (?) Розмір огляду в IoK (у Legends — 7×7; Engadget пише «6x6 hexes») — не звірив.
- (?) Чи такт 10 с спільний для всіх гравців (одночасне виконання) чи лише ліміт на гравця — джерела кажуть «одна команда кожні 10 секунд».
- (?) Назви 7 класів IoK (Legends має 5: Fighter, Martial Artist, Thief, Wizard, Thaumaturge) — не знайшов.
- (?) Що робить павутина `@@` — лише символ у легенді.
- (?) PvP: Filfre — «лише в окремих зонах», довідка Legends — «повністю заборонено»; правила, мабуть, змінювались.
- (?) Рух по діагоналі в IoK (Engadget наводить «nw») — прийнято 8 напрямків.
