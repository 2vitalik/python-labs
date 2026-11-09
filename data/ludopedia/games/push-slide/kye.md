---
title: Kye
slug: kye
aka: [The Game of Kye, Python Kye, Kye 3.1, Xye]
family: push-slide
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: collect
year: 1992
platforms: [Windows 3.x, Linux (Python Kye), web (Kye 3.1), C64 (2022)]
links:
  - {kind: other, url: "http://www.kye.me.uk/description.html", best: true, note: "Playing Pieces: поведінка кожної фігури (слайдери, мармур, сентрі, магніти, таймери, чорні діри, двері, монстри)"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Kye_(video_game)", note: "історія, версії 1/2, поле 30×20, життя, паролі, редактори, ремейки"}
  - {kind: play, url: "https://playkye.com", note: "Kye 3.1 — ремейк і браузерна версія, 500+ рівнів, редактор"}
  - {kind: official, url: "http://games.moria.org.uk/kye/", note: "Python Kye (Colin Phipps)"}
  - {kind: other, url: "http://www.kye.me.uk/jumping.html", note: "перехід між рівнями за назвою в різних версіях"}
  - {kind: other, url: "https://xye.sourceforge.net/home.php", note: "Xye — розширений клон із новими елементами"}
  - {kind: itch, url: "https://cobbpg.itch.io/kye-c64", note: "порт на Commodore 64 (2022)"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=is-9SjYr_WE", note: "Kye — Introduction (посилання з kye.me.uk)"}
stage: v1
coverage: 65
mechanics: [move-4dir, keyboard-controls, cell-click, push-object, pull-object, dig-terrain, item-pickup, collect-all, goal-counter, impassable-cells, roll-off-rounded, turn-when-blocked, chase-greedy, touch-death, player-death, one-way-cell, timed-despawn, spawner-entity, spawn-schedule, sequential-levels, level-password, level-select, in-game-editor, level-from-txt, cheat-codes, game-loop, +magnet-hold, +redirect-tile, +npc-pusher, +object-sink]
proposes: ["+effect:hold", "+effect:release", "+trigger:hit", "+role:magnet", "+feature:god-mode", "+card:magnet-hold", "+card:redirect-tile", "+card:npc-pusher", "+card:object-sink"]
author: opus
date: 2026-11-09
---

# Kye — збери всі діаманти на екрані, де все повзе саме: real-time Sokoban з магнітами, слайдерами й монстрами

## Суть
Зелена куля Kye ходить по екрану 30×20 і має зібрати всі діаманти. Поле живе в реальному часі: слайдери й «мармур» повзуть у своєму напрямку, сентрі відскакують і штовхають, таймери зникають, «гармати» плюються новими слайдерами, монстри женуться за Kye. Гравець лише ходить — але штовхає блоки, риє землю і через **магніти** може тягнути предмети, будуючи з цього механізми. На рівнях лише з блоками й магнітами виходить чистий покроковий Sokoban.

## Поле і час
- Один екран 30×20 клітин, одна сутність на клітину; зовнішня стіна рекомендована.
- Стіни мають кути — квадратні або **округлі**: мармур (rocky) обкочується довкола округлих.
- Час — тіки реального часу: обʼєкти рухаються самі, монстри ходять незалежно від гравця; швидкості різних типів — (?).
- Камера нерухома (весь рівень на екрані).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Kye | player | життя | рух 4 напрямки (у класиці й діагоналі через мишу (?)); штовхає, риє, збирає |
| Діамант | pickup | — | не штовхається, лише збирається; усі зібрані → рівень пройдено |
| Стіна | static | кут: квадратний / округлий | нерухома; округлий кут — мармур обкочується |
| Земля (soft block) | terrain | — | Kye знищує, заходячи; інших зупиняє |
| Квадратний блок | object | — | Kye штовхає, якщо за ним вільно; зупиняє монстрів, слайдерів, мармур |
| Круглий блок | object | — | як квадратний, але мармур обкочується довкола |
| Slider | object | напрям | рухається стрілкою до упору або доки не тримає магніт |
| Marble (rocky) | object | напрям | як slider, але обкочується довкола круглих обʼєктів (і інших мармурів), якщо є місце |
| Sentry (bouncer) | object | напрям | рухається вперед; на перешкоді розвертається; рухомий обʼєкт попереду зсуває на 1 |
| Магніт (sticker) | object | вісь H / V | тягне рухомі обʼєкти до своїх кінців і тримає їх; Kye сильніший — магніт іде за Kye |
| Clocker / Anticlocker | static | напрям обертання | slider/мармур, що вдарився, повертає на 90° |
| Таймер | object | 3–9 | лічильник спадає, на 0 зникає; часто «відпускає» монстрів |
| Чорна діра (blackie) | sink | — | ковтає все, що в неї заходить |
| Shooter (auto slider / auto rocky) | spawner | напрям | періодично випускає slider / мармур |
| Одностороння двері | gate | напрям | Kye проходить лише в один бік (у класиці напрям не видно) |
| Монстри: gnasher, blob, virus, spike, twister | enemy | — | усі однаково женуться за Kye; дотик — мінус життя |
| Tracker, Guard, Sploder (Kye 3.1) | enemy | — | tracker полює й руйнує монстрів на шляху; guard іде вздовж стін; sploder вибухає після 5 дотиків |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(kye, dir)`.
- КОЛИ `contact(kye, earth)` → ТО `disappear_b`, `move(kye, dir)`.
- КОЛИ `contact(kye, diamond)` → ТО `pickup`, `counter(diamonds, -1)`.
- КОЛИ `all_gone(diamond)` → ТО `win`, `next_level`.
- КОЛИ `contact(kye, block|magnet)` → ЯКЩО `free(cell_behind)` → ТО `push`; інакше `block`.
- КОЛИ `tick` → ЯКЩО `free(cell_ahead)` and not `state(slider, held)` → ТО `move(slider, facing)`.
- КОЛИ `blocked(marble)` → ЯКЩО `custom: «перешкода кругла, а клітина збоку й по діагоналі вільна»` → ТО `roll(marble)`.
- КОЛИ `custom: «slider/мармур вдарився в clocker»` → ТО `rotate(slider, ±90)`.
- КОЛИ `tick` → ЯКЩО `free(cell_ahead)` → ТО `move(sentry, facing)`; КОЛИ `blocked(sentry)` → ТО `push` (рухома перешкода на 1), `bounce(sentry)`.
- КОЛИ `adjacent(magnet_end, movable)` → ТО `custom: «притягнути до кінця й тримати»`; бокові сторони магніту нейтральні.
- КОЛИ `input(dir)` → ЯКЩО `adjacent(kye, magnet_end)` → ТО `move(kye, dir)`, `pull(magnet)` (Kye тягне магніт, а з ним — те, що він тримає).
- КОЛИ `timer(every)` → ТО `counter(timer_block, -1)`; КОЛИ `counter(timer_block, =, 0)` → ТО `disappear_a`.
- КОЛИ `enter(obj, black_hole)` → ТО `disappear_a`.
- КОЛИ `timer(every)` → ЯКЩО `free(cell_ahead)` → ТО `spawn_at(slider|marble, cell_ahead)`.
- КОЛИ `input(dir)` → ЯКЩО `cell(next_cell, door)` and not `custom: «напрям руху = напрям дверей»` → ТО `block`.
- КОЛИ `tick` → ТО `custom: «монстр крокує до Kye»` (жадібно (?)); блоки й магніти можуть його зупинити чи пришпилити.
- КОЛИ `contact(monster, kye)` → ТО `lives(-1)`; що далі з рівнем — (?).
- КОЛИ `counter(lives, =, 0)` → ТО `lose` (?).
- Перемога: зібрати всі діаманти рівня. · Поразка: монстр дістав Kye, життя скінчились. · Рахунок: нема (лише прогрес рівнів).

## Керування і ввід
- Клавіатура: стрілки — крок; утримання — безперервний рух (C64-порт покращив автоповтор джойстика).
- Миша: клік у бік, куди йти (?); у класиці є діагональний рух, Xye його прибрав.
- Меню рівня: ввести назву рівня, щоб перейти (паролі); рестарт (?).

## Вікна, меню, HUD
- `game-screen`: поле 30×20; HUD — запасні Kye (`lives`), назва рівня, підказка рівня (?).
- `level-password` (класика): поле для назви рівня; Python Kye — меню Level зі списком пройдених + ввід назви; Christmas Kye — лише досягнуті.
- `editor-window` (v2+): візуальний редактор одного рівня; Kye 3.1 / Python Kye — багаторівневі файли, гортання елементів колесом/бамперами, попередження «рівень без діамантів».
- `settings-window` (Kye 3.1): розблокувати всі рівні, god mode, нескінченні життя.
- `help-window` (Kye 3.1): опис обʼєктів (`codex-window`) і екран клавіш.
- `level-select` (Kye 3.1): списки рівнів з кнопкою редагування; пошук рівнів, зокрема K64.
- Переходи: старт → game-screen (перший рівень набору) → усі діаманти → наступний рівень.

## Фічі поза полем
- `levels-sequential` наборами (.kye-файл = кілька рівнів), перехід за назвою рівня (`level-password`).
- `level-editor`: v1 — лише текстовий редактор; v2 — візуальний для одного рівня; 3.1 і Python Kye — багаторівневі файли.
- Формат рівня — простий текст (`level-from-txt`); понад 500 рівнів спільноти.
- Kye 3.1: `assist-mode`-подібні god mode / нескінченні життя / усе відкрито (`cheat-codes`), прогресія рівнів, браузерна версія.
- Shareware: реєстрація пожертвою Save the Children → 20 додаткових рівнів.

## Варіації й родичі
- Версії: Kye 1.0 (01.1992), 2.0 (05.1992: таймери, чорні діри, гармати, односторонні двері, редактор), Christmas Kye, Dr Floyd's Kye, Python Kye, Xye (нові елементи, без діагоналі), Kye 3.1 (2020, tracker/guard/sploder), C64 (2022), tikuScape! (Android).
- Родичі: [sokoban](sokoban.md) (штовхання), Boulder Dash (земля, діаманти, обкочування круглого — тут без гравітації), Chip's Challenge, [adventures-of-lolo](adventures-of-lolo.md).
- Осі варіацій:
  - **хто штовхає**: лише гравець (Sokoban) / ще й NPC-сентрі (Kye);
  - **тяжіння**: вниз (Boulder Dash) / нема, кожен обʼєкт має свій напрям (Kye);
  - **як тягнути**: нема / магніт-посередник (Kye) / пряме тягнення (Pushmo);
  - **час**: покроково / real-time з власними тіками обʼєктів.

## Цікавинки для курсу
- Магніт: притягнути й тримати сусідів на кінцях осі, нейтральні боки, «Kye сильніший» — 🥉.
- Мармур, що обкочує круглі кути й обʼєкти (вибір боку, перевірка двох клітин) — 📎.
- Порядок оновлення в тіку: хто рухається першим, коли слайдер і монстр претендують на одну клітину — 🥉.
- Сентрі — NPC, що штовхає: механізми з обʼєктів, які штовхають один одного — 🥉.
- Гармата + чорна діра як джерело й стік потоку обʼєктів (конвеєр без конвеєра) — 📎.
- Рівень як текстова мапа 30×20 з символом на тип — 🌱.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` + `cell-click`; `push-object`; `pull-object` ↔ тягнення через магніт; `dig-terrain` ↔ земля; `item-pickup` + `collect-all` + `goal-counter` ↔ діаманти; `impassable-cells`; `roll-off-rounded` ↔ мармур (тут без гравітації); `turn-when-blocked` ↔ сентрі; `chase-greedy` ↔ монстри; `touch-death` + `player-death` ↔ життя; `one-way-cell` ↔ двері; `timed-despawn` ↔ таймер; `spawner-entity` + `spawn-schedule` ↔ гармати; `sequential-levels` + `level-password` + `level-select`; `in-game-editor` + `level-from-txt`; `cheat-codes` ↔ god mode; `game-loop` ↔ real-time тіки.
- **Нема** → пропозиції карток:
  - `+magnet-hold` «Магніт притягує й утримує рухомі обʼєкти на кінцях осі» · entities/interact · 🥉 · слот {axis, range}.
  - `+redirect-tile` «Плитка, що повертає рухомий обʼєкт на 90° при ударі» · entities/move · 🌱 · слот {cw|ccw}.
  - `+npc-pusher` «Неігровий обʼєкт штовхає інші» · entities/legality · 📎.
  - `+object-sink` «Клітина ковтає все, що в неї заходить» · entities/interact · 🌱.

## Пропозиції до словників
- `+effect:hold` / `+effect:release` — магніт утримує / відпускає обʼєкт (у реченні — `custom`).
- `+trigger:hit(a, b)` — рухомий A вдарився в B (clocker, сентрі); `contact` описує вхід у клітину, тут клітина не спільна.
- `+role:magnet` — сутність з полем притягання (відрізняти від `object`).
- `+feature:god-mode` — безсмертя як налаштування (Kye 3.1); ближче до `assist-mode`.
- `+card:magnet-hold`, `+card:redirect-tile`, `+card:npc-pusher`, `+card:object-sink`.

## Джерела
- ⭐ [kye.me.uk: Playing Pieces](http://www.kye.me.uk/description.html) — поведінка кожної фігури: земля, блоки, слайдер, мармур, сентрі, магніт, clocker, таймер 3–9, чорна діра, гармати, двері, монстри.
- [Wikipedia: Kye (video game)](https://en.wikipedia.org/wiki/Kye_(video_game)) — автор Colin Garbutt, версії 1/2, 30×20, 4 життя, паролі, редактори, ремейки.
- [playkye.com — Kye 3.1](https://playkye.com) — ремейк, нові обʼєкти tracker/guard/sploder, налаштування, редактор.
- [Python Kye](http://games.moria.org.uk/kye/) — клон, що зберігає поведінку оригіналу.
- [kye.me.uk: Jumping Levels](http://www.kye.me.uk/jumping.html) — перехід між рівнями за назвою.
- [Xye](https://xye.sourceforge.net/home.php), [Kye C64](https://cobbpg.itch.io/kye-c64), [YouTube: Kye — Introduction](https://www.youtube.com/watch?v=is-9SjYr_WE).

## Непевне
- (?) Життя: Wikipedia — 4 на рівень (3 запасні Kye), kye.me.uk — «три життя»; що відбувається після втрати життя (рестарт рівня чи продовження з місця) і після останнього — не знайдено.
- (?) Радіус магніту: Wikipedia — «дві клітини вздовж осі», kye.me.uk — «одна клітина»; у правилах взято «сусідні».
- (?) Монстри «поводяться однаково» (kye.me.uk) — алгоритм переслідування (жадібний?) і швидкості обʼєктів у тіках не перевірено.
- (?) Tracker/Guard/Sploder — схоже, лише Kye 3.1 (чи були в класиці — не перевірено).
- (?) Призначення миші в класиці (клік-напрям) і діагональний рух.
