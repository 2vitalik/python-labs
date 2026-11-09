---
title: Quarries of Scred 2
slug: quarries-of-scred-2
aka: [QoS2, QoS 2]
family: dig-gravity
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: hotseat
  info: full
  random: setup
  goal: survive
year: 2015
platforms: [PC (Windows)]
links:
  - {kind: itch, url: "https://darkestkale.itch.io/quarries-of-scred-2", best: true, note: "сторінка й 4 скриншоти: до 4 гравців локально + ШІ, вибір персонажа й кольору, 6 режимів (Last Drone Standing, Team LDS, Mycological Melee, Race Condition, Big Gem Hunter, Pure Credits), геймпад"}
  - {kind: itch, url: "https://darkestkale.itch.io/quarries-of-scred", note: "перша гра серії: копай униз, збирай мінерали, повертайся здати; лазери, міни, самознищення; валуни, ranklers, кажани; Daily Quarry"}
  - {kind: itch, url: "https://kactusgames.itch.io/qos-1982", note: "фанатська текстова версія QoS (Kactus Games): 100 випадкових рівнів, нестійкі камені, ranklers, отруйні гази"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Quarries+of+Scred+2+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 30
mechanics: [move-4dir, keyboard-controls, dig-terrain, gravity-fall, environment-death, player-death, item-pickup, time-out, ai-opponent, realtime-ai, mode-select, character-select, match-setup, end-screen, message-log, main-menu, +shared-field-versus, +player-elimination, +team-play, +territory-capture, +local-referee]
proposes: ["+window:match-results", "+feature:mode-team", "+card:last-drone-standing"]
author: opus
date: 2026-11-09
---

# Quarries of Scred 2 — Boulder Dash-арена на чотирьох: копай, збирай і не дай себе розчавити на QuarryFest

## Суть
Локальний мультиплеєр на базі Quarries of Scred (Boulder Dash-подібного копання): до 4 гравців (або гравець проти ШІ) копають спільну кар'єр-сітку на час. Персонажі — Ruby, Crabbens, Bathory, Rankles і Bob; змагання — фестиваль «QuarryFest 2215». Шість режимів міняють ціль: вижити останнім (поодинці або командами), контролювати площу, перегони, полювання на великий самоцвіт, чисті кредити. Гинуть переважно під камінням: журнал смертей на фінальному екрані — суцільні «SQUISHED».

## Поле і час
- Квадратна сітка на весь екран (за скриншотами): земля, камені, самоцвіти, сірі стіни; усі гравці на одному полі без розділення екрана.
- Real-time з відліком «TIME REMAINING» угорі.
- Під полем — чотири панелі гравців з лічильниками; набір лічильників залежить від режиму.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець-«дрон» (Ruby, Crabbens, Bathory, Rankles, Bob) | player | спрайт, колір, життя (?) | копає землю, збирає; гине під камінням |
| Земля | terrain | — | прокопується |
| Стіна | static | — | непрохідна |
| Камінь (валун) | object | — | падає без опори; розчавлює гравця («SQUISHED») |
| Самоцвіти (червоні, сині) | pickup | — | лічильники на панелях гравців |
| Гриби кольору гравця | zone | власник | розмітка площі в Mycological Melee (?) |
| Мох | zone | — | друга «флора» (команди Moss і Mushroom) (?) |
| Ranklers, кажани | enemy | — | загрози першої гри; чи є в QoS2 — (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `cell(next, dirt|empty)` → ТО `move(player, dir)`; земля → `set_cell(next, empty)`.
- КОЛИ `tick` → ЯКЩО `free(below)` → ТО `fall(boulder)`.
- КОЛИ `contact(falling boulder, player)` → ТО `custom: «гравця розчавлено (SQUISHED)»`, `message(death_log)`, `lives(-1)` (?).
- КОЛИ `contact(player, gem)` → ТО `pickup`, `counter(gems, +1)`.
- КОЛИ `custom: «у гравця скінчились життя»` → ТО `custom: «панель гравця показує DEAD — вибув»`.
- КОЛИ `counter(alive_players, ==, 1)` → ЯКЩО `mode(last_drone_standing)` → ТО `win` (команди — `mode(team_lds)`, остання жива команда) (?).
- КОЛИ `counter(time_left, ==, 0)` → ТО `game_over`, `window(end-screen)` — «судді рахують очки».
- Mycological Melee: `custom: «контроль площі — гриби кольору гравця»` (?); Race Condition — перегони (?); Big Gem Hunter — великий самоцвіт (?); Pure Credits — лише кредити (?).
- Перемога: залежить від режиму. · Поразка: смерть під каменем → вибування. · Рахунок: лічильники самоцвітів і кредитів (?).

## Керування і ввід
- Клавіатура або геймпад (перевірено Xbox 360); до 4 гравців на одному компʼютері; ШІ на вільні місця для тренування.
- Кнопка дії називається TECH («PRESS TECH TO CONTINUE»); що вона робить у грі — (?).

## Вікна, меню, HUD
- `main-menu`: Start Game · Options · Credits & Thanks · Exit Game; номер збірки й «Update available» (перевірка версії).
- `character-select`: спрайт (Bob, Crabbens, Rankler, Bathory, Ruby) і колір.
- `mode-select` / `match-setup`: шість режимів, команди (?).
- `game-screen`: поле + `timer-countdown` «TIME REMAINING» + чотири панелі з лічильниками кожного гравця; мертвий — «DEAD».
- `end-screen` (GAME OVER): тип матчу (TEAM LDS), час матчу, склад команд, `message-log` останніх смертей, команда-переможець; коментатор Crabbens: «Now we wait for the judges to calculate the scores».

## Фічі поза полем
- `local-multiplayer` 1–4, `ai-opponent-levels` (?), команди, шість режимів; перевірка версії (не DRM).
- Перша гра серії мала Daily Quarry, режими Darkness і 60/120 секунд, графічні режими EGA / CGA / Monogreen — чи є щось із цього в QoS2 — (?).

## Варіації й родичі
- Quarries of Scred (2014–2015): одиночна — копай униз, збирай мінерали, повертайся здати, лазери, міни й самознищення для важких місць; валуни, ranklers, кажани; Daily Quarry.
- QoS 1982 (Kactus Games): фанатська текстова «версія 1982 року» — 100 випадкових рівнів, нестійкі камені, ranklers, отруйні гази.
- У сімʼї: [mine-bombers](mine-bombers.md) (мультиплеєр у шахті), [emerald-mine](emerald-mine.md) (BD на двох), [boulder-dash](boulder-dash.md).
- **Осі варіацій**: гравців — 1 / 2 / 4 на одному полі; ціль — квота й вихід (BD) / останній живий / контроль площі / перегони.

## Цікавинки для курсу
- Спільне поле на 4 гравців з одночасним вводом і камінням, що вбиває будь-кого — 🥉.
- Режими як набір правил перемоги над тим самим двіжком (LDS, команди, площа, перегони, самоцвіт, кредити) — 🥉.
- Фінальний екран з журналом смертей і причиною («SQUISHED») — 🌱.
- ШІ-суперник у BD-фізиці (не стати під камінь, дістатися самоцвіта) — 🥈.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls`; `dig-terrain` ↔ земля; `gravity-fall` ↔ камені; `environment-death` + `player-death` ↔ SQUISHED; `item-pickup` ↔ самоцвіти; `time-out` ↔ відлік; `ai-opponent` + `realtime-ai` ↔ ШІ; `mode-select` + `match-setup` + `character-select` ↔ налаштування матчу; `end-screen` + `message-log` ↔ GAME OVER і журнал смертей; `main-menu`.
- Повтори з корпусу: `+shared-field-versus` · `+player-elimination` · `+team-play` · `+territory-capture` (Mycological Melee, (?)) · `+local-referee` (коментатор-«суддя»).
- **Нема** → `+last-drone-standing` «Перемагає останній живий гравець / команда» · game-logic/win · 🌱.

## Пропозиції до словників
- `+window:match-results` — фінал матчу: тип, час, команди, журнал смертей, переможець (ширше за `end-screen` одного гравця).
- `+feature:mode-team` — командний варіант будь-якого режиму.
- `+card:last-drone-standing` — див. «Мапа на каталог».

## Джерела
- ⭐ [itch.io: Quarries of Scred 2](https://darkestkale.itch.io/quarries-of-scred-2) — опис, персонажі, режими (лише назви), гравці й ввід, дата 24.10.2015; скриншоти меню, поля, панелей гравців і екрана GAME OVER.
- [itch.io: Quarries of Scred](https://darkestkale.itch.io/quarries-of-scred) — ядро серії: копання, мінерали, здача, лазери, міни, самознищення, загрози, режими.
- [itch.io: QoS 1982](https://kactusgames.itch.io/qos-1982) — текстова фан-версія.
- YouTube: пошук «Quarries of Scred 2 gameplay».

## Непевне
- (?) Правила режимів відомі лише з назв (Mycological Melee — «area control», інше — здогад з назви); що таке «drone» — гравці чи окремі юніти.
- (?) Чи в QoS2 лишились лазери, міни й самознищення першої гри; чи є вороги.
- (?) Значення іконок на панелях гравців (червоні й сині самоцвіти, земля, «J», «L» — життя?).
- (?) Чи кар'єри генеруються випадково (QoS1 мав щоденний стандартний кар'єр, QoS 1982 — випадкові рівні).
- (?) Статус «In development»; збірка на скриншоті — 2015-07-16 v0.1.
