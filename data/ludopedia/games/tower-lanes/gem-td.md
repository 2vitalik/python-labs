---
title: Gem TD (Gem Tower Defense, Gem Tower Defense 2)
slug: gem-td
aka: [Gem Tower Defense, Gem Tower Defense 2, Gem TD+, GTD2, Самоцвітний TD]
family: tower-lanes
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: survive
year: 2022
platforms: [Warcraft III (custom map), PC (Steam)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1953220/Gem_Tower_Defense_2/", best: true, note: "Gem Tower Defense 2 (2022): 5 випадкових самоцвітів за хвилю, один лишаєш, решта — камені лабіринту; злиття ×2/×4, рецепти, зіркові й еволюційні вежі"}
  - {kind: other, url: "https://github.com/nvs/gem", note: "Gem TD+ — оновлена WC3-мапа (оригінал Bryvx), README"}
  - {kind: other, url: "https://raw.githubusercontent.com/nvs/gem/master/CHANGELOG.md", note: "changelog Gem TD+: Keep / Combine 2x/3x/4x / Downgrade, чекпоінти, slates, Extra Chance, Level 50 бос, leak з 10-го рівня = поразка"}
  - {kind: other, url: "https://github.com/M3etis/GemTD", note: "фанатський клон (Godot): 8 типів × 5 якостей, 13 спецвеж, 12 slates, рівні удачі — свої числа"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Gem+TD+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [tower-placement, tower-range, chase-bfs, enemy-waves, spawn-schedule, spawn-points, enemy-reached-base, tile-merge, weighted-spawn, round-currency, in-round-upgrades, hp-damage, speed-per-type, status-effects, teleport, cell-click, keyboard-controls, +maze-by-towers, +keep-one-rest-wall, +tower-recipe-table, +waypoint-route, +downgrade-for-recipe, +star-merge, +tower-evolve, +luck-chance-upgrade, +aura-slate, +flying-ignores-maze, +leak-loss-after-level, +blocked-teleport-checkpoint]
proposes: ["+effect:keep", "+effect:upgrade", "+effect:recompute_path", "+role:waypoint", "+role:blocker", "+trigger:build_phase", "+cond:recipe_match", "+ui:recipe-table", "+ui:chance-indicator", "+ui:dps-meter", "+window:recipe-book"]
author: opus
date: 2026-11-09
---

# Gem TD — щохвилі 5 випадкових самоцвітів: один лишаєш вежею, решта стають каменями твого лабіринту

## Суть
Mazing-TD з Warcraft III (мапа Bryvx), відома як Gem TD; Gem TD+ — її оновлення спільнотою, Gem Tower Defense 2 (2022) — окрема гра в Steam. Поле відкрите, вороги біжать від спавну через чекпоінти до виходу, а гравець перед кожною хвилею ставить **5 самоцвітів**: тип і якість кожного випадкові. Лише один стає вежею — решта чотири перетворюються на камені й працюють як стіни лабіринту. Тому кожен раунд — подвійне рішення: де поставити п'ять клітин стін і яку одну вежу залишити (або злити однакові, або зібрати рецепт спецвежі).

## Поле і час
- Квадратна будівельна сітка без дороги, вхід, кілька чекпоінтів і вихід фіксовані; шлях прокладається між чекпоінтами по черзі.
- Раунд = фаза будування (5 самоцвітів + вибір) → хвиля в реальному часі; вежі бʼють самі.
- Повністю перекрити шлях не можна: гра попереджає гравця, що блокує; у Gem TD+ ворог, упершись у блок, телепортується до наступного чекпоінта.
- Повітряні рівні — летючі вороги (лабіринт для них, імовірно, не діє (?)).
- Рівні нумеровані (у Gem TD+ — щонайменше до 50-го з босом Damage Test).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Самоцвіт (gem) | tower | тип (8), якість | ставиться на клітину; лишений — вежа, що автоматично бʼє в радіусі |
| Якості | — | Chipped → Flawed → Normal → Flawless → Perfect → Great | вища якість = сильніша вежа; шанс якості задає рівень удачі |
| Камінь (stone/rock) | static (`+role:blocker`) | 1 клітина | неналишений самоцвіт стає непрохідним каменем лабіринту |
| Спецвежа (synthesis) | tower | рецепт | лише з рецепта: Star Ruby, Blood Star, Fire Star, Opal Vein, Uranium 235/238, Paraiba Tourmaline тощо |
| Slate (кам'яна плита) | zone | тип: Damage, Hold, Slow, Poison, Air, Spell… | плита з аурою (шкода/утримання/сповільнення/баф); у Gem TD+ — рухома в межах зони гравця, 2 базові → комбо (Hold + Air = Ancient) |
| Зіркова вежа (GTD2) | tower | 1–3 ★ | супер-злиття лишених однакового типу; далі в синтез не йде |
| Еволюційна вежа (GTD2) | tower | гілки еволюції | синтезована вежа росте за золото до найвищого рівня |
| Спавн | spawner | — | хвиля виходить тут |
| Чекпоінт | static (`+role:waypoint`) | номер | ворог мусить пройти по черзі |
| Вихід / фортеця | static | — | ворог дійшов → «leak» |
| Ворог наземний | enemy | HP, швидкість, броня | найкоротший шлях між чекпоінтами |
| Ворог летючий | enemy | HP | повітряні рівні |
| Бос Damage Test | boss | HP | 50-й рівень (Gem TD+), разом з міньйонами |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `custom: «trigger build_phase»` → ТО гравець 5 разів `input(place, gem, cell)` → ЯКЩО `free(cell)` and `path_exists(spawn, exit)` → ТО `place(gem, cell)`, `custom: «тип і якість — випадково за рівнем удачі»`; інакше `block` + попередження.
- КОЛИ `input(keep, gem)` → ТО `custom: «effect keep: gem лишається вежею»`, `transform(other_4_gems, stone)`.
- КОЛИ `input(combine_2x, gem)` → ЯКЩО `custom: «серед 5 щойно поставлених ≥2 однакових»` → ТО `merge(gem, gem → quality+1)`, решта → `transform(stone)`.
- КОЛИ `input(combine_4x, gem)` → ЯКЩО `custom: «≥4 однакових»` → ТО `merge(→ quality+2)`; у Gem TD+ є й Combine (3x) — три однакових пропускають якість.
- КОЛИ `input(special, gem)` → ЯКЩО `custom: «cond recipe_match: 5 поставлених збігаються з рецептом»` → ТО `transform(gem, special_tower)`, решта → `transform(stone)`.
- КОЛИ `input(special, tower)` → ЯКЩО `custom: «на полі вже стоять усі складники рецепта»` → ТО `merge(ingredients → special_tower)`, `custom: «складники стають каменями (?)»`.
- КОЛИ `input(downgrade, gem)` → ТО `transform(gem, quality-1)`, `custom: «keep»` — щоб влізти в рецепт.
- КОЛИ `input(star_merge, towers)` → ЯКЩО `same(kept_a, kept_b, type)` and `custom: «зірок < 3»` → ТО `merge(→ star+1)` (GTD2).
- КОЛИ `input(evolve, tower)` → ЯКЩО `has(gold, cost)` → ТО `currency(-cost)`, `transform(tower, next_evolution)` (GTD2).
- КОЛИ `input(extra_chance, target_quality)` → ЯКЩО `has(gold, cost)` → ТО `currency(-cost)`, `custom: «бонус шансу на target росте з кожним раундом будування»` (Gem TD+; у ранніх версіях — апгрейд рівня шансу).
- КОЛИ `wave_start` → ТО `spawn_at(wave, spawn)`; КОЛИ `tick` → ТО `move(enemy, next_on_path)` до найближчого непройденого чекпоінта.
- КОЛИ `blocked(enemy)` → ТО `teleport(enemy, next_checkpoint)` (Gem TD+).
- КОЛИ `in_range(tower, enemy, r)` → ТО `damage(enemy, n)` з перезарядкою; спецвежі й slates — `speed(enemy, ×k)`, `set_state(enemy, poison, dur)`, `stun(enemy, n)`.
- КОЛИ `in_range(slate, tower, r)` → ТО `custom: «аура-баф вежі»`.
- КОЛИ `input(move, slate, cell)` → ЯКЩО `custom: «клітина в зоні гравця»` → ТО `teleport(slate, cell)`.
- КОЛИ `hp_zero(enemy)` → ТО `disappear(enemy)`, `currency(+bounty)`.
- КОЛИ `reach(enemy, exit)` → ЯКЩО `level(>=, 10)` → ТО `lose` (Gem TD+); раніше — лише втрата часу й нагороди.
- КОЛИ `wave_start` → ЯКЩО `level(==, 50)` → ТО `spawn_at(boss_damage_test, spawn)` разом з міньйонами.
- Перемога: пережити останню хвилю · Поразка: «leak» після 10-го рівня (Gem TD+) / ворог у фортеці (GTD2 (?)) · Рахунок: час і результат для рейтингу (Gem TD+, лідерборди спільноти).

## Керування і ввід
- Миша: клік по клітині ставить самоцвіт (5 за раунд); клік по самоцвіту → кнопки Keep / Combine (2x, 4x; у Gem TD+ ще 3x) / Downgrade / спецсинтез.
- GTD2: пробіл — швидко поставити й лишити; клік по будь-якому самоцвіту, коли 5 збігаються з рецептом, — синтез.
- Золото — на шанс якості, апгрейд веж і еволюцію (GTD2).

## Вікна, меню, HUD
- `game-screen`: сітка з чекпоінтами, `coins`, `level-number` / `wave-counter`, кнопки дій над вибраним самоцвітом, `+ui:chance-indicator` і `+ui:dps-meter` (Gem TD+ дошка).
- `+window:recipe-book` — таблиця рецептів спецвеж (`+ui:recipe-table`) (?).
- `main-menu`, `end-screen` (?) — у GTD2; лобі WC3 з вибором раси (лише косметика) — `lobby-window`.
- Переходи: лобі / меню → гра → поразка або перемога → результат.

## Фічі поза полем
- WC3: мультиплеєр — кожен гравець у своїй зоні мапи; команда `-maze` вмикає/вимикає mazing-режим (`custom-rules`).
- Лідерборди Gem TD+ — у спільноті (Discord, репозиторій зі скріншотами й повторами) (`replay`).
- GTD2: лише одиночна гра; китайська й англійська локалізація.

## Варіації й родичі
- Gem TD (WC3, Bryvx) → Gem TD+ (WC3, спільнота: Combine 3x, Extra Chance замість рівнів шансу, без життів) → Gem Tower Defense 2 (Steam, Ranger Game: зіркові й еволюційні вежі, slates лише в раунді синтезу).
- Фанатські клони (Godot-клон: 8 типів × 5 якостей, 13 спецвеж × 3 рівні, 12 slates, 9 рівнів удачі, ламання стін).
- Родичі в корпусі: [mazing-td-modern](mazing-td-modern.md), [desktop-tower-defense](desktop-tower-defense.md), [element-td-2](element-td-2.md) (рецепти з елементів), [gemcraft](gemcraft.md) (злиття самоцвітів), [random-dice](random-dice.md) (злиття однакових випадкових), [circuit-maze](circuit-maze.md) (лабіринт без бою).
- **Осі варіацій**: стіни — вежі самі / окремі блоки / **невдалі кидки удачі** · вибір — купуєш вежу / тягнеш 5 випадкових і лишаєш 1 · злиття — 2→+1, 3→+1 через крок, 4→+2 · удача — фіксована / рівень за золото / бонус, що росте.

## Цікавинки для курсу
- «5 кидків → 1 вежа, 4 стіни»: випадковість веде і бойовою силою, і геометрією лабіринту — 🥉.
- Таблиця рецептів + перевірка збігу серед 5 щойно поставлених і серед усіх на полі — 🥈 (мультимножинний пошук, вибір складників).
- Злиття однакових ×2/×4 з пропуском якості, Downgrade заради рецепта — 📎.
- Шлях через чекпоінти по черзі + заборона повного блоку + телепорт до наступного чекпоінта, якщо заблоковано — 🥇 (BFS по сегментах, перевірка до посадки).
- Зважена випадковість якості з рівнем удачі / бонусом, що росте, — 📎.
- Slates: аура на зону з рухомою плитою й злиттям двох типів — 🥉.

## Мапа на каталог
- Є: `tower-placement` + `tower-range` · `chase-bfs` ↔ шлях між чекпоінтами · `enemy-waves` + `spawn-schedule` + `spawn-points` · `enemy-reached-base` ↔ leak · `tile-merge` ↔ Combine · `weighted-spawn` ↔ шанс якості · `round-currency` · `in-round-upgrades` ↔ апгрейд і еволюція · `hp-damage` · `speed-per-type` · `status-effects` ↔ отрута/сповільнення · `teleport` ↔ ворог до наступного чекпоінта · `cell-click` · `keyboard-controls` ↔ пробіл і кнопки.
- **Нема** → пропозиції карток:
  - `+maze-by-towers`, `+waypoint-route`, `+tower-recipe-table`, `+tower-evolve`, `+flying-ignores-maze` — уже пропонувались сімʼєю (DTD, Element TD 2, Legion TD).
  - `+keep-one-rest-wall` «N випадкових — один лишаєш, решта стають стінами» · game-logic/economy · 🥉 · слот {n: 5}.
  - `+downgrade-for-recipe` «Понизити рівень заради рецепта» · game-logic/economy · 🌱.
  - `+star-merge` «Супер-злиття лишених однакового типу, ★1–3» · entities/legality · 📎.
  - `+luck-chance-upgrade` «Рівень удачі зсуває ймовірності якості» · entities/spawn · 📎 · слот {levels}.
  - `+aura-slate` «Плита-аура на підлозі» · entities/state · 📎.
  - `+leak-loss-after-level` «Пропуск ворога програшний лише з рівня N» · game-logic/lose · 🌱 · слот {n: 10}.
  - `+blocked-teleport-checkpoint` «Заблокований ворог перескакує до наступного чекпоінта» · entities/move · 🌱.

## Пропозиції до словників
- `+effect:keep` — вибрати один з кандидатів, решта стають іншим (стіною); `+effect:upgrade`, `+effect:recompute_path` — підтвердження сімʼї.
- `+role:waypoint`, `+role:blocker` — підтвердження (Element TD 2); роль `tower` уже є в `roles.md`.
- `+trigger:build_phase` — почалась фаза будування раунду (підтвердження Legion TD).
- `+cond:recipe_match` — набір сутностей збігається з рецептом.
- `+ui:recipe-table` (підтвердження), `+ui:chance-indicator` — поточний бонус шансу, `+ui:dps-meter` — шкода за секунду.
- `+window:recipe-book` — книга рецептів спецвеж.

## Джерела
- ⭐ [Steam: Gem Tower Defense 2](https://store.steampowered.com/app/1953220/Gem_Tower_Defense_2/) — 5 випадкових самоцвітів, Keep, камені-лабіринт, злиття 2→+1 і 4→+2, рецепти серед 5 і на полі, Downgrade, базові 8 типів × 6 рівнів, синтезовані, slates, зіркові, еволюційні вежі, пробіл.
- [GitHub: nvs/gem (Gem TD+)](https://github.com/nvs/gem) — оновлена WC3-мапа, оригінал Bryvx, лідерборди в спільноті.
- [CHANGELOG Gem TD+](https://raw.githubusercontent.com/nvs/gem/master/CHANGELOG.md) — Keep/Combine 2x/3x/4x/Downgrade, назви спецвеж і slates, чекпоінти й телепорт при блоці, попередження про блок, Extra Chance, leak ≥ 10 = поразка, Level 50 Damage Test, `-maze`.
- [GitHub: M3etis/GemTD](https://github.com/M3etis/GemTD) — фанатський клон з повним описом циклу раунду (числа клону, не оригіналу).
- YouTube: [пошук «Gem TD gameplay»](https://www.youtube.com/results?search_query=Gem+TD+gameplay).

## Непевне
- (?) Рік і автор оригінальної WC3-мапи (лише «Bryvx»); чи була версія для Dota 2 — не перевірено.
- (?) Назви 8 базових типів: у джерелах видно лише Ruby, Emerald, Opal (решта, як-от Amethyst, Aquamarine, Diamond, Sapphire, Topaz, — з памʼяті).
- (?) Якості: GTD2 каже «6 рівнів», changelog Gem TD+ — Flawed…Great; Chipped як найнижча — зі сніпета пошуку.
- (?) Чи лабіринт діє на летючих; чи складники рецепта з поля стають каменями.
- (?) Розмір сітки, кількість чекпоінтів, рівнів і життів у GTD2; що буває при leak у GTD2.
- (?) Slates у GTD2 «використовні лише в раунді, коли поставлені й синтезовані» — формулювання Steam неоднозначне.
