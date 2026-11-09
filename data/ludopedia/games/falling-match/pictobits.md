---
title: Pictobits
slug: pictobits
aka: [PiCOPiCT, Picopict, Pictopict, ピコピクト, "Art Style: Pictobits"]
family: falling-match
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: collect
year: 2009
platforms: [Nintendo DSi (DSiWare)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pictobits", best: true, note: "правила: тач-поле, картинка на верхньому екрані, POW, монети, Ura-етапи, магазин музики"}
  - {kind: other, url: "https://ja.wikipedia.org/wiki/ピコピクト", note: "JA: палітра на 8, Deka-picto, лінія 4+ або квадрат 2×2, ×-перешкоди, game over за 3 с, ціни"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=pictobits+dsiware+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [cell-click, inventory-limit, gravity-fall, line-match-clear, chain-reaction, combo-multiplier, event-points, time-bonus, round-currency, shop-catalog, level-unlock, sequential-levels, score-records, sound-warnings, background-music, music-toggle, game-settings, +picture-reveal, +square-group-match, +lifo-hand, +hand-pickup-drop, +obstacle-tile, +panic-bomb, +big-piece-breakup, +slot-cost-powerup]
proposes: ["+effect:absorb", "+trigger:stuck_for", "+ui:picture-progress", "+ui:palette-slots", "+feature:handedness", "+card:big-piece-breakup", "+card:slot-cost-powerup"]
author: opus
date: 2026-11-09
---

# Pictobits — бери дрібні кольорові «піксі» стилусом, підкладай під великі падаючі блоки, і зібраний колір домальовує 8-бітну картинку

## Суть
На нижньому тач-екрані зверху падають великі складені блоки (Deka-picto), а внизу лежать дрібні «picto». Гравець торканням забирає picto у палітру (до 8) і викладає їх на поле так, щоб великий блок і picto того самого кольору склали лінію з 4+ або квадрат 2×2+ — тоді вони зникають. Ні дрібні, ні великі окремо не зчищаються: потрібна **комбінація двох шарів**. Кожен зчищений колір додає пікселі до картинки на верхньому екрані — персонажа NES (Маріо, Лінк, Боузер); завершена картинка = етап пройдено.

## Поле і час
- Два екрани: нижній — поле з гравітацією (до 6 кольорів на етап), верхній — піксельна картинка, що заповнюється.
- Real-time: великі блоки падають згори; після часткового зчищення решта великого блоку швидко падає і, сівши на стовпець з picto, розпадається на дрібні picto.
- Палітра — поза полем, стопка до 8 picto; її бік (ліворуч/праворуч) — за налаштуванням руки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Picto | tile | колір | лежить унизу; торкнувся → у палітру; падає до опори |
| Deka-picto | object | колір, форма з кількох клітин | падає згори; зчищається лише разом із picto свого кольору; частково зчищений — падає, на picto розпадається |
| ×-picto (перешкода) | tile | позначка × | не береться в палітру; знімається лише зчищенням поруч (?) або падінням на нього |
| Палітра | supply | ≤ 8 слотів, порядок | приймає picto; викладає верхній першим |
| Заблокований слот | zone | — | після POW один слот палітри вимкнено; відновлення за монети |
| POW-блок | pickup | — | прибирає 2 нижні ряди, усе в повітрі падає; ціна — 1 слот палітри |
| Монета | resource | — | +1 за повне зчищення Deka-picto або зняту перешкоду |
| Картинка | zone | пікселі за кольорами | заповнюється кольорами, що їх зчищено, поки є пікселі цього кольору |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `timer(drop_rate)` → ТО `spawn_at(deka_picto, top)`, `fall(deka_picto)`.
- КОЛИ `input(tap, picto)` → ЯКЩО `not state(picto, obstacle)` and `count(palette, <, palette_slots)` → ТО `pickup(picto)` у палітру.
- КОЛИ `input(tap, empty_cell)` → ЯКЩО `count(palette, >, 0)` → ТО `place(top_of_palette, cell)`, `fall(picto)` (?).
- КОЛИ `pattern(line(4+) | square(2×2+))` → ЯКЩО `custom: «у групі є і Deka-picto, і picto одного кольору»` → ТО `clear(group)`, `score(n)`, `reveal(picture_pixels[color])`.
- КОЛИ `after(clear)` → ТО `fall(deka_rest)`; КОЛИ `enter(deka_rest, column_with_picto)` → ТО `custom: «розпадається на picto в точці посадки»` (`transform(picto)`).
- КОЛИ `after(clear)` → ЯКЩО `chain(n)` або нова група склалась до кінця анімації попередньої → ТО `combo(+1)`, `score(bonus)`.
- КОЛИ `custom: «Deka-picto зчищено повністю»` або перешкоду знято → ТО `currency(+1)`.
- КОЛИ `input(tap, pow)` → ЯКЩО `count(free_slots, >, 0)` → ТО `clear(bottom_2_rows)`, `fall(all)`, `set_state(palette_slot, disabled)`.
- КОЛИ `input(tap, recover)` → ЯКЩО `counter(coins, ≥, 5)` → ТО `currency(-5)`, `clear_state(palette_slot, disabled)`.
- КОЛИ `custom: «стовпці дійшли до верху»` → ТО `message(DANGER!)`, `custom: «частина picto блимає»`; прибрав їх → гра триває.
- КОЛИ `custom: «жоден Deka-picto не може впасти 3 секунди»` → ТО `lose`.
- КОЛИ `custom: «картинку заповнено»` → ТО `win`, `score(time_bonus)`; ЯКЩО `custom: «POW не вживано»` → `custom: «зірка етапу»`.
- Перемога: картинка завершена. Поразка: поле переповнене 3 с. Рахунок: очки + час проходження, комбо (зчищення до завершення попереднього або від падіння).

## Керування і ввід
- Лише стилус: торкання picto — забрати в палітру; торкання порожнього місця поля — викласти верхній picto з палітри.
- POW і кнопка відновлення — тач-кнопки біля палітри; їх бік і бік палітри задає налаштування «KIKITE» (правша/лівша).
- Гравець не рухає великі блоки: лише підкладає під них дрібні.

## Вікна, меню, HUD
- `main-menu`: GAME · MUSIC · KIKITE (`settings-window`: рука).
- `level-select` (GAME): етапи Omote і відкриті за монети Ura/Dark/Remix; зірка біля етапу без POW.
- `game-screen`: верхній екран — картинка, що домальовується; нижній — поле, `custom: «palette-slots» — 8 слотів зі станом`, кнопка POW, кнопка відновлення, `score`, `timer-elapsed`, `coins`.
- `toast`/`message` «DANGER!» з блиманням picto.
- `shop-window` — купівля етапів і треків за монети (оригінал дешевше, ремікс дорожче).
- MUSIC — плеєр куплених треків YMCK; грає й при закритій DSi.
- `end-screen` етапу: очки, час, зірка; Game Over.

## Фічі поза полем
- `levels-sequential` етапів; кожен має складну версію — `level-unlock` за монети.
- `stars-rating`: одна зірка за проходження без POW.
- Валюта в раунді (монети) витрачається і в грі (слоти палітри), і поза нею (етапи, музика) — одна економіка на два рівні.
- `leaderboard-local` за очками й часом (?); `music-toggle`/плеєр музики.
- Серія Art Style (7 ігор DSiWare) — мінімалістичні правила, без режимів versus.

## Варіації й родичі
- Родичі: Tetris (падаючі фігури), Magical Drop і Klax (рука-буфер над полем), Puyo Puyo (каскади від падіння), Meteos (підтримка для DS-стилуса), Lumines (квадрат 2×2 як група).
- **Осі варіацій**: хто рухається (фігура / буфер гравця) · умова зчищення (лише одного шару / комбінація двох шарів) · куди йде зчищене (у нікуди / у картинку-прогрес) · ціна паніки (безкоштовно / слот палітри / життя).

## Цікавинки для курсу
- Зчищення лише змішаної групи (великий + дрібні одного кольору) — 📎 (перевірка групи з умовою складу).
- Палітра-стопка з вимкненими слотами як ціна POW — 📎.
- Розпад великої фігури на дрібні при посадці на непорожній стовпець — 🥉.
- Картинка-прогрес: кожен зчищений колір домальовує свої пікселі — 🥉 у GUI, 📎 у консолі (ASCII-арт).
- Game over за таймером «нема куди впасти 3 с» з попередженням DANGER — 🌱.
- Монети як одна валюта для в-грі (відновлення слота) і мета-прогресії (етапи, музика) — 🌱.

## Мапа на каталог
- Є: `cell-click` (тач-ввід) · `inventory-limit` (палітра ≤ 8) · `gravity-fall` · `line-match-clear` (лінія 4+) · `chain-reaction` · `combo-multiplier` · `event-points` · `time-bonus` · `round-currency` (монети) · `shop-catalog` · `level-unlock` · `sequential-levels` · `score-records` · `sound-warnings` (DANGER) · `background-music` · `music-toggle` · `game-settings`.
- **Нема** → пропозиції карток:
  - `+big-piece-breakup` «Велика фігура розпадається на клітини при посадці» · entities/state · 🥉.
  - `+obstacle-tile` «Плитка, яку не можна взяти» · entities/legality · 🌱.
  - `+slot-cost-powerup` (картка-пропозиція) «Паніка-кнопка коштує слот буфера» · entities/state · 📎.
  - `+picture-reveal` · `+square-group-match` · `+lifo-hand` · `+hand-pickup-drop` · `+panic-bomb` — теги вже є в корпусі.

## Пропозиції до словників
- `+effect:absorb` — забрати плитку з поля в буфер, де вона лишається плиткою (Pictobits; родич `catch` у Klax).
- `+trigger:stuck_for` — умова «стан триває N секунд» (жоден блок не може впасти 3 с).
- `+ui:picture-progress` — картинка, що заповнюється пікселями як прогрес етапу.
- `+ui:palette-slots` — буфер зі слотами, які можуть бути вимкнені.
- `+feature:handedness` — перемикання правша/лівша дзеркалить HUD (палітра, POW).
- `+card:big-piece-breakup` · `+card:slot-cost-powerup` — див. «Мапу».

## Джерела
- ⭐ [Wikipedia: Pictobits](https://en.wikipedia.org/wiki/Pictobits) — нижній тач-екран, падаючі блоки, картинка зверху, POW (2 нижні ряди, ціна — резерв), монети, Ura/Dark/Remix, магазин музики, комбо.
- [JA Wikipedia: ピコピクト](https://ja.wikipedia.org/wiki/ピコピクト) — палітра 8, Deka-picto, лінія 4+ / квадрат 2×2, ×-перешкоди, розпад при посадці, DANGER і 3 с, 5 монет за слот, KIKITE.
- YouTube: пошук «pictobits dsiware gameplay».

## Непевне
- (?) Де саме лягає викладений picto (у клітину торкання чи на дно стовпця) — джерела кажуть лише «торкнутись порожнього місця».
- (?) Як знімається ×-перешкода — Wikipedia: «зчистити, поки не сіла, або дочекатись, щоб на неї впали блоки того кольору»; механізм неясний.
- (?) Наявність `timer-elapsed` на екрані і таблиці рекордів — Wikipedia каже «оцінка за очками і часом», без деталей інтерфейсу.
- (?) Порядок появи Deka-picto — випадковий чи заданий етапом (картинка задана, тож, імовірно, набір кольорів фіксований).
