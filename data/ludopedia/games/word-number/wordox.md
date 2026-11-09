---
title: Wordox
slug: wordox
aka: [Wordox - Multiplayer word game]
family: word-number
also: [chess-abstract]
klass: cursor
axes:
  field: square
  time: turn
  opponent: online
  info: full
  random: runtime
  goal: race
year: 2000
platforms: [PC, web, Facebook, iOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Scrabble_variants", best: true, note: "розділ Wordox: Othello + Scrabble, 13×13, спільна стійка 7, колір плиток, очки за свій колір, рожеві й помаранчеві клітини"}
  - {kind: wiki, url: "https://fr.wikipedia.org/wiki/Wordox", note: "історія (березень 2000, WON.net → flipside → cafe.com → Facebook → IsCool), очищення поля зі збереженням рахунку, гра до заданого рахунку"}
  - {kind: official, url: "https://iscool.helpshift.com/hc/en/3-wordox-mobile/faq/5-game-rules", note: "FAQ IsCool: 2 гравці, спільна стійка 6, 1 очко за літеру, до 25, перше слово через центр"}
  - {kind: official, url: "https://iscool.helpshift.com/hc/en/3-wordox-mobile/faq/8-how-do-you-steal-letters/", note: "крадіжка: NOT → NOTES, +2 і +3 вкрадені, суперник −3"}
  - {kind: official, url: "https://iscool.helpshift.com/hc/en/3-wordox-mobile/faq/9-why-are-there-stars-on-the-game-board/", note: "16 зірок, лічильник зірок, вихор (Vortex)"}
  - {kind: official, url: "https://iscool.helpshift.com/hc/en/3-wordox-mobile/faq/213-should-you-skip-your-turn/", note: "2 пропуски чистять стійку, 3 поспіль — поле"}
  - {kind: other, url: "https://apps.apple.com/us/app/wordox-multiplayer-word-game/id582340397", note: "App Store (IsCool, 2012): крадіжка очок, AI-челендж, монети, тижневі події"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=wordox+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [cursor-place, drag-drop-piece, word-validation, turn-enforcement, pass-turn, online-multiplayer, async-multiplayer, ai-opponent, event-points, round-currency, leaderboard, profile-stats, game-screen, end-screen, shop-window, help-window, lobby-window, +claim-by-word, +shared-rack, +word-steal-by-extension, +board-wipe-square, +star-bank, +skip-refresh]
proposes: ["+trigger:passes", "+effect:refill", "+ui:shared-rack", "+ui:star-counter", "+window:league-window", "+window:daily-bonus", "+feature:league", "+feature:daily-bonus", "+card:shared-rack", "+card:word-steal-by-extension", "+card:board-wipe-square"]
author: opus
date: 2026-11-09
---

# Wordox — Scrabble з кольорами Othello: спільна стійка, слово перефарбовує чужі літери, вихор стирає поле

## Суть
Двоє гравців по черзі складають слова на спільному полі з **однієї спільної стійки** літер: що не взяв ти, дістається супернику. Кожна викладена плитка — твого кольору, а очко дає кожна літера твого кольору; продовживши слово суперника (NOT → NOTES), ти перефарбовуєш його літери й забираєш його очки. Премій ×2/×3 нема; натомість є клітини-«вихори», що стирають поле (рахунок лишається), і зірки, які банкуються при вихорі. Гра йде до заданого рахунку — у мобільній версії до 25.

## Поле і час
- Квадратна сітка; в оригіналі (WON.net) — 13×13; спецклітини стоять там, де в Scrabble премії. Розмір мобільного поля — (?).
- Шари: клітина (звичайна / центр / зірка / вихор) + плитка з власником (колір гравця).
- Хід = одне слово або пропуск. Онлайн, «у своєму темпі» (асинхронно) (?).
- Інформація повна: стійка спільна й відкрита обом; випадковість — у поповненні стійки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка-літера | tile | літера, власник (колір) | кладеться зі стійки; змінює власника, коли входить у нове слово суперника |
| Спільна стійка | supply | 7 плиток (оригінал) / 6 (IsCool) | обидва гравці беруть з неї; поповнюється після ходу |
| Центральна клітина | zone | — | перше слово на порожньому полі мусить через неї пройти |
| Зірка | zone | 16 на полі (IsCool) | плитка на зірці дає гравцю зірку в банк |
| Вихор (рожева / червона клітина) | zone | — | слово з плиткою на ньому стирає поле; зірки конвертуються |
| Помаранчева клітина (оригінал) | zone | — | при стиранні — бонус-очко за кожну свою плитку на ній |
| Джокер (IsCool) | pickup | купується / дається | допомагає не втратити хід (?) |
| Гравець | player | колір, очки, банк зірок | 2 сторони, хід по черзі |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «кожному гравцю колір»`, `custom: «спільна стійка набирається з мішка»`.
- КОЛИ `input(play word)` → ЯКЩО перший хід → ТО слово мусить покрити центральну клітину.
- КОЛИ `input(play word)` → ЯКЩО не перший хід and `custom: «слово торкається наявної літери»` and `in_dictionary(word)` → ТО `place(player, tiles)`; інакше `block`.
- Слова — по горизонталі або вертикалі; заборонені слова — за власним словником гри (окремі FAQ про допустимі двобуквені й відхилені слова).
- КОЛИ `input(play word)` → ЯКЩО `legal(move)` → ТО `set_side(all_tiles_of_word, me)`, `score(+1 × нових плиток)`, `score(+1 × перефарбованих чужих)`, `custom: «суперник −1 за кожну перефарбовану»`, `end_turn`.
- Приклад крадіжки: КОЛИ `input(play «ES»)` → ЯКЩО `custom: «ES продовжує чуже слово NOT до NOTES»` → ТО `set_side(N, O, T → me)` — мені +5 (2 за ES, 3 за NOT), супернику −3.
- КОЛИ `after(play)` → ТО `custom: «у спільну стійку добираються літери з мішка»` — наступний гравець бачить і бере те, що лишилось.
- КОЛИ `enter(tile, star)` → ТО `counter(stars_me, +1)` (IsCool).
- КОЛИ `enter(tile, vortex)` → ТО `score(+stars_me)`, `counter(stars_me, =0)`, `counter(stars_opponent, =0)`, `clear(all)` — поле порожніє, рахунок лишається.
- Оригінал: КОЛИ `enter(tile, pink)` → ТО `score(+1 × своїх плиток на помаранчевих клітинах)`, `clear(all)`.
- КОЛИ `input(skip)` → ТО `pass_turn`.
- КОЛИ `custom: «два пропуски»` → ТО `custom: «спільна стійка очищається й набирається заново»`.
- КОЛИ `custom: «три пропуски поспіль»` → ТО `clear(all)`.
- КОЛИ `counter(score, >=, 25)` → ТО `win`, `game_over` (IsCool; в оригіналі — рахунок, узгоджений наперед).
- Перемога: першим досягти цільового рахунку · Поразка: суперник дійшов першим · Рахунок: +1 за кожну свою літеру, яку поставив або перефарбував; −1 за кожну, яку перефарбували в тебе; зірки при вихорі.

## Керування і ввід
- Перетягування плиток зі спільної стійки на клітини, підтвердження слова (?); кнопка пропуску ходу.
- Вибір суперника: випадковий онлайн, друг, AI-челендж (App Store).
- Push-сповіщення про хід суперника (FAQ про сповіщення iOS/Android).

## Вікна, меню, HUD
- `game-screen`: поле зі зірками й вихорами, `shared-rack`, рахунки обох, `star-counter` над рахунком, `turn-indicator`; червона смуга внизу з часом до кінця ліги.
- `lobby-window`: старт гри з випадковим суперником або другом (?).
- `daily-bonus`: щоденний бонус.
- `league-window`: ліга на кілька днів, рейтинг за монетами з онлайн-ігор, кнопка Awards.
- `shop-window`: покупка джокерів і фішок/монет.
- `profile-window` / `stats-window`: акаунт на кількох пристроях (?).
- `help-window`: FAQ з правилами.
- `end-screen`: переможець, монети за гру (?).
- Переходи: `lobby-window` → `game-screen` → (25 очок) `end-screen` → `lobby-window`.

## Фічі поза полем
- `online-multiplayer` по черзі «у своєму темпі» (`async-multiplayer`) (?), `ai-opponent-levels`-подібний AI-челендж (App Store).
- `league` — багатоденне змагання за монетами з будь-яких онлайн-ігор, нагороди.
- `daily-bonus`, валюта (монети, фішки), джокери за гроші.
- Шість мов (мобільна версія IsCool, кінець 2012).

## Варіації й родичі
- Історія: WON.net (оригінал) → flipside.fr → cafe.com (2008–2011) → Facebook (2012) → iOS / Android від IsCool Entertainment (2012). Wordsteal і Fundox — пізніші ігри з тією ж ідеєю.
- Оригінал vs IsCool: стійка 7 / 6 плиток; рожеві (очищення) + помаранчеві (бонус) клітини / вихор + 16 зірок; заданий рахунок / 25.
- **Осі варіацій:** власність плитки (нема — `scrabble.md` / колір і перефарбування — тут, `letterpress.md`) · стійка (своя прихована / спільна відкрита) · очки (вартість літер і премії / 1 за свою плитку) · скидання поля (нема / клітина-вихор / три паси).
- Родичі: `scrabble.md` (лінійне викладання), `letterpress.md` (перефарбування словом, але без розміщення), `mojipittan.md` (versus перефарбовує клітини довшим словом), `upwords.md` (зміна чужого слова надбудовою).

## Цікавинки для курсу
- Власник плитки як поле стану + перерахунок очок як різниця «моїх» і «чужих» при перефарбуванні — 🌱.
- Спільна стійка: хід одного змінює вибір іншого; поповнення з мішка — 📎.
- Перевірка ходу: лінія, звʼязність, перший хід через центр, усі утворені слова в словнику — 🥈 (як у Scrabble).
- Вихор: очищення поля зі збереженням рахунку й конвертацією банку зірок — 📎.
- Лічильник пропусків поспіль (2 → нова стійка, 3 → чисте поле) — 🌱.
- AI, що оцінює хід як «скільки перефарбую мінус що залишу супернику в стійці» — 🥇.

## Мапа на каталог
- Є: `cursor-place` / `drag-drop-piece` ↔ плитки зі стійки · `word-validation` · `turn-enforcement` · `pass-turn` ↔ пропуск · `online-multiplayer` / `async-multiplayer` · `ai-opponent` · `event-points` ↔ 1 очко за літеру · `round-currency` ↔ монети · `leaderboard` ↔ ліга · `profile-stats` · `game-screen`, `end-screen`, `shop-window`, `help-window`, `lobby-window`.
- **Нема** → пропозиції карток:
  - `+claim-by-word` (з `letterpress.md`) — слово перефарбовує плитки в колір гравця.
  - `+shared-rack` «Спільна відкрита стійка для обох гравців» · entities/spawn · 📎.
  - `+word-steal-by-extension` «Продовж чуже слово — забери його очки» · game-logic/score · 📎.
  - `+board-wipe-square` «Клітина, що стирає поле зі збереженням рахунку» · entities/interact · 🌱.
  - `+star-bank` «Банк бонусів, що конвертується при події» · game-logic/score · 🌱.
  - `+skip-refresh` «Пропуски поспіль оновлюють стійку / поле» · game-logic/opponent · 🌱.

## Пропозиції до словників
- `+trigger:passes` — N пропусків поспіль (уже просили з го; тут 2 → стійка, 3 → поле).
- `+effect:refill` — поповнити / замінити запас (стійку) (уже просили в корпусі).
- `+ui:shared-rack` — стійка літер, спільна для обох гравців; `+ui:star-counter` — банк зірок над рахунком.
- `+window:league-window` — багатоденна ліга з нагородами; `+window:daily-bonus` — щоденний бонус.
- `+feature:league` — сезонний рейтинг за валютою з усіх партій; `+feature:daily-bonus`.
- `+card:shared-rack`, `+card:word-steal-by-extension`, `+card:board-wipe-square` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Scrabble variants — Wordox](https://en.wikipedia.org/wiki/Scrabble_variants) — Othello + Scrabble, 13×13, спільна стійка 7, кольори, 1 очко за свою плитку, рожеві (очищення) і помаранчеві (бонус) клітини, WON.net 1999.
- [Wikipedia FR: Wordox](https://fr.wikipedia.org/wiki/Wordox) — винайдено в березні 2000 двома американськими програмістами; спільна стійка «успадковує» залишок суперника; червоні клітини чистять поле, рахунок лишається; гра до заданого рахунку; історія платформ.
- [IsCool FAQ: Game Rules](https://iscool.helpshift.com/hc/en/3-wordox-mobile/faq/5-game-rules) — 2 гравці, спільна стійка 6, 1 очко, до 25, центр і звʼязність.
- [IsCool FAQ: How do you steal letters?](https://iscool.helpshift.com/hc/en/3-wordox-mobile/faq/8-how-do-you-steal-letters/) — приклад NOT → NOTES.
- [IsCool FAQ: stars](https://iscool.helpshift.com/hc/en/3-wordox-mobile/faq/9-why-are-there-stars-on-the-game-board/) — 16 зірок, вихор конвертує / спалює зірки.
- [IsCool FAQ: Should You Skip Your Turn?](https://iscool.helpshift.com/hc/en/3-wordox-mobile/faq/213-should-you-skip-your-turn/) — 2 пропуски → нова стійка, 3 поспіль → чисте поле.
- [IsCool FAQ: Wordox League](https://iscool.helpshift.com/hc/en/3-wordox-mobile/faq/207-how-does-wordox-league-work/) — ліга за монетами, червона смуга з часом, Awards.
- [App Store: Wordox](https://apps.apple.com/us/app/wordox-multiplayer-word-game/id582340397) — опис IsCool, реліз 2012-12-18.
- YouTube: пошук «wordox gameplay».

## Непевне
- (?) Рік: FR-вікі — березень 2000; EN-вікі — запуск на WON.net у 1999.
- (?) Чи крадіжка працює лише продовженням у кінці слова (FAQ показує суфікс), чи й префіксом і перехресними словами; чи перефарбовуються літери перпендикулярних слів.
- (?) Як саме нараховуються очки при стиранні поля в мобільній версії (вихор = рожева клітина оригіналу — моє зіставлення).
- (?) «Два пропуски» — двоє гравців по разу чи один гравець двічі; чи стійка повністю міняється.
- (?) Функція джокера («щоб не втратити хід») — не розписана.
- (?) Розмір мобільного поля, наявність таймера ходу, асинхронність — не бачив (сторінка PhoneArena віддала 403).
