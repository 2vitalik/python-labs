---
title: inbento
slug: inbento
aka: [InBento]
family: thinky
also: []
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2019
platforms: [iOS, Android, Switch, Xbox One, Xbox Series, PC (Steam, Windows, macOS)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1567440/inbento/", best: true, note: "опис і трейлер: обмежений набір шматків + картинка страви; обертати, рухати, вкладати в порядку; далі — міняти, виймати, копіювати; 120+ рецептів; відгуки з клавішами й структурою"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Inbento", note: "розробник Afterburn (Golf Peaks), видавець 7Levels, Unity; платформи, оцінки"}
  - {kind: other, url: "https://russelltroxel.com/writing/2020/3/19/inbento-review", note: "огляд: коробка 3×3 → 4×3, шматки 1–3 клітини, накривання, дії swap / copy / scoop, 14 розділів × 9"}
  - {kind: other, url: "https://vooks.net/inbento-switch-review", note: "огляд Switch: модифікатори повертають і копіюють, 127 рівнів, тач і стіки, iOS/Android — вересень 2019"}
  - {kind: other, url: "https://www.thexboxhub.com/inbento-review/", note: "огляд Xbox: розрізання, шматки без обертання, дублювання, обмін; 127 пазлів, 14 розділів"}
  - {kind: other, url: "http://www.148apps.com/inbento/inbento-review/", note: "огляд мобільної версії: блоки виймання й копіювання, undo тапом"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=inbento+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [polyomino-placement, piece-rotate-flip, drag-drop-piece, cell-click, keyboard-controls, move-limit, undo-unlimited, restart-level, sequential-levels, level-unlock, level-select, save-progress, +target-pattern-panel, +layered-tile-stack, +copy-region, +overwrite-placement, +modifier-pieces, +scoop-reuse, +chapter-unlock-quota, +rotate-lock]
proposes: ["+effect:scoop", "+card:overwrite-placement", "+card:modifier-pieces", "+card:scoop-reuse", "+card:chapter-unlock-quota", "+card:rotate-lock", "+ui:target-panel"]
author: opus
date: 2026-11-09
---

# inbento — склади бенто за картинкою: поклади шматки в правильному порядку, верхній накриває нижній

## Суть
Пазл на маленькій сітці-коробці (3×3, пізніше 4×3): є картинка готової страви і обмежений набір шматків їжі (поліоміно з 1–3 клітин). Шматок, покладений на зайняті клітини, **накриває** те, що там було, тож головне — порядок і поворот. Далі додаються **модифікатори** — шматки-дії, що змінюють уже покладене: обмін двох клітин, копіювання клітини, виймання верхнього шару, зсув, поворот. Від Afterburn (автори Golf Peaks), 127 рівнів у 14 розділах з німою історією про кішку-маму.

## Поле і час
- Коробка — прямокутна сітка від 1×2 до 4×3; часто вже частково заповнена на старті.
- Кожна клітина має **стос шарів**: видно верхній; виймання знімає верхній шар (LIFO) (?).
- Поруч — лоток (запас) шматків і дій та зразок-картинка в куті екрана.
- Хід = використати один шматок/дію; кількість шматків = ліміт ходів; часу нема.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Коробка бенто | zone | w×h, стос шарів у клітині | приймає шматки; порівнюється зі зразком |
| Зразок (рецепт) | mark | картинка w×h | ціль: коробка має виглядати так само |
| Шматок їжі | tile | форма 1–3 клітини, вид їжі на кожній | кладеться в коробку; накриває клітини під собою |
| Заблокований шматок | tile | замок | не обертається |
| Лоток | supply | список шматків і дій | кожен елемент — один раз; порожній лоток = кінець спроб |
| Обмін (swap) | object | 2 клітини | міняє вміст двох клітин коробки |
| Копія (copy) | object | джерело → ціль | вміст однієї клітини копіюється в іншу |
| Виймання (scoop) | object | форма | забирає клітини з коробки, їх можна покласти знову (?) |
| Зсув (move) | object | напрям | переносить клітини в коробці (?) |
| Поворот-модифікатор | object | 90° | повертає те, що вже лежить у коробці (?) |
| Новий тип плитки (розділ 13) | tile | — | зʼявляється пізно; суть (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag piece → box)` → ЯКЩО `fits(piece, cells)` (усі клітини в межах коробки) → ТО `place(player, piece)`, `custom: «клітини шматка лягають верхнім шаром і накривають попередні»`.
- КОЛИ `input(rotate)` → ЯКЩО `not state(piece, locked)` → ТО `rotate(piece, 90)`.
- КОЛИ `input(apply swap → cell_a, cell_b)` → ТО `swap(cell_a, cell_b)`.
- КОЛИ `input(apply copy → src, dst)` → ТО `set_value(dst, food(src))`.
- КОЛИ `input(apply scoop → cells)` → ТО `custom: «верхній шар клітин виймається й повертається в лоток як новий шматок»` (?).
- КОЛИ `input(apply move → cells, dir)` → ТО `move(cells, dir)` (?).
- КОЛИ `input(apply rotate_modifier → cells)` → ТО `rotate(cells, 90)` (?).
- КОЛИ `after(place|apply)` → ТО `take(supply, item)` — використаний елемент зникає з лотка.
- КОЛИ `pattern(target_picture)` → ТО `win`, `next_level`.
- КОЛИ `counter(supply, ==, 0)` → ЯКЩО `not pattern(target_picture)` → ТО `custom: «глухий кут: undo або рестарт»`; штрафу нема.
- КОЛИ `input(undo)` → ТО `undo(1)` (без ліміту); КОЛИ `input(restart)` → ТО `restart`.
- КОЛИ `counter(solved_in_chapter, >=, 7)` → ТО `unlock(next_chapter)` — з 9 рівнів розділу досить 7.
- КОЛИ `custom: «гравець знаходить вхід у титрах»` → ТО `custom: «відкривається прихований рівень»`.
- Перемога: коробка = зразок. · Поразка: нема (лише глухий кут). · Рахунку нема.

## Керування і ввід
- Миша/тач: перетягнути шматок або клік — взяти, клік — покласти; правий клік під час тримання — поворот (якщо не заблокований).
- Клавіатура (PC): стрілки — вибір шматка/клітини, Tab — поворот, Enter — покласти, Esc — повернути шматок.
- Switch: тач або стіки + A; мобільні: тап по екрану — undo.

## Вікна, меню, HUD
- `main-menu` (?): продовжити, розділи, налаштування.
- `puzzle-select` / `chapter-select`: «сторінки» книги рецептів по 9 рівнів; відкрито 3 нерозвʼязані рівні пачки водночас; позначки розвʼязаних.
- `game-screen`: коробка, лоток шматків і дій, зразок угорі праворуч; `undo-button`, `restart-button`.
- `custom-window`: інтерактивна ілюстрація-історія після розділу (без тексту).
- `tutorial-window`: безтекстове навчання — перші 1–2 рівні розділу показують нову дію.
- `credits-window`: титри, з яких відкривається прихований рівень.
- `settings-window`: звук, мова (16 мов).

## Фічі поза полем
- `levels-sequential` + `level-unlock` (розділ відкривається після 7 з 9) + `level-select`.
- `undo` ∞, `restart-level`; підказок у грі нема (гравці шукають гайди).
- `achievements` (за розділи, прихований рівень «Family Portrait»), `cloud-save`, `localization`, `touch-controls`, `gamepad-support`, `mouse-and-keyboard`.
- `tutorial` без тексту; сюжет — картинки між розділами.

## Варіації й родичі
- Порти: iOS/Android (вересень 2019) → Switch (березень 2020) → Xbox (2021) → PC (Steam); видавець 7Levels.
- Того ж автора: `games/thinky/golf-peaks.md` (та сама структура розблокування), Railbound (`games/connect-rotate/railbound.md`).
- Родичі: Patchwork/Blokus (викладання поліоміно), `games/thinky/recopy.md` (копіювання області за зразком), Mendel Palace (стос шарів плиток).
- **Осі варіацій:** накладання — заборонене (Blokus) / накриває (inbento); дії над полем — лише покласти / обмін / копія / виймання / зсув / поворот; ліміт — кількість шматків / кількість ходів; шари — один / стос з LIFO.

## Цікавинки для курсу
- Поліоміно в межах коробки з поворотом і замком — 📎.
- Стос шарів у клітині, видно верхній, виймання знімає верхній — 🥉.
- Модифікатори як «шматки-дії» в тому ж лотку (swap / copy / move / rotate) — 🥉 за сімʼю, кожен 🌱.
- Перевірка «коробка == зразок» (порівняння двох матриць) — 🌱.
- Розвʼязувач: перебір порядку, поворотів і позицій для ≤5 елементів — 🥈 (малий, але комбінаторний простір).
- Розблокування розділу квотою 7/9 і «3 відкриті водночас» — 🌱.

## Мапа на каталог
- Є: `polyomino-placement` ↔ шматки 1–3 клітини; `piece-rotate-flip` ↔ поворот перед покладанням; `drag-drop-piece` + `cell-click` + `keyboard-controls` ↔ ввід; `move-limit` ↔ лоток = ліміт; `undo-unlimited` + `restart-level`; `sequential-levels` + `level-unlock` + `level-select`; `save-progress`.
- Уже пропоновані іншими файлами: `+target-pattern-panel` (Recopy), `+layered-tile-stack` (Mendel Palace), `+copy-region` (Recopy).
- **Нема** → пропозиції карток:
  - `+overwrite-placement` «Нова фігура накриває покладене» · entities/legality · 📎.
  - `+modifier-pieces` «Фігури-дії в запасі поряд з фігурами-обʼєктами» · entities/interact · 🥉 · слот {kinds: swap|copy|scoop|move|rotate}.
  - `+scoop-reuse` «Вийняти шар з поля й покласти знову» · entities/interact · 📎.
  - `+chapter-unlock-quota` «Наступний розділ — після N з M рівнів» · levels/progression · 🌱.
  - `+rotate-lock` «Фігура з замком не обертається» · entities/legality · 🌱.

## Пропозиції до словників
- `+effect:scoop` — вийняти верхній шар клітин і повернути його в запас як фігуру.
- `+card:overwrite-placement`, `+card:modifier-pieces`, `+card:scoop-reuse`, `+card:chapter-unlock-quota`, `+card:rotate-lock` — механік нема в каталозі.
- `+ui:target-panel` — зразок цілі в куті екрана (як у Recopy).

## Джерела
- ⭐ [Steam: inbento](https://store.steampowered.com/app/1567440/inbento/) — опис (обертати, рухати, вкладати в порядку; міняти, виймати, копіювати; 120+ рецептів; безтекстове навчання; ілюстрації за розділ); відгуки: накривання шарами, LIFO-виймання, клавіші, 127 рівнів у 14 світах, 7 з 9 для наступного світу, прихований рівень із титрів.
- [Wikipedia](https://en.wikipedia.org/wiki/Inbento) — Afterburn, 7Levels, Unity, платформи, рецензії.
- [Russell Troxel](https://russelltroxel.com/writing/2020/3/19/inbento-review) — 3×3 → 4×3, 1–5 шматків, шматки 1–3 клітини, накривання, swap / copy / scoop, undo, 14 × 9.
- [Vooks](https://vooks.net/inbento-switch-review) — модифікатори повертають і копіюють, 127 рівнів, тач + стіки, мобільний реліз вересня 2019.
- [TheXboxHub](https://www.thexboxhub.com/inbento-review/) — розрізання, шматки без повороту, дублювання, обмін; ≤6–7 ходів на пазл.
- [148Apps](http://www.148apps.com/inbento/inbento-review/) — блоки виймання і копіювання, undo тапом.

## Непевне
- (?) Точні назви й поведінка дій: «scoop» (Troxel) = «take out» (відгук) = «cut» (TheXboxHub)? Чи вийняте повертається в лоток як фігура тієї ж форми.
- (?) Чи кожна клітина справді тримає стос шарів (виймання відкриває нижній) чи покладене просто стирає попереднє — відгуки кажуть і «зникає», і «last in, first out».
- (?) Чи треба використати всі шматки лотка; що за новий тип плитки в розділі 13.
- (?) Дата PC-релізу в Steam (на сторінці — 3 вересня 2019, як мобільний); inbento 2 — згадується в пошуку, не перевірено.
