---
title: Omniban
slug: omniban
aka: []
family: thinky
also: [push-slide]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2018
platforms: [web]
links:
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=96608bd07725a3a105bb0027a7b73da3", best: true, note: "грати в браузері: 18 рівнів + бонусний"}
  - {kind: other, url: "https://api.github.com/gists/96608bd07725a3a105bb0027a7b73da3", note: "вихідний код (gist, JSON, 2018-12-22): 4 види «всевидющих» істот, що несуть вміст своєї клітини; фіктивний Player у куті"}
  - {kind: other, url: "https://www.puzzlescript.net/Gallery/gifs/96608bd07725a3a105bb0027a7b73da3.gif", note: "GIF з галереї: червона крапка проходить крізь стіни й переносить ящики"}
  - {kind: other, url: "https://raw.githubusercontent.com/increpare/PuzzleScript/master/src/games_dat.js", note: "дані галереї PuzzleScript: назва, автор Patrickgh3, лінк"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Omniban+puzzlescript", note: "пошук; геймплей"}
stage: v1
coverage: 80
mechanics: [move-4dir, move-by-input, keyboard-controls, push-object, fill-hole, all-on-targets, impassable-cells, undo-unlimited, restart-level, sequential-levels, save-progress, level-from-txt, sound-effects, +carry-cell-contents, +collision-layers]
proposes: ["+card:carry-cell-contents", "+card:collision-layers", "+axis:control", "+window:title-screen", "+window:message-screen"]
author: opus
date: 2026-11-19
---

# Omniban — Sokoban без героя: стрілки рухають «всевидющу» крапку, що проходить крізь усе й везе з собою вміст своєї клітини

## Суть
PuzzleScript-гра Patrickgh3 (2018), 18 рівнів і бонусний. Штовхача нема: стрілки рухають «всевидющу істоту» — одну кольорову крапку, яку зупиняє лише край поля. Усе, що стоїть у її клітині й дозволене її видом, їде разом з нею; вантаж, що вперся, лишається, а крапка йде далі — це єдиний спосіб його відпустити.

Чотири види крапки везуть дедалі більше: червона — лише ящики; блакитна — ще цілі й людей; жовта — ще й діри; зелена — ще й стіни. Мета — під кожною ціллю ящик; діра ковтає ящик, а людина, яку везе крапка, штовхає ящики, як у Sokoban.

## Поле і час
- Квадратна сітка 9×11 у всіх рівнях (з коду); у кожному рівні одна істота, зазвичай стартує в лівому нижньому куті, часто над стіною; колір крапки = вид.
- Розділи в коментарях коду: «move blocks» (червона) → «move blocks and goals» і «holes» (блакитна) → «human» (блакитна) → «move holes» (жовта) → «move walls» (зелена) → бонус (блакитна, 5 ящиків).
- Шари колізій: фон → {ціль, діра} → {людина, стіна, ящик} → {істота} → {фіктивний гравець}. Обʼєкт блокує лише свій шар: ціль ковзає під ящик, діра — під стіну, а істота в шарі сама, тож її спиняє тільки край.
- Покроково: хід = натискання. Ввід отримує невидимий фіктивний гравець у правому нижньому куті; правило передає рух істоті, вона — вмісту своєї клітини; далі рушій розвʼязує зіткнення пошарово. Дії нема (`noaction`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Червона істота (`Omni3`) | player | везе: ящики | рух у 4 напрямки крізь усе; ящик у своїй клітині везе з собою |
| Блакитна істота (`Omni1`) | player | везе: ящики, цілі, людей | те саме |
| Жовта істота (`Omni2`) | player | везе: + діри | те саме |
| Зелена істота (`Omni4`) | player | везе: + стіни | те саме |
| Ящик | object | — | їде з істотою; упершись у стіну, ящик чи людину, лишається; на дірі — зникає разом з нею |
| Ціль | object | — | під ящиком = виконано; блакитна, жовта й зелена істоти її везуть; упор для неї — інша ціль чи діра |
| Людина | ally | — | сама не ходить, її везе істота; штовхає ящик перед собою (лише один); стоїть над дірами |
| Діра | terrain | — | ящик на ній зникає разом з нею (засипано); людину й істоту не чіпає; жовта й зелена істоти її везуть |
| Стіна | static | — | упор для ящиків і людей; зелена істота її везе |
| Фіктивний гравець (`Player`) | player | невидимий, правий нижній кут | лише приймає ввід, сам ні на що не впливає |

## Правила (КОЛИ → ЯКЩО → ТО)
Істота і вантаж:
- КОЛИ `input(dir)` → ТО `move(omni, dir)` — крізь стіни, діри, ящики й людей; спиняє лише край поля.
- КОЛИ `input(dir)` → ЯКЩО `occupied(omni_cell, crate)` → ТО `carry(crate)` — для всіх видів.
- КОЛИ `input(dir)` → ЯКЩО `occupied(omni_cell, target|human)` and `state(omni, cyan|yellow|green)` → ТО `carry(target|human)`.
- КОЛИ `input(dir)` → ЯКЩО `occupied(omni_cell, hole)` and `state(omni, yellow|green)` → ТО `carry(hole)`.
- КОЛИ `input(dir)` → ЯКЩО `occupied(omni_cell, wall)` and `state(omni, green)` → ТО `carry(wall)`.
- КОЛИ `blocked(cargo)` → ТО `block` для вантажу: попереду обʼєкт його шару, тож вантаж лишається, а істота йде далі й стає на клітину того, що його спинило.

Людина, діри, перемога:
- КОЛИ `contact(human, crate)` → ЯКЩО `free(cell_behind_crate)` → ТО `push`; інакше людина теж стоїть на місці.
- КОЛИ `enter(crate, hole)` → ТО `disappear_both`, `sound(fill)` — ящик засипав діру; так само, коли діру принесли під ящик.
- КОЛИ `all_on(target, crate)` → ТО `win`, `next_level` (умова коду «All Target on Crate»).
- Перемога: під кожною ціллю ящик (істота може лишитись на ньому) · Поразки нема: ящик у дірі може зробити рівень нерозвʼязним → undo / restart · Рахунку нема.

## Керування і ввід
- Стрілки / WASD — рух істоти; дії нема. Z — undo, R — рестарт (стандарт PuzzleScript).
- «Взяти» — зайти в клітину обʼєкта; «відпустити» — рушити так, щоб вантаж уперся в обʼєкт свого шару.

## Вікна, меню, HUD
- `main-menu` — титульний екран PuzzleScript (`title-screen`): «Omniban», «Patrickgh3»; світло-зелений текст на чорному тлі.
- `game-screen` — поле без HUD; вид істоти видно з кольору крапки, стартова клітина в куті показує його одразу.
- `custom-window` (`message-screen`): «Thank you for playing!» → «Bonus level» → «Very thank you for playing!».
- Переходи: титул → рівні 1–18 → подяка → бонусний рівень → фінальна подяка.

## Фічі поза полем
- `levels-sequential` (18 рівнів + бонус), `undo` ∞, `restart-level`, `continue` (стандарт PuzzleScript).
- `sound-effects`: свій звук кроку для кожного виду істоти; окремі — для руху ящика, людини, стіни, цілі, діри й для засипання діри.
- У коді лишились закоментовані рівні: ще один «human» і розминка перед бонусом.

## Варіації й родичі
- [Sokoban](../push-slide/sokoban.md) — оригінал; тут штовхач лише вантаж. [increpare: мікро-Sokoban-и](increpare-micro-puzzles.md) — Sokoban-и з одним перекрученим правилом; [Magiciban](magiciban.md) — підлога зсувається й везе пасажирів; [Carto](carto.md) — тайл переїжджає разом із героїнею; [Baba Is You](baba-is-you.md) — що саме є «YOU», вирішують правила.
- Осі варіацій: **що рухає ввід** — героя (Sokoban) / усі ящики разом (мікро-Sokoban-и) / «руку», що проходить крізь світ (тут); **як відпустити вантаж** — окремою дією «взяти / відпустити» / лише упором вантажу (тут); **що можна везти** — драбина видів «ящики → + цілі й люди → + діри → + стіни»: кожен вид відкриває нову частину світу для перестановки.

## Цікавинки для курсу
- Курсор-«рука», що везе вміст клітини за списком дозволених типів, і «відпустити» лише упором — 📎.
- Шари колізій: обʼєкт блокує лише свій шар (ціль під ящиком, діра під стіною, істота крізь усе) — 📎: корисна модель для власного рушія.
- Драбина видів «що везе» як дані, а не код — 🌱.
- Людина-штовхач як вантаж: Sokoban-поштовх усередині перенесення — 📎.
- Ящик + діра → обидва зникають — 🌱 (картка `fill-hole`).
- Розвʼязувач BFS: стан = позиція істоти + усі обʼєкти; граф ходів повний, бо істота проходить крізь стіни — 🥉.

## Мапа на каталог
- Є: `move-4dir` · `move-by-input` · `keyboard-controls` ↔ стрілки; `push-object` ↔ людина штовхає ящик; `fill-hole` ↔ ящик + діра; `all-on-targets` ↔ «All Target on Crate»; `impassable-cells` ↔ стіни для ящиків і людей; `undo-unlimited` · `restart-level` · `sequential-levels` · `save-progress` · `level-from-txt` · `sound-effects`.
- **Нема** → пропозиції карток:
  - `+carry-cell-contents` «Курсор-істота везе вміст своєї клітини; відпустити — упором» · entities/interact · 📎 · слоти {carries: crate | target | human | hole | wall}.
  - `+collision-layers` «Шари колізій: обʼєкт блокує лише свій шар» · entities/legality · 📎.

## Пропозиції до словників
- `+card:carry-cell-contents`, `+card:collision-layers` — див. вище.
- `+axis:control` — значення `carrier-cursor`: ввід рухає не аватара, а «руку», що везе обʼєкти своєї клітини.
- `+window:title-screen`, `+window:message-screen` — повтор (стандартні екрани PuzzleScript).

## Джерела
- ⭐ [PuzzleScript: Omniban](https://www.puzzlescript.net/play.html?p=96608bd07725a3a105bb0027a7b73da3) — гра в браузері, 18 рівнів + бонус.
- [Вихідний код (gist через GitHub API)](https://api.github.com/gists/96608bd07725a3a105bb0027a7b73da3) — обʼєкти й шари; правила передачі руху від фіктивного гравця істоті й від істоти вмісту клітини для 4 видів; людина штовхає ящики; ящик засипає діру; умова «All Target on Crate»; коментар автора «I just put a dummy Player in the corner of each level»; gist від 2018-12-22.
- [GIF з галереї](https://www.puzzlescript.net/Gallery/gifs/96608bd07725a3a105bb0027a7b73da3.gif) — рівень з двома ящиками: червона крапка йде крізь стіни, везе ящик і перемикається на інший, коли перший уперся.
- [Дані галереї PuzzleScript](https://raw.githubusercontent.com/increpare/PuzzleScript/master/src/games_dat.js) — запис «Omniban · Patrickgh3».
- YouTube: пошук «Omniban puzzlescript».

## Непевне
- (?) Людина над дірою не падає — у коді нема правила «людина + діра»; у грі не перевірено.
- (?) Черга описує гру як «ввід рухає шари поля; кожен шар несе свої ящики, цілі, стіни»; за кодом і GIF це одна істота-крапка, що везе вміст своєї клітини.
- (?) Справжнє імʼя автора (Patrickgh3) не перевірено.
- (?) Клавіші Z / R — стандарт PuzzleScript, у коді не задані.
