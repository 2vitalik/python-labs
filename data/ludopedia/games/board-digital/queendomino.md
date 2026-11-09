---
title: Queendomino (Квіндоміно)
slug: queendomino
aka: [Квіндоміно]
family: board-digital
also: []
klass: cursor
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: runtime
  goal: score
year: 2017
platforms: [board]
links:
  - {kind: other, url: "https://www.ultraboardgames.com/queendomino/game-rules.php", best: true, note: "повні правила: дії A–E, лицарі-податки, будівлі й символи, королева, дракон, рахунок, тай-брейк"}
  - {kind: other, url: "https://rulespal.com/queendomino/rulebook", note: "рулбук: 20 червоних клітин, гра на 2, поєднання з Kingdomino (5–6 гравців, команди 6/8)"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=Queendomino", note: "пошук BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Queendomino+how+to+play", note: "пошук; пояснення правил"}
stage: v1
coverage: 70
mechanics: [cell-click, drag-drop-piece, tile-rotate, hover-highlight, legal-move-highlight, turn-enforcement, hot-seat, ai-opponent, round-currency, shop-catalog, event-points, field-size-picker, game-settings, match-setup, game-screen, end-screen, +domino-tile, +connected-placement, +edge-matching, +bounded-grid-growth, +draft-order-by-value, +area-times-multiplier, +connected-group-scoring, +discard-unplayable, +drafting-market, +tax-by-territory, +majority-holder-token, +market-burn, +slide-refill-market, +build-slot-cells, +ongoing-income-bonus, +tiebreak-chain]
proposes: ["+trigger:round_end", "+effect:discard", "+effect:draft", "+effect:burn_offer", "+cond:afford", "+cond:holds_token", "+role:building", "+role:market", "+ui:builders-board", "+ui:coin-counter", "+ui:opponent-boards", "+card:tax-by-territory", "+card:majority-holder-token", "+card:market-burn"]
author: opus
date: 2026-11-09
---

# Queendomino — Kingdomino з економікою: лицарі збирають податки з території, монети купують будівлі на червоних клітинах міст, королева йде до власника більшості веж

## Суть
Основа — як у [kingdomino.md](kingdomino.md): драфт доміно за номером, прибудова з хоча б одним збігом місцевості, рахунок «площа × корони». Нове — червона місцевість «місто» з будівельними клітинами, монети, лицарі (податок = розмір території), ринок будівель і дві спільні фігури: королева (знижка й корона тому, в кого найбільше веж) і дракон (за монету спалює будівлю на ринку). Хід розгортається з 2 дій у 5.

## Поле і час
- Королівство 5×5 (3–4 гравці) або 7×7 (2 гравці); у Kingdomino 7×7 — лише варіант Mighty Duel.
- **Усі 48 доміно** в будь-якому складі (у Kingdomino для 2–3 гравців частину прибирають); у грі на 3 — останнє незайняте доміно лінії скидається щораунду.
- Спільні зони: дві лінії по 4 доміно; **дошка будівельників** із 6 відкритими будівлями, упорядкованими за ціною; печера дракона; банк монет.
- Хід = 5 дій A–E (у грі на 2 — двічі, по разу на кожного короля). 12 раундів, останній — лише A–D.

## Сутності
Лише нові або змінені відносно Kingdomino; доміно, король, стартова клітина — як там.

| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Місто (червона місцевість) | terrain | 20 червоних клітин на всіх доміно | клітина без будівлі = будівельний майданчик; область міст рахується як інші (площа × корони) |
| Будівля | tile | ціна; 4 символи: миттєвий, постійний, корони, кінцеві очки | купується з дошки, ставиться на вільну червону клітину свого королівства |
| Дошка будівельників | supply | 6 слотів за зростанням ціни | порожні слоти — до кінця раунду; тоді будівлі зсуваються до дешевих, решта зі стосу |
| Стос будівель | supply | 32 будівлі, лицем догори | доповнює дошку |
| Лицар | piece | старт 1; більше — з будівель | ставиться на щойно покладене доміно (1–2), лишається до кінця; приносить податок |
| Монета | resource | старт 7 | платіж за будівлю / дракона; 3 монети = 1 очко наприкінці |
| Вежа | mark | на будівлях | більшість (включно з нічиєю) забирає королеву |
| Королева | neutral | 1 | у власника: будівлі −1 монета; у кінці — +1 корона на найбільшу територію; її власник не може кликати дракона |
| Дракон | neutral | 1, печера | раз на раунд, за 1 монету: прибрати будівлю з дошки з гри; повертається в печеру на початку раунду |

## Правила (КОЛИ → ЯКЩО → ТО)
- Дія A (обовʼязкова): як у Kingdomino — КОЛИ `input(place(domino))` → ЯКЩО `fits(domino, kingdom)` and `custom: «хоча б одна пара сусідніх клітин тієї ж місцевості (замок — джокер)»` → ТО `place(player, domino)`; нема легального місця → `custom: «доміно скидається без очок; скидати можна лише нелегальне»`.
- Дія B (опц.): КОЛИ `input(place(knight, domino_cell))` → ЯКЩО `has(player, knight)` and `custom: «не більше 1 лицаря на клітину щойно покладеного доміно»` → ТО `place(player, knight)` і `currency(+N)`, N = клітин у звʼязній території під лицарем.
- Постійні бонуси під час податку: КОЛИ `after(tax)` → ТО `currency(+лицарів_усього)` за кожну будівлю з постійним символом лицаря; `currency(+веж)` за будівлю з постійним символом вежі.
- Дія C (опц.): КОЛИ `input(buy(building))` → ЯКЩО `custom: «є вільна червона клітина»` and `counter(coins, >=, ціна)` → ТО `currency(-ціна)` (−1, якщо `has(player, queen)`), `place(player, building)`; слот на дошці лишається порожнім.
- Миттєві символи: КОЛИ `after(build)` → ТО `give(player, knight)` (діють з наступного ходу) та/або `counter(towers, +n)`.
- Королева: КОЛИ `after(build)` → ЯКЩО `custom: «у гравця веж ≥ у будь-кого»` → ТО `move(queen, player)`.
- Дія D (опц.): КОЛИ `input(bribe_dragon(building))` → ЯКЩО `custom: «дракон у печері»` and `not has(player, queen)` and `counter(coins, >=, 1)` → ТО `currency(-1)`, `custom: «будівля зі слоту виходить з гри, дракон стає на її місце»`.
- Дія E (обовʼязкова): як у Kingdomino — король на вільне доміно наступної лінії; більший номер → пізніший хід.
- КОЛИ `phase_start(round)` → ТО дракон у печеру; `custom: «будівлі зсуваються до дешевих слотів, порожні доповнюються зі стосу»`; нова лінія з 4 доміно.
- КОЛИ `custom: «останні 4 доміно взято»` → ТО фінальний хід лише A–D, потім `game_over`.
- Рахунок: території `score(+площа × корони)` (міста теж) · 3 монети = `score(+1)` · кінцеві очки будівель · бонус «хрест місцевості»: `score(+2)` за кожну окрему територію вказаного типу · бонус веж `score(+1)` за вежу · бонус лицарів `score(+1)` за лицаря.
- КОЛИ `game_over` → ЯКЩО `has(player, queen)` → ТО `custom: «королева = +1 корона на найбільшій території гравця»`.
- Тай-брейк: найбільша територія → спільна перемога.
- Kingdomino + Queendomino: лінії по черзі з обох коробок; 3–4 гравці — 7×7, 5–6 — 5×5 з лініями по 8 доміно; команди 6/8 гравців — пари на спільному 7×7.

## Керування і ввід
- Порядок дій жорсткий: A → B → C → D → E; опційні можна пропустити кнопкою.
- Лицар: клік по клітині щойно покладеного доміно (підсвічені дві), показ очікуваного податку.
- Купівля: клік по будівлі на дошці (недоступні затемнені за ціною), потім по вільній червоній клітині.
- Дракон: клік по будівлі на дошці з підтвердженням.

## Вікна, меню, HUD
(цифрова версія — за аналогією з Kingdomino)
- `match-setup`: гравці, режим 5×5/7×7, поєднання з Kingdomino, команди.
- `game-screen`: королівство з рамкою; `draft-line`; `builders-board` (6 слотів з ціною, стос); `coin-counter`; лічильники лицарів і веж; маркер королеви й дракона; `opponent-boards`; `turn-indicator` з поточною дією A–E; `score-preview`.
- `confirm-dialog`: спалити будівлю драконом?
- `end-screen`: таблиця — території, монети, будівлі, бонуси, королева.

## Фічі поза полем
- `custom-rules`: поєднання з Kingdomino (до 8 гравців, команди).
- `hotseat`; `ai-opponent-levels` — лише якщо буде цифрова версія (?).
- `rules-page` з легендою символів будівель (чотири кути тайла).

## Варіації й родичі
- База: `kingdomino` (сусід по теці). Інші спіноффи — у [kingdomino.md](kingdomino.md): Age of Giants, Origins, Duel, Dragomino.
- Родичі економіки «дохід від території»: The Castles of Burgundy (`the-castles-of-burgundy`) — купівля тайлів з ринку.
- **Осі варіацій**: дохід (нема / податок від розміру / від будівель) · ринок (фіксований / зсув до дешевших / спалювання) · спільна фігура-бонус (нема / більшість веж / найбільший рахунок).

## Цікавинки для курсу
- Податок = розмір звʼязної території під лицарем (flood fill при кожній дії) — 📎.
- Ринок, що зсувається до дешевих слотів і доповнюється на кінці раунду — 🌱.
- Токен більшості (королева) з передачею при нічиїй на користь нового — 🌱; плюс заборона дракона власнику — 🌱.
- Покроковий хід з 5 фаз: машина станів A–E з обовʼязковими й опційними кроками — 🥉.
- Будівля з чотирма видами ефектів (миттєвий / постійний / корони / кінцеві) — data-driven картки — 🥉.
- AI, що оцінює «податок зараз vs будівлі потім» — 🥇.

## Мапа на каталог
- Є: як у Kingdomino (`cell-click`, `drag-drop-piece`, `tile-rotate`, `legal-move-highlight`, `turn-enforcement`, `hot-seat`, `field-size-picker`) + `round-currency` (монети в партії) · `shop-catalog` (дошка будівельників).
- З Kingdomino: `+domino-tile` · `+connected-placement` · `+edge-matching` · `+bounded-grid-growth` · `+draft-order-by-value` · `+area-times-multiplier` · `+connected-group-scoring` · `+discard-unplayable`.
- **Нема** → пропозиції карток:
  - `+tax-by-territory` «Дохід = розмір звʼязної території під фігурою» · game-logic/economy · 📎.
  - `+majority-holder-token` «Спільний токен у того, в кого більшість, з бонусом і обмеженням» · game-logic/score · 🌱.
  - `+market-burn` «Заплатити, щоб прибрати пропозицію з ринку» · game-logic/economy · 🌱.
  - `+slide-refill-market` «Ринок зсувається до дешевих слотів, доповнюється в кінці раунду» · game-logic/economy · 🌱.
  - `+build-slot-cells` «Будувати лише на клітинах-майданчиках свого поля» · entities/legality · 🌱.
  - `+ongoing-income-bonus` «Постійний бонус до кожного доходу» · game-logic/economy · 🌱.

## Пропозиції до словників
- `+trigger:round_end` · `+effect:discard` · `+effect:draft` — як у Kingdomino/Azul/Sagrada.
- `+effect:burn_offer` — прибрати пропозицію з ринку назавжди (дракон).
- `+cond:afford` — вистачає валюти на ціну (з урахуванням знижки).
- `+cond:holds_token` — гравець тримає спільний токен (королева) — родич `has`, але токен один на гру.
- `+role:building` · `+role:market` — будівля на полі; ринок пропозицій.
- `+ui:builders-board` — ринок з ціною слотів · `+ui:coin-counter`.

## Джерела
- ⭐ [UltraBoardGames: Queendomino rules](https://www.ultraboardgames.com/queendomino/game-rules.php) — склад (48 доміно, 32 будівлі, 22 лицарі), дії A–E, символи будівель, королева, дракон, рахунок, тай-брейки.
- [RulesPal: Queendomino rulebook](https://rulespal.com/queendomino/rulebook) — 20 червоних клітин, гра на 2 з двома королями, поєднання з Kingdomino.
- [kingdomino.md](kingdomino.md) — база правил і варіантів.

## Непевне
- (?) Діапазон цін будівель і повний список 32 будівель — на самих тайлах, у джерелах не перелічено.
- (?) Цифрової версії Queendomino не знайдено; вікна — за аналогією з Kingdomino.
- (?) «Кожна будівля — лише на червону клітину, одна на клітину» — так у правилах; чи можна будувати на червоній клітині з короною — не уточнено.
- (?) Варіанти Harmony / Middle Kingdom у Queendomino не згадані в джерелах.
