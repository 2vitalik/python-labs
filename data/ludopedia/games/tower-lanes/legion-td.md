---
title: Legion TD / Legion TD 2
slug: legion-td
aka: [Legion TD 2, LTD2, Legion TD Mega]
family: tower-lanes
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: online
  info: partial
  random: setup
  goal: survive
year: 2008
platforms: [PC (Warcraft III mod), PC/Mac (Legion TD 2, 2017)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Legion_TD", best: true, note: "мод Warcraft III і LTD2: дві команди, золото на захисників, лісоматеріал/мітіум на атаку, король"}
  - {kind: steam, url: "https://store.steampowered.com/app/469600/Legion_TD_2__Multiplayer_Tower_Defense/", note: "6 випадкових бійців на партію, найманці, економіка, король, 2v2/4v4, кампанія, челенджі"}
  - {kind: fandom, url: "https://legiontd2.wiki.gg/wiki/Mercenary", note: "wiki.gg: ціни в мітіумі, дохід, коли й де спавняться найманці"}
  - {kind: fandom, url: "https://legiontd2.wiki.gg/wiki/King", note: "wiki.gg: протікання до короля, апгрейди 20 мітіуму ×10"}
  - {kind: fandom, url: "https://legiontd2.wiki.gg/wiki/Worker", note: "wiki.gg: робітник 50 золота → 1 мітіум / 10 с"}
  - {kind: fandom, url: "https://legiontd2.wiki.gg/wiki/Wave", note: "wiki.gg: 21 хвиля, боси на 5/10/15/20/21"}
  - {kind: fandom, url: "https://legiontd2.wiki.gg/wiki/Legion_Spell", note: "wiki.gg: спільні 3 випадкові заклинання, вибір після 10-ї хвилі"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=legion+td+2+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [tower-placement, tower-range, enemy-waves, spawn-schedule, enemy-reached-base, hp-damage, chase-greedy, melee-vs-ranged, round-currency, shop-catalog, shop-buyback, online-multiplayer, ai-opponent, mode-select, lobby-window, leaderboard, +auto-battle, +send-units-to-opponent, +income-economy, +worker-economy, +king-core, +random-roster-roll, +aura-buff, +tower-evolve, +leak-to-core, +shared-random-spell]
proposes: ["+role:unit", "+role:lane", "+role:core", "+trigger:leak", "+trigger:build_phase", "+trigger:battle_phase", "+effect:sell", "+effect:upgrade", "+effect:income", "+cond:all_defenders_dead", "+ui:income-panel", "+ui:recommended-value", "+ui:send-panel", "+window:choice-window", "+feature:mode-versus", "+axis:time"]
author: opus
date: 2026-11-09
---

# Legion TD — tower defense, де твої вежі воюють самі, а гроші на атаку — це хвилі, які ти шлеш суперникові

## Суть
Командний PvP tower defense з моду Warcraft III. Кожен гравець має свою **смугу**: у фазі будування ставить бійців (юнітів-«веж») на сітку смуги, у фазі бою хвиля монстрів іде смугою, а бійці **самі** бʼються з нею (гравець не керує). Друга валюта (лісоматеріал у моді, **мітіум** у LTD2) іде на **найманців**, які додаються до хвилі суперника, — і кожен найманець назавжди підвищує твій дохід. Монстри, що прорвались (leak), біжать до **короля** команди; помер король — команда програла.

## Поле і час
- Мапа: дві команди по 1–4 гравці; у кожного гравця — власна прямокутна смуга-сітка для будування, згори вниз; знизу — король команди.
- Цикл хвилі: **фаза будування** (ставити/апгрейдити/продавати бійців, наймати робітників, слати найманців, апгрейдити короля) → **фаза бою** (real-time: хвиля + найманці суперника йдуть смугою; бійці бʼються автоматично) → дохід.
- 21 хвиля зі сталим складом (боси на 5, 10, 15, 20, 21); далі — фінальна фаза (Sudden death (?)).
- Інформація: склад наступної хвилі видно; найманців суперника — під час бою; ростер бійців — випадковий на партію (6 з легіонів).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Будівник | player | легіон | ставить бійців на свою смугу; сам не бʼється |
| Боєць (fighter) | tower (`+role:unit`) | ціна в золоті, атака/захист за типом, HP, дальність, аура, форми апгрейду | стоїть, де поставили, до бою; у бою сам атакує найближчих (`chase-greedy`) |
| Боєць-танк / дальній / літун | tower | — | ролі зі списку легіонів; авра підсилює сусідів |
| Особливі бійці (Eggsack, Soul Gate) | tower | — | не рухаються й не бʼють; Eggsack за 2 хвилі стає Hydra |
| Хвиля (creep) | enemy | склад за номером хвилі | спавн угорі смуги, іде вниз, бʼється з бійцями |
| Бос хвилі | boss | хвилі 5/10/15/20/21 | Legion Lord повертається сильнішим після смерті |
| Найманець (mercenary) | enemy (від суперника) | ціна в мітіумі (Snail 20 … Kraken 400), +дохід | спавн з наступною хвилею суперника: танки попереду, мілі всередині, дальні позаду |
| Король | static (`+role:core`) | HP, атака, реген, спел; апгрейди | бʼється з тими, хто протік; помер — поразка команди |
| Робітник (worker) | spawner | 50 золота | +1 мітіум кожні 10 с |
| Золото | resource | — | бійці, робітники, деякі здібності; дохід, зачищення, протікання суперника |
| Мітіум (лісоматеріал у моді) | resource | — | найманці, апгрейди короля; кожна витрата +дохід |
| Дохід (income) | resource | — | виплачується золотом наприкінці кожної фази бою |
| Legion Spell | pickup | 3 випадкові, однакові для всіх | обовʼязковий вибір одного після 10-ї хвилі |
| Смуга | zone (`+role:lane`) | сітка будування | своя для кожного гравця |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «кожному гравцю випадковий ростер з 6 бійців (можливий reroll)»`; `custom: «3 випадкові Legion Spells, однакові для всіх»`.
- КОЛИ `input(build, fighter, cell)` → ЯКЩО `has(gold, cost)` and `free(cell)` and `custom: «фаза будування, своя смуга»` → ТО `place(fighter, cell)`, `currency(-cost)`.
- КОЛИ `input(upgrade, fighter)` → ЯКЩО `has(gold, cost)` → ТО `transform(fighter → evolved)`; деякі мають розгалужені форми або «адаптацію» (Devilfish ↔ Seraphin).
- КОЛИ `input(sell, fighter)` → ТО `currency(+part)`, `disappear_a` (деякі бійці — з підвищеним поверненням).
- КОЛИ `input(hire, worker)` → ЯКЩО `has(gold, 50)` → ТО `spawn(worker)`; КОЛИ `timer(10s)` → ТО `counter(mythium, +workers)`.
- КОЛИ `input(send, merc)` → ЯКЩО `has(mythium, cost)` → ТО `counter(mythium, -cost)`, `custom: «effect income: +дохід назавжди»`, `send_garbage(merc → opponent_lane)` на початку наступної фази бою.
- КОЛИ `input(upgrade, king, attack|regen|spell)` → ЯКЩО `has(mythium, 20)` and `custom: «фаза будування, рівень < 10»` → ТО `custom: «+8% атаки / +реген / +9% шкоди спела»`, +дохід.
- КОЛИ `schedule(wave_n)` → ТО `spawn_at(wave, lane_top)` для кожного гравця + найманці суперника (танки попереду, мілі всередині, дальні позаду).
- КОЛИ `in_range(fighter, creep, range)` → ТО `damage(f(attack_type, armor_type))`; аура → `set_state(adjacent, buff)`.
- КОЛИ `custom: «усі бійці на смузі загинули, а вороги лишились»` → ТО `custom: «trigger leak»`: `move(creeps, king)`.
- КОЛИ `contact(creep, king)` → ТО `damage(king)`; король бʼє у відповідь; КОЛИ `hp_zero(king)` → ТО `lose` команди, `win` суперникам.
- КОЛИ `wave_cleared` (смуга без ворогів) → ТО `currency(+bounty)`; КОЛИ `custom: «суперник протік / його король отримав шкоду»` → ТО `currency(+leak_gold)` атакуючому.
- КОЛИ `custom: «кінець фази бою»` → ТО `currency(+income)`, `custom: «бійці відроджуються на місцях для наступної хвилі»` (?).
- КОЛИ `custom: «після 10-ї хвилі»` → ТО `choose(legion_spell)` до спавну 11-ї.
- КОЛИ `died(legion_lord)` → ЯКЩО `first_time` → ТО `respawn(legion_lord, stronger)`.
- Перемога: король суперників загинув · Поразка: свій король загинув · Рахунок: рейтинг, MVP партії.
- Мод WC3: золото → захисники, лісоматеріал (віспи-збирачі за золото) → атакуючі юніти й апгрейди короля.

## Керування і ввід
- RTS-керування мишею: обрати бійця з панелі ростеру → клік по клітині своєї смуги (є «подвійне будування» (?)); клік по бійцю → Upgrade/Sell.
- Панель найманців — клік = надіслати; кнопки робітника й апгрейдів короля; активні здібності деяких бійців (Pack Rat, Peewee, Nekomata).
- Пінги для команди; гарячі клавіші за сіткою панелі (?).

## Вікна, меню, HUD
- `main-menu`: PvP (рангові/звичайні 2v2, 4v4), кампанія (одиночна/кооп), Weekly Challenge, турнір, профіль.
- `lobby-window` — пошук матчу, вибір легіону (Mastermind — плейстайли з «lock-in»); `mode-select` (`Game mode` на вікі).
- `game-screen`: смуги всіх гравців (камера переходить між ними), сітка будування, панель ростеру бійців з цінами, `+ui:send-panel` найманців, `coins` + мітіум, `+ui:income-panel`, `+ui:recommended-value` (вартість бійців проти рекомендованої на хвилю), `wave-counter` і `next-wave-preview`, HP королів, `timer-countdown` фази будування, `threat-range` (радіус бійця).
- `+window:choice-window` — вибір Legion Spell після 10-ї хвилі.
- `end-screen` — переможець, MVP, статистика хвиль (протікання, вартість); `leaderboard` рангів; `stats-window` / історія матчів.

## Фічі поза полем
- `online-multiplayer` 1–8 гравців, 2v2/4v4 матчмейкінг; `+feature:mode-versus`; рейтинг `rank-tiers`.
- Кампанія (8–12 год + 10 AI-рівнів), `mode-coop`; Weekly Challenge (`mode-daily`-подібне), місячний турнір.
- Здача (Surrendering), MVP, power score (вікі); `unlockables` легіонів/косметики (?).

## Варіації й родичі
- Мод Legion TD (WC3, Lisk) → Legion TD Mega (Su Shui) → Legion TD 2 (AutoAttack Games, 2017/2021).
- Родичі в сімʼї: [desktop-tower-defense](desktop-tower-defense.md) і [fieldrunners](fieldrunners.md) (класичний TD на сітці), [mechabellum](mechabellum.md) (розстановка + автобій проти людини), [dota-auto-chess](dota-auto-chess.md) і [teamfight-tactics](teamfight-tactics.md) (нащадки ідеї «розставив — бій сам»); поза сімʼєю — Tetris 99 / Puyo (атака = сміття супернику).
- **Осі варіацій**: атака на суперника — немає (класичний TD) / найманці в його хвилю (LTD) / сміття (Tetris) · вежі — стрілянина з клітини / юніти, що рухаються в бою · дохід — фіксований / росте від агресії.

## Цікавинки для курсу
- Дві валюти: золото на оборону, мітіум на атаку, яка ще й піднімає дохід — 📎 (дилема «ризик ↔ економіка»).
- Найманці додаються до хвилі суперника за правилом порядку (танки → мілі → дальні) — 🥉.
- Протікання: коли смуга впала, решта біжить до спільного короля — 🌱.
- Автобій веж-юнітів з типами атаки × броні (таблиця множників) — 🥉.
- Випадковий ростер на партію + спільні випадкові заклинання — 📎.
- Король з апгрейдами (до 10 рівнів) як спільний ресурс команди — 🌱.

## Мапа на каталог
- Є: `tower-placement` ↔ бійці на сітці смуги · `tower-range` ↔ радіус · `enemy-waves` + `spawn-schedule` ↔ 21 хвиля · `enemy-reached-base` ↔ протікання до короля · `hp-damage` · `chase-greedy` ↔ бійці атакують найближчих · `melee-vs-ranged` ↔ танки/дальні · `round-currency` ↔ золото · `shop-catalog` ↔ ростер · `shop-buyback` ↔ продаж · `online-multiplayer` · `ai-opponent` ↔ кампанія · `mode-select` · `lobby-window` · `leaderboard`.
- **Нема** → пропозиції карток:
  - `+send-units-to-opponent` «Надіслати юнітів у хвилю суперника» · game-logic/opponent · 🥉.
  - `+income-economy` «Дохід, що росте від витрат» · game-logic/economy · 📎.
  - `+worker-economy` «Робітники генерують другу валюту» · game-logic/economy · 🌱.
  - `+king-core` «Спільний король команди з апгрейдами» · game-logic/lose · 📎.
  - `+random-roster-roll` «Випадковий набір доступних юнітів на партію» · game-logic/economy · 🌱.
  - `+tower-evolve` «Вежа апгрейдиться в іншу форму» · entities/state · 📎.
  - `+leak-to-core` «Прорвані вороги біжать до ядра» · entities/move · 🌱.
  - `+shared-random-spell` «Спільний випадковий вибір для всіх» · game-logic/economy · 🌱.

## Пропозиції до словників
- `+role:unit` — бойовий юніт; `+role:lane` — смуга гравця; `+role:core` — ядро/король, чия смерть = поразка команди.
- `+trigger:leak` — вороги прорвали смугу; `+trigger:build_phase` / `+trigger:battle_phase` — початок фаз циклу хвилі.
- `+effect:sell` · `+effect:upgrade` (перетворити в покращену форму за ціну) · `+effect:income` (змінити постійний дохід).
- `+cond:all_defenders_dead` — на смузі не лишилось захисників.
- `+ui:income-panel` · `+ui:recommended-value` (порівняння вартості оборони з нормою хвилі) · `+ui:send-panel`.
- `+window:choice-window` — вибір 1 з N.
- `+feature:mode-versus` — командний PvP.
- `+axis:time` — значення `phased` (будування без бою → автобій).

## Джерела
- ⭐ [Wikipedia: Legion TD](https://en.wikipedia.org/wiki/Legion_TD) — мод WC3, 2/4/6/8 гравців у двох командах, золото → захисники, лісоматеріал → атака й апгрейди короля, віспи; LTD2 (AutoAttack Games, 20.11.2017), мітіум, 8 фракцій по 6 юнітів.
- [Steam: Legion TD 2](https://store.steampowered.com/app/469600/Legion_TD_2__Multiplayer_Tower_Defense/) — 6 випадкових бійців, найманці, економіка, король, 2v2/4v4, кампанія, Weekly, турнір; повний реліз 1.10.2021.
- [LTD2 Wiki: Mercenary](https://legiontd2.wiki.gg/wiki/Mercenary) — ціни, дохід, таймінг, позиції спавну.
- [LTD2 Wiki: King](https://legiontd2.wiki.gg/wiki/King) — протікання, апгрейди 20 мітіуму ×10, спели.
- [LTD2 Wiki: Worker](https://legiontd2.wiki.gg/wiki/Worker) — 50 золота, 1 мітіум / 10 с.
- [LTD2 Wiki: Wave](https://legiontd2.wiki.gg/wiki/Wave) — 21 хвиля, склад, боси.
- [LTD2 Wiki: Legion Spell](https://legiontd2.wiki.gg/wiki/Legion_Spell) — 3 однакові випадкові, вибір після 10-ї хвилі.
- [LTD2 Wiki: Fighter](https://legiontd2.wiki.gg/wiki/Fighter) — легіони, ролі, аури, форми, особливі бійці.
- [LTD2 Wiki: Income](https://legiontd2.wiki.gg/wiki/Income) · [Gold](https://legiontd2.wiki.gg/wiki/Gold) — виплата в кінці фази бою, витрата мітіуму = +дохід.

## Непевне
- (?) Рік моду: черга каже 2008, Wikipedia — «late 2000s».
- (?) Розмір сітки смуги, тривалість фази будування, HP короля, стартові золото/дохід — не знайдено.
- (?) Чи бійці відновлюються між хвилями (за досвідом LTD — так, щоразу «з нуля» на місцях).
- (?) Що після 21-ї хвилі (Sudden death — сторінка-заглушка); точна формула leak gold; Dual building.
- (?) Як саме протікання розподіляється в командному режимі (до короля напряму чи через інші смуги).
