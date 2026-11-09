---
title: Pix the Cat
slug: pix-the-cat
aka: [PIX the CAT]
family: maze-arcade
also: [push-slide]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: setup
  goal: score
year: 2014
platforms: [PS4, PS Vita, Windows/Linux (Steam, 2015), Xbox One (2017), Switch (2019)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/330180/", best: true, note: "опис від розробника: яйця → каченята за Pix, кола-цілі, вкладені рівні Grid of Infinity, 4 режими, лідерборди, до 4 гравців"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pix_the_Cat", note: "Snake + Pac-Man, хвіст не врізати в перешкоду, платформи й дати виходу"}
  - {kind: official, url: "https://www.nintendo.com/us/store/products/pix-the-cat-switch/", note: "eShop: Arena — яйця як набої; Laboratory — рух до стіни, мінімум ходів; Nostalgia — квота й коза з квіткою; гонка з привидами"}
  - {kind: other, url: "https://www.thesixthaxis.com/?p=230520", note: "огляд: мікрорівні 10–20 с, ворота без паузи, Fever Time, вороги на фіксованих шляхах, пастка хвостом, Lab — спершу зібрати всі бульбашки"}
  - {kind: other, url: "https://middleofnowheregaming.com/2014/10/27/pix-the-cat-review", note: "огляд: Arcade до кінця часу, портали, привиди друзів; Lab 100 рівнів; Nostalgia 70 рівнів; місії відкривають режими"}
  - {kind: other, url: "https://www.pocketgamer.com/pix-the-cat/review/", note: "огляд: Fever вмикається на висоті комбо — ворогів можна їсти; камера відʼїжджає після смерті"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Pix+the+Cat+gameplay", note: "пошук; геймплей Arcade"}
stage: v1
coverage: 60
mechanics: [move-auto, body-queue, self-collision, no-moves-left, item-pickup, collect-quota, enemy-patrol, temporary-modes, combo-multiplier, teleport-pair, time-out, progress-acceleration, sequential-levels, inertia-slide, move-counter, level-bank, puzzle-select, mode-select, level-unlock, projectile-shot, score-records, leaderboard, achievements-window, game-screen, end-screen, background-music, +deliver-tail-to-goal, +nested-level-gate, +fever-mode, +score-driven-speed, +score-attack-timer, +collect-before-deliver, +ghost-run, +bonus-objectives, +player-elimination]
proposes: ["+effect:deliver", "+card:deliver-tail-to-goal", "+card:nested-level-gate", "+card:fever-mode", "+card:collect-before-deliver", "+card:ghost-run", "+window:missions-window"]
author: opus
date: 2026-11-09
---

# Pix the Cat — кіт без зупинки мчить сіткою, збирає яйця в хвіст-каченят і здає їх у кола, пірнаючи все глибше у вкладені рівні

## Суть
Pix рухається безперервно, гравець лише повертає його. Яйця на полі вилуплюються в каченят, що йдуть за котом хвостом, як тіло змійки; каченят треба здати в кола-цілі, після чого відкривається прохід у наступний рівень — він лежить «усередині» поточного (Grid of Infinity). Arcade — гонка на очки проти таймера: безпомилкова серія розганяє комбо до Fever, де кіт найшвидший і може їсти ворогів. Окремі режими перевертають ядро: Laboratory — ковзання до стіни на мінімум ходів, Nostalgia — квота без здачі, Arena — бій яйцями.

## Поле і час
- Квадратна сітка-лабіринт на один екран; рух жорстко по прямих, повороти — на клітинах.
- Рівні вкладені: ворота кожного мікрорівня ведуть у наступний, камера «занурюється» глибше без паузи; у дрібних лабіринтах Pix зменшується (PocketGamer). Після кінця забігу камера відʼїжджає й показує всю пройдену глибину.
- Arcade: мікрорівень ≈10–20 с, забіг обмежено загальним таймером; плани рівнів трохи змінюються між забігами, тож їх не завчиш.
- Laboratory — без часу (`time` фактично покроковий); Nostalgia — свій таймер «коза їсть квітку».

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Pix | player | швидкість росте з комбо | рух без зупинки, гравець задає напрямок |
| Яйце | pickup | — | взяте — вилуплюється в каченя в кінці хвоста |
| Каченя | object | позиція в хвості | повторює шлях Pix; крізь нього не пройти |
| Коло-ціль | zone | — | сюди здають каченят |
| Ворота (прохід) | gate | відкриті після здачі всіх | ведуть у наступний вкладений рівень |
| Стіна | static | — | непрохідна |
| Ворог | enemy | фіксований маршрут | зіткнення забирає хвіст і комбо; у Fever — їстівний |
| Портал | terrain | пара | переносить на парний портал (?) |
| Бульбашка (Laboratory) | object | — | збирається в хвіст, здається в ціль |
| Блоб (Laboratory) | player | — | ковзає до упору, напрямок міняється лише на зупинці |
| Коза й квітка (Nostalgia) | — | таймер | поки коза не зʼїла квітку — бонус |
| Яйце-набій (Arena) | projectile | запас = зібрані яйця | вибиває суперника |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `move(pix, facing)` — Pix не зупиняється.
- КОЛИ `input(dir)` → ТО `face(pix, dir)`.
- КОЛИ `contact(pix, egg)` → ТО `disappear(egg)`, `grow(tail, 1)`, `custom: «яйце вилуплюється в каченя в кінці хвоста»`.
- КОЛИ `tick` → ТО `custom: «каченята повторюють шлях Pix клітина за клітиною»`.
- КОЛИ `enter(pix, goal_circle)` → ЯКЩО `count(tail, >, 0)` → ТО `custom: «каченята з хвоста лишаються в колі»` (`+effect:deliver`), `score(+)`, `combo(+1)`.
- КОЛИ `all_on(duckling, goal_circle)` → ТО `unlock(gate)`.
- КОЛИ `enter(pix, gate)` → ТО `next_level`, `camera(zoom_in)` — наступний рівень усередині поточного.
- КОЛИ `contact(pix, tail)` → ТО `block` — крізь каченят не пройти.
- КОЛИ `no_moves(pix)` → ТО `game_over` — хвіст замкнув кота.
- КОЛИ `contact(pix, enemy)` → ЯКЩО `not state(pix, fever)` → ТО `custom: «каченята хвоста втрачено»`, `reset_combo`, `multiplier(-1)`.
- КОЛИ `contact(pix, enemy)` → ЯКЩО `state(pix, fever)` → ТО `disappear(enemy)`, `score(+)`.
- КОЛИ `counter(combo, >=, n)` → ТО `set_state(pix, fever)`, `speed(pix, max)`, `flash`.
- КОЛИ `counter(combo, >=, k)` → ТО `speed(pix, +1)` — що довша серія, то швидший кіт.
- КОЛИ `custom: «помилка: втрачено хвіст»` → ТО `clear_state(pix, fever)`; після багатьох помилок повернути Fever майже неможливо.
- КОЛИ `tick` → ТО `custom: «ворог іде своїм фіксованим маршрутом»`.
- КОЛИ `enter(pix, portal)` → ТО `teleport(pix, paired_portal)` (?).
- КОЛИ `counter(time_left, ==, 0)` → ТО `game_over`, `camera(zoom_out)`, `window(end-screen)`.
- Laboratory: КОЛИ `input(dir)` → ЯКЩО `state(blob, stopped)` → ТО `slide(blob, dir)`, `counter(moves, +1)`.
- Laboratory: КОЛИ `contact(blob, bubble)` → ТО `attach(bubble, tail)`.
- Laboratory: КОЛИ `enter(blob, goal)` → ЯКЩО `count(bubble_on_field, >, 0)` → ТО `lose` — здавати лише всі разом.
- Laboratory: КОЛИ `all_on(bubble, goal)` → ТО `win`; ЯКЩО `counter(moves, <=, par)` → ТО `custom: «бонусний штамп»`.
- Nostalgia: КОЛИ `counter(ducklings, >=, quota)` → ТО `win` (здавати не треба); ЯКЩО `custom: «коза ще не зʼїла квітку»` → ТО `score(bonus)`.
- Nostalgia: КОЛИ `no_moves(pix)` → ТО `lose`.
- Arena: КОЛИ `contact(pix, egg)` → ТО `pickup(pix, egg)`.
- Arena: КОЛИ `input(fire)` → ЯКЩО `has(pix, egg)` → ТО `spawn(egg_shot)`, `take(pix, egg)`.
- Arena: КОЛИ `contact(egg_shot, rival)` → ТО `custom: «суперника вибито з раунду»`; ривок (`input(dash)`) у суперника — так само.
- Arena: КОЛИ `count(players_alive, ==, 1)` → ТО `win` для останнього.
- Перемога: Arcade — рекорд очок; Laboratory — рівень за мінімум ходів; Nostalgia — квота; Arena — останній уцілілий. Поразка: таймер (Arcade) або пастка хвостом.

## Керування і ввід
- Лише чотири напрямки (d-pad чи стік): напрямок застосовується на клітинах, зупинитися не можна (Arcade/Nostalgia).
- Laboratory: напрямок — лише коли блоб стоїть біля стіни; кожен запуск — один хід.
- Arena: напрямок + постріл яйцем + ривок; 2–4 гравці на одній консолі.

## Вікна, меню, HUD
- `main-menu` → `mode-select`: Arcade · Laboratory · Nostalgia · Arena (Arena й частина режимів відкриваються місіями).
- `puzzle-select`: 100 рівнів Laboratory з найкращим результатом; 70 рівнів Nostalgia.
- `game-screen` (Arcade): поле, `score`, `timer-countdown`, `combo-meter` / `multiplier`, Fever — спалахи екрана й ритмічна музика; привид друга чи лідера поверх поля (?).
- `end-screen`: камера відʼїжджає й показує всі пройдені вкладені рівні + рахунок.
- `leaderboard`: друзі й світ (Arcade); вибір привида для гонки — свого, друга, лідера таблиці, розробників.
- `custom-window` місій (`+window:missions-window`): цілі в кожному режимі й прогрес; `achievements-window` (Steam).
- `settings-window` (?).
- Переходи: menu → mode-select → game-screen → end-screen → leaderboard / знову.

## Фічі поза полем
- `mode-classic` (Arcade на очки) + `mode-puzzle` (Laboratory) + Nostalgia + `mode-versus` (Arena, `local-multiplayer` до 4).
- `ghost-run`: гонка з привидом свого, друга, лідера чи розробників.
- `leaderboard-online`, `achievements`, `cloud-save` (Steam), `level-unlock` через місії (`+bonus-objectives`).
- `par-target` у Laboratory: штамп за мінімум ходів.

## Варіації й родичі
- `snake` (хвіст як тіло, пастка собою), `pac-man` (лабіринт, тимчасова сила проти ворогів), `pac-man-championship-edition` (найближчий родич: забіг на очки проти таймера, швидкість від рахунку, ланцюг за гравцем).
- `nibbler` — змійка в лабіринті на швидкість; push-slide/Inertia — ядро Laboratory (ковзання до упору).
- Arena — родич `bomberman-battle-mode` (бій кількох на одній арені).
- **Осі варіацій:** хвіст — вантаж для здачі / квота без здачі / тіло-перешкода · рух — безперервний / ковзання до стіни · перехід рівнів — ворота у вкладений рівень / окремий екран · кара за помилку — втрата хвоста й комбо / кінець забігу.

## Цікавинки для курсу
- Хвіст-черга з каченят, що здаються в кола: змійка, яка не лише росте, а й розвантажується — 📎.
- Вкладені рівні з «зануренням» камери: наступний рівень намальований усередині клітини-воріт поточного — 🥈 (рекурсивний рендер і плавний зум).
- Fever за серію без помилок: тимчасовий режим, який вмикає не предмет, а комбо — 📎.
- Laboratory: ковзання до стіни + підрахунок ходів + умова «збери все перед здачею» — 🥉 з BFS-розвʼязувачем на мінімум ходів 🥇.
- Привид найкращого забігу (запис вводу по тіках і відтворення поверх гри) — 🥉.
- Arena: яйця як набої з того самого підбирання — 📎.

## Мапа на каталог
- Є: `move-auto` · `body-queue` · `self-collision` + `no-moves-left` (пастка хвостом) · `item-pickup` · `collect-quota` (Nostalgia) · `enemy-patrol` · `temporary-modes` (Fever) · `combo-multiplier` · `teleport-pair` (портали) · `time-out` · `progress-acceleration` · `sequential-levels` · `inertia-slide` + `move-counter` (Laboratory) · `level-bank` + `puzzle-select` · `mode-select` · `level-unlock` · `projectile-shot` (Arena) · `score-records` + `leaderboard` · `achievements-window` · `game-screen` · `end-screen` · `background-music`.
- **Нема** → пропозиції карток:
  - `+deliver-tail-to-goal` «Здати хвіст-вантаж у клітини-цілі» · entities/interact · 📎 · слот {all_at_once: false}.
  - `+nested-level-gate` «Ворота у вкладений наступний рівень» · levels/progression · 🥈 · слот {zoom: true}.
  - `+fever-mode` «Fever за серію без помилок» · game-logic/score · 📎 · слот {threshold}.
  - `+score-driven-speed`, `+score-attack-timer` (є в Pac-Man CE) — тут швидкість від комбо.
  - `+collect-before-deliver` «Здача лише після збору всього» · game-logic/lose · 🌱.
  - `+ghost-run` «Привид найкращого забігу» · interface/results · 🥉.
  - `+bonus-objectives` (є пропозиція) — місії режимів.
  - `+player-elimination` (є пропозиція) — Arena до останнього.

## Пропозиції до словників
- `+effect:deliver` — залишити вантаж/хвіст у клітині-цілі (каченята в коло, бульбашки в ціль); `custom` у реченні здачі.
- `+card:deliver-tail-to-goal`, `+card:nested-level-gate`, `+card:fever-mode`, `+card:collect-before-deliver`, `+card:ghost-run` — див. «Мапу на каталог».
- `+window:missions-window` — список місій режиму з прогресом і нагородами (відкриття режимів і рівнів).

## Джерела
- ⭐ [Steam: Pix the Cat](https://store.steampowered.com/app/330180/) — опис від Pastagames: яйця, каченята, кола, Grid of Infinity, режими, лідерборди, локальний бій до 4.
- [Wikipedia: Pix the Cat](https://en.wikipedia.org/wiki/Pix_the_Cat) — «Snake + Pac-Man», платформи, дати виходу.
- [Nintendo eShop](https://www.nintendo.com/us/store/products/pix-the-cat-switch/) — описи чотирьох режимів, привиди, Arena з яйцями-набоями.
- [TheSixthAxis: огляд](https://www.thesixthaxis.com/?p=230520) — мікрорівні, Fever Time, вороги на маршрутах, Laboratory, Arena.
- [Middle of Nowhere Gaming: огляд](https://middleofnowheregaming.com/2014/10/27/pix-the-cat-review) — таймер Arcade, портали, привиди, 100 рівнів Lab, 70 рівнів Nostalgia, місії.
- [Pocket Gamer: огляд](https://www.pocketgamer.com/pix-the-cat/review/) — Fever з висоти комбо, поїдання ворогів, зум після смерті.
- YouTube: пошук «Pix the Cat gameplay».

## Непевне
- (?) Скільки каченят приймає одне коло й чи здаються вони по одному з хвоста чи всі разом.
- (?) Що буває, коли Pix біжить у стіну в Arcade: зупинка, розворот чи помилка з втратою комбо.
- (?) Тривалість таймера Arcade, поріг комбо для Fever, значення очок і множників.
- (?) Портали — лише зі скриншотів одного огляду.
- (?) Steam пише «70 рівнів» — імовірно про Nostalgia; Laboratory за оглядом має 100.
- (?) Arena: Steam згадує «до чотирьох PixBots» — чи це боти-суперники, чи назва персонажів; один огляд каже, що Arena була лише на PS4 на старті.
