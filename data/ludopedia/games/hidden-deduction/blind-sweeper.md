---
title: Blind Sweeper
slug: blind-sweeper
aka: [Сапер наосліп]
family: hidden-deduction
also: []
klass: cursor
axes:
  field: square
  time: static
  opponent: none
  info: hidden
  random: setup
  goal: state
year: 2026
platforms: [web (HTML5)]
links:
  - {kind: itch, url: "https://cubenape.itch.io/blind-sweeper", best: true, note: "грати в браузері; опис, правила, усі клавіші й жести прямо на сторінці гри; EN/FR"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Blind+Sweeper+cubenape+gameplay", note: "пошук; відео не знайдено"}
stage: v1
coverage: 70
mechanics: [cell-click, keyboard-controls, selection-highlight, mines-after-first-click, neighbor-count-clue, flood-reveal, remaining-counter, field-size-picker, difficulty-levels, game-settings, volume-control, language-picker, sound-effects, sound-volume, restart-level, help-window, settings-window, game-screen, confirm-dialog, +speech-announce, +spatial-audio-neighbors, +sonified-numbers, +neighbor-tour, +blind-mode, +screen-reader-output, +verbosity-levels, +jump-to-next-hidden, +edge-bump-sound, +post-game-mine-list, +tap-select-then-confirm]
proposes: ["+effect:speak", "+effect:spatial_sound", "+ui:spoken-caption", "+ui:last-announcement", "+feature:screen-reader-mode", "+feature:blind-mode", "+feature:verbosity", "+feature:voice-rate", "+window:size-menu", "+axis:output=audio", "+card:speech-announce", "+card:spatial-audio-neighbors", "+card:sonified-numbers", "+card:neighbor-tour", "+card:blind-mode", "+card:screen-reader-output", "+card:verbosity-levels", "+card:jump-to-next-hidden", "+card:edge-bump-sound", "+card:post-game-mine-list", "+card:tap-select-then-confirm"]
author: opus
date: 2026-11-09
---

# Blind Sweeper — класичний сапер, у який грають на слух: голос називає клітини, а сусіди звучать по колу навколо голови

## Суть
Звичайний [minesweeper](minesweeper.md) (міни, числа 8 сусідів, каскад нулів, прапорці, безпечний перший хід), перероблений під незрячого гравця. Курсор ходить стрілками, кожна клітина оголошується голосом («B3, 2»), кожна дія має свій звук; клавіша Enter програє «тур сусідів» — 8 коротких сигналів, розставлених у навушниках по колу навколо голови, і після кожного — слово. Зрячий може ввімкнути «blind mode», що ховає курсор і числа. Браузерна гра 2026 року (cubenape), зроблена з AI-асистентом як демонстрація доступних ігор.

## Поле і час
- Квадратна сітка з координатами шахового типу: стовпці A…, рядки 1…; курсор стартує на A1.
- Чотири розміри: Small 5×5 / 3 міни · Medium 8×8 / 10 · Large 12×12 / 25 · Expert 16×16 / 40.
- Статичний пазл; годинник стартує з першого відкриття й лише міряє час.
- Шари: приховане (міна / ні) + стан клітини (закрита / прапорець / відкрита з числом) + курсор. «Поле» для гравця — звукова мапа: стерео = стовпець, висота тону кроку = рядок.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Курсор | player | клітина (r, c) | рух на 1 стрілками; на краю — глухий подвійний «бум» |
| Закрита клітина | static | прихований вміст | відкривається пробілом; у турі — низький «тік» |
| Міна | hazard | — | відкрив — програш; ставиться після першого відкриття, ніколи не в нього |
| Число | mark | 0–8 мін серед 8 сусідів | у режимі «лише звуки» — нота, тим вища, чим більше число |
| Порожня (0) | mark | — | відкриває сусідів каскадом; у турі — «empty» |
| Прапорець | mark | — | ставиться/знімається; блокує відкриття; у турі — два високі «тіки» |
| Край | static | — | у турі — тиша / слово «edge»; при русі — «бум» |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` (у межах сітки) → ТО `move(cursor, dir)`, `sound(step: тон = рядок, панорама = стовпець)`, `custom: «озвучити координату й вміст ("C4 hidden")»`.
- КОЛИ `edge(cursor)` → ТО `block`, `sound(bump)`, `message(«Edge of the grid»)`.
- КОЛИ `input(reveal, c)` → ЯКЩО `first_time` → ТО `spawn_at(mine, random_cells_except_c)`, `timer(start)`.
- КОЛИ `input(reveal, c)` → ЯКЩО `state(c, flag)` → ТО `block`.
- КОЛИ `input(reveal, c)` → ЯКЩО `state(c, revealed)` → ТО `custom: «нічого, повідомити "already"»`.
- КОЛИ `input(reveal, c)` → ЯКЩО `occupied(c, mine)` → ТО `lose`, `sound(boom)`, `message(«Boom! Mine at C4. You lose.»)`, `custom: «спалах поля (крім blind mode)»`.
- КОЛИ `input(reveal, c)` → ЯКЩО `not occupied(c, mine)` → ТО `reveal(c)` (число = міни серед 8 сусідів), `sound(reveal)`; відкрилось більше однієї — додатковий «свуш».
- КОЛИ `after(reveal(c))` → ЯКЩО `adjacent_count(c, mine, ==, 0)` → ТО `reveal(neighbors8)` рекурсивно (прапорці не чіпає).
- КОЛИ `input(flag, c)` → ЯКЩО `not state(c, revealed)` → ТО `mark(c, flag)` / `unmark(c)` (перемикач), `sound(flag_on|flag_off)`; інакше `sound(buzz)`, `message(«Cell already revealed»)`.
- КОЛИ `input(tour)` → ТО `custom: «вміст клітини, тік-розділювач, далі 8 сусідів за годинниковою від верхнього: сигнал у просторі на позиції сусіда + слово hidden/flag/empty/N/edge»`; нижні сусіди звучать глухіше (фільтр) — підказка й на моно.
- КОЛИ `input(tour)` → ЯКЩО `mode(sounds_only)` → ТО `custom: «тур нотами без слів: число — нота вище для більшого, закрита — низький тік, прапорець — два високі, край — тиша»`.
- КОЛИ `input(neighbors)` (V) → ТО `message(«Hidden: up, up-right… Flags: left…»)` — напрямки закритих сусідів і прапорців.
- КОЛИ `input(next)` (N) → ТО `custom: «стрибнути до наступної закритої незапрапореної клітини по рядках, з переходом на початок»`, координата оголошується завжди.
- КОЛИ `input(mines)` (M) → ТО `message(mines − flags)`; ЯКЩО прапорців більше → ТО `message(«Too many flags: N more than mines»)`.
- КОЛИ `counter(revealed, ==, cells − mines)` → ТО `win`, `timer(stop)`, `sound(win)`, `message(«You win! … in 1 minute 12 seconds»)`.
- КОЛИ `input(list)` (L) → ЯКЩО `custom: «партію завершено»` → ТО `message(«Row 2: B, F. Row 5: A…»)` — де були міни; інакше «The game is not over yet».
- КОЛИ `input(restart)` → ЯКЩО `custom: «партія триває»` → ТО `custom: «попередити й чекати повторного R протягом 4 с»`; інакше `restart`.
- Перемога: усі безпечні клітини відкриті (прапорці не обовʼязкові). · Поразка: відкрита міна. · Рахунок: лише час партії.

## Керування і ввід
- Клавіатура: стрілки — рух; Space — відкрити; Alt або F — прапорець; Enter — тур сусідів; V — напрямки закритих/прапорців; N — наступна закрита; M — мін лишилось; T — час; R — рестарт; G — розмір сітки (меню: ↑↓ або 1–4, Space — так, Esc — скасувати); S — налаштування (←→ вибір, ↑↓ значення); L — міни після гри; H — довідка голосом; Esc — замовкнути; E — blind mode; P — голос вкл/викл; B — правила ще раз.
- Тач: дотик — вибрати й озвучити клітину; другий дотик тієї ж — відкрити; два швидкі дотики — прапорець; утримання — тур сусідів. Ряд екранних кнопок дублює всі дії.
- Вивід: власний голос гри (Web Speech) або екранний читач (VoiceOver, TalkBack, NVDA) через live-регіон; звуки — Web Audio з HRTF-панорамою.

## Вікна, меню, HUD
- `splash-screen` / старт: заголовок, «Start playing», «Test sound and voice», перемикач «оголошення через екранний читач», вибір мови EN/FR.
- `game-screen`: сітка з координатами, `cursor`, панель «Mines / Time / Grid / Status», `+ui:last-announcement` (останнє повідомлення текстом), ряд екранних кнопок дій (Reveal, Flag, Summary, Neighbors, Next hidden, Mines left, Time, Spoken help, Restart, Grid size, Settings, Show mines), перемикачі «Voice» і «Blind mode».
- `+window:size-menu` — голосове меню розміру сітки (4 пункти).
- `settings-window` — голосове: швидкість голосу 100–200 %, гучність 0–10, детальність Full / Short / Sounds only.
- `help-window` — таблиця клавіш і правила на сторінці + та сама довідка голосом (H, B).
- `confirm-dialog` — повторне R для рестарту під час партії (голосом, не модалом).
- `end-screen` не окремий: голосове повідомлення перемоги/поразки з підказкою «R — знову, G — інший розмір, L — де були міни».

## Фічі поза полем
- `difficulty-presets` = 4 розміри; `save-slots` нема, але налаштування й мова зберігаються в localStorage.
- `+feature:screen-reader-mode`, `+feature:blind-mode` (зрячий грає як незрячий), `+feature:verbosity` (повно / коротко / лише звуки), `+feature:voice-rate`, `volume-sliders`, `localization` EN/FR.
- `restart-level`, `rules-page`, `tutorial` (правила читаються вголос на першому старті).
- Нема undo, підказок, no-guess-генерації, рекордів.

## Варіації й родичі
- Ядро — [minesweeper](minesweeper.md) без змін; інша лише **модальність виводу**. Зворотний підхід — [mamono-sweeper](mamono-sweeper.md) blind-режим (ховає числа як ускладнення, а не як доступність).
- Осі варіацій:
  - **канал виводу**: зір / голос / звук без слів / екранний читач;
  - **як передано напрямок сусіда**: словами («up-right») / просторовим звуком / стереопанорамою за стовпцем;
  - **як передано число**: слово / висота ноти;
  - **навігація**: клік мишею / курсор стрілками / «стрибок до наступної закритої».

## Цікавинки для курсу
- Сонифікація поля: тон кроку з рядка, панорама зі стовпця, число → нота — 📎.
- «Тур сусідів»: послідовність 8 звуків з затримками, кожен на своїй позиції в 3D (HRTF) — 🥉.
- Озвучення через TTS з чергою реплік і перериванням (Esc), режим «екранний читач» через aria-live — 🥉.
- Рушій «чистих правил» без DOM (тестується під Node) окремо від звуку й рендеру — 📎 (картка `logic-render-split`).
- Тач-модель «дотик — вибрати, ще дотик — підтвердити, утримання — довідка» — 🌱.
- Blind mode як перемикач рендеру при тому ж стані — 🌱.

## Мапа на каталог
- Є: `cell-click` (тач) · `keyboard-controls` · `selection-highlight` ↔ курсор · `mines-after-first-click` · `neighbor-count-clue` · `flood-reveal` · `remaining-counter` ↔ M · `field-size-picker` + `difficulty-levels` ↔ 4 розміри · `game-settings` + `volume-control` + `sound-volume` · `language-picker` ↔ EN/FR · `sound-effects` · `restart-level` · `help-window` · `settings-window` · `game-screen` · `confirm-dialog` ↔ подвійне R.
- **Нема** → пропозиції карток:
  - `+speech-announce` «Голосове оголошення клітин і подій» · interface/sound · 🥉.
  - `+spatial-audio-neighbors` «Сусіди звучать з їхнього напрямку» · interface/sound · 🥉.
  - `+sonified-numbers` «Число як висота ноти» · interface/sound · 📎.
  - `+neighbor-tour` «Обхід 8 сусідів по колу з озвученням» · interface/input · 📎.
  - `+blind-mode` «Режим без картинки при тому ж стані» · interface/settings · 🌱.
  - `+screen-reader-output` «Оголошення через екранний читач (aria-live)» · interface/settings · 📎.
  - `+verbosity-levels` «Детальність повідомлень: повно / коротко / лише звуки» · interface/settings · 🌱.
  - `+jump-to-next-hidden` «Стрибок курсора до наступної закритої клітини» · interface/input · 🌱.
  - `+edge-bump-sound` «Звук упору в край поля» · interface/sound · 🌱.
  - `+post-game-mine-list` «Список мін по рядках після гри» · interface/results · 🌱.
  - `+tap-select-then-confirm` «Тач: перший дотик вибирає, другий діє» · interface/input · 🌱.

## Пропозиції до словників
- `+effect:speak` — озвучити текст голосом (TTS), окремо від `message` (текст на екрані).
- `+effect:spatial_sound` — звук із позицією в просторі (напрямок сусіда).
- `+ui:spoken-caption` — дубль голосу текстом на екрані; `+ui:last-announcement` — поле «останнє оголошення».
- `+feature:screen-reader-mode`, `+feature:blind-mode`, `+feature:verbosity`, `+feature:voice-rate` — доступність.
- `+window:size-menu` — голосове меню вибору сітки.
- `+axis:output=audio` — гра повністю грається без зору (вісь «канал виводу»: visual / audio / both).

## Джерела
- ⭐ [itch.io: Blind Sweeper](https://cubenape.itch.io/blind-sweeper) — опис («minesweeper you play by ear»), просторовий звук сусідів, безпечний перший хід, голос або екранний читач, клавіатура й тач, blind mode, EN/FR; гра вбудована: на сторінці гри — таблиця всіх клавіш, жести, правила, пояснення туру й режиму «Tones only»; з коду сторінки — 4 розміри сітки (5×5/3 … 16×16/40), швидкості голосу, налаштування.
- YouTube: пошук «Blind Sweeper cubenape gameplay» — відео не знайдено.

## Непевне
- (?) Точна дата релізу — сторінка itch показувала «4 days ago» на 2026-11-09, тобто ≈ 5 листопада 2026.
- (?) Чи є статистика/рекорди між сесіями — у коді бачив лише збереження налаштувань і мови.
- (?) Як звучить гра без навушників: моно-підказка «нижні сусіди глухіші» описана в коді, реальний ефект не перевіряв.
