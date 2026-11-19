---
title: Stand Off
slug: stand-off
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
year: 2016
platforms: [web]
links:
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=14a2f967a1978e28e91118126ac22d6a", best: true, note: "грати в браузері; 10 рівнів; код — через «hack»"}
  - {kind: other, url: "https://gist.github.com/Hand-E-Food/14a2f967a1978e28e91118126ac22d6a", note: "вихідний код PuzzleScript: обʼєкти, шари, правила лінії зору й пострілу, ліміт двох револьверів, 10 рівнів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Stand+Off+PuzzleScript+Mark+Richardson", note: "пошук; геймплей"}
stage: v1
coverage: 85
mechanics: [move-4dir, move-by-input, keyboard-controls, push-object, impassable-cells, line-of-sight-attack, projectile-shot, touch-death, player-death, reach-exit, mode-indicator, sequential-levels, undo-unlimited, restart-level, sound-effects, +attached-tool, +aim-separate-from-move, +see-through-block, +aim-blocks-sight]
proposes: ["+card:aim-blocks-sight", "+card:attached-tool", "+card:see-through-block"]
author: opus
date: 2026-11-19
---

# Stand Off — вестерн-дуель на клітинах: бандит стріляє, щойно бачить тебе, якщо ти не цілишся в нього

## Суть
Маленька PuzzleScript-гра Mark Richardson: ковбой має вийти з містечка через вихід у стіні, а нерухомі бандити стріляють уздовж рядків і стовпців, щойно між ними й гравцем нема перешкоди. Захист — «мексиканська дуель»: витягнутий револьвер стоїть у сусідній клітині дулом у свій бік і закриває бандитам лінію зору саме з того напрямку. Револьверів два, тож прикрити можна лише два напрямки з чотирьох; решту закривають стіни, ящики (їх можна штовхати) і самі бандити. Вікна непрохідні, але прозорі — крізь них видно й стріляють.

## Поле і час
- Квадратна сітка, один екран; рівні від 10×11 до 17×17 клітин разом зі стінами (з коду). Шари: тло · тверді обʼєкти (стіна, вікно, гравець, бандит, ящик, револьвер, труп) · прозорий шар (вихід, позначка режиму, промінь зору, куля).
- Покроково: хід — крок, перемикання режиму або витягування/ховання револьвера; після кожного ходу в `late`-фазі рахується лінія зору й постріли.
- Куля летить анімацією `again` (0,05 с на клітину) без участі гравця — після пострілу врятуватися вже не можна.
- Видимість повна: усе поле видно, туману нема.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Ковбой | player | режим ходу / режим зброї | рух 4 напрямки; у режимі зброї стрілки витягують або ховають револьвер замість кроку |
| Револьвер | object | напрямок дула (U/D/L/R); не більше 2 на полі | стоїть у сусідній клітині дулом від гравця; рухається разом із гравцем; непрозорий для зору; упершись у перешкоду — зникає (ховається) |
| Бандит | enemy | — | нерухомий; бачить гравця по рядку чи стовпцю до першої непрозорої клітини й стріляє; сусідство з ним — смерть |
| Куля | projectile | — | зʼявляється перед бандитом і летить до гравця; влучання → труп; розбиває вікна на шляху |
| Ящик | object | — | штовхається на 1, якщо за ним вільно; непрозорий щит |
| Стіна | static | — | непрохідна, непрозора |
| Вікно / розбите вікно | static | — | непрохідне для гравця й ящиків, прозоре для зору й куль; куля перетворює вікно на розбите (лише вигляд) |
| Вихід | static | один або кілька в рамці | гравець на виході — перемога; непрозорий; револьвер на виході зникає |
| Труп | static | — | стан гравця після влучання; керування вже нема — лише undo/рестарт |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(X)` → ЯКЩО `state(player, gun_mode)` → ТО `clear_state(player, gun_mode)`; інакше `set_state(player, gun_mode)` — перемикання теж є ходом.
- КОЛИ `input(dir)` → ЯКЩО `state(player, gun_mode)` and `occupied(next_cell, gun)` → ТО `disappear(gun)` (сховати).
- КОЛИ `input(dir)` → ЯКЩО `state(player, gun_mode)` and `not free(next_cell)` → ТО `block` — хід скасовано повністю.
- КОЛИ `input(dir)` → ЯКЩО `state(player, gun_mode)` and `free(next_cell)` and `count(gun, <, 2)` → ТО `place(player, gun)` у сусідню клітину дулом у напрямку вводу; гравець стоїть.
- КОЛИ `input(dir)` → ЯКЩО `not state(player, gun_mode)` and `free(next_cell)` → ТО `move(player, dir)`, `move(gun, dir)` для кожного витягнутого револьвера.
- КОЛИ `contact(player, crate)` → ЯКЩО `free(cell_behind)` → ТО `push`, `move(player, dir)`; інакше `block` (ланцюга ящиків нема).
- КОЛИ `blocked(gun)` (попереду стіна, вікно, ящик чи бандит) → ТО `disappear(gun)` — гравець іде, револьвер ховається.
- КОЛИ `enter(gun, exit)` → ТО `disappear(gun)`.
- КОЛИ `adjacent(player, bandit)` → ТО `transform(player, corpse)`, `lose` — впритул не рятує навіть револьвер.
- КОЛИ `line_of_sight(bandit, player)` (промінь іде від гравця 4 напрямками до першої непрозорої клітини: стіна, ящик, револьвер, бандит, вихід, куля; вікна й трупи прозорі) → ТО `spawn_at(bullet, клітина перед бандитом)`.
- КОЛИ `spawned(bullet)` → ТО `move(bullet, dir_to_player)` щотіку анімації до влучання.
- КОЛИ `contact(bullet, player)` → ТО `disappear(bullet)`, `transform(player, corpse)`, `lose`.
- КОЛИ `enter(bullet, window)` → ТО `set_cell(window, broken_window)`.
- КОЛИ `enter(player, exit)` → ТО `win`, `next_level`.
- КОЛИ `input(Z)` → ТО `undo(1)`.
- КОЛИ `input(R)` → ТО `restart`.
- Перемога: гравець на будь-якому виході. · Поразка: влучання або сусідство з бандитом → труп, рівень стоїть до undo/рестарту. · Рахунку нема.

## Керування і ввід
- Стрілки або WASD — крок; X — перемкнути режим ходу / режим зброї (`norepeat_action`: утримання X не повторює дію).
- У режимі зброї стрілка в бік порожньої клітини витягує револьвер, у бік уже витягнутого — ховає; у перешкоду — нічого.
- Z — undo, R — рестарт, Esc — меню (стандарт PuzzleScript); миші нема.

## Вікна, меню, HUD
- `main-menu` — титул PuzzleScript: назва, автор, «start game» / «continue».
- `custom-window` — текстові повідомлення: два вступні («Don't let them varmints point a gun at ya unless yer pointin' one at them too», підказка про X) і фінальне.
- `game-screen` — поле без HUD; режим зброї видно кольором спрайта ковбоя (`mode-indicator`).
- Переходи: титул → повідомлення → рівень 1 → … → рівень 10 → фінальне повідомлення → титул.

## Фічі поза полем
- `levels-sequential`: 10 рівнів; автозбереження поточного рівня (стандарт PuzzleScript, «continue»).
- `undo` без ліміту, `restart-level`; звуки на витягування й ховання револьвера, поштовх ящика, постріл, розбите вікно, смерть, кінець рівня.
- Нема налаштувань, підказок, редактора.

## Варіації й родичі
- Родичі в корпусі: [Adventures of Lolo](../push-slide/adventures-of-lolo.md) (погляд Медузи по лінії, щити-блоки), [DROD](drod.md) (меч як окрема клітина поруч з аватаром), [Hoplite](../tactics/hoplite.md) (лучники бʼють по лінії), [Hitman GO](../push-slide/hitman-go.md) (вартові дивляться в одному напрямку), [The Observer's Paradox](the-observers-paradox.md) (зір як правило).
- Осі варіацій:
  - **що зупиняє постріл**: лише перешкоди (Lolo) / власний приціл гравця (тут) / нічого;
  - **як бачить ворог**: 4 напрямки (тут) / один напрямок погляду (Hitman GO) / радіус;
  - **скільки «щитів-прицілів»**: 0 / 2 одночасно (тут) / необмежено;
  - **що робить ворог, побачивши**: миттєвий постріл / снаряд-анімація (тут) / наближається.

## Цікавинки для курсу
- Промінь зору від гравця 4 напрямками до першої непрозорої клітини з таблицею «прозоре / непрозоре» (вікно прозоре, але непрохідне) — 📎.
- Приціл як непрозорий обʼєкт поруч з гравцем: «ворог не стріляє в того, хто цілиться в нього» без жодного окремого правила — 🌱 поверх променя, але гарна вправа на моделювання.
- Револьвери, жорстко зчеплені з гравцем: рухаються разом, зникають, упершись у перешкоду, не більше двох — 🥉.
- Режим вводу на X: ті самі стрілки або ходять, або цілять — 🌱.
- Куля як анімована сутність, що летить кілька тіків і розбиває вікна по дорозі — 📎.
- Розвʼязувач BFS: стан = позиція гравця + револьвери + ящики, перехід відкидає стани з видимим бандитом — 🥈.

## Мапа на каталог
- Є: `move-4dir` · `move-by-input` · `keyboard-controls` ↔ крок; `push-object` ↔ ящики; `impassable-cells` ↔ стіни, вікна; `line-of-sight-attack` ↔ бандити; `projectile-shot` ↔ куля; `touch-death` ↔ сусідство з бандитом; `player-death` ↔ труп; `reach-exit` ↔ вихід; `mode-indicator` ↔ колір ковбоя в режимі зброї; `sequential-levels` · `undo-unlimited` · `restart-level` · `sound-effects`.
- **Нема** → пропозиції карток:
  - `+aim-blocks-sight` «Приціл закриває ворогові лінію зору» · entities/combat · 🌱 · слоти {max_aims: 2} — дитина `line-of-sight-attack`.
  - `+attached-tool` (вже в корпусі, Raking Sokoban) — тут слоти {ahead: block_sight, on_blocked: vanish, max: 2}.
  - `+see-through-block` (вже в корпусі, LaserTank) — вікно: непрохідне, але прозоре для зору й куль.
  - `+aim-separate-from-move` (вже в корпусі) — X перемикає стрілки між ходом і прицілом.

## Пропозиції до словників
- `+card:aim-blocks-sight`, `+card:attached-tool`, `+card:see-through-block` — див. «Мапа на каталог».
- ⏳-слова, вжиті тут: `input`, `adjacent`, `blocked`, `spawned`, `count`, `place`, `spawn_at`, `set_state`, `clear_state`, `set_cell`, `transform`, `undo`, `restart`, `next_level`.

## Джерела
- ⭐ [PuzzleScript: грати](https://www.puzzlescript.net/play.html?p=14a2f967a1978e28e91118126ac22d6a) — сама гра.
- [Gist із кодом](https://gist.github.com/Hand-E-Food/14a2f967a1978e28e91118126ac22d6a) — OBJECTS, LEGEND (Obstacle, Shroud), COLLISIONLAYERS, RULES (режим, револьвери, ліміт двох через `random`-перевірку, лінія зору, куля), WINCONDITIONS `any Exit on Player`, 10 рівнів і тексти; прочитано через `api.github.com/gists/<id>` разом з історією ревізій.
- YouTube: [пошук «Stand Off PuzzleScript»](https://www.youtube.com/results?search_query=Stand+Off+PuzzleScript+Mark+Richardson).

## Непевне
- (?) Рік: gist створено 24.10.2016, останні зміни коду — 25.10.2016; дата 2018 у черзі — це, найімовірніше, оновлення метаданих gist (17.03.2018).
- (?) Чи кулі кількох бандитів, що бачать гравця одночасно, летять разом — з коду так (правило зору застосовується до кожного), у грі не перевірено.
- (?) Пункти титульного меню (continue / level select) залежать від версії рушія PuzzleScript, яку віддає сайт.
