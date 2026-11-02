---
title: Wrecking Crew
slug: wrecking-crew
family: grid-platformer
also: [dig-gravity]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: hotseat
  info: full
  random: none
  goal: state
year: 1985
platforms: ["arcade (VS. Wrecking Crew 1984)", NES/Famicom (1985), Famicom Disk System, GBA, Wii/Wii U/3DS Virtual Console, Switch Online]
links:
  - {kind: fandom, url: "https://www.mariowiki.com/Wrecking_Crew", best: true, note: "Super Mario Wiki — обʼєкти, вороги, призи динаміту, бонус-етапи, Design mode, вибір фази"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Wrecking_Crew_(video_game)", note: "невидима сітка «одна клітина — один обʼєкт», бомби руйнують звʼязане, редактор на касету"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Wrecking+Crew+NES+gameplay", note: "пошук; геймплей NES"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Wrecking+Crew+NES+design+mode", note: "пошук; редактор фаз"}
stage: v1
coverage: 70
mechanics: [move-4dir, gravity-fall, impassable-cells, chase-player, chase-greedy, touch-death, player-death, event-points, combo-multiplier, score-records, level-select, sequential-levels, hot-seat, in-game-editor, editor-palette, editor-erase, editor-playtest, save-game, status-panel, +ladder-climb, +hammer-break, +bomb-flood-destroy, +chain-reaction, +door-banish-enemy, +drum-trap, +timeout-punisher, +knock-off-platform, +ordered-hit-bonus, +letter-collection, +wrap-edges, +bonus-stage-search, +self-softlock]
proposes: ["+effect:break", "+effect:explode", "+effect:set_state", "+effect:fall", "+trigger:idle", "+cond:connected", "+cond:hit_count", "+role:hazard", "+role:gate", "+window:editor-window", "+window:mode-select", "+feature:level-editor", "+card:bomb-flood-destroy"]
author: opus
date: 2026-11-02
---

# Wrecking Crew — Маріо з молотом зносить усі стіни фази, не вміючи стрибати

## Суть
Маріо (у 2P — Луїджі) на будові: треба знести молотом усі стіни, драбини-стіни й колони фази. Стрибати він не може — молот заважкий, тож лізе лише драбинами, і **порядок руйнування** — головна головоломка: зламав драбину завчасно — стіна вгорі недосяжна. Бомби зносять усе звʼязане з ними руйнівне (ланцюгові реакції), двері відсилають ворогів у фон, бочки ловлять ворогів. Вбудований Design mode — редактор фаз.

## Поле і час
- Фаза = один екран-сітка, де **кожна клітина тримає один обʼєкт** (Wikipedia: «invisible grid»). Поверхи-балки, драбини між ними.
- Горизонтально екран **замкнений у кільце** (wraparound), по вертикалі — прокрутка (NES).
- Real-time: вороги рухаються безперервно, удари молота мають анімацію; затримка в одному місці → зʼявляються вогняні кулі.
- Фон — окремий шар: туди потрапляють вороги через двері й там ходить Foreman Spike.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Маріо / Луїджі | player | 5 життів (?); не стрибає | хід ←/→, драбини ↑/↓, удар молотом перед собою |
| Стіна | object | ударів до руйнування (?) | руйнується молотом; усі знесені → фаза пройдена |
| Стіна-драбина | object | — | нею можна лізти, доки не зламана; руйнується (й Spike теж ламає) |
| Колона (pillar) | object | частини (?) | вибивається молотом |
| Драбина (незламна) | terrain | — | лізти; молот не бере |
| Бомба (динаміт) | object | — | удар → руйнує все звʼязане/в лінії руйнівне; збиває з платформи тих, хто поруч |
| Бочка (drum) | object | незламна | падає й накриває ворога під нею; гравець у пастці — лише перезапуск фази |
| Двері | gate | closed/open | удар відчиняє; ворог, що входить, іде у фон (силует, нешкідливий) |
| Gotcha Wrench Jr. / Gotcha Wrench | enemy | повільний / швидкий | переслідує Маріо (жадібно) |
| Eggplant Man | enemy | — | бігає фазою, заступає дорогу |
| Вогняна куля | enemy | — | зʼявляється, якщо гравець задовго в одній зоні |
| Foreman Spike | boss | у фоні | ламає стіни-драбини, намагається скинути Маріо вниз; влучив молотом — падає сам |
| Букви M-A-R-I-O | pickup | порядок | проявляються з певних стін у певному порядку; усі → +1 життя |
| Приз (свинка/Санта/манекі-неко/Золотий молот) | pickup | 800–3200 | з'являється за 3 бомби в заданому порядку |
| Золотий молот | pickup | тимчасово | ламає швидше; влучно — скидає ворогів на дно |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(hammer)` → ЯКЩО `cell(ahead, wall|ladder_wall|pillar)` → ТО `custom: «break»` (за `hit_count` ударів (?)), `score(n)`.
- КОЛИ `input(hammer)` → ЯКЩО `cell(ahead, bomb)` → ТО `custom: «explode»`: `custom: «знищити все руйнівне, connected з бомбою»`; інші бомби в групі — теж (`+chain-reaction`); сусіди-персонажі `fall`.
- КОЛИ `custom: «кілька обʼєктів за одну дію»` → ТО `score(bonus)` (більше за довший ланцюг).
- КОЛИ `input(climb)` → ЯКЩО `cell(here, ladder|ladder_wall)` → ТО `move(a, up|down)`; стрибка нема.
- КОЛИ `input(hammer)` → ЯКЩО `cell(ahead, door)` → ТО `set_state(door, open)`; КОЛИ `contact(enemy, open_door)` → ТО `set_state(enemy, background)` (силует, нешкідливий).
- КОЛИ `count(enemy_foreground, ==, 0)` and ворогів було >1 → ТО `freeze(enemies, ≈8s)`.
- КОЛИ `input(hammer)` під бочкою з ворогом → ТО `fall(drum)`, `set_state(enemy, trapped)`; КОЛИ бочка накрила Маріо → ТО `custom: «застряг — лише abort фази»`.
- КОЛИ `contact(player, enemy|fireball)` → ТО `lives(-1)`, `restart` фази.
- КОЛИ `idle(n)` у зоні → ТО `spawn_at(fireball, side)`.
- КОЛИ Spike б'є стіну-драбину під Маріо / вибух поруч → ТО `fall(player)` до нижньої опори (не смерть (?)).
- КОЛИ `input(hammer)` по Spike → ТО `fall(spike)`.
- КОЛИ стіни/бомби знесено в певному порядку → ТО `spawn(letter)`; КОЛИ `counter(letters, ==, 5)` → ТО `lives(+1)`.
- КОЛИ 3+ бомби підірвано в заданому порядку → ТО `spawn(prize)`: `(phase + swings) mod 8` → 0/3/6 свинка 800 · 2/5 Санта 1600 · 4/7 манекі-неко 3200 · 1 Золотий молот 3200.
- КОЛИ `all_gone(destructible)` → ТО `win`, `next_level`; кожні 4 фази → бонус-етап.
- Бонус-етап: КОЛИ ламаєш стіну → ЯКЩО за нею монета раніше за Spike → ТО `score(до 10000)` (10000 — з першої стіни); таймер.
- Поразка: 0 життів → `game_over`. Глухий кут (недосяжна стіна) — гравець сам перериває фазу. Рахунок: очки за обʼєкти, ланцюги, призи, бонус-етапи; рекорд.

## Керування і ввід
- Хрестовина ←/→ — ходити; ↑/↓ на драбині — лізти; кнопка — удар молотом перед собою (?яка саме: A/B).
- Start — пауза; є переривання фази (abort), коли Маріо застряг або фаза зламана.
- Design mode: курсор по сітці, вибір обʼєкта з палітри, кнопка — поставити/стерти (?точна схема).
- 2P на NES — по черзі: Луїджі грає, коли Маріо втрачає життя (`hotseat`); аркада VS — одночасно.

## Вікна, меню, HUD
- `splash-screen` / титул з пунктами: 1 Player · 2 Players · Design (`mode-select`) (?) і вибір номера фази 1–100 (`level-select`).
- `game-screen` — фаза; HUD: `score`, `hi-score`, `lives`, `level-number` (Phase N), зібрані букви (?).
- `custom-window` — бонус-етап (ряд стін, гонка зі Spike, `timer-countdown`).
- `editor-window` (Design mode) — сітка + палітра обʼєктів (стіни, драбини, бомби, бочки, двері, вороги, старт Маріо), тест, збереження/завантаження.
- `end-screen` — Game Over; після фази 100 — гра йде по колу.
- Переходи: титул → (вибір фази) → game-screen → фаза пройдена → наступна (кожні 4 → бонус) · титул → Design → editor-window ↔ тест-гра.

## Фічі поза полем
- `level-editor` (Design mode): до 4 власних фаз; збереження на касету Famicom Data Recorder (+клавіатура Family BASIC, лише Японія); FDS-версія пише на дискету; Virtual Console емулює периферію, Switch Online — без збереження.
- `level-select`: старт з будь-якої з 100 фаз; бонус-етапи не обираються.
- `leaderboard-local` (hi-score), `hotseat` 2P.

## Варіації й родичі
- VS. Wrecking Crew (аркада, одночасні 2P), Wrecking Crew '98 (SFC, з поєдинком у стилі падаючих блоків).
- Родичі: Lode Runner (копання + драбини, редактор у грі), Donkey Kong (Маріо + молот + драбини), Bomberman (вибух руйнує стіни), Boulder Dash.
- **Осі варіацій:** що руйнує вибух (сусіди-хрест / лінія / уся звʼязана група) · чи може гравець стрибати (так / ні → пазл порядку) · що робити з ворогом (уникати / двері у фон / бочка-пастка / скинути).

## Цікавинки для курсу
- Бомба знищує всю **звʼязану групу** руйнівних обʼєктів — flood fill / BFS + ланцюг бомб — 🥉.
- Пазл порядку руйнування без стрибка: перевірка «чи досяжні всі стіни після цього удару» — 🥇 (досяжність на графі, що змінюється).
- Двері, що відсилають ворога у фоновий шар — 📎 (стан сутності «у фоні» = вимкнені колізії).
- Приз за порядок підриву + формула `(phase + swings) mod 8` — 🌱, кумедний приклад детермінованого «рандому».
- Вогняна куля-покарання за затримку — 📎 (таймер бездіяльності в зоні).
- Design mode з палітрою й тестом — 🥈 (повний редактор + збереження фаз у файл).

## Мапа на каталог
- Є: `move-4dir` · `gravity-fall` · `impassable-cells` · `chase-player` / `chase-greedy` (Gotcha Wrench) · `touch-death` · `player-death` · `event-points` · `combo-multiplier` (ланцюг бомб) · `score-records` · `level-select` · `sequential-levels` · `hot-seat` · `in-game-editor` + `editor-palette` + `editor-erase` + `editor-playtest` · `save-game` (фази редактора) · `status-panel`.
- **Нема** → пропозиції карток:
  - `+ladder-climb` (повтор) — драбини й стіни-драбини.
  - `+hammer-break` «Руйнування перед собою за N ударів» · entities/interact · 🌱 · слот {hits}.
  - `+bomb-flood-destroy` «Вибух знищує звʼязану групу» · entities/combat · 🥉 · слот {connect: 4|8, kinds}.
  - `+chain-reaction` (повтор) — бомба підриває бомби групи.
  - `+door-banish-enemy` «Двері відсилають ворога у фон» · entities/interact · 📎.
  - `+drum-trap` «Падаючий обʼєкт-пастка накриває ворога» · entities/interact · 📎.
  - `+timeout-punisher` (повтор Bomberman) — вогняна куля за затримку.
  - `+knock-off-platform` «Скинути на нижню опору без смерті» · entities/move · 📎.
  - `+ordered-hit-bonus` «Приз за дії в заданому порядку» · game-logic/score · 🌱.
  - `+letter-collection` (повтор) — M-A-R-I-O → життя.
  - `+wrap-edges` (повтор) — горизонтальне кільце.
  - `+bonus-stage-search` «Бонус-етап: знайти приз раніше суперника» · game-logic/score · 📎.
  - `+self-softlock` «Гравець може зробити рівень непрохідним (abort)» · levels/solvability · 🥉 — родич `unsolvable-states`.

## Пропозиції до словників
- `+effect:break(cell)` — руйнування обʼєкта молотом (відмінне від `disappear_b`: є лічильник ударів) — або `set_cell` + `+cond:hit_count` (повтор Solomon's Key).
- `+effect:explode(area, into?)` (🔥) — тут `area = connected group`; `+cond:connected` (🔥) — обʼєкт у звʼязній групі з бомбою.
- `+effect:set_state(enemy, background)` — шар фону як стан.
- `+trigger:idle(n)` — гравець довго в одній зоні (вогняна куля).
- `+role:hazard` (вогняна куля), `+role:gate` (двері), `+role:boss` — Spike.
- `+window:editor-window`, `+window:mode-select` (1P/2P/Design).
- `+feature:level-editor` — збереження на зовнішній носій (касета/дискета).
- `+card:bomb-flood-destroy` — див. вище.

## Джерела
- ⭐ [Super Mario Wiki: Wrecking Crew](https://www.mariowiki.com/Wrecking_Crew) — обʼєкти, вороги, Spike, призи динаміту з формулою, букви, бонус-етапи, Design mode і периферія, вибір фази.
- [Wikipedia: Wrecking Crew](https://en.wikipedia.org/wiki/Wrecking_Crew_(video_game)) — невидима сітка, без стрибка, бомби → звʼязане, 5 життів, abort, 4 фази в редакторі, касета.
- YouTube: пошук «Wrecking Crew NES gameplay» і «… design mode».

## Непевне
- (?) Скільки ударів треба стіні, стіні-драбині, колоні — джерела не дають чисел.
- (?) Бомба: Wikipedia — «руйнує все звʼязане», Mario Wiki — «цеглу в лінії з нею»; можливо, обидва описи одного правила.
- (?) Падіння Маріо (від Spike/вибуху) не смертельне — з памʼяті.
- (?) Призначення кнопок, вигляд титульного меню, чи показуються зібрані букви в HUD.
- (?) Mario Wiki змішує аркадну й NES-версії (двері «рідше, ніж в аркаді»); тут описано NES.
