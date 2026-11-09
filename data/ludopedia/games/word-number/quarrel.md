---
title: Quarrel
slug: quarrel
aka: [Quarrel Deluxe]
family: word-number
also: []
klass: hybrid
axes:
  field: graph
  time: turn
  opponent: ai
  info: full
  random: both
  goal: territory
year: 2011
platforms: [iOS, Xbox 360]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Quarrel_(video_game)", best: true, note: "ідея «Scrabble × Risk × Countdown», атака сусідньої території словом, 9 AI-суперників, таблиця вартості літер 1–15, BAFTA Scotland 2011"}
  - {kind: other, url: "https://gameinformer.com/games/quarrel/b/xbox360/archive/2012/02/02/quarrel-review-turning-words-into-war", note: "Game Informer: 12 мап, 8 літер, війська = макс. довжина слова, нічия — швидший, режими Quick / Domination / Showdown / Challenge / online"}
  - {kind: other, url: "https://ztgd.com/?p=18817", note: "ZTGD: переможець переводить усіх, крім одного, полонені за перемогу андердога, +1 солдат на територію, скарб і бонусне розгортання, слово глядача, режими"}
  - {kind: other, url: "https://toucharcade.com/?p=74815", note: "TouchArcade (Deluxe): фаза атаки, однакові 8 плиток, одна плитка на солдата, нічия — хто раніше, підкріплення за кількістю територій, AI іноді помиляється"}
  - {kind: other, url: "https://www.pocketgamer.com/quarrel-deluxe/review/", note: "Pocket Gamer: старт 4–7 солдатів, захист зводить атакувальника до 1, анаграма глядача, шкала бонусного солдата, профілі AI"}
  - {kind: other, url: "https://geeknative.com/25683/a-war-of-words-quarrel-review", note: "2–4 гравці, до 8 армій на сторону, полонені"}
  - {kind: other, url: "https://denki.co.uk/2011/08/31/introducing-quarrel-faq-part-1/", note: "Denki: зміст FAQ (backup troops, prisoners, reinforcements, treasure, trailblazing, transferring, bonus time, timed quarrels); сам FAQ 404"}
  - {kind: official, url: "https://denki.co.uk/games/archive/quarrel/", note: "сторінка гри в архіві Denki: словник HarperCollins, платформи"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=quarrel+denki+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [ai-opponent, turn-enforcement, word-validation, event-points, move-timer, online-multiplayer, mode-select, match-setup, sequential-levels, leaderboard, achievements-window, tutorial-window, game-screen, end-screen, map-window, +territory-capture, +word-duel, +troops-cap-word-length, +shared-letter-rack, +letter-value-scoring, +speed-tiebreak, +territory-reinforcements, +troop-transfer, +prisoners-capture, +treasure-meter, +spectator-word, +anagram-bonus, +ai-personalities, +medal-rank, +ai-takeover-on-quit]
proposes: ["+trigger:word_submitted", "+cond:word_length_max", "+cond:word_score_higher", "+effect:move_troops", "+effect:reinforce", "+ui:troop-count", "+ui:treasure-meter", "+ui:word-slots", "+window:duel-screen", "+feature:ai-profiles", "+axis:turn-structure=phased"]
author: opus
date: 2026-11-09
---

# Quarrel — Risk на маленькому острові, де кожен бій — двобій на найдорожче слово з тих самих восьми літер

## Суть
Два–чотири генерали ділять острів на території з військами; мета — забрати всі. Атака на сусідню територію запускає «сварку»: обидві сторони отримують ті самі 8 літер зі Scrabble-подібною вартістю, і кожен складає слово не довше, ніж у нього солдатів у бою. Дорожче слово перемагає; при рівності — той, хто подав швидше. Тож гра на мапі визначає «ліміт довжини», а словесний двобій — результат бою: велика армія дає право на довше, а отже дорожче слово.

## Поле і час
- Мапа — острів, поділений на території з сусідством (`field: graph`); мапи менші й простіші за Risk, з вузькими місцями, які легко тримати. Усього 12 мап-островів.
- На старті території розподілено порівну між гравцями, хто ходить першим — випадково.
- Хід = фаза атак (скільки завгодно атак (?)), потім перекидання військ і кінець ходу з підкріпленням.
- Сварка — окреме «поле»: ряд із 8 плиток-літер і слоти під слово; у частині режимів — таймер, у частині — час необмежений.
- Мінімальна інформація прихована: мапа й літери видно всім; випадковість — у розподілі територій і в наборі літер.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Територія | zone | власник, війська 1…8, сусіди | атакує сусідню ворожу; приймає підкріплення |
| Солдат | piece | фракція (ніндзя, роботи, шотландці…) | 1 солдат = 1 дозволена літера в сварці |
| Набір літер | supply | 8 плиток, однаковий для обох | анаграма 8-літерного слова (?) |
| Плитка-літера | tile | буква, вартість 1–15 | кожна плитка — не більше разу в слові |
| Слово | mark | ≤ кількість солдатів у бою | сума вартостей = сила удару |
| Скарб | resource | шкала | росте від слів і захоплень; повна шкала дає бонусного солдата |
| Бонусний солдат (backup troop) | pickup | — | можна ввести на старті сварки (+1 до ліміту довжини (?)) |
| Полонені | resource | кількість | забираються в переможеного при перемозі меншою армією; поповнюють твої війська |
| AI-генерал | enemy | імʼя, Word IQ, стиль | 9 характерів від Dwayne (найлегший) до Kali (найсильніший) |

Вартість літер (Wikipedia; за частотою в усному мовленні): A, E, I, N, O, S, T = 1 · C, L, R = 2 · D, P, U = 3 · G, H, M = 4 · B, F, W, Y = 5 · K, V = 6 · X = 10 · Z = 12 · J, Q = 15.

## Правила (КОЛИ → ЯКЩО → ТО)
Атака:
- КОЛИ `input(своя територія → сусідня ворожа)` → ЯКЩО `turn_of(player)` and `custom: «території сусідні»` → ТО `custom: «почати сварку»`, `spawn(8 плиток)` однакових для обох, `timer(start)` у таймерних режимах.
- КОЛИ `input(подати слово)` → ЯКЩО `in_dictionary(word)` (Collins) and `custom: «довжина ≤ солдатів сторони в бою»` and `custom: «лише видані плитки, кожна раз»` → ТО `score(Σ вартостей)`.
- КОЛИ `custom: «обидва подали слова або вийшов час»` → ЯКЩО `custom: «очки атакувальника > очок захисника»` → ТО `set_side(територія, атакувальник)`, `custom: «перевести всіх солдатів, крім одного, на здобуту територію»`.
- КОЛИ `custom: «сварка завершена»` → ЯКЩО `custom: «захисник має не менше очок»` → ТО `custom: «військо атакувальника зводиться до 1 солдата»`.
- КОЛИ `custom: «рівні очки»` → ТО `custom: «перемагає той, хто подав слово раніше»` (нічиїх нема).
- КОЛИ `custom: «переміг той, у кого менше солдатів»` → ТО `custom: «бере полонених — солдати суперника переходять до нього»` (кількість (?)).
- Більша армія може перебити дорожче коротке слово довшою формою того самого (AI так робить: +S тощо).

Інші гравці й скарб:
- КОЛИ `custom: «сваряться двоє інших (3–4 гравці)»` → ТО `custom: «глядач може скласти слово з тих самих 8 літер без ліміту довжини»` → `counter(treasure, +мало)`; ЯКЩО `custom: «використано всі 8 літер»` → ТО `custom: «бонус за анаграму»`.
- КОЛИ `custom: «склав слово або захопив територію»` → ТО `counter(treasure, +n)`; серії захоплень дають більше.
- КОЛИ `counter(treasure, =, повна)` → ТО `give(player, бонусний солдат)`; КОЛИ `input(розгорнути)` на старті сварки → ТО `custom: «+1 солдат у бою»`.

Кінець ходу:
- КОЛИ `input(перекинути війська)` → ЯКЩО `custom: «на сусідню свою територію»` → ТО `custom: «перемістити солдатів на одну територію»`.
- КОЛИ `turn_end(player)` → ТО `custom: «підкріплення: +1 солдат кожній твоїй території»` (ZTGD; TouchArcade — «за кількістю територій»).
- КОЛИ `custom: «солдатів на території = 8»` → ТО `custom: «більше не додається»` (до 8 армій на сторону в бою) (?).

Кінець партії:
- КОЛИ `count(території гравця, =, усі)` → ТО `win`, `window(end-screen)` з медаллю bronze/silver/gold.
- КОЛИ `count(території гравця, =, 0)` → ТО `lose` (вибуває).
- КОЛИ `custom: «онлайн-гравець вийшов»` → ТО `custom: «його місце займає AI без зупинки партії»`.
- Перемога: усі території твої · Поразка: втрачено всі · Рахунок: медаль, Word IQ (швидкість і використання плиток), бонус андердога за перемогу проти переваги.

## Керування і ввід
- Мапа: вибрати свою територію, потім ворожу сусідню (атака) або свою сусідню (перекидання); кнопка завершення ходу.
- Сварка: тапом/курсором набрати слово з 8 плиток (на Xbox — стік і кнопка A), подати; швидкість важить при рівності.
- 3–4 гравці: поки сваряться інші — можна скласти власне слово для скарбу.

## Вікна, меню, HUD
- `main-menu` → `mode-select`: Quick Match · Domination · Showdown · Challenge · Online (Xbox) / Daily Challenge (Deluxe).
- `match-setup`: суперники (до трьох AI), таймер вкл/викл.
- `game-screen` / `map-window`: острів, `troop-count` на кожній території, власник кольором, `treasure-meter`, `turn-indicator`.
- `duel-screen` (custom-window): 8 плиток з вартостями, `word-slots` за кількістю солдатів, портрети генералів, `timer-countdown` у таймерних режимах, показ обох слів і рахунку.
- `end-screen`: перемога / поразка, медаль.
- `leaderboard`: Domination, Word IQ.
- `achievements-window` (Xbox), `tutorial-window`, `codex-window`-подібні профілі AI (And! → Profiles: стиль і Word IQ).
- `lobby-window` (Xbox online) (?).

## Фічі поза полем
- Режими: `mode-classic` (Quick Match з AI різної сили), Domination — 12 островів підряд зі зростанням складності (`levels-sequential`), Showdown — серія з 9 дуелей один на один, Challenge — N територій поспіль або серія сутичок «8 на 8», Daily Challenge (Deluxe), `online-multiplayer` до 4 (Xbox; локального нема).
- `ai-opponent-levels`: 9 AI з характерами (сильний словник / слабка тактика, швидкий / короткі слова; Kali часто кладе 7–8 літер), AI іноді свідомо помиляється.
- `stats`: Word IQ; медалі за партію; `leaderboard-online`; `achievements`.
- Таймер сварок вимикається в Deluxe у Daily Challenge / Domination (FAQ) (?).
- `tutorial`.

## Варіації й родичі
- Quarrel (XBLA, 2012) → Quarrel Deluxe (iOS, 2012, соло, мультиплеєр обіцяли пізніше).
- Risk — карта, сусідство, підкріплення; Countdown (`countdown-numbers.md` — числова гілка того ж шоу) — найдовше слово з виданих літер.
- Wordbase (`wordbase.md`), Letterpress (`letterpress.md`) — територія через слова, але на сітці літер.
- Bookworm Adventures (`bookworm-adventures.md`), Word RPG battlers (`word-rpg-battlers.md`) — слово як удар.
- **Осі варіацій:** звʼязок мапи й слова (війська = ліміт довжини / без ліміту) · набір літер (спільний / окремий) · нічия (швидкість / мовний тайбрейк) · підкріплення (за територію / за очки).

## Цікавинки для курсу
- Граф територій: сусідство, перевірка «атакувати можна лише сусіда», перемога = всі вершини — 🌱.
- Сварка: найдорожче слово ≤ k літер з 8 плиток по словнику (перебір підмножин або індекс анаграм) — 🥉.
- AI-генерали з профілями: обмеження словника, затримка відповіді, свідомі помилки, тактика вибору цілі — 🥈.
- Наслідки бою: перевести n−1, звести до 1, полонені для андердога — 📎.
- Шкала скарбу і бонусний солдат, слово глядача з анаграмним бонусом — 📎.
- Тайбрейк за часом подачі (мітка часу, сервер в онлайні) — 🥉.

## Мапа на каталог
- Є: `ai-opponent` ↔ 9 генералів; `turn-enforcement` ↔ черга ходів; `word-validation` ↔ словник Collins; `event-points` ↔ таблиця вартостей літер; `move-timer` ↔ таймерні сварки; `online-multiplayer`; `mode-select` + `match-setup`; `sequential-levels` ↔ Domination; `leaderboard`, `achievements-window`, `tutorial-window`, `game-screen`, `end-screen`, `map-window`.
- **Нема** → пропозиції карток:
  - `+word-duel` «Двобій словами на однакових літерах» · game-logic/opponent · 🥉.
  - `+troops-cap-word-length` «Розмір армії = макс. довжина слова» · game-logic/constraints · 🌱.
  - `+shared-letter-rack` «Обом гравцям ті самі плитки» · entities/state · 🌱.
  - `+speed-tiebreak` «Нічию вирішує швидкість подачі» · game-logic/opponent · 📎.
  - `+territory-reinforcements` «Підкріплення за території в кінці ходу» · game-logic/economy · 📎.
  - `+troop-transfer` «Перекинути війська на сусідню свою територію» · entities/move · 🌱.
  - `+prisoners-capture` «Переможець-андердог забирає солдатів» · game-logic/economy · 📎.
  - `+treasure-meter` «Шкала дій → бонусний юніт» · game-logic/economy · 📎.
  - `+spectator-word` «Глядач грає на чужих літерах за бонус» · game-logic/opponent · 🥉.
  - `+anagram-bonus` «Бонус за використання всіх літер» · game-logic/score · 🌱.
  - `+ai-personalities` «AI з характерами й профілями» · game-logic/opponent · 🥈.
  - `+medal-rank` «Медаль за партію» · interface/results · 🌱.
  - `+ai-takeover-on-quit` «AI замінює гравця, що вийшов» · game-logic/opponent · 📎.
  - `+territory-capture`, `+letter-value-scoring` — уже пропоновані іншими файлами.

## Пропозиції до словників
- `+trigger:word_submitted` — гравець подав слово.
- `+cond:word_length_max` — довжина слова ≤ N (тут N = солдати в бою).
- `+cond:word_score_higher` — слово дорожче за слово суперника.
- `+effect:move_troops` — перевести N солдатів між територіями.
- `+effect:reinforce` — додати солдатів територіям за правилом.
- `+ui:troop-count` — число солдатів на території.
- `+ui:treasure-meter` — шкала скарбу.
- `+ui:word-slots` — слоти під слово з лімітом довжини.
- `+window:duel-screen` — окремий екран бою (сварки).
- `+feature:ai-profiles` — профілі AI зі стилем і рейтингом.
- `+axis:turn-structure=phased` — нове значення наявної осі: атаки → перекидання → підкріплення.

## Джерела
- ⭐ [Wikipedia: Quarrel (video game)](https://en.wikipedia.org/wiki/Quarrel_(video_game)) — суть, 9 AI, таблиця вартості літер, платформи й дати, BAFTA Scotland.
- [Game Informer: Quarrel review](https://gameinformer.com/games/quarrel/b/xbox360/archive/2012/02/02/quarrel-review-turning-words-into-war) — 12 мап, 8 літер, ліміт довжини військами, тайбрейк швидкістю, режими, AI на місці того, хто вийшов.
- [ZTGD: Quarrel Review](https://ztgd.com/?p=18817) — n−1 солдатів на здобуту територію, полонені андердога, +1 на територію в кінці ходу, перекидання, скарб, слово глядача, Domination 12 / Showdown 9, медалі, Word IQ.
- [TouchArcade: Quarrel Deluxe](https://toucharcade.com/?p=74815) — фаза атаки, одна плитка на солдата, підкріплення за територіями, AI-помилки.
- [Pocket Gamer: Quarrel Deluxe review](https://www.pocketgamer.com/quarrel-deluxe/review/) — старт 4–7 солдатів, захист зводить до 1, бонусний солдат від шкали, профілі AI.
- [GeekNative](https://geeknative.com/25683/a-war-of-words-quarrel-review) — до 8 армій на сторону, полонені.
- [Denki: Quarrel FAQ part 1](https://denki.co.uk/2011/08/31/introducing-quarrel-faq-part-1/) — зміст FAQ; [Denki: архів Quarrel](https://denki.co.uk/games/archive/quarrel/) — словник HarperCollins.
- YouTube: пошук «quarrel denki gameplay».

## Непевне
- (?) Скільки атак за хід, мінімум солдатів для атаки, точна кількість полонених і розмір бонусу андердога — FAQ Denki (де це пояснено) віддає 404.
- (?) Підкріплення: «+1 кожній території» (ZTGD) проти «за кількістю територій» (TouchArcade) — можливо, те саме.
- (?) Чи 8 літер завжди анаграма 8-літерного слова — одне джерело в пошуку, TouchArcade каже «scrambled anagram».
- (?) Ліміт 8 солдатів на території — «до 8 армій на сторону в бою» (GeekNative), окремого правила про стек не бачив.
- (?) Trailblazing, Bonus Time, timed quarrels — назви з FAQ, суть невідома.
- (?) Мапи як граф чи як квадратна сітка «клітин» — Pocket Gamer згадує «square», інші — «territories».
