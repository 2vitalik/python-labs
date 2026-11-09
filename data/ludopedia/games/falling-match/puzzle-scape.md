---
title: Puzzle Scape
slug: puzzle-scape
aka: [PuzzleScape]
family: falling-match
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: online
  info: full
  random: runtime
  goal: state
year: 2007
platforms: [PSP, PlayStation Minis (PS3, PS Vita)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Puzzle_Scape", best: true, note: "суть: квадрат 2×2 видаляє всіх дотичних того ж кольору; розробник, видання"}
  - {kind: other, url: "https://www.honestgamers.com/5878/psp/puzzle-scape/review.html", note: "огляд: ряди на всю ширину згори, захват двох клітин і зсув ←/→, зони з цілями на час, медалі, Paint, 40 скінів"}
  - {kind: other, url: "https://www.pocketgamer.com/puzzle-scape/psps-puzzle-scape-turns-lumines-on-its-head", note: "режими Architect / Artist / Bomb Run (до 8 гравців), 4 теми"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=puzzle+scape+psp+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [gravity-fall, chain-reaction, connectivity-check, keyboard-controls, time-out, progress-acceleration, sequential-levels, level-select, simultaneous-versus, event-points, score-records, end-screen, mode-select, +square-group-match, +rising-stack, +swap-cursor, +zone-objectives, +medal-rating, +skin-unlock-progression, +recolor-power]
proposes: ["+effect:flood_clear", "+ui:objective-list", "+card:zone-objectives", "+card:recolor-power"]
author: opus
date: 2026-11-09
---

# Puzzle Scape — довгі «нитки» одного кольору, які підриває квадрат 2×2

## Суть
Блоки падають на поле повними рядами згори; фігуру не обертають, як у Lumines, — гравець **переставляє вже лежачі блоки**, захоплюючи дві клітини й зсуваючи їх уліво-вправо (як у Tetris Attack). Збіг — квадрат 2×2 одного кольору; коли він складається, разом із ним видаляються **всі дотичні блоки того ж кольору** — тож вигідно спершу виростити довгу звʼязну «нитку» й лише потім замкнути квадрат. Довші ланцюги дають більше павер-апів.

## Поле і час
- Прямокутне поле з верхом і низом; розмір не названо (?).
- Нові блоки надходять **рядами на всю ширину** згори — новий ряд при високому стеку смертельний.
- Real-time; поразка — стек дійшов верху (попереджувальний звук перед кінцем).
- Лише горизонтальні переміщення; вертикально блок рухається тільки гравітацією.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Курсор-захват | player | 2 клітини | хапає дві сусідні клітини й зсуває ←/→ |
| Блок | tile | колір | падає в порожнечу; у звʼязній групі з квадратом 2×2 — видаляється |
| Квадрат 2×2 | zone | 4 блоки одного кольору | «детонатор»: видаляє себе і всю звʼязну групу свого кольору |
| Ряд згори | spawner | повна ширина | приходить періодично, тисне на стек |
| Paint (апгрейд) | pickup | шкала | коли шкала повна — перефарбовує блоки (?) |
| Верх поля | static | межа | стек тут → поразка |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(grab)` → ТО `custom: «курсор захоплює дві сусідні клітини»`.
- КОЛИ `input(left|right)` → ЯКЩО `free(target)` або там блок → ТО `move(grabbed, dir)` (обмін із сусідом (?)).
- КОЛИ `after(move)` → ЯКЩО `free(cell_below)` → ТО `fall(block)`.
- КОЛИ `pattern(group(2×2, same_color))` → ТО `custom: «flood_clear — видалити квадрат і всі звʼязні блоки того ж кольору»`, `score(n)`.
- КОЛИ `pattern(group(2×2))` → ЯКЩО `connected(same_color_group)` велика → ТО `give(player, power_up)` — довший ланцюг дає більше павер-апів.
- КОЛИ блок посунуто під миготливу групу, що видаляється → ТО `block` — захват зривається, треба взяти знову.
- КОЛИ `after(clear)` → ТО `fall(blocks_above)`; КОЛИ `settled` → ЯКЩО новий квадрат → ТО ланцюг.
- КОЛИ `timer(every)` → ТО `spawn_at(row, top)` — новий ряд на всю ширину.
- КОЛИ `counter(meter, ≥, full)` → ЯКЩО `has(player, paint)` → ТО `custom: «recolor — перефарбувати блоки»` (?).
- КОЛИ `reach(stack, top)` → ТО `lose`.
- Architect: КОЛИ `all_constraints_met` (усі 10–12 цілей зони, напр. «нитка з 12 блоків одного кольору без вибуху») → ЯКЩО `timer(>, 0)` → ТО `win`, медаль за час.
- Bomb Run: КОЛИ `counter(destroyed, ≥, quota)` → ТО `win` (перший з до 8 гравців).
- Перемога: виконати цілі зони вчасно / перший у Bomb Run · Поразка: стек дійшов верху · Рахунок: Artist — очки на виживання.

## Керування і ввід
- Хрестовина — курсор; утримання кнопки — захват двох клітин; ←/→ — зсув захопленого.
- Без обертання фігур; уся гра — у перестановці лежачих блоків під тиском рядів.

## Вікна, меню, HUD
- `main-menu` → `mode-select`: Architect · Artist · Bomb Run (Wi-Fi) · кооператив/versus для Architect і Artist.
- `level-select`: меню зон; наступна зона відкривається після проходження.
- `game-screen`: поле, курсор, `+ui:objective-list` (цілі зони), `timer-countdown`, шкала павер-апу (`energy-bar`), `score`.
- `end-screen` з медаллю (золото тощо) і розблокованим скіном.
- Збереження знімка рівня як шпалери PSP (`custom-window`).

## Фічі поза полем
- Режими: Architect (цілі на час), Artist (виживання / рекорд), Bomb Run (до 8 гравців, гонка).
- `level-unlock`, повтор зон заради кращого часу/медалі (`stars-rating`-подібні медалі).
- `unlockables`: 40 скінів (по одному за перше проходження рівня), апгрейд Paint за золото.
- 4 теми (клітини, квіти, машини, сни) зі зростанням рівня; `local-multiplayer` по Wi-Fi.

## Варіації й родичі
- Квадрат 2×2 як збіг — від [lumines](lumines.md); перестановка лежачих блоків під тиском рядів — від [panel-de-pon](panel-de-pon.md).
- Видалення всієї звʼязної групи кольору, коли спрацював «детонатор» — родич [puyo-puyo](puyo-puyo.md) (звʼязна група) і [samegame-flood](samegame-flood.md) (flood-заливка групи).
- **Осі варіацій**: форма-тригер (лінія / квадрат 2×2 / група N) · що зникає (лише шаблон / шаблон + уся звʼязна група) · ввід (керувати фігурою / swap / захват 2 клітин) · подача (фігури / повні ряди).

## Цікавинки для курсу
- «Детонатор» 2×2 + flood fill звʼязної групи того ж кольору — 📎.
- Захват двох клітин і зсув ←/→ без вертикалі — 🌱.
- Список цілей зони (нитка з N, без вибуху тощо) як чекліст з таймером — 🥉.
- Медалі за час + розблокування скіна за перше проходження — 📎.
- Bomb Run — гонка до квоти для кількох гравців — 🥈.

## Мапа на каталог
- Є: `gravity-fall` · `chain-reaction` · `connectivity-check` (звʼязна група) · `keyboard-controls` · `time-out` · `progress-acceleration` (?) · `sequential-levels` · `level-select` · `simultaneous-versus` · `event-points` · `score-records` · `end-screen` · `mode-select`.
- **Нема** → пропозиції карток:
  - `+square-group-match` — ⏳ підтверджую (Lumines); тут квадрат лише «запал».
  - `+rising-stack` (тут — ряди згори) · `+swap-cursor` — ⏳ підтверджую.
  - `+zone-objectives` «Список цілей рівня на час» · game-logic/win · 🥉.
  - `+medal-rating` «Медаль за час проходження» · levels/progression · 🌱.
  - `+skin-unlock-progression` — ⏳ підтверджую (Lumines).
  - `+recolor-power` «Павер-ап перефарбовує блоки» · entities/interact · 🌱.

## Пропозиції до словників
- `+effect:flood_clear` — ⏳ підтверджую (Lumines): прибрати всю звʼязну групу кольору.
- `+ui:objective-list` — список цілей рівня з галочками.
- `+card:zone-objectives` · `+card:recolor-power`.

## Джерела
- ⭐ [Wikipedia: Puzzle Scape](https://en.wikipedia.org/wiki/Puzzle_Scape) — правило 2×2 + дотичні того ж кольору, Farmind, видання 2007, Minis 2009.
- [HonestGamers: Puzzle Scape review](https://www.honestgamers.com/5878/psp/puzzle-scape/review.html) — ряди на всю ширину, захват двох клітин, зони з 10–12 цілями на час, медалі, Paint, 40 скінів.
- [Pocket Gamer: Puzzle Scape turns Lumines on its head](https://www.pocketgamer.com/puzzle-scape/psps-puzzle-scape-turns-lumines-on-its-head) — Architect / Artist / Bomb Run до 8 гравців, 4 теми.
- YouTube: пошук «puzzle scape psp gameplay».

## Непевне
- (?) Розмір поля, темп рядів, чи прискорюється подача.
- (?) Захват 2 клітин: обмін із сусідом чи зсув у порожнечу — джерела розходяться («swap two adjacent» у пошуку vs «grab two spaces and slide»).
- (?) Повний список павер-апів; Paint — «перефарбовує блоки, коли шкала повна».
- (?) Чи звʼязність рахується лише по 4 сторонах.
- (?) Bomb Run і Wi-Fi — локальна бездротова (ad hoc), не інтернет; `opponent: online` умовно.
