---
title: Pac-Man Battle Royale
slug: pac-man-battle-royale
aka: [PMBR, Pac-Man Battle Royale Chompionship]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: hotseat
  info: full
  random: runtime
  goal: survive
year: 2011
platforms: [arcade, iOS (демо), Pac-Man Museum, Pac-Man Museum+]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pac-Man_Battle_Royale", best: true, note: "до 4 Пекменів, енерджайзер дозволяє їсти суперників, раунди по 2 хв"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=pac-man+battle+royale+arcade+gameplay", note: "пошук; геймплей на 4"}
stage: v1
coverage: 70
mechanics: [move-auto, collect-all, item-pickup, temporary-modes, touch-death, player-death, mode-indicator, time-out, ai-opponent, realtime-ai, match-setup, game-screen, end-screen, +eat-rival-when-powered, +equal-bump-knockback, +last-standing-round, +round-wins-match, +dot-refill, +bonus-wipes-dots, +local-versus-shared-field]
proposes: ["+effect:knockback", "+trigger:last_standing", "+ui:round-wins", "+card:eat-rival-when-powered", "+card:last-standing-round"]
author: opus
date: 2026-11-09
---

# Pac-Man Battle Royale — чотири Пекмени в одному лабіринті: зʼїж енерджайзер і зʼїж суперників

## Суть
До чотирьох гравців одночасно керують Пекменами різних кольорів у спільному лабіринті з привидами. Звичайний Пекмен гине від привида; той, хто зʼїв енерджайзер, росте і може їсти привидів **і суперників без посилення** — ті синіють. Раунд виграє останній Пекмен, що вижив; матч — той, хто виграв найбільше раундів. Класичний «енерджайзер перевертає ролі» перенесено з PvE на PvP.

## Поле і час
- Один лабіринт Pac-Man-типу на екрані кабінету-столу; привиди з будиночком у центрі.
- Точки й енерджайзери **поповнюються**, коли зʼїдені всі; бонус біля клітки привидів прибирає всі точки, і вони зʼявляються заново.
- Раунд — до 2 хвилин, останні 10 с — відлік на екрані.
- Real-time, усі гравці одночасно; перед грою обирають довжину матчу 3–9 раундів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Пекмен гравця ×1–4 | player | колір (жовтий, рожевий, синій, червоний) | безперервний рух; їсть точки, пілюлі |
| Посилений Пекмен | player (стан) | тривалість | більший; їсть привидів і непосилених суперників |
| Синій Пекмен | player (стан) | контур свого кольору | непосилений, поки хтось інший посилений; не їсть привидів |
| CPU-Пекмен | enemy | 1 | суперник у грі на одного |
| Точка | pickup | — | поповнюється після повного зʼїдання |
| Енерджайзер | pickup | — | вмикає посилення того, хто зʼїв |
| Бонус біля клітки | pickup | — | прибирає всі точки й пілюлі → перезаповнення |
| Привид | enemy | — | дотик → непосилений Пекмен вибуває з раунду |
| Будиночок привидів | spawner | — | центр поля |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `contact(pac, dot)` → ТО `pickup`.
- КОЛИ `all_gone(dot+pellet)` → ТО `spawn(dots+pellets)` — поповнення.
- КОЛИ `contact(pac, bonus)` → ТО `pickup`, `custom: «прибрати всі точки й пілюлі»`, `spawn(dots+pellets)`.
- КОЛИ `contact(pac, pellet)` → ТО `pickup`, `set_state(pac, powered, t)`, `transform(pac → big)`, `set_state(other_pacs, blue)`, `set_state(ghosts, frightened)`.
- КОЛИ `contact(pac_a, pac_b)` → ЯКЩО `state(pac_a, powered) and not state(pac_b, powered)` → ТО `disappear_b` (B вибуває з раунду).
- КОЛИ `contact(pac_a, pac_b)` → ЯКЩО `same(pac_a, pac_b, power)` → ТО `custom: «обох відкидає на кілька клітин, без шкоди»` (`+effect:knockback`).
- КОЛИ `contact(blue_a, blue_b)` → ТО `block` — сині не проходять і не відкидають одне одного.
- КОЛИ `contact(pac, ghost)` → ЯКЩО `state(pac, powered)` → ТО `transform(ghost → eyes)`; інакше `disappear_a` (вибуває).
- КОЛИ `state_off(pac, powered)` → ТО `transform(pac → normal)`, `clear_state(others, blue)` (якщо більше ніхто не посилений).
- КОЛИ `count(alive_pacs, ==, 1)` → ТО `custom: «раунд виграв останній»` (`+trigger:last_standing`), `counter(round_wins, +1)`.
- КОЛИ `timer(120 s)` → ТО `custom: «раунд закінчується за часом»` (хто переможець при кількох живих — (?)).
- КОЛИ `level_start` (новий раунд) → ТО `respawn(all_pacs, start)`.
- КОЛИ `counter(rounds, ==, N)` → ТО `custom: «переможець матчу — найбільше виграних раундів»`, `window(end-screen)`.
- Перемога: найбільше виграних раундів. Поразка в раунді: зʼїв привид або посилений суперник. Рахунок очками не ведеться (за статтею).

## Керування і ввід
- Кожен гравець — свій джойстик з боку кабінету-столу; напрям, Пекмен біжить сам.
- Гра на одного — проти CPU-Пекмена.
- Перед матчем — вибір кількості раундів (3–9).

## Вікна, меню, HUD
- `match-setup` — кількість гравців і раундів.
- `game-screen` — лабіринт; `+ui:round-wins` (виграні раунди кожного кольору) (?); `timer-countdown` в останні 10 с.
- `end-screen` — переможець матчу.
- Переходи: атракт → (монети, старт) → match-setup → раунд → … → end-screen → атракт.

## Фічі поза полем
- `mode-versus` — PvP на одному полі до 4 гравців; `ai-opponent-levels` — CPU-суперник у грі на одного (рівні складності — (?)).
- `local-multiplayer` — усі за одним кабінетом.
- Pac-Man Museum / Museum+ — версія для консолей і ПК.

## Варіації й родичі
- **Pac-Man Battle Royale Chompionship** (2022) — прямий сиквел; **Pac-Man Party Royale** (Apple Arcade), **Pac-Man Mega Tunnel Battle** (Stadia, мережевий BR у лабіринтах-кімнатах), **Pac-Man 99** (Switch, 99 гравців, кожен у своєму лабіринті).
- Родичі в корпусі: Pac-Man (енерджайзер як перевертання ролей), Pac-Man Championship Edition (поповнення точок), Bomberman (арена «останній вижив», раунди до перемог), Achtung, die Kurve! (локальний PvP «останній живий»).
- **Осі варіацій:** суперники (на одному полі / окремі поля з атаками — Pac-Man 99); що робить посилення (їсти привидів / і суперників); рівні сили при зіткненні (нічого / відкидання / обидва гинуть).

## Цікавинки для курсу
- Енерджайзер як PvP-перемикач «хто кого їсть» з синіми суперниками — 🥉 (стан, що залежить від інших гравців).
- Зіткнення рівних — відкидання без шкоди — 📎 (окреме правило за порівнянням станів).
- Раунд «останній вижив» + матч до N раундів — 🌱.
- Поповнення точок і бонус-«перемішування» — 🌱.
- Кілька аватарів у реальному часі на одній клавіатурі — 🥉.
- CPU-Пекмен для гри на одного — 🥈 (AI, що полює на тебе і тікає від посиленого).

## Мапа на каталог
- Є: `move-auto` · `collect-all` (у межах «хвилі» точок) · `item-pickup` · `temporary-modes` · `touch-death` · `player-death` · `mode-indicator` (сині суперники) · `time-out` (2 хв) · `ai-opponent` · `realtime-ai` · `match-setup` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+eat-rival-when-powered` «Посилений гравець їсть суперників» · game-logic/opponent · 🥉.
  - `+equal-bump-knockback` «Рівні при зіткненні відскакують» · entities/interact · 📎.
  - `+last-standing-round` «Раунд до останнього живого» · game-logic/win · 🌱.
  - `+round-wins-match` «Матч до N виграних раундів» · game-logic/win · 🌱 · слот {rounds}.
  - `+dot-refill` «Зібране зʼявляється знову» · entities/spawn · 🌱.
  - `+bonus-wipes-dots` «Бонус перезапускає точки» · entities/interact · 🌱.
  - `+local-versus-shared-field` «Кілька гравців на одному полі одночасно» · game-logic/opponent · 🥉.

## Пропозиції до словників
- `+effect:knockback` — відкинути сутність на кілька клітин від точки зіткнення.
- `+trigger:last_standing` — на полі лишився один гравець (Battle Royale, Bomberman, Achtung).
- `+ui:round-wins` — виграні раунди кожного гравця.
- `+card:eat-rival-when-powered`, `+card:last-standing-round` — див. вище.

## Джерела
- ⭐ [Wikipedia: Pac-Man Battle Royale](https://en.wikipedia.org/wiki/Pac-Man_Battle_Royale) — до 4 гравців, кольори, CPU на одного, 3–9 раундів, поповнення точок, бонус, посилення і сині, відкидання рівних, раунд 2 хв з відліком 10 с, переможець за раундами, порти й сиквели.
- YouTube: пошук «pac-man battle royale arcade gameplay».

## Непевне
- (?) Хто виграє раунд, якщо після 2 хвилин живих кілька.
- (?) Тривалість посилення, поведінка привидів, вигляд HUD.
- (?) Що нового в Chompionship (2022).
