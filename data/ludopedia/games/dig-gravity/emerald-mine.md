---
title: Emerald Mine
slug: emerald-mine
family: dig-gravity
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: coop
  info: full
  random: runtime
  goal: collect
year: 1987
platforms: [Amiga, Atari ST, C64, C16/Plus4]
links:
  - {kind: official, url: "https://www.artsoft.org/rocksndiamonds/manual/reference.html", best: true, note: "довідник Rocks'n'Diamonds: точна поведінка кожного EM-елемента (позначки EM/EMC)"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Emerald_Mine", note: "огляд: Kingsoft, 2 гравці, горіхи, магічна стіна, сиквели"}
  - {kind: wiki, url: "https://de.wikipedia.org/wiki/Emerald_Mine", note: "кількість рівнів, кожен 4-й — кооперативний, редактор EM2, CD з 14 160 рівнями"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Rocks%27n%27Diamonds", note: "відкритий двіжок, що відтворює EM (грати сьогодні)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Emerald+Mine+Amiga+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-4dir, gravity-fall, push-object, collect-quota, reach-exit, time-out, time-bonus, touch-death, environment-death, player-death, chain-detonation, key-and-door, cell-transform, inventory-items, item-pickup, chase-player, impassable-cells, event-points, sequential-levels, level-unlock, score-records, in-game-editor, status-panel, goal-counter, +dig-terrain, +roll-off-rounded, +explode-3x3, +wall-follower, +expanding-wall, +explosion-content, +crack-open, +acid-pool, +lure-switch, +pass-through-door, +shared-screen-coop]
proposes: ["+trigger:smashed", "+trigger:enter", "+effect:explode", "+effect:fall", "+effect:roll", "+effect:spread", "+cond:prop", "+role:container", "+role:hazard", "+card:explosion-content", "+card:crack-open", "+card:acid-pool", "+card:lure-switch", "+card:pass-through-door", "+card:shared-screen-coop", "+feature:mode-coop"]
author: opus
date: 2026-11-02
---

# Emerald Mine — Boulder Dash на двох: смарагди, кислота, динаміт і вороги з «начинкою»

## Суть
Шахтар копає пісок, збирає смарагди й алмази до квоти і виходить, поки йде час; камені й самоцвіти падають і вбивають. Нове порівняно з Boulder Dash: **два гравці одночасно в одній шахті** (частина рівнів — лише для двох), вороги, що при загибелі вибухають у «вміст» (жук → алмаз + 8 смарагдів, Yam-Yam — у задану рівнем картину), горіхи, які треба розколоти каменем, кислотні басейни, динаміт, ключі й двері чотирьох кольорів. Набір елементів EM став другим стовпом «rocks-and-diamonds» поряд з BD і повністю живе в Rocks'n'Diamonds.

## Поле і час
- Шахта — прямокутна сітка зі скролом; обидва гравці ділять **одну спільну ділянку екрана**, тож мусять триматися поруч (?) щодо деталей прокрутки.
- Один шар: у клітині один елемент; падіння/напрямок — стан елемента.
- Синхронний тік: усе рухається разом раз на 8 кадрів (50 кадр/с) — так EM відтворює двіжок EM у Rocks'n'Diamonds.
- Таймер рівня; квота «смарагдів» рахується з вагою (алмаз = 3).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Шахтар ×2 | player | гравітація на гравця не діє | рух 4 напрямки, копає пісок, штовхає камінь убік, кладе динаміт |
| Пісок | terrain | diggable | гравець проходить → порожньо |
| Камінь | object | pushable, falling, slippery (?) | падає; убік штовхається у порожнечу; падаючий вбиває, розчавлює алмаз |
| Смарагд | pickup | 1 до квоти; slippery | падає, з нього скочується; збір −1 від квоти |
| Алмаз | pickup | 3 до квоти | падає; камінь, що падає на нього, його знищує |
| Горіх | container | вміст: смарагд | падає; камінь згори розколює → смарагд; вибух знищує разом із вмістом |
| Бомба | object | pushable, falling, slippery | вибухає 3×3, якщо її розчавити, якщо вона впала або в вибуху |
| Динаміт | pickup → object | запал | кладеться утриманням клавіші; горить і вибухає 3×3; погасити не можна |
| Ключ ×4 (червоний, жовтий, зелений, синій) | pickup | колір | відкриває двері свого кольору |
| Двері ×4 | gate | колір | прохідні наскрізь: гравець проходить на клітину за дверима, стояти в них не можна |
| Стіна | static | руйнується вибухом | непрохідна |
| Сталева стіна | static | невразлива | рамка; самоцвіти з неї зісковзують, горіхи ні |
| Магічна (синя) стіна | switch | діє обмежений час (?) | падаюче крізь неї перетворюється: камінь → смарагд → алмаз → камінь |
| Росла стіна | static | вісь росту | росте в порожнечу вбік/вгору (?) |
| Кислотний басейн | hazard | слизькі краї, невразливий | знищує все, що в нього впало, і гравця |
| Жук | enemy | 4 стартові напрямки | тримається **правої** сторони; смерть від дотику; розчавлений → 1 алмаз + 8 смарагдів, ланцюговий вибух |
| Космічний корабель | enemy | 4 напрямки | тримається **лівої** сторони; смерть від дотику; вибух у порожнечу |
| Yam-Yam | enemy | вміст 3×3 задається рівнем | іде прямо до упору, потім новий напрям; їсть алмази; розчавлений → свій вміст |
| Робот | enemy | — | крокує до найближчого гравця |
| Колесо | switch | час обертання | натиснув → роботи йдуть до колеса, а не до гравця; поки крутиться, повторне натискання не продовжує |
| Амеба (крапельна) | hazard | — | не гине, періодично кидає краплю; крапля падає, вбиває, приземлившись стає новою амебою |
| Вихід | gate | квота | відкривається, коли лічильник квоти = 0 |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `cell(target, sand)` → ТО `move`, `set_cell(empty)`; ЯКЩО `cell(target, empty|gem)` → `move` (+ `pickup`).
- КОЛИ `contact(miner, rock|bomb)` горизонтально → ЯКЩО `free(cell_behind)` → ТО `push`; інакше `block`.
- КОЛИ `contact(miner, emerald|diamond)` → ТО `pickup`, `counter(quota, -1|-3)`, `score(n)`.
- КОЛИ `tick` → ЯКЩО `free(below)` → ТО `fall(rock|gem|nut|bomb|drop)`; ЯКЩО `state(falling)` and `prop(below, slippery)` → `roll(left|right)`.
- КОЛИ `smashed(diamond)` камінням → ТО `disappear_a`.
- КОЛИ `smashed(nut)` камінням → ТО `transform(emerald)`, `score(n)`.
- КОЛИ `smashed(bomb)` або `custom: «бомба впала на тверде»` → ТО `explode(3×3)`.
- КОЛИ `smashed(miner|bug|spaceship|yamyam)` → ТО `explode(3×3, into: content)`: жук → 1 алмаз + 8 смарагдів (менше біля сталі), корабель → порожнеча, Yam-Yam → вміст рівня.
- КОЛИ `explode` → ТО клітини 3×3, крім невразливих, `set_cell(content|empty)`; бомби, динаміт, жуки в зоні — `chain-detonation`.
- КОЛИ `input(drop)` утримано → ЯКЩО `has(miner, dynamite)` → ТО `spawn(burning_dynamite)`; КОЛИ `timer(fuse)` → `explode(3×3)`.
- КОЛИ `contact(miner, door[c])` → ЯКЩО `has(miner, key[c])` and `free(cell_beyond)` → ТО `custom: «пройти крізь двері на клітину за ними»`; інакше `block`.
- КОЛИ `contact(falling rock|gem, magic_wall)` → ЯКЩО `free(below wall)` → ТО `transform(next_in_cycle)` під стіною.
- КОЛИ `enter(any, acid)` → ТО `disappear_a`; гравець → `lose`.
- КОЛИ `tick` → ТО жук — `custom: «тримайся правої стіни»`; корабель — `custom: «тримайся лівої»`; Yam-Yam — `blocked(a)` → `face(a, rng)` (?); робот — `chase-greedy` до найближчого гравця або до колеса, якщо воно крутиться.
- КОЛИ `adjacent(miner, bug|spaceship)` або `contact` → ТО `lose` (вибух гравця).
- КОЛИ `contact(yamyam, diamond)` → ТО `disappear_b` (зʼїв).
- КОЛИ `contact(miner, wheel)` → ТО `set_state(wheel, spinning, t)`; роботи `custom: «ціль = колесо»`.
- КОЛИ `timer(drip)` → ТО `spawn(drop)` під амебою; КОЛИ краплю `fall` зупинено → `transform(amoeba)`.
- КОЛИ `tick` → ТО `spread(growing_wall, axis)` у порожнечу.
- КОЛИ `counter(quota, <=, 0)` → ТО `set_state(exit, open)`; КОЛИ `contact(miner, exit)` → ЯКЩО відкрито → ТО гравець виходить; рівень пройдено, коли вийшли всі живі гравці (?), `score(time_left)`.
- КОЛИ `counter(time_left, ==, 0)` → ТО `lose`.
- Перемога: квота + вихід. Поразка: камінь/вибух/ворог/кислота/крапля/час. Рахунок: самоцвіти, розчавлені вороги, розколоті горіхи, залишок часу; рекорди окремо для кожного рівня.

## Керування і ввід
- Джойстик: 4 напрямки; кнопка + напрямок — дія на сусідню клітину без руху (?) у EM-оригіналі; утримання кнопки на місці — покласти динаміт.
- Два джойстики — два гравці одночасно на одному екрані.

## Вікна, меню, HUD
- `splash-screen` — титул Kingsoft.
- `main-menu` (?): кількість гравців · вибір рівня з уже відкритих (`level-select`) · старт.
- `game-screen`: шахта + рядок стану — `remaining-counter` (скільки «смарагдів» лишилось), `timer-countdown`, `score`, кількість динаміту і ключі (`inventory-bar`).
- `leaderboard` — рекорди по рівню.
- `editor-window` — у Emerald Mine 2 (1988).
- Переходи: титул → меню → рівень → (вихід) → наступний відкритий; смерть → той самий рівень.

## Фічі поза полем
- `levels-sequential` + `level-unlock`: пройдений рівень відкриває наступний.
- `mode-coop` / `local-multiplayer`: 80 рівнів на одного, 60 з них і на двох + 20 лише для двох; кожен 4-й рівень спроєктовано під кооперацію.
- `leaderboard-local` по кожному рівню.
- `level-editor` (EM2) → тисячі фан-рівнів; Emerald Mines CD (1994) — 14 160 рівнів (177 наборів по 80); на CD32 без збережень — старт лише з кожного 8-го рівня.

## Варіації й родичі
- Emerald Mine 2 (1988, +100 рівнів, редактор), Emerald Mine 3 Professional (1990, фан-рівні), Emerald Mines CD (1994), Emerald Mine Club — фанатські розширення (кулі, вітер, пружини, андроїд; у RnD позначені EMC).
- Предок — Boulder Dash; нащадок, що зберіг EM повністю, — Rocks'n'Diamonds (EM-двіжок із тіком 8 кадрів).
- **Осі варіацій**: вибух ворога — «у порожнечу / в алмази / у вміст, заданий рівнем»; двері — «зникають після ключа / прохідні наскрізь»; амеба — «росте плямою (BD) / капає краплями (EM)»; ворог іде до — «стіни / гравця / приманки-колеса».

## Цікавинки для курсу
- Вибух із «вмістом» 3×3, заданим рівнем (Yam-Yam) — 🥉: дані рівня керують результатом вибуху.
- Магічна стіна як цикл перетворень камінь → смарагд → алмаз → камінь — 📎.
- Горіх-контейнер: розкрити можна лише падінням каменя, вибух знищує вміст — 📎.
- Колесо-приманка: глобальна зміна цілі ворогів на час — 🥉.
- Кооператив на одному екрані з рівнями «лише для двох» — 🥈: два вводи, спільна камера, умова виходу обох.
- Синхронний тік (усе рухається разом) проти скану BD — 🥉, якщо студент порівняє обидва.

## Мапа на каталог
- Є: `move-4dir` · `gravity-fall` · `push-object` · `collect-quota` (вага алмаза 3) · `reach-exit` · `time-out` + `time-bonus` · `touch-death` · `environment-death` (кислота, камінь, крапля) · `player-death` · `chain-detonation` · `key-and-door` · `cell-transform` (магічна стіна) · `inventory-items` (динаміт, ключі) · `item-pickup` · `chase-player` (робот) · `impassable-cells` · `event-points` · `sequential-levels` + `level-unlock` · `score-records` · `in-game-editor` (EM2) · `status-panel` + `goal-counter`.
- **Нема** → пропозиції карток:
  - `+explosion-content` «Вибух у заданий вміст» · entities/combat · 🥉 · слот {content: 3×3 map} — Yam-Yam, жук.
  - `+crack-open` «Контейнер розкривається ударом» · entities/interact · 📎 — горіх.
  - `+acid-pool` «Басейн, що знищує падаюче» · entities/interact · 🌱.
  - `+lure-switch` «Приманка змінює ціль ворогів на час» · entities/move · 🥉 · слот {duration}.
  - `+pass-through-door` «Двері, крізь які проходять на клітину далі» · entities/legality · 📎 — дитина `key-and-door`.
  - `+shared-screen-coop` «Два гравці, одна камера» · game-logic/opponent · 🥈.
  - `+dig-terrain`, `+roll-off-rounded`, `+explode-3x3`, `+wall-follower`, `+expanding-wall` — повтор з Boulder Dash.

## Пропозиції до словників
- `+trigger:smashed(a)` — на A впав обʼєкт (горіх, алмаз, бомба, ворог); повтор з Rocks'n'Diamonds.
- `+trigger:enter` ⏳ — у кислоту.
- `+effect:explode(area, into)` · `+effect:fall` ⏳ · `+effect:roll` · `+effect:spread` — повтори з Boulder Dash (рахунок на правило трьох).
- `+cond:prop(a, slippery)` — властивість клітини як умова скочування.
- `+role:container` ⏳ (горіх), `+role:hazard` ⏳ (кислота, амеба).
- `+feature:mode-coop` ⏳ — рівні, що проходяться лише вдвох.

## Джерела
- ⭐ [Rocks'n'Diamonds Elements Reference](https://www.artsoft.org/rocksndiamonds/manual/reference.html) — EM-елементи: ваги самоцвітів, горіх, бомба, динаміт, магічна стіна (цикл), жук/корабель/Yam-Yam/робот, колесо, крапельна амеба, двері-наскрізь, кислота, тік 8 кадрів.
- [Wikipedia](https://en.wikipedia.org/wiki/Emerald_Mine) — Kingsoft 1987, Klaus Heinz і Volker Wertich, кооператив, горіхи, синя стіна, сиквели.
- [Wikipedia DE](https://de.wikipedia.org/wiki/Emerald_Mine) — 80 рівнів (60 на двох + 20 лише для двох), відкриття рівнів, рекорди по рівню, CD 14 160 рівнів.
- [Rocks'n'Diamonds (Wikipedia)](https://en.wikipedia.org/wiki/Rocks%27n%27Diamonds) — де зіграти EM-рівні сьогодні.
- YouTube: пошук «Emerald Mine Amiga gameplay».

## Непевне
- (?) Тривалість роботи магічної стіни і росту стіни (напрями) — у EM-оригіналі не перевірено; описано за RnD.
- (?) Чи гравець має snap-дію в оригінальному EM; як саме ділиться екран між двома гравцями.
- (?) Умова кінця рівня на двох (обидва мають вийти чи достатньо одного).
- (?) Поведінка Yam-Yam після упору (випадковий напрям) і що саме він їсть в оригіналі (RnD каже — EM-алмази).
- (?) Колесо в запиті описане як «зупиняє ворогів»; у джерелі — воно **приманює роботів**, інших ворогів не чіпає.
