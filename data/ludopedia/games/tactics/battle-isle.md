---
title: Battle Isle
slug: battle-isle
aka: [BI, "Battle Isle (1991)", "Battle Isle Data Disk", "History Line 1914–1918"]
family: tactics
also: []
klass: figure
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: hidden
  random: runtime
  goal: state
year: 1991
platforms: [Amiga, DOS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Battle_Isle", best: true, note: "серія: розділений екран, фази руху й атаки, один рухає — інший атакує; паливо/набої, погода, туман, досвід; що змінили BI2/BI3"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Battle_Isle_(video_game)", note: "перша гра: дві фази, перемога — знищити всіх або взяти штаб, 32 сценарії, режим на двох"}
  - {kind: other, url: "https://www.atarimagazines.com/compute/issue144/A24_Battle_Isle.php", note: "огляд COMPUTE! 1992: 22 типи юнітів, ландшафт, 32 острови (16+16), фабрики й депо, енергія із сировини, піхота в штаб, паролі, сейви"}
  - {kind: other, url: "https://dazeland.com/en/Amiga/Battle_Isle.html", note: "огляд Amiga: двоє одночасно, «рухаєшся, якщо пережив залп», кристали енергії, перехоплення транспорту, анімація бою, код CONRA"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Battle+Isle+1991+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [hp-damage, melee-vs-ranged, piece-move-patterns, legal-move-highlight, destroy-all-enemies, ai-opponent, simultaneous-versus, level-password, sequential-levels, save-game, fog-of-war, unit-xp-skills, round-currency, collect-quota, cursor-place, +hex-grid-render, +split-screen-versus, +phase-cycle, +offset-phases, +unit-production, +capture-property, +capture-hq-win, +repair-depot, +energy-crystals, +strength-points, +terrain-move-cost, +terrain-defense, +fuel-ammo, +mount-transport, +air-ground-layers, +combat-animation]
proposes: ["+cond:phase", "+effect:capture", "+effect:produce", "+effect:repair", "+role:factory", "+role:depot", "+role:hq", "+ui:split-view", "+ui:phase-indicator", "+window:unit-stats", "+window:combat-cutscene", "+axis:turn-structure=offset-phases", "+axis:opponent=same-screen-simultaneous"]
author: opus
date: 2026-11-09
---

# Battle Isle — гекс-варгейм на двох за одним екраном: поки один рухає війська, другий стріляє, а потім навпаки

## Суть
Двоє полководців на одному компʼютері, екран **розділено навпіл** — у кожного своя половина мапи острова й свій курсор. Хід поділено на **фази Руху і Дії**, і вони **зсунуті**: поки гравець A рухає юніти, гравець B атакує; потім ролі міняються. Тож свої юніти рушать, лише якщо пережили ворожий залп, а планувати треба з урахуванням чужої фази. Мета — знищити всі ворожі сили або **ввести піхоту у ворожий штаб**; фабрики будують і ремонтують юніти за енергію, яку дає сировина з мапи.

## Поле і час
- Мапа — гекс-сітка острова, розмір від 4 до 35 екранів залежно від сценарію; ландшафт: дороги, ліс, гори, затоки різної глибини (мілке/глибоке море).
- Кожен гравець бачить свою половину екрана й прокручує її сам; у грі проти AI — так само (?).
- Цикл: `Рух A ‖ Дія B` → `Рух B ‖ Дія A` → … — дві фази на «хід», обидві сторони діють одночасно в різних фазах.
- Ліміту ходів нема; опційний гандикап обмежує кількість дій за хід.
- Туман: ворожі юніти поза оглядом своїх не показані (?); розвідка важлива в серії.
- Бій — кидок долі (третина — удача): втрати знімають юніт за юнітом у загоні.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Піхота | piece | сила (кількість у загоні), броня, досвід | бере ворожі споруди; вхід у ворожий штаб — перемога |
| Легка машина (FAV), танк, ракетна установка, артилерія | piece | рух за ландшафтом, атака/захист, дальність | наземний бій; артилерія — на відстань |
| Інженери | piece | — | будівельні роботи (?) |
| Наземний транспорт | object | місткість | везе піхоту; можна перехопити |
| Винищувач, бомбардувальник, гелікоптер, повітряний транспорт | piece | — | повітряний шар; ігнорує ландшафт |
| Тральщик, підводний човен, ракетний катер (hydrofoil), есмінець | piece | — | лише вода відповідної глибини |
| Штаб (HQ) | zone | власник | ворожа піхота всередині → перемога |
| Фабрика | static | власник, енергія, запас | будує, ремонтує, зберігає юніти |
| Депо | static | власник, енергія | ремонтує і поповнює |
| Сировина / енергокристали | resource | — | доставити до фабрики/депо → енергія |
| Дорога / ліс / гори / мілина / глибока вода | terrain | ціна руху, захист | змінюють рух і шанси в бою |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(move, A)` → ТО `custom: «одночасно: A у фазі Руху, B у фазі Дії»`; КОЛИ обидві фази закінчено → ТО `custom: «ролі міняються»`.
- КОЛИ `input(move, u, hex)` → ЯКЩО `turn_of(move_phase)` and `path_exists(u, hex)` за ціною ландшафту → ТО `move(u, hex)`.
- КОЛИ `input(move, u, hex)` → ЯКЩО `custom: «u знищено в чужій фазі Дії до виконання»` → ТО `block`.
- КОЛИ `input(attack, u, t)` → ЯКЩО `turn_of(action_phase)` and (`adjacent(u, t)` або `in_range(u, t, range)`) → ТО `custom: «бій: шанс за силою, бронею, ландшафтом і досвідом; втрати — по одному юніту загону»` з анімацією.
- КОЛИ `custom: «загін бʼється і виживає»` → ТО `counter(xp, +1)` — досвідченіший бʼє краще.
- КОЛИ `enter(infantry, enemy_building)` у фазі Дії → ТО `set_side(building, side)` (фабрика, депо).
- КОЛИ `enter(infantry, enemy_hq)` → ТО `win`.
- КОЛИ `custom: «сировину доставлено до фабрики/депо»` → ТО `counter(energy, +n)`.
- КОЛИ `input(build, factory, type)` → ЯКЩО `counter(energy, ≥, price)` → ТО `spawn_at(unit, factory)`, `counter(energy, −price)`.
- КОЛИ `input(enter, u, depot)` → ЯКЩО `counter(energy, ≥, cost)` → ТО `heal(u, n)` і поповнення.
- КОЛИ `input(load, infantry, transport)` → ЯКЩО `adjacent(infantry, transport)` → ТО `custom: «сісти в транспорт»`; КОЛИ транспорт знищено → ТО гинуть і пасажири (?).
- КОЛИ `custom: «ворожий транспорт зайняли / перехопили»` → ТО `set_side(transport, side)` (?).
- КОЛИ `enter(ship, cell)` → ЯКЩО `not cell(cell, water)` (з потрібною глибиною) → ТО `block`.
- КОЛИ `all_gone(enemy_units)` → ТО `win`.
- КОЛИ `win` на одиночному сценарії → ТО `message(password)` — пароль наступної, складнішої мапи.
- Перемога: штаб або повне знищення · Поразка: те саме для суперника · Рахунок: —.

## Керування і ввід
- Джойстик/миша, у кожного гравця свій курсор на своїй половині екрана (два джойстики або джойстик + клавіатура (?)).
- Обрати юніт → утримуючи кнопку, відхилити в напрямок → меню дій: рух/постріл, показати параметри, кінець ходу.
- Досяжні гекси підсвічено (?); бій показується короткою анімацією «юніт проти юніта».

## Вікна, меню, HUD
- `main-menu`: один гравець / двоє, вибір мапи, `level-password` (код мапи), завантаження збереження.
- Захист від копіювання: код (CONRA) для гри проти компʼютера — `confirm-dialog` з кодом.
- `game-screen`: `+ui:split-view` — дві половини мапи, `cursor` кожного гравця, `+ui:phase-indicator` (чия фаза Рух/Дія), підсвітка досяжних гексів.
- `+window:unit-stats` — тип, сила, броня, досвід, рух.
- `custom-window` фабрики — що збудувати, запас енергії.
- `+window:combat-cutscene` — анімований поєдинок двох юнітів з результатом.
- `end-screen` — перемога/поразка; пароль наступної мапи.
- `save-slots` — збереження великих битв.

## Фічі поза полем
- 32 мапи-острови: 16 для гри на одного (послідовна кампанія через паролі), 16 для двох.
- Data Disk I (1992) і II (1993) — нові мапи/кампанії; History Line 1914–1918 (1992) — той самий двигун у Першу світову.
- `custom-rules`: гандикап — обмеження дій за хід для сильнішого гравця.

## Варіації й родичі
- Battle Isle 2 (Battle Isle 2200, 1993/94): кожному весь екран, фази Руху і Атаки злито, 3D-сцени бою; BI3 (1995) — те саме з більшою кількістю юнітів; The Andosia War (2000) — 3D і змішаний час.
- Відкриті клони: Advanced Strategic Command (1998), Crimson Fields (2001).
- Родичі в корпусі: [Advance Wars](advance-wars.md) (фабрики, штаб, піхота бере будівлі), [Panzer General](panzer-general.md) (гекси, рід військ), [Nectaris](nectaris.md) (гекс-острів на двох), [Wargroove](wargroove.md).
- **Осі варіацій**: структура ходу — по черзі (AW, PG) / **зсунуті фази Рух‖Дія** (BI) / одночасне планування (Frozen Synapse) · екран — спільний / розділений навпіл · економіка — дохід з міст (AW) / енергія з доставленої сировини (BI).

## Цікавинки для курсу
- Зсунуті фази: поки один рухає, інший стріляє — 🥉 (два гравці в одному тіку з різними легальними діями).
- Розділений екран з двома курсорами і двома вʼюпортами — 📎.
- Рух відбувається, лише якщо юніт пережив чужу фазу атаки — 📎.
- Енергія фабрик із сировини, яку треба довезти — 📎.
- Перемога «піхота в штаб» поруч із «знищ усіх» — 🌱.
- Паролі мап кампанії — 🌱.

## Мапа на каталог
- Є: `hp-damage` ↔ сила загону · `melee-vs-ranged` ↔ артилерія · `piece-move-patterns` ↔ суша/море/повітря · `legal-move-highlight` · `destroy-all-enemies` · `ai-opponent` · `simultaneous-versus` ↔ обидва діють одночасно · `level-password` · `sequential-levels` · `save-game` · `fog-of-war` (?) · `unit-xp-skills` ↔ досвід · `round-currency` ↔ енергія · `collect-quota` ↔ сировина · `cursor-place`.
- **Нема** → пропозиції карток:
  - `+hex-grid-render`, `+split-screen-versus`, `+phase-cycle`, `+unit-production`, `+capture-property`, `+strength-points`, `+terrain-move-cost`, `+terrain-defense`, `+fuel-ammo`, `+mount-transport`, `+air-ground-layers` — уже в корпусі.
  - `+offset-phases` «Зсунуті фази: Рух одного ‖ Дія іншого» · game-logic/opponent · 🥉.
  - `+capture-hq-win` «Піхота у ворожому штабі — перемога» · game-logic/win · 🌱.
  - `+repair-depot` «Депо ремонтує за енергію» · entities/state · 🌱.
  - `+energy-crystals` «Сировина на мапі живить фабрики» · game-logic/economy · 📎.
  - `+combat-animation` «Окрема сцена поєдинку» · interface/render · 📎.

## Пропозиції до словників
- `+cond:phase` — поточна фаза гравця (рух чи дія).
- `+effect:capture` — захопити споруду; `+effect:produce` — збудувати юніт; `+effect:repair` — відремонтувати.
- `+role:factory`, `+role:depot`, `+role:hq` — споруди зі власником.
- `+ui:split-view` — дві половини екрана з окремими курсорами; `+ui:phase-indicator`.
- `+window:unit-stats`, `+window:combat-cutscene`.
- `+axis:turn-structure=offset-phases`; `+axis:opponent=same-screen-simultaneous`.

## Джерела
- ⭐ [Wikipedia: Battle Isle (серія)](https://en.wikipedia.org/wiki/Battle_Isle) — розділений екран, фази руху й атаки «поки один рухає, інший діє», типи юнітів серії, паливо/набої, погода, туман, досвід, що змінили BI2/BI3, клони.
- [Wikipedia: Battle Isle (1991)](https://en.wikipedia.org/wiki/Battle_Isle_(video_game)) — дві фази, перемога (знищення або штаб), 32 сценарії.
- [COMPUTE! 144 (1992)](https://www.atarimagazines.com/compute/issue144/A24_Battle_Isle.php) — 22 типи юнітів, ландшафт, 32 острови 16+16, 4–35 екранів, бій «юніт за юнітом», фабрики й депо, енергія із сировини, піхота в штаб, гандикап, паролі, сейви.
- [Dazeland: Battle Isle (Amiga)](https://dazeland.com/en/Amiga/Battle_Isle.html) — двоє одночасно, «рухаєшся, якщо пережив залп», кристали, перехоплення транспорту, анімація бою, керування джойстиком, код CONRA.
- YouTube: пошук «Battle Isle 1991 gameplay».

## Непевне
- (?) Туман війни в першій грі — Wikipedia каже про серію загалом.
- (?) Як грає AI: окремий екран чи та сама половинна схема; чи AI теж діє в зсунутих фазах.
- (?) Перехоплення транспорту — механізм (захоплення чи знищення) не описано.
- (?) «22 combat units» — типи юнітів чи кількість юнітів у армії.
- (?) Чи гинуть пасажири разом із транспортом; керування двома гравцями (два джойстики?).
