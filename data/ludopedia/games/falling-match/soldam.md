---
title: Soldam
slug: soldam
aka: [ソルダム, "Soldam: Drop, Connect, Erase", そるだむ 開花宣言, Soldam FC]
family: falling-match
also: [chess-abstract]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: hotseat
  info: partial
  random: runtime
  goal: score
year: 1992
platforms: [arcade, Game Boy, NES, Switch, PS4]
links:
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ソルダム_(ゲーム)", best: true, note: "JA-вікі: правило перефарбування, Clear Soldam, режими, перешкоди Sekiro, боси, рімейк"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Soldam", note: "EN-стаття: 2×2 фруктів, перефарбування «як у Reversi», ряд одного кольору, релізи"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=soldam+jaleco+arcade+gameplay", note: "пошук; аркадний геймплей"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=soldam+drop+connect+erase+gameplay", note: "пошук; рімейк Switch/PS4"}
stage: v1
coverage: 70
mechanics: [gravity-fall, piece-rotate-flip, multi-cell-size, line-match-clear, progress-acceleration, difficulty-levels, mode-select, garbage-attack, simultaneous-versus, hot-seat, event-points, score-records, next-queue, end-screen, +sandwich-recolor, +mono-color-row-clear, +wildcard-tile, +color-weighted-spawn, +preview-hide-attack, +letter-collect-bonus, +recolor-guide]
proposes: ["+cond:sandwiched", "+card:sandwich-recolor", "+card:mono-color-row-clear", "+card:color-weighted-spawn", "+card:recolor-guide", "+role:wildcard"]
author: opus
date: 2026-11-09
---

# Soldam — падає квадрат 2×2 фруктів; «затиснуті» між двома однаковими перефарбовуються, як у Reversi

## Суть
Тетріс-подібна аркада Jaleco (спін-оф Rod Land, феї Tam і Rit): згори падає блок 2×2 з чотирьох фруктів різних кольорів. Коли він ляже, кожен ряд чужих фруктів, затиснутий між двома фруктами одного кольору **по вертикалі, горизонталі чи діагоналі**, перефарбовується в цей колір — правило Reversi на падаючих блоках. Горизонтальний ряд, повністю одного кольору, зникає і дає очки. Кінець — стакан до верху.

## Поле і час
- Стакан — прямокутна сітка; ширина/висота — (?). Блок 2×2 падає зверху real-time, швидкість росте з рівнем.
- Рівень у режимі Soldam — до 999; кількість кольорів росте з рівнем (EASY: 2 → 3 з рівня 10 → 4 з рівня 30).
- Інформація: видно поле і NEXT (наступний блок); бос Ujira може сховати NEXT.
- Нові кольори зважені в бік тих, що вже є на полі (не рівномірний рандом).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Блок 2×2 | piece | 4 фрукти, кольори з поточного набору | падає; обертається (?) і зсувається; лягає — 4 окремі фрукти |
| Фрукт | tile | колір (2–4 кольори) | може бути затиснутий і перефарбований; у ряду одного кольору зникає |
| Clear Soldam | tile | безбарвний | лишається після зникнення ряду, падає на дно; працює як «кінець» затискання; в аркаді зникає після одного вжитку, у рімейку — вічний |
| Sekiro | hazard | 2×2 куля | блокує перефарбування крізь себе; знімається двома повними рядами |
| Puchi Sekiro | hazard | 1×1 | те саме, знімається одним рядом |
| Decabura | piece | 2×2 одного кольору | дає 4 однакові фрукти; поруч із Sekiro / Puchi Sekiro перетворює їх на фрукти |
| Фрукти E·X·T·R·A | pickup | буква | зібрати (зникненням чи перефарбуванням) усі 5 → фея чистить поле й дає бонус |
| Боси Sekiro-режиму | boss | Crocowani, Ujira, Zosan, Bisonhord | бомба руйнує блок · вода ховає NEXT · трус прискорює падіння · блискавка робить блок Sekiro |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `timer(fall)` → ЯКЩО `free(cells_below)` → ТО `move(piece, down)`; інакше `custom: «блок лягає, 4 фрукти фіксуються»`.
- КОЛИ `input(left|right)` → ЯКЩО `free(cells_side)` → ТО `move(piece, dir)`.
- КОЛИ `input(rotate)` → ТО `rotate(piece, 90)` — кольори обертаються в квадраті (?).
- КОЛИ `locked(piece)` → ЯКЩО `custom: «ряд чужих фруктів затиснутий між двома фруктами кольору C по горизонталі, вертикалі або діагоналі»` → ТО `set_side(run, fruit_color)` — затиснуті фрукти беруть колір країв.
- Затискання діє від кожного з чотирьох щойно покладених фруктів (?) і не проходить крізь Sekiro / Puchi Sekiro.
- КОЛИ `pattern(row_full)` → ЯКЩО `custom: «усі фрукти ряду одного кольору»` → ТО `clear(row)`, `score(n)`, `spawn_at(clear_soldam, bottom)`.
- КОЛИ `custom: «Clear Soldam став краєм затискання»` → ТО `disappear_a` (аркада); у рімейку — лишається.
- КОЛИ `after(clear)` → ТО `fall(fruits_above)` (?).
- КОЛИ `counter(cleared_rows, >=, 2)` поруч із Sekiro → ТО `disappear(sekiro)`; Puchi Sekiro — 1 ряд.
- КОЛИ `adjacent(decabura, sekiro)` → ТО `transform(sekiro → fruits)`.
- КОЛИ `counter(extra_letters, ==, 5)` → ТО `clear(all)`, `score(bonus)`.
- КОЛИ `spawned(piece)` → ТО колір кожного фрукта — `custom: «зважено за кольорами на полі»`.
- VS: КОЛИ `clear(rows ≥ 2)` → ТО `send_garbage(opponent, n)`; розмір атаки показують феї (до 9). Гравець 1 чистить лише червоні ряди, гравець 2 — сині.
- Поразка: стакан заповнився і ряди не очищено. Режим Sekiro — перемога на 60-му поверсі вежі Mabuts.

## Керування і ввід
- Джойстик: вліво/вправо — зсув блока, вниз — прискорити (?); кнопка — поворот блока (?).
- Рімейк: опція «Guide» показує, як зміняться кольори, якщо блок ляже тут (перегляд перед ходом).
- Rakudamu (рімейк): без вільного падіння — блок опускаєш сам, тиску часу нема.

## Вікна, меню, HUD
- `game-screen`: стакан, `next-piece-preview`, `score`, рівень/поверх; у VS — два стакани й `garbage-meter` (феї).
- `mode-select`: Soldam / Sekiro / VS (аркада); Soldam / Rakudamu / Tsumedamu / Taiketsu (рімейк).
- `difficulty-select` (Soldam): EASY (рівень 1) / NORMAL (рівень 10, старт з 500 000) / HARD (рівень 30, старт з 2 000 000).
- `end-screen` — Game Over; `game-over-continue` (аркада).
- `puzzle-select` — 50 етапів Tsumedamu (рімейк).
- `codex-window` — енциклопедія форм істоти Plamy (рімейк).
- Переходи: mode-select → difficulty-select → game-screen → end-screen.

## Фічі поза полем
- `mode-endless` (Soldam), сюжетна вежа на 60 поверхів з босами (Sekiro), `mode-versus`.
- Рімейк: `mode-practice` (Rakudamu, нескінченно або 5 хв), `mode-puzzle` (Tsumedamu: фіксована кількість ходів і блоків), `online-multiplayer`, `codex` (Plamy змінює форму від певних очищень; набір форм відкриває фінал).
- `difficulty-presets` зі стартовими очками; `leaderboard-local`.

## Варіації й родичі
- Версії: аркада 1992 · Game Boy 1993 · NES (зроблено 1993, видано 2025 як Soldam FC) · рімейк Switch 2017 / PS4 2019 · Arcade Archives 2021.
- Родичі: Reversi/Othello (правило затискання — [chess-abstract]); [columns](columns.md), [puyo-puyo](puyo-puyo.md) (падаючі кольорові блоки); [tetris](tetris.md) (ряд зникає повним — тут ще й одного кольору).
- **Осі варіацій**: напрямки затискання (4 / 8) · вжиток прозорого краю (одноразовий / вічний) · правило ряду (повний / повний одного кольору / свій колір у VS) · кількість кольорів (фіксована / росте) · перегляд наслідків (нема / Guide).

## Цікавинки для курсу
- Перефарбування затиснутих по 8 напрямках від щойно покладених клітин — 📎 (Reversi-код, перенесений у стакан).
- Ряд зникає лише, коли весь одного кольору — 🌱 поверх Tetris-перевірки.
- Clear Soldam як «джокер-край» з одноразовим вжитком — 🌱.
- Спавн кольорів, зважений частотою кольору на полі — 🌱.
- «Guide» — превʼю перефарбування до приземлення (чиста функція над копією поля) — 📎.
- VS, де кожен чистить лише свій колір, і сміття феями — 🥉.

## Мапа на каталог
- Є: `gravity-fall` · `piece-rotate-flip` · `multi-cell-size` (2×2) · `line-match-clear` (ряд) · `progress-acceleration` · `difficulty-levels` · `mode-select` · `garbage-attack` · `simultaneous-versus` · `hot-seat` · `event-points` · `score-records` · `next-queue` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+sandwich-recolor` «Затиснуті між двома однаковими перефарбовуються» · entities/interact · 📎 · слоти {dirs: 4|8}.
  - `+mono-color-row-clear` «Ряд зникає, якщо весь одного кольору» · entities/interact · 🌱.
  - `+wildcard-tile` — підтверджую (Clear Soldam як нейтральний край).
  - `+color-weighted-spawn` «Колір нової частіше з наявних на полі» · entities/spawn · 🌱.
  - `+preview-hide-attack` «Атака ховає превʼю наступної» · game-logic/opponent · 🌱.
  - `+letter-collect-bonus` «Зібрати букви EXTRA» · game-logic/score · 🌱.
  - `+recolor-guide` «Превʼю наслідків приземлення» · interface/hud · 📎.

## Пропозиції до словників
- `+cond:sandwiched(run, color)` — ряд чужих затиснутий між двома своїми (Reversi, Soldam) — підтверджую.
- `+card:sandwich-recolor` — перефарбування за затисканням у падаючому стакані.
- `+card:mono-color-row-clear` — повний ряд одного кольору.
- `+card:color-weighted-spawn` — спавн кольорів, зважений станом поля.
- `+card:recolor-guide` — превʼю перефарбування (Guide).
- `+role:wildcard` — сутність-джокер, що підходить під будь-який колір/вид (Clear Soldam, wildcard Triple Town).

## Джерела
- ⭐ [JA Wikipedia: ソルダム (ゲーム)](https://ja.wikipedia.org/wiki/ソルダム_(ゲーム)) — затискання по 3 осях, Clear Soldam, кольори за рівнями, Sekiro-перешкоди, боси, VS (червоний/синій), рімейк і його режими.
- [EN Wikipedia: Soldam](https://en.wikipedia.org/wiki/Soldam) — суть, 2×2, ряд одного кольору, Game Over, релізи.
- YouTube: пошук «soldam jaleco arcade gameplay» · «soldam drop connect erase gameplay».

## Непевне
- (?) Розмір стакана і обертання блока — у джерелах нема.
- (?) Чи падають фрукти після зникнення ряду (гравітація всередині стакана) — ймовірно так, не підтверджено.
- (?) Затискання рахується від кожного з 4 нових фруктів чи від будь-якої пари на полі; чи є каскад перефарбувань.
- (?) Як саме Clear Soldam «падає на дно» — займає нижній ряд чи падає до опори.
- (?) Відмінності Game Boy-версії від аркади.
