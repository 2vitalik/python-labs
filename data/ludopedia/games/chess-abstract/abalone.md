---
title: Abalone (Абалон)
slug: abalone
family: chess-abstract
also: [push-slide]
klass: figure
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: score
year: 1987
platforms: [board, web, PC]
links:
  - {kind: other, url: "https://www.ultraboardgames.com/abalone/game-rules.php", best: true, note: "повні правила: колона, in-line і side-step, усі ситуації sumito й коли штовхати не можна"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Abalone_(board_game)", note: "автори, 1987/1990, Daisy-розстановки, Grand Abalone, AI Aba-Pro"}
  - {kind: play, url: "https://en.boardgamearena.com/gamepanel?game=abalone", note: "Board Game Arena — онлайн на двох"}
  - {kind: play, url: "https://www.playabalone.com", note: "PlayAbalone (лінк зі статті Wikipedia)"}
  - {kind: other, url: "https://playstrategy.org/analysis/abalone", note: "PlayStrategy: дошка аналізу"}
  - {kind: other, url: "https://playstrategy.org/variant/grandabalone", note: "правила Grand Abalone"}
  - {kind: steam, url: "https://store.steampowered.com/app/279480/Abalone/", note: "Steam-видання"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=abalone+board+game+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 75
mechanics: [push-object, piece-capture, legal-move-highlight, hot-seat, turn-enforcement, move-timer, ai-opponent, ai-minimax, cell-click, hover-highlight, drag-drop-piece, game-screen, main-menu, end-screen, help-window, settings-window, theme-select, replay, state-as-data, +hex-grid-render, +group-move, +majority-push, +push-off-capture, +capture-count-win, +board-layouts, +rule-variants]
proposes: ["+cond:outnumbers", "+effect:push_line", "+effect:move_group", "+ui:group-selection", "+ui:direction-arrows", "+window:layout-select", "+axis:field-bounds", "+card:group-move", "+card:majority-push", "+card:push-off-capture", "+card:capture-count-win"]
author: opus
date: 2026-11-02
---

# Abalone — штовхай ворожі кульки з гекса колоною, що чисельно сильніша

## Суть
Двоє по черзі рухають свої кульки на шестикутному полі з 61 клітини: одну або колону з 2–3 своїх кульок, що стоять у ряд, на одну клітину. Взяття — лише **виштовхуванням за край**: колона, яка чисельно переважає ворожу групу перед собою на тій самій лінії (sumito), зсуває її, а крайня ворожа кулька, що зійшла з поля, вибуває. Перший, хто виштовхнув 6 кульок суперника, виграє. Фігури однакові — уся тактика в геометрії ліній і в «рахунку сил» 3>2>1.

## Поле і час
- Гексагон зі стороною 5 = 61 клітина (`field: hex`); 6 напрямків руху. Навколо — жолоб, куди падають виштовхнуті кульки.
- По 14 кульок у кожного (чорні й білі); стандартна розстановка — два сегменти біля протилежних країв; альтернативні — Belgian Daisy, German Daisy (кульки «квітками» ближче до центру, щоб уникнути пасивної гри).
- Покроково; першими ходять чорні. Партія без ліміту ходів — тому пасивна оборона може тягнути гру нескінченно (турніри вводять ліміти й альтернативні розстановки).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кулька | piece | сторона black/white | рухається сама або в колоні; штовхається сильнішою ворожою колоною |
| Колона | — | 2 або 3 своїх кульки в ряд, впритул | рухається цілою на 1 клітину в одному напрямку: in-line (вздовж своєї лінії) або side-step (бічний зсув) |
| Порожня клітина | static | — | ціль руху без штовхання |
| Край / жолоб | zone | 6 сторін | кулька, виштовхнута за край, вибуває з гри |
| Лічильник вибулих | zone | 0–6 на сторону | 6 вибулих = поразка їхнього власника |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, group, dir)` → ЯКЩО `turn_of(side)` і `custom: «group — 1–3 своїх кульки в ряд впритул»` → ТО продовжити перевірку; інакше `block`.
- In-line: КОЛИ `dir` вздовж лінії колони → ЯКЩО `free(cell_ahead)` → ТО `custom: «зсунути всі кульки групи на 1»` (`+effect:move_group`).
- Side-step: КОЛИ `dir` не вздовж лінії → ЯКЩО для **кожної** кульки `free(target)` → ТО `move_group`; side-step ніколи не штовхає.
- Sumito: КОЛИ in-line і попереду ворожі кульки → ЯКЩО `custom: «своїх у колоні більше, ніж ворожих підряд попереду»` (`+cond:outnumbers`: 2>1, 3>1, 3>2) і за ворожими — порожня клітина або край → ТО `custom: «зсунути весь ряд на 1»` (`+effect:push_line`); інакше `block`.
- Штовхати не можна: одна кулька (1 проти 1); рівні сили (2 проти 2, 3 проти 3); ворожа група, за якою стоїть **своя** кулька (затиснута); ворожа група через порожню клітину; понад 3 своїх — 4 проти 3 не є sumito, бо рухати можна максимум 3.
- КОЛИ `push_line` → ЯКЩО крайня ворожа кулька `edge(a)` → ТО `disappear(a)`, `counter(ejected[enemy], +1)`.
- Свою кульку за край виштовхнути не можна (власний хід за край заборонений) (?).
- КОЛИ `counter(ejected[side], ==, 6)` → ТО `win` суперника.
- Перемога: 6 виштовхнутих ворожих · Поразка: втратити 6 своїх · Рахунок: вибулі кульки (6:x).

## Керування і ввід
- Настільна: пересунути кульки руками; виштовхнута скочується в жолоб.
- (цифрова версія) Вибір 1–3 кульок кліком/обведенням (виділяються лише валідні колони), потім стрілка одного з 6 напрямків або drag групи; легальні напрямки підсвічені; sumito показаний наперед (стрілка штовхання).
- Hotseat / онлайн; без випадковості й прихованої інформації.

## Вікна, меню, HUD
- `main-menu`: Грати проти AI / друга / онлайн → `layout-select` (Standard, Belgian Daisy, German Daisy) → `settings-window` (рівень AI, колір, годинник).
- `game-screen`: гекс-дошка, `turn-indicator`, `captured-pieces` (жолоби з вибулими, 0–6), `group-selection` (обрані кульки), `direction-arrows` (6 напрямків), `legal-move-highlight`, `last-move-highlight`, `move-list`, `player-clock` (онлайн).
- `end-screen`: перемога (6 вибулих) / здача / час.
- `help-window`: правила sumito з діаграмами.
- Переходи: main-menu → layout-select → game-screen → end-screen → game-screen.

## Фічі поза полем
- `online-multiplayer` і `turn-timer` (Board Game Arena, PlayAbalone, PlayStrategy), `ai-opponent-levels` (Steam-видання) (?).
- Дошка аналізу (PlayStrategy) — `replay` + запис ходів.
- `custom-rules`: розстановки (Daisy), Grand Abalone.
- `stats`, `rating` на онлайн-платформах.

## Варіації й родичі
- Grand Abalone — більше поле (6 клітин на сторону), два ходи за хід (крім першого), колона до 4 кульок, перемога — 10 виштовхнутих.
- 3–6 гравців і командна гра — менше кульок на гравця.
- The Pillar — нерухома кулька в центрі; версії з другим шаром кульок.
- Осі варіацій: **розстановка** (Standard / Belgian Daisy / German Daisy) · **макс. колона** (3 / 4) · **ходів за хід** (1 / 2) · **ціль** (6 / 10 виштовхнутих).
- Родичі: Sumo-штовхання в Kamisado, Push-ігри (Push Fight), Sokoban-подібне «зсунути ряд, якщо за ним вільно» (`push-object`).

## Цікавинки для курсу
- Гекс-поле 61 клітина: осьові/кубові координати, 6 напрямків, перевірка «в межах гексагона» — 🥉.
- Валідація групи (1–3 у ряд впритул) + in-line vs side-step — 📎.
- Sumito: підрахунок своїх і ворожих на промені, умови «затиснута / через проміжок / рівні сили» — 📎.
- Виштовхування за край як єдиний вид взяття + лічильник до 6 — 🌱.
- AI minimax з оцінкою «центр + згуртованість + вибулі» — 🥇 (велике розгалуження: десятки групових ходів).
- Альтернативні розстановки як дані (Daisy) — 🌱.

## Мапа на каталог
- Є: `push-object` ↔ sumito (тут з порівнянням сил) · `piece-capture` ↔ виштовхування · `legal-move-highlight` · `hot-seat`, `turn-enforcement`, `move-timer` · `ai-opponent`, `ai-minimax` · `cell-click`, `hover-highlight`, `drag-drop-piece` · `game-screen`, `main-menu`, `end-screen`, `help-window`, `settings-window`, `theme-select` · `replay`, `state-as-data`.
- **Нема** → пропозиції карток:
  - `+hex-grid-render` (див. hex.md) — шестикутна дошка-гексагон.
  - `+group-move` «Хід групою фігур» · entities/move · 📎 · слоти {max: 3, modes: [inline, broadside]}.
  - `+majority-push` «Штовхання чисельною перевагою» · entities/combat · 📎 · слоти {max_pusher: 3} — дитина `push-object`.
  - `+push-off-capture` «Взяття виштовхуванням за край» · entities/combat · 🌱.
  - `+capture-count-win` «Перемога за кількістю взятих» · game-logic/win · 🌱 · слоти {n: 6|10}.
  - `+board-layouts` (див. ataxx.md) — Standard / Daisy.
  - `+rule-variants` (див. lichess-variants.md) — Grand Abalone.

## Пропозиції до словників
- `+cond:outnumbers` — своїх у колоні більше, ніж ворожих підряд на тій самій лінії.
- `+effect:push_line` — зсунути ряд сутностей на 1 (Abalone, Sumo-вежі Kamisado).
- `+effect:move_group` — зсунути кілька фігур одним ходом в одному напрямку.
- `+ui:group-selection` — виділення групи; `+ui:direction-arrows` — вибір напрямку стрілками навколо групи.
- `+window:layout-select` — вибір стартової розстановки.
- `+axis:field-bounds` — край поля як смертельна зона, а не стіна.
- `+card:group-move`, `+card:majority-push`, `+card:push-off-capture`, `+card:capture-count-win` — див. «Мапа на каталог».

## Джерела
- ⭐ [UltraBoardGames: Abalone rules](https://www.ultraboardgames.com/abalone/game-rules.php) — колона, in-line і side-step, усі варіанти sumito і заборони, виштовхування, 6 для перемоги.
- [Wikipedia: Abalone](https://en.wikipedia.org/wiki/Abalone_(board_game)) — Lalet і Lévi (1987, видано 1990), 4,5 млн проданих, Daisy-розстановки (1999, MSO), Grand Abalone, Aba-Pro vs Nacre, онлайн-платформи.
- [Board Game Arena](https://en.boardgamearena.com/gamepanel?game=abalone) — гра в браузері.
- [PlayAbalone](https://www.playabalone.com), [PlayStrategy: аналіз](https://playstrategy.org/analysis/abalone), [Grand Abalone](https://playstrategy.org/variant/grandabalone) — лінки зі статті Wikipedia (не відкривав).
- [Steam: Abalone](https://store.steampowered.com/app/279480/Abalone/) — цифрове видання (сторінку не відкривав).
- YouTube: пошук «abalone board game how to play».

## Непевне
- (?) Заборона виштовхнути власну кульку за край — випливає з правил sumito, явно в джерелі не сказано.
- (?) Точна розстановка Standard / Belgian Daisy / German Daisy — у текстах лише діаграми; не описано по рядах.
- (?) Функції цифрових версій (рівні AI на Steam, підсвітка sumito) — не перевірено.
- (?) Правило з Wikipedia «якщо до 15-го ходу ніхто не виштовхнув — виграє той, хто ближче до центру» — незрозуміло, чий це регламент.
