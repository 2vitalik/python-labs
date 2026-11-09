---
title: Alphabear
slug: alphabear
aka: [Alphabear: Hardcover Edition, Alphabear 2]
family: word-number
also: [board-digital]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: hidden
  random: runtime
  goal: score
year: 2015
platforms: [iOS, Android, macOS, Windows]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Alphabear", best: true, note: "суть: використана плитка відкриває сусідів, невикористані кам'яніють, ведмеді-бонуси, мед, звичайні й timed-пазли"}
  - {kind: official, url: "https://www.spryfox.com/our-games/alphabear/", note: "ведмеді на очищеному місці, сила ведмедів, Hardcover-видання"}
  - {kind: other, url: "https://www.destructoid.com/review-alphabear/", note: "огляд: лічильники, камінь, ріст ведмедя лише повним прямокутником, зірка/череп, рівні ведмедів, фрази зі слів"}
  - {kind: other, url: "http://www.148apps.com/news/alphabear-tips-tricks-and-strategies-to-bear-all-that-you-can-bear/", note: "поради: 3 ведмеді на гру, дублікати підсилюють, очки за залишок часу, мед і монети"}
  - {kind: other, url: "https://games.jayisgames.com/review/alphabear.php", note: "огляд: кінець гри — поле без літер, нагорода за ціль рівня, cooldown ведмедів, бос-рівні"}
  - {kind: other, url: "https://www.pocketgamer.com/articles/078593/alphabear-2-review/", note: "огляд Alphabear 2 (бачено в пошуку)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=alphabear+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [cell-click, word-validation, event-points, character-select, level-unlock, sequential-levels, mode-select, game-screen, end-screen, shop-window, share-result, save-progress, +reveal-adjacent-on-use, +tile-countdown-decay, +rectangle-growth-zone, +booster-loadout, +duplicate-upgrade, +booster-cooldown, +energy-play-limit, +random-reward-drop, +word-sentence-share, +marked-cell-modifier]
proposes: ["+cond:rectangle_full", "+effect:decay", "+ui:tile-countdown", "+window:collection-window", "+feature:energy-regen", "+feature:booster-loadout", "+feature:prestige"]
author: opus
date: 2026-11-09
---

# Alphabear — склади слово з відкритих літер; використані плитки відкривають сусідів, невикористані кам'яніють, а на розчищеному ростуть ведмеді

## Суть
Поле — сітка, де спершу відкрита лише частина літер. Гравець складає слово з відкритих плиток; використані плитки зникають, а сусідні клітини відкривають нові літери. Кожна відкрита літера має лічильник ходів: не вжив вчасно — вона стає каменем, що займає місце. На розчищених клітинах виростає ведмідь, але розширюється він лише повним прямокутником, тож камінь посеред поля «ріже» фінального ведмедя. Звідси ядро: довге слово дає більше очок зараз, але відкриває забагато нових літер, які можна не встигнути вжити.

## Поле і час
- Квадратна сітка змінного розміру й форми; розкладка поля визначає стратегію (різні дошки).
- Шари: клітина (закрита / відкрита літера / камінь / очищена під ведмедя) + позначки зірка/череп + лічильник на кожній літері.
- Хід = одне слово; після ходу всі невикористані відкриті літери −1 до лічильника.
- Гра закінчується, коли на полі не лишилось літер (усі вжиті або скам'яніли).
- Режими: звичайні й timed-пазли (Alphabear 2 — етапи з лімітом часу).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Закрита клітина | tile | прихована літера | відкривається, коли сусідню плитку вжито в слові |
| Плитка-літера | tile | літера, лічильник ходів | у слові → зникає; щоходу без вжитку лічильник −1; що більше лишилось, то більше очок |
| Червона плитка | tile | лічильник = останній хід | попередження: наступний хід без вжитку → камінь |
| Камінь | static | — | невживна, займає клітину, не дає ведмедю рости крізь себе |
| Очищена клітина | zone | — | місце під ведмедя |
| Ведмідь на полі | zone | розмір (площа прямокутника) | росте, коли очищене утворює повний прямокутник; розмір → очки в кінці |
| Клітина-зірка | terrain | — | літера, що тут відкриється, має незвично великий лічильник |
| Клітина-череп | terrain | — | літера тут має незвично малий лічильник |
| Ведмідь-підсилювач | ally | сила, рівень, cooldown | до 3 на гру: бонус за літери/слова, множник, частота або довговічність літер, +час |
| Мед | resource | регенерує з часом | плата за кожну партію |
| Монети ведмедів | resource | — | купити мед, розбудити ведмедя, відкрити спеціальні рівні |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(tap tile)` → ЯКЩО `state(tile, revealed)` → ТО `custom: «літера додається в кінець слова»`.
- КОЛИ `input(submit)` → ЯКЩО `in_dictionary(word)` → ТО `score(custom: «Σ вартостей літер; вартість спадає з лічильником»)`, `clear(word tiles)`; інакше `block`.
- КОЛИ `after(clear)` → ТО `reveal(adjacent closed cells)`, `spawn_at(bear, cleared cells)`.
- КОЛИ `after(reveal)` → ЯКЩО `occupied(cell, star)` → ТО `set_value(countdown, high)`.
- КОЛИ `after(reveal)` → ЯКЩО `occupied(cell, skull)` → ТО `set_value(countdown, low)`.
- КОЛИ `turn_end` → ТО `counter(countdown, -1)` для кожної відкритої невживаної літери.
- КОЛИ `counter(countdown, ==, 1)` → ТО `set_state(tile, red)`.
- КОЛИ `counter(countdown, ==, 0)` → ТО `transform(tile, stone)`.
- КОЛИ `after(clear)` → ЯКЩО `custom: «ведмідь разом із сусідніми очищеними клітинами утворює повний прямокутник»` → ТО `grow(bear, n)`.
- КОЛИ `after(clear)` → ЯКЩО `occupied(cell, stone)` у прямокутнику росту → ТО `block` — камінь обмежує ведмедя.
- КОЛИ `input(submit)` → ЯКЩО `has(team, bear)` і `custom: «слово / літера під бонус ведмедя»` → ТО `score(+bonus)` або `multiplier(×k)`.
- КОЛИ `all_gone(letter tile)` → ТО `score(custom: «за розмір ведмедів: один великий вигідніший за два менших»)`, `multiplier(final, bears)`.
- КОЛИ `level_end` → ЯКЩО `counter(score, >=, par)` → ТО `give(player, random bear)`; ЯКЩО `counter(score, >=, gold)` → ТО `custom: «шанс на рідкісного ведмедя»`.
- КОЛИ `picked(player, bear)` → ЯКЩО `has(player, same bear)` → ТО `custom: «рівень ведмедя +1, його множник росте»`.
- КОЛИ `level_end` → ЯКЩО `custom: «використано потужного ведмедя»` → ТО `set_state(bear, napping, dur)` — до кількох годин.
- КОЛИ `level_start` → ЯКЩО `counter(honey, <, cost)` → ТО `block`; інакше `currency(-cost)`.
- КОЛИ `timer(every)` → ТО `currency(+honey)`; також мед за перегляд відео або обмін монет.
- КОЛИ `level_end` → ТО `message(custom: «новий ведмідь складає фрази зі слів партії»)`.
- Перемога: набрати ціль рівня (par / gold) · Поразка: окремої нема — замалий рахунок без нагороди · Рахунок: слова + ведмеді + множники ведмедів-підсилювачів.

## Керування і ввід
- Тап по відкритих літерах по черзі — слово; кнопка підтвердження й скасування (?).
- Перед рівнем — вибір до трьох ведмедів-підсилювачів.
- PC/Mac (Hardcover) — миша; словник у грі в реальному часі.

## Вікна, меню, HUD
- `game-screen`: поле з лічильниками на літерах (`tile-countdown`), кольори тривоги на малих лічильниках, поточне слово, рахунок, обрані ведмеді, `energy-bar` меду зверху ліворуч.
- `map-window` / `level-select`: глави й дошки, частина відкривається щодня; бос-рівні; спеціальні рівні за монети (у т. ч. treasure challenges).
- `character-select`: вибір 3 ведмедів, зі станом «спить» і cooldown.
- `collection-window`: колекція ведмедів з рівнями.
- `end-screen`: рахунок проти par/gold, отриманий ведмідь, фрази зі слів — поділитись.
- `shop-window`: мед, безлімітний мед за разовий платіж.
- Переходи: мапа → вибір ведмедів → гра → результат → мапа.

## Фічі поза полем
- Прогресія: глави, `level-unlock`, нагорода-ведмідь за ціль, дублікати підсилюють; Hardcover — `prestige` для кампанії.
- `energy-regen`: мед обмежує кількість партій поспіль.
- `booster-loadout`: до 3 підсилювачів з cooldown-сном.
- Режими: звичайні та на час.
- `share-result`: картинка з ведмедем і «дурними» фразами зі слів партії.
- Hardcover (PC/Mac): без IAP і реклами, перебалансування, вбудований словник.

## Варіації й родичі
- Panda Poet (2010, Spry Fox) — попередник; Alphabear 2 (2018) — етапи з таймером, нова мета.
- Родичі: [scrabble.md](scrabble.md) (рука літер), [letterpress.md](letterpress.md) (слово змінює поле), [spelltower.md](spelltower.md) (тиск поля), [bananagrams.md](bananagrams.md).
- **Осі варіацій:** як відкривається поле (сусіди вжитого / все видно) · тиск (лічильник плитки / таймер / ряд знизу) · що дає розчищене (площа-ведмідь / нічого) · підсилювачі (ведмеді з рівнями / нема).

## Цікавинки для курсу
- Відкриття сусідів вжитої плитки + приховані літери — 🌱.
- Лічильник життя на кожній плитці, червоний стан, перетворення на камінь — 📎.
- Ріст зони лише повним прямокутником, найбільший прямокутник без каменів — 🥉 (задача «максимальний прямокутник у бінарній матриці»).
- Ризик-баланс: довге слово відкриває більше літер, ніж встигнеш ужити — 🌱.
- Ведмеді-підсилювачі: вибір 3, рівні від дублікатів, cooldown у реальному часі — 📎.
- Фрази зі слів партії для поділитися — 📎.

## Мапа на каталог
- Є: `cell-click` ↔ тап по літері · `word-validation` · `event-points` ↔ вартість літер · `character-select` ↔ вибір ведмедів · `level-unlock` / `sequential-levels` ↔ глави · `mode-select` ↔ звичайні / на час · `share-result` ↔ фрази · `shop-window` ↔ мед · `save-progress` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+reveal-adjacent-on-use` «Вжита плитка відкриває сусідні клітини» · entities/interact · 🌱.
  - `+tile-countdown-decay` «Плитка з лічильником ходів → камінь» · entities/state · 📎 · слоти {start, on_zero}.
  - `+rectangle-growth-zone` «Зона росте лише повним прямокутником» · entities/state · 🥉.
  - `+booster-loadout` «До N підсилювачів перед рівнем» · game-logic/economy · 📎 · слоти {slots}.
  - `+duplicate-upgrade` «Дублікат підсилює наявне» · game-logic/economy · 🌱.
  - `+booster-cooldown` «Підсилювач спить N годин після вжитку» · game-logic/economy · 📎.
  - `+energy-play-limit` «Енергія на партію з регенерацією» · game-logic/economy · 📎.
  - `+random-reward-drop` «Випадкова нагорода за ціль рівня» · levels/progression · 🌱.
  - `+word-sentence-share` «Фрази зі слів партії» · interface/results · 📎.
  - `+marked-cell-modifier` «Позначена клітина змінює параметр того, що в ній зʼявиться» · entities/spawn · 🌱.

## Пропозиції до словників
- `+cond:rectangle_full` — набір клітин утворює повний прямокутник (ріст ведмедя).
- `+effect:decay` — лічильник сутності спадає щоходу (є в index/proposals — Block'hood, Screeps).
- `+ui:tile-countdown` — число-лічильник на плитці з кольором тривоги.
- `+window:collection-window` — колекція зібраних сутностей з рівнями.
- `+feature:energy-regen` — енергія на партію, що відновлюється з часом; `+feature:booster-loadout` — слоти підсилювачів перед рівнем; `+feature:prestige` — повторне проходження кампанії з бонусами.

## Джерела
- ⭐ [Wikipedia: Alphabear](https://en.wikipedia.org/wiki/Alphabear) — ядро, мед, до 3 ведмедів, сон ведмедів, режими, платформи й дати.
- [Spry Fox: Alphabear](https://www.spryfox.com/our-games/alphabear/) — сили ведмедів, Hardcover-видання.
- [Destructoid: огляд](https://www.destructoid.com/review-alphabear/) — прямокутники, камінь, зірка/череп, рівні ведмедів, фрази.
- [148Apps: поради](http://www.148apps.com/news/alphabear-tips-tricks-and-strategies-to-bear-all-that-you-can-bear/) — очки за залишок часу, дублікати, мед.
- [JayIsGames: огляд](https://games.jayisgames.com/review/alphabear.php) — кінець гри, нагороди, бос-рівні.
- YouTube: пошук «alphabear gameplay».

## Непевне
- (?) Чи мають літери слова бути суміжними — джерела кажуть «tap available letters», тобто, схоже, ні.
- (?) Мінімальна довжина слова, точна формула очок і множника ведмедів.
- (?) Як саме очищена клітина стає ведмедем: Destructoid — «вжита плитка стає ведмедем», інші — «ведмеді ростуть у розчищеному місці».
- (?) Що відбувається в timed-режимі, коли час вийшов.
- (?) Деталі Alphabear 2 понад етапи з таймером.
