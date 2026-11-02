---
title: Klotski (Хуажунський шлях) + Lunar Lockout
slug: klotski
family: push-slide
also: []
klass: figure
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: state
year: 1909
platforms: [wooden, Windows (Entertainment Pack), GNOME, mobile, board (Lunar Lockout)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Klotski", best: true, note: "правила, 10 фігур на 4×5, 81 хід (Гарднер 1964), назви по країнах, варіанти, комп'ютерні версії"}
  - {kind: other, url: "https://en.wikipedia.org/wiki/Sliding_puzzle", note: "жанр ковзних блоків, споріднені пазли"}
  - {kind: other, url: "https://puzzleworld.org/PuzzleWorld/puz/lunar_lockout.htm", note: "Lunar Lockout: автор Hiroshi Yamamoto (UFO), G4G 1998, Binary Arts 2000, поле 9×9 → 5×5"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Games_100", note: "Lunar Lockout у списку Games 100"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Klotski+81+moves+solution", note: "пошук; оптимальний розвʼязок"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Lunar+Lockout+puzzle", note: "пошук; правила Lunar Lockout"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=klotski", note: "пошук; цифрові версії"}
stage: v1
coverage: 75
mechanics: [multi-cell-size, impassable-cells, reach-exit, drag-drop-piece, cell-click, keyboard-controls, legal-move-highlight, inertia-slide, level-bank, level-select, level-rating, difficulty-levels, level-solver, level-from-txt, unique-puzzle-generation, difficulty-rating, score-records, completion-detection, +undo-redo, +select-then-move, +stop-on-entity, +move-vs-step, +state-string, +stars-rating, +slide-needs-blocker, +shape-equivalent-state, +exit-gap]
proposes: ["+trigger:input", "+trigger:reach", "+trigger:blocked", "+cond:free", "+cond:occupied", "+effect:move", "+effect:slide", "+effect:counter", "+role:piece", "+ui:move-counter", "+ui:par-moves", "+ui:legal-move-highlight", "+window:puzzle-select", "+feature:par-target", "+feature:puzzle-bank", "+axis:stop-rule"]
author: opus
date: 2026-11-02
---

# Klotski + Lunar Lockout — зсунь блоки, щоб великий вийшов; або ковзай, доки не вдаришся в робота

## Суть
**Klotski** (Хуажунський шлях, L'Âne Rouge, «Дочка в коробці») — коробка 4×5 з десятьма прямокутними блоками чотирьох розмірів і двома порожніми клітинами; блоки ковзають у порожнечу, мета — вивести великий 2×2 через щілину внизу посередині. Без випадковості й ворогів, уся складність — у тісноті: мінімум **81 хід** (якщо хід = переміщення однієї фігури куди завгодно). **Lunar Lockout** (Hiroshi Yamamoto, 2000) додає протилежне правило руху: фігура ковзає до упору, а **стін нема** — зупинити може лише інший робот; мета — привести червоний корабель у центр 5×5. Разом — дві осі «що обмежує рух»: тіснота (Klotski) і брак опор (Lunar Lockout).

## Поле і час
- Klotski: прямокутна коробка 4 (ширина) × 5 (висота); вихід — щілина шириною 2 посередині нижнього борту (лише для 2×2). 18 клітин зайнято, 2 порожні.
- Lunar Lockout: квадрат 5×5 без стін (прототип 9×9); центральна клітина — ціль (отвір корабля); краї — відкритий космос.
- Один шар фігур; поле видно цілком. Хід = переміщення однієї фігури; часу нема (`static`), лише лічильник ходів (фізична версія — на честь, цифрова — HUD).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Великий квадрат 2×2 («Цао Цао», «осел») | piece | 2×2, ціль | ковзає в будь-якому з 4 напрямків, якщо обидві клітини попереду вільні; виходить крізь щілину |
| Вертикальний 1×2 ×4 (генерали) | piece | ширина 1, висота 2 | ковзає, якщо вільні клітини попереду всієї кромки |
| Горизонтальний 2×1 ×1 (Гуань Юй) | piece | ширина 2, висота 1 | так само |
| Малий 1×1 ×4 (солдати) | piece | 1×1 | ковзає на 1–2 клітини, може завернути «за ріг» у межах одного ходу |
| Порожня клітина ×2 | terrain | — | єдиний ресурс руху |
| Борт коробки | static | — | непрохідний |
| Вихід-щілина | static | ширина 2, низ посередині | крізь нього проходить лише 2×2 → перемога |
| Червоний корабель (Lunar Lockout) | piece | ціль — центр | ковзає по прямій до першого робота; зупиняється перед ним |
| Робот-помічник ×1–5 (?) (Lunar Lockout) | piece | колір | ковзає так само; служить «стіною» для інших |
| Центр (Lunar Lockout) | terrain | ціль | червоний, що зупинився тут, — перемога; проліт крізь центр не рахується |
| Космос за краєм (Lunar Lockout) | hazard | — | хід, після якого фігура вилетіла б без зупинки, заборонений |

## Правила (КОЛИ → ЯКЩО → ТО)
- Klotski: КОЛИ `input(select(piece), dir)` → ЯКЩО `free(cells_ahead_of_piece_edge)` → ТО `move(piece, dir)`; інакше `block`.
- Klotski: КОЛИ ту саму фігуру зсунуто ще раз одразу після попереднього кроку → ТО `counter(moves, +0)` у метриці «хід = фігура» (`counter(steps, +1)`); у метриці «хід = клітина» — +1 кожен крок. Гарднерові 81 — у першій метриці.
- Klotski: перехід «за ріг» малого 1×1 (вправо, потім униз в одній дії) — один хід у метриці «фігура».
- Klotski: КОЛИ `reach(big_2x2, exit_slot)` → ТО `win` (у фізичній версії — великий блок посеред нижнього ряду, можна висунути назовні).
- Lunar Lockout: КОЛИ `input(select(piece), dir)` → ЯКЩО `custom: «на лінії руху є інша фігура»` → ТО `slide(piece, dir)` до клітини перед нею (`+stop-on-entity`); інакше `block` (у космос летіти не можна).
- Lunar Lockout: КОЛИ `custom: «червоний зупинився в центрі»` → ТО `win`; проходження центру без зупинки — звичайний хід.
- Lunar Lockout: стін і бортів нема — крайові клітини не зупиняють.
- Обидві: фігури не обертаються, не знімаються, не перестрибують одна одну.
- Перемога: Klotski — 2×2 у виході; Lunar Lockout — червоний у центрі. · Поразка: нема (глухих кутів у Klotski нема: усі ходи оборотні; у Lunar Lockout ходи не завжди оборотні — можна «розгубити» опори (?)). · Рахунок: кількість ходів проти мінімуму (81 для класики; у картках Lunar Lockout — рівень складності 1–4 (?)).

## Керування і ввід
- Фізично: пальцем штовхати блок у порожнечу; Lunar Lockout — пересувати фігуру по картці-завданню.
- Цифрові версії: drag фігури в напрямку (фігура йде настільки, наскільки тягнуть, у межах вільного); або клік фігури → клік цільової клітини (`select-then-move`); стрілки при обраній фігурі (?).
- Lunar Lockout цифрово: свайп по фігурі — ковзання до упору; підсвітка допустимих напрямків.

## Вікна, меню, HUD
- `game-screen`: коробка з фігурами; HUD — `move-counter`, `par-moves` (мінімум), `undo-button`, `restart-button`.
- `puzzle-select` (GNOME Klotski, мобільні): категорії стартових розстановок (Huarong Trail, Pennant, Ma's, «Дочка в коробці»…) з позначкою «розвʼязано» і рекордом ходів (?).
- `level-select` Lunar Lockout (цифрова версія): 40 карток-завдань за 4 рівнями складності (?).
- `end-screen`: «розвʼязано за N ходів» + порівняння з оптимумом; `leaderboard` — локальні рекорди (GNOME Klotski — таблиця рекордів (?)).
- `help-window` — правила з картинкою виходу.
- Переходи: main-menu / puzzle-select → game-screen → (виведено) end-screen → наступна розстановка.

## Фічі поза полем
- `puzzle-bank` стартових розстановок: оригінал (81 хід), Pennant Puzzle (59), Ma's Puzzle (непрямокутні фігури), Khun Chang Khun Phaen (тайська, трохи інша розстановка), 1934 англійський патент (79), китайська книга 1952 (100 кроків).
- `undo` / `restart-level`; `par-target` (оптимум ходів); `stats` (рекорд по розстановці).
- Комп'ютерні версії: Jim Bates (1988), Klotski для Windows 3.x від ZH Computer (1991) у Microsoft Entertainment Pack, GNOME Klotski.
- Lunar Lockout: 40 завдань у фізичному наборі (колекціонери з 1998 мали «сорок або більше» прикладів 5×5).

## Варіації й родичі
- [Rush Hour](rush-hour.md) — блоки 1×2/1×3, кожен рухається лише вздовж своєї осі (`+axis-locked-move`); Klotski — блоки рухаються в обох осях.
- [Sliding-tile permutation](sliding-tile-permutation.md) — 15-puzzle, прабатько: усі плитки 1×1, одна дірка.
- [Ricochet Robots](ricochet-robots.md) — ковзання до упору, зупиняють **і стіни, і роботи**; Lunar Lockout = Ricochet без стін.
- [Atomix](atomix.md) — ковзання атомів до упору, зібрати молекулу.
- Осі варіацій:
  - **форма фігур**: усі 1×1 (15-puzzle) · прямокутники різних розмірів (Klotski) · непрямокутні (Ma's Puzzle) · закріплені осі (Rush Hour);
  - **дальність ходу**: на 1 клітину · на будь-яку відстань у межах вільного (`+any-distance-slide`) · до упору (Lunar Lockout);
  - **що зупиняє ковзання** (Lunar Lockout-вісь): лише фігури · фігури й стіни (Ricochet) · спецклітини-стопи ([Inertia](ice-sliding-puzzles.md));
  - **метрика ходу**: фігура-хід vs клітина-крок (`+move-vs-step`).
- Складність: задача «чи досяжний вихід» для ковзних блоків загалом PSPACE-повна (Hearn & Demaine) (?).

## Цікавинки для курсу
- Рух прямокутної фігури: перевірка вільної кромки для 1×1/1×2/2×1/2×2 — 🌱.
- Drag фігури з «прилипанням» до клітин і заворотом за ріг для 1×1 — 🥉.
- BFS-розвʼязувач Klotski з нормалізацією стану (однакові за формою фігури взаємозамінні → у рази менше станів) — 🥈; показ оптимального шляху як replay — 📎.
- Дві метрики (фігура/крок) і оптимум у кожній — 📎.
- Lunar Lockout: генерація від цілі назад (обернений BFS з центру) + відбір карток з довгим мінімумом — 🥇.
- Правило «ковзай лише якщо є опора» — 🌱, але змінює весь простір станів (ходи стають необоротними).

## Мапа на каталог
- Є: `multi-cell-size` ↔ блоки 1×2/2×1/2×2; `impassable-cells` ↔ борт; `reach-exit` ↔ щілина / центр; `drag-drop-piece` + `cell-click` + `keyboard-controls` ↔ способи ходу; `legal-move-highlight` ↔ напрямки Lunar Lockout; `inertia-slide` ↔ ковзання до упору; `level-bank` + `level-select` + `level-rating` + `difficulty-levels` ↔ розстановки й картки; `level-solver` + `unique-puzzle-generation` + `difficulty-rating` ↔ BFS, генерація карток; `level-from-txt` ↔ розстановка з txt; `score-records` ↔ рекорд ходів; `completion-detection`.
- **Нема** → пропозиції карток:
  - `+slide-needs-blocker` «Ковзання лише до іншої фігури» · entities/legality · 🌱 — хід без зупинки заборонений (Lunar Lockout).
  - `+shape-equivalent-state` «Однакові фігури взаємозамінні в стані» · levels/solvability · 📎 — нормалізація для BFS.
  - `+exit-gap` «Вихід лише для фігури певного розміру» · game-logic/win · 🌱 — щілина 2 клітини.
  - Повтор корпусу: `+undo-redo`, `+select-then-move`, `+stop-on-entity`, `+move-vs-step`, `+state-string`, `+stars-rating`.

## Пропозиції до словників
- `+trigger:input`, `+trigger:reach` — фігура досягла виходу/центру, `+trigger:blocked`.
- `+cond:free` — уся кромка фігури вільна; `+cond:occupied` — на лінії є фігура-опора.
- `+effect:move`, `+effect:slide`, `+effect:counter` (ходи/кроки).
- `+role:piece` — фігури без аватара.
- `+ui:move-counter`, `+ui:par-moves`, `+ui:legal-move-highlight`.
- `+window:puzzle-select`; `+feature:par-target`, `+feature:puzzle-bank`.
- `+axis:stop-rule` — що зупиняє ковзання: `wall` · `entity` · `wall+entity` · `stop-cell` · `none` (крок на 1); одна вісь на Klotski, Lunar Lockout, Ricochet, Inertia, Pokémon-лід.

## Джерела
- ⭐ [Wikipedia: Klotski](https://en.wikipedia.org/wiki/Klotski) — 4×5, склад фігур, 81 хід (метрика «фігура в будь-яку досяжну позицію»), Pennant 59, назви по країнах, історія (1909 копірайт Pennant, 1934 патент, Гарднер 1964), версії Jim Bates 1988 / ZH Computer 1991 / GNOME, рекорд 3.99 с (2024).
- [Wikipedia: Sliding puzzle](https://en.wikipedia.org/wiki/Sliding_puzzle) — жанр і споріднені пазли.
- [Puzzle World: Lunar Lockout](https://puzzleworld.org/PuzzleWorld/puz/lunar_lockout.htm) — Hiroshi Yamamoto, назва UFO, Gathering for Gardner 1998, Binary Arts весна 2000, 9×9 → 5×5, «40 або більше» прикладів.
- [Wikipedia: Games 100](https://en.wikipedia.org/wiki/Games_100) — Lunar Lockout у списку.
- YouTube: пошуки «Klotski 81 moves solution», «Lunar Lockout puzzle».

## Непевне
- (?) Точні правила Lunar Lockout (кількість роботів 1–5, 40 карток за 4 рівнями, заборона вилету за край) — з памʼяті; сторінка Puzzle World правил не містить, ThinkFun-сторінка 404, пошук вичерпано.
- (?) PSPACE-повнота ковзних блоків (Hearn & Demaine) — з памʼяті, у статті Klotski не згадано.
- (?) Набори розстановок GNOME Klotski і наявність таблиці рекордів.
- (?) Чи всі ходи Lunar Lockout необоротні / чи можливий глухий кут.
