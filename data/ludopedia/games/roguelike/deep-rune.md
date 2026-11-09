---
title: Deep Rune
slug: deep-rune
aka: []
family: roguelike
also: [thinky, grid-platformer]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: setup
  goal: score
year: 2021
platforms: [PC (Windows)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1631780/Deep_Rune/", best: true, note: "Moonskull Games (JC Bailey), 14.10.2021, free to play; бічний розріз, натхнення Tower of the Sorcerer і DROD RPG, динамічна складність = рахунок"}
  - {kind: other, url: "https://steamcommunity.com/app/1631780/discussions/0/3370404731641042416/", note: "розробник: Insight — множник рівня ворогів і впливає на фінальний рахунок"}
  - {kind: other, url: "https://steamcommunity.com/app/1631780/discussions/0/3198114142304143152/", note: "класи: відкриття за 1000 / 2000 очок, INS у рахунку, ревенанти"}
  - {kind: other, url: "https://steamcommunity.com/app/1631780/reviews/?browsefilter=toprated&l=english", note: "відгуки: покроково на сітці, падіння шкодить, крит зі спини, міцність зброї, 10 відроджень"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Deep+Rune+Moonskull+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [hp-damage, gravity-fall, inventory-items, inventory-limit, shop-catalog, cell-click, keyboard-controls, character-select, respawn, save-multi-slot, leaderboard, +deterministic-combat, +fall-damage, +backstab-facing, +weapon-durability, +character-classes, +random-trait, +insight-difficulty-score, +enemy-level-scaling, +limited-respawns, +ability-gated-areas, +fast-travel, +class-unlock-by-score, +multiple-endings, +spell-runes]
proposes: ["+effect:fight(a, b)", "+cond:fall_height", "+cond:behind(a, b)", "+effect:level_up", "+trigger:level_up", "+feature:fast-travel", "+ui:mana-bar", "+ui:trait-tooltip", "+axis:view=side"]
author: opus
date: 2026-11-09
---

# Deep Rune — Magic Tower у бічному розрізі: падіння ранить, удар зі спини критує, а «прозріння» робить ворогів сильнішими й рахунок більшим

## Суть
Безкоштовна покрокова гра JC Bailey (Moonskull Games): підземні руїни скандинавської міфології в бічному розрізі на сітці, натхнення — Tower of the Sorcerer ([magic-tower](magic-tower.md)), DROD RPG і King's Field. Бій без випадковості, HP, MP, інвентар і навіть момент підвищення рівня — ресурси, як у вежі. Нове: **гравітація** (падіння завдає шкоди), **позиційний крит зі спини**, **міцність зброї**, класи з рисами і **Insight** — стат, що множить рівень ворогів і водночас іде у фінальний рахунок («динамічна складність як рахунок»).

## Поле і час
- Ручний нелінійний світ-підземелля в бічному розрізі на сітці; «метроідванія»: секретні входи й печери «поза мапою» відкриваються новими здібностями.
- Покроково; гравітація вниз — герой падає, висота падіння = шкода.
- Мапа статична: маршрут однаковий у кожному проходженні; є мінімапа.
- Швидке переміщення між точками відкривається після деяких босів (v1.03).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | клас, риси, HP, MP, ATT, рівень, XP, INS, золото | ходить сіткою; падає; бій детермінований |
| Ворог | enemy | рівень × множник INS, напрямок | удар у спину — крит |
| Ревенант | enemy | — | убивство дає INS, навіть коли забирає XP |
| Бос | boss | — | після перемоги — руна/закляття (?), відкриває швидке переміщення |
| Зброя | pickup | ATT, міцність | зношується; лук посилює риса Marksman |
| Щит, кільце | pickup | — | спорядження (Skill Ring синергує з магією) |
| Руна | pickup | закляття | відкриває магію (список заклять «відкладений» на кінець гри) |
| Сонячний камінь | pickup | — | ставиться на мапу; ефект неочевидний (відгук) |
| Тіло NPC із синьою точкою | pickup | — | повністю відновлює HP і MP |
| NPC-торговець | neutral | ціни | крамниця; риса Haggler дає знижку |
| Точка швидкого переміщення | static | — | телепорт між відкритими точками |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell)` → ТО `move(hero, dir)`.
- КОЛИ `custom: «під героєм порожньо»` → ТО `fall(hero)`; КОЛИ `custom: «приземлення з висоти»` → ТО `damage(hero, n)`; ЯКЩО `state(hero, agile)` → ТО `custom: «шкода падіння / 2 з округленням униз»`.
- КОЛИ `contact(hero, enemy)` → ТО `custom: «детермінований бій за статами»`, `damage(hero, n)`.
- КОЛИ `contact(hero, enemy)` → ЯКЩО `facing(enemy, away_from_hero)` → ТО `custom: «критичний удар зі спини»`.
- КОЛИ `contact(hero, enemy)` → ЯКЩО `custom: «зброя в руці»` → ТО `counter(durability, −1)`; КОЛИ `counter(durability, <=, 0)` → ТО `custom: «зброя ламається»` (?).
- КОЛИ `died(enemy)` → ТО `counter(xp, +n)`, `counter(insight, +n)`.
- КОЛИ `died(revenant)` → ТО `counter(insight, +n)`, `counter(xp, −n)`.
- КОЛИ `custom: «INS зріс»` → ТО `custom: «рівень ворогів = базовий × множник(INS)»`.
- КОЛИ `counter(xp, >=, n)` → ТО `custom: «рівень-ап у вибраний момент — ресурс»`.
- КОЛИ `died(boss)` → ТО `unlock(fast_travel)` (деякі боси).
- КОЛИ `contact(hero, npc_corpse_blue)` → ТО `heal(hero, full)`, `custom: «MP повністю»`.
- КОЛИ `input(buy)` → ЯКЩО `custom: «золота вистачає»` → ТО `currency(−price)`; ЯКЩО `state(hero, haggler)` → ТО `custom: «знижка»`.
- КОЛИ `hp_zero(hero)` → ЯКЩО `counter(respawns, <, 10)` → ТО `respawn(hero, room_start)`.
- КОЛИ `level_end` (кінець гри) → ТО `score(f(INS, …))`; ЯКЩО `counter(score, >=, 1000)` → ТО `unlock(Scholar)`; ЯКЩО `counter(score, >=, 2000)` → ТО `unlock(third_class)`.
- Перемога: знайти Deep Rune (є альтернативна кінцівка). Поразка: смерть понад ліміт відроджень (?). Рахунок: фінальний рахунок від INS і досягнення кінця; таблиці лідерів Steam.

## Керування і ввід
- Повне керування мишею (клік по клітині/дії), клавіатура — опційно; миша обовʼязкова.
- Швидке завантаження — F8; збереження в обмежені слоти, «завантаження посеред кімнати працює не зовсім правильно» (відгук).
- Перейменування персонажа на екрані вибору класу.

## Вікна, меню, HUD
- `character-select` — клас, риси (підказки), найкращий рахунок, імʼя.
- `game-screen` — бічний розріз, HP/MP, стати, спорядження, мінімапа; `tooltip` предметів і заклять.
- `shop-window` — торговець; `inventory-window` — обмежений інвентар.
- `save-slots` — обмежені слоти; `leaderboard` — таблиці Steam; `end-screen` — рахунок і кінцівка.
- `map-window` (?) — мінімапа/мапа з позначками сонячних каменів.
- Переходи: `main-menu` → `character-select` → `game-screen` ⇄ `shop-window` / `inventory-window` → `end-screen`.

## Фічі поза полем
- `unlockables`: класи відкриваються рахунком (1000 → Scholar, 2000 → третій клас, «по суті hard mode», подвоює INS).
- Риси класів: Amnesiac, Insightful, Marksman (+2 ATT з луком), Agile (половина шкоди падіння), Affluent (стартове золото), Haggler (знижка), Skillful, Tribesman.
- `leaderboard-online` (Steam), `achievements` (Ego Death, Chieftain, Ecliptic), `cloud-save`.
- `+feature:fast-travel` після босів; альтернативна кінцівка.

## Варіації й родичі
- [magic-tower](magic-tower.md) — детермінований бій і ресурси; [achronal-dungeon](achronal-dungeon.md) — його автор рекомендує Deep Rune як схожу гру; [tactical-nexus](tactical-nexus.md), [towerbound](towerbound.md) — сучасні вежі; King's Field і DROD RPG — заявлені натхнення.
- Відмінність від Magic Tower: бічний розріз із гравітацією, крит від позиції, зношування зброї, класи й риси, складність, що росте від самого гравця (INS).
- Осі варіацій: **вид** (згори / збоку з гравітацією) · **складність** (фіксована / росте з дією гравця й множить рахунок) · **смерть** (кінець / N відроджень кімнати) · **спорядження** (вічне / зношується).

## Цікавинки для курсу
- Падіння по сітці з шкодою за висоту й рисою, що її ділить — 🌱.
- Крит зі спини: орієнтація ворога + позиція героя — 🌱.
- INS як «добровільна складність»: множить рівень ворогів і рахунок — 📎 (один стат керує двома системами).
- Міцність зброї (лічильник ударів) — 🌱.
- Класи, що відкриваються порогом рахунку — 🌱.
- Ліміт відроджень у межах кімнати — 📎 (знімок стану кімнати на вході).

## Мапа на каталог
- Є: `hp-damage` · `gravity-fall` · `inventory-items` + `inventory-limit` · `shop-catalog` · `cell-click` (миша) · `keyboard-controls` · `character-select` · `respawn` (кімната) · `save-multi-slot` · `leaderboard`.
- **Нема** → пропозиції карток:
  - `+insight-difficulty-score` «Стат гравця множить силу ворогів і фінальний рахунок» · game-logic/difficulty · 📎.
  - `+enemy-level-scaling` «Рівень ворогів залежить від стану гравця» · game-logic/difficulty · 📎.
  - `+limited-respawns` «N відроджень на початку кімнати» · game-logic/lose · 🌱 (родич `respawn`).
  - `+class-unlock-by-score` «Клас відкривається рахунком» · progression/meta · 🌱.
  - `+ability-gated-areas` «Зони, доступні після нової здібності» · levels/progression · 📎.
  - `+random-trait` «Одна випадкова риса персонажа, видна згодом» · entities/state · 🌱.
  - `+spell-runes` «Руни відкривають закляття» · entities/state · 🌱.
  - `+deterministic-combat`, `+fall-damage`, `+backstab-facing`, `+weapon-durability`, `+character-classes`, `+fast-travel`, `+multiple-endings` — уже пропоновані корпусом.

## Пропозиції до словників
- `+effect:fight(a, b)` — атомарний детермінований бій.
- `+cond:fall_height` — висота падіння (для шкоди).
- `+cond:behind(a, b)` — A стоїть за спиною B (з урахуванням `facing`).
- `+trigger:level_up` / `+effect:level_up` — підвищення рівня як подія й ефект.
- `+feature:fast-travel` — телепорт між відкритими точками світу.
- `+ui:mana-bar` — шкала MP.
- `+ui:trait-tooltip` — підказка рис класу на екрані вибору.
- `+axis:view=side` — бічний розріз сітки (поле `view` є в code-words, на осі шапки — нема).

## Джерела
- ⭐ [Steam: Deep Rune](https://store.steampowered.com/app/1631780/Deep_Rune/) — бічний розріз, RPG + пазл, предмети/магія/стати, 6+ класів із рисами, зброя, щити, кільця, руни, динамічна складність як рахунок, миша, лідерборди.
- [Steam: Does insight do anything?](https://steamcommunity.com/app/1631780/discussions/0/3370404731641042416/) — розробник: INS — множник рівня ворогів, впливає на фінальний рахунок.
- [Steam: How to unlock new character classes?](https://steamcommunity.com/app/1631780/discussions/0/3198114142304143152/) — пороги 1000/2000, Scholar, INS у рахунку, ревенанти, тіла NPC із синьою точкою.
- [Steam: відгуки](https://steamcommunity.com/app/1631780/reviews/?browsefilter=toprated&l=english) — покроково на сітці, шкода падіння, крит зі спини, міцність зброї, 10 відроджень, нема undo, обмежені сейви.
- [Патч-нотатки v1.01–1.03 (Steam News API)](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=1631780&count=15&maxlength=4000) — риси Agile/Marksman/Affluent/Haggler/Insightful, швидке переміщення, F8.

## Непевне
- (?) Формула бою (хто бʼє першим, як рахується крит) — лише «прості стати, без випадковості».
- (?) Що буває після 10 відроджень — кінець гри чи завантаження сейва.
- (?) Як INS конвертується в ману і чи це вміння класу чи предмета (Skill Ring).
- (?) Чи вороги ходять (`opponent: ai` поставлено через напрямок погляду й крит зі спини).
- (?) Ефект сонячних каменів; чи закляття дають руни від босів, чи рівні.
- (?) `random: setup` — за відгуком, у стартового героя є одна випадкова риса; інший відгук каже «без випадковості».
