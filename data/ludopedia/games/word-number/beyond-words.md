---
title: Beyond Words
slug: beyond-words
aka: []
family: word-number
also: [roguelike]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: partial
  random: both
  goal: score
year: 2026
platforms: [PC, PS5, Xbox Series X/S, Switch, Steam Deck]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3823370/Beyond_Words/", best: true, note: "опис, трейлер, безкоштовне демо; 300+ модифікаторів, 30+ босів, режими time attack / seeded / negative scoring"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Beyond_Words_(video_game)", note: "Scrabble + роглайк: рука з мішка, ліміт ходів на раунд, монети й карти між раундами; розробка, рецепція"}
  - {kind: official, url: "https://www.pqube.co.uk/games/beyond-words/", note: "видавець: типи плиток (Standard, Blue, Purple, Virus, Retrigger, Coins, Bomb, NoDiscard), боси, карти, перки"}
  - {kind: other, url: "https://www.thumbculture.co.uk/?p=87592", note: "огляд PS5: фігурні й розірвані дошки, 9 раундів, трофеї 3/6/9, бос «лише 2-літерні слова», бомба-стікер із запалом"}
  - {kind: other, url: "https://rogueliker.com/beyond-words-review/", note: "огляд: мапа кампанії з вузлами, таймові рівні, слова лишаються між раундами"}
  - {kind: other, url: "https://www.digitallydownloaded.net/2026/04/review-beyond-words-nintendo-switch-2.html", note: "огляд: ціль за N ходів, дошки з готовими плитками, місце закінчується"}
  - {kind: other, url: "https://steamcommunity.com/stats/3823370/achievements", note: "досягнення: продовжити слово, кілька слів за хід, вайлдкарди, бомби, рівно ціль"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Beyond+Words+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [word-validation, move-limit, run-relics, shop-between-levels, shop-catalog, round-currency, world-map, seed-share, explode-area, bomb-fuse, achievements-window, game-screen, end-screen, shop-window, codex-window, tutorial-window, +tile-bag-draw, +tile-rack, +tile-exchange, +line-placement, +cross-word-scoring, +premium-squares, +letter-value-scoring, +target-score-rounds, +multi-board, +shaped-board, +deck-builder, +special-letter-tiles, +wildcard-tile, +boss-fight, +shop-reroll, +base-times-mult, +board-carries-over, +virus-tile, +tile-retrigger, +word-length-levels, +round-trophies, +negative-score-mode, +mystery-pack, +timed-board-half-score]
proposes: ["+trigger:round_start", "+effect:draw", "+effect:discard", "+effect:spread", "+effect:retrigger", "+effect:reroll", "+ui:target-score", "+ui:bag-meter", "+ui:word-level", "+window:pack-opening", "+feature:mode-negative-score", "+axis:session=run"]
author: opus
date: 2026-11-19
---

# Beyond Words — Scrabble як роглайк-декбілдер: слова на фігурних дошках з бонус-клітинами, ціль раунду за ліміт ходів, карти й стікери між раундами

## Суть
Однокористувацький Scrabble з будовою Balatro: з руки, добраної з мішка, викладаєш слова на дошку, кожне слово дає «база × множник», і за обмежену кількість ходів треба набрати ціль раунду. Між раундами за монети купуєш карти сили (пасивні правила), бустери й перки, а плитки мішка дублюєш, знищуєш і обклеюєш стікерами. Незвичне для корпусу — самі дошки: невеликі, фігурні (транспорт, тварини, емодзі) або з кількох незвʼязаних підполів, з бонус-клітинами, підбирачками й блокерами; слова лишаються між раундами, тож місце — ресурс.

## Поле і час
- Квадратна сітка, менша за 15×15 Scrabble; форма — маска клітин: силуети, рамки зі стінами або кілька окремих підполів (в огляді — вісім малих); деякі дошки стартують з готовими плитками й спецклітинами.
- Клітини: бонусні (множники), підбирачки (монети, «+Mult», іконки зірок і блискавок), блокери; підполя різного кольору.
- Хід = викласти слово (−1 хід) або скинути плитки (−1 скидання). Раунд — до вичерпання ходів; рівень — 9 раундів зі зростанням цілі (≈500 → до 10 000 000); слова з минулих раундів лишаються на дошці.
- Час: покроковий; окремі «timed» дошки з таймером (кінець часу — половина очок замість нуля, патч #1).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка-літера (Standard) | tile | літера, очки (число в куті) | з руки на дошку; дає базові очки слова |
| Синя плитка (+Mult) | tile | +k | додає до множника слова |
| Фіолетова плитка (×Mult) | tile | ×k | множить множник слова |
| Вайлдкард | tile | будь-яка літера | заміняє потрібну літеру |
| Плитка зі стікером | tile | Points / Blue / Purple / Retrigger / Coin / No Discard | Points + до бази; Retrigger — спрацьовує ще раз; Coin — монети (з червня 2026 — 2); No Discard — не скидається |
| Бомба (стікер) | tile | запал N ходів | вибухає: прибирає свою плитку й сусідні — звільняє місце |
| Вірус (мутація) | tile | — | поширюється сусідніми плитками, дає швидкий бонус очок; заражені згодом гинуть |
| Бонусна клітина | terrain | + / × | слово, що лягає на неї, отримує бонус |
| Підбирачка | pickup | монета, +Mult, інші (?) | забирається словом, викладеним через клітину |
| Блокер | static | — | клітина, куди не можна класти |
| Стартові плитки | tile | — | уже на дошці; до них прикладають слова |
| Бос | boss | правило-модифікатор | раз на кілька раундів міняє правила; часом його треба знищити або обійти |
| Мішок плиток | supply | N/M плиток | джерело добору; поповнюється (досягнення «Refill Tile bag») |
| Стійка (рука) | supply | ~6–8 плиток (?) | звідси викладають слова; сортування A–Z, перемішування |
| Карта сили (Power) | pickup | пасивна до кінця рівня | змінює рахунок (×2 за слова парної довжини, випадковий множник на слово) |
| Бустер (Normal / Level / Tile) | pickup | одноразовий | миттєва вигода / база довжини слова +LV / апгрейд плитки |
| Перк | pickup | пасивний | бонуси рахунку, комбо або монет |
| Монети | resource | — | за слова й підбирачки; витрачаються в магазині |
| Ціль раунду | static | очки | набрав — раунд пройдено |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `custom: «початок раунду»` → ТО `custom: «добрати плитки з мішка до повної стійки»`.
- КОЛИ `input(place tiles)` → ЯКЩО `custom: «плитки в один ряд або стовпець і торкаються вже викладених»` і `in_dictionary(кожне утворене слово ≥ 2 літер)` → ТО `place(player, tiles)`, `score(Σ слів)`, `counter(moves, −1)`; інакше `block`.
- Рахунок слова: `custom: «база = очки літер + база довжини слова (LV)»` × множник; синя плитка → `counter(mult, +k)`; фіолетова → `multiplier(×k)`; Retrigger → `custom: «плитка спрацьовує ще раз»`.
- КОЛИ `enter(tile, bonus_cell)` → ТО `custom: «бонус клітини: множник / монети / +Mult»`; підбирачка → `pickup`, `currency(+n)`.
- КОЛИ `input(discard)` → ЯКЩО `counter(discards, >, 0)` і `not state(tile, no_discard)` → ТО `custom: «плитки йдуть з руки, добір нових»`, `counter(discards, −1)`.
- КОЛИ `counter(score, >=, goal)` → ТО `currency(+n)`, `window(shop-window)`, `custom: «наступний раунд з вищою ціллю»`.
- КОЛИ `counter(moves, ==, 0)` → ЯКЩО `counter(score, <, goal)` → ТО `lose` (рівень програно).
- КОЛИ `counter(round, ==, 3 | 6 | 9)` → ТО `give(player, трофей bronze | silver | gold)`.
- КОЛИ `counter(fuse, ==, 0)` (стікер Bomb) → ТО `explode(сусіди)`, `disappear` своєї й сусідніх плиток.
- КОЛИ `turn_end` → ЯКЩО `state(tile, virus)` → ТО `custom: «вірус переходить на сусідні плитки»`, `score(+n)`; заражені плитки згодом `disappear` (?).
- Бос-раунд: `custom: «правило-модифікатор»` — напр. «лише 2-літерні слова дають очки, 100 000 за 5 ходів», інверсія рахунку, ліміт довжини слова, перемішування дошки, обмеження доступних літер, штраф за повтор шаблону слова.
- КОЛИ `counter(time_left, ==, 0)` (timed-дошка) → ТО `custom: «раунд зараховується з половиною очок»`.
- Магазин: `choose(товари)`, `currency(−ціна)`; `custom: «перекинути вітрину»` (reroll); дублювати / знищити / посилити плитки мішка; mystery packs.
- Перемога: пройти 9 раундів рівня (gold), далі — вузли кампанії · Поразка: ходи вичерпано, ціль не набрано · Рахунок: Σ (база × множник) за слова; є режим негативного рахунку.

## Керування і ввід
- Перетягнути плитки зі стійки на клітини (ПК — миша (?), консолі — геймпад), підтвердити хід; кнопки: перемішати стійку, сортувати A–Z, скинути вибрані.
- Над словом — превʼю: довжина, рівень довжини (LV), «база × множник» і сума.
- Словник приймає власні назви й абревіатури (TIBET, LIBYAN, SATURN на знімках) і лайливі слова.

## Вікна, меню, HUD
- `game-screen`: ліва панель — Round x/9, Moves, Discards, Total Score, Goal, Coins, слова ходу (довжина, LV, база × множник), лічильник плиток мішка «N/M TILES»; верх — ряд карт сили й бустерів; низ — стійка з кнопками; на дошці — спливні «+4 Mult», «5 × 5» (`popup-text`).
- `shop-window` між раундами: випадкова вітрина, reroll, mystery packs.
- `map-window`: мапа кампанії з вузлами-рівнями (таймові позначені; вміст вузла видно лише всередині).
- `codex-window`: сторінка «Tiles & Features» з прикладами рахунку +MULT / ×MULT; «Game Info» з вкладкою Active Perks.
- `tutorial-window`: туторіал CATS; одноразові уроки при першому Bronze / Silver.
- `end-screen` з трофеєм рівня; `achievements-window` (51); `settings-window`.
- Переходи: мапа → рівень (раунд → магазин → раунд …) → трофей → мапа.

## Фічі поза полем
- `mode-time-attack` (таймові дошки), `seed-input` (seeded runs), режим негативного рахунку; трофеї Bronze / Silver / Gold за раунди 3 / 6 / 9, далі `rank-tiers` Platinum і Platinum+ (червень 2026).
- `unlockables`: Mystery Packs і тайл-паки (MATERIALS, COLOURS Bumper) відкриваються умовами; 300+ модифікаторів, 30+ босів.
- `achievements` (51), `cloud-save`, Steam Deck Verified; словник +1000 слів у червневому оновленні; лише англійська.

## Варіації й родичі
- Корпус: Scrabble (`scrabble.md` — правила викладання й рахунок літер), Wordatro (`wordatro.md` — Balatro зі словами без дошки), Watchword (`watchword.md` — роглайк з дошкою, що росте), Bookworm Adventures (`bookworm-adventures.md` — слово як атака), WordTactics (`wordtactics.md`), Overwords (`overwords.md`), Upwords (`upwords.md`).
- Поза сімʼєю: Balatro (карти-«джокери», база × множник), Luck be a Landlord (`build-sim/luck-be-a-landlord.md`).
- **Осі варіацій:** поле (рука без дошки / квадратна дошка Scrabble / фігурні й розірвані дошки / дошка, що росте) · що з полем між раундами (чиститься / слова лишаються) · де модифікатори (на плитках-стікерах / на клітинах / на картах) · бос (сильніший суперник / правило-модифікатор).

## Цікавинки для курсу
- Валідація ходу Scrabble: одна лінія, дотик до наявних, усі утворені перехресні слова в словнику — 🥈.
- Рахунок «база × множник» з конвеєром модифікаторів (+Mult, ×Mult, retrigger; порядок важить — досягнення «рівно 5! = 120») — 📎.
- Дошка як маска клітин: силуети й кілька незвʼязаних підполів — 📎.
- Слова лишаються між раундами — простір як ресурс; бомба-стікер із запалом звільняє місце — 📎.
- Вірус, що поширюється сусідами й згодом знищує плитки — 📎.
- Бос як декоратор правил раунду (інверсія, ліміт довжини, перемішування) — 🥉.
- Мапа кампанії з вузлами й окремою економікою всередині рівня — 🥉.

## Мапа на каталог
- Є: `word-validation` · `move-limit` ↔ Moves на раунд · `run-relics` ↔ карти сили й перки · `shop-between-levels` + `shop-catalog` + `round-currency` ↔ магазин і монети · `world-map` ↔ мапа кампанії · `seed-share` ↔ seeded runs · `explode-area` + `bomb-fuse` ↔ стікер Bomb · `achievements-window` · `game-screen` · `end-screen` · `shop-window` · `codex-window` · `tutorial-window`.
- **Нема** → пропозиції карток:
  - Уже в корпусі: `+tile-bag-draw`, `+tile-rack`, `+tile-exchange` (скидання), `+line-placement`, `+cross-word-scoring` («Play 5 words at once»), `+premium-squares`, `+letter-value-scoring`, `+target-score-rounds`, `+multi-board`, `+shaped-board`, `+deck-builder`, `+special-letter-tiles` (стікери), `+wildcard-tile`, `+boss-fight`, `+shop-reroll`.
  - `+base-times-mult` «Рахунок = база × множник з плиток і карт» · game-logic/score · 📎 · слоти {add_mult, x_mult, retrigger}.
  - `+board-carries-over` «Слова лишаються на полі між раундами» · game-logic/economy · 🌱.
  - `+virus-tile` «Мутація, що поширюється сусідніми плитками» · entities/state · 📎.
  - `+tile-retrigger` «Плитка спрацьовує ще раз» · game-logic/score · 🌱.
  - `+word-length-levels` «Рівень бази для кожної довжини слова» · game-logic/score · 🌱 (як «руки» Balatro).
  - `+round-trophies` «Трофеї за пройдені раунди 3 / 6 / 9» · levels/progression · 🌱.
  - `+negative-score-mode` «Режим, де ціль — мінусовий рахунок» · game-logic/score · 📎.
  - `+mystery-pack` «Пак із випадковим вмістом у магазині» · game-logic/economy · 🌱.
  - `+timed-board-half-score` «Таймова дошка: кінець часу — половина очок» · game-logic/score · 🌱.

## Пропозиції до словників
- `+trigger:round_start` — початок раунду (добір до повної руки).
- `+effect:draw` — добрати плитки з мішка.
- `+effect:discard` — скинути плитки з руки (витрачає скидання).
- `+effect:spread` — мутація переходить на сусідні плитки (вірус).
- `+effect:retrigger` — сутність спрацьовує ще раз у тому ж підрахунку.
- `+effect:reroll` — замінити вітрину магазину новою випадковою.
- `+ui:target-score` — ціль раунду поруч із сумою.
- `+ui:bag-meter` — скільки плиток лишилось у мішку («N/M TILES»).
- `+ui:word-level` — довжина слова з рівнем LV і «база × множник».
- `+window:pack-opening` — відкриття mystery pack.
- `+feature:mode-negative-score` — режим негативного рахунку.
- `+axis:session=run` — рівень = забіг із власною економікою.

## Джерела
- ⭐ [Steam: Beyond Words](https://store.steampowered.com/app/3823370/Beyond_Words/) — опис, демо, теги; новини Steam: «Dr Doak's Written Prescription» (плитки Blue / Purple, вірус, стікери, бустери Normal / Level / Tile, перки, боси), патчі (таймові дошки — половина очок, Platinum+, Mystery Packs, +1000 слів); знімки — інтерфейс раунду, LV слова, «5 × 5», підполя.
- [Wikipedia](https://en.wikipedia.org/wiki/Beyond_Words_(video_game)) — Scrabble + роглайк, рука з мішка, ліміт ходів, монети й карти; MindFuel (Steve Ellis, David Doak), реліз 9.04.2026.
- [PQube](https://www.pqube.co.uk/games/beyond-words/) — 11 типів плиток, боси, карти, перки, платформи.
- [Thumb Culture](https://www.thumbculture.co.uk/?p=87592) — фігурні й розірвані дошки, 9 раундів, трофеї, перехресні слова від 2 літер, бос «лише 2-літерні слова», бомба із запалом, приклад 100 × 50.
- [Rogueliker](https://rogueliker.com/beyond-words-review/) — мапа кампанії, таймові рівні, ранні слова «повертаються» в наступних раундах.
- [Digitally Downloaded](https://www.digitallydownloaded.net/2026/04/review-beyond-words-nintendo-switch-2.html) — ціль за N ходів, готові плитки на дошках, місце закінчується.
- [The Geekly Grind](https://www.thegeeklygrind.com/all-posts/beyond-words-review) — магазин (дублювати, посилити, знищити плитки), боси.
- [Steam: досягнення](https://steamcommunity.com/stats/3823370/achievements) — 51 досягнення (видно 26).
- YouTube: пошук «Beyond Words gameplay».

## Непевне
- (?) Розмір руки (стійки) і кількість ходів / скидань на раунд — на знімках 0–4 ходи й 2–3 скидання, правила не знайдено.
- (?) Як бос існує «на полі»: PQube каже «знищити, щоб відкрити дошку, або обійти» — механіку не бачив.
- (?) Значення іконок на клітинах (зірки, блискавки, циліндри) — лише зі знімків.
- (?) Чи заражені вірусом плитки гинуть за таймером чи після N поширень.
- (?) Кількість рівнів у кампанії й чи є загальний забіг поверх рівнів.
- (?) Ввід на ПК (drag чи клік) не перевірено.
