---
title: Pool Letter
slug: pool-letter
aka: []
family: word-number
also: []
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: state
year: 2025
platforms: [web]
links:
  - {kind: itch, url: "https://cisuthen.itch.io/pool-letter", best: true, note: "грати в браузері; опис, керування, підказка «чи є ще слова», словник SOWPODS"}
  - {kind: other, url: "https://cisuthen.itch.io/pool-letter/devlog/1137008/about-custom-levels", note: "формат коду власного рівня: розмір, старт, ціль, літери"}
  - {kind: other, url: "https://cisuthen.itch.io/pool-letter/devlog/1136978/hints-and-achievements-for-pool-letter", note: "7 досягнень з розвʼязками-ланцюжками (спойлери)"}
  - {kind: other, url: "https://cisuthen.itch.io/pool-letter/devlog/1143707/update", note: "V3: звуки й підказка; V4: виправлено сейв у збірці"}
  - {kind: other, url: "https://confoundingcalendar.itch.io/", note: "Confounding Calendar 2025 — адвент-календар міні-пазлів, гра в «2025 Week 4+»"}
  - {kind: other, url: "https://github.com/kamilmielnik/scrabble-dictionaries", note: "репозиторій словника SOWPODS, яким гра перевіряє слова"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Pool+Letter+word+maze", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [word-validation, path-drawing, cell-click, keyboard-controls, move-4dir, impassable-cells, reach-exit, undo-redo, restart-level, state-string, level-exchange, achievements-window, sound-effects, game-screen, +path-trace-word, +word-chain-overlap, +unsolvable-warning, +multiple-endings, +optional-challenges, +loop-detection]
proposes: ["+cond:word_chain", "+cond:words_possible"]
author: opus
date: 2026-11-19
---

# Pool Letter — лабіринт із літер: ланцюжком слів, де кожне починається там, де скінчилось попереднє, дійди до помаранчевої цілі

## Суть
Безкоштовна браузерна міні-головоломка з адвент-календаря Confounding Calendar 2025. Поле — лабіринт клітин-літер з порожнинами; зі старту гравець веде слово по сусідніх літерах, а наступне слово починається на тій клітині, де закінчилось попереднє. Мета — довести ланцюжок до помаранчевої цілі; кожне слово перевіряється словником SOWPODS.

Основний рівень один і великий (за автором, у ньому є всі літери абетки), але кінцівок кілька — за тим, яке слово останнє. Є власні рівні з рядка-коду, підказка «чи лишились слова звідси» і 7 досягнень-викликів. Натхнення — NYT Strands та інші словесні ігри.

## Поле і час
- Прямокутна сітка W×H; клітина — літера або порожньо («-» у коді), порожні клітини — стіни лабіринту.
- Дві особливі клітини — старт і ціль (координати в коді рівня); ціль помаранчева.
- Часу нема; хід = одне підтверджене слово. Стан гри — поточна позиція (кінець останнього слова) і ланцюжок слів.
- Палітра з 4 кольорів (Lospec «Calm and Chloric»); на itch позначено високу контрастність.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітина-літера | tile | символ A–Z | крок шляху слова; одну клітину можна пройти в різних словах |
| Порожня клітина | static | «-» у коді рівня | непрохідна, задає стіни |
| Старт | terrain | (стовпець, рядок) | перша поточна позиція |
| Ціль | terrain | (стовпець, рядок), помаранчева | слово, що на ній закінчилось, виграє рівень |
| Поточна позиція | player | клітина | кінець останнього слова; звідси починається наступне |
| Слово | zone | шлях сусідніх клітин | перша літера — поточна позиція; додається до ланцюжка |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «поточна позиція = старт»`.
- КОЛИ `input(drag | tap letter)` → ЯКЩО `custom: «шлях починається в поточній позиції, кожна наступна клітина — сусідня літера»` → ТО `mark(cells, selected)`; інакше `block` (порожня клітина непрохідна).
- КОЛИ `input(confirm)` → ЯКЩО `in_dictionary(word)` (SOWPODS) → ТО `custom: «слово додано до ланцюжка; поточна позиція = остання клітина слова»`, `counter(words, +1)`.
- КОЛИ `input(confirm)` → ЯКЩО `not in_dictionary(word)` → ТО `block` (?).
- КОЛИ `reach(position, goal)` → ТО `win`; літери на полі вібрують.
- КОЛИ `input(undo)` → ТО `undo(1)` — зняти останнє слово (?).
- КОЛИ `input(reset)` → ТО `restart`.
- КОЛИ `input(hint)` → ЯКЩО `custom: «з поточної позиції ще можна скласти хоч одне слово»` → ТО `message(«слова є»)`; інакше `message(«слів нема»)` у рядку стану — глухий кут, треба undo.
- КОЛИ `level_end` → ЯКЩО `custom: «останнє слово — MYTHIC / RELIC / ERIC»` → ТО `unlock(Ending A / Ending B / Secret Ending)`.
- КОЛИ `level_end` → ЯКЩО `counter(words, <=, 8)` → ТО `unlock(Win with ≤8 Words)`.
- КОЛИ `level_end` → ЯКЩО `counter(words, >=, 14)` and `not custom: «у ланцюжку була петля»` → ТО `unlock(Win ≥14 Words no Loop)`.
- КОЛИ `pattern(loop_closed)` → ТО `unlock(Find a Loop)`; петля — `custom: «слово закінчилось на клітині, з якої починалось якесь слово»`.
- КОЛИ `input(confirm)` → ЯКЩО `custom: «у слові є J»` → ТО `unlock(Use the Letter J)`.
- КОЛИ `input(custom level, code)` → ТО `custom: «розібрати "W,H,старт_x,старт_y,ціль_x,ціль_y;літери в порядку читання", "-" — порожньо»`, `restart`.
- КОЛИ `input(M)` → ТО `custom: «повернути основний рівень»`.
- Перемога: ланцюжок дійшов до цілі · Поразки нема (глухий кут → undo чи reset) · Рахунку нема: кількість слів і останнє слово важать лише для досягнень.

## Керування і ввід
- Миша чи тач: тягнути по літерах або тапати по одній і тапнути останню вдруге — підтвердження.
- Клавіатура: WASD / IJKL / стрілки — крок виділення на сусідню клітину; X / E / O / Space — підтвердити слово; Z / Q / U — undo; R — reset; H — підказка; F — повний екран; M — досягнення або повернення рівня; P — власний рівень.
- Скинути прогрес — кнопка або двічі T на екрані досягнень.

## Вікна, меню, HUD
- `game-screen`: лабіринт, виділений шлях, помаранчева ціль; угорі кнопки (власний рівень, досягнення, повний екран), унизу — undo і підказка; `hint-text` — рядок стану з відповіддю підказки.
- `achievements-window`: 7 досягнень; звідти ж повернення основного рівня і скидання прогресу.
- `level-password`-подібне вікно: введення коду власного рівня (P).
- Перемога — без окремого вікна (?): літери вібрують.
- Переходи: game-screen ↔ achievements-window (M); game-screen → ввід коду (P) → game-screen власного рівня.

## Фічі поза полем
- `share-code`: власний рівень — рядок-код; гравці діляться рівнями в коментарях itch (від «колонки» 1×25 до 14×8).
- `achievements` як виклики й кінцівки; `undo`, `restart-level`, `hint` («чи є слова звідси»).
- `fullscreen`, `high-contrast`; прості звуки (V3); прогрес досягнень зберігається між сесіями.
- Словник — SOWPODS з відкритого репозиторію; мова — англійська.

## Варіації й родичі
- NYT Strands (див. [nyt-connections.md](nyt-connections.md)) — натхнення: слова-шляхи в сітці літер.
- Boggle ([boggle.md](boggle.md)), Squaredle ([squaredle.md](squaredle.md)) — слово шляхом по сусідніх клітинах, але без ланцюжка й цілі.
- Spiral puzzle ([spiral-puzzle.md](spiral-puzzle.md)) — «остання літера = перша наступного» на папері; Weaver ([weaver.md](weaver.md)) — ланцюжок слів до цільового слова.
- **Осі варіацій:** звʼязок слів (спільна клітина / спільна літера / без звʼязку) · мета (дійти до цілі / покрити все поле / знайти список) · повтор клітин (між словами дозволено / заборонено) · поле (лабіринт з порожнинами / суцільне).

## Цікавинки для курсу
- Розвʼязувач: граф «клітина → клітини, куди веде слово зі словника», BFS до цілі дає найкоротший ланцюжок — 🥈.
- Підказка «чи є слова звідси»: DFS по сусідах з обрізанням за префіксами trie, вихід на першому слові — 🥉.
- Код рівня «W,H,x,y,x,y;літери»: парсер, валідація, експорт — 🌱.
- Досягнення як предикати над історією ланцюжка (останнє слово, кількість слів, петлі, літера J) — 📎.
- Undo слова з поверненням поточної позиції — 🌱.

## Мапа на каталог
- Є: `word-validation` ↔ SOWPODS · `path-drawing` ↔ drag по літерах · `cell-click` ↔ тап-тап-підтвердження · `keyboard-controls` + `move-4dir` ↔ WASD / IJKL / стрілки · `impassable-cells` ↔ «-» · `reach-exit` ↔ помаранчева ціль · `undo-redo` ↔ undo слова · `restart-level` ↔ R · `state-string` ↔ код рівня · `level-exchange` ↔ коди в коментарях · `achievements-window` · `sound-effects` (V3) · `game-screen`.
- **Нема** → пропозиції карток:
  - `+path-trace-word` (корпус) — слово шляхом по сусідніх клітинах.
  - `+word-chain-overlap` (корпус, Spiral puzzle) «Остання літера = перша наступного» · game-logic/constraints · 🌱 — тут спільна клітина, а не лише літера.
  - `+unsolvable-warning` (корпус, Shisen-Sho) «Попередити, що далі ходу нема» · levels/solvability · 🥉 — тут на запит і лише «чи є хоч одне слово звідси».
  - `+multiple-endings` (корпус) «Кінцівка за останнім словом» · levels/progression · 🌱.
  - `+optional-challenges` (корпус) «Досягнення-виклики: ≤8 слів, ≥14 без петель, слово з J» · game-logic/score · 📎.
  - `+loop-detection` (корпус) «Петля: слово закінчилось на клітині старту іншого слова» · game-logic/constraints · 📎.

## Пропозиції до словників
- `+cond:word_chain` — слово починається на клітині, де закінчилось попереднє (Pool Letter; Spiral puzzle — на тій самій літері).
- `+cond:words_possible` — з клітини ще можна скласти хоч одне слово словника (підказка Pool Letter; попередження Shisen-Sho).

## Джерела
- ⭐ [itch.io: Pool Letter](https://cisuthen.itch.io/pool-letter) — опис «Connect Letters Through Word Maze», керування, підказка, SOWPODS, натхнення Strands, коди рівнів і розвʼязки гравців у коментарях.
- [Devlog: About Custom Levels](https://cisuthen.itch.io/pool-letter/devlog/1137008/about-custom-levels) — формат коду з прикладом «5,3,3,1,5,3;DEPOO-LTEL-ETEL».
- [Devlog: Hints and Achievements](https://cisuthen.itch.io/pool-letter/devlog/1136978/hints-and-achievements-for-pool-letter) — 7 досягнень, розвʼязки-ланцюжки (CONCLUSION-NEARBY-…), «усі літери абетки тут».
- [Devlog: Update](https://cisuthen.itch.io/pool-letter/devlog/1143707/update) — V3 (звуки, підказка, вібрація після перемоги), V4.
- [Confounding Calendar](https://confoundingcalendar.itch.io/) — календар 2025, гра в колекції «Week 4+».
- YouTube: пошук «Pool Letter word maze».

## Непевне
- (?) Діагоналі: клавіші дають 4 напрямки, відомі розвʼязки гравців ортогональні; чи drag дозволяє діагональ — не перевірено.
- (?) Повтор клітини в одному слові: досягнення «Find a Loop» з розвʼязком CORKED-DICED натякає, що слово може замкнутись на своєму старті.
- (?) Мінімальна довжина слова: у всіх відомих розвʼязках — від 4 літер.
- (?) Як гра відповідає на невалідне слово і яка глибина undo.
- (?) Чи ціль треба саме закінчити словом, чи досить пройти крізь неї — усі кінцівки (MYTHIC, RELIC, ERIC) закінчуються на ній.
- (?) Дата: devlog-и від 08.12.2025, а на сторінці календаря гра — у «2025 Week 4+».
