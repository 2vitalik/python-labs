---
title: Maze Mice
slug: maze-mice
family: maze-arcade
also: [roguelike]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: both
  goal: survive
year: 2025
platforms: [PC (Steam)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3385370/Maze_Mice/", best: true, note: "офіційна сторінка: «time only moves when you move», трейлер, демо"}
  - {kind: other, url: "https://www.siliconera.com/preview-maze-mice-combines-vampire-survivors-and-pac-man/", note: "превʼю: кольорові точки, великі точки, сплячі коти й коти-привиди, зброя"}
  - {kind: other, url: "https://indiecator.org/2025/05/03/maze-mice-heads-into-early-access-and-is-already-way-too-much-fun-review/", note: "огляд: 4 активні + 4 пасивні слоти, 25 шкоди за удар, коти-привиди крізь стіни"}
  - {kind: other, url: "https://rogueliker.com/maze-mice-review/", note: "огляд: заморозка котів, flea bombs, flame trail"}
  - {kind: other, url: "https://www.tech-gaming.com/maze-mice/", note: "огляд: коти прокидаються, «conga line», пасивки"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=maze+mice+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-4dir, chase-player, hp-damage, item-pickup, spawn-random-cell, in-round-upgrades, inventory-limit, temporary-modes, progress-acceleration, event-points, avatar-picker, save-progress, game-screen, end-screen, +move-driven-time, +xp-level-up, +upgrade-draft, +upgrade-stacking, +auto-weapons, +wake-on-event, +ghost-through-walls, +damage-trail, +chain-damage, +big-pickup-respawn, +run-meta-carry, +character-start-kit, +wrap-edges]
proposes: ["+axis:time=move-driven", "+axis:session=run", "+trigger:input(move)", "+trigger:proximity_wake", "+cond:state", "+effect:choose", "+effect:leave_trail", "+effect:chain", "+role:hazard", "+ui:xp-bar", "+ui:hp-bar", "+ui:ability-slots", "+window:upgrade-window", "+window:character-select", "+feature:meta-progression", "+card:move-driven-time", "+card:upgrade-draft"]
author: opus
date: 2026-11-02
---

# Maze Mice — Pac-Man × Vampire Survivors, де час іде лише тоді, коли рухаєшся ти

## Суть
Мишка бігає лабіринтом, збирає точки-досвід, на кожному рівні вибирає нову здібність або прокачує наявну, а здібності самі б'ють котів, що женуться за нею. Головний твіст: **час іде, лише коли гравець рухається** — зупинився, і коти завмирають разом із рештою гри (порівнюють із SUPERHOT). Це перетворює bullet heaven на напівпокрокову тактику: можна зупинитись і спланувати, куди прорватись. Мета — вижити якомога довше (рани 10–30 хв).

## Поле і час
- Невеликий одноекранний лабіринт зі стінами в стилі Pac-Man (першу локацію називають горищем); один огляд згадує перехід через край екрана (?).
- Тік гри привʼязаний до руху гравця: нема вводу руху → нема часу. Усередині руху — real-time.
- Кількість котів росте з часом, екран швидко заповнюється; пізніше зʼявляється більший і швидший кіт.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Мишка | player | HP (удар = 25), персонаж зі стартовою здібністю | рух 4 напрямки (?), час іде лише під час руху |
| Стіна лабіринту | static | — | непрохідна для мишки і звичайних котів |
| Точка досвіду | pickup | колір (синя → зелена/червона/жовта) | дає XP |
| Велика точка | pickup | — | дає XP, висипає рядки малих точок і нову велику деінде |
| Сплячий кіт | enemy | колір = сила | спить; прокидається, коли мишка пробігає повз |
| Кіт | enemy | — | женеться по лабіринту в 4 напрямках, іноді зрізає шлях |
| Кіт-привид | enemy | — | летить до мишки крізь стіни |
| Великий кіт | enemy | більший, швидший | зʼявляється згодом (?) |
| Активна здібність | object | рівень, cooldown | б'є котів сама: слід вогню, промінь (Prism), блохи-бомби, спиці, клубки, пил, світло |
| Пасивна здібність | object | рівень | +XP, радіус підбору, −cooldown, +макс. HP, реген, ухилення (Popcorn), воскресіння |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО `move(mouse, dir)` і `custom: «тік світу — коти, снаряди, cooldown-и рухаються»`.
- КОЛИ `custom: «нема вводу руху»` → ТО `freeze(all, ∞)` — гра стоїть, доки мишка стоїть.
- КОЛИ `contact(mouse, dot)` → ТО `pickup`, `counter(xp, +n)`.
- КОЛИ `contact(mouse, big_dot)` → ТО `pickup`, `spawn_at(dot_rows, here)`, `spawn_at(big_dot, rng_cell)`.
- КОЛИ `counter(xp, >=, next_level)` → ТО `choose(3 options: нова здібність | рівень наявної)` (?кількість варіантів).
- КОЛИ `custom: «мишка пробігає поруч зі сплячим котом»` → ТО `set_state(cat, awake)` → `chase-player`.
- КОЛИ `timer(cooldown)` (у часі руху) → ТО `custom: «активна здібність б'є»`: слід вогню палить котів позаду, блохи перескакують між цілями.
- КОЛИ `contact(mouse, cat)` → ЯКЩО `state(mouse, dodge_ready)` → ТО `custom: «ухилення»`; інакше `hp(mouse, −25)`.
- КОЛИ `hp_zero(mouse)` → ЯКЩО `has(mouse, revive)` → ТО `heal`; інакше `lose`, `end-screen`.
- Слоти: максимум 4 активні + 4 пасивні; повторний вибір здібності = її рівень +1.
- Перемога: вижити (один огляд — «дожити до боса і перемогти» ?). Поразка: HP = 0. Мета-прогрес: досвід за ран відкриває персонажів, здібності, ворогів, локації.

## Керування і ввід
- Напрямки руху — і все; зброя стріляє сама (bullet heaven).
- Стояти на місці = пауза-планування без штрафу; ця «пауза» — частина правил, не меню.
- Вибір апгрейда — меню між кадрами при підвищенні рівня.

## Вікна, меню, HUD
- `main-menu` → `character-select` (мишки з різними стартовими здібностями) → `game-screen`.
- `game-screen` — лабіринт; HUD: HP (`hp-bar`), XP-смуга (`custom: «xp-bar»`), слоти 4+4 здібностей (`custom: «ability-slots»`), таймер рану (?).
- `upgrade-window` — вибір нової здібності / рівня наявної при level-up.
- `end-screen` — результат рану, нарахування досвіду на відкриття.
- Переходи: main-menu → character-select → game-screen ⇄ upgrade-window → (HP = 0) end-screen → main-menu.

## Фічі поза полем
- `meta-progression`: відкриття за сумарним досвідом ранів (не за досягненнями) — мишки, здібності, вороги, локації; ~30 персонажів (дані огляду раннього доступу).
- `achievements` (Steam), `cloud-save`, 18 мов (`localization`).
- У ранньому доступі не було reroll/skip/banish для вибору апгрейдів (у релізі — ?).

## Варіації й родичі
- Родичі: Pac-Man (лабіринт, коти-«привиди»), Vampire Survivors (автозброя, level-up вибір), SUPERHOT (час з рухом), Space Mouse 2 (миша в лабіринті), Luck be a Landlord (той самий автор).
- Осі: **що рухає час** — таймер (аркади) / хід (роглайки) / рух гравця (тут, SUPERHOT); **як ворог проходить лабіринт** — по коридорах / крізь стіни (привиди); **звідки сила** — енерджайзер на полі / вибір апгрейда за досвід.

## Цікавинки для курсу
- Час, що йде лише під час руху гравця: усі сутності тікають від одного «годинника руху» — 🥉 (game-loop із умовним тіком).
- Level-up з вибором з 3 варіантів і стекуванням рівнів здібності, ліміт слотів 4+4 — 🥉.
- Сплячі вороги, що прокидаються від близькості — 📎.
- Ворог-привид крізь стіни поряд зі звичайним по коридорах — 📎 (два режими руху одного класу).
- Слід вогню, що б'є тих, хто йде слідом — 📎.
- Велика точка, що при взятті перекидає себе в нове місце і сипле дрібні — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `chase-player` · `hp-damage` (25 за удар) · `item-pickup` · `spawn-random-cell` (нова велика точка) · `in-round-upgrades` · `inventory-limit` (4+4 слоти) · `temporary-modes` (ухилення) · `progress-acceleration` · `event-points` · `avatar-picker` · `save-progress` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+move-driven-time` «Час іде лише під час руху гравця» · code/architecture · 🥉.
  - `+xp-level-up` (вже Dragonsweeper) — XP → рівень.
  - `+upgrade-draft` «Вибір 1 з N апгрейдів при level-up» · game-logic/economy · 🥉 · слот {options: 3}.
  - `+upgrade-stacking` «Повторний вибір = рівень +1» · game-logic/economy · 📎.
  - `+auto-weapons` «Зброя діє сама за cooldown» · entities/combat · 🥉.
  - `+wake-on-event` (вже Adventures of Lolo) — сплячий кіт прокидається.
  - `+ghost-through-walls` «Ворог ігнорує стіни» · entities/move · 🌱.
  - `+damage-trail` «Слід, що шкодить ворогам» · entities/combat · 📎.
  - `+chain-damage` «Шкода перескакує між цілями» · entities/combat · 📎.
  - `+big-pickup-respawn` «Великий предмет переноситься й сипле дрібні» · entities/spawn · 🌱.
  - `+run-meta-carry` (вже Into the Breach) — досвід ранів відкриває контент.
  - `+character-start-kit` «Персонаж = стартова здібність» · interface/settings · 🌱.
  - `+wrap-edges` (вже Pac-Man) — якщо підтвердиться.

## Пропозиції до словників
- `+axis:time=move-driven` — тік світу = рух гравця (SUPERHOT, Maze Mice); не `turn` і не чистий `realtime`.
- `+axis:session=run` — ран роглайту з мета-прогресом.
- `+trigger:input(move)` — саме рух, а не будь-яка дія, рухає час.
- `+trigger:proximity_wake` — сутність прокидається, коли гравець поруч (споріднено `in_range`).
- `+effect:choose` (вже Backpack Hero) — вибір апгрейда; `+effect:leave_trail` (вже Xonix) — слід вогню; `+effect:chain` — перескок шкоди.
- `+role:hazard` — слід вогню.
- `+ui:xp-bar`, `+ui:hp-bar`, `+ui:ability-slots` — смуги й слоти здібностей.
- `+window:upgrade-window`, `+window:character-select` (🔥) — вибір апгрейда / мишки.
- `+feature:meta-progression` (🔥).
- `+card:move-driven-time`, `+card:upgrade-draft` — див. вище.

## Джерела
- ⭐ [Steam: Maze Mice](https://store.steampowered.com/app/3385370/Maze_Mice/) — опис «bullet heaven roguelite where time only moves when you move», TrampolineTales, трейлер, теги, демо.
- [Siliconera: превʼю](https://www.siliconera.com/preview-maze-mice-combines-vampire-survivors-and-pac-man/) — кольорові й великі точки, сплячі коти за кольорами, коти-привиди, Flame Trail і Prism, розблокування за досвідом.
- [Indiecator: огляд раннього доступу](https://indiecator.org/2025/05/03/maze-mice-heads-into-early-access-and-is-already-way-too-much-fun-review/) — 4+4 слоти, 25 шкоди за удар, Popcorn-ухилення, привиди крізь стіни, 30 персонажів.
- [Rogueliker: огляд](https://rogueliker.com/maze-mice-review/) — повна заморозка котів, flea bombs, слід вогню, коти по 4 напрямках.
- [Tech-Gaming: огляд](https://www.tech-gaming.com/maze-mice/) — коти прокидаються, «conga line», пасивки (реген, +XP).
- YouTube: пошук «maze mice gameplay».

## Непевне
- (?) Чи рух мишки клітинний (4 напрямки по коридорах) чи вільний — огляди кажуть лише про котів «у 4 напрямках».
- (?) Перехід через край екрана — згадано лише в одному огляді.
- (?) Бос і умова перемоги: Rogueliker — «дожити й перемогти боса»; інші — «вижити якнайдовше».
- (?) Кількість варіантів при level-up; чи з'явились reroll/skip/banish у релізі.
- (?) Чи заморожуються снаряди й cooldown-и, коли мишка стоїть (огляди кажуть «уся дія»).
- (?) Мобільна версія: у пошуку трапилась сторінка App Store, але не перевірена.
