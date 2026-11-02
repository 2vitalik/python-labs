---
title: Hanano Puzzle (ハナノパズル)
slug: hanano-puzzle
family: thinky
also: [push-slide]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2011
platforms: [PC (Windows)]
links:
  - {kind: other, url: "https://arxiv.org/html/2205.03400v3", best: true, note: "Chavrimootoo «Defying Gravity»: найточніший опис правил — стрілки, розквіт, квітка штовхає, обмін блоків, гравітація, з малюнками"}
  - {kind: official, url: "https://qrostar.net/hanano/", note: "офіційна сторінка (EN): безкоштовна збірка для Windows, hanano1000.zip"}
  - {kind: official, url: "https://qrostar.jp/hanano/", note: "японська сторінка; радить Hanano Puzzle 2 як трохи легшу"}
  - {kind: official, url: "https://qrostar.net/hanano2/", note: "Hanano Puzzle 2 — продовження"}
  - {kind: other, url: "https://arxiv.org/html/2601.08057v2", note: "«Carrying is Hard»: що саме в Hanano дає PSPACE-складність — блоки «носять» один одного й каскади розквіту"}
  - {kind: other, url: "https://arxiv.org/html/2501.12282v2", note: "Crabtree & Mitsou: Hanano NP-складна навіть з однією обмеженою стороною поля"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Hanano+Puzzle+gameplay", note: "пошук; проходження"}
stage: v1
coverage: 70
mechanics: [cell-click, gravity-fall, multi-cell-size, impassable-cells, orientation-state, completion-detection, sequential-levels, level-select, movement-animation, level-solver, +undo-redo, +bloom-on-contact, +growth-push, +swap-adjacent, +chain-reaction, +one-shot-state]
proposes: ["+trigger:input", "+trigger:adjacent", "+trigger:after", "+cond:same", "+cond:free", "+cond:state", "+cond:supported", "+effect:move", "+effect:swap", "+effect:fall", "+effect:grow", "+effect:spawn_at", "+effect:set_state", "+effect:push", "+role:tile", "+feature:undo", "+axis:undo"]
author: opus
date: 2026-11-02
---

# Hanano Puzzle — бутони розквітають, коли торкаються квітки свого кольору; нова квітка росте, штовхає сусідів і будить наступні бутони

## Суть
Поле збоку з гравітацією: кольорові блоки-бутони (червоні, сині, жовті) зі стрілкою на одній грані, сірі блоки-вантажі й нерухомі платформи з квітками. Гравець зсуває блоки на одну клітину ліворуч/праворуч або міняє місцями два сусідні вузькі блоки. Коли бутон торкається боком квітки свого кольору — **розквітає**: з грані зі стрілкою виростає нова квітка, прикріплена до блока, яка може штовхнути інші блоки і сама розбудити бутон того ж кольору (ланцюг). Мета — розквітнути всі кольорові блоки. Ядро — ріст тіла на контакт і каскади, які гравець запускає, але не контролює повністю.

## Поле і час
- Квадратна сітка «збоку» n×m; нерухомі сірі блоки (стіни/платформи), рухомі сірі блоки довільної форми, кольорові блоки 1×1, квітки 1×1, порожні клітини.
- Хід = один зсув / обмін → гравітація (усе без опори падає за один крок) → розквіти й каскади → гравітація…
- Квітка не має власної опори: вона прикріплена до блока чи платформи й рухається лише з ним. Квітка на нерухомому блоці не рухається ніколи.
- Ні часу, ні випадковості; повна інформація. Складність — PSPACE-повна (Chavrimootoo 2022), NP-складна вже з одним кольором (Liu & Yang 2019).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кольоровий блок (бутон) | tile | колір ∈ {red, blue, yellow}; стрілка ∈ {↑,↓,←,→}; стан bloomed | зсувається на 1 ліворуч/праворуч у порожнечу; падає; розквітає раз |
| Квітка | object | колір; прикріплена до блока/платформи | нерухома сама; будить бутони свого кольору, що торкаються ребром |
| Розквітлий блок | tile | блок + квітка як одне тіло (?) | рухається разом із квіткою; більше не розквітає; дотик до нього нічого не робить |
| Рухомий сірий блок | object | довільна форма | рухається й падає, не розквітає — вантаж, опора, клин |
| Нерухомий сірий блок | static | довільна форма; може нести квітки | стіна/платформа, опора |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, block, dir∈{left,right})` → ЯКЩО `free(cell_beside)` (або клітина зайнята тим самим блоком) → ТО `move(block, dir)`; інакше `block`. Блоки не штовхають інших.
- КОЛИ `input(swap, a, b)` → ЯКЩО `adjacent(a, b)` горизонтально і обидва шириною 1, а вищий поміщається на новому місці → ТО `swap(a, b)`.
- КОЛИ блок, що тримав інший, зсунуто → ТО верхній **лишається** на місці (нема перенесення) і `fall`, якщо втратив опору.
- КОЛИ `after(move|swap|bloom)` → ЯКЩО `not supported(x)` → ТО `fall(x)` до опори (рухомі блоки разом із прикріпленими квітками).
- КОЛИ `adjacent(bud, flower)` (спільне ребро) → ЯКЩО `same(bud, flower, color)` і `not state(bud, bloomed)` → ТО спроба розквіту:
  - ЯКЩО `free(cell_at_arrow)` → ТО `spawn_at(flower, cell_at_arrow)`, `set_state(bud, bloomed)`.
  - ЯКЩО клітину займає блок → ТО квітка `push` його або зсувається сам бутон, якщо є куди; `custom: «немає зсуву — немає розквіту»`.
- КОЛИ нова квітка `adjacent` бутону свого кольору → ТО той розквітає в тому ж кроці — каскад (`trigger(rule)`).
- Розквіт одноразовий і незворотний (у правилах гри; undo гравця — окремо).
- КОЛИ `all(colored_blocks, bloomed)` → ТО `win`.
- Поразки нема (глухий кут → undo/restart); рахунку нема.

## Керування і ввід
- Миша: клік по блоку → зсув ліворуч/праворуч; обмін двох сусідніх блоків — окрема дія (?). Точну схему кнопок не перевірено.
- Undo і restart рівня (?).

## Вікна, меню, HUD
- `level-select` — список/сітка рівнів з позначками (?).
- `game-screen` — поле збоку, номер рівня, `undo-button`, `restart-button` (?); анімація розквіту і падіння.
- `end-screen` — «Clear» → наступний рівень (?).
- Переходи: level-select → game-screen → (усе розквітло) → наступний / level-select.

## Фічі поза полем
- `undo` + `restart-level` (?); `levels-sequential`, кількість рівнів не перевірено (?).
- Безкоштовна гра для Windows, мови EN/JA; Hanano Puzzle 2 — окремий набір рівнів, автор радить його як трохи легший.
- Нема редактора, рахунку, підказок.

## Варіації й родичі
- Jelly no Puzzle (той самий автор): та сама фізика, але однакові кольори **зливаються** в одне тіло замість рости ([jelly-no-puzzle.md](jelly-no-puzzle.md)); через злиття там нема каскадів і «перенесень» (arXiv 2601.08057).
- Hanano Puzzle 2 — продовження з новими рівнями.
- Родичі за «ростом на контакт»: Snakebird (ріст від фрукта), A Good Snowman (ріст кулі на снігу), Baba Is You (`GROW`-подібні правила).
- **Осі варіацій:** що дає контакт — злиття / ріст / перетворення; куди росте — у напрямку стрілки / у бік контакту / усюди; ріст штовхає перешкоду чи блокується; розквіт одноразовий чи багаторазовий; каскад — у тому ж ході чи на наступному.

## Цікавинки для курсу
- Розквіт як тригер на суміжність + ріст тіла в заданому напрямку — 🥉 (сутність з орієнтацією-стрілкою, мінімум коду, багато наслідків).
- Каскад розквітів у межах одного ходу (черга подій до спокою) — 🥈 (порядок обробки, черга/BFS по подіях, повторна гравітація).
- Ріст, що штовхає блок або зсуває сам бутон, з відмовою, якщо зсуву нема — 🥈 (вибір, хто рухається, і відкат).
- Обмін двох вузьких блоків з перевіркою висоти — 📎.
- Розвʼязувач BFS для малих рівнів — 🥇 (PSPACE-повна гра; канонічний стан + памʼять відвіданих).

## Мапа на каталог
- Є: `cell-click` ↔ клік по блоку; `gravity-fall` ↔ падіння; `multi-cell-size` ↔ сірі блоки довільної форми; `impassable-cells` ↔ платформи; `orientation-state` ↔ стрілка бутона (наближено: тут орієнтація не змінюється); `completion-detection` ↔ усе розквітло; `sequential-levels` + `level-select`; `movement-animation`; `level-solver`.
- **Нема** → пропозиції карток:
  - `+undo-redo` «Undo ходів у грі» · game-logic/flow · 📎.
  - `+bloom-on-contact` «Ріст на контакт з однаковим» · entities/interact · 🥉 · слот {dir: arrow|contact|all} — бутон + квітка.
  - `+growth-push` «Ріст штовхає перешкоду або власника» · entities/legality · 🥈 — дитина `push-object`.
  - `+swap-adjacent` «Обмін двох сусідніх обʼєктів» · entities/move · 📎 — також у match-3 (Bejeweled).
  - `+chain-reaction` «Каскад подій у межах ходу» · game-logic/flow · 🥈 — узагальнення `chain-detonation` не лише для бомб.
  - `+one-shot-state` «Незворотний одноразовий стан (розквіт, активовано)» · entities/state · 🌱.

## Пропозиції до словників
- `+trigger:input`; `+trigger:adjacent` — бутон торкнувся квітки ребром (без спільної клітини); `+trigger:after` — каскад.
- `+cond:same(bud, flower, color)`; `+cond:free(cell_at_arrow)`; `+cond:state(bud, bloomed)`; `+cond:supported`.
- `+effect:move`, `+effect:swap`, `+effect:fall`, `+effect:grow` (тіло +1 клітина в напрямку стрілки), `+effect:spawn_at`, `+effect:set_state`; `push` тут — від росту, не від руху гравця.
- `+role:tile` — бутон із кольором і стрілкою.
- `+feature:undo`; `+axis:undo`.

## Джерела
- ⭐ [Chavrimootoo, «Defying Gravity: The Complexity of the Hanano Puzzle»](https://arxiv.org/html/2205.03400v3) — формальні правила: типи блоків, рух, обмін, гравітація, розквіт зі стрілкою, «no shift — no bloom», каскади, одноразовість; посилається на сайт гри 2011 р.
- [Qrostar: Hanano Puzzle (EN)](https://qrostar.net/hanano/) · [JP](https://qrostar.jp/hanano/) · [Hanano Puzzle 2](https://qrostar.net/hanano2/) — завантаження для Windows.
- [«Carrying is Hard», arXiv 2601.08057](https://arxiv.org/html/2601.08057v2) — верхній блок не їде з нижнім; блоки незалежні, тому «носять» одне одного ходами; квітка штовхає, якщо є місце.
- [Crabtree & Mitsou, arXiv 2501.12282](https://arxiv.org/html/2501.12282v2) — коротко правила й складність з обмеженнями.
- [YouTube: пошук «Hanano Puzzle gameplay»](https://www.youtube.com/results?search_query=Hanano+Puzzle+gameplay).

## Непевне
- (?) Хто саме зсувається, коли квітка впирається в блок (перешкода чи сам бутон) — пріоритет у статтях не уточнено.
- (?) Чи блок і його квітка рухаються як одне тіло з точки зору зіткнень (ймовірно так — квітка прикріплена).
- (?) Схема керування мишею, наявність undo, кількість рівнів обох частин, рік Hanano Puzzle 2.
- (?) Рік 2011 — з бібліографії статті Chavrimootoo, не з сайту автора.
