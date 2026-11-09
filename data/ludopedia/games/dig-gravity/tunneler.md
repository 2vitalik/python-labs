---
title: Tunneler
slug: tunneler
aka: [TUNNELER 2.0]
family: dig-gravity
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: hotseat
  info: partial
  random: setup
  goal: state
year: 1991
platforms: [MS-DOS, Linux (ремейк Kaniansky)]
links:
  - {kind: official, url: "https://kaniansky.com/tunneler/", best: true, note: "ремейк за декомпільованим кодом: правила оригіналу, ціни дій у енергії, бази, клавіші, раунди, режими"}
  - {kind: other, url: "https://dosgames.com/game/tunneler", note: "оригінал: Geoffrey Silverton, 1991, shareware, 2 гравці за однією клавіатурою, «тунелюй до суперника»"}
  - {kind: other, url: "https://github.com/kaniansky/tunneler", note: "README: оригінал байт-у-байт (BLUE vs GREEN, medium-мапа, 3 раунди), розміри мап, текстовий режим 160×100, без лінії зору в оригіналі"}
  - {kind: other, url: "https://raw.githubusercontent.com/kaniansky/tunneler/main/docs/NOTES.md", note: "нотатки декомпіляції: танк 7×7, вʼюпорт 76×71, тік 54.9 мс, бази з двома проходами, енергія 3500/10500"}
  - {kind: other, url: "https://flathub.org/zh-Hans/apps/com.kaniansky.Tunneler", note: "Flathub: «кожен бачить лише мале вікно довкола себе», режими, skirmish, онлайн до 8"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Tunneler+1991+DOS+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-by-input, move-8dir, keyboard-controls, dig-terrain, destructible-blocks, impassable-cells, projectile-shot, hp-damage, player-death, hot-seat, player-camera, status-panel, game-screen, end-screen, ai-opponent, online-multiplayer, in-game-editor, fog-of-war, minimap-radar, controls-remap, +split-screen-duel, +fuel-ammo, +action-energy-cost, +base-refuel-repair, +rounds-to-win]
proposes: ["+effect:refuel", "+effect:repair", "+role:base", "+ui:split-screen", "+card:action-energy-cost", "+card:base-refuel-repair", "+card:rounds-to-win"]
author: opus
date: 2026-11-09
---

# Tunneler — два танки під землею: кожен бачить лише своє вікно, риє тунель до суперника і стріляє, поки не скінчилась енергія

## Суть
DOS-дуель двох гравців за однією клавіатурою: танки BLUE і GREEN стартують у своїх базах глибоко в землі й мають прорити шлях один до одного, перш ніж зможуть стріляти. Кожна дія коштує енергії — рух дешево, копання дорожче, постріл найдорожче; енергію поповнює будь-яка база, щит лагодить лише своя. Екран розділено навпіл, і кожен гравець бачить тільки невелике вікно довкола свого танка — суперника треба знайти. Раунд виграє той, хто лишився живим; матч — до трьох раундів.

## Поле і час
- Мапа — растр клітин-пікселів: земля, незламний камінь, тунелі, дві бази; розмір оригіналу — «medium» 1024×512 (README ремейку); мапа генерується генератором оригіналу (`random: setup`).
- Танк займає 7×7 клітин; рух у 8 напрямках (дві клавіші — діагональ).
- Камера: екран розділено на два вікна, кожне довкола свого танка (вʼюпорт 76×71 з нотаток ремейку, ?) (`info: partial` — решту мапи не видно; лінії зору в оригіналі нема — у вікні видно все).
- Час — real-time, тік = один тік таймера BIOS ≈ 54.9 мс; обидва гравці діють одночасно.
- Відображення оригіналу — текстовий режим 160×100 «пікселів» у 16 кольорах.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Танк BLUE / GREEN | player | енергія, щит; 7×7 | їде 8 напрямками, риє землю, стріляє вперед |
| Земля (dirt) | terrain | — | прокопується рухом або пострілом → тунель |
| Тунель | terrain | — | вільний прохід |
| Камінь | static | — | не копається, зупиняє танк і постріл |
| Своя база | zone | стіни з двома проходами (?) | поповнює енергію й лагодить щит |
| Чужа база | zone | — | поповнює лише енергію |
| Снаряд | projectile | — | летить по напрямку танка; прибирає землю; ранить танк |
| Уламки вибуху | object | випадковий розкид | лишаються після знищеного танка (?) |
| Вода (ремейк 1.3+) | terrain | — | половина швидкості, не копається, постріли пролітають над нею |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cells_ahead)` → ТО `move(tank, dir)`, `counter(energy, −move_cost)`.
- КОЛИ `input(dir)` → ЯКЩО `cell(cells_ahead, dirt)` → ТО `set_cell(cells_ahead, tunnel)`, `move(tank, dir)` повільніше, `counter(energy, −dig_cost)`; dig_cost > move_cost.
- КОЛИ `input(dir)` → ЯКЩО `cell(cells_ahead, rock)` → ТО `block`.
- КОЛИ `input(fire)` → ТО `spawn(shot)` у напрямку танка, `counter(energy, −shot_cost)`; постріл — найдорожча дія.
- КОЛИ `contact(shot, dirt)` → ТО `set_cell(cell, tunnel)`, `disappear(shot)`; тому стрільба на ходу риє швидше.
- КОЛИ `contact(shot, rock)` → ТО `disappear(shot)`.
- КОЛИ `contact(shot, tank)` → ТО `damage(tank.shield, n)`, `disappear(shot)`.
- КОЛИ `hp_zero(tank)` → ТО `explode(circle, r)`, `custom: «танк знищено: чорний екран DESTROYED і уламки»`.
- КОЛИ `counter(energy, ==, 0)` → ТО `custom: «танк вибухає без енергії»`.
- КОЛИ `enter(tank, base)` → ТО `custom: «поповнити енергію»` — будь-яка база.
- КОЛИ `enter(tank, own_base)` → ТО `heal(tank.shield, n)`; у ремейку база союзника лагодить удвічі повільніше.
- КОЛИ `custom: «лишився один танк»` → ТО `counter(rounds, +1)` переможцю, наступний раунд на новій мапі (?).
- КОЛИ `counter(rounds, ==, 3)` → ТО `win`.
- Ремейк, ліміт часу раунду: КОЛИ `timer(round_limit)` → ТО раунд виграє сторона з більшою кількістю влучань.
- Перемога: знищити танк суперника (3 раунди) · Поразка: щит або енергія 0 · Рахунок: виграні раунди.

## Керування і ввід
- BLUE: W A S D — рух, Left Shift / Space — постріл. GREEN: стрілки — рух, Enter / Right Shift — постріл.
- Дві клавіші напряму — діагональ; стріляти можна на ходу.
- Ремейк: Tab — рахунок (і мапа, якщо увімкнена); перепризначення клавіш, геймпади, тач.

## Вікна, меню, HUD
- `splash-screen` / заголовок раунду (колір циклічно мерехтить).
- `game-screen`: два вікна (`split-screen`), під кожним — `energy-bar` і `shield-bar` свого танка (?) щодо розташування.
- `end-screen`: чорний екран DESTROYED у вікні знищеного; підсумок раундів.
- Ремейк: `main-menu` → `match-setup` (режим, мапа small/medium/large, раунди 1–9, ліміт часу, friendly fire, лінія зору, показ мапи), `lobby-window` онлайн (місця, команди, чат, глядачі), `editor-window` (інструменти: тунель, земля, камінь, вода, база), тренувальний полігон.
- Переходи: старт → раунд → DESTROYED → наступний раунд → переможець матчу.

## Фічі поза полем
- Оригінал: лише hot-seat двох гравців, 3 раунди, shareware (1991), Turbo Pascal, звук PC-speaker.
- Ремейк Kaniansky (Flathub, v1.5.2): `custom-rules` (розмір мапи, раунди, час, friendly fire), `ai-opponent-levels` (1–7 CPU easy/medium/hard, free-for-all або команди), `online-multiplayer` до 8 танків, `level-editor`, опційні `fog-of-war` (лінія зору — лампи не світять крізь землю й камінь) і мапа на Tab, що оновлюється лише побаченим, `remap-controls`, `localization` (EN, SK, CZ, UA, RU).

## Варіації й родичі
- Режими ремейку: Gold Rush (золото — на свою базу, влучання вибиває), Infection (заражений заражає тих, кого знищив), Survival (до 10 хвиль CPU), King of the Hill, Shrinking World (безпечна зона меншає кожні 30 с, поза нею тане щит), CTF, Base Siege (бази руйнуються), Deathmatch (респавн за 3 с, ліміт фрагів), Hot Potato.
- У сімʼї: [liero.md](liero.md) — той самий split-screen поєдинок у копаній землі, але бічний вид, гравітація, мотузка; [dig-dug.md](dig-dug.md) — тунелі з видом згори; [scorched-earth.md](scorched-earth.md) — танки й руйнований рельєф покроково.
- **Осі варіацій**: видимість «вікно довкола себе / лінія зору / уся мапа»; ресурс «одна енергія на рух, копання і постріл / окремі патрони»; бази «лише своя лагодить / будь-яка заправляє / руйнуються»; ціль «вижити в раунді / фраги / прапор / золото».

## Цікавинки для курсу
- Дві камери-вікна на одному полі, кожна центрована на своєму танку — 📎.
- Єдина енергія як ціна всіх дій (рух < копання < постріл) + заправка на базі — 🌱.
- Щит і енергія: дві смерті з різних причин, різне відновлення (своя / будь-яка база) — 🌱.
- Постріл, що копає землю (стрільба на ходу пришвидшує тунель) — 🌱.
- Генератор мапи: земляний масив із камінням і двома базами на відстані — 📎.
- Лінія зору ремейку: лампа танка не світить крізь землю — 🥉 (raycast по растру).
- Shrinking World — безпечна зона, що стискається за таймером — 📎.

## Мапа на каталог
- Є: `move-by-input` + `move-8dir` + `keyboard-controls` ↔ WASD/стрілки з діагоналями · `dig-terrain` + `destructible-blocks` ↔ земля → тунель · `impassable-cells` ↔ камінь · `projectile-shot` · `hp-damage` ↔ щит · `player-death` · `hot-seat` ↔ одна клавіатура · `player-camera` ↔ вікно за танком · `status-panel` ↔ смуги енергії й щита · `game-screen` / `end-screen` · ремейк: `ai-opponent`, `online-multiplayer`, `in-game-editor`, `fog-of-war`, `minimap-radar`, `controls-remap`.
- **Нема** → пропозиції карток:
  - `+action-energy-cost` «Кожна дія має ціну в енергії» · game-logic/economy · 🌱 · слоти {move, dig, shoot}.
  - `+base-refuel-repair` «База: заправка будь-яка, ремонт лише своя» · entities/interact · 🌱.
  - `+rounds-to-win` «Матч до N виграних раундів» · game-logic/win · 🌱 · слот {n: 3}.
  - Повтори: `+split-screen-duel` (Liero), `+fuel-ammo` — енергія і як паливо, і як набої.

## Пропозиції до словників
- `+effect:refuel` — повтор (Motherload): поповнити ресурс-таймер (тут — на базі).
- `+effect:repair` — повтор: відновити щит/корпус на базі.
- `+role:base` — повтор: власна зона гравця, що дає ресурси й ремонт.
- `+ui:split-screen` — повтор (Liero): поле показано двома камерами.

## Джерела
- ⭐ [Tunneler (Kaniansky)](https://kaniansky.com/tunneler/) — «Two tanks under the ground»: ціни рух < копання < постріл, бази (заправка / ремонт), камінь не копається, клавіші, раунди, режими.
- [DOS Games: Tunneler](https://dosgames.com/game/tunneler) — автор Geoffrey Silverton, 1991, shareware, 2 гравці за однією клавіатурою.
- [GitHub kaniansky/tunneler](https://github.com/kaniansky/tunneler) — оригінал байт-у-байт, мапи 512×256 / 1024×512 / 2048×1024, вода й редактор у 1.3+, лінія зору вимкнена в оригіналі, DESTROYED-екран.
- [NOTES.md](https://raw.githubusercontent.com/kaniansky/tunneler/main/docs/NOTES.md) — танк 7×7, вʼюпорт 76×71, тік 54.925 мс, бази з двома проходами, енергія 3500 → 10500 у тренуванні.
- [Flathub](https://flathub.org/zh-Hans/apps/com.kaniansky.Tunneler) — опис «кожен бачить лише мале вікно», режими, skirmish 1–7 CPU, онлайн до 8, мови.

## Непевне
- (?) Числа оригіналу: максимум енергії й щита, ціни дій, шкода снаряда — у джерелах нема (крім прикладу 3500/10500 із тренування ремейку).
- (?) Чи стіни бази незламні і скільки в них проходів в оригіналі (у нотатках — «два проходи»).
- (?) Чи нова мапа генерується щораунду, чи на весь матч.
- (?) Розташування смуг енергії/щита на екрані — з памʼяті, у джерелах лише «gauges».
- (?) Лінк черги `pemasat.itch.io/tunneler` — HTML5-«ремастер» з AI-контентом, «score chasing»; схоже, інша гра з тією ж назвою, у шапку не клав.
- (?) Чи снаряд зупиняється на першій клітині землі, чи прорізає кілька.
