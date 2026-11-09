---
title: Alhambra (Альгамбра)
slug: alhambra
aka: [Альгамбра, Der Palast von Alhambra]
family: board-digital
also: []
klass: cursor
axes:
  field: square
  time: turn
  opponent: hotseat
  info: hidden
  random: runtime
  goal: score
year: 2003
platforms: [board]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Alhambra_(board_game)", best: true, note: "правила коротко: 4 валюти, 3 дії, точна оплата, стіни й фонтан, 3 підрахунки, найдовша стіна, Дірк для двох, доповнення"}
  - {kind: other, url: "https://www.ultraboardgames.com/alhambra/game-rules.php", note: "повні правила: компоненти, ринок, резерв, правила викладання, підрахунки 1–3 місць, кінець"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=Alhambra", note: "пошук BGG"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Alhambra", note: "пошук Steam"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Alhambra+board+game+how+to+play", note: "пошук; пояснення правил"}
stage: v1
coverage: 65
mechanics: [cell-click, drag-drop-piece, hover-highlight, legal-move-highlight, reachability-check, connectivity-check, impassable-cells, turn-enforcement, hot-seat, pass-device, ai-opponent, event-points, round-currency, match-setup, end-screen, help-window, +multi-currency-market, +exact-payment-bonus, +tile-reserve-slots, +connected-placement, +wall-edge-match, +no-enclosed-holes, +majority-bonus, +scoring-card-in-deck, +longest-wall-scoring, +dummy-player, +bag-draw-refill]
proposes: ["+cond:afford", "+cond:exact_pay", "+cond:no_holes", "+cond:edge_match", "+trigger:scoring_card", "+effect:buy", "+effect:to_reserve", "+ui:currency-market", "+ui:building-market", "+ui:reserve-board", "+ui:majority-table", "+window:scoring-round", "+card:exact-payment-bonus", "+card:no-enclosed-holes", "+card:scoring-card-in-deck", "+card:dummy-player"]
author: opus
date: 2026-11-09
---

# Alhambra — купуй будівлі за чотири валюти й прибудовуй до свого палацу так, щоб до кожної можна було дійти від фонтану, не перетинаючи стін

## Суть
На ринку чотири будівлі, кожна — за свою валюту (слот ринку = валюта). За хід — одна дія: взяти гроші, купити будівлю або перебудувати палац. Решти не дають, а **точна оплата дає ще одну дію**. Будівлі мають стіни на частині сторін; викладати можна лише так, щоб стіни на спільних краях збігались, до плитки можна було дійти від фонтану без перетину стін і щоб не лишалось замкнених дір. Очки — за більшість кожного типу будівель у трьох підрахунках і за найдовшу зовнішню стіну.

## Поле і час
- Особистий палац — необмежена квадратна сітка, що росте від стартового фонтану; плитки не повертаються (усі «прямо», як фонтан).
- Поза палацом — резерв без ліміту: куплене можна відкласти й пізніше вбудувати.
- Спільні ринки: валюти (4 карти лицем догори) і будівель (4 слоти з валютою кожен).
- Хід = одна дія (з ланцюгом додаткових за точну оплату, до 5 за хід); наприкінці ходу ринки дозаповнюються до 4.
- Час гри: колода грошей у 5 стосах; дві картки підрахунку вкладені в 2-й і 4-й — їхня поява запускає підрахунки 1 і 2; третій — у кінці.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фонтан (стартова плитка) | static | 1 на гравця | корінь палацу; не прибирається й не міняється |
| Плитка будівлі | tile | тип (6 видів), ціна, стіни на 0–3 сторонах (?) | купується в слоті ринку; кладеться в палац або резерв |
| Стіна | static | сторона плитки | непрохідна для шляху від фонтану; стіна ↔ стіна на спільних краях |
| Ринок будівель | zone | 4 слоти, кожен — валюта | дозаповнюється з мішка наприкінці ходу |
| Ринок валют | zone | 4 карти | дозаповнюється з колоди |
| Карта грошей | resource | валюта ×4, номінал | у руці прихована; витрачається без решти |
| Картка підрахунку | object | 1-ша / 2-га | у колоді грошей; поява → підрахунок |
| Мішок плиток | supply | 54 плитки | неможливо дозаповнити ринок → кінець гри |
| Резерв | supply | без ліміту | місце для відкладених плиток; у підрахунку не рахується |
| Дірк | neutral | лише у грі на двох | уявний третій гравець: отримує будівлі, рахує більшість, без стін |

## Правила (КОЛИ → ЯКЩО → ТО)
- Старт: КОЛИ `game_start` → ТО `custom: «роздати гроші, доки сума в руці ≥ 20»`; починає той, у кого найменше карт (рівність — менша сума).
- КОЛИ `turn_start(p)` → ТО `choose(take_money | buy | redesign)` — одна дія.
- Гроші: КОЛИ `input(take(cards))` → ЯКЩО `custom: «1 карта будь-якого номіналу або кілька з сумою ≤ 5»` → ТО `give(p, cards)`.
- Купівля: КОЛИ `input(buy(tile, slot))` → ЯКЩО `custom: «сума карт валюти слоту ≥ ціни»` → ТО `take(p, cards)` і `give(p, tile)`; решти нема.
- КОЛИ `custom: «оплачено купівлю»` → ЯКЩО `custom: «сума = ціні точно»` → ТО `extra_move`; ланцюг до 5 дій за хід.
- Перебудова: КОЛИ `input(redesign)` → ТО `custom: «резерв → палац, палац → резерв або обмін плитки резерву з плиткою палацу на тому ж місці»`; фонтан не чіпається.
- Викладання: КОЛИ `input(place(tile, cell))` → ЯКЩО `free(cell)` and `custom: «≥1 повна спільна сторона з палацом»` and `custom: «на кожному спільному краю обидві сторони зі стіною або обидві без»` and `path_exists(fountain, cell)` (не перетинаючи стін і не виходячи з плиток) and `custom: «не утворюється замкнена порожня клітина»` → ТО `place(tile)`; інакше `block` → лише в резерв.
- Куплене кладеться наприкінці ходу, після перебудови.
- КОЛИ `turn_end(p)` → ТО `spawn_at(tile, empty_slot)` з мішка і `custom: «докласти карти валют до 4»`.
- Підрахунок: КОЛИ `custom: «з колоди вийшла картка підрахунку»` → ТО для кожного типу будівель `custom: «більшість плиток у палаці»`: 1-й підрахунок — лише 1-ше місце; 2-й — 1-ше і 2-ге; фінальний — 1–3 місця; `score(+n)` за таблицею.
- Рівність: ЯКЩО `custom: «кілька гравців рівні за місцем»` → ТО `custom: «очки місць діляться порівну, з округленням донизу»`.
- Стіна: при кожному підрахунку `score(+1 × сегменти найдовшої зовнішньої стіни)`; внутрішні стіни «спина до спини» не рахуються.
- Кінець: КОЛИ `custom: «мішок не може дозаповнити ринок до 4»` → ТО решта плиток ринку `give(custom: «тому, у кого найбільше грошей цієї валюти»)` (рівність — лишається), можна вбудувати → фінальний підрахунок → `game_over`.
- Двоє гравців: `custom: «Дірк отримує плитки автоматично й рахує більшість, без очок за стіни»`.
- Перемога: найбільше очок · нічия — спільна.

## Керування і ввід
- Цифрова версія: вибір карт грошей кліками (підсумок суми й валюти), кнопка «Купити» на слоті ринку активна, лише якщо `afford`; точна сума підсвічена як «+дія».
- Викладання: drag плитки з резерву/купленого на палац; підсвітка легальних клітин (збіг стін + досяжність від фонтану + без дір).
- Перебудова — drag між палацом і резервом.

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Нова гра → `match-setup` · Правила → `help-window` · Вихід.
- `match-setup`: 2–6 гравців, люди/AI, Дірк для двох, модулі доповнень.
- `game-screen`: свій палац (зум/скрол); `building-market` — 4 слоти з валютою й ціною; `currency-market` — 4 карти; `reserve-board`; рука грошей (прихована від інших); `opponent-boards` (палаци суперників); `majority-table` — хто лідирує в кожному типі; `score-track`; лічильник дій ходу.
- `scoring-round` (кандидат): таблиця типів × гравців, місця й очки, найдовша стіна кожного.
- `pass-device` у hotseat — гроші приховані.
- `end-screen`: фінальний рахунок і розподіл останніх плиток.
- Переходи: main-menu → match-setup → game-screen ⇄ scoring-round → end-screen.

## Фічі поза полем
- `hotseat` із завісою, `ai-opponent` (?), `custom-rules` / `expansion-toggle` — модулі шести доповнень.
- `rules-page` з таблицею очок підрахунків.
- `autosave` — партія ~1 год (?).

## Варіації й родичі
- Доповнення (по 4 модулі): The Vizier's Favor, The City Gates, The Thief's Turn, The Treasure Chamber, The Power of Sultan, The Falconers; промо Magic Buildings, Medina Buildings. Спінофи: The Gardens of the Alhambra, Alhambra: The Dice Game.
- Родичі «купи плитку на ринку й вбудуй у своє поле»: [the-castles-of-burgundy](the-castles-of-burgundy.md), [the-isle-of-cats](the-isle-of-cats.md), [barenpark](barenpark.md); стіни й досяжність — родич [labyrinth](labyrinth.md); більшість — [carcassonne](carcassonne.md).
- **Осі варіацій**: валюта (одна / кілька за слотом) · решта (дають / нема + бонус за точність) · правила стін (збіг + досяжність / лише збіг) · коли підрахунок (картки в колоді / фіксовані раунди) · кількість призових місць (зростає / стала).

## Цікавинки для курсу
- Валідатор викладання: збіг стін на спільних краях + BFS від фонтану по ребрах без стін + перевірка «замкнених дір» (flood fill порожніх клітин ззовні) — 🥉.
- Найдовша зовнішня стіна: зовнішній контур палацу як цикл, найдовший суцільний відрізок стін — 🥈.
- Оплата без решти: підмножина карт однієї валюти з сумою ≥ ціни, мінімізуючи переплату; точна — бонус (subset sum) — 📎.
- Картки підрахунку, вкладені в певні стоси колоди (контрольована випадковість моменту) — 🌱.
- Більшість із діленням очок місць при рівності + віртуальний гравець Дірк — 📎.

## Мапа на каталог
- Є: `cell-click` · `drag-drop-piece` · `hover-highlight` · `legal-move-highlight` · `reachability-check` (від фонтану) · `connectivity-check` (палац звʼязний) · `impassable-cells` (стіни як ребра) · `turn-enforcement` · `hot-seat` · `pass-device` · `ai-opponent` · `event-points` · `round-currency` (4 валюти) · `match-setup` · `end-screen` · `help-window`.
- **Нема** → пропозиції карток:
  - `+tile-reserve-slots` · `+connected-placement` · `+majority-bonus` · `+bag-draw-refill` — уже в сімʼї.
  - `+multi-currency-market` «Слот ринку визначає валюту оплати» · game-logic/economy · 📎 · слоти {slots: 4, currencies: 4}.
  - `+exact-payment-bonus` «Точна оплата без решти → додаткова дія» · game-logic/economy · 🌱 · слоти {max_actions: 5}.
  - `+wall-edge-match` «Стіни на спільних краях мають збігатись» · entities/legality · 🌱 — дитина `+edge-matching`.
  - `+no-enclosed-holes` «Заборона замкнених порожніх клітин» · entities/legality · 🥉.
  - `+scoring-card-in-deck` «Картка підрахунку вкладена у випадкову частину колоди» · game-logic/waves · 🌱.
  - `+longest-wall-scoring` «Очки за найдовшу зовнішню стіну» · game-logic/score · 🥈 — родич `+longest-path-scoring`.
  - `+dummy-player` «Віртуальний гравець для гри на двох» · game-logic/opponent · 📎.

## Пропозиції до словників
- `+cond:afford` — уже в сімʼї (9 разів), тут з валютою слоту.
- `+cond:exact_pay` — оплата точно дорівнює ціні.
- `+cond:no_holes` — розміщення не створює замкнених порожніх клітин.
- `+cond:edge_match` — краї сусідніх плиток сумісні (тут — стіна/без стіни).
- `+trigger:scoring_card` — з колоди вийшла картка підрахунку.
- `+effect:buy` — купити компонент з ринку за валюту.
- `+effect:to_reserve` — відкласти компонент у резерв поза полем.
- `+ui:currency-market` · `+ui:building-market` · `+ui:reserve-board` · `+ui:majority-table`.
- `+window:scoring-round` — проміжний підрахунок посеред гри.
- `+card:exact-payment-bonus` · `+card:no-enclosed-holes` · `+card:scoring-card-in-deck` · `+card:dummy-player`.

## Джерела
- ⭐ [Wikipedia: Alhambra](https://en.wikipedia.org/wiki/Alhambra_(board_game)) — правила коротко, Дірк, доповнення, Spiel des Jahres 2003, скасована версія XBLA.
- [UltraBoardGames: Alhambra rules](https://www.ultraboardgames.com/alhambra/game-rules.php) — 54 плитки, 108 карт, ринок, резерв, правила викладання, ліміт 5 дій, підрахунки 1–3 місць, кінець гри.
- BGG: [пошук](https://boardgamegeek.com/geeksearch.php?action=search&q=Alhambra); Steam: [пошук](https://store.steampowered.com/search/?term=Alhambra); YouTube: пошук «Alhambra board game how to play».

## Непевне
- (?) Назви й кількість типів будівель (павільйон, сераль, аркади, покої, сад, вежа) — з памʼяті; джерела кажуть лише «6 видів» (UBG — «кожен вид»).
- (?) Таблиця очок за місця в кожному підрахунку й номінали карт грошей — не бачив.
- (?) Кількість гравців 2–6 — виведено з 6 фонтанів і 6 резервів.
- (?) Цифрові версії: Wikipedia згадує лише скасовану XBLA; інших (мобільні, BGA) не перевірено.
