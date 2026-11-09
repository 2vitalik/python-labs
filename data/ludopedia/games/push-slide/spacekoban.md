---
title: Spacekoban
slug: spacekoban
aka: [Space Sokoban]
family: push-slide
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2014
platforms: [web (PuzzleScript)]
links:
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=6a6c07f71d7039e4155e", best: true, note: "грати в браузері: 20 рівнів"}
  - {kind: other, url: "https://gist.github.com/octoConnors/6a6c07f71d7039e4155e", note: "код PuzzleScript: обʼєкти, імпульс u/d/l/r, відштовхування, драбини, промені, умови перемоги; 14 ревізій"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Spacekoban+puzzlescript", note: "пошук; геймплей"}
stage: v1
coverage: 80
mechanics: [move-4dir, keyboard-controls, inertia-slide, stop-cell, impassable-cells, all-on-targets, undo-unlimited, restart-level, sequential-levels, +push-off-move, +recoil-push, +momentum-transfer, +push-chain, +handhold-cell, +win-at-rest]
proposes: ["+card:push-off-move", "+card:recoil-push", "+card:handhold-cell", "+card:win-at-rest", "+card:momentum-transfer", "+card:push-chain", "+window:title-screen"]
author: opus
date: 2026-11-09
---

# Spacekoban — Sokoban у невагомості: ходити не можна, лише відштовхнутись і летіти до упору

## Суть
Космонавт на станції має загнати всі ящики на цілі, але в невагомості він не ходить: рушити можна, лише відштовхнувшись від стіни чи ящика **позаду**, і тоді летиш до першої перешкоди. Відштовхнувся від ящика — ви розлітаєтесь у протилежні боки (віддача). Летючий обʼєкт, вдарившись в інший, запускає його, і далі вони летять «поїздом», доки передній не впреться у стіну. Драбини-поручні ловлять космонавта й дають стартувати в будь-який бік, промені зупиняють усе.

## Поле і час
- Квадратна сітка в стінах; шари: підлога → цілі → драбина / вихід → гравець, стіни, ящики, кришка → промінь → невидимий маркер імпульсу (u / d / l / r).
- Імпульс — **стан обʼєкта** (маркер напрямку): поки він є, обʼєкт щокадру зсувається на 1 клітину; анімація польоту — крок кожні 0,12 с (`again_interval`).
- Хід = один ввід; увесь політ (кілька кадрів `again`) розвʼязується в межах цього ходу, наступний ввід — коли все зупинилось.
- 20 рівнів, від коридору з одним ящиком до великих кімнат із драбинами й променями.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Космонавт | player | імпульс (напрям / нема) | не ходить; відштовхується від стіни чи ящика позаду або з драбини й летить до упору |
| Стіна | static | solid | опора для відштовху; зупиняє будь-який політ |
| Ящик | object | імпульс | летить до упору після віддачі чи удару; удар передає імпульс тому, що попереду |
| Ціль | terrain | — | місце для ящика |
| Драбина (поручень) | terrain | лише для космонавта | ловить космонавта в польоті; з неї можна рушити в будь-який бік; ящики пролітають крізь |
| Промінь (beam) | terrain | для всіх | зупиняє будь-який летючий обʼєкт на цій клітині |
| Вихід | gate | під кришкою, поки хоч один ящик не на цілі | відкрита кришка — прохід; у 20 рівнях не вжито |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `not cell(here, ladder)` і `not occupied(cell_behind, wall)` і `not occupied(cell_behind, crate)` → ТО `block` (нема від чого відштовхнутись).
- КОЛИ `input(dir)` → ЯКЩО `occupied(cell_behind, wall)` → ТО `set_state(player, momentum(dir))`, `slide(player, dir)`.
- КОЛИ `input(dir)` → ЯКЩО `occupied(cell_behind, crate)` → ТО `slide(player, dir)`, `slide(crate, -dir)` — віддача: розлітаються навпаки.
- КОЛИ `input(dir)` → ЯКЩО `cell(here, ladder)` → ТО `slide(player, dir)` (з поручня — у будь-який бік, опора позаду не потрібна).
- КОЛИ `contact(a, b)` → ЯКЩО `state(a, momentum(dir))` і `occupied(next_cell, crate|player)` → ТО `set_state(b, momentum(dir))` — передача імпульсу; `a` теж летить далі, тож дотичні обʼєкти рухаються «поїздом».
- КОЛИ `blocked(a)` → ЯКЩО `occupied(next_cell, wall)` або (`occupied(next_cell, exit)` і `state(exit, closed)`) → ТО `clear_state(a, momentum)` — зупинка; задні вагони «поїзда» впираються в передній і теж стають.
- КОЛИ `enter(player, ladder)` → ЯКЩО `state(player, momentum)` → ТО `clear_state(player, momentum)` (схопився за поручень).
- КОЛИ `enter(a, beam)` → ТО `clear_state(a, momentum)` (промінь гасить політ і ящика, і космонавта).
- КОЛИ `enter(crate, ladder)` → ТО `custom: «нічого — ящик летить далі»`.
- КОЛИ `tick` → ЯКЩО `custom: «хоч один ящик не на цілі»` → ТО `set_state(exit, closed)` (кришка — суцільна); інакше `clear_state(exit, closed)`.
- КОЛИ `all_on(crate, target)` → ЯКЩО `not state(any, momentum)` і `custom: «на кожному виході стоїть космонавт»` → ТО `win`, `next_level`.
- КОЛИ `input(undo)` → ТО `undo(1)`; КОЛИ `input(restart)` → ТО `restart`.
- Перемога: усі ящики на цілях і все зупинилось (вихід — лише якщо є в рівні). · Поразка: нема; ящик у куті чи космонавт без опори в кутку — undo/рестарт. · Рахунок: нема.

## Керування і ввід
- Стрілки / WASD — «відштовхнутись у цей бік» (стандарт PuzzleScript); напрям означає, куди летіти, а опора має бути з протилежного боку.
- `Z` — undo, `R` — рестарт; дія `X` у правилах не вжита.
- Ввід, що не має опори, просто ігнорується — це основне «правило гри», а не помилка.

## Вікна, меню, HUD
- `title-screen` (custom, стандарт PuzzleScript): «Spacekoban», автор Connorses [Loneship Games].
- `game-screen`: поле на темно-синьому тлі, без HUD.
- Повідомлень між рівнями нема; після 20-го — стандартне завершення PuzzleScript.
- Переходи: title → 20 рівнів підряд.

## Фічі поза полем
- `levels-sequential`: 20 рівнів.
- `undo` ∞ і `restart-level` (рушій PuzzleScript, `noundo` не задано).
- Відкритий код (gist) — можна відкрити в редакторі й змінити.

## Варіації й родичі
- Рушій тих самих ідей: [ice-sliding-puzzles](ice-sliding-puzzles.md) (ковзання до упору), [pengo](pengo.md) (штовхнутий блок летить), [isaac-conservation-of-momentum](../thinky/isaac-conservation-of-momentum.md) (імпульс передається, як у колисці Ньютона), [sokoban](sokoban.md) (мета й ящики), [ricochet-robots](ricochet-robots.md) (рух до упору, зупинка об сутність).
- Осі варіацій:
  - **як починається рух**: крок (Sokoban) / ковзання від будь-якої клітини (Inertia) / лише відштовхуванням від опори позаду (Spacekoban);
  - **що робить удар**: зупиняє ударника й запускає ціль (Isaac) / обидва летять далі «поїздом» (Spacekoban) / ціль не рухається (Inertia);
  - **віддача**: нема / від ящика — розліт у протилежні боки (Spacekoban);
  - **що зупиняє**: лише стіни / ще й клітини-гальма для всіх (промінь) / гальма лише для гравця (драбина);
  - **коли перемога**: одразу / лише коли все зупинилось.

## Цікавинки для курсу
- Рух відштовхуванням: перевірка опори позаду замість клітини попереду — 🌱 (мінімальна зміна Sokoban, а відчуття гри інше).
- Імпульс як стан обʼєкта + цикл «рухай усе з імпульсом, доки щось рухається» — 📎.
- Віддача від ящика (дві сутності отримують протилежні напрямки) — 🌱.
- «Поїзд»: передача імпульсу ланцюгом дотичних обʼєктів і зупинка всього складу, коли передній вперся, — 🥉 (порядок оновлення важливий).
- Клітини-гальма двох видів: для всіх (промінь) і лише для гравця, з дозволом старту в будь-який бік (драбина) — 📎.
- Розвʼязувач: BFS по станах, де хід — повний політ до спокою; детектор «космонавт без опори» як глухий кут — 🥇.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ 4 напрямки вводу; `inertia-slide` ↔ політ до упору; `stop-cell` ↔ промінь; `impassable-cells` ↔ стіни; `all-on-targets`; `undo-unlimited` + `restart-level`; `sequential-levels`.
- **Нема** → пропозиції карток:
  - `+push-off-move` «Рух лише відштовхуванням від опори позаду» · entities/move · 🌱 · слот {anchors: wall|crate|ladder}.
  - `+recoil-push` «Віддача: гравець і ящик розлітаються в протилежні боки» · entities/interact · 🌱.
  - `+momentum-transfer` (вже пропонована, Isaac) — удар передає рух; слот {striker: stops|continues}.
  - `+push-chain` (вже пропонована, Cell Machine) — летючий обʼєкт штовхає весь ряд дотичних.
  - `+handhold-cell` «Клітина-поручень: ловить гравця й дозволяє старт у будь-який бік» · entities/interact · 📎.
  - `+win-at-rest` «Перемога перевіряється лише після зупинки всіх рухів» · game-logic/win · 🌱.

## Пропозиції до словників
- `+card:push-off-move`, `+card:recoil-push`, `+card:handhold-cell`, `+card:win-at-rest`; повтор `+card:momentum-transfer`, `+card:push-chain`.
- `+window:title-screen` — повтор (стандарт PuzzleScript).
- ⏳-слова, вжиті тут: `input`, `cell`, `occupied`, `state`, `set_state`, `clear_state`, `slide`, `blocked`, `enter`, `tick`, `all_on`, `undo`.

## Джерела
- ⭐ [Грати в PuzzleScript](https://www.puzzlescript.net/play.html?p=6a6c07f71d7039e4155e) — 20 рівнів (сторінка вантажить код із gist).
- [Gist з кодом](https://gist.github.com/octoConnors/6a6c07f71d7039e4155e) — автор Connorses [Loneship Games]; OBJECTS, LEGEND, шари, усі правила (скасування руху без опори, `[< player | solid] -> [player D | solid]`, віддача від ящика, передача маркера імпульсу, `late`-зупинка на драбині й промені, кришка виходу), WINCONDITIONS `all crate on target` · `all exit on player` · `no dir`; остання активність 17.03.2018, 14 ревізій.
- YouTube: пошук «Spacekoban puzzlescript».

## Непевне
- (?) Рік 2014 — з рядка черги; на сторінці gist видно лише «last active March 17, 2018». Пошук знайшов автора Connorses у групі PuzzleScript 2014 року, але без назви гри.
- (?) Вихід з кришкою є в коді, але в жодному з 20 рівнів не стоїть — можливо, лишок від ранньої версії.
- (?) Тонкощі порядку рушія: що стається, коли два «поїзди» летять назустріч, або ящик врізається в космонавта, що стоїть на драбині, — з коду не очевидно, не перевірено грою.
