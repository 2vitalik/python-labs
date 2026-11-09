---
title: Nondango (ノンダンゴ)
slug: nondango
aka: [ノンダンゴ, «No dumplings», Нонданго]
family: pencil-logic
also: []
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
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/nondango.js", best: true, note: "puzz.link/pzpr: правила EN/JP, Nikoli vol. 152, коди помилок, тести вводу"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Nondango/index.htm", note: "Janko: правила DE/EN, сірі кружечки в інтерактиві, 120 пазлів, родич Fobidoshi"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json", note: "тексти помилок `.nondango`"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=nondango+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 70
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, conflict-highlight, level-bank, in-game-editor, import-open-formats, +irregular-regions, +region-quota, +no-triple-run, +input-scheme-toggle, +undo-redo, +diagonal-run-check]
proposes: ["+cond:count_in", "+cond:run_length(color, dirs8, n)", "+card:diagonal-run-check"]
author: opus
date: 2026-11-09
---

# Nondango — перефарбуй кружечки так, щоб у кожній кімнаті був рівно один чорний і ніде не стояли три однакові поспіль, навіть по діагоналі

## Суть
Поле поділене товстими лініями на кімнати; у частині клітинок стоять кружечки. Гравець робить кожен кружечок чорним або білим: у кожній кімнаті — рівно один чорний. Три кружечки одного кольору не можуть стояти поспіль ні по горизонталі, ні по вертикалі, ні по діагоналі; порожня клітинка чи кружечок іншого кольору розриває ряд. Назва — «без данґо» (шашлички з трьох кульок на паличці).

## Поле і час
- Прямокутна сітка; кімнати — довільні області з товстими межами.
- Клітинки: порожня (без кружечка) · кружечок (невідомий / чорний / білий).
- Шари: кімнати й позиції кружечків (незмінні) · колір кружечків.
- Janko: на папері кружечки біліють за замовчуванням і їх зачорнюють; в інтерактиві всі сірі й кожен треба зробити чорним або білим.
- Час статичний; хід = змінити колір кружечка.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кімната | zone | межі | рівно один чорний кружечок |
| Кружечок | mark | невідомий / чорний / білий | гравець перемикає колір |
| Порожня клітинка | terrain | — | не має кольору; розриває ряд |
| Ряд «данґо» | mark | 3 у лінію | три однакові кружечки поспіль у 8 напрямках — заборонені |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, circle)` → ТО `mark(circle, black)`; правий клік — `mark(circle, white)`; повтор — зняти (puzz.link, тести з left/right і `setconfig,use`) (?).
- КОЛИ `constraint_broken(room_quota)` → ЯКЩО `custom: «у кімнаті ≥ 2 чорні кружечки»` (`+cond:count_in`) → ТО `set_state(room, error)` (`bkMSGe2`: «An area has two or more shaded circles»).
- КОЛИ `constraint_broken(room_empty)` → ЯКЩО `custom: «у кімнаті нема чорного кружечка»` → ТО `set_state(room, error)` (`bkNoMS`: «An area has no shaded circle»).
- КОЛИ `pattern(line(3))` → ЯКЩО `same(circles, black)` and `custom: «три сусідні клітинки по рядку, стовпцю чи діагоналі, усі з кружечками»` (`+cond:run_length(color, dirs8, n)`) → ТО `set_state(run, error)` (`msConsecGt3`).
- КОЛИ `pattern(line(3))` → ЯКЩО `same(circles, white)` → ТО `set_state(run, error)` (`muConsecGt3`: «There are three or more unshaded circles in a row»).
- Розрив ряду: ЯКЩО `cell(middle, empty)` → ТО ряд не рахується (pzpr JP: «між ними порожня клітинка — можна»).
- КОЛИ `all_constraints_met` → ТО `win`.
- Дедукція «квота»: кімната з одним кружечком — він чорний; щойно в кімнаті є чорний, решта її кружечків білі.
- Дедукція «пари»: два чорні поспіль у лінії → третій у тій лінії білий; два білі поспіль → третій чорний — як у [Takuzu](takuzu.md), але у 8 напрямках.
- Дедукція «каскад»: білі кружечки, вимушені квотою, тягнуть чорні сусідні через заборону білих трійок — і ті закривають квоти інших кімнат.
- Перемога: кожна кімната — рівно один чорний; нема однакових трійок. Поразки й рахунку нема.

## Керування і ввід
- Папір: зачорнити кружечок; решта лишаються білими.
- puzz.link play: лівий / правий клік по кружечку — чорний / білий; налаштування `use` міняє схему кнопок (?).
- puzz.link edit: малювати межі кімнат, ставити кружечки (тести створюють поля 2×1, 3×2, 2×3).
- Цифрова версія: undo/redo, перевірка за кнопкою.

## Вікна, меню, HUD
- `game-screen`: сітка з межами кімнат, кружечки трьох станів, `conflict-highlight` на кімнаті чи трійці.
- puzz.link: перемикач play/edit, кнопка перевірки з текстом першої помилки, `settings-window`.
- `help-window` — правила (pzpr EN/JP, Janko).
- `puzzle-select` — 120 пазлів Janko.
- Переходи: edit → play; check → повідомлення.

## Фічі поза полем
- `auto-check` за кнопкою з кодами pzpr.
- `undo` / `redo`; `level-editor` + `share-code` (URL puzz.link).
- `puzzle-bank` Janko.

## Варіації й родичі
- [Takuzu](takuzu.md) — заборона трійок, але без діагоналей і без кімнат; [Star Battle](star-battle.md) — квота на кімнату; [Hitori](hitori.md) — зафарбування з обмеженнями.
- Janko називає родича **Fobidoshi** (заборона чотирьох поспіль) (?).
- **Осі варіацій**: довжина забороненого ряду (3 / 4) · напрямки (4 / 8) · хто розриває ряд (порожня клітинка / лише інший колір) · квота на кімнату (1 / N / за числом).

## Цікавинки для курсу
- Перевірка трійок у 8 напрямках з урахуванням порожніх клітинок — 🌱; один цикл по 4 векторах напрямків.
- Квота «рівно один чорний на кімнату» — 🌱.
- Пропагація «двоє однакових → третій інший» + квота кімнати до нерухомої точки — 📎.
- Розвʼязувач (2-SAT-подібні імплікації + перебір) — 🥉; генератор з єдиним розвʼязком — 🥇.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `cell-click`, `conflict-highlight` · `level-bank` (Janko) · `in-game-editor`, `import-open-formats` (puzz.link).
- Перевикористано: `+irregular-regions`, `+region-quota` (Star Battle; слот n=1, колір black), `+no-triple-run` (Takuzu), `+input-scheme-toggle`, `+undo-redo`.
- **Нема** → пропозиції карток:
  - `+diagonal-run-check` «Заборонений ряд у 8 напрямках з розривами» · game-logic/constraints · 🌱 · слот {n: 3|4, dirs: 4|8, breakers: empty|other-color} — Nondango, Fobidoshi, Gomoku-перевірки.

## Пропозиції до словників
- `+cond:count_in` — повтор зі Star Battle: кількість позначок виду в області.
- `+cond:run_length(color, dirs8, n)` — є ряд з n однакових поспіль у заданих напрямках.
- `+card:diagonal-run-check` — див. мапу.

## Джерела
- ⭐ [puzz.link nondango.js](https://puzz.link/js/pzpr-samples/nondango.js) — правила EN/JP («horizontal, vertical, or diagonal»; порожня клітинка розриває), «first appeared in Puzzle Communication Nikoli vol. 152», коди `bkMSGe2`, `msConsecGt3`, `muConsecGt3`, `bkNoMS`.
- [Janko: Nondango](https://www.janko.at/Raetsel/Nondango/index.htm) — правила, назва «no dumplings», автор і рік невідомі, Fobidoshi, 120 пазлів.
- [pzprjs failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json) — тексти помилок.

## Непевне
- (?) Рік: Nikoli vol. 152 — рік видання не перевірено (`year: null`); автор невідомий (Janko).
- (?) Точне призначення лівої/правої кнопки в play-режимі puzz.link — за тестами, не за документацією.
- (?) Fobidoshi як «чотири поспіль» — з памʼяті; Janko лише називає його родичем.
- ⭐ — сторінка `puzz.link/rules.html?nondango` віддала порожній шаблон, тому ⭐ — файл правил pzpr.
