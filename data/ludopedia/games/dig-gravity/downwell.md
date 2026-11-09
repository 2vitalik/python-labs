---
title: Downwell
slug: downwell
aka: []
family: dig-gravity
also: [grid-platformer, roguelike]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: partial
  random: both
  goal: state
year: 2015
platforms: [iOS, PC, Android, PS4, Vita, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Downwell_(video_game)", best: true, note: "чоботи-гармати, перезаряд при приземленні, топтання, червоні вороги, самоцвіти, timevoid, апгрейд 1 з 3, стилі, палітри"}
  - {kind: steam, url: "https://store.steampowered.com/app/360740/Downwell/", note: "Steam: постріл сповільнює падіння, процедурні рівні, апгрейди стакаються"}
  - {kind: other, url: "http://www.148apps.com/news/downwell-guide-tips-and-tricks-for-gunboot-initiates/", note: "гайд: комбо 8/15/25, топтання перезаряджає, білий бар HP, wall jump, Member's Card"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Downwell+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [gravity-fall, move-by-input, projectile-shot, shoot-cooldown, destructible-blocks, hp-damage, touch-death, combo-multiplier, round-currency, shop-window, shop-catalog, in-round-upgrades, run-relics, dungeon-generation, sequential-levels, permadeath, theme-select, player-camera, +stomp-kill, +ammo-recharge-on-landing, +shot-slows-fall, +stomp-immune-enemy, +combo-rewards, +gem-high, +time-void-room, +pick-1-of-3, +style-modifies-generation, +unlock-palettes-styles]
proposes: ["+trigger:landed", "+effect:reload", "+cond:airborne", "+ui:ammo-counter", "+ui:combo-meter", "+window:upgrade-window", "+window:skin-select", "+card:ammo-recharge-on-landing", "+card:combo-rewards", "+card:gem-high", "+card:time-void-room"]
author: opus
date: 2026-11-09
---

# Downwell — падай у колодязь і стріляй собі під ноги: чоботи-гармати перезаряджаються, щойно торкнешся землі

## Суть
Велтаро стрибає в нескінченно глибокий колодязь і падає вниз крізь процедурні рівні. Чоботи-гармати стріляють униз лише в повітрі; кожен постріл трохи сповільнює падіння, а набої поповнюються, коли торкаєшся будь-якої поверхні — землі, блока чи голови ворога. Звідси ядро: **бити ворогів у польоті, не приземлюючись**, ланцюжком комбо. Для теки `dig-gravity` — ось її клітинний шар: колодязь складений з тайлів, частину з яких руйнують постріли, а рух — постійне падіння; решта (стрільба, комбо) — платформер-роглайк.

## Поле і час
- Вертикальна шахта фіксованої ширини, що прокручується вниз за гравцем; тайли стін, платформ і руйнованих блоків (`field: square` — для тайлового шару; рух аватара — плавний).
- 4 світи по 3 рівні, кожен зі своїми ворогами; рівні процедурні; бічні «timevoid»-кімнати зупиняють час зовні.
- Real-time; палітра з 4 кольорів (чорний фон, білі контури, червоні — самоцвіти, вороги й ключові предмети, синій — вода).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Велтаро | player | HP, набої (charge), самоцвіти | ліво/право, стрибок із землі; у повітрі стрибок = постріл униз |
| Набій чобота | projectile | — | летить униз, бʼє ворогів і руйнує блоки; постріл сповільнює падіння |
| Стіна / платформа | static | — | опора; приземлення перезаряджає й обриває комбо |
| Руйнований блок | terrain | — | розбивається пострілом; кольорові блоки дають самоцвіти |
| Самоцвіт | pickup | — | валюта забігу; 100 поспіль → Gem High |
| Звичайний ворог | enemy | — | червоний відблиск і білий контур: можна і стоптати, і застрелити |
| Червоний ворог | enemy | — | повністю червоний: топтати не можна, лише стріляти |
| Timevoid | gate | — | вхід у кімнату, де час зовні стоїть: печера (самоцвіти/зброя) або крамниця |
| Альтернативна зброя (модуль чобіт) | pickup | — | міняє швидкість, затримку, витрату й місткість набоїв, патерн пострілу; підбір дає HP або +макс. набоїв |
| Крамниця (Jizō) | static | 3 товари | обмін самоцвітів на предмети (HP, апгрейди) |
| Бар здоровʼя (білий) | pickup | — | HP-підбирання при повному HP заповнюють бар; повний → +1 макс. HP |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(jump)` → ЯКЩО `supported(player)` → ТО `custom: «стрибок»`; ЯКЩО `not supported(player)` and `counter(ammo, >, 0)` → ТО `spawn(bullet, below)`, `counter(ammo, −1)`, `custom: «падіння сповільнюється»`.
- КОЛИ `tick` → ЯКЩО `not supported(player)` → ТО `fall(player)`.
- КОЛИ `custom: «гравець приземлився на будь-яку поверхню»` → ТО `custom: «набої до максимуму»`, `reset_combo`.
- КОЛИ `contact(player, enemy)` → ЯКЩО `moving(player, down)` and `not state(enemy, red)` → ТО `disappear_b`, `combo(+1)`, `custom: «відскок і перезаряд»`; інакше `damage(player, 1)`.
- КОЛИ `contact(bullet, enemy)` → ТО `damage(enemy, n)`; КОЛИ `hp_zero(enemy)` → ТО `combo(+1)`, `spawn(gems)`.
- КОЛИ `contact(bullet, block)` → ТО `set_cell(empty)`; ЯКЩО `cell(target, colored_block)` → ТО `spawn(gems)`.
- КОЛИ `counter(combo, >=, 8)` → ЯКЩО `custom: «комбо обірвано»` → ТО `currency(+100)`; ≥ 15 — ще й `+1` набій до максимуму; ≥ 25 — ще й `+1` HP.
- КОЛИ `counter(gems_in_row, >=, 100)` → ТО `set_state(player, gem_high)` — потужніші й далекобійніші постріли на час.
- КОЛИ `enter(player, timevoid)` → ТО `freeze(outside)`, `custom: «кімната: печера або крамниця»`; комбо не скидається.
- КОЛИ `input(buy, item)` → ЯКЩО `has(player, gems, price)` → ТО `currency(−price)`, `give(player, item)`.
- КОЛИ `picked(player, gun_module)` → ТО `custom: «нова зброя чобіт»` і `heal(1)` або `+макс. набоїв`.
- КОЛИ `level_end` → ТО `choose(1 of 3 upgrades)` — діє до кінця забігу.
- КОЛИ `hp_zero(player)` → ТО `game_over` (забіг з початку).
- КОЛИ `reach(player, bottom)` → ТО `next_level`; після останнього світу — `win`.
- Перемога: дно колодязя. Поразка: HP 0. Рахунок: самоцвіти, найкраще комбо.

## Керування і ввід
- Три дії: ліво, право, стрибок/постріл (одна кнопка: на землі — стрибок, у повітрі утримання — стрільба).
- Wall jump: упертись у стіну й натиснути стрибок (потрібен повний запас набоїв, набій не витрачає).
- Мобільна версія — тач-зони (портретний екран); ПК/консолі — клавіатура/геймпад.

## Вікна, меню, HUD
- `main-menu` → вибір стилю й палітри (`skin-select`) → забіг.
- `game-screen`: вертикальна шахта; HUD — `hp-bar` (сегменти + білий бар), `ammo-counter` (вертикальна шкала набоїв), `coins` (самоцвіти), `combo-meter`, глибина (?).
- `shop-window` у timevoid (3 товари); `upgrade-window` між рівнями (1 з 3).
- `end-screen` забігу (самоцвіти, вороги, найкраще комбо) (?); `pause-menu`, `settings-window`.

## Фічі поза полем
- `unlockables`: палітри й стилі руху відкриваються прогресом; стиль міняє рух на землі і генерацію (частоту й тип timevoid).
- Режим Levitate — повільніше падіння (зручно тренувати комбо) (?).
- `achievements` (Wow Combo 30, Sugoi Combo 100 — з результатів пошуку).

## Варіації й родичі
- [spelunky.md](spelunky.md) — тайловий рельєф, процедурні кімнати, роглайк; [noita.md](noita.md) — руйнування вниз.
- [mr-driller.md](mr-driller.md), [dig-dug.md](dig-dug.md) — рух углиб як мета.
- **Осі варіацій**: ресурс атаки — «нескінченний / набої з перезарядом при опорі / кулдаун»; комбо — «обривається приземленням / таймером»; спуск — «копаєш сам / падаєш і руйнуєш постріли».

## Цікавинки для курсу
- Перезаряд набоїв при приземленні + постріл сповільнює падіння: одна кнопка, два режими за станом `supported` — 📎.
- Комбо, що обриває лише дотик до опори, з порогами нагород 8/15/25 — 📎.
- Gem High: 100 самоцвітів поспіль вмикають стан — 🌱.
- Вороги «можна топтати / лише стріляти» як прапорець сутності — 🌱.
- Timevoid: кімната, де зовнішній час стоїть, а комбо зберігається — 📎.
- Апгрейд «1 з 3» між рівнями, що стакаються — 🥉.

## Мапа на каталог
- Є: `gravity-fall` · `move-by-input` · `projectile-shot` · `shoot-cooldown` ↔ витрата/перезаряд набоїв · `destructible-blocks` · `hp-damage` · `touch-death` · `combo-multiplier` ↔ лічильник комбо · `round-currency` ↔ самоцвіти · `shop-window` / `shop-catalog` · `in-round-upgrades` · `run-relics` ↔ стакання апгрейдів · `dungeon-generation` ↔ процедурні рівні · `sequential-levels` · `permadeath` ↔ забіг з нуля · `theme-select` ↔ палітри · `player-camera`.
- **Нема** → пропозиції карток:
  - `+ammo-recharge-on-landing` «Набої повні при дотику до опори» · entities/combat · 📎.
  - `+combo-rewards` «Пороги комбо дають нагороди» · game-logic/score · 📎 · слоти {8: 100 gems, 15: +ammo, 25: +HP}.
  - `+gem-high` «N збираних поспіль вмикають тимчасовий стан» · entities/state · 🌱.
  - `+time-void-room` «Кімната, де зовнішній час стоїть» · levels/progression · 📎.
  - Також: `+stomp-kill`, `+shot-slows-fall`, `+stomp-immune-enemy`, `+pick-1-of-3`, `+style-modifies-generation`.

## Пропозиції до словників
- `+trigger:landed` — повтор: аватар торкнувся опори (перезаряд, обрив комбо).
- `+effect:reload` — повтор: набої до максимуму.
- `+cond:airborne` — аватар у повітрі (вмикає стрільбу); можна `not supported`, слабка.
- `+ui:ammo-counter` — повтор; `+ui:combo-meter` — є в ui-elements як ⏳, тут повтор вживання.
- `+window:upgrade-window` / `+window:skin-select` — повтори.

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/Downwell_(video_game)) — Moppin / Devolver Digital, 2015; перезаряд при приземленні, топтання і червоні вороги, самоцвіти й timevoid, Jizō з 3 товарами, апгрейд 1 з 3, стилі змінюють генерацію, 4 світи × 3 рівні, палітри.
- [Steam](https://store.steampowered.com/app/360740/Downwell/) — постріл сповільнює падіння, процедурні рівні, апгрейди стакаються.
- [148Apps guide](http://www.148apps.com/news/downwell-guide-tips-and-tricks-for-gunboot-initiates/) — комбо 8/15/25 без дотику платформ, топтання перезаряджає, білий бар HP, wall jump, Levitate, Member's Card.

## Непевне
- (?) Комбо-нагорода нараховується при обриві комбо чи при досягненні порогу — джерела розходяться.
- (?) Gem High: 100 поспіль і більша шкода/дальність — з результатів пошуку (фан-вікі не відкрилась).
- (?) Чи блоки під ногами обривають комбо (дзеркало вікі: так — «solid ground or breakable blocks»).
- (?) Вигляд HUD (глибиномір, кінцевий екран) — з памʼяті.
- (?) Hard mode після проходження — не підтверджено.
