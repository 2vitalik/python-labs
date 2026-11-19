---
title: Spell Slide
slug: spell-slide
aka: []
family: word-number
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2025
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3330410/", best: true, note: "опис і 5 знімків: аватар штовхає літери, зелені / червоні слова, двері з картинками, діаманти, роботи, картинки-підказки; трейлер"}
  - {kind: other, url: "https://steamcommunity.com/app/3330410/discussions/0/689742961454416724/", note: "розробник розвʼязує 7.3: двері MOON, заклинити двері літерою, стрілки, MONOXIDE"}
  - {kind: other, url: "https://steamcommunity.com/app/3330410/discussions/0/689742961454418419/", note: "розробник розвʼязує 8.9: роботи, PI, ION, COGITATION"}
  - {kind: other, url: "https://steamcommunity.com/app/3330410/discussions/0/686366880770900940/", note: "редактор рівнів: стіни, роботи, діаманти, правило «не будувати неправильних слів», лабіринти"}
  - {kind: other, url: "https://steamcommunity.com/stats/3330410/achievements", note: "досягнення: три тварини в розвʼязку, слово з 11 літер, усі складні слова"}
  - {kind: other, url: "https://rawg.io/games/spell-slide", note: "опис Steam дослівно"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Spell+Slide+Lonely+Deckchair+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [move-4dir, keyboard-controls, controls-remap, push-object, word-validation, key-and-door, item-pickup, collect-all, cell-transform, undo-unlimited, save-progress, sequential-levels, level-select, in-game-editor, editor-palette, level-exchange, achievements-window, background-music, game-screen, main-menu, settings-window, +push-chain, +word-door, +word-color-validity, +hidden-challenge-word, +picture-clue, +progressive-clues, +letter-shift-cell, +robot-companion, +no-invalid-words-rule]
proposes: ["+cond:no_new_invalid_words", "+trigger:word_formed", "+window:word-lookup", "+ui:clue-image", "+ui:world-progress-mark"]
author: opus
date: 2026-11-19
---

# Spell Slide — Sokoban з літерами: кругляш штовхає букви по сітці, ряди й стовпці мають скластися в слова

## Суть
Покрокова головоломка Lonely Deckchair (автор Push Blox): аватар-кругляш ходить сіткою й штовхає плитки-літери, як ящики в Sokoban. Кожен горизонтальний і вертикальний ряд літер гра читає як слово: правильне світиться зеленим, неправильне — червоним. Рівні змінюють мету: зібрати слова з розкиданих літер, відкрити двері, на яких намальована річ (скласти її назву поруч), зібрати діаманти в лабіринті, задіяти роботів; у кожному рівні ще сховано «складне слово» за картинкою збоку від поля. Основне випробування — словникове, штовхання ускладнюється поступово.

## Поле і час
- Квадратна сітка з коричневими стінами-перегородками (знімки: від ≈9×9 до ≈16×10); вигляд згори, усе поле видно.
- Хід = крок аватара; гра памʼятає до двох швидких натискань під час анімації.
- Світи пронумеровані (рівні 3-2 «Anagram junction», 4.2 «Twisted», 6.8 «All the Suits», 7.3, 8.9, 8-2 «Need a Nudge») — щонайменше 8 світів + розділ «User Created».
- Часу нема.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Аватар (чорний кругляш) | player | — | рух 4 напрямки, штовхає літери, «зʼїдає» діаманти й числа |
| Плитка-літера | object | літера | штовхається; ряд літер підряд штовхається разом (?) |
| Слово на полі | mark | ряд / стовпець літер | зелене — є в словнику, червоне — нема |
| Стіна | static | — | непрохідна для аватара й літер |
| Двері з картинкою | gate | слово-ключ (басейн → SWIM, мотузка → COIL, молоток → MALLET) | відкриті, поки поруч складено слово; зламав слово — закриваються, якщо не заклинити літерою |
| Двері-підказка «?» | gate | дія, задана автором рівня | відкриваються після певної дії (?) |
| Діамант | pickup | — | зʼїсти; у рівнях-лабіринтах зібрати всі |
| Робот | ally | число на корпусі (0) | напарник у «стратегічних» рівнях; поведінка (?) |
| Число на підлозі (1, 2) | pickup | значення | «зʼїсти 2 й піти двічі вгору» (8.9); дія (?) |
| Клітина-стрілка | terrain | напрям | літера, проштовхнута через неї, змінюється на сусідню в абетці (?) |
| Картинка-підказка збоку | mark | зображення (вітрильник → SLOOP) | вказує «складне слово» рівня |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(player, dir)`.
- КОЛИ `contact(player, letter)` → ЯКЩО `free(клітина за рядом літер)` → ТО `push` ряду (?); інакше `block`.
- КОЛИ `after(push)` → ЯКЩО `in_dictionary(кожен ряд / стовпець з ≥ 2 літер)` → ТО `paint(run, green)`; інакше `paint(run, red)`.
- КОЛИ `custom: «поруч із дверима складено слово з їхньої картинки»` → ТО `set_state(door, open)`.
- КОЛИ `custom: «слово біля дверей зламано»` → ЯКЩО `not occupied(дверна клітина, letter)` → ТО `set_state(door, closed)`.
- КОЛИ `contact(player, diamond)` → ТО `pickup`.
- КОЛИ `all_gone(diamond)` → ТО `win` (?) — за тредами останній діамант завершує рівень.
- КОЛИ `custom: «усі літери стоять у правильних словах»` → ТО `win` (?) (досягнення кажуть про «winning solution»).
- КОЛИ `custom: «на полі складено складне слово рівня»` → ТО `custom: «слово зараховано»`; усі знайдено у світі → `custom: «лупа на виборі світу зелена»`.
- КОЛИ `custom: «літера пройшла клітину-стрілку»` → ТО `transform(letter, наступна | попередня літера)` (?).
- КОЛИ `input(dir)` → ЯКЩО `mode(no-new-wrong-words)` і `custom: «хід збільшує кількість неправильних слів»` → ТО `block` (правило рівнів-лабіринтів).
- КОЛИ `input(undo)` → ТО `undo(1)`; історія undo зберігається разом зі станом рівня.
- Перемога: умова рівня (слова / двері / діаманти) (?) · Поразка: нема, лише undo · Рахунок: нема; складні слова й досягнення (три тварини в розвʼязку, слово з 11 літер).

## Керування і ввід
- Стрілки — крок аватара; undo; клавіші перепризначаються.
- Лампочка вгорі праворуч — поступові підказки до складного слова; шестерня — налаштування.
- Повний екран або вікно довільного розміру.

## Вікна, меню, HUD
- `main-menu`: Play → вибір світу → рівень; Info → Credits і словник; налаштування; після всіх світів — «User Created».
- `level-select` (World Select): назва й номер світу; лупа червона / зелена — чи знайдено всі складні слова світу.
- `game-screen`: поле, назва рівня під полем («Patch and prime», «Thread level: critical», «Sanctify»), картинки-підказки по боках, шестерня, лампочка підказок.
- `custom-window`: вбудований словник із визначеннями.
- `editor-window`: стіни, роботи, діаманти, двері зі словом-замком, блоки інкремент / декремент, правило «не збільшувати неправильних слів»; рівень шлють поштою розробнику.
- `settings-window`: клавіші, вікно / повний екран.

## Фічі поза полем
- `levels-sequential` у світах, `hint` (поступові клуї), `undo` з памʼяттю на рівень, `autosave` стану кожного рівня.
- `level-editor` + `level-sharing` (поштою) + `user-levels-browser` («User Created»; «mirror world» з рівнями гравців — у планах).
- `achievements` (6): Three animals, Eleven letter word, Won Spell Slide, All challenging words, As below (рівень 6.8), Wordsmith (надіслати рівень).
- Оригінальний гітарний саундтрек; `remap-controls`; `window-size` / `fullscreen`.
- Рекомендована англійська — вільна або середня зі словником і підказками.

## Варіації й родичі
- Корпус: Bananagrams (`bananagrams.md` — кросворд з власних літер), Overwords (`overwords.md`), Wormspell (`wormspell.md` — аватар вписує слова в поле), Knotwords (`knotwords.md`); з `push-slide` — Sokoban і Push Blox того ж автора; Baba Is You (`thinky`) — слова-правила, які штовхають.
- **Осі варіацій:** що читається як слово (будь-який ряд / лише позначені клітини) · що дає слово (колір / двері / перемога) · хто рухає літери (аватар-штовхач / курсор / ковзання рядів) · обмеження ходу (вільно / «не збільшувати неправильних слів»).

## Цікавинки для курсу
- Після кожного кроку перечитати всі ряди й стовпці літер і пофарбувати слова — 🌱.
- Штовхання ряду літер (ланцюг Sokoban) — 📎.
- Двері, відкриті, поки існує слово (стан дверей = предикат поля), і заклинювання літерою — 🥉.
- Правило «хід не може збільшити кількість неправильних слів» як фільтр легальних ходів — 📎.
- Клітини-стрілки, що зсувають літеру абеткою — 🌱.
- Редактор із палітрою (стіни, роботи, діаманти, двері) і відправкою рівня — 🥈.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` + `controls-remap` · `push-object` · `word-validation` ↔ зелені / червоні ряди · `key-and-door` ↔ двері зі словом-ключем · `item-pickup` + `collect-all` ↔ діаманти · `cell-transform` ↔ стрілки-інкремент · `undo-unlimited` + `save-progress` · `sequential-levels` + `level-select` · `in-game-editor` + `editor-palette` + `level-exchange` · `achievements-window` · `background-music` · `game-screen` · `main-menu` · `settings-window`.
- **Нема** → пропозиції карток:
  - `+push-chain` (є в корпусі) — штовхання ряду літер.
  - `+word-door` «Двері відкриті, поки поруч складено слово» · entities/interact · 📎 · слоти {word, jam: bool}.
  - `+word-color-validity` «Ряди літер фарбуються: слово / не слово» · interface/hud · 🌱.
  - `+hidden-challenge-word` «Приховане слово рівня за картинкою» · levels/bank · 🌱.
  - `+picture-clue` «Картинка як підказка слова» · interface/hud · 🌱.
  - `+progressive-clues` «Поступові підказки до слова» · levels/solvability · 🌱.
  - `+letter-shift-cell` «Клітина зсуває літеру абеткою» · entities/interact · 🌱.
  - `+robot-companion` «Напарник-робот у рівні» · entities/move · 📎 (?).
  - `+no-invalid-words-rule` «Хід не може збільшити кількість неправильних слів» · entities/legality · 📎.

## Пропозиції до словників
- `+cond:no_new_invalid_words` — хід не збільшує кількість неправильних рядів.
- `+trigger:word_formed` — на полі склалося слово (двері, складне слово).
- `+window:word-lookup` — вбудований словник із визначеннями.
- `+ui:clue-image` — картинка-підказка біля поля.
- `+ui:world-progress-mark` — лупа «усі складні слова світу знайдено».

## Джерела
- ⭐ [Steam: Spell Slide](https://store.steampowered.com/app/3330410/) — опис, теги (Sokoban, Grid-Based Movement), 5 знімків (зелені / червоні слова, двері з картинками, діаманти, роботи, числа, картинки-підказки), трейлер; новини Steam (редактор: стіни, роботи, діаманти, двері, інкремент / декремент, правило неправильних слів; лупа на виборі світу; undo; заміна складного слова «Sloop» у 3-2).
- [Steam: розвʼязок 7.3](https://steamcommunity.com/app/3330410/discussions/0/689742961454416724/) — двері MOON, заклинювання, стрілки, MONOXIDE.
- [Steam: розвʼязок 8.9](https://steamcommunity.com/app/3330410/discussions/0/689742961454418419/) — роботи, PI, ION, COGITATION.
- [Steam: редактор](https://steamcommunity.com/app/3330410/discussions/0/686366880770900940/) — можливості редактора й правило «не будувати неправильних слів».
- [Steam: досягнення](https://steamcommunity.com/stats/3330410/achievements) — 6 досягнень.
- [RAWG](https://rawg.io/games/spell-slide) — опис Steam.
- YouTube: пошук «Spell Slide Lonely Deckchair gameplay».

## Непевне
- (?) Умова завершення рівня: «усі літери в правильних словах» чи «зібрані всі діаманти» — схоже, залежить від світу; з тредів: останній діамант завершує рівень.
- (?) Чи штовхається ряд літер разом (у тредах «push PEAT right one», «push OAT up once» — схоже на так).
- (?) Роботи: як рухаються, що означає число на них, навіщо «ставити робота під слово» (8.9).
- (?) Числа на підлозі («зʼїсти 2 й піти двічі вгору») і клітини-стрілки — лише з тредів і редактора.
- (?) Чи поодинока літера вважається «неправильним словом» (на знімках поодинокі літери червоні).
- (?) Кількість світів і рівнів (згадано рівні до 8.9 і світ «lettershifts»).
- (?) Thinky Games (сторінка не відкрилась, 403), за пошуком: «абстрактний Sokoban про штовхання літер, щоб складати й ламати слова».
