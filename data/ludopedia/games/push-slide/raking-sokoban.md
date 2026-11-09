---
title: Raking Sokoban (Ilija Biškup)
slug: raking-sokoban
aka: [Sokoban з граблями]
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
year: 2024
platforms: [web]
links:
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=ea5982c0e23eb7f892325d003423f65f", best: true, note: "грати в браузері (PuzzleScript), 5 рівнів"}
  - {kind: other, url: "https://api.github.com/gists/ea5982c0e23eb7f892325d003423f65f", note: "повний код: жорстке зчеплення граблів, штовхання, тягнення, поворот від стіни, смітники, умова перемоги"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Raking+Sokoban+puzzlescript", note: "пошук; геймплей"}
stage: v1
coverage: 85
mechanics: [move-4dir, keyboard-controls, push-object, pull-object, impassable-cells, all-on-targets, facing-icon, sequential-levels, undo-unlimited, restart-level, level-from-txt, sound-effects, +attached-tool, +rotating-tool-sweep, +push-by-type, +typed-targets]
proposes: ["+role:tool", "+effect:move_group", "+card:attached-tool", "+card:push-by-type", "+card:typed-targets"]
author: opus
date: 2026-11-09
---

# Raking Sokoban — склад, де ящики рухаються лише граблями, що жорстко стирчать із гравця

## Суть
PuzzleScript-гра Іліі Бішкупа: садівник тримає граблі, які завжди займають сусідню клітину й рухаються разом із ним як одне тверде тіло. Тілом гравець ящиків не штовхає — лише граблями: граблі попереду штовхають ящик, позаду тягнуть ящик, на якому лежать, а збоку проходять над ящиками й, упершись у стіну, перескакують гравцеві за спину. З третього рівня зʼявляються смітники з протилежним правилом: їх штовхає лише тіло, а граблі об них зупиняються.

## Поле і час
- Квадратна сітка, рівні — ASCII-карти PuzzleScript (14×9 символів), ігрова частина — «острів» усередині стін; 5 рівнів.
- Хід = одне натискання: гравець і граблі зсуваються на 1 клітину одночасно; ковзання нема.
- Шари (`COLLISIONLAYERS`): фон · цілі · {гравець, стіни, ящики, смітники} · граблі окремо. Через окремий шар граблі можуть лежати поверх ящика, а від стін і смітників їх зупиняють лише окремі правила.
- Орієнтація граблів R/L/U/D = з якого боку від гравця вони стирчать; спрайт гравця щоходу повертається обличчям до граблів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | — | рух 4 напрямки разом із граблями; тілом штовхає лише смітник; у ящик тілом не входить |
| Граблі | object | бік відносно гравця: R/L/U/D | завжди в сусідній клітині; попереду — штовхають ящик; позаду — тягнуть ящик під собою; збоку — лягають поверх ящика, від стіни перескакують за спину |
| Ящик | object | — | зсувається на 1 лише граблями; має стати на ціль ящика |
| Смітник | object | — | зсувається на 1 лише тілом гравця; для граблів — стіна; має стати на ціль смітника |
| Стіна (2 спрайти) | static | — | непрохідна для всіх; другий спрайт — лише інший вигляд краю |
| Ціль ящика | terrain | — | потрібна під кожним ящиком |
| Ціль смітника | terrain | — | потрібна під кожним смітником |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО `move(player, dir)` і `move(rake, dir)` — `custom: «rigid: якщо гравець не може рушити, граблі теж стоять»`.
- КОЛИ `contact(player, crate)` → ТО `block` — тілом ящик не штовхається.
- КОЛИ `contact(player, wall)` → ТО `block`.
- КОЛИ `contact(rake, wall)` → ЯКЩО `facing(rake, dir)` (граблі попереду) → ТО `block` — увесь хід.
- КОЛИ `contact(rake, crate)` → ЯКЩО `facing(rake, dir)` і `free(cell_behind_crate)` → ТО `push`; за ящиком ящик, стіна чи смітник → `block`.
- КОЛИ `input(dir)` → ЯКЩО `facing(rake, opposite(dir))` (граблі позаду) і `occupied(rake_cell, crate)` → ТО `pull` — ящик із клітини граблів їде слідом.
- КОЛИ `input(dir)` → ЯКЩО `custom: «граблі збоку»` і `occupied(rake_next_cell, crate)` → ТО `move(rake, dir)` — граблі лягають поверх ящика, ящик стоїть.
- КОЛИ `blocked(rake)` (попереду граблів стіна або смітник) → ЯКЩО `custom: «граблі збоку»` → ТО `rotate(rake, 90)` — `custom: «граблі переносяться в клітину за спиною гравця й їдуть за ним»`, `sound(rake)`; гравець робить крок.
- КОЛИ `contact(player, trashcan)` → ЯКЩО `free(cell_behind)` → ТО `push`.
- КОЛИ `contact(rake, trashcan)` → ЯКЩО `facing(rake, dir)` → ТО `block` (у коді — `cancel` усього ходу).
- Після кожного ходу: ТО `face(player, rake_side)`.
- КОЛИ `all_on(crate, crate_target)` і `all_on(trashcan, trash_target)` → ТО `win`, `next_level`.
- КОЛИ `input(z)` → ТО `undo(1)` · КОЛИ `input(r)` → ТО `restart`.
- Перемога: усі ящики й усі смітники на своїх цілях. · Поразка: нема (глухий кут → undo/рестарт). · Рахунок: нема.

## Керування і ввід
- Стрілки / WASD — крок гравця з граблями; кнопка дії (X) оголошена штатно, але правил на неї нема.
- Z — undo без ліміту, R — рестарт рівня; Esc — у титульне меню (стандарт PuzzleScript (?)).
- Ні вибору інструмента, ні окремої команди повороту: граблі повертаються лише від стіни.

## Вікна, меню, HUD
- `splash-screen` / `main-menu` — титул PuzzleScript: назва, автор, «start game» / «continue» (?).
- `game-screen` — лише поле, без HUD.
- `custom-window` — екран `message` перед 3-м рівнем: «So now they're leaving Trashcans around as well?».
- Переходи: титул → рівні 1–2 → повідомлення → рівні 3–5 → фінал.

## Фічі поза полем
- `levels-sequential` (5 рівнів), `undo` (∞), `restart-level`.
- Звуки: рух ящика, рух смітника, крок гравця, поява граблів після повороту.
- Код відкритий: гру можна вставити в редактор PuzzleScript і правити рівні (readme гісту).

## Варіації й родичі
- Осі варіацій:
  - **хто штовхає**: тіло (`sokoban`) / лише інструмент (Raking Sokoban, ящики) / тіло, але не інструмент (Raking Sokoban, смітники);
  - **інструмент**: жорсткий, завжди поруч (Raking Sokoban) / повертається за командою й замітає дугу (`thinky/stephens-sausage-roll`, виделка) / багатосегментна палиця (`thinky/elephant-in-a-bottle`);
  - **інструмент збоку**: замітає й штовхає (виделка SSR) / проходить над обʼєктом (граблі) / від стіни перескакує за спину (граблі);
  - **цілі**: одного типу (`sokoban`) / типізовані, свої для кожного вантажу (ящики vs смітники).
- Родичі: `sokoban`, `kwirk` (поворот турнікета від поштовху), `thinky/stephens-sausage-roll`, `thinky/elephant-in-a-bottle`.

## Цікавинки для курсу
- Аватар із двох клітин (гравець + інструмент), бік інструмента як стан і перевірки «попереду / позаду / збоку» — 📎.
- Три режими інструмента від відносного положення (штовхає / тягне / лягає поверх) — 🥉.
- Автоповорот інструмента від стіни за спину гравця — 📎.
- Два класи вантажу з різними «штовхачами» й своїми цілями — 🌱.
- Інструмент на окремому шарі: перекриття з ящиком — легальний стан (як `COLLISIONLAYERS`) — 🌱.
- Розвʼязувач BFS: стан = позиція гравця + бік граблів + ящики + смітники — 🥇.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ стрілки; `push-object` ↔ граблі попереду; `pull-object` ↔ граблі позаду тягнуть ящик; `impassable-cells` ↔ стіни; `all-on-targets` ↔ обидва типи цілей; `facing-icon` ↔ гравець дивиться на граблі; `sequential-levels` ↔ 5 рівнів; `undo-unlimited` + `restart-level` ↔ Z / R; `level-from-txt` ↔ ASCII-карти; `sound-effects` ↔ звуки рухів.
- **Нема** → пропозиції карток:
  - `+attached-tool` «Інструмент, жорстко зчеплений з аватаром» · entities/interact · 🥉 · слоти {ahead: push, behind: pull, side: pass|sweep}.
  - `+rotating-tool-sweep` (вже пропонована SSR) · слот {trigger: command|on-wall} — тут поворот лише від стіни.
  - `+push-by-type` «Хто що може штовхати» · entities/legality · 🌱 · слот {pusher → kinds}: тіло → смітники, граблі → ящики.
  - `+typed-targets` «Цілі свого типу для кожного виду вантажу» · game-logic/win · 🌱 — дитина `all-on-targets`.

## Пропозиції до словників
- `+role:tool` — інструмент, зчеплений з аватаром (граблі; виделка Stephen's Sausage Roll).
- `+effect:move_group` — зсунути зчеплену групу як одне тверде тіло (гравець + граблі; уже просила Elephant in a Bottle).
- `+card:attached-tool` · `+card:push-by-type` · `+card:typed-targets` — див. «Мапа на каталог».

## Джерела
- ⭐ [PuzzleScript: Raking Sokoban](https://www.puzzlescript.net/play.html?p=ea5982c0e23eb7f892325d003423f65f) — гра в браузері.
- [GitHub Gist (API)](https://api.github.com/gists/ea5982c0e23eb7f892325d003423f65f) — сирці: `rigid [ > player] [rake] -> [ > player] [ > rake]`, тягнення `[ > RakeSpriteL Crate] -> [ > RakeSpriteL > Crate]`, штовхання граблями, поворот `[ | > player][ > rake | wall]`, смітник `[ > Player | Trashcan]` і `cancel` для граблів, перемога «all crate on Target / all Trashcan on TargetTrash», 5 карт; гіст створено 17.10.2024.
- YouTube: пошук «Raking Sokoban puzzlescript».

## Непевне
- (?) Рік 2024 — за датою гісту; чи гра публікувалась ще деінде (itch, галерея PuzzleScript) — не перевірено.
- (?) Рідкісні стани виведено з коду, а не з гри: граблі лежать на ящику, а гравець іде в їхній бік (за кодом хід блокується — ящик під граблями не штовхається); `rigid` разом із тягненням, коли гравець упирається.
- (?) Титульний екран, Esc і фінальний екран — стандарт PuzzleScript, у цій грі не перевірені.
