---
title: Escape from the Aliens in Outer Space
slug: escape-from-the-aliens-in-outer-space
aka: [EFTAIOS, Escape from the Aliens]
family: hidden-deduction
also: [board-digital]
klass: avatar
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: hidden
  random: both
  goal: race
year: 2010
platforms: [board (Santa Ragione; Ultimate Edition — Osprey Games 2016)]
links:
  - {kind: other, url: "https://www.ospreypublishing.com/media/fssckwfb/efa-rulebook-for-web.pdf", best: true, note: "офіційні правила Ultimate Edition: сетап, 5 типів секторів, рух, карти небезпечного сектора, атака, живлення, 9 предметів, 16 персонажів, капсули, 40 ходів, 8 зон"}
  - {kind: other, url: "https://rulespal.com/escape-from-the-aliens-in-outer-space/rulebook", note: "конспект попереднього видання: базова/розширена гра, 39 раундів, 6 предметів, ліміт 3 предмети, люки, сценарії Infection / Arena / Old School"}
  - {kind: official, url: "https://www.eftaios.com/", note: "сайт гри: онлайн-редактор карт і сценаріїв, правила, завантаження"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Escape+from+the+Aliens+in+Outer+Space+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 70
mechanics: [move-by-input, impassable-cells, reach-exit, inventory-items, inventory-limit, teleport, cell-click, turn-enforcement, hot-seat, move-notation, message-log, fog-of-war, character-select, match-setup, pass-device, level-select, in-game-editor, rule-variants, game-screen, end-screen, help-window, +hidden-movement, +hidden-roles, +noise-announcement-deck, +bluff-declaration, +area-attack-blind, +killed-joins-enemy, +escape-pod-lottery, +belief-set-tracking, +team-vs-team-secret, +role-abilities-once]
proposes: ["+effect:secret_move", "+effect:announce", "+effect:draw_card", "+effect:reveal_identity", "+trigger:attack", "+cond:identity", "+role:character-card", "+ui:movement-record", "+ui:noise-log", "+ui:hand-cards", "+window:role-screen", "+window:movement-sheet", "+feature:map-editor-web", "+card:noise-announcement-deck", "+card:bluff-declaration", "+card:area-attack-blind", "+card:killed-joins-enemy", "+card:escape-pod-lottery", "+card:hidden-roles", "+card:team-vs-team-secret", "+card:role-abilities-once"]
author: opus
date: 2026-11-09
---

# Escape from the Aliens in Outer Space — у темряві станції люди тікають до капсул, а приховані серед них чужі полюють на «шум»: позиції пишуть олівцем, а ролі — секрет

## Суть
Кожен гравець — член екіпажу на гекс-карті станції, але **ніхто не знає, хто людина, а хто чужий**: ролі роздаються закритими картками. Фішок нема: кожен таємно записує координати свого сектора в журнал ходів. Стати в небезпечний сектор — тягнути карту, що змушує оголосити «шум у моєму секторі», дозволяє збрехати («шум у будь-якому») або дає тишу. Чужі атакують «наосліп» сектор, куди прийшли, — гинуть усі, хто там є, зокрема свої. Люди виграють поодинці, дістаючись рятувальних капсул, які можуть виявитись зламаними.

## Поле і час
- Гекс-сітка поверх плану станції; сектор має координати «літера+число» (D08); спеціальні сектори — символами без координат. 8 зон (Galilei, Fermi, Galvani, Volta, Marconi, Socrates, Morgenland, Levi-Montalcini) з різною кількістю гравців.
- Типи секторів: тихий, небезпечний, сектор людей (старт), сектор чужих (старт), рятувальна капсула (нумерована); стіни — поза сіткою.
- Раунд: кожен гравець за годинниковою **обовʼязково** рухається; 40 ходів у журналі (Ultimate; попереднє видання — 39).
- Інформація: своя роль і позиція — лише власнику; публічно — оголошення шуму/тиші, атаки, використані предмети, розкриті картки загиблих. Кожен веде нотатки на своїй карті маркером.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Людина | player | швидкість 1 | рух на 1 сектор; не атакує (лише з предметом); може використовувати предмети; виграє, втікши капсулою |
| Чужий | enemy | швидкість 1–2; після живлення 1–3 | атакує сектор, у який прийшов; предмети лише збирає для блефу |
| Тихий сектор | terrain | — | оголосити «Silent Sector», хід скінчено |
| Небезпечний сектор | terrain | — | тягнути карту небезпечного сектора (крім ходу з атакою) |
| Сектор людей / чужих | static | без координат | стартова точка; після старту не можна ні пройти, ні стати |
| Рятувальна капсула | gate | номер; лише люди | тягнути карту капсули: зелена — втеча, червона — зламана |
| Карта «Noise in Your Sector» | object | — | оголосити свої справжні координати |
| Карта «Noise in Any Sector» | object | — | оголосити будь-які координати (блеф) |
| Карта «Silence» | object | — | «Silence in all sectors»; лишається в руці для блефу |
| Карта предмета | pickup | 17 у колоді, одноразові | оголошується як тиша; лише люди використовують |
| Attack | pickup | — | людина атакує за правилами чужих (після руху на 1) |
| Teleport | pickup | — | перенос у сектор людей, на додачу до руху |
| Adrenaline | pickup | — | +1 сектор руху цього ходу |
| Sedatives | pickup | — | не тягнути карту небезпечного сектора цього ходу |
| Defence | pickup | — | атака на тебе без наслідків |
| Spotlight | pickup | — | усі в названому секторі й 6 сусідніх оголошують точні координати |
| Clone | pickup | — | при загибелі не стаєш чужим: наступний хід з сектора людей |
| Sensor | pickup | — | обраний гравець оголошує точні координати |
| Mutation | pickup | — | людина стає чужим на місці |
| Cat | pickup | — | оголосити шум у двох різних секторах |
| Карта персонажа | container | 16: 8 людей, 8 чужих, ранг | роль + унікальна здібність (часто раз за гру) |
| Карта капсули | object | 5, зелені й червоні | визначає результат спроби втечі |
| Журнал ходів | zone | 40 клітинок | координати кожного ходу + ініціали використаних предметів, «*» для здібності |

## Правила (КОЛИ → ЯКЩО → ТО)
- Сетап: КОЛИ `game_start` → ТО `custom: «з двох стосів (сині люди, червоні чужі) взяти по половині кількості гравців, +1 чужий при непарній, перемішати й роздати сорочкою»`; люди стартують у секторі людей, чужі — у секторі чужих.
- Рух: КОЛИ `turn_start(player)` → ТО `custom: «таємно записати координати нового сектора в журнал»`; ЯКЩО `state(player, human)` → 1 сектор; ЯКЩО `state(player, alien)` → 1–2; ЯКЩО `state(player, fed)` → 1–3.
- Обмеження руху: ЯКЩО `custom: «кінцевий сектор = стартовий сектор ходу»` → `block`; ЯКЩО `cell(path, human_sector|alien_sector)` → `block`; ЯКЩО `cell(target, escape_pod)` і `state(player, alien)` → `block`.
- КОЛИ `enter(player, silent_sector)` → ТО `message("Silent Sector")`.
- КОЛИ `enter(player, dangerous_sector)` → ЯКЩО `not custom: «гравець атакує цього ходу»` і `not state(player, sedated)` → ТО `custom: «тягнути карту небезпечного сектора, нікому не показуючи»`.
- КОЛИ `custom: «витягнуто Noise in Your Sector»` → ТО `message(own_coords)`; карту скинути сорочкою.
- КОЛИ `custom: «витягнуто Noise in Any Sector»` → ТО `message(any_coords)` на вибір гравця; скинути сорочкою.
- КОЛИ `custom: «витягнуто Silence або предмет»` → ТО `message("Silence in all sectors")`, `give(player, card)` (карта лишається перед гравцем сорочкою).
- КОЛИ `custom: «колода скінчилась»` → ТО `custom: «перетасувати лише скинуті карти шуму»`.
- Атака: КОЛИ `input(attack)` → ЯКЩО `state(player, alien)` або `has(player, attack_item)` → ТО `message("I attack in sector X")` = власний сектор; без тягнення карти.
- КОЛИ `custom: «атака в секторі»` → ЯКЩО `occupied(sector, any_player)` → ТО `custom: «гине кожен у секторі — людина чи чужий»`; загиблий розкриває картку персонажа й скидає карти.
- КОЛИ `died(human)` → ЯКЩО `not has(human, clone)` → ТО `transform(human, alien)`, `respawn(alien, alien_sector)` наступного ходу без здібностей і предметів.
- КОЛИ `died(alien)` → ТО `custom: «вибуває назавжди»`.
- Живлення: КОЛИ `custom: «чужий убив людину»` → ТО `set_state(alien, fed)` → швидкість 1–3 до кінця гри; повторні вбивства не додають.
- Предмети: КОЛИ `input(use, item)` → ЯКЩО `state(player, human)` (або здібність чужого) → ТО `custom: «показати й виконати; карта лишається відкритою перед гравцем до кінця гри»`; скільки завгодно за хід, кожен раз.
- КОЛИ `custom: «на гравця напали»` → ЯКЩО `has(human, defence)` → ТО `block`; ЯКЩО `has(human, clone)` → ТО `respawn(human, human_sector)` (скинувши тишу й предмети).
- КОЛИ `input(use, spotlight, sector)` → ТО `custom: «усі в секторі й 6 сусідніх оголошують точні координати (не роль)»`.
- КОЛИ `input(use, sensor, player)` → ТО `custom: «гравець оголошує точні координати»`.
- КОЛИ `input(use, teleport)` → ТО `teleport(player, human_sector)`; Adrenaline → `custom: «+1 сектор руху»`; Sedatives → без карти; Mutation → `transform(human, alien)` на місці.
- КОЛИ `input(use, cat)` → ЯКЩО `custom: «до тягнення карти»` → ТО `custom: «оголосити шум у двох секторах; якщо витягнуто Noise in Your Sector — один із них справжній»`.
- Капсула: КОЛИ `enter(human, escape_pod)` → ТО `custom: «назвати капсулу, витягнути й показати карту капсули»`.
- КОЛИ `custom: «карта капсули зелена»` → ТО `win` (ця людина), `set_cell(pod, used)` — для інших закрита.
- КОЛИ `custom: «карта капсули червона»` → ТО `set_cell(pod, damaged)`; гравця там не можна атакувати, але наступного ходу він мусить вийти.
- КОЛИ `custom: «усі капсули використано або зламано»` → ТО `lose` для людей, що лишились.
- КОЛИ `counter(turn, =, 40)` → ТО `lose` для людей на борту, `win` чужим.
- КОЛИ `custom: «останню людину на борту вбито»` → ТО `win` чужим (люди, що втекли, теж переможці).
- Персонажі: Captain — перший небезпечний сектор без карти; Pilot — раз «два шуми» як Cat; Psychologist — стартує в секторі чужих; Soldier — раз атакує без предмета; Executive Officer — раз стоїть на місці непомітно; Co-Pilot — раз Teleport, розкриваючи роль; Engineer — тягне 2 карти капсули й обирає; Medic — раз змушує гравця розкрити роль.
- Чужі-персонажі: Blink / Silent / Surge — можуть використовувати Teleport / Sedatives / Adrenaline непомітно; Brute — імунний до атак (розкривається); Invisible — імунний до Sensor і Spotlight (розкриває роль замість позиції); Lurking — може атакувати свій сектор без руху; Fast — перший рух до 3 секторів; Psychic — Silence для нього діє як Noise in Any Sector.
- Перемога людини: втекти зеленою капсулою · Перемога чужих: убити останню людину на борту або дотягти до 40-го ходу · Рахунку нема.

## Керування і ввід
- Настолка: олівцем/маркером — координати в журнал; голосом — «Silent Sector», «Noise in sector D08», «Silence in all sectors», «I attack in sector D08»; карти — у руці сорочкою.
- Рух за ходом обовʼязковий; гравець може й повинен вести нотатки про чужі оголошення на своїй карті.
- Цифрова версія (?): клік по досяжному гексу (`reachable-highlight`), вибір «атакувати / ні», вибір сектора для фальшивого шуму, рука карт; передача пристрою, бо позиція й роль секретні.

## Вікна, меню, HUD
- `match-setup` (цифрова версія): кількість гравців, `level-select` зони (8 карт з рекомендованою кількістю гравців), базова гра без предметів і здібностей / повна, сценарії.
- `role-screen` (custom-window, цифрова версія): закрита картка персонажа — роль, ранг, здібність; відкривається лише власнику.
- `pass-device` (цифрова версія): між ходами, щоб наступний не бачив чужого журналу.
- `game-screen` (цифрова версія): гекс-карта зони з власними нотатками, `movement-record` (40 клітинок), `noise-log` оголошень усіх гравців за ходами, `hand-cards` (тиша й предмети сорочкою), `turn-counter`, `turn-indicator`.
- `movement-sheet` (custom-window): журнал на весь екран з ініціалами предметів і «*» здібностей.
- `end-screen` (цифрова версія): хто втік, хто загинув, розкриття всіх ролей і маршрутів (`replay-window`).
- `help-window`: правила, памʼятка предметів (у книжці карт).
- Переходи: match-setup → role-screen → game-screen ↔ pass-device → end-screen.

## Фічі поза полем
- Базова гра для новачків: зона Galilei, без предметів і здібностей; карти з предметами = тиша.
- `custom-rules`: сценарії попереднього видання (Infection, Arena, Old School); там же розширена гра з лімітом 3 предмети.
- `level-editor` + `level-sharing`: онлайн-редактор карт і сценаріїв на eftaios.com, друк вдома.
- `hotseat`/`local-multiplayer` 2–8 гравців (до 16 — дві коробки, за RulesPal).

## Варіації й родичі
- Видання: попереднє (RulesPal) — 39 раундів, загиблі люди вибувають, 6 предметів, ліміт 3, «люки» з картами зелений/червоний, базова гра — перша людина на люку виграє; Ultimate (Osprey, 2016) — 40 ходів, загиблі люди воскресають чужими, 9 предметів, 16 персонажів, 8 зон.
- [Scotland Yard](scotland-yard.md), [Fury of Dracula](fury-of-dracula.md), [Specter Ops](specter-ops.md) — прихований рух, але ролі відомі; [Captain Sonar](captain-sonar.md) — дедукція позиції з оголошень; [Hunt the Wumpus](hunt-the-wumpus.md) — «звуки» сусідніх небезпек.
- **Осі варіацій**: ролі «відомі / приховані»; оголошення «завжди правда / колода з блефом»; атака «по фішці / по сектору наосліп, дружній вогонь»; загиблий «вибуває / переходить до ворогів»; вихід «гарантований / лотерея капсул».

## Цікавинки для курсу
- Гекс-сітка з координатами «літера+число», сусідство й досяжність за N кроків з заборонними стартовими секторами — 📎.
- Прихований рух + журнал + колода оголошень (правда / блеф / тиша) — 🥉 (модель «що бачать інші»).
- Атака наосліп по сектору з дружнім вогнем і перетворенням загиблих людей на чужих — 📎.
- 16 персонажів з одноразовими здібностями як таблиця модифікаторів правил — 🥉.
- Трекер можливих позицій кожного гравця з урахуванням блефу (Noise in Any Sector робить оголошення недостовірним) — 🥈.
- AI-чужий: атакувати сектор з найбільшою ймовірністю людини, не видавши себе зарано — 🥇.

## Мапа на каталог
- Є: `move-by-input` + `impassable-cells` (стіни, стартові сектори) · `reach-exit` (капсули) · `inventory-items` + `inventory-limit` (предмети, ліміт 3 у старому виданні) · `teleport` · `cell-click` · `turn-enforcement` + `hot-seat` · `move-notation` + `message-log` (журнал і оголошення) · `fog-of-war` · `character-select` (роль) · `match-setup` + `level-select` (зона) · `pass-device` · `in-game-editor` (редактор карт на сайті) · `rule-variants` (сценарії) · `game-screen` / `end-screen` / `help-window`.
- **Нема** → пропозиції карток:
  - `+hidden-movement` (Scotland Yard) — рух записом у журнал.
  - `+hidden-roles` «Ролі роздано закрито, сторону треба вгадати з поведінки» · game-logic/players · 📎.
  - `+noise-announcement-deck` «Колода оголошень позиції: правда / будь-де / тиша» · game-logic/info · 📎.
  - `+bluff-declaration` «Гравець має право збрехати в оголошенні» · game-logic/info · 🌱.
  - `+area-attack-blind` «Атака по клітині наосліп, гинуть усі в ній» · entities/combat · 🌱.
  - `+killed-joins-enemy` «Загиблий переходить на бік ворога» · game-logic/players · 🌱.
  - `+escape-pod-lottery` «Вихід — лотерея карт: успіх або зламаний вихід» · game-logic/win · 🌱.
  - `+belief-set-tracking` (Scotland Yard) — множина можливих позицій.
  - `+team-vs-team-secret` «Дві команди, склад яких прихований» · game-logic/players · 📎.
  - `+role-abilities-once` «Здібність ролі раз за гру» · entities/state · 🌱.

## Пропозиції до словників
- `+effect:secret_move` — рух, відомий лише гравцю (запис у журнал).
- `+effect:announce` — гравець оголошує координати/подію вголос (правдиво чи ні, за правилом).
- `+effect:draw_card` — витягнути карту з колоди подій.
- `+effect:reveal_identity` — розкрити приховану роль (не позицію).
- `+trigger:attack` — гравець оголосив атаку по сектору.
- `+cond:identity` — прихована роль гравця (human / alien).
- `+role:character-card` — картка ролі зі здібністю.
- `+ui:movement-record` — журнал координат за ходами.
- `+ui:noise-log` — публічна стрічка оголошень усіх гравців.
- `+ui:hand-cards` — закриті карти перед гравцем (тиша, предмети).
- `+window:role-screen` — показ секретної ролі власнику.
- `+window:movement-sheet` — журнал ходів на весь екран.
- `+feature:map-editor-web` — онлайн-редактор карт і сценаріїв поза грою.

## Джерела
- ⭐ [Rulebook Ultimate Edition (Osprey, PDF)](https://www.ospreypublishing.com/media/fssckwfb/efa-rulebook-for-web.pdf) — склад (16 персонажів, 5 капсул, 77 карт сектора, з них 17 предметів, 8 карт), сетап, зони, типи секторів, рух, оголошення, атака, живлення, 9 предметів, усі здібності персонажів, капсули, 40 ходів, умови перемоги; автори Mario Porpora, Pietro Righi Riva, Luca Francesco Rossi, Nicolò Tedeschi.
- [RulesPal: конспект правил](https://rulespal.com/escape-from-the-aliens-in-outer-space/rulebook) — попереднє видання: 39 раундів, базова/розширена гра, 6 предметів, ліміт 3, люки, сценарії, до 16 гравців.
- [eftaios.com](https://www.eftaios.com/) — редактор карт і сценаріїв, правила, видання (Standard, Limited, Ultimate).
- YouTube: пошук «Escape from the Aliens in Outer Space how to play».

## Непевне
- (?) Рік першого видання 2010 — з черги; у джерелах підтверджено лише © 2016 для Ultimate Edition.
- (?) Розміри гекс-карт: координати Galilei на прикладі — A…W × 01…14, але чи такий розмір для всіх зон — не перевіряв.
- (?) Склад колоди: 77 карт небезпечного сектора, з них 17 предметів; скільки «шуму в моєму», «шуму будь-де» й тиші — не сказано.
- (?) Скільки з 5 карт капсул зелені й скільки червоні.
- (?) Офіційні цифрові версії — не бачив; усі вікна «(цифрова версія)».
- (?) RulesPal: у сценарії/старому виданні «люди й чужі можуть виграти разом, якщо вбито останню людину» — у Ultimate це так само записано для людей, що втекли.
