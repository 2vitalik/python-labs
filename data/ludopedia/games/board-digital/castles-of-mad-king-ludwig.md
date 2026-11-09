---
title: Castles of Mad King Ludwig (Замки божевільного короля Людвіга)
slug: castles-of-mad-king-ludwig
aka: [Замки божевільного короля Людвіга, CoMKL, Castles of Mad King Ludwig 2nd Edition]
family: board-digital
also: [build-sim]
klass: cursor
axes:
  field: free
  time: turn
  opponent: hotseat
  info: partial
  random: setup
  goal: score
year: 2014
platforms: [board]
links:
  - {kind: other, url: "https://officialgamerules.org/game-rules/castles-of-mad-king-ludwig/", best: true, note: "правила: компоненти, сетап за кількістю гравців, фази раунду, Майстер-будівельник, викладання кімнат, порядок підрахунку, нагороди за завершення за типами, фінал, соло"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Ted_Alspach", note: "автор Ted Alspach: 2014, Bézier Games, Mensa Select, Secrets (2015), 2-ге видання (2023)"}
  - {kind: official, url: "https://beziergames.com/products/castles-of-mad-king-ludwig", note: "сторінка видавця (при відкритті 429)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Castles+of+Mad+King+Ludwig+how+to+play", note: "пошук; як грати"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=Castles+of+Mad+King+Ludwig", note: "пошук BGG"}
stage: v1
coverage: 50
mechanics: [drag-drop-piece, piece-rotate-flip, hover-highlight, legal-move-highlight, multi-cell-size, event-points, turn-enforcement, hot-seat, ai-opponent, match-setup, end-screen, help-window, save-game, pass-device, +seller-sets-prices, +door-connection-placement, +room-completion-reward, +room-type-adjacency-score, +adjacency-penalty, +majority-bonus, +secret-bonus-cards, +stairs-to-lower-level, +keep-external-entrance, +rescore-room, +extra-turn-reward, +market-refill-from-deck, +depleted-stack-bonus, +tiebreak-by-area]
proposes: ["+trigger:area_complete", "+trigger:placed", "+cond:doors_connected(room)", "+cond:edge_match", "+cond:level(room, upstairs|downstairs)", "+effect:rescore(room)", "+effect:set_price(item, slot)", "+role:room", "+role:door", "+role:supply", "+ui:price-board", "+ui:favor-track", "+window:market-pricing", "+card:seller-sets-prices", "+card:room-completion-reward"]
author: opus
date: 2026-11-09
---

# Castles of Mad King Ludwig — по черзі призначаєш ціни на кімнати для інших і будуєш власний замок з кімнат-тайлів, зʼєднаних дверима

## Суть
Кожен гравець будує свій замок з тайлів-кімнат різної форми й площі, що дотикаються **дверними прорізами**. Ролі Майстра-будівельника по колу: він розкладає доступні кімнати на ціновій шкалі, інші купують у нього (гроші йдуть йому), а сам він купує останнім і платить банку. Кожна кімната дає очки одразу: базові, плюс/мінус за сусідні типи кімнат; коли всі двері кімнати зʼєднані, вона «завершена» й дає нагороду свого типу. Наприкінці — таємні бонус-картки й королівські милості за більшість.

## Поле і час
- Поле — вільна площина без сітки, але тайли кімнат прямокутні, круглі й фігурні з прорізами на краях; повороти на 90°. Фактично — сітка з кроком у сторону тайла (?).
- Два рівні: наземний (з фойє) і підвал (`downstairs`); підвальні кімнати зʼєднуються з наземними лише через сходи.
- Раунд: фаза Майстра (поповнити й оцінити кімнати) → фаза купівлі (від лівого сусіда Майстра, по одній покупці або пас) → викладання й підрахунок одразу → Майстер переходить за годинниковою стрілкою.
- Інформація: замки й ринок відкриті; бонус-картки (2 на старті) приховані; стоси тайлів закриті.
- Кінець: після раунду, у якому вичерпалась колода карток кімнат.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фойє | static | стартове | перша кімната кожного гравця |
| Кімната | tile | тип, площа 100–600, базові очки, іконки | кладеться дверима до дверей; рахується одразу |
| Двері (проріз) | static | на краю кімнати | зʼєднання = двері до дверей; усі зʼєднані → кімната завершена |
| Житлова (living) | tile | тип | завершення: перерахувати цю кімнату ще раз |
| Розважальна (activity) | tile | тип | завершення: +5; штраф за деяких сусідів |
| Спальня (sleeping) | tile | тип | завершення: переглянути й переставити стос тайлів |
| Надвірна (outdoor) | tile | огороджений край | завершення: +1 000 грошей; не можна класти огородженим краєм до кімнати |
| Службова (utility) | tile | тип | завершення: взяти 2 бонус-картки, лишити 1 |
| Їдальня (food) | tile | тип | завершення: додатковий хід |
| Коридорна (corridor) | tile | тип | завершення: безкоштовний коридор або сходи |
| Підвальна (downstairs) | tile | рівень −1 | за кожні 2 завершені — перерахувати будь-яку кімнату |
| Коридор / підвальний коридор | tile | 1 000 грошей | двобічний тайл, зʼєднувач |
| Сходи | tile | 1 000 грошей | темний кінець — до підвальної кімнати або коридору |
| Майстер-будівельник | player | роль по колу | ставить ціни; гроші за покупки інших — йому |
| Дошка контрактів | zone | цінові слоти | одна кімната на слот, без повторів |
| Королівська милість | objective | більшість | фінальні очки за лідерство в категорії |
| Бонус-картка | objective | прихована | фінальні очки за умову |
| Гроші | resource | 15 000 на старті | 1 очко за 10 000 наприкінці |

## Правила (КОЛИ → ЯКЩО → ТО)
- Ринок: КОЛИ `turn_start(master)` → ТО `custom: «доповнити дошку контрактів картками кімнат»` + `custom: «Майстер ставить кожну кімнату на свій ціновий слот, без повторів»`; на двох слот 2 000 не діє.
- Купівля в Майстра: КОЛИ `input(custom: «купити кімнату»)` → ЯКЩО `has(p, price)` and `custom: «кімнату можна легально покласти»` → ТО `take(p, price)` + `give(master, price)`; Майстер у свій хід платить банку.
- Коридор / сходи: КОЛИ `input(custom: «купити коридор або сходи»)` → ЯКЩО `has(p, 1000)` → ТО `take(p, 1000)` у банк.
- Пас: КОЛИ `input(custom: «пас»)` → ТО `pass_turn`.
- Викладання: КОЛИ `input(place(room))` → ЯКЩО `custom: «хоча б одні двері збігаються з дверима наявної кімнати»` and `custom: «без накладання»` → ТО `place(room)`; повороти — `rotate(room, 90)`.
- Надвірна: ЯКЩО `custom: «огороджений край торкається кімнати»` → ТО `block`.
- Підвал: ЯКЩО `custom: «кімната підвальна»` → ТО `custom: «зʼєднання з наземним рівнем лише через сходи»`.
- Вихід назовні: ЯКЩО `custom: «після викладання в замку не лишилось жодних вільних зовнішніх дверей»` → ТО `block`.
- Підрахунок 1: КОЛИ `custom: «кімнату покладено»` → ТО `score(n)` — базові очки з іконки замку.
- Підрахунок 2: ТО `score(±n)` за іконки в центрі кімнати — за суміжні/зʼєднані типи кімнат.
- Підрахунок 3: ЯКЩО `custom: «поруч розважальна кімната»` → ТО `score(−n)` — штраф сусідства.
- Підрахунок 4: ТО `score(n)` — бонуси «за зʼєднаний тип кімнати» в інших кімнатах.
- Завершення: КОЛИ `custom: «усі двері кімнати зʼєднані»` → ТО нагорода типу: living — `custom: «перерахувати»` · activity — `score(5)` · sleeping — `custom: «переглянути стос тайлів»` · outdoor — `currency(+1000)` · utility — `choose(2 bonus cards → 1)` · food — `extra_move` · corridor — `give(p, hallway|stairs)` · downstairs — `custom: «за кожні 2 — перерахувати кімнату»`.
- Вичерпаний стос: КОЛИ `custom: «стос тайлів певної площі закінчився»` → ТО `custom: «фінально +2 за кожну кімнату з цього стосу»`.
- Фінал: КОЛИ `custom: «колода карток кімнат вичерпана»` → ТО `custom: «дограти раунд»` → `game_over`.
- Фінальні очки: королівські милості (більшість) · бонус-картки · `score(1)` за кожні 10 000 · вичерпані стоси.
- Перемога: найбільше очок · нічия — більша загальна площа замку.
- Соло: 3 картки щоходу на слоти 2 000 / 4 000 / 6 000, некуплене прибирається; без милостей; ранг за очками.

## Керування і ввід
- Майстер: drag кімнат з ринку на цінові слоти, підтвердження цін.
- Покупець: клік по кімнаті на дошці контрактів → режим викладання: drag + поворот на 90°, підсвітка легальних позицій (двері до дверей, без накладань), перемикач рівня «наземний / підвал».
- Прев'ю очок до підтвердження (цифрова версія).

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Нова гра → `match-setup` · Соло · Правила → `help-window`.
- `match-setup`: 1–4 гравці, люди/AI.
- `market-pricing` (кандидат): Майстер розставляє кімнати на цінових слотах.
- `game-screen`: дошка контрактів з цінами (`price-board`, кандидат), свій замок з двома рівнями, `favor-track` (кандидат: королівські милості й лідери), рахунок і гроші, `turn-indicator`, приховані бонус-картки.
- `opponent-boards` — замки суперників.
- `end-screen`: милості, бонуси, гроші, стоси, тай-брейк площею; соло — ранг.
- Переходи: main-menu → match-setup → game-screen ⇄ market-pricing → end-screen.

## Фічі поза полем
- `hotseat` 2–4 з `pass-device` для прихованих бонус-карток; соло-режим з рангами.
- `custom-rules`: доповнення Secrets (2015) (?); 2-ге видання (2023).

## Варіації й родичі
- Родичі: The Palace of Mad King Ludwig (2017), Between Two Castles of Mad King Ludwig (2018, драфт кімнат на двох сусідів).
- Тайли з зʼєднувачами на краях: [carcassonne](carcassonne.md) (ребра мусять збігатись), [railroad-ink](railroad-ink.md), [galaxy-trucker](galaxy-trucker.md) (конектори модулів), [the-isle-of-cats](the-isle-of-cats.md) (заповнення кімнат).
- Ринок із ціною від гравця: [acquire](acquire.md) (акції), [alhambra](alhambra.md) (ринок будівель і валюти).
- Облаштування приміщень з бонусами: [caverna](caverna.md).
- **Осі варіацій**: хто ставить ціну (гравець-продавець / фіксована / аукціон) · зʼєднання (двері до дверей / ребро до ребра) · рівні (один / наземний + підвал) · нагорода за завершення (за типом / однакова) · фінальні цілі (приховані / спільні більшості).

## Цікавинки для курсу
- Тайли з дверима на краях і перевірка «хоча б одні двері до дверей, без накладань» на вільній площині з кроком сітки — 🥉.
- Завершення кімнати як «усі прорізи зʼєднані» і таблиця нагород за типом — 📎.
- Підрахунок суміжності: іконки «+n за кожну сусідню кімнату типу X» і штрафи — 📎.
- Ринок, де продавець — гравець: ціну ставить Майстер, гроші йдуть йому, сам платить банку — 🌱.
- Два рівні замку зі сходами як порталом між шарами — 📎.
- AI Майстра: розставити ціни так, щоб суперники не взяли найкраще — 🥇.

## Мапа на каталог
- Є: `drag-drop-piece` · `piece-rotate-flip` · `hover-highlight` · `legal-move-highlight` · `multi-cell-size` (кімнати різної площі) · `event-points` · `turn-enforcement` · `hot-seat` · `ai-opponent` · `match-setup` · `end-screen` · `help-window` · `save-game`.
- Є: `pass-device` (приховані бонус-картки в hot-seat).
- Уже в корпусі: `+majority-bonus` (королівські милості).
- **Нема** → пропозиції карток:
  - `+seller-sets-prices` «Гравець-продавець ставить ціни, гроші — йому» · game-logic/economy · 🌱 · слоти {slots: [1000…], no_dup: true}.
  - `+door-connection-placement` «Тайл кладеться прорізом до прорізу» · entities/legality · 🥉.
  - `+room-completion-reward` «Усі прорізи зʼєднані → нагорода типу кімнати» · game-logic/score · 📎.
  - `+room-type-adjacency-score` «Очки за суміжні типи кімнат» · game-logic/score · 📎.
  - `+adjacency-penalty` «Штраф за небажаного сусіда» · game-logic/score · 🌱.
  - `+stairs-to-lower-level` «Сходи — єдиний перехід між рівнями» · entities/legality · 📎.
  - `+keep-external-entrance` «Конструкція мусить лишати вільний зовнішній вхід» · entities/legality · 🌱.
  - `+rescore-room` «Повторно нарахувати очки обʼєкта» · game-logic/score · 🌱.
  - `+extra-turn-reward` «Нагорода — додатковий хід» · game-logic/turns · 🌱.
  - `+market-refill-from-deck` «Ринок поповнюється з колоди» · game-logic/economy · 🌱.
  - `+depleted-stack-bonus` «Бонус за обʼєкти з вичерпаного стосу» · game-logic/score · 🌱.
  - `+tiebreak-by-area` «Нічия — за загальною площею» · game-logic/win · 🌱.
  - `+secret-bonus-cards` «Приховані картки фінальних бонусів, вибір 2 з 3» · game-logic/score · 🌱.

## Пропозиції до словників
- `+trigger:area_complete` — область/кімната завершена (усі виходи зʼєднані).
- `+trigger:placed` — тайл щойно покладено (підрахунок одразу).
- `+cond:doors_connected(room)` — усі прорізи кімнати мають пару.
- `+cond:edge_match` — край тайла збігається з сусіднім (двері до дверей).
- `+cond:level(room, upstairs|downstairs)` — рівень кімнати.
- `+effect:rescore(room)` — повторний підрахунок.
- `+effect:set_price(item, slot)` — гравець призначає ціну.
- `+role:room` · `+role:door` · `+role:supply`.
- `+ui:price-board` · `+ui:favor-track`.
- `+window:market-pricing`.
- `+card:seller-sets-prices` · `+card:room-completion-reward`.

## Джерела
- ⭐ [Official Game Rules: Castles of Mad King Ludwig](https://officialgamerules.org/game-rules/castles-of-mad-king-ludwig/) — компоненти й номінали тайлів, сетап за кількістю гравців, три фази раунду, правила викладання, порядок підрахунку, нагороди за завершення за типами, фінал, тай-брейк, соло.
- [Wikipedia: Ted Alspach](https://en.wikipedia.org/wiki/Ted_Alspach) — 2014, Bézier Games, Mensa Select, Secrets (2015), Palace (2017), 2-ге видання (2023).
- [Bézier Games](https://beziergames.com/products/castles-of-mad-king-ludwig) — сторінка видавця (429 при відкритті).
- BGG: [пошук](https://boardgamegeek.com/geeksearch.php?action=search&q=Castles+of+Mad+King+Ludwig); YouTube: пошук «how to play».

## Непевне
- (?) Повна шкала цінових слотів Майстра (1 000…15 000?) — сторінка перелічує лише слот 2 000 і соло-слоти 2 000/4 000/6 000.
- (?) Значення іконок кімнат, штрафів сусідства й королівських милостей — у джерелі не наведено.
- (?) Чи зʼєднання дверей вимагає точного збігу прорізів чи лише суміжності — сторінка: «хоча б один вхід зʼєднаний з входом іншої кімнати».
- (?) Цифрова версія: у Steam лише Between Two Castles; мобільна версія Castles (Bézier) — з памʼяті, не перевірено. Вікна гіпотетичні.
