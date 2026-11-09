---
title: Triple Match 3D / Tile Explorer
slug: triple-match-3d
aka: [Tile Explorer, Match 3D, 3 Tiles, triple tile match, tray match, Sheep a Sheep]
family: falling-match
also: []
klass: cursor
axes:
  field: free
  time: realtime
  opponent: none
  info: partial
  random: setup
  goal: state
year: 2022
platforms: [iOS, Android, Amazon Fire]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Triple_Match_3D", best: true, note: "правила: купа 3D-предметів, 3 однакові зникають, лоток, таймер, бустери"}
  - {kind: other, url: "https://play.google.com/store/apps/details?id=com.oakever.tiletrip", note: "Tile Explorer – Triple Match (Oakever Games), 100M+ завантажень"}
  - {kind: other, url: "https://apps.apple.com/ee/app/tile-explorer-triple-match/id6498883328", note: "App Store: Tile Explorer, тисячі рівнів"}
  - {kind: other, url: "https://en.wikipedia.org/wiki/Tile-matching_video_game", note: "жанрова стаття про tile-matching"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=triple+match+3d+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [cell-click, line-match-clear, collect-all, time-out, undo-step, sequential-levels, level-unlock, world-map, round-currency, shop-window, goal-counter, end-screen, game-over-continue, hidden-under-block, +match-tray, +tray-overflow-lose, +covered-pick-rule, +pre-level-boosters, +magnet-booster, +shuffle-booster, +freeze-timer]
proposes: ["+cond:uncovered", "+effect:to_tray", "+card:match-tray", "+card:covered-pick-rule", "+ui:tray-bar", "+feature:pre-level-boosters"]
author: opus
date: 2026-11-09
---

# Triple Match 3D / Tile Explorer — бери предмети з купи в лоток: три однакові зникають, лоток переповнився — програш

## Суть
На екрані — купа предметів (3D-обʼєкти у Triple Match 3D, плоскі плитки шарами в Tile Explorer). Тап по предмету переносить його в **лоток** унизу; щойно в лотку три однакові — вони зникають. Лоток має обмежену місткість: якщо він заповнився без трійки — рівень програно. Мета — розібрати купу (або зібрати цільові предмети) за час рівня. Незвичне: поле злиття — не сітка, а **буфер скінченної довжини**; гра — про планування черги, а не про геометрію.

## Поле і час
- Triple Match 3D: вільна 3D-купа з фізикою; предмети накривають один одного, частина схована, доки верхні не прибрано (`field: free`, `info: partial`).
- Tile Explorer: плитки шарами (як Mahjong Solitaire), брати можна лише незакриту плитку (?).
- Лоток (collection bar) — лінійка з 7 слотів (?); однакові предмети стають поруч (?).
- Час: real-time — рівень має ліміт часу (Triple Match 3D); у Tile Explorer таймера може не бути (?).
- Розклад купи задано рівнем; набір предметів кратний 3 (?) (`random: setup`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Предмет (3D-обʼєкт / плитка) | tile | тип | тап → іде в лоток; три однакові в лотку зникають |
| Схований предмет | tile | накритий | не береться (Tile Explorer) або не видно (3D), доки верхні не прибрано |
| Цільовий предмет | tile | тип, квота | рівень вимагає прибрати N таких (Triple Match 3D) |
| Лоток (collection bar) | container | 7 слотів (?) | тримає взяті предмети; трійка зникає; повний без трійки → програш |
| Купа / поле | zone | — | місце, звідки беруть предмети |
| Super Lightning | pickup | бустер до рівня | прибирає частину предметів на старті (?) |
| Extra Time | pickup | бустер до рівня | додає час до таймера |
| Magnet | pickup | бустер у рівні | забирає трійку однакових (?) |
| Undo | pickup | бустер у рівні | повертає останній предмет з лотка на поле |
| Fan | pickup | бустер у рівні | перемішує купу (?) |
| Freeze Time | pickup | бустер у рівні | зупиняє таймер на час |
| Монети | resource | — | нагорода за рівень, купівля бустерів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(tap item)` → ЯКЩО `custom: «предмет не накритий»` → ТО `custom: «to_tray — предмет переходить у лоток, біля однакових»`; інакше `block`.
- КОЛИ `after(to_tray)` → ЯКЩО `pattern(match(type, 3))` у лотку → ТО `clear(triple)`, `counter(goal_type, +3)`, `score(+n)`.
- КОЛИ `after(to_tray)` → ЯКЩО `count(tray_items, ==, capacity)` і `not pattern(match(type, 3))` → ТО `lose` → `window(game-over-continue)`.
- КОЛИ `after(clear)` → ТО `custom: «предмети, що лежали на прибраних, відкриваються / осідають»` (3D-фізика) (?).
- КОЛИ `all_gone(target_items)` → ТО `win` → `window(end-screen)`, `currency(+n)`.
- КОЛИ `counter(time_left, ==, 0)` → ТО `lose` (Triple Match 3D).
- КОЛИ `input(use extra_time)` → ТО `timer(+n)`; КОЛИ `input(use freeze_time)` → ТО `custom: «таймер зупинено на N с»`.
- КОЛИ `input(use undo)` → ТО `undo(1)` — останній предмет повертається з лотка на поле.
- КОЛИ `input(use magnet)` → ТО `custom: «три однакові предмети одразу йдуть у лоток і зникають»` (?).
- КОЛИ `input(use fan)` → ТО `custom: «купа перемішується»` (?).
- КОЛИ `level_start` → ЯКЩО `has(player, super_lightning)` → ТО `custom: «частина предметів прибрана до старту»` (?).
- Перемога: прибрати всі (цільові) предмети. Поразка: лоток переповнено або вийшов час. Рахунок: зірки/монети за рівень (?).

## Керування і ввід
- Тап по предмету в купі — взяти; у 3D купу можна трохи обертати/зсувати (?).
- Тап по кнопці бустера — застосувати; бустери до рівня обираються на екрані старту рівня.
- Офлайн-гра підтримується.

## Вікна, меню, HUD
- `game-screen`: купа предметів, лоток (`+ui:tray-bar`), таймер (`timer-countdown`), цілі рівня (`progress-bar`/`objective-text`), кнопки бустерів (`ability-buttons`), монети (`coins`).
- `custom-window`: старт рівня з вибором бустерів (Super Lightning, Extra Time).
- `game-over-continue`: лоток повний / час вийшов — продовжити за монети (?).
- `end-screen`: рівень пройдено, нагорода.
- `map-window`: шлях рівнів / середовища (Tile Explorer: «coastal villages», «ancient ruins»).
- `shop-window`: монети, бустери, «Piggy Bank», прибрати рекламу.
- `settings-window`: звук, вібрація (?).
- Переходи: map-window → старт рівня → game-screen → end-screen / game-over-continue.

## Фічі поза полем
- `levels-sequential` + `level-unlock` + `world-map` («thousands of levels»).
- Бустери: купуються або заробляються за рівні; `+feature:pre-level-boosters`.
- Монетизація: монети, реклама; офлайн-гра.

## Варіації й родичі
- **Mahjong Solitaire** (`mahjong-solitaire.md`) — предок «бери незакриту плитку»; там пари знімаються одразу, тут — трійки через буфер.
- **Shisen-Sho** (`shisen-sho.md`) — пари з умовою шляху.
- **Triple Town** (`triple-town.md`), **Water Sort** (`water-sort.md`) — інші «три однакові / сортування».
- Sheep a Sheep (羊了个羊, 2022) — вірусний китайський варіант з дуже складним другим рівнем (?); 3 Tiles, Zen Match, Match Factory (натхненний Triple Match 3D).
- **Осі варіацій**: поле (3D-купа з фізикою / шари плиток / сітка) · місткість лотка (5 / 7 / 8) · таймер (є / нема) · ціль (усе / лише цільові) · бустери (вийняти 3 з лотка / undo / перемішати / магніт).

## Цікавинки для курсу
- Лоток скінченної місткості з автоочищенням трійок і вставкою біля однакових — 🌱.
- Правило «накрита плитка недоступна» на шарах (перевірка перекриття прямокутників) — 📎.
- Генератор розвʼязного рівня (кількість кожного типу кратна 3, гарантія проходження) — 🥈.
- Солвер: пошук порядку взяття без переповнення лотка (DFS з відсіканням) — 🥇.
- Бустери undo / магніт / перемішування як окремі операції над станом — 📎.

## Мапа на каталог
- Є: `cell-click` · `line-match-clear` (тут «3 однакові в лотку») · `collect-all` · `time-out` · `undo-step` · `sequential-levels` + `level-unlock` + `world-map` · `round-currency` + `shop-window` · `goal-counter` · `end-screen` + `game-over-continue` · `hidden-under-block` (схований під верхніми).
- **Нема** → пропозиції карток:
  - `+match-tray` «Лоток-буфер: N однакових зникають» · entities/interact · 🌱 слоти {capacity, n}.
  - `+tray-overflow-lose` «Переповнений буфер = програш» · game-logic/lose · 🌱.
  - `+covered-pick-rule` «Брати можна лише незакрите» · entities/legality · 📎 (Mahjong, Tile Explorer).
  - `+pre-level-boosters` «Бустери на старті рівня» · game-logic/economy · 🌱.
  - `+magnet-booster` · `+shuffle-booster` · `+freeze-timer` — одноразові дії гравця · 🌱.

## Пропозиції до словників
- `+cond:uncovered` — сутність не накрита іншими (Mahjong Solitaire, Tile Explorer, купа 3D).
- `+effect:to_tray` — перенести взятий предмет у буфер-лоток (поки `custom`).
- `+card:match-tray` · `+card:covered-pick-rule` — див. «Мапа на каталог».
- `+ui:tray-bar` — лоток слотів під полем.
- `+feature:pre-level-boosters` — вибір бустерів перед стартом рівня.

## Джерела
- ⭐ [Wikipedia: Triple Match 3D](https://en.wikipedia.org/wiki/Triple_Match_3D) — BoomBox Games (Miniclip), 13.04.2022; тап трьох однакових, купа зі схованими, collection bar (повний — провал), ліміт часу, бустери Super Lightning, Extra Time, Magnet, Undo, Fan, Freeze Time; офлайн.
- [Google Play: Tile Explorer](https://play.google.com/store/apps/details?id=com.oakever.tiletrip) — Oakever Games, 100M+ завантажень.
- [App Store: Tile Explorer](https://apps.apple.com/ee/app/tile-explorer-triple-match/id6498883328) — «triple match», тисячі рівнів, середовища, © 2022.
- [Wikipedia: Tile-matching video game](https://en.wikipedia.org/wiki/Tile-matching_video_game) — жанр (про лоткові ігри не пише).
- YouTube: пошук «triple match 3d gameplay».

## Непевне
- (?) Місткість лотка — 7 слотів (з рядка черги й памʼяті); Wikipedia числа не дає.
- (?) Чи однакові предмети в лотку стають поруч, чи в порядку взяття.
- (?) Дії Magnet, Fan, Super Lightning — лише назви з Wikipedia.
- (?) Рік Tile Explorer (черга: 2020; App Store © 2022); правила шарів Tile Explorer — з памʼяті жанру.
- (?) Sheep a Sheep — Wikipedia-статті не знайшлося; деталі з памʼяті.
