---
title: "CodinGame Summer Challenge 2024: Olymbits"
slug: codingame-olymbits
aka: [Olymbits, Summer Challenge 2024, Arcade Olympics, Аркадна олімпіада]
family: program-robots
also: []
klass: avatar
axes:
  field: 1d
  time: programmed
  opponent: online
  info: full
  random: both
  goal: score
year: 2024
platforms: [web]
links:
  - {kind: official, url: "https://github.com/CodinGame/SummerChallenge2024Olymbits", best: true, note: "вихідний код судді й умова (HTML GitHub дав 504; сирі файли нижче відкрились)"}
  - {kind: other, url: "https://raw.githubusercontent.com/CodinGame/SummerChallenge2024Olymbits/main/config/statement_en.html.tpl", note: "умова: 4 мініігри, регістри GPU/reg0–reg6, медалі, добуток, ліги, протокол, 50 мс"}
  - {kind: other, url: "https://raw.githubusercontent.com/CodinGame/SummerChallenge2024Olymbits/main/src/main/java/com/codingame/game/Game.java", note: "цикл мініігор, reset-хід, медалі, ліги (1 / 4 бар'єрних / 4 різні), 100 ходів у Referee.java"}
  - {kind: other, url: "https://raw.githubusercontent.com/CodinGame/SummerChallenge2024Olymbits/main/src/main/java/com/codingame/game/mini/HurdleRace.java", note: "генерація доріжки, стрибок, оглушення, ранній фініш; поруч Archery.java, RollerSpeedSkating.java, Diving.java"}
  - {kind: other, url: "https://github.com/CGjupoulton/SummerChallenge2024Olymbits", note: "посилання на код з умови (не відкривав)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=codingame+olymbits", note: "пошук; реплеї й розбори"}
stage: v1
coverage: 70
mechanics: [move-by-input, combo-multiplier, event-points, wrap-edges, weighted-spawn, move-timer, replay, leaderboard, state-as-data, game-loop, +text-io-protocol, +turn-time-limit, +simultaneous-hidden-orders, +league-boss-promotion, +local-referee, +one-input-many-games, +register-io, +medal-product-score, +tie-shares-medal, +jump-over-cell, +stun-on-hit, +wind-scaled-move, +shuffled-action-meaning, +risk-meter, +sequence-match-combo, +reset-turn-between-runs, +early-race-end]
proposes: ["+trigger:run_over(game)", "+effect:award_medal(a, rank)", "+cond:action_index(a, list, i)", "+trigger:timeout(bot)", "+ui:register-panel", "+window:league-ladder", "+feature:bot-upload", "+feature:league-promotion"]
author: opus
date: 2026-11-09
---

# Olymbits — одна команда щоходу йде в чотири аркадні мініігри одразу: біг з барʼєрами, стрільба з луку, ролики, стрибки у воду

## Суть
Конкурс CodinGame (літо 2024): три боти на «старих аркадних автоматах». Кожен хід бот друкує **одну** з чотирьох дій — `UP`, `DOWN`, `LEFT`, `RIGHT` — і вона застосовується **в усіх чотирьох мініграх одночасно**, де означає різне: у бігу — довжину кроку, у луку — напрям зсуву прицілу, на роликах — ризик залежно від перемішаного порядку, у стрибках — збіг із заданою послідовністю. Мініігри крутяться по колу, за кожен забіг дають медалі, а фінальний рахунок — **добуток** очок за чотири ігри, тож провалити одну — означає нуль. Ядро — компроміс: яка гра «важливіша» саме цього ходу. Рамка арен — у [bot-arenas](bot-arenas.md).

## Поле і час
- Чотири незалежні «автомати», кожен показує стан у 8 регістрах: рядок `GPU` і числа `reg0…reg6` (невживані = −1).
- **Біг з барʼєрами** — 1D-доріжка з 30 клітин: старт 3–7 порожніх, далі 3–6 барʼєрів `#`, кожен з 3 або 4 порожніми клітинами за ним, остання клітина — фініш.
- **Стрільба з луку** — 2D-координати прицілу в межах [−20, 20], ціль — (0, 0); вітер — список 12–15 цифр (1–9, малі значення частіші).
- **Ролики** — кільцева доріжка з 10 клітин; позиція — пройдена відстань, зіткнення рахуються за модулем 10; забіг — 15 ходів.
- **Стрибки у воду** — без поля: послідовність-ціль з 12–15 літер `U/D/L/R`.
- Тік = хід; усі три гравці відповідають одночасно; партія — 100 ходів; 50 мс на хід, 1000 мс на перший.
- Після кінця забігу мініігра один хід «перезавантажується»: ввід ігнорується, `GPU` = `GAME_OVER`, генерується новий забіг.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Бігун (на гравця) | player | позиція 0–29, таймер оглушення | `LEFT` +1, `DOWN` +2, `RIGHT` +3, `UP` +2 зі стрибком через першу клітину |
| Барʼєр `#` | hazard | клітина доріжки | бігун, що ступив без стрибка, зупиняється на ньому й оглушений |
| Фініш | static | остання клітина | перший, хто дійшов, завершує забіг |
| Приціл лучника | player | x, y ∈ [−20, 20] | зсувається на силу поточного вітру в напрямку дії |
| Вітер | — (черга) | цифри 1–9 | щохід знімається перша; кінець черги = постріл |
| Роликовий спортсмен | player | пройдено, ризик 0–5 або −таймер оглушення | хід і ризик залежать від позиції дії в перемішаному порядку |
| Порядок дій роликів | — | перестановка `UDLR` | перемішується щоходу, показаний у `GPU` |
| Стрибун | player | очки, комбо | збіг з літерою цілі → комбо +1 і очки += комбо; промах → комбо 0 |
| Медалі | — (рахунок) | золото / срібло / бронза на гру | очки гри = срібло + 3·золото |

## Правила (КОЛИ → ЯКЩО → ТО)
Спільні:
- КОЛИ `turn_start` → ТО `custom: «суддя шле 3 рядки рахунків (фінальні очки й медалі кожної гри) і nbGames рядків GPU reg0…reg6»`.
- КОЛИ `input(UP|DOWN|LEFT|RIGHT)` → ТО `trigger(rule)` у кожній мінігрі з тією самою дією.
- КОЛИ `custom: «мінігра завершила забіг»` → ТО `custom: «медалі за місцем; рівні ділять вищу медаль, наступний бере місце за позицією (двоє перших — золото, третій — бронза)»`; наступного ходу — `restart` забігу з новою генерацією.
- КОЛИ `custom: «бот не відповів вчасно або нерозпізнана команда»` → ТО `lose`: фінальний рахунок −1, у мініграх він далі отримує бронзу.
- КОЛИ `counter(turn, ==, 100)` або `custom: «активних гравців < 2»` → ТО `game_over`; рахунок = ∏ (срібло + 3·золото) по іграх.

Біг з барʼєрами:
- КОЛИ `input(dir)` → ЯКЩО `counter(stun, >, 0)` → ТО `counter(stun, −1)`, `block`.
- КОЛИ `input(dir)` → ТО `move(runner, +1)` по одній клітині 1/2/3 рази (`LEFT`/`DOWN`, `UP`/`RIGHT`).
- КОЛИ `enter(runner, hurdle)` → ЯКЩО `custom: «це не перша клітина стрибка UP»` → ТО `block` решти кроків, `stun(runner, 2)` (див. «Непевне»).
- КОЛИ `reach(runner, finish)` → ТО `custom: «забіг закінчується одразу; місця — за позицією на доріжці»`.

Стрільба з луку:
- КОЛИ `input(dir)` → ТО `move(cursor, dir)` на `wind[0]` одиниць (`UP` — −y, `DOWN` — +y, `LEFT` — −x, `RIGHT` — +x), `custom: «обрізати до [−20, 20]»`, `custom: «зняти wind[0]»`.
- КОЛИ `custom: «черга вітру порожня»` → ТО `custom: «місця за x² + y², ближче до центру — вище»`.

Ролики:
- КОЛИ `input(dir)` → ЯКЩО `custom: «ризик < 0 (оглушений)»` → ТО `counter(risk, +1)`, `block`.
- КОЛИ `input(dir)` → ЯКЩО `custom: «дія стоїть на місці 0 / 1 / 2 / 3 у порядку GPU»` → ТО `move` на 1 / 2 / 2 / 3, `counter(risk, −1 / 0 / +1 / +2)` (не нижче 0).
- КОЛИ `custom: «після руху двоє на одній клітині за модулем 10»` → ТО `counter(risk, +2)` кожному з них.
- КОЛИ `counter(risk, >=, 5)` → ТО `stun(skater, 2)` (ризик = −2), `custom: «перемішати порядок дій»`.
- КОЛИ `counter(timer, ==, 0)` (15 ходів) → ТО `custom: «місця за пройденою відстанню»`.

Стрибки у воду:
- КОЛИ `input(dir)` → ЯКЩО `same(dir, goal[0])` → ТО `combo(+1)`, `score(+combo)`; інакше `reset_combo`; `custom: «зняти goal[0]»`.
- КОЛИ `custom: «ціль скінчилась»` → ТО `custom: «місця за очками»`.
- Перемога: найбільший добуток очок мініігор · Поразка: таймаут, хибна команда, добуток 0 через одні бронзи · Рахунок: ∏ (срібло + 3·золото).

## Керування і ввід
- Ініціалізація: `playerIdx` (0–2), `nbGames` (1 у Wood-лігах, 4 вище).
- Щоходу: 3 рядки рахунків (Wood — 4 числа, вище — 13: фінальні очки + золото/срібло/бронза × 4); потім `nbGames` рядків `GPU reg0 … reg6`.
- Вивід — одне слово `UP`, `DOWN`, `LEFT` або `RIGHT`.
- Регістри в кожній грі означають своє: біг — позиції й оглушення; лук — x/y трьох прицілів; ролики — відстані, ризики, `reg6` = ходів лишилось; стрибки — очки й комбо.

## Вікна, меню, HUD
- `arena-ide` (рамка — [bot-arenas](bot-arenas.md)): умова, редактор коду, консоль, Play testing / Submit.
- `replay-viewer`: чотири автомати з мініграми, номери ходів; текстовий підсумок «Game over: Hurdle Race», «… earns a GOLD medal».
- `end-screen`: рахунок у вигляді `1🥇+2🥈 * … = N` для кожного гравця.
- `league-ladder`: Wood (лише біг, один забіг; best-of-five проти боса) → ліга з чотирма бігами → чотири різні мініігри.

## Фічі поза полем
- `bot-upload`, `leaderboard-online`, `league-promotion` — ліги відкривають правила поступово.
- `local-referee`: відкритий Java-код судді (CodinGame SDK), конфіг на рівно 3 гравців.
- `replay` будь-якого матчу; undo/pause — лише в переглядачі.

## Варіації й родичі
- Аркадні «олімпіади» (Track & Field, Hyper Sports) — тема, не механіка; ядро — «одна кнопка на чотири ігри».
- Інші конкурси CodinGame в корпусі: [codingame-hypersonic](codingame-hypersonic.md), [codingame-keep-off-the-grass](codingame-keep-off-the-grass.md), [codingame-soak-overflow](codingame-soak-overflow.md), [codingame-cellularena](codingame-cellularena.md).
- Родичі за ідеєю «один ввід керує кількома полями» — `simultaneous-versus` (Puyo), але тут поля **різні** й гравець один на всіх.
- Осі варіацій: **кількість паралельних ігор** (1 / 4 однакові / 4 різні); **агрегація** (добуток / сума / мінімум); **значення дії** (фіксоване / залежить від стану / перемішане щоходу); **кінець забігу** (перший фініш / усі фінішували / таймер).

## Цікавинки для курсу
- Чотири мініігри як чотири класи з одним інтерфейсом `tick(actions)` / `get_rankings()` — 📎: чистий приклад поліморфізму.
- Біг з барʼєрами: крок по клітині з перевіркою барʼєра, стрибок, оглушення — 🌱.
- Медалі з рівними місцями й добуток очок — 🌱; пояснює, чому стратегія «підтягнути найслабшу гру» виграє.
- Вибір дії, що максимізує очікуване зростання добутку з урахуванням чотирьох станів — 🥈.
- Пошук на кілька ходів по всіх чотирьох іграх (біг і стрибки детерміновані, ролики — з перемішуванням) — 🥇.

## Мапа на каталог
- Є: `move-by-input` (дія → зсув) · `combo-multiplier` (стрибки) · `event-points` (медалі за місце) · `wrap-edges` (кільце роликів) · `weighted-spawn` (вітер зі зваженими значеннями) · `move-timer` (50 мс) · `replay` · `leaderboard` · `state-as-data` · `game-loop`.
- **Нема** → пропозиції карток:
  - `+text-io-protocol`, `+turn-time-limit`, `+simultaneous-hidden-orders`, `+league-boss-promotion`, `+local-referee` — з [bot-arenas](bot-arenas.md).
  - `+one-input-many-games` «Одна дія застосовується в кількох мініграх одразу» · game-logic/opponent · 🥉.
  - `+register-io` «Стан гри — у фіксованих регістрах (рядок + 7 чисел)» · code/architecture · 🌱.
  - `+medal-product-score` «Підсумок — добуток очок за частини» · game-logic/score · 🌱.
  - `+tie-shares-medal` «Рівні місця ділять вищу нагороду» · game-logic/score · 🌱.
  - `+jump-over-cell` «Стрибок через наступну клітину ігнорує перешкоду» · entities/move · 🌱.
  - `+stun-on-hit` «Удар об перешкоду — пропуск N ходів» · entities/state · 🌱.
  - `+wind-scaled-move` «Довжина зсуву задана зовнішньою чергою (вітер)» · entities/move · 🌱.
  - `+shuffled-action-meaning` «Значення дій перемішується щоходу» · game-logic/opponent · 📎.
  - `+risk-meter` «Лічильник ризику: ризиковий хід швидший, переповнення — оглушення» · entities/state · 📎.
  - `+sequence-match-combo` «Збіг з послідовністю-ціллю нарощує комбо» · game-logic/score · 🌱.
  - `+reset-turn-between-runs` «Хід-пауза між забігами, ввід ігнорується» · game-logic/waves · 🌱.
  - `+early-race-end` «Забіг закінчується з першим фінішем, решта — за позицією» · game-logic/win · 🌱.

## Пропозиції до словників
- `+trigger:run_over(game)` — мінігра/забіг завершився (Olymbits, багатоігрові арени).
- `+effect:award_medal(a, rank)` — нагорода за місце в частині партії.
- `+cond:action_index(a, list, i)` — дія стоїть на i-му місці в показаному списку (ролики).
- `+trigger:timeout(bot)` · `+window:league-ladder` · `+feature:bot-upload` · `+feature:league-promotion` — підтвердження з арен.
- `+ui:register-panel` — показ сирих регістрів автомата поруч з картинкою.

## Джерела
- ⭐ [CodinGame/SummerChallenge2024Olymbits](https://github.com/CodinGame/SummerChallenge2024Olymbits) — репозиторій судді (HTML недоступний у момент читання, сирі файли — так).
- [statement_en.html.tpl](https://raw.githubusercontent.com/CodinGame/SummerChallenge2024Olymbits/main/config/statement_en.html.tpl) — повна умова з правилами кожної мініігри і протоколом.
- [Game.java](https://raw.githubusercontent.com/CodinGame/SummerChallenge2024Olymbits/main/src/main/java/com/codingame/game/Game.java) — цикл, reset-хід, медалі, ліги; `Referee.java` — 100 ходів, 50/1000 мс; `Player.java` — добуток `3·gold + silver`.
- [HurdleRace.java](https://raw.githubusercontent.com/CodinGame/SummerChallenge2024Olymbits/main/src/main/java/com/codingame/game/mini/HurdleRace.java), `Archery.java`, `RollerSpeedSkating.java`, `Diving.java`, `MiniGame.java` — генерація й тік кожної гри, ранжування з нічиїми.

## Непевне
- (?) Оглушення в бігу: умова каже «на 3 ходи» й регістр 3→2→1, у коді репозиторію `STUN_DURATION = 2` (пропускаються два наступні ходи) — версії могли розійтись.
- (?) Комбо стрибків: умова — «стартує з 1», код — з 0 і +1 перед нарахуванням (перший збіг дає 1 очко в обох прочитаннях).
- (?) Назва сторінки арени CodinGame (`/multiplayer/bot-programming/…`) і розклад ліг — не бачив; тому лінка на арену нема.
- (?) Вигляд переглядача (картинки автоматів, HUD) — не відкривав.
