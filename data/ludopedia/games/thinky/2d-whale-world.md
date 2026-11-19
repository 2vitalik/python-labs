---
title: 2D Whale World
slug: "2d-whale-world"
aka: []
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2013
platforms: [web]
links:
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=6841165", best: true, note: "грати в браузері (PuzzleScript, 8 рівнів)"}
  - {kind: other, url: "https://api.github.com/gists/6841165", note: "вихідний код — анонімний gist від 2013-10-05: правила, шари колізії, рівні"}
  - {kind: other, url: "https://gist.githubusercontent.com/anonymous/6841165/raw/eae110632df83ac16737955a2b2641cc2b39d4e3/script.txt", note: "сирий script.txt"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=2D+Whale+World+increpare", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [move-4dir, keyboard-controls, impassable-cells, sequential-levels, undo-unlimited, restart-level, level-from-txt, objective-text, +beam-push, +push-off-edge, +no-direct-push, +cancel-turn-if-blocked]
proposes: ["+trigger:beam_hit", "+role:beam-block", "+effect:cancel_turn", "+card:beam-push", "+card:push-off-edge"]
author: opus
date: 2026-11-19
---

# 2D Whale World — кита не штовхнеш: перетни його промінь, і він зсунеться здалеку; виштовхни всіх у порожнечу

## Суть
Пласка PuzzleScript-версія китових рівнів English Country Tune від самого increpare (2013): коментар у коді — «a port of the Whale section of my puzzle game English Country Tune». Гравець ходить кімнатою зі стінами; кити напряму не штовхаються, але світять жовтими променями вздовж усього свого рядка й стовпця. Коли гравець **поперек** заходить у клітину променя, кит зсувається на клітину в той самий бік, хоч би де стояв; мета — виштовхати кожного кита в порожнечу за стінами («Push a whale off to free it»).

## Поле і час
- Квадратна сітка; мапа — ASCII у коді: `0` порожнеча, `.` підлога, `#` стіна, `P` гравець, `W` кит. Вісім рівнів, найбільший — 17×16 клітин; у 5 з 8 рівнів кілька китів.
- Шари колізії: фон → порожнеча → {гравець, стіна, кит} → горизонтальний промінь → вертикальний промінь. Промені лежать в окремих шарах, тож проходять крізь стіни й не заважають руху.
- Покроково: правила застосовуються на кожне натискання. Промені — похідний шар: їх стирають і кладуть заново наприкінці кожного ходу (`late`) і на старті рівня (`run_rules_on_level_start`).
- Прапорець `require_player_movement`: якщо гравець не зрушив (уперся), увесь хід скасовано — кити теж стоять.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | — | крок у 4 напрямки; у порожнечу не заходить; кита й стіну не штовхає |
| Кит | object | позиція | дотиком не зсувається; зсувається на 1, коли гравець поперек перетинає його промінь; у порожнечі зникає («звільнений») |
| Горизонтальний промінь (HBeam) | zone | рядок кита | на всіх клітинах рядка обабіч кита до краю мапи; реагує на вертикальний рух гравця |
| Вертикальний промінь (VBeam) | zone | стовпець кита | те саме для стовпця; реагує на горизонтальний рух |
| Стіна | static | — | непрохідна для гравця й кита; промінь проходить крізь неї |
| Підлога | terrain | — | звичайна клітина |
| Порожнеча | zone | — | гравцеві закрита; кит, що заїхав, зникає |

## Правила (КОЛИ → ЯКЩО → ТО)
Вихідний код правил (`script.txt`, по порядку): `[ > player | void ] -> [ player | void ]` · `Horizontal [ > Player | VBeam ] -> [ > Player | > VBeam ]` · `Vertical [ > Player | HBeam ] -> [ > Player | > HBeam ]` · `[ Whale | ... | Perpendicular Beam ] -> [ Perpendicular Whale | ... | Perpendicular Beam ]` · `late [ Whale Void ] -> [ Void ]` · `[ Beam ] -> []` · `late Horizontal [ Whale | ... | ] -> [ Whale | ... | HBeam ]` · `late Vertical [ Whale | ... | ] -> [ Whale | ... | VBeam ]`; перемога — `No Whale`. Далі — те саме реченнями:
- КОЛИ `input(dir)` → ЯКЩО `cell(next_cell, void)` → ТО `block` — гравець у порожнечу не ступає.
- КОЛИ `input(dir)` → ЯКЩО `occupied(next_cell, wall)` or `occupied(next_cell, whale)` → ТО `block` — гравець, стіна й кит в одному шарі колізії, правила поштовху нема.
- КОЛИ `input(left|right)` → ЯКЩО `occupied(next_cell, vbeam)` → ТО `custom: «вертикальний промінь отримує рух гравця»`.
- КОЛИ `input(up|down)` → ЯКЩО `occupied(next_cell, hbeam)` → ТО `custom: «горизонтальний промінь отримує рух гравця»`.
- КОЛИ `custom: «у стовпці чи рядку кита промінь рушив поперек»` → ТО `move(whale, dir)` у той самий бік — зсуваються всі кити цього стовпця чи рядка.
- КОЛИ `custom: «кит зсувається»` → ЯКЩО `occupied(target, wall)` or `occupied(target, whale)` or `occupied(target, player)` → ТО `block` для кита; гравець свій крок робить.
- КОЛИ `enter(whale, void)` → ТО `disappear(whale)`.
- КОЛИ `turn_end` → ТО `custom: «стерти промені й покласти заново від кожного кита по всьому рядку й стовпцю до краю мапи»`.
- КОЛИ `blocked(player)` → ТО `custom: «скасувати весь хід»`.
- КОЛИ `all_gone(whale)` → ТО `win`, `message(level N of 8)`, `next_level`; після 8-го — «all the 2d whales are freed».
- Перемога: на полі нема жодного кита (`No Whale`). · Поразка: нема; кит, загнаний у кут чи під стіну, — глухий кут → undo / restart. · Рахунок: нема.

## Керування і ввід
- Стрілки / WASD — крок; Z — undo без ліміту; R — рестарт рівня; Esc — меню (стандарт PuzzleScript; прапорців `noundo` / `norestart` у коді нема).
- Дії X нема: у правилах немає `action`.

## Вікна, меню, HUD
- `main-menu` (титул PuzzleScript): «2D Whale World», автор increpare, старт / продовження (?).
- `custom-window` повідомлення: «Push a whale off to free it.» перед першим рівнем, далі «level N of 8», фінал «all the 2d whales are freed».
- `game-screen`: лише поле (палітра mastersystem: помаранчева порожнеча, синя підлога, коричневі кити, жовті промені), без HUD.
- Переходи: main-menu → game-screen → (усі кити) повідомлення → наступний рівень → … → фінальне повідомлення.

## Фічі поза полем
- `levels-sequential` (8 рівнів); `undo` ∞ і `restart-level` — вбудовані в рушій.
- Відкритий код: вставити `script.txt` у редактор PuzzleScript (readme gist-а) — можна правити правила й рівні, по суті `level-editor` + `custom-rules`.

## Варіації й родичі
- Батько — `games/thinky/english-country-tune.md`: там кити на гранях 3D-структури й зникають, коли їхні промені ні на що не падають; тут — пласка сітка, промінь завжди сягає краю мапи, звільнення — порожнеча. Цей файл дає точні правила китового шару, які в ECT позначено (?).
- Родичі у PuzzleScript: `games/thinky/increpare-micro-puzzles.md`, `games/thinky/increpare-sokoban-variants.md` (той самий автор, Sokoban зі зміненим правилом руху); виштовхування за край — тег `+push-off-edge` (ECT).
- **Осі варіацій:** як рухати обʼєкт — дотиком (Sokoban) / перетином його лінії здалеку (кити); промінь — до першої перешкоди / наскрізь до краю (тут); мета — обʼєкти на цілі / усі обʼєкти за край; на скількох китів діє один перетин — на одного / на всіх у лінії (тут).

## Цікавинки для курсу
- Віддалений поштовх: перетин променя зсуває кита в бік кроку — 📎.
- Промені як похідний шар, що перебудовується наприкінці ходу з позицій китів, — 📎.
- Шари колізії (фон / порожнеча / тверде / промені) замість однієї клітинної змінної — 🥉.
- `require_player_movement`: хід, у якому гравець не зрушив, скасовано цілком — 🌱.
- Розвʼязувач BFS по станах (позиції гравця й китів) — 🥈.
- PuzzleScript-правило з `...`: шаблон «кит, будь-які клітини, промінь» — сканування рядка як одне правило переписування — 🥉.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ стрілки; `impassable-cells` ↔ стіни (і порожнеча для гравця); `sequential-levels` ↔ 8 рівнів; `undo-unlimited` + `restart-level` ↔ Z / R; `level-from-txt` ↔ ASCII-мапи в коді; `objective-text` ↔ «Push a whale off to free it.».
- **Нема** → пропозиції карток:
  - `+beam-push` (уже в корпусі: English Country Tune) «Обʼєкт рухається, коли гравець перетинає його промінь» · entities/interact · 🥉.
  - `+push-off-edge` (уже в корпусі) «Мета — виштовхнути обʼєкти за край поля» · game-logic/win · 🌱.
  - `+no-direct-push` «Обʼєкт не штовхається дотиком, лише здалеку» · entities/legality · 🌱.
  - `+cancel-turn-if-blocked` «Хід без руху гравця скасовано цілком» · game-logic/history · 🌱.

## Пропозиції до словників
- `+trigger:beam_hit` — сутність увійшла в промінь іншої (уже пропонував English Country Tune); тут — поперек променя.
- `+role:beam-block` — блок, що випромінює промені й керується ними (кит; уже пропонував English Country Tune).
- `+effect:cancel_turn` — скасувати весь хід разом з усіма наслідками (PuzzleScript `require_player_movement`, `cancel`).
- `+card:beam-push`, `+card:push-off-edge` — механік нема в каталозі.

## Джерела
- ⭐ [PuzzleScript: грати](https://www.puzzlescript.net/play.html?p=6841165) — гра в браузері.
- [GitHub gist API: 6841165](https://api.github.com/gists/6841165) — повний `script.txt` (прелюдія, обʼєкти, шари колізії, правила, `No Whale`, 8 рівнів з повідомленнями) і `readme.txt`; дата 2013-10-05.
- [script.txt (raw)](https://gist.githubusercontent.com/anonymous/6841165/raw/eae110632df83ac16737955a2b2641cc2b39d4e3/script.txt) — той самий код.
- YouTube: [пошук «2D Whale World increpare»](https://www.youtube.com/results?search_query=2D+Whale+World+increpare).

## Непевне
- (?) На increpare.com гри не знайдено (переглянуто каталог до 2011 року) — опубліковано, схоже, лише як gist; лінк на сайт із черги не подаю.
- (?) Порядок ходу в рушії (рух гравця й китів в одній фазі): що буде, якщо кит зсувається в клітину, звідки саме йде гравець, — виведено з семантики PuzzleScript, не перевірено грою.
- (?) Пункти титульного меню («continue») і свайп-керування на мобільному — стандарт PuzzleScript з памʼяті.
