---
title: Welcome To… (Ласкаво просимо до…)
slug: welcome-to
aka: ["Welcome To... Your Perfect Home", Welcome To, Ласкаво просимо до…]
family: board-digital
also: []
klass: cursor
axes:
  field: 1d
  time: turn
  opponent: hotseat
  info: full
  random: runtime
  goal: score
year: 2018
platforms: [board, web]
links:
  - {kind: other, url: "https://www.ultraboardgames.com/welcome-to/game-rules.php", best: true, note: "повні правила: 3 стоси карт, зростання номерів, 6 дій, відмови, квартали, плани міста, кінець, підрахунок, тайбрейки"}
  - {kind: play, url: "https://en.boardgamearena.com/gamepanel?game=welcometo", note: "BGA: 1–12 гравців, просунутий варіант (кільцева розвʼязка), експерт-правила, тематичні листи"}
  - {kind: other, url: "https://rulespal.com/welcome-to/rulebook", note: "книга правил (сторінку не відкривав)"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=Welcome+To", note: "пошук BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Welcome+To+board+game+how+to+play", note: "пошук; пояснення правил"}
stage: v1
coverage: 65
mechanics: [cell-click, hover-highlight, legal-move-highlight, simultaneous-versus, online-multiplayer, event-points, completion-detection, game-settings, match-setup, rule-variants, game-screen, end-screen, help-window, score-records, +simultaneous-turns, +flip-and-write, +pair-choice-market, +ascending-sequence-rule, +gap-fill-later, +fence-split-segments, +segment-size-scoring, +upgrade-track, +escalating-track-score, +number-modifier, +duplicate-neighbor, +strike-penalty-track, +public-objectives, +first-to-achieve-bonus, +majority-bonus, +multi-end-trigger, +deck-reshuffle, +tiebreak-chain]
proposes: ["+cond:ascending", "+cond:segment_closed", "+effect:cross_box", "+trigger:objective_met", "+role:objective", "+ui:score-tracks", "+ui:card-pairs", "+window:sheet-view", "+feature:themed-sheets", "+card:ascending-sequence-rule", "+card:fence-split-segments", "+card:strike-penalty-track", "+card:pair-choice-market"]
author: opus
date: 2026-11-09
---

# Welcome To… — flip-and-write: усі вибирають одну з трьох пар «номер + дія» і вписують номер у будинок так, щоб на вулиці номери зростали

## Суть
Щоходу відкривають три пари «номер будинку + дія»; кожен гравець **одночасно** вибирає одну пару, вписує номер у порожній будинок на одній із трьох своїх вулиць і за бажання виконує дію. Номери на вулиці мусять строго зростати зліва направо, без повторів, але з дірками — їх заповнять пізніше. Дії ставлять паркани (ділять вулицю на квартали), підвищують ціну кварталів певного розміру, будують парки й басейни, змінюють номер на ±1/2 або дублюють сусідній («bis»). Хто не може вписати номер — ставить хрестик відмови; три відмови завершують гру. Ядро — укладання впорядкованої послідовності з дірками під випадковий потік чисел і «трек-апгрейди», що змінюють вартість майбутніх очок.

## Поле і час
- Особистий аркуш: 3 вулиці-ряди будинків (поле `1d` ×3), паркани між будинками, позначки басейнів над деякими будинками, трек парків у кінці кожної вулиці; збоку — треки «нерухомість» (6 колонок за розмірами кварталів 1–6), басейни, тимчасова агенція, bis, відмови, плани міста.
- Будинок — клітина з номером 0–17 або порожня; квартал = 1–6 сусідніх заповнених будинків між двома парканами.
- Хід = одночасний вибір з 3 пар; 81 карта будівництва в 3 стосах по 27; коли стоси скінчились — перетасувати й розкласти знову.
- Гравців від 1 до 12+ на BGA (взаємодія лише через плани міста й агенцію).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Будинок | zone | порожній / номер 0–17 / bis | номер вписують раз; зростання вздовж вулиці |
| Вулиця | zone | 3 штуки; кількість будинків (?) | номери строго зростають, без повторів |
| Паркан | mark | між будинками; крайні — постійні | ділить вулицю на квартали; не ставиться всередину вже зарахованого кварталу |
| Квартал (estate) | zone | 1–6 будинків | зарахований, лише коли всі будинки заповнені й обидва краї — паркани |
| Басейн | terrain | над деякими будинками | дія «басейн» + номер у цьому будинку → хрестик на треку басейнів |
| Парк | mark | трек у кінці вулиці | дія «садівник» → наступне дерево вулиці, куди вписано номер |
| Карта будівництва | supply | номер 1–15 (?) спереду; дія ззаду | пара = номер однієї карти + дія іншої (?) |
| Стос карт | supply | 3 × 27 | щоходу відкривається верх кожного |
| План міста | supply | №1, №2, №3; Project / Approved | набір кварталів заданих розмірів; першим — більше очок |
| Трек нерухомості | mark | 6 колонок | кожен хрестик підвищує ціну кварталу цього розміру |
| Трек тимчасової агенції | mark | лічильник | більшість: 7 / 4 / 1 очко |
| Трек bis | mark | лічильник | у кінці мінус найменше незакреслене число |
| Трек відмов | mark | 3 клітини | третя → кінець гри; штраф |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(all)` → ТО `custom: «відкрити верх кожного з 3 стосів — 3 пари "номер + дія"»`; усі вибирають одночасно, одну пару можуть узяти кілька гравців.
- КОЛИ `input(write(n, house))` → ЯКЩО `free(house)` і `custom: «n більше за всі номери ліворуч і менше за всі праворуч на цій вулиці»` (`+cond:ascending`) → ТО `mark(house, n)`; інакше `block`.
- КОЛИ `custom: «жоден із 3 номерів не можна легально вписати»` → ТО `mark(refusal_box, x)` (`+effect:cross_box`), дію не виконують.
- КОЛИ `counter(refusals, =, 3)` → ТО `game_over` одразу.
- Землемір: КОЛИ `input(action(fence, gap))` → ЯКЩО `not state(estate, used_for_plan)` → ТО `mark(gap, fence)`.
- Агент нерухомості: КОЛИ `input(action(agent, size))` → ТО `counter(estate_value[size], +1)` — `custom: «закреслити найнижчу клітину колонки розміру; квартал цього розміру коштує найменше незакреслене число»`.
- Садівник: КОЛИ `input(action(landscaper))` → ТО `counter(parks[street], +1)` — вулиця, куди щойно вписано номер.
- Басейн: КОЛИ `input(action(pool))` → ЯКЩО `cell(house, pool)` → ТО `counter(pools, +1)`; інакше — нічого.
- Агенція: КОЛИ `input(action(temp))` → ТО `custom: «вписати n±1 або n±2 (у межах 0–17)»`, `counter(temp, +1)`.
- Bis: КОЛИ `input(action(bis, house))` → ЯКЩО `free(house)` і `custom: «сусід ліворуч чи праворуч має номер, між ними нема паркану»` → ТО `mark(house, same + "bis")`, `counter(bis, +1)`.
- Квартал: КОЛИ `pattern(region_closed)` → ЯКЩО `custom: «між двома парканами 1–6 будинків, усі з номерами»` (`+cond:segment_closed`) → ТО квартал завершено.
- План міста: КОЛИ `custom: «є завершені квартали всіх розмірів плану»` (`+trigger:objective_met`) → ЯКЩО `first_time` (перші в цьому ході) → ТО `score(+project)`, `set_state(plan, approved)`; інакше `score(+approved)`; `set_state(estates, used_for_plan)`.
- КОЛИ `custom: «план виконано вперше за гру»` → ТО `choose(reshuffle_or_not)` — `custom: «виконавець може перетасувати всі 81 карту»`.
- КОЛИ `custom: «виконано всі 3 плани»` або `custom: «заповнено всі будинки»` → ТО `game_over` (кінець ходу).
- КОЛИ `custom: «стоси вичерпано»` → ТО `custom: «перетасувати й розкласти 3 нові стоси»`.
- Підрахунок: ТО `score(+plans)` + `score(+parks за треком кожної вулиці)` + `score(+pools за треком)` + `score(+temp: 7/4/1 за більшість)` + `score(+estates: кількість × ціна розміру)` − `score(-bis: найменше незакреслене)` − `score(-refusals)`.
- Перемога: найбільше очок · Тайбрейк: більше кварталів → більше 1-будинкових → 2-будинкових → … · Поразка: — (3 відмови лише завершують гру).

## Керування і ввід
- Паперово: вибрати пару, ручкою вписати номер, закреслити клітину відповідного треку.
- (цифрова версія; BGA) Клік по парі карт → підсвічуються легальні будинки (`legal-move-highlight`) на всіх вулицях; клік по будинку → номер; далі — запит дії: для паркану клік по проміжку, для агента — колонка розміру, для агенції — вибір ±1/±2 перед вписуванням; кнопка «пропустити дію».
- Хід закінчується, коли всі підтвердили; анімація показує, хто що вписав.

## Вікна, меню, HUD
(цифрова версія; BGA)
- `lobby-window` / `match-setup`: кількість гравців, просунутий варіант, експерт-правила, тематичний аркуш (Ice Cream Truck, Christmas Lights, Easter Eggs), соло.
- `game-screen`: свій аркуш (3 вулиці, треки); `card-pairs` — 3 пари «номер + дія»; три плани міста з позначкою, хто виконав першим («1» / «2»); `score-tracks` — бічні треки з поточною ціною; лічильник відмов; `turn-indicator` — хто ще вибирає.
- `sheet-view` (кандидат): клік по імені гравця — його аркуш.
- `end-screen`: таблиця підрахунку за категоріями.
- `help-window`: 6 дій і правило зростання.
- Переходи: lobby-window → game-screen → end-screen.

## Фічі поза полем
- `hotseat` (одночасний вибір на одному столі), `online-multiplayer` (BGA, 1–12).
- `custom-rules`: просунутий варіант (кільцева розвʼязка: ≤2 на гру, ≤1 за хід; додаткові плани №1/№2); експерт-правила (кожен має власні карти, передає їх сусідові); тематичні аркуші — один на партію.
- Соло: окрема карта плану (?) — правила на окремій сторінці.
- `rules-page`, `score-records`.

## Варіації й родичі
- Сиквели й тематичні аркуші: Welcome to New Las Vegas (?), Welcome to the Moon (?), Halloween/Christmas листи.
- Родичі: Railroad Ink, Cartographers, Take It Easy (усі грають той самий потік), Ganz schön clever (roll-and-write з треками), Next Station: London.
- **Осі варіацій**: що вписують (число / фігуру / маршрут) · обмеження послідовності (зростання / сума / без повторів) · джерело чисел (карти-пари / кубики / спільна колода) · штраф за неможливість (хрестик / пропуск) · спільні цілі (перший отримує більше / усі однаково).

## Цікавинки для курсу
- Вулиця як масив з дірками і перевірка «строго зростає з урахуванням порожніх» — 🌱.
- Квартали між парканами: розбиття масиву на сегменти й підрахунок завершених — 📎.
- Треки-апгрейди: кожна дія змінює вартість майбутніх очок (таблиця «закреслено → ціна») — 📎.
- Bis і агенція як модифікатори легальності (дубль сусіда, ±2) — 📎.
- Спільні плани «перший отримує більше» при одночасних ходах — синхронізація ходу — 🥉.
- Детектор «жоден із трьох номерів не лягає» → відмова — 🌱.
- AI-порадник: куди вписати 7, щоб лишити місце для майбутніх чисел (розподіл 81 карти) — 🥇.

## Мапа на каталог
- Є: `cell-click` · `hover-highlight` · `legal-move-highlight` · `simultaneous-versus` ↔ усі грають ті самі карти · `online-multiplayer` · `event-points` · `completion-detection` ↔ квартал/план · `match-setup` · `rule-variants` ↔ просунутий/експерт · `score-records` · `game-screen`, `end-screen`, `help-window`.
- **Нема** → пропозиції карток:
  - `+simultaneous-turns` · `+public-objectives` · `+first-to-achieve-bonus` · `+majority-bonus` — як в інших іграх сімʼї.
  - `+flip-and-write` «Відкрити карти — усі вписують» · game-logic/opponent · 📎.
  - `+pair-choice-market` «Вибір з N пар "значення + дія"» · game-logic/economy · 🌱 · слоти {pairs: 3}.
  - `+ascending-sequence-rule` «Значення в ряду строго зростають, дірки дозволені» · entities/legality · 🌱.
  - `+gap-fill-later` · `+fence-split-segments` «Паркани ділять ряд на сегменти» · game-logic/constraints · 📎.
  - `+segment-size-scoring` · `+upgrade-track` · `+escalating-track-score` — очки за треками · game-logic/score · 📎.
  - `+number-modifier` (±2) · `+duplicate-neighbor` (bis) · 🌱.
  - `+strike-penalty-track` «Хрестики відмов, N → кінець» · game-logic/lose · 🌱.
  - `+multi-end-trigger` · `+deck-reshuffle` · `+tiebreak-chain` — по 🌱.

## Пропозиції до словників
- `+cond:ascending` — значення в ряду строго зростають (з урахуванням порожніх клітин).
- `+cond:segment_closed` — сегмент між двома межами повністю заповнений.
- `+effect:cross_box` — закреслити наступну клітину треку (roll-and-write: Welcome To, Ganz schön clever, Cartographers).
- `+trigger:objective_met` — виконано спільну/особисту ціль.
- `+role:objective` — ціль-карта поза полем (план міста, спільні цілі Next Station).
- `+ui:score-tracks` — бічні треки з поточною ціною категорій.
- `+ui:card-pairs` — 3 пари «номер + дія» на вибір.
- `+window:sheet-view` — перегляд аркуша іншого гравця.
- `+feature:themed-sheets` — альтернативні аркуші з іншими діями (один на партію).
- `+card:ascending-sequence-rule` · `+card:fence-split-segments` · `+card:strike-penalty-track` · `+card:pair-choice-market` — див. «Мапа на каталог».

## Джерела
- ⭐ [UltraBoardGames: Welcome To rules](https://www.ultraboardgames.com/welcome-to/game-rules.php) — 81 карта в 3 стосах, 29 планів, правило зростання, відмови, 6 дій, квартали 1–6, плани (Project/Approved), три умови кінця, підрахунок, тайбрейки.
- [BGA: Welcome To](https://en.boardgamearena.com/gamepanel?game=welcometo) — 1–12 гравців, просунутий варіант (кільцева розвʼязка), експерт-правила, тематичні аркуші, інтерфейс.
- [RulesPal: rulebook](https://rulespal.com/welcome-to/rulebook) — не відкривав.
- BGG: [пошук](https://boardgamegeek.com/geeksearch.php?action=search&q=Welcome+To); YouTube: пошук «Welcome To board game how to play».

## Непевне
- (?) Кількість будинків на вулицях (10 / 11 / 12 — з памʼяті), позиції басейнів і довжина треків парків — джерела не дають.
- (?) Як саме формується пара: номер з лицьового боку відкритої карти + дія зі звороту наступної карти стосу — з памʼяті; UBG каже лише «комбінація номера й дії».
- (?) Діапазон номерів на картах (1–15), вартості кварталів за колонками і штраф за відмови (0 / −3 / −5) — не бачив.
- (?) Соло-правила, кільцева розвʼязка в деталях, сиквели — на окремих сторінках, не відкривав.
- (?) Мобільний застосунок (?) — не перевіряв.
