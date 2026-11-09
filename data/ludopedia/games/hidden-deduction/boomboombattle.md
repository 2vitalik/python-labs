---
title: BoomBoomBattle
slug: boomboombattle
aka: [Boom Boom Battle]
family: hidden-deduction
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: online
  info: hidden
  random: setup
  goal: race
year: 2026
platforms: [web (boomboombattle.com, itch.io HTML5), mobile browser]
links:
  - {kind: itch, url: "https://unitendded.itch.io/boomboombattle", best: true, note: "таблиця раундів (гравці, поле, міни, таймер), критерії проходу, керування, режими, fair play з хешем поля"}
  - {kind: official, url: "https://boomboombattle.com/en/rules/", note: "правила: порядок заліку, кінець раунду, фінал, прапорці, акорд"}
  - {kind: official, url: "https://boomboombattle.com/fr/regles/", note: "ті самі правила французькою"}
  - {kind: official, url: "https://boomboombattle.com", note: "головна: грати без реєстрації, видно, як вибухають інші"}
  - {kind: youtube, url: "https://www.youtube.com/@BoomBoomBattle-YT", note: "канал гри (лінк зі сторінки itch; сам канал не відкривав)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=BoomBoomBattle+minesweeper+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [cell-click, chord-click, neighbor-count-clue, flood-reveal, mines-after-first-click, no-guess-generation, completion-detection, time-out, simultaneous-versus, online-multiplayer, leaderboard, rating-system, controls-remap, game-screen, +elimination-rounds, +progress-tiebreak, +player-elimination, +board-hash-commit, +practice-any-round]
proposes: ["+trigger:round_end", "+effect:eliminate", "+ui:live-ranking", "+feature:private-room", "+feature:fair-play-hash", "+card:elimination-rounds", "+card:progress-tiebreak", "+card:board-hash-commit", "+card:practice-any-round"]
author: opus
date: 2026-11-09
---

# BoomBoomBattle — королівська битва в сапера: 32 гравці, кожен на своєму полі, щораунду проходить половина

## Суть
Звичайний [minesweeper](minesweeper.md) без вгадувань, але на швидкість проти 31 суперника онлайн. Кожен грає своє поле однакової складності; раунд обмежений таймером, і до наступного проходить половина — спершу ті, хто очистив поле, у порядку фінішу, далі ті, хто відкрив більше. Міна не вибиває одразу: твоя гра в раунді зупиняється, але відкрите поле ще може пройти в залік. Чотири фіналісти змагаються за подіум.

## Поле і час
- Квадратна сітка, розмір росте з раундами: 9×9 / 10 мін → 9×12 / 16 → 9×14 / 20 → фінал 9×14 / 24.
- Таймер раунду: 60 → 90 → 120 → 150 с; гравці грають одночасно, кожен на своєму полі (`time: realtime` — гонка, а не ходи).
- Поля «усі однакової складності» й розвʼязні без вгадування; чи це одне й те саме поле для всіх — (?).
- Сусідство 8-клітинне, нуль відкриває сусідів автоматично.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Закрита клітина | tile | — | відкривається тапом/кліком |
| Число | mark | 0–8 | кількість мін серед 8 сусідів; 0 — каскад |
| Міна | hazard | — | відкрити = твоя гра в раунді зупиняється |
| Прапорець | mark | — | довге натискання / ПКМ; потрібен для акорду |
| Гравець | player | стан: грає / очистив / вибухнув | одне поле, одне «життя» на раунд |
| Раунд | zone | гравців, місць для проходу, поле, міни, таймер | 32→16 → 16→8 → 8→4 → фінал 4 |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` (раунд) → ТО `custom: «кожному живому гравцю — своє поле розміру раунду, без вгадувань; хеш поля публікується»`, `timer(start, 60|90|120|150 s)`.
- КОЛИ `input(open, cell)` → ЯКЩО `first_time` → ТО `custom: «клітина гарантовано безпечна»`, `reveal(cell)`.
- КОЛИ `input(open, cell)` → ЯКЩО `not occupied(cell, mine)` → ТО `reveal(cell)`, `set_value(cell, adjacent_count(cell, mine))`.
- КОЛИ `after(reveal)` → ЯКЩО `adjacent_count(cell, mine, ==, 0)` → ТО `reveal(neighbors8)` (каскад).
- КОЛИ `input(flag, cell)` → ТО `mark(cell, flag)` / повторно `unmark(cell)`.
- КОЛИ `input(open, number)` → ЯКЩО `custom: «навколо стоїть стільки прапорців, скільки показує число»` → ТО `reveal(unflagged neighbors)` (акорд).
- КОЛИ `input(open, cell)` → ЯКЩО `occupied(cell, mine)` → ТО `set_state(player, exploded)` — гра в раунді зупиняється, відкрите поле зберігається для заліку; інші бачать вибух наживо.
- КОЛИ `counter(closed_safe, ==, 0)` → ТО `set_state(player, cleared)`, `custom: «місце в черзі фінішу»`.
- КОЛИ `custom: «усі місця для проходу зайняті очищеними полями»` або `timer(0)` або `custom: «ніхто вже не грає»` → ТО `custom: «кінець раунду»` (`+trigger:round_end`).
- КОЛИ `timer(0)` → ЯКЩО `state(player, playing)` → ТО `set_state(player, exploded)` — хто не встиг, «вибухає».
- КОЛИ `custom: «кінець раунду»` → ТО `custom: «залік: 1) очищені — за часом фінішу; 2) решта — за часткою відкритого; 3) нічия — хто раніше досяг цієї частки»`; верхня половина проходить, решта — `custom: «вибуває»` (`+effect:eliminate`).
- Фінал: КОЛИ `counter(closed_safe, ==, 0)` для першого гравця → ТО `win`; решта місць подіуму — за тим самим заліком.
- Фінал: КОЛИ `custom: «лишився один гравець, що грає, і він далі за всіх, хто вибухнув»` → ТО `win` одразу.
- Перемога: перше місце у фіналі · Поразка: не пройти залік раунду · Рахунок: очки й ранги профілю (формула — (?)).

## Керування і ввід
- Телефон/планшет: тап — відкрити, довге натискання — прапорець, тап по числу з усіма прапорцями — акорд; налаштування «Tap = flag» міняє тап і довге натискання місцями.
- Компʼютер: ЛКМ — відкрити, ПКМ або Ctrl+клік — прапорець, клік по числу — акорд.
- Мовна: EN / FR; вхід через Google чи Discord — лише на сайті, гість має окремий прогрес.

## Вікна, меню, HUD
- `main-menu` сайту: грати одразу, без реєстрації; режими — битва, тренування, приватна кімната.
- `lobby-window` (?) — набір 32 гравців перед битвою; деталі не бачив.
- `game-screen`: власне поле, таймер раунду (`timer-countdown`), вибухи інших наживо (`+ui:live-ranking`, вигляд — (?)).
- `end-screen` раунду: хто пройшов, твоє місце (?); у кінці — подіум фіналу і перевірка хешу полів.
- `leaderboard`: рекорди дня, тижня, місяця й усіх часів.
- `settings-window`: «Tap = flag», мова.

## Фічі поза полем
- `mode-practice`: будь-яке поле раунду, з таймером або без (`+practice-any-round`).
- `online-multiplayer` на сервері; `+feature:private-room` — приватні кімнати для друзів.
- `rank-tiers` і очки профілю, `custom-skins` — налаштовувані предмети поля (що саме — (?)).
- `+feature:fair-play-hash` — хеш кожного поля публікується на старті й розкривається в кінці: гравці можуть перевірити, що поле не підмінили.
- `leaderboard-online` — щоденні, тижневі, місячні й абсолютні рекорди.

## Варіації й родичі
- База — [minesweeper](minesweeper.md); без вгадувань — як [kaboom](kaboom.md) і [hexcells](hexcells.md); інший мультиплеєр сапера — [minesweeper-together](minesweeper-together.md) (спільне поле в кооперативі, versus з одним сідом).
- Королівські битви в корпусі: [pac-man-battle-royale](../maze-arcade/pac-man-battle-royale.md), [babble-royale](../word-number/babble-royale.md); формат «кожен на своєму полі, вибуває половина» — як Tetris 99 у [tetris](../falling-match/tetris.md) (?).
- **Осі варіацій «змагання в сапера»:** одне поле на всіх / однакове поле кожному / однакова складність; відсів — останній живий / половина щораунду / рахунок у кінці; міна — кінець гри / зупинка з заліком прогресу / втрата життя.

## Цікавинки для курсу
- Залік раунду: сортування за ключем `(not cleared, finish_time, -opened, reached_at)` і прохід верхньої половини — 🌱.
- Таймер раунду + три умови кінця раунду (місця зайняті / час / ніхто не грає) — 📎.
- Таблиця раундів як дані (`players, qualify, size, mines, seconds`) і турнір 32 → 16 → 8 → 4 — 📎.
- Чесність через хеш: показати `sha256(поле)` на старті, розкрити поле в кінці — 🌱 (і гарна тема про commit–reveal).
- Генерація полів без вгадування однакової складності — 🥇.
- Сервер з 32 одночасними гравцями й трансляцією вибухів — 🥇 (картка `online-multiplayer`).

## Мапа на каталог
- Є: `cell-click`, `chord-click`, `neighbor-count-clue`, `flood-reveal`; `mines-after-first-click` ↔ перший тап безпечний; `no-guess-generation`; `completion-detection` ↔ очищене поле; `time-out` ↔ таймер раунду; `simultaneous-versus` ↔ кожен на своєму полі; `online-multiplayer`; `leaderboard` ↔ рекорди за періоди; `rating-system` ↔ очки й ранги; `controls-remap` ↔ «Tap = flag»; `game-screen`.
- **Нема** → пропозиції карток:
  - `+elimination-rounds` «Серія раундів, після кожного проходить частина гравців» · game-logic/opponent · 📎 · слоти {qualify: half, rounds}.
  - `+progress-tiebreak` «Залік за часткою виконаного й часом, коли ціль не досягнута» · game-logic/score · 🌱.
  - `+player-elimination` (вже пропонована) — вибування з турніру.
  - `+board-hash-commit` «Хеш поля на старті, розкриття в кінці» · game-logic/opponent · 🌱.
  - `+practice-any-round` «Тренування на будь-якій конфігурації раунду» · levels/bank · 🌱.

## Пропозиції до словників
- `+trigger:round_end` — кінець раунду з кількох причин (уже пропонувався в корпусі).
- `+effect:eliminate` — гравець вибуває з турніру, гра триває для інших (уже пропонувався).
- `+ui:live-ranking` — поточний порядок гравців/вибухи наживо (уже пропонувався).
- `+feature:private-room` — закрита кімната для своїх; `+feature:fair-play-hash` — див. вище.
- `+card:elimination-rounds`, `+card:progress-tiebreak`, `+card:board-hash-commit`, `+card:practice-any-round`.

## Джерела
- ⭐ [itch.io: BoomBoomBattle](https://unitendded.itch.io/boomboombattle) — таблиця раундів, критерії проходу, керування для тач і ПК, тренування, рекорди, приватні кімнати, очки й ранги, хеш полів; PixiJS, EN/FR, 2026.
- [BoomBoomBattle: Rules](https://boomboombattle.com/en/rules/) — порядок заліку, три умови кінця раунду, фінал і дострокова перемога, прапорці, акорд.
- [BoomBoomBattle: Règles](https://boomboombattle.com/fr/regles/) — те саме французькою («attendre ne rapporte rien»).
- [boomboombattle.com](https://boomboombattle.com) — головна: одночасна гра, видно вибухи інших.
- YouTube: канал гри (лінк зі сторінки) і пошук «BoomBoomBattle minesweeper gameplay».

## Непевне
- (?) Чи всі гравці раунду грають ідентичне поле, чи лише поля однакової складності («toutes de même difficulté»).
- (?) Чи 31 суперник — завжди живі люди, чи порожні місця добирають боти.
- (?) Як нараховуються очки й ранги профілю; які саме «предмети поля» налаштовуються.
- (?) Що саме видно про інших під час раунду (лише вибухи чи прогрес), як виглядає лобі й екран між раундами.
- (?) Порівняння з Tetris 99 — моя аналогія, не з джерел.
