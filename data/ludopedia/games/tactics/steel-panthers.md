---
title: Steel Panthers
slug: steel-panthers
aka: [SP, SP1, "Steel Panthers II: Modern Battles", "Steel Panthers III: Brigade Command", "Steel Panthers: World at War", SPWaW, WinSPWW2, WinSPMBT]
family: tactics
also: []
klass: figure
axes:
  field: hex
  time: turn
  opponent: ai
  info: hidden
  random: runtime
  goal: score
year: 1995
platforms: [DOS, Windows, Mac]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Steel_Panthers", best: true, note: "серія: гекс-оверлей на мапі, окремі танки й відділення 8–12 осіб, генератори битв і кампаній, купівля підкріплень за очки, hotseat/PBEM/AI"}
  - {kind: other, url: "https://discmaster.textfiles.com/view/24001/1996-01_Disc_14.iso/steel/readme.txt", note: "readme демо 1995: постріли за хід, бонус за рух ≤1 гекс, броня за сторонами, поворот на загрозу ближче 2 гексів, придушення й піннінг, rout/rally, досвід за діапазонами, 21 прапор-ціль, рахунок 10:1 / 2:1"}
  - {kind: other, url: "https://www.grognard.com/reviews/sprev.txt", note: "огляд: 1 танк = 1 юніт, 24 core-юніти кампанії, засідки прихованих, дим, артилерія за мапою, авіаудари по своїх, міни, руйнування будинків, ціни в очках"}
  - {kind: other, url: "https://nodicenoglory.com/steel-panthers-series-retrospective-part-one/", note: "ретроспектива серії: броня за напрямком, постріли за хід, 62 сценарії, 7 кампаній, генератори"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Steel+Panthers+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [hp-damage, projectile-shot, line-of-sight-attack, fog-of-war, orientation-state, melee-vs-ranged, destructible-blocks, environment-death, ai-opponent, hot-seat, async-multiplayer, difficulty-levels, game-settings, sequential-levels, shop-between-levels, unit-xp-skills, in-game-editor, placement-screen, codex-window, time-out, event-points, reinforcements, message-log, +hex-grid-render, +armor-by-facing, +opportunity-fire, +shots-per-turn, +suppression-pin, +morale-states, +rout-rally, +leader-ratings, +hidden-ambush, +spotting-by-movement, +indirect-fire, +smoke-screen, +friendly-fire, +minefield, +objective-flags, +victory-ratio, +core-army-carryover, +branching-campaign, +battle-generator, +point-buy-army, +stack-units-in-cell, +surrender]
proposes: ["+trigger:enemy_moved", "+trigger:spotted", "+trigger:attacked", "+cond:moved_this_turn", "+cond:suppression", "+cond:facing_side", "+effect:suppress", "+effect:rally", "+effect:rout", "+effect:interrupt", "+role:objective-flag", "+role:leader", "+ui:unit-roster-table", "+ui:suppression-value", "+window:purchase-units", "+window:battle-generator", "+window:bombardment", "+feature:pbem"]
author: opus
date: 2026-11-09
---

# Steel Panthers — тактичний варгейм на гексах, де кожен танк окремий: броня за стороною, постріли за хід, придушення і засідки з прихованих позицій

## Суть
Гравець командує батальйоном (або ротою, полком) 1930–2025 рр. **до окремого танка й відділення**: на гекс-оверлеї мапи танки, гармати, піхота, артилерія за мапою і авіація. Хід — кожен юніт рухається і робить **кілька пострілів**, кількість яких залежить від екіпажу, досвіду, лідера і придушення. **Броня різна з різних боків**, тож у лоб «Тигр» не пробити — треба заходити з флангу чи тилу; ворожий танк, якого підпустили ближче двох гексів, розвертається до загрози. Ті, хто не рухався, лишаються **прихованими** і бʼють з засідки; хто рухається на очах, наражається на зустрічний вогонь. Результат — співвідношення очок за прапори-цілі і втрати.

## Поле і час
- Мапа — місцевість (ліс, поле, будинки, річки, бокаж, траншеї, окопи, доти) з гексагональним оверлеєм; масштаб гекса — десятки метрів (?).
- Хід поперемінний: сторона рухає й стріляє юнітами в будь-якому порядку; ліміт ходів сценарію (зустрічний бій — зазвичай 10–20).
- Видимість: ворожий юніт показано, лише коли його помітили; рух робить юніт помітнішим; дим блокує огляд; складність впливає на автоматичне виявлення сусідів, що стріляли.
- В одному гексі — до двох юнітів (Shift+клік).
- Випадковість: влучання, пробиття, втрати, перевірки моралі.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Танк / САУ / бронемашина | piece | броня спереду/збоку/ззаду (корпус і башта), гармата, швидкість, екіпаж, досвід, мораль | рух, постріли за хід; знерухомлений при Speed 0; може бути покинутий (AB) |
| Відділення піхоти | piece | 8–12 осіб, зброя, досвід, мораль, придушення | стріляє, бʼє впритул (close assault), відступає до 3 гексів, кидає дим |
| Інженери | piece | — | знімають міни й драконові зуби за кілька ходів |
| Снайпер | piece | 1 особа | окремий юніт |
| Гармата (ПТ, польова) | piece | обслуга | стріляє, буксирується |
| Командир / штаб | piece | рейтинги rally, armor, infantry, artillery | збирає тих, хто тікає; від нього залежать постріли |
| Артилерія за мапою | ally | калібр, час на заряджання | удар по гексу: фугас, дим, контрбатарейний вогонь |
| Авіаудар | ally | — | по цільовому району, може зачепити своїх |
| Баржа / транспорт | object | місткість | піхота сідає й висідає (висадка — 1 постріл) |
| Прапор-ціль | zone | очки, власник | утримання дає очки; у гексі можна скласти кілька |
| Мінне поле | hazard | щільність | шкодить тому, хто входить; знімається інженерами |
| Драконові зуби | static | — | непрохідні для танків до розчищення |
| Будинок | terrain | захист, міцність | руйнується артилерією і танковим вогнем |
| Дим | terrain | легкий / густий | блокує огляд (крізь легкий — видно сусіда) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, u, hex)` → ЯКЩО `not custom: «u уже рухався цього ходу»` and `not state(u, routed|retreating|pinned)` → ТО `move(u, hex)` за ціною ландшафту.
- КОЛИ `turn_end(side)` → ЯКЩО `custom: «u рухався не більше 1 гекса»` → ТО `set_state(u, defensive_bonus)`.
- КОЛИ `turn_start(side)` → ТО `custom: «постріли = f(тип юніта, розмір екіпажу, стан, досвід, лідерство)»`; ЯКЩО `state(u, pinned)` → ТО менше.
- КОЛИ `input(fire, u, hex)` → ЯКЩО `line_of_sight(u, hex)` and `counter(shots, >, 0)` → ТО `counter(shots, −1)`; ЯКЩО `prob(hit)` (менше, якщо стрілець рухався) → ТО `custom: «перевірка пробиття броні тієї сторони, куди влучили»` → `damage` / `custom: «KO, знерухомлено, зброю зруйновано»`.
- КОЛИ `in_range(enemy_tank, u, 2)` → ТО `face(enemy_tank, u)` — заходити в тил треба з ~3 гексів.
- КОЛИ `custom: «ворог рухається в полі зору»` → ЯКЩО `counter(shots, >, 0)` → ТО `custom: «opportunity fire: постріл у чужий хід»` (ПТ-обслуга може змарнувати набої).
- КОЛИ `custom: «юніт під вогнем»` → ТО `counter(suppression, +n)`; КОЛИ `custom: «придушення високе»` → ТО `set_state(u, pinned)`, далі `set_state(u, retreating)` → `set_state(u, routed)`.
- КОЛИ `state(u, routed)` → ТО `custom: «юніт рухає компʼютер, доки не зібраний»`.
- КОЛИ `custom: «командир поруч, rally-перевірка»` → ЯКЩО `prob(rally)` → ТО `clear_state(u, routed)` → «positioned»; піхоті менше половини — важко зібрати при придушенні ≥ 10.
- КОЛИ `custom: «поруч горить танк / втрати / нема лідера»` → ТО `custom: «pinned може триматися до кінця сценарію»`.
- КОЛИ `input(fire, u, t)` → ЯКЩО `adjacent(u, t)` and `custom: «ціль зламана»` → ТО `custom: «ціль здається»`; японська піхота і морпіхи США не здаються, японська піхота не тікає.
- КОЛИ `input(close_assault, inf, vehicle)` → ЯКЩО `custom: «на машині десант»` → ТО `custom: «удар приймає десант»`.
- КОЛИ `custom: «юніт не рухався й не стріляв»` → ТО `set_state(u, hidden)`; КОЛИ `custom: «стріляє або рухається на відкритому»` → ТО `reveal(u)`; на Easy/Average сусід, що стріляв по тобі, виявляється автоматично, на Hard — ні.
- КОЛИ `input(bombard, battery, hex)` → ТО `custom: «удар за затримкою; дим / фугас / контрбатарейний»`; КОЛИ `custom: «близький розрив біля машини»` → ЯКЩО `prob(shock)` → ТО `set_state(vehicle, immobilized)`.
- КОЛИ `input(airstrike, hex)` → ТО `explode(area)`; ЯКЩО `occupied(area, own)` або `custom: «густий дим»` → ТО може влучити по своїх.
- КОЛИ `custom: «піхота відходить»` → ЯКЩО `has(inf, smoke)` → ТО `custom: «автоматично ставить дим»`.
- КОЛИ `enter(u, minefield)` → ТО `damage(u, n)`; КОЛИ `input(clear, engineers)` → ТО `counter(mines, −n)`.
- КОЛИ `custom: «будинок отримав досить шкоди»` → ТО `set_cell(building, rubble)`.
- КОЛИ `custom: «юніт вижив у бою»` → ТО `counter(xp, +n)`; Green < 50, Average 50–79, Veteran 80–100, Elite > 100; зелені ростуть швидше.
- КОЛИ `level_end` → ТО `custom: «очки = прапори-цілі у власності + втрати ворога»`; ЯКЩО `custom: «≥ 10× очок суперника»` → ТО `custom: «decisive victory»`; ≥ 2× — marginal; між 2:1 і 1:2 — `draw`.
- Перемога: співвідношення очок · Поразка: те саме для суперника · Рахунок: VP за прапори й втрати.

## Керування і ввід
- Миша: клік юніта → клік гекса (рух) / ПКМ або кнопка вогню по видимому ворогу; Shift+клік — другий юніт у гекс.
- Режим формування («All Formation») рухає формування разом; undo в ньому не працює; у звичайному русі undo є (?).
- Кнопки: Load/Unload («L»), Bombard (меню артилерії), Smoke on/off (CLR), Show Units, кінець ходу.
- Розстановка: Auto / Select / Manual; «A» — розставити все формування; Shift — не переходити до наступного юніта.

## Вікна, меню, HUD
- `main-menu`: Scenario (62 готові), Campaign (7 готових, гілкові чи лінійні), Battle Generator, Long Campaign, Editor, Load, Options.
- `+window:battle-generator` (`match-setup`): тип бою (атака / оборона / зустрічний), країна, рік, ландшафт, розстановка обох сторін / своєї / автоматично.
- `+window:purchase-units` (`shop-window`): формування за очками (5 Шерманів — 50, 4 Тигри — 120, піхота 5–20, артилерія 50–100); Delete, Mission (мета бою).
- `placement-screen` — розстановка в своїй зоні.
- `game-screen`: гекс-мапа, вікно юніта (екіпаж, броня, постріли, придушення, досвід, мораль), `message-log` пострілів і пробиттів.
- `+window:bombardment` — список батарей і авіації (по 20 на сторінку), кнопка «Eye» — дані юніта.
- `+ui:unit-roster-table` (Show Units): ID, Name, Status, Move, Shots, Sup, HE, AP, Dam, Exp, Mor; позначки H, KO, IM, AB.
- `codex-window` — енциклопедія машин і літаків доступних у періоді.
- `settings-window`: realism-налаштування, рівень повідомлень Low/Medium/High, звук; складність (впливає лише на гравця).
- `editor-window` — редактор сценаріїв: мапа, юніти, рейтинги лідерів, мораль, прапори-цілі (21 у 3 групах по 7, мінімум 1).
- `end-screen`: рівень перемоги, очки, втрати; у кампанії — поповнення.

## Фічі поза полем
- Кампанії: коротка 4–6 боїв (задані), довга 20–30 (генерується); **24 core-юніти** переходять між боями, набирають досвід, ремонтуються, поповнюються, модернізуються; support points — на підкріплення перед боєм; поразка не завжди кінець.
- `hotseat`, `+feature:pbem` (гра поштою), AI проти AI (спостерігати); `ai-opponent-levels`.
- `level-editor` + генератор битв і кампаній; `custom-rules` (realism-перемикачі).

## Варіації й родичі
- Steel Panthers II: Modern Battles (1996), III: Brigade Command (1997, взводи замість окремих машин), SP: World at War (2000, Matrix, безкоштовна), WinSPWW2 і WinSPMBT (оновлюються досі).
- Родичі в корпусі: [Panzer General](panzer-general.md) (операційний масштаб, сила 10), [Unity of Command](unity-of-command.md) (постачання), [Silent Storm](silent-storm.md), [XCOM](xcom.md) (фланг як обхід укриття).
- Відмінності від [Panzer General](panzer-general.md): 1 фішка = 1 машина / відділення; броня за сторонами і пробиття замість «атака/захист за типом»; постріли за хід; придушення → піннінг → втеча з ралі командирами; приховані юніти й зустрічний вогонь; результат — співвідношення VP.
- **Осі варіацій**: броня — одна (PG) / за стороною (SP, Into the Breach — ні) / за стороною і частиною (башта/корпус) · реакція — нема (PG) / opportunity fire (SP, Laser Squad) / overwatch (XCOM) · мораль — нема / придушення-піннінг-втеча (SP) / паніка (XCOM).

## Цікавинки для курсу
- Броня за стороною + поворот ворожого танка до загрози ближче 2 гексів — 📎 (кут між напрямком і вектором удару на гексах).
- Придушення як лічильник із порогами pinned → retreat → rout і ралі лідером — 📎.
- Приховані юніти, що розкриваються пострілом/рухом, і зустрічний вогонь — 🥉.
- Постріли за хід як функція екіпажу, досвіду і лідера — 🌱.
- Рахунок за співвідношенням очок (10:1, 2:1, нічия) — 🌱.
- Генератор битв: ландшафт за театром і роком, бюджет очок на закупівлю — 🥈.
- Авіаудар і артилерія з затримкою та дружнім вогнем — 📎.

## Мапа на каталог
- Є: `hp-damage` · `projectile-shot` · `line-of-sight-attack` · `fog-of-war` · `orientation-state` ↔ напрямок машини · `melee-vs-ranged` ↔ close assault · `destructible-blocks` ↔ будинки · `environment-death` ↔ міни · `ai-opponent` · `hot-seat` · `async-multiplayer` ↔ PBEM · `difficulty-levels` · `game-settings` · `sequential-levels` ↔ кампанії · `shop-between-levels` ↔ закупівля · `unit-xp-skills` · `in-game-editor` · `placement-screen` · `codex-window` · `time-out` ↔ ліміт ходів · `event-points` ↔ VP · `reinforcements` · `message-log`.
- **Нема** → пропозиції карток:
  - `+hex-grid-render`, `+morale-states`, `+friendly-fire`, `+core-army-carryover`, `+branching-campaign`, `+stack-units-in-cell` — уже в корпусі.
  - `+armor-by-facing` «Броня за стороною удару» · entities/combat · 🌱 (з Laser Squad).
  - `+opportunity-fire` «Постріл по рухомому ворогу в чужий хід» · entities/combat · 🥉.
  - `+shots-per-turn` «Кількість пострілів від екіпажу/досвіду/лідера» · entities/state · 🌱.
  - `+suppression-pin` «Придушення → піннінг → відступ» · entities/state · 📎 · слот {thresholds}.
  - `+rout-rally` «Тікає під AI, доки командир не збере» · entities/ai · 📎.
  - `+leader-ratings` «Командир впливає на постріли й ралі» · entities/state · 📎.
  - `+hidden-ambush` «Нерухомий юніт прихований до пострілу» · interface/render · 📎.
  - `+spotting-by-movement` «Рух робить помітнішим» · interface/render · 🌱.
  - `+indirect-fire` «Удар по гексу без лінії видимості, з затримкою» · entities/combat · 📎.
  - `+smoke-screen` «Дим блокує огляд» · entities/state · 🌱.
  - `+minefield` «Мінне поле і розмінування» · entities/interact · 🌱.
  - `+objective-flags` «Прапори-цілі з очками» · game-logic/win · 🌱.
  - `+victory-ratio` «Рівень перемоги за співвідношенням очок» · game-logic/win · 🌱.
  - `+battle-generator` «Генератор битви за театром/роком/типом» · levels/generation · 🥈.
  - `+point-buy-army` «Закупівля армії на бюджет очок» · game-logic/economy · 📎.
  - `+surrender` «Зламаний юніт здається від пострілу впритул» · entities/combat · 🌱.

## Пропозиції до словників
- `+trigger:enemy_moved` — ворог рухається в полі зору (opportunity fire); `+trigger:spotted` — юніт помічено; `+trigger:attacked` — юніт під вогнем (придушення).
- `+cond:moved_this_turn` — рухався цього ходу; `+cond:suppression` — рівень придушення; `+cond:facing_side` — з якої сторони прийшов удар (front/side/rear).
- `+effect:suppress` — додати придушення; `+effect:rally` — зібрати; `+effect:rout` — перевести у втечу; `+effect:interrupt` — постріл у чужий хід.
- `+role:objective-flag` — ціль з очками; `+role:leader` — командир-модифікатор.
- `+ui:unit-roster-table` — таблиця всіх юнітів зі станами; `+ui:suppression-value`.
- `+window:purchase-units`, `+window:battle-generator`, `+window:bombardment`.
- `+feature:pbem` — гра поштою (обмін файлами ходу).

## Джерела
- ⭐ [Wikipedia: Steel Panthers (серія)](https://en.wikipedia.org/wiki/Steel_Panthers) — масштаб юнітів, генератори битв і кампаній, очки на підкріплення, hotseat/PBEM/AI, хронологія серії.
- [Readme демо Steel Panthers (1995)](https://discmaster.textfiles.com/view/24001/1996-01_Disc_14.iso/steel/readme.txt) — рух/бонус за ≤1 гекс, постріли за хід, поворот на загрозу, броня за сторонами, придушення, піннінг, rout/rally, здача, досвід, дим, артилерія, 21 прапор-ціль, рахунок 10:1 / 2:1, кнопки й таблиця Show Units.
- [Огляд на grognard.com](https://www.grognard.com/reviews/sprev.txt) — 1 танк = 1 юніт, 24 core-юніти, кампанії 4–6 / 20–30, засідки, дим, авіаудари по своїх, міни, руйнування будинків, ціни.
- [No Dice No Glory: ретроспектива](https://nodicenoglory.com/steel-panthers-series-retrospective-part-one/) — броня за напрямком, дальність за гекс-відстанню, 62 сценарії, 7 кампаній.
- YouTube: пошук «Steel Panthers gameplay».

## Непевне
- (?) Масштаб гекса (50 м?) — у відкритих джерелах не бачив.
- (?) Opportunity fire в оригіналі 1995 описано оглядом побіжно («рух під прицілом провокує постріли навскидку»); формула — ні.
- (?) Пороги придушення для pinned/retreat/rout і точна формула пострілів за хід.
- (?) Undo руху поза режимом формування.
- (?) Опція приховування «hidden fire» — огляд сиквела каже, що SP2 її додав; в оригіналі — засідки за рахунок невиявлення.
