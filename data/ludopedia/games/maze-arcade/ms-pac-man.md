---
title: Ms. Pac-Man
slug: ms-pac-man
aka: [Crazy Otto, Міс Пекмен]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: collect
year: 1982
platforms: [arcade, Atari 2600, Atari 7800, NES, Genesis, Game Boy, PC, mobile]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Ms._Pac-Man", best: true, note: "4 лабіринти за рівнями, 2 пари тунелів, мандрівний фрукт, напіввипадкові Blinky й Pinky, Sue, Crazy Otto від GCC"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pac-Man", note: "база: цілі привидів, розклад scatter/chase"}
  - {kind: other, url: "https://pacman.holenet.info/", note: "Pac-Man Dossier — механіка оригіналу, від якої відраховуються відмінності"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=ms+pac-man+arcade+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-4dir, move-auto, collect-all, touch-death, temporary-modes, chase-greedy, random-walk, scatter-chase-schedule, wrap-edges, speed-per-type, event-points, progress-acceleration, sequential-levels, ghost-house-release, escalating-kill-points, +maze-rotation-by-level, +roaming-bonus-item, +random-bonus-sequence, +random-start-phase, +multi-tunnel-pairs]
proposes: ["+feature:maze-rotation", "+card:roaming-bonus-item", "+card:random-start-phase", "+effect:path_to(a, cell)"]
author: opus
date: 2026-11-09
---

# Ms. Pac-Man — той самий Пекмен, але лабіринт міняється, фрукт мандрує, а привиди на старті не за схемою

## Суть
Ядро — як у [pac-man](pac-man.md): зʼїсти всі точки, тікати від чотирьох привидів, енерджайзер перевертає ролі. Ms. Pac-Man (Midway/GCC, 1982) ламає головну стратегію оригіналу — **завчені маршрути-«патерни»**: привиди на початку рівня рухаються випадково, лабіринтів чотири, а бонус-фрукт не стоїть у центрі, а заїжджає через тунель і блукає. Тут описано лише відмінності; цілі привидів, будиночок, frightened, таблиці — у `pac-man.md`.

## Поле і час
- Чотири лабіринти, кожен своїм кольором, змінюються після інтермісій: рожевий — рівні 1–2, блакитний — 3–5, коричневий — 6–9, темно-синій — 10–13; далі коричневий і темно-синій чергуються кожні 4 рівні в інших кольорах.
- Рожевий, блакитний і темно-синій мають **дві пари** тунелів-тору (в оригіналі — одна).
- Стіни залиті суцільним кольором, а не обведені контуром — коридори легше читати.
- Привиди сповільнюються в тунелях лише перші три раунди; швидкість росте з кожним раундом.
- Real-time; решта (клітинна логіка, рух по осях коридорів) — як у `pac-man.md`.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Ms. Pac-Man | player | — | як Пекмен; при смерті крутиться й «непритомніє» |
| Точка, енерджайзер | pickup | — | як у `pac-man.md`; тривалість frightened скорочується з раундами до нуля |
| Blinky, Pinky | enemy | — | перші секунди рівня — випадковий рух до першого розвороту, далі — свої цілі |
| Inky, Sue | enemy | Sue замість Clyde | від старту — як в оригіналі: ідуть у свої кути до першого розвороту |
| Тунель | terrain | 1 або 2 пари | `wrap`; сповільнює привидів лише в раундах 1–3 |
| Фрукт | pickup | 2 рази за раунд | заїжджає через тунель, підстрибуючи йде лабіринтом і виїжджає через тунель |
| Лабіринт | zone | 4 варіанти | обирається за номером рівня |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «лабіринт = maze_for(level): 1–2 рожевий, 3–5 блакитний, 6–9 коричневий, 10–13 темно-синій, далі чергування»`.
- КОЛИ `level_start` → ТО `set_state(blinky+pinky, random_walk)`; КОЛИ `custom: «перший примусовий розворот режиму»` → ТО `clear_state(blinky+pinky, random_walk)`, `set_state(blinky+pinky, scatter|chase)`.
- КОЛИ `level_start` → ТО `set_state(inky+sue, scatter)` — у свої кути, як в оригіналі.
- КОЛИ `enter(ghost, tunnel)` → ЯКЩО `level(<=, 3)` → ТО `speed(ghost, −)`; інакше — без сповільнення.
- КОЛИ `edge(a)` → ТО `wrap(a)` — у лабіринтах з двома парами тунелів вихід на тому ж рядку протилежного краю.
- КОЛИ `counter(dots_eaten, ==, n1|n2)` → ТО `spawn_at(fruit, tunnel_entry)`, `custom: «фрукт обирає шлях до виходу через інший тунель, підстрибуючи»` (`+effect:path_to`).
- КОЛИ `reach(fruit, tunnel_exit)` → ТО `disappear_a`.
- КОЛИ `contact(mspac, fruit)` → ТО `pickup`, `score(fruit_value)`.
- КОЛИ `spawned(fruit)` → ЯКЩО `level(>=, 8)` → ТО `custom: «вид фрукта випадковий»` (напр., банан на 5000, потім вишні на 100); інакше — фіксована послідовність за рівнем.
- КОЛИ `contact(mspac, energizer)` → ТО `set_state(ghosts, frightened, T(level))`; `T` спадає з раундами й зрештою = 0.
- КОЛИ `contact(mspac, ghost)` → ЯКЩО `not state(ghost, frightened)` → ТО `lives(-1)`.
- КОЛИ `all_gone(dot+energizer)` → ТО `next_level`; після певних рівнів — `window(intermission)` (три сценки).
- Перемога: рекорд очок. Поразка: життя скінчились. Рахунок — точки, енерджайзери, привиди, фрукти (значення — як в оригіналі (?)).

## Керування і ввід
- Як у Pac-Man: 4-позиційний джойстик, 1P/2P Start, два гравці по черзі. Відмінностей у вводі джерела не дають.

## Вікна, меню, HUD
- `attract-demo` — представлення персонажів, демо-гра.
- `game-screen` — лабіринт поточного кольору; `score`, `hi-score`, `lives`, рядок фруктів рівня.
- `+window:intermission` — три сценки: історія пари від знайомства до лелеки, що приносить малюка.
- Переходи — як у `pac-man.md`; додається зміна лабіринту після інтермісії.

## Фічі поза полем
- `levels-sequential` з `+feature:maze-rotation` — лабіринт як функція номера рівня.
- `operator-settings` (DIP) — є (?), деталі не перевірено.
- Перевидання: Atari 2600/7800, NES (зокрема неліцензійна Tengen), Genesis та ін.

## Варіації й родичі
- Походження: Crazy Otto — набір-модифікація для Pac-Man від General Computer Corporation; Midway викупила й випустила як сиквел.
- Далі по лінії: [pac-man-sequels](pac-man-sequels.md) (Jr. Pac-Man зі скролом, Pac-Mania зі стрибком, Pac-Man Vs., Pac-Man 99), [super-pac-man](super-pac-man.md).
- **Осі варіацій:** лабіринт (один / ротація за рівнем / генерований); бонус (стоїть у центрі / мандрує тунель→тунель / мандрує і псує поле — Jr.); детермінізм привидів (повний — патерни працюють / випадкова стартова фаза / випадкові цілі).

## Цікавинки для курсу
- Лабіринт як функція рівня (`maze_for(level)`, таблиця діапазонів) — 🌱.
- Мандрівний бонус: спавн на вході тунелю, шлях до виходу, зникнення — 📎 (потрібен пошук шляху або випадкове блукання з метою).
- Випадкова стартова фаза двох привидів — найпростіший спосіб зламати завчені маршрути — 🌱.
- Дві пари тунелів: тор лише для певних рядків — 🌱.
- Порівняння «патерн проходить / не проходить» як експеримент з детермінізмом — 📎.

## Мапа на каталог
- Є: `move-auto` · `collect-all` · `touch-death` · `temporary-modes` · `chase-greedy` · `random-walk` · `scatter-chase-schedule` · `ghost-house-release` · `wrap-edges` · `speed-per-type` · `escalating-kill-points` · `progress-acceleration` · `sequential-levels`.
- **Нема** → пропозиції карток:
  - `+maze-rotation-by-level` «Лабіринт змінюється за номером рівня» · levels/progression · 🌱.
  - `+roaming-bonus-item` «Бонус заходить з краю, блукає й виходить» · entities/spawn · 📎.
  - `+random-bonus-sequence` «Вид бонусу випадковий з рівня N» · entities/spawn · 🌱.
  - `+random-start-phase` «Вороги перші секунди рухаються випадково» · entities/move · 🌱.
  - `+multi-tunnel-pairs` «Кілька пар тунелів-тору» · entities/move · 🌱 (дитина `wrap-edges`).

## Пропозиції до словників
- `+feature:maze-rotation` — набір полів, що змінюються за номером рівня.
- `+effect:path_to(a, cell)` — сутність іде шляхом до клітини (фрукт до тунелю); ширше за `move`, вужче за `custom`.
- `+card:roaming-bonus-item`, `+card:random-start-phase` — див. вище.

## Джерела
- ⭐ [Wikipedia: Ms. Pac-Man](https://en.wikipedia.org/wiki/Ms._Pac-Man) — кольори й діапазони лабіринтів, тунелі, фрукт, напіввипадковий AI, Sue, інтермісії, Crazy Otto.
- [Wikipedia: Pac-Man](https://en.wikipedia.org/wiki/Pac-Man) — база.
- [The Pac-Man Dossier](https://pacman.holenet.info/) — механіка оригіналу.
- YouTube: пошук «ms pac-man arcade gameplay».

## Непевне
- (?) Пороги точок для двох появ фрукта і таблиця фруктів до 8-го рівня (вишні 100 … банан 5000) — у відкритому джерелі лише приклад «банан 5000, вишні 100».
- (?) Скільки саме триває випадкова фаза Blinky й Pinky («перші кілька секунд»).
- (?) Чи фрукт обирає маршрут випадково чи за фіксованими шляхами для кожного лабіринту.
- (?) Значення очок за привидів/точки та поріг додаткового життя — Wikipedia не дає; ймовірно, як в оригіналі.
- (?) Назви сценок «Act I–III» — з памʼяті; Wikipedia описує лише сюжет трьох інтермісій.
