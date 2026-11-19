---
title: "Shall We Golf? (みんなでGOLF！)"
slug: shall-we-golf
aka: ["みんなでGOLF！"]
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
year: 2021
platforms: [web (HTML5, PuzzleScript)]
links:
  - {kind: itch, url: "https://nebu-soku.itch.io/golfshall-we-golf", best: true, note: "грати в браузері; опис EN/JA: «Human Barricade», «Your club belongs to everyone»; X — удар, стрілки — приціл і передача ключки; 15 лунок"}
  - {kind: other, url: "https://www.puzzlescript.net/editor.html?hack=86a02fbb49c6c73b4bf899dab5bc63ca", note: "сирець у редакторі PuzzleScript (лінк зі сторінки itch)"}
  - {kind: other, url: "https://api.github.com/gists/86a02fbb49c6c73b4bf899dab5bc63ca", note: "gist зі script.txt (22.03.2021): правила удару, бункера, води, сліду друзів, передачі ключки; 15 мап + 5 закоментованих"}
  - {kind: other, url: "https://nebu-soku.itch.io/golfshall-we-golf/devlog/234508/system-update32221", note: "девлог 22.03.2021: точніше навчальне повідомлення, курсор над тим, у кого ключка"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Shall+We+Golf+puzzlescript+nebu+soku", note: "пошук; геймплей"}
stage: v1
coverage: 80
mechanics: [move-4dir, keyboard-controls, inertia-slide, impassable-cells, floor-types, all-on-targets, undo-unlimited, restart-level, sequential-levels, level-from-txt, tutorial-window, movement-animation, sound-effects, +trail-wall, +follower-chain, +stop-on-entity, +fall-into-water, +tool-relay, +pass-over-target, +short-hit-terrain]
proposes: ["+card:tool-relay", "+card:pass-over-target", "+card:short-hit-terrain", "+ui:holder-marker", "+axis:actors"]
author: opus
date: 2026-11-19
---

# Shall We Golf? — гольф на сітці: мʼяч летить до першої перешкоди, а друзі, що йдуть за тобою чергою, стають бортиками й беруть ключку

## Суть
Пазл nebu soku на PuzzleScript: гольфіст веде за собою чергу друзів по зеленому полю, і мʼяч треба зупинити рівно на лунці. Удар посилає мʼяч по прямій, доки перед ним не опиниться перешкода, — він пролітає й воду, й саму лунку («hard not to hit too far»). Тому головний інструмент — власна черга: кожна клітина, яку покинув гольфіст, назавжди зайнята другом-«барикадою», а ключку можна передати будь-якому другові поруч, і бити буде вже він.

JA-назва — пародія на відому японську гру (слова автора в коментарях); 15 лунок, близько години гри.

## Поле і час
- Квадратна сітка 14×11 на кожну лунку; зелене поле посередині, довкола — «поза полем» (синє тло), яке непрохідне й зупиняє мʼяч.
- Шари: тло → трава / вода / бункер / лунка → гольфіст, друзі, дерева, мʼяч → ключка, курсор → напис перемоги.
- Хід = натискання; світ не рухається без вводу, крім анімацій. Політ мʼяча — по клітині на тік `realtime_interval 0.13` (≈0,13 с), тож удар видно як короткий кидок.
- Камери нема: уся лунка на одному екрані.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гольфіст (лідер) | player | з ключкою / без | рух 4 боки по траві й бункеру; не заходить на мʼяч, лунку, дерево, воду, поза поле |
| Друг | ally | 3 кольори футболок по колу | стоїть на кожній клітині, яку покинув лідер, назавжди; барʼєр для мʼяча й лідера; може взяти ключку |
| Ключка | object | у лідера або в одного друга | хто її тримає, той бʼє; власника позначає червоний курсор |
| Мʼяч | object | стоїть / летить у напрямку | після удару летить по прямій до першої перешкоди |
| Лунка з прапорцем | static | — | мʼяч, що зупинився на ній, — забитий; летючий мʼяч її минає |
| Трава | terrain | — | клітини поля |
| Поза полем | static | — | непрохідне; зупиняє мʼяч |
| Дерево | static | — | непрохідне; зупиняє мʼяч |
| Вода | hazard | — | гольфістові непрохідна; мʼяч над нею пролітає, але зупинений на ній тоне |
| Бункер | terrain | — | гольфіст ходить; удар з бункера — рівно 1 клітина |
| Старт | terrain | — | клітина появи; з неї тягнеться черга друзів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` (трава, бункер) → ТО `move(leader, dir)`, `spawn_at(friend, old_cell)` — на покинутій клітині стає друг.
- КОЛИ `input(dir)` → ЯКЩО `cell(next, ball|hole|tree|water|out)` → ТО `block`.
- КОЛИ `input(dir)` → ЯКЩО `occupied(next, friend)` → ТО `give(friend, club)`, `take(leader, club)`, `set_state(leader, still)` — замість кроку ключка переходить другові, лідер стоїть і сам стає барʼєром.
- КОЛИ `input(dir)` → ЯКЩО `has(friend, club)` and `occupied(next, friend)` → ТО `give(next_friend, club)`, `take(friend, club)`; немає сусіда в тому напрямку → `block` (друг з ключкою не ходить).
- КОЛИ `input(dir)` → ЯКЩО `has(friend, club)` and `occupied(next, leader)` → ТО `give(leader, club)`, `clear_state(leader, still)` — лідер знову ходить.
- КОЛИ `input(action)` → ЯКЩО `has(holder, club)` and `occupied(neighbour, ball)` and `free(cell_behind_ball)` → ТО `slide(ball, dir)` — напрям «від власника ключки до мʼяча»; перешкода одразу за мʼячем → удару нема.
- КОЛИ `input(action)` → ЯКЩО `cell(ball, bunker)` → ТО `move(ball, dir)` — лише на 1 клітину.
- КОЛИ `blocked(ball)` → ЯКЩО `cell(ball_cell, hole)` → ТО `win`, `message(«NICE SHOT!»)`, `next_level`.
- КОЛИ `blocked(ball)` → ЯКЩО `cell(ball_cell, water)` → ТО `disappear(ball)`, `sound(ripples)` — лунку вже не пройти, лише undo або рестарт.
- Перешкоди для мʼяча: гольфіст, друзі, дерева, поза полем; вода, бункер і лунка — ні.
- КОЛИ `input(z)` → ТО `undo` (стандарт PuzzleScript, без ліміту).
- КОЛИ `input(r)` → ТО `restart`.
- Перемога: мʼяч зупинився на лунці. · Поразка: формально нема; мʼяч у воді чи лідер, замкнений власною чергою, — глухий кут для undo. · Рахунку нема: удари й кроки не рахуються.

## Керування і ввід
- Стрілки (WASD — стандарт PuzzleScript): крок лідера; натиск у бік сусіднього друга — передати йому ключку; у друга з ключкою стрілки лише передають її далі.
- X — удар тим, у кого ключка; напрям задає не клавіша, а те, з якого боку від мʼяча стоїть власник.
- Z — undo без ліміту, R — рестарт лунки.

## Вікна, меню, HUD
- `splash-screen` — титул PuzzleScript «Shall We Golf? by nebu soku».
- `tutorial-window` — текстові екрани між мапами: «Hole N of 15», «X to hit.», «Everybody can use the club.», «Press move key towards followers.», «The bunker could be useful.», фінал «Thanks for playing!».
- `game-screen` — уся лунка; HUD нема; червоний курсор-куточки над другом, у якого ключка (`selection-highlight`).
- `end-screen` — після влучання екран заливає синім і по літерах складається «NICE SHOT!».
- Переходи: титул → «Hole 1 of 15» → лунка → «NICE SHOT!» → наступне повідомлення → … → «Thanks for playing!».

## Фічі поза полем
- `undo` без ліміту, `restart-level`; `levels-sequential` 15 лунок; `continue` — стандарт PuzzleScript.
- Девлог 22.03.2021: додано точніше навчальне повідомлення й курсор над власником ключки.
- Лише HTML5: автор пояснив, що збірки для Windows рушій не дає.

## Варіації й родичі
- У сирці є, але лише в закоментованих мапах: **стрілки на траві** — мʼяч, що летить поперек стрілки, зсувається на 1 клітину в її бік і летить далі; проти стрілки — відкочується на 1 і зупиняється; уздовж — не помічає.
- Родичі: [ice-sliding-puzzles](ice-sliding-puzzles.md) і [ricochet-robots](ricochet-robots.md) (ковзання до упору, фігури як рухомі стінки); [herugolf](../pencil-logic/herugolf.md) (гольф-пазл Nikoli); [blockade](../maze-arcade/blockade.md) і [snake](../maze-arcade/snake.md) (слід як стіна); [kwirk](kwirk.md) (кілька персонажів).
- Осі варіацій:
  - **що зупиняє мʼяч**: стіни (ice-sliding) / фігури (Ricochet Robots) / власний слід і люди (тут);
  - **хто бʼє**: один аватар / будь-хто з ланцюжка, кому передали ключку (тут);
  - **поверхня**: трава — політ до упору; бункер — 1 клітина; вода — втрата, якщо там зупинився.

## Цікавинки для курсу
- Мʼяч летить до першої перешкоди, пролітаючи воду й лунку; перевірка, де він зупинився, — 🌱.
- Черга друзів як постійний слід від старту: кожна покинута клітина стає стіною — 🌱 (Snake, у якого хвіст не рухається).
- Передача ключки сусідові: хто зараз «гравець», визначає токен, а не аватар — 📎.
- Удар з бункера рівно на 1 клітину: клітина змінює дальність дії — 🌱.
- Ілюзія руху черги: три кольори футболок зсуваються по колу щокроку, хоча друзі стоять — 🌱 (рендер окремо від логіки).
- Розвʼязувач: стан = шлях лідера (весь слід), власник ключки, мʼяч; простір станів росте з довжиною сліду — 🥇.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ стрілки й X; `inertia-slide` ↔ політ мʼяча до упору; `impassable-cells` ↔ дерева, поза полем, вода для гольфіста; `floor-types` ↔ трава / бункер / вода; `all-on-targets` ↔ мʼяч на лунці; `undo-unlimited` + `restart-level` ↔ Z і R; `sequential-levels` ↔ 15 лунок; `level-from-txt` ↔ ASCII-мапи сирця; `tutorial-window` ↔ екрани-підказки; `movement-animation` ↔ анімація ходьби; `sound-effects` ↔ удар, сплеск, передача ключки.
- **Нема** → пропозиції карток:
  - `+trail-wall` (є в корпусі) — покинута клітина стає перешкодою.
  - `+follower-chain` (є в корпусі) — черга друзів за лідером.
  - `+stop-on-entity` (є в корпусі) — ковзання зупиняється об фігуру.
  - `+fall-into-water` (є в корпусі) — мʼяч, що зупинився на воді, утрачений.
  - `+tool-relay` «Інструмент дії передається сусідові по ланцюжку» · entities/interact · 📎 · слот {holders: adjacent}.
  - `+pass-over-target` «Ковзний обʼєкт минає ціль, якщо за нею нема упору» · entities/move · 🌱.
  - `+short-hit-terrain` «З клітини-пастки удар лише на 1 клітину» · entities/interact · 🌱.

## Пропозиції до словників
- `+card:tool-relay`, `+card:pass-over-target`, `+card:short-hit-terrain` — див. «Мапу на каталог».
- `+ui:holder-marker` — курсор над тим, хто зараз діє (тут — над власником ключки); ширше за `selection-highlight`, бо вибір робить не гравець.
- `+axis:actors` — `party`: керуєш одним лідером, але діяти може будь-хто з ланцюжка.

## Джерела
- ⭐ [itch.io: みんなでGOLF！(Shall We Golf?)](https://nebu-soku.itch.io/golfshall-we-golf) — гра в браузері, опис EN/JA, керування X і стрілки, коментарі автора (15 лунок, лише HTML5).
- [Сирець у редакторі PuzzleScript](https://www.puzzlescript.net/editor.html?hack=86a02fbb49c6c73b4bf899dab5bc63ca) і [gist API](https://api.github.com/gists/86a02fbb49c6c73b4bf899dab5bc63ca) — обʼєкти, правила (`OBforP`, `Obstacles`, удар `action Player`, бункер `OnBunker`, вода `Ripples`, слід `RSV`→`TM`, передача `club`), 15 мап, повідомлення.
- [Девлог «System update (3/22/21)»](https://nebu-soku.itch.io/golfshall-we-golf/devlog/234508/system-update32221) — курсор над власником ключки, нове навчальне повідомлення.
- YouTube: пошук «Shall We Golf puzzlescript nebu soku».

## Непевне
- (?) Чи можна під час польоту мʼяча (тіки 0,13 с) встигнути зробити крок і поставити друга на шляху — сирець цього не забороняє, у грі не перевірено.
- (?) Стрілки-«схили» є лише в закоментованих мапах; чи були вони в ранній версії гри — невідомо.
- (?) Керування WASD, Z і R — стандарт рушія; на сторінці гри названо лише X і стрілки.
