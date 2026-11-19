---
title: Tres Undos
slug: tres-undos
aka: []
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2021
platforms: [web]
links:
  - {kind: itch, url: "https://knexator.itch.io/tres-undos", best: true, note: "грати в браузері; «Short puzzle game about orienting yourself in time»; натхнення — Braid і At the Hedges of Time; ~ відкриває редактор"}
  - {kind: other, url: "https://github.com/knexator/old_page/tree/master/undoTres_build", note: "вихідний код збірки (лінк автора в коментарях): undotres_v5.js — логіка часових ліній, levels_named.js — рівні з авторами"}
  - {kind: other, url: "https://knexator.itch.io/tres-undos/devlog/344048/player-pack-update", note: "девлог 06.02.2022: Player Pack з рівнів гравців, нові дошки над дірами й капелюхи; оригінал мав 17 рівнів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Tres+Undos+knexator", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [move-4dir, move-by-input, keyboard-controls, push-object, impassable-cells, fill-hole, reach-exit, undo-unlimited, restart-level, level-select, sequential-levels, save-progress, in-game-editor, editor-erase, editor-playtest, level-exchange, level-from-txt, +multi-level-undo, +undo-immune-objects, +undo-immune-avatar, +meta-undo, +immunity-pickup, +one-shot-cell, +undo-reopens-hole, +fall-into-hole-stuck, +undo-auto-skip-noop, +progressive-controls-unlock, +level-entry-exit-sides]
proposes: ["+trigger:undo", "+cond:immune", "+axis:undo", "+feature:multi-level-undo", "+card:multi-level-undo", "+card:undo-immune-objects", "+card:immunity-pickup"]
author: opus
date: 2026-11-19
---

# Tres Undos — Sokoban із чотирма клавішами undo різної глибини і статуями, яких не бере «мілке» скасування

## Суть
Покроковий Sokoban knexator-а, де головний інструмент — **undo кількох рівнів**: Z скасовує хід, X («really undo») скасовує й натискання Z, C — і натискання X, V — ще глибше. Кожна сутність має рівень імунітету: сіра статуя відкочується будь-яким undo, помаранчева ігнорує Z, червона — Z і X. Розвʼязок — зсунути статую, «відмотати» себе мілким undo, а статую лишити на місці, і так розплутати час.

Пізніше зʼявляються діри, дошки, що ламаються, знаки, які змінюють імунітет статуї, і капелюхи, що змінюють імунітет гравця.

## Поле і час
- Квадратна сітка, вигляд згори; кімнати основного пакета від 8×7 до 14×9 клітин, рівні гравців — до 18×14 (за текстом рівнів, разом зі стінами); у кожного рівня є сторона входу й сторона виходу.
- Шари: підлога / стіна / діра → дошка, знак-коло, капелюх → статуї й гравець.
- Покроково: хід = крок або натискання undo. Гра зберігає **часову лінію**: для кожного ходу — глибина undo (0 — звичайний хід, 1–4 — Z/X/C/V); стан сутності на поточному тіку обчислюється з цієї лінії за її імунітетом.
- Undo без меж у глибину історії; за початок рівня відмотати не можна.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | імунітет 0 (капелюх змінює) | 4 напрямки; штовхає статую на 1; може впасти в діру |
| Статуя сіра «1» | object | імунітет 0 | штовхається; відкочується будь-яким undo |
| Статуя помаранчева «2» | object | імунітет 1 | ігнорує Z |
| Статуя червона «3» | object | імунітет 2 | ігнорує Z і X |
| Статуя фіолетова «4» | object | імунітет 3 | відкочує лише V (рівні гравців) |
| Діра | hazard | відкрита / засипана статуєю | статуя засипає її; гравець падає й застрягає |
| Дошка над дірою | terrain | імунітет 0–3 | тримає, поки на ній є вага; щойно вагу знято — ламається |
| Знак-коло (sigil) | switch | імунітет 0–3 | статуя, заштовхана на нього, бере його рівень імунітету; знак зникає |
| Капелюх | pickup | імунітет 0–3 | гравець, що став на нього, бере його рівень імунітету |
| Стіна | static | — | непрохідна |
| Вихід | static | напрям виходу | стоїш на ньому й робиш крок назовні — наступний рівень |

## Правила (КОЛИ → ЯКЩО → ТО)
Хід:
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(player, dir)`; інакше `block`.
- КОЛИ `contact(player, statue)` → ЯКЩО `free(cell_behind)` → ТО `push(statue)`, `move(player, dir)`.
- КОЛИ `contact(player, statue)` → ЯКЩО `occupied(cell_behind, statue)` → ТО `block` — ланцюгом статуї не штовхаються.
- КОЛИ `enter(statue, hole)` → ТО `fall(statue)`, `custom: «діра засипана — по ній ходять»`.
- КОЛИ `enter(player, hole)` → ТО `fall(player)`, `set_state(player, stuck)` — далі кроки ігноруються, рятує лише undo.
- КОЛИ `leave(any, plank)` → ЯКЩО `custom: «на дошці був вантаж, а тепер нема»` → ТО `set_cell(plank, hole)`.
- КОЛИ `enter(statue, sigil)` → ТО `set_value(statue_immunity, sigil_level)`, `disappear(sigil)`.
- КОЛИ `enter(player, hat)` → ТО `set_value(player_immunity, hat_level)`, `disappear(hat)`.
- КОЛИ `input(dir)` → ЯКЩО `occupied(player_cell, exit)` і `moving(player, exit_dir)` → ТО `next_level`.
Час:
- КОЛИ `input(undo_d)` (Z=1, X=2, C=3, V=4) → ЯКЩО `custom: «імунітет сутності < d»` → ТО `undo(1)` для неї, `custom: «натискання мілкіших undo для неї — звичайні ходи, їх теж скасовано»`.
- КОЛИ `input(undo_d)` → ЯКЩО `custom: «імунітет сутності ≥ d»` → ТО `custom: «сутність лишається, де була»`.
- КОЛИ `after(undo)` → ЯКЩО `custom: «імунна сутність опинилась над дірою, яку щойно відкрито»` → ТО `fall(a)`.
- КОЛИ `after(undo)` → ЯКЩО `custom: «жодна сутність не змінилась»` → ТО `custom: «повторити той самий undo»`.
- КОЛИ `input(undo_d)` → ЯКЩО `custom: «довжина лінії до початку рівня < 1»` → ТО `block`.
- КОЛИ `input(restart)` → ТО `restart`.
- Перемога: гравець вийшов через вихід. · Поразка: нема — падіння в діру чи глухий кут лікує undo або рестарт. · Рахунку нема.

## Керування і ввід
- WASD / стрілки — крок; Z — undo; X — «really undo»; C — «really, really undo»; V — четвертий рівень (лише на рівнях із фіолетовими сутностями).
- R — рестарт; P / Esc — вибір рівня; ~ (Backquote) — редактор. Утримання клавіш undo повторює їх.
- Клавіші відкриваються поступово: R — на рівні «Don't reset yet» після кількох безуспішних undo, X — з 4-го рівня, C — з 8-го (за кодом).
- Свайпи на тач-екрані — у збірці є бібліотека свайпів (?).

## Вікна, меню, HUD
- `game-screen`: кімната; підказки керування намальовані на підлозі перших рівнів («WASD / Arrow Keys to Move», «Z to undo», «R to Reset», «X to really undo», «Recap: …»); HUD нема.
- `level-select`: дві сторінки — Main Pack (номери 1.0–4.0) і Player Pack; позначки пройдених; назва й автор рівня.
- `editor-window`: ЛКМ — стіна, ПКМ — стерти, E — діра, 1/2/3 — статуї, Shift+1/2/3 — знаки, Alt+1/2/3 — дошки, Shift+Alt+1/2/3 — капелюхи; поворот, віддзеркалення, зміна розміру; чернетки (зберегти / грати / видалити), експорт у текст.
- `end-screen`: «Thanks for Playing! — @knexator».
- Переходи: рівень → (вихід) → наступний рівень; P/Esc ↔ level-select; ~ ↔ editor-window.

## Фічі поза полем
- `undo` чотирьох глибин без ліміту історії, `restart-level`.
- `level-select` з прогресом у localStorage (приватний режим браузера може заважати).
- `level-editor` із чернетками й текстовим форматом рівня; рівні гравців (Discord, Twitter) зібрано в Player Pack.
- `onboarding-hints` — керування відкривається разом із рівнями, де воно вперше потрібне.

## Варіації й родичі
- Braid (зелені обʼєкти, імунні до перемотування) і At the Hedges of Time — автор називає їх джерелами ідей; Tres Undos дає імунітет **рівнями**.
- [Entwined Time](entwined-time.md) — окремі часові лінії персонажів і meta-undo; [Meet Me at Noon](meet-me-at-noon.md); [Catrap](../grid-platformer/catrap.md) — перемотування як механіка; [5D Chess](../chess-abstract/5d-chess.md); [Sokoban](../push-slide/sokoban.md).
- **Осі варіацій:** undo — один рівень / кілька вкладених рівнів (тут) / перемотування · хто імунний — ніхто / клас обʼєктів (Braid) / рівень на сутність, що змінюється в грі (знаки, капелюхи) · діра — смерть / застрягання до undo (тут) / засипка.

## Цікавинки для курсу
- Undo кількох глибин: лінія ходів із глибинами, пошук «оригінального тіку» з лічильником вкладених скасувань — 🥇.
- Статуї з різним імунітетом до undo — 🥉 (поверх стека станів окремо на кожну сутність).
- Знаки й капелюхи, що змінюють рівень імунітету посеред рівня — 📎.
- Дошка, що ламається, коли з неї зійшли, і її відновлення undo — 🌱.
- Undo відкриває діру під імунною сутністю — вона падає — 📎.
- Авто-повтор undo, якщо нічого не змінилось — 🌱.
- Редактор із чернетками й рівнем-рядком — 🥉.

## Мапа на каталог
- Є: `move-4dir`, `move-by-input`, `keyboard-controls` · `push-object` ↔ статуї · `impassable-cells` · `fill-hole` ↔ статуя в діру · `reach-exit` ↔ вихід · `undo-unlimited` · `restart-level` · `level-select`, `sequential-levels`, `save-progress` · `in-game-editor`, `editor-erase`, `editor-playtest`, `level-exchange` ↔ Player Pack · `level-from-txt` ↔ рівень-рядок.
- **Нема** → пропозиції карток:
  - `+multi-level-undo` «Undo кількох глибин: глибше скасовує й мілкіші undo» · game-logic/history · 🥇 · слоти {levels: 2..4}.
  - `+undo-immune-objects` «Обʼєкти, яких не бере undo свого рівня» · game-logic/history · 🥉 · слоти {immunity: 0..3}.
  - `+immunity-pickup` «Предмет або клітина змінює імунітет до undo» · entities/state · 📎.
  - `+one-shot-cell` (дошка над дірою, одноразова) · entities/legality · 🌱.
  - `+undo-reopens-hole` «Undo відкриває діру під імунним» · game-logic/history · 📎.
  - `+progressive-controls-unlock` «Клавіші відкриваються з рівнями» · interface/input · 🌱.

## Пропозиції до словників
- `+trigger:undo(level)` — гравець натиснув undo заданої глибини (повтор з інших файлів).
- `+cond:immune(a, level)` — імунітет сутності A не менший за глибину undo.
- `+axis:undo` — нове значення `layered`: кілька вкладених глибин undo.
- `+feature:multi-level-undo` — кілька клавіш undo різної глибини.
- `+card:multi-level-undo`, `+card:undo-immune-objects`, `+card:immunity-pickup` — див. вище.

## Джерела
- ⭐ [itch: Tres Undos](https://knexator.itch.io/tres-undos) — опис, натхнення (Braid, At the Hedges of Time), теги Sokoban / thinky / Time Travel; коментарі: «C — really, really undo», «V — triple really undo», ~ — редактор, лінк на код; автор: PuzzleScript не тягне таку систему undo.
- [Вихідний код](https://github.com/knexator/old_page/tree/master/undoTres_build) — `get_original_tick` (імунітет і глибини undo), `fallFlying` (падіння після undo), дошки `maybeBreakHoleCovers`, знаки й капелюхи міняють імунітет, `isWon` = гравець на виході, відкриття R/X/C за номером рівня, тексти підказок і редактора, 19 рівнів основного пакета + рівні гравців з авторами.
- [Девлог Player Pack](https://knexator.itch.io/tres-undos/devlog/344048/player-pack-update) — 17 рівнів у першому релізі, нові дошки («walk over a hole, but only once») і капелюхи.

## Непевне
- (?) Рік: коміти збірки — з листопада 2021, оновлення Player Pack — 06.02.2022; у черзі стоїть 2022. Точну дату першого релізу на itch не знайдено.
- (?) Точна кількість рівнів: 17 у релізі (девлог), у коді 19 рівнів автора (з фінальним) і 16 рівнів гравців.
- (?) Підтримка тач-свайпів — лише за кодом, у грі не перевірено.
