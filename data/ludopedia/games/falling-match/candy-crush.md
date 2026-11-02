---
title: Candy Crush Saga
slug: candy-crush
family: falling-match
also: []
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: runtime
  goal: state
year: 2012
platforms: [Facebook web, iOS, Android, Windows]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Candy_Crush_Saga", best: true, note: "обмін сусідів, каскади, цілі (желе, інгредієнти, очки), ліміт ходів, спецкукерки з 4+, 5 життів по 30 хв, епізоди по 15, монетизація"}
  - {kind: official, url: "https://www.candycrush.com/", note: "офіційний сайт (з king.com/game/candycrush)"}
  - {kind: official, url: "https://king.com/game/candycrush", note: "сторінка King (редирект)"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tile-matching_video_game", note: "Candy Crush як популяризатор рівнів з ціллю, ліміту ходів і saga-мапи"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=candy+crush+saga+special+candy+combinations", note: "пошук; комбінації спецкукерок"}
stage: v1
coverage: 65
mechanics: [cell-click, drag-drop-piece, swipe-gestures, gravity-fall, spawn-random-cell, collect-quota, collect-all, event-points, combo-multiplier, chain-detonation, blast-wave, sequential-levels, level-unlock, level-select, save-progress, shop-window, round-currency, inventory-items, end-screen, +match-3-swap, +chain-reaction, +cascade-refill, +special-tiles, +special-combos, +color-clear-special, +no-moves-detection, +hint-move, +countdown-tile, +level-goals, +move-limit, +layered-blocker, +spreading-blocker, +lock-overlay, +ingredient-drop, +star-thresholds, +end-bonus-conversion, +pre-level-boosters, +stamina-energy, +saga-map, +buy-extra-moves]
proposes: ["+trigger:settled", "+trigger:counter", "+trigger:turn_end", "+trigger:reach", "+cond:adjacent", "+cond:count", "+effect:swap", "+effect:clear_color", "+effect:explode_area", "+effect:clear_row_col", "+effect:spread", "+effect:layer_down", "+effect:reshuffle", "+effect:convert_specials", "+role:zone", "+ui:objective-panel", "+ui:countdown-on-tile", "+window:level-intro", "+window:out-of-moves-offer", "+window:map-window", "+feature:lives-regen", "+feature:world-map", "+feature:stars-rating", "+axis:session"]
author: opus
date: 2026-11-02
---

# Candy Crush Saga — match-3 обміном, але кожен рівень — задача: ціль + ліміт ходів + блокери, на мапі з життями

## Суть
Механіка поля — класичний match-3 (обмін двох сусідів лише зі збігом, каскади, поповнення згори), успадкований від Bejeweled. Новизна — **рівень як задача**: ціль (очки / зняти все желе / довести інгредієнти донизу / зібрати замовлення / змішані) і **ліміт ходів**, на полі — нерухомі форми, блокери з шарами, шоколад, що розростається, бомби з лічильником. Довкола — **мета-шар**: 1–3 зірки, 5 життів із відновленням, бустери, «+5 ходів» за валюту, лінійна saga-мапа з епізодами по 15 рівнів. Для курсу це еталон **таксономії цілей** і того, як дані рівня (форма, шари, цілі) перетворюють одне ядро на тисячі задач.

## Поле і час
- Поле до 9×9 (?) довільної форми: частина клітин відсутня (дірки, острови); 4–6 кольорів цукерок залежно від рівня.
- **Шари клітини** (знизу вгору): основа (желе 1–2 шари / порожньо) → цукерка або блокер → накладка (лакричний замок, обгортка). Плюс сутності рівня: вихідні стрілки інгредієнтів, портали, конвеєр (?), генератори.
- Покроково: хід = обмін; далі автоматична фаза каскаду до стабілізації; потім ходи блокерів (шоколад, лічильники бомб); потім перевірка цілі/ходів. Таймерні рівні (Timed) існували раніше (?).
- Поповнення: нові цукерки падають у стовпці з верхніх (або позначених) клітин-спавнерів; через дірки цукерки можуть «сповзати» по діагоналі (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Звичайна цукерка | tile | колір (6) | обмін із сусідом; 3+ в ряд → зникає; падає |
| Смугаста (striped) | tile | колір, напрям (гориз./верт.) | з 4 в лінію; у збігу або від вибуху чистить свій рядок або стовпець |
| Обгорнута (wrapped) | tile | колір | з L/T 5; вибухає 3×3, падає, вибухає вдруге (?) |
| Кольорова бомба (colour bomb) | tile | без кольору | з 5 в лінію; обмін з цукеркою → зникає весь цей колір |
| Рибка (jelly fish) | tile | колір | з квадрата 2×2 (?); пливе й зʼїдає 1 ціль (желе/блокер), пріоритет цілей (?) |
| Желе (jelly) | zone | 1–2 шари | знімається шар збігом/вибухом на клітині; ціль Jelly-рівнів |
| Інгредієнт (вишня, фундук) | object | — | не збігається; падає з каскадами; на клітині-виході внизу → зібрано |
| Лакричний замок (licorice lock) | gate | 1 шар | цукерка під ним не рухається; збіг із нею знімає замок |
| Лакричний вихор (licorice swirl) | hazard | — | займає клітину, падає, не збігається; знищується сусіднім збігом; гасить смугасті промені (?) |
| Шоколад (chocolate) | hazard | — | знищується сусіднім збігом; ЯКЩО за хід не знищено жодного → розростається на 1 сусідню клітину |
| Безе / frosting (meringue) | hazard | 1–5 шарів | нерухомий; сусідній збіг знімає шар |
| Цукеркова бомба (candy bomb) | hazard | колір, лічильник ходів | збіг знищує; лічильник −1 за хід; 0 → програш рівня |
| Мармелад (marmalade) | gate | — | обгортає цукерку/спецкукерку; збиття — звільняє (?) |
| Шоколадний фонтан / генератор | spawner | — | породжує шоколад або блокери (?) |
| Торт-бомба (cake bomb) | hazard | 8 частин | знищується по частинах; повне знищення — вибух на півполя (?) |
| Таємнича цукерка (mystery) | container | — | знищення відкриває випадковий бонус чи блокер (?) |
| Клітина-вихід інгредієнта | static | стрілка | інгредієнт на ній → `counter(ingredients, +1)` |
| Портал | static | пара вхід/вихід | цукерки падають крізь нього в інший стовпець (?) |
| Спавнер зверху | spawner | колір/тип за даними рівня | породжує цукерки, інгредієнти, бомби в межах квоти рівня |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(swap a, b)` → ЯКЩО `adjacent(a, b) and not occupied(a|b, lock)` → ТО `swap(a, b)`; ЯКЩО нема `pattern(line(3+))` і жодна не спецкукерка в комбінації → ТО `custom: «revert_swap»`, хід не витрачено.
- КОЛИ легальний обмін → ТО `counter(moves_left, −1)`.
- КОЛИ `pattern(line(3, color))` → ТО `clear(cells)`, `score(60)` (?), `custom: «layer_down — желе/замок під клітинами −1»`, `custom: «layer_down — сусідні безе/шоколад/вихор −1»`.
- КОЛИ `pattern(line(4))` → ТО `spawn_at(striped, swap_cell)`; напрям смуг залежить від напряму обміну/лінії (?).
- КОЛИ `pattern(L|T, 5)` → ТО `spawn_at(wrapped)`; `pattern(square 2×2)` → `spawn_at(fish)`; `pattern(line(5))` → `spawn_at(colour_bomb)`.
- КОЛИ `clear(striped)` → ТО `custom: «clear_row_col — увесь рядок або стовпець»`; `clear(wrapped)` → ТО `explode(3×3)`, `fall`, `explode(3×3)`; спецкукерка, зачеплена ефектом, спрацьовує (`chain-detonation`).
- КОЛИ `input(swap colour_bomb, candy)` → ТО `clear_color(candy.color)`.
- Комбінації двох спецкукерок обміном: striped + striped → рядок + стовпець · striped + wrapped → 3 рядки + 3 стовпці · wrapped + wrapped → вибух 5×5 (двічі (?)) · colour bomb + striped → усі цукерки кольору стають смугастими й спрацьовують · colour bomb + wrapped → колір зникає, потім ще один (?) · colour bomb + colour bomb → очищення всього поля · fish + спец → рибки несуть спецефект (?).
- КОЛИ `after(clear)` → ТО `fall(tiles)`, `spawn_at(random_candy, spawners)`; КОЛИ `pattern` знову → `clear`, `combo(+1)`, `score(× cascade)`; до `settled`.
- КОЛИ `settled` → ЯКЩО `not destroyed_this_turn(chocolate)` → ТО `custom: «spread — шоколад займає 1 сусідню клітину»`; КОЛИ `turn_end` → ТО `counter(bomb, −1)`; КОЛИ `counter(bomb, ==, 0)` → ТО `lose`.
- КОЛИ `reach(ingredient, exit_cell)` → ТО `disappear_a`, `counter(ingredients, +1)`.
- КОЛИ `settled` → ЯКЩО `no_moves(player)` → ТО `custom: «reshuffle»` (без витрати ходу).
- **Цілі рівня** (`counter`): Moves — `score ≥ target` (ранні рівні, далі прибрані (?)) · Jelly — `count(jelly, ==, 0)` · Ingredients — `counter(ingredients, ==, n)` · Candy Order — зібрати N цукерок кольору / N спецкукерок / N комбінацій / N блокерів · Mixed — кілька цілей одночасно · Timed — очки за час (?) · Rainbow Rapids — провести «райдужний потік» до цілей (?).
- КОЛИ `all_goals_met` → ТО `custom: «Sugar Crush — решта ходів стають спецкукерками/рибками й спрацьовують на бонусні очки»`, `win`.
- КОЛИ `counter(moves_left, ==, 0)` → ЯКЩО `not all_goals_met` → ТО `window(out-of-moves-offer)` (+5 ходів за золото); відмова → `lose`, `lives(−1)`.
- Рахунок: очки за цукерку/спецкукерку/каскад + Sugar Crush; зірки: 1★ = мінімум для проходження (?) у Moves; 2★ і 3★ — пороги очок, показані смужкою.
- Мета: КОЛИ `lose` → ТО `lives(−1)`; КОЛИ `lives < 5` → ТО `timer(30 хв)` → `lives(+1)`; КОЛИ `lives == 0` → ТО гра недоступна (чекати / попросити друзів / купити).
- Мета: КОЛИ `win(level)` → ТО `unlock(next_level)`; кінець епізоду (15 рівнів) → в оригіналі ворота: 3 запити друзів / оплата / чекання.

## Керування і ввід
- Тач — свайп цукерки в бік сусіда; миша — drag або клік-клік (Facebook).
- Бездіяльність кілька секунд → анімація-підказка можливого ходу (`hint-move`).
- In-game бустери (вибір іконкою, потім ціль): льодяниковий молот — прибрати одну клітину без ходу; free switch — обмін будь-яких двох сусідів без збігу (?); смугастий пензель — зробити цукерку смугастою (?); party booster — удар по всьому полю (?).
- Pre-level бустери (галочки у вікні рівня): colour bomb + fish, striped + wrapped, coconut wheel, +3 ходи, lucky candy (?).

## Вікна, меню, HUD
- `splash-screen` (King) → `custom: «saga map»` (`map-window`): вертикальна доріжка рівнів по епізодах, аватари друзів на їхніх рівнях, зірки під пройденими, події.
- `custom: «level-intro»` — вікно рівня: номер, ціль словами й іконками, рекорд друзів, вибір pre-level бустерів, кнопка Play (знімає життя лише при програші).
- `game-screen`: поле; `custom: «objective-panel»` (іконки цілей з лічильниками «лишилось»), `move-counter` «Moves», `score` + `progress-bar` із трьома зірками-порогами, панель in-game бустерів; `custom: «countdown-on-tile»` (число на бомбі); `popup-text` очок; голосові «Sweet / Tasty / Delicious / Divine» за каскади (?).
- `custom: «out-of-moves-offer»` — «+5 ходів» за золоті злитки перед програшем.
- `end-screen`: перемога — зірки, очки, таблиця друзів по рівню; поразка — «Level Failed», мінус життя, Retry.
- `shop-window` — золоті злитки, бустери, набори; `custom: «lives-window»` — таймер наступного життя, «попросити друзів».
- `settings-window`: звук, музика, мова, підключення Facebook/King account.
- `daily-window` — щоденне колесо бустерів (Daily Booster Wheel) (?).
- Переходи: splash → map → level-intro → game-screen → (ціль) Sugar Crush → end-screen win → map (наступний рівень); (ходи 0) offer → end-screen fail → map / retry.

## Фічі поза полем
- `world-map` (saga map) + `levels-sequential` + `level-unlock`; епізоди по 15; понад 2000 рівнів (2016), нові — регулярно.
- `stars-rating` 1–3 за рівень; `leaderboard-online` по рівню серед друзів.
- `custom: «lives-regen»` — 5 життів, +1 за 30 хв; запит життів у друзів (Facebook).
- `shop-window` + `round-currency`-подібна валюта (gold bars) поза раундом: життя, ходи, бустери, відкриття епізоду.
- `cloud-save` — прогрес синхронізується між Facebook і мобільним.
- Події й ліги (Sugar Track, турніри) (?); історичний режим Dreamworld (Odus, Moon Struck) — прибрано.
- `onboarding-hints` — навчальні підказки при першій появі кожного елемента.

## Варіації й родичі
- Bejeweled (ядро обміну) → Candy Crush (2012, цілі + ліміт ходів + saga) → Candy Crush Soda Saga (вода/газування), Jelly Saga (желе, що розтікається, бос), Farm Heroes Saga (збір елементів) — усе від King; Homescapes/Gardenscapes, Royal Match (мета «будуй будинок»).
- **Осі варіацій**: ціль (очки / прибрати шар / довести обʼєкт / замовлення / мікс) · ресурс (ходи / час) · блокер (замок / шари / розростання / лічильник / генератор) · мета (мапа / будинок / сюжет) · штраф програшу (нема / життя з таймером).
- Таксономія цілей Candy Crush — готовий словник `win`-умов для будь-якої сіткової гри.

## Цікавинки для курсу
- Рівень як дані: форма поля + шари клітин + цілі + ліміт ходів у файлі — 🥉 (парсер + валідатор + 3 типи цілей).
- Таксономія цілей з HUD-лічильниками й мікс-цілями — 📎 за тип, 🥉 за 3+.
- Спецкукерки з розпізнаванням форми (4 / L-T / 2×2 / 5) і таблиця комбінацій двох спецкукерок — 🥈 (матриця взаємодій як дані).
- Шоколад, що розростається, якщо за хід не знищено жодного — 📎 (стан «за цей хід»).
- Блокери з шарами (желе, безе) і накладки-замки — 📎.
- Інгредієнти, що падають до клітин-виходів крізь каскади — 📎.
- Sugar Crush — конвертація залишку ходів у бонусні спрацювання — 🌱.
- Мета-шар: зірки, життя з таймером реального часу, saga-мапа зі збереженням — 🥉 (час між сесіями).

## Мапа на каталог
- Є: `cell-click` · `drag-drop-piece` · `swipe-gestures` · `gravity-fall` · `spawn-random-cell` · `collect-quota` (інгредієнти, замовлення) · `collect-all` (усе желе) · `event-points` · `combo-multiplier` (каскад) · `chain-detonation` (спецкукерка підриває іншу) · `blast-wave` (обгорнута, 3×3) · `sequential-levels` · `level-unlock` · `level-select` (мапа) · `save-progress` · `shop-window` · `round-currency` (золото — поза раундом, найближча) · `inventory-items` (бустери) · `end-screen`.
- **Нема** → пропозиції карток:
  - `+match-3-swap` · `+chain-reaction` · `+cascade-refill` · `+special-tiles` · `+no-moves-detection` · `+hint-move` · `+countdown-tile` — спільні з Bejeweled.
  - `+special-combos` «Комбінації двох спецплиток» · entities/interact · 🥈 · слот {table}.
  - `+color-clear-special` · entities/interact · 🌱 (спільна з Magical Drop/Columns).
  - `+level-goals` «Ціль рівня з таксономії» · game-logic/win · 🥉 · слот {kinds: score|clear-layer|bring-down|order|mixed}.
  - `+move-limit` «Ліміт ходів на рівень» · game-logic/lose · 🌱 · слот {moves} (спільна з Flood).
  - `+layered-blocker` «Блокер із шарами» · entities/state · 📎 · слот {layers: 1..5}.
  - `+spreading-blocker` «Блокер, що розростається» · entities/spawn · 📎 · слот {rule: if_none_destroyed}.
  - `+lock-overlay` «Замок-накладка на плитці» · entities/legality · 🌱.
  - `+ingredient-drop` «Довести обʼєкт до клітини-виходу» · game-logic/win · 📎.
  - `+star-thresholds` «1–3 зірки за порогами очок» · game-logic/score · 🌱.
  - `+end-bonus-conversion` «Залишок ресурсу → бонусні дії» · game-logic/score · 🌱 (Sugar Crush).
  - `+pre-level-boosters` «Бустери перед рівнем» · game-logic/economy · 📎.
  - `+stamina-energy` · game-logic/economy · 📎 (спільна з P&D; тут — життя з таймером).
  - `+saga-map` «Лінійна мапа рівнів з епізодами» · levels/progression · 📎.
  - `+buy-extra-moves` «Продовжити за валюту» · game-logic/economy · 🌱.

## Пропозиції до словників
- `+trigger:settled` · `+trigger:counter` · `+trigger:turn_end` — 🔥 підтверджую (каскад скінчився → ходи блокерів; ціль/ходи; лічильник бомби).
- `+trigger:reach` — ⏳ підтверджую: інгредієнт досяг клітини-виходу.
- `+cond:adjacent` — як у Bejeweled; `+cond:count` — 🔥 підтверджую (желе = 0).
- `+effect:swap` — 🔥; `+effect:clear_color`, `+effect:explode_area`, `+effect:clear_row_col`, `+effect:reshuffle` — як у Bejeweled, підтверджую.
- `+effect:spread` — сутність займає сусідню клітину за правилом (шоколад; Jelly Saga; родич Life).
- `+effect:layer_down` — зняти шар з багатошарової сутності/клітини (желе, безе, frosting); не `damage`, бо шари видимі й мають ціль.
- `+effect:convert_specials` — перетворити залишок ресурсу на спецплитки (Sugar Crush).
- `+role:zone` — 🔥 підтверджую: желе як шар клітини.
- `+ui:objective-panel` — іконки кількох цілей з лічильниками (не `objective-text`); `+ui:countdown-on-tile` — як у Bejeweled.
- `+window:level-intro` — вікно перед рівнем (ціль + бустери + Play); `+window:out-of-moves-offer` — «продовжити за валюту?» (родич `game-over-continue`); `+window:map-window` — 🔥 підтверджую.
- `+feature:lives-regen` — життя, що відновлюються за реальним часом; `+feature:world-map`, `+feature:stars-rating` — 🔥 підтверджую.
- `+axis:session` — `level` + мета між рівнями (час реального світу).

## Джерела
- ⭐ [Wikipedia: Candy Crush Saga](https://en.wikipedia.org/wiki/Candy_Crush_Saga) — обмін, каскади, желе, інгредієнти, ліміт ходів, спецкукерки з 4+, лакриця й шоколад, бустери, 5 життів / 30 хв, епізоди по 15, ворота епізодів, Dreamworld, монетизація, 2000+ рівнів.
- [Wikipedia: Tile-matching video game](https://en.wikipedia.org/wiki/Tile-matching_video_game) — Candy Crush як популяризатор рівнів з цілями, ліміту ходів і saga-підходу.
- [candycrush.com](https://www.candycrush.com/) · [king.com/game/candycrush](https://king.com/game/candycrush) — офіційні сторінки (без опису механік у тексті).
- YouTube: пошук «candy crush saga special candy combinations».

## Непевне
- Фан-вікі candycrush.fandom.com не відкрилась (HTTP 402), WebSearch вичерпано — назви й правила спецкукерок, блокерів і бустерів понад Wikipedia — з памʼяті.
- (?) Розмір 9×9, очки 60 за трійку, голосові «Sweet/Tasty/Delicious/Divine».
- (?) Від чого залежить напрям смугастої (напрям обміну чи лінії), подвійний вибух обгорнутої, рибка з квадрата 2×2 і її пріоритет цілей.
- (?) Точні ефекти комбінацій colour bomb + wrapped, wrapped + wrapped (5×5 двічі), fish + спец.
- (?) Мармелад, торт-бомба, таємнича цукерка, фонтан, портали, діагональне сповзання, Rainbow Rapids, долі Moves/Timed-рівнів (переробки 2016–2018), Sugar Track, колесо бустерів, набір in-game бустерів.
