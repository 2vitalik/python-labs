---
title: SlideMaze
slug: slidemaze
aka: [MazeSlide]
family: roguelike
also: [board-digital, push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: setup
  goal: state
year: 2024
platforms: [web (HTML5), PC (Windows)]
links:
  - {kind: itch, url: "https://squaredev.itch.io/slidemaze", best: true, note: "грати в браузері; опис: зсув рядів і стовпців як у Labyrinth, ключ → двері, вороги, пастки, зілля, щити, монети, апгрейди між поверхами"}
  - {kind: other, url: "https://itch.io/jam/agdg-demo-day-54/rate/2428231", note: "AGDG Demo Day 54 (січень 2024): коментарі — обмежені зсуви з перезарядкою, не всі ряди рухомі, зброя перезаписує зброю, лук"}
  - {kind: other, url: "https://itch.io/games/tag-broughlike", note: "тег broughlike на itch.io — SlideMaze серед інших"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=SlideMaze+SquareDev+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 35
mechanics: [move-4dir, keyboard-controls, row-conveyor, key-and-door, reach-exit, hp-damage, item-pickup, round-currency, in-round-upgrades, shop-between-levels, sequential-levels, random-walk, impassable-cells, pipe-connectors, destructible-blocks, player-death, pause-menu, restart-level, +row-col-insert, +slide-charges, +single-weapon-slot]
proposes: ["+effect:shift_row(row, dir)", "+cond:slidable(row)", "+cond:passage(a, b)", "+ui:slide-arrows", "+ui:slide-charges", "+feature:reload-level", "+card:row-col-insert"]
author: opus
date: 2026-11-09
---

# SlideMaze — broughlike на полі «Лабіринту»: зсуваєш цілі ряди плиток, щоб прокласти шлях до ключа й дверей

## Суть
Джем-гра (7 днів) за мотивами настолки Labyrinth: поле складене з плиток-коридорів, і гравець, крім кроків героя, **зсуває цілі ряди й стовпці**, щоб зʼєднати коридори. На поверсі треба взяти ключ і дійти до дверей; заважають вороги й пастки, допомагають зілля, щити й монети, а між поверхами — апгрейди зброї та статів. Зсуви обмежені: кількість використань відновлюється з часом, і рухаються не всі ряди. Мала, «недороблена» гра, але єдина в корпусі, де ядро broughlike — **перебудова лабіринту зсувом рядів**.

## Поле і час
- Квадратна сітка плиток-коридорів (як у Labyrinth: прямі, кути й інші з'єднувачі зі стінками); поле менше, ніж у настолці (коментар джему).
- Частина рядів/стовпців рухома (стрілки на екрані біля країв), решта — ні.
- Покроково (?): хід = крок героя або зсув; вороги ходять.
- Край поля — стіна: вийти через край на інший бік не можна.
- Поверхи йдуть послідовно; процедурність рівнів — (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | HP (серця), зброя, стати | крок 4 напрямки лише коридором плитки |
| Плитка-коридор | tile | форма проходів, рухома/нерухома | зсувається разом зі своїм рядом / стовпцем |
| Рухомий ряд / стовпець | zone | — | стрілка-кнопка на краю зсуває весь ряд |
| Ключ | pickup | — | потрібен для дверей |
| Двері | gate | замкнені / відчинені | з ключем — вихід на наступний поверх |
| Ворог | enemy | HP (?) | рухається, але не переслідує; вбивство нагороди не дає (за коментарем) |
| Пастка | hazard | — | шкодить (?) |
| Зілля | pickup | — | лікування |
| Щит | pickup | — | захист від удару (?) |
| Монета | pickup | — | валюта для апгрейдів (?) |
| Зброя (напр., лук) | pickup | одна в слоті | нова замінює попередню |
| Апгрейд стату | pickup | — | між поверхами |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `custom: «між плитками є прохід у цьому напрямку»` → ТО `move(hero, dir)`; інакше `block`.
- КОЛИ `input(slide_arrow)` → ЯКЩО `custom: «ряд позначено рухомим»` і `counter(slides, >, 0)` → ТО `shift(row, dir)`, `counter(slides, −1)`.
- КОЛИ `custom: «ряд зсунуто»` → ТО `custom: «плитка, що вийшла за край, повертається з протилежного боку»` (?); сутності на плитках їдуть разом (?).
- КОЛИ `turn_end(hero)` → ЯКЩО `counter(slides, <, max)` → ТО `custom: «заряд зсуву відновлюється з часом»` (стук у стіну теж «чекає»).
- КОЛИ `contact(hero, key)` → ТО `pickup`.
- КОЛИ `contact(hero, door)` → ЯКЩО `has(hero, key)` → ТО `next_level`; інакше `block`.
- КОЛИ `contact(hero, enemy)` → ТО `custom: «бій: обмін ударами»` (?), `damage(…)`.
- КОЛИ `contact(hero, trap)` → ТО `damage(hero, n)` (?).
- КОЛИ `contact(hero, potion)` → ТО `pickup`, `heal(hero, n)` · КОЛИ `contact(hero, shield)` → ТО `set_state(hero, shield)` (?).
- КОЛИ `contact(hero, coin)` → ТО `currency(+1)`.
- КОЛИ `level_end` → ТО `choose(weapon|stat)`; ЯКЩО `custom: «обрано зброю»` → `custom: «нова зброя замінює стару»`.
- КОЛИ `custom: «використано руйнування стіни»` → ТО `set_cell(wall, floor)` (?).
- КОЛИ `hp_zero(hero)` → ТО `lose` (у джем-версії баг: гра триває).
- КОЛИ `input(pause → reload)` → ТО `restart` (рецепт розробника від софтлоку).
- Перемога: пройти поверхи (кількість — (?)). Поразка: HP = 0. Рахунку не згадано.

## Керування і ввід
- WASD — крок героя.
- Екранні кнопки-стрілки біля рухомих рядів/стовпців — зсув у напрямку стрілки (мишею).
- Пауза-меню — перезавантажити рівень.

## Вікна, меню, HUD
- `game-screen`: поле плиток, стрілки зсуву, HUD — серця (`hp-bar`), монети (`coins`), заряди зсувів (?), поточна зброя.
- `upgrade-window` — між поверхами: зброя або стати.
- `pause-menu` — перезавантаження рівня.
- `main-menu` (?).

## Фічі поза полем
- `restart-level` через паузу (від софтлоків).
- Прогресія: поверхи послідовно, апгрейди між ними (`meta`-прогресії нема).
- Нема undo, збережень, рекордів (за сторінкою).

## Варіації й родичі
- Настолка Labyrinth (Ravensburger, 1986) — вставляєш запасну плитку, зсуваючи ряд; у SlideMaze плитку не повертаєш перед вставкою (коментар).
- Родичі: broughlike-школа — [868-HACK](868-hack.md), [Mosaic](mosaic-broughlike.md), [Magpie](magpie-broughlike.md); зсув рядів — Loopover / «Sixteen» (`push-slide`).
- Осі варіацій: **зсув** (будь-який ряд / лише позначені) · **ліміт** (без ліміту / заряди з перезарядкою / коштує хід) · **вихідна плитка** (повертається з іншого боку / стає запасною для вставки, як у Labyrinth) · **поворот плитки** (нема / перед вставкою).

## Цікавинки для курсу
- Зсув ряду/стовпця плиток з переносом за край — 🌱.
- Перевірка проходу між двома плитками за портами (дві сторони мають збігатися) — 🌱 (картка `pipe-connectors`).
- Заряди зсуву, що відновлюються з ходами — 🌱.
- BFS досяжності ключа й дверей з урахуванням можливих зсувів (детектор софтлоку) — 🥇.
- Слот зброї з заміною + вибір апгрейда між поверхами — 🌱.

## Мапа на каталог
- Є: `move-4dir`, `keyboard-controls`; `row-conveyor` ↔ зсув ряду; `pipe-connectors` ↔ плитки-коридори; `key-and-door` + `reach-exit` ↔ ключ і двері; `hp-damage`, `item-pickup` ↔ зілля, щити; `round-currency` ↔ монети; `in-round-upgrades` + `shop-between-levels` ↔ апгрейди між поверхами; `random-walk` ↔ вороги без погоні; `impassable-cells`; `destructible-blocks` ↔ руйнування стін; `player-death`; `pause-menu` + `restart-level`.
- **Нема** → пропозиції карток:
  - `+row-col-insert` «Зсув ряду/стовпця плиток-коридорів з виходом за край (Labyrinth)» · entities/move · 🌱 · слоти {wrap, spare_tile, rotate_before}.
  - `+slide-charges` «Обмежені зсуви з перезарядкою за ходи» · entities/state · 🌱.
  - `+single-weapon-slot` «Нова зброя замінює стару» · entities/state · 🌱.

## Пропозиції до словників
- `+effect:shift_row(row, dir)` — уточнення `shift` для одного ряду плиток разом із сутностями на них.
- `+cond:slidable(row)` — ряд/стовпець рухомий; `+cond:passage(a, b)` — між сусідніми плитками є прохід.
- `+ui:slide-arrows` — кнопки-стрілки на краях поля; `+ui:slide-charges` — лічильник зсувів.
- `+feature:reload-level` — перезавантаження рівня з паузи як аварійний вихід із софтлоку.
- `+card:row-col-insert`.

## Джерела
- ⭐ [itch: SlideMaze](https://squaredev.itch.io/slidemaze) — опис розробника (Labyrinth, ключ і двері, вороги, пастки, зілля, щити, монети, апгрейди), керування, теги broughlike / roguelike / board game.
- [AGDG Demo Day 54: SlideMaze](https://itch.io/jam/agdg-demo-day-54/rate/2428231) — «Labyrinth-inspired broughlike»; коментарі гравців про ліміт зсувів, нерухомі ряди, ворогів без погоні, лук, заміну зброї, відсутність переходу через край.
- [itch: тег broughlike](https://itch.io/games/tag-broughlike).
- YouTube: пошук «SlideMaze SquareDev gameplay».

## Непевне
- (?) Чи плитка, що виходить за край, повертається з іншого боку, чи стає «запасною», як у Labyrinth; чи сутності їдуть із плиткою.
- (?) Скільки зсувів і як швидко вони відновлюються; чи зсув коштує хід ворогам.
- (?) Бій: як саме шкодять вороги й пастки, що робить щит, на що йдуть монети (апгрейди / магазин).
- (?) Процедурні поверхи чи ручні (`random: setup` — припущення), кількість поверхів, чи є фінальна перемога.
- (?) Рік — 2024 за датами джему (5–8.01.2024); сторінка гри дати не показує.
