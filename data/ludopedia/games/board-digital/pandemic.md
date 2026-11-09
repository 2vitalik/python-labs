---
title: Pandemic
slug: pandemic
aka: [Пандемія, Pandemie]
family: board-digital
also: []
klass: figure
axes:
  field: graph
  time: turn
  opponent: coop
  info: partial
  random: both
  goal: state
year: 2008
platforms: [board, iOS, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pandemic_(board_game)", best: true, note: "огляд: 48 міст, хід, епідемія, спалах і ланцюг, ролі, перемога й поразка, доповнення, Legacy, цифрові версії"}
  - {kind: other, url: "https://rulespal.com/pandemic/rulebook", note: "правила 2-го видання: склад, підготовка, 8 дій, 7 ролей, епідемія, спалахи, викорінення, ліміт руки"}
  - {kind: other, url: "https://www.ultraboardgames.com/pandemic/game-rules.php", note: "правила 1-го видання (5 ролей), стоси з епідеміями, Red lines через край"}
  - {kind: other, url: "https://lehi-innovation.github.io/boardgame-rules/rules/pandemic/", note: "трек темпу інфекції 2-2-2-3-3-4-4, 5 карт подій"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Pandemic+board+game+how+to+play", note: "пошук; пояснення правил"}
stage: v1
coverage: 75
mechanics: [chain-reaction, teleport, wrap-edges, spawn-random-cell, difficulty-levels, character-select, match-setup, game-screen, end-screen, help-window, tutorial-window, +shared-field-coop, +action-points, +variable-player-powers, +deck-draw, +hand-limit, +graph-board, +overflow-spread, +intensify-reshuffle, +epidemic-pile-split, +escalating-draw-count, +doom-track, +set-collection-cure, +discard-to-move, +card-transfer-same-cell, +eradication, +deck-out-lose, +supply-out-lose, +aura-block-placement, +event-cards-any-time]
proposes: ["+effect:spread", "+effect:reshuffle", "+effect:draw_cards", "+effect:discard", "+trigger:deck_empty", "+role:card", "+ui:doom-track", "+ui:card-hand", "+card:overflow-spread", "+card:intensify-reshuffle", "+card:doom-track"]
author: opus
date: 2026-11-09
---

# Pandemic — кооп на графі з 48 міст: четвертий кубик у місті спричиняє спалах у сусідів, і ланцюг може обійти пів світу

## Суть
2–4 гравці — команда фахівців з різними ролями — разом шукають ліки від 4 хвороб, поки ті розповзаються графом міст. Хід: 4 дії (переїзди, лікування, станції, передача карт, ліки), 2 карти гравця, потім «інфектор» — карти інфекції кладуть кубики в міста. Четвертий кубик одного кольору в місті — **спалах**: по кубику в кожне сусіднє місто, що може спричинити нові спалахи; карта «Епідемія» прискорює темп і кладе відіграні міста знову на верх колоди. Автор Matt Leacock, Z-Man Games.

## Поле і час
- Поле — граф (`graph`): 48 міст (по 12 чотирьох кольорів), ребра — лінії сполучення; червоні лінії ведуть через край мапи (Тихий океан) на протилежний бік.
- Шар міста: до 3 кубиків кожного кольору, дослідна станція (так / ні), фішки гравців.
- Хід: 4 дії → взяти 2 карти гравця (з розіграшем «Епідемій») → інфікувати міста (карт = темп інфекції). Хід — за годинниковою стрілкою; першим — той, хто хворів останнім.
- Темп інфекції — трек 2, 2, 2, 3, 3, 4, 4 (крок за кожну епідемію); трек спалахів 0…8.
- Інформація часткова: колоди закриті, але скид інфекції відкритий — гравці знають, які міста повернуться на верх після епідемії.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фахівець | piece | 1 з 7 ролей; стартує в Атланті | 4 дії на хід + вміння ролі |
| Лікар (Medic) | piece | — | «лікувати» знімає всі кубики кольору; кубики вилікуваної хвороби знімаються самі там, де він є, і не кладуться в його місто |
| Науковець (Scientist) | piece | — | ліки за 4 карти кольору замість 5 |
| Дослідник (Researcher) | piece | — | передає будь-яку карту міста гравцеві в своєму місті |
| Диспетчер (Dispatcher) | piece | — | дією переміщує будь-яку фішку до міста з іншою фішкою або рухає чужу як свою (зі згоди) |
| Операційний експерт | piece | — | будує станцію без карти; раз на хід — зі станції в будь-яке місто за будь-яку карту міста |
| Планувальник (Contingency Planner) | piece | 1 слот на ролі | дією бере карту події зі скиду на роль; зіграна звідти — з гри |
| Спеціаліст із карантину | piece | — | у його місті й усіх сусідніх кубики не кладуться й спалахів нема |
| Місто | zone | колір, сусіди, ≤3 кубики кольору | вузол графа; 4-й кубик → спалах |
| Кубик хвороби | hazard | 24 кожного з 4 кольорів | кладеться інфекцією; нестача в запасі — поразка |
| Дослідна станція | static | 6; перша в Атланті | місце ліків; вузол «шатлу» |
| Карта міста | card | 48 | квиток (пряма / чартерна), будування станції, ліки (5 одного кольору) |
| Карта події | card | 5 | граються будь-коли, без дії |
| Карта «Епідемія» | card | 6 (у грі 4/5/6) | прискорення, інфекція з низу, перетасування скиду на верх |
| Карта інфекції | card | 48 (по місту) | 1 кубик кольору міста; скид відкритий |
| Маркер ліків | mark | 4: знайдено / викорінено | стан хвороби |
| Трек темпу інфекції | supply | 2-2-2-3-3-4-4 | скільки карт інфекції тягнути |
| Трек спалахів | supply | 0…8 | 8-й спалах — поразка |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «3 карти інфекції — по 3 кубики, 3 — по 2, 3 — по 1»`; роздати карти гравця (2 гравці — по 4, 3 — по 3, 4 — по 2); `custom: «решту колоди поділити на 4/5/6 стосів, у кожен — 1 «Епідемію», менші стоси вниз»`.
- КОЛИ `input(drive(city))` → ЯКЩО `custom: «місто сполучене лінією з поточним»` → ТО `move(pawn, city)` (`wrap` по червоних лініях).
- КОЛИ `input(direct_flight(city))` → ЯКЩО `has(player, card[city])` → ТО `custom: «скинути карту»` (`+effect:discard`), `teleport(pawn, city)`.
- КОЛИ `input(charter_flight(city))` → ЯКЩО `has(player, card[current_city])` → ТО `custom: «скинути карту поточного міста»`, `teleport(pawn, any_city)`.
- КОЛИ `input(shuttle(city))` → ЯКЩО `occupied(here, station)` і `occupied(city, station)` → ТО `teleport(pawn, city)`.
- КОЛИ `input(build_station)` → ЯКЩО `has(player, card[here])` (Операційний — без карти) → ТО `place(player, station)`; ЯКЩО `count(station_supply, ==, 0)` → ТО `custom: «перенести станцію з іншого міста»`.
- КОЛИ `input(treat(color))` → ЯКЩО `occupied(here, cube[color])` → ТО `disappear(cube[color] ×1)`; ЯКЩО `state(disease[color], cured)` або `state(pawn, medic)` → ТО `disappear(all cube[color] here)`.
- КОЛИ `input(share(card, other))` → ЯКЩО `occupied(here, other)` і `same(card, here, city)` (Дослідник — будь-яку при передачі) → ТО `give(other, card)` за 1 дію, обидва згодні.
- КОЛИ `input(discover_cure(color))` → ЯКЩО `occupied(here, station)` і `has(player, card[color] ×5)` (Науковець — ×4) → ТО `custom: «скинути карти»`, `set_state(disease[color], cured)`.
- КОЛИ `after(cure)` або `after(treat)` → ЯКЩО `state(disease[color], cured)` і `count(cube[color] on_board, ==, 0)` → ТО `set_state(disease[color], eradicated)`.
- КОЛИ `phase_start(draw)` → ТО `custom: «взяти 2 карти гравця»` (`+effect:draw_cards`); ЯКЩО `count(player_deck, <, 2)` → ТО `lose`.
- КОЛИ `after(draw_cards)` → ЯКЩО `counter(hand, >, 7)` → ТО `custom: «скинути або зіграти події до 7»` — діє одразу, і після передачі карти.
- КОЛИ `custom: «взято «Епідемію»»` → ТО `counter(infection_rate, +1 step)`; `custom: «нижня карта інфекції — 3 кубики в місто»`; `custom: «перетасувати скид інфекції й покласти на верх колоди»` (`+effect:reshuffle`); карта «Епідемія» — з гри.
- КОЛИ `phase_start(infect)` → ТО `custom: «тягнути карти інфекції = темп; по 1 кубику кольору в місто з карти»` = `spawn_at(cube[color], city)`.
- КОЛИ `spawned(cube[color])` → ЯКЩО `state(disease[color], eradicated)` → ТО `block` (кубик не кладеться).
- КОЛИ `spawned(cube[color])` → ЯКЩО `custom: «місто — Спеціаліста з карантину або сусіднє з ним»` або (`occupied(city, medic)` і `state(disease[color], cured)`) → ТО `block`.
- КОЛИ `spawned(cube[color])` → ЯКЩО `count(cube[color]@city, >, 3)` → ТО `custom: «4-й не кладеться — спалах»`, `counter(outbreaks, +1)`, `custom: «по 1 кубику кольору в кожне сусіднє місто»` (`+effect:spread`).
- КОЛИ `after(spread)` → ЯКЩО `count(cube[color]@neighbor, >, 3)` і `not state(neighbor, outbroke_this_chain)` → ТО ланцюговий спалах у сусіді; кожне місто спалахує не більше 1 разу за одну карту інфекції.
- КОЛИ `counter(outbreaks, ==, 8)` → ТО `lose`.
- КОЛИ `custom: «треба покласти кубик кольору, а в запасі нема»` → ТО `lose`.
- КОЛИ `input(play_event(e))` → ЯКЩО `custom: «не між взяттям і розіграшем карти»` → ТО ефект без дії: Airlift — `teleport(any_pawn, any_city)` · One Quiet Night — `custom: «пропустити наступну фазу інфекції (не епідемії)»` · Resilient Population — `disappear(one_infection_discard)` · Government Grant — `place(station, any_city)` · Forecast — `custom: «переглянути й переставити 6 верхніх карт інфекції»`.
- КОЛИ `input(take_event)` → ЯКЩО `state(pawn, contingency_planner)` і `custom: «слот ролі порожній»` → ТО `pickup(planner, event_from_discard)`.
- КОЛИ `input(dispatch(pawn_b, city))` → ЯКЩО `state(pawn, dispatcher)` і `occupied(city, any_pawn)` → ТО `teleport(pawn_b, city)` за 1 дію.
- КОЛИ `counter(cures, ==, 4)` → ТО `win` — викорінювати не обовʼязково.
- Перемога: 4 ліки · Поразка: 8 спалахів / нестача кубиків / нема 2 карт гравця в колоді · Рахунок: нема.

## Керування і ввід
- Настільна: активний гравець витрачає 4 дії (переїзд, 3 види перельотів, станція, лікування, передача карти, ліки; можна «пас»); події — будь-хто будь-коли.
- Кооп: обговорення відкрите, карти гравців можна показувати; рішення — за активним гравцем.
- (цифрова версія) Тап по місту → доступні способи руху з ціною в картах (`path-preview`); перетяг карти на гравця — передача; кнопки дій ролі; кнопка завершення дій запускає взяття карт і анімацію інфекції / ланцюга спалахів.

## Вікна, меню, HUD
(цифрова версія: Asmodee Digital, iOS 2013, Steam)
- `main-menu`: Нова гра · Навчання · Правила · Налаштування.
- `match-setup`: 2–4 ролі, складність Introductory / Standard / Heroic (4/5/6 епідемій).
- `character-select`: 7 ролей з описами.
- `game-screen`: мапа-граф міст з кубиками й станціями; `doom-track` спалахів (0…8) і темпу інфекції; маркери 4 ліків; запаси кубиків кожного кольору (`remaining-counter`); лічильник колоди гравця (до програшу); `card-hand` кожного; відкритий скид інфекції; `action-points` (4 → 0); `turn-indicator`; `message-log` (що інфіковано, де спалах).
- `confirm-dialog`: скидання понад 7, вибір цілі події, Forecast — переставляння 6 карт.
- `end-screen`: перемога / причина поразки.
- `tutorial-window`, `help-window`.
- Переходи: main-menu → match-setup → character-select → game-screen → end-screen.

## Фічі поза полем
- `difficulty-presets`: 4 / 5 / 6 епідемій (Introductory / Standard / Heroic).
- `mode-coop`, `hotseat` (у цифрі — один гравець керує кількома ролями).
- Доповнення: On the Brink (2009, 5-й гравець, нові ролі, 5-та хвороба Mutation, Virulent Strain), In the Lab (2013, лабораторія, соло й командний режим), State of Emergency (2015, нові ролі, Hinterlands, Emergency Events, Superbug).
- Legacy: Season 1 (2015), Season 2 (2017), Season 0 (2020) — гра змінює правила й поле назавжди між партіями.

## Варіації й родичі
- 1-ше видання (2008) — 5 ролей; 2-ге (2013) додало Планувальника й Спеціаліста з карантину.
- Forbidden Desert (`forbidden-desert.md`) і Forbidden Island — той самий автор: кооп, ролі, 4 дії, події наприкінці ходу, шкала ескалації.
- Механічні родичі: Chain Reaction (переповнення клітини → вибух у сусідів), «піщана купа» Abelian sandpile (`build-sim/abelian-sandpile.md`).
- **Осі варіацій**: поріг переповнення (3 / за кількістю сусідів) · куди розходиться (сусіди графа / сітка 4 / 8) · захист від повторного спалаху (раз за ланцюг / нема) · ескалація (трек темпу / постійна) · як «повертаються» погані події (перетасування скиду на верх / випадково).

## Цікавинки для курсу
- Спалах: переповнення 3 → по кубику кожному сусідові, ланцюг через чергу з забороною повторного спалаху міста — 🥉.
- «Intensify»: перетасувати скид і покласти **на верх** колоди — керована повторюваність (міста, що вже хворіли, повернуться першими) — 📎.
- Розподіл епідемій по рівних стосах колоди — гарантований темп небезпеки без випадкових скупчень — 📎.
- 7 ролей як модифікатори дій і правил розміщення (аура карантину, лікар-фільтр) — 🥉.
- Три незалежні умови поразки + одна перемоги — лічильники ресурсів поля — 🌱.
- Карти міст як «квитки»: пряма / чартерна / шатл між станціями + BFS для «за скільки дій я дістанусь» — 📎.
- Порадник для коопу: Монте-Карло по колоді інфекції (відкритий скид = знання про майбутнє) — 🥇.

## Мапа на каталог
- Є: `chain-reaction` (ланцюг спалахів) · `teleport` (перельоти, Airlift) · `wrap-edges` (червоні лінії через Тихий океан) · `spawn-random-cell` (інфекція міста з колоди) · `difficulty-levels` · `character-select` · `match-setup` · `game-screen` · `end-screen` · `help-window` · `tutorial-window`.
- **Нема** → пропозиції карток:
  - `+overflow-spread` «Переповнення клітини розходиться до сусідів» · game-logic/score · 🥉 · слоти {threshold: 3, once_per_chain} — спалах.
  - `+intensify-reshuffle` «Скид перетасовується на верх колоди» · game-logic/difficulty · 📎.
  - `+epidemic-pile-split` «Події, рівно розкладені по стосах колоди» · levels/generation · 📎.
  - `+graph-board` «Поле-граф міст» · entities/move · 📎.
  - `+set-collection-cure` «N карт одного кольору на станції» · game-logic/score · 🌱.
  - `+discard-to-move` «Карта як квиток руху» · entities/move · 🌱.
  - `+card-transfer-same-cell` «Передача карти в одній клітині» · entities/interact · 🌱.
  - `+eradication` «Ціль знищено — події цього типу ігноруються» · game-logic/state · 🌱.
  - `+deck-out-lose` / `+supply-out-lose` «Поразка від вичерпання колоди / запасу» · game-logic/defeat · 🌱.
  - `+aura-block-placement` «Аура фігури забороняє спавн» · entities/legality · 📎 — Спеціаліст із карантину.
  - `+event-cards-any-time` «Карти подій поза ходом» · game-logic/opponent · 📎.
  - `+shared-field-coop` · `+action-points` · `+variable-player-powers` · `+deck-draw` · `+hand-limit` · `+escalating-draw-count` · `+doom-track` — уже в корпусі або в цій пачці.

## Пропозиції до словників
- `+effect:spread` — по одиниці в кожного сусіда (спалах Pandemic; поширення вогню).
- `+effect:reshuffle` — перетасувати скид і покласти на верх / замість колоди (Intensify).
- `+effect:draw_cards` — взяти N карт з колоди (2 карти гравця, карти інфекції).
- `+effect:discard` — скинути карту з руки (переліт, ліки, ліміт 7).
- `+trigger:deck_empty` — колода гравця вичерпана → поразка.
- `+role:card` — карта як сутність.
- `+ui:doom-track` — трек до поразки (спалахи 0…8) і трек темпу.
- `+ui:card-hand` — руки гравців (у коопі — відкриті).
- `+card:overflow-spread` · `+card:intensify-reshuffle` · `+card:doom-track` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/Pandemic_(board_game)) — автор, 48 міст, 24 кубики кольору, хід, епідемія, спалах і ланцюг, ролі, поразки, доповнення, Legacy, цифрові версії.
- [RulesPal](https://rulespal.com/pandemic/rulebook) — правила 2-го видання: 59 карт гравця (48 + 6 + 5), підготовка, 8 дій, 7 ролей, епідемія, спалах «раз на карту інфекції», викорінення, ліміт руки.
- [UltraBoardGames](https://www.ultraboardgames.com/pandemic/game-rules.php) — правила 1-го видання (5 ролей), стоси з епідеміями, червоні лінії через край.
- [Lehi Innovation: правила](https://lehi-innovation.github.io/boardgame-rules/rules/pandemic/) — трек темпу 2-2-2-3-3-4-4, тексти 5 карт подій.
- YouTube: пошук «Pandemic board game how to play».

## Непевне
- (?) Інтерфейс цифрових версій (Asmodee Digital iOS 2013, Steam ~2018, знято з продажу у 2022) — не бачив, вікна «(цифрова версія)».
- (?) Чи Лікар блокує розміщення кубиків вилікуваної хвороби лише у своєму місті (так у Lehi Innovation) — у RulesPal так само; сусідніх не захищає.
- (?) Порядок розіграшу двох «Епідемій» підряд: RulesPal — кроки двічі; деталі взаємодії з картами подій між ними не перевіряв.
- (?) Platforms: Android-версії в прочитаних джерелах не бачив.
