---
title: Shadowrun Returns
slug: shadowrun-returns
aka: [Shadowrun: Dragonfall, Shadowrun: Hong Kong, SRR]
family: tactics
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: runtime
  goal: state
year: 2013
platforms: [PC, Mac, Linux, iOS, Android, Switch, PS4, PS5, Xbox One, Xbox Series]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Shadowrun_Returns", best: true, note: "2→3 AP, три зброї без витрат на зміну, перезарядка, дрони й духи за AP, Матриця в певних точках, сейви на переходах, редактор"}
  - {kind: other, url: "http://www.gamebanshee.com/9fhr", note: "оновлення розробників №51: тіло декера нерухоме, 3 ходи в Матриці = 1 хід реальності, вихід через той самий портал або dumpshock, IC, ESP, IP деки, поріг тривоги"}
  - {kind: steam, url: "https://store.steampowered.com/app/234650/", note: "6 архетипів, безкласова прогресія, редактор, Workshop"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Shadowrun+Returns+matrix+gameplay", note: "пошук; Матриця й бій"}
stage: v1
coverage: 60
mechanics: [hp-damage, melee-vs-ranged, inventory-items, fog-of-war, ai-opponent, reachable-highlight, path-preview, hover-highlight, in-game-editor, level-exchange, save-game, checkpoint, character-select, difficulty-levels, permadeath, +action-points, +cover-system, +hit-chance, +nested-battlefield, +time-ratio-fields, +inert-body, +alarm-threshold, +summon-ally, +drone-control, +reload-action, +classless-skills, +terminal-hack-switch]
proposes: ["+trigger:jack_in", "+trigger:jack_out", "+trigger:alarm", "+effect:dumpshock", "+cond:summon_control", "+role:ice", "+role:avatar-proxy", "+ui:alarm-meter", "+ui:ap-pips", "+window:character-sheet", "+window:dialogue-window", "+feature:workshop-campaigns", "+axis:field-nested"]
author: opus
date: 2026-11-09
---

# Shadowrun Returns — XCOM-подібний бій на AP, де хакер «пірнає» в друге поле, а його тіло лишається беззахисним у першому

## Суть
Покрокова тактична RPG у кіберпанк-фентезі: загін до 4 «ранерів» (герой + до трьох найманців) бʼється на ізометричній сітці за очки дії (2, згодом 3 за хід). Незвичне для корпусу — **вкладене поле**: декер у спеціальних точках входить у Матрицю — окрему мапу з власними ворогами (IC), де він ходить **три ходи на один хід реального світу**, а його тіло нерухоме і його мусить захищати решта загону. Інші архетипи теж керують «другим тілом»: рігер — дроном, шаман — духом, що може вирватися з-під контролю.

## Поле і час
- Квадратна сітка з ізометричним рендером; укриття біля стін і обʼєктів; туман/видимість персонажів.
- Поза боєм — вільне дослідження (клік-рух), діалоги, термінали; бій починається, коли вороги помітили загін або за сценарієм, і перемикає гру в покроковий режим: спершу ходить уся команда гравця, потім вороги.
- **Матриця** — окрема мапа-LAN з вузлами; вхід лише в певних точках («jack point»). Час: 3 ходи аватара = 1 хід інших учасників.
- Ресурс ходу — очки дії (AP): рух, постріл, перезарядка, заклинання, предмети, керування дроном/духом; здібності й предмети дають або забирають AP.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Ранер (герой / найманець) | piece | раса (5), атрибути, навички, карма, AP 2→3, HP, до 3 зброй | рух, постріл, ближній бій, предмети, магія за AP |
| Street Samurai | piece | зброя, кібер | стрілецький/ближній боєць |
| Mage | piece | заклинання | бачить лей-лінії, що підсилюють магію |
| Shaman | piece | духи | закликає одного духа (предметом або в особливому місці) |
| Decker | piece | кібердека, навичка Decking, ESP | входить у Матрицю в jack point |
| Rigger | piece | дрон як «зброя» | керує дроном за AP |
| Physical Adept | piece | ближній бій | підсилений тілесною магією |
| Дух | ally | сила каналу, час виклику | бʼється за шамана; може **вирватися** і стати ворожим або втекти |
| Дрон | ally | — | діє за AP рігера; дрон і дух одночасно не можна |
| Ворог (гангстер, охорона, маг, дрон) | enemy | HP, зброя | ховається, стріляє, кидає заклинання |
| Укриття | terrain | рівень захисту | знижує шанс влучання по тому, хто за ним (?) |
| Термінал / двері / обʼєкт для штовхання | switch | — | хакінг або штовхання відкривають приховані кімнати й маршрути |
| Jack point | static | — | точка входу декера в Матрицю; вихід лише тут |
| Тіло декера в Матриці | piece | HP | нерухоме, без дій, ціль для ворогів |
| Аватар декера | player | IP деки, програми | ходить по LAN-мапі, бореться з IC |
| IC (Intrusion Countermeasures) | enemy | — | атакують аватара; шкода спершу йде в IP деки |
| Black IC / ворожий декер | boss | — | бʼють аватара в обхід деки — прямо по HP |
| ESP (Expert System Program) | ally | сила від підвміння ESP | автономна «жива» програма під керуванням декера |
| Вузол LAN | switch | — | керує фізичним світом: двері, камери, турелі, допуски, газ у кімнаті |
| Дані | pickup | — | інформація — мета багатьох забігів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(player)` → ТО кожен ранер `custom: «AP = 2 (3 після прокачки)»`.
- КОЛИ `input(move, r, cell)` → ЯКЩО `custom: «вистачає AP на шлях»` → ТО `move`, −AP.
- КОЛИ `input(shoot, r, t)` → ЯКЩО `line_of_sight(r, t)` and `custom: «магазин не порожній»` → ТО `prob(hit)` → `damage(n)`; набої безкінечні, але `custom: «перезарядка коштує AP»`.
- КОЛИ `input(switch_weapon, r)` → ТО `custom: «зміна однієї з трьох зброй без AP»`.
- КОЛИ `input(cast, mage, target)` → ЯКЩО `custom: «стоїть на лей-лінії»` → ТО `custom: «заклинання сильніше»`.
- КОЛИ `input(summon, shaman, spot)` → ЯКЩО `has(shaman, fetish)` or `cell(spot, summon_point)` → ТО `spawn_at(spirit, spot)`.
- КОЛИ `turn_start(player)` → ЯКЩО `state(spirit, summoned)` → ТО `custom: «шаман платить AP за контроль»`; ЯКЩО `custom: «перевірка контролю провалена (сила каналу × час виклику)»` → ТО `set_side(spirit, enemy)` або `disappear_a` (втеча).
- КОЛИ `input(command, rigger, drone)` → ТО `custom: «дрон діє за AP рігера»`; ЯКЩО `state(rigger, has_spirit)` → ТО `block` (дрон і дух — не разом).
- КОЛИ `input(jack_in, decker)` → ЯКЩО `enter(decker, jack_point)` → ТО `set_state(body, inert)`, `spawn_at(avatar, matrix_entry)`.
- Часове співвідношення: КОЛИ `turn_end(avatar)` → ТО `counter(matrix_turns, +1)`; КОЛИ `counter(matrix_turns, ==, 3)` → ТО `custom: «минає один хід реального світу»`, `counter(matrix_turns, 0)`.
- КОЛИ `contact(ic, avatar)` → ТО `damage` → `custom: «спершу IP деки, потім HP»`; ЯКЩО `custom: «атакує Black IC або ворожий декер»` → ТО `damage` прямо по HP.
- КОЛИ `input(action, avatar)` → ТО `counter(alarm, +n)`; КОЛИ `counter(alarm, >=, threshold)` → ТО `spawn(black_ic)` / `spawn(enemy_decker)` / `custom: «проблеми у фізичному світі»`.
- КОЛИ `input(hack, avatar, node)` → ЯКЩО `custom: «вузол захоплено»` → ТО `set_state(door|camera|turret, …)` у фізичному світі.
- КОЛИ `input(jack_out, avatar)` → ЯКЩО `enter(avatar, entry_portal)` → ТО `custom: «декер прокидається без шкоди»`; інакше (eject) → ТО `custom: «dumpshock: шкода тілу»`.
- КОЛИ `hp_zero(body)` → ТО `custom: «декер падає разом з аватаром»` (?).
- КОЛИ `custom: «бій виграно»` → ТО `custom: «повернення в режим дослідження»`; КОЛИ `custom: «досягнуто переходу зони»` → ТО `checkpoint` (автосейв).
- Прогресія: КОЛИ `custom: «сюжетний етап»` → ТО `counter(karma, +n)`; `custom: «карма витрачається на атрибути й навички, клас не обмежує»`.
- Перемога: виконати цілі місії. Поразка: загинув головний герой / весь загін (?).

## Керування і ввід
- Миша: клік по клітині — рух (підсвітка досяжного за 1/2 AP (?)), клік по ворогу — атака поточною зброєю; панель дій унизу — зброя, заклинання, предмети, дрон/дух, перезарядка, Overwatch (?), кінець ходу.
- Поза боєм: клік-рух, діалоги з варіантами (доступність залежить від навичок: Etiquette, Charisma тощо), взаємодія з терміналами й обʼєктами.
- Матриця: керування аватаром тим самим інтерфейсом, але з програмами замість зброї.

## Вікна, меню, HUD
- `main-menu`: Story (кампанія Dead Man's Switch), User Content / Workshop, Editor, Options, Quit.
- `character-select` — створення персонажа: стать, вигляд, раса, архетип (необовʼязковий).
- `game-screen`: ізометрична сітка; портрети загону з HP; `ap-pips` (очки дії); `ability-buttons`; `hit-chance` при наведенні на ціль (?); `turn-indicator` (хід гравця / ворога).
- `dialogue-window` — текстові діалоги з виборами, деякі заблоковані без навичок.
- `character-sheet` — атрибути, навички, витрата карми.
- `inventory-window` — спорядження, 3 зброї, кібердека, предмети.
- `shop-window` — крамниці в хабі між місіями.
- Матриця: окремий `game-screen` з `alarm-meter` (поріг тривоги) і IP деки.
- `pause-menu`: Save (лише в певних точках у базовій грі), Load, Options, Quit.

## Фічі поза полем
- `in-game-editor` — Shadowrun Editor для власних кампаній; `level-sharing` через Steam Workshop і зовнішні сайти.
- Збереження: у базовій грі — **лише на переходах між зонами** (`checkpoint`); вільний сейв додали в Dragonfall.
- Найм найманців на місію; безкласова прогресія за карму.
- Продовження: Dragonfall (2014; Director's Cut — окрема версія), Hong Kong (2015) — Матриця зі стелсом: Watcher IC з конусами огляду й трасуванням (за обговореннями гравців).

## Варіації й родичі
- Родичі в корпусі: [xcom](xcom.md) (2 дії, укриття), [jagged-alliance-2](jagged-alliance-2.md) (AP і найм загону), [invisible-inc](invisible-inc.md) (хакінг як друге поле поверх мапи: інкогніта), [spybot-nightfall](spybot-nightfall.md) (бій програм у мережі), [silent-storm](silent-storm.md).
- Шарові попередники: Shadowrun (SNES/Genesis) — окремий кіберпростір-мінігра.
- **Осі варіацій «друге тіло»:**
  - **хто**: аватар у Матриці (декер) / дрон (рігер) / дух (шаман) / нема;
  - **де**: та сама мапа (дрон, дух) / вкладена мапа зі своїм часом (Матриця) / шар поверх тієї ж мапи (Invisible Inc.);
  - **ризик**: тіло беззахисне / контроль може зірватись (дух) / тривога LAN (Матриця).

## Цікавинки для курсу
- Два поля з різним темпом (3:1) і спільним станом — 🥈: два цикли тіків з синхронізацією.
- Вкладене поле: вузол Матриці перемикає двері/турель у реальному світі — 🥉 (звʼязок сутностей між мапами).
- Шкода спершу в «щит-деку» (IP), потім у HP; окремий тип атаки в обхід — 📎.
- Поріг тривоги: кожна дія додає, перевищення спавнить сильного ворога — 🌱.
- Дух з ймовірністю бунту, що росте з часом і силою — 📎.
- AP з трьома зброями без витрат на зміну і платною перезарядкою — 🌱.
- Сейв лише на переходах зон — 🌱 (і чому гравці його не люблять).

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` · `inventory-items` · `fog-of-war` · `ai-opponent` · `reachable-highlight` / `path-preview` / `hover-highlight` · `in-game-editor` ↔ Shadowrun Editor · `level-exchange` ↔ Workshop · `save-game` / `checkpoint` ↔ сейви на переходах · `character-select` ↔ створення персонажа · `difficulty-levels` · `permadeath` ↔ смерть найманця (?).
- **Нема** → пропозиції карток:
  - `+action-points` (з XCOM) — тут 2→3 AP і витрати на керування дроном/духом.
  - `+cover-system`, `+hit-chance` (з XCOM, Wesnoth).
  - `+nested-battlefield` «Вкладене поле зі своїми сутностями» · levels/format · 🥈 · слот {entry: jack_point}.
  - `+time-ratio-fields` «Різний темп двох полів» · game-logic/opponent · 🥈 · слот {ratio: 3}.
  - `+inert-body` «Тіло без керування, поки дух/розум деінде» · entities/state · 📎.
  - `+alarm-threshold` «Шкала тривоги з порогом» · game-logic/waves · 🌱 · слот {threshold}.
  - `+summon-ally` «Закликаний союзник із ризиком бунту» · entities/spawn · 🥉.
  - `+drone-control` «Друге тіло за AP власника» · entities/move · 📎.
  - `+reload-action` «Перезарядка як дія» · entities/combat · 🌱.
  - `+classless-skills` «Очки досвіду на будь-які навички» · entities/state · 📎.
  - `+terminal-hack-switch` «Хакнутий термінал перемикає двері/турелі» · entities/interact · 📎.

## Пропозиції до словників
- `+trigger:jack_in(a, point)` / `+trigger:jack_out(a)` — вхід у вкладене поле й вихід.
- `+trigger:alarm(level)` — шкала тривоги досягла порогу.
- `+effect:dumpshock(a, n)` — шкода тілу за аварійний вихід (окремий випадок `damage` з іншою причиною — можна звести до `damage`).
- `+cond:summon_control(a, p)` — перевірка контролю над закликаним.
- `+role:ice` — захисна програма-ворог у мережевому полі; `+role:avatar-proxy` — проєкція сутності в іншому полі.
- `+ui:alarm-meter` — шкала тривоги; `+ui:ap-pips` — очки дії над портретом.
- `+window:character-sheet` — атрибути й навички; `dialogue-window` ⏳ — діалоги з перевіркою навичок.
- `+feature:workshop-campaigns` — кампанії спільноти.
- `+axis:field-nested` — у шапці `field` одне значення; тут фактично `square` + `nested` (поле Матриці).

## Джерела
- ⭐ [Wikipedia: Shadowrun Returns](https://en.wikipedia.org/wiki/Shadowrun_Returns) — 5 рас, 6 архетипів, карма, AP 2→3, 3 зброї, перезарядка, дрони й духи, Матриця «в певних точках», сейви на переходах, редактор, Dragonfall/Hong Kong.
- [GameBanshee: post-funding update #51 «Deckers and the Matrix»](http://www.gamebanshee.com/9fhr) — тіло нерухоме, 3:1, вихід через портал / dumpshock, IC і Black IC, ESP, IP деки, поріг тривоги, що керують вузли.
- [Steam: Shadowrun Returns](https://store.steampowered.com/app/234650/) — список фіч, редактор, Workshop.
- YouTube: пошук «Shadowrun Returns matrix gameplay».

## Непевне
- (?) Механіка укриття і точний вплив на шанс — у джерелах лише «є укриття».
- (?) Overwatch як дія ранера — з памʼяті.
- (?) Що буде, коли тіло декера гине в Матриці; чи є таймер на Матрицю.
- (?) Умова поразки місії (смерть героя чи всього загону) і чи найманці гинуть назавжди.
- (?) «Jack point» — назва зі спільноти; у статті — «specific points».
- (?) Стелс у Матриці Hong Kong (Watcher IC, trace) — лише з обговорень гравців.
