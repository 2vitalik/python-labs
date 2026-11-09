---
title: CIPHER ZERO
slug: cipher-zero
aka: [Cipher Zero]
family: thinky
also: [pencil-logic]
klass: puzzle
axes:
  field: graph
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2025
platforms: [PC, Mac, Linux, Steam Deck]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1332180/CIPHER_ZERO/", best: true, note: "ядро словами розробників: дві дії — перемкнути клітинку і перевірити розвʼязок; 300+ пазлів, локації, що змінюються"}
  - {kind: other, url: "https://steamcommunity.com/app/1332180/discussions/0/596281215576813549/", note: "обговорення «Stuck in Road 2»: правила дротів, секторів і зірок (дерево з N тупиками)"}
  - {kind: other, url: "https://steamcommunity.com/app/1332180/discussions/0/591810592556272848/", note: "«Dots in the City»: гліф-фігура з повних/порожніх квадратиків, що має «влізти» в розвʼязок"}
  - {kind: other, url: "https://steamcommunity.com/app/1332180/discussions/0/596281215576948057/", note: "«Undo function»: розробник про прапорці трьох кольорів (ПКМ / Shift), undo нема"}
  - {kind: other, url: "https://steamcommunity.com/app/1332180/reviews/?browsefilter=toprated", note: "відгуки: перевірка показує стан кожного гліфа, 373 рівні, лінійна прогресія, дзеркальні шляхи наприкінці"}
  - {kind: other, url: "http://www.thegeeklygrind.com/all-posts/cipher-zero-review", note: "огляд: як Picross, але підказки — символи; нові форми плиток (прямокутники, гекси)"}
  - {kind: other, url: "https://blog.zarfhome.com/2025/07/summer-puzzle-games", note: "Zarf: «Witness-like», починається з nonogram-подібних пазлів, 5 розділів"}
  - {kind: other, url: "https://ldjam.com/events/ludum-dare/45/cipher", note: "прототип CIPHER, Ludum Dare 45 (2019)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Cipher+Zero+Zapdot+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [cell-click, keyboard-controls, satisfy-constraints, completion-detection, markup-validity, connectivity-check, dot-mark, sequential-levels, level-unlock, level-select, world-map, save-progress, settings-window, controls-remap, game-screen, background-music, sound-effects, event-effects, +tile-toggle, +submit-check, +per-rule-feedback, +rule-teaching-by-example, +polyomino-fit, +tree-leaf-count, +wire-path-glyph, +symmetry-path, +mixed-cell-shapes, +reactive-music]
proposes: ["+trigger:submit", "+cond:leaf_count", "+effect:feedback_per_rule", "+ui:submit-button", "+ui:flag-colors", "+feature:reactive-music", "+axis:rules", "+card:per-rule-feedback", "+card:tree-leaf-count"]
author: opus
date: 2026-11-09
---

# CIPHER ZERO — увімкни клітинки й натисни «перевірити»: що означає кожен гліф, вгадуєш із того, які з них загорілись червоним

## Суть
Мінімалістична логічна гра студії Zapdot (повна версія джемової CIPHER з Ludum Dare 45). Є лише **дві дії**: перемкнути клітинку (увімкнено/вимкнено) і **перевірити розвʼязок**. На полі стоять гліфи без жодного пояснення; кожен — правило про увімкнені клітинки навколо чи в його області. Після перевірки гра показує, який гліф виконано, а який ні, — так гравець виводить правила. Далі гра стає класичним nonogram-подібним пазлом із наростаючим набором гліфів і форм сітки.

## Поле і час
- Поле — невеликий набір плиток довільної форми: спершу квадрати в нерівній сітці, далі прямокутники, «зчеплені» форми й шестикутники (суміжність нестандартна → `graph`).
- Плитка має два стани: увімкнена (світла) / вимкнена; плюс невидимий для перевірки прапорець одного з трьох кольорів.
- Гліфи стоять на плитках або поза сіткою (риски біля рядків, фігурки з квадратиків, зірки, трикутники-сектори, кінці «дроту»).
- Часу нема; пазл статичний. Кожна локація — пейзаж, що змінюється з прогресом; музика реагує на дії.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка | tile | on / off; форма (квадрат, прямокутник, гекс) | клік перемикає стан |
| Прапорець | mark | 3 кольори | нотатка гравця; на перевірку не впливає, лишається після перемикання |
| Риска біля рядка/стовпця | mark | — | перший гліф; nonogram-подібна підказка про увімкнені в лінії (?) |
| Гліф-фігура (повні й порожні квадратики) | mark | форма | така конфігурація on/off має «влізти» десь у розвʼязок, як фігура Tetris |
| Гліф-зірка (3, 4, 5 променів) | mark | N | його область — дерево без 2×2 з рівно N тупиками; дві зірки не діляться одною областю |
| Дріт (кінці лінії) | mark | — | увесь шлях від початку до кінця має бути увімкнений |
| Гліф-сектор (трикутники) | zone | — | дивиться на площу свого сектора незалежно від кольору клітин (?) |
| Гліфи «вартістю N клітин» | mark | N | рахують площу; на великих полях сума гліфів = кількість клітин (з відгуку) |
| Дзеркальний шлях | mark | — | у останніх світах шлях малюється симетрично (?) |
| Кнопка «Submit Solution» | switch | — | запускає перевірку всіх гліфів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, tile)` → ТО `set_state(tile, toggle)` (`custom: «on ↔ off»`).
- КОЛИ `input(flag, tile)` → ТО `mark(tile, color)`; повторне — наступний колір / зняти (?).
- КОЛИ `input(reset)` → ТО `custom: «усі плитки вимкнено»` (Tab або R), прапорці лишаються.
- КОЛИ `input(submit)` → ТО `custom: «перевірити кожен гліф окремо й показати, які виконано, а які ні»` (`+effect:feedback_per_rule`), `counter(fails, +1)` при невдачі.
- КОЛИ `all_constraints_met` → ТО `win`, `animate(solved)`, `unlock(next_level)`, `sound(chord)`.
- КОЛИ `constraint_broken(glyph)` → ТО `custom: «гліф позначено невиконаним»`; поле лишається як було.
- Гліф-фігура: ЯКЩО `fits(shape, cells)` для `custom: «повні квадратики = on, порожні = off, у будь-якому місці поля»` → виконано (поворот фігури — (?)).
- Гліф-зірка: ЯКЩО `connected(region)` і `no_2x2(region)` і `custom: «рівно N тупиків»` (`+cond:leaf_count`) і `custom: «одна зірка на область»` → виконано.
- Дріт: ЯКЩО `path_exists(start, end)` по увімкнених і `custom: «увесь дріт увімкнений»` → виконано.
- Сектор: ЯКЩО `custom: «площа сектора відповідає гліфу незалежно від кольору клітин»` → виконано (?).
- Перемога: усі гліфи виконано; розвʼязків може бути кілька — будь-який зараховується. Поразки нема.

## Керування і ввід
- Миша: ЛКМ — перемкнути плитку; ПКМ — прапорець; кнопка внизу — Submit Solution.
- Клавіатура: курсор по плитках, Shift (лівий/правий) — прапорець, Tab / R — скинути сітку; повне перепризначення клавіш.
- Геймпад (повна підтримка), лише миша, лише клавіатура, лише тач — окремі прапорці Steam; без таймінгу.

## Вікна, меню, HUD
- `main-menu` (?) → вибір локації.
- `level-select` / `map-window`: пейзаж локації з ланцюжком прямокутників-рівнів, зʼєднаних лінією; пройдені світяться (скриншот Steam); 30 с бездіяльності тут — досягнення.
- `game-screen`: поле плиток з гліфами на тлі пейзажу; угорі — смуга прогресу локації; унизу — кнопка Submit Solution з підказкою вводу і стрілка «назад»; після перевірки — підсвітка гліфів (`+ui:submit-button`, `+ui:flag-colors`).
- `settings-window`: System (V-Sync), Controls (перепризначення, «Reset Keyboard Configuration»), гучність, кольорові альтернативи, 14 мов.
- Переходи: розвʼязано → анімація, світ змінюється → наступний рівень у ланцюжку.

## Фічі поза полем
- `levels-sequential` строго лінійно: наступний рівень відкривається лише після попереднього; пропусків, підказок і undo нема (гравці просили undo — розробник відповідав про прапорці).
- `+feature:reactive-music` — саундтрек кожної локації нарощує інструменти з прогресом і реагує на кліки.
- `achievements`: пройти все, 300 невдалих перевірок (у v1.0.4 спрощено), 250 прапорців, 30 с на екрані вибору.
- `autosave` (Save Anytime), хмарні сейви, перенесення сейва з демо; `colorblind-palette` (Color Alternatives), `remap-controls`, `localization` на 14 мов.

## Варіації й родичі
- CIPHER (Ludum Dare 45, 2019) — прототип за 72 години; CIPHER ZERO розширює його до 373 пазлів і кількох локацій.
- `games/thinky/taiji-witness-panels.md` — той самий жанр «гліф на сітці → невимовлене правило»; у Taiji перевірка мовчить, тут показує кожен гліф.
- `games/thinky/understand.md` — схожий відгук «по кожному правилу»; `games/thinky/islands-of-insight.md` — сітки з правилами у відкритому світі.
- Picross / nonogram — перший гліф і загальна механіка «увімкни клітинки за підказками».
- **Осі варіацій:** що каже перевірка — лише «так/ні» / кожен гліф (тут) / нічого; скільки розвʼязків — один / будь-який, що задовольняє; форма сітки — квадрат / змішані плитки / гекс.

## Цікавинки для курсу
- Перемикач клітинки + перевірка всіх правил із відгуком «по гліфу» — 🥉.
- Зірка: перевірити, що область — дерево без 2×2, і порахувати тупики (BFS + ступені вершин) — 🥈.
- Гліф-фігура: пошук місця, куди вкладається шаблон on/off (перебір зсувів і поворотів) — 🥉.
- Поле з плиток різної форми як граф суміжності — 🥈.
- Прапорці трьох кольорів, що не впливають на перевірку — 🌱.
- Музика, що нарощує шари з прогресом — 📎.

## Мапа на каталог
- Є: `cell-click`, `keyboard-controls`; `satisfy-constraints`, `completion-detection`, `markup-validity` ↔ перевірка гліфів; `connectivity-check` ↔ дріт і зірка; `dot-mark` ↔ кольорові прапорці; `sequential-levels`, `level-unlock`, `level-select`, `world-map` ↔ ланцюжок рівнів на пейзажі; `save-progress`; `settings-window`, `controls-remap`, `game-screen`; `background-music`, `sound-effects`, `event-effects`.
- **Нема** → пропозиції карток:
  - `+tile-toggle` «Клітинка on/off як єдиний хід» · interface/input · 🌱.
  - `+submit-check` «Явна кнопка перевірки замість автоперевірки» · game-logic/constraints · 🌱.
  - `+per-rule-feedback` «Перевірка показує стан кожного правила» · game-logic/constraints · 📎.
  - `+tree-leaf-count` «Область — дерево з N тупиками» · game-logic/constraints · 🥈.
  - `+polyomino-fit` «Шаблон on/off має вкластися в поле» · game-logic/constraints · 🥉.
  - `+wire-path-glyph` «Шлях між двома кінцями має бути увімкнений» · game-logic/constraints · 📎.
  - `+symmetry-path` «Дзеркальний шлях» · game-logic/constraints · 📎.
  - `+mixed-cell-shapes` «Поле з плиток різних форм (граф)» · levels/format · 🥈.
  - `+reactive-music` «Музика реагує на прогрес і дії» · interface/sound · 📎.

## Пропозиції до словників
- `+trigger:submit` — гравець натиснув «перевірити» (CIPHER ZERO; на відміну від `all_constraints_met`, перевірка лише на запит).
- `+cond:leaf_count(region, n)` — у дереві-області рівно n тупиків.
- `+effect:feedback_per_rule` — показати стан кожного правила/гліфа окремо.
- `+ui:submit-button` — кнопка «Submit Solution»; `+ui:flag-colors` — прапорці кількох кольорів.
- `+feature:reactive-music` — музика нарощує шари з прогресом.
- `+axis:rules` — правила `given` / `discovered` (тут discovered).
- `+card:per-rule-feedback`, `+card:tree-leaf-count` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: CIPHER ZERO](https://store.steampowered.com/app/1332180/CIPHER_ZERO/) — «You have two actions: Toggle a tile on or off. Check your solution»; 300+ пазлів, локації, реактивний саундтрек; прапорці доступності; 22.07.2025.
- [Steam-обговорення «Stuck in Road 2»](https://steamcommunity.com/app/1332180/discussions/0/596281215576813549/) — дріт мусить бути увімкнений повністю; сектор дивиться на площу без огляду на колір; зірка = дерево без 2×2 з N тупиками.
- [«Dots in the City»](https://steamcommunity.com/app/1332180/discussions/0/591810592556272848/) — фігура з повних/порожніх квадратиків «Tetris-ується» в розвʼязок.
- [«Undo function»](https://steamcommunity.com/app/1332180/discussions/0/596281215576948057/) — прапорці трьох кольорів, ПКМ / Shift; undo нема.
- [Відгуки Steam](https://steamcommunity.com/app/1332180/reviews/?browsefilter=toprated) — перевірка по кожному гліфу, 373 рівні, лінійність, кілька розвʼязків, дзеркальні шляхи, Tab скидає сітку.
- [The Geekly Grind](http://www.thegeeklygrind.com/all-posts/cipher-zero-review) — «як Picross, але символи»; нові форми плиток; локації Farmland, Lake, Powerplant.
- [Zarf: Summer puzzle games](https://blog.zarfhome.com/2025/07/summer-puzzle-games) — nonogram-подібний старт, 5 розділів.
- [Ludum Dare 45: CIPHER](https://ldjam.com/events/ludum-dare/45/cipher) — прототип 2019 (через API ldjam: автори Jamie McLean, Ben Wu, Jordan Toth).
- Новини Steam (v1.0.3, v1.0.4) — R для скидання сітки, V-Sync, досягнення за невдалі перевірки.

## Непевне
- (?) Точне правило першого гліфа-риски (кількість увімкнених у лінії?) — лише зі скриншота й порівнянь із nonogram.
- (?) Правило гліфа-сектора (трикутники) — гравці описують по-різному; певно лише, що колір клітин не важить.
- (?) Чи можна повертати гліф-фігуру — з відгуку «shape which can be set in any rotation», не перевірено.
- (?) Локації: Farmland, Lake, Powerplant, Road, Suburbs, City, Moon — з підписів і обговорень; поділ на 5 розділів (Zarf) з ними не звірено.
- (?) 373 рівні — з двох відгуків/гайдів; Steam каже «300+».
- (?) Дзеркальні шляхи останніх світів — лише з одного відгуку.
