---
title: Keyword (The Washington Post)
slug: wapo-keyword
aka: [Keyword, WaPo Keyword, Washington Post Keyword]
family: word-number
also: []
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: hidden
  random: none
  goal: state
year: 2023
platforms: [web, mobile]
links:
  - {kind: official, url: "https://helpcenter.washingtonpost.com/hc/en-us/articles/16190753288475-What-is-Keyword", best: true, note: "офіційна довідка «What is Keyword?»: 6 слів з пропуском, keyword із 6 літер, ідеал — 6 спроб; агентові віддає 403, бачив у пошуку"}
  - {kind: play, url: "https://www.washingtonpost.com/games/keyword/", note: "грати; агентові віддає 403"}
  - {kind: other, url: "https://www.editorandpublisher.com/stories/the-washington-post-expands-games-suite-with-keyword,244335", note: "запуск 20.06.2023, щодня опівночі ET, desktop / mobile web / застосунок"}
  - {kind: other, url: "https://nerdschalk.com/washington-post-keyword-hints-and-answers-october-22-2026/", note: "розкладка: 6 слів униз, пропуски в одному ряду; кожна спроба рахується"}
  - {kind: other, url: "https://www.journalism.co.uk/the-washington-post-discovers-an-engaged-gaming-audience/", note: "метрики: 2/3 гравців повертаються, тест з ~1000 користувачів, розсилка Game Break"}
  - {kind: other, url: "https://gist.github.com/zamora/3e385e0387a5d43047f3110d6c9dcd1a", note: "розвʼязувач на Python: кандидати для кожного пропуску → regex keyword"}
  - {kind: other, url: "https://www.askdavetaylor.com/how-to-play-keyword-game-from-the-washington-post/", note: "покроковий гайд (агентові 403; у пошуку: правильна літера — зелений фон, обрана клітина — синя)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=washington+post+keyword+game", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [cell-click, keyboard-controls, selection-highlight, word-validation, completion-detection, daily-puzzle, profile-stats, stats-window, game-screen, end-screen, help-window, +letter-feedback, +keyword-crossing, +guess-count-score, +retry-wrong-letter, +bonus-puzzle, +account-sync]
proposes: ["+cond:fills_word", "+cond:matches_answer", "+ui:guess-counter", "+feature:bonus-puzzle", "+card:keyword-crossing"]
author: opus
date: 2026-11-09
---

# Keyword — шість слів із пропущеною літерою; пропуски стоять в одному ряду, і їхні літери складають ключове слово

## Суть
Щоденна газетна гра «кросворд без підказок»: шість слів на дошці, у кожному бракує однієї літери, а шість пропусків вишикувані в один ряд. Літера в пропуску мусить дати справжнє слово у своєму стовпці **і** разом з іншими п'ятьма скласти шестилітерне ключове слово. Гравець вписує літери по одній; кожна спроба рахується, хибну можна пробувати знову. Ідеальний результат — 6 спроб (жодної помилки).

## Поле і час
- Дошка: 6 вертикальних слів різної довжини, зсунутих так, що пропуски стоять у спільному горизонтальному ряду — це і є keyword (приклад 22.10.2026: MIND, MAGNET, RUBBLE, SPLASH, STARRY, EIGHT → DEBATE).
- Шари: літери слів (дано), пропуски (порожні клітини), ряд keyword.
- Часу на поразку нема; секундомір іде для статистики («середній час»).
- Новий пазл щодня опівночі за Eastern Time; раз на тиждень — бонусний рівень.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Слово-стовпець | zone | літери, позиція пропуску | дано; має рівно один пропуск |
| Літера слова | tile | буква | дана, не змінюється |
| Пропуск | tile | правильна літера (прихована) | приймає спробу; правильна — фіксується зеленим, хибна — позначається й лишає клітину для нової спроби |
| Ряд keyword | zone | 6 пропусків | читається зліва направо як ключове слово |
| Лічильник спроб | mark | ≥ 6 | +1 за кожну вписану літеру |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click пропуск)` → ТО `custom: «клітину обрано»` (синє підсвічування).
- КОЛИ `input(type letter)` → ЯКЩО `state(пропуск, selected)` → ТО `counter(guesses, +1)`.
- КОЛИ `input(type letter)` → ЯКЩО `same(letter, answer, letter)` → ТО `set_value(пропуск, letter)`, `feedback(correct)` (зелений фон), `custom: «перейти до наступного пропуску»` (?).
- КОЛИ `input(type letter)` → ЯКЩО not `same(letter, answer, letter)` → ТО `feedback(wrong)` (рожевий фон), `message("N is incorrect after 1 guess. Try again.")`; пропуск лишається відкритим для нової спроби.
- Перевірка — проти авторської відповіді, а не словника: літера, що дає інше справжнє слово в стовпці, але не пасує keyword, теж хибна.
- КОЛИ `custom: «усі 6 пропусків заповнено»` → ТО `win`, `window(end-screen)`.
- ЯКЩО `counter(guesses, =, 6)` → ТО `custom: «perfect — без помилок»`.
- Конструкція пазла: КОЛИ `custom: «автор складає дошку»` → ЯКЩО `custom: «для кожного стовпця множина літер, що дає слово, у перетині з keyword-словником дає рівно одне слово»` → ТО `custom: «пазл має єдиний розвʼязок»` (?).
- Перемога: keyword розкрито · Поразки нема (обмеження спроб не знайшов) · Рахунок: кількість спроб (менше — краще; 6 — ідеал) і час.

## Керування і ввід
- Тап/клік по пропуску → вибір клітини; літера — з екранної клавіатури або фізичної.
- Стратегія з гайдів: шукати стовпець із найменшою кількістю варіантів літери і від нього звужувати keyword.

## Вікна, меню, HUD
- `game-screen`: шість стовпців-слів, ряд пропусків, екранна клавіатура, `selection-highlight`, повідомлення про хибну спробу, `timer-elapsed` (?), `guess-counter` (?).
- `end-screen`: keyword, кількість спроб, час; підказка-означення слова з прикладом вживання (?).
- `stats-window`: середня кількість спроб, середній час, кількість perfect-розвʼязків.
- `help-window`: правила «What is Keyword?».
- Переходи: розсилка Game Break / сторінка ігор → `game-screen` → `end-screen` → `stats-window`.

## Фічі поза полем
- `daily-puzzle` опівночі ET; `bonus-puzzle` — додаткова гра раз на тиждень.
- `stats`: середні спроби, середній час, perfect-кількість; синхронізація між пристроями після входу в акаунт Post.
- Доступ: desktop, mobile web, застосунок Post; розсилка Game Break щодня з посиланнями й середнім часом розвʼязання.

## Варіації й родичі
- Wordle (`wordle.md`) — вгадування слова з відгуком по літерах; тут відгук лише «так/ні» на одну клітину.
- Crosswordle (`crosswordle.md`), Waffle (`waffle.md`) — перетин слів як джерело обмежень.
- Codeword (`codeword.md`), Fill-In (`fill-in.md`) — вписати літери в готові слова без означень.
- **Осі варіацій:** кількість стовпців (6) · де стоять пропуски (одним рядом / діагоналлю) · відгук (одразу на літеру / на ціле слово) · рахунок (спроби / час / обидва).

## Цікавинки для курсу
- Модель дошки: стовпці зі зсувом так, щоб пропуски стали в ряд — 🌱.
- Ввід з відгуком на кожну літеру і лічильником спроб — 🌱.
- Розвʼязувач як у gist zamora: для кожного стовпця множина літер зі словника → regex `[..][..]…` по 6-літерних словах — 📎.
- Генератор: обрати keyword, для кожної літери підібрати слово-стовпець так, щоб розвʼязок був єдиним — 🥉.
- Статистика: середні спроби/час, perfect-лічильник — 🌱.

## Мапа на каталог
- Є: `cell-click` + `keyboard-controls` ↔ вибір і ввід; `selection-highlight`; `word-validation` ↔ стовпці — справжні слова (на етапі генерації); `completion-detection`; `daily-puzzle`; `profile-stats` + `stats-window`; `game-screen`, `end-screen`, `help-window`.
- **Нема** → пропозиції карток:
  - `+keyword-crossing` «Літери-пропуски кількох слів складають ключове слово» · game-logic/constraints · 📎.
  - `+guess-count-score` «Рахунок = кількість спроб, ідеал = мінімум» · game-logic/score · 🌱.
  - `+retry-wrong-letter` «Хибна літера позначається, клітина приймає нову спробу» · game-logic/history · 🌱.
  - `+bonus-puzzle` «Додатковий пазл раз на тиждень» · levels/bank · 🌱.
  - `+account-sync` «Статистика між пристроями через акаунт» · game-logic/save · 🥉.
  - `+letter-feedback` — уже в корпусі (Wordle-подібні).

## Пропозиції до словників
- `+cond:fills_word` — літера в пропуску дає справжнє слово в стовпці.
- `+cond:matches_answer` — спроба збігається з авторською відповіддю клітини (не словником).
- `+ui:guess-counter` — лічильник спроб.
- `+feature:bonus-puzzle` — тижневий бонусний пазл.
- `+card:keyword-crossing` — механіка, якої в каталозі нема.

## Джерела
- ⭐ [Washington Post Help Center: What is Keyword?](https://helpcenter.washingtonpost.com/hc/en-us/articles/16190753288475-What-is-Keyword) — правила, ідеал 6 спроб, повідомлення про хибну літеру, бонусний рівень, екран підсумків (403 для фетчу, зміст — з фрагментів пошуку).
- [Editor & Publisher: запуск Keyword](https://www.editorandpublisher.com/stories/the-washington-post-expands-games-suite-with-keyword,244335) — 20.06.2023, шість слів-підказок з пропущеною літерою, щодня опівночі ET.
- [Nerdschalk: Keyword 22.10.2026](https://nerdschalk.com/washington-post-keyword-hints-and-answers-october-22-2026/) — «шість слів униз, пропуски в одному ряду», кожна спроба рахується, приклад дошки.
- [journalism.co.uk](https://www.journalism.co.uk/the-washington-post-discovers-an-engaged-gaming-audience/) — метрики й Game Break.
- [gist zamora: wapo-keyword.py](https://gist.github.com/zamora/3e385e0387a5d43047f3110d6c9dcd1a) — алгоритм розвʼязувача.
- [Ask Dave Taylor](https://www.askdavetaylor.com/how-to-play-keyword-game-from-the-washington-post/) — гайд (403; фрагменти з пошуку: зелений фон правильної, синя обрана клітина).

## Непевне
- (?) Орієнтація: Nerdschalk і черга — слова вертикальні, keyword горизонтальний; фрагмент довідки в пошуку казав «complete six horizontal words». Не бачив гри сам.
- (?) Рожевий фон хибної літери — зі стороннього блогу (у пошуку); чи хибна літера лишається видимою — невідомо.
- (?) Чи є ліміт спроб, таймер на екрані, кнопка підказки, share-результат — не бачив.
- (?) Чи курсор сам переходить до наступного пропуску після правильної літери.
- (?) Чи гра й досі лише для передплатників (один гайд казав так).
