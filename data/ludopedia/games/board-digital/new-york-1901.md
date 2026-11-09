---
title: New York 1901 (Нью-Йорк 1901)
slug: new-york-1901
aka: [Нью-Йорк 1901, NY1901]
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
year: 2015
platforms: [board]
links:
  - {kind: other, url: "https://www.ultraboardgames.com/new-york-1901/game-rules.php", best: true, note: "правила: дільниці й ділянки, хід Expand / Demolish / Build, правила будівництва, кінець, рахунок вулиць"}
  - {kind: other, url: "https://rulespal.com/new-york-1901/rulebook", note: "книга правил: картки дій, легендарні хмарочоси, бонус-челенджі, вулиці, експертні пороги"}
  - {kind: other, url: "https://blueorangegames.com/webroot/img/games/rules/5efdb34a69b105d69c9210fc6d98ee3c-NY1901-Rule-US-2.pdf", note: "PDF правил від Blue Orange (бачив у пошуку, не відкривав)"}
  - {kind: official, url: "https://www.blueorangegames.com/games/newyork-1901", note: "сторінка видавця"}
  - {kind: other, url: "https://www.geekyhobbies.com/new-york-1901-board-game-review-and-rules/", note: "огляд і правила (бачив у пошуку)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=New+York+1901+how+to+play", note: "пошук; пояснення правил"}
stage: v1
coverage: 55
mechanics: [polyomino-placement, piece-rotate-flip, drag-drop-piece, hover-highlight, legal-move-highlight, event-points, turn-enforcement, hot-seat, pass-turn, game-screen, main-menu, match-setup, end-screen, help-window, +worker-claim-lots, +card-market-refill, +tech-tier-unlock-by-score, +demolish-and-rebuild, +must-touch-street, +owned-area-placement, +street-majority, +public-objective-card, +one-shot-action-cards, +unique-legendary-buildings, +tiebreak-chain, +end-trigger-last-round]
proposes: ["+trigger:market_low", "+cond:in_estate", "+cond:touches(street)", "+cond:tier_unlocked", "+effect:demolish", "+effect:claim", "+effect:refill", "+effect:reclaim_worker", "+role:worker", "+ui:tier-tracker", "+ui:card-row", "+window:score-sheet", "+card:demolish-and-rebuild", "+card:street-majority", "+card:tech-tier-unlock-by-score"]
author: opus
date: 2026-11-09
---

# New York 1901 — займай ділянки Мангеттену робітниками, будуй на них тетроміно-хмарочоси й зноси старі заради вищих

## Суть
Гравці — забудовники Фінансового району Нью-Йорка. Карта ділянок з ринку дозволяє поставити робітника на вільну ділянку того ж кольору й розміру; з кількох своїх ділянок складається «маєток», у який кладуться хмарочоси-поліоміно. Очки за побудоване відкривають наступні покоління (бронза → срібло → золото), а знесення старших хмарочосів під новіші дає ще більше очок. Наприкінці — бонуси за більшість на вулицях, спільний челендж і невикористані картки дій.

## Поле і час
- **Карта**: 5 дільниць (червона, синя, жовта, зелена, рожева) по 13 ділянок = 65 ділянок; ділянки на 2 або 3 клітини (на ділянках з 3 клітин — квіти). Між ділянками — 5 кольорових вулиць і парки; довкола — трек очок.
- **Ринок**: відкритий ринок з 4 карт ділянок + закрита колода («майбутній ринок»).
- **Запас гравця**: 19 хмарочосів (разом зі стартовою будівлею), 4 робітники, жетон короля, 3 картки дій.
- Спільні: 4 легендарні хмарочоси (золоті), 3 з 5 карт вулиць, 1 з 5 бонус-челенджів.
- **Час**: хід за годинниковою стрілкою; кожен хід — набуття ділянки або знесення, далі будівництво. Кінець — за порогом запасу хмарочосів або вичерпання ринку, потім кожен інший ще один хід.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Ділянка (lot) | zone | дільниця-колір, розмір 2 / 3 клітини | займається робітником за картою того ж кольору й розміру |
| Дільниця | zone | колір, 13 ділянок | хмарочос через межу рахується в обох |
| Вулиця | static | 5 названих (Nassau & Broad, Broadway, Pine & Thames, Wall Street, Cedar) | хмарочос, що торкається, рахується в більшості вулиці |
| Парк | static | — | дотик стороною дозволяє будувати |
| Карта ділянки | supply | колір, розмір, 65 шт. | ринок 4 відкриті + колода; 1 карта на кожну ділянку |
| Робітник | piece | 4 на гравця | займає ділянку; повертається, коли на ділянці побудовано |
| Хмарочос | piece | покоління (бронза / срібло / золото), форма (прямокутна / не прямокутна), очки | кладеться в маєток; дає очки одразу |
| Стартова будівля | piece | без покоління, 0 очок | стоїть на стартовій 2-клітинній ділянці |
| Легендарний хмарочос | piece | Park Row 9 · Singer 10 · Metropolitan Life 12 · Woolworth 13 очок; висота | вважається золотим; кожен будує ≤ 1, кожен легендарний — лише раз; не зноситься |
| Жетон короля | mark | — | позначає власника легендарного |
| Картка дії | pickup | Construction Boom, Market Shift, Land Grab | раз за гру; невикористана = 1 очко |
| Карта вулиці | zone | 3 з 5 у грі | 5 очок за більшість хмарочосів на вулиці; нічия — 0 |
| Бонус-челендж | zone | 1 з 5 | спільна ціль: Gold Tycoon, Master Architect, Gold Prestige, Bronze Baron, Generation King |
| Маркер очок | object | позиція на треку | відкриває покоління: срібло з 6, золото з 18 (експерт: 10 / 25) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(player)` → ТО `choose(Варіант 1: набути ділянку → можна будувати / Варіант 2: знести → обовʼязково будувати)`.
- КОЛИ `input(expand(card))` → ЯКЩО `custom: «карта з відкритого ринку»` and `has(player, worker)` and `custom: «є вільна ділянка того ж кольору й розміру»` → ТО `place(worker, lot)`, `custom: «поповнити ринок до 4 з колоди»`.
- КОЛИ `turn_start(player)` → ЯКЩО `has(player, worker)` and `custom: «не зносить»` → ТО `custom: «набуття ділянки обовʼязкове»`.
- КОЛИ `input(build(skyscraper, cells))` → ЯКЩО `fits(skyscraper, estate)` and `custom: «торкається вулиці або парку стороною (кут не рахується)»` and `custom: «покоління відкрите за очками»` → ТО `place(skyscraper, cells)`, `score(+points)`, `custom: «повернути робітників з ділянок, на яких побудовано»`; інакше `block`.
- Хмарочос може перетинати межі ділянок і дільниць і не мусить заповнювати ділянку; перекривати інші не можна (крім знесення).
- КОЛИ `input(demolish(new_skyscraper))` → ЯКЩО `custom: «під новим лише хмарочоси нижчого покоління (золоті не зносяться)»` and `custom: «кожна звільнена ділянка поза новим має робітника»` → ТО `disappear(old_skyscrapers)` (очки не віднімаються), `custom: «обовʼязкове будівництво цього ходу»`.
- КОЛИ `counter(score, >=, 6)` → ТО `unlock(silver)` · КОЛИ `counter(score, >=, 18)` → ТО `unlock(gold)` (експерт: 10 / 25, без стартової будівлі).
- КОЛИ `input(build(legendary))` → ЯКЩО `custom: «гравець ще не будував легендарний і цей вільний»` and `custom: «золото відкрите»` → ТО `place(legendary)`, `place(king_token)`, `score(+points)`.
- КОЛИ `input(action(Construction Boom))` → ЯКЩО `not state(card, used)` → ТО `extra_move` (друге будівництво на вже набутій землі, без другого знесення; не можна, якщо перше будівництво запустило кінець).
- КОЛИ `input(action(Market Shift))` на початку ходу → ТО `custom: «замінити 4 карти ринку на 4 верхні з колоди, старі — під низ»`.
- КОЛИ `input(action(Land Grab))` → ЯКЩО `has(player, worker)` and `custom: «колода не порожня, ділянка не на 3 клітини»` → ТО `custom: «ще одна ділянка з ринку»`.
- КОЛИ `turn_start(player)` → ЯКЩО `not has(player, worker)` → ТО `custom: «пропустити набуття, лише будувати»`.
- КОЛИ `turn_start(player)` → ЯКЩО `not has(player, worker)` and `custom: «нема легального будівництва чи знесення»` → ТО `custom: «повернути одного робітника, його карту — під низ колоди»`, `pass_turn`.
- КОЛИ `custom: «у гравця лишилось 4 непобудовані хмарочоси»` or `custom: «на ринку 3 карти і колода порожня»` → ТО `custom: «кожен інший гравець робить останній хід»`, `game_over`.
- Gold Prestige (під час гри): КОЛИ `input(build(gold))` → ЯКЩО `adjacent_count(opponent_older_skyscraper, >=, 1)` (лише ребром) → ТО `score(+1 за кожного)`.
- Рахунок: очки побудованого + 5 за більшість на кожній із 3 вулиць (нічия — 0; хмарочос на кількох вулицях рахується скрізь) + бонус-челендж + 1 за невикористану картку дії.
- Челенджі: Gold Tycoon 3 за дільницю з ≥ 2 золотими · Master Architect 3 / 6 / 10 за 3 / 4 / 5+ непрямокутних · Bronze Baron 5 / 10 / 15 за 4 / 5 / 6 бронзових · Generation King 5 за покоління, де в гравця найбільше.
- Перемога: найбільше очок; тай-брейк — найвищий легендарний, далі більше золотих, далі спільна перемога.
- Вдвох: прибрати 13 рожевих карт ділянок і персонажа David Schneider.

## Керування і ввід
- Настільна: взяти карту, поставити робітника, викласти тайл хмарочоса (поворот; дзеркало — (?)).
- Цифрова версія: клік по карті ринку → підсвічені вільні ділянки того кольору й розміру → клік; хмарочос — drag з запасу, поворот, підсвічення легального (в маєтку, дотик до вулиці); знесення — показ, що буде знесено, і підтвердження.
- Картки дій — кнопки з позначкою «використано».

## Вікна, меню, HUD
- `main-menu` (цифрова версія): нова гра, правила.
- `match-setup`: 2–4 гравці, персонажі, експертні правила, вибір вулиць і челенджа (випадково).
- `game-screen`: карта з дільницями, вулицями й парками; ринок 4 карт (`+ui:card-row`) і лічильник колоди (`remaining-counter`); запас хмарочосів гравця за поколіннями (`+ui:tier-tracker` — що відкрито); робітники; трек очок довкола (`score`); картки дій; `turn-indicator`; `legal-move-highlight`.
- `help-window`: опис вулиць, челенджів і легендарних.
- `end-screen` (`+window:score-sheet`): побудоване, вулиці, челендж, картки дій, тай-брейк.
- `confirm-dialog`: підтвердження знесення.

## Фічі поза полем
- Цифрової версії не знайдено; як було б: `hotseat`, `ai-opponent-levels`, `tutorial`, `rules-page`.
- Експертні правила: пороги 10 / 25 і старт без стартової будівлі (`custom-rules`).
- Рекомендація: попереджати інших, коли лишилось 5 хмарочосів.

## Варіації й родичі
- Варіанти: базові / експертні пороги; набір вулиць (3 з 5) і челендж (1 з 5) змінюють цілі партії.
- Родичі: Patchwork і Blokus (поліоміно), Tiny Towns і Kingdom Builder (обмеження розміщення), Tigris & Euphrates (більшості), The Isle of Cats (поліоміно в області); знесення-перебудова — рідкісне в корпусі.
- **Осі варіацій**: де можна будувати (будь-де / лише на своїх ділянках) · замінювати (ні / лише вищим поколінням) · відкриття форм (за очками / за кількістю будівель) · умова доступу (дотик до вулиці / будь-де) · кінцеві бонуси (більшість / набори / челенджі).

## Цікавинки для курсу
- Маєток як обʼєднання зайнятих ділянок + перевірка «хмарочос цілком у маєтку й не перекриває» — 📎.
- Дотик стороною до вулиці/парку (кут не рахується) — 🌱.
- Знесення-перебудова: новий хмарочос перекриває лише нижчі покоління, звільнені ділянки мусять мати робітника — 🥉.
- Відкриття поколінь за порогами очок — 🌱.
- Більшість на вулицях (хмарочос на кількох вулицях, нічия — нікому) — 📎.
- Тай-брейк ланцюгом (висота легендарного → кількість золотих → спільна) — 🌱.
- AI «де будувати» з перебором форм, поворотів і знесень — 🥈.

## Мапа на каталог
- Є: `polyomino-placement` · `piece-rotate-flip` · `drag-drop-piece` · `hover-highlight` · `legal-move-highlight` · `event-points` · `turn-enforcement` · `hot-seat` · `pass-turn` · вікна `game-screen` / `main-menu` / `match-setup` / `end-screen` / `help-window`.
- **Нема** → пропозиції карток:
  - `+demolish-and-rebuild` «Знести й перебудувати вищим» · entities/legality · 🥉 · слот {replace_if: tier_lower}.
  - `+tech-tier-unlock-by-score` «Покоління за порогами очок» · game-logic/score · 🌱 · слоти {thresholds: [6, 18]}.
  - `+street-majority` «Більшість на лінії/вулиці» · game-logic/score · 📎 (родич `+area-majority` з Samurai).
  - `+worker-claim-lots` · `+owned-area-placement` · `+must-touch-street` · `+card-market-refill` · `+one-shot-action-cards` · `+unique-legendary-buildings` · `+public-objective-card` · `+tiebreak-chain` · `+end-trigger-last-round`.

## Пропозиції до словників
- `+trigger:market_low` — ринок/колода нижче порогу (кінець гри).
- `+cond:in_estate(shape)` — фігура цілком у зоні власника.
- `+cond:touches(street)` — дотик ребром до лінії/обʼєкта (без кутів).
- `+cond:tier_unlocked(t)` — покоління відкрите.
- `+effect:demolish(cells)` — зняти побудоване з поля без втрати очок.
- `+effect:claim(lot)` — зайняти ділянку робітником; `+effect:reclaim_worker` — повернути робітника.
- `+effect:refill(market)` — поповнити ринок з колоди.
- `+role:worker` — фішка, що займає місце й повертається.
- `+ui:tier-tracker` — запас за поколіннями з позначкою відкритого; `+ui:card-row` — ряд відкритих карт.
- `+window:score-sheet` — підсумок за категоріями.
- `+card:demolish-and-rebuild` · `+card:street-majority` · `+card:tech-tier-unlock-by-score`.

## Джерела
- ⭐ [UltraBoardGames: New York 1901 rules](https://www.ultraboardgames.com/new-york-1901/game-rules.php) — карта, сетап, хід Expand / Demolish / Build, будівництво, нестандартні ситуації, кінець, вулиці, тай-брейк.
- [RulesPal: New York 1901 rulebook](https://rulespal.com/new-york-1901/rulebook) — картки дій, легендарні з очками, пороги поколінь (база й експерт), вулиці поіменно, 5 челенджів.
- [Blue Orange: New York 1901](https://www.blueorangegames.com/games/newyork-1901) — видавець; автор Chénier La Salle.
- [Geeky Hobbies: огляд і правила](https://www.geekyhobbies.com/new-york-1901-board-game-review-and-rules/) — бачив у пошуку: тайли «у формі тетроміно».
- YouTube: пошук «New York 1901 how to play».

## Непевне
- (?) Точні форми й очки бронзових/срібних/золотих хмарочосів — джерела не дають (лише «прямокутні / непрямокутні», «тетроміно»).
- (?) Чи можна дзеркалити тайл хмарочоса — не перевірено.
- (?) Чи будування після набуття ділянки необовʼязкове — так випливає з «після знесення будувати ОБОВʼЯЗКОВО», прямо не сказано.
- (?) Розмір клітинної сітки карти — не вказано.
- (?) Розширення (New Blood, Chicago 1875 тощо) — не перевірено; стаття Wikipedia New_York_1901 — 404.
- (?) Цифрової версії не знайдено; вікна — «(цифрова версія)», гіпотетичні.
