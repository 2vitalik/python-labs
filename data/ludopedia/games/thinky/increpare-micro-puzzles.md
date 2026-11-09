---
title: "increpare: мікро-Sokoban-и (Crates move when you move · Pushy-V Pully-H · Muraphilic Monophobic Multiban)"
slug: increpare-micro-puzzles
aka: [Crates move when you move, Pushy-V Pully-H, Muraphilic Monophobic Multiban]
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2021
platforms: [web]
links:
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=b8f93072878708ce91fb3e5126a02b0b", best: true, note: "Crates move when you move — грати (10 рівнів)"}
  - {kind: other, url: "https://www.puzzlescript.net/editor.html?hack=b8f93072878708ce91fb3e5126a02b0b", note: "Crates move when you move — вихідний код PuzzleScript (2 правила)"}
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=47bb12909e13a1f9170114505813a5d1", note: "Pushy-V Pully-H — грати (11 рівнів)"}
  - {kind: other, url: "https://www.puzzlescript.net/editor.html?hack=47bb12909e13a1f9170114505813a5d1", note: "Pushy-V Pully-H — вихідний код"}
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=8d2f0e7542ba8a51f1ded3c3fee41e86", note: "Muraphilic Monophobic Multiban — грати (8 рівнів)"}
  - {kind: other, url: "https://www.puzzlescript.net/editor.html?hack=8d2f0e7542ba8a51f1ded3c3fee41e86", note: "Multiban — вихідний код"}
  - {kind: official, url: "https://www.increpare.com/game/muraphilic-monophobic-multiban.html", note: "сторінка Multiban (2024-05-10): лінки play/source"}
  - {kind: official, url: "https://www.increpare.com/", note: "каталог increpare games з датами 2021/08/16, 2021/08/17, 2024/05/10"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=increpare+puzzlescript+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 80
mechanics: [move-4dir, keyboard-controls, push-object, pull-object, impassable-cells, all-on-targets, inertia-slide, sequential-levels, save-progress, undo-unlimited, restart-level, level-from-txt, sound-effects, +move-all-with-player, +axis-dependent-push-pull, +push-needs-two, +pushable-walls, +push-chain, +rule-minimal-variant]
proposes: ["+cond:line_length", "+effect:slide_all", "+card:move-all-with-player", "+card:axis-dependent-push-pull", "+card:push-needs-two", "+card:pushable-walls"]
author: opus
date: 2026-11-09
---

# increpare: мікро-Sokoban-и — один перекручений рядок правил змінює всю гру

## Суть
Три маленькі PuzzleScript-гри Stephen Lavelle (increpare): класичний Sokoban (гравець, стіни, ящики, цілі; перемога — на кожній цілі ящик), де змінено **одне-два правила руху**. *Crates move when you move* — гравець не штовхає, а всі ящики самі їдуть у бік його кроку до упору. *Pushy-V Pully-H* — по вертикалі гравець штовхає, по горизонталі тягне. *Muraphilic Monophobic Multiban* — гравець штовхає лише ряд із ≥2 обʼєктів, і стіни теж штовхаються. Цінність для курсу — показати, що «варіант Sokoban» — це заміна кількох рядків у правилах, а рівні змінюють сенс.

## Поле і час
- Квадратна сітка, рівень — текстова мапа PuzzleScript (`#` стіна, `P` гравець, `*` ящик, `O` ціль, `@` ящик на цілі). Розміри малі: 5×6…16×10 клітин.
- Шари колізії: фон → ціль → {гравець, стіна, ящик} (у клітині лише один із трьох).
- Покроково: хід = одне натискання стрілки; спершу застосовуються правила, потім фаза руху PuzzleScript (рух, що впирається, скасовується). Час, вороги, випадковість — нема.
- Multiban: рівні обрамлені смугою порожнього фону, щоб стіни було куди виштовхнути; край мапи — непрохідний.

## Сутності
**Crates move when you move** (2021-08-17, 10 рівнів)
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | — | крок на 1 у 4 напрямки; сам нічого не штовхає |
| Ящик | object | — | на кожен крок гравця ковзає в тому ж напрямку до перешкоди (стіна, ящик, гравець) |
| Стіна | static | — | непрохідна, нерухома |
| Ціль | static | — | має бути під ящиком |

**Pushy-V Pully-H** (2021-08-16, 11 рівнів)
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | — | крок на 1; вертикально штовхає ящик перед собою, горизонтально тягне ящик позаду |
| Ящик | object | — | рухається лише від гравця: вгору/вниз поштовхом, вліво/вправо тягненням; ланцюгом не йде |
| Стіна | static | — | непрохідна |
| Ціль | static | — | має бути під ящиком |

**Muraphilic Monophobic Multiban** (2024-05-10, 8 рівнів, розкладки за Microban Девіда Скіннера)
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | — | крок на 1; штовхає лише ряд ≥2 штовхуваних (ящик або стіна) |
| Ящик | object | штовхуваний | рухається лише в ряду з іще одним штовхуваним позаду себе; сам-один — нерухомий |
| Стіна | object | штовхувана | як ящик: їде в ряду з ≥2; «стіна» лише назва |
| Ціль | static | — | має бути під ящиком (стіна на цілі не рахується) |

## Правила (КОЛИ → ЯКЩО → ТО)
Спільне для всіх трьох:
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(player, dir)`; інакше `block`.
- КОЛИ `all_on(crate, target)` → ТО `win`, `message(«level N of M»)`, `next_level`.
- Поразки нема (глухий кут → undo/restart). Рахунку нема.

Crates move when you move (вихідний код: `[ > Player ] [ Crate ] -> [ > Player ] [ > Crate ]` і `[ > crate | no obstacle ] -> [ | > crate ]`):
- КОЛИ `input(dir)` → ТО `custom: «кожен ящик на полі отримує рух dir»` (`+effect:slide_all`).
- КОЛИ `after(slide_all)` → ЯКЩО `moving(crate, dir)` і `free(cell_ahead)` → ТО `slide(crate, dir)` — правило повторюється, доки ящик не впреться у стіну, ящик чи гравця.
- КОЛИ `input(dir)` → ЯКЩО `not free(next_cell)` → ТО `block` для гравця, але `slide_all` усе одно відбувається.
- КОЛИ `contact(player, crate)` → ТО `block` для гравця: штовхання нема; «поштовх» виникає лише тоді, коли гравець стоїть на шляху ковзання.
- КОЛИ `custom: «ящик зупинився впритул до гравця, що йде в той самий бік»` → ТО `move(crate, dir)` на 1 у фазі руху, слідом за гравцем (?).

Pushy-V Pully-H (`vertical [ > Player | Crate ] -> [ > Player | > Crate ]`, `horizontal [ < Player | Crate ] -> [ < Player | < Crate ]`):
- КОЛИ `input(up|down)` → ЯКЩО `occupied(cell_ahead, crate)` і `free(cell_behind_crate)` → ТО `push`, `move(player, dir)`; інакше `block`.
- КОЛИ `input(left|right)` → ЯКЩО `occupied(cell_behind_player, crate)` і `free(cell_ahead)` → ТО `move(player, dir)`, `pull(crate)`.
- КОЛИ `input(left|right)` → ЯКЩО `occupied(cell_ahead, crate)` → ТО `block` (горизонтально не штовхає).
- КОЛИ `input(up|down)` → ЯКЩО `occupied(cell_behind_player, crate)` і `free(next_cell)` → ТО `move(player, dir)` без `pull` (вертикально не тягне).
- Ящик у ящик: `block` — ланцюгового поштовху нема.

Muraphilic Monophobic Multiban (`[ > Player | pushable | pushable ] -> …`, `[ > pushable | pushable ] -> …`, `pushable = wall or crate`):
- КОЛИ `contact(player, crate|wall)` → ЯКЩО `custom: «одразу за ним ще один штовхуваний»` (`+cond:line_length(≥2)`) → ТО `push` усього ряду штовхуваних підряд.
- КОЛИ `contact(player, crate|wall)` → ЯКЩО `custom: «за ним порожньо — обʼєкт сам-один»` → ТО `block`.
- КОЛИ `push` ряду → ЯКЩО `custom: «кінець ряду впирається в край мапи»` → ТО `block` (увесь ряд і гравець стоять).
- Стіни рухаються за тими самими правилами, що й ящики, але на цілі не зараховуються.

## Керування і ввід
- Стрілки / WASD — крок; Z — undo без ліміту; R — рестарт рівня; Esc — меню; X/пробіл — лише пропуск повідомлень (у Crates — `noaction`, дії нема).
- Мишею/тачем — свайп на мобільному (стандарт PuzzleScript) (?).

## Вікна, меню, HUD
- `main-menu` (титульний екран PuzzleScript): назва, автор, «start game» / «continue» (якщо є прогрес).
- `custom-window` повідомлення між рівнями: «level N of M» (Multiban — ще вступна фраза героя на 1-му рівні), фінальна жартівлива фраза.
- `game-screen`: лише поле, без HUD; звук на рух ящика, старт і кінець рівня.
- `pause-menu` (Esc): продовжити / вийти на титул (?).
- Переходи: main-menu → game-screen → (усі цілі) повідомлення → наступний рівень → … → фінальне повідомлення.

## Фічі поза полем
- `levels-sequential` (10 / 11 / 8 рівнів), `continue` — прогрес у браузері (localStorage PuzzleScript).
- `undo` ∞ і `restart-level` — вбудовані в рушій.
- Вихідний код відкритий: кнопка редактора (`editor.html?hack=…`) дає змінити правила й рівні — це по суті `level-editor` + `custom-rules`.
- У коментарях Crates — інструменти автора: PuzzleScript з розвʼязувачем і генератор рівнів (блок TRANSFORMATION з `choose N` — випадкові стіни/ящики/цілі).

## Варіації й родичі
- Батько — Sokoban (`games/push-slide/sokoban.md`); Multiban — переробка Microban (David W. Skinner).
- increpare має десятки таких мініатюр: Sokoban[Sokoban[Sokoban]]], Scalesoban, Explodoban, «an OK multiban level» (2018).
- У корпусі: ящики, що їдуть усі разом, — родич tilt-ігор (`games/push-slide/ice-sliding-puzzles.md`, 2048-зсув); рухомі стіни — `games/thinky/baba-is-you.md` (WALL IS PUSH).
- **Осі варіацій:** хто рухає ящики — гравець поштовхом / гравець тягненням / усі ящики разом за вводом; залежність від осі — нема / вертикаль штовхає, горизонталь тягне; мінімум ряду — 1 / ≥2; що штовхується — лише ящики / і стіни; довжина ланцюга — 1 / ∞.

## Цікавинки для курсу
- Sokoban як таблиця правил «шаблон → заміна» (PuzzleScript-мислення): студент змінює одне правило — 🥉 (рушій правил по сітці).
- «Усі ящики ковзають у бік кроку» з правильним порядком обробки (від стіни назустріч) — 🥉.
- Штовхання/тягнення залежно від осі — 🌱 (одна умова на напрямок).
- Поштовх лише ряду ≥2 + стіни як штовхувані — 📎 (сканування ряду до порожньої клітини).
- Розвʼязувач BFS для всіх трьох (той самий код, інша функція ходу) — 🥈: гарний приклад, що solver не залежить від правил.
- Фаза руху PuzzleScript: рух, що впирається, скасовується, решта повторюється до стабілізації — 🥈.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ стрілки; `push-object` ↔ вертикальний поштовх / ряд; `pull-object` ↔ горизонтальне тягнення; `inertia-slide` ↔ ящики до упору; `impassable-cells` ↔ стіни (крім Multiban); `all-on-targets` ↔ перемога; `sequential-levels` + `save-progress` ↔ рівні й continue; `undo-unlimited` + `restart-level` ↔ Z/R; `level-from-txt` ↔ текстові мапи PuzzleScript; `sound-effects`.
- **Нема** → пропозиції карток:
  - `+move-all-with-player` «Усі ящики рухаються з кроком гравця» · entities/move · 🥉 · слот {mode: slide|step}.
  - `+axis-dependent-push-pull` «Вісь визначає: штовхати чи тягнути» · entities/legality · 🌱.
  - `+push-needs-two` «Штовхається лише ряд ≥N» · entities/legality · 📎 · слот {min: 2}.
  - `+pushable-walls` «Стіни теж штовхаються» · entities/legality · 🌱.
  - `+push-chain` «Ланцюговий поштовх ряду» · entities/legality · 📎 (уже пропонувалась іншими файлами).
  - `+rule-minimal-variant` «Варіант гри заміною одного правила» · game-logic/constraints · 🥉 — методична картка.

## Пропозиції до словників
- `+cond:line_length(dir, op, n)` — довжина суцільного ряду обʼєктів у напрямку (Multiban: ≥2).
- `+effect:slide_all(kind, dir)` — усі сутності виду ковзають у напрямку до упору (Crates; tilt-ігри).
- `+card:move-all-with-player`, `+card:axis-dependent-push-pull`, `+card:push-needs-two`, `+card:pushable-walls` — механік нема в каталозі.

## Джерела
- ⭐ [Crates move when you move — грати](https://www.puzzlescript.net/play.html?p=b8f93072878708ce91fb3e5126a02b0b) · [код](https://www.puzzlescript.net/editor.html?hack=b8f93072878708ce91fb3e5126a02b0b) — 2 правила, 10 рівнів, `noaction`, фінальне повідомлення.
- [Pushy-V Pully-H — грати](https://www.puzzlescript.net/play.html?p=47bb12909e13a1f9170114505813a5d1) · [код](https://www.puzzlescript.net/editor.html?hack=47bb12909e13a1f9170114505813a5d1) — `vertical`/`horizontal` правила, 11 рівнів.
- [Muraphilic Monophobic Multiban — грати](https://www.puzzlescript.net/play.html?p=8d2f0e7542ba8a51f1ded3c3fee41e86) · [код](https://www.puzzlescript.net/editor.html?hack=8d2f0e7542ba8a51f1ded3c3fee41e86) · [сторінка](https://www.increpare.com/game/muraphilic-monophobic-multiban.html) — `pushable = wall or crate`, 8 рівнів за Microban.
- [increpare.com](https://www.increpare.com/) — каталог ігор з датами.
- Код прочитано через GitHub gist API (GET `api.github.com/gists/<hash>`).

## Непевне
- (?) Слідування ящика за гравцем на 1 клітину у фазі руху (Crates) — виведено з семантики PuzzleScript, не перевірено грою.
- (?) Меню паузи і свайп-керування — стандарт рушія PuzzleScript з памʼяті.
- (?) Черга (`queue/thinky.md`) описувала Multiban як «кілька героїв одночасно» і Crates як «дзеркалення» — код показує інше: один герой; ящики не дзеркалять, а ковзають у той самий бік.
