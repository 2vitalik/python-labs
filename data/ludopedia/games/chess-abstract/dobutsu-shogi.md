---
title: Dōbutsu shōgi (Звіряче шогі, Let's Catch the Lion!)
slug: dobutsu-shogi
aka: [Dobutsu shogi, Doubutsu shogi, どうぶつしょうぎ, Let's Catch the Lion!, Dobutsu, 3×4 shogi, Звіряче шогі]
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: state
year: 2008
platforms: [board, mobile, web, Switch, PS4]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dōbutsu_shōgi", best: true, note: "3×4, 4 фігури, дропи без обмежень, Catch і лев на дальньому ряду, повторення, розвʼязок Танаки 2009, варіанти Goro goro і 9×9"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/どうぶつしょうぎ", note: "JA: ходи, трай «пережити наступний хід», 千日手, історія видань 2008–2010, застосунки 2010–2019"}
  - {kind: play, url: "https://lishogi.org/variant/dobutsu", note: "Lishogi: правила варіанта Dobutsu, онлайн-гра, аналіз, редактор"}
  - {kind: other, url: "https://ludii.games/details.php?keyword=Let%27s%20Catch%20the%20Lion", note: "Ludii: автор Кітао Мадока, 2008, nestorgames, правила і нічия повторенням"}
  - {kind: other, url: "https://www.tanaka.ecc.u-tokyo.ac.jp/ktanaka/dobutsushogi/", note: "сторінка розвʼязку Танаки (лінк зі статті Wikipedia, не відкривав)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=dobutsu+shogi+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [piece-move-patterns, piece-capture, piece-drop, pocket, pawn-promotion, repetition-draw, legal-move-highlight, selection-highlight, last-move-highlight, cell-click, drag-drop-piece, hot-seat, turn-enforcement, ai-opponent, ai-minimax, online-multiplayer, level-solver, game-screen, main-menu, end-screen, help-window, tutorial-window, state-as-data, unit-tests, +king-capture-win, +reach-row-win, +dead-square-allowed, +royal-try, +retrograde-solver]
proposes: ["+cond:not_attacked_after", "+card:royal-try", "+card:retrograde-solver", "+card:dead-square-allowed"]
author: opus
date: 2026-11-09
---

# Dōbutsu shōgi — шогі 3×4 для дітей: зловити лева або завести свого на дальній ряд

## Суть
Мінімальне [шогі](shogi.md): у кожного 4 звірята, кожне ходить лише на 1 клітину, взяті фігури повертаються з руки на твій бік (дропи). Виграє той, хто **зловив** (взяв) лева суперника, або хто завів **свого** лева на дальній ряд так, що його не можна взяти наступним ходом. Гру вигадала професійна шогістка Кітао Мадока (LPSA) як вхід у шогі для дітей і дівчат; фігури намалювала Фудзіта Маїко. Гру повністю розвʼязано: за ідеальної гри виграє другий гравець.

## Поле і час
- Дошка 3 вертикалі × 4 горизонталі; свій перший ряд — «ліс», дальній ряд — «небо».
- Старт (від себе): на першому ряду слон — лев — жирафа (лев у центрі), курча — перед левом; суперник — дзеркально. Решта клітин порожні.
- Поза дошкою — рука кожної сторони з узятими фігурами.
- Покроково; хід = один крок фігурою **або** дроп з руки на порожню клітину.
- Перший хід — Sente (у діаграмі JA-вікі — жирні фігури); за розвʼязком перший гравець у програші.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Лев (ライオン) | piece | royal; ×1 | 1 клітина в 8 напрямках; не перетворюється |
| Жирафа (きりん) | piece | ×1 | 1 клітина ортогонально (тура на 1 крок) |
| Слон (ぞう) | piece | ×1 | 1 клітина по діагоналі (слон шахів на 1 крок) |
| Курча (ひよこ) | piece | ×1 | 1 клітина прямо вперед; бʼє так само |
| Курка (にわとり) | piece | перетворене курча | 1 клітина в усі боки, крім двох діагоналей назад (як золото шогі) |
| Рука | zone | лічильник за типом | узяті фігури; курка повертається в руку курчам |
| «Небо» (дальній ряд) | zone | 1 ряд | курча, що прийшло ходом, → курка; лев тут без шаху → перемога |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, piece, to)` → ЯКЩО `turn_of(side)` і `custom: «to — сусідня клітина за патерном фігури»` і `not occupied(to, own)` → ТО `move(piece, to)`, `end_turn`.
- КОЛИ `contact(piece, enemy_piece)` → ТО `disappear(enemy_piece)`, `give(side, kind)`; курка йде в руку як курча.
- **Catch** — КОЛИ `contact(piece, enemy_lion)` → ТО `win`.
- КОЛИ `reach(chick, last_rank)` → ЯКЩО `custom: «прийшло ходом, а не дропом»` → ТО `transform(chick, hen)`.
- КОЛИ `input(drop, kind, cell)` → ЯКЩО `has(side, kind)` і `free(cell)` → ТО `place(side, kind)`, `take(side, kind)`, `end_turn`.
- Обмежень дропу шогі **нема**: два курчати на вертикалі, мат дропом курчати, дроп курчати на дальній ряд — легальні.
- КОЛИ `after(place)` → ЯКЩО `custom: «курча скинуте на дальній ряд»` → ТО `custom: «не перетворюється і не має ходу, доки його не візьмуть»`.
- **Try** — КОЛИ `reach(lion, last_rank)` → ЯКЩО `not in_check(lion)` (`+cond:not_attacked_after`: суперник не може взяти лева наступним ходом) → ТО `win`.
- КОЛИ `reach(lion, last_rank)` → ЯКЩО `in_check(lion)` → ТО гра триває; суперник бере лева → `win` суперника.
- Лишити лева під шахом за оригінальними правилами **не заборонено**: `legal` шах не перевіряє, помилка карається «Catch».
- КОЛИ `repetition(3)` → ТО `draw`; вічний шах — теж нічия (на відміну від шогі).
- Пату не буває (JA-вікі): у кожної сторони завжди є хід.
- Перемога: Catch · Try · Нічия: триразове повторення · Рахунку нема.

## Керування і ввід
- Настільна: пересунути фішку, взяту — у свою руку; курча перевернути на курку.
- (цифрова версія) Клік або drag фігури → підсвітка сусідніх легальних клітин; дроп — клік по фігурі в руці → підсвічені всі порожні клітини.
- Діалогу перетворення нема: курча перетворюється автоматично.

## Вікна, меню, HUD
- (цифрова версія; Lishogi і застосунки)
- `main-menu`: проти AI / проти людини / онлайн (Dōbutsu Shōgi Wars, Lishogi) → `match-setup` (колір, годинник).
- `game-screen`: дошка 3×4, два `pocket` з лічильниками ×N, `turn-indicator`, `last-move-highlight`, `legal-move-highlight`, лев під ударом підсвічений.
- `end-screen`: «Catch» / «Try» / нічия повторенням, кнопка «Ще партію».
- `tutorial-window` — навчання ходів звірят (дитяча аудиторія).
- `help-window` — правила варіанта; Lishogi — ще аналіз-дошка, редактор позицій, blind mode.
- Переходи: main-menu → match-setup → game-screen → end-screen → (реванш) game-screen.

## Фічі поза полем
- Застосунки: iOS/Android (2010), офіційний iOS (2012), онлайн «Dōbutsu Shōgi Wars» (2013), «Minna no Dōbutsu Shōgi» на Switch (05.2019) і PS4 (08.2019).
- Lishogi: `online-multiplayer`, рейтинг, аналіз рушієм, редактор позицій, режим для незрячих (blind mode).
- Гандикап «працює погано» (розвʼязок): поле замале для компенсації фігурами.

## Варіації й родичі
- Батько — [shogi.md](shogi.md); міні-родичі в [shogi-rule-twists.md](shogi-rule-twists.md) (Kyoto 5×5, де теж «мертвий дроп» легальний).
- **Goro goro dōbutsu shōgi** — 5×6, у кожного 3 курчати, 2 коти (срібло), 2 собаки (золото), лев; зона перетворення — два дальні ряди; обмеження дропу шогі (nifu, uchifuzume) діють; вічний шах (4 повторення) — нічия.
- **Ōkina mori no dōbutsu shōgi** («у великому лісі») — 9×9, повні правила шогі зі звірятами: слон і жирафа ходять на будь-яку відстань, додано кабана (лансер) і кролика (кінь).
- **Anpanman Hajimete Shōgi** (Segatoys) — 3×5, три фігури.
- **Осі варіацій**: розмір (3×4 / 5×6 / 9×9) · дальність фігур (1 крок / слайдер) · обмеження дропу (нема / як у шогі) · умова перемоги (Catch+Try / лише Catch / мат) · вічний шах (нічия / поразка).
- Сусіди за ідеєю «маленька розвʼязана гра»: [hexapawn.md](hexapawn.md), [l-game.md](l-game.md), [onitama.md](onitama.md).

## Цікавинки для курсу
- Найменша гра з рукою й дропами — перший крок до шогі: 5 типів, 12 клітин — 🥉.
- Try-перевірка: після ходу лева на дальній ряд згенерувати відповіді суперника й перевірити, чи бʼє хтось лева — 📎.
- Повний розвʼязувач ретроградним аналізом (~2,5·10⁸ досяжних позицій, компактний індекс позиції з рукою) — 🥇.
- Minimax з таблицею транспозицій і детектором повторень на 3×4 — 🥈.
- Порівняння «лишити короля під шахом можна» vs «заборонено» як перемикач правил — 📎.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ 5 типів · `piece-capture` · `piece-drop` + `pocket` ↔ рука · `pawn-promotion` ↔ курча → курка · `repetition-draw` ↔ 3 повторення · `legal-move-highlight`, `selection-highlight`, `last-move-highlight` · `cell-click`, `drag-drop-piece` · `hot-seat`, `turn-enforcement` · `ai-opponent`, `ai-minimax` · `online-multiplayer` · `level-solver` ↔ розвʼязок · `game-screen`, `main-menu`, `end-screen`, `help-window`, `tutorial-window` · `state-as-data`, `unit-tests`.
- **Нема** → пропозиції карток:
  - `+king-capture-win` (див. chess-rule-twists.md) — Catch.
  - `+reach-row-win` (див. checkers.md) — Try, але з умовою безпеки.
  - `+royal-try` «Трай: король на дальньому ряду, не під ударом» · game-logic/win · 📎 · слоти {row, safe: bool}.
  - `+dead-square-allowed` (див. shogi-rule-twists.md) — курча на дальньому ряду.
  - `+retrograde-solver` «Ретроградний розвʼязок усієї гри» · levels/solvability · 🥇 · слоти {index, max_ply}.

## Пропозиції до словників
- `+cond:not_attacked_after` — після ходу фігура не під ударом жодного ходу суперника (Try тут; «не ставити короля під шах» деінде).
- `+card:royal-try`, `+card:retrograde-solver` — див. «Мапа на каталог»; `+card:dead-square-allowed` — ще голос (shogi-rule-twists).

## Джерела
- ⭐ [Wikipedia: Dōbutsu shōgi](https://en.wikipedia.org/wiki/Dōbutsu_shōgi) — автори, 3×4, ходи, «ліс»/«небо», дропи без обмежень, Catch і лев на дальньому ряду «не під шахом», повторення й вічний шах, розвʼязок 2009 (246 803 167 позицій, другий виграє за 78 півходів), варіанти.
- [Wikipedia JA: どうぶつしょうぎ](https://ja.wikipedia.org/wiki/どうぶつしょうぎ) — ходи, трай «пережити наступний хід», лишити лева під шахом — не порушення, 千日手, хронологія видань і застосунків, Gorogoro / Ōkina mori / Anpanman.
- [Lishogi: Dobutsu](https://lishogi.org/variant/dobutsu) — ті самі правила; Try — «якщо лева не можна взяти наступним ходом».
- [Ludii: Let's Catch the Lion](https://ludii.games/details.php?keyword=Let%27s%20Catch%20the%20Lion) — автор, 2008, nestorgames, нічия триразовим повторенням.
- Розвʼязок Танаки — лінк зі статті Wikipedia (не відкривав); YouTube — пошук.

## Непевне
- (?) Try: «одразу, якщо не під шахом» (EN, Lishogi) чи «після того, як пережив хід суперника» (JA) — у майже всіх позиціях те саме; різниця — якщо суперник у відповідь сам робить Try.
- (?) Чи Lishogi забороняє лишати лева під шахом (оригінал — ні) — на сторінці варіанта не сказано.
- (?) Goro goro: у JA-вікі неясно, чи там є Try чи лише Catch; зона перетворення «перші й останні два ряди» в EN — дивне формулювання.
- (?) Кількість рівнів AI і склад меню застосунків — не відкривав.
- (?) Хто ходить першим «офіційно» — джерела показують Sente лише діаграмою.
