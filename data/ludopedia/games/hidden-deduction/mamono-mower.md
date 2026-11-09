---
title: Mamono Mower
slug: mamono-mower
aka: []
family: hidden-deduction
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: hidden
  random: setup
  goal: state
year: 2022
platforms: [web (HTML5)]
links:
  - {kind: itch, url: "https://hempuli.itch.io/mamono-mower", best: true, note: "грати в браузері; правила: косити перешкоди ≤ свого рівня, ривок — на рівень вище; коментарі про режими й життя"}
  - {kind: other, url: "https://hempuli.itch.io/mamono-mower/devlog", note: "девлог 24.11.2022: числа рівня небезпеки (1.0.3b), фікси"}
  - {kind: other, url: "https://www.mzrg.com/mines/mamono.shtml", note: "правила оригіналу Mamono Sweeper (Hojamaka): сума рівнів, HP, EXP, режими"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Mamono+Mower+Hempuli", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [move-4dir, keyboard-controls, hp-damage, player-death, destroy-all-enemies, restart-level, game-screen, +sum-of-levels-clue, +xp-level-up, +dash-power-boost, +avatar-reveal-walk]
proposes: ["+trigger:hold(action)", "+cond:level_cmp", "+effect:xp", "+effect:level_up", "+card:dash-power-boost"]
author: opus
date: 2026-11-09
---

# Mamono Mower — Mamono Sweeper у реальному часі: їдь косаркою, кось перешкоди свого рівня, ривком — на рівень вище

## Суть
Переробка Mamono Sweeper (сапер із «рівнями монстрів») від Hempuli: замість кліків — косарка, що їде полем у реальному часі. Перешкоди на газоні мають рівень; косити можна лише ті, що не вищі за твій, — це дає досвід, досвід підвищує рівень. Затиснутий ривок дозволяє скосити перешкоду на рівень вище. Мета — скосити весь газон; наїзд на сильнішу перешкоду забирає життя (?).

## Поле і час
- Квадратна сітка-газон з прихованими перешкодами (?) — гравці кажуть, що рух «по шляху» не дає перевірити далекі клітини за бажанням.
- Реальний час: косарка рухається, поки тримаєш стрілку (?); режими Classic і Strategy (останній — повільніший / «thinking mode» (?)).
- Числа рівня небезпеки на клітинах (1.0.3b) — імовірно, як у Mamono: сума рівнів сусідніх перешкод (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Косарка | player | рівень, досвід, життя (?) | їде 4 напрямками; косить перешкоди |
| Перешкода газону («mamono») | enemy | рівень | скошується, якщо рівень ≤ рівня косарки (або +1 під час ривка) |
| Нескошена трава | static | прихований вміст | відкривається проїздом (?) |
| Скошена клітина / число | mark | n | рівень небезпеки поруч (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, dir)` → ТО `move(mower, dir)`.
- КОЛИ `contact(mower, obstacle)` → ЯКЩО `custom: «рівень перешкоди ≤ рівня косарки»` → ТО `disappear_b`, `custom: «+досвід»`.
- КОЛИ `contact(mower, obstacle)` → ЯКЩО `state(mower, dash)` and `custom: «рівень перешкоди = рівень косарки + 1»` → ТО `disappear_b`, `custom: «+досвід»`.
- КОЛИ `contact(mower, obstacle)` → ЯКЩО `custom: «перешкода сильніша»` → ТО `lives(-1)` (?).
- КОЛИ `custom: «натиснуто й утримується Space»` → ТО `set_state(mower, dash)` — ривок (швидший рух (?)).
- КОЛИ `counter(exp, >=, need)` → ТО `custom: «рівень косарки +1»`.
- КОЛИ `custom: «скошено всі перешкоди»` → ТО `win` («MISSION ACCOMPLISHED»); без втрат — «perfect».
- КОЛИ `input(R)` → ТО `restart`.
- Перемога: скосити весь газон. · Поразка: втрата всіх життів (?). · Рахунок: час і «damageless»/«perfect» (гравці міряють час проходження).

## Керування і ввід
- Стрілки — рух; Space (утримувати) — ривок; R — рестарт; Enter — пропустити заставку (фікс 2).
- Гравці просять режим лише мишею — автор відсилає до оригіналу Mamono Sweeper.

## Вікна, меню, HUD
- `splash-screen`/інтро (виходить Enter), `mode-select` Classic / Strategy (?), `game-screen`: газон, рівень/досвід, життя (?).
- `end-screen`: «MISSION ACCOMPLISHED» / «perfect» (?).
- Пауза, коли вкладка без фокусу (фікс 2).

## Фічі поза полем
- Режими `mode-classic` і Strategy (?); `restart-level` клавішею R.
- Нічого більше не підтверджено.

## Варіації й родичі
- Оригінал — Mamono Sweeper (Hojamaka): клік-сапер, монстри рівнів 1–9, число = сума рівнів у 8 сусідах, шкода = рівень монстра × ⌈різниця/твій рівень⌉, HP 10 (Huge — 30), EXP 1 за рівень 1 і подвоюється; режими Easy 16×16/30, Normal 30×16/99, Huge 50×25/260, Extreme 30×16/125, Blind (рівень 0, 1 HP) і комбінації (mzrg). Окремого файла в корпусі ще нема — пропоную описати як `mamono-sweeper`.
- Нащадки ідеї «сапер + рівні монстрів»: [dragonsweeper](dragonsweeper.md), [demoncrawl](demoncrawl.md).
- Сапер з аватаром: [mined-out](mined-out.md), [lizzi-crossing](lizzi-crossing.md).
- Осі варіацій: **ввід** клік (Mamono) / аватар у реальному часі (Mower); **числа** кількість / сума рівнів; **поразка** HP / життя; **підсилення** нема / ривок +1 рівень.

## Цікавинки для курсу
- Порівняння рівнів «мій ≥ перешкоди» + досвід → рівень — 🌱.
- Ривок як тимчасовий стан, що змінює правило контакту (+1 рівень) — 🌱.
- Числа-суми рівнів сусідів (як у Mamono) — 📎.
- Перенесення клік-пазла в реальний час з аватаром: що лишається дедукцією, а що реакцією — 📎 (проєктне питання).

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` · `hp-damage` + `player-death` ↔ життя (?) · `destroy-all-enemies` ↔ скосити все · `restart-level` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+dash-power-boost` «Затиснутий ривок дає тимчасову перевагу (+1 рівень)» · entities/state · 🌱.
  - `+sum-of-levels-clue`, `+xp-level-up` — як у Dragonsweeper; `+avatar-reveal-walk` — як у Lizzi Crossing.

## Пропозиції до словників
- `+trigger:hold(action)` — клавіша утримується (не одноразовий `input`).
- `+cond:level_cmp(a, b, op, k)` — рівень A порівняно з рівнем B (+k).
- `+effect:xp` · `+effect:level_up` — як у Dragonsweeper (ще не у словнику).

## Джерела
- ⭐ [itch.io: Mamono Mower](https://hempuli.itch.io/mamono-mower) — «lawnmowing sim & minesweeper hybrid», правила рівнів і ривка, керування, «Based on Mamono Sweeper by Hojamaka»; коментарі: життя, Classic/Strategy, perfect.
- [Девлог](https://hempuli.itch.io/mamono-mower/devlog) — 24.11.2022: «Added numbers to indicate hazard level better», пауза без фокусу, Enter на інтро.
- [mzrg: Mamono Sweeper](https://www.mzrg.com/mines/mamono.shtml) — правила оригіналу.
- YouTube: пошук «Mamono Mower Hempuli».

## Непевне
- (?) Чи поле приховане й чи є числа-суми сусідів — «minesweeper hybrid» і девлог про числа на це натякають, прямо не написано.
- (?) Кількість життів, поріг досвіду, розмір газону — не бачив.
- (?) Чим Strategy («thinking mode») відрізняється від Classic — імовірно, покроковий або повільніший рух.
- (?) Рух: безперервний чи по клітинах.
