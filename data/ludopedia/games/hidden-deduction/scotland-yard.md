---
title: Scotland Yard (Скотланд-Ярд)
slug: scotland-yard
aka: [Скотланд-Ярд, Mister X, Scotland Yard – Hunting Mister X, Die Jagd nach Mister X]
family: hidden-deduction
also: [board-digital]
klass: hybrid
axes:
  field: graph
  time: turn
  opponent: hotseat
  info: hidden
  random: setup
  goal: survive
year: 1983
platforms: [board (Ravensburger 1983, Milton Bradley), Game Boy (1990), CD-i (1993), PC (Cryo 1998), Nintendo DS (2008), iOS (2012), Android (2015), Steam (2024)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Scotland_Yard_(board_game)", best: true, note: "199 станцій, види транспорту, квитки, чорні квитки, подвійний хід, 5 появ, бобі, умови перемоги, видання й відеоігри"}
  - {kind: other, url: "https://www.ultraboardgames.com/scotland-yard/game-rules.php", note: "правила: квитки детективів 11/8/4, раунди появи 3·8·13·18·24, бобі за кількістю детективів, гра удвох"}
  - {kind: steam, url: "https://store.steampowered.com/app/3073810/", note: "Scotland Yard – Hunting Mister X (BitBarons, 2024): до 6 гравців, туторіал"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=scotland+yard+board+game+how+to+play", note: "пошук; правила"}
stage: v1
coverage: 70
mechanics: [turn-enforcement, hot-seat, ai-opponent, cell-click, legal-move-highlight, reachable-highlight, fog-of-war, move-notation, last-move-highlight, message-log, objective-text, remaining-counter, game-screen, end-screen, main-menu, help-window, tutorial-window, character-select, match-setup, pass-device, rule-variants, online-multiplayer, +hidden-movement, +graph-transport-edges, +ticket-economy, +scheduled-reveal, +belief-set-tracking, +double-move-token, +wildcard-ticket, +team-vs-one]
proposes: ["+effect:secret_move", "+cond:edge_type", "+role:ticket", "+ui:travel-log", "+ui:ticket-board", "+ui:possible-locations", "+window:travel-log-window", "+feature:location-tracker", "+card:hidden-movement", "+card:graph-transport-edges", "+card:ticket-economy", "+card:scheduled-reveal", "+card:belief-set-tracking", "+card:double-move-token", "+card:wildcard-ticket", "+card:team-vs-one"]
author: opus
date: 2026-11-09
---

# Scotland Yard — детективи женуть невидимого Mr. X мапою Лондона: він показується лише в 5 раундах, а між ними видно тільки, яким транспортом він їхав

## Суть
Один гравець — Mr. X, решта — команда детективів. Mr. X таємно записує кожен свій хід у журнал і накриває запис квитком транспорту: детективи бачать **вид транспорту**, але не станцію. У п'ять наперед відомих раундів Mr. X стає на мапу відкрито. Детективи виграють, ставши на його станцію; Mr. X — якщо дотягне до кінця або детективам скінчаться квитки. `klass: hybrid`: Mr. X — **avatar** (одна фішка), детективи — **figure** (команда з 5 фішок і бобі), а ядро — дедукція множини можливих позицій на графі.

## Поле і час
- Граф Лондона: 199 станцій, ребра чотирьох видів — таксі (жовті, усюди, на 1 станцію), автобус (зелені), метро (червоні), пором по Темзі (чорні, лише Mr. X).
- Станцію може займати лише одна фішка; Mr. X не може стати на станцію детектива.
- Раунд: спершу ходить Mr. X (таємно), потім кожен детектив. Кількість раундів обмежена журналом (див. «Непевне»).
- Видимість односторонньо прихована: Mr. X бачить усе, детективи — лише записи квитків і точку останньої появи.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Mr. X | player | позиція прихована | щораунду таємно ходить ребром, що відповідає квитку; з'являється в раунди появи |
| Детектив | piece | ×5 (MB-версія завжди 5); 11 таксі, 8 автобус, 4 метро | хід = віддати квиток і проїхати ребро цього виду на вільну станцію |
| Бобі (Bobby) | ally | ≤2, кільце на фішці | ходить без квитків; ходи вирішує команда детективів |
| Станція | static | 199, номер | вузол графа; має набір видів транспорту |
| Ребро таксі / автобуса / метро | terrain | вид | зʼєднання станцій; хід лише квитком того ж виду |
| Ребро порому | terrain | Темза, Greenwich ↔ Whitehall | лише Mr. X і лише чорним квитком |
| Квиток таксі / автобуса / метро | supply | лічильник у гравця | витрачається на хід; детективські переходять до Mr. X (класика) |
| Чорний квиток | supply | 5 у Mr. X | будь-який вид транспорту, ховає вид; єдиний доступ до порому |
| Подвійний хід | supply | 2 у Mr. X (у коробці 3) | два ходи за раунд, кожен — окремий запис і квиток |
| Журнал Mr. X | zone | рядок на раунд; вікна появи іншої форми | таємні номери станцій, накриті квитками |
| Стартова карта | supply | 29 карт (2013), окремо D і X | випадкові стартові станції; Mr. X свою не ставить |

## Правила (КОЛИ → ЯКЩО → ТО)
- Старт: КОЛИ `game_start` → ТО `custom: «кожен тягне стартову карту»`; детективи — `place(detective, start)`; Mr. X лише запамʼятовує свою станцію.
- КОЛИ `input(ticket, to)` → ЯКЩО `turn_of(mr_x)` і `has(mr_x, ticket)` і `custom: «з поточної станції є ребро виду квитка до to»` і `free(to)` → ТО `custom: «записати to у журнал і накрити квитком»`, `move(mr_x, to)` приховано.
- КОЛИ `input(black_ticket, to)` → ЯКЩО `custom: «будь-яке ребро, зокрема пором»` → ТО хід як вище, вид транспорту прихований.
- КОЛИ `input(double_move)` → ЯКЩО `has(mr_x, double_move)` → ТО `take(mr_x, double_move)`, `extra_move` (два окремі записи, два квитки).
- КОЛИ `schedule([3, 8, 13, 18, 24])` → ТО `reveal(mr_x)`: фішка стає на станцію відкрито (за ultraboardgames).
- КОЛИ `input(ticket, to)` → ЯКЩО `turn_of(detective)` і `has(detective, ticket)` і `custom: «ребро виду квитка до to»` і `free(to)` → ТО `move(detective, to)`, `give(mr_x, ticket)` (класика; в одній редакції — у загальний запас).
- КОЛИ `input(move, bobby, to)` → ЯКЩО `turn_of(detectives)` і `free(to)` → ТО `move(bobby, to)` без квитка.
- КОЛИ `contact(detective|bobby, mr_x)` → ТО `win` (детективи).
- КОЛИ `turn_start(mr_x)` → ЯКЩО `no_moves(mr_x)` (усі сусідні станції зайняті) → ТО `lose` (Mr. X).
- КОЛИ `custom: «кінець останнього раунду журналу»` → ТО `win` (Mr. X).
- КОЛИ `turn_start(detectives)` → ЯКЩО `no_moves(detectives)` (нема квитків або застрягли) → ТО `win` (Mr. X).
- Детективи не обмінюються квитками.
- Гра удвох: один детектив веде дві фішки зі спільним запасом (20 / 16 / 8) і двох бобі.
- Перемога детективів: зловити · Перемога Mr. X: вижити до кінця журналу / детективи без ходу · Рахунок: нема (у «Die Jagd nach Mister X» — очки за роль Mr. X по черзі).

## Керування і ввід
- Mr. X (настолка): таємно пише номер станції в журнал і кладе зверху квиток; на появі ставить фішку.
- Детективи — радяться і по черзі віддають квиток та ставлять фішку; бобі ходять за спільним рішенням.
- Цифрова версія: клік по фішці → підсвітка станцій, досяжних кожним видом квитка → вибір квитка і станції. Для Mr. X — окремий прихований хід із передачею пристрою, якщо гравці за одним екраном.

## Вікна, меню, HUD
- `main-menu` (цифрова версія): Гра → `match-setup`; Туторіал → `tutorial-window`; Правила → `help-window`.
- `match-setup` / `character-select` (цифрова версія): кількість гравців до 6, хто Mr. X (людина/AI), кількість бобі, правила для початківців.
- `game-screen` (цифрова версія): граф Лондона з кольоровими ребрами; фішки детективів; `travel-log` — рядок за раундом: квиток, номер (відкритий лише на появах), позначені раунди появи; `ticket-board` кожного детектива з лічильниками; `turn-indicator`; `objective-text` («ще 4 раунди до появи»); `last-move-highlight` останньої появи; `possible-locations` — підсвітка станцій, де може бути Mr. X (допомога, не з настолки).
- `pass-device` (цифрова версія) — коли за одним екраном ходить Mr. X.
- `end-screen` (цифрова версія): хто виграв, повний маршрут Mr. X на мапі (`replay-window`).
- Переходи: main-menu → match-setup → game-screen ↔ pass-device → end-screen.

## Фічі поза полем
- `custom-rules`: бобі (2 детективи → 2 бобі, 3 → 1, 4 → 0); правила для початківців (Mr. X стартує на 82, 13 ходів, без метро, 1 чорний квиток і 1 подвійний хід); альтернативні правила Munoz і Laget (1986).
- `ai-opponent-levels` (?) — Mr. X або детективи за AI у відеоіграх.
- `tutorial`, `local-multiplayer` (Steam: shared/split screen).

## Варіації й родичі
- Видання: Scotland Yard Tokyo (переважно косметика), Swiss Edition (човни, лижні траси для Mr. X), NY Chase (без передачі квитків; блокпости й вертоліт детективів), Die Jagd nach Mister X (Mr. X прихований лише чорним квитком; ролі по черзі, очки), Alerta Roja (1986).
- Родичі «прихованого руху»: Fury of Dracula, Letters from Whitechapel (?); [Captain Sonar](captain-sonar.md) — дедукція позиції з оголошених напрямків; [Hunt the Wumpus](hunt-the-wumpus.md) — прихована ціль на графі.
- **Осі варіацій**: що видно між появами «вид транспорту / нічого (чорний квиток) / завжди видно»; появи «за розкладом / за подією»; ресурс детективів «скінченні квитки / безкоштовно (бобі)»; передача квитків «до Mr. X / у запас / нема»; поле «граф міста / сітка».

## Цікавинки для курсу
- Множина можливих позицій Mr. X: після кожного квитка — `{сусіди за видом}` від попередньої множини, на появі — одна станція — 🥈 (класичний фільтр переконань на графі).
- Граф з типізованими ребрами як дані (199 вузлів, 4 види ребер) і пошук досяжних станцій за квитком — 📎.
- Квиткова економіка: скінченні квитки детективів, що перетікають до Mr. X — 🌱.
- Розклад появ, подвійний хід і чорний квиток — інструменти Mr. X, кожен окремою картою правил — 🌱 кожен.
- AI за Mr. X: максимізувати розмір множини можливих позицій і відстань від детективів — 🥇.
- AI за детективів: оточити множину можливих позицій (вибір ходів команди) — 🥇; дослідницька межа — 👑.
- Журнал ходів як прихований стан із частковим розкриттям — 📎.

## Мапа на каталог
- Є: `turn-enforcement` + `hot-seat` · `ai-opponent` · `cell-click` + `legal-move-highlight` + `reachable-highlight` (станції за квитком) · `fog-of-war` (позиція Mr. X) · `move-notation` + `message-log` (журнал) · `last-move-highlight` (остання поява) · `objective-text` · `remaining-counter` (квитки) · `game-screen` / `end-screen` / `main-menu` / `help-window` / `tutorial-window` / `character-select` / `match-setup` / `pass-device` · `rule-variants` · `online-multiplayer` (?).
- **Нема** → пропозиції карток:
  - `+hidden-movement` «Прихований рух сутності з записом у журнал» · game-logic/info · 🥉.
  - `+graph-transport-edges` «Граф з типами ребер, хід ребром свого типу» · field/topology · 📎 · слот {edge_types}.
  - `+ticket-economy` «Скінченні квитки на рух, передача супернику» · game-logic/economy · 🌱.
  - `+scheduled-reveal` «Розкриття прихованої сутності за розкладом» · game-logic/info · 🌱 · слот {rounds}.
  - `+belief-set-tracking` «Множина можливих позицій прихованої сутності» · ai/logic · 🥈.
  - `+double-move-token` «Обмежений жетон подвійного ходу» · game-logic/turns · 🌱.
  - `+wildcard-ticket` «Квиток-джокер, що ховає тип ходу» · game-logic/info · 🌱.
  - `+team-vs-one` «Команда проти одного, асиметрія інформації» · game-logic/players · 📎.

## Пропозиції до словників
- `+effect:secret_move` — сутність рухається приховано для інших сторін (запис у журнал).
- `+cond:edge_type` — ребро між станціями має вид, що відповідає квитку.
- `+role:ticket` — одиниця ресурсу руху (ширше за `supply`: тип визначає дозволене ребро).
- `+ui:travel-log` — журнал прихованих ходів з видимими типами і вікнами появи.
- `+ui:ticket-board` — лічильники квитків за видами в кожного гравця.
- `+ui:possible-locations` — підсвітка станцій, де може бути прихована сутність.
- `+window:travel-log-window` — журнал на весь екран (цифрова версія, перегляд маршруту).
- `+feature:location-tracker` — автоматичне обчислення можливих позицій (допомога детективам).

## Джерела
- ⭐ [Wikipedia: Scotland Yard (board game)](https://en.wikipedia.org/wiki/Scotland_Yard_(board_game)) — станції, транспорт, квитки (таблиця видань), чорні квитки, подвійний хід, журнал, 5 появ, бобі, умови перемоги, видання й відеоігри, нагороди (Spiel des Jahres 1983).
- [UltraBoardGames: правила](https://www.ultraboardgames.com/scotland-yard/game-rules.php) — квитки детективів, раунди появи, стартові карти, бобі за кількістю детективів, гра удвох, зайнятість станцій.
- [Steam: Scotland Yard – Hunting Mister X](https://store.steampowered.com/app/3073810/) — цифрова версія 2024 (BitBarons / Markt+Technik).
- YouTube: пошук «scotland yard board game how to play».

## Непевне
- (?) Кількість раундів: ultraboardgames пише і «до 22 раундів», і появу «після 24-го ходу»; класичний журнал — 24 рядки (з памʼяті); Wikipedia числа не дає.
- (?) Куди йдуть квитки детективів: Wikipedia — до Mr. X; ultraboardgames (нова редакція) — у загальний запас, з якого тягне Mr. X.
- (?) Подвійних ходів у Mr. X 2 (сетап) чи 3 (компоненти) — розбіжність у джерелі.
- (?) Як виглядає інтерфейс відеоверсій (журнал, підсвітка можливих позицій) — не бачив; вікна описані як «(цифрова версія)».
- (?) Fury of Dracula / Letters from Whitechapel як родичі — з памʼяті, не перевірено.
