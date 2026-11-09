---
title: "Apple News+ Quartiles"
slug: quartiles
aka: [Quartiles]
family: word-number
also: []
klass: cursor
axes:
  field: square
  time: static
  opponent: none
  info: partial
  random: none
  goal: score
year: 2024
platforms: [iOS 17.5, iPadOS 17.5, macOS 14.5 (Apple News+, США й Канада)]
links:
  - {kind: official, url: "https://support.apple.com/guide/news/iph701ef27fb/mac", best: true, note: "довідка Apple: сітка 4×5, плитки 2–4 літери, 1/2/4/8 очок, +40 за всі квартилі, Expert = 100, Reveal All Words, Shuffle, Arrangement"}
  - {kind: other, url: "https://www.cultofmac.com/how-to/quartiles", note: "how-to: кнопки ✓ і ×, сортування знайдених, shuffle, меню ⋯ (туторіал, здатися), збереження прогресу"}
  - {kind: official, url: "https://apple.com/newsroom/2024/05/apple-news-plus-introduces-quartiles-a-new-game-and-offline-mode-for-subscribers", note: "анонс 2024-05-13: щоденні пазли, очки за довжину, офлайн-режим, Scoreboard зі статистикою й серіями"}
  - {kind: other, url: "https://www.macrumors.com/2024/04/10/ios-17-5-apple-news-quartiles-game/", note: "бета iOS 17.5: 20 плиток, слова з 1–4 плиток, бонус 40, лідерборди Game Center"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=apple+news+quartiles+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [daily-puzzle, word-validation, cell-click, drag-drop-piece, selection-highlight, keep-playing-after-win, remaining-counter, goal-counter, streak-stats, stats-window, leaderboard, tutorial-window, puzzle-select, save-progress, game-screen, +fragment-tiles, +tile-count-scoring, +full-set-bonus, +rank-thresholds, +found-words-list, +shuffle-board, +found-group-anchor, +reveal-solution, +reveal-voids-streak]
proposes: ["+cond:in_puzzle_list", "+effect:shuffle", "+ui:found-words-list", "+ui:shuffle-button", "+ui:next-rank", "+window:archive-window", "+feature:offline-mode", "+feature:reveal-penalty", "+feature:share-puzzle", "+card:fragment-tiles", "+card:tile-count-scoring", "+card:found-group-anchor"]
author: opus
date: 2026-11-09
---

# Apple News+ Quartiles — 20 плиток-складів: склей слова з 1–4 плиток і знайди п'ять «квартилів» із чотирьох

## Суть
Сітка 4×5 із двадцяти плиток, на кожній — фрагмент слова на 2–4 літери (склад, префікс, суфікс). Гравець натискає плитки по черзі, склеюючи слово з однієї–чотирьох плиток; що більше плиток, то більше очок (1 → 2 → 4 → 8). Слова з чотирьох плиток — «квартилі»: їх у кожному пазлі п'ять, і разом вони розбивають усі 20 плиток. Мета — ранг Expert (100 очок), після нього можна шукати далі.

## Поле і час
- Сітка 4×5 = 20 плиток; знайдений квартиль стає групою з чотирьох і якориться рядом унизу сітки (опційно — вгорі).
- Плитки не витрачаються: одна плитка може входити в багато слів.
- Час: статичний, без таймера; прогрес зберігається, до пазла можна повернутись.
- Щодня новий пазл; минулі — в архіві (вкладка Quartiles).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка-фрагмент | tile | 2–4 літери | натискається; входить у поточне слово; не зникає |
| Поточне слово | mark | 1–4 плитки в порядку натискання | порядок міняється перетягуванням; ✓ — перевірити, × — скинути |
| Квартиль | zone | 4 плитки, 8 очок | знайдений → група-ряд, якориться, не перемішується |
| Список слів пазла | zone | прихований | лише «звичайні» слова: без рідкісних і технічних, власних назв, лайки |
| Words Found | zone | знайдені слова з очками | після Expert показує, скільки слів лишилось |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(tap tile)` → ЯКЩО `count(word_tiles, <, 4)` і `custom: «плитки ще нема в поточному слові»` (?) → ТО `set_state(tile, selected)`, `custom: «фрагмент дописується в кінець поточного слова»`.
- КОЛИ `input(drag selected tile)` → ТО `custom: «змінити порядок плиток у поточному слові»`.
- КОЛИ `input(clear ×)` → ТО `clear_state(word_tiles, selected)`.
- КОЛИ `input(check ✓)` → ЯКЩО `in_dictionary(word)` і `custom: «слово є у списку цього пазла»` і `custom: «ще не знайдене»` → ТО `score(1 | 2 | 4 | 8)` за 1 | 2 | 3 | 4 плитки, `custom: «слово з очками — у Words Found»`; інакше `custom: «слово не зараховано»` (?).
- КОЛИ `input(check ✓)` → ЯКЩО `count(word_tiles, ==, 4)` і слово зараховано → ТО `set_state(4 плитки, quartile)`, `custom: «група якориться рядом унизу сітки»`.
- КОЛИ `counter(quartiles, ==, 5)` → ТО `score(+40)`.
- КОЛИ `counter(score, >=, 100)` → ТО `custom: «ранг Expert»`, `custom: «Words Found показує кількість незнайдених слів»`; гра триває, очки далі ростуть.
- КОЛИ `input(next rank)` → ТО `custom: «показати, скільки очок до наступного рангу»`.
- КОЛИ `input(shuffle)` → ЯКЩО `state(arrangement, on)` → ТО `custom: «перемішати плитки поза знайденими квартилями»`; інакше `custom: «перемішати всі плитки»`.
- КОЛИ `input(sort found quartiles)` → ТО `custom: «якорити знайдені квартилі вгорі замість унизу»`.
- КОЛИ `input(reveal all words)` → ТО `custom: «показати всі незнайдені слова»`; ЯКЩО `counter(score, <, 100)` → ТО `custom: «пазл не йде в Scoreboard і рве серію»`.
- КОЛИ `input(back)` → ТО `custom: «прогрес збережено»`.
- Перемога: ранг Expert (100) · Поразка: нема · Рахунок: Σ (1/2/4/8 за слово) + 40 за всі квартилі. Квартилі дають максимум 5×8 + 40 = 80, тож до Expert потрібні й короткі слова.

## Керування і ввід
- Тап по плитках у порядку слова; перетягування — змінити порядок; ✓ (Check) — подати; × (Clear) — скинути.
- Кнопка внизу ліворуч — Shuffle; внизу праворуч — сортування/якорення знайдених квартилів; Arrangement — вимкнути якорення.
- Меню ⋯ (More): How to Play, More Puzzles, Sort Found Quartiles, Reveal All Words.
- Тап по смузі Words Found — розгорнути список знайденого.

## Вікна, меню, HUD
- `game-screen`: сітка 4×5, поточне слово, кнопки ✓/×, `found-words-list` з очками, `score`, ранг і `next-rank`, `shuffle-button`, якорені квартилі.
- `tutorial-window`: How to Play (повторюваний з меню).
- `archive-window` / `puzzle-select`: стрічка пазлів Quartiles (минулі дні).
- `stats-window`: Puzzles Scoreboard — solve rate, поточна й найдовша серія.
- `leaderboard`: Game Center (з iOS 17.5); рейтинг вимикається в налаштуваннях.
- `confirm-dialog` перед Reveal All Words (?).
- Переходи: Apple News → Puzzles → Quartiles → `game-screen`; ⋯ → туторіал / стрічка / reveal; Back → вихід зі збереженням.

## Фічі поза полем
- `daily-puzzle` + архів минулих днів; `streaks` і `stats` у Scoreboard.
- `leaderboard-online` через Game Center (щоденний рахунок і час розвʼязку (?)).
- `show-solution` (Reveal All Words) з `reveal-penalty`: до Expert — без статистики й серії.
- `offline-mode`: пазли завантажуються разом з новинами (iOS 17.5).
- `share-puzzle`: поділитися пазлом з іншими підписниками.
- `tutorial`; збереження прогресу (`autosave`); підписка Apple News+ ($12.99/міс).

## Варіації й родичі
- [squaredle.md](squaredle.md), [boggle.md](boggle.md) — пошук усіх слів на полі, список знайденого; тут плитки — фрагменти, а суміжність не потрібна.
- [typeshift.md](typeshift.md) — слова з вертикальних «барабанів» літер.
- [nyt-connections.md](nyt-connections.md) — розбиття 16 елементів на 4 групи; квартилі розбивають 20 плиток на 5.
- NYT Spelling Bee — ранги за порогами очок і «Genius»; Quartiles переносить ідею на склади.
- **Осі варіацій:** одиниця плитки (літера / склад / слово) · суміжність (шлях по сусідах / будь-які плитки) · очки (за літери / за плитки експоненційно) · ціль (усі слова / поріг рангу / спецслова-розбиття).

## Цікавинки для курсу
- Очки 2^(n−1) за кількість плиток і бонус за повне розбиття — 🌱.
- Розбиття 20 фрагментів на 5 квартилів як точне покриття; генератор, де кожна плитка в рівно одному квартилі — 🥈.
- Перебір усіх слів з 1–4 плиток зі словника (перестановки ≤ 20·19·18·17) для списку відповідей і кількості «лишилось» — 📎.
- Якорення знайдених груп і shuffle лише решти — 🌱.
- Reveal зі штрафом для серії: стан «пазл зарахований / ні» — 🌱.

## Мапа на каталог
- Є: `daily-puzzle` · `word-validation` · `cell-click` ↔ тап по плитці · `drag-drop-piece` ↔ перестановка в слові · `selection-highlight` · `keep-playing-after-win` ↔ після Expert · `remaining-counter` ↔ скільки слів лишилось · `goal-counter` ↔ до наступного рангу · `streak-stats` · `stats-window` · `leaderboard` · `tutorial-window` · `puzzle-select` · `save-progress` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+fragment-tiles` «Плитки-фрагменти з кількох літер» · entities/state · 🌱.
  - `+tile-count-scoring` «Очки за кількість плиток у слові (1/2/4/8)» · game-logic/score · 🌱 · слоти {table}.
  - `+full-set-bonus` «Бонус за знаходження всіх спецслів» · game-logic/score · 🌱.
  - `+rank-thresholds` «Ранги за порогами очок у пазлі» · game-logic/win · 🌱 · слоти {thresholds}.
  - `+found-words-list` — див. [squaredle.md](squaredle.md); `+shuffle-board` — див. [nyt-connections.md](nyt-connections.md).
  - `+found-group-anchor` «Знайдена група фіксується рядом поля» · interface/hud · 🌱.
  - `+reveal-solution` — див. [nyt-digits.md](nyt-digits.md); `+reveal-voids-streak` «Reveal до порогу не зараховує пазл» · interface/results · 🌱.

## Пропозиції до словників
- `+cond:in_puzzle_list` — слово є в кураторському списку відповідей пазла (вужче за словник).
- `+effect:shuffle` — перемішати плитки (крім закріплених).
- `+ui:found-words-list`, `+ui:shuffle-button`, `+ui:next-rank` — скільки очок до наступного рангу.
- `+window:archive-window` — архів минулих щоденних пазлів.
- `+feature:offline-mode` — пазли доступні без мережі; `+feature:reveal-penalty` — показ розвʼязку знімає зарахування; `+feature:share-puzzle` — поділитися пазлом з іншим гравцем.
- `+card:fragment-tiles`, `+card:tile-count-scoring`, `+card:found-group-anchor`.

## Джерела
- ⭐ [Apple Support: Play Quartiles](https://support.apple.com/guide/news/iph701ef27fb/mac) — сітка 4×5, плитки 2–4 літери, таблиця очок, Expert, Reveal, Shuffle, Arrangement, сортування.
- [Cult of Mac: How to play Quartiles](https://www.cultofmac.com/how-to/quartiles) — кнопки, меню ⋯, збереження, «завжди можна набрати 100».
- [Apple Newsroom, 2024-05-13](https://apple.com/newsroom/2024/05/apple-news-plus-introduces-quartiles-a-new-game-and-offline-mode-for-subscribers) — анонс, офлайн-режим, Scoreboard.
- [MacRumors, 2024-04-10](https://www.macrumors.com/2024/04/10/ios-17-5-apple-news-quartiles-game/) — 20 плиток, бонус 40, Game Center.

## Непевне
- (?) Чи можна взяти ту саму плитку двічі в одному слові — джерела мовчать (логіка гри — ні).
- (?) Що кожна плитка входить рівно в один квартиль — висновок з 20 = 5×4 і якорення квартилів рядами, прямо не сказано.
- (?) Назви й пороги рангів, крім Expert = 100.
- (?) Метрики лідербордів Game Center (Daily Score, Daily Solve Time) — зі сніпета 9to5Mac, сторінку не відкривав.
- (?) Реакція на хибне слово (трусіння, повідомлення) і чи є діалог підтвердження перед Reveal.
- Рік: черга — 2024 ✓ (бета квітень, реліз з iOS 17.5 у травні 2024).
