---
title: Minesweeper Infinite
slug: minesweeper-infinite
aka: []
family: hidden-deduction
also: []
klass: cursor
axes:
  field: square
  time: static
  opponent: none
  info: hidden
  random: runtime
  goal: score
year: 2024
platforms: [PC (Windows / Steam)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2842090/", best: true, note: "Cobalt Code, 05.04.2024: нескінченне поле з чанків, Endless / Blitz / Time Trial / Survival / Classic до 128×128, Defusers, налаштування акорду"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Minesweeper+Infinite+Cobalt+Code+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [infinite-field, cell-click, chord-click, neighbor-count-clue, mode-select, time-out, event-points, field-size-picker, game-settings, controls-remap, theme-select, achievements-window, player-camera, field-scaling, game-screen, end-screen, settings-window, +flood-reveal, +chunk-generation, +defuser-token, +score-decay, +chunk-race]
proposes: ["+feature:mode-survival-decay", "+feature:mode-blitz", "+ui:defuser-counter", "+effect:flood_reveal", "+card:chunk-generation", "+card:defuser-token", "+card:score-decay", "+card:chunk-race"]
author: opus
date: 2026-11-09
---

# Minesweeper Infinite — сапер без меж: поле з чанків, що генеруються, поки ти йдеш далі

## Суть
Класичні правила сапера на нескінченному полі: числа рахують міни серед сусідів, міна — вибух. Поле складене з чанків — «будівельних блоків» поля, — і нові зʼявляються в міру просування. Гра дає «знешкоджувачі» за добру гру: такий жетон безпечно відкриває будь-яку клітину й прибирає міну, якщо вона там була, — відповідь на неминучі 50/50. Поверх нескінченного режиму — режими на час, на кількість чанків і з рахунком, що тане.

## Поле і час
- Квадратна сітка без меж; поле поділене на чанки фіксованого розміру (?), які генеруються на льоту — потрібна камера, що рухається полем.
- Classic — скінченне поле до 128×128.
- Час: у Endless і Classic статичний (нічого без кліку); Time Trial — відлік до кінця часу; Survival — рахунок спадає з часом; Blitz — секундомір до N чанків.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Закрита клітина | static | — | відкрити / прапорець |
| Число | mark | n = міни серед сусідів | підказка; акорд по числу (вимикається) |
| Міна | hazard | — | відкриття → вибух; наслідок у Endless (?) |
| Прапорець | mark | — | позначка міни; «flag chording» — акорд прапорцями |
| Чанк | zone | розмір (?) | блок поля, генерується при наближенні; одиниця прогресу Blitz |
| Defuser | pickup | лічильник жетонів | застосувати до клітини → безпечно відкрити; міна там — видаляється |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(open, c)` → ЯКЩО `cell(c, mine)` → ТО `explode(c)`, `custom: «наслідок залежить від режиму»` (?).
- КОЛИ `input(open, c)` → ЯКЩО `not cell(c, mine)` → ТО `reveal(c)` зі значенням `adjacent_count(c, mine)`.
- КОЛИ `after(reveal(c))` → ЯКЩО `adjacent_count(c, mine, ==, 0)` → ТО `custom: «flood reveal сусідів»` (?).
- КОЛИ `input(chord, n)` → ЯКЩО `mode(chording_on)` and `custom: «прапорців навколо = n»` → ТО `reveal(закриті незапрапорені сусіди)`.
- КОЛИ `input(flag, c)` → ТО `mark(c, flag)`.
- КОЛИ `custom: «камера/відкриття наближається до межі згенерованого»` → ТО `custom: «згенерувати сусідній чанк»`.
- КОЛИ `custom: «чанк повністю розвʼязано»` → ТО `counter(chunks, +1)`, `score(n)` (?).
- КОЛИ `custom: «серія добрих ходів»` → ТО `give(player, defuser)`.
- КОЛИ `input(defuse, c)` → ЯКЩО `has(player, defuser)` → ТО `take(player, defuser)`, `reveal(c)`; ЯКЩО `cell(c, mine)` → ТО `set_cell(c, empty)`.
- КОЛИ `counter(chunks, >=, N)` → ЯКЩО `mode(blitz)` → ТО `win`, `timer(stop)`.
- КОЛИ `counter(time_left, <=, 0)` → ЯКЩО `mode(time_trial)` → ТО `custom: «кінець, рахунок фіксується»`.
- КОЛИ `tick` → ЯКЩО `mode(survival)` → ТО `score(-k)`; КОЛИ `counter(score, <=, 0)` → ТО `lose` (?).
- Перемога: Blitz — N чанків; Classic — усі безпечні клітини. · Поразка: міна / час / рахунок до нуля. · Рахунок: очки в Time Trial і Survival (формула не опублікована).

## Керування і ввід
- Миша: відкрити, прапорець, акорд; кнопки миші можна поміняти місцями.
- Акорд вимикається в налаштуваннях; окремо — акорд прапорцями (flag chording).
- Застосування Defuser — окрема дія (?).

## Вікна, меню, HUD
- `mode-select`: Endless (за замовчуванням), Blitz, Time Trial, Survival, Classic.
- `game-screen`: поле з камерою, `score`, `timer-countdown` / `timer-elapsed` за режимом, `defuser-counter`.
- `settings-window`: візуальні теми, вигляд прапорців, акорд і flag chording, обмін кнопок миші.
- `end-screen` з рахунком; `achievements-window` (Steam).

## Фічі поза полем
- `mode-endless`, `mode-time-attack`, `mode-classic` + `custom-difficulty` (до 128×128), Blitz і Survival.
- `remap-controls` (обмін кнопок), `theme-select`, `achievements`.
- Демо-версія в Steam.

## Варіації й родичі
- [minesweeper](minesweeper.md) — скінченний оригінал; [endless-mines](endless-mines.md) — нескінченність у часі (рядки зникають); [globesweeper](globesweeper.md) — поле без меж, але скінченне.
- Теорія: нескінченний сапер Тюрінг-повний (згадано в minesweeper).
- Осі варіацій: **нескінченність** — у просторі (чанки) / у часі (рядки, що зникають) / тор; **рятівник від 50/50** — нема / no-guess генерація / жетон-знешкоджувач; **тиск** — нема / таймер / спадний рахунок.

## Цікавинки для курсу
- Генерація поля чанками за координатами (seed + хеш чанка → детермінована розкладка) — 🥈: лінива генерація, словник чанків.
- Числа на межі чанків: сусід може бути в ще не згенерованому чанку — генерувати сусідів наперед — 🥉.
- Defuser як нагорода й рятівник від вгадування — 📎.
- Survival зі спадним рахунком — 🌱; Blitz «N чанків на час» — 🌱.
- Камера по нескінченному полю + рендер лише видимого — 🥉.

## Мапа на каталог
- Є: `infinite-field` ↔ нескінченне поле · `cell-click` · `chord-click` · `neighbor-count-clue` · `mode-select` ↔ 5 режимів · `time-out` ↔ Time Trial · `event-points` ↔ очки · `field-size-picker` ↔ Classic до 128×128 · `game-settings` · `controls-remap` ↔ обмін кнопок · `theme-select` · `achievements-window` · `player-camera` + `field-scaling` ↔ рух полем · `game-screen` · `end-screen` · `settings-window`.
- **Нема** → пропозиції карток:
  - `+chunk-generation` «Ліниве генерування поля чанками» · levels/generation · 🥈 — дитина `infinite-field` для двовимірного поля.
  - `+defuser-token` «Жетон безпечного відкриття» · entities/state · 📎.
  - `+score-decay` «Рахунок тане з часом» · game-logic/score · 🌱.
  - `+chunk-race` «Розвʼязати N блоків на час» · game-logic/win · 🌱.
  - `+flood-reveal` — повтор пропозиції з minesweeper.

## Пропозиції до словників
- `+feature:mode-survival-decay` — режим, де ресурс/рахунок спадає і треба його поповнювати.
- `+feature:mode-blitz` — пройти фіксований обсяг якомога швидше (відрізняється від `mode-time-attack`, де обсяг за час).
- `+ui:defuser-counter` — лічильник рятівних жетонів.
- `+effect:flood_reveal` — повтор для правила трьох.

## Джерела
- ⭐ [Steam: Minesweeper Infinite](https://store.steampowered.com/app/2842090/) — Cobalt Code, 05.04.2024; «endless mine field», чанки як блоки поля, режими Endless / Blitz / Time Trial / Survival / Classic (до 128×128), Defusers, теми, акорд і flag chording, обмін кнопок, досягнення, демо.
- YouTube: пошук «Minesweeper Infinite Cobalt Code gameplay».

## Непевне
- (?) Що стається після вибуху в Endless (кінець забігу, штраф, блокування чанка) — не описано.
- (?) Розмір чанка, формула очок, умова отримання Defuser («consistent good play») — не розкриті.
- (?) Каскад нулів і перший безпечний клік — не згадані, але очікувані.
- (?) Поразка в Survival при нулі — виведено з опису «score decays».
