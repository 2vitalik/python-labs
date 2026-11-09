---
title: Wordament
slug: wordament
aka: [Microsoft Wordament]
family: word-number
also: []
klass: puzzle
axes:
  field: square
  time: realtime
  opponent: online
  info: full
  random: setup
  goal: score
year: 2012
platforms: [Windows Phone, Windows, iOS, Android, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Wordament", best: true, note: "правила пошуку, спецплитки (диграф, either/or, префікс, суфікс), платформи, Xbox Live, Word Twister і Crosswords у релізі 2017"}
  - {kind: other, url: "https://wiki-origin.giantbomb.com/wiki/Games/Wordament", note: "синхронна безперервна сесія раундів для всіх, лідерборд після раунду, дати релізів"}
  - {kind: other, url: "https://blogs.windows.com/devices/2012/08/20/challenge-your-mind-and-the-world-with-wordament/", note: "раунд 2 хв, 4×4, у кожного поля 100+ слів, вартість літер, guest mode"}
  - {kind: other, url: "https://blogs.windows.com/windowsexperience/2012/03/05/sidebar-5-tips-for-boosting-your-wordament-sc/", note: "поради: дорогі Q/Qu/K/Z/V, кожна плитка входить хоч в одне слово"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=wordament+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [word-validation, time-out, event-points, online-multiplayer, simultaneous-versus, leaderboard, rating-system, profile-stats, path-drawing, path-cut, completion-detection, achievements-window, game-screen, end-screen, help-window, stats-window, +path-trace-word, +letter-value-scoring, +multi-letter-face, +either-or-tile, +affix-tile, +synced-global-rounds, +percentile-rank, +found-words-list]
proposes: ["+cond:at_word_start", "+cond:at_word_end", "+cond:path_adjacent8", "+window:round-results", "+ui:percentile-rank", "+ui:round-countdown", "+feature:synced-global-rounds", "+feature:guest-mode", "+card:synced-global-rounds"]
author: opus
date: 2026-11-09
---

# Wordament — Boggle 4×4 як безперервний світовий турнір: усі отримують ту саму сітку на 2 хвилини

## Суть
Пошук слів по сусідніх плитках сітки 4×4, як у Boggle, але кожен раунд одночасно грають усі онлайн-гравці світу на тому самому полі. Раунди йдуть безперервно один за одним; після кожного — таблиця, де ти бачиш своє місце й перцентиль серед усіх. Очки — за вартість літер слова (дорогі Q, Z, K, V), а не лише за довжину; особливі плитки (диграфи, «або-або», префікси й суфікси) змінюють граф слів. Ядро — синхронна масова сесія замість кімнати на кількох гравців.

## Поле і час
- Сітка 4×4, 16 плиток; суміжність 8 (з діагоналями); кожна плитка — не більше раз на слово.
- На кожному полі понад 100 можливих слів.
- Раунд ~2 хв; раунди йдуть одною безперервною синхронізованою сесією для всіх; між раундами — показ результатів (тривалість (?)).
- Поле статичне протягом раунду; новий раунд — нова сітка.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка-літера | tile | літера, вартість (?) | вузол графа слова; дорожчі рідкісні літери |
| Диграф | tile | дві літери без косої (напр. «TH») | вживається обидві літери разом |
| Either/Or | tile | дві літери через «/» | читається як одна з двох; зараховується одне прочитання (?) |
| Префікс-плитка | tile | «літери-» | може бути лише на початку слова |
| Суфікс-плитка | tile | «-літери» | може бути лише в кінці слова |
| Знайдене слово | mark | слово, очки | повтор того самого слова не рахується |
| Гравець | player | рахунок раунду, ранг | грає з усіма на тому самому полі |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `custom: «старт раунду для всіх»` → ТО `custom: «однакова сітка всім гравцям»`, `timer(start, 120 s)`.
- КОЛИ `input(drag path)` → ЯКЩО `custom: «наступна плитка — 8-сусід, плитка ще не в шляху»` → ТО `set_state(tile, selected)`; інакше `block`.
- КОЛИ `input(release)` → ЯКЩО `custom: «довжина ≥ 3»` and `in_dictionary(word)` and `custom: «ще не знайдене в цьому раунді»` → ТО `score(сума вартостей літер)`, `custom: «слово в список»`.
- Заборонені: абревіатури й власні назви; множини, часові форми й анаграми — дозволені.
- КОЛИ `input(path)` → ЯКЩО `custom: «префікс-плитка не перша»` → ТО `block`.
- КОЛИ `input(path)` → ЯКЩО `custom: «суфікс-плитка не остання»` → ТО `block`.
- КОЛИ `input(path)` → ЯКЩО `custom: «плитка — диграф»` → ТО `custom: «додати обидві літери»`.
- КОЛИ `input(path)` → ЯКЩО `custom: «плитка — either/or»` → ТО `custom: «підставити ту літеру, з якою слово валідне»`.
- КОЛИ `counter(time_left, ==, 0)` → ТО `custom: «ввід закрито»`, `window(round-results)`.
- КОЛИ `after(window(round-results))` → ТО `custom: «місце і перцентиль серед усіх гравців раунду»`, `custom: «показ усіх слів поля»` (?).
- КОЛИ `custom: «результати показано»` → ТО `custom: «наступний раунд автоматично»`.
- Рахунок: сума очок раунду; переможця сесії як стану нема — порівняння з усім світом · Поразки нема.

## Керування і ввід
- Тач/миша: провести пальцем по сусідніх плитках без відриву; відпуск — подати слово.
- Повернення назад по шляху — укоротити слово (?).
- Guest mode: інша людина грає без впливу на статистику власника.

## Вікна, меню, HUD
- `game-screen`: сітка 4×4, `round-countdown`, `word-preview` поточного шляху, `score`, `found-words-list` (?).
- `round-results`: лідерборд раунду, твоє місце, `percentile-rank`, секунди на слово, очки на слово (?), список слів поля.
- `main-menu` (з 2017): Wordament · Word Twister · Crosswords.
- `achievements-window` / `stats-window` — Xbox Live досягнення і Gamerscore, статистика профілю.
- `help-window` — правила й типи спецплиток.
- Переходи: `main-menu` → `game-screen` (раунд) → `round-results` → `game-screen` (наступний) → … ; вихід у меню будь-коли.

## Фічі поза полем
- `online-multiplayer` масового масштабу: одна сесія на всіх, `leaderboard-online` після кожного раунду, скидання лідерборду через період (?).
- `achievements`, `stats` (Xbox Live, і на iOS/Android) · `guest-mode`.
- Інші режими релізу 2017: Word Twister (слова з набору плиток, «Bonus Twister»), Crosswords (кросворди з кнопкою Check).
- Продовження: Wordament Snap Attack (2014).

## Варіації й родичі
- Boggle (`boggle.md`) — те саме поле й суміжність; там скасування спільних слів, тут масовий ранг.
- Squaredle (`squaredle.md`) — той самий пошук, але щоденний і з обовʼязковим списком.
- SpellTower (`spelltower.md`), Bookworm (`bookworm.md`) — шлях по сусідах з гравітацією.
- **Осі варіацій:** суперники (стіл / кімната / весь світ синхронно) · рахунок (довжина / вартість літер / множники плиток у Snap Attack) · спецплитки (Qu / диграф / або-або / префікс / суфікс) · таймер раунду.

## Цікавинки для курсу
- Шлях по 8-сусідах з перевіркою «плитка вже в шляху» — 📎.
- Спецплитки з позиційними обмеженнями (префікс/суфікс) і варіантним читанням (either/or) у DFS-солвері — 🥉.
- Солвер «усі слова поля» з trie для показу після раунду — 🥇.
- Синхронні раунди для всіх клієнтів за серверним годинником + перцентиль у результатах — 🥈.
- Очки як сума вартостей літер — 🌱.

## Мапа на каталог
- Є: `word-validation` · `time-out` ↔ кінець раунду · `event-points` ↔ вартість літер · `online-multiplayer` · `simultaneous-versus` ↔ усі на тому самому полі · `leaderboard` · `rating-system` ↔ ранг/перцентиль · `profile-stats` · `path-drawing` ↔ drag по плитках · `path-cut` (?) · `completion-detection` · `achievements-window` · `game-screen` · `end-screen` · `help-window` · `stats-window`.
- **Нема** → пропозиції карток:
  - `+path-trace-word`, `+multi-letter-face`, `+found-words-list` — див. `boggle.md`.
  - `+letter-value-scoring` «Очки слова = сума вартостей літер» · game-logic/score · 🌱.
  - `+either-or-tile` «Плитка з двома альтернативними літерами» · entities/state · 📎.
  - `+affix-tile` «Плитка лише на початку / в кінці слова» · entities/legality · 📎.
  - `+synced-global-rounds` «Безперервні раунди на одному полі для всіх онлайн» · game-logic/opponent · 🥈.
  - `+percentile-rank` «Перцентиль серед усіх гравців раунду» · interface/results · 📎.

## Пропозиції до словників
- `+cond:at_word_start` / `+cond:at_word_end` — елемент стоїть першим / останнім у слові (префікс/суфікс-плитки).
- `+cond:path_adjacent8` — шлях по 8-сусідах без повтору (Boggle, SpellTower, Strands, Wordament, Squaredle).
- `+window:round-results` — результати раунду з місцем і словами поля.
- `+ui:percentile-rank` — твій перцентиль серед усіх гравців.
- `+ui:round-countdown` — зворотний відлік раунду, спільний для всіх.
- `+feature:synced-global-rounds` — безперервні синхронні раунди для всіх.
- `+feature:guest-mode` — гра гостя без впливу на статистику власника.
- `+card:synced-global-rounds` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Wordament](https://en.wikipedia.org/wiki/Wordament) — правила шляху, мін. 3 літери, спецплитки, Microsoft Casual Games, 24.04.2012, релаунч 2017 з Word Twister і Crosswords, Xbox Live на iOS/Android.
- [Giant Bomb: Wordament](https://wiki-origin.giantbomb.com/wiki/Games/Wordament) — синхронна безперервна сесія, лідерборд після раунду, дати по платформах (WP 2011, Win8 2012, iOS 2012, веб 2013, Android 2013), Snap Attack.
- [Windows Blog 2012-08](https://blogs.windows.com/devices/2012/08/20/challenge-your-mind-and-the-world-with-wordament/) — раунд 2 хв, 4×4, 100+ слів, вартість літер, guest mode.
- [Windows Blog 2012-03: 5 tips](https://blogs.windows.com/windowsexperience/2012/03/05/sidebar-5-tips-for-boosting-your-wordament-sc/) — дорогі літери, кожна плитка в слові, множини й анаграми валідні.
- YouTube: пошук «wordament gameplay».

## Непевне
- (?) Рік: Wikipedia — 24.04.2012, Giant Bomb — Windows Phone 01.04.2011; узяв 2012 з черги.
- (?) Точні вартості літер і чи є бонус за довжину — джерела кажуть лише «кожна літера має вартість».
- (?) Пауза між раундами, тривалість показу результатів, період скидання лідерборду — не знайшов.
- (?) Перцентиль, секунди і очки на слово на екрані результатів — лише з пошукового резюме (TrueAchievements віддав 403).
- (?) Тематичні раунди — згадка з памʼяті, у відкритих джерелах не бачив.
- (?) Either/or: чи зараховуються обидва прочитання як окремі слова — у резюме пошуку «credit only for one».
