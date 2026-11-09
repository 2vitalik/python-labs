---
title: Tempest
slug: tempest
aka: [Темпест]
family: maze-arcade
also: [tower-lanes]
klass: avatar
axes:
  field: 1d
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: score
year: 1981
platforms: [arcade, BBC Micro, Acorn Electron, ZX Spectrum, Amstrad CPC, Atari ST, Atari 5200]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tempest_(video_game)", best: true, note: "труба зі смуг, кіготь на ободі, 7 типів ворогів, Superzapper, варп, SkillStep, 16 форм"}
  - {kind: other, url: "https://www.arcade-museum.com/Videogame/tempest", note: "KLOV: інструкція з автомата, Superzapper 1/2/0, умова кінця рівня, зелені рівні з 81, перекрут рахунку"}
  - {kind: other, url: "https://arcade-museum.com/dipswitch-settings/tempest", note: "DIP: 2–5 життів, бонус кожні 10–70 тис., складність, діапазон стартового рівня"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Tempest+arcade+1981", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-by-input, wrap-edges, projectile-shot, shoot-forward, projectile-collision, touch-death, player-death, spawn-points, destroy-all-enemies, sequential-levels, progress-acceleration, level-select, extra-life-threshold, event-points, score-records, leaderboard, attract-demo, difficulty-levels, +lane-tube-field, +rotary-spinner-input, +superzapper, +splitting-enemy, +spike-trail, +warp-through-hazards, +capture-drag, +lane-electrify, +edge-jumper, +invisible-levels]
proposes: ["+axis:field=tube", "+effect:electrify(lane)", "+card:lane-tube-field", "+card:rotary-spinner-input", "+card:superzapper", "+card:splitting-enemy", "+card:spike-trail"]
author: opus
date: 2026-11-09
---

# Tempest — кіготь на ободі труби зі смуг: крути ручку, стріляй уздовж смуги, не пусти ворогів на обід

## Суть
Поле — тривимірна «труба», розрізана на смуги й видима з одного кінця; гравець — кіготь на ближньому ободі, що крутильною ручкою перескакує зі смуги на смугу й стріляє вглиб своєї смуги. Вороги вилазять з далекого кінця й повзуть смугами до обода; на ободі фліпери перекидаються вбік і хапають кіготь. Межова гра сімʼї: позиція гравця — лінія (кільце) смуг, глибина — неперервна; клітинної сітки нема, тому опис короткий. Родич смугових полів `tower-lanes`.

## Поле і час
- 16 різних форм поля: замкнені труби (кільце смуг, без країв) і відкриті поверхні з лівим і правим кінцем (пряма, «нескінченність» тощо).
- Позиція кігтя — номер смуги на ободі (`field: 1d`): замкнена — тор, відкрита — відрізок. Вороги мають ще й глибину в смузі.
- Real-time, векторний дисплей Color-QuadraScan. Після 16 форм цикл повторюється з новими кольорами й складністю; рівні 65–80 — «невидимі» (чорні), з 81 — зелені.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кіготь (Blaster) | player | смуга, Superzapper (2 заряди на рівень) | крок на сусідню смугу ручкою; швидкий вогонь уздовж смуги |
| Смуга | terrain | відкрита / замкнена труба | по ній іде весь рух углиб |
| Далекий кінець | spawner | — | вороги зʼявляються там закрученими точками, спершу по одному, далі частіше |
| Фліпер | enemy | — | повзе смугою; на ободі перекидається зі смуги на смугу, хапає й тягне кіготь углиб |
| Танкер | enemy | — | повільно повзе однією смугою; влучання або обід → ділиться на 2 фліпери |
| Танкер фузболів / пульсарів | enemy | — | пізні рівні; ділиться на 2 фузболи / 2 пульсари |
| Спайкер | enemy | — | спіраль ходить смугою вгору-вниз і лишає шип |
| Шип | hazard | довжина | стоїть у смузі; постріли його вкорочують; убиває при варпі |
| Фузбол | enemy | — | стрибає вздовж ребер смуг непередбачувано; дотик — смерть; між смугами повільний — вікно для пострілу |
| Пульсар | enemy | — | періодично електризує свою смугу; кіготь у ній гине |
| Ворожий постріл | projectile | — | летить смугою до обода (усі, крім фузболів і пульсарів) |
| Постріл гравця | projectile | — | летить углиб смуги; збиває ворогів і ворожі постріли |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(spin)` → ТО `move(claw, ±1 lane)`; ЯКЩО `custom: «труба замкнена»` → ТО `wrap(claw)` на кінцях; інакше на краю `block`.
- КОЛИ `input(fire)` → ТО `spawn(shot)` углиб своєї смуги.
- КОЛИ `contact(shot, enemy|enemy_shot)` → ТО `disappear_both`, `score(n)`.
- КОЛИ `contact(shot, tanker)` → ТО `split(tanker)` на 2 фліпери (фузболи / пульсари); те саме КОЛИ `reach(tanker, rim)`.
- КОЛИ `reach(flipper, rim)` → ТО `custom: «перекидається вздовж обода до кігтя»`; КОЛИ `contact(flipper, claw)` → ТО `custom: «тягне кіготь на дно»`, `lives(-1)`.
- КОЛИ `custom: «спайкер пройшов смугою»` → ТО `grow(spike, +n)`; КОЛИ `contact(shot, spike)` → ТО `shrink(spike, 1)`.
- КОЛИ `timer(pulse)` → ТО `custom: «пульсар електризує смугу»` (`+effect:electrify`); ЯКЩО `occupied(lane, claw)` → ТО `lives(-1)`.
- КОЛИ `contact(fuseball|enemy_shot, claw)` → ТО `lives(-1)`.
- КОЛИ `input(superzap)` → ЯКЩО `counter(zaps, ==, 0)` → ТО `disappear(all_enemies)`; ЯКЩО `counter(zaps, ==, 1)` → ТО `disappear(random_enemy)`; третій раз — нічого. КОЛИ `level_start` → ТО `custom: «Superzapper перезаряджено»`.
- КОЛИ `all_gone(enemy)` (або на ободі лишились самі фліпери) → ТО `custom: «варп: кіготь летить углиб і за край поля»`.
- КОЛИ `contact(claw, spike)` під час варпу → ТО `lives(-1)`, `custom: «варп заново»`; інакше `next_level`.
- КОЛИ `counter(score, >=, bonus_step)` → ТО `lives(+1)` (не більше 6 запасних).
- КОЛИ `counter(lives, ==, 0)` → ТО `game_over`.
- Перемога: нема — нескінченний цикл форм. · Поразка: усі життя втрачено. · Рахунок: очки за ворогів; рахунок перекручується після 999 999.

## Керування і ввід
- Оптична крутильна ручка (як у Pong): за / проти годинникової — смуга вліво / вправо.
- Кнопки Fire і Superzap; 1–2 гравці по черзі.

## Вікна, меню, HUD
- `attract-demo` — демо (є режим Demonstration-Freeze).
- `level-select` — SkillStep: на старті вибір стартового рівня з діапазону (1, 3, 5, 7, 9 або залежно від рекорду); перша гра з такою функцією.
- `game-screen`: труба; HUD — `score`, `hi-score`, `lives`, `level-number`.
- `leaderboard` — таблиця рекордів (обнуляється в test mode).
- `custom-window` — test mode оператора (перегляд параметрів).
- Переходи: демо → монета → SkillStep → рівень → (усі знищені) варп → наступний рівень → … → game over → рекорди.

## Фічі поза полем
- `operator-settings`: 2–5 життів, бонус-життя кожні 10–70 тис. або ніколи, складність Easy / Medium / Hard (швидкість ворогів, кількість пострілів, +1 ворог на полі), діапазон SkillStep, мова EN / FR / DE / ES.
- `level-unlock`-подібне: SkillStep дає стартувати вище й «продовжити» минулу гру.
- Чіт-коди через рахунок у таблиці рекордів (test mode, старт з будь-якого рівня до 81).

## Варіації й родичі
- Tempest 2000 (1994, Jeff Minter, Jaguar; на PS — Tempest X3), TxK → Tempest 4000 (2018) — та сама труба з павер-апами.
- [Space Invaders](space-invaders.md), [Centipede](centipede.md) — «стріляй угору своєю колонкою»; тут колонки згорнуті в трубу, а вороги виходять на обід.
- Смугові поля `tower-lanes` (PvZ): ворог іде смугою до краю, але там гравець ставить вежі, а не бігає ободом.
- **Осі варіацій:** топологія смуг (відрізок / кільце); що буває на краю (ворог проходить / перекидається ободом / розщеплюється); бомба (нема / Superzapper 1 повний + 1 частковий).

## Цікавинки для курсу
- Поле «N смуг × глибина» з кільцевою або відкритою топологією на тому ж коді — 📎.
- Розщеплення танкера на два вороги, зокрема коли той дійшов до обода — 🌱.
- Шип як слід, що вкорочується пострілами й убиває при варпі — 📎.
- Superzapper з двома різними зарядами на рівень — 🌱.
- Ввід ручкою: кутова дельта → крок по смугах — 🌱 (на клавіатурі — колесо миші).
- Варп-фаза між рівнями як міні-гра ухилянь — 📎.

## Мапа на каталог
- Є: `move-by-input` · `wrap-edges` (замкнена труба) · `projectile-shot` + `shoot-forward` · `projectile-collision` · `touch-death` + `player-death` · `spawn-points` (далекий кінець) · `destroy-all-enemies` · `sequential-levels` + `progress-acceleration` · `level-select` (SkillStep) · `extra-life-threshold` · `event-points` · `score-records` + `leaderboard` · `attract-demo` · `difficulty-levels`.
- **Нема** → пропозиції карток:
  - `+lane-tube-field` «Поле: N смуг з глибиною, кільце або відрізок» · levels/field · 📎 · слоти {lanes, closed}.
  - `+rotary-spinner-input` «Крутильна ручка: дельта кута → крок» · interface/input · 🌱.
  - `+superzapper` «Розумна бомба з повним і частковим зарядом на рівень» · entities/combat · 🌱 · слот {charges}.
  - `+splitting-enemy` «Ворог ділиться на два при влучанні або на краю» · entities/spawn · 🌱.
  - `+spike-trail` «Ворог лишає шип у смузі; постріли вкорочують» · entities/interact · 📎.
  - `+warp-through-hazards` «Перехід між рівнями — політ крізь лишені пастки» · levels/progression · 📎.
  - `+capture-drag` «Ворог хапає й тягне гравця» · entities/combat · 🌱.
  - `+lane-electrify` «Періодично смертельна смуга» · entities/hazard · 🌱.
  - `+edge-jumper` «Ворог ходить ребрами між смугами» · entities/move · 🌱.
  - `+invisible-levels` «Рівні без видимого поля» · levels/progression · 🌱.

## Пропозиції до словників
- `+axis:field=tube` — смуги навколо осі з глибиною: позиція на ободі 1d + неперервна глибина (Tempest, Gyruss-подібні).
- `+effect:electrify(lane)` — смуга/клітина на час стає смертельною (пульсар).
- `+card:lane-tube-field`, `+card:rotary-spinner-input`, `+card:superzapper`, `+card:splitting-enemy`, `+card:spike-trail` — див. вище.

## Джерела
- ⭐ [Wikipedia: Tempest](https://en.wikipedia.org/wiki/Tempest_(video_game)) — поле зі смуг (замкнене / відкрите), кіготь і ручка, сім типів ворогів з поведінкою, Superzapper, варп і шипи, 16 форм і цикл кольорів, невидимі рівні 65–80, SkillStep, до 6 запасних життів, порти й сиквели.
- [KLOV: Tempest](https://www.arcade-museum.com/Videogame/tempest) — інструкція: вороги знизу, кінець рівня (знищено всіх або на ободі лише фліпери), шипи, Superzapper 1 / обмежений / 0, зелені рівні з 81, кнопки, коди таблиці рекордів, перекрут рахунку.
- [KLOV: DIP-перемикачі](https://arcade-museum.com/dipswitch-settings/tempest) — життя, бонус-життя, мова, складність, діапазон стартового рівня, демо-режими.
- YouTube: пошук «Tempest arcade 1981».

## Непевне
- (?) Кількість смуг на поле (у черзі — 16): джерела кажуть лише «16 форм»; число смуг у кожній формі не перевірено.
- (?) Очки за кожного ворога і бонус SkillStep за старт з вищого рівня — у відкритих джерелах нема.
- (?) «Після кількох перших рівнів шипи в кожній смузі» — формулювання Wikipedia непевне; спавн після рівня 99 — з позначкою «потрібне джерело».
- (?) `random: runtime` — за фузболами («непередбачувано»); чи порядок появи ворогів випадковий — не перевірено.
