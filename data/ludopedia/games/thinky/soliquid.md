---
title: Soliquid
slug: soliquid
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
year: 2019
platforms: [web]
links:
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=4adc7b17c2c0449c3a8b6c730e8cbfc9", best: true, note: "грати в браузері: 11 рівнів"}
  - {kind: other, url: "https://api.github.com/gists/4adc7b17c2c0449c3a8b6c730e8cbfc9", note: "вихідний код (gist, JSON, 2019-07-24): рідке й тверде тіло, слід, «фронт» упору, морозилка й нагрівач"}
  - {kind: other, url: "https://www.puzzlescript.net/Gallery/gifs/4adc7b17c2c0449c3a8b6c730e8cbfc9.gif", note: "GIF з галереї: рівень 2 — тіло тягнеться до 3 клітин і сплющується об стіни"}
  - {kind: other, url: "https://raw.githubusercontent.com/increpare/PuzzleScript/master/src/games_dat.js", note: "дані галереї PuzzleScript: назва, автор Anton Klinger, лінк"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Soliquid+puzzlescript", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [move-4dir, move-by-input, keyboard-controls, push-object, impassable-cells, all-on-targets, undo-unlimited, restart-level, sequential-levels, save-progress, level-from-txt, sound-effects, +stretchy-body, +form-swap-pad, +assemble-shape-in-template]
proposes: ["+card:stretchy-body", "+card:form-swap-pad", "+card:assemble-shape-in-template", "+window:title-screen", "+window:message-screen"]
author: opus
date: 2026-11-19
---

# Soliquid — рідке тіло тягнеться за рухом до трьох клітин і сплющується об стіни; на морозилці твердне, на нагрівачі тане; заповни контур цілей

## Суть
PuzzleScript-гра Anton Klinger (2019), 11 рівнів. Герой — пляма з кількох клітин, і всі вони рухаються разом; на старті це одна клітина. Рідке тіло у вільному русі тягнеться (кожна лінія вздовж руху подовжується позаду, до 3 клітин), а впершись — сплющується (кожна лінія коротшає на 1, до 1 клітини).

Коли все тіло стоїть на морозилках, воно твердне: форма застигає, не росте й не стискається; на нагрівачах — знову рідке. Мета — щоб тіло точно покрило контур цілей; ящики штовхаються по одному.

## Поле і час
- Квадратна сітка, один екран на рівень; 11 рівнів від 8×8 до 11×17 клітин (з коду).
- Шари колізій: фон → ціль → {морозилка, нагрівач} → {рідке тіло, стіна, ящик, тверде тіло} → службові маркери (фронт упору, напрям руху, звідки / куди ящик, «хоче замерзнути / розтанути»).
- Покроково: хід = натискання; усі клітини тіла отримують той самий рух, потім пізні правила дотягують слід чи сплющують тіло й перевіряють морозилки та нагрівачі. Дії нема (`noaction`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Рідке тіло (`Liquid`) | player | кількість клітин змінюється; лінія вздовж руху ≤ 3 | рух усіма клітинами; вільний крок — лінії вздовж руху подовжуються позаду на 1 (до 3); упершись — коротшають на 1 (до 1) |
| Тверде тіло (`Frozen`) | player | форма застигла | рух усіма клітинами; упершись — стоїть, форма не змінюється |
| Морозилка | terrain | — | рідке тіло, що ЦІЛКОМ стоїть на морозилках, твердне |
| Нагрівач | terrain | — | тверде тіло, що ЦІЛКОМ стоїть на нагрівачах, тане |
| Ящик | object | — | штовхається на 1, якщо за ним вільно; ланцюгом — ні |
| Стіна | static | — | непрохідна |
| Ціль | zone | — | контур, який тіло має покрити точно: ні клітини поза ним, ні дірки в ньому |

## Правила (КОЛИ → ЯКЩО → ТО)
Рух:
- КОЛИ `input(dir)` → ТО `move(body, dir)` — кожна клітина тіла на 1 (усі клітини — гравець).
- КОЛИ `contact(body, crate)` → ЯКЩО `free(cell_behind_crate)` → ТО `push`; інакше ящик — упор.
- КОЛИ `blocked(body_cell)` → ТО `custom: «тіло не просувається: передні клітини стоять, решта підтягується на 1»`; поштовх ящика в цьому ході скасовано.

Рідке й тверде:
- КОЛИ `after(move)` → ЯКЩО `state(body, liquid)` and `custom: «лінія тіла вздовж руху коротша за 3»` → ТО `grow(line, 1)` — клітина позаду лишається рідиною: одна клітина за 2 кроки стає лінією з 3, а ще за 2 кроки вбік — квадратом 3×3.
- КОЛИ `blocked(body_cell)` → ЯКЩО `state(body, liquid)` → ТО `shrink(line, 1)` — кожна лінія вздовж руху коротшає на 1 (до 1): тіло сплющується об перешкоду.
- КОЛИ `blocked(body_cell)` → ЯКЩО `state(body, frozen)` → ТО `block` — форма тверда, тіло стоїть цілим.
- Тверде тіло у вільному русі не росте й не коротшає.
- КОЛИ `after(move)` → ЯКЩО `state(body, liquid)` and `custom: «кожна клітина тіла на морозилці»` → ТО `transform(body, frozen)`, `sound(freeze)`.
- КОЛИ `after(move)` → ЯКЩО `state(body, frozen)` and `custom: «кожна клітина тіла на нагрівачі»` → ТО `transform(body, liquid)`, `sound(melt)`.

Перемога:
- КОЛИ `all_on(body, target)` → ЯКЩО `custom: «і кожна ціль покрита тілом»` → ТО `win`, `next_level` (у коді: «All Player on Target», «All Target on Player»).
- Перемога: тіло точно збігається з контуром цілей, у будь-якому стані · Поразки нема · Рахунку нема.

## Керування і ввід
- Стрілки / WASD — рух усього тіла; дії нема.
- Z — undo, R — рестарт (стандарт PuzzleScript).
- Форму тіла задають лише рухом: тягнути у вільному просторі, сплющувати об стіни, «заморожувати» потрібну форму.

## Вікна, меню, HUD
- `main-menu` — титульний екран PuzzleScript (`title-screen`): «Soliquid», «Anton Klinger».
- `game-screen` — поле без HUD; стан тіла видно з кольору: зелене — рідке, блакитне — тверде.
- `custom-window` (`message-screen`) — фінал «Thank you for playing my game!».
- Переходи: титул → рівні 1–11 → фінальне повідомлення.

## Фічі поза полем
- `levels-sequential` (11 рівнів), `undo` ∞, `restart-level`, `continue` (стандарт PuzzleScript).
- `sound-effects`: окремі звуки кроку рідкого й твердого тіла, замерзання, танення, кінця рівня й гри.

## Варіації й родичі
- Родичі в корпусі: [Jelly no Puzzle](jelly-no-puzzle.md) — желе з кількох клітин, форма незмінна, злипаються за кольором; [Snakebird](snakebird.md) — тіло-черга з гравітацією; [Stoneman's Adventure](stonemans-adventure.md) — клітина перемикає форму героя; [A Good Snowman Is Hard to Build](a-good-snowman-is-hard-to-build.md) — кулі ростуть від руху снігом; [Lime Rick](lime-rick.md) — слід стає тілом; [Elephant in a Bottle](elephant-in-a-bottle.md) — скласти фігуру точно в шаблон.
- Осі варіацій: **тіло у вільному русі** — незмінне (Jelly, тверде тут) / тягнеться до N (рідке тут) / лишає слід-стіну (Lime Rick); **тіло при упорі** — стоїть / сплющується (рідке тут); **перемикач стану** — одна клітина (Stoneman) / усе тіло на клітинах-перемикачах (тут).

## Цікавинки для курсу
- Тіло з багатьох клітин-гравців, що рухаються разом, і правило «хоч одна вперлась — не просувається ніхто» — 📎.
- Розтягування рідкого тіла (лінії до 3) і сплющування об упор — 🥉: операції над лініями тіла вздовж осі руху.
- Зміна стану всього тіла лише тоді, коли всі клітини на перемикачах, — 🌱.
- Перемога «тіло точно = контур»: усі клітини на цілях і всі цілі покриті — 🌱.
- Розвʼязувач BFS: стан = множина клітин тіла + стан + ящики — 🥈 (форма змінюється, простір станів великий).

## Мапа на каталог
- Є: `move-4dir` · `move-by-input` · `keyboard-controls` ↔ стрілки; `push-object` ↔ ящики по одному; `impassable-cells` ↔ стіни; `all-on-targets` ↔ тіло на цілях; `undo-unlimited` · `restart-level` · `sequential-levels` · `save-progress` · `level-from-txt` · `sound-effects`.
- **Нема** → пропозиції карток:
  - `+stretchy-body` «Рідке тіло тягнеться за рухом і сплющується об упор» · entities/state · 🥉 · слоти {max_len: 3, min_len: 1}.
  - `+form-swap-pad` (Stoneman's Adventure) — тут слот {all_cells: true}: морозилка → тверде, нагрівач → рідке.
  - `+assemble-shape-in-template` (Elephant in a Bottle) — тіло має точно покрити контур цілей.

## Пропозиції до словників
- `+card:stretchy-body`, `+card:form-swap-pad`, `+card:assemble-shape-in-template` — див. вище.
- `+window:title-screen`, `+window:message-screen` — повтор (стандартні екрани PuzzleScript).

## Джерела
- ⭐ [PuzzleScript: Soliquid](https://www.puzzlescript.net/play.html?p=4adc7b17c2c0449c3a8b6c730e8cbfc9) — гра в браузері, 11 рівнів.
- [Вихідний код (gist через GitHub API)](https://api.github.com/gists/4adc7b17c2c0449c3a8b6c730e8cbfc9) — обʼєкти й шари; правила «фронту» упору, сліду рідкого тіла, відновлення форми твердого, замерзання й танення лише цілим тілом; умови перемоги; 11 рівнів; gist від 2019-07-24.
- [GIF з галереї](https://www.puzzlescript.net/Gallery/gifs/4adc7b17c2c0449c3a8b6c730e8cbfc9.gif) — рівень 2: одна клітина тягнеться в лінію, сплющується об стіну, росте до 3×3 і знову сплющується.
- [Дані галереї PuzzleScript](https://raw.githubusercontent.com/increpare/PuzzleScript/master/src/games_dat.js) — запис «Soliquid · Anton Klinger».
- YouTube: пошук «Soliquid puzzlescript».

## Непевне
- (?) Семантику «тягнеться до 3 / сплющується на 1» виведено з правил коду й звірено з GIF; рідкісні випадки (частковий упор разом із ящиком) у грі не перевірено.
- (?) Ящик штовхає «голова» будь-якої лінії тіла; чи може ящик заїхати в клітину, де теж стоїть тіло, — за кодом так (умова лише «нема стіни чи ящика»), не перевірено.
- (?) Клавіші Z / R — стандарт PuzzleScript, у коді не задані.
