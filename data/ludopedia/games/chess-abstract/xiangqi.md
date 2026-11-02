---
title: Xiangqi (Сянці, китайські шахи)
slug: xiangqi
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
year: 1000
platforms: [board, web, mobile, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Xiangqi", best: true, note: "дошка, усі фігури з блокуваннями, літаючий генерал, заборона вічного шаху/переслідування, нотації, варіанти"}
  - {kind: play, url: "https://www.xiangqi.com/how-to-play-xiangqi", note: "Xiangqi.com: правила для новачка, задачі, AI-аналіз, ліміти повторень"}
  - {kind: other, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=xiangqi", note: "пошук BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=xiangqi+chinese+chess+rules", note: "пошук; правила"}
stage: v1
coverage: 70
mechanics: [piece-move-patterns, piece-capture, legal-move-highlight, no-move-into-check, check-stalemate, checkmate, hot-seat, turn-enforcement, move-timer, ai-opponent, ai-minimax, cell-click, hover-highlight, drag-drop-piece, game-screen, main-menu, end-screen, help-window, settings-window, theme-select, replay, state-as-data, sound-warnings, +palace-zone, +blockable-leap, +screen-capture, +facing-kings, +perpetual-ban, +repetition-draw, +move-notation, +handicap-setup, +engine-analysis]
proposes: ["+cond:in_zone", "+cond:in_check", "+trigger:check", "+trigger:repetition", "+cond:path_blocked", "+cond:screen_count", "+cond:kings_facing", "+effect:announce", "+role:zone", "+ui:last-move-highlight", "+ui:intersection-grid", "+window:puzzle-window", "+window:analysis-board", "+feature:handicap", "+feature:piece-set-select", "+card:palace-zone", "+card:blockable-leap", "+card:screen-capture", "+card:facing-kings", "+card:perpetual-ban"]
author: opus
date: 2026-11-02
---

# Xiangqi — шахи на перетинах: палац, річка, гармата через екран і генерали, що не бачать один одного

## Суть
Китайські шахи: двоє рухають по 16 фігур на **перетинах** 9×10 ліній, мета — мат генералу суперника. Від західних шахів відрізняють зони з обмеженнями (генерал і радники не покидають палацу, слони не переходять річку, солдати після річки отримують бічний хід), фігури з **блокованим стрибком** (кінь і слон зупиняються, якщо «нога»/«око» зайняте), **гармата**, що бʼє лише через рівно одну фігуру-екран, та правило «літаючого генерала». Пат — поразка, а не нічия; вічний шах і вічне переслідування заборонені.

## Поле і час
- Дошка 9 вертикалей × 10 горизонталей = 90 перетинів; фігури стоять на точках, не в клітинах (`field: square` — логічно це сітка 9×10).
- Річка між 5-м і 6-м рядами ділить дошку на половини; вертикалі на ній розірвані лише малюнком — на рух фігур (крім слона й солдата) вона не впливає.
- Палац — квадрат 3×3 точок у центрі тилу кожної сторони, з двома діагоналями; генерал і радники живуть лише в ньому.
- Старт: на 1-му ряду — колісниця, кінь, слон, радник, генерал, радник, слон, кінь, колісниця; гармати на 3-му ряду; 5 солдатів на 4-му ряду через одну точку. Червоні ходять першими.
- Покроково; турнірно — шаховий годинник.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Генерал (帥/將) | piece | 1; лише палац | 1 крок ортогонально в межах палацу; не може стояти на одній відкритій вертикалі з ворожим генералом |
| Радник (仕/士) | piece | 2; лише палац | 1 крок по діагоналі в межах палацу |
| Слон (相/象) | piece | 2; своя половина | рівно 2 кроки по діагоналі; не перетинає річку; блокується, якщо проміжна точка («око слона») зайнята |
| Кінь (傌/馬) | piece | 2 | 1 ортогонально, потім 1 діагонально назовні; блокується фігурою на першій ортогональній точці («спутаний кінь») — на відміну від шахового коня |
| Колісниця (俥/車) | piece | 2 | як тура: будь-яка відстань ортогонально, без перестрибувань |
| Гармата (炮/砲) | piece | 2 | ходить як колісниця; **бʼє** лише стрибком через рівно одну фігуру будь-якого кольору (екран) на ворожу за нею |
| Солдат (兵/卒) | piece | 5 | 1 вперед; після річки — також 1 вбік; назад ніколи; не перетворюється |
| Палац | zone | 3×3 точок з діагоналями | межа руху генерала й радників |
| Річка | zone | між рядами 5 і 6 | межа для слона; вмикає бічний хід солдата |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, piece, to)` → ЯКЩО `turn_of(side)` і `custom: «to за патерном фігури»` і `legal(move)` → ТО `move(piece, to)`; ЯКЩО `occupied(to, enemy)` → `disappear_b` (взяття).
- КОЛИ `input(move, general|advisor, to)` → ЯКЩО `not in_zone(to, own_palace)` → ТО `block`.
- КОЛИ `input(move, elephant, to)` → ЯКЩО `custom: «to за річкою»` або `occupied(midpoint)` (`+cond:path_blocked`) → ТО `block`.
- КОЛИ `input(move, horse, to)` → ЯКЩО `occupied(leg)` — точка першого ортогонального кроку → ТО `block`.
- КОЛИ `input(move, chariot|cannon, to)` без взяття → ЯКЩО на шляху є фігура → ТО `block`.
- КОЛИ `input(capture, cannon, to)` → ЯКЩО `custom: «між гарматою й to рівно одна фігура»` (`+cond:screen_count == 1`) → ТО `disappear_b`; інакше `block`.
- КОЛИ `input(move, soldier, to)` → ЯКЩО `custom: «to — назад»` або (`custom: «вбік»` і ще не за річкою) → ТО `block`.
- КОЛИ `after(move)` → ЯКЩО `custom: «генерали на одній вертикалі без фігур між ними»` (`+cond:kings_facing`) → ТО хід нелегальний (`block`): «літаючий генерал» прирівнюється до взяття генерала.
- КОЛИ `input(move)` → ЯКЩО після ходу свій генерал під боєм → ТО `block` (`no-move-into-check`).
- КОЛИ `trigger:check(side)` → ТО `custom: «оголосити шах»` (`+effect:announce`).
- КОЛИ `turn_start(side)` → ЯКЩО `in_check(side)` і `no_moves(side)` → ТО `lose` (мат).
- КОЛИ `turn_start(side)` → ЯКЩО `not in_check(side)` і `no_moves(side)` → ТО `lose` (пат — теж поразка).
- КОЛИ `trigger:repetition` → ЯКЩО одна сторона кожним ходом шахує (вічний шах) → ТО `lose` тій стороні.
- КОЛИ `trigger:repetition` → ЯКЩО одна сторона кожним ходом переслідує незахищену фігуру (не генерала й не солдата) → ТО `lose` тій стороні; обопільні вічні дії → `draw`; кількість повторень залежить від регламенту (Asian / Chinese / клубні правила).
- Нічия: згода, жодна сторона не має атакувальних фігур, повторення без порушень, ліміт ходів без взять (на сайтах).
- Перемога: мат або пат супернику, порушення ним заборони вічного шаху/переслідування, час · Поразка: те саме навпаки · Рахунок: 1 / ½ / 0.

## Керування і ввід
- Настільна: круглі диски з ієрогліфами (червоні й чорні мають різні знаки для генерала, радника, слона, солдата).
- (цифрова версія) Клік по фігурі → підсвітка легальних точок (з урахуванням ноги коня, ока слона, екрана гармати, літаючого генерала) → клік по точці; drag-n-drop; кнопки «Нічия», «Здатись», «Скасувати хід» (проти AI).
- Вибір набору фігур: ієрогліфи (традиційні/спрощені) або «західні» піктограми для новачків; перевертання дошки.

## Вікна, меню, HUD
- `main-menu`: Грати онлайн / проти AI / з другом · Задачі → `puzzle-window` · Навчання → `tutorial-window` · Налаштування → `settings-window` (набір фігур, дошка, звук, нотація).
- `game-screen`: дошка з перетинами, річкою («楚河 漢界») і палацами, `player-clock` обох, `turn-indicator`, `move-list` (WXF-нотація), `captured-pieces`, `last-move-highlight`, `legal-move-highlight`, позначка шаху (звук + підсвітка генерала), `offer-draw-button`, `resign-button`.
- `end-screen`: результат і причина (мат, пат, вічний шах, час) → «Аналіз» (`analysis-board` з оцінкою двигуна) / «Реванш».
- `help-window`: правила з анімаціями руху кожної фігури.
- Переходи: main-menu → (пошук суперника) game-screen → end-screen → analysis-board / game-screen.

## Фічі поза полем
- `online-multiplayer`, `rating`, `turn-timer` (бліц 5–10 хв), `ai-opponent-levels`, `engine-analysis` після партії (Xiangqi.com).
- `puzzle-bank` — задачі на мат в 1, 2…; `tutorial`.
- `handicap` — сильніший гравець знімає колісницю/гармату/коня або слабшому дають додаткові ходи.
- `custom-skins` — ієрогліфи / західні фігури (`+feature:piece-set-select`).
- Автоматичний арбітр повторень: сайт забороняє повторювати шах чи переслідування понад 3 рази поспіль.
- `export-import` партій у нотаціях (числова WXF, алгебраїчна, ієрогліфічна).

## Варіації й родичі
- Banqi — фігури лицем донизу на половині дошки, відкриваються під час гри (зовсім інші правила, `info: hidden`).
- Manchu chess — у червоних прибрано коней, гармати й одну колісницю, але колісниця, що лишилась, ходить ще й як кінь чи гармата.
- Formation — випадкова розстановка однієї сторони; Supply chess — 4 гравці на двох дошках, збиті фігури передаються партнеру.
- San Guo Qi / San You Qi / Si Guo Qi — на 3–4 гравців.
- Родичі: західні шахи, shogi, janggi (корейські: палац, гармати), makruk — спільний предок чатуранга.
- Осі варіацій: **зони обмеження** (палац / річка / нема) · **взяття** (заміщенням / через екран) · **блокування стрибка** (кінь шахів не блокується / кінь сянці блокується) · **пат** (нічия / поразка) · **повторення** (нічия / поразка того, хто повторює агресивно).

## Цікавинки для курсу
- Зони на полі, що обмежують типи фігур (палац, річка) — 📎; та сама ідея, що `impassable-cells` «для типу сутності».
- Блокований стрибок коня/слона: перевірка проміжної точки — 🌱 поверх шахових патернів.
- Гармата: різні правила для ходу й для взяття, підрахунок фігур на промені — 📎.
- Літаючий генерал як додаткова умова легальності (`no-move-into-check` + перевірка вертикалі) — 🥉.
- Пат = поразка: одна зміна в `check-stalemate` — 🌱; заборона вічного шаху/переслідування: історія позицій + класифікація ходу як «шах»/«переслідування» — 👑 (регламент складний навіть для людей-арбітрів).
- Рендер на перетинах з річкою й діагоналями палацу; два набори фігур — 🥉.

## Мапа на каталог
- Є: `piece-move-patterns` · `piece-capture` · `legal-move-highlight` · `no-move-into-check` · `check-stalemate` (пат = поразка) · `checkmate` · `hot-seat`, `turn-enforcement`, `move-timer` · `ai-opponent`, `ai-minimax` · `cell-click`, `hover-highlight`, `drag-drop-piece` · `game-screen`, `main-menu`, `end-screen`, `help-window`, `settings-window`, `theme-select` (набори фігур) · `replay`, `state-as-data` · `sound-warnings` (шах).
- **Нема** → пропозиції карток:
  - `+palace-zone` «Зона, з якої фігура не виходить» · entities/legality · 📎 · слоти {pieces, region} — палац, річка для слона.
  - `+blockable-leap` «Стрибок, що блокується проміжною клітиною» · entities/legality · 🌱 — кінь і слон сянці.
  - `+screen-capture` «Взяття через екран» · entities/combat · 📎 · слоти {screens: 1} — гармата.
  - `+facing-kings` «Королі не бачать один одного» · entities/legality · 🥉.
  - `+perpetual-ban` «Заборона вічного шаху/переслідування» · game-logic/constraints · 👑 · слоти {n_repeats, chase_targets}.
  - `+repetition-draw` (див. chess.md) — тут повторення може бути і поразкою.
  - `+move-notation` (див. chess.md) — WXF/числова.
  - `+handicap-setup` (див. go.md/shogi.md) — гандикап зняттям фігур.
  - `+engine-analysis` (див. chess.md) — аналіз партії двигуном.

## Пропозиції до словників
- `+cond:in_zone` — точка належить зоні (палац, своя половина).
- `+cond:in_check`, `+trigger:check`, `+trigger:repetition` — уже в chess/shogi.
- `+cond:path_blocked` — проміжна точка ходу зайнята (нога коня, око слона).
- `+cond:screen_count` — кількість фігур між двома точками на промені (гармата: рівно 1).
- `+cond:kings_facing` — генерали на одній відкритій лінії.
- `+effect:announce` — оголошення стану (шах) звуком/текстом; близько до ⏳ `message`/`sound`.
- `+role:zone` — палац, річка.
- `+ui:last-move-highlight`; `+ui:intersection-grid` — рендер фігур на перетинах ліній, а не в клітинах (go, сянці).
- `+window:puzzle-window` — задачі на мат; `+window:analysis-board` — дошка аналізу з оцінкою двигуна; `+feature:handicap`; `+feature:piece-set-select` — ієрогліфи / західні фігури.
- `+card:palace-zone`, `+card:blockable-leap`, `+card:screen-capture`, `+card:facing-kings`, `+card:perpetual-ban` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Xiangqi](https://en.wikipedia.org/wiki/Xiangqi) — дошка, палац, річка, усі фігури з блокуваннями, літаючий генерал, пат = поразка, вічний шах і переслідування, цінність фігур, гандикапи, нотації, варіанти, компʼютерна гра.
- [Xiangqi.com: How to play](https://www.xiangqi.com/how-to-play-xiangqi) — правила для новачка, задачі, AI-аналіз, ліміт повторень шаху/переслідування (3 рази).
- [BGG: пошук](https://boardgamegeek.com/geeksearch.php?action=search&q=xiangqi) — пошукова сторінка (не відкривав).
- YouTube: пошук «xiangqi chinese chess rules».

## Непевне
- (?) `year: 1000` — умовний (сучасна форма зазвичай датується династією Сун); дату не перевіряв.
- (?) Точна кількість повторень для вічного шаху/переслідування відрізняється між Asian rules, китайськими правилами й сайтами — деталі регламенту не прочитані.
- (?) Набори фігур «західні піктограми» й перевертання дошки — типові для сайтів, на конкретному сайті не перевірено.
- (?) Сучасні двигуни (Pikafish тощо) — у прочитаній частині статті не згадані.
