---
title: Dungeon Master
slug: dungeon-master
aka: [DM, Dungeon Master (FTL)]
family: roguelike
also: [thinky]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: hidden
  random: runtime
  goal: state
year: 1987
platforms: [Atari ST, Amiga, PC (DOS), Apple IIGS, SNES, TurboGrafx-CD, X68000, PC-9801, FM Towns]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dungeon_Master_(video_game)", best: true, note: "суть: real-time на сітці, 24 дзеркала чемпіонів, руни, навички від вживання, paper doll, сиквели"}
  - {kind: other, url: "https://discmaster.textfiles.com/view/2217/ACE%20CD%201.iso/files/docs/dmasterd.lha/DungeonMaster.doc1", note: "текстовий гайд, ч.1: 24 руни (сила, стихія, форма, клас)"}
  - {kind: other, url: "https://discmaster.textfiles.com/view/2217/ACE%20CD%201.iso/files/docs/dmasterd.lha/DungeonMaster.doc2", note: "текстовий гайд, ч.2: чемпіони, стати, руки, рух 6 кнопками, їжа/вода, сон, список заклинань"}
  - {kind: other, url: "https://mocagh.org/ftl/dm-handbook.pdf", note: "скан оригінального handbook (бачив у пошуку, не відкривав)"}
  - {kind: other, url: "https://www.mobygames.com/game/834", note: "MobyGames (бачив у пошуку, не відкривав)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=dungeon+master+1987+atari+st+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, orientation-state, impassable-cells, key-and-door, button-toggle, hp-damage, inventory, inventory-items, inventory-limit, item-pickup, hunger-clock, status-effects, unit-xp-skills, melee-vs-ranged, projectile-shot, chase-player, stairs-levels, save-game, player-death, party-switch, drag-drop-piece, gui-render, player-camera, +first-person-grid, +party-formation, +rune-casting, +skill-by-use, +light-source, +thirst-clock, +load-speed, +two-hand-slots, +resurrect-reincarnate, +sleep-regen, +throw-to-cell, +spinner-tile]
proposes: ["+trigger:spell_cast(runes)", "+cond:rune_sequence", "+cond:load(op, n)", "+cond:leader(a)", "+effect:cast(runes)", "+effect:sleep(party)", "+effect:skill_xp(a, skill, n)", "+role:party-member", "+ui:party-portraits", "+ui:hand-slots", "+ui:rune-grid", "+ui:eye-mouth-boxes", "+ui:movement-arrows", "+window:character-sheet", "+window:character-create", "+feature:sleep-zzz", "+axis:view=first-person", "+card:skill-by-use", "+card:resurrect-reincarnate"]
author: opus
date: 2026-11-09
---

# Dungeon Master — загін із чотирьох у реальному часі на клітинній мапі; заклинання складаються з рун

## Суть
Перший-особовий данжен-кроулер, де загін до 4 чемпіонів рухається як одна фігура по клітинах підземелля, а бій, голод і магія йдуть у **реальному часі**. Заклинання не вибираються з меню: їх **складають з рун** (сила + стихія + форма + клас), кожен склад коштує мани. Немає XP і рівнів персонажа — **навички (Fighter, Ninja, Priest, Wizard) ростуть від використання**, навіть від невдалих спроб. Мишею беруть і кладуть предмети прямо в 3D-виді й «ляльці» персонажа (paper doll).

## Поле і час
- Сітка клітин на кількох поверхах; загін займає клітину й має орієнтацію; крок вперед/назад/вбік, поворот на 90°.
- Вид від першої особи з глибиною в кілька клітин; немає мапи — гравець малює сам.
- Real-time: монстри ходять і бʼють без очікування вводу; голод і спрага падають з часом; факели згасають.
- Світло — від факелів у руці або заклинань; темрява ховає коридор.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Загін | player | до 4 чемпіонів, орієнтація, швидкість = найповільніший | рух 6 кнопками; клітина = весь загін |
| Чемпіон | ally | Health, Stamina, Mana (поточне/макс), Strength, Dexterity, Wisdom, Vitality, Anti-magic, Anti-fire, Load (кг), 4 навички, 2 руки, рюкзак 17 | діє рукою дії; автоматично повертається до загрози |
| Лідер | player | один із загону | лише він бере/кладе/кидає предмети й натискає кнопки |
| Монстри (огри, скрімери, черви, бехолдери, дракони, камʼяні істоти, ефірні…) | enemy | HP, тип шкоди, вразливості | підходять у real-time; деякі регенерують (скрімери, черви — джерело їжі); бехолдери кидають вогонь |
| Лорд Хаос | boss | — | фінал: знищити вогняним посохом (Firestaff) |
| Дзеркало чемпіона (24) | container | замерзлий чемпіон | вибір: воскресити або переродити |
| Двері | gate | відкрито/закрито | лідер відкриває; деякі — лише заклинанням «відкрити двері-кнопки» (ZO) |
| Замок | gate | потрібен ключ | ключ підносять до замка й клацають |
| Важіль / кнопка на стіні | switch | — | натиснути, стоячи перед стіною |
| Прихована пастка | hazard | — | клацає; відкриває/закриває двері поруч (?) |
| Плита-обертач | terrain | — | повертає загін (виявляє заклинання «сліди») |
| Факел | pickup | горить | світить, лише поки в руці |
| Їжа / вода / фляга | pickup | — | у «рот» чемпіона; порожня фляга — для зілля |
| Зброя, лук + стріли, сагайдак | pickup | дії | рука дії — меню дій; лук потребує стріл у руці готовності; сагайдак сам перезаряджає |
| Скриня | container | вміст | відкривається в руці дії |
| Предмети мани (Staff of Manar, Yew Staff, Moonstone…) | pickup | +мана 1–4 | підвищують ману носія |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(forward|back|strafe)` → ЯКЩО `free(target)` → ТО `move(party, dir)`; інакше `block`.
- КОЛИ `input(turn)` → ТО `face(party, ±90°)`.
- КОЛИ `custom: «загін перевантажений»` → ТО `speed(party, −)` (швидкість = найповільніший).
- КОЛИ `input(action hand)` → ТО `choose(actions of held item)`; ЯКЩО `custom: «дія розблокована навичкою»` → ТО виконати; лук — ЯКЩО `has(ready hand, arrow)`.
- КОЛИ `custom: «удар впритул»` → ЯКЩО `adjacent(party, monster)` → ТО `damage(n)`; інакше промах.
- КОЛИ `input(throw)` (лідер) → ТО `throw(item, ahead)` (дальність від лідера), `custom: «досвід кидання +»`.
- КОЛИ `input(rune)` → ЯКЩО `custom: «мана ≥ ціна складу»` → ТО `custom: «додати склад до заклинання»`, `counter(mana, −cost)`; інакше склад не вимовлено.
- КОЛИ `input(cast)` → ЯКЩО `custom: «послідовність рун відповідає відомому заклинанню й навичка достатня»` → ТО ефект (`spawn_at(fireball, ahead)` для FUL IR, `heal` для VI-зілля, світло для OH IR RA…); інакше `message(невдача)`.
- КОЛИ `after(cast or attempt)` → ТО `custom: «досвід навички Wizard/Priest +»` (і за невдачу).
- КОЛИ `after(melee|throw)` → ТО `custom: «досвід Fighter/Ninja +»`.
- КОЛИ `custom: «перша руна»` → ТО `custom: «сила LO…MON задає потужність і ціну; кожен щабель — однаковий приріст мани»`.
- КОЛИ `timer(every)` → ТО `counter(food, −)`, `counter(water, −)`; ЯКЩО `custom: «їжа/вода в червоному»` → ТО `custom: «здібності слабшають»`; ЯКЩО 0 → `damage` аж до смерті.
- КОЛИ `input(mouth, food|drink)` → ТО `counter(food|water, +)`; неїстівне — не приймається.
- КОЛИ `contact(monster, champion)` → ТО `damage(champion, n)`; ЯКЩО `custom: «атака збоку/ззаду»` → ТО `custom: «небезпечніше»`; можливе `set_state(champion, injured part | poisoned)`.
- КОЛИ `hp_zero(champion)` → ТО `custom: «чемпіон мертвий»` (кістки; воскрешення — у святилищі (?)); ЯКЩО всі мертві → `lose`.
- КОЛИ `input(ZZZ)` → ТО `set_state(party, sleep)`: мана, HP, витривалість відновлюються швидше; КОЛИ `contact(monster, party)` або `input(wake)` → `clear_state(party, sleep)`.
- КОЛИ `input(lever|button)` → ЯКЩО `facing(party, wall with control)` → ТО `custom: «перемкнути ціль (двері, міст, пастку)»`.
- КОЛИ `contact(key, lock)` → ЯКЩО `same(key, lock)` → ТО `custom: «відчинити двері»`.
- КОЛИ `enter(party, spinner)` → ТО `face(party, other dir)`.
- КОЛИ `input(mirror: resurrect)` → ТО `custom: «чемпіон з навичками й іменем»`; `input(mirror: reincarnate)` → ТО `custom: «навички → вищі атрибути, нове імʼя ≤ 7 літер»`.
- КОЛИ `died(Lord Chaos)` з Firestaff → ТО `win` (справжня кінцівка); вийти з посохом без бою — альтернативна кінцівка.
- Перемога: знищити Лорда Хаоса посохом. Поразка: загинули всі чемпіони. Рахунку нема.

## Керування і ввід
- Миша: 6 екранних стрілок (2 повороти, вперед/назад, вбік); те саме з клавіатури.
- Клік у 3D-виді — взяти/покласти предмет, натиснути кнопку, кинути (лідер).
- Ліва «лялька» чемпіона: перетягування предметів між руками, тілом, рюкзаком; «око» — оглянути предмет (вага), «рот» — їсти/пити, перевірка голоду й отрути.
- Панель рун: 6 символів поточної групи; клік — додати склад; кнопка «cast».
- Панель дій: кнопка руки дії → меню дій (рубати, штрикати, стріляти, кидати…).
- Перетягнути портрет на портрет — поміняти місцями; клік по імені — лідер.
- `Esc` — заморозити гру; `Ctrl+S` — збереження.

## Вікна, меню, HUD
- `game-screen`: 3D-вид; вгорі — `party-portraits` з `hp-bar`/`energy-bar` (Health, Stamina, Mana) і `hand-slots`; праворуч — `rune-grid` заклинателя, меню дій, `movement-arrows`.
- `character-sheet` (inventory-window): «лялька» чемпіона, рюкзак 17, сагайдак, око/рот, атрибути, навички.
- `character-create`: дзеркало чемпіона — воскресити/переродити, імʼя ≤ 7 і титул ≤ 19 літер.
- `save-slots`: збереження на чистий диск (є форматування), «save and quit» / «save and continue», «reenter» — продовжити.
- `pause-menu` (Esc — заморозка), `end-screen` (кінцівки), `main-menu` (Enter / Resume).
- Переходи: `main-menu` → Hall of Champions (дзеркала) → підземелля; Ctrl+S → `save-slots`.

## Фічі поза полем
- `save-game` / `continue` (reenter), без автосейву.
- Без мапи — гравець малює сам (рецензенти: «головна складність»).
- Сиквел Chaos Strikes Back (1989) — новий данж і редактор чемпіонів (?).

## Варіації й родичі
- Нащадки: Eye of the Beholder, Lands of Lore, Chaos Strikes Back, Dungeon Master II: The Legend of Skullkeep, Theron's Quest, Dungeon Master Nexus; сучасний — [legend-of-grimrock](legend-of-grimrock.md) (9 рун у сітці 3×3, загін 2×2).
- Попередник: [dungeons-of-daggorath](dungeons-of-daggorath.md) — real-time клітинний кроулер від першої особи для одного героя.
- Осі варіацій: **магія** (руни-склади з ціною / сітка рун / список заклинань) · **прогресія** (від вживання / XP-рівні) · **загін** (1 / 4 у 2×2 / 6) · **час** (real-time / покроково-клітинний).

## Цікавинки для курсу
- Заклинання як послідовність рун з чотирьох груп: парсинг у словник заклинань, ціна мани за кожен склад — 📎.
- Навички від вживання: лічильник досвіду на кожну дію й поріг рівня навички — 🌱.
- Загін як одна фігура в клітині з позиціями всередині (передній/задній ряд) і «найповільніший задає швидкість» — 📎.
- Голод/спрага/факели як годинники реального часу — 🌱.
- Лідер — єдиний, хто взаємодіє зі світом; рука дії/готовності; сагайдак, що перезаряджає — 📎.
- Воскресити чи переродити: перетворення навичок на атрибути — 🌱.
- Клітинний real-time з першої особи: рендер коридору з глибиною з 2D-мапи — 🥈.

## Мапа на каталог
- Є: `move-4dir` + `orientation-state` · `impassable-cells` · `key-and-door` · `button-toggle` · `hp-damage` · `inventory` / `inventory-items` / `inventory-limit` (рюкзак 17, вага) · `item-pickup` · `hunger-clock` · `status-effects` (отрута, травми, сон) · `unit-xp-skills` (≈ навички) · `melee-vs-ranged` · `projectile-shot` (fireball, стріли) · `chase-player` · `stairs-levels` · `save-game` · `player-death` · `party-switch` (вибір лідера) · `drag-drop-piece` (предмети мишею) · `gui-render` · `player-camera`.
- **Нема** → пропозиції карток:
  - `+first-person-grid` «Вид від першої особи на клітинній мапі» · interface/render · 🥈.
  - `+party-formation` «Загін в одній клітині з позиціями 2×2» · entities/move · 📎.
  - `+rune-casting` «Заклинання = послідовність рун з ціною за склад» · entities/combat · 📎.
  - `+skill-by-use` «Навичка росте від кожного вжитку» · entities/state · 🌱.
  - `+light-source` «Факел світить лише в руці й догорає» · interface/render · 📎.
  - `+thirst-clock` «Спрага окремо від голоду» · entities/state · 🌱.
  - `+load-speed` «Вага сповільнює; загін = найповільніший» · entities/move · 🌱.
  - `+two-hand-slots` «Рука дії й рука готовності» · entities/state · 🌱.
  - `+resurrect-reincarnate` «Створення героя з готового: зберегти або перетворити навички» · interface/menus · 🌱.
  - `+sleep-regen` «Сон прискорює відновлення, перериває атака» · entities/state · 🌱.
  - `+throw-to-cell` (як у Grimrock) · `+spinner-tile` (як у Grimrock).

## Пропозиції до словників
- `+trigger:spell_cast(runes)` — завершено вимову послідовності рун.
- `+cond:rune_sequence` (як у Grimrock) — послідовність рун відповідає заклинанню; `+cond:load(op, n)` — вага носія; `+cond:leader(a)` — A лідер загону.
- `+effect:cast(runes)` — виконати заклинання з рун; `+effect:sleep(party)`; `+effect:skill_xp(a, skill, n)` — досвід навички за дію.
- `+role:party-member` — член загону, не окрема клітина.
- `+ui:party-portraits`, `+ui:hand-slots`, `+ui:rune-grid` (усі як у Grimrock); `+ui:eye-mouth-boxes` — «око» оглянути / «рот» зʼїсти; `+ui:movement-arrows` — 6 стрілок руху на екрані.
- `+window:character-sheet`, `+window:character-create` (як у Grimrock).
- `+feature:sleep-zzz` — кнопка сну загону.
- `+axis:view=first-person` (`actors: party` — уже ⏳ у classes.md).
- `+card:skill-by-use` · `+card:resurrect-reincarnate`.

## Джерела
- ⭐ [Wikipedia: Dungeon Master](https://en.wikipedia.org/wiki/Dungeon_Master_(video_game)) — real-time, 24 дзеркала, руни (вогонь + крило = fireball), навички без XP, paper doll, кінцівки, платформи й сиквели.
- [Текстовий гайд ч.1 (discmaster)](https://discmaster.textfiles.com/view/2217/ACE%20CD%201.iso/files/docs/dmasterd.lha/DungeonMaster.doc1) — 24 руни в 4 групах: LO UM ON EE PAL MON · YA VI OH FUL DES ZO · VEN EW KATH IR BRO GOR · KU ROS DAIN NETA RA SAR.
- [Текстовий гайд ч.2 (discmaster)](https://discmaster.textfiles.com/view/2217/ACE%20CD%201.iso/files/docs/dmasterd.lha/DungeonMaster.doc2) — воскресити/переродити, лідер, стати й атрибути, вага, їжа/вода, руки, рюкзак 17, 6 кнопок руху, сон ZZZ, збереження, список заклинань.

## Непевне
- (?) Формація 2×2 (два передні бʼють впритул, задні — стріли/магія/довга зброя) — з памʼяті; гайд каже лише про обмін місцями перетягуванням портретів і «бити впритул лише сусіднє».
- (?) Ями-провали на нижній поверх, плити тиску, телепорти — класика серії з памʼяті; гайд згадує лише приховані пастки, обертачі й двері.
- (?) Кількість поверхів (в памʼяті 14 (?)).
- (?) Воскрешення загиблого чемпіона (вівтар/святилище VI) — з памʼяті.
- (?) Сайт dmweb.free.fr (лінк черги) не відкрився (ECONNREFUSED) — у шапку не клав.
- (?) Скани оригінального handbook/manual (mocagh.org) бачив лише в пошуку.
- (?) Редактор чемпіонів у Chaos Strikes Back — з памʼяті.
