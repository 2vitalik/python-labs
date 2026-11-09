---
title: Meet me at NooN
slug: meet-me-at-noon
aka: [Meet me at Noon]
family: thinky
also: [grid-platformer]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2022
platforms: [PC, Mac, Linux, web]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1880490/Meet_me_at_NooN/", best: true, note: "опис механіки: два духи, запис ходів, денний перемотує назад, нічний повторює; таймлайн; 9 мов"}
  - {kind: itch, url: "https://pandaroointeractive.itch.io/meet-me-at-noon", note: "повна гра на itch; дії: вліво/вправо, стрибок угору, чекати вниз"}
  - {kind: play, url: "https://alex-pandaroo.itch.io/meet-me-at-noon-free-web-demo", note: "безкоштовне веб-демо"}
  - {kind: other, url: "https://ladiesgamers.com/meet-me-at-noon-review", note: "рецензія: таймлайн день/ніч, Нічний штовхає Денного, сині й золоті зірки, сузірʼя-розділи"}
  - {kind: other, url: "https://megavisions.net/mini-review-meet-me-at-noon-pc", note: "рецензія: Нічний повертається на старт і повторює; духи як платформа один для одного; падіння з уступу безповоротне"}
  - {kind: other, url: "https://www.comicsbeat.com/review-relax-with-the-timeless-puzzles-of-meet-me-at-noon", note: "рецензія: зворотний рух Денного вночі, легкий відкат по таймлайну"}
  - {kind: other, url: "https://2023.amaze-berlin.de/submissions/meet-me-noon", note: "A MAZE. Berlin 2023: «що, якби Tenet був пазлом»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Meet+me+at+NooN+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [move-by-input, keyboard-controls, gravity-fall, impassable-cells, move-limit, undo-unlimited, item-pickup, level-select, level-unlock, save-progress, language-picker, movement-animation, +time-clone-replay, +reverse-playback, +phase-alternating-control, +wait-turn, +actor-as-platform, +timeline-scrub, +bonus-star]
proposes: ["+effect:replay", "+effect:replay_reverse", "+ui:timeline-bar", "+feature:timeline-scrub", "+axis:turn-structure=phase-alternating", "+card:reverse-playback", "+card:phase-alternating-control", "+card:timeline-scrub"]
author: opus
date: 2026-11-09
---

# Meet me at NooN — покроковий платформер на двох духів: денний програє свої ходи назад, нічний — повторює з початку

## Суть
Великий пісковий годинник розбився на двох духів — Денного й Нічного. Рівень — бічна сітка з уступами; таймлайн унизу ділить ходи на денні й нічні. У денні ходи гравець веде Денного, у нічні — Нічного, і кожен хід записується: поки ведеш Нічного, Денний **перемотує** свій запис у зворотному порядку, а Нічний свій запис **повторює** від стартової точки. Мета — щоб наприкінці Денний стояв на сонці, а Нічний на місяці; взаємодії духів (поштовх, стояння один на одному) теж записуються й змінюють подальше відтворення. Програти не можна: помилка виправляється перемотуванням таймлайну.

## Поле і час
- Квадратна сітка, вид збоку, з гравітацією: уступи, урвища, платформи; падіння з уступу назад не відіграти (стрибок лише на одну клітину вгору (?)).
- Покроково: хід = одна дія активного духа; таймлайн показує, скільки ходів має рівень і які з них денні (сонце), які нічні (місяць).
- Пізніші рівні чергують денні й нічні відрізки кілька разів, тож записи обох духів відтворюються більше одного разу.
- Неактивний дух не стоїть: він виконує запис — Денний задом наперед, Нічний з початку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Денний дух | player | запис денних ходів | ходить у денні ходи; у нічні — відтворює свій запис у зворотному порядку |
| Нічний дух | player | запис нічних ходів | ходить у нічні ходи; поза ними — вертається на старт і повторює запис уперед |
| Сонце | zone | — | ціль Денного |
| Місяць | zone | — | ціль Нічного |
| Золота зірка | pickup | необовʼязкова | бонус за рівень; взяти, провівши духа через неї |
| Блок / уступ | static | — | тверда клітина, на якій стоять; непрохідна |
| Порожнеча | terrain | — | падіння, доки нема опори |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ЯКЩО `turn_of(active)` and `free(next_cell)` → ТО `move(active, dir)`, `custom: «дію записано в таймлайн духа»`.
- КОЛИ `input(up)` → ТО `custom: «стрибок угору (?) — записується як дія»`.
- КОЛИ `input(down)` → ТО `pass_turn`, `custom: «очікування теж записується»`.
- КОЛИ `turn_end(active)` → ЯКЩО `not supported(spirit)` → ТО `fall(spirit)`.
- КОЛИ `phase_start(night)` → ТО `custom: «керування переходить до Нічного; Денний щоходу виконує свій денний запис від кінця до початку»`.
- КОЛИ `phase_start(day)` (повторний відрізок) → ТО `teleport(night, start)`, `custom: «Нічний повторює нічний запис від початку»` (?).
- КОЛИ `contact(night, day)` → ЯКЩО `free(cell_behind)` → ТО `push` (Денного), `custom: «подальший зворотний запис Денного грає від нової позиції»`.
- КОЛИ `custom: «дух стоїть на голові іншого або перегородив йому шлях»` → ТО `custom: «нижній — платформа, передній — стіна: не дає впасти з урвища»`.
- Зворотне відтворення Денного може йти «проти гравітації» (рецензія) — як саме зворотний стрибок і падіння, (?).
- КОЛИ `contact(spirit, gold_star)` → ТО `pickup`, `counter(gold_stars, +1)`.
- КОЛИ `level_end` → ЯКЩО `all_on(day, sun)` and `all_on(night, moon)` → ТО `win`, `counter(blue_stars, +1)`, `window(end-screen)`.
- КОЛИ `input(timeline_step)` → ТО `undo(n)` — перемотати таймлайн на будь-який крок і грати звідти.
- КОЛИ `counter(stars, >=, n)` → ТО `unlock(next_chapter)`.
- Перемога: обидва духи на своїх символах одночасно · Поразки нема, ліміту часу нема · Рахунок: синя зірка за проходження, золота — бонус.

## Керування і ввід
- Стрілки (і геймпад): ← → — крок, ↑ — стрибок, ↓ — чекати хід.
- Керується завжди той дух, чия зараз фаза на таймлайні; перемикання — автоматичне за таймлайном, не кнопкою.
- Відкат — перехід по таймлайну назад до потрібного кроку.

## Вікна, меню, HUD
- `main-menu` (?): гра, налаштування, вихід.
- `chapter-select`: розділи-«сузірʼя»; наступні відкриваються за кількість зірок.
- `level-select` у розділі: рівні з позначками синьої й золотої зірки.
- `game-screen`: поле збоку; символи сонця й місяця; золота зірка; HUD — `timeline-bar` (ходи з позначками день / ніч, поточний хід, записані дії), зміна дня й ночі анімацією фону.
- `end-screen`: «Next Level» / «Next Chapter».
- `settings-window` (?): мова (EN + 8), звук.
- Переходи: main-menu → chapter-select → level-select → game-screen → end-screen → наступний рівень.

## Фічі поза полем
- `undo` через таймлайн: перехід на будь-який крок (відкат замість поразки).
- `stars-rating`: синя за проходження + золота бонусна; зірки — валюта розблокування розділів (`level-unlock`).
- `achievements` (Steam), `cloud-save`; `localization` — 9 мов.
- Безкоштовне веб-демо на itch.

## Варіації й родичі
- Loophole (минулі «я» повторюють записані дії — `time-clone-replay`), Braid і Catrap (перемотування часу), The Lost Vikings (кілька героїв і стояння одне на одному), Cosmic Express / Snakebird (бічна сітка thinky).
- Натхнення — фільм «Tenet»: один герой іде вперед у часі, другий — назад.
- Осі варіацій:
  - **як відтворюється запис**: уперед із поточного місця (клон) / від старту знову (Нічний) / задом наперед (Денний);
  - **хто керований**: обидва по черзі за таймлайном (тут) / перемикання кнопкою / один, решта — записи;
  - **взаємодія з записом**: незмінний запис / запис зсувається від поштовху (тут) / парадокс при зустрічі (Loophole).

## Цікавинки для курсу
- Запис дій і відтворення вперед / назад для двох акторів на спільному таймлайні — 🥈.
- Зворотне відтворення дій із фізикою (обернений крок, стрибок, падіння) — 🥇 (що є «оберненою» дією при гравітації).
- Взаємодія з записом: поштовх змінює позицію, звідки грає решта запису (відносні дії, а не абсолютні позиції) — 🥈.
- Таймлайн як undo: перехід на будь-який хід перерахунком від початку — 📎.
- Зірки-валюта для розблокування розділів — 🌱.

## Мапа на каталог
- Є: `move-by-input` · `keyboard-controls` ↔ стрілки; `gravity-fall` ↔ падіння з уступів; `impassable-cells` ↔ блоки; `move-limit` ↔ довжина таймлайну; `undo-unlimited` ↔ перемотування таймлайну; `item-pickup` ↔ золота зірка; `level-select` · `level-unlock` ↔ розділи за зірки; `save-progress`; `language-picker`; `movement-animation`.
- **Нема** → пропозиції карток:
  - `+time-clone-replay` (уже в корпусі, Loophole) — Нічний повторює запис.
  - `+reverse-playback` «Відтворення записаних дій задом наперед» · game-logic/history · 🥇.
  - `+phase-alternating-control` «Фази таймлайну визначають, хто керований» · game-logic/opponent · 📎.
  - `+wait-turn` (уже в корпусі) — дія «чекати».
  - `+actor-as-platform` «Аватар — опора для іншого» · entities/legality · 📎.
  - `+timeline-scrub` «Перехід на будь-який крок таймлайну» · game-logic/history · 📎.
  - `+bonus-star` «Необовʼязкова зірка в незручному місці рівня» · levels/progression · 🌱.

## Пропозиції до словників
- `+effect:replay` — сутність виконує записані дії (уперед); `+effect:replay_reverse` — виконує їх у зворотному порядку.
- `+ui:timeline-bar` — смуга ходів із фазами день / ніч і поточним кроком.
- `+feature:timeline-scrub` — відкат переходом на крок таймлайну.
- `+axis:turn-structure=phase-alternating` — фази таймлайну чергують керованого актора.
- `+card:reverse-playback`, `+card:phase-alternating-control`, `+card:timeline-scrub` — див. вище.
- ⏳-слова, вжиті тут: `input`, `turn_end`, `phase_start`, `level_end`, `turn_of`, `free`, `supported`, `all_on`, `move`, `fall`, `pass_turn`, `teleport`, `counter`, `undo`, `unlock`, `window`.

## Джерела
- ⭐ [Steam: Meet me at NooN](https://store.steampowered.com/app/1880490/Meet_me_at_NooN/) — опис: одна дія за хід, два духи, запис і відтворення (денний перемотує, нічний повторює), мета — обидва на символах одночасно, «You can't lose», відкат по таймлайну; Pandaroo Interactive, 20.06.2022.
- [itch: Meet me at NooN](https://pandaroointeractive.itch.io/meet-me-at-noon) — дії: вліво / вправо, стрибок угору, чекати вниз; платформи.
- [itch: веб-демо](https://alex-pandaroo.itch.io/meet-me-at-noon-free-web-demo) — той самий опис дій.
- [LadiesGamers](https://ladiesgamers.com/meet-me-at-noon-review) — таймлайн день / ніч, ліміт кроків кожного духа, поштовх Нічним, сині й золоті зірки, сузірʼя-розділи за зірки.
- [Megavisions](https://megavisions.net/mini-review-meet-me-at-noon-pc) — Нічний вертається на старт, Денний грає назад; духи як платформа й стіна один для одного; падіння з уступу безповоротне; стрілки.
- [ComicsBeat](https://www.comicsbeat.com/review-relax-with-the-timeless-puzzles-of-meet-me-at-noon) — зворотний рух Денного вночі, відкат, «Next Level, Next Chapter».
- [A MAZE. Berlin 2023](https://2023.amaze-berlin.de/submissions/meet-me-noon) — задум «Tenet як пазл», запис змінюється від взаємодій.

## Непевне
- (?) Точна семантика кількох чергувань день / ніч: коли саме Нічний вертається на старт і чи Денний знову грає вперед після перемотування — джерела описують лише загально.
- (?) Як виглядає зворотний стрибок і зворотне падіння Денного («проти гравітації» — слова рецензії).
- (?) Чи може Денний штовхати Нічного (джерела кажуть лише про поштовх Нічним); чи перемогу перевіряють лише в останній хід таймлайну.
- (?) Кількість рівнів і розділів не вказана ні в магазині, ні в рецензіях; «міст» і «черепаха», про які питають у коментарях itch, — назви рівнів чи елементів, невідомо.
- (?) Меню й налаштування описано з загальних рис (мови, Steam Cloud), без скріншотів.
