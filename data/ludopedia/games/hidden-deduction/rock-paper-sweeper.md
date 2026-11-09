---
title: Rock Paper Sweeper
slug: rock-paper-sweeper
aka: [RPS, Камінь-ножиці-сапер]
family: hidden-deduction
also: [pencil-logic]
klass: cursor
axes:
  field: square
  time: static
  opponent: none
  info: hidden
  random: setup
  goal: state
year: 2026
platforms: [web (HTML5, PICO-8)]
links:
  - {kind: itch, url: "https://puleo.itch.io/rps", best: true, note: "грати в браузері; правила, daily, expert boards; коментар автора про «?» з 14 Minesweeper Variants"}
  - {kind: other, url: "https://puleo.itch.io/rps/devlog/1530524/upcoming-feature-expert-boards", note: "devlog: ~2700 випадкових і стільки ж daily дошок як 12-бітні seed-и, перевірені офлайн; 100 expert boards"}
  - {kind: other, url: "https://puleo.itch.io/rps/devlog/1527442/removal-of-auto-open", note: "devlog: чому прибрали авто-відкриття"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Rock+Paper+Sweeper+pico-8", note: "пошук; відео не знайдено"}
stage: v1
coverage: 75
mechanics: [cell-click, keyboard-controls, selection-highlight, neighbor-count-clue, no-guess-generation, level-solver, daily-puzzle, level-bank, puzzle-select, share-result, pencil-marks, combo-multiplier, completion-detection, save-progress, mode-indicator, event-effects, sound-effects, main-menu, pause-menu, end-screen, help-window, about-window, game-settings, +form-safety, +cyclic-dominance, +same-symbol-clue, +no-hint-tile, +surplus-display, +form-change-cost, +baked-seed-bank, +daily-lockout, +revealed-corners-start]
proposes: ["+cond:beats", "+feature:display-mode", "+feature:daily-lockout", "+ui:form-banner", "+ui:symbol-notes", "+window:tips-window", "+card:form-safety", "+card:cyclic-dominance", "+card:same-symbol-clue", "+card:no-hint-tile", "+card:surplus-display", "+card:form-change-cost", "+card:baked-seed-bank", "+card:daily-lockout", "+card:revealed-corners-start"]
author: opus
date: 2026-11-09
---

# Rock Paper Sweeper — сапер, де кожна плитка — камінь, папір або ножиці, а безпечність відкриття залежить від твоєї поточної форми

## Суть
Поле 6×6, під кожною плиткою — один із трьох символів. Гравець має **форму** (камінь, папір чи ножиці) і відкриває плитки; якщо під плиткою символ, що перемагає форму, — програш. Число на відкритій плитці — скільки її сусідів (з діагоналями) мають **той самий символ**, що й вона; частина плиток показує лише «?». Форму міняють, натиснувши на вже відкриту плитку іншого символу, — це коштує очок, тож гра — дедукція «які символи можливі тут» + вибір форми, якій вони не страшні. PICO-8, автор Gregory J. Puleo, натхнення — [dragonsweeper](dragonsweeper.md), [mamono-sweeper](mamono-sweeper.md), [14-minesweeper-variants](14-minesweeper-variants.md).

## Поле і час
- 6×6 = 36 плиток; рівно по 12 каменів, паперів і ножиць (генератор: 4 кути — усі три символи + один зайвий, решта 32 — по 11 мінус один для «зайвого»).
- Старт: 4 кутові плитки відкриті; генератор перездає, доки хоч один кут не має числа 0 або 3.
- Статичний пазл; таймер іде з першого відкриття, лише для результату.
- Шари плитки: символ (прихований) · відкрита / закрита · число або «?» · нотатки R/P/S.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець-форма | player | rock / paper / scissors / ще не обрано | визначає, які плитки безпечно відкривати |
| Курсор | player | клітина | рух стрілками; до вибору першої форми стрибає між кутами (крок 5) |
| Плитка «камінь» | tile | символ | перемагає ножиці |
| Плитка «ножиці» | tile | символ | перемагають папір |
| Плитка «папір» | tile | символ | перемагає камінь |
| Число | mark | 0–8 сусідів того ж символу | підказка; тьмяніє, коли всі сусіди відкриті |
| «?» | mark | без числа | ≈30 % внутрішніх плиток випадкових дошок; може приховувати й нуль |
| Нотатка | mark | R / P / S | гравцеві мітки «який символ можливий» на закритій плитці |
| Плитка-вбивця | mark | — | плитка, що спричинила поразку, підсвічена |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `reveal(4 corners)`, `custom: «форму не обрано»`.
- КОЛИ `input(confirm, t)` → ЯКЩО `state(t, revealed)` і `not same(t, form, symbol)` → ТО `set_state(player, form)` (форма = символ t), `sound(form)`, `set_state(player, grace)`.
- КОЛИ `input(confirm, t)` (зміна форми) → ЯКЩО `not state(player, grace)` → ТО `counter(combo, -2)`.
- КОЛИ `input(confirm, t)` → ЯКЩО `not state(t, revealed)` і `state(player, has_form)` → ТО `reveal(t)`, `timer(start)` при першому, `score(+combo)`, `counter(combo, +1)`, `clear_state(player, grace)`.
- КОЛИ `after(reveal(t))` → ЯКЩО `custom: «символ t перемагає форму: камінь > ножиці > папір > камінь»` (`+cond:beats`) → ТО `lose`, `mark(t, killer)`, `custom: «тряска екрана»`.
- КОЛИ `after(reveal(t))` → ЯКЩО `not state(t, no_hint)` → ТО `set_value(t, n)` — n = сусіди того ж символу серед 8 (закритих і відкритих); інакше `mark(t, ?)`.
- Режим «show surplus»: показ «+N», де N = n − відкриті сусіди того ж символу; закритих сусідів нема → «-».
- КОЛИ `counter(revealed, ==, 36)` → ТО `win`, `reveal(all)`, `custom: «відблиск по плитках»`, зберегти статус daily / expert.
- КОЛИ `input(notes, t)` → ЯКЩО `not state(t, revealed)` → ТО `set_state(input, notes)`; стрілки → `mark(t, R|P|S)` / `unmark`; повторне натискання — вихід.
- КОЛИ `input(daily)` → ЯКЩО `custom: «сьогоднішній daily уже виграно або програно»` → ТО `block`, меню показує «daily in hh:mm».
- КОЛИ `input(share_daily)` → ТО `custom: «текст у буфер: дата + час і очки (або "Paper covered rock after m:ss" + скільки з 36 відкрито)»`.
- Гарантія: усі дошки (random, daily, expert) розвʼязні дедукцією без вгадувань — перевірено офлайн солвером.
- Перемога: відкриті всі 36. · Поразка: відкрита плитка, що б'є поточну форму. · Рахунок: сума combo за відкриття (1 + 2 + 3 …), кожна зміна форми −2 до combo (дві зміни поспіль без відкриття — штраф раз).

## Керування і ввід
- PICO-8: стрілки — курсор; ❎ (X) — на закритій: відкрити, на відкритій: прийняти її форму; 🅾️ (Z/C) — режим нотаток на закритій плитці, стрілки перемикають R/P/S (точне призначення стрілок — (?)).
- Тач/мобільний — екранні кнопки PICO-8 (копіювання результату daily може не працювати).
- Пауза-меню PICO-8 (Enter/P): перемикач «show counts / show surplus», «endgame fx» вкл/викл.

## Вікна, меню, HUD
- `main-menu` (титул): random board · daily board (або «daily in hh:mm», «dailies expired») · expert boards · rules · tips · credits.
- `game-screen`: поле 6×6 карток; угорі `+ui:form-banner` «form of rock / paper / scissors» або «choose your first form»; курсор кольору форми; у режимі нотаток — банер підказки.
- `puzzle-select` «expert boards»: сітка 10×10 номерів 0–99 з галочками розвʼязаних.
- `help-window` «rules» — кілька сторінок тексту; `+window:tips-window` — очки й режими показу з живою ілюстрацією плиток.
- `about-window` «credits» — автор, шрифти, звуки, натхнення.
- `pause-menu` — системне меню PICO-8 з двома перемикачами.
- `end-screen` (спливне меню): заголовок перемоги/поразки, час; пункти show board · new board / share daily / next expert · main menu.
- Переходи: main-menu → game-screen → (36 або поразка) end-screen → game-screen / main-menu; main-menu → puzzle-select → game-screen.

## Фічі поза полем
- `daily-puzzle` із заблокованою повторною спробою до півночі (`+feature:daily-lockout`) і `share-result` у буфер.
- `puzzle-bank`: ~2700 випадкових дошок + стільки ж daily (до ≈2033) як 12-бітні seed-и + 100 expert boards явним форматом; прогрес expert — у cartdata (localStorage).
- `+feature:display-mode` (лічильники / залишок), `animation-toggle` (endgame fx).
- `rules-page`, `tips` (окремий екран порад).
- Авто-відкриття (auto-open) було в першій версії і прибране (devlog 18.05.2026): «затіняло дедукцію».

## Варіації й родичі
- [minesweeper](minesweeper.md) — одна категорія небезпеки; тут три, і небезпечність **відносна** (залежить від форми).
- [dragonsweeper](dragonsweeper.md), [mamono-sweeper](mamono-sweeper.md) — небезпека з рівнями, яку переживаєш при достатній силі; [14-minesweeper-variants](14-minesweeper-variants.md) — джерело «?»-плиток.
- [voltorb-flip](voltorb-flip.md), [hexcells](hexcells.md) — підказки, що рахують не міни, а властивість сусідів.
- Осі варіацій:
  - **що рахує число**: міни / суму рівнів / сусідів того ж символу (тут);
  - **небезпека**: абсолютна / відносна до стану гравця (форма);
  - **зміна стану**: вільна / платна (−2 combo, тут) / обмежена.

## Цікавинки для курсу
- Циклічна домінація камінь > ножиці > папір як таблиця `beats[form] = symbol` — 🌱.
- Підказка «скільки сусідів мають мій символ» + «?»-плитки: генератор і перевірка розвʼязності для трьох типів — 🥇.
- Режим «surplus»: число мінус уже відкриті того ж символу — 📎.
- Combo-очки зі штрафом за зміну форми й пільгою на дві зміни поспіль — 📎.
- Банк дошок як seed-и, перевірені офлайн (бо PICO-8 не потягне генерацію з гарантією) — 🥉.
- Daily з блокуванням до півночі й текстом-результатом у буфер — 📎.
- Нотатки R/P/S на закритих плитках — 🌱 (картка `pencil-marks`).

## Мапа на каталог
- Є: `cell-click` + `keyboard-controls` · `selection-highlight` ↔ курсор кольору форми · `neighbor-count-clue` (варіант «того ж символу») · `no-guess-generation` + `level-solver` ↔ офлайн перевірка seed-ів · `daily-puzzle` · `level-bank` + `puzzle-select` ↔ 100 expert boards · `share-result` · `pencil-marks` ↔ нотатки R/P/S · `combo-multiplier` · `completion-detection` · `save-progress` ↔ cartdata · `mode-indicator` ↔ банер форми · `event-effects` ↔ тряска / відблиск · `sound-effects` · `main-menu` · `pause-menu` · `end-screen` · `help-window` · `about-window` · `game-settings`.
- **Нема** → пропозиції карток:
  - `+form-safety` «Безпечність відкриття залежить від стану гравця» · game-logic/constraints · 🥉 · слот {forms: list}.
  - `+cyclic-dominance` «Циклічна перемога типів (RPS)» · entities/interact · 🌱.
  - `+same-symbol-clue` «Число = сусіди того ж символу» · game-logic/constraints · 📎 (дитина `neighbor-count-clue`).
  - `+no-hint-tile` «Відкрита плитка без числа (?)» · game-logic/constraints · 🌱.
  - `+surplus-display` «Показ залишку замість повного числа» · interface/hud · 📎.
  - `+form-change-cost` «Зміна стану коштує очок» · game-logic/score · 🌱.
  - `+baked-seed-bank` «Банк перевірених seed-ів замість генерації на льоту» · levels/bank · 🥉.
  - `+daily-lockout` «Daily — одна спроба на день, таймер до півночі» · levels/bank · 🌱.
  - `+revealed-corners-start` «Старт із відкритими опорними клітинами» · levels/generation · 🌱.

## Пропозиції до словників
- `+cond:beats` — символ A перемагає B у циклічній таблиці (RPS).
- `+feature:display-mode` — перемикач подачі підказок (повне число / залишок); `+feature:daily-lockout` — повтор daily заборонено до півночі.
- `+ui:form-banner` — банер поточної форми/режиму вгорі; `+ui:symbol-notes` — три міні-позначки на закритій плитці.
- `+window:tips-window` — сторінка порад з живою ілюстрацією.

## Джерела
- ⭐ [itch.io: Rock Paper Sweeper](https://puleo.itch.io/rps) — правила (6×6, три форми, зміна форми, поразка від сильнішого символу, числа сусідів, без вгадувань), PICO-8, клавіатура/тач, коментарі про «?» (може бути нулем; ідея з 14 Minesweeper Variants); гра вбудована — з картриджа прочитано тексти rules / tips / credits, меню, генератор дошки, очки.
- [Devlog: expert boards](https://puleo.itch.io/rps/devlog/1530524/upcoming-feature-expert-boards) — ~2700 random + ~2700 daily дошок як 12-бітні seed-и, перевірені офлайн; план expert boards.
- [Devlog: expert boards are live](https://puleo.itch.io/rps/devlog/1534093/expert-boards-are-live) — 100 дошок, прогрес у localStorage.
- [Devlog: removal of auto-open](https://puleo.itch.io/rps/devlog/1527442/removal-of-auto-open) — авто-відкриття прибрано 18.05.2026.
- YouTube: пошук «Rock Paper Sweeper pico-8».

## Непевне
- (?) Точне призначення стрілок у режимі нотаток (символи кнопок PICO-8 у коді не прочиталися); розташування міток: R — зліва внизу, P — вгорі, S — справа внизу.
- (?) Частка «?»-плиток (≈30 %) — з коду генератора випадкових дошок; у expert boards вона задана явно для кожної дошки.
- (?) Дата першого релізу — найраніший devlog 13.05.2026 («Pre-release updates»).
