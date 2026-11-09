---
title: Squaredle
slug: squaredle
aka: [Squaredle Express, Squaredle Squared]
family: word-number
also: []
klass: puzzle
axes:
  field: graph
  time: static
  opponent: none
  info: full
  random: none
  goal: collect
year: 2022
platforms: [web]
links:
  - {kind: play, url: "https://squaredle.app", best: true, note: "сама гра: правила, перки, обовʼязкові й бонусні слова, підказки, налаштування, статистика"}
  - {kind: other, url: "https://help.squaredle.app/support/solutions/articles/151000167237-how-do-i-play-", note: "довідка «How do I play»: суміжність, ввід з клавіатури, згасання клітин, зірки-перки"}
  - {kind: other, url: "https://wordfinder.yourdictionary.com/blog/the-story-of-squaredle-talking-with-game-creator-michael-giuffrida", note: "інтервʼю з автором: 4+ літери, розміри за днями тижня, дірки, курування списку слів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=squaredle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [daily-puzzle, word-validation, path-drawing, keyboard-controls, completion-detection, collect-all, goal-counter, remaining-counter, share-result, streak-stats, leaderboard, stats-window, settings-window, theme-select, achievements-window, puzzle-select, level-bank, help-window, tutorial-window, music-toggle, sound-effects, game-screen, +path-trace-word, +found-words-list, +required-bonus-words, +tile-fade-when-exhausted, +progress-perks, +word-reveal-hint, +accuracy-score, +board-rotate-view, +next-puzzle-countdown]
proposes: ["+cond:path_adjacent8", "+cond:required_word", "+trigger:all_found", "+ui:tile-word-count", "+ui:progress-stars", "+ui:accuracy-meter", "+ui:words-by-length", "+feature:progress-perks", "+feature:board-rotate", "+feature:word-reveal", "+card:required-bonus-words", "+card:tile-fade-when-exhausted"]
author: opus
date: 2026-11-09
---

# Squaredle — щоденний Boggle з фіксованим списком обовʼязкових слів; клітина згасає, коли всі її слова знайдено

## Суть
Щодня всім видається та сама сітка літер (зазвичай 4×4, іноді з дірками); треба знайти **всі обовʼязкові** слова від 4 літер, сполучаючи сусідні клітини в будь-якому напрямку. Список обовʼязкових слів курує автор (поширені слова), а рідкісні й архаїчні — бонусні, вони не потрібні для розвʼязку. Прогрес відкриває «перки»-підказки: скільки слів починається з клітини, скільки слів її використовує. Ядро — не таймер і не суперник, а повне покриття заздалегідь відомого списку з поступовими підказками.

## Поле і час
- Сітка: 3×3 (понеділок, Express), 4×4 (більшість), 5×5 (часто неділя); у центрі буває дірка — клітина без літери (тому `field: graph`).
- Суміжність 8 («вгору, вниз, вліво, вправо, по діагоналі»); клітина — не більше раз на слово.
- Час статичний; таймер є лише для лідерборду (паузиться, коли вкладка у фоні чи відкрите вікно).
- Складність росте за тиждень: пн найлегший, пт найважчий 4×4, сб — експерименти («twists»), нд — багато слів.
- Новий пазл щодня (3:00 Pacific на сайті; в інтервʼю — 6:00 Eastern, тобто той самий час).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітина-літера | tile | літера; лічильники «починається з» / «входить у» | вузол графа; згасає, коли всі обовʼязкові слова через неї знайдено |
| Дірка | static | порожня клітина | розриває граф |
| Обовʼязкове слово | mark | ≥4 літери | знайти всі = розвʼязати пазл |
| Бонусне слово | mark | рідкісне/архаїчне/сленг | «+1» біля лічильника; не в рахунку пазла, але в рейтингу бонусів |
| Bonus Word of the Day | mark | одне слово | знайти — отримати безплатне розкриття слова |
| Прогрес-бар із зірками | zone | 3 зірки + глобус | пороги відкривають перки |
| Розкриття слова | pickup | 1 за пазл (+1 за Bonus Word of the Day, +4 у Squared) | відкриває одне слово 4–6 літер |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «однакова сітка всім, список обовʼязкових слів прихований, видно лічильники за довжинами»`.
- КОЛИ `input(drag path | typed word)` → ЯКЩО `custom: «шлях по 8-сусідах без повтору клітини, без дірок»` → ТО `set_state(tile, selected)`; інакше `block`.
- КОЛИ `input(submit)` → ЯКЩО `custom: «довжина ≥ 4»` and `in_dictionary(word)` and `custom: «слово в обовʼязковому списку»` → ТО `score(+, довші — більше)`, `mark(word, found)`, `counter(found, +1)`.
- КОЛИ `input(submit)` → ЯКЩО `in_dictionary(word)` and `custom: «слово бонусне»` → ТО `counter(bonus, +1)` — точність не страждає.
- КОЛИ `input(submit)` → ЯКЩО `not in_dictionary(word)` → ТО `message`, `custom: «точність падає»`.
- КОЛИ `input(cancel)` (Esc або свайп до верху екрана) → ТО `custom: «слово скасовано без впливу на точність»`.
- КОЛИ `custom: «знайдено всі обовʼязкові слова через клітину»` → ТО `set_state(tile, faded)`.
- КОЛИ `counter(progress, >=, star1)` → ТО `reveal(starts_count on tiles)`; star2 → `reveal(uses_count on tiles)`; star3 → `unlock(word-list hints)`.
- КОЛИ `input(hint: show letters)` → ЯКЩО `custom: «зірка 3 або 15:00 Pacific»` → ТО `reveal(first letter; у довгих — перші 2 і кінцеві)`.
- КОЛИ `input(reveal word)` → ЯКЩО `has(player, reveal)` → ТО `reveal(word 4–6 літер)`, `take(player, reveal)`.
- КОЛИ `input(found bonus word of the day)` → ТО `give(player, reveal)`.
- КОЛИ `counter(found, ==, required)` → ТО `win`, `custom: «пазл розвʼязано; solve streak +1»`.
- Рахунок: очки за довжину; лідерборд за очками і словами, тай-брейки — бонусні слова, точність, швидкість · Поразки нема.

## Керування і ввід
- Тач/миша: drag від літери до літери з діагоналями.
- Клавіатура: набрати слово → сітка сама підсвічує шлях; Enter — подати, Backspace — стерти літеру, Esc — скасувати, Space — перемкнути між клітинами з однаковою літерою.
- Кнопка повороту сітки (свіжий погляд); у Squared — поворот на 45°.

## Вікна, меню, HUD
- `game-screen`: сітка з `tile-word-count` у кутах клітин (після зірок), згаслі клітини, `progress-bar` з `progress-stars` і глобусом (середній рахунок світу), лічильник слів «знайдено / усього + бонусні», `timer-elapsed`, кнопка повороту.
- `found-words-list` (вікно списку): вкладки Today / Yesterday / Past; знайдені й пропущені слова, `words-by-length`; підказки: сортування за алфавітом, перші літери, розкрити слово, порядок знаходження.
- `stats-window`: streak (дні гри), solve streak, зіграно/розвʼязано, середній і світовий рахунок, поточна точність і прогрес.
- `leaderboard`: Global · Favorites · Your scores.
- `settings-window`: темна тема, режим правші, таймер знизу, великий текст, музика і звуки; теми (10 кольорів) і шрифти (7); Squared-налаштування (45°, швидші перки).
- `share-window` (`custom-window`): Facebook / Copy, лінк-запрошення в улюблені лідерборду, підказка Bonus Word of the Day за поділ.
- `puzzle-select`: архів і класика (за підпискою), спецпазли (свята, Waffle-подібний, Member Weekly), Squaredle Express 3×3.
- `achievements-window`, `help-window` (About & feedback), `tutorial-window` (Skip tutorial).
- Переходи: вхід → (туторіал) → `game-screen` → розвʼязано → `stats-window` / `share-window`; «Next board in» — відлік до нового пазла.

## Фічі поза полем
- `daily-puzzle` + `streaks` (гри і розвʼязку) + `share-result` + `leaderboard-online` з друзями.
- `progress-perks` — підказки відкриваються прогресом, не кнопкою; `hint` за часом (15:00 Pacific).
- `word-reveal` як обмежений ресурс (1 + бонуси).
- `puzzle-bank` (архів), Express 3×3, спецпазли; Squaredle Squared — платна підписка (архів, більше розкриттів, іконка).
- `theme-select`, `font-scale`, `one-hand-mode` (правша), `sound-toggle`, `music-toggle`.

## Варіації й родичі
- Boggle (`boggle.md`), Wordament (`wordament.md`) — той самий пошук, але таймер і суперники; тут — повне покриття списку.
- Wordhuntle — гра, що надихнула автора; NYT Strands (див. `nyt-connections.md`) — шлях по сусідах з покриттям поля.
- Waffle (`waffle.md`) — щоденна сітка зі статистикою; Squaredle має Waffle-подібний спецпазл.
- **Осі варіацій:** мета (покрити список / набрати очки) · список (курований обовʼязковий + бонус / увесь словник) · підказки (за прогресом / за часом / ресурсом) · поле (3×3 / 4×4 / 5×5 / з дірками) · суперник (нема / лідерборд / раунд онлайн).

## Цікавинки для курсу
- Солвер усіх слів поля з trie і поділ на обовʼязкові/бонусні за курованим списком — 🥇.
- Лічильники на клітинах (скільки слів починається / використовує) з результату солвера — 📎.
- Згасання клітини, коли всі її обовʼязкові слова знайдено — 📎.
- Перки за порогами прогрес-бару — 🌱.
- Ввід з клавіатури: за набраним словом знайти шлях на сітці + Space перебирає однакові літери — 🥉.
- Лідерборд з тай-брейками (бонуси → точність → швидкість) і таймер, що паузиться у фоні — 📎.

## Мапа на каталог
- Є: `daily-puzzle` · `word-validation` ↔ NWL2023 · `path-drawing` ↔ drag · `keyboard-controls` ↔ набір з автошляхом · `completion-detection` · `collect-all` ↔ усі обовʼязкові · `goal-counter` / `remaining-counter` ↔ знайдено/лишилось · `share-result` · `streak-stats` · `leaderboard` · `stats-window` · `settings-window` · `theme-select` · `achievements-window` · `puzzle-select` / `level-bank` ↔ архів · `help-window` · `tutorial-window` · `music-toggle` · `sound-effects` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+path-trace-word`, `+found-words-list` — див. `boggle.md`.
  - `+required-bonus-words` «Обовʼязковий курований список + бонусні слова поза рахунком» · game-logic/score · 📎.
  - `+tile-fade-when-exhausted` «Клітина згасає, коли всі її слова знайдено» · interface/hud · 📎.
  - `+progress-perks` «Підказки відкриваються порогами прогресу» · game-logic/score · 🌱.
  - `+word-reveal-hint` «Розкрити одне слово як обмежений ресурс» · levels/solvability · 🌱.
  - `+accuracy-score` «Точність = частка валідних спроб» · game-logic/score · 🌱.
  - `+board-rotate-view` «Поворот поля лише для погляду» · interface/render · 🌱.
  - `+next-puzzle-countdown` — див. `wordle.md`.

## Пропозиції до словників
- `+cond:path_adjacent8` — шлях по 8-сусідах без повтору клітин (Boggle, Wordament, Squaredle).
- `+cond:required_word` — слово з курованого обовʼязкового списку (на відміну від бонусного).
- `+trigger:all_found` — знайдено всі елементи списку, що проходять через сутність (згасання клітини).
- `+ui:tile-word-count` — число слів, що починаються з клітини / використовують її.
- `+ui:progress-stars` — прогрес-бар з порогами-зірками.
- `+ui:accuracy-meter` — частка валідних спроб.
- `+ui:words-by-length` — скільки лишилось слів кожної довжини.
- `+feature:progress-perks` · `+feature:board-rotate` · `+feature:word-reveal`.
- `+card:required-bonus-words`, `+card:tile-fade-when-exhausted` — див. «Мапа на каталог».

## Джерела
- ⭐ [Squaredle](https://squaredle.app) — правила на сторінці: суміжність, клавіатура, згасання, перки, бонусні слова (~2× обовʼязкових), підказки, Bonus Word of the Day, Express, статистика, лідерборд, налаштування, теми, шрифти, розклад складності.
- [Squaredle Help: How do I play](https://help.squaredle.app/support/solutions/articles/151000167237-how-do-i-play-) — суміжність «around corners», Esc/свайп-скасування без втрати точності, Space, зірки, «+» = 10+ слів.
- [WordFinder: The story of Squaredle](https://wordfinder.yourdictionary.com/blog/the-story-of-squaredle-talking-with-game-creator-michael-giuffrida) — автор Michael Giuffrida, запуск 05.03.2022, мінімум 4 літери, розміри за днями, дірка в центрі, курування списку з Merriam-Webster, натхнення Wordhuntle.
- YouTube: пошук «squaredle gameplay».

## Непевне
- (?) Словник: сайт — NWL2023, інтервʼю 2022 — Merriam-Webster як старт; ймовірно змінювався.
- (?) Скільки очок за слово кожної довжини — лише «довші — більше».
- (?) Пороги зірок прогрес-бару — не бачив чисел.
- (?) Як саме падає точність (частка невалідних подань?) — виведено з «cancel without affecting accuracy».
- (?) Дірки: в інтервʼю — «іноді в центрі»; чи бувають інші форми поля — не бачив.
- (?) Реальний вигляд вікон — сторінка віддалась у стані «Loading puzzle», вікна узагальнено з меню й тексту правил.
