---
title: SwapBot
slug: swapbot
aka: []
family: thinky
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: collect
year: 2014
platforms: [web]
links:
  - {kind: itch, url: "https://gate.itch.io/swapbot", best: true, note: "грати в браузері; опис (12 рівнів зі зростанням складності) і керування: стрілки/WASD, X/C/Space/Enter — обмін, Z/U — undo, R, M"}
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=0590a6662f9e8e6afe4a", note: "та сама гра в галереї PuzzleScript"}
  - {kind: other, url: "https://api.github.com/gists/0590a6662f9e8e6afe4a", note: "вихідний код (gist, JSON): виділення, обмін через буферну клітину, батарейки, картки, люки, телепорт; ревізії 2014 і 2018"}
  - {kind: other, url: "https://gate.itch.io/swapbot/devlog/53050/swapbot-update", note: "devlog 2018: головоломки 8 і 10 замінено новими"}
  - {kind: other, url: "https://www.puzzlescript.net/Gallery/gifs/0590a6662f9e8e6afe4a.gif", note: "GIF з галереї: рівень 3 — батарейки, виділення, обміни стін"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=SwapBot+puzzlescript", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [move-4dir, move-by-input, keyboard-controls, facing-icon, impassable-cells, item-pickup, collect-quota, reach-exit, key-and-door, selection-highlight, tutorial-window, undo-unlimited, restart-level, sequential-levels, save-progress, level-from-txt, +tile-swap, +battery-charge, +carry-one-item, +crumbling-floor, +turn-in-place, +hud-in-field]
proposes: ["+card:tile-swap", "+card:battery-charge", "+card:carry-one-item", "+card:crumbling-floor", "+card:turn-in-place", "+card:hud-in-field", "+window:title-screen", "+window:message-screen"]
author: opus
date: 2026-11-19
---

# SwapBot — робот виділяє одну клітину, потім іншу, і за батарейку міняє їхній вміст місцями: стіни, ключі, телепорт, навіть цифри номера рівня

## Суть
Пазл John M. Williams (gate) на PuzzleScript, 12 рівнів «roughly increasing difficulty»; перша версія — 2014, оновлення 2018. Робот збирає всі «+», щоб увімкнути телепорт, і йде в нього; дорогу перекривають стіни, діри, кольорові захисні плитки й люки.

Головний інструмент — обмін: X виділяє клітину перед роботом, далі він іде куди завгодно, розвертається до іншої клітини, і друге X міняє вміст обох. Міняється майже все — стіни, «+», батарейки, ключі-картки, захисні плитки, люки, телепорт, цифри номера рівня, — крім підлоги й дір; кожен обмін забирає одну батарейку.

## Поле і час
- Квадратна сітка, один екран на рівень; 12 рівнів від 6×6 до ~10×16 клітин (з коду).
- Праворуч у кожному рівні — колонка чорних дір: у ній від нижньої клітини-буфера (через неї йде обмін) росте вгору смуга заряду. Номер рівня намальовано цифрами в нижній стіні.
- Шари колізій: фон (зелена підлога) → діри → {телепорт, захисні плитки, картки, люк} → «бейдж» картки робота → {робот, стіна} → {батарейка, «+», цифри} → службові шари (буфер, смуга заряду, виділення, анімації).
- Покроково: хід = натискання; анімації обміну й променя телепорту — повторними проходами `again` (0.05 с).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| SwapBot | player | напрям погляду ↑↓←→; картка в руці: нема / червона / синя / помаранчева | крок у 4 напрямки; упершись — лише розвертається; X — виділити клітину попереду або обміняти її з виділеною |
| Підлога | terrain | — | прохідна; не обмінюється |
| Стіна | static | — | непрохідна; обмінюється |
| Діра | terrain | — | непрохідна; не виділяється, не стає ціллю обміну, не обмінюється |
| Люк | terrain | — | прохідний; щойно робот зійшов — стає дірою; обмінюється |
| «+» (чип) | pickup | — | збирається кроком; поки лишився хоч один — телепорт вимкнений; обмінюється |
| Телепорт | static | вимкнений / увімкнений | вмикається, коли «+» не лишилось; робот на увімкненому → промінь → рівень пройдено; обмінюється |
| Батарейка | pickup | — | крок на неї → +1 сегмент смуги заряду; обмінюється |
| Смуга заряду | resource | сегментів = обмінів у запасі | вертикальна смуга в правій колонці; кожен обмін знімає верхній сегмент; у рівні 2 заряд нескінченний |
| Картка-ключ ×3 | pickup | колір | крок на неї → робот носить її, попередня картка зникає; обмінюється |
| Захисна плитка ×3 | gate | колір | прохідна лише з карткою свого кольору; обмінюється |
| Цифри номера рівня | static | — | частина нижньої стіни; обмінюються разом зі стіною |
| Виділення | mark | одне на рівень | жовта рамка на клітині; зникає після обміну або коли клітина стала дірою |

## Правила (КОЛИ → ЯКЩО → ТО)
Рух:
- КОЛИ `input(dir)` → ТО `face(bot, dir)` — робот розвертається завжди, навіть якщо крок не вдасться.
- КОЛИ `input(dir)` → ЯКЩО `free(cell_ahead)` → ТО `move(bot, dir)`; інакше `block` (стіна, діра).
- КОЛИ `input(dir)` → ЯКЩО `occupied(cell_ahead, door[c])` and `not has(bot, card[c])` → ТО `block`.

Виділення й обмін:
- КОЛИ `input(action)` → ЯКЩО `custom: «на полі нема виділення»` and `not cell(cell_ahead, hole)` → ТО `mark(cell_ahead, selected)`.
- КОЛИ `input(action)` → ЯКЩО `occupied(cell_ahead, selected)` → ТО `unmark(cell_ahead)`.
- КОЛИ `input(action)` → ЯКЩО `custom: «виділення є в іншій клітині»` and `counter(battery, >, 0)` → ТО `swap(cell_ahead, selected)`, `counter(battery, -1)`, `unmark(selected)`, `animate(swap)`; у рівні з нескінченним зарядом — без `counter`.
- КОЛИ `input(action)` → ЯКЩО `custom: «є виділення»` and `cell(cell_ahead, hole)` → ТО `custom: «скасувати весь хід»` — заряд не витрачено («SwapBot cannot swap holes»).
- КОЛИ `input(action)` → ЯКЩО `counter(battery, =, 0)` → ТО `custom: «обміну немає»`.
- Що міняється: шари з переліку коду Copyable — стіна, «+», батарейка, картка, захисна плитка, люк, телепорт, цифри і сам робот; міняються пошарово через клітину-буфер унизу правої колонки. Підлога, діри, виділення й картка в руці робота лишаються на місці.

Предмети:
- КОЛИ `enter(bot, chip)` → ТО `pickup`.
- КОЛИ `enter(bot, battery)` → ТО `pickup`, `counter(battery, +1)` — новий сегмент над верхнім.
- КОЛИ `enter(bot, card[c])` → ТО `pickup`, `custom: «нова картка замінює попередню — у руці лише одна»`; колір робота показує картку.
- КОЛИ `leave(bot, trapdoor)` → ТО `set_cell(trapdoor_cell, hole)`; виділення на клітині, що стала дірою, знімається.

Телепорт і перемога:
- КОЛИ `counter(chips, =, 0)` → ТО `set_state(teleporter, active)` — перевіряється щоходу.
- КОЛИ `enter(bot, teleporter)` → ЯКЩО `state(teleporter, active)` → ТО `transform(bot, beam)`, `animate(teleport)`; коли промінь згас — `win`, `next_level` (умови коду «No Player» і «No TeleportAnim»).
- Перемога: зібрано всі «+» і робот пішов у телепорт · Поразки нема: глухий кут — undo / restart · Рахунку нема.

## Керування і ввід
- Стрілки / WASD — крок; якщо попереду перешкода — лише поворот на місці (itch: «Move/Rotate»).
- X / C / Space / Enter — «Swap»: виділити клітину попереду → піти й розвернутись до іншої → ще раз, і клітини обміняються; натиск на виділену клітину знімає виділення. Утримання X не повторює дію (`norepeat_action`).
- Кожна з двох клітин обміну — та, що перед роботом у момент свого натиску; між собою вони можуть бути на будь-якій відстані.
- Z / U — undo, R — рестарт, M — вимкнути звук (itch).

## Вікна, меню, HUD
- `main-menu` — титульний екран PuzzleScript (`title-screen`): «SwapBot», «John M. Williams».
- `custom-window` (`message-screen`) — навчальні повідомлення перед рівнями: «Collect '+' to activate teleporter» → «Press 'x' to select a tile» / «Press 'x' on another tile to swap» → «Swapping uses batteries» → «Collect key cards to access security tiles» → «SwapBot cannot swap holes» → «Trapdoors create holes»; фінал — «SwapBot has swapped everything!», «Congratulations!».
- `game-screen` — поле; HUD **усередині поля**: `energy-bar` — смуга заряду в правій колонці дір; `level-number` — цифри в нижній стіні (теж обмінювані); `selection-highlight` — жовта рамка виділеної клітини; колір робота — картка в руці (однослотовий `inventory-bar`).
- Переходи: титул → повідомлення → `game-screen` → (телепорт) → наступне повідомлення чи рівень → … → фінальні повідомлення.

## Фічі поза полем
- `levels-sequential` (12 рівнів), `undo` ∞, `restart-level`, `continue` (стандарт PuzzleScript).
- `onboarding-hints`: кожне нове правило подано повідомленням перед рівнем; у рівні 2 заряд нескінченний — навчальний.
- `sound-toggle` (M) — з опису itch; секція звуків у коді порожня.
- Оновлення 2018: рівні 8 і 10 замінено новими (devlog), реліз на itch.

## Варіації й родичі
- Версії: gist 2014 (підпис «John Williams») → 2018 (нові рівні 8 і 10, підпис «John M. Williams», сайт gate.itch.io).
- Родичі в корпусі: [Chip's Challenge](../maze-arcade/chips-challenge.md) — збери чипи, щоб відкрити вихід, кольорові ключі й двері; [Void Stranger](void-stranger.md) — жезл переносить плитку підлоги деінде (переміщення, а не обмін); [Wildfire Swap](wildfire-swap.md) — обмін лише сусідніх плиток; картка `swap-on-contact` (Baba SWAP) — обмін при вході.
- Осі варіацій: **що міняється** — сусідні плитки (match-3, Wildfire Swap) / дві будь-які клітини, виділені по черзі (тут) / аватар з обʼєктом (Baba); **ціна** — безкоштовно / заряд-батарейки (тут) / хід; **що незмінне** — фон і діри (тут): межі світу, які обмін не перетягне.

## Цікавинки для курсу
- Обмін двох довільних клітин у два кроки (виділити → обміняти) з переліком «що міняється» за шарами — 📎: просто, але треба продумати, що з чим їде.
- Заряд як ресурс обмінів і смуга заряду — 🌱.
- Одна картка в руці (нова витісняє стару) і захисні плитки за кольором — 📎.
- Люк, що стає дірою після сходження, і діра, яку не можна обміняти, — 🌱.
- HUD зі шматків поля: смуга заряду в колонці дір, номер рівня — обмінювані цифри — 📎 (жарт як дизайн).
- Розвʼязувач: стан = усе поле + заряд + картка, бо обмін зачіпає будь-яку клітину — 🥇 (простір станів вибухає, потрібні евристики).

## Мапа на каталог
- Є: `move-4dir` · `move-by-input` · `keyboard-controls` ↔ стрілки; `facing-icon` ↔ спрайт робота за напрямом погляду; `impassable-cells` ↔ стіни й діри; `item-pickup` ↔ «+», батарейки, картки; `collect-quota` + `reach-exit` ↔ усі «+» вмикають телепорт; `key-and-door` ↔ картки й захисні плитки; `selection-highlight` ↔ рамка виділення; `tutorial-window` ↔ навчальні повідомлення; `undo-unlimited` · `restart-level` · `sequential-levels` · `save-progress` · `level-from-txt`.
- **Нема** → пропозиції карток:
  - `+tile-swap` (Klocki, Railway Islands) — тут слоти {reach: дві клітини будь-де, обрані по черзі; cost: заряд; immune: підлога, діри}.
  - `+battery-charge` (Robot Odyssey) — заряд, який витрачає кожен обмін.
  - `+carry-one-item` (Atari Adventure) — одна картка-ключ у руці.
  - `+crumbling-floor` (Manic Miner) — люк провалюється, щойно з нього зійшли.
  - `+turn-in-place` (self reflection) — поворот без кроку, коли попереду перешкода.
  - `+hud-in-field` «HUD зі шматків поля: лічильники — клітини рівня» · interface/hud · 🌱.

## Пропозиції до словників
- `+card:tile-swap`, `+card:battery-charge`, `+card:carry-one-item`, `+card:crumbling-floor`, `+card:turn-in-place`, `+card:hud-in-field` — див. вище.
- `+window:title-screen`, `+window:message-screen` — повтор (стандартні екрани PuzzleScript).

## Джерела
- ⭐ [SwapBot на itch.io](https://gate.itch.io/swapbot) — гра, опис «a unique swapping mechanic … twelve levels of roughly increasing difficulty», керування.
- [Вихідний код (gist через GitHub API)](https://api.github.com/gists/0590a6662f9e8e6afe4a) — усі обʼєкти й шари, правила виділення, обміну, батарейок, карток, люків і телепорту, 12 рівнів і повідомлення; ревізії 2014-10-13…20 і 2018-10-20…21.
- [Devlog «SwapBot update»](https://gate.itch.io/swapbot/devlog/53050/swapbot-update) — 2018: нові головоломки 8 і 10; автор «a few years out» від першої версії.
- [PuzzleScript: SwapBot](https://www.puzzlescript.net/play.html?p=0590a6662f9e8e6afe4a) і [дані галереї](https://raw.githubusercontent.com/increpare/PuzzleScript/master/src/games_dat.js) — запис «SwapBot · John M. Williams · gate.itch.io».
- [GIF з галереї](https://www.puzzlescript.net/Gallery/gifs/0590a6662f9e8e6afe4a.gif) — рівень 3: збір батарейок, рамка виділення, обміни стін, смуга заряду справа.
- YouTube: пошук «SwapBot puzzlescript».

## Непевне
- (?) Робот теж у переліку обмінюваного: якщо стати на виділену клітину й обміняти, він переїде в клітину попереду, а її вміст — на його місце; виведено з коду, у грі не перевірено.
- (?) Чи можна набрати більше заряду, ніж висота правої колонки: за кодом зайва батарейка лишається на полі; не перевірено.
- (?) Звуків у коді нема — клавіша M з опису itch, можливо, нічого не вимикає.
- (?) Рік: черга дає 2018 (оновлення й реліз на itch); перша версія gist — жовтень 2014.
