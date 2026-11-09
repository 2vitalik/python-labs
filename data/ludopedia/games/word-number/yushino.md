---
title: Yushino
slug: yushino
aka: [Yushino!]
family: word-number
also: []
klass: cursor
axes:
  field: square
  time: turn
  opponent: online
  info: partial
  random: runtime
  goal: score
year: 2012
platforms: [iOS, Android, web, Facebook]
links:
  - {kind: official, url: "https://yushino.com/official_yushino_rules.html", best: true, note: "офіційні правила: два правила послідовності, 96 плиток, премії 2*/3*/2X/3X, бонус 100, обмін, кінець гри, тай-брейк"}
  - {kind: official, url: "https://yushino.com/FAQ.html", note: "FAQ: послідовність валідна лише після дописування, бульбашка очок, струшування руки, Coach, чат, онлайн-партії, нагадування, авто-резиґнація"}
  - {kind: official, url: "https://yushino.com/", note: "«Words with Friends of Numbers», © Yushino LLC 2012–2013, App Store / Facebook / браузер / Android"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Scrabble_variants", note: "Yushino серед числових варіантів Scrabble"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=yushino+numbers+game", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [async-multiplayer, online-multiplayer, hot-seat, pass-device, turn-enforcement, event-points, leftover-penalty, pass-turn, rating-system, leaderboard, popup-text, game-screen, end-screen, help-window, settings-window, +tile-rack, +tile-bag-draw, +premium-squares, +bingo-bonus, +tile-exchange, +wild-number, +line-placement, +cross-word-scoring, +recurrence-sequence, +exchange-cooldown, +async-match-list, +word-strength, +turn-reminder, +auto-resign, +in-game-chat, +rank-badges]
proposes: ["+cond:sequence_rule", "+feature:exchange-cooldown", "+feature:turn-reminder", "+feature:auto-resign", "+feature:word-strength", "+ui:score-preview", "+window:game-list", "+card:recurrence-sequence"]
author: opus
date: 2026-11-09
---

# Yushino — «Words with Friends з числами»: кожна цифра ряду — остання цифра суми двох попередніх

## Суть
Асинхронний онлайн-двобій у стилі Scrabble, де замість слів — **числові послідовності** по горизонталі чи вертикалі. Ряд з 3+ цифр валідний, якщо кожна цифра = (сума двох попередніх) mod 10, тобто це Фібоначчі за модулем 10 (875, 7291); ряд з двох цифр — якщо вони відрізняються на 1 за модулем 10 (56, 87, 90, 09). Очки — номінали цифр нових і змінених послідовностей з множниками клітин; за всі 7 плиток руки — +100. «Словник» замінено арифметичним правилом, тому перевірка ходу — формула, а не база слів.

## Поле і час
- Квадратне поле з центральною клітиною і премійними клітинами 2* / 3* (цифра) та 2X / 3X (послідовність); розмір у правилах не вказано.
- Читання лише ліворуч → праворуч і згори → вниз (FAQ).
- Покроково, двоє гравців; партія живе днями (асинхронно), хід = одна лінія плиток, обмін або пас.
- Інформація часткова: рука суперника й мішок приховані; видно «Numbers left».

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Цифра 0–9 | tile | номінал = очки; 0×10, 1×14, 2×14, 3×14, 4×8, 5×8, 6×8, 7×6, 8×6, 9×6 | на полі незмінна; входить у горизонтальну й вертикальну послідовність |
| Бланк | tile | 2 шт., 0 очок | стає будь-якою цифрою |
| Рука | container | 7 плиток | поповнюється з мішка; струсити пристрій — перемішати, тап — відсортувати |
| Мішок | container | 96 плиток | тягнення наосліп; лічильник «Numbers left» |
| Клітина 2* / 3* | zone | ×2 / ×3 цифри | діє лише на щойно викладену цифру |
| Клітина 2X / 3X | zone | ×2 / ×3 послідовності | множить суму нової/зміненої послідовності; дві — множать двічі |
| Центр | zone | — | перша послідовність мусить його торкатися |
| Гравець | player | рахунок, рейтинг, бейджі | хід по черзі; Player 2 робить перший хід |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(play)` → ЯКЩО `first_time` → ТО одна з плиток послідовності мусить торкатися центру.
- КОЛИ `input(play)` → ЯКЩО `legal(move)` → ТО `place(player, tiles)`, `score(...)`, `give(player, tiles until 7)`, `end_turn`; інакше `block`.
- `legal(move)`: усі плитки ходу в одній лінії (рядок або стовпець); нова послідовність має спільну плитку з наявною; жодна утворена з сусідами послідовність не невалідна.
- КОЛИ `after(place)` → ЯКЩО `custom: «ряд ≥ 3 цифр і кожна = (сума двох попередніх) mod 10»` → ТО послідовність валідна (875: 8+7=15 → 5; 7291: 7+2=9, 2+9=11 → 1).
- КОЛИ `after(place)` → ЯКЩО `custom: «ряд з 2 цифр, що відрізняються на 1 за mod 10»` → ТО послідовність валідна (56, 87, 90, 09, 98).
- Послідовність може бути невалідною, доки її не дописали: [5 2] — ні, [5 2 7] — так (FAQ); у межах ходу перевіряється підсумок.
- КОЛИ `after(place)` → ЯКЩО `custom: «утворено або продовжено кілька послідовностей»` → ТО кожна рахується окремо, суми додаються.
- КОЛИ `after(place)` → ТО `score(Σ номіналів усіх цифр нової/зміненої послідовності, включно зі старими)`, нова цифра на 2*/3* ×2/×3; потім `multiplier(×2 | ×3 за кожну 2X/3X під новими плитками)`; старі премії не діють.
- КОЛИ `counter(tiles_played, ==, 7)` → ТО `score(+100)`.
- КОЛИ `input(place blank)` → ТО `choose(digit)`, `set_value(blank, d)`; очок 0.
- КОЛИ `input(exchange k)` → ЯКЩО `custom: «минулого ходу не міняв»` і `count(bag, >, 7)` → ТО `take(player, k)`, `give(player, k)`, `end_turn`; інакше `block`.
- КОЛИ `input(pass)` → ТО `pass_turn`.
- КОЛИ `custom: «гравець виклав останню плитку, мішок порожній»` або `custom: «3 паси поспіль»` → ТО `game_over`.
- КОЛИ `game_over` → ЯКЩО `custom: «хтось вийшов першим»` → ТО `score(+Σ руки суперника)` йому, `score(−Σ своєї руки)` суперникові.
- КОЛИ `game_over` → ЯКЩО `custom: «нічия після перерахунку»` → ТО перемагає той, хто мав більше до перерахунку; ЯКЩО знову нічия → ТО `lose` гравцю, що зробив перший хід (Player 2).
- КОЛИ `input(resign)` → ЯКЩО `turn_of(player)` → ТО `lose`.
- КОЛИ `idle(long)` → ТО `custom: «суперника автоматично резиґнують через деякий час»` (?) — тривалість не вказана.
- Перемога: більше очок після перерахунку · Поразка: менше / резиґнація / неактивність · Рахунок: Σ номіналів послідовностей з 2*/3* і 2X/3X, +100 за всю руку.

## Керування і ввід
- Тач: перетягнути цифри з руки на поле; над останньою цифрою зʼявляється бульбашка з очками, лише якщо хід валідний.
- Струсити пристрій — перемішати руку; тап — відсортувати.
- Кнопки: Play, Exchange, Pass, Resign (лише у свій хід).
- Бланк: вибір цифри при викладанні.
- Соціальне: чат із суперником під час очікування, нагадування повільному супернику.

## Вікна, меню, HUD
- `game-list` (головний екран): поточні партії, спершу ті, де твій хід; кнопка нової гри.
- `lobby-window`: суперник — друг з Facebook, випадковий, запрошення email чи іменем Yushino; або «передай пристрій» (`pass-device`).
- `game-screen`: поле з 2*/3*/2X/3X, `pocket` (рука 7), рахунки, `remaining-counter` («Numbers left»), `score-preview` (бульбашка), кнопки ходу, Coach.
- `help-window`: правила й FAQ.
- `confirm-dialog`: резиґнація, обмін.
- `leaderboard` (Ratings): ранг, гравець, рахунок, бейджі (Ninja, Samurai, Daimyo, Shogun, Dachi, Uchi, Uke, Zuki, Geri).
- Турніри: реєстрація на сайті.
- `settings-window`: імʼя, пароль, email, телефон, вихід.
- `end-screen`: фінальні рахунки з перерахунком рук.
- Переходи: `game-list` → `game-screen` партії; нова гра → `lobby-window` → `game-screen`; кінець → `end-screen` → `game-list`.

## Фічі поза полем
- `async-multiplayer`: push-сповіщення «твій хід», кілька партій паралельно, нагадування (`turn-reminder`), авто-резиґнація неактивних.
- `hotseat` через «передай пристрій».
- `word-strength` — Coach оцінює, наскільки добрий твій хід.
- `chat` у партії.
- `leaderboard-online` + `rank-tiers` (бейджі), турніри.
- Платформи: App Store, Android (apk), Facebook, браузер.

## Варіації й родичі
- `scrabble.md` — та сама схема (рука 7, мішок, 2*/3*/2X/3X, бонус за всю руку, перерахунок рук); Words With Friends — асинхронний прототип.
- `triolet.md` — групи з сумою 15; `equate.md`, `mathable.md` — рівності; `nerdle.md` — вгадати рівність.
- Послідовність Фібоначчі mod 10 (період Пізано 60) як «словник» — рідкісне правило в корпусі.
- **Осі варіацій:** правило «слова» (словник / сума / рівність / рекурентність) · модуль (10 / інший) · правило для коротких рядів (±1 / заборона) · напрямок читання (лише вперед / обидва) · обмін (вільний / з кулдауном).

## Цікавинки для курсу
- Валідатор послідовності: `all(s[i] == (s[i-1] + s[i-2]) % 10)` + правило пари ±1 mod 10 — 🌱.
- Перевірка ходу: знайти всі максимальні ряди, що зачепили нові плитки, у двох напрямках; кожен — валідний — 📎.
- Рахунок нових і змінених послідовностей з преміями за цифру й за ряд — 📎.
- Генератор ходів: для заданого початку a, b рух однозначний (третя цифра визначена), тож перебір — по якорях і довжинах, а не по перестановках руки — 🥉.
- Coach: оцінка ходу відносно найкращого можливого — 🥇 (той самий генератор + рахунок).
- Асинхронні партії зі списком «твій хід», нагадуваннями й тайм-аутом — 🥈.

## Мапа на каталог
- Є: `async-multiplayer` ↔ партії днями · `online-multiplayer` ↔ сервер · `hot-seat` + `pass-device` ↔ один пристрій · `turn-enforcement` · `event-points` ↔ номінали · `leftover-penalty` ↔ перерахунок рук · `pass-turn` · `rating-system` + `leaderboard` ↔ Ratings · `popup-text` ↔ бульбашка очок · `game-screen` / `end-screen` / `help-window` / `settings-window`.
- **Нема** → пропозиції карток:
  - `+tile-rack`, `+tile-bag-draw`, `+premium-squares`, `+bingo-bonus`, `+tile-exchange`, `+line-placement`, `+cross-word-scoring` — див. `scrabble.md`; `+wild-number` — бланк-цифра; `+async-match-list` — див. інші асинхронні ігри сімʼї; `+word-strength` — див. `scrabble.md`.
  - `+recurrence-sequence` «Ряд за рекурентним правилом (Фібоначчі mod 10)» · entities/legality · 🌱 · слоти {rule: fib, mod: 10, pair_rule: step1}.
  - `+exchange-cooldown` «Обмін не два ходи поспіль і не при малому мішку» · game-logic/opponent · 🌱.
  - `+turn-reminder` «Нагадати супернику про хід» · game-logic/opponent · 🌱.
  - `+auto-resign` «Авто-поразка за неактивність» · game-logic/opponent · 📎.
  - `+in-game-chat` «Чат у партії» · game-logic/opponent · 📎.
  - `+rank-badges` «Бейджі рангу в таблиці» · interface/results · 🌱.

## Пропозиції до словників
- `+cond:sequence_rule` — лінія чисел задовольняє правило (кожне = (a+b) mod 10; пара — ±1 mod 10).
- `+feature:exchange-cooldown`, `+feature:turn-reminder`, `+feature:auto-resign` — див. «Мапа на каталог».
- `+feature:word-strength` — оцінка ходу (Coach; у WWF — Word Strength).
- `+ui:score-preview` — бульбашка очок над останньою плиткою, лише для валідного ходу.
- `+window:game-list` — список паралельних асинхронних партій.
- `+card:recurrence-sequence` — див. «Мапа на каталог».

## Джерела
- ⭐ [Yushino: Official rules](https://yushino.com/official_yushino_rules.html) — мета, два правила послідовності з прикладами, розподіл 96 плиток, центр, «одна лінія», премії 2*/3*/2X/3X, бонус 100, обмін, кінець гри, тай-брейк.
- [Yushino: FAQ](https://yushino.com/FAQ.html) — напрям читання, валідність після дописування, бульбашка очок, «Numbers left», струшування/сортування руки, обмін, резиґнація й авто-резиґнація, способи почати гру, сповіщення, нагадування, Coach, чат, налаштування.
- [Yushino.com](https://yushino.com/) — «Words with Friends of Numbers», © 2012–2013, платформи; сторінки about/press/ratings: команда 2011–2012, ідея — Yiannis Tsiounis, бейджі рангів.
- [Wikipedia: Scrabble variants](https://en.wikipedia.org/wiki/Scrabble_variants) — Yushino в ряду числових варіантів.
- YouTube: пошук «yushino numbers game».

## Непевне
- (?) Розмір поля й розклад премійних клітин — у правилах і FAQ не вказано (ймовірно 15×15 як у WWF).
- (?) Чи можна читати послідовність справа наліво чи знизу вгору — FAQ каже лише «left-to-right or top-to-bottom».
- (?) Обмін: правила — «не можна, коли в мішку лише 7», FAQ — «коли менше 7»; межа на 7 — неточна.
- (?) Кінець за пасами: правила — «3 паси поспіль», FAQ — «будь-хто пасує 3 рази поспіль».
- (?) Через скільки часу неактивного суперника резиґнують; як рахується рейтинг і видаються бейджі.
- (?) Чи сервіс досі працює: застосунки 2012–2013, сайт відповідає, але завантаження не перевіряв.
