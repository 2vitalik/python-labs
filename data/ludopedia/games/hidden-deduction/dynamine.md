---
title: Dynamine
slug: dynamine
aka: []
family: hidden-deduction
also: [build-sim]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: hidden
  random: setup
  goal: score
year: 2026
platforms: [web (HTML5), Windows, macOS, Linux]
links:
  - {kind: itch, url: "https://hexagonnico.itch.io/dynamine", best: true, note: "демо 0.5.4 у браузері; правила копання, продаж, печі, ліфт, інструменти; відповіді автора в коментарях"}
  - {kind: steam, url: "https://store.steampowered.com/app/4480100/Dynamine/", note: "опис: вибухівка коштує лише ремонт, печі, ліфт, біоми, вагонетки; реліз TBA"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Dynamine+minesweeper+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [move-4dir, dig-terrain, neighbor-count-clue, flood-reveal, round-currency, shop-catalog, inventory-items, inventory-limit, infinite-field, stairs-levels, save-game, save-progress, controls-remap, keyboard-controls, game-settings, language-picker, main-menu, game-screen, +ore-selling-decay, +furnace-processing, +repair-cost-death, +explosion-scar-blocks, +auto-flag-tool, +chest-press-puzzle, +rail-placement]
proposes: ["+effect:sell", "+effect:process", "+cond:value_decayed", "+ui:bag-meter", "+feature:one-button-mode", "+feature:death-penalty-setting", "+feature:reset-progress", "+card:ore-selling-decay", "+card:furnace-processing", "+card:repair-cost-death", "+card:explosion-scar-blocks", "+card:auto-flag-tool", "+card:chest-press-puzzle", "+card:rail-placement"]
author: opus
date: 2026-11-09
---

# Dynamine — сапер як шахта: копай клітини за числами, виноси руду на продаж, купуй інструменти й опускайся ліфтом глибше

## Суть
Інкрементальна гра про видобуток на правилах сапера: персонаж копає клітини підземелля, число на ґрунті — кількість вибухівки серед 8 сусідів. Розкопана клітина буває порожньою, з мінералом або відкриває велику порожнину. Руду продають за гроші (сира з часом дешевшає, піч підвищує ціну), гроші йдуть на апгрейди й інструменти, а ліфт кожного шару веде глибше — до цінніших і небезпечніших покладів.

## Поле і час
- Квадратна сітка, нескінченний процедурний світ з біомами, покинутими спорудами й рідкісними скарбами.
- Шари шахти; на кожному — ліфт униз; глибше = цінніше й небезпечніше.
- Вид згори, персонаж ходить полем (avatar); темп — реальний час (?).
- Після вибуху лишаються чорні блоки — нерозбірливі зони мапи (захист від «зачистки смертями»).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Шахтар | player | сумка (місткість (?)) | ходить, копає сусідні клітини, несе руду |
| Ґрунт/стіна | terrain | прихований вміст | копається; після відкриття — порожньо, мінерал або порожнина |
| Число на ґрунті | mark | n = вибухівка серед 8 сусідів | класична підказка |
| Вибухівка | hazard | — | копнув — вибух: ремонт за гроші (або кінець гри — залежно від версії/налаштувань) |
| Чорний блок | static | — | слід вибуху |
| Мінерал/руда | resource | ціна, що падає | у сумку; продаж біля ліфта |
| Піч | object | — | переплавляє сиру руду в дорожчу |
| Ліфт | static | — | продаж (?) і спуск на глибший шар |
| Рейки вагонетки | object | напрям руху | кладуться в напрямку ходу персонажа; швидке переміщення |
| Екскаватор | pickup | — | швидко набиває сумку землею (за гравцем) |
| Червоне відро фарби | pickup | — | позначає стіни довкола числа, якщо число = кількість лишених стін |
| Замкнена скриня | container | числа-підказки | міні-пазл: числа кажуть, скільки сусідніх плит натиснути |
| Скарб | pickup | — | рідкісна знахідка |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, dir)` → ТО `move(miner, dir)`.
- КОЛИ `input(dig, c)` → ЯКЩО `not occupied(c, explosive)` → ТО `reveal(c)` з числом `adjacent_count(c, explosive, =, n)`.
- КОЛИ `after(reveal(c))` → ЯКЩО `custom: «0 вибухівки довкола»` → ТО `reveal(neighbors8)` — «відкриває велику область».
- КОЛИ `after(reveal(c))` → ЯКЩО `occupied(c, ore)` → ТО `pickup(miner, ore)`.
- КОЛИ `input(dig, c)` → ЯКЩО `occupied(c, explosive)` → ТО `explode(area, into: black_block)`, `currency(-repair)` (Steam-опис) або `game_over` (опис itch); штраф налаштовується.
- КОЛИ `input(flag, c)` → ТО `mark(c, flag)`.
- КОЛИ `input(use, paint_bucket, c)` → ЯКЩО `custom: «число c = кількість ще закритих стін довкола»` → ТО `mark(all_closed_neighbors, flag)`.
- КОЛИ `input(sell, ore)` → ТО `currency(+price)`; `custom: «ціна сирої руди з часом падає»`.
- КОЛИ `input(use, furnace, ore)` → ТО `transform(ore, ingot)` — дорожче за сиру (?).
- КОЛИ `input(buy, item)` → ЯКЩО `custom: «вистачає грошей»` → ТО `currency(-cost)`, `give(miner, item)`.
- КОЛИ `input(place, rail)` → ТО `place(miner, rail)` у `facing(miner, dir)`; утримання кнопки — ставити безперервно (0.4.3).
- КОЛИ `enter(miner, elevator)` → ЯКЩО `input(go_deeper)` → ТО `custom: «наступний шар»` (`next_level`).
- КОЛИ `input(press, plate)` → ЯКЩО `custom: «натиснуто стільки плит, скільки кажуть числа скрині»` → ТО `custom: «скриня відкривається»`, `give(miner, treasure)` (?).
- Перемога: — (мета — заробляти; демо має кінець (?)). · Поразка: вибух — ремонт або кінець гри. · Рахунок: гроші.

## Керування і ввід
- Клавіатура, миша, геймпад; перепризначення клавіш; режим «однією кнопкою».
- Рух персонажем, копання сусідньої клітини, ПКМ — прапорець; утримання — безперервне розставлення інструмента.

## Вікна, меню, HUD
- `main-menu`: Грати / Extra → Reset progress (скинути апгрейди) / налаштування.
- `game-screen`: шахта, сумка (?), гроші (?).
- `shop-window`: апгрейди й інструменти (?) — місце купівлі не бачив.
- `settings-window`: вигляд чисел, штраф за смерть, керування, мова (DE/EN/IT).
- `save-slots` (?) — збереження й завантаження додані в оновленні.

## Фічі поза полем
- `meta-progression`: апгрейди переходять у нові ігри; повний скид — Extra → Reset progress (або видалити сейв).
- `save-slots`/`autosave` (?) · `remap-controls` · `one-hand-mode`-подібний one-button play · `localization`.
- Налаштування штрафу за смерть і вигляду чисел (відповідь на скарги про читабельність).

## Варіації й родичі
- Сапер з аватаром: [mined-out](mined-out.md), [lizzi-crossing](lizzi-crossing.md); нескінченне поле — [minesweeper-infinite](minesweeper-infinite.md), [endless-mines](endless-mines.md).
- Сапер з економікою: [keepsweeper](keepsweeper.md); сапер-роглайк з магазином: [demoncrawl](demoncrawl.md).
- **Осі варіацій**: вибух = програш / штраф грошима / слід на мапі; відкрита клітина = інформація / ресурс; прогресія = нема / апгрейди між іграми; простір = рамка / нескінченні шари.

## Цікавинки для курсу
- Вибух як грошовий штраф + «шрам» на мапі замість програшу — 🌱.
- Ціна сирої руди, що падає з часом, і піч як множник — 📎.
- Інструмент авто-прапорців (відро) — по суті «акорд» для прапорців — 🌱.
- Нескінченний процедурний світ з чанками й біомами під правила сапера — 🥈.
- Скриня-міні-пазл «скільки плит натиснути» всередині гри — 📎.
- Рейки в напрямку руху як швидкий транспорт — 📎.

## Мапа на каталог
- Є: `move-4dir` · `dig-terrain` · `neighbor-count-clue` · `flood-reveal` · `round-currency` ↔ гроші · `shop-catalog` + `inventory-items` ↔ інструменти · `inventory-limit` ↔ сумка (?) · `infinite-field` ↔ нескінченний світ · `stairs-levels` ↔ ліфт на шар · `save-game` + `save-progress` · `controls-remap`.
- **Нема** → пропозиції карток:
  - `+ore-selling-decay` «Ціна товару падає з часом» · game-logic/economy · 🌱.
  - `+furnace-processing` «Переробка підвищує вартість» · game-logic/economy · 📎.
  - `+repair-cost-death` «Помилка — штраф валютою, а не програш» · game-logic/lose · 🌱.
  - `+explosion-scar-blocks` «Вибух лишає непрозорі блоки» · entities/interact · 🌱.
  - `+auto-flag-tool` «Інструмент ставить прапорці, коли число однозначне» · interface/input · 🌱.
  - `+chest-press-puzzle` «Міні-пазл замкненої скрині» · entities/interact · 📎.
  - `+rail-placement` «Рейки за напрямком руху» · entities/move · 📎.

## Пропозиції до словників
- `+effect:sell(item)` — обміняти предмет на валюту (від `currency` відрізняє втрата предмета).
- `+effect:process(item)` — переробити предмет в інший дорожчий у споруді.
- `+cond:value_decayed(item)` — вартість упала з часом.
- `+ui:bag-meter` — заповненість сумки.
- `+feature:one-button-mode` · `+feature:death-penalty-setting` · `+feature:reset-progress`.

## Джерела
- ⭐ [itch.io: Dynamine](https://hexagonnico.itch.io/dynamine) — демо, опис, відповіді автора про скрині, чорні блоки, штраф смерті.
- [Steam: Dynamine](https://store.steampowered.com/app/4480100/Dynamine/) — опис механік, платформи, реліз TBA; демо — 22.03.2026.

## Непевне
- (?) Вибух: itch — «кінець гри», Steam — «лише плата за ремонт»; автор каже, що штраф налаштовується. Яке значення за замовчуванням — не бачив.
- (?) Типи руд і їхні ціни; як швидко падає ціна.
- (?) Де продавати (гравці — біля ліфта) і де купувати апгрейди.
- (?) Рух покроковий чи вільний; місткість сумки.
- (?) Рік: Steam-демо 22.03.2026; ранні itch-збірки могли бути раніше.
