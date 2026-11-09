---
title: Subterrarium
slug: subterrarium
aka: []
family: dig-gravity
also: [grid-platformer]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: setup
  goal: state
year: 2016
platforms: [PC (Windows), Mac]
links:
  - {kind: itch, url: "https://slimefriend.itch.io/subterrarium", best: true, note: "опис: гроші з землі → газовані напої з автоматів → полив насіння; рослини-інструменти (ліана, бомбова рослина); кожен хід послаблює ґрунт"}
  - {kind: steam, url: "https://store.steampowered.com/app/467170/", note: "Steam 2016: те саме + Adventure — процедурні пазли"}
  - {kind: other, url: "https://steamcommunity.com/app/467170/reviews/?browsefilter=toprated", note: "огляди: покроковий платформер, підйом на 1 клітину, монета за блок, паливо = джетпак/полив/підрив бомби, «dirtalanche», 8 ручних рівнів, Challenge/Adventure"}
  - {kind: other, url: "https://gamebrain.co/game/subterrarium", note: "агрегатор: «digging, gardening, and vending machines», дата 2015"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Subterrarium+slimefriend+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-by-input, dig-terrain, gravity-fall, ladder-climb, round-currency, bomb-fuse, explode-area, environment-death, player-death, permadeath, sequential-levels, tutorial-window, keyboard-controls, +turn-based-gravity, +jump-fixed-height, +fuel-ammo, +plant-seed-growth, +cascade-gravity, +procedural-levels, +move-instability, +vending-machine, +air-jump-fuel]
proposes: ["+card:move-instability", "+card:vending-machine", "+card:air-jump-fuel", "+card:turn-based-gravity"]
author: opus
date: 2026-11-09
---

# Subterrarium — копай додому крізь ґрунт, що слабшає з кожним кроком; монети з землі → газовані напої → рослини-інструменти

## Суть
Покроковий пазл-платформер: героїня риє тунелі додому, а кожен вибитий блок землі дає монету. Монети витрачаються в автоматах на газовані напої — «паливо», яким заправляють джетпак на додатковий стрибок, поливають насіння (ліана для висоти, бомбова рослина розчищає шматок землі) або підривають бомби. Пастка гри — стійкість ґрунту: кожен хід її зменшує, і один зайвий крок обвалює землю над головою («dirtalanche») — смертельно. Таймінгу нема, лише планування ходів.

## Поле і час
- Квадратна сітка земляних блоків, вид збоку; гравітація вниз діє на героїню й землю.
- Хід = одна дія (крок, копання, стрибок, полив); між ходами світ стоїть. За оглядом: якщо не рухатись, земля над головою «висить» нескінченно, хоча бомби відлічують своє (?).
- Два режими з однаковими правилами: Challenge — 8 ручних рівнів з задуманим розвʼязком; Adventure — нескінченні процедурні рівні з аркадним прогресом.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Героїня | player | 1 життя | крок, копання в будь-якому напрямку, стрибок на 1 клітину |
| Земляний блок | terrain | стійкість (спільна?) | копається → +1 монета; при обвалі падає |
| Автомат з напоями | neutral | ціна в монетах | продає газований напій (паливо) |
| Газований напій (паливо) | resource | кількість | джетпак (+1 стрибок), полив насіння, підрив бомби |
| Насіння | spawner | вид рослини | політе → виростає рослина |
| Ліана | object | висота | росте вгору; по ній лізуть на висоту |
| Бомбова рослина | object | — | вибухом розчищає шматок землі |
| Гриб | object | — | теж поливається паливом; ефект (?) |
| Бомба | hazard | відлік | після запуску відлічує ходи й вибухає → обвал |
| Дім / вихід | static | — | мета рівня (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, dir)` → ЯКЩО `free(target)` → ТО `move(heroine, dir)`, `counter(stability, -1)`.
- КОЛИ `input(dig, dir)` → ЯКЩО `cell(target, dirt)` → ТО `set_cell(target, empty)`, `currency(+1)`.
- КОЛИ `input(jump)` → ЯКЩО `supported(heroine)` → ТО `move(heroine, up)` — лише на 1 клітину.
- КОЛИ `input(jump)` → ЯКЩО `not supported(heroine)` і `has(heroine, soda)` → ТО `take(heroine, soda)`, `move(heroine, up)` — джетпак.
- КОЛИ `turn_end(heroine)` → ЯКЩО `not supported(heroine)` → ТО `fall(heroine)`.
- КОЛИ `contact(heroine, vending_machine)` → ЯКЩО `counter(coins, >=, price)` → ТО `currency(-price)`, `give(heroine, soda)`.
- КОЛИ `input(water, seed)` → ЯКЩО `has(heroine, soda)` → ТО `take(heroine, soda)`, `transform(seed, plant)`.
- КОЛИ `spawned(vine)` → ТО `grow(vine, n)` вгору; героїня лізе по ліані.
- КОЛИ `input(use, bomb_plant)` → ТО `explode(area, n, empty)` — розчищає шматок землі (?).
- КОЛИ `input(trigger, bomb)` → ЯКЩО `has(heroine, soda)` → ТО `take(heroine, soda)`, `timer(start, n)`.
- КОЛИ `counter(bomb_fuse, ==, 0)` → ТО `explode(area, n, empty)`, `custom: «обвал землі (dirtalanche)»`.
- КОЛИ `counter(stability, <=, 0)` → ТО `custom: «обвал: незакріплена земля падає»`, `fall(dirt)`.
- КОЛИ `contact(falling_dirt, heroine)` → ТО `lose` — смертельний обвал.
- КОЛИ `reach(heroine, home)` → ТО `win`, `next_level` (?).
- Перемога: дістатися дому (?) · Поразка: обвал (permadeath) або глухий кут · Рахунок: Adventure — аркадний прогрес (?).

## Керування і ввід
- Лише клавіатура: напрямок = крок або копання в той бік; стрибок; полив / застосування — окремі клавіші (?).
- Покрокове: жодного тиску часу.

## Вікна, меню, HUD
- `main-menu` (?): Challenge · Adventure · навчання.
- `tutorial-window` — інтерактивне навчання (itch: accessibility).
- `game-screen`: печера, `coins`, запас напоїв (?), відлік бомб (?).
- `end-screen` після обвалу або виходу — (?).
- `settings-window` — кольори для дальтоніків (?).

## Фічі поза полем
- `mode-puzzle` (Challenge, 8 рівнів) і `mode-endless` (Adventure, процедурні рівні, що щоразу інші).
- `tutorial`, `colorblind-palette` (itch: «Color-blind friendly»).
- Сесія ≈ пів години (itch).

## Варіації й родичі
- У сімʼї: [motherload](motherload.md) і [steamworld-dig](steamworld-dig.md) (копання за гроші, магазин), [dig-dug](dig-dug.md), [mr-driller](mr-driller.md) (небезпека згори), [dig-dig-boom](dig-dig-boom.md) (теж покрокова гравітація).
- **Осі варіацій**: що спричиняє обвал — втрата опори (Boulder Dash) / вичерпана стійкість від ходів (Subterrarium) / таймер-хитання (Mr. Driller); звідки інструменти — магазин (Motherload) / вирощуєш на полі з купленого ресурсу (Subterrarium).

## Цікавинки для курсу
- Стійкість ґрунту як лічильник ходів → обвал — 📎 (глобальний бюджет ходів у «фізичній» обгортці).
- Один ресурс, три застосування (джетпак, полив, бомба) — 🌱; економіка «блок → монета → напій» — 🌱.
- Насіння → рослина-інструмент (ліана росте вгору клітинами) — 🥉.
- Покрокова гравітація героїні й землі з бомбою, що відлічує ходи — 🥉.
- Процедурний режим нескінченних рівнів з гарантованою прохідністю — 🥇.

## Мапа на каталог
- Є: `move-by-input` · `dig-terrain` · `gravity-fall` · `ladder-climb` ↔ ліана · `round-currency` ↔ монети · `bomb-fuse` · `explode-area` ↔ бомбова рослина · `environment-death` ↔ обвал · `player-death` + `permadeath` · `sequential-levels` ↔ Challenge · `tutorial-window` · `keyboard-controls`.
- Повтори з корпусу: `+jump-fixed-height` (1 клітина) · `+fuel-ammo` (напій як паливо й «заряд») · `+plant-seed-growth` · `+cascade-gravity` · `+procedural-levels` · `+turn-based-gravity` (запропоновано в dig-dig-boom).
- **Нема** → пропозиції карток:
  - `+move-instability` «Кожен хід послаблює ґрунт до обвалу» · entities/state · 📎 · слот {budget}.
  - `+vending-machine` «Автомат-крамниця на полі» · game-logic/economy · 🌱.
  - `+air-jump-fuel` «Додатковий стрибок у повітрі за паливо» · entities/move · 🌱.

## Пропозиції до словників
- `+card:move-instability` — ґрунт слабшає від кожного ходу (Subterrarium).
- `+card:vending-machine` — купівля в обʼєкта на полі, а не в меню.
- `+card:air-jump-fuel` — джетпак: стрибок у повітрі коштує ресурс.
- `+card:turn-based-gravity` — повтор з dig-dig-boom.

## Джерела
- ⭐ [itch.io: Subterrarium](https://slimefriend.itch.io/subterrarium) — опис механіки, теги (turn-based, permadeath, puzzle-platformer), клавіатура, дальтонікам, інтерактивне навчання, сесія ~30 хв.
- [Steam](https://store.steampowered.com/app/467170/) — 26.05.2016, Adventure з процедурними пазлами.
- [Steam-огляди](https://steamcommunity.com/app/467170/reviews/?browsefilter=toprated) — підйом на 1, монета за блок, паливо (джетпак/полив/бомби), «dirtalanche», 8 ручних рівнів, режими.
- [gamebrain](https://gamebrain.co/game/subterrarium) — «digging, gardening, and vending machines».
- YouTube: пошук «Subterrarium slimefriend gameplay».

## Непевне
- (?) Рік: Steam — 2016-05-26, gamebrain — 2015-07-30 (ймовірно itch-реліз); у черзі рік не вказано.
- (?) Як саме рахується стійкість (спільний лічильник рівня чи на блок) і які блоки падають при обвалі.
- (?) «Земля висить, якщо не рухаєшся, а бомби відлічують» — переказ одного огляду; точна семантика тіку не перевірена.
- (?) Що дає гриб; чи «rocket fuel» з огляду = газований напій з опису; мета рівня («дім») і рахунок Adventure.
