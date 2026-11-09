---
title: Kirby's Star Stacker
slug: kirbys-star-stacker
aka: [カービィのきらきらきっず, Kirby no Kirakira Kids, Kirby's Super Star Stacker]
family: falling-match
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: collect
year: 1997
platforms: [Game Boy, Super Famicom, Wii VC, 3DS VC, Switch Online]
links:
  - {kind: other, url: "https://wikirby.com/wiki/Kirby%27s_Star_Stacker_(Game_Boy)", best: true, note: "WiKirby: доміно-пари, друзі, зіркові/тверді/бомби, ланцюг дає 2…12 зірок, ряди Dedede, режими й розблокування"}
  - {kind: other, url: "https://wikirby.com/wiki/Kirby%27s_Super_Star_Stacker", note: "SFC-ремейк: Story з 8 суперниками, HP Dedede = квота зірок, Challenge до 9999"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Kirby%27s_Star_Stacker", note: "огляд, режими, дати, SFC Kirakira Kids"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/カービィのきらきらきっず", note: "JA: друзі, що торкаються, зникають; точна таблиця зірок за ланцюгом; Story; складності"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Kirby%27s+Star+Stacker+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [gravity-fall, multi-cell-size, keyboard-controls, chain-reaction, collect-quota, difficulty-levels, level-unlock, mode-select, time-out, score-records, garbage-attack, simultaneous-versus, ai-opponent, +pair-match-removal, +sandwich-clear, +split-on-landing, +rising-stack, +row-clear-bomb, +chain-reward-drop, +artwork-unlock]
proposes: ["+cond:sandwiched", "+effect:raise_stack", "+card:sandwich-clear", "+card:chain-reward-drop"]
author: opus
date: 2026-11-09
---

# Kirby's Star Stacker — зірка зникає, лише коли її затиснуто між двома однаковими друзями

## Суть
Згори падають доміно-пари з блоків трьох «друзів» Кірбі (Рік, Кайн, Ку) і зірок. Два однакові друзі, що торкаються, зникають; якщо між ними в лінію стоять зірки, зірки зникають разом і йдуть у лічильник — це й є очки. Тож зірка сама по собі — сміття, її треба «взяти в дужки». Ланцюги скидають з неба нові зірки, які оживають лише там, де приземлились між двома друзями, а тим часом King Dedede підіймає стос знизу.

## Поле і час
- Прямокутне поле; нові пари зʼявляються в двох центральних стовпцях; ширина — ймовірно 6 (JA: ланцюг на 5 скидає 6 зірок «на весь ряд») (?).
- Real-time: пара падає; приземлившись, розпадається, і кожен блок падає окремо (гравітація на клітину).
- Тиск: за інтервалом знизу підіймається новий ряд і штовхає весь стос угору; частота — за складністю.
- Після зникнення — фаза осідання й ланцюгів, як у Puyo.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Доміно-пара | player | 2 блоки випадкових типів | зсув ←/→, поворот A (праворуч) / B (ліворуч), прискорене падіння; приземлилась → розпадається |
| Рік / Кайн / Ку (друзі) | tile | тип із 3 | два однакові, що торкаються, зникають; два однакові з зірками між ними — зникають разом із зірками |
| Зіркова плитка | tile | — | сама не зникає; зараховується, коли затиснута між двома однаковими друзями |
| Твердий блок (камінь) | tile | — | затиснутий між однаковими друзями — стає зірковою плиткою |
| Бомба | tile | — | затиснута між однаковими друзями — стирає весь свій ряд |
| Зірки-нагорода | pickup | 2 / 4 / 5 / 6 / 12 за ланцюг 2 / 3 / 4 / 5 / 6+ | падають у проміжки; приземлилась між двома друзями — стає зірковою плиткою й продовжує комбо; інакше зникає |
| Ряд знизу (Dedede / рука / Tick-Tock Jr.) | spawner | інтервал за складністю | додає ряд знизу, стос піднімається |
| Два центральні стовпці | zone | точка спавну | заповнились догори → Game Over |
| King Dedede (Round Clear, SFC) | boss | HP = квота зірок | кожна зірка знімає HP; 0 → раунд пройдено |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ЯКЩО `free(cells_below)` → ТО `move(pair, down)`.
- КОЛИ `input(left|right)` → ЯКЩО `free(target)` → ТО `move(pair, dir)`.
- КОЛИ `input(a|b)` → ЯКЩО `free(new_cells)` → ТО `rotate(pair, ±90)` — A праворуч, B ліворуч.
- КОЛИ `input(down)` → ТО `speed(pair, ×k)`.
- КОЛИ `locked(pair)` → ТО `split(pair)`, `fall(block)` — кожен блок окремо.
- КОЛИ `settled` → ЯКЩО `adjacent_count(friend, same_friend, ≥, 1)` → ТО `clear(group)`.
- КОЛИ `settled` → ЯКЩО `custom: «між двома однаковими друзями в лінію стоять лише зіркові плитки»` → ТО `clear(friends_and_stars)`, `counter(stars, +n)`.
- КОЛИ `settled` → ЯКЩО `custom: «твердий блок затиснуто між двома однаковими друзями»` → ТО `clear(friends)`, `transform(hard_block, star)`.
- КОЛИ `settled` → ЯКЩО `custom: «бомбу затиснуто між двома однаковими друзями»` → ТО `clear(row)`.
- КОЛИ `after(clear)` → ТО `fall(unsupported)`.
- КОЛИ `settled` → ЯКЩО `chain(n)` → ТО `spawn_at(falling_stars, gaps)` — 2 зірки за ланцюг 2, 4 за 3, 5 за 4, 6 за 5, 12 за 6+.
- КОЛИ `enter(falling_star, cell)` → ЯКЩО `custom: «клітина між двома однаковими друзями»` → ТО `transform(falling_star, star_block)` — інакше зірка зникає.
- КОЛИ `timer(rise_interval)` → ТО `custom: «raise_stack — новий ряд знизу піднімає стос»`.
- КОЛИ `reach(stack, top_center)` → ТО `lose` — і нові пари більше не зʼявляються.
- Round Clear: КОЛИ `counter(stars, ≥, quota)` → ТО `win`, `next_level`, `unlock(artwork)`.
- Time Attack: КОЛИ `counter(time_left, ==, 0)` → ТО `game_over` — ліміт 3 хвилини.
- Challenge (SFC): КОЛИ `counter(stars, ≥, 9999)` → ЯКЩО `mode(challenge)` → ТО `game_over`.
- VS / Story: КОЛИ `settled` → ЯКЩО `chain(n)` → ТО `send_garbage(rows)` — ряди знизу в поле суперника.
- Розблокування: КОЛИ `counter(stars, ≥, 100)` → ЯКЩО `mode(time_attack)` → ТО `unlock(insane)`; у Challenge поріг 1000.
- Перемога: Round Clear — квота зірок раунду; VS — суперник отримав Game Over. · Поразка: центральні стовпці заповнені. · Рахунок: кількість зібраних зірок (лічильник праворуч).

## Керування і ввід
- Хрестовина ←/→ — зсув пари; ↓ — прискорене падіння; A — поворот праворуч, B — ліворуч (WiKirby); функція ↑ — (?).
- VS: два Game Boy через Link Cable, дві касети; гравець 1 — Кірбі, гравець 2 — Waddle Dee.

## Вікна, меню, HUD
- `splash-screen` — титул.
- `mode-select`: Round Clear · Challenge · Time Attack · VS (SFC — ще Story).
- `difficulty-select`: Normal · Hard · Very Hard · Super Hard · Insane (прихована до розблокування).
- `game-screen`: поле, ліворуч/праворуч — анімований антагоніст режиму (Dedede, рука, Tick-Tock Jr., Mr. Star); `score` — лічильник зірок праворуч; `hp-bar` Dedede (SFC Round Clear); `next-piece-preview` — (?).
- `leaderboard` — топ-3 для Challenge і Time Attack.
- `end-screen` — Stage Clear / Game Over.
- `custom-window` — галерея відкритих картинок (Round Clear за раунди, Challenge за 50+ зірок) (?).
- Super Game Boy — рамка, що змінюється після повного проходження.
- Переходи: splash → mode-select → difficulty-select → game-screen → (квота) Stage Clear → наступний раунд / (поразка) Game Over → records.

## Фічі поза полем
- `difficulty-presets` 5 рівнів; Insane — `level-unlock` за порогами (Time Attack ≥100 зірок, Challenge ≥1000; SFC: Time Attack ≥150, VS — 30 перемог).
- `unlockables`: тематичні картинки за раунди й пороги зірок.
- `leaderboard-local` топ-3 у двох режимах.
- `mode-versus` через Link Cable; SFC — `ai-opponent-levels`: Story з 8 суперниками (Amateur / Professional), VS на 1 / best of 3 / best of 5.
- SFC (Kirby no Kirakira Kids, 1998/1999, лише Японія) — «майже ідентичний» ігролад + Story; у Story ряд із двох однакових друзів теж зчищується.

## Варіації й родичі
- GB (1997) → SFC-ремейк з Story; Wii VC, 3DS VC, Nintendo Classics.
- Родичі: Puyo Puyo (`puyo-puyo`, пара + каскад), Yoshi (`yoshi-nes`, половинки шкаралупи замикають ворогів між собою — «дужки» по вертикалі), Wario's Woods (`warios-woods`, монстрів прибирає лише бомба-каталізатор), Reversi (захоплення затисканням).
- **Осі варіацій**: що зчищує (група кольору / **затискання між двома однаковими**) · що затискається (зірка → очки / камінь → зірка / бомба → ряд) · нагорода за ланцюг (множник / **падаючі зірки, що оживають лише в «дужках»**) · тиск (стеля / ряд знизу).

## Цікавинки для курсу
- Перевірка «затиснуто між двома однаковими» по рядку й стовпцю (сканування від друга до друга через зірки) — 📎.
- Ланцюг, що скидає нагороду, яка оживає лише в правильних місцях (рекурсивний каскад) — 🥉.
- Пара, що розпадається при приземленні, + гравітація на клітину — 🌱.
- Ряд знизу за таймером, що піднімає стос — 🌱.
- Три типи «начинки» сендвіча з різним ефектом (зірка / камінь / бомба) — 📎.
- AI-суперник для VS/Story: пошук ходу з найдовшим ланцюгом — 🥈.

## Мапа на каталог
- Є: `gravity-fall` · `multi-cell-size` (доміно 1×2) · `keyboard-controls` · `chain-reaction` · `collect-quota` (зірки раунду) · `difficulty-levels` · `level-unlock` (Insane) · `mode-select` · `time-out` (Time Attack) · `score-records` (топ-3) · `garbage-attack` + `simultaneous-versus` (VS) · `ai-opponent` (SFC Story).
- **Нема** → пропозиції карток:
  - `+sandwich-clear` «Зчищення затисканням між двома однаковими» · entities/interact · 📎 · слоти {filler: star|rock|bomb, dirs: 2|4}.
  - `+chain-reward-drop` «Ланцюг скидає нагороду, що оживає лише в правильних клітинах» · game-logic/score · 🥉 · слот {table}.
  - `+row-clear-bomb` «Бомба стирає свій ряд» · entities/interact · 🌱.
  - `+artwork-unlock` «Картинки галереї за пороги» · levels/progression · 🌱.
  - `+pair-match-removal` · `+split-on-landing` · `+rising-stack` — теги вже є в корпусі.

## Пропозиції до словників
- `+cond:sandwiched` — сутність затиснута між двома однаковими по лінії (пропозиція вже є в корпусі — підтверджую).
- `+effect:raise_stack` — знизу додається ряд, стос піднімається (пропозиція вже є — підтверджую).
- `+card:sandwich-clear`, `+card:chain-reward-drop` — див. «Мапу».

## Джерела
- ⭐ [WiKirby: Kirby's Star Stacker (Game Boy)](https://wikirby.com/wiki/Kirby%27s_Star_Stacker_(Game_Boy)) — доміно-пари й розпад, друзі, зіркові/тверді/бомби, ланцюг 2…12 зірок, ряди Dedede, Game Over центральних стовпців, усі режими, пороги розблокування, топ-3, керування A/B.
- [WiKirby: Kirby's Super Star Stacker](https://wikirby.com/wiki/Kirby%27s_Super_Star_Stacker) — SFC: Story з 8 суперниками, HP Dedede, Challenge до 9999, VS best of 3/5, пороги Insane.
- [Wikipedia: Kirby's Star Stacker](https://en.wikipedia.org/wiki/Kirby%27s_Star_Stacker) — суть, режими, дати, SFC-версія.
- [JA Wikipedia: カービィのきらきらきっず](https://ja.wikipedia.org/wiki/カービィのきらきらきっず) — друзі, що торкаються, зникають; таблиця зірок за ланцюгом; камінь і бомба; ряди в поле суперника; складності.
- YouTube: пошук «Kirby's Star Stacker gameplay».

## Непевне
- (?) Напрям затискання — лише по горизонталі й вертикалі чи й по діагоналі (джерела не кажуть; з памʼяті — без діагоналей).
- (?) Ширина поля (6 — висновок з JA «6 зірок на весь ряд»), висота, наявність превʼю наступної пари.
- (?) Набір складностей: WiKirby GB — Normal…Insane (5), JA — Normal, Hard, Super, прихований Mega Super і Easy лише на GB.
- (?) Квоти зірок для раундів, кількість раундів, інтервал рядів знизу.
- (?) Чи двоє однакових друзів, що торкаються, зникають і на GB (JA — так; WiKirby SFC — «у Story також»), і чи це дає зірки.
