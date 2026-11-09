---
title: ZÈRTZ
slug: zertz
aka: [Zertz, Зертц, ZÈRTZ+11, ZÈRTZ+24]
family: chess-abstract
also: []
klass: figure
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: collect
year: 1999
platforms: [board, web]
links:
  - {kind: other, url: "https://www.gipf.com/zertz/rules/rules.html", best: true, note: "офіційні правила: хід кулькою + зняття вільного кільця, обовʼязкові стрибки, ізоляція, особливі випадки, розширені поля, blitz"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/ZÈRTZ", note: "6/8/10 кульок, 37→49→61 кільце, стратегія жертв, ZÈRTZ+11 і +24"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/GIPF_project", note: "третя гра серії; ZÈRTZ-potential у GIPF"}
  - {kind: play, url: "https://www.boardspace.net/english/about_zertz.html", note: "BoardSpace — онлайн (у списку є і ZÈRTZ+11)"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=ZERTZ", note: "пошук BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=ZERTZ+board+game+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 70
mechanics: [piece-capture, connectivity-check, repetition-draw, legal-move-highlight, selection-highlight, last-move-highlight, hot-seat, turn-enforcement, move-timer, ai-opponent, ai-minimax, cell-click, hover-highlight, drag-drop-piece, pocket, online-multiplayer, move-notation, replay, mode-select, field-size-picker, game-screen, main-menu, end-screen, help-window, settings-window, state-as-data, unit-tests, +hex-grid-render, +shared-pool, +shrinking-board, +forced-capture, +multi-jump, +island-capture, +color-set-win, +board-layouts]
proposes: ["+effect:remove_cell", "+effect:claim_island", "+cond:free_edge_cell", "+cond:can_capture", "+effect:jump_capture", "+trigger:pool_empty", "+ui:captured-by-color", "+ui:free-ring-highlight", "+window:board-size-select", "+card:shrinking-board", "+card:island-capture", "+card:color-set-win", "+card:shared-pool"]
author: opus
date: 2026-11-09
---

# ZÈRTZ — спільні кульки, поле з кілець тане під ногами, а обовʼязкові стрибки перетворюють жертву на зброю

## Суть
Кульки трьох кольорів нікому не належать. Хід — або поставити будь-яку кульку на порожнє кільце й зняти з краю одне вільне кільце, або (якщо можна — обовʼязково) стрибнути кулькою через сусідню й забрати її собі. Поле з кожним ходом зменшується, а відрізаний острів кілець, повністю зайнятий кульками, забирає той, хто відрізав. Виграє той, хто зібрав 4 білих, 5 сірих, 6 чорних або по 3 кожного кольору. Ядро — жертви: змусити суперника взяти дешеве, щоб узяти дороге. Третя гра GIPF Project (Kris Burm).

## Поле і час
- Поле складене з окремих кілець, щільно в гексагон: 37 кілець (4 на сторону) у базовій грі (`field: hex`, 6 сусідів). Розширення: +11 (нерегулярний гексагон 4/5) — турнірний стандарт, +24 (5 на сторону, 61 кільце); турніри — від 48 кілець.
- Поле фізично зменшується: зняте кільце зникає назавжди; можуть утворюватись острови.
- Покроково, один хід = скидання + зняття кільця або серія стрибків. Без випадковості й прихованої інформації.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кулька | piece | white ×6 / grey ×8 / black ×10; нічия | ставиться будь-ким на порожнє кільце; стрибає через сусідню; перестрибнута — взята |
| Кільце | terrain | 37 (49 / 61) | клітина поля; порожнє вільне кільце знімається після скидання |
| Вільне кільце | terrain | порожнє, на краю, знімається без зсуву інших | кандидат на зняття |
| Пул | supply | спільний | звідси скидають; порожній — скидають зі своїх взятих |
| Взяті кульки | zone | по кольорах, у кожного свої | квота кольору або 3+3+3 = перемога |
| Острів | zone | відокремлена група кілець | якщо всі зайняті — кульки й кільця забирає той, хто відрізав |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(side)` → ЯКЩО `custom: «є хоч один стрибок»` (`+cond:can_capture`) → ТО хід — лише стрибок; інакше — скидання.
- Скидання: КОЛИ `input(drop, color, ring)` → ЯКЩО `free(ring)` → ТО `place(marble, ring)` (будь-якого кольору з пулу).
- КОЛИ `after(place)` → ЯКЩО `custom: «є порожнє кільце на краю, яке знімається, не зсуваючи інших»` (`+cond:free_edge_cell`) → ТО `choose(ring)` → `custom: «прибрати кільце з поля»` (`+effect:remove_cell`); вільних нема — хід закінчено без зняття.
- КОЛИ `after(remove_cell)` → ЯКЩО `custom: «відрізано острів, і всі його кільця зайняті»` → ТО `custom: «забрати острів: кульки — собі, кільця — з поля»` (`+effect:claim_island`); острів з порожнім кільцем лишається.
- Стрибок: КОЛИ `input(jump, marble, dir)` → ЯКЩО `occupied(adjacent, marble)` і `free(cell_behind)` → ТО `move(marble, cell_behind)`, `take(opponent_pool, jumped)` — перестрибнута кулька йде до тебе (`+effect:jump_capture`); колір і хто ставив — неважливо.
- КОЛИ `after(jump_capture)` → ЯКЩО `custom: «та сама кулька може стрибати далі»` → ТО стрибати далі тією самою кулькою, у будь-якому напрямку; кілька серій — `choose`.
- КОЛИ `after(jump_capture)` → ТО кільце не знімається і скидання нема — стрибок = весь хід.
- КОЛИ `custom: «пул порожній»` (`+trigger:pool_empty`) → ТО скидати кульку будь-якого кольору зі своїх взятих.
- КОЛИ `custom: «зайнято останнє порожнє кільце»` → ТО `win` того, хто поставив, і він забирає всі кульки з поля.
- КОЛИ `repetition` (послідовність ходів повторюється) → ТО `draw`.
- КОЛИ `counter(white, >=, 4)` або `counter(grey, >=, 5)` або `counter(black, >=, 6)` або `counter(each, >=, 3)` → ТО `win`.
- Blitz (37 кілець, 5/7/9 кульок): КОЛИ `counter(white, >=, 3)` або `counter(grey, >=, 4)` або `counter(black, >=, 5)` або `counter(each, >=, 2)` → ТО `win`.
- Перемога: квота кольору або набір з усіх трьох · Поразка: суперник першим зібрав · Рахунок: взяті за кольорами.

## Керування і ввід
- Настільна: поставити кульку → зсунути вільне кільце з поля; стрибок — перенести кульку через сусідню, взяту — до себе.
- (цифрова версія) Вибір кольору з пулу (три кнопки з лічильниками) → клік по порожньому кільцю → підсвітка вільних кілець → клік для зняття. Якщо є стрибок — гра підсвічує лише кульки, що мусять стрибати; серія — клік по кожному приземленню.

## Вікна, меню, HUD
- `main-menu` (цифрова версія): Грати → `mode-select` (звичайна / blitz) → `board-size-select` (37 / +11 / +24) → `match-setup`.
- `game-screen`: поле кілець, `turn-indicator`, пул з `remaining-counter` за кольорами, `captured-by-color` (взяті кожного проти квот 4/5/6 і 3+3+3), `free-ring-highlight`, `legal-move-highlight` (обовʼязкові стрибки), `last-move-highlight`, `move-list`, `player-clock`.
- `end-screen`: квота кольору / набір / повне поле / нічия повторенням.
- `help-window`: діаграми ізоляції і серій стрибків.
- Переходи: main-menu → mode-select → board-size-select → game-screen → end-screen.

## Фічі поза полем
- `online-multiplayer`: BoardSpace (зокрема ZÈRTZ+11), BoiteAJeux.
- `custom-difficulty` через розмір поля: більше кілець — важче контролювати.
- `ai-opponent-levels` — роботи на BoardSpace (?).

## Варіації й родичі
- Розміри поля: 37 / 40 / 43 / 44 / 48 / 61 кільце; ZÈRTZ+11 (турнірний стандарт за Wikipedia), ZÈRTZ+24 (61). Blitz — менше кульок і квоти.
- У GIPF — ZÈRTZ-potential: перестрибнути сусідню фішку.
- Серія: [gipf](gipf.md), [dvonn](dvonn.md) (теж зникають відрізані частини), [yinsh](yinsh.md), PÜNCT, TZAAR, LYNGK.
- Обовʼязкові серії стрибків — [checkers](checkers.md) і [checkers-variants](checkers-variants.md); поле, що зникає, — Isola / [amazons](amazons.md) (там клітини «спалюються» стрілою).
- Осі варіацій: **хто володіє фігурами** (нікому / своїм) · **як зменшується поле** (кільце з краю / будь-яка клітина) · **ціль** (квота кольору / набір / усе) · **розмір поля**.

## Цікавинки для курсу
- Поле як множина клітин, що зменшується: «вільне кільце» = порожнє + на краю + знімається без зсуву (перевірка геометрії сусідів) — 🥉.
- Ізоляція: BFS по компонентах після зняття, захоплення острова лише без порожніх — 🥉.
- Обовʼязкові стрибки з продовженням серії і вибором — 📎.
- Спільний пул кульок трьох кольорів + перемога «квота кольору або набір» — 🌱.
- Особливі випадки: пул порожній, поле заповнене, повтор — 🌱.
- AI з жертвами: оцінка форсованих серій і «темпу» — глибокий пошук по обовʼязкових ходах — 🥇.

## Мапа на каталог
- Є: `piece-capture` ↔ взяття стрибком · `connectivity-check` ↔ острови · `repetition-draw` · `pocket` ↔ взяті за кольорами · `legal-move-highlight`, `selection-highlight`, `last-move-highlight` · `hot-seat`, `turn-enforcement`, `move-timer`, `online-multiplayer` · `ai-opponent`, `ai-minimax` · `cell-click`, `hover-highlight`, `drag-drop-piece` · `field-size-picker` ↔ 37/+11/+24 · `move-notation`, `replay`, `state-as-data`, `unit-tests` · `mode-select`, `game-screen`, `main-menu`, `end-screen`, `help-window`, `settings-window`.
- **Нема** → пропозиції карток:
  - `+hex-grid-render` (див. hex.md), `+forced-capture`, `+multi-jump` (див. lasca.md, checkers.md), `+board-layouts` (див. ataxx.md).
  - `+shared-pool` «Спільні фігури нікому не належать» · entities/state · 🌱.
  - `+shrinking-board` «Поле зменшується: клітина знімається після ходу» · entities/state · 🥉 · слоти {rule: free-edge|any}.
  - `+island-capture` «Захоплення відрізаного острова» · entities/combat · 🥉.
  - `+color-set-win` «Перемога квотою кольору або набором» · game-logic/win · 🌱 · слоти {quotas: [4,5,6], set: 3}.

## Пропозиції до словників
- `+effect:remove_cell` — клітина зникає з поля назавжди (ZÈRTZ; у словнику є `set_cell`, але тут — зміна топології).
- `+effect:claim_island` — забрати відрізану групу клітин разом із вмістом.
- `+cond:free_edge_cell` — клітина порожня, на краю й знімається без зсуву інших.
- `+cond:can_capture` — у фігури є доступне взяття (Lasca, ZÈRTZ).
- `+effect:jump_capture` — стрибок через сусідню з її взяттям (шашки, Lasca, ZÈRTZ).
- `+trigger:pool_empty` — спільний пул вичерпано (див. yinsh.md).
- `+ui:captured-by-color` — взяті по кольорах проти квот; `+ui:free-ring-highlight` — підсвітка клітин, які можна зняти.
- `+window:board-size-select` — вибір розміру/форми поля перед партією.
- `+card:shrinking-board`, `+card:island-capture`, `+card:color-set-win`, `+card:shared-pool` — див. «Мапа на каталог».

## Джерела
- ⭐ [gipf.com: правила ZÈRTZ](https://www.gipf.com/zertz/rules/rules.html) — хід, вільне кільце, ізоляція (необовʼязкова), обовʼязкові серії стрибків, квоти, blitz, порожній пул, повне поле, повтор = нічия, розширення поля.
- [Wikipedia: ZÈRTZ](https://en.wikipedia.org/wiki/ZÈRTZ) — 6/8/10 кульок, 37/49/61 кільце, стратегія жертв, варіанти +11 і +24.
- [Wikipedia: GIPF project](https://en.wikipedia.org/wiki/GIPF_project) — місце в серії, ZÈRTZ-potential.
- [BoardSpace: ZÈRTZ](https://www.boardspace.net/english/about_zertz.html) — онлайн (лінк зі списку ігор BoardSpace; сторінку не відкривав).

## Непевне
- (?) Рік: GIPF project на Wikipedia — 1999, стаття про гру — видання 2000.
- (?) Захоплення ізольованого острова: офіційні правила — «можеш забрати» (необовʼязково), Wikipedia — «також знімаються» (автоматично).
- (?) Турнірний розмір: Wikipedia — ZÈRTZ+11 (48 кілець), офіційні — «не менше 48»; збігається, але +24 «може стати стандартом».
