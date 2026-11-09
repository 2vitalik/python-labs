---
title: Gloomhaven
slug: gloomhaven
aka: [Глумхейвен, Gloomhaven Digital, Jaws of the Lion, Frosthaven]
family: tactics
also: [roguelike]
klass: figure
axes:
  field: hex
  time: turn
  opponent: coop
  info: partial
  random: runtime
  goal: state
year: 2017
platforms: [board, PC, Mac]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Gloomhaven", note: "огляд: 1–4 гравці, гекси, 2 карти (верх/низ), колода модифікаторів замість кубиків, легасі-кампанія 95 сценаріїв, видання"}
  - {kind: other, url: "https://www.orderofgamers.com/downloads/Gloomhaven_v1.1.pdf", best: true, note: "rules summary (EOG): раунд, ініціатива, дії, LOS, модифікатори, умови, стихії, ШІ монстрів, відпочинок, виснаження, тайли, кампанія"}
  - {kind: other, url: "https://rules.dized.com/gloomhaven/rule/resting-1/short-rest", note: "Dized: правила відпочинку, ініціатива 99"}
  - {kind: steam, url: "https://store.steampowered.com/app/780290/Gloomhaven/", note: "цифрова версія: кампанія 95 місій, Guildmaster 160+ місій, кооп до 4"}
  - {kind: steam, url: "https://store.steampowered.com/app/1809490/Gloomhaven_Jaws_of_the_Lion/", note: "Jaws of the Lion (цифрова)"}
  - {kind: steam, url: "https://store.steampowered.com/app/2347080/Frosthaven/", note: "Frosthaven (сиквел, цифрова)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Gloomhaven+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [hp-damage, impassable-cells, floor-types, push-object, pull-object, melee-vs-ranged, line-of-sight-attack, explode-area, status-effects, temporary-modes, spawn-points, key-and-door, item-pickup, inventory, inventory-limit, round-currency, shop-between-levels, shop-catalog, unit-xp-skills, destroy-all-enemies, world-map, map-window, ai-opponent, ai-greedy, chase-bfs, difficulty-levels, game-screen, main-menu, end-screen, character-select, save-autosave, online-multiplayer, +deck-draw, +two-card-turn, +card-initiative, +hand-as-stamina, +rest-recover, +lost-cards, +attack-modifier-deck, +advantage-draw-two, +element-infusion, +monster-ability-deck, +monster-focus, +summon-creature, +retaliate-shield, +room-reveal, +legacy-campaign, +retirement-perks, +scenario-level-scaling]
proposes: ["+trigger:round_end", "+trigger:attacked", "+trigger:room_revealed", "+cond:element", "+cond:initiative_order", "+effect:draw_card", "+effect:discard", "+effect:lose_card", "+effect:infuse", "+effect:consume_element", "+effect:recover_cards", "+effect:rest", "+role:summon", "+role:card", "+ui:initiative-track", "+ui:element-board", "+ui:card-halves", "+ui:modifier-reveal", "+window:card-select", "+window:town-screen", "+window:road-event", "+window:enhancement-window", "+window:party-sheet", "+feature:legacy-unlocks", "+feature:scenario-level", "+axis:turn-structure"]
author: opus
date: 2026-11-09
---

# Gloomhaven — кооперативна тактика на гексах: щораунду дві карти (верх однієї + низ іншої), ініціатива з карт, а рука — це і запас сил, і таймер до виснаження

## Суть
1–4 найманці зачищають підземелля на гексах проти монстрів з автоматичним ШІ. Щораунду кожен гравець таємно обирає **2 карти** з руки: одна визначає ініціативу, а на своєму ході він виконує **верхню дію однієї й нижню дію іншої**. Зіграні карти йдуть у скидання, а сильні — назавжди «втрачаються» на сценарій; відпочинок повертає руку ціною однієї карти. Тож рука — це таймер: хто вичерпав карти, той виснажений. Кубиків нема — випадковість дає колода модифікаторів атаки. Навколо — легасі-кампанія з наклейками, конвертами й містом.

## Поле і час
- Гекс-поле з тайлів-кімнат, зʼєднаних дверима; оверлей-тайли: перешкоди, пастки, небезпечна і складна місцевість, скарби, коридори, плити; нові кімнати відкриваються, коли персонаж заходить у двері.
- Раунд: 1) вибір карт (таємно) → 2) розкриття, ініціатива: карта монстрів на кожен тип + провідні карти гравців → ходи від меншої ініціативи до більшої → 3) ходи персонажів і монстрів → 4) кінець раунду: перетасовки, згасання стихій, короткий відпочинок.
- LOS: лінія від будь-якого кута гекса атакувальника до будь-якого кута цілі, не торкаючись стін; блокують лише стіни. Через стіну гекси не сусідні.
- Рівень сценарію 0–7: від рівня партії (середній /2, вгору) ±складність; він задає силу монстрів, шкоду пасток, курс золота, бонусний досвід.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Персонаж (клас) | piece | HP, рука (розмір з планшета), XP, колода модифікаторів, предмети | дві дії на хід з двох карт; урон можна поглинути втратою карт |
| Карта вміння | supply | ініціатива, верхня дія, нижня дія, символи «lost» / активна | грається парою; у скидання / втрачені / активну зону |
| Колода модифікаторів (персонажа / монстрів) | supply | 20 стандартних карт: ±, ×2, null, rolling, shuffle | тягнеться на кожну ціль атаки |
| Монстр звичайний / елітний | enemy | статкарта за рівнем, номер стенді | діє за картою свого типу; еліти першими, далі за номером |
| Карта дій монстрів | supply | ініціатива, дії ±X, іноді shuffle | одна на тип на раунд |
| Бос | boss | окрема статкарта і колода | спецдії, імунітет до частини умов |
| Названий монстр | boss | — | ціль сценарію; не «звичайний / елітний» |
| Призвана істота (summon) | ally | HP, атака, рух | діє перед власником як монстр (Move+0 Attack+0), колодою власника |
| Перешкода | static | можливо HP | блокує звичайний рух, не постріли; з HP — руйнується |
| Пастка | hazard | шкода 2+L або умова | спрацьовує при вході (у т.ч. примусовому), зникає |
| Небезпечна місцевість | hazard | ½ пастки | шкода за кожен вхід, лишається |
| Складна місцевість | terrain | 2 руху | дорожчий звичайний рух |
| Двері | gate | закриті / відкриті / замкнені | персонаж відчиняє входом → відкривається кімната; для монстрів закриті = стіна |
| Коридор, натискна плита | terrain | — | як порожній гекс; плита — спецефект сценарію |
| Монета | pickup | вартість за рівнем | з убитого монстра; збирається в кінці ходу / дією Loot |
| Скарб | pickup | номер | предмет / схема / сценарій з індексу |
| Стихія (вогонь, лід, повітря, земля, світло, темрява) | resource | inert → strong → waning | дія насичує; інша дія споживає для посилення |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(card_selection)` → ТО кожен гравець таємно `choose(2 cards)` і позначає провідну; або оголошує довгий відпочинок (ініціатива 99).
- КОЛИ `phase_start(card_selection)` → ЯКЩО `count(hand, <=, 1)` → ТО обовʼязковий довгий відпочинок; ЯКЩО ще й `count(discard, <=, 1)` → ТО `custom: «виснаження»`.
- КОЛИ `phase_start(initiative)` → ТО `custom: «відкрити карту монстрів на кожен тип на полі»`; порядок — від меншої ініціативи; нічия гравців — за другою картою; гравець і монстр — першим гравець.
- КОЛИ `turn_start(character)` → ТО `custom: «верхня дія однієї карти + нижня дія іншої»`; будь-яку карту можна зіграти як Attack 2 (верх) або Move 2 (низ) у скидання.
- КОЛИ `input(move, figure, cell)` → ЯКЩО `legal(path ≤ X)` → ТО `move(figure, cell)` крізь союзників, не крізь ворогів і перешкоди; не можна завершити на зайнятому гексі.
- КОЛИ `input(move, jump|flying)` → ТО ігнорувати фігури й місцевість (стрибок — крім останнього гекса; політ — і пастки, і перешкоди).
- КОЛИ `enter(figure, trap)` → ЯКЩО `not state(figure, flying|jump)` → ТО `damage(2+L)` або умова, `disappear_b`.
- КОЛИ `enter(figure, hazardous)` → ТО `damage(⌊(2+L)/2⌋)`; КОЛИ `enter(figure, difficult)` → ТО `custom: «2 очки руху»`.
- КОЛИ `enter(character, closed_door)` → ТО `set_cell(door, open)`, `reveal(room)`, `spawn_at(monsters, room)`; монстри з меншою ініціативою, ніж у персонажа, ходять одразу після нього.
- КОЛИ `input(attack, target)` → ЯКЩО `in_range(a, target, r) and line_of_sight(a, target)` → ТО базова атака + бонуси → `custom: «тягнути модифікатор»` → мінус щит цілі → `damage(n)`; дальня атака по сусідові — з disadvantage.
- КОЛИ `custom: «тягнути модифікатор»` → ЯКЩО `custom: «rolling»` → ТО тягнути ще й сумувати; `null` → 0 шкоди; `2x` → ×2; null/2x → перетасувати колоду в кінці раунду.
- КОЛИ `custom: «advantage»` → ТО тягнути 2, брати кращу; disadvantage — гіршу.
- КОЛИ `after(attack, push X)` → ТО `push(target)` на X гексів, кожен — далі від атакувальника; pull — ближче; крізь союзників цілі, не крізь ворогів.
- КОЛИ `after(attack, condition)` → ТО `set_state(target, poison|wound|immobilize|disarm|stun|muddle)` (навіть без шкоди); curse/bless — `custom: «вкласти карту в колоду модифікаторів»`.
- КОЛИ `turn_start(figure)` → ЯКЩО `state(figure, wound)` → ТО `damage(1)`; КОЛИ `input(heal, figure)` → ЯКЩО `state(figure, poison|wound)` → ТО `clear_state(poison, wound)` (при poison лікування більше нічого не робить).
- КОЛИ `turn_end(figure)` → ЯКЩО `state(figure, immobilize|disarm|stun|muddle|invisible|strengthen)` → ТО `clear_state` (тривалість — до кінця наступного ходу).
- КОЛИ `custom: «атака з дією-символом стихії»` → ТО `custom: «стихія → strong у кінці ходу»`; КОЛИ `custom: «дія споживає стихію»` → ЯКЩО `custom: «стихія strong або waning»` → ТО посилення, стихія → inert; створити й спожити в той самий хід не можна.
- КОЛИ `custom: «кінець раунду»` → ТО стихії strong → waning → inert; round-бонуси знімаються; можна короткий відпочинок.
- КОЛИ `custom: «персонажа атакують»` → ЯКЩО `state(target, retaliate) and adjacent(attacker, target)` → ТО `damage(X)` атакувальнику після атаки; shield X зменшує шкоду атаки.
- КОЛИ `custom: «персонаж отримує шкоду»` → ТО `choose(hp | lose 1 карту з руки | lose 2 карти зі скидання)` — втрата карт поглинає всю шкоду, ефекти атаки лишаються.
- КОЛИ `input(short_rest)` → ЯКЩО `count(discard, >=, 2)` → ТО `custom: «випадкова карта скидання → втрачені, решта в руку»`; раз за відпочинок можна `damage(1)` і перетягнути іншу.
- КОЛИ `custom: «довгий відпочинок на ініціативі 99»` → ТО `custom: «обрати 1 карту на втрату, решта в руку»`, `heal(self, 2)`, `custom: «оновити витрачені предмети»`.
- КОЛИ `turn_start(monster)` → ТО `custom: «focus»`: ціль, до якої найкоротший шлях у дальність і LOS атаки; нічия — ближча зараз, далі — раніша в ініціативі; summon-и в пріоритеті над власником.
- КОЛИ `custom: «монстр рухається»` → ТО мінімальний рух для атаки по focus з максимальним ефектом (`chase-bfs`); дальні — відходять, щоб зняти disadvantage; пастки — як перешкоди, якщо є інший шлях.
- КОЛИ `input(summon)` → ЯКЩО `free(adjacent)` → ТО `spawn_at(summon, adjacent)`; діє перед власником, не в раунд призову; зникає з 0 HP або виснаженням власника.
- КОЛИ `hp_zero(monster)` → ТО `disappear_a`, `spawn_at(coin, cell)` (крім призваних).
- КОЛИ `turn_end(character)` → ЯКЩО `occupied(cell, coin|treasure)` → ТО `pickup`.
- КОЛИ `hp_zero(character)` → ТО `custom: «виснаження»`: усі карти втрачені, фігура знімається; КОЛИ `custom: «виснажені всі»` → ТО `lose`.
- КОЛИ `all_constraints_met` → ТО `win` після дограного раунду: XP, золото = монети × курс, бонус XP 4 + 2L, бойові цілі (3 галочки = перк).
- Перемога: умова сценарію (найчастіше вбити всіх / боса) · Поразка: виснажені всі персонажі (або спецумова) · Рахунок: XP, золото, галочки бойових цілей.

## Керування і ввід
- Настільна: карти в руці, таємний вибір пари, фігурки й стенді на гексах, жетони умов і стихій, лічильник HP/XP.
- Цифрова версія: клік по двох картах у руці → кнопка підтвердження; на своєму ході — вибір половини карти, підсвітка гексів руху/атаки, наведення на монстра показує статкарту й намір (?); кнопки довгого/короткого відпочинку.
- Гравці можуть домовлятися про план, але не розкривають точні числа карт (правило настолки).

## Вікна, меню, HUD
- `main-menu` (цифрова): Кампанія · Guildmaster · Мультиплеєр · Налаштування · Вихід.
- `map-window` — карта регіону з наклейками сценаріїв (відкриті / пройдені).
- `custom-window` «Місто» — магазин предметів (`shop-window`), покращення карт (enhancement), храм, рівень і перки, відставка (?).
- `custom-window` «Подія» — міська / дорожня подія: карта з варіантами, результат залежить від класу, репутації, золота.
- `character-select` — найм класу (17 у цифровій), стартова рука до розміру руки.
- `custom-window` «Вибір карт раунду» — рука, дві карти, провідна для ініціативи.
- `game-screen`: гекс-поле; трек ініціативи; дошка стихій (inert/waning/strong); `hp-bar` і XP; `pocket` (рука), скидання, втрачені, активна зона; відкрита карта дій кожного типу монстрів; анімація модифікатора атаки; `tooltip` монстра.
- `end-screen` — підсумок сценарію: XP, золото, бойові цілі, нагороди, відкриті сценарії.
- `upgrade-window` — підвищення рівня: нова карта вміння, перк до колоди модифікаторів.

## Фічі поза полем
- Легасі-кампанія: 95 сценаріїв, наклейки на мапі, конверти й коробки з новими класами, глобальні й партійні досягнення, процвітання міста, репутація партії (−20…20).
- Відставка персонажа за особистою ціллю → відкриває новий клас і нову історію міста (town records).
- Режими: кампанія / casual (будь-який відкритий сценарій без нагород); цифрова — Guildmaster (160+ місій); соло-сценарії DLC.
- `difficulty-presets`: Easy (−1) · Normal · Hard (+1) · Very hard (+2) до рівня сценарію; соло — +1 рівень монстрів.
- `mode-coop` 1–4; цифрова — онлайн-кооп, соло кількома найманцями; `autosave` (?).

## Варіації й родичі
- Forgotten Circles (2019, розширення), Jaws of the Lion (2020, вступна, 25 сценаріїв, 5 навчальних), Frosthaven (сиквел, аванпост), Second Edition (2025), Buttons and Bugs (соло), цифрові версії Flaming Fowl (2019–2021).
- Родичі в корпусі: [heroquest-space-hulk](heroquest-space-hulk.md) (настільний данжен-кроул), [fire-emblem](fire-emblem.md), [xcom](xcom.md); у роглайках — колодо-тактики.
- Поза корпусом: Slay the Spire (рука-колода), Mage Knight (карти = рух/бій), Fights in Tight Spaces (карти на сітці).
- **Осі варіацій**: дія — 2 половини з 2 карт / одна карта / AP · ініціатива — з карти щораунду / фіксована / за швидкістю · випадковість — кубики / колода модифікаторів / нема · «HP» гравця — HP + рука як таймер / лише HP.

## Цікавинки для курсу
- Дві карти на хід: верх однієї + низ іншої, провідна задає ініціативу — 🥉 (вибір пари, валідатор).
- Рука як таймер: скидання → відпочинок (−1 карта) → втрачені → виснаження — 📎 + прекрасна задача на математику ходів.
- Колода модифікаторів замість кубика (null, ×2, rolling, shuffle, bless/curse, advantage = тягни 2) — 🥉.
- Дошка стихій: infuse → strong → waning → inert, спожити для посилення — 📎.
- ШІ монстрів за правилом focus (найкоротший шлях до гекса атаки, тай-брейки) — 🥇 (BFS на гексах з LOS по кутах).
- LOS «кут до кута» на гексах без торкання стін — 🥈.
- Легасі: відкриті конверти, наклейки й постійні зміни світу як збереження кампанії — 🥉.

## Мапа на каталог
- Є: `hp-damage` · `impassable-cells` (стіни, перешкоди) · `floor-types` (пастки, небезпечна, складна) · `push-object` / `pull-object` · `melee-vs-ranged` · `line-of-sight-attack` · `explode-area` (area-атаки) · `status-effects` / `temporary-modes` (умови) · `spawn-points` (спавн сценарію) · `key-and-door` (двері, замкнені двері) · `item-pickup` (монети, скарби) · `inventory` / `inventory-limit` (слоти предметів) · `round-currency` (золото) · `shop-between-levels` / `shop-catalog` · `unit-xp-skills` · `destroy-all-enemies` · `world-map` / `map-window` · `ai-opponent` / `ai-greedy` / `chase-bfs` (ШІ монстрів) · `difficulty-levels` · `character-select` · `online-multiplayer` (цифрова).
- **Нема** → пропозиції карток:
  - `+deck-draw` «Колода / рука / скидання» · entities/state · 🥉.
  - `+two-card-turn` «Хід = верх однієї + низ іншої карти» · game-logic/opponent · 🥉.
  - `+card-initiative` «Ініціатива з обраної карти щораунду» · game-logic/opponent · 📎.
  - `+hand-as-stamina` «Рука як таймер сценарію» · game-logic/lose · 📎.
  - `+rest-recover` «Відпочинок повертає скидання ціною карти» · entities/state · 📎.
  - `+lost-cards` «Сильна дія = карта втрачена до кінця бою» · entities/state · 🌱.
  - `+attack-modifier-deck` «Колода модифікаторів атаки» · entities/combat · 🥉 · {null, x2, rolling}.
  - `+advantage-draw-two` «Перевага: тягни 2, бери кращу» · entities/combat · 🌱.
  - `+element-infusion` «Стихії, що згасають» · game-logic/economy · 📎 · {elements: 6}.
  - `+monster-ability-deck` «Спільна карта дій на тип монстрів» · game-logic/opponent · 📎.
  - `+monster-focus` «Вибір цілі монстром за правилом focus» · game-logic/opponent · 🥇.
  - `+summon-creature` «Призвана істота з автоматичною поведінкою» · entities/spawn · 📎.
  - `+retaliate-shield` «Щит і відплата» · entities/combat · 📎.
  - `+room-reveal` «Кімната відкривається при вході в двері» · levels/generation · 📎.
  - `+legacy-campaign` «Постійні зміни світу кампанії» · levels/progression · 🥉.
  - `+retirement-perks` «Відставка й перки» · levels/progression · 📎.
  - `+scenario-level-scaling` «Рівень сценарію від рівня партії» · game-logic/difficulty · 🌱.

## Пропозиції до словників
- `+trigger:round_end` — кінець раунду (усі сходили): перетасовки, згасання стихій, short rest.
- `+trigger:attacked` — фігуру атакують (retaliate, shield).
- `+trigger:room_revealed` — відкрилась нова кімната (спавн, позачерговий хід монстрів).
- `+cond:element` — стихія в стані strong/waning; `+cond:initiative_order` — хто раніше в черзі.
- `+effect:draw_card`, `+effect:discard`, `+effect:lose_card` — рух карти між рукою, скиданням і «втраченими».
- `+effect:infuse` / `+effect:consume_element` — створити / спожити стихію.
- `+effect:recover_cards` — повернути карти зі скидання/втрачених у руку; `+effect:rest` — відпочинок як дія.
- `+role:summon` — призвана істота гравця з автоматичною поведінкою; `+role:card`.
- `+ui:initiative-track` — черга ходів раунду; `+ui:element-board` — 6 стихій у 3 колонках; `+ui:card-halves` — карта з двома клікабельними половинами; `+ui:modifier-reveal` — показ витягнутого модифікатора.
- `+window:card-select` — таємний вибір 2 карт; `+window:town-screen` — місто між сценаріями; `+window:road-event` — подія з умовними варіантами; `+window:enhancement-window` — наліпки-покращення карт; `+window:party-sheet` — партія, репутація, досягнення.
- `+feature:legacy-unlocks` — незворотні відкриття в кампанії; `+feature:scenario-level` — рівень сценарію 0–7.
- `+axis:turn-structure` — `card-initiative` (порядок щораунду з карт).

## Джерела
- ⭐ [EOG rules summary v1.1](https://www.orderofgamers.com/downloads/Gloomhaven_v1.1.pdf) — повний раунд, дії, LOS, модифікатори, умови, стихії, ШІ монстрів, відпочинок, виснаження, тайли, рівень сценарію, кампанія.
- [Wikipedia](https://en.wikipedia.org/wiki/Gloomhaven) — огляд механіки, видання, цифрова версія, нагороди.
- [Dized: short rest](https://rules.dized.com/gloomhaven/rule/resting-1/short-rest) — відпочинок, ініціатива 99.
- [Steam: Gloomhaven](https://store.steampowered.com/app/780290/Gloomhaven/) — цифрова: 95 місій, Guildmaster, кооп до 4, дати.
- [Steam: Jaws of the Lion](https://store.steampowered.com/app/1809490/Gloomhaven_Jaws_of_the_Lion/) · [Steam: Frosthaven](https://store.steampowered.com/app/2347080/Frosthaven/).
- YouTube: пошук «Gloomhaven gameplay».

## Непевне
- (?) Інтерфейс цифрової версії (кнопки, тултипи намірів, автосейв) — з памʼяті.
- (?) Відставка: що саме відкриває і як працює міський екран у цифровій версії — з памʼяті; правила відставки в зведенні не дочитав.
- (?) Друга редакція (2025) змінює класи й сценарії — деталі не перевіряв.
