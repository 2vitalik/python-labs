---
title: Ice path
slug: ice-path
aka: []
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
year: 2018
platforms: [web]
links:
  - {kind: itch, url: "https://rosden.itch.io/ice-path", best: true, note: "грати в браузері; «making trails of walkable floor to create solvable levels that use ice blocks»"}
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=6df83154fb88dfa09d40775ffbf065a1", note: "мобільна версія на puzzlescript.net"}
  - {kind: other, url: "https://www.puzzlescript.net/editor.html?hack=6df83154fb88dfa09d40775ffbf065a1", note: "вихідний код у редакторі PuzzleScript"}
  - {kind: other, url: "https://api.github.com/gists/6df83154fb88dfa09d40775ffbf065a1", note: "той самий код як gist (JSON), 2018-08-24"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Ice+path+Rosden+puzzlescript", note: "пошук; геймплей"}
stage: v1
coverage: 80
mechanics: [move-4dir, move-by-input, keyboard-controls, visited-trail, impassable-cells, push-object, inertia-slide, all-on-targets, cell-transform, sequential-levels, save-progress, undo-unlimited, restart-level, level-from-txt, sound-effects, +trail-wall, +self-built-level, +level-phase-switch, +kick-slide]
proposes: ["+effect:leave_trail", "+effect:kick", "+trigger:phase_switch", "+card:self-built-level", "+card:kick-slide"]
author: opus
date: 2026-11-09
---

# Ice path — спершу намалюй власним слідом підлогу рівня, потім розвʼяжи на ній льодовий Sokoban

## Суть
Коротка PuzzleScript-гра Rosden Shadow (Mark Signorelli) з його серії «daily puzzlescript creations», 6 рівнів. **Фаза 1:** гравець ходить кімнатою, і кожна клітина під ним стає слідом, через який не можна пройти вдруге. Щойно він торкнеться цілі, **усе, крім сліду, цілей і міток льоду, зникає** в порожнечу зі стінками по краю, а мітки стають крижаними блоками. **Фаза 2:** на «намальованому» рівні треба виштовхати ковзні блоки на всі цілі. Тобто гравець сам будує рівень, від якого залежить, чи буде розвʼязок.

## Поле і час
- Квадратна сітка, вид згори; рівні 9×10 клітин (за кодом рівнів): кімната в стінах, довкола — порожнеча.
- Шари: фон → слід → ціль → мітка льоду → {гравець, стіна, блок, порожнеча, нова стіна} → службові мітки ковзання.
- Покроково: хід = натискання; ковзання блока відбувається серією `again`-кроків (0,15 с) без вводу, поки не впреться.
- Фаза рівня змінюється раз: від дотику до першої цілі й до кінця рівня.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | дивиться ліво/право (косметика) | рух 4 напрямки; у фазі 1 лишає слід; у фазі 2 копає блок |
| Підлога | terrain | — | фаза 1: прохідна; фаза 2: без сліду → порожнеча |
| Стіна (зелена) | static | — | непрохідна; у фазі 2 зникає в порожнечу |
| Слід | terrain | — | клітина, де стояв гравець у фазі 1; непрохідна для нього в фазі 1; у фазі 2 — звичайна підлога |
| Мітка льоду | terrain | — | у фазі 1 по ній можна ходити; у фазі 2 стає крижаним блоком на сліді |
| Ціль | zone | неактивна / активна | фаза 1: дотик гравця вмикає фазу 2; фаза 2: місце для блока (не зупиняє ковзання) |
| Крижаний блок | object | — | від поштовху ковзає до першої перешкоди; гравець при цьому лишається на місці |
| Порожнеча | static | — | непрохідна, але не зупиняє ковзання сама — край завжди закритий новою стіною |
| Нова стіна (коричнева) | static | — | ставиться на порожнечу, що межує з уцілілою клітиною; зупиняє блоки й гравця |

## Правила (КОЛИ → ЯКЩО → ТО)
Фаза 1 — малювання:
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(player, dir)`.
- КОЛИ `input(dir)` → ЯКЩО `cell(next, wall)` → ТО `block`.
- КОЛИ `input(dir)` → ЯКЩО `occupied(next, trail)` і `count(target, >, 0)` → ТО `block`, `sound(bump)` — свій слід не перетнути.
- КОЛИ `tick` → ЯКЩО `count(target, >, 0)` і `not occupied(under_player, trail)` → ТО `custom: «під гравцем лишається слід»` (`+effect:leave_trail`); на старті рівня — теж.
- КОЛИ `enter(player, target)` → ТО `transform(target, active_target)`, `custom: «усі цілі рівня стають активними»`, `sound(switch)` — старт фази 2.

Перебудова (одразу після дотику):
- КОЛИ `custom: «зʼявилась активна ціль»` (`+trigger:phase_switch`) → ЯКЩО `custom: «у клітині нема ні сліду, ні цілі, ні мітки льоду, ні гравця»` → ТО `set_cell(cell, void)` — зникають і підлога, і старі стіни.
- КОЛИ `custom: «зʼявилась активна ціль»` → ЯКЩО `adjacent_count(void_cell, kept_cell, >=, 1)` → ТО `set_cell(void_cell, new_wall)` — край нового рівня.
- КОЛИ `custom: «зʼявилась активна ціль»` → ТО `transform(ice_mark, ice_block)`, `set_cell(trail, floor)`.

Фаза 2 — льодовий Sokoban:
- КОЛИ `contact(player, ice_block)` → ТО `push(ice_block)`, `custom: «гравець не рухається — лише копає»` (`+effect:kick`).
- КОЛИ `after(push)` → ЯКЩО `free(next)` (нема стіни, блока, гравця) → ТО `slide(ice_block, dir)`; ціль не зупиняє — блок проїжджає повз неї.
- КОЛИ `blocked(ice_block)` → ТО `custom: «блок зупинився»`.
- КОЛИ `input(dir)` → ЯКЩО `cell(next, void|new_wall)` → ТО `block`; у блок, що впирається, — копняк без руху обох.
- КОЛИ `all_on(ice_block, active_target)` → ЯКЩО `custom: «жоден блок не в русі»` → ТО `win`, `message(level N of 6)`, `next_level`.
- Перемога: на кожній цілі стоїть блок у спокої. · Поразка: нема — глухий кут (слід закрив прохід, блоки не мають упорів) → undo/restart. · Рахунку нема.

## Керування і ввід
- Стрілки/WASD — крок; Z — undo без ліміту; R — рестарт рівня (стандарт PuzzleScript). Дія X вимкнена (`noaction`).
- Undo особливо важливий: помилка фази 1 видна лише у фазі 2.

## Вікна, меню, HUD
- `main-menu` (титул PuzzleScript): Ice path · Rosden Shadow; start / continue.
- `custom-window` повідомлення: «Touch the targets to travel into your trails», «then place the ice blocks on all the targets», «level N of 6».
- `game-screen`: поле без HUD; фаза видна по зміні вигляду цілей і зникненню кімнати.
- `end-screen`: фінальна картинка з ящиків, що поступово осипається (кадри `again`).

## Фічі поза полем
- `levels-sequential` (6 рівнів), `continue` у браузері.
- `undo` ∞, `restart-level`.
- Окремий файл `Ice path.html` (293 kB) — «name your own price» на itch; код відкритий у редакторі PuzzleScript.

## Варіації й родичі
- [Ice-sliding puzzles](../push-slide/ice-sliding-puzzles.md) — головний родич: ковзання до упору; тут лід ковзає лише в блоків, а упори гравець будує сам формою сліду.
- [Pokémon overworld puzzles](../push-slide/pokemon-overworld-puzzles.md) — «Ice Path» там печера з льодовими підлогами для героя; спільна лише назва.
- [Lime Rick](lime-rick.md) — слід теж стає твердим, але одразу й назавжди; тут слід навпаки стає **єдиною підлогою** наступної фази.
- [Magiciban](magiciban.md) — автор називає натхненням іншу гру Rosden («Sliding Ground»).
- **Осі варіацій:** слід — стіна / підлога / нічого · хто ковзає — гравець / блок / обидва · фаз рівня — одна / дві (побудуй → розвʼяжи) · штовхання — з кроком (Sokoban) / копанням на місці (тут).

## Цікавинки для курсу
- Слід, що не перетинається (self-avoiding walk), + перемикання фази за дотиком — 🌱.
- Перебудова рівня: заливка «зберегти лише слід» + обводка краю стінами (сусіди порожнечі) — 📎.
- Ковзання копнутого блока через повтор кроків до упору, перевірка «в русі» в умові перемоги — 📎.
- Розвʼязувач двох фаз: перебір самоуникних шляхів від старту до цілі × льодовий Sokoban на кожному — 🥇 (простір шляхів вибухає навіть на 7×7).

## Мапа на каталог
- Є: `move-4dir`, `move-by-input`, `keyboard-controls` ↔ крок; `visited-trail` ↔ слід; `impassable-cells` ↔ стіни, слід у фазі 1; `push-object` + `inertia-slide` ↔ лід; `all-on-targets` ↔ перемога; `cell-transform` ↔ мітка → блок, слід → підлога; `sequential-levels`, `save-progress`, `undo-unlimited`, `restart-level`, `level-from-txt`, `sound-effects`.
- **Нема** → пропозиції карток:
  - `+trail-wall` (уже пропонувалась) — слід непрохідний у фазі 1.
  - `+self-built-level` «Гравець будує рівень, який потім розвʼязує» · levels/generation · 🥉 · слоти {build: trail|place, keep: cells}.
  - `+level-phase-switch` «Подія перемикає правила рівня» · game-logic · 📎.
  - `+kick-slide` «Копнути: обʼєкт ковзає, гравець стоїть» · entities/interact · 🌱.

## Пропозиції до словників
- `+effect:leave_trail(a, kind)` — клітина під/після сутності стає сутністю виду (повтор з Lime Rick, Tron).
- `+effect:kick(b)` — зсунути обʼєкт без кроку того, хто штовхає (повтор).
- `+trigger:phase_switch` — рівень перейшов у наступну фазу (тут — дотик до цілі); відрізняти від `phase_start` (фаза тіку).
- `+card:self-built-level`, `+card:kick-slide` — див. вище.

## Джерела
- ⭐ [itch: Ice path](https://rosden.itch.io/ice-path) — опис («making trails of walkable floor to create solvable levels that use ice blocks»), «Made with PuzzleScript», «Part of my daily puzzlescript creations», теги Sokoban / Difficult / Short, лінки на play та editor.
- [Вихідний код (gist API)](https://api.github.com/gists/6df83154fb88dfa09d40775ffbf065a1) — правила: слід `late [target][player no trail]`, заборона `[> player | trail]`, перебудова `[target2][no surv] -> thefloor` і обводка `wall2`, `iceground -> Crate2`, ковзання `movr…movd` з `again`, умови перемоги `all Target2 on crate2` + `no mov on Target2`; 6 рівнів; gist від 2018-08-24.
- [puzzlescript.net: play](https://www.puzzlescript.net/play.html?p=6df83154fb88dfa09d40775ffbf065a1) і [editor](https://www.puzzlescript.net/editor.html?hack=6df83154fb88dfa09d40775ffbf065a1).

## Непевне
- (?) Рік 2018 — за датою gist; на itch дату не показано (коментарі «8 years ago»).
- (?) У коді є невикористані обʼєкти (cloner, swapcrate, стрілки, `nomove`) — у шести рівнях їх нема; можливо, лишки з інших ігор серії.
- (?) Поведінка порожнечі як упору для ковзання не перевірена грою: за кодом вона не в групі `blocker`, але край завжди закритий новою стіною.
