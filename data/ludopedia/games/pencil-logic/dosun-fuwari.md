---
title: Dosun-Fuwari (ドッスンフワリ)
slug: dosun-fuwari
aka: [Dosufuwa, ドッスンフワリ, Досун-Фуварі]
family: pencil-logic
also: [dig-gravity]
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
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/dosun_fuwari/", best: true, note: "Nikoli: правила — кульки (білі) спливають, ядра (чорні) тонуть, по одній парі на область"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/dosufuwa.js", note: "puzz.link: правила EN/JP, «Nikoli vol. 151», коди помилок"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=dosun+fuwari+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 70
mechanics: [markup-validity, completion-detection, satisfy-constraints, gravity-fall, impassable-cells, cell-click, level-solver, unique-puzzle-generation, level-bank, in-game-editor, import-open-formats, undo-redo, dot-mark, +irregular-regions, +region-quota, +gravity-support-check, +anti-gravity-support]
proposes: ["+cond:supported_above", "+cond:count_in", "+card:gravity-support-check", "+card:anti-gravity-support"]
author: opus
date: 2026-11-09
---

# Dosun-Fuwari — у кожну область поклади одну кульку й одне ядро: кулька спливає вгору, ядро падає вниз

## Суть
Сітка розбита жирними лініями на області; деякі клітинки зафарбовані чорним (тверді блоки). Гравець ставить у кожну область рівно одну кульку (білий кружок, легка) й одне залізне ядро (чорний кружок, важке). Кулька має «спливти до упору»: стояти у верхньому ряду, під чорною клітинкою або під іншою кулькою; ядро — «впасти до упору»: у нижньому ряду, на чорній клітинці або на іншому ядрі. Незвичне: **гравітація як статичне обмеження** — дві протилежні гравітації в одному полі, і стовпчики з куль/ядер підпирають одне одного.

## Поле і час
- Прямокутна сітка; області — довільні звʼязні групи клітинок, обведені жирними лініями.
- Чорні клітинки дані умовою, не належать жодній області (?), служать «стелею» для кульок і «підлогою» для ядер.
- Вертикаль важлива: верх і низ поля — різні межі (верхній ряд — стеля, нижній — підлога), ліво/право симетричні.
- Шари: області й чорні клітинки (незмінні) · кульки/ядра гравця · мітки «тут порожньо» (?).
- Час статичний; хід = поставити/стерти кульку чи ядро.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Біла клітинка | mark | порожньо / кулька / ядро | може прийняти один обʼєкт |
| Чорна клітинка | static | — | опора: під нею може висіти кулька, на ній — лежати ядро |
| Область | zone | клітинки | рівно 1 кулька і 1 ядро |
| Кулька (balloon, ○) | object | легка | стоїть у верхньому ряду, під чорною або під кулькою |
| Ядро (iron ball, ●) | object | важке | стоїть у нижньому ряду, на чорній або на ядрі |
| Стовпчик кульок / ядер | zone | вертикальний ряд | ланцюг опор: кожна кулька тримається за ту, що вище; кожне ядро — на тому, що нижче |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, cell)` → ТО `set_value(cell, balloon|iron|empty)` по колу (puzz.link) (?).
- КОЛИ `constraint_broken(balloon)` → ЯКЩО `not custom: «верхній ряд»` and `not custom: «над кулькою чорна клітинка або кулька»` (`+cond:supported_above`) → ТО конфлікт (puzz.link `cuNotTop`).
- КОЛИ `constraint_broken(iron)` → ЯКЩО `not custom: «нижній ряд»` and `not supported(iron)` (під ним чорна клітинка або ядро) → ТО конфлікт (puzz.link `csNotBottom`).
- КОЛИ `constraint_broken(region)` → ЯКЩО `custom: «в області дві чи більше кульок»` (`+cond:count_in`) → ТО конфлікт (puzz.link `bkUCGe2`).
- КОЛИ `constraint_broken(region)` → ЯКЩО `custom: «в області два чи більше ядер»` (`+cond:count_in`) → ТО конфлікт (puzz.link `bkSCGe2`).
- КОЛИ `constraint_broken(region)` → ЯКЩО `custom: «в області нема кульки»` → ТО конфлікт (puzz.link `bkNoUC`).
- КОЛИ `constraint_broken(region)` → ЯКЩО `custom: «в області нема ядра»` → ТО конфлікт (puzz.link `bkNoSC`).
- КОЛИ `all_constraints_met` → ТО `win`.
- Фізична метафора: розвʼязок — стан, у якому `fall(iron)` і `custom: «спливання кульки»` нічого не зрушили б (поле «осіло» в обидва боки).
- Дедукція «область з одного стовпця»: кулька — найвища клітинка області, якщо над нею стеля/чорна; ядро — найнижча, якщо під нею підлога/чорна.
- Дедукція «ланцюг»: ядро на висоті над підлогою вимагає суцільного стовпчика ядер або чорної клітинки під собою — кожне ядро нижче має бути з іншої області (бо в області одне ядро).
- Дедукція «дві клітинки»: область з двох клітинок — одна кулька й одне ядро; вертикальна пара без опор зверху й знизу неможлива, якщо вона не впирається в стелю/підлогу.
- Перемога: кожна область має рівно одну кульку й одне ядро, усі кульки «сплили», усі ядра «впали». Поразки й рахунку нема.

## Керування і ввід
- puzz.link: клік по клітинці перемикає порожньо → кулька → ядро (ліва/права кнопка — у різному порядку) (?).
- Мітка «тут нічого нема» (крапка) — звична для pzpr-жанрів (?).
- Цифрова версія: undo/redo, перевірка за кнопкою з повідомленням першої помилки.

## Вікна, меню, HUD
- `game-screen`: сітка з жирними областями, чорні клітинки, кульки ○ і ядра ●, `conflict-highlight` області чи кулі-порушника.
- puzz.link: перемикач play/edit, кнопка перевірки, `settings-window` (цифрова версія).
- `help-window` — правила (Nikoli / puzz.link).
- Переходи: edit → play; check → повідомлення з кодом помилки.

## Фічі поза полем
- `auto-check` за кнопкою (коди puzz.link).
- `undo` / `redo`; `level-editor` + `share-code` (URL пазла puzz.link).
- Банк — журнал Nikoli; генератора не бачив (?).

## Варіації й родичі
- Перша поява — Puzzle Communication Nikoli vol.151 (puzz.link).
- Родичі «квота в області»: [Star Battle](star-battle.md) (N зірок на область), [LITS](lits.md), [Heyawake](heyawake.md).
- Гравітація з аркад: `dig-gravity` (Boulder Dash — камені падають, доки є порожнє під), `grid-platformer`; тут фізика — лише перевірка кінцевого стану.
- Споріднене в пазлах «гравітація»: Statue Park / Nikoji (?) — не перевіряв.
- **Осі варіацій**: напрямки гравітації (одна / дві протилежні / за типом) · що є опорою (стеля/підлога, чорні, свій вид, будь-яка куля) · квота в області (1+1 / N кожного).

## Цікавинки для курсу
- Перевірка опори: кулька — верхній ряд або над нею чорна/кулька; ядро — дзеркально — 🌱.
- Квота «по одному кожного виду на область» — 🌱.
- Анімація «відпустити»: після розвʼязання ядра падають, кульки спливають — і нічого не зрушує (демо стабільності) — 📎.
- Розвʼязувач: для кожної області перелічити пари (кулька, ядро), відсікати за опорами; ланцюги опор між областями — пропагація + перебір — 🥉.
- Генератор: розбиття на області + розстановка, що «осіла», + перевірка єдиності — 🥇.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `gravity-fall` ↔ ядра «падають» · `impassable-cells` ↔ чорні клітинки · `cell-click`, `dot-mark` · `level-solver`, `unique-puzzle-generation`, `level-bank`, `in-game-editor`, `import-open-formats`, `undo-redo`.
- Перевикористано: `+irregular-regions`, `+region-quota` (зі Star Battle).
- **Нема** → пропозиції карток:
  - `+gravity-support-check` «Обʼєкт має опору знизу (статична гравітація)» · game-logic/constraints · 🌱 · слот {support: floor|block|same-kind}.
  - `+anti-gravity-support` «Легкий обʼєкт має опору зверху» · game-logic/constraints · 🌱 — пара до попередньої; разом — вісь `gravity: per-type` з classes.md.

## Пропозиції до словників
- `+cond:supported_above` — має опору зверху (дзеркало `supported` для «легких»: кульки, бульбашки).
- `+cond:count_in` — кількість сутностей виду в області = N (повтор зі Star Battle / Tentai Show).
- `+card:gravity-support-check`, `+card:anti-gravity-support` — див. мапу.

## Джерела
- ⭐ [Nikoli: Dosun-Fuwari](https://www.nikoli.co.jp/en/puzzles/dosun_fuwari/) — 4 правила: по одній кульці й ядру на область; кульки — вгорі / під чорною / під кулькою; ядра — внизу / на чорній / на ядрі.
- [puzz.link: dosufuwa.js](https://puzz.link/js/pzpr-samples/dosufuwa.js) — правила EN/JP, «Nikoli vol. 151», коди помилок `bkUCGe2`, `bkSCGe2`, `cuNotTop`, `csNotBottom`, `bkNoUC`, `bkNoSC`.
- YouTube: пошук «dosun fuwari puzzle».

## Непевне
- (?) Рік першої появи (vol.151) — номер бачив, рік — ні.
- (?) Чи чорні клітинки належать областям (у тестах puzz.link не перевіряв).
- (?) Розкладка вводу puzz.link (який клік ставить кульку, який ядро), мітка «порожньо».
- (?) Назва: «dossun» — японське звуконаслідування важкого удару, «fuwari» — легкого ширяння; з власних знань.
- (?) Statue Park / інші «гравітаційні» жанри як родичі — не перевіряв.
