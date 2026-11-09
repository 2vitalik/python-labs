---
title: Achtung, die Kurve! (Увага, поворот!)
slug: achtung-die-kurve
aka: [Zatacka, Achtung die Kurve, Curve Fever, Увага поворот]
family: maze-arcade
also: []
klass: avatar
axes:
  field: free
  time: realtime
  opponent: hotseat
  info: full
  random: runtime
  goal: survive
year: 1995
platforms: [Amiga, MS-DOS, web (ремейки), PC (Curve Fever Pro, Steam)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Achtung,_die_Kurve!", best: true, note: "правила: дві клавіші, мін. радіус повороту, дірки в сліді, останній живий"}
  - {kind: wiki, url: "https://de.wikipedia.org/wiki/Achtung,_die_Kurve!", note: "2–8 гравців, ціль (гравців−1)·10 очок, автори, Cervii, Curve Fever"}
  - {kind: play, url: "https://achtungkurve.com/", note: "браузерний ремейк: вибір гравців, клавіші ліво/право, суперсили"}
  - {kind: steam, url: "https://store.steampowered.com/app/1133700/Curve_Fever_Pro/", note: "сучасний онлайн-нащадок: до 10 гравців, 30 сил, режими, ранкед"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=achtung+die+kurve+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-auto, touch-death, spawn-random-cell, keyboard-controls, event-points, controls-remap, match-setup, game-screen, end-screen, online-multiplayer, rating-system, leaderboard, replay, item-pickup, temporary-modes, projectile-shot, +trail-wall, +trail-gaps, +relative-turn-controls, +free-angle-steering, +turn-radius-limit, +survival-points, +shared-keyboard-multiplayer, +shared-field-versus, +loadout-powerups]
proposes: ["+effect:leave_trail", "+effect:gap", "+trigger:player_out", "+cond:alive", "+window:player-join", "+ui:player-scoreboard", "+feature:target-score", "+card:trail-gaps", "+card:free-angle-steering", "+card:turn-radius-limit", "+card:survival-points", "+card:shared-keyboard-multiplayer", "+axis:control:direct-relative"]
author: opus
date: 2026-11-09
---

# Achtung, die Kurve! — «змійки» на одній клавіатурі: слід під будь-яким кутом, дірки в лінії, переживи всіх

## Суть
Від двох до восьми гравців за однією клавіатурою, кожен має лише дві клавіші — повернути ліворуч і праворуч. Крапка безупинно рухається зі сталою швидкістю й малює за собою постійну лінію свого кольору; поворот плавний, з мінімальним радіусом, тож різко розвернутися неможливо. Хто торкнувся рамки, своєї чи чужої лінії — вибув; раунд виграє останній живий. Час від часу в лінії сама собою зʼявляється дірка, крізь яку можна прослизнути — це рятує з пасток.

## Поле і час
- Вільне поле (не сітка): позиція — дійсні координати, напрям — кут; лінії — пікселі кольору власника. Тому `field: free`.
- Прямокутна арена з рамкою; дотик рамки = вибування (тору в оригіналі нема).
- Real-time: кожен кадр усі крапки зсуваються на сталу відстань; утримання клавіші повертає з обмеженою кутовою швидкістю.
- Раунд: старт у випадкових точках з випадковим напрямом; лінії лишаються до кінця раунду; новий раунд — чисте поле.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Крапка гравця («Kurve») | player | колір, 2 клавіші, кут | рух із сталою швидкістю; поворот із мін. радіусом; малює лінію |
| Лінія (слід) | static | власник | постійна до кінця раунду; дотик = вибування будь-кого, включно з власником |
| Дірка в лінії | terrain | — | короткий відрізок без сліду; прохідна |
| Рамка арени | static | — | дотик = вибування |
| Суперсила (ремейки, Curve Fever) | pickup | тип, тривалість | підбирається на полі: прискорення, сповільнення, інверсія керування, «гідра», імунітет тощо |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `spawn_at(dot, random)`, `face(dot, random)` для кожного гравця.
- КОЛИ `tick` → ТО `move(dot, heading)`, `custom: «пройдений відрізок стає лінією власника»`.
- КОЛИ `input(left|right)` (утримання) → ТО `rotate(dot, ±ω·dt)` — кутова швидкість обмежена.
- КОЛИ `rng(p)` → ТО `custom: «на короткий час крапка не малює лінію — утворюється дірка»`.
- КОЛИ `contact(dot, line|frame)` → ТО `disappear_a`, `custom: «лінія вибулого лишається на полі»`.
- КОЛИ `died(dot)` → ТО `score(+1)` кожному, хто ще живий.
- КОЛИ `count(alive_dots, ==, 1)` → ТО `level_end`, `custom: «новий раунд»`.
- КОЛИ `counter(score, >=, (players−1)·10)` → ТО `win` (кінець партії).
- Curve Fever / ремейки: КОЛИ `contact(dot, powerup)` → ТО `pickup`, `set_state(dot|others, power, duration)` — `speed(±)`, `invert_controls(n)`, `custom: «гідра: крапка розділяється»`.
- Перемога: першим набрати (гравців−1)·10 · Поразка: у раунді — дотик лінії/рамки · Рахунок: +1 за кожного суперника, якого пережив.

## Керування і ввід
- Кожному гравцю — пара клавіш «ліво/право» на спільній клавіатурі (оригінал використовує розкидані по клавіатурі пари; у DOS-версії гравець може грати й мишею (?)).
- Керування відносне: «ліво» = проти годинникової стрілки від поточного напряму.
- Перед партією гравці «входять», натиснувши свою клавішу; старт — пробіл (ремейк achtungkurve.com).

## Вікна, меню, HUD
- `match-setup` (`+window:player-join`): список кольорів-гравців з колонками «гравець · ліво · право · суперсила»; натиснув клавішу — увійшов; SPACE — старт.
- `game-screen`: арена ліворуч; праворуч `+ui:player-scoreboard` — очки кожного кольору й ціль партії.
- `end-screen`: переможець партії (DOS: напис «Konec hry»).
- Між раундами — пауза з оновленими очками (?).
- Curve Fever Pro: `main-menu` → `lobby-window` / Quick Play (ранкед) → вибір сил перед матчем → `game-screen` → `end-screen`; `replay-window`, друзі, чат.

## Фічі поза полем
- `local-multiplayer` / `hotseat` одночасний: до 6 (EN-Wikipedia, оригінал) або 2–8 (DE-Wikipedia) гравців на одній клавіатурі.
- `+feature:target-score` — довжина партії залежить від кількості гравців: (n−1)·10.
- Ремейк achtungkurve.com: суперсили (hydra, reverse) і система імунітету.
- Curve Fever Pro: `online-multiplayer` до 10 гравців, 30 сил на вибір перед матчем, режими Classic FFA / Classic Teams / Survival Teams / 1v1, `rating-system` (ліги, Grandmaster), кастомні кімнати (розмір мапи, очки, сили, турелі, модифікатори) — `custom-rules`, `replay`.

## Варіації й родичі
- Cervii (Чехія, 1993, DOS) — оригінал, клоном якого є Kurve; Achtung, die Kurve! 2 → Curve Fever → Curve Fever 3 (2016) → Curve Fever Pro (2018).
- Blockade (див. `blockade`) і Tron Light Cycles (див. `tron-light-cycles`) — той самий «слід = стіна», але на сітці з поворотами 90°.
- Snake (див. `snake`) — слід рухається за головою; тут він вічний.
- **Осі варіацій:**
  - повороти: 90° по сітці / 45° / плавні з мін. радіусом (Kurve);
  - слід: суцільний / з випадковими дірками / з кнопкою «стрибка» (сили Curve Fever);
  - рахунок: очко за виживання кожної смерті / за вбивства / командний;
  - сили: нема / підбір на полі / лоадаут перед матчем.

## Цікавинки для курсу
- Рух із кутом і сталою швидкістю, поворот з кутовою швидкістю — 📎: перехід від сітки до float-координат.
- Колізія лінії в неперервному полі: перевірка пікселя попереду / відрізків — 🥉 (треба не вбити себе власним щойно намальованим хвостом).
- Випадкові дірки в сліді — 🌱: таймер «малюю / не малюю».
- До 8 гравців на одній клавіатурі, по 2 клавіші — 📎: обробка багатьох одночасних утримань, ghosting клавіатури.
- Рахунок «+1 кожному живому за кожну смерть» і ціль (n−1)·10 — 🌱.
- Суперсили, що діють на себе чи на всіх інших — 🥉.

## Мапа на каталог
- Є: `move-auto` · `touch-death` · `spawn-random-cell` (старт) · `keyboard-controls` + `controls-remap` · `event-points` · `match-setup` · `game-screen` · `end-screen` · (Curve Fever) `online-multiplayer`, `rating-system`, `leaderboard`, `replay`, `item-pickup`, `temporary-modes`, `projectile-shot`.
- **Нема** → пропозиції карток:
  - `+trail-wall` (запропоновано в `tron-light-cycles`).
  - `+trail-gaps` «Випадкові дірки в сліді» · entities/move · 🌱 · слот {p, gap_len}.
  - `+relative-turn-controls` (запропоновано в `snake`).
  - `+free-angle-steering` «Рух під довільним кутом поза сіткою» · entities/move · 📎.
  - `+turn-radius-limit` «Мінімальний радіус повороту» · entities/move · 📎 · слот {omega}.
  - `+survival-points` «Очко кожному живому за кожне вибування» · game-logic/score · 🌱.
  - `+shared-keyboard-multiplayer` «Багато гравців на одній клавіатурі» · interface/input · 📎 · слот {players: 2–8}.
  - `+shared-field-versus` (запропоновано в `blockade`).
  - `+loadout-powerups` (запропоновано в `pac-man-256`) — сили перед матчем у Curve Fever Pro.

## Пропозиції до словників
- `+effect:leave_trail` — підтверджую (Tron, Blockade, Xonix).
- `+effect:gap` — тимчасово не лишати слід (дірка).
- `+trigger:player_out` — гравець вибув з раунду (для «очко всім живим»); `died` не розрізняє раунд і партію.
- `+cond:alive` — сутність/гравець ще в раунді.
- `+window:player-join` — екран входу гравців натисканням своєї клавіші.
- `+ui:player-scoreboard` — таблиця очок усіх гравців поруч із полем.
- `+feature:target-score` — довжина партії як функція кількості гравців.
- `+card:trail-gaps`, `+card:free-angle-steering`, `+card:turn-radius-limit`, `+card:survival-points`, `+card:shared-keyboard-multiplayer`.
- `+axis:control:direct-relative` — нове значення осі `control`: дві клавіші, ліво/право від поточного напряму.

## Джерела
- ⭐ [Wikipedia: Achtung, die Kurve!](https://en.wikipedia.org/wiki/Achtung,_die_Kurve!) — дві кнопки, будь-який напрям, мін. радіус повороту, дірки, рамка вбиває, останній живий виграє.
- [Wikipedia DE: Achtung, die Kurve!](https://de.wikipedia.org/wiki/Achtung,_die_Kurve!) — 2–8 гравців, ціль (гравців−1)·10, автори (Filip Oščádal, Kamil Doležal, Брно), Cervii, Curve Fever 3 і Pro.
- [achtungkurve.com](https://achtungkurve.com/) — грати в браузері; вибір гравців, суперсили hydra/reverse, імунітет.
- [Steam: Curve Fever Pro](https://store.steampowered.com/app/1133700/Curve_Fever_Pro/) — онлайн до 10, 30 сил, режими, ранкед, кастомні кімнати.
- YouTube: пошук «achtung die kurve gameplay».

## Непевне
- (?) Кількість гравців в оригіналі: 6 (EN) чи 8 (DE).
- (?) Правило «+1 кожному живому за кожну смерть» виведене з DE-формули «(n−1)·10 = десять виграних раундів»; чи потрібен відрив у 2 очки — не підтверджено.
- (?) Розкладка клавіш за замовчуванням (пари на різних кінцях клавіатури, миша для одного гравця) — з памʼяті.
- (?) Частота й довжина дірок, швидкість і радіус повороту — чисел у джерелах нема.
- (?) Пауза між раундами і вигляд таблиці очок.
