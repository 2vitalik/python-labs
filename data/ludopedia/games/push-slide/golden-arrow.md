---
title: Golden Arrow
slug: golden-arrow
aka: []
family: push-slide
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2025
platforms: [PC (Windows)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3633540/Golden_Arrow/", best: true, note: "опис («стрілки рухаються у свій бік, доки ніщо не заважає»), 82 рівні, демо з 6 рівнів, досягнення, Steam Cloud, контролер; трейлер і 6 знімків; новини оновлень зі світами й керуванням"}
  - {kind: itch, url: "https://inbluegames.itch.io/golden-arrow", note: "та сама гра на itch: Godot, теги, посилання на демо й плейлист-проходження"}
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=071df0d50ec338bb7593dc2d78f6f6a6", note: "PuzzleScript-версія автора як редактор рівнів: самохідні стрілки, ланцюговий поштовх, камені-поліоміно, телепорти, золота стрілка"}
  - {kind: other, url: "https://inbluegames.itch.io/golden-arrow/devlog/1086469/golden-arrow-level-editor-puzzlescript", note: "девлог 17.10.2025: PuzzleScript-версія для власних рівнів"}
  - {kind: other, url: "http://dongchagames.itch.io/golden-arrow-demo", note: "демо на itch"}
  - {kind: youtube, url: "https://www.youtube.com/playlist?list=PLbjjG8CodnfyepXm4Rc5MsYzJV6UW7FZM", note: "плейлист-проходження від автора (посилання зі сторінки itch)"}
stage: v1
coverage: 70
mechanics: [move-4dir, keyboard-controls, push-object, multi-cell-size, inertia-slide, all-on-targets, teleport-pair, teleport-cooldown, undo-unlimited, restart-level, sequential-levels, level-select, level-bank, field-scaling, facing-icon, movement-animation, music-toggle, +push-chain, +typed-targets, +self-propelled-block, +move-conflict-cancel, +carry-goal-object]
proposes: ["+effect:advance", "+cond:contested", "+card:self-propelled-block", "+ui:solved-flag"]
author: opus
date: 2026-11-19
---

# Golden Arrow — Sokoban, де «ящики» — кольорові стрілки, що самі їдуть у свій бік до першої перешкоди

## Суть
Замість ящиків — **кольорові стрілки**: кожна сама їде туди, куди дивиться, поки клітина попереду порожня, і зупиняється перед першою перешкодою. Гравець — біла стрілка-герой: ходить у 4 боки й штовхає стрілки та камені (навіть цілі ряди), щоб кожна стрілка **зупинилась** на контурі свого кольору. Сама ціль стрілку не тримає — зупинити її там має стіна, камінь, інша стрілка чи сам герой.

Гра Dong Cha (Inblue Games, рушій Godot), 20.04.2025, 82 рівні в 7 світах. Автор опублікував PuzzleScript-версію з тими самими правилами як редактор рівнів — з неї взято точні правила руху.

## Поле і час
- Квадратна сітка; кімната неправильної форми, усередині — стіни-ями. Рівень видно цілком; є кнопка зуму.
- Шари: підлога + цілі-контури + телепорти → тверді обʼєкти (герой, стрілки, камені, золота стрілка, стіни).
- Хід = крок героя (можливо з поштовхом), потім **доїзд**: кожна стрілка з порожньою клітиною попереду просувається на 1, усі одночасно; підкроки повторюються, доки всі не стануть (у PuzzleScript — цикл `again`). Без вводу світ стоїть.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой (біла стрілка) | player | у кадрах завжди «дивиться» вгору | рух 4 боки; штовхає ряд обʼєктів, якщо за останнім вільно; сам не їде |
| Кольорова стрілка | object | колір = напрям (Steam: червона ↑, фіолетова ↓, синя ←, зелена →) | їде у свій бік по 1 клітині, доки попереду порожньо; нікого не штовхає; штовхати її можна з будь-якого боку |
| Стрілка-поліоміно | object | форма (L, довга «змія»), голова задає напрям | лише в Steam-версії; їде як ціле (?) |
| Камінь | object | 1 клітина або зчеплена фігура | сам не рухається; зчеплені частини штовхаються разом |
| Ціль-контур | zone | колір і напрям | на ній має стояти стрілка свого кольору; рух не зупиняє |
| Золота стрілка | object | — | у PuzzleScript-версії сама не їде; стала на свою ціль — перемога одразу |
| Золота ціль | zone | — | ціль золотої стрілки |
| Телепорт (пара) | terrain | вхід ↔ вихід | герой чи стрілка, що стала на один, переноситься на інший, якщо він вільний; камені — ні |
| Стіна / яма | static | — | непрохідна для всіх |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(hero, dir)`.
- КОЛИ `contact(hero, arrow|stone|golden_arrow)` → ЯКЩО `custom: «за останнім обʼєктом ряду в напрямку руху вільно»` → ТО `push` усього ряду на 1, `move(hero, dir)`; інакше `block`.
- КОЛИ `contact(hero, stone_part)` → ЯКЩО `custom: «жодна зчеплена частина каменя не впирається»` → ТО `push` усього каменя разом; інакше `block` для всього ряду.
- КОЛИ `after(input)` → ЯКЩО `free(cell_ahead_of_arrow)` → ТО `move(arrow, facing)` — для всіх стрілок одночасно; підкроки повторюються, доки поле не осяде (settled).
- КОЛИ `custom: «дві стрілки цілять в одну порожню клітину»` → ТО `block` для обох (жодна не їде).
- КОЛИ `blocked(arrow)` → ТО стрілка стоїть: `custom: «сама нікого не штовхає»`.
- КОЛИ `enter(arrow, target)` → ЯКЩО `free(cell_ahead)` → ТО `move(arrow, facing)` далі — ціль не зупиняє.
- КОЛИ `enter(x, teleport_a)` → ЯКЩО `free(teleport_b)` і `not same(x, stone, type)` → ТО `teleport(x, teleport_b)`, `set_state(x, just_teleported)`.
- КОЛИ `leave(x, teleport)` → ТО `clear_state(x, just_teleported)` — поки стан стоїть, телепорт не спрацьовує вдруге.
- КОЛИ `enter(golden_arrow, golden_target)` → ТО `win`.
- КОЛИ `all_on(arrow, target)` → ЯКЩО `same(arrow, target, colour)` → ТО `win`, `next_level`.
- Стрілка-поліоміно (Steam): КОЛИ `after(input)` → ЯКЩО `custom: «перед усією фігурою в бік голови порожньо»` → ТО `move(shape, head_dir)` (?).
- КОЛИ `input(z)` → ТО `undo`.
- КОЛИ `input(r)` → ТО `restart`.
- Перемога: кожна кольорова стрілка на контурі свого кольору (або золота — на своїй цілі). · Поразка: нема; глухий кут — undo / R. · Рахунку нема; є позначка «розвʼязано».

## Керування і ввід
- Клавіатура: напрямки — крок героя; Z — undo; R — рестарт; Esc — вихід у меню; Enter / Space — підтвердити; X — зум (до версії 1.0.1 — Y); M — звук.
- Геймпад Xbox (з 1.0.1): D-pad — рух, B — undo, Y — рестарт, Start — меню, A — підтвердити, X — зум, R/RS — звук.
- Ввід покроковий: поки стрілки доїжджають, новий хід чекає.

## Вікна, меню, HUD
- `level-select` / `chapter-select`: ряд із 7 значків світів, підпис світу («1: BEGINNER'S ISLAND»), лічильник «Completed Levels: N / 82».
- `game-screen`: поле по центру; знизу панель — назва рівня з номером (`level-number`: «1: First Arrow»), кнопка ESC, позначка «Solved: Y/N» (чи розвʼязано раніше), кнопки M (звук), R (`restart-button`), Z (`undo-button`), Y/X (`zoom-control`). На перших рівнях ліворуч підказки «Z: Undo», «R: Restart» (`hint-text`).
- `achievements-window` — 8 досягнень Steam.
- Переходи: вибір світу → рівень → (перемога) наступний рівень; ESC — назад до вибору (?).

## Фічі поза полем
- `levels-sequential` у 7 світах (Beginner's Island, Springland, The Village, Death Valley, Forbidden Temple, The Tower та ще один (?)); 82 рівні після правок 1.0.5 (було 84).
- `undo` без ліміту (оновлення 1.1.1 лагодило undo «багато разів»), `restart-level`, зум, вимкнення звуку.
- `cloud-save`, `achievements`, `gamepad-support`.
- Демо з 6 рівнів (5 з них лише в демо); плейлист-проходження від автора; PuzzleScript-версія як `level-editor` для фанатів (поза Steam-грою).
- Рівні «multi-player» у світі The Village (за новиною 1.1.0) — ймовірно, з кількома героями (?).

## Варіації й родичі
- [AutomaticBox](automaticbox.md) — ящики самі крокують за стрілками, але героя нема.
- [A Directionless Cycle](a-directionless-cycle.md) — ввід рухає всі фігури зі стрілкою цього напрямку.
- [Atomix](atomix.md), [Ice-sliding puzzles](ice-sliding-puzzles.md) — ковзання до упору, але лише після поштовху.
- [Sokoban](sokoban.md); автор порівнює з [Stephen's Sausage Roll](../thinky/stephens-sausage-roll.md), [Snakebird](../thinky/snakebird.md), [Jelly no Puzzle](../thinky/jelly-no-puzzle.md).
- Осі варіацій:
  - **хто рухає обʼєкт**: лише гравець / сам обʼєкт за своєю стрілкою / обидва (тут);
  - **як далеко**: на 1 клітину / до упору / до упору самохідно;
  - **ціль**: будь-яка / свого кольору й напряму;
  - **конфлікт двох в одну клітину**: обидва стоять (тут) / пріоритет / злиття.

## Цікавинки для курсу
- Самохідні стрілки: після кожного ходу — підкроки «доїзду», доки поле не стабілізується, — 📎.
- Конфлікт: дві стрілки цілять в одну клітину — обидві стоять (резервування клітин на підкрок) — 🥉.
- Ланцюговий поштовх ряду різнотипних обʼєктів з відкатом, якщо хвіст упирається, — 📎.
- Камені-поліоміно: зчеплені клітини рухаються разом, блок однієї блокує всі — 🥉.
- Телепорт-пара з «затримкою», щоб обʼєкт не стрибав туди-сюди, — 📎.
- Розвʼязувач BFS (стан = герой + стрілки + камені) з детермінованим доїздом — 🥇.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ крок героя; `push-object` ↔ поштовх; `multi-cell-size` ↔ камені-фігури й стрілки-поліоміно; `inertia-slide` ↔ стрілка їде до упору; `all-on-targets` ↔ стрілки на контурах; `teleport-pair` + `teleport-cooldown` ↔ телепорти з затримкою; `undo-unlimited` + `restart-level` ↔ Z і R; `sequential-levels` + `level-select` ↔ 7 світів; `level-bank` ↔ «Solved: Y/N» і «Completed Levels»; `field-scaling` ↔ зум; `facing-icon` ↔ стрілка намальована за напрямом; `movement-animation` ↔ плавний доїзд; `music-toggle` ↔ M (?).
- **Нема** → пропозиції карток:
  - `+push-chain` (уже пропонована) — ряд обʼєктів одним поштовхом.
  - `+typed-targets` (уже пропонована) — ціль свого кольору для кожної стрілки.
  - `+self-propelled-block` «Обʼєкт сам їде у свій бік, доки попереду порожньо» · entities/move · 📎 (родич `inertia-slide` і AutomaticBox).
  - `+move-conflict-cancel` (уже пропонована) — двоє в одну клітину — обидва стоять.
  - `+carry-goal-object` (уже пропонована) — золота стрілка на своїй цілі.

## Пропозиції до словників
- `+effect:advance` — самохідний обʼєкт просувається на 1 у свій бік, якщо попереду порожньо (стрілки Golden Arrow, ящики AutomaticBox); `move` не каже, хто ініціює.
- `+cond:contested` — у цільову клітину цього підкроку претендує більше одного обʼєкта.
- `+card:self-propelled-block` — див. «Мапу на каталог».
- `+ui:solved-flag` — позначка «рівень уже розвʼязано» на екрані гри.

## Джерела
- ⭐ [Steam: Golden Arrow](https://store.steampowered.com/app/3633540/Golden_Arrow/) — опис механіки, 82 рівні, демо, категорії (досягнення, Cloud, контролер); новини 1.0.1–1.1.1: керування клавіатурою й геймпадом, назви світів, правки рівнів; 6 знімків і трейлер (переглянуто покадрово: доїзд стрілок, поштовх збоку, контури цілей, HUD).
- [PuzzleScript-версія автора](https://www.puzzlescript.net/play.html?p=071df0d50ec338bb7593dc2d78f6f6a6) — сирець (gist): обʼєкти, ланцюговий поштовх з відкатом, зчеплені камені, доїзд стрілок з конфліктом, телепорти з затримкою, умови перемоги.
- [itch.io: Golden Arrow](https://inbluegames.itch.io/golden-arrow) — рушій Godot, теги, демо, плейлист-проходження.
- [Девлог про редактор](https://inbluegames.itch.io/golden-arrow/devlog/1086469/golden-arrow-level-editor-puzzlescript) — навіщо PuzzleScript-версія.
- [YouTube: проходження від автора](https://www.youtube.com/playlist?list=PLbjjG8CodnfyepXm4Rc5MsYzJV6UW7FZM).

## Непевне
- (?) Чи все в Steam-версії точно як у PuzzleScript-версії (зокрема конфлікт двох стрілок і те, що стрілка нікого не штовхає) — «except for some specific circumstances» в описі Steam натякає на винятки.
- (?) Стрілки-поліоміно («Tetris», «The Great Snake») і в PuzzleScript-версії відсутні — як вони рухаються й зупиняються, не перевірено.
- (?) Сині й помаранчеві кола на знімках («9: Grenade») — найімовірніше, телепорти; чи є «гранати» як окремий обʼєкт — невідомо.
- (?) Чи їде золота стрілка в Steam-версії сама; чи стрілки рушають на старті рівня без ходу.
- (?) «Multi-player» рівні The Village, сьомий світ, екран вибору рівня всередині світу, M вимикає музику чи весь звук.
