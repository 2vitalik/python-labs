---
title: MazezaM
slug: mazezam
aka: []
family: push-slide
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2002
platforms: [ZX Spectrum, web (PuzzleScript)]
links:
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=7718522", best: true, note: "PuzzleScript-версія автора (2013): 30 мазезамів підряд, undo, назви рівнів"}
  - {kind: other, url: "https://worldofspectrum.org/pub/sinclair/games-info/m/MazezaM.txt", note: "інструкція ZX-оригіналу (2002): мета, ряди вліво-вправо, повтор коштує життя"}
  - {kind: official, url: "https://sites.google.com/site/malcolmsprojects/mazezam-home-page", note: "сторінка автора: історія, натхнення (Fall Guy, Sokoban), NP-hard"}
  - {kind: other, url: "https://gist.github.com/Malcohol/7718522", note: "код PuzzleScript: правило вільного кінця ряду, зсув усього ряду, ворота за входом, розвʼязки в коментарях"}
  - {kind: other, url: "https://github.com/Malcohol/ZXMazezaM", note: "код ZX-оригіналу (GPL-3), рівні original.mzm, формат .mzm"}
  - {kind: other, url: "https://worldofspectrum.org/archive/software/games/mazezam-malcolm-tyrrell", note: "картка World of Spectrum: 48K, freeware, 2002"}
  - {kind: other, url: "http://redfrontdoor.org/blog/?p=174", note: "Ben North: MazezaM NP-hard через 3-SAT (2012, уточнення 2017)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=MazezaM+ZX+Spectrum+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 80
mechanics: [move-4dir, keyboard-controls, push-object, impassable-cells, reach-exit, sequential-levels, level-from-txt, level-metadata, undo-unlimited, restart-level, sound-effects, +row-shift-push, +closing-entrance, +restart-costs-life]
proposes: ["+card:row-shift-push", "+card:closing-entrance", "+card:restart-costs-life", "+window:title-screen", "+window:message-screen"]
author: opus
date: 2026-11-09
---

# MazezaM — пройди лабіринт зліва направо, зсуваючи цілі ряди блоків, поки кінець ряду вільний

## Суть
Гравець заходить у «мазезам» через вхід у лівій стіні й має вийти через вихід у правій. Поле — горизонтальні ряди з блоками; штовхнувши блок уліво чи вправо, гравець зсуває **весь ряд блоків разом**, з усіма проміжками між ними. Зсув можливий лише тоді, коли клітина в дальньому кінці ряду (біля стіни) вільна. Вертикально блоки не рухаються, тож уся гра — про те, як вирівняти проміжки в сусідніх рядах, щоб прослизнути вгору-вниз.

## Поле і час
- Прямокутник у зовнішній стіні; стіни — **лише** по периметру (вимога формату `.mzm`). Внутрішні ряди — коридори однакової ширини між лівою й правою стіною.
- Вхід — проріз у лівій стіні, вихід — у правій, по одному на рівень. Праворуч від входу завжди порожня клітина.
- Один шар обʼєктів: гравець, блоки, стіни; під ними — підлога, вхід, вихід (у PuzzleScript ще клітина-ціль X за виходом).
- Хід = крок гравця (можливо зі зсувом ряду); без вводу нічого не змінюється.
- Стан рівня зручно уявляти як **зсув кожного ряду** відносно старту + позицію гравця.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | — | рух 4 напрямки; штовхає лише ліворуч/праворуч |
| Блок | object | ряд; у PuzzleScript — спрайти кінців і середини «бруска» (L / I / R) | рухається лише разом з усіма блоками свого ряду |
| Ряд | zone | горизонтальна смуга між стінами | одиниця зсуву: усі блоки — на 1 клітину разом |
| Зовнішня стіна | static | лише периметр | непрохідна; для ряду — упор |
| Вхід | gate | у лівій стіні | відкритий, поки гравець не пройшов; потім стає воротами |
| Ворота (Gate) | gate | — | закритий вхід: непрохідні, для зсуву ряду — як стіна |
| Вихід | static | у правій стіні | прохідний для гравця; для зсуву ряду — як стіна |
| Ціль X (PuzzleScript) | terrain | за виходом | гравець на ній = рівень пройдено |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(player, dir)`.
- КОЛИ `input(up|down)` → ЯКЩО `occupied(next_cell, block)` → ТО `block` (вертикально блоки не штовхаються).
- КОЛИ `input(left|right)` → ЯКЩО `occupied(next_cell, block)` і `free(row_end)` (остання клітина ряду перед стіною / воротами / виходом у напрямку поштовху) → ТО `shift(row, dir)`, `move(player, dir)`, `sound(crate_move)`.
- Зсувається **кожен** блок ряду, і ті, що позаду гравця: блок, що стояв упритул за спиною, займає клітину, яку гравець звільнив.
- КОЛИ `input(left|right)` → ЯКЩО `occupied(next_cell, block)` і `not free(row_end)` → ТО `block`, `sound(cant_move)`.
- КОЛИ `leave(player, entrance)` → ТО `set_cell(entrance, gate)`, `sound(gate)` — назад через вхід не вийти.
- КОЛИ `reach(player, exit)` → ТО `win`, `next_level` (PuzzleScript: перемога, коли гравець на клітині X за виходом).
- КОЛИ `input(retry)` → ТО `restart`, `lives(-1)` (ZX-оригінал: «retry the mazezam, but this will cost you a life»).
- КОЛИ `input(undo)` → ТО `undo(1)` (PuzzleScript; в оригіналі undo не згадано).
- Перемога: гравець вийшов праворуч. · Поразка: формально нема; глухий кут → повтор (ZX — ціною життя) або undo. · Рахунок: нема; у коді PuzzleScript автор записав розвʼязки у нотації LURD (`Pushes:` / `Moves:`, велика літера = поштовх).

## Керування і ввід
- Чотири напрямки — крок; поштовх — крок у бік блока ліворуч/праворуч.
- PuzzleScript: стрілки / WASD, `Z` — undo, `R` — рестарт; дії `X` нема (`noaction`).
- ZX: клавіші руху й повтору — (?); повтор мазезаму коштує життя.

## Вікна, меню, HUD
- `title-screen` (custom, стандарт PuzzleScript): назва, автор, старт.
- `message-screen` (custom): назва кожного мазезаму перед рівнем («First Principles», «Humble Origins» … «The Beast»), фінал «Well done. You escaped.».
- `game-screen`: поле без HUD у PuzzleScript; у ZX — лічильник життів (`lives`) і номер рівня (?).
- Переходи: title → message (назва) → game-screen → … → фінальне повідомлення.

## Фічі поза полем
- `levels-sequential`: ZX-оригінал — 10 мазезамів (`original.mzm`), PuzzleScript — 30.
- `undo` ∞ і `restart-level` у PuzzleScript; у ZX — повтор за життя.
- Формат рівнів `.mzm` (на основі `.xsb` Sokoban): `#` стіна, пробіл, `$` блок, `+` вхід, `*` вихід; метадані `;;Title:` `;;Author:` `;;Comment:` `;;Version:` — `export-import` і основа для `level-sharing` (автор просив надсилати свої мазезами).
- Правила валідності рівня: прямокутна стіна, стіни лише по периметру, один вхід у лівій стіні з вільною клітиною праворуч, один вихід у правій.

## Варіації й родичі
- ZX Spectrum (2002) → PuzzleScript (2013, AGPLv3); за словами автора, версій «many many» — список портів не перевірено.
- Натхнення: Oric-1-гра Fall Guy (з книжки «Sixty Programs for the Oric-1») і [sokoban](sokoban.md); механічний попередник, який автор згадує, — Storm Seas (Binary Arts) / Wave Breaker (ThinkFun).
- Родичі в корпусі: [sliding-tile-permutation](sliding-tile-permutation.md) (Loopover — циклічний зсув цілого ряду), [rush-hour](rush-hour.md) (блок рухається лише вздовж осі), [kwirk](kwirk.md), [lock-and-pin](../thinky/lock-and-pin.md) (поштовх одного рушить групу).
- Осі варіацій:
  - **що рухає поштовх**: один ящик (Sokoban) / ланцюг дотичних / увесь ряд з проміжками (MazezaM) / усі одного кольору (Lock & Pin);
  - **умова зсуву**: вільна клітина за ящиком / вільний кінець ряду (MazezaM) / завжди, бо тор (Loopover);
  - **напрям**: лише горизонтально (MazezaM) / уздовж осі обʼєкта (Rush Hour) / будь-який;
  - **ціна помилки**: undo ∞ / повтор за життя (ZX).

## Цікавинки для курсу
- Зсув ряду з перевіркою вільного кінця (зсуваються й блоки за спиною) — 🌱: одна перевірка й одна операція над рядком масиву.
- Вхід, що закривається за гравцем, — 🌱: подія «зійшов з клітини» → зміна типу клітини.
- Парсер `.mzm` з метаданими й валідатором рівня (периметр, один вхід/вихід, вільна клітина за входом) — 📎.
- Розвʼязувач: стан = вектор зсувів рядів + позиція гравця, BFS із відновленням шляху в LURD — 🥈 (компактний стан, але простір росте як добуток зсувів).
- Генератор мазезамів із гарантованою розвʼязністю й оцінкою складності — 🥇.
- Доведення NP-складності через 3-SAT (Ben North) як тема доповіді — 👑.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls`; `push-object` ↔ поштовх блока (тут — ряду); `impassable-cells` ↔ периметр і ворота; `reach-exit` ↔ вихід праворуч; `sequential-levels`; `level-from-txt` + `level-metadata` ↔ формат `.mzm`; `undo-unlimited` + `restart-level` (PuzzleScript); `sound-effects` ↔ CantMove / Gate / Crate Move / EndLevel.
- Близько, але не те: `row-conveyor` — смуга зсувається сама (конвеєр), тут — лише від поштовху й з умовою вільного кінця.
- **Нема** → пропозиції карток:
  - `+row-shift-push` «Поштовх зсуває весь ряд блоків, якщо кінець ряду вільний» · entities/legality · 🌱 · слот {axis: horizontal|vertical|both}.
  - `+closing-entrance` «Вхід закривається за гравцем» · entities/interact · 🌱.
  - `+restart-costs-life` «Повтор рівня коштує життя» · game-logic/lose · 🌱 · слот {lives}.

## Пропозиції до словників
- `+card:row-shift-push`, `+card:closing-entrance`, `+card:restart-costs-life` — див. вище.
- `+window:title-screen`, `+window:message-screen` — повтор (стандартні екрани PuzzleScript).
- ⏳-слова, вжиті тут: `input`, `free`, `occupied`, `move`, `shift`, `leave`, `set_cell`, `reach`, `sound`, `lives`, `undo`.

## Джерела
- ⭐ [PuzzleScript-версія](https://www.puzzlescript.net/play.html?p=7718522) — 30 мазезамів; [її код](https://gist.github.com/Malcohol/7718522): шари, правило `[> Player | Crate | ... | No Object | WallLike]`, рух усіх блоків ряду, `Late Right [Entrance | Player] -> [Gate | Player]`, перемога `All Player on Target`, назви рівнів і розвʼязки LURD у коментарях.
- [MazezaM.txt (WoS)](https://worldofspectrum.org/pub/sinclair/games-info/m/MazezaM.txt) — мета, ряди вліво-вправо, повтор коштує життя, натхнення, умови для інших реалізацій.
- [Сторінка автора](https://sites.google.com/site/malcolmsprojects/mazezam-home-page) — винайдено 2000, видано 2002, Storm Seas / Wave Breaker, NP-hard (Ben North), поправка Aaron Williams щодо NP-повноти.
- [ZXMazezaM на GitHub](https://github.com/Malcohol/ZXMazezaM) — код оригіналу, `mazezams/original.mzm` (10 рівнів), `doc/mzmFormat.txt` (формат і правила валідності).
- [Картка WoS](https://worldofspectrum.org/archive/software/games/mazezam-malcolm-tyrrell) — 48K, freeware, 2002.
- [Ben North, 2012](http://redfrontdoor.org/blog/?p=174) — зведення 3-SAT → MazezaM; з 2017 — лише NP-hard, не NP-complete.
- YouTube: пошук «MazezaM ZX Spectrum gameplay».

## Непевне
- (?) Кількість життів і чи є game over у ZX-версії; клавіші керування ZX — у відкритих текстах не названо.
- (?) Чи є в ZX-версії HUD з життями й номером рівня — не перевірено.
- (?) Порти на інші платформи («many many versions») — список не знайдено, у шапці лише ZX і web.
- (?) Розвʼязки в коментарях PuzzleScript — мінімальні за поштовхами/кроками чи просто авторські — не сказано.
