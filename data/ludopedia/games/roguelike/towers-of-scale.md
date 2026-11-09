---
title: Towers of Scale
slug: towers-of-scale
aka: ["[GMTK2024 Jam] Tower of Scale"]
family: roguelike
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: score
year: 2026
platforms: [PC (Windows, Linux)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3962750/Towers_of_Scale/", best: true, note: "Makiki, Early Access 17.04.2026: ключі, кайла, золото, предмети в руці, односторонні шляхи; рекорди → геми; undo без ліміту й сейвстейти"}
  - {kind: itch, url: "https://makiki99.itch.io/towers-of-scale", note: "демо й білди (LÖVE), теги magic-tower, optimization, high score"}
  - {kind: itch, url: "https://makiki99.itch.io/gmtk2024", note: "джем-версія GMTK 2024: сила росте на порядки, стартова сила 5, корона як предмет у руці"}
  - {kind: other, url: "https://itch.io/jam/gmtk-2024/rate/2912361", note: "коментарі джему: еліксири зберігати до корони, рахунок у мільярдах, undo від кінця до початку"}
  - {kind: other, url: "https://steamcommunity.com/app/3962750/discussions/0/760682265019691706/", note: "розробник: оцінка A = 4 млн у Training Tower без гемів; еліксири, брами ділення, ворог «−10k»"}
  - {kind: other, url: "https://steamcommunity.com/app/3962750/discussions/0/836124531564268287/", note: "оцінки A/S/★/★+N без гемів по стадіях"}
  - {kind: other, url: "https://steamcommunity.com/app/3962750/discussions/0/582805296104163559/", note: "розробник про трекер статистики, брами за геми, ключі, сейвстейти, режим мапи"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3962750&count=30&maxlength=0", note: "патчноути: Keysmasher, перо левітації, Hyper Pickaxe, сфери, брами, грейди, геми"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Towers+of+Scale+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [move-4dir, keyboard-controls, cell-click, key-and-door, item-pickup, inventory-items, inventory-limit, impassable-cells, round-currency, one-way-cell, teleport, push-object, stairs-levels, level-select, level-unlock, event-points, score-records, undo-redo, undo-unlimited, save-multi-slot, map-window, stats-window, achievements-window, +single-stat-power, +multiplier-pickup, +division-gate, +money-door, +meta-currency-gates, +grade-to-gems, +held-item-slot, +color-flip-orb]
proposes: ["+trigger:bump(a, b)", "+cond:can_damage(a, b)", "+effect:stat(a, name, ×k)", "+effect:flip_colors(kind)", "+ui:power-near-sprite", "+ui:next-gem-threshold", "+window:savestates", "+window:item-list", "+feature:savestates", "+feature:fast-travel-floors", "+feature:map-markers", "+card:division-gate"]
author: opus
date: 2026-11-09
---

# Towers of Scale — Magic Tower з одним числом: сила — це HP, ключ до дверей і рахунок водночас, а еліксири її множать

## Суть
Герой підіймається вежею з поверхів-лабіринтів до корони; на шляху вороги, двері з ключами, стіни під кайло, брами за золото й односторонні проходи. Замість звичних HP/ATK/DEF — **одна характеристика «сила» (Power)**: вона відкриває більшість перешкод і водночас є рахунком, з яким дійдеш до корони. Сила росте на порядки (з 5 до мільярдів), бо частина бонусів **множить** її, тож головне — порядок: що витратити, поки сила мала, а що зберегти до кінця. Рекорди стадій дають **геми** — мета-валюту на додаткові ресурси й бонусні зони, тож оптимальний маршрут змінюється з кожним новим рекордом.

## Поле і час
- Квадратна сітка, вежа з кількох поверхів; перехід поверхами — сходи, швидке переміщення між відвіданими поверхами клавішами `[` `]`.
- Покроково, рух лише від вводу; вороги стоять (жанр Magic Tower) (?).
- Повна інформація на поверсі (?); є режим мапи з усією вежею, списком предметів і маркерами.
- Сесія — стадія (вежа): глави 1–3, бонусні EX-стадії, навчальна Training Tower; кожна стадія закінчується короною.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | сила (Power), золото, ключі, кайла, один предмет у руці | рух 4 напрямки; бій — входом у клітину ворога (?) |
| Ворог | enemy | число сили (бувають «від'ємні», напр. −10k) | переможений зникає й лишає трохи золота |
| Двері + ключ | gate / pickup | колір | ключ відкриває двері свого кольору; є майстер-ключі |
| Стіна / укріплена стіна | static | — | кайло прокопує звичайну, герой переходить у прокопану клітину; укріплена — ні (?) |
| Кайло | pickup | кількість | одна стіна — одне кайло |
| Золото | resource | — | платня за грошові брами |
| Грошова брама | gate | ціна в золоті | відкривається оплатою |
| Брама ділення (division gate) | gate | — | відкривається за силу; дешевше, коли сила мала (?) |
| Брама за геми | gate | ціна в гемах | мета-брама до бонусних зон; деякі можна обійти |
| Еліксир | pickup | ×2 (джем) | множить силу; вигідно зберігати до корони; один — обовʼязковий на шляху |
| Предмет у руці: Keysmasher | pickup | — | бонус до сили, поки в руці; повʼязаний з ключами (?) |
| Предмет у руці: перо левітації | pickup | — | прохід по шипах і висувних плитках |
| Предмет у руці: Hyper Pickaxe | pickup | — | посилене кайло (?) |
| Сфери (телепорт, сила, зміна кольору) | pickup | одноразові | телепорт; штовхання речей; міняють кольори ключів і дверей |
| Шипи / висувні плитки | hazard | — | без пера не пройти (?) |
| Одностороння стіна / шлях | terrain | напрям | прохід лише в один бік |
| Сходи | static | — | на поверх вище / нижче |
| Корона | static | — | фінал стадії; сила в цей момент — рахунок |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell)` → ТО `move(hero, dir)`.
- КОЛИ `contact(hero, enemy)` → ЯКЩО `custom: «сила героя перевищує ворога»` (?) → ТО `custom: «сила змінюється на величину ворога»` (?), `disappear(enemy)`, `currency(+gold)`.
- КОЛИ `contact(hero, door[c])` → ЯКЩО `has(hero, key[c])` → ТО `take(hero, key[c])`, `set_cell(door, open)`; інакше `block`.
- КОЛИ `contact(hero, wall)` → ЯКЩО `has(hero, pickaxe)` → ТО `take(hero, pickaxe)`, `set_cell(wall, floor)`, `move(hero, dir)`.
- КОЛИ `contact(hero, money_gate)` → ЯКЩО `counter(gold, >=, cost)` → ТО `currency(−cost)`, `set_cell(gate, open)`.
- КОЛИ `contact(hero, division_gate)` → ТО `custom: «плата частиною поточної сили»` (?), `set_cell(gate, open)`.
- КОЛИ `contact(hero, gem_gate)` → ЯКЩО `counter(gems, >=, cost)` → ТО `custom: «брама відкрита назавжди за геми»`.
- КОЛИ `input(use, elixir)` → ТО `custom: «сила × k»` (у джемі ×2).
- КОЛИ `contact(hero, held_item)` → ЯКЩО `custom: «рука вільна»` → ТО `pickup`; інакше `block` (спершу витратити поточний предмет).
- КОЛИ `enter(hero, spikes)` → ЯКЩО `not has(hero, feather)` → ТО `block` (?).
- КОЛИ `input(use, orb)` → ТО `teleport(hero, …)` | `push(object)` | `custom: «поміняти кольори ключів і дверей»`.
- КОЛИ `input(dir)` → ЯКЩО `custom: «рух проти односторонньої стіни»` → ТО `block`.
- КОЛИ `contact(hero, crown)` → ТО `win`, `score(power)`, `custom: «оцінка B…S, ★, ★+N → геми»`.
- КОЛИ `input(undo)` → ТО `undo(1)` (без ліміту, хоч до початку стадії; кроки з пером по шипах в undo-чергу не пишуться).
- Перемога: корона. Поразка: глухий кут ресурсів (вирішується undo / сейвстейтом) (?). Рахунок: сила на короні → оцінка → геми (перераховуються при кращому результаті).

## Керування і ввід
- Клавіатура: стрілки — крок; клавіші предметів і undo; `[` `]` — швидкий перехід між поверхами.
- Миша: клік по клітині — пошук шляху (з налаштуванням урахування односторонніх стін); повна гра лише мишею або лише клавіатурою.
- Сейвстейти з назвами й часом; режим мапи з маркерами.

## Вікна, меню, HUD
- `game-screen`: поверх вежі + `stat-panel` (сила, золото, ключі, кайла, предмет у руці); опційно приблизна сила біля спрайта героя.
- `level-select` — стадії глав 1–3 і EX; для частини потрібна кількість корон (напр., 4 для 2-1).
- `map-window` — уся вежа, маркери з прозорістю, `item-list` (предмети, брами ділення), знімок мапи.
- `savestates` — список сейвстейтів, видалення, «<new save>».
- `stats-window` — трекер минулих дій: витрачене золото, майстер-ключі, використані витратні предмети.
- `end-screen` — підсумок стадії: рахунок, оцінка, скільки треба до наступного гема.
- `shop-window` (?) — витрата гемів на додаткові ресурси.
- `achievements-window` (23 досягнення Steam), `settings-window` (кольори, контраст, клавіші (?)), `help-window`/інтерактивний туторіал.

## Фічі поза полем
- `undo` без ліміту, `snapshots`/сейвстейти, `autosave` (?).
- `meta-progression`: геми за оцінки → додаткові ресурси, бонусні зони, нові предмети; повернення на старі вежі з новими маршрутами.
- `stars-rating`-подібні оцінки (C…S, ★, ★+N з м'якою стелею) та `leaderboard-local` як особистий рекорд.
- `colorblind-palette`, `high-contrast`, `mouse-and-keyboard`, `one-hand-mode`-подібне «лише миша».
- Перенесення прогресу з демо в повну гру; підтримка модів неофіційно (Discord).

## Варіації й родичі
- Джем-версія GMTK 2024 («Built to Scale»): одна вежа, стартова сила 5, корона займає слот руки, армурія й банк; повна гра (2026) — стадії, геми, сейвстейти, мапа.
- Родичі: [Magic Tower](magic-tower.md) (жанр), [Tactical Nexus](tactical-nexus.md) (довші вежі, HP/ATK/DEF), [DROD RPG](drod-rpg.md), [DungeonUp](dungeonup.md), [h5mota](h5mota.md).
- Осі варіацій: **статів** (HP/ATK/DEF / одна сила) · **ріст** (адитивні самоцвіти / мультиплікативні еліксири) · **ціна брами** (фіксована / частка сили) · **мета** (нема / геми за оцінку відкривають ресурси).

## Цікавинки для курсу
- Одна характеристика як ресурс і рахунок: модель «витрачай, поки мало; множ наприкінці» — 🌱.
- Брама, що бере частку сили (дешева при малій силі), проти еліксира-множника: оптимальний порядок — 📎.
- Слот «предмет у руці» (один) як обмеження інвентаря — 🌱.
- Оцінка за порогами + геми, перераховані при покращенні рекорду — 🌱.
- Сфера, що міняє кольори всіх ключів і дверей — 🌱.
- Розвʼязувач маршруту з мультиплікативними бонусами (пошук максимуму сили) — 👑.

## Мапа на каталог
- Є: `move-4dir`, `keyboard-controls`, `cell-click` ↔ рух і автошлях; `key-and-door`; `item-pickup`, `inventory-items`, `inventory-limit` ↔ предмет у руці; `impassable-cells`; `round-currency` ↔ золото; `one-way-cell`; `teleport`, `push-object` ↔ сфери; `stairs-levels`; `level-select` + `level-unlock` ↔ стадії за корони; `event-points` + `score-records` ↔ сила як рахунок; `undo-redo` + `undo-unlimited`; `save-multi-slot` ↔ сейвстейти; `map-window`, `stats-window`, `achievements-window`.
- **Нема** → пропозиції карток:
  - `+single-stat-power` «Одна характеристика замість HP/ATK/DEF» · entities/state · 🌱.
  - `+multiplier-pickup` «Бонус множить характеристику, а не додає» · entities/state · 🌱.
  - `+division-gate` «Брама за частку ресурсу» · entities/interact · 🌱.
  - `+money-door` (DROD RPG) — брама за золото.
  - `+meta-currency-gates` (Tactical Nexus) — брами за мета-валюту.
  - `+grade-to-gems` «Оцінка за порогами дає мета-валюту, перерахунок при рекорді» · game-logic/score · 🌱.
  - `+held-item-slot` «Один предмет у руці» · entities/state · 🌱.
  - `+color-flip-orb` «Перефарбувати всі ключі й двері» · entities/interact · 🌱.

## Пропозиції до словників
- `+trigger:bump(a, b)` — бій входом у клітину ворога.
- `+cond:can_damage(a, b)` — чи досить сили на ворога.
- `+effect:stat(a, name, ×k)` — множення характеристики (еліксир); `+effect:flip_colors(kind)` — перефарбування ключів і дверей.
- `+ui:power-near-sprite` — число сили біля героя; `+ui:next-gem-threshold` — скільки до наступного гема.
- `+window:savestates`, `+window:item-list` — список предметів поверху/вежі в режимі мапи.
- `+feature:savestates` — іменовані знімки стану; `+feature:fast-travel-floors`; `+feature:map-markers`.
- `+card:division-gate`.

## Джерела
- ⭐ [Steam: Towers of Scale](https://store.steampowered.com/app/3962750/Towers_of_Scale/) — опис ресурсів, корона, геми, undo і сейвстейти, теги, дати.
- [itch: Towers of Scale](https://makiki99.itch.io/towers-of-scale) — теги magic-tower / optimization, рушій LÖVE, туторіал.
- [itch: GMTK 2024 версія](https://makiki99.itch.io/gmtk2024) і [сторінка джему](https://itch.io/jam/gmtk-2024/rate/2912361) — стартова сила 5, «перерости ворогів», еліксири ×2, слот руки, undo без ліміту.
- Steam-обговорення: [рекорд Training Tower](https://steamcommunity.com/app/3962750/discussions/0/760682265019691706/), [оцінки без гемів](https://steamcommunity.com/app/3962750/discussions/0/836124531564268287/), [трекер статистики](https://steamcommunity.com/app/3962750/discussions/0/582805296104163559/).
- [Steam News API](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3962750&count=30&maxlength=0) — патчноути: предмети в руці, сфери, брами, грейди, геми, мапа, fast travel.
- [Огляди Steam](https://steamcommunity.com/app/3962750/reviews/?browsefilter=toprated&p=1) — «одна сила замість ATK/DEF/HP, вона ж рахунок»; порівняння з Tactical Nexus і Tower of the Sorcerer.

## Непевне
- (?) Точне правило бою не знайдено: «перерости ворога» (джем), «Power/HP» (відгук) і «ворог −10k» (розробник) — схоже, що ворог віднімає (або додає, якщо від'ємний) свою силу; не перевірено.
- (?) Як саме брама ділення бере силу (ділить на N чи бере частку) — відомо лише, що її вигідно відкривати при малій силі.
- (?) Ефекти Keysmasher (бонус сили в руці — так; зв'язок з ключами — з назви) і Hyper Pickaxe.
- (?) Чи шипи шкодять, чи лише блокують без пера; чи поверх видно цілком одразу.
- (?) Чи є магазин гемів окремим вікном; повний набір налаштувань.
