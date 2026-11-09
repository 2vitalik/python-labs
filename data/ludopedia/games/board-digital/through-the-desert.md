---
title: Through the Desert (Крізь пустелю)
slug: through-the-desert
aka: [Durch die Wüste, Крізь пустелю]
family: board-digital
also: [chess-abstract]
klass: cursor
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: score
year: 1998
platforms: [board]
links:
  - {kind: other, url: "https://www.ultraboardgames.com/through-the-desert/game-rules.php", best: true, note: "повні правила: компоненти, розстановка вершників, 2 верблюди за хід, заборона торкатись чужого того ж кольору, оазиси, огороджені області, бонус каравану"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Through_the_Desert", note: "Knizia, Kosmos/FFG; коротко правила й підрахунок"}
  - {kind: other, url: "https://rulespal.com/through-the-desert/rulebook", note: "вартості водопоїв 1/2/3 по 15 штук; менша частина поля на 2–3 гравців"}
  - {kind: other, url: "https://www.ultraboardgames.com/through-the-desert/variants.php", note: "варіанти: бік з річкою Нігер, змійкова розстановка, приховані водоносні шари"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=Through+the+Desert", note: "пошук BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Through+the+Desert+Knizia+how+to+play", note: "пошук; пояснення правил"}
stage: v1
coverage: 75
mechanics: [cell-click, hover-highlight, legal-move-highlight, turn-enforcement, hot-seat, ai-opponent, impassable-cells, connectivity-check, event-points, game-settings, match-setup, rule-variants, game-screen, end-screen, help-window, +hex-grid-render, +connected-placement, +shared-color-pieces, +no-touch-same-color-rival, +multi-group-ownership, +pickup-on-enter, +adjacency-once-reward, +enclose-area-scoring, +area-closed-to-all, +majority-bonus, +supply-exhaustion-end, +setup-placement-phase, +serpentine-order, +hidden-score-tokens, +two-placements-per-turn]
proposes: ["+cond:owner_same", "+cond:touches_rival_same_color", "+trigger:linked", "+effect:close_area", "+role:leader", "+ui:caravan-colors", "+ui:hidden-score", "+feature:serpentine-setup", "+card:no-touch-same-color-rival", "+card:enclose-area-scoring", "+card:shared-color-pieces"]
author: opus
date: 2026-11-09
---

# Through the Desert — пʼять кольорів верблюдів спільні для всіх: тягни свої каравани гексами до водопоїв і оазисів і замикай пустелю петлею

## Суть
У кожного гравця пʼять вершників — по одному в кожному з пʼяти кольорів верблюдів; кольори не належать гравцям, гравцеві належить **караван** (група верблюдів кольору, що містить його вершника). За хід ставиш два верблюди будь-яких кольорів, кожен — поруч зі своїм караваном того ж кольору. Не можна ставити верблюда поруч із чужим верблюдом того ж кольору — каравани не зливаються, тож вони блокують одне одного. Очки — за водопої, на які ступив, оазиси, яких торкнувся (раз на караван), області, які огородив одним караваном, і найбільший караван кожного кольору. Ядро — спільна палітра кольорів з приватним володінням групами і боротьба за простір на гекс-полі.

## Поле і час
- Гекс-поле пустелі: гори по краях і хребет у центрі (непрохідні), малі калюжі (водопої з жетонами 1/2/3) і великі калюжі (оазиси-пальми або водопої). На 2–3 гравців менша частина поля, відділена темною лінією, не використовується.
- Межі області — край поля або гори.
- Хід = 2 верблюди (першому гравцю в першому ході — 1). Гра йде, доки не вичерпається запас будь-якого кольору.
- Зворотний бік поля — річка Нігер (варіант).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гекс пустелі | terrain | порожній / з верблюдом | приймає одного верблюда; порожній в огородженій області = 1 очко |
| Гора | static | край і центральний хребет | непрохідна; може бути частиною огорожі |
| Водопій | pickup | жетон 1 / 2 / 3 очки (по 15) | верблюд стає на нього → жетон гравцеві (закрито) |
| Оазис (пальма) | static | 5 у грі; на великій калюжі | ставити не можна; караван-сусід бере 5 очок раз |
| Верблюд | tile | 5 кольорів × 35; спільний запас | кладеться поруч зі своїм караваном того ж кольору |
| Вершник (лідер) | piece | 6 на гравця: 5 кольорових + сірий | голова каравану; визначає власника групи |
| Сірий вершник | mark | 1 на гравця | лише нагадування, якого кольору гравець |
| Караван | zone | колір + власник | звʼязна група верблюдів кольору з вершником; може розгалужуватись |
| Огороджена область | zone | порожні гекси всередині петлі | закрита для всіх; жетони всередині — тому, хто огородив |
| Жетон каравану | resource | 10 очок (5 у грі) | найбільший караван кольору; нічия — по 5 кожному |
| Жетони 5 / 10 | resource | — | очки за оазиси, бонуси |

## Правила (КОЛИ → ЯКЩО → ТО)
- Розстановка: КОЛИ `input(place(leader, cell))` (по черзі за годинниковою, по одному) → ЯКЩО `free(cell)` і `not cell(cell, waterhole|oasis|mountain)` і `adjacent_count(cell, oasis|leader, =, 0)` і `custom: «перший вершник гравця — колір, якого ще ніхто не ставив»` → ТО `place(leader, cell)`; інакше `block`.
- КОЛИ `turn_start(player)` → ТО `custom: «взяти 2 верблюди: два одного кольору або два різних»` (перший хід першого гравця — 1).
- КОЛИ `input(place(camel, cell))` → ЯКЩО `free(cell)` і `not cell(cell, mountain|oasis)` і `adjacent_count(cell, own_caravan_same_color, >=, 1)` → ТО перевірити далі; інакше `block`.
- КОЛИ `input(place(camel, cell))` → ЯКЩО `adjacent_count(cell, rival_camel_same_color, >=, 1)` (`+cond:touches_rival_same_color`) → ТО `block` — каравани одного кольору не зливаються.
- Сусідство з іншими кольорами (свої чи чужі) — дозволене; караван може розгалужуватися.
- КОЛИ `enter(camel, waterhole)` → ТО `pickup(token)` закрито (очки сховані до кінця).
- КОЛИ `custom: «караван уперше став сусідом оазису»` (`+trigger:linked`) → ЯКЩО `first_time` (для цієї пари караван–оазис) → ТО `score(+5)`; один караван може привʼязати кілька оазисів, один оазис — кілька караванів.
- КОЛИ `pattern(region_closed)` → ЯКЩО `custom: «петля з одного каравану (+ край поля / гори)»` і `count(camels_inside, =, 0)` → ТО `custom: «область закрита для всіх»` (`+effect:close_area`), `pickup(waterholes_inside)`, `score(+5)` за кожен оазис усередині, не привʼязаний цим караваном.
- КОЛИ `input(place(camel, cell))` → ЯКЩО `custom: «клітина в чужій або своїй огородженій області»` → ТО `block`.
- КОЛИ `turn_end(player)` → ЯКЩО `custom: «останній верблюд будь-якого кольору покинув запас»` (`+trigger:supply_empty` — пропонує Reef) → ТО `game_over`.
- Бонус каравану: для кожного кольору ЯКЩО `custom: «у гравця найбільший караван кольору»` → ТО `score(+10)`; нічия → `score(+5)` кожному з рівних, 10 не дають.
- Огороджені області: КОЛИ `game_over` → ТО `score(+1)` за кожен порожній гекс області (оазиси не рахуються).
- Варіант «Річка»: вершника можна ставити поруч із річкою; КОЛИ `custom: «караван уперше перетнув річку»` → ТО `score(+5)`.
- Варіант «Змійкова розстановка»: порядок A-B-C-D-D-C-B-A…; «Водоносні шари»: жетони водопоїв лежать закрито.
- Перемога: найбільше очок · Нічия: спільна перемога · Поразка: — · Рахунок: водопої + оазиси + огороджені гекси + бонуси караванів.

## Керування і ввід
- Фізично: брати верблюдів зі спільного запасу і ставити на гекси.
- (цифрова версія) Вибір кольору з палітри 5 запасів (лічильник лишку) → підсвітка легальних гексів для своїх караванів цього кольору (з урахуванням заборони торкатися чужого того ж кольору) → клік; другий верблюд — так само; кнопка «завершити хід».
- Розстановка вершників — окрема фаза з підсвіткою дозволених гексів.

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Нова гра · Правила · Налаштування.
- `match-setup`: 2–5 гравців, людина/AI, бік поля (гори / річка), змійкова розстановка, приховані водопої.
- `placement-screen` (кандидат): фаза розстановки вершників.
- `game-screen`: гекс-поле; `caravan-colors` — запаси 5 кольорів з лічильниками (хто ближчий до кінця); на кожному караван-вершнику колір власника; `hidden-score` — свої закриті жетони видно лише собі; підсвітка огороджених областей; `turn-indicator`; лічильник «поставлено 0/2».
- `end-screen`: розклад очок — водопої, оазиси, області, бонуси за кольори.
- `help-window`: правило «не торкатися чужого того ж кольору».
- Переходи: main-menu → match-setup → розстановка → game-screen → end-screen.

## Фічі поза полем
- `custom-rules`: бік поля з річкою, змійкова розстановка, водоносні шари.
- `hotseat`; `ai-opponent-levels` (цифрова версія).
- Прихований рахунок: закриті жетони — у цифровій версії не показувати чужі очки (`+ui:hidden-score`).

## Варіації й родичі
- Видання Kosmos (Durch die Wüste) і Fantasy Flight; бік з річкою Нігер у виданні FFG.
- Родичі: Go (огородження території), Blokus (блокування простору), Kingdom Builder (поселення на гексах), Acquire (спільні «кольори»-компанії, приватні частки), Tigris & Euphrates (Knizia, групи на полі).
- **Осі варіацій**: кольори (спільні / особисті) · групи одного кольору (зливаються / блокують) · що дає очки (вхід на клітину / сусідство / огородження / найбільша група) · хто може огородити (одна група / будь-які свої) · кінець (вичерпано один запас / усі).

## Цікавинки для курсу
- Гекс-сітка й сусідство (6 сусідів), непрохідні гори — 🌱.
- Спільні кольори + приватне володіння групою: верблюд належить каравану з вершником — 📎.
- Легальність: «торкається свого каравану кольору» і «не торкається чужого того ж кольору» — 📎.
- Огородження області: flood fill від кожної порожньої компоненти, перевірка, що межа — лише один караван + край/гори — 🥈.
- «Раз на пару караван–оазис» — множина привʼязок — 🌱.
- Бонус найбільшого каравану кольору з нічиїми — 🌱.
- AI: блокувати чужий караван, тягнучись до оазису, і закривати області — 🥇.

## Мапа на каталог
- Є: `cell-click` · `hover-highlight` · `legal-move-highlight` · `turn-enforcement` · `hot-seat` · `ai-opponent` · `impassable-cells` ↔ гори · `connectivity-check` ↔ каравани · `event-points` · `match-setup` · `rule-variants` · `game-screen`, `end-screen`, `help-window`.
- **Нема** → пропозиції карток:
  - `+hex-grid-render` · `+connected-placement` · `+majority-bonus` — як в інших іграх сімʼї.
  - `+shared-color-pieces` «Кольори фігур спільні, власник — група» · entities/state · 📎.
  - `+no-touch-same-color-rival` «Не можна торкатися чужої групи того ж кольору» · entities/legality · 📎.
  - `+multi-group-ownership` «У гравця кілька груп різних кольорів» · entities/state · 🌱.
  - `+pickup-on-enter` (водопій) · `+adjacency-once-reward` (оазис раз на караван) · 🌱.
  - `+enclose-area-scoring` «Очки за огороджену область» · game-logic/score · 🥈; `+area-closed-to-all` · 🌱.
  - `+setup-placement-phase` · `+serpentine-order` · `+hidden-score-tokens` · `+two-placements-per-turn` · `+supply-exhaustion-end` — по 🌱.

## Пропозиції до словників
- `+cond:owner_same` — сутності належать одному гравцеві (верблюд → караван із вершником власника).
- `+cond:touches_rival_same_color` — клітина сусідить із чужою групою того ж кольору.
- `+trigger:linked` — група вперше стала сусідом обʼєкта (оазис, місто, джерело).
- `+effect:close_area` — область стає закритою для всіх ходів.
- `+role:leader` — голова групи, що визначає її власника.
- `+ui:caravan-colors` — запаси спільних кольорів з лічильниками.
- `+ui:hidden-score` — свої закриті жетони видно лише собі.
- `+feature:serpentine-setup` — змійковий порядок розстановки.
- `+card:no-touch-same-color-rival` · `+card:enclose-area-scoring` · `+card:shared-color-pieces` — див. «Мапа на каталог».

## Джерела
- ⭐ [UltraBoardGames: Through the Desert rules](https://www.ultraboardgames.com/through-the-desert/game-rules.php) — компоненти (175 верблюдів, 30 вершників, 5 пальм, 45 водопоїв), розстановка й заборони, 2 верблюди за хід, правила розміщення, оазиси, огороджені області, кінець, бонус каравану.
- [Wikipedia: Through the Desert](https://en.wikipedia.org/wiki/Through_the_Desert) — ⭐ черги; коротко (вершник = лідер, огородження, найдовший караван); вартостей нема.
- [RulesPal: rulebook](https://rulespal.com/through-the-desert/rulebook) — водопої 1/2/3 по 15, менше поле на 2–3 гравців, тайбрейк.
- [UltraBoardGames: variants](https://www.ultraboardgames.com/through-the-desert/variants.php) — річка (+5 за перший перетин), змійкова розстановка, водоносні шари.
- BGG: [пошук](https://boardgamegeek.com/geeksearch.php?action=search&q=Through+the+Desert); YouTube: пошук «Through the Desert Knizia how to play».

## Непевне
- (?) Кількість пальм: UBG — 5 пальм на великі калюжі, RulesPal — «7 місць для пальм (6 на 2–3 гравців)»; імовірно 7 великих калюж, пальм 5.
- (?) Скільки верблюдів повертають на 4–5 гравців (відомо лише 2 і 3 гравці: −8 / −4 кожного кольору) і що «5 гравців повертають по вершнику».
- (?) Чи може область огородити кілька караванів одного гравця разом — джерело: «один караван одного кольору».
- (?) Цифрові версії (BGA-сторінка не завантажилась) — не підтверджено.
- (?) Як рахувати «найбільший караван» — за кількістю верблюдів (Wikipedia: «most camels») — так і записано.
