---
title: X2 Blocks
slug: x2-blocks
aka: [X2 Blocks: 2048 Number Games, X2 Blocks: Number Block Puzzle, X2 Blocks: 2048 Merge Puzzle, X2 Blocks: Number Stack Games]
family: falling-match
also: []
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: runtime
  goal: score
year: 2019
platforms: [iOS, Android]
links:
  - {kind: other, url: "https://apps.apple.com/us/app/x2-blocks-2048-merge-puzzle/id1480338372", best: true, note: "App Store: «drag and shoot the block», комбо, 1024 → 2048 → 4096 → ∞, без ліміту часу, автосейв, глобальні таблиці; відгуки — превʼю наступного числа, прибрати/обміняти блок за діаманти"}
  - {kind: other, url: "https://itunes.apple.com/lookup?id=1480338372&country=us", note: "iTunes API: реліз 2019-11-07, версія 4.4.0, 5 скриншотів (5 стовпців, хвіст пострілу знизу, +10…+40, молоток, swap, New High Score)"}
  - {kind: other, url: "https://www.bluestacks.com/apps/puzzle/x2-blocks-on-pc.html", note: "розробник Inspired Square FZE, пакет com.inspiredsquare.blocks"}
  - {kind: other, url: "https://play.google.com/store/apps/details?id=com.inspiredsquare.blocks", note: "Google Play (у фетчі сторінка обрізана)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=x2+blocks+2048+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [tile-merge, gravity-fall, chain-reaction, combo-multiplier, popup-text, next-queue, drag-drop-piece, swipe-gestures, score-records, leaderboard, save-autosave, shop-window, game-screen, end-screen, +shoot-into-column, +multi-neighbor-merge, +booster-hammer, +booster-swap, +rewarded-ad-continue]
proposes: ["+cond:group_size", "+effect:launch", "+feature:boosters", "+card:shoot-into-column", "+card:multi-neighbor-merge"]
author: opus
date: 2026-11-09
---

# X2 Blocks — стріляєш числовим блоком у стовпець знизу; він злипається з усіма однаковими сусідами, і злиття тягнуть ланцюг

## Суть
Мобільна merge-головоломка на 2048-числах (2, 4, 8 … 1024, 2048 і далі «до нескінченності»). Гравець бачить поточний блок і наступний, перетягує поточний під один із пʼяти стовпців і «стріляє» ним угору: блок летить до стелі або до першого блока в стовпці. Прилипнувши, він зливається з однаковими сусідами; після злиття блоки підтягуються, і нові збіги дають ланцюг-комбо. Ядро — та сама «гравітація навпаки», що й у Drop the Number: стос росте від стелі вниз.

## Поле і час
- Квадратна сітка з 5 стовпців (видно на всіх скриншотах); висота — 7 рядів (?).
- Гравітація вгору: блоки тримаються стелі, новий летить знизу вгору до упору (на скриншотах — хвіст пострілу під блоком).
- Покроково: хід = один постріл, далі каскад злиттів до стабілізації; таймера нема («No time limits»).
- Інформація повна; випадковість — номінал наступного блока.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Числовий блок | tile | номінал 2ⁿ, колір за номіналом | стоїть у стовпці; зливається з однаковими сусідами |
| Поточний блок | player | номінал | перетягується під стовпець і вистрілюється вгору |
| Наступний блок | tile | номінал | превʼю; стає поточним після пострілу |
| Стовпець | zone | 5 штук | приймає постріл; повний стовпець не приймає (?) |
| Молоток | pickup | ціна в діамантах / реклама (?) | прибирає обраний блок |
| Swap | pickup | ціна в діамантах / реклама (?) | міняє місцями два блоки |
| Діаманти | resource | лічильник | валюта бустерів; купуються або заробляються грою |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, column)` → ЯКЩО `free(bottom_cell(column))` → ТО `slide(current, up)` — до стелі або до першого блока; інакше `block`.
- КОЛИ `blocked(current)` → ЯКЩО `same(current, neighbour, value)` → ТО `merge(current, neighbours, into)`: `custom: «усі однакові сусіди (ліворуч, праворуч, згори) зливаються з блоком за один крок»`; номінал результату — див. «Непевне».
- КОЛИ `after(merge)` → ТО `fall(all_unsupported)` (гравітація вгору: блоки під злитими підтягуються до стелі).
- КОЛИ `settled` → ЯКЩО `same(tile, neighbour, value)` → ТО `merge(…)`, `combo(+1)` — ланцюг повторюється, доки є збіги.
- КОЛИ `after(merge)` → ЯКЩО `chain(n)` → ТО `score(n)`, `message(+10·n)` — спливні +10, +20, +30, +40 на кроках ланцюга (скриншот «Create combos»; формула — (?)).
- КОЛИ `settled` → ТО `custom: «наступний блок стає поточним»`, `spawn_at(next, preview)`.
- КОЛИ `counter(max_value, >=, 1024)` (далі 2048, 4096 …) → ТО `custom: «відкрито новий номінал»`, `window(custom-window)` (?).
- КОЛИ `input(hammer, cell)` → ЯКЩО `has(player, diamonds)` → ТО `disappear(tile)`, `take(player, diamonds)`, `fall(all_unsupported)`.
- КОЛИ `input(swap, a, b)` → ЯКЩО `has(player, diamonds)` → ТО `swap(a, b)`, `take(player, diamonds)`; після обміну можливий новий ланцюг (?).
- КОЛИ `custom: «поточний блок нікуди вистрілити і злиття неможливе»` → ТО `lose`, `window(end-screen)` (?).
- КОЛИ `game_over` → ЯКЩО `custom: «рахунок > рекорд»` → ТО `window(custom-window)` «New High Score!».
- Перемоги нема · Поразка: стос заповнив поле (?) · Рахунок: очки за злиття і кроки ланцюга, рекорд і глобальна таблиця.

## Керування і ввід
- Тач: перетягнути поточний блок під стовпець і відпустити — постріл («drag and shoot»); тап по стовпцю — (?).
- Бустер: натиснути кнопку молотка → тап по блоку; swap → вибрати два блоки.
- Haptic feedback на злиттях.

## Вікна, меню, HUD
- `game-screen`: поле 5 стовпців, поточний блок під полем, `next-queue` (1 блок), `score`, `hi-score`, лічильник діамантів (`coins`), кнопки бустерів, `popup-text` за кроки ланцюга.
- `custom-window` «New High Score!» з кубком (скриншот 5); `custom-window` відкриття нового номіналу (?).
- `shop-window`: пакети діамантів, AdFree Forever, X2 Premium і підписки (1/6/12 міс.).
- `leaderboard` — Global Leader Boards.
- `end-screen` (?), `settings-window` (?).
- Реклама: ad-break і банери між іграми; після «нескінченності» відгуки згадують перегляд відео заради переміщення/видалення числа.

## Фічі поза полем
- `autosave` партії; гра офлайн без мережі.
- `leaderboard-online`, рекорд.
- Монетизація: діаманти, підписки, AdFree; бустери за діаманти або рекламу (?).
- Режимів, рівнів і щоденних завдань у джерелах нема.

## Варіації й родичі
- Drop the Number і численні «2048 shoot/drop»-клони — те саме ядро (5 стовпців, постріл, злиття з кількома сусідами) (?).
- Родичі в корпусі: [2048](2048.md) (злиття однакових, номінали 2ⁿ), [2248](2248.md) і [just-get-10](just-get-10.md) (злиття групи), [threes](threes.md), [drop7](drop7.md) (кидок у стовпець + каскад), [suika-game](suika-game.md) (злиття при контакті).
- **Осі варіацій**: напрям гравітації (вниз / угору — X2) · скільки сусідів зливаються за раз (2 / усі однакові) · що дає злиття (×2 / ×2ᵏ за k сусідів) · запуск (кидок згори / постріл знизу) · допомога (молоток, swap, undo).

## Цікавинки для курсу
- Постріл угору до упору в стовпці з гравітацією «вгору» — 🌱 (той самий `fall`, лише знак напрямку).
- Злиття з усіма однаковими сусідами одразу + підтягування + каскад до стабілізації — 📎.
- Ланцюг із наростаючими +10/+20/+30 через `popup-text` — 🌱.
- Бустери «молоток» і «swap» як разові дії гравця поза ходом — 🌱.
- Простий AI «куди стріляти» (перебір 5 стовпців × симуляція каскаду) — 🥉.

## Мапа на каталог
- Є: `tile-merge` ↔ злиття однакових; `gravity-fall` ↔ осідання (угору); `chain-reaction` + `combo-multiplier` ↔ ланцюг; `popup-text` ↔ +10…+40; `next-queue` ↔ наступний блок; `drag-drop-piece` / `swipe-gestures` ↔ drag and shoot; `score-records` + `leaderboard` ↔ рекорд і глобальні таблиці; `save-autosave`; `shop-window` ↔ діаманти й підписки; `game-screen`, `end-screen`.
- **Нема** → пропозиції карток:
  - `+shoot-into-column` «Постріл блоком у стовпець до упору» · entities/move · 🌱 · слоти {direction: up|down}.
  - `+multi-neighbor-merge` «Злиття з усіма однаковими сусідами за один крок» · entities/legality · 📎 · слоти {result: ×2|×2ᵏ}.
  - `+booster-hammer` / `+booster-swap` «Разові бустери: прибрати блок / обміняти два» · game-logic/economy · 🌱.
  - `+rewarded-ad-continue` «Продовження/допомога за перегляд реклами» · game-logic/economy · 🌱.

## Пропозиції до словників
- `+cond:group_size` — розмір групи однакових сусідів визначає результат злиття (уже пропонувалось у корпусі).
- `+effect:launch` — постріл блоком уздовж стовпця до упору (відрізняється від `slide` тим, що стартує ззовні поля).
- `+feature:boosters` — разові інструменти допомоги за валюту (молоток, swap).
- `+card:shoot-into-column`, `+card:multi-neighbor-merge` — див. «Мапа на каталог».

## Джерела
- ⭐ [App Store: X2 Blocks](https://apps.apple.com/us/app/x2-blocks-2048-merge-puzzle/id1480338372) — опис («drag and shoot the block», комбо, номінали до ∞, без ліміту часу), фічі, покупки, версії; відгуки про превʼю наступного числа й бустери за діаманти.
- [iTunes lookup API](https://itunes.apple.com/lookup?id=1480338372&country=us) — дата релізу 2019-11-07, назва, 5 скриншотів (сітка 5 стовпців, постріл знизу, +10…+40, молоток, swap, New High Score).
- [BlueStacks: X2 Blocks](https://www.bluestacks.com/apps/puzzle/x2-blocks-on-pc.html) — розробник, пакет Android.
- [Google Play](https://play.google.com/store/apps/details?id=com.inspiredsquare.blocks) — сторінка існує, опис у фетчі не дістався.

## Непевне
- (?) Номінал після злиття k+1 однакових блоків (×2 чи ×2ᵏ) — джерело не каже; скриншот показує постріл 256 у клітину з трьома сусідами 256, але не результат.
- (?) Чи блок зливається й з сусідом знизу та по діагоналі — з памʼяті жанру лише 4-сусідство.
- (?) Висота поля (7 рядів) і точна умова поразки (стовпець повний / нема куди стріляти) — не перевірено.
- (?) Формула очок: +10/+20/+30/+40 на скриншоті можуть бути кроками ланцюга, а не номіналами.
- (?) Чи при відкритті нового великого номіналу найменший номінал зникає з поля й набору — у джерелах нема.
- (?) Drop the Number — окрема гра іншого видавця з тим самим ядром чи інша назва X2 Blocks: назва в черзі в дужках, джерел не знайдено.
- (?) Рік: App Store дає 2019-11-07, а рядок копірайту — «© 2016 Inspired Square».
