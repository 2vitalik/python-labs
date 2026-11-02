---
title: Libble Rabble
slug: libble-rabble
family: maze-arcade
also: []
klass: hybrid
axes:
  field: square
  time: realtime
  opponent: ai
  info: hidden
  random: runtime
  goal: collect
year: 1983
platforms: [arcade, X68000, Super Famicom, FM Towns Marty, PC (Namco Collection Vol. 2), Wii VC, Switch/PS4 (Arcade Archives)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Libble_Rabble", best: true, note: "twin-stick, петлі довкола стовпчиків, вороги, скрині, Topcups, бонус-стадія"}
  - {kind: other, url: "https://ja.wikipedia.org/wiki/リブルラブル", note: "найдетальніше: правила замикання, енергія, рослини, очки, магічні предмети"}
  - {kind: play, url: "https://archive.org/details/arcade_liblrabl", note: "Internet Arcade — грати аркаду (два 8-позиційні джойстики)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=libble+rabble+arcade+gameplay", note: "пошук; геймплей аркади"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=arcade+archives+libble+rabble", note: "пошук; перевидання Hamster"}
stage: v1
coverage: 60
mechanics: [touch-death, player-death, time-out, event-points, combo-multiplier, collect-all, item-pickup, inventory-items, temporary-modes, spawn-schedule, random-walk, chase-player, sequential-levels, progress-acceleration, status-panel, mode-indicator, leaderboard, game-screen, +two-point-control, +tether-line, +lasso-capture, +enclosure-capture, +region-fill, +hidden-chest-in-area, +word-spelling-bonus, +border-timer, +overcharge-invincible, +soil-fertility, +plant-growth-stages, +position-swap-enemy, +path-cut, +extra-life-threshold, +bonus-stage]
proposes: ["+trigger:region_closed", "+trigger:line_cut", "+cond:region_has", "+cond:region_small", "+effect:fill", "+effect:cut_line", "+effect:swap", "+effect:grow", "+effect:add_letter", "+role:zone", "+role:boss", "+ui:border-timer", "+ui:word-slots", "+axis:actors=pair", "+axis:control=twin-stick", "+card:tether-line", "+card:lasso-capture"]
author: opus
date: 2026-11-02
---

# Libble Rabble — два курсори з мотузкою: обмотай стовпчики й замкни петлю довкола грибів

## Суть
Гравець керує **двома стрілками одночасно** (Libble — червона, Rabble — синя, по джойстику на кожну), між якими натягнута лінія. Лінію чіпляють за стовпчики поля і замикають петлю — усе, що всередині, «бащиші» (захоплено): гриби-Mushlin збираються, вороги гинуть, у малій області відкривається скриня зі скарбом. Сезон пройдено, коли зібрано всі Mushlin. Ядро — **геометрія мотузки на гратці стовпчиків**, керована двома точками.

## Поле і час
- Поле з гратки стовпчиків (кілків); навесні й улітку їх багато, восени (з 7-го сезону) — вдвічі менше, взимку — ще менше. Розкладки повторюються з 21-го по 40-й сезон.
- Межі поля діють як лінія при замиканні: петля може замкнутись «через край» (обидві стрілки біля одного краю).
- Поле має невидимий стан **родючості**: захоплена область виснажується, рослини там ростуть повільніше. Скрині сховані — `info: hidden`.
- Real-time; таймер-енергія — смуга по периметру поля, тане з часом.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Libble / Rabble | player | пара = 1 життя | дві стрілки, рух 8 напрямків, кожна своїм джойстиком |
| Лінія | object | довжина, точки обмотки | тягнеться між стрілками, чіпляється за стовпчики; вороги крізь неї не проходять |
| Стовпчик (кілок) | static | — | точка, за яку обмотується лінія |
| Mushlin | pickup | 5 у кожного Hobblin | нешкідливий гриб; петля → очки + енергія |
| Hobblin | enemy | 4, стартують у кутах | блукає, іноді переслідує (лише Rabble); зібрані 5 його Mushlin → краде плід |
| Shears | enemy | — | йде по прямій від краю; ріже лінію й квіти; на дотик нешкідливий |
| Changer | enemy | зʼявляється, якщо сезон затягнувся | зигзаг із кута; торкнувся лінії → Libble і Rabble міняються місцями |
| Killer (×2) | enemy | парою, при затягуванні | на лінії іскрить, тягне енергію, біжить нею до стрілки |
| Gargoyle | boss | біля скрині | зʼявляється при замиканні малої області; нищить рослини, переслідує, не спускається донизу |
| Demon | enemy | — | також ріже лінію (?) |
| Скриня | container | 1 на сезон, схована | відкривається петлею лише довкола неї; дає 6 Topcup або предмет |
| Topcup | pickup | буква ключового слова | фея втікає до країв; петля → буква |
| Рослина | pickup | насіння 5 → паросток 10 → квітка 25 → плід 40 | росте стадіями; збір дає енергію; плід, якщо не зібраний, розсипається в насіння |
| Магічний предмет | pickup | вид | зі скрині: пісочний годинник, кристал, меч, конюшина, шолом, прапор… |
| Енергія (рамка) | static (HUD у полі) | рівень | тане; 0 → втрата життя; понад поріг → overcharge |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(stick_L|stick_R, dir)` → ТО `move(libble|rabble, dir)`; лінія тягнеться за ними й огинає стовпчики.
- КОЛИ `custom: «лінія торкнулась стрілки або іншої ділянки лінії»` або `custom: «обмотана лінія і стрілка біля краю поля»` → ТО `custom: «region_closed — бащиші»`.
- КОЛИ `custom: «лінія перетнула саму себе під прямим кутом»` → ТО нічого (петлі нема) — так «ловлять живцем».
- КОЛИ `region_closed` → ЯКЩО `custom: «в області є Mushlin»` → ТО `pickup`, `score(10, 20, 30… до 200 за порядком у петлі)`, `custom: «енергія +1 за кожен»`.
- КОЛИ `region_closed` → ЯКЩО `custom: «в області є Killer/Changer/Shears/Hobblin»` → ТО `disappear_b`, `score(500…2000)`; Hobblin — `custom: «на мить вилітає вгору екрана»`.
- КОЛИ `region_closed` → ТО `custom: «родючість області −1»`; ЯКЩО `custom: «в області є прихована скриня»` → ТО `flash` (з 3-го сезону — лише сигнал).
- КОЛИ `region_closed` → ЯКЩО `custom: «область охоплює лише скриню»` → ТО `reveal(chest)`; повторна петля довкола відкритої скрині → `spawn(topcup ×6)` або `give(magic_item)` / коштовність 4000–100 000.
- КОЛИ `contact(shears|demon, line)` → ТО `custom: «лінія перерізана — нова пряма між стрілками»`.
- КОЛИ `contact(changer, line)` → ТО `swap(libble, rabble)`; Changer втрачає здатність, доки гравець не зʼїсть плід.
- КОЛИ `contact(killer, line)` → ТО `custom: «енергія −n, Killer біжить лінією до стрілки»`; петля довкола одного Killer знищує обох.
- КОЛИ `contact(libble|rabble, enemy)` → ТО `lose` (Shears і Mushlin — нешкідливі).
- КОЛИ `timer(every)` → ТО `custom: «енергія −1»`; `counter(energy, ==, 0)` → `lose`.
- КОЛИ `counter(energy, >, threshold)` → ТО `set_state(arrows, invincible)` — overcharge, інша музика.
- КОЛИ `custom: «зібрано 6 букв ключового слова»` → ТО `custom: «Miracle»`, сезон пройдено, бонус-стадія.
- КОЛИ `all_gone(mushlin)` → ТО `win` сезону; ЯКЩО `state(overcharge)` → ТО `score(energy_left)`.
- Бонус-стадія: час = енергія на момент Miracle; знайти й обвести 6 схованих скринь.
- Поразка: 0 пар стрілок. Рахунок: Mushlin/вороги/Topcup/коштовності; життя на 40k, 120k, 200k, 400k, 600k, 1M. Рейтинг рекордів — спершу кількість Miracle, потім менше сезонів, потім очки.

## Керування і ввід
- Два 8-позиційні джойстики (twin-stick): лівий — Libble, правий — Rabble; кнопок дії нема. SFC-версія давала накладку на D-pad/кнопки, що імітує двостиковий ввід.
- Уся «дія» — геометрична: замкнути петлю, торкнувшись лінії стрілкою, звівши стрілки разом або до одного краю.
- Ловля «живцем»: перехрестити лінію під прямим кутом — область без замикання.

## Вікна, меню, HUD
- `attract-demo` / `splash-screen`.
- `game-screen` — поле зі стовпчиками; HUD: `score`, `hi-score`, `lives` (пари стрілок), номер сезону (`level-number`, лічильник зупиняється на 99), енергія-рамка по периметру (`custom: «border-timer»`), слово-ключ із зібраними буквами (`custom: «word-slots»`), індикатор overcharge (`mode-indicator`, музика).
- `custom-window`: «Miracle» → бонус-стадія з таймером.
- `leaderboard` — ввід ініціалів; ранжування за Miracle/сезонами/очками.
- Переходи: attract → game-screen (сезон N) → (усі Mushlin) сезон N+1 · (слово зібране) бонус-стадія → сезон N+1 · (0 життів) ініціали → attract.

## Фічі поза полем
- `levels-sequential` за порами року (весна → зима), `progress-acceleration` (менше стовпчиків, більше ворогів).
- `onboarding-hints` — у перших двох сезонах розташування скринь показують явно.
- `leaderboard-local` з нестандартним ранжуванням; `hotseat` (?).
- SFC: «Miracle Mode» з новими ключовими словами (`mode-*`).

## Варіації й родичі
- Порти: X68000, Super Famicom, FM Towns Marty, Windows (Namco Collection Vol. 2), Wii VC (JP), Arcade Archives (Switch/PS4, 2021).
- Родичі: Qix/Xonix (захоплення області лінією — тут лінія не «слід», а мотузка між двома точками), Lady Bug (букви слова), Robotron (двостиковий ввід), Pac-Man (вороги з кутів).
- Осі: **чим креслиш контур** — слід аватара (Xonix) / мотузка між двома курсорами (тут) / стіни (Rampart); **що буває всередині** — збір / вбивство / відкриття схованого; **покарання за велику область** — нема / виснаження ґрунту (тут).

## Цікавинки для курсу
- Мотузка між двома курсорами, що обмотується довкола стовпчиків, — 🥇: геометрія ламаної з точками обмотки, розмотка при зворотному русі.
- Детекція замкненої петлі (самоперетин лінії, зведення стрілок, замикання через край) + «що всередині» (point-in-polygon) — 🥈.
- Скриня, що відкривається лише петлею «тільки довкола неї» — 📎 (перевірка розміру/вмісту області).
- Changer міняє місцями два аватари — 🌱; Shears ріже лінію → нова пряма — 📎.
- Енергія-рамка, яку поповнює збір, з overcharge понад поріг — 📎.
- Рослини зі стадіями росту і родючість ґрунту, що падає від захоплень — 🥉 (стан клітини, що впливає на швидкість процесу).

## Мапа на каталог
- Є: `touch-death` · `player-death` · `time-out` (енергія) · `event-points` · `combo-multiplier` (10→200 за Mushlin в одній петлі) · `collect-all` (усі Mushlin) · `item-pickup` · `inventory-items` (магічні предмети — миттєвої дії) · `temporary-modes` (overcharge, пісочний годинник) · `spawn-schedule` (Changer/Killer при затягуванні) · `random-walk` · `chase-player` · `sequential-levels` · `progress-acceleration` · `status-panel` · `mode-indicator` · `leaderboard` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+two-point-control` «Два аватари одночасно, кожен своїм вводом» · interface/input · 🥉.
  - `+tether-line` «Мотузка між двома точками, що обмотується довкола стовпчиків» · entities/move · 🥇.
  - `+lasso-capture` «Захоплення вмісту замкненої петлі» · game-logic/score · 🥈 · слот {close_by: self-touch|arrows-meet|edge}.
  - `+enclosure-capture` (вже Triple Town) — замкнений ворог гине.
  - `+region-fill` (вже Xonix) — найближче до замкненої області, але без заливки.
  - `+hidden-chest-in-area` «Схований обʼєкт відкривається лише малою областю» · entities/interact · 📎 · слот {max_area}.
  - `+word-spelling-bonus` (вже Lady Bug) — букви ключового слова від Topcup.
  - `+border-timer` (вже Lady Bug) — енергія як рамка поля.
  - `+overcharge-invincible` «Невразливість понад поріг ресурсу» · entities/state · 🌱.
  - `+soil-fertility` «Клітини виснажуються від захоплень» · entities/state · 🥉.
  - `+plant-growth-stages` «Обʼєкт росте стадіями, цінність росте» · entities/state · 📎.
  - `+position-swap-enemy` «Ворог міняє місцями два аватари» · entities/interact · 🌱.
  - `+path-cut` (вже Railbound) — Shears ріже лінію.
  - `+extra-life-threshold` (вже Pac-Man) · `+bonus-stage` «Бонус-стадія з таймером між рівнями» · levels/progression · 📎.

## Пропозиції до словників
- `+trigger:region_closed` (вже Xonix) — петлю замкнено.
- `+trigger:line_cut` — ворог перетнув лінію-мотузку.
- `+cond:region_has(kind)` (вже Xonix) · `+cond:region_small` — площа області ≤ N (відкриття скрині).
- `+effect:fill` · `+effect:cut_line` — перерізати лінію, перебудувати прямою · `+effect:swap` — обміняти позиції двох аватарів · `+effect:grow` — стадія рослини · `+effect:add_letter` (вже Lady Bug).
- `+role:zone` (🔥) — захоплена область; `+role:boss` — Gargoyle.
- `+ui:border-timer`, `+ui:word-slots` (вже Lady Bug).
- `+axis:actors=pair` — два аватари одночасно; `+axis:control=twin-stick` — по стіку на кожен.
- `+card:tether-line`, `+card:lasso-capture` — див. вище.

## Джерела
- ⭐ [Wikipedia: Libble Rabble](https://en.wikipedia.org/wiki/Libble_Rabble) — twin-stick, петлі, Hobblins/Killers/Changers/Shears, скрині й Topcups, бонус-стадія, рамка-таймер, життя за очки, порти.
- [Wikipedia JA: リブルラブル](https://ja.wikipedia.org/wiki/リブルラブル) — умови «бащиші», перехрест під прямим кутом, родючість, енергія й overcharge, рослини, Gargoyle, очки й предмети.
- [Internet Arcade: Libble Rabble](https://archive.org/details/arcade_liblrabl) — грати в браузері; короткий опис MobyGames.
- YouTube: пошуки «libble rabble arcade gameplay», «arcade archives libble rabble».

## Непевне
- (?) Demon: EN Wikipedia каже, що ріже лінію; JA-стаття його не згадує (можливо, це Gargoyle під іншою назвою).
- (?) Точні умови петлі «через край» і як рахується Mushlin «без зовнішнього краю» (×2 очок?).
- (?) Розмір гратки стовпчиків; наскільки саме родючість сповільнює ріст.
- (?) Чи є одночасна гра двох гравців (аркада — по черзі, вважаю).
- (?) Чи Hobblin переслідує лише Rabble — так пише JA-стаття, але причина не пояснена.
