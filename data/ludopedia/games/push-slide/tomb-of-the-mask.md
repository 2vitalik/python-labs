---
title: Tomb of the Mask
slug: tomb-of-the-mask
family: push-slide
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: setup
  goal: survive
year: 2016
platforms: [iOS, Android, Switch, Apple Arcade (Tomb of the Mask+)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tomb_of_the_Mask", best: true, note: "свайп до стіни, точки й монети, шипи/пастки/риба-їжак, приплив знизу, магніт і заморозка, Arcade vs Stage, маски"}
  - {kind: official, url: "https://happymagenta.com/tomb-of-the-mask/index.html", note: "сайт Happymagenta: нескінченний процедурний вертикальний лабіринт"}
  - {kind: other, url: "https://apps.apple.com/app/tomb-of-the-mask/id1057889290", note: "App Store: опис і історія версій (події, маски зі здібностями, змія-переслідувач)"}
  - {kind: other, url: "https://play.google.com/store/apps/details?id=com.playgendary.tom", note: "Google Play"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=tomb+of+the+mask+gameplay", note: "пошук; геймплей Arcade і Stage"}
stage: v1
coverage: 65
mechanics: [inertia-slide, swipe-gestures, impassable-cells, item-pickup, reach-exit, touch-death, environment-death, enemy-patrol, temporary-modes, round-currency, shop-between-levels, shop-catalog, avatar-picker, infinite-field, player-camera, event-points, leaderboard, sequential-levels, level-unlock, +rising-hazard, +freeze-all-enemies, +coin-magnet, +toggle-spikes, +continue-for-ad, +stage-stars]
proposes: ["+trigger:input", "+trigger:blocked", "+trigger:timer", "+effect:slide", "+effect:currency", "+effect:set_state", "+effect:freeze", "+role:hazard", "+role:terrain", "+role:projectile", "+ui:coins", "+ui:distance", "+window:game-over-continue", "+window:mode-select", "+feature:stars-rating", "+feature:ad-revive", "+axis:session", "+card:rising-hazard"]
author: opus
date: 2026-11-02
---

# Tomb of the Mask — свайп: маска летить до стіни; збирай точки, тікай від припливу

## Суть
Герой у масці «прилипає» до стін: свайп у бік — він миттєво летить по прямій, доки не вдариться в стіну, і зупиняється біля неї. По дорозі збирає точки (очки) і монети (валюта), ухиляючись від шипів, пасток-дротиків і ворогів. В Arcade-режимі лабіринт процедурний і нескінченний угору, а знизу безупинно піднімається смертельний приплив — гра стає real-time перегонами з плануванням маршруту з кількох ковзань. Ядро — `inertia-slide` у real-time: між ковзаннями думати можна, але приплив не чекає.

## Поле і час
- Квадратна сітка-лабіринт у піксельній графіці, вузька (на ширину екрана телефона) і висока; камера скролиться вгору за героєм (`player-camera`), видно лише шматок лабіринту — `info: partial`.
- Arcade: процедурна генерація вертикального лабіринту на льоту (`infinite-field`); Stage (з v1.2, 2016): фіксовані рівні з виходом, згодом 146+ рівнів.
- Час real-time: ковзання дуже швидке, але не миттєве; вороги й пастки мають власний тік/цикл; приплив піднімається рівномірно (?) і пришвидшується (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой у масці | player | маска (скін/здібність) | свайп → `slide` до стіни; зупиняється, «прилипнувши» до стіни |
| Стіна | static | — | зупиняє ковзання; до неї «чіпляється» герой |
| Точка (dot) | pickup | — | +очки; у Stage — частина зірки/повноти рівня (?) |
| Монета | pickup | — | +1 валюта (магазин масок і апгрейдів) |
| Зірка | pickup | 3 на рівень (?) | Stage: рейтинг рівня |
| Шипи (статичні) | hazard | сторона стіни | контакт → смерть |
| Шипова пастка | hazard | період висування | шипи висуваються й ховаються циклічно; висунуті — смерть |
| Пастка-стрілець (дротики) | spawner | напрям, період | стріляє дротиками вздовж лінії |
| Дротик | projectile | напрям | летить по прямій; контакт → смерть; зникає об стіну |
| Риба-їжак (pufferfish) | hazard | цикл | періодично роздувається на сусідні клітини (?) |
| Кажан / літаючий ворог | enemy | маршрут | патрулює туди-сюди (?) |
| Рухома стіна / блок-обличчя | hazard | — | зсувається; може розчавити (?) |
| Приплив (tide / лава) | hazard | швидкість | піднімається знизу екрана; торкнувся героя → кінець гри |
| Змія / котуча куля (Stage, пізніші версії) | enemy | — | переслідує ззаду; треба втекти до виходу |
| Магніт | pickup (power-up) | тривалість | притягує монети з околиць |
| Заморозка | pickup (power-up) | тривалість | зупиняє ворогів |
| Щит | pickup (power-up) | 1 удар (?) | переживає один контакт із небезпекою (?) |
| Вихід (Stage) | static | — | кінець рівня |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(swipe_dir)` → ЯКЩО `custom: «герой стоїть (не в польоті)»` → ТО `slide(hero, dir)`.
- КОЛИ `blocked(hero)` → ТО `custom: «зупинитись і прилипнути до стіни»` — нова точка вибору.
- КОЛИ `contact(hero, dot)` → ТО `pickup`, `score(+n)`.
- КОЛИ `contact(hero, coin)` → ТО `pickup`, `currency(+1)`.
- КОЛИ `contact(hero, spikes|dart|enemy)` → ЯКЩО `not state(hero, shield)` → ТО `lose`; інакше `clear_state(hero, shield)` (?).
- КОЛИ `timer(trap_period)` → ТО `set_state(spike_trap, extended|retracted)`; КОЛИ `contact(hero, spike_trap)` → ЯКЩО `state(spike_trap, extended)` → ТО `lose`.
- КОЛИ `timer(shooter_period)` → ТО `spawn(dart)` у напрямку стрільця; дротик `blocked` → `disappear_a`.
- КОЛИ `tick` → ТО `custom: «рівень припливу +v»`; КОЛИ `contact(hero, tide)` → ТО `lose`.
- КОЛИ `contact(hero, magnet)` → ТО `set_state(hero, magnet, duration)`; поки активний — `custom: «монети в радіусі летять до героя»`.
- КОЛИ `contact(hero, freeze)` → ТО `freeze(all_enemies, duration)`.
- КОЛИ `contact(hero, exit)` (Stage) → ТО `win`, зірки за зібране (?), `next_level`.
- КОЛИ `custom: «смерть»` → ТО `window(game-over-continue)`: продовжити за рекламу/монети або кінець забігу.
- Перемога: Stage — вихід; Arcade — нема, лише рекорд. · Поразка: дотик до небезпеки або припливу. · Рахунок: Arcade — очки за точки й дистанцію вгору (два онлайн-лідерборди: score і distance); монети — окрема валюта.

## Керування і ввід
- Свайп у 4 напрямки (тач) — `swipe-zone` на весь екран; Switch — стік або D-pad.
- Ввід під час польоту ігнорується (?) — новий напрям лише після зупинки об стіну; звідси «планування з 1–2 ковзань наперед».
- Додаткових кнопок на полі нема; пауза — кнопка в куті.

## Вікна, меню, HUD
- `splash-screen` → `main-menu`: Arcade · Stage · маски · магазин · налаштування.
- `mode-select`: Arcade (нескінченний) / Stage (рівні) — на головному екрані.
- `level-select` (Stage): рівні з позначками зірок, послідовне відкриття (`level-unlock`).
- `game-screen`: лабіринт, HUD — `score`, `coins`, `distance` (?), активні power-up-и з таймером (`inventory-duration`), `pause-button`.
- `pause-menu`: продовжити, вихід, звук.
- `game-over-continue`: «продовжити?» за перегляд реклами або валюту.
- `end-screen`: очки, рекорд, монети за забіг; Stage — зірки.
- `shop-window`: маски (16+ у Wikipedia, з v1.17 — зі здібностями), апгрейди power-up-ів (довша дія), пакети валюти за гроші.
- `achievements-window` (Game Center / Google Play, 60 досягнень), `leaderboard` (онлайн, score і distance).
- `settings-window`: звук, музика.
- Переходи: main-menu → Arcade → game-screen → (смерть) game-over-continue → end-screen → main-menu; main-menu → Stage → level-select → game-screen → (вихід) end-screen → наступний рівень.

## Фічі поза полем
- `mode-endless` (Arcade) + `levels-sequential`/`level-unlock` (Stage) + `stars-rating`.
- `meta-progression`: монети → постійні апгрейди сили power-up-ів, маски-скіни (`unlockables`), маски зі здібностями (з v1.17).
- `leaderboard-online` (два), `achievements`.
- Подієві режими пізніх версій: Boss Clash, Color Quest, Fortune Maze, Word of the Day, «idle income» — `custom` (живий сервіс).
- Монетизація: реклама за продовження, покупка валюти, Remove Ads, VIP-пакет масок.
- Нема undo, редактора; Apple Arcade-версія Tomb of the Mask+ без реклами (?).

## Варіації й родичі
- Осі варіацій ковзання: **хто ковзає** — аватар (ToTM, Ice-пазли Pokémon) / фігури (Ricochet Robots, Atomix) / усе поле (2048); **що зупиняє** — стіна / стіна і сутності / спецклітина-«гальмо»; **час** — покроково (пазл) / real-time з тиском (ToTM).
- **Тиск часу**: приплив знизу (ToTM) / таймер рівня (Chip's Challenge) / переслідувач ззаду (змія ToTM Stage, Frogger-«idle punisher») — одна вісь «що змушує рухатися».
- Родичі: Pac-Man (точки на маршруті), Chip's Challenge (лід = ковзання), Ricochet Robots, Pengo (ковзний блок), endless-climbers (Doodle Jump) за структурою сесії. Наступник від тих самих авторів — Tomb of the Mask: Color (?) не перевірено.

## Цікавинки для курсу
- Ковзання аватара до стіни з підбором предметів на шляху (перебір клітин траси) — 🌱 у покроковому, 📎 з анімацією і вводом «лише в стані спокою».
- Приплив, що піднімається (рядок смерті росте з тіком), + камера вгору — 🥉: перша real-time механіка тиску без ворогів.
- Процедурний нескінченний вертикальний лабіринт з гарантією прохідності для ковзання (граф «зупинок» біля стін, BFS по ньому) — 🥇: досяжність для `inertia-slide` інша, ніж для кроку.
- Циклічні шипи й стрільці дротиками (стан на N тіків) — 📎.
- Power-up-и з тривалістю (магніт — притягання в радіусі, заморозка — пауза ворогів) — 📎 кожен.
- Магазин масок + постійні апгрейди за валюту з забігів — 🥉.

## Мапа на каталог
- Є: `inertia-slide` ↔ ковзання до стіни; `swipe-gestures` ↔ свайп; `impassable-cells` ↔ стіни; `item-pickup` ↔ точки, монети; `reach-exit` ↔ вихід рівня; `touch-death` + `environment-death` ↔ шипи, вороги, приплив; `enemy-patrol` ↔ кажани; `temporary-modes` ↔ power-up-и з тривалістю; `round-currency` ↔ монети; `shop-between-levels` + `shop-catalog` ↔ маски й апгрейди; `avatar-picker` ↔ маски; `infinite-field` ↔ Arcade; `player-camera` ↔ скрол угору; `event-points` + `leaderboard`; `sequential-levels` + `level-unlock` ↔ Stage.
- **Нема** → пропозиції карток:
  - `+rising-hazard` «Смертельна межа наступає» · game-logic/lose · 🥉 · слот {speed, accel} — приплив/лава/стіна, що наздоганяє.
  - `+freeze-all-enemies` (вже пропонована Q*bert) — заморозка ворогів.
  - `+coin-magnet` «Магніт: предмети в радіусі летять до гравця» · entities/interact · 📎 · слоти {radius, duration}.
  - `+toggle-spikes` «Шипи, що циклічно висуваються» · entities/state · 📎 · слот {period, phase} — також Helltaker.
  - `+continue-for-ad` «Продовження після смерті за рекламу/валюту» · game-logic/economy · 🌱.
  - `+stage-stars` «Зірки рівня за повноту збору» · levels/progression · 🌱 — дитина `stars-rating`-фічі.

## Пропозиції до словників
- `+trigger:input` — свайп; `+trigger:blocked` — зупинка об стіну; `+trigger:timer` — цикли пасток.
- `+effect:slide`; `+effect:currency` — монети; `+effect:set_state` — шипи висунуто/сховано, щит, магніт; `+effect:freeze` — заморозка ворогів.
- `+role:hazard` — шипи, приплив, риба-їжак; `+role:terrain`; `+role:projectile` — дротики.
- `+ui:coins`; `+ui:distance` — пройдена висота як окрема метрика рекорду.
- `+window:game-over-continue` — «продовжити?» за рекламу; `+window:mode-select` — Arcade/Stage.
- `+feature:stars-rating`; `+feature:ad-revive` — продовження за рекламу як мобільна фіча.
- `+axis:session` — `endless` (Arcade) і `level` (Stage) в одній грі.
- `+card:rising-hazard`.

## Джерела
- ⭐ [Wikipedia: Tomb of the Mask](https://en.wikipedia.org/wiki/Tomb_of_the_Mask) — свайп до упору, точки й монети, Spikes / Spike traps / Pufferfish, приплив знизу (у Arcade — ще й лава), магніт і заморозка, перки за монети, Arcade (два лідерборди, 60 досягнень) і Stage, 16 масок, платформи.
- [Happymagenta: Tomb of the Mask](https://happymagenta.com/tomb-of-the-mask/index.html) — офіційний опис: процедурний нескінченний вертикальний лабіринт.
- [App Store](https://apps.apple.com/app/tomb-of-the-mask/id1057889290) — опис, editors' note («постійно наступна смертельна стіна»), історія версій: маски зі здібностями, змія-переслідувач, події, idle income.
- [Google Play](https://play.google.com/store/apps/details?id=com.playgendary.tom) — Android-версія (опис не відкрився).
- YouTube: пошук «tomb of the mask gameplay».

## Непевне
- (?) Щит як power-up і його поведінка (поглинає один удар) — з памʼяті; Wikipedia називає лише магніт і заморозку.
- (?) Кажани, рухомі блоки, поведінка риби-їжака (роздування на сусідні клітини) — з памʼяті/відгуків; точного довідника елементів (фан-вікі) дістати не вдалося.
- (?) Як саме нараховуються зірки в Stage (точки / зірки на рівні) і чи приплив пришвидшується.
- (?) Чи можна змінити напрям у польоті — здається, ні.
- (?) Сиквели (Tomb of the Mask: Color / Neon) — не перевірено.
