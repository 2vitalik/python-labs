---
title: Pushmo World / Stretchmo
slug: pushmo-world-stretchmo
aka: [引ク押ス ワールド, 引ク出ス ヒッパランド, Fullblox, Stretchmo]
family: grid-platformer
also: [push-slide, thinky]
klass: avatar
axes:
  field: 3d
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 2014
platforms: [Wii U eShop (Pushmo World 2014), 3DS eShop (Stretchmo 2015, free-to-start)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pushmo_World", best: true, note: "Pushmo World: 250 рівнів, Pushmo Studio, QR і World Pushmo Fair (Miiverse, закрито 2017)"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Stretchmo", note: "розтягування шматків, небезпеки, демо на 7 рівнів, 4 платні атракціони + Perilous Peak, Stretchmo Studio, QR"}
  - {kind: other, url: "https://ja.wikipedia.org/wiki/引ク出ス_ヒッパランド", note: "JP: витягування з 4 боків до 2 кроків, перемикачі-трикутник і ромб, люки, вороги як опора, курси й ціни, режими редактора"}
  - {kind: other, url: "https://ja.wikipedia.org/wiki/引ク押ス", note: "JP: нові блоки Pushmo World — перемикач вштовхування, звʼязані, протилежні, блоки-повернення"}
  - {kind: other, url: "https://ja.wikipedia.org/wiki/引ク押スシリーズ", note: "JP: порівняння частин серії"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Stretchmo+gameplay", note: "пошук; геймплей Stretchmo"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Pushmo+World+Wii+U+gameplay", note: "пошук; геймплей Pushmo World"}
stage: v1
coverage: 60
mechanics: [pull-object, push-object, multi-cell-size, teleport-pair, button-toggle, reach-exit, level-select, level-unlock, in-game-editor, level-exchange, game-screen, +depth-pull-wall, +color-switch-extend, +linked-pieces, +qr-level-share, +four-side-drawer, +auto-return-block, +enemy-as-platform, +paid-level-packs]
proposes: ["+card:four-side-drawer", "+card:auto-return-block", "+card:enemy-as-platform", "+card:paid-level-packs", "+feature:paid-level-packs"]
author: opus
date: 2026-11-09
---

# Pushmo World / Stretchmo — ті самі висувні шматки-сходинки, плюс групові блоки (World) і витягування з усіх чотирьох боків (Stretchmo)

## Суть
Продовження [pushmo](pushmo.md): Мелло лізе на кольорову структуру, висуваючи шматки як шухляди. Тут — **лише відмінності**. Pushmo World (Wii U) лишає правила, але додає блоки, що діють групою за кольором, і онлайн-обмін рівнями. Stretchmo змінює геометрію: структура стоїть посеред поля, і шматки витягуються **спереду, ззаду, зліва й справа** (до 2 кроків з кожного боку), тож рівень стає справжнім 3D-обʼєктом.

## Поле і час
- Pushmo World: як у Pushmo — стіна з глибиною 0…3 спереду.
- Stretchmo: центральне ядро структури закріплене; з кожної з 4 бічних граней шматок можна витягти на 1–2 кроки; камера обходить структуру (?).
- Real-time, детерміновано; у частині курсів Stretchmo — вороги (рух real-time).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Перемикач вштовхування (World) | switch | колір | наступив → усі шматки цього кольору повертаються в початковий стан |
| Звʼязані блоки (World) | object | колір | висунув/вштовхнув один → усі того ж кольору в той самий стан |
| Протилежні блоки (World) | object | пара типів | один висувається → другий вштовхується |
| Блок-повернення (World) | object | затримка | висунутий сам вштовхується назад через час |
| Шматок-шухляда (Stretchmo) | object | бік, глибина 0–2 | витягується з передньої, задньої, лівої або правої грані |
| Перемикач-трикутник (Stretchmo) | switch | колір | висуває всі шматки кольору повністю вперед |
| Перемикач-ромб (Stretchmo) | switch | колір | висуває всі шматки кольору повністю в усі 4 боки |
| Люк (Stretchmo) | gate | колір пари | зʼявляється, коли шматок витягнуто; вхід → люк того ж кольору |
| Ворог (Stretchmo, Action Plaza) | enemy | — | не знищується; може атакувати; на нього можна стати як на опору |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `enter(mallo, push_in_switch)` → ТО `custom: «усі шматки кольору → початкова глибина»` (World).
- КОЛИ `input(grab+back)` → ЯКЩО `state(piece, linked)` → ТО `pull(piece)` і `custom: «усі шматки того ж кольору — у той самий стан»` (World).
- КОЛИ `after(pull)` → ЯКЩО `state(piece, opposite_pair)` → ТО `custom: «парний шматок вштовхується на стільки ж»` (World).
- КОЛИ `timer(return_delay)` → ЯКЩО `state(piece, return_block)` і `state(piece, pulled)` → ТО `custom: «шматок вштовхується назад»` (World).
- КОЛИ `input(grab+back)` → ЯКЩО `facing(mallo, piece_face)` і `custom: «з цього боку витягнуто < 2»` → ТО `pull(piece)`, `move(mallo, back)` (Stretchmo; бік — будь-який з 4).
- КОЛИ `input(grab+forward)` → ЯКЩО `custom: «з цього боку витягнуто > 0»` → ТО `push(piece)` (Stretchmo).
- КОЛИ `enter(mallo, triangle_switch)` → ТО `custom: «шматки кольору — повністю вперед»`; КОЛИ `enter(mallo, diamond_switch)` → ТО `custom: «шматки кольору — повністю в усі 4 боки»`.
- КОЛИ `after(pull)` → ЯКЩО `custom: «на гранях відкрився люк»` → ТО `spawn(manhole)`; КОЛИ `enter(mallo, manhole)` → ТО `teleport(mallo, pair)`.
- КОЛИ `contact(mallo, enemy)` → ЯКЩО `custom: «Мелло зверху»` → ТО ворог — опора; інакше `custom: «атака»` (?).
- Перемога, поразка, рахунок — як у [pushmo](pushmo.md).

## Керування і ввід
- Як у Pushmo; у Pushmo World — Wii U GamePad (?).
- Stretchmo: той самий «схопити й потягти», але до будь-якої з 4 граней — гравець обходить структуру.

## Вікна, меню, HUD
- Pushmo World: `level-select` (250 рівнів) · Pushmo Studio (`editor-window`) · World Pushmo Fair — `custom-window` для публікації й гри чужих рівнів через Miiverse (закрито 07.11.2017) · QR-обмін.
- Stretchmo: хаб атракціонів-курсів: Playtime Plaza (100) · Sculpture Square (50, фігури-тварини й предмети) · Fortress of Fun (50, більше «екшну», вороги) · NES Expo (50, персонажі NES) · Perilous Peak (50, складні; відкривається після всіх чотирьох) · безкоштовний вступ (7 курсів).
- Stretchmo Studio (`editor-window`): режим «обʼєкт» (глибокі 3D-фігури) і режим «ілюстрація» (пласкі); відкривається після покупки будь-якого атракціону.
- `game-screen`: як у Pushmo.

## Фічі поза полем
- `level-editor` + `level-sharing` через QR (обидві гри); World — ще й онлайн-майданчик.
- Stretchmo — `paid-level-packs`: безкоштовне завантаження, курси продаються окремо, групами або всі разом; редактор і фінальний курс — за умовами покупки/проходження.

## Варіації й родичі
- Лінія: [pushmo](pushmo.md) (2011) → Crashmo (2012, описано в pushmo.md) → Pushmo World (2014) → Stretchmo (2015).
- Родичі «тягни блок, лізь»: Catherine, [boxboy](boxboy.md), [block-dude](block-dude.md).
- Осі: **звідки тягнеш** (лише спереду / з 4 боків / вільно з гравітацією — Crashmo); **групова дія** (один шматок / усі кольору / пара навпаки); **стан у часі** (тримається / сам повертається); **монетизація рівнів** (усе в грі / платні паки).

## Цікавинки для курсу
- Структура-ядро з шухлядами на 4 гранях (глибина на кожен бік окремо) — 🥈 (3D-стан і рендер).
- Звʼязані за кольором блоки: одна дія → стан усієї групи — 📎.
- Протилежна пара: висунув один — другий вштовхнувся — 📎.
- Блок, що сам повертається за таймером — 🌱.
- Ворог як рухома опора, якого не можна вбити — 🥉 (стояти на рухомому обʼєкті).

## Мапа на каталог
- Є: `pull-object` · `push-object` · `multi-cell-size` · `teleport-pair` (люки) · `button-toggle` (перемикачі) · `reach-exit` · `level-select` · `level-unlock` (Perilous Peak) · `in-game-editor` · `level-exchange` · `game-screen`.
- Вже запропоновано в pushmo.md: `+depth-pull-wall` · `+color-switch-extend` · `+linked-pieces` · `+qr-level-share`.
- **Нема** → пропозиції карток:
  - `+four-side-drawer` «Шухляди на 4 гранях ядра, глибина на кожен бік» · entities/state · 🥈.
  - `+auto-return-block` «Висунутий блок повертається за часом» · entities/state · 🌱.
  - `+enemy-as-platform` «Ворог як опора» · entities/move · 🥉.
  - `+paid-level-packs` «Пакети рівнів, що відкриваються окремо» · levels/progression · 🌱.

## Пропозиції до словників
- `+card:four-side-drawer`, `+card:auto-return-block`, `+card:enemy-as-platform`, `+card:paid-level-packs` — див. вище.
- `+feature:paid-level-packs` — курси/рівні як окремі покупки, фінальний курс за проходженням усіх.

## Джерела
- ⭐ [Wikipedia: Pushmo World](https://en.wikipedia.org/wiki/Pushmo_World) — 250 рівнів, Studio, QR, World Pushmo Fair.
- [Wikipedia: Stretchmo](https://en.wikipedia.org/wiki/Stretchmo) — розтягування, небезпеки, атракціони, Studio, QR.
- [ja.wikipedia: 引ク出ス ヒッパランド](https://ja.wikipedia.org/wiki/引ク出ス_ヒッパランド) — 4 боки по 2 кроки, перемикачі, люки, вороги, курси, режими редактора.
- [ja.wikipedia: 引ク押ス](https://ja.wikipedia.org/wiki/引ク押ス) — нові блоки Pushmo World.
- [ja.wikipedia: 引ク押スシリーズ](https://ja.wikipedia.org/wiki/引ク押スシリーズ) — порівняння серії.

## Непевне
- (?) Чи можна в Stretchmo витягувати вгору/вниз — JP-стаття згадує лише 4 горизонтальні боки.
- (?) Як вороги «атакують» і чи це забирає життя чи скидає рівень.
- (?) Обертання камери в Stretchmo і керування GamePad у Pushmo World.
- (?) EU-назва Pushmo World (Pullblox World) — з памʼяті, не перевірено.
- (?) pushmo.md описує звʼязані блоки World як «пару»; JP-стаття — як групу одного кольору (тут — друге).
