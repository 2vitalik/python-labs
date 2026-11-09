---
title: Duplicate Scrabble (Scrabble duplicate)
slug: duplicate-scrabble
aka: [Scrabble duplicate, Duplicate, Дуплікат, Topping]
family: word-number
also: [board-digital]
klass: cursor
axes:
  field: square
  time: wego
  opponent: none
  info: full
  random: runtime
  goal: score
year: 1972
platforms: [board, PC, web]
links:
  - {kind: wiki, url: "https://fr.wikipedia.org/wiki/Scrabble_duplicate", best: true, note: "повні правила: тираж і rejet (2+2 голосні/приголосні до 15-го ходу), reliquat, бюлетені, top, нічия за «відкриває поле», кінець гри, 3 / 2 / 1 хв, нотація, формати турнірів, програми DupliTop та ін., історія"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Duplicate_Scrabble", note: "спільна рука 7 літер, слипи з рахунком і позицією, найкращий хід на дошку, 0 за невалідне, відсоток / мінус від top, понад 1000 гравців в одній грі, пари, Wouters"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Scrabble_variants", note: "розділ Duplicate: рекорд 1485 гравців (Віші, 1998), основний формат франкомовних чемпіонатів світу"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=scrabble+duplicate+partie", note: "пошук; партії й трансляції турнірів"}
stage: v1
coverage: 65
mechanics: [word-validation, move-timer, event-points, leaderboard, profile-stats, game-screen, end-screen, +premium-squares, +tile-rack, +tile-bag-draw, +line-placement, +cross-word-scoring, +bingo-bonus, +blank-tile, +move-generator, +shared-rack, +top-move-advance, +rack-balance-rule, +percent-of-top]
proposes: ["+cond:rack_balance", "+ui:slip-input", "+ui:top-history", "+feature:topping-mode", "+feature:simultaneous-tournament", "+card:shared-rack", "+card:top-move-advance", "+card:rack-balance-rule", "+card:percent-of-top"]
author: opus
date: 2026-11-09
---

# Duplicate Scrabble — усі отримують ту саму руку на тій самій дошці; на дошку йде найкращий хід, а рахуєш лише свій

## Суть
Турнірна форма Scrabble (`scrabble.md`), популярна у франкомовних країнах. Арбітр витягає 7 літер, усі гравці бачать ту саму дошку й ту саму руку і за обмежений час записують свій найкращий хід із рахунком. Потім на спільну дошку кладуть **top** — найдорожчий можливий хід (з кінця 1980-х його знаходить програма), — і всі продовжують з однакової позиції. Удачі в тиражі нема: кожен змагається з оптимумом, а місце визначає сума власних очок.

## Поле і час
- Поле, премії, вартості й бінго — як у `scrabble.md` (французькі турніри — за словником ODS).
- `time: wego`: усі думають одночасно (зазвичай 3 хв на хід; semi-rapide — 2, blitz — 1), потім один спільний хід на дошці. Партія на 3 хв — близько 2 годин.
- Суперника за дошкою нема: позицію рухає top, тому гравці один на одного не впливають — гра на будь-яку кількість учасників (понад 1000 в одному залі; світовий simultané — понад 5000).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Спільна рука (тираж) | supply | 7 плиток, однакова для всіх | після ходу reliquat лишається, решту добирають до 7 |
| Мішок | container | плитки Scrabble | арбітр тягне наосліп; rejet повертає 7 літер назад |
| Майстер-дошка | zone | 15 × 15 з преміями | на неї кладуть лише top |
| Бюлетень (slip) | mark | слово, позиція, рахунок | один на хід від гравця / пари |
| Top | static | найкращий хід ходу | рахується програмою; кладеться на дошки всіх |
| Арбітр | neutral | — | тягне й оголошує літери, обирає top при нічиїй |
| Гравець / пара | player | сума очок, % від top | пара домовляється про одну відповідь |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start` → ТО `give(rack, до 7 з мішка)` — reliquat попереднього ходу лишається; літери оголошують усім.
- КОЛИ `after(give)` → ЯКЩО `custom: «ходи 1–15: < 2 голосних або < 2 приголосних; з 16-го: < 1 голосної або < 1 приголосної»` (`+cond:rack_balance`) → ТО `custom: «rejet: усі 7 літер у мішок, перемішати, новий тираж»`; Y і джокер рахує як голосну чи приголосну той, хто тягне.
- КОЛИ `timer(3 min)` (2 — semi-rapide, 1 — blitz) → ТО `custom: «бюлетені закрито»`.
- КОЛИ `custom: «бюлетень гравця»` → ЯКЩО `not in_dictionary(word)` або `not legal(move)` → ТО `score(0)` гравцю за цей хід; інакше `score(points)` — лише йому, на дошку його хід не йде.
- КОЛИ `custom: «бюлетені закрито»` → ТО `place(top, master_board)` на всіх дошках; ЯКЩО `custom: «кілька ходів з однаковим top»` → ТО арбітр обирає той, що «найбільше відкриває поле».
- Бінго, премії, бланк — за `scrabble.md`: 7 плиток за хід = +50; джокер у нотації — літера в дужках / мала.
- КОЛИ `custom: «лишилась одна літера або лише голосні / лише приголосні»` → ТО `game_over`.
- Рахунок гравця = сума його ходів; показник — % від суми top (790 з 800 = 98,75 %) або «−10» від top.
- Перемога: найбільша сума очок · Поразка: менша · Нічия — однакова сума (?).
- Пари: КОЛИ `custom: «хід пари»` → ТО `custom: «двоє домовляються й подають один бюлетень»`.

## Керування і ввід
- Настільна: гравець пише на бюлетені слово, координати й рахунок; ранер збирає бюлетені для арбітра.
- Координати: літера першою — горизонтальне слово, цифра першою — вертикальне.
- Цифрова версія (DupliTop, Scrabble 2005 — до 16 гравців на одній дошці, Duplikat, Zwyx, Duplics): поставити плитки на дошку або ввести слово з позицією, таймер ходу, автопідрахунок (?).

## Вікна, меню, HUD
- `game-screen` (цифрова версія): майстер-дошка, спільна рука, `timer-countdown`, `slip-input` (слово + позиція + очки), свій рахунок і % від top.
- `solutions-window` (цифрова версія): після ходу — top, твій хід і різниця.
- `log-window` / `top-history`: протокол партії — номер ходу, тираж («+» відділяє reliquat від нових, «−» — rejet, «?» — джокер), слово, позиція, бали.
- `end-screen` / `leaderboard`: місце, сума, % від top (турнірна таблиця).
- `mode-select` (цифрова версія): класика 3 хв / semi-rapide / blitz / topping (?).

## Фічі поза полем
- `turn-timer` 1–3 хв; формати: клубна партія (PAP), TRAP, турнір homologué (~200 гравців, 3 партії на день), фестиваль (до 2000 гравців), simultané (тиражі заздалегідь розсилають центрам).
- `simultaneous-tournament`: одна партія для тисяч гравців у різних містах — можлива, бо тираж детермінований.
- `topping-mode` у DupliTop (?): мета — знайти саме top, а не просто хороший хід.
- Варіанти правил (`custom-rules`): «Partie Joker» (реальну літеру грають замість джокера, щоб його зберегти), «7 sur 8» (+50 за 7 літер), «7 et 8» (+75 за всі 8, +50 за 7).

## Варіації й родичі
- Scrabble (`scrabble.md`) — базове ядро; тут змінено лише, хто ходить і як рахується успіх.
- Duplicate bridge — звідси назва (усі грають ті самі роздачі).
- Daily-пазли зі спільним seed (`wordle.md`, `fibble.md`) — та сама ідея «однакові умови для всіх», але без спільної дошки.
- **Осі варіацій:** хто рухає дошку (top / власний хід) · час на хід (3 / 2 / 1 хв) · вимога до тиражу (2+2 / 1+1) · бонуси (бінго 50 / варіанти 7 sur 8, 7 et 8) · показник (сума / % від top / мінус від top).

## Цікавинки для курсу
- Тираж із перевіркою балансу голосних і приголосних і rejet — 🌱.
- Reliquat: після ходу лишаються невикористані літери, добір до 7 — 🌱.
- Генератор усіх легальних ходів і вибір top (anchor squares + cross-checks, trie / DAWG) — 🥇; тай-брейк «найбільше відкриває поле» — 🥈 (метрика відкритості).
- Рахунок у % від top і протокол партії в нотації (+ / − / ?) — 📎.
- Багато гравців одночасно на сервері: прийом бюлетенів до таймера, спільний top — 🥈.

## Мапа на каталог
- Є: `word-validation` ↔ ODS · `move-timer` ↔ 3 / 2 / 1 хв · `event-points` ↔ вартості літер · `leaderboard` ↔ турнірна таблиця · `profile-stats` ↔ % від top · `game-screen` · `end-screen`.
- Вже запропоновано в `scrabble.md`: `+premium-squares`, `+tile-rack`, `+tile-bag-draw`, `+line-placement`, `+cross-word-scoring`, `+bingo-bonus`, `+blank-tile`, `+move-generator`.
- **Нема** → пропозиції карток:
  - `+shared-rack` «Одна рука для всіх гравців» · game-logic/opponent · 🌱.
  - `+top-move-advance` «Позицію рухає найкращий хід, а не хід гравця» · game-logic/opponent · 🥇 (потрібен генератор ходів).
  - `+rack-balance-rule` «Тираж з мінімумом голосних / приголосних, інакше перетягнути» · entities/spawn · 🌱 · слоти {early: 2, late: 1, until_move: 15}.
  - `+percent-of-top` «Результат як відсоток від оптимуму» · game-logic/score · 🌱.

## Пропозиції до словників
- `+cond:rack_balance` — у тиражі достатньо голосних і приголосних.
- `+ui:slip-input` — бюлетень: слово, позиція, рахунок; `+ui:top-history` — протокол top-ходів.
- `+feature:topping-mode` — шукати саме оптимальний хід; `+feature:simultaneous-tournament` — один тираж для багатьох залів.
- `+card:shared-rack`, `+card:top-move-advance`, `+card:rack-balance-rule`, `+card:percent-of-top` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipédia: Scrabble duplicate](https://fr.wikipedia.org/wiki/Scrabble_duplicate) — правила тиражу, rejet, reliquat, бюлетені, top, тай-брейк, кінець гри, час, нотація, формати, програми, історія (Myriam Fabri, Hippolyte Wouters, Канни 1972, Льєж 1973).
- [Wikipedia: Duplicate Scrabble](https://en.wikipedia.org/wiki/Duplicate_Scrabble) — правила англійською, % і мінус від top, масштаб турнірів, пари.
- [Wikipedia: Scrabble variants](https://en.wikipedia.org/wiki/Scrabble_variants) — рекорд 1485 гравців.
- YouTube: пошук «scrabble duplicate partie».

## Непевне
- (?) Рік: ідея — кінець 1960-х (Myriam Fabri), просування — з 1972 (Wouters, Канни), EN-вікі каже «близько 1970»; у шапці 1972.
- (?) Бонус «solo» (тому, хто єдиний знайшов top) у турнірних правилах FFSc — не знайшов у відкритих джерелах.
- (?) Як цифрові версії приймають хід (дошка чи текст) і чи є в них режими blitz / topping як окремі пункти — лише назви програм із FR-вікі.
- (?) Розвʼязання нічиїх у турнірній таблиці.
- (?) Правило кінця гри розходиться: EN — «коли скінчились голосні або приголосні», FR — ще й «лишилась одна літера».
