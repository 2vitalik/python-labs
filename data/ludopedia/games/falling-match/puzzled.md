---
title: Puzzled (Joy Joy Kid)
slug: puzzled
aka: [Joy Joy Kid, ジョイジョイキッド, ACA NEOGEO PUZZLED]
family: falling-match
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: state
year: 1990
platforms: [arcade (Neo Geo MVS), Neo Geo AES, Neo Geo CD, mobile, Wii VC, Neo Geo X, PS4, Xbox One, Switch, Windows, iOS, Android]
links:
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ジョイジョイキッド", best: true, note: "12 стовпців, тетроміно, куля/дирижабль знизу, поблокове падіння після зчищення, типи блоків, блоки на 3 удари, Lightning Ball 3 розмірів, 6 етапів × 10 поверхів, другий персонаж"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Puzzled_(video_game)", note: "мета — вивільнити кулю нагору, роботи, регенерація, золоті блоки, L-Ball, 2P одночасно, порти"}
  - {kind: other, url: "https://neo-geo.com/reviews/neo-reviews/puzzled/puzzled.html", note: "огляд: куля спливає в розчищений прохід, золоті блоки на 3 зчищення, L-Ball після 1/3 шкали на B, поворот в один бік"}
  - {kind: other, url: "https://neo-geo.com/reviews/neo-reviews/puzzled/puzzled1.html", note: "огляд, ч. 2: блоки, що розпадаються на частини й дають ланцюг"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=puzzled+neo+geo+joy+joy+kid+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [gravity-fall, multi-cell-size, piece-rotate-flip, keyboard-controls, chain-reaction, destructible-blocks, impassable-cells, explode-area, sequential-levels, character-select, reach-exit, simultaneous-versus, enemy-patrol, +line-clear, +cascade-gravity, +multi-hit-block, +fixed-vs-movable, +regen-block, +free-the-target, +special-meter-blast]
proposes: ["+ui:special-meter", "+card:free-the-target", "+card:regen-block", "+card:special-meter-blast"]
author: opus
date: 2026-11-09
---

# Puzzled (Joy Joy Kid) — Tetris навпаки: зчищай ряди не заради очок, а щоб прорубати прохід повітряній кулі з дна

## Суть
Падають тетроміно, повний ряд зникає — як у Tetris; але на дні кожного «поверху» замурована повітряна куля (дирижабль) героя в заздалегідь викладеній кладці. Треба зчищати ряди так, щоб над кулею відкрився прохід: тоді вона спливає нагору, і поверх пройдено. Після зчищення кожен блок падає **окремо**, наскільки може (не цілими рядами, як у Tetris), тож виникають ланцюги; стартова кладка при цьому не падає. Заважають золоті блоки на 3 зчищення, блоки, що відновлюються, плаваючі міни/роботи, дроти під напругою й стіни; виручає Lightning Ball — вибух навколо кулі за накопичену шкалу.

## Поле і час
- Ширина 12 стовпців (у Tetris — 10); висота — (?).
- Шари: стартова кладка рівня (фіксовані блоки) + покладені тетроміно + рухомі вороги (міни/роботи) + куля героя на дні.
- Real-time: тетроміно падає з темпом; поверх — окремий пазл, 10 поверхів = етап, 6 етапів = 60 поверхів на персонажа.
- Два гравці одночасно, кожен на своєму полі (взаємодії між полями майже нема); шкала L-Ball — у центрі екрана.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Тетроміно | player | 4 квадрати, орієнтація | зсув, поворот лише в один бік, падіння |
| Звичайний блок | tile | — | зникає у повному ряду; після зчищення падає окремо до упору |
| Фіксований блок кладки | static | — | частина стартового рівня; не падає після зчищень |
| Золотий блок | tile | 3 удари | зникає лише з третім зчищенням свого ряду |
| Відновлюваний блок (再生ブロック) | tile | — | після зчищення зʼявляється знову |
| Незнищенний блок / стіна | static | — | не зникає ніколи |
| Плаваюча міна / робот | enemy | — | плаває в полі й атакує кулю |
| Дріт під напругою (高圧線) | hazard | — | перешкода; поведінка — (?) |
| Повітряна куля / дирижабль | object | позиція на дні | замурована; відкрився прохід — спливає нагору |
| Lightning Ball | projectile | розмір 1–3 за шкалою | вибух навколо кулі, руйнує блоки поруч |
| Бог-охоронець | neutral | ключ | кожні 10 поверхів; дає ключ при дотику або після бонусної стрибкової проби |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move|rotate|drop)` → ЯКЩО `free(cells)` → ТО `move(piece, dir)` / `rotate(piece, 90)` (лише в один бік); інакше `block`.
- КОЛИ `locked(piece)` → ЯКЩО `pattern(row_full)` (12 клітин) → ТО `clear(row)`, `counter(lball_meter, +n)`.
- КОЛИ `after(clear)` → ЯКЩО `not cell(block, fixed)` → ТО `fall(each_block)` — кожен блок окремо, «наскільки може».
- КОЛИ `settled` → ЯКЩО `pattern(row_full)` → ТО `clear(row)` (ланцюг).
- КОЛИ `after(clear)` → ЯКЩО `cell(x, gold)` → ТО `damage(1)`; КОЛИ `hp_zero(gold)` → ТО `disappear`; на першому й другому зчищенні блок лишається.
- КОЛИ `after(clear)` → ЯКЩО `cell(x, regen)` → ТО `disappear`, потім `spawn_at(regen_block, same_cell)` (коли — (?)).
- КОЛИ `after(clear)` → ЯКЩО `cell(x, wall)` → ТО `block` — стіна лишається.
- КОЛИ `tick` → ТО `custom: «міна/робот плаває полем»`; КОЛИ `contact(enemy, balloon)` → ТО `custom: «заважає кулі»` (?).
- КОЛИ `custom: «над кулею відкрився прохід до верху»` → ЯКЩО `path_exists(balloon, top)` → ТО `move(balloon, up)` до виходу.
- КОЛИ `reach(balloon, top)` → ТО `win`, `next_level`.
- КОЛИ `input(B)` → ЯКЩО `counter(lball_meter, ≥, 1/3)` → ТО `explode(around_balloon, size(lball_meter))` (3 розміри: що повніша шкала, то більший), `counter(lball_meter, 0)`.
- КОЛИ `reach(stack, top)` → ТО `game_over`.
- КОЛИ `counter(floor, ==, 10·k)` → ТО `custom: «бог-охоронець: ключ дотиком або після бонусної проби зі стрибками»`, `unlock(next_section)`.
- КОЛИ `custom: «пройдено 60 поверхів одним персонажем»` → ТО `custom: «ще 60 поверхів іншим персонажем; кладка інша й важча»`; разом 120.

## Керування і ввід
- Джойстик — зсув і прискорення падіння тетроміно; кнопка — поворот (лише в один бік, за оглядом).
- B — випустити Lightning Ball (доступно після 1/3 шкали).
- Другий гравець — свій джойстик і своє поле, одночасна гра.

## Вікна, меню, HUD
- `attract-demo` (аркада) (?) → `character-select`: Rad (дирижабль-акула) або Am (повітряна куля); від вибору трохи змінюються кладки.
- `game-screen`: поле 12 у ширину з кулею на дні, `custom: «шкала Lightning Ball у центрі»` (`+ui:special-meter`), `level-number` (поверх), `score` (?), `next-piece-preview` (?).
- `custom-window` — бонусна проба бога-охоронця зі стрибками кожні 10 поверхів.
- `game-over-continue` (аркада) (?) · `end-screen` — кінцівка після 60 / 120 поверхів.
- Переходи: character-select → поверх → поверх … → бог (кожні 10) → наступна секція → фінал → другий персонаж.

## Фічі поза полем
- `levels-sequential`: 6 етапів × 10 поверхів, потім ще 60 за іншого героя (усього 120).
- `local-multiplayer` — 2 гравці одночасно (рецензенти дорікали, що поля майже не взаємодіють).
- Домашня версія — без налаштування складності; ACA-перевидання Hamster (PS4, Xbox One, Switch, Windows, мобільні) з режимами Arcade Archives (?).

## Варіації й родичі
- Аркада Neo Geo MVS (1990) → Neo Geo AES (1991), Neo Geo CD (1994), мобільні (2005), Wii VC (2011), Neo Geo X (2012), ACA NEOGEO (2017+), Neo Geo mini (2018), iOS/Android (2022), Arcade Archives NEOGEO Selection Vol.4 (2025).
- Родичі в корпусі: `tetris` (ряди, але падіння цілими рядами), `quarth` (тетроміно як «снаряди» проти кладки), `bombliss` (кладка й бомби в склянці), `dr-mario` (стартова кладка-ціль), `tetris-plus` (Puzzle-режим: професор має спуститися крізь стек на дно — дзеркальна мета, найближчий родич).
- **Осі варіацій**: гравітація після зчищення (цілими рядами — Tetris / кожен блок окремо — Puzzled / липкі групи) · мета (очки / рядки / вивільнити обʼєкт) · міцність блоків (1 / 3 зчищення / незнищенний / відновлюваний) · спецудар (нема / шкала з розміром за повнотою).

## Цікавинки для курсу
- Поблокова гравітація після зчищення ряду з виключенням для фіксованої кладки + повторна перевірка рядів — 📎 (і звідси ланцюги).
- Мета «прохід над кулею до верху» — перевірка шляху flood fill щокадру — 📎.
- Блоки з міцністю 3 і блоки, що відновлюються — 🌱 кожен, разом 📎.
- Шкала спецудару з трьома розмірами вибуху за повнотою — 🌱.
- Плаваючі вороги всередині стеку, що атакують ціль — 🥉 (рух крізь порожнечі поля, зіткнення з падаючими фігурами).
- Генерація/редактор поверхів «кладка + куля», перевірка, що розвʼязно — 🥇.

## Мапа на каталог
- Є: `gravity-fall` + `multi-cell-size` + `piece-rotate-flip` ↔ тетроміно; `keyboard-controls` ↔ джойстик/кнопки; `chain-reaction` ↔ ланцюги після поблокового падіння; `destructible-blocks` ↔ кладка; `impassable-cells` ↔ стіни; `explode-area` ↔ Lightning Ball; `reach-exit` ↔ куля дісталась верху; `sequential-levels` ↔ 120 поверхів; `character-select` ↔ Rad/Am; `simultaneous-versus` ↔ два поля одночасно (без атак — найближча картка); `enemy-patrol` ↔ міни/роботи (?).
- **Нема** → пропозиції карток:
  - `+line-clear` (спільна з Tetris) — повний ряд зникає.
  - `+cascade-gravity` (спільна) — тут поблоково.
  - `+multi-hit-block` (спільна з Crystal Mines II, Megapanel) — золотий блок, 3 зчищення.
  - `+fixed-vs-movable` (спільна) — кладка не падає, покладене падає.
  - `+regen-block` «Блок відновлюється після зчищення» · entities/state · 🌱 · слот {delay}.
  - `+free-the-target` «Перемога — вивільнити обʼєкт: прохід до краю» · game-logic/win · 📎 · слот {target: top|exit}.
  - `+special-meter-blast` «Шкала → вибух навколо точки з розміром за повнотою» · entities/combat · 🌱.

## Пропозиції до словників
- `+ui:special-meter` — шкала Lightning Ball (повтор з інших файлів).
- `+card:free-the-target`, `+card:regen-block`, `+card:special-meter-blast` — див. мапу.

## Джерела
- ⭐ [Wikipedia JA: ジョイジョイキッド](https://ja.wikipedia.org/wiki/ジョイジョイキッド) — 4-квадратні фігури, 12 стовпців, куля/дирижабль на дні, поблокове падіння й ланцюги, нерухома кладка, типи блоків (звичайний, золотий, відновлюваний, міна, дріт, стіна), «зникає з 3-го разу / ніколи», Lightning Ball 3 розмірів, 6×10 поверхів, другий персонаж, боги кожні 10 поверхів, усі видання.
- [Wikipedia EN: Puzzled](https://en.wikipedia.org/wiki/Puzzled_(video_game)) — прохід для кулі, роботи, регенерація, золоті блоки, L-Ball, 2P одночасно, порти.
- [Neo-Geo.com: Puzzled](https://neo-geo.com/reviews/neo-reviews/puzzled/puzzled.html) — куля спливає в розчищене, золоті блоки на 3 рази, шкала L-Ball (після 1/3 — B), поворот в один бік, 10 поверхів на ярус.
- [Neo-Geo.com: Puzzled, ч. 2](https://neo-geo.com/reviews/neo-reviews/puzzled/puzzled1.html) — блоки розпадаються на частини й дають ланцюги.
- YouTube: пошук «puzzled neo geo joy joy kid gameplay».

## Непевне
- (?) Висота поля, наявність next-превʼю, очки — не знайдено.
- (?) Що саме роблять міни/роботи з кулею (сповільнюють, штовхають, забирають життя) і що робить дріт під напругою — джерела лише перелічують.
- (?) Коли відновлюється відновлюваний блок (таймер чи після кожного зчищення).
- (?) Чи блокує незнищенний блок зчищення ряду, у якому стоїть.
- (?) EN-вікі: «60 пазлів», JA: 60 поверхів на персонажа, 120 разом — беру JA.
- (?) Розробник: EN-вікі — SNK; на ACA-сторінку не дістався.
