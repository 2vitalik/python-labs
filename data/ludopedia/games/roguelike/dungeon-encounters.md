---
title: Dungeon Encounters
slug: dungeon-encounters
family: roguelike
also: [hidden-deduction]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: runtime
  goal: state
year: 2021
platforms: [Switch, PS4, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dungeon_Encounters", best: true, note: "сітка клітин з числами: білі — події, чорні — бої; ATB; фізичний/магічний захист блокує шкоду до нуля"}
  - {kind: steam, url: "https://store.steampowered.com/app/1451080/", note: "99 поверхів, мапа порожня до відвідування, очки здібностей за дослідження, журнал подій"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=dungeon+encounters+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-4dir, hp-damage, item-pickup, shop-catalog, round-currency, sequential-levels, player-death, reach-exit, temporary-modes, keyboard-controls, cell-click, minimap-radar, player-camera, +event-tile-codes, +dual-armor, +ability-points-explore, +movement-abilities, +revealed-by-step, +reveal-battles-ability, +rescue-fallen, +recruit-ally, +atb-combat, +event-log, +coordinate-warp]
proposes: ["+trigger:revealed", "+trigger:stepped(code)", "+cond:code(cell, n)", "+cond:has_ability(a)", "+cond:armor(kind, op, n)", "+effect:reveal(cells)", "+effect:battle(group)", "+effect:learn(ability)", "+effect:warp(floor, x, y)", "+role:event-tile", "+role:ally", "+ui:tile-code", "+ui:coordinates", "+ui:armor-bars", "+ui:atb-gauge", "+window:event-log", "+window:ability-window", "+window:shop-window", "+feature:codex", "+axis:render=abstract"]
author: opus
date: 2026-11-02
---

# Dungeon Encounters — RPG, де мапа — це лише сітка клітин з числами-кодами подій

## Суть
Загін із чотирьох шукачів спускається 99 (100) поверхами підземелля, яке на екрані — **лише сітка квадратів**: жодних стін, кімнат чи спрайтів. Мапа порожня, доки на клітину не ступили; деякі клітини несуть **число-код**: білі — події (здібність, скарб, лікування, торговець), чорні — бій. Сила гри — у розумінні кодів, зборі здібностей (які змінюють, як рухатись по сітці) і в детермінованому бою, де захист треба «зняти» до нуля, перш ніж пошкодити HP. Розробник Cattle Call, режисер Hiroyuki Ito (батько ATB), видавець Square Enix.

## Поле і час
- Поверх — квадратна сітка з розгалуженими «доріжками» клітин (WP: «board-like grid of squares with branching paths»); порожнеча між ними непрохідна без спеціальних здібностей (?).
- Видимість: мапа порожня до відвідування; кожна відвідана клітина зʼявляється (Steam: «visit every tile on each level»); чорні числа приховані, поки не ступиш або не відкриєш здібністю.
- Числа-коди — **шістнадцяткові** (00–FF?) (?) і означають тип події; гравець вивчає «словник» кодів сам (журнал подій).
- Час дослідження — покроковий (крок = хід); бій — ATB: шкала кожного юніта заповнюється, юніт діє, коли повна (WP).
- Мапи рукотворні (?), випадкові — влучання й шкала бою (`random: runtime`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Загін (маркер на мапі) | player | 4 бійці | рух по сусідніх клітинах; ступив — подія |
| Боєць | ally | HP, фізичний захист (PD), магічний захист (MD), швидкість ATB, спорядження, здібності | у бою обирає атаку фізичну чи магічну (?) |
| Порожня клітина | terrain | — | відкривається при відвідуванні |
| Біла клітина з кодом | static | код | подія: здібність, скарб, лікування, прихований торговець (Steam) |
| Чорна клітина з кодом | spawner | код = група ворогів | ступив → бій |
| Ворог | enemy | HP, PD, MD | атакує в ATB |
| Сходи вниз/вгору | static | — | перехід між поверхами |
| Торговець | neutral | товар | зброя, броня, здібності (WP: «buy … abilities in shops») |
| Загублений шукач | ally | — | знайти → може приєднатись (Steam) |
| Тіло полеглого бійця | container | — | повернути в загін (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move)` → ЯКЩО `free(cell)` або `has_ability(movement)` → ТО `move(party)`; ЯКЩО клітину вперше відвідано → ТО `reveal(cell)`, `counter(ability_points, +n)` (Steam: очки здібностей за дослідження).
- КОЛИ `stepped(code)` на білу клітину → ТО подія за кодом: `learn(ability)` / `give(item)` / `heal_full(party)` / `custom: «відкрити торговця»`; запис у `event-log`.
- КОЛИ `stepped(code)` на чорну клітину → ТО `battle(group(code))`.
- КОЛИ `input(reveal-battles ability)` → ТО `reveal(black cells)` — бій можна обійти або обрати (Steam).
- КОЛИ `tick` у бою → ТО `counter(atb, +speed)`; ЯКЩО повна → ТО юніт діє.
- КОЛИ фізична атака → ТО `custom: «шкода спершу знімає PD; лише при PD = 0 — HP»`; магічна — так само через MD. WP: «even a single point remaining in the defense will block damage».
- КОЛИ `hp_zero(enemy group)` → ТО `custom: «бій виграно»`, `give(gold|items)` (?).
- КОЛИ `hp_zero(member)` → ТО боєць вибуває; тіло лишається на клітині (?) — `rescue-fallen`.
- КОЛИ `all_gone(member)` → ТО `lose`, повернення на поверхню (?).
- КОЛИ `contact(party, stairs)` → ТО `next_level`.
- КОЛИ `input(warp ability, floor, x, y)` (?) → ТО `warp(floor, x, y)` — телепорт за координатами.
- КОЛИ `contact(party, lost adventurer)` → ТО `make_ally`.
- Перемога: дійти до найнижчого поверху й перемогти фінального ворога (?). Поразка: загін знищено. Рахунку нема.

## Керування і ввід
- Стрілки/стік — крок на сусідню клітину; кнопка — меню здібностей (рух, розвідка, телепорт).
- Бій: на кожного бійця, коли повна ATB, — вибір дії (фізична / магічна атака, здібність, ціль).
- Курсор на мапі: огляд кодів і координат (?).

## Вікна, меню, HUD
- `game-screen` — сітка поверху з кодами на клітинах (`tile-code`), `coordinates` (x, y) і номер поверху, `minimap` (?).
- Бійовий екран (`custom-window`): шкали `atb-gauge`, `armor-bars` (PD / MD / HP) кожного юніта.
- `event-log` — журнал усіх знайдених подій і кодів (Steam: «Event Log»).
- `ability-window` — встановлення здібностей за очки; `inventory-window` — спорядження; `shop-window`.
- `character-select` / склад загону, `main-menu`, `settings-window`, `save-slots` (?).
- Переходи: `main-menu` → `game-screen` (поверх) ↔ бій ↔ меню здібностей/журналу → наступний поверх.

## Фічі поза полем
- `codex` у формі журналу подій: «словник» кодів, який гравець збирає сам.
- `save-slots` / `autosave` (?), `difficulty-presets` (?).
- Без процедурної генерації (?) — повторне проходження ті самі мапи.

## Варіації й родичі
- Dungeon Master / Etrian Odyssey (сіткові данжі з картографуванням), Desktop Dungeons (числа на іконках), Minesweeper/Hexcells (числа = зміст клітини), Final Fantasy (ATB — від того ж автора).
- Осі варіацій: **рендер** (спрайти / ASCII / лише коди) · **знання** (подія підписана / код, який вчиш) · **шкода** (HP одразу / через шари броні з порогом) · **рух** (будь-куди / по доріжках / здібності відкривають нові способи руху).

## Цікавинки для курсу
- «Сітка — це весь UI»: поле з кодів подій замість графіки — 🌱 (ідеально для консольного рендера, `console-render`).
- Таблиця «код → подія» як дані (dispatch по числу) — 📎.
- Подвійна броня PD/MD, що блокує шкоду, поки >0 — 📎 (одна гілка, але змінює всю тактику).
- Здібності, що змінюють правила руху по сітці (через порожнечу, телепорт за координатами) — 🥉.
- ATB-бій: шкали заповнюються за швидкістю, хто першим повний — діє — 🥉 (черга подій у часі).
- Розкриття мапи кроком + очки за нові клітини — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `hp-damage` · `item-pickup` · `shop-catalog` · `round-currency` · `sequential-levels` (поверхи) · `player-death` · `reach-exit` (сходи) · `temporary-modes` · `keyboard-controls` · `cell-click` (?) · `minimap-radar` · `player-camera`.
- **Нема** → пропозиції карток:
  - `+event-tile-codes` «Клітина з числовим кодом події» · entities/interact · 📎 · слот {table}.
  - `+dual-armor` «Фізичний і магічний захист як шари перед HP» · entities/combat · 📎.
  - `+ability-points-explore` «Очки за відкриті клітини» · entities/state · 🌱.
  - `+movement-abilities` «Здібності, що міняють правила руху» · entities/move · 🥉.
  - `+revealed-by-step` «Мапа зʼявляється під кроками» · interface/render · 🌱.
  - `+reveal-battles-ability` «Показати приховані бої» · entities/state · 🌱.
  - `+rescue-fallen` «Тіло полеглого треба забрати» · entities/interact · 📎.
  - `+recruit-ally` — як у DotE.
  - `+atb-combat` «Бій зі шкалами активності» · entities/combat · 🥉 · слот {speed}.
  - `+event-log` «Журнал знайдених подій» · interface/hud · 🌱.
  - `+coordinate-warp` «Телепорт за координатами» · entities/interact · 📎.

## Пропозиції до словників
- `+trigger:revealed` (як у Rogue) · `+trigger:stepped(code)` — ступив на клітину з кодом (уточнення `enter`).
- `+cond:code(cell, n)` — код клітини; `+cond:has_ability(a)` — здібність встановлена; `+cond:armor(kind, op, n)` — залишок шару захисту.
- `+effect:reveal(cells)` (⏳) · `+effect:battle(group)` — перехід у бій з групою · `+effect:learn(ability)` · `+effect:warp(floor, x, y)`.
- `+role:event-tile` — клітина-подія з кодом (не `pickup`: не зникає, не `static`: має ефект); `+role:ally` — вжито.
- `+ui:tile-code` — число на клітині як основний рендер; `+ui:coordinates`; `+ui:armor-bars`; `+ui:atb-gauge`.
- `+window:event-log` · `+window:ability-window` · `+window:shop-window` (✅).
- `+feature:codex` (⏳) — тут журнал подій.
- `+axis:render=abstract` — гра свідомо без образного рендера (лише коди), нова вісь подачі.

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/Dungeon_Encounters) — сітка з гілками, білі/чорні числа, ATB, PD/MD блокують шкоду, Cattle Call, Ito, Uematsu, платформи.
- [Steam](https://store.steampowered.com/app/1451080/) — 99 поверхів, мапа порожня до відвідування, очки здібностей за дослідження, журнал подій, загублені шукачі, відкриття чорних чисел здібністю.
- YouTube: пошук «dungeon encounters gameplay».

## Непевне
- (?) Коди шістнадцяткові (00–FF) і конкретні значення кодів — з памʼяті; сторінок зі списком кодів не знайшов (fandom 402, офіційний сайт 404).
- (?) 99 чи 100 поверхів: Steam — 99, WP — 100.
- (?) Тіла полеглих на мапі, телепорт за координатами, прохід крізь порожнечу здібністю — з памʼяті.
- (?) Мапи рукотворні чи генеровані; фінальна умова перемоги.
- (?) Дата: WP у тексті 14.10.2021, в інфобоксі 14.11.2021; Steam — 14.10.2021.
