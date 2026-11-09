---
title: Harmless7DRL
slug: harmless-7drl
aka: [Harmless, Harmless 7DRL]
family: roguelike
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2010
platforms: [PC (Windows, Linux), Python]
links:
  - {kind: other, url: "https://github.com/svk/harmless7drl", best: true, note: "код і README (MIT): керування, руни, посохи; monsters.py, traps.py, magic.py — повна механіка"}
  - {kind: other, url: "https://roguetemple.com/7drl/2010", note: "ревʼю 7DRL 2010: «low HP, indirect centered combat is what is innovative»"}
  - {kind: other, url: "https://groups.google.com/g/rec.games.roguelike.development/c/7mtbWal8Nd4", note: "анонс автора (kaw) і відгуки: без прямих атакуючих заклинань, w/m, версія 1.1"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=harmless7drl+roguelike", note: "пошук; відео не знайдено"}
stage: v1
coverage: 60
mechanics: [move-8dir, dungeon-generation, stairs-levels, hp-damage, inventory, inventory-items, inventory-limit, item-pickup, item-identification, thief, chase-player, chase-bfs, random-walk, push-object, fill-hole, explode-area, chain-detonation, environment-death, touch-death, teleport-random-exit, dig-terrain, status-effects, spawner-entity, console-render, message-log, keyboard-controls, permadeath, save-single-slot, fog-of-war, +rune-crafting, +depleting-mana-source, +indirect-combat, +flight-over-traps, +turbulent-air, +escort-carry-back, +ascent-repopulate, +trail-follower, +look-mode]
proposes: ["+trigger:noticed_trap", "+cond:flying(a)", "+cond:identified", "+cond:provoked(a)", "+effect:scribe(spell)", "+effect:identify", "+effect:drop_level(a)", "+effect:gust(a)", "+role:trap", "+role:escort", "+ui:status-line", "+window:spellbook", "+window:look-mode", "+feature:win-report", "+feature:abandon-character", "+card:indirect-combat", "+card:rune-crafting"]
author: opus
date: 2026-11-09
---

# Harmless7DRL — герой із 5 HP, якого вбʼють з одного удару: перемагай пастками, валунами й чарами без атаки

## Суть
Роглайк 7DRL 2010 (kaw), що виглядає як звичайний hack-and-slash, але гравець — помічник професора, слабкий і з дуже малим HP. Майже кожен монстр сильніший і має **свою поведінку**; виграють не боєм, а вивченням поведінки, пастками, валунами, втечею й заклинаннями. Атакуючих заклинань нема: магія — рух, політ, невидимість, копання, телепорт інших, умиротворення. Заклинання не дають готовими: їх **складають з рун**, які треба знайти й ідентифікувати, а мана береться з посоха, що не перезаряджається.

## Поле і час
- Квадратна сітка, процедурні поверхи з кімнатами, дверима, сходами `<` `>`; поверхи памʼятаються (можна підніматись).
- Глибина нескінченна, але ціль — на поверсі 10; далі нового нема.
- Покроково з різною швидкістю сутностей (VerySlow … VeryQuick): один хід гравця = кілька кроків швидких монстрів.
- Видимість обмежена (поле зору), запамʼятовані клітини; помічена пастка підсвічується червоним тлом.
- Шари клітини: підлога/стіна/двері, пастка (прихована/виявлена), «турбулентне повітря», дірка в стелі, предмети, сутність.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець `@` | player | HP 5 (?), стартовий посох: шкода 3, мана 50 | рух 8 напрямками; удар — рухом у монстра; ходить і плаває |
| Посох (crooked/ornate/magnificent) | pickup | шкода 2, мана 50–100 / 100–200 / 200–300 | джерело мани для заклинань; порожній — викинути, носити запасні |
| Сталевий посох | pickup | шкода 5, мана 0 | краща зброя, але без магії |
| Руна `\` | pickup | одна з 10, невідома назва з 17 складів | складник заклинань; губиться при записі заклинання |
| Сувій магії (Tome) | pickup | — | ідентифікує один вид руни в інвентарі |
| Талісмани | pickup | +1 виявлення пасток / +1 макс. HP | діють, поки в інвентарі |
| Зілля лікування | pickup | вага 3 | відновлює HP |
| Валун `0` | object | HP 400, штовхається | закриває огляд; засипає яму-пастку (обидва зникають) |
| Муфлон M | enemy | HP 10, удар 3 | ненавидить магію: у радіусі 5 тупотить, потім атакує, якщо в руці гравця посох з маною > 0; інакше блукає |
| Тура R | enemy | HP 1, удар 3 | стоїть, доки гравець не на одній горизонталі/вертикалі з чистою лінією; тоді мчить до 8 клітин і бʼє; «взяття» тури ставить гравця на її клітину |
| Імп i | enemy | HP 5, дуже швидкий, літає | дебафер: знімає баффи гравця |
| Гном g | enemy | HP 5 | краде посох |
| Гігантський кріт m | enemy | HP 8, повільний | риє стіни |
| Альфон A | enemy | HP 10, удар 3 | переслідує поранених: нападає, лише коли HP гравця < макс |
| Жук-бомбардир b | enemy | HP 1, повільний | при смерті вибухає (радіус 4, шкода 1) — ланцюгова реакція |
| Привид смерті S | enemy | HP 1000, удар 1000, дуже повільний, безтілесний | з поверху 8: проходить крізь усе, вбиває дотиком |
| Нюхач s | enemy | HP 5, удар 1 | іде по сліду гравця |
| Кулярготт C | enemy | HP 20, дуже швидкий | спить у вузьких проходах; неагресивний, поки не спровокувати |
| Уффліан U | spawner | HP 30, удар 4 | породжує 3–6 дитинчат і захищає їх |
| Дитинча уффліана u | enemy | HP 1, швидкий | тримається біля матері; напад на нього провокує її |
| Рибка `~` | enemy | швидка | лише у воді |
| Автомат-професор `h` | neutral | HP 100, вага 30, essential | блукає, уникає пасток; не може шкодити людині; кодове слово — засинає |
| Яма з кілками | hazard | завжди видима | миттєва смерть будь-кого, хто ступив (не літає) |
| Яма-пастка (несмертельна) | hazard | — | застрягнути на 3–6 ходів |
| Міна | hazard | з пов. 3 | вибух радіус 5, шкода 3 усім; одноразова |
| Стрілова пастка | hazard | 1–10 стріл, до пов. 5 | стріла з бійниці: шкода 1 першому на лінії |
| Люк / відкрита діра | hazard | — | падіння на поверх нижче, шкода 1 |
| Телепорт-пастка | hazard | до пов. 8 | у випадкову клітину поверху |
| Обвал | hazard | з пов. 5 | сусідні клітини стають стіною, сутностей виштовхує |
| Турбулентне повітря | terrain | у кімнатах після пов. 5 | порив зносить гравця на сусідню клітину (75 % опору) |
| Двері | gate | відкриті/закриті | відкриваються рухом, `c` — закрити |
| Портал (сходи вгору на пов. 1) | static | — | вихід із підземелля |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(target)` → ТО `move(player, dir)`; ЯКЩО `occupied(target, enemy)` → ТО `damage(enemy, weapon)`; ЯКЩО `occupied(target, boulder)` → ТО `push(boulder)`; ЯКЩО `cell(target, closed door)` → ТО `custom: «відчинити двері»`.
- КОЛИ `input(attack)` по монстру → ТО `custom: «монстр спровокований»` (провокує й захисника-матір).
- КОЛИ `contact(enemy, player)` → ЯКЩО `custom: «гравець не літає над наземним монстром і не в Rockform»` → ТО `damage(player, n)`; інакше `block`.
- КОЛИ `hp_zero(player)` → ТО `lose` (permadeath, звіт у .txt).
- КОЛИ `enter(mob, spike pit)` → ЯКЩО `not custom: «літає»` → ТО `disappear_a` (смерть).
- КОЛИ `enter(mob, web pit)` → ТО `stun(mob, 3–6)`.
- КОЛИ `enter(mob, mine)` → ТО `explode(r5, 3)`, `disappear_b`.
- КОЛИ `enter(mob, arrow trap)` → ЯКЩО `counter(ammo, >, 0)` → ТО `spawn(arrow)`, `damage(first on line, 1)`.
- КОЛИ `enter(mob, trapdoor|hole)` → ТО `custom: «падає на поверх нижче»`, `damage(mob, 1)`.
- КОЛИ `enter(mob, teleport trap)` → ТО `teleport(mob, random)`.
- КОЛИ `enter(mob, rockslide)` → ТО `set_cell(neighbours, wall)`, `push(mobs on them)`.
- КОЛИ `enter(boulder, pit)` → ТО `disappear_both`, `set_cell(pit, floor)`.
- КОЛИ `died(bomber beetle)` → ТО `explode(r4, 1)` → `custom: «підриває сусідніх жуків»`.
- КОЛИ `enter(player, turbulent)` → ЯКЩО `custom: «летить»` або `prob(0.25)` → ТО `move(player, gust dir)` (наступна турбулентна клітина — з імовірністю ×½; летючого зносить завжди).
- КОЛИ `line_of_sight(rook, player)` → ЯКЩО `custom: «по горизонталі/вертикалі»` → ТО `custom: «тура мчить до 8 клітин»` і `damage(player, 3)`, якщо доїхала впритул.
- КОЛИ `in_range(mufflon, player, 5)` → ЯКЩО `custom: «посох у руці з маною > 0»` → ТО `custom: «тупотить, наступного ходу атакує»`.
- КОЛИ `contact(gnome, player)` → ЯКЩО `has(player, staff)` → ТО `take(player, staff)`.
- КОЛИ `contact(imp, player)` → ТО `clear_state(player, buff)`.
- КОЛИ `tick` → ЯКЩО `custom: «HP гравця < макс»` і `in_range(alfon, player, 6)` → ТО `custom: «альфон нападає»`.
- КОЛИ `tick` → ЯКЩО `custom: «клітина на сліді гравця»` → ТО `move(sniffler, along trail)`.
- КОЛИ `input(read Tome)` → ЯКЩО `has(player, unidentified rune)` → ТО `custom: «вибрати вид руни — відкрити її назву»`, `take(player, tome)`.
- КОЛИ `input(w)` → ЯКЩО `custom: «в інвентарі ідентифіковані руни рецепта»` → ТО `take(player, runes)`, `custom: «заклинання записано в книгу»`.
- КОЛИ `input(m, spell)` → ЯКЩО `custom: «мана посоха ≥ ціни»` → ТО `counter(staff mana, −cost)` + ефект заклинання.
- КОЛИ `input(Escape)` (Move+Self, 5) → ТО `teleport(player, random non-trap)`.
- КОЛИ `input(Teleport Other)` (Move+Other, 15) → ЯКЩО `line_of_sight(player, target)` → ТО `teleport(target, random)`.
- КОЛИ `input(Dig)` (Destroy+Earth, 15) → ТО вниз: `custom: «дірка на поверх нижче»`; вгору: `custom: «люк з поверху вище»`; вбік: `set_cell(walls on ray 8, floor)`, `disappear(diggable mobs)`.
- КОЛИ `input(Flight)` (Air+Self, 25) → ТО `set_state(player, flying, 1000–2000)`: пастки не спрацьовують, наземні монстри не дістають.
- КОЛИ `input(Invisibility | Visions | Lifesense)` → ТО `set_state(player, invisible | visions | lifesense, n)`.
- КОЛИ `input(Windblast)` (Move+Air, 5) → ТО `push(flying mobs, out r8)`, `stun(mob, 20–40 per step)`.
- КОЛИ `input(Pacify)` (Calm+Other, 10) → ТО `set_state(target, pacified)`, `clear_state(target, provoked)`.
- КОЛИ `input(Create Boulder)` (Create+Earth, 5) → ТО `spawn(boulder, random free neighbour)`.
- КОЛИ `input(Rockform)` (Earth+Self, 10) → ТО `set_state(player, unattackable, 10)` поки стоїть.
- КОЛИ `input(Heal)` (Negate+Destroy+Self, 20) → ТО `heal(player, full)` · `Reveal Map` (See+Earth, 20) → ТО `reveal(level)` · `Serenity` (Calm+Air, 10) → ТО `custom: «заспокоїти повітря під собою»`.
- КОЛИ `contact(player, automaton)` → ТО `custom: «кодове слово: автомат засинає»`, `pickup(player, automaton)` (якщо вага дозволяє) → `spawn_at(10–14 ascent monsters, every previous level)`.
- КОЛИ `input(<)` під діркою в стелі → ЯКЩО `custom: «літає»` і `not has(player, automaton)` → ТО `custom: «підлетіти на поверх вище»`; з автоматом — `block`.
- КОЛИ `reach(player, portal)` → ЯКЩО `has(player, automaton)` → ТО `win`; інакше `message(«назад не можна»)`.
- Перемога: принести автомат з 10-го поверху до порталу 1-го. Поразка: HP = 0 або здатись `Q` (застряг живим). Рахунку нема — звіт про партію.

## Керування і ввід
- Рух: vi-клавіші (h j k l y u b n), numpad, стрілки (без діагоналей — «невигідно»).
- `.` чекати · `,` підібрати · `d` викинути · `c` зачинити двері · `<` `>` сходи (і дірки, якщо летиш) · `i` інвентар (вжити/озброїтись) · `:` режим огляду (курсор + опис клітини).
- `w` — записати заклинання з рун · `m` — меню заклинань з гарячими клавішами.
- `q` — вийти зі збереженням (сейв стирається при завантаженні) · `Q` — здатися · `?` — довідка клавіш.

## Вікна, меню, HUD
- `main-menu`: нова гра / продовжити (за іменем героя) / інструкції / про гру; вибір імені й статі.
- `help-window`: три сторінки «стіни тексту» для новачків + `?`-список клавіш.
- `game-screen`: ASCII-поле, `status-line` (HP x/y, DL: глибина, баффи), `message-log`.
- `inventory-window`: предмети з вагою, вжити/озброїтись.
- `spellbook` (меню `m`): записані заклинання з ціною й гарячою клавішею.
- `look-mode`: курсор по полю, опис клітини.
- `end-screen`: вступ/фінал текстом; звіт партії записується у файл.
- Переходи: `main-menu` → `game-screen`; `i`/`m`/`:` — модальні; смерть/перемога → звіт.

## Фічі поза полем
- `permadeath`: сейв лише при виході, стирається при завантаженні.
- Звіт про партію в .txt (HP, глибина, вбиті) — `win-report`; автор просив ділитись.
- Конфіг шрифту й розміру терміналу (з v1.1); два фронтенди: curses і libtcod.
- Немає складності, сідів, режимів.

## Варіації й родичі
- Брати 7DRL з «слабким героєм»: Hellth, [not-the-robots](not-the-robots.md) (вороги гинуть від довкілля), [robots](robots.md) (зіткнення роботів як єдина зброя).
- Руни як складники заклинань — у [dungeon-master](dungeon-master.md) і [legend-of-grimrock](legend-of-grimrock.md) (там — послідовність рун), тут — множина рун, що витрачається.
- Ідентифікація назв — як у [rogue](rogue.md) і [nethack](nethack.md), але лише для рун і через окремий сувій.
- Осі варіацій: **бій** (прямий / лише довкіллям / лише втеча) · **мана** (власна з регеном / в предметі без регену) · **заклинання** (дають / купуєш / складаєш з рун) · **повернення** (нема / з вантажем і новими монстрами).

## Цікавинки для курсу
- Бестіарій поведінок: кожен монстр — окремий AI-клас (слідопит, злодій, захисник виводку, мисливець на поранених, шахова тура) — 🥉 (стратегії як обʼєкти).
- Пастки як зброя: яма вбиває будь-кого, валун засипає яму, міна й жуки — ланцюгові вибухи — 📎.
- Рецепти заклинань як множини рун з ідентифікацією через сувій: перевірка `recipe ⊆ inventory` — 🌱.
- Мана в посоху без регенерації — ресурс-предмет, який можна вкрасти — 🌱.
- Турбулентне повітря: порив з каскадом ймовірності `p/2` — 🌱.
- Зворотний шлях з вантажем: заборона літати з ним і перенаселення пройдених поверхів — 📎.
- Шкода залежить від «літає × приземлений»: таблиця досяжності атаки — 🌱.

## Мапа на каталог
- Є: `move-8dir` · `dungeon-generation` · `stairs-levels` · `hp-damage` · `inventory` / `inventory-items` / `inventory-limit` (вага) · `item-pickup` · `item-identification` (руни) · `thief` (гном краде посох) · `chase-player` / `chase-bfs` (pathfind) · `random-walk` (автомат) · `push-object` (валуни) · `fill-hole` (валун у яму) · `explode-area` / `chain-detonation` (міни, жуки) · `environment-death` / `touch-death` (ями, привид) · `teleport-random-exit` · `dig-terrain` (кріт, Dig) · `status-effects` · `spawner-entity` (уффліан) · `console-render` · `message-log` · `keyboard-controls` · `permadeath` · `save-single-slot` · `fog-of-war`.
- **Нема** → пропозиції карток:
  - `+rune-crafting` «Заклинання з набору знайдених рун, руни витрачаються» · entities/state · 📎.
  - `+depleting-mana-source` «Мана в предметі без регенерації» · entities/state · 🌱.
  - `+indirect-combat` «Перемога довкіллям: вороги гинуть у пастках» · entities/combat · 🥉.
  - `+flight-over-traps` «Політ: пастки й наземні вороги не діють» · entities/state · 🌱.
  - `+turbulent-air` «Клітина, що зносить на сусідню з імовірністю» · entities/move · 🌱.
  - `+escort-carry-back` «Принести ціль назад до виходу» · game-logic/win · 🌱.
  - `+ascent-repopulate` «Після здобуття цілі пройдені рівні заповнюються новими ворогами» · game-logic/waves · 🌱.
  - `+trail-follower` «Ворог іде по сліду гравця» · entities/move · 📎.
  - `+look-mode` «Курсор огляду з описом клітини» · interface/input · 🌱.

## Пропозиції до словників
- `+trigger:noticed_trap` — гравець помітив тригер пастки (підсвітка).
- `+cond:flying(a)` — сутність летить; `+cond:identified` (як у Rogue) — руна відома; `+cond:provoked(a)` — монстр спровокований.
- `+effect:scribe(spell)` — записати заклинання, витративши руни; `+effect:identify` (як у Rogue); `+effect:drop_level(a)` — впасти на поверх нижче; `+effect:gust(a)` — порив вітру зносить.
- `+role:trap` — прихована пастка, що спрацьовує на вхід (відрізнити від видимого `hazard`); `+role:escort` — ціль, яку треба донести.
- `+ui:status-line` (як у Rogue).
- `+window:spellbook` — книга записаних заклинань; `+window:look-mode` — режим огляду курсором.
- `+feature:win-report` — текстовий звіт партії у файл; `+feature:abandon-character` — здатись, коли застряг.
- `+card:indirect-combat` · `+card:rune-crafting`.

## Джерела
- ⭐ [GitHub svk/harmless7drl](https://github.com/svk/harmless7drl) — README (керування, руни, посохи без регену, «майже кожен монстр має свою поведінку»), `monsters.py` (бестіарій зі статами й AI), `traps.py` (8 пасток), `magic.py` (10 рун, 14 заклинань з цінами), `items.py`, `plot.py` (сюжет, мета, кодове слово), `level.py` (глибина цілі 10, турбулентність, валуни).
- [Roguelike Review Team 7DRL 2010](https://roguetemple.com/7drl/2010) — оцінки й ревʼю: «low HP, indirect centered combat».
- [rec.games.roguelike.development: анонс](https://groups.google.com/g/rec.games.roguelike.development/c/7mtbWal8Nd4) — «без прямих атакуючих заклинань», клавіші w/m, посох із 50 мани, v1.1 (24.03.2010).

## Непевне
- (?) HP гравця 5 — значення за замовчуванням у конструкторі `Mobile`; гравець його не перевизначає, але в грі могли змінювати (талісман +1).
- (?) Шанс пориву 25 % (75 % опору для пішого, летючого зносить завжди) — прочитано з `level.py`, у грі не перевірив.
- (?) Хто кого вбиває при пастках — за `traps.py`; чи монстри уникають видимих пасток, крім автомата (RandomWalker avoids traps), — не перевірив.
- (?) Вода й рибки: `Nibblefish` визначено, але чи генерується вода у фінальній версії — не перевірив.
- (?) Сторінка RogueBasin «Harmless» з рядка черги — 404, у шапку не клав; відео геймплею не знайшов.
