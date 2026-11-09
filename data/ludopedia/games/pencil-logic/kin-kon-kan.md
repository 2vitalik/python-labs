---
title: Kin-Kon-Kan (キンコンカン)
slug: kin-kon-kan
aka: [Kinkonkan, キンコンカン, Кін-кон-кан]
family: pencil-logic
also: [connect-rotate]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: null
platforms: [paper, web]
links:
  - {kind: other, url: "https://www.janko.at/Raetsel/Kinkonkan/index.htm", best: true, note: "Janko: правила DE/EN, 170 пазлів грати в браузері"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/kinkonkan.js", note: "puzz.link/pzpr: правила EN/JP, Nikoli vol. 89, тести вводу, коди помилок"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json", note: "тексти кодів помилок (bkObjGe2.kinkonkan…)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=kinkonkan+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 70
mechanics: [markup-validity, completion-detection, satisfy-constraints, beam-tracing, mirror-reflect, cell-click, conflict-highlight, in-game-editor, editor-palette, import-open-formats, level-bank, undo-redo, +irregular-regions, +region-quota, +paired-beam-endpoints, +reflection-count-clue]
proposes: ["+role:clue-outside", "+cond:count_in", "+card:paired-beam-endpoints", "+card:reflection-count-clue"]
author: opus
date: 2026-11-09
---

# Kin-Kon-Kan — по одному дзеркалу в кожну кімнату так, щоб промінь з кожної літери вийшов у парній літері з потрібною кількістю відбиттів

## Суть
Поле поділене на кімнати; навколо поля стоять пари однакових літер, часто з числом. Гравець ставить у клітинки діагональні дзеркала (`/` або `\`), рівно одне в кожній кімнаті. Промінь, запущений від літери перпендикулярно до краю, відбивається від дзеркал під прямим кутом і мусить вийти біля другої такої ж літери, відбившись стільки разів, скільки каже число; кожне дзеркало має бути використане хоча б одним променем. Незвичне: зворотна задача до лазерних ігор — не прокласти промінь, а розставити дзеркала під задані траєкторії.

## Поле і час
- Прямокутна сітка, поділена товстими лініями на кімнати.
- Підказки — поза полем, на рамці: літера (пара входу/виходу) і необовʼязкове число відбиттів.
- Шари: кімнати й підказки (незмінні) · дзеркала гравця · допоміжні мітки «тут дзеркала нема» (?).
- Час статичний; хід = поставити / змінити / стерти дзеркало. Промінь — не сутність гравця, а обчислювана траєкторія.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кімната | zone | межі | містить рівно одне дзеркало |
| Клітинка | terrain | — | порожня — промінь іде крізь неї прямо |
| Дзеркало | mark | `/` або `\` | ставить гравець; відбиває промінь на 90° (?: з обох боків) |
| Літера на рамці | source | літера, позиція | промінь входить у поле перпендикулярно краю; виходить біля парної літери |
| Число біля літери | mark | N | кількість відбиттів цього променя |
| Промінь | projectile | траєкторія | прямо крізь порожні, відбиття на дзеркалах, до виходу за рамку |
| Мітка «нема дзеркала» | mark | — | допоміжна точка гравця (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, cell)` → ТО `custom: «циклічно: / → \ → порожньо»`; ліва і права кнопки — у протилежних напрямках (тести `leftx2…x4`, `rightx2`) (?).
- КОЛИ `contact(beam, mirror)` → ТО `bounce(beam)` + `counter(reflections, 1)`.
- КОЛИ `tick` (крок трасування) → ЯКЩО `not occupied(cell, mirror)` → ТО `move(beam, dir)` (промінь іде прямо до наступного дзеркала чи краю).
- КОЛИ `edge(beam)` → ЯКЩО `not same(exit_clue, entry_clue, letter)` → ТО `set_state(clue, error)` (pzpr `pairedLetterNe`: «Beam from a light doesn't reach its pair»).
- КОЛИ `edge(beam)` → ЯКЩО `not counter(reflections, =, n)` → ТО `set_state(clue, error)` (`pairedNumberNe`: «The number of reflections is wrong»).
- КОЛИ `constraint_broken(room_mirrors)` → ЯКЩО `count(mirror, >, 1)` у кімнаті (`+cond:count_in`) → ТО `set_state(room, error)` (`bkObjGe2`: «A room has more than one mirror»).
- КОЛИ `constraint_broken(room_mirrors)` → ЯКЩО `count(mirror, =, 0)` у кімнаті → ТО `set_state(room, error)` (`bkNoObj`).
- КОЛИ `constraint_broken(unused)` → ЯКЩО `custom: «жоден промінь не торкається дзеркала»` → ТО `set_state(mirror, error)` (`ceUnused`: «A mirror is unused»).
- КОЛИ `all_constraints_met` → ТО `win`.
- Дедукція «нуль відбиттів»: літера з числом 0 — промінь іде прямо, отже парна літера навпроти й на всьому ряду дзеркал нема.
- Дедукція «одне відбиття»: вхід і вихід на сусідніх сторонах рамки — дзеркало стоїть у перетині ряду входу й стовпця виходу, орієнтація визначена.
- Дедукція «кімната»: якщо в кімнаті лишилась одна клітинка, куди можна поставити дзеркало без зламу променів, — ставимо; решта клітинок кімнати порожні.
- Перемога: у кожній кімнаті одне дзеркало, кожен промінь зʼєднує свою пару літер з правильною кількістю відбиттів, кожне дзеркало використане. Поразки й рахунку нема.

## Керування і ввід
- puzz.link play: клік по клітинці перебирає стан дзеркала; повторні кліки (`leftx2`, `x3`, `x4`) — по колу; drag по ряду (`mouse,left, 1,1, 7,1`) — масова зміна (?).
- puzz.link edit: клавішами літера + число на клітинці рамки (`a,1`, `b,1`, `c,2`), `-` і пробіл — стерти; межі кімнат — drag (?).
- Цифрова версія: показ траєкторії променя по кліку на літеру був би природним, але в джерелах не бачив (?).

## Вікна, меню, HUD
- `game-screen`: сітка з кімнатами, рамка з літерами й числами, дзеркала, `conflict-highlight` для кімнати / дзеркала / літери з помилкою.
- puzz.link: перемикач play/edit, кнопка перевірки з текстом першої помилки, `settings-window`.
- `help-window` — правила (puzz.link, Janko).
- `puzzle-select` — 170 пазлів Janko.
- Переходи: edit → play; check → повідомлення.

## Фічі поза полем
- `auto-check` за кнопкою з кодами pzpr.
- `undo` / `redo`; `level-editor` + `share-code` (URL puzz.link).
- `puzzle-bank` Janko; генератора не бачив (?).

## Варіації й родичі
- У сімʼї: [Undead](undead.md) (дзеркала дано, рахується видимість монстрів), [Reflect Link](reflect-link.md) (трикутник-дзеркало як кут петлі), [Light Up](light-up.md) (промені ламп), [Star Battle](star-battle.md) (квота обʼєктів на регіон).
- Janko називає схожими Rifurekuta і Mirapu (?).
- Поза сімʼєю: Deflektor, Laser Tank, Khet (`connect-rotate` — прямі задачі з променем); Black Box (`hidden-deduction` — дзеркала-атоми сховані, промені — запити).
- **Осі варіацій**: дзеркала ставить гравець / дано · квота на кімнату (1 / N / без кімнат) · що каже підказка (пара + відбиття / лише пара / довжина) · типи дзеркал (діагональні / однобічні / подільники променя).

## Цікавинки для курсу
- Трасування променя по сітці з діагональними дзеркалами (таблиця «напрямок × тип дзеркала → новий напрямок») — 🌱.
- Валідатор: для кожної літери провести промінь, перевірити пару, кількість відбиттів, позначити використані дзеркала — 📎.
- Квота «рівно одне в кімнаті» — 🌱.
- Показ траєкторій усіх променів з підсвіткою помилкових — 📎.
- Розвʼязувач перебором з відсіканням по кімнатах — 🥉; генератор з унікальним розвʼязком — 🥇.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `beam-tracing`, `mirror-reflect` ↔ промінь і дзеркала · `cell-click` ↔ перебір дзеркала · `conflict-highlight` · `in-game-editor`, `editor-palette`, `import-open-formats` (puzz.link) · `level-bank` (Janko) · `undo-redo`.
- **Нема** → пропозиції карток:
  - `+irregular-regions`, `+region-quota` — повтори з Star Battle: рівно N обʼєктів у кожній області.
  - `+paired-beam-endpoints` «Промінь з мітки на рамці мусить вийти біля парної мітки» · game-logic/constraints · 📎 · слот {pairs: letters|colors}.
  - `+reflection-count-clue` «Число = кількість відбиттів променя» · game-logic/constraints · 🌱.

## Пропозиції до словників
- `+role:clue-outside` — повтор: підказка на рамці поза полем.
- `+cond:count_in` — повтор зі Star Battle: кількість сутностей виду в області.
- `+card:paired-beam-endpoints`, `+card:reflection-count-clue` — див. мапу.

## Джерела
- ⭐ [Janko: Kinkonkan](https://www.janko.at/Raetsel/Kinkonkan/index.htm) — правила DE/EN («genau einen diagonalen Spiegel» у кожному гебіті, промінь з літери, число = відбиття, кожне дзеркало використане), 170 пазлів; винахідник невідомий; схожі — Rifurekuta, Mirapu.
- [puzz.link kinkonkan.js](https://puzz.link/js/pzpr-samples/kinkonkan.js) — правила EN/JP («Every outlined region contains exactly one mirror»), Nikoli vol. 89, тести вводу, коди `bkObjGe2`, `pairedLetterNe`, `pairedNumberNe`, `bkNoObj`, `ceUnused`.
- [pzprjs failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json) — тексти помилок.
- YouTube: пошук «kinkonkan puzzle».

## Непевне
- (?) Рік: перша поява — Puzzle Communication Nikoli vol. 89; рік не перевірено (`year: null`).
- (?) Дзеркала двобічні — випливає з правил (промінь відбивається від будь-якого), явно не сказано.
- (?) Стани кліку в play-режимі (`/`, `\`, точка?) і що робить drag — з тестів, не з опису.
- (?) Чи може промінь проходити через одну клітинку двічі (схрещення з іншим чи собою) — правила не забороняють; вважаю, що може.
- (?) Rifurekuta, Mirapu — лише названі Janko, не відкривав.
