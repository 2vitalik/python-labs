---
title: Word Factori
slug: word-factori
aka: [factori]
family: program-robots
also: [word-number, build-sim]
klass: cursor
axes:
  field: graph
  time: programmed
  opponent: none
  info: full
  random: none
  goal: state
year: 2023
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2072840/Word_Factori/", best: true, note: "суть: єдиний ресурс — «i»; згин, поворот, відбиття, злиття; рецепти, наліпки, щоденне слово, свої слова, три метрики; скриншоти"}
  - {kind: itch, url: "https://stargardengames.itch.io/word-factori", note: "сторінка гри й коментарі: джем GMTK 2021 за 48 год, синій кошик-ціль, shift-клік міняє тип будівлі, «?» для неможливої комбінації"}
  - {kind: official, url: "https://stargardengames.com/word-factori", note: "сторінка студії Star Garden Games, прес-кіт"}
  - {kind: other, url: "https://gamedeveloper.com/design/an-i-for-details-designing-for-approachably-complex-letter-bending-puzzles-in-i-factori-i-", note: "дизайн: 4 типи фабрик, лінії з магнітними вузлами, літери рухаються кроками, рекорди на AWS, тема джему «Joined Together»"}
  - {kind: other, url: "https://steamcommunity.com/app/2072840/guides/", note: "гайди: нотація bend/hf/vf/cw/ccw/+, мінімум будівель, секретні рівні KEY + DOOR"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Word+Factori+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [drag-drop-piece, piece-rotate-flip, tile-merge, sequential-levels, level-unlock, level-select, main-menu, game-screen, end-screen, help-window, settings-window, daily-puzzle, theme-select, +dataflow-graph, +glyph-transform-ops, +glyph-merge, +recipe-discovery, +recipe-book, +solution-metrics, +metric-histograms, +overflow-metric, +type-your-own-level, +shared-words, +sticker-collection, +restricted-building-palette, +result-preview-known, +secret-levels-key]
proposes: ["+role:building", "+role:token", "+effect:mirror(a, axis)", "+effect:bend(a)", "+window:recipe-book", "+window:sticker-book", "+window:type-a-word", "+ui:bin-row", "+feature:solution-metrics"]
author: opus
date: 2026-11-09
---

# Word Factori — фабрики гнуть, крутять, віддзеркалюють і зливають літеру «i», доки з неї не складеться потрібне слово

## Суть
Пазл-конвеєр Star Garden Games (з джему GMTK 2021, тема «Joined Together»): єдина сировина — літера «i», яку видають фабрики-джерела. Гравець ставить будівлі чотирьох типів — згинач (I → C), поворотник (90° за/проти годинника), дзеркало (горизонтальне/вертикальне), злиття (2 або 4 входи) — і зʼєднує їх лініями в граф, що веде до синіх кошиків-літер цільового слова вгорі. Кожна літера має кілька «рецептів» (A = — + Λ, D = Ↄ + I, W = I + I + I + I); нові рецепти відкриваються в журналі. Після розвʼязку гра показує три метрики й гістограми всіх гравців. Межова для сімʼї гра: сітки як правила нема — це **граф потоку даних** на папері в клітинку; сітковий шар — хіба що самі гліфи, які крутять і дзеркалять.

## Поле і час
- Полотно — «папір у клітинку»; будівлі ставляться перетягуванням, лінії між виходом (червона точка) і входом (синя точка) прокладаються автоматично ортогонально; вузли «магнітно» липнуть до країв будівлі, лінії перебудовуються при перетягуванні.
- Вгорі — ряд синіх кошиків, по одному на літеру цільового слова, з лічильником доставлених літер над кожним.
- Час `programmed`: запуск ▶ — джерела випускають «i», літери рухаються лініями кроками (цикли), будівлі перетворюють їх на вході; є прискорення, пауза, стоп.
- Детерміновано; літери, що не вміщаються, «переливаються» (лічильник letters overflowed).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Літера-гліф | object | форма (I, C, Ↄ, V, —, …) | рухається лінією; будівля змінює форму |
| Джерело «i» (фіолетова фабрика) | source | лише вихід | випускає «i» щоцикл (?) |
| Згинач (помаранчевий) | object | 1 вхід, 1 вихід | гне гліф: I → C (bend) |
| Поворотник (зелений) | object | за / проти год. (shift-клік) | повертає гліф на 90° (I → —) |
| Дзеркало (синій) | object | горизонтальне / вертикальне (shift-клік) | відбиває гліф (C → Ↄ) |
| Злиття (червоне) | object | 2 або 4 входи, 1 вихід | складає форми входів в один гліф (V + i → Y) |
| Лінія | conduit | автотраса | веде літери від виходу до входу, черга літер |
| Кошик-літера | sink | цільова літера, лічильник | приймає літеру слова |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, building)` → ТО `place(player, building)`; КОЛИ `input(connect, out, in)` → ТО `custom: «лінія від виходу до входу»`.
- КОЛИ `input(shift_click, building)` → ТО `custom: «дзеркало: горизонтальне ↔ вертикальне; поворотник: за ↔ проти годинника»`.
- КОЛИ `tick` → ТО `spawn_at(letter_i, source_output)` (?) і `move(letter, along_line)`.
- КОЛИ `enter(letter, bender)` → ТО `transform(letter, bent_shape)` (I → C).
- КОЛИ `enter(letter, rotator)` → ТО `rotate(letter, ±90)`.
- КОЛИ `enter(letter, reflector)` → ТО `custom: «віддзеркалити гліф по горизонталі або вертикалі»`.
- КОЛИ `enter(letter, merger)` → ЯКЩО `custom: «на всіх входах є по гліфу»` → ТО `merge(inputs → glyph)`; ЯКЩО `custom: «результат — не відомий символ»` → ТО `custom: «будівля показує «?»»`.
- КОЛИ `custom: «змінено граф»` → ЯКЩО `custom: «символ цієї комбінації вже відкритий»` → ТО `custom: «будівля показує превʼю результату»`; ще не відкритий — порожньо.
- КОЛИ `enter(letter, bin)` → ЯКЩО `same(letter, bin, glyph)` → ТО `counter(bin, +1)`.
- КОЛИ `custom: «лінія/вхід переповнені»` → ТО `disappear(letter)`, `counter(overflowed, +1)` (?).
- КОЛИ `custom: «усі кошики слова наповнено»` (?) → ТО `win`, `window(end-screen)` з метриками buildings placed · letters overflowed · cycles.
- КОЛИ `custom: «символ уперше зроблено новим рецептом»` → ТО `unlock(recipe)` у журналі рецептів.
- КОЛИ `custom: «зібрано особливе слово»` → ТО `unlock(sticker)` (word art у sticker book).
- КОЛИ `custom: «рівень 31: зібрано KEY і DOOR»` → ТО `unlock(secret_levels)`.
- Перемога: слово зібрано · Поразка: нема · Рахунок: три метрики (менше — краще), порівняння з гістограмою всіх гравців і своїм best.

## Керування і ввід
- Миша: перетягнути будівлю з палітри праворуч на полотно; тягнути від вихідної точки до вхідної — лінія; shift-клік — альтернативний тип будівлі.
- Кнопки внизу ліворуч: ▶ / прискорення, пауза, стоп; «?» — довідка.
- type-a-word: набрати будь-яке слово — воно стає рівнем.

## Вікна, меню, HUD
- `main-menu`: play · type-a-word · журнали (recipes, sticker book, words) · Discord · options.
- `level-select`: сторінки рівнів; остання сторінка за «дверима» (секретні рівні).
- `game-screen`: полотно в клітинку, `bin-row` (custom) — кошики слова з лічильниками, палітра будівель праворуч (у challenge-рівнях обмежена), кнопки запуску; `help-window` «?».
- `end-screen`: наліпка слова, «N other players have built this word», три картки-гістограми (buildings placed, letters overflowed, cycles) з поточним і best; кнопки next level · continue editing · menu.
- `recipe-book` (custom): «letter recipes», «discovered N / M», відкриті рецепти з галочками.
- `sticker-book` (custom): зібрані наліпки word art; `words` — журнал зібраних слів (?).
- `type-a-word` (custom): ввід власного слова; слово дня; слова, якими поділились інші гравці.
- `settings-window` (options): темна тема, hard mode (?).

## Фічі поза полем
- Метрики й гістограми спільноти (анонімні рекорди на сервері) — оптимізація за будівлями або швидкістю, або без неї.
- Журнал рецептів (кілька рецептів на літеру, секретні символи й цифри), наліпки за особливі слова, досягнення Steam.
- Щоденне слово (word of the day), свої слова, слова інших гравців; challenge-рівні з обмеженими будівлями; секретні рівні.
- Dark mode, hard mode (оновлення itch-версії) (?).

## Варіації й родичі
- Корпус: [opus-magnum](opus-magnum.md) і [spacechem](spacechem.md) (продукт із сировини + гістограми метрик), [manufactoria](manufactoria.md) (конвеєр-обробка), [infinite-turtles](infinite-turtles.md) (потік токенів між блоками), [factorio-circuit-network](factorio-circuit-network.md). Поза сімʼєю: Mini Metro (стиль ліній, натхнення), Wordle-подібні (сімʼя word-number).
- Осі варіацій: **поле** (сітка з клітинами-машинами / вільний граф з лініями); **операції над формою** (поворот, відбиття — група D4; згин і злиття — специфічні); **ціль** (одна літера / слово / слово дня / своє слово).

## Цікавинки для курсу
- Гліф як мала сітка штрихів: поворот на 90° і віддзеркалення — 📎; злиття накладанням з розпізнаванням символу — 🥉.
- Граф потоку даних (джерела → перетворювачі → кошики) з кроковою симуляцією й чергами на лініях — 🥈.
- Книга рецептів: кілька шляхів до одного символу, відкриття нового рецепта — 📎.
- Три метрики й гістограма серед усіх гравців — 🥉.
- «Своє слово» як генератор рівня з будь-якого тексту — 📎.

## Мапа на каталог
- Є: `drag-drop-piece` (будівлі) · `piece-rotate-flip` (поворот/відбиття гліфа) · `tile-merge` (злиття форм) · `sequential-levels` / `level-unlock` / `level-select` · `main-menu` · `game-screen` · `end-screen` · `help-window` · `settings-window` · `daily-puzzle` (слово дня) · `theme-select` (темна тема).
- **Нема** → пропозиції карток:
  - `+dataflow-graph` «Граф перетворювачів, зʼєднаних лініями» · game-logic/program · 🥈.
  - `+glyph-transform-ops` «Згин, поворот, відбиття форми» · entities/state · 📎; `+glyph-merge` «Злиття форм у символ» · entities/interact · 🥉.
  - `+recipe-discovery` + `+recipe-book` «Відкриття рецептів і журнал» · interface/menus · 📎.
  - `+solution-metrics` / `+metric-histograms` «Метрики розвʼязку й розподіл спільноти» · interface/results · 🥉; `+overflow-metric` · 🌱.
  - `+type-your-own-level` «Рівень з власного слова» · levels/generation · 📎; `+shared-words` · levels/bank · 📎; `+sticker-collection` · 🌱.
  - `+restricted-building-palette` · game-logic/difficulty · 🌱; `+result-preview-known` · interface/hud · 🌱; `+secret-levels-key` · levels/progression · 🌱.

## Пропозиції до словників
- `+role:building` — будівля-перетворювач на полі (фабрика); `+role:token` — літера як дані, що течуть лініями.
- `+effect:mirror(a, axis)` — віддзеркалити форму по осі; `+effect:bend(a)` — згин гліфа (I → C) — специфічний, але без нього речення не прочитати.
- `+window:recipe-book` · `+window:sticker-book` · `+window:type-a-word` — журнали й ввід свого рівня.
- `+ui:bin-row` — ряд цільових кошиків з лічильниками.
- `+feature:solution-metrics` — кілька метрик розвʼязку з гістограмою гравців.

## Джерела
- ⭐ [Steam: Word Factori](https://store.steampowered.com/app/2072840/Word_Factori/) — опис, реліз 3 серпня 2023, Windows; скриншоти (полотно, end-screen з трьома метриками, журнал рецептів, головне меню).
- [itch.io](https://stargardengames.itch.io/word-factori) — джем-походження, кошики, shift-клік, «?» і превʼю в коментарях.
- [Game Developer](https://gamedeveloper.com/design/an-i-for-details-designing-for-approachably-complex-letter-bending-puzzles-in-i-factori-i-) — дизайн ліній і фабрик, метрики, тема джему.
- [Steam-гайди](https://steamcommunity.com/app/2072840/guides/) — нотація рецептів, мінімум будівель, секретні рівні.
- [stargardengames.com](https://stargardengames.com/word-factori) — сторінка студії.

## Непевне
- (?) Чи будівлі прилипають до клітин паперу — полотно в клітинку, але правила розміщення не описані; тому `field: graph`.
- (?) Умова перемоги (скільки літер має отримати кожен кошик) і що саме рахує «letters overflowed».
- (?) Чи джерело «i» випускає літеру щоцикл і чи лінія має місткість.
- (?) Як злиття розташовує входи (порядок входів = позиція штриха?); у рецептах A = — + Λ, D = Ↄ + I.
- (?) Hard mode й dark mode — зі слів розробника в коментарях itch; журнал «words» — лише кнопка на скриншоті.
