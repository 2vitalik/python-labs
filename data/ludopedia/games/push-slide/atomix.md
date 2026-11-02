---
title: Atomix
slug: atomix
family: push-slide
also: []
klass: figure
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 1990
platforms: [Amiga, Atari ST, MS-DOS, C64, PC (KAtomic, GNOME Atomix)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Atomix_(video_game)", best: true, note: "правила, таймер, бонус-рівні з колбами, режим на двох, клони"}
  - {kind: official, url: "https://apps.kde.org/katomic/", note: "KAtomic — відкритий клон: клік по атому + зелені стрілки"}
  - {kind: official, url: "https://gitlab.gnome.org/GNOME/atomix/", note: "GNOME Atomix — відкритий клон, код"}
  - {kind: other, url: "https://wiki.gnome.org/Apps/Atomix", note: "архівна сторінка GNOME Atomix"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=atomix+amiga+1990+gameplay", note: "пошук; геймплей Amiga"}
stage: v1
coverage: 75
mechanics: [inertia-slide, impassable-cells, cell-click, keyboard-controls, hover-highlight, time-out, time-bonus, hot-seat, move-timer, sequential-levels, level-select, level-from-txt, level-solver, movement-animation, score-records, +pattern-anywhere, +select-then-move, +order-by-value, +undo-redo]
proposes: ["+trigger:input", "+trigger:pattern", "+effect:slide", "+effect:timer", "+effect:score", "+cond:timer", "+ui:target-preview", "+window:bonus-level", "+feature:restart-cost", "+axis:control"]
author: opus
date: 2026-11-02
---

# Atomix — штовхай атоми, що ковзають до упору, і склади з них молекулу за схемою

## Суть
На полі-лабіринті розкидані атоми (зі стрічками звʼязків), а збоку — схема молекули. Гравець обирає будь-який атом і штовхає в одному з 4 напрямків — атом **ковзає до першої стіни або іншого атома**, як у Ricochet Robots. Мета — щоб атоми стали в точне взаємне розташування зі схеми, у будь-якому місці поля. Час обмежено, швидше — більше очок.

## Поле і час
- Квадратна сітка з внутрішніми стінами (лабіринт), розмір рівня різний (?). Один шар: стіна / підлога / атом. Усе видно.
- Час — real-time лише як таймер рівня; сам пазл детермінований і покроковий: світ змінюється тільки після ходу.
- Схема цілі показана окремо (зліва в оригіналі, вгорі справа в KAtomic) — це шаблон, а не координати.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Атом | piece | елемент (H, C, O, N…), звʼязки (напрями й кратність) | обраний — ковзає в заданому напрямку до упору; блокує інші атоми |
| Стіна | static | — | непрохідна; зупиняє атом |
| Підлога | terrain | — | атом ковзає крізь |
| Курсор / виділення | — (не сутність) | обраний атом | показує, який атом рухатиметься |
| Схема молекули | mark | розташування атомів відносно один одного | ціль-шаблон; позиція на полі довільна, поворот — ні |
| Колба (бонус-рівень) | piece | рівень рідини | ковзає як атом; мета — розставити від порожньої до повної |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(select, atom)` → ТО `custom: «атом стає обраним»`.
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `slide(atom, dir)` до клітини перед першою стіною/атомом; інакше `block` (хід не відбувається).
- Атом не штовхає інших: зупиняється впритул (без ланцюга й без передачі імпульсу).
- КОЛИ `pattern(custom: «атоми утворюють молекулу зі схеми в будь-якому місці, без повороту»)` → ТО `win`, `score(time_left × k)` (?), `next_level`.
- Однакові атоми взаємозамінні: важить лише елемент і звʼязки, а не «який саме» H.
- КОЛИ `counter(time_left, ==, 0)` → ТО `lose` рівня; ЯКЩО `custom: «очок вистачає»` → ТО можна `restart` рівня, сплативши частиною рахунку.
- Кожні 5 рівнів — бонус-рівень: КОЛИ `pattern(custom: «колби впорядковані від порожньої до повної»)` → ТО `score(bonus)`.
- Режим на двох: гравці по черзі розвʼязують той самий пазл, хід кожного — до 30 с.
- Перемога: молекула зібрана в часі. · Поразка: час вичерпано і нема очок на рестарт → `game_over`. · Рахунок: що швидше, то більше.

## Керування і ввід
- Оригінал: курсор (джойстик/миша) наводиться на атом, кнопка — «захопити», напрямок — запустити ковзання (?).
- KAtomic: клік по атому → навколо зʼявляються зелені стрілки в доступні напрямки → клік по стрілці; клавіатура — вибір атома і стрілки (?).
- Двоетапний ввід «обрати фігуру → обрати напрям», як у Ricochet Robots.

## Вікна, меню, HUD
- `splash-screen` / титул Thalion.
- `game-screen`: поле + бічна панель — схема молекули (`+ui:target-preview`), `timer-countdown`, `score`, `level-number`, назва молекули (?).
- `custom-window` бонус-рівень з колбами (`+window:bonus-level`).
- `end-screen`: рівень пройдено / час вичерпано з пропозицією рестарту за очки.
- `leaderboard` — рекорди (?).
- KAtomic: `level-select` (будь-який відкритий рівень), `settings-window` (швидкість анімації (?)), `leaderboard` найменшої кількості ходів (?).
- Переходи: титул → рівень 1 → … → кожен 5-й → бонус-рівень → наступний.

## Фічі поза полем
- `levels-sequential` (30 пазлів зростаючої складності) + бонус кожні 5.
- `mode-versus` / `hotseat` на двох з `turn-timer` 30 с.
- Рестарт за очки — рахунок як ресурс (`+feature:restart-cost`).
- Клони: KAtomic і GNOME Atomix додають `undo`, `level-select`, вибір рівня без таймера (?); рівні описані текстовими файлами (?).

## Варіації й родичі
- Клони: Atomiks, GNOME Atomix, KAtomic, WAtomic; Atomic / Atomic Reloaded (Atari Jaguar).
- Осі варіацій: **хто ковзає**: усі атоми окремо (Atomix) / усе поле разом (2048, Tilt) / роботи, що зупиняються лише об інших (Ricochet Robots, Lunar Lockout); **ціль**: точний шаблон без повороту / шаблон з поворотами (?) / конкретна клітина (Ricochet); **злипання**: ні (Atomix) / атоми зчіплюються при контакті й рухаються разом (Sokobond).
- Родичі: Ricochet Robots, Lunar Lockout, Inertia, Pengo (ковзання до упору), Sokobond.

## Цікавинки для курсу
- Ковзання до упору як єдиний хід (цикл «поки вільно — крок») — 🌱.
- Перевірка «шаблон присутній будь-де на полі» (зсув схеми по всіх позиціях, однакові атоми взаємозамінні) — 📎.
- Двоетапний ввід: вибір атома + стрілки лише в доступні напрями (підсвітка легальних ходів) — 📎.
- BFS-розвʼязувач по станах (позиції атомів, однакові — як мультимножина) з мінімальною кількістю ходів — 🥇.
- Бонус-рівень «впорядкувати за значенням» тими самими правилами — 📎.
- Hot-seat з таймером ходу на одному пазлі — 🌱.

## Мапа на каталог
- Є: `inertia-slide` ↔ атом ковзає до упору; `impassable-cells` ↔ стіни; `cell-click` + `hover-highlight` + `keyboard-controls` ↔ вибір атома; `time-out` + `time-bonus` ↔ таймер і бонус; `hot-seat` + `move-timer` ↔ режим на двох з 30 с; `sequential-levels` + `level-select`; `level-from-txt` ↔ рівні клонів (?); `level-solver` ↔ BFS; `movement-animation`; `score-records`.
- **Нема** → пропозиції карток:
  - `+pattern-anywhere` «Ціль — шаблон будь-де на полі» · game-logic/win · 📎 · слот {rotations: bool}.
  - `+select-then-move` «Вибір фігури, потім напрям» · interface/input · 📎.
  - `+order-by-value` «Впорядкувати обʼєкти за значенням» · game-logic/win · 🌱 — колби.
  - `+undo-redo` «Undo/redo ходів у грі» · game-logic/flow · 📎 (клони).

## Пропозиції до словників
- `+trigger:input` — вибір атома й напрям; `+trigger:pattern` — молекула з атомів (новий підвид `pattern(template, anywhere)`).
- `+effect:slide` — основний хід; `+effect:timer` — рестарт ціною очок поновлює час; `+effect:score`.
- `+cond:timer` — бонус за залишок часу.
- `+ui:target-preview` — мініатюра цілі поруч із полем (схема молекули, картинка-ціль).
- `+window:bonus-level` — бонусний рівень з іншими правилами цілі.
- `+feature:restart-cost` — рестарт рівня коштує очок/життя.
- `+axis:control` — `select-then-move`: вибір фігури, потім команда (не `direct`, не `indirect`).

## Джерела
- ⭐ [Wikipedia: Atomix](https://en.wikipedia.org/wiki/Atomix_(video_game)) — правила, таймер, рестарт за очки, бонус-рівні з колбами, режим на двох (30 с), 30 рівнів, клони.
- [KAtomic (KDE)](https://apps.kde.org/katomic/) — клік по атому + зелені стрілки, молекулу можна скласти будь-де.
- [GNOME Atomix (GitLab)](https://gitlab.gnome.org/GNOME/atomix/) — відкритий код клону.
- [GNOME Wiki: Atomix](https://wiki.gnome.org/Apps/Atomix) — коротко: атоми ковзають до стіни/атома, превʼю молекули.
- YouTube: пошук «atomix amiga 1990 gameplay».

## Непевне
- (?) Розмір поля, керування в оригіналі (курсор/кнопка), формула очок і таблиця рекордів — не перевірено.
- (?) Чи дозволено повертати молекулу (ймовірно ні — звʼязки атомів мають напрям) — джерела прямо не кажуть.
- (?) Undo, вибір рівня, лічильник ходів і формат рівнів у KAtomic/GNOME Atomix — сторінки цього не описують; за памʼяттю.
- Пошуковий бюджет сесії вичерпався; документація KAtomic на docs.kde.org повернула 404.
