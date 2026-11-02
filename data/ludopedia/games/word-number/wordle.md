---
title: Wordle
slug: wordle
family: word-number
also: [hidden-deduction]
klass: puzzle
axes:
  field: square
  time: turn
  opponent: none
  info: hidden
  random: setup
  goal: state
year: 2021
platforms: [web, mobile (NYT Games app)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Wordle", best: true, note: "правила, дублікати літер, hard mode, high contrast, share-сітка, історія, варіанти"}
  - {kind: play, url: "https://www.nytimes.com/games/wordle/index.html", note: "офіційна гра NYT; fetch-ем не перевірено (NYT блокує)"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Quordle", note: "4 поля разом, 9 спроб"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Absurdle", note: "адверсаріальний варіант (qntm)"}
  - {kind: official, url: "https://fubargames.se/squardle/", note: "Squardle — правила 2D-фідбеку"}
  - {kind: other, url: "https://www.gamedeveloper.com/design/the-world-of-i-wordle-i-variants", note: "огляд варіантів (Absurdle, Quordle, Worldle)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=wordle+gameplay+hard+mode", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [daily-puzzle, keyboard-controls, cell-click, completion-detection, profile-stats, end-screen, game-screen, help-window, settings-window, theme-select, save-progress, event-effects, +letter-feedback, +word-validation, +hard-mode, +keyboard-state, +share-result, +streak-stats, +adversarial-answer, +multi-board, +grid-word-feedback]
proposes: ["+trigger:input", "+cond:in_dictionary", "+cond:consistent_with_hints", "+effect:feedback", "+effect:paint", "+effect:message", "+effect:shake", "+role:tile", "+ui:on-screen-keyboard", "+ui:guess-distribution", "+ui:share-button", "+ui:next-puzzle-countdown", "+window:stats-window", "+feature:hard-mode", "+feature:share-result", "+feature:streaks", "+axis:session"]
author: opus
date: 2026-11-02
---

# Wordle — вгадай 5-літерне слово дня за 6 спроб, читаючи кольори літер

## Суть
Гравець вводить 5-літерні слова; кожна спроба розфарбовується: зелений — літера на своєму місці, жовтий — є в слові, але не тут, сірий — нема. За 6 спроб треба вийти на загадане слово, одне на день для всіх у світі. Ядро — Mastermind/Jotto над словником: фідбек по позиціях + обмеження «спроба мусить бути справжнім словом». Незвичне — соціальна обгортка: серії днів і емодзі-сітка для поширення без спойлера.

## Поле і час
- Поле 6×5: рядок = спроба, клітина = літера. Під полем — екранна клавіатура QWERTY, що теж є «полем стану» (кольори літер).
- Хід = введення й підтвердження одного слова; часу нема. Анімація: плитки перевертаються по черзі зліва направо, відкриваючи колір.
- Сесія = одна щоденна задача (seed — дата); нова о локальній півночі. Повторно зіграти той самий день не можна (архів — лише окремі варіанти/клони).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Загадане слово | static (приховане) | 5 літер, зі списку відповідей (~2 309) | фіксоване на день; не відображається до кінця |
| Рядок спроби | zone | 5 клітин, індекс 1–6 | активний — поки не підтверджено; далі заморожений |
| Плитка-літера | tile | літера, стан empty/typed/green/yellow/grey | стан визначається при підтвердженні рядка |
| Клавіша клавіатури | tile (UI) | літера, найкращий відомий стан | фарбується за пріоритетом green > yellow > grey |
| Словник допустимих спроб | static | ширший за список відповідей (?) | спроба поза ним відхиляється |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(letter)` → ЯКЩО `count(typed, <, 5)` → ТО `custom: «літера в наступну клітину активного рядка»`.
- КОЛИ `input(backspace)` → ТО `custom: «стерти останню введену літеру»`.
- КОЛИ `input(enter)` → ЯКЩО `count(typed, <, 5)` → ТО `message("Not enough letters")`, `shake`.
- КОЛИ `input(enter)` → ЯКЩО `not in_dictionary(guess)` → ТО `message("Not in word list")`, `shake`; спроба не витрачається.
- КОЛИ `input(enter)` → ЯКЩО `mode(hard) and not consistent_with_hints(guess)` → ТО `message("2nd letter must be E" | "Guess must contain O")`, `shake`.
- КОЛИ `input(enter)` → ЯКЩО слово валідне → ТО `feedback(guess)`: прохід 1 — `paint(i, green)` для кожного `guess[i] == answer[i]`; прохід 2 — для решти позицій зліва направо `paint(i, yellow)`, якщо в answer лишились невикористані копії цієї літери, інакше `paint(i, grey)`.
- Дублікати: повторена літера отримує green/yellow не більше разів, ніж вона є у відповіді; зайві копії — grey (приклад з вікі: дві «O» у ROBOT).
- КОЛИ `after(feedback)` → ТО `paint(key[letter], max(state))` для кожної літери спроби — клавіша ніколи не «деградує» з green у yellow.
- КОЛИ `pattern(row all green)` → ТО `win`, `message(Genius|Magnificent|Impressive|Splendid|Great|Phew за номером спроби)`, `animate(bounce)`, `window(stats-window)`.
- КОЛИ `counter(guesses, ==, 6)` → ЯКЩО не вгадано → ТО `lose`, `message(answer)`, `window(stats-window)`.
- Hard mode: кожна наступна спроба мусить містити всі відкриті підказки — green-літери на тих самих позиціях, yellow-літери будь-де в слові. Сірі літери повторно вживати дозволено (обмеження лише позитивне).
- Hard mode вмикається лише до першої спроби дня (?); вимкнути можна будь-коли.
- Перемога: рядок з 5 зелених до 6-ї спроби включно · Поразка: 6 спроб без вгадування · Рахунок: номер спроби (1–6) або X; агреговано — розподіл і серія.
- КОЛИ `game_over` → ТО `counter(streak, +1)` при перемозі, інакше `counter(streak, =0)`; пропущений день теж обнуляє серію.

## Керування і ввід
- Фізична клавіатура: літери, Backspace, Enter. Або тап по екранній клавіатурі (ENTER і ⌫ — окремі широкі клавіші).
- Опція «Onscreen Keyboard Input Only» (?) — ігнорувати фізичну клавіатуру (для мобільних).
- Курсора по клітинах нема: введення завжди в наступну вільну клітину активного рядка.

## Вікна, меню, HUD
- `game-screen`: заголовок, кнопки-іконки (довідка, статистика, налаштування), поле 6×5, `on-screen-keyboard` зі станами літер, `toast` для повідомлень («Not in word list»).
- `help-window` («How To Play»): правила + три приклади слів з по одній кольоровій плитці; показується автоматично при першому вході.
- `stats-window`: Played · Win % · Current Streak · Max Streak · `guess-distribution` (гістограма 1–6, сьогоднішній стовпчик підсвічено) · `next-puzzle-countdown` (до наступного Wordle) · `share-button`.
- `settings-window`: Hard Mode · Dark Theme · High Contrast Mode (green/yellow → orange/blue) · Onscreen Keyboard Input Only (?) · лінки на фідбек.
- `end-screen` фактично = `stats-window`, що відкривається після кінця гри; на поразці — тост із відповіддю.
- Переходи: перший вхід → `help-window` → `game-screen`; кінець гри → `stats-window`; повторний вхід того ж дня → `game-screen` у фінальному стані + `stats-window`.
- NYT-версія додала WordleBot (окремий екран аналізу: «luck» і «skill» на кожну спробу) — `custom-window`.

## Фічі поза полем
- `mode-daily` / `daily-puzzle`: одна задача на день, однакова для всіх; номер дня входить у share-текст.
- `share-result`: копіювання в буфер тексту «Wordle 196 4/6» + рядки емодзі 🟩🟨⬛ (⬜ у світлій темі) — патерн кольорів без літер.
- `stats` + `streaks`: серія днів; у NYT-версії статистика привʼязана до акаунта (`cloud-save`), до міграції — localStorage (частина гравців втратила серії при переїзді на сайт NYT у лютому 2022).
- `autosave`: стан поточного дня зберігається — перезавантаження не скидає спроби.
- `colorblind-palette` (High Contrast), `theme-select` (Dark Theme), `hard-mode` як опційне правило.
- `hint`, `undo`, `archive` в оригіналі нема.

## Варіації й родичі
- Предки: Mastermind (кольоровий фідбек по позиціях), Jotto (лише кількість спільних літер), телешоу Lingo.
- **Quordle** (2022, Freddie Meyer; з 2023 — Merriam-Webster): 4 поля одночасно, 9 спроб; одна введена спроба застосовується до всіх незакритих полів. **Octordle** — 8 полів, 13 спроб (?); є режими Sequence (поля відкриваються по черзі) і Rescue (стартові спроби вже дано) (?).
- **Absurdle** (2022, qntm): загаданого слова нема — після кожної спроби гра розбиває множину кандидатів за патерном відповіді й обирає той патерн, що найменше скорочує множину. Перемога — коли лишилось одне слово і ти його ввів; рахунок = кількість спроб, ліміту нема.
- **Squardle** (fubargames): 6 слів хрестом на сітці 5×5 з 4 дірками; спроба лягає одночасно в рядок і стовпець (позицію обирає гра, стрілками показано наступну); 10 спроб + 1 бонус за кожне з перших 5 розвʼязаних слів. Кольори: green — тут; yellow — в цьому рядку (не стовпці); red — в цьому стовпці (не рядку); orange — і там, і там; white — деінде на полі; black — нема ніде; стрілки — мінімальна кількість копій.
- Інші: Nerdle (рівняння замість слів), Worldle/Globle (країни, фідбек відстанню й напрямком), Semantle (семантична близькість), Heardle (музика), Termo (португальська).
- **Осі варіацій:** кількість полів (1 / 4 / 8 / 2D-хрест) · хто загадує (фіксоване слово / адверсарій) · вид фідбеку (позиційний / лише кількість / відстань-напрямок / семантичний) · алфавіт (літери / цифри й операції / країни) · обмеження спроб (лише словник / hard mode / рівняння мусить бути істинним).

## Цікавинки для курсу
- Фідбек із дублікатами (два проходи: спочатку green, потім yellow з лічильником залишку) — 🥉: класична пастка, наївна версія фарбує зайві копії.
- Hard mode як валідатор спроби проти всієї історії підказок — 📎: збирання обмежень і перевірка з людським повідомленням.
- Клавіатура зі станами (максимум за пріоритетом) — 🌱: похідний стан від історії спроб.
- Share-сітка емодзі + серії й гістограма спроб — 📎: статистика між сесіями й «спойлер-вільний» експорт.
- Absurdle: адверсарій, що групує ~2 300 кандидатів у ≤243 патерни і вибирає найбільшу групу — 🥈: чистий алгоритм над словником.
- Розвʼязувач/«WordleBot»: вибір спроби з максимальною ентропією (очікуване зменшення множини) — 🥇.
- Squardle: фідбек одночасно по рядку й стовпцю з 6 кольорами — 🥈 (2D-узагальнення правила дублікатів).

## Мапа на каталог
- Є: `daily-puzzle` ↔ слово дня · `keyboard-controls` ↔ введення літер · `cell-click` ↔ тап по екранній клавіатурі · `completion-detection` ↔ рядок з 5 зелених · `profile-stats` ↔ статистика · `save-progress` ↔ серії між днями · `end-screen` · `game-screen` · `help-window` · `settings-window` · `theme-select` ↔ темна тема · `event-effects` ↔ перевертання плиток, «трясіння» рядка.
- **Нема** → пропозиції карток:
  - `+letter-feedback` «Позиційний кольоровий фідбек спроби» · game-logic/constraints · 🥉 · слоти {duplicates: count-limited|naive} — Wordle, Mastermind.
  - `+word-validation` «Перевірка слова за словником» · game-logic/constraints · 🌱 · слоти {list: file} — Wordle, Scrabble, Letterpress.
  - `+hard-mode` «Hard mode: спроба мусить враховувати підказки» · game-logic/difficulty · 📎.
  - `+keyboard-state` «Клавіатура зі станами літер» · interface/hud · 🌱.
  - `+share-result` «Поширення результату емодзі-сіткою» · interface/results · 🌱.
  - `+streak-stats` «Серії днів і розподіл результатів» · interface/results · 📎 (дитина `profile-stats`).
  - `+adversarial-answer` «Адверсарне загадування (Absurdle)» · game-logic/opponent · 🥈.
  - `+multi-board` «Одна спроба — кілька полів одночасно (Quordle)» · game-logic/constraints · 📎 · слоти {boards: int, guesses: int}.
  - `+grid-word-feedback` «Фідбек по рядку й стовпцю (Squardle)» · game-logic/constraints · 🥈.

## Пропозиції до словників
- `+trigger:input` — введення літери / Enter / Backspace як окремі дії.
- `+cond:in_dictionary` — слово є у списку допустимих (Wordle, Scrabble, Letterpress, Strands).
- `+cond:consistent_with_hints` — спроба не суперечить відкритим підказкам (hard mode).
- `+effect:feedback` — обчислити й показати кольори спроби проти прихованої відповіді (Wordle, Mastermind, Squardle, Waffle).
- `+effect:paint`, `+effect:message`, `+effect:shake` — розфарбування плитки/клавіші, тост, трясіння рядка на помилці.
- `+role:tile` — плитка-літера зі станом.
- `+ui:on-screen-keyboard` — екранна клавіатура зі станами клавіш; `+ui:guess-distribution` — гістограма результатів; `+ui:share-button`; `+ui:next-puzzle-countdown` — таймер до наступної щоденної задачі.
- `+window:stats-window` — статистика з серіями (⏳ у словнику, тут — головне вікно кінця гри).
- `+feature:hard-mode` — опційне посилення правил; `+feature:share-result` — текстовий експорт результату без спойлера; `+feature:streaks`.
- `+axis:session` — тут `daily`: одна задача на день для всіх, повтору нема.

## Джерела
- ⭐ [Wikipedia: Wordle](https://en.wikipedia.org/wiki/Wordle) — правила, дублікати, hard mode, high contrast, share-сітка, WordleBot, список варіантів.
- [NYT Wordle](https://www.nytimes.com/games/wordle/index.html) — грати; вікна довідки, статистики, налаштувань (fetch заблоковано, описано з памʼяті).
- [Wikipedia: Quordle](https://en.wikipedia.org/wiki/Quordle) — 4 поля, 9 спроб, Merriam-Webster.
- [Wikipedia: Absurdle](https://en.wikipedia.org/wiki/Absurdle) — адверсарний алгоритм.
- [Squardle](https://fubargames.se/squardle/) — повні правила 2D-фідбеку, бонусні спроби, стрілки-кількості.
- [Game Developer: The World of Wordle Variants](https://www.gamedeveloper.com/design/the-world-of-i-wordle-i-variants) — огляд варіантів.
- YouTube: пошук «wordle gameplay hard mode».

## Непевне
- (?) Розмір списку допустимих спроб (~10 657 + 2 315 = 12 972 в оригіналі) — з памʼяті, вікі не дає.
- (?) Hard mode можна ввімкнути лише до першої спроби дня; точні тексти повідомлень hard mode — з памʼяті.
- (?) Пункт «Onscreen Keyboard Input Only» у налаштуваннях NYT — з памʼяті; NYT-сторінку не вдалося відкрити.
- (?) Octordle: 13 спроб, режими Sequence/Rescue — з памʼяті (сайт Merriam-Webster віддав порожню JS-сторінку).
- (?) Повідомлення перемоги Genius…Phew за номером спроби — з памʼяті.
