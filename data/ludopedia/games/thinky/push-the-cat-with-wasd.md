---
title: Push The Cat with WASD
slug: push-the-cat-with-wasd
aka: [Push The Cat]
family: thinky
also: [push-slide, word-number]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2024
platforms: [PC, web]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2683570/", best: true, note: "опис: «story і texts — це пазл», літери W/A/S/D у тексті штовхають кота; підказки й розвʼязки; 13 челендж-рівнів"}
  - {kind: itch, url: "https://blinkhydrate.itch.io/push-the-cat", note: "джем-версія GMTK 2023 (20 рівнів, грати в браузері): клік по літерах, кнопка рестарту — теж обʼєкт"}
  - {kind: other, url: "https://www.4gamer.net/games/810/G081070/20240618034/", note: "4Gamer: текст з W/A/S/D рухається у свій бік, 13 челенджів, 3–4 год, натхнення Baba Is You"}
  - {kind: other, url: "https://steamcommunity.com/app/2683570/reviews/?browsefilter=toprated&l=english", note: "відгуки: QEZC — діагоналі, SHIFT, Ctrl-C/X/V, стрілки замість літер, 3 стилі"}
  - {kind: other, url: "https://blinkhydrate.itch.io/push-the-cat/devlog/751019/push-the-cat-with-wasd-is-out-now", note: "девлог релізу: «Player is not cat. Player is level.»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Push+The+Cat+with+WASD+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [cell-click, push-object, impassable-cells, reach-exit, move-4dir, move-8dir, sequential-levels, restart-level, undo-redo, achievements-window, theme-select, language-picker, +text-as-level, +actuator-pieces, +ui-as-object, +clipboard-objects, +direction-flip, +push-goal-to-target, +hint-reveal, +show-solution, +challenge-levels]
proposes: ["+role:pusher", "+effect:copy_to_buffer", "+effect:flip_dir", "+ui:glyph-style-toggle", "+card:text-as-level", "+card:actuator-pieces", "+card:clipboard-objects"]
author: opus
date: 2026-11-09
---

# Push The Cat with WASD — рівень — це сторінка оповіді, а літери W/A/S/D у ній штовхають кота до прапорця

## Суть
Гравець не кіт: гравець — рівень («Player is not cat. Player is level. Player push the cat»). Кожен рівень — абзац сюжетного тексту, і кожна літера W, A, S чи D у ньому — штовхач, що зсувається у «свій» бік клавіатури (W — вгору, A — ліворуч, S — вниз, D — праворуч) і штовхає все перед собою. Мета — загнати кота на ціль (або ціль на кота). Виросла з GMTK Game Jam 2023 (тема «roles reversed»); пряме натхнення — [Baba Is You](baba-is-you.md).

## Поле і час
- Поле — текст на екрані, розкладений по сітці знакомісць: слова — це ряди клітин-літер (відгук: «треба сканувати сітку, щоб знайти літери»).
- Покроково: один клік — один зсув однієї літери; часу нема.
- Розділи-історії + 13 окремих челендж-рівнів (Steam); основних рівнів у кілька разів більше, ніж 20 у джем-версії (4Gamer); 3–4 години (4Gamer).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кіт | object | — | пасивний: рухається лише від поштовху |
| Ціль (прапорець) | object | — | теж штовхається: можна «привезти ціль до кота» |
| Літера W / A / S / D | piece | напрям ↑ ← ↓ → | клік → зсув на 1 у свій бік, штовхає те, що попереду |
| Літера Q / E / Z / C | piece | діагональ | рух по діагоналі (відгук) |
| Решта тексту (літери, розділові знаки) | object | — | може бути зсунута штовхачем (?) |
| Кнопка рестарту, серце | object | — | елементи UI як фізичні обʼєкти; рестарт можна виштовхати за екран (джем) |
| SHIFT | piece | — | міняє літеру на протилежну або міняє місцями кота і ціль (відгук) |
| Ctrl-C / Ctrl-X / Ctrl-V | piece | — | копіює / вирізає обʼєкт і вставляє в місця Ctrl-V (відгук) |
| «Штовхачі»-відволікачі | piece | — | зайві літери, що не потрібні для розвʼязку (відгук) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, wasd_letter)` → ЯКЩО `free(cell_ahead)` → ТО `move(letter, letter_dir)`.
- КОЛИ `input(click, wasd_letter)` → ЯКЩО `occupied(cell_ahead, cat|goal|letter)` → ТО `push(next)`, `move(letter, letter_dir)`; ланцюг до упору → `block` (?).
- КОЛИ `input(click, qezc_letter)` → ТО `move(letter, diagonal)`.
- КОЛИ `contact(letter, cat)` → ЯКЩО `free(cell_behind)` → ТО `push(cat)`; інакше `block`.
- КОЛИ `contact(letter, goal)` → ТО `push(goal)`.
- КОЛИ `custom: «спрацював SHIFT»` → ТО `custom: «літера стає протилежною (W↔S, A↔D)»` або `swap(cat, goal)`.
- КОЛИ `custom: «спрацював Ctrl-C / Ctrl-X»` → ТО `custom: «обʼєкт копіюється / вирізається в буфер»`.
- КОЛИ `custom: «спрацював Ctrl-V»` → ТО `place(buffer, paste_cell)` — у кожне місце вставки (?).
- КОЛИ `edge(a)` → ТО `disappear(a)` — обʼєкт, виштовхнутий за екран, втрачено (джем: кнопка рестарту).
- КОЛИ `input(click, restart_button)` → ТО `restart`.
- КОЛИ `contact(cat, goal)` → ТО `win`, `next_level`.
- Перемога: кіт і ціль в одній клітині. Поразки нема; глухий кут → undo/рестарт. Рахунку нема.

## Керування і ввід
- Миша: клік по літері-штовхачу (джем-версія; для Steam відгук пише «letters move when you select them»).
- Клавіші W/A/S/D у назві — «реквізит»: у джемі клавіатура в тексті «натискається» мишею, ролі перевернуто.
- Перемикач відображення: літери ↔ стрілки, 3 стилі літер (відгук).
- Undo, redo, restart — обіцяні автором для повної версії (коментар на itch) (?).

## Вікна, меню, HUD
- `game-screen`: сторінка тексту-рівня з котом, ціллю й підсвіченими штовхачами.
- `hints-window`: підказка; окрема кнопка «показати розвʼязок» (Steam, 4Gamer).
- `settings-window`: стиль літер (текст / стрілки), мова (EN, 简体, 繁體, 日本語).
- `level-select` з розділами і окремим режимом Challenge (?).
- `achievements-window` (Steam Achievements).
- Переходи: розділ історії → рівні-абзаци → наступний абзац; Challenge — окремий набір з 13 рівнів.

## Фічі поза полем
- `hint`, `show-solution` — щоб пройти сюжет без застрягання (4Gamer).
- `undo`, `redo`, `restart-level` (?).
- `localization` (4 мови), `theme-select` ↔ 3 стилі літер, режим стрілок.
- Сюжет із ламанням четвертої стіни; челенджі як `mode-puzzle` для досвідчених.

## Варіації й родичі
- Джем-версія Push The Cat (GMTK 2023, 20 рівнів, HTML5) → Push The Cat with WASD (Steam, 2024) з сюжетом, новими механіками (діагоналі, SHIFT, буфер обміну) і підказками.
- Родичі: [Baba Is You](baba-is-you.md) (текст-обʼєкти), [One More Button](one-more-button.md) (керування як обʼєкти), Sokoban — «гравець є ящиком».
- **Осі варіацій**: хто рухається — аватар / сам рівень · штовхач — напрям-літера / діагональ / протилежна (SHIFT) · обʼєкти UI — декор / фізичні (рестарт можна втратити).

## Цікавинки для курсу
- Текст як поле: розкласти рядок у сітку, знайти літери-штовхачі — 🌱.
- Клік по штовхачу → зсув із ланцюговим штовханням — 📎.
- Ціль теж рухома: перемога = збіг двох рухомих клітин — 🌱.
- SHIFT (інверсія напрямку) і буфер Ctrl-C/X/V як ефекти над обʼєктами — 🥉 (копія сутності зі станом).
- Кнопка рестарту як обʼєкт, який можна втратити — 📎 (UI-шар і поле в одній моделі).
- Розвʼязувач BFS над станами «позиції літер + кіт + ціль» — 🥈.

## Мапа на каталог
- Є: `cell-click` ↔ клік по літері · `push-object` · `impassable-cells` · `reach-exit` ↔ кіт на цілі · `move-4dir`, `move-8dir` ↔ WASD і QEZC · `sequential-levels` · `restart-level`, `undo-redo` · `achievements-window` · `theme-select`, `language-picker`.
- **Нема** → пропозиції карток:
  - `+text-as-level` «Рівень — текст, літери — клітини» · levels/format · 📎.
  - `+actuator-pieces` «Клік по обʼєкту → він рухається у свій вбудований напрям і штовхає» · entities/move · 📎 · слоти {dirs}.
  - `+clipboard-objects` «Копіювати/вирізати/вставити обʼєкт поля» · entities/interact · 🥉.
  - `+ui-as-object` — див. one-more-button.md; `+direction-flip` (SHIFT: протилежна літера / обмін кота й цілі), `+push-goal-to-target`, `+hint-reveal`, `+show-solution`, `+challenge-levels`.

## Пропозиції до словників
- `+role:pusher` — сутність, що рухається у свій напрям за кліком і штовхає (літера W/A/S/D).
- `+effect:copy_to_buffer` — обʼєкт іде в буфер (копія або виріз), для `place` пізніше.
- `+effect:flip_dir` — напрям сутності стає протилежним (SHIFT).
- `+ui:glyph-style-toggle` — показ штовхачів літерою або стрілкою.
- `+card:text-as-level`, `+card:actuator-pieces`, `+card:clipboard-objects` — див. вище.

## Джерела
- ⭐ [Steam](https://store.steampowered.com/app/2683570/) — «A cat-pushing puzzle game where narratives are puzzle levels»; WASD у тексті штовхає кота; підказки й розвʼязки; 13 челенджів; GMTK 2023; мови.
- [itch.io, джем-версія](https://blinkhydrate.itch.io/push-the-cat) — 20 рівнів, клік по літерах мишею, «push the goal to the cat», рестарт можна виштовхати за екран; натхнення Baba Is You.
- [4Gamer](https://www.4gamer.net/games/810/G081070/20240618034/) — реліз 18.06.2024, «текст з W/A/S/D рухається у свій бік», 3–4 год, 13 челенджів, ціна.
- [Відгуки Steam](https://steamcommunity.com/app/2683570/reviews/?browsefilter=toprated&l=english) — QEZC, SHIFT, Ctrl-C/X/V, режим стрілок, 3 стилі, кнопки підказки й розвʼязку.
- [Девлог релізу](https://blinkhydrate.itch.io/push-the-cat/devlog/751019/push-the-cat-with-wasd-is-out-now) — «Player is not cat. Player is level.»
- YouTube: пошук «Push The Cat with WASD gameplay».

## Непевне
- (?) Як саме активується SHIFT і Ctrl-C/X/V — це слова в тексті, клавіші чи окремі обʼєкти; на що діють (кіт, літери, обидва).
- (?) Чи звичайні літери тексту штовхаються, чи є непрохідними; що відбувається на краю рядка.
- (?) Чи в повній версії є клавіатурний ввід крім кліку; чи є undo/redo/restart (обіцяно у коментарі автора).
- (?) Точна кількість основних рівнів не названа (лише «у кілька разів більше за 20»).
- Дата релізу: Steam — 17.06.2024, 4Gamer і девлог — 18.06.2024 (різниця часових поясів).
