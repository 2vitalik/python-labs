---
title: Letterpress
slug: letterpress
family: word-number
also: [chess-abstract]
klass: cursor
axes:
  field: square
  time: turn
  opponent: online
  info: full
  random: setup
  goal: territory
year: 2012
platforms: [iOS, macOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Letterpress_(video_game)", best: true, note: "правила: 5×5, захоплення, заблоковані плитки, кінець гри, Game Center, freemium"}
  - {kind: other, url: "https://www.macrumors.com/2012/10/24/letterpress-combines-boggle-and-go-in-one-simple-word-game/", note: "MacRumors 2012: «Boggle + го», покупка $0.99"}
  - {kind: play, url: "https://play.google.com/store/search?q=letterpress%20word%20game&c=apps", note: "пошук Google Play (Solebon)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=letterpress+word+game+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [cell-click, turn-enforcement, ai-opponent, replay, theme-select, completion-detection, end-screen, game-screen, help-window, save-game, +word-validation, +claim-by-word, +defended-cells, +word-reuse-ban, +async-match-list]
proposes: ["+trigger:input", "+cond:in_dictionary", "+cond:not_played", "+cond:adjacent_count", "+effect:set_side", "+effect:pass_turn", "+role:tile", "+ui:word-tray", "+ui:score-bar", "+window:game-list", "+window:played-words", "+feature:async-multiplayer", "+axis:session"]
author: opus
date: 2026-11-02
---

# Letterpress — склади слово з будь-яких літер 5×5 і перефарбуй їх у свій колір; оточені — недоторкані

## Суть
Двоє гравців по черзі складають слова з 25 літер спільного поля 5×5 — літери можна брати будь-де, без суміжності (на відміну від Boggle). Усі використані плитки фарбуються в колір гравця, крім тих, що захищені суперником. Плитка, з усіх боків оточена плитками свого кольору, стає «захищеною» (темніший відтінок) і не перефарбовується. Ядро — Boggle + го: слово — це хід захоплення території, а захист — геометрія кольорів на полі.

## Поле і час
- Поле 5×5 випадкових літер; літери не змінюються всю гру — змінюється лише колір клітини (нейтральна / синя / червона, кожна — звичайна або захищена).
- Хід = одне слово або пас; асинхронно через Game Center (хід може чекати днями), або проти бота.
- Сусідство для захисту — 4 ортогональні сусіди в межах поля (кутова клітина має 2, крайова — 3) (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка-літера | tile | літера, власник none/A/B, defended | бере участь у слові будь-скільки разів за гру |
| Захищена плитка | tile (стан) | defended = true | не змінює власника, навіть якщо суперник використав її у слові |
| Гравець A / B | player | колір, рахунок = кількість плиток | хід по черзі |
| Зіграні слова | static | список | заборонено повторити слово або його префікс (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(tap tile)` → ТО `custom: «літера додається в кінець слова у лотку; плитка на полі позначена»`; повторний тап / drag з лотка — прибрати.
- КОЛИ `input(submit)` → ЯКЩО `not in_dictionary(word)` → ТО `message("Not a word")`, `block`.
- КОЛИ `input(submit)` → ЯКЩО `not not_played(word)` (слово вже зіграно або є префіксом зіграного) → ТО `message`, `block`.
- КОЛИ `input(submit)` → ЯКЩО слово валідне → ТО для кожної використаної плитки: ЯКЩО `not state(tile, defended_by_opponent)` → ТО `set_side(tile, me)`; потім перерахунок захисту всіх плиток, `end_turn`.
- Перерахунок захисту: КОЛИ `after(set_side)` → для кожної плитки ЯКЩО `adjacent_count(tile, same_owner, ==, all_neighbours)` → ТО `set_state(tile, defended)`; інакше `clear_state(tile, defended)` — захоплення сусідньої плитки знімає захист.
- Захищену плитку суперник може використовувати в слові (літера доступна), але очок і кольору вона йому не дає.
- КОЛИ `input(pass)` → ТО `pass_turn`; КОЛИ обидва гравці пасували підряд → ТО `game_over`.
- КОЛИ `count(neutral_tiles, ==, 0)` → ТО `game_over` (після ходу, що зафарбував останню нейтральну).
- Рахунок у будь-який момент = кількість плиток твого кольору (захищених і ні); хід може дати +9 тобі й −2 супернику (крадіжка).
- Перемога: більше плиток на кінець · Поразка: менше / резиґнація · Нічия: рівна кількість (?).
- Обмеження слова: за вікі — не можна повторювати слова й слова «тієї ж родини» (word family); на практиці — заборонено префікс уже зіграного слова (?).

## Керування і ввід
- Тап по плитках у будь-якому порядку → слово збирається в лотку над полем; плитки в лотку перетягуються для зміни порядку; свайп/тап — повернути назад (?).
- Кнопки: Submit, Clear (?), Pass, Resign.
- Порядок ходів: тільки свій хід; поле суперника видно, але неактивне.

## Вікна, меню, HUD
- `game-screen`: поле 5×5 з кольорами (світлий / темний відтінок = захищено), `word-tray` (слово, що складається), `score-bar` з аватарами й кількістю плиток, `turn-indicator`.
- `game-list`: список партій Game Center (твій хід / чекає суперника / завершені), «+» нова гра (випадковий суперник або друг).
- `replay-window`: покроковий перегляд партії (оновлення грудня 2012).
- `played-words`: список зіграних слів (преміум).
- `skin-select` / `theme-select`: кольорові теми (преміум).
- `end-screen`: фінальне поле, рахунок, перемога/поразка.
- `help-window`: короткі правила з анімованим прикладом захисту (?).
- Переходи: `game-list` → `game-screen` партії → після ходу назад у `game-list`; завершена партія → `end-screen` → Rematch (у ранніх версіях не було — критика).

## Фічі поза полем
- `async-multiplayer` через Game Center: матчмейкінг, push про хід; безкоштовно — до 2 партій одночасно, преміум — без ліміту.
- `ai-opponent-levels`: бот замість другого гравця (соло).
- `replay` партій, `theme-select`, `stats` (критика: бідна статистика Game Center).
- Нема чату й кнопки реваншу в оригіналі — гравці домовлялися через iMessage.

## Варіації й родичі
- Boggle (слова з сусідніх літер), го (оточення = захист), Reversi (перефарбування чужого).
- Клони й наслідувачі: Wordbase (2014: слова мусять бути шляхом від своєї бази, «доріжка» до протилежного краю, захоплення через бомби) (?).
- **Осі варіацій:** вибір літер (будь-які / лише суміжний шлях, як Boggle/Wordbase) · умова захисту (усі 4 сусіди / 8 сусідів / регіон) · кінець (поле зафарбоване / ліміт ходів / досягнення краю) · рахунок (плитки / довжина слів).

## Цікавинки для курсу
- Захист «усі ортогональні сусіди мого кольору» і перерахунок після кожного ходу — 🌱.
- Захоплення й крадіжка з урахуванням захисту + рахунок як кількість плиток — 📎.
- Заборона повтору слова й його префіксів (trie/startswith по зіграних) — 🌱.
- Генерація поля 5×5, з якого можна скласти достатньо слів (перевірка за словником, частоти літер) — 🥉.
- AI: перебір слів зі словника, що складаються з мультимножини 25 літер, оцінка ходу (захоплення + захист − вразливість) — 🥇.
- Асинхронні партії й список «чий хід» — 🥈 (стан партії як дані між сесіями).

## Мапа на каталог
- Є: `cell-click` ↔ тап по плитці · `turn-enforcement` · `ai-opponent` ↔ бот · `replay` · `theme-select` · `completion-detection` ↔ усе поле зафарбоване · `save-game` ↔ партії живуть між сесіями · `end-screen` · `game-screen` · `help-window`.
- **Нема** → пропозиції карток:
  - `+word-validation` — див. wordle.md.
  - `+claim-by-word` «Слово захоплює використані клітини» · game-logic/score · 📎.
  - `+defended-cells` «Захист клітини, оточеної своїми» · entities/legality · 🌱 · слоти {neighbours: 4|8}.
  - `+word-reuse-ban` «Заборона повтору слова/префікса» · game-logic/constraints · 🌱.
  - `+async-match-list` «Список асинхронних партій» · interface/menus · 🥈.

## Пропозиції до словників
- `+trigger:input` — тап по плитці, submit, pass.
- `+cond:in_dictionary`; `+cond:not_played` — слово (і його префікси) ще не зіграні; `+cond:adjacent_count` (⏳) — тут «усі сусіди мого кольору».
- `+effect:set_side` (⏳) — головний ефект: зміна власника плитки; `+effect:pass_turn`.
- `+role:tile`.
- `+ui:word-tray` — лоток слова, що складається; `+ui:score-bar` — смуга рахунку з аватарами.
- `+window:game-list` — паралельні асинхронні партії; `+window:played-words` — список зіграних слів.
- `+feature:async-multiplayer`.
- `+axis:session` — `match` асинхронна.

## Джерела
- ⭐ [Wikipedia: Letterpress (video game)](https://en.wikipedia.org/wiki/Letterpress_(video_game)) — правила, заблоковані плитки, кінець гри, бот, Game Center, replay, freemium, Solebon.
- [MacRumors, 2012](https://www.macrumors.com/2012/10/24/letterpress-combines-boggle-and-go-in-one-simple-word-game/) — «Boggle + го», ліміт 2 партій, покупка.
- [Google Play: пошук Letterpress](https://play.google.com/store/search?q=letterpress%20word%20game&c=apps) — Android-версія.
- YouTube: пошук «letterpress word game gameplay».

## Непевне
- (?) Захист — саме 4 ортогональні сусіди з урахуванням краю поля; вікі каже лише «оточена своїми».
- (?) Правило префікса (не можна зіграти CAT після CATS) — з памʼяті; вікі формулює «не з тієї ж родини слів».
- (?) Нічия при рівній кількості плиток; кнопки Clear/Resign; перестановка літер у лотку — з памʼяті.
- (?) Wordbase як нащадок — з памʼяті, не перевірено.
- Офіційний сайт atebits.com віддав сторінку перевірки бота — не прочитано.
