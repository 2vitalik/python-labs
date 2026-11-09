---
title: "Bomberman: Panic Bomber (ぱにっくボンバー)"
slug: panic-bomber
aka: [Panic Bomber, ぱにっくボンバー, Tobidase! Panibon, とびだせ!ぱにボン, "Super Bomberman: Panic Bomber W", Panibon]
family: falling-match
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: survive
year: 1994
platforms: [PC Engine Super CD-ROM², Neo Geo, Super Famicom, Virtual Boy, FM Towns, PC-98, X68000, PSP, Wii VC, Wii U VC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bomberman:_Panic_Bomber", best: true, note: "суть: трійки дають бомби, бомбу підриває лише вибух запаленої, сміття супернику, гігантська бомба; версії й дати"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ぱにっくボンバー", note: "L-подібна трійка, 3+ по вертикалі/горизонталі/діагоналі, бомби знизу за ланцюг, コゲボン, でかバク, камені, версії"}
  - {kind: other, url: "https://www.virtual-boy.com/games/panic-bomber/guides/976525/", note: "FAQ VB: полумʼя хрестом довжини рівня вогню, Flame Up/Level Up, Decker Bomb, SKULL-предмети, меню й паролі"}
  - {kind: other, url: "https://cinemaoftheabstract.blogspot.com/2022/05/games-of-abstract-panic-bomber-1995.html?hl=en", note: "огляд VB: L-фігури, Skull Mode, бос-структура, автопауза"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=panic+bomber+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [gravity-fall, multi-cell-size, piece-rotate-flip, keyboard-controls, line-match-clear, chain-detonation, explode-area, blast-wave, chain-reaction, garbage-attack, simultaneous-versus, ai-opponent, item-pickup, temporary-modes, sequential-levels, difficulty-levels, level-password, score-records, help-window, theme-select, game-pause, +cascade-gravity, +rising-garbage-row, +lit-bomb-trigger, +garbage-blast-clear, +big-bomb-gauge, +indestructible-block, +flame-level-powerup]
proposes: ["+effect:raise_stack", "+ui:special-meter", "+card:lit-bomb-trigger", "+card:garbage-blast-clear", "+feature:auto-pause"]
author: opus
date: 2026-11-09
---

# Bomberman: Panic Bomber — трійки голів Бомбермена родять бомби знизу, а підриває їх лише запалена бомба згори

## Суть
Падають L-подібні трійки «голів» Бомбермена кількох кольорів; 3+ однакових у лінію (рядок, стовпець або діагональ) зникають, і за це знизу в стек підіймаються **незапалені бомби**. Сама бомба не вибухає ніколи: час від часу згори падає **запалена** бомба, і при приземленні пускає полумʼя хрестом; кожна незапалена бомба, якої торкнулось полумʼя, вибухає, зникає з твого поля й приходить супернику **обгорілою** («коґебон») — сміттям. Хто першим заповнив поле до верху, той програв; накопичена шкала дає **гігантську бомбу**, що розчищає велику ділянку.

## Поле і час
- Вертикальна «склянка» на кожного гравця, поля поруч; розмір у клітинах — (?).
- Шари: стек (голови, бомби, сміття, камені) + падаюча трійка + шкала гігантської бомби біля поля.
- Real-time: фігура падає з темпом рівня; за ланцюги/збіги знизу піднімаються ряди бомб; згори іноді падають запалені й незапалені бомби.
- Після зникнення блоки над порожниною падають (каскад) — звідси ланцюги.
- Virtual Boy: червоно-чорний стереоскопічний паралакс, опція автопаузи для очей; гра лише 1P.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Падаюча трійка | player | 3 блоки, L-форма, орієнтація | зсув, поворот, падіння; приземлилась → блоки розсипаються вниз |
| Голова Бомбермена | tile | колір (білий, чорний, червоний…); 5 наборів скінів на VB | 3+ однакових у рядок/стовпець/діагональ → зникає; полумʼя її не бере |
| Незапалена бомба | object | — | зʼявляється знизу після збігів, іноді падає згори; вибухає лише від полумʼя |
| Запалена бомба | projectile | — | падає згори час від часу; при приземленні — полумʼя хрестом |
| Полумʼя | hazard | довжина = рівень вогню (старт 2) | 4 напрямки на N клітин; підриває бомби, спалює сміття |
| Обгоріла бомба (コゲボン) | hazard | — | сміття від суперника; не збігається; зникає від полумʼя або гігантської бомби |
| Гігантська бомба (Deka/Decker Bomb) | projectile | — | падає, коли повна шкала; розчищає велику ділянку, шле багато сміття |
| Камінь (石) | static | — | зʼявляється в затяжному матчі; не збігається, не горить; бере лише гігантська бомба |
| Цегла (SKULL-режим VB) | object | — | підірвана — випускає SKULL-предмет |
| Flame Up | pickup | +1 | рівень вогню +1 до кінця етапу |
| Level Up | pickup | — | фігури падають швидше |
| SKULL-предмети (VB) | pickup | 8 видів | Interfering Bomber, Speed Blocks, Joystick (інверсія керування), Stop (заморозка 5 с), Next (наступна — гігантська бомба), Brick to Bomb, Bomb to Boom (запалити всі), Block to Blank (зняти всі голови) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move|rotate|drop)` → ЯКЩО `free(cells)` → ТО `move(piece, dir)` / `rotate(piece, 90)`; інакше `block`.
- КОЛИ `locked(piece)` → ТО `fall(each_block)` — блоки трійки розсипаються вниз окремо (?).
- КОЛИ `pattern(line(3+, same_color))` (рядок, стовпець або діагональ) → ТО `clear(cells)`, `counter(deka_gauge, +n)`.
- КОЛИ `after(clear)` → ТО `fall(blocks_above)`; КОЛИ `settled` → ЯКЩО `pattern(line(3+))` → ТО `clear(cells)`, `combo(+1)` (ланцюг).
- КОЛИ `custom: «збіг/ланцюг завершено»` → ТО `custom: «raise_stack — знизу підіймаються незапалені бомби, кількість залежить від довжини ланцюга»`.
- КОЛИ `custom: «ланцюг завершено»` → ЯКЩО `chain(5)` → ТО `custom: «бомби підіймаються вже запаленими й одразу вибухають»`; 6–9 ланцюгів — лише окремі анімації (ракета, ядерний вибух, …).
- КОЛИ `timer(interval)` → ТО `spawn_at(lit_bomb, top)` (як частина падіння; інтервал — (?)).
- КОЛИ `locked(lit_bomb)` → ТО `explode(cross, flame_level)`, `disappear(lit_bomb)`.
- КОЛИ `contact(flame, unlit_bomb)` → ТО `explode(cross, flame_level)` для тієї бомби (ланцюг детонацій), `disappear(unlit_bomb)`, `send_garbage(scorched, 1)`.
- КОЛИ `contact(flame, scorched)` → ТО `disappear(scorched)`.
- КОЛИ `contact(flame, head)` → ТО `block` — голови полумʼя не бере.
- КОЛИ `contact(flame, stone)` → ТО `block`.
- КОЛИ `counter(deka_gauge, ≥, full)` → ТО `spawn_at(deka_bomb, top)`, `counter(deka_gauge, 0)`.
- КОЛИ `locked(deka_bomb)` → ТО `explode(large_area)` — знищує бомби, голови, сміття й камені; `send_garbage(scorched, many)`.
- КОЛИ `counter(match_time, ≥, long)` → ТО `spawn_at(stone, …)` (?).
- КОЛИ `picked(flame_up)` → ТО `counter(flame_level, +1)`; КОЛИ `picked(level_up)` → ТО `speed(piece, +)`; обидва скидаються з новим етапом.
- SKULL (VB): КОЛИ `contact(flame, brick)` → ТО `disappear(brick)`, `spawn(skull_item)`; ефект предмета — за таблицею сутностей (`stun`, `invert_controls(n)`, `clear(all heads)`, …).
- КОЛИ `custom: «стек суперника досяг верхнього ряду»` → ТО `win` (раунду); власний стек угорі → `lose`.
- Бос-матчі (VB) — до 2 перемог із 3; КОЛИ `custom: «двічі поспіль переміг Count Dracu-Boom»` → ТО `unlock(Ms. Flashy)`.

## Керування і ввід
- D-pad — зсув трійки ліворуч/праворуч, вниз — прискорення (?); кнопки — поворот (напрям(и) — (?)).
- Меню паролів (VB): вгору/вниз — цифра, ліворуч/праворуч — позиція, A — підтвердити; A виходить і з демонстрації правил.
- Versus — одночасно на двох полях; PC Engine — до 5 гравців (?), PSP — до 4 через Game Sharing.

## Вікна, меню, HUD
- `main-menu` (VB): Start · Password · The Rules · Options.
- `difficulty-select` — VERY EASY / EASY / NORMAL / HARD; далі вибір набору блоків (`theme-select`, 5 наборів; лише вигляд).
- `level-password` — 4-значні паролі етапів і медалей; окремі коди (лише боси, голови-фігурки, новий старт на складності).
- `help-window` — The Rules: демонстрація й пояснення правил (вихід — A).
- `settings-window` — Boss Battle (SKULL / NORMAL), контраст 1–10, прокрутка фону, автопауза.
- `game-screen`: два поля (твоє й CPU/2P) — `opponent-boards`; `custom: «шкала гігантської бомби»` біля поля; `score`; портрети суперників — `player-portraits` (?); `popup-text`/анімації ланцюгів 6–9.
- `dialogue-window` — сюжетні сценки між суперниками (пошук статуї Golden Bomber) (?).
- `end-screen`; `leaderboard` — введення імені в топ-5 після game over або проходження 9 етапів.
- Переходи: main-menu → difficulty → набір блоків → game-screen (матч) → наступний суперник / пароль → бос → фінал.

## Фічі поза полем
- Режими: 1P «сюжет» проти CPU (9 етапів із названими суперниками; VB — 3 етапи по 2 вороги + мінібос + бос), `mode-versus` 2P (другий гравець може приєднатися посеред гри).
- `difficulty-presets` (4 рівні на VB), `level-password`, `leaderboard-local` (топ-5).
- `custom-rules` — Boss Battle SKULL/NORMAL (предмети, цегла й камені вмикаються).
- Доступність VB: автопауза, контраст; `rules-page` — The Rules.
- Розблоковки: секретна бос Ms. Flashy за 2 перемоги поспіль над Count Dracu-Boom; справжня кінцівка — Hard.

## Варіації й родичі
- PC Engine Super CD-ROM² (1994) — перенесення аркадної версії; Neo Geo (1995); Super Famicom — Super Bomberman: Panic Bomber W (1995, свої доповнення); FM Towns, PC-98, X68000 (1995); Virtual Boy — Tobidase! Panibon (1995, лише 1P); PSP (2005, предмети зміни вигляду, 4P); Wii VC (2008), Wii U VC (2015/2017); Super Bomberman Collection (2026) — перший англійський реліз Panic Bomber W.
- Мінігри: Bomberman 64 (2001) і Bomberman Land 2 — «трохи інші правила»; GBA Bomberman Jetters Game Collection — «Ain no Panibon»: кольорові блоки без голів, режими «зробити N обгорілих» і score attack, без versus.
- Родичі в корпусі: `bomberman` (хрест полумʼя з довжиною рівня вогню — звідти), `bombliss` (бомби в Tetris), `puyo-puyo` (сміття супернику, ланцюги), `columns` (3+ у будь-якому напрямку), `yoshis-cookie`.
- **Осі варіацій**: що підриває бомбу (зчищений ряд — BomBliss / лише полумʼя іншої бомби — Panic Bomber / таймер-запал — Bomberman) · куди йде підірване (зникає / стає сміттям у суперника) · форма вибуху (хрест довжини N / квадрат / ціла ділянка) · хто чистить сміття (сусідній збіг — Puyo / лише вибух — Panic Bomber).

## Цікавинки для курсу
- Бомба, що вибухає лише від чужого полумʼя, + хрест довжиною N, що зупиняється на голові/камені, + ланцюг детонацій — 🥉 (BFS по бомбах з обмеженням дальності).
- Перенесення підірваних бомб у поле суперника як сміття, яке горить лише від вибухів — 🥉.
- Ланцюг збігів → кількість бомб, що підіймаються знизу; 5-ланцюг — бомби вже запалені — 📎.
- Шкала гігантської бомби від зчищених блоків + вибух великої площі, що бере навіть камені — 📎.
- Падаюча L-трійка з розсипанням після приземлення й діагональні збіги — 📎.
- SKULL-предмети як таблиця тимчасових ефектів (інверсія, заморозка 5 с, «запалити всі») — 🥉.

## Мапа на каталог
- Є: `gravity-fall` + `multi-cell-size` + `piece-rotate-flip` ↔ трійка, що падає й обертається; `line-match-clear` ↔ 3+ у лінію; `chain-detonation` ↔ полумʼя підриває бомби; `blast-wave` ↔ хрест полумʼя; `explode-area` ↔ гігантська бомба; `chain-reaction` ↔ каскадні збіги; `garbage-attack` + `simultaneous-versus` + `ai-opponent`; `item-pickup` + `temporary-modes` ↔ Flame Up, SKULL-ефекти на час; `sequential-levels`, `difficulty-levels`, `level-password`, `score-records`, `help-window` (The Rules), `theme-select` (набори блоків), `game-pause` (автопауза).
- **Нема** → пропозиції карток:
  - `+cascade-gravity` (спільна) — падіння після зникнення.
  - `+rising-garbage-row` (спільна) — тут знизу підіймаються власні бомби, а не сміття.
  - `+lit-bomb-trigger` «Бомба вибухає лише від вибуху запаленої» · entities/combat · 🥉 · слот {trigger: flame|line|timer}.
  - `+garbage-blast-clear` «Сміття знімається лише вибухом» · entities/interact · 🌱 — пара до `+garbage-adjacent-clear`.
  - `+big-bomb-gauge` «Шкала за зчищення → гігантська бомба» · game-logic/score · 📎 (родич `+attack-gauge`).
  - `+indestructible-block` «Блок, що не збігається й не горить» · entities/interact · 🌱.
  - `+flame-level-powerup` «Рівень вогню +1 на етап» · entities/state · 🌱 (з Bomberman).

## Пропозиції до словників
- `+effect:raise_stack` — знизу підіймається ряд (тут — незапалених бомб).
- `+ui:special-meter` — шкала спецздібності (гігантська бомба).
- `+card:lit-bomb-trigger`, `+card:garbage-blast-clear` — див. мапу на каталог.
- `+feature:auto-pause` — автоматична пауза через інтервал (Virtual Boy, від втоми очей).

## Джерела
- ⭐ [Wikipedia: Bomberman: Panic Bomber](https://en.wikipedia.org/wiki/Bomberman:_Panic_Bomber) — мета (заповнити поле суперника), бомби за трійки, вибух лише від запаленої бомби, сміття, гігантська бомба, паролі, усі версії й дати.
- [Wikipedia JA: ぱにっくボンバー](https://ja.wikipedia.org/wiki/ぱにっくボンバー) — L-трійки, 3+ у будь-якому напрямку, бомби знизу за ланцюги, 5-ланцюг із запаленими, コゲボン, でかバクメーター, камені, Flame-ріст, 9 етапів, топ-5, версії й мінігри.
- [Virtual-Boy.com: FAQ Panic Bomber](https://www.virtual-boy.com/games/panic-bomber/guides/976525/) — трійки, полумʼя хрестом довжини рівня вогню (старт 2), голови не горять, Decker Bomb, SKULL-предмети, цегла/камені, меню, складності, паролі.
- [Cinema of the Abstract: Panic Bomber](https://cinemaoftheabstract.blogspot.com/2022/05/games-of-abstract-panic-bomber-1995.html?hl=en) — огляд VB: Skull Mode, етапи й боси, автопауза, лише 1P.
- YouTube: пошук «panic bomber gameplay».

## Непевне
- (?) Розмір поля, кількість кольорів голів, інтервал падіння запалених бомб — не знайдено.
- (?) Чи розсипається трійка після приземлення (як у Puyo) чи лежить цілою — з контексту каскадів; прямо не сказано.
- (?) Чи пускає підірвана незапалена бомба власне полумʼя далі (класичний ланцюг Bomberman) — JA каже «誘爆 — детонація від запаленої поруч», FAQ — «бомби в полумʼї вибухають»; беру ланцюг.
- (?) Як саме зʼявляються Flame Up / Level Up на полі.
- (?) Аркадна версія: JA пише, що PCE — порт аркади, але аркада (Neo Geo MVS) датована 1995 — порядок релізів неясний.
- (?) Кількість гравців: інфобокс — 1–2, JA про PCE — до 5 одночасно.
