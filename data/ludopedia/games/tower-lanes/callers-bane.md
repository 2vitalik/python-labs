---
title: Caller's Bane (Scrolls)
slug: callers-bane
aka: [Scrolls, Mojang Scrolls]
family: tower-lanes
also: [tactics]
klass: figure
axes:
  field: hex
  time: turn
  opponent: online
  info: hidden
  random: setup
  goal: state
year: 2014
platforms: [PC, macOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Caller's_Bane", best: true, note: "5 ідолів по 10 HP, 3 з 5, Attack/Countdown/Health, рух на сусідню клітину, жертва карти, 4 ресурси + Wild, таймер 90 с, історія Scrolls → Caller's Bane"}
  - {kind: official, url: "https://mojang.github.io/CallersBaneSiteArchive/", note: "архів сайту, клієнт і сервер Caller's Bane 2.0.1 (сервер дозволяє правити карти й ruleset-и)"}
  - {kind: other, url: "https://www.gameindustry.com/reviews/game-review/the-scrolls-foretell-a-great-future", note: "рецензія: 5 рядів з ідолами в кінці, атака по прямій на нулі countdown, жертва за ресурс або 2 карти"}
  - {kind: other, url: "https://game-mechanics.blogspot.com/2013/07/scrolls-review.html", note: "розбір: колода ≥ 50, ≤ 3 копії, рука 5, +1 карта за хід, стіни й катапульти"}
  - {kind: other, url: "https://gamepressure.com/games/scrolls/z32782", note: "огляд: фракції, туторіал, 25 сценаріїв-випробувань"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Scrolls+Mojang+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [hp-damage, cursor-place, drag-drop-piece, pocket, line-of-sight-attack, move-timer, ai-opponent, online-multiplayer, rating-system, tutorial-window, mode-select, +lane-grid, +deck-draw, +deck-builder, +card-collection, +countdown-initiative, +idol-row-targets, +n-of-m-objectives, +sacrifice-for-resource, +multi-resource-max, +wild-resource, +immobile-structures, +move-or-act, +card-tier-crafting, +draft-mode, +trial-scenarios, +self-hosted-server]
proposes: ["+effect:draw_card", "+effect:sacrifice_card", "+effect:reset_countdown", "+trigger:countdown_zero", "+role:card", "+role:idol", "+ui:countdown-badge", "+ui:idol-hp", "+ui:resource-pools", "+ui:hourglass-button", "+window:deck-builder", "+feature:server-rulesets", "+card:idol-row-targets", "+card:sacrifice-for-resource"]
author: opus
date: 2026-11-09
---

# Caller's Bane (Scrolls) — гексова картярка Mojang: юніти з лічильником до атаки б'ють по своєму ряду, мета — знести 3 з 5 ідолів

## Суть
Карткова тактика від Mojang: кожен гравець має половину гексового поля з **5 рядами** і **ідолом у кінці кожного ряду**. Юніти мають три числа — Attack, **Countdown**, Health: щоходу countdown зменшується, на нулі юніт сам атакує вздовж свого ряду першу ворожу ціль, а якщо ряд порожній — ідола. Раз за хід можна **пожертвувати карту** — за +1 до максимуму ресурсу або за 2 нові карти. Перемога — зруйнувати **3 з 5** ворожих ідолів. Після закриття Scrolls (2018) гра стала безкоштовною як Caller's Bane з власним сервером.

## Поле і час
- Гексова сітка, поділена навпіл: 5 рядів на кожну сторону; у кінці кожного ряду — ідол (10 HP у стандартній партії). Розмір половини — див. «Непевне».
- Атака лінійна: юніт б'є по прямій уздовж свого ряду; рух — на сусідню вільну клітину, отже юніт міняє «смугу».
- Хід почерговий: добір 1 карти → жертва (необовʼязково) → розіграш карт і рухи → кінець ходу: countdown-и, атаки юнітів з нулем.
- Таймер ходу 90 с у мультиплеєрі, без ліміту в одиночній грі.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Істота (Creature) | piece (`+role:card`) | Attack, Countdown (база 1–6, зазвичай 2), Health, ціна 1–8 | ставиться на свою клітину; раз за хід рухається на сусідню вільну; на countdown 0 атакує по ряду |
| Споруда (Structure) | piece | Attack або «-», Countdown, Health | ставиться на поле, не рухається (лише чарами чи закляттям); стіни, катапульти |
| Закляття (Spell) | object | ціна | миттєвий ефект на юніти, ряди, поле |
| Зачарування (Enchantment) | object | ціна, носій | кріпиться до істоти чи споруди, зазвичай постійний ефект |
| Ідол | static (`+role:idol`) | 10 HP, по одному на ряд | ціль атаки, коли ряд перед ним порожній; 0 HP — зруйнований |
| Ресурси Energy · Order · Growth · Decay | resource | поточне / max для кожного | карта коштує ресурс своєї фракції; поточне поповнюється до max на початку ходу |
| Wild | resource | — | «суперресурс», замінює будь-який; жертвувати за нього можна з обмеженнями |
| Колода · рука | zone | колода ≥ 50, ≤ 3 копії, рука на старті 5 | +1 карта на початку ходу |
| Пісочний годинник | switch | — | кнопка кінця ходу |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «кожен бере 5 карт»`; ідоли `custom: «по 10 HP у кожному з 5 рядів»`.
- КОЛИ `turn_start(side)` → ТО `custom: «draw_card ×1»`, `custom: «поточні ресурси = max»`.
- КОЛИ `input(sacrifice, card)` → ЯКЩО `custom: «цього ходу ще не жертвував»` → ТО `choose(+1 max ресурсу обраного типу | draw_card ×2)`, `custom: «карта зникає з руки»`.
- КОЛИ `input(play, card, cell)` → ЯКЩО `counter(resource[фракція], >=, cost)` and `free(cell)` and `custom: «клітина на своїй половині»` → ТО `place(player, creature|structure)`, `counter(resource, -cost)`; інакше `block`.
- КОЛИ `input(play, enchantment, unit)` → ЯКЩО `counter(resource, >=, cost)` → ТО `set_state(unit, enchanted)`.
- КОЛИ `input(play, spell, target)` → ЯКЩО `counter(resource, >=, cost)` → ТО `custom: «ефект закляття (шкода, рух, зміна countdown…)»`.
- КОЛИ `input(move, creature, cell)` → ЯКЩО `in_range(creature, cell, 1)` and `free(cell)` and `custom: «цього ходу ще не рухалась»` and `not state(unit, structure)` → ТО `move(creature, cell)`.
- КОЛИ `turn_end(side)` → ТО `custom: «countdown −1 у кожного свого юніта»` (з винятками).
- КОЛИ `custom: «countdown юніта = 0»` → ЯКЩО `line_of_sight(unit, enemy_unit)` → ТО `damage(first_enemy_in_row, attack)`.
- КОЛИ `custom: «countdown юніта = 0»` → ЯКЩО `count(enemy_units_in_row, ==, 0)` → ТО `damage(idol_of_row, attack)`.
- КОЛИ `after(damage)` → ТО `custom: «reset_countdown: countdown = база юніта»`.
- КОЛИ `hp_zero(unit)` → ТО `disappear(unit)`.
- КОЛИ `hp_zero(idol)` → ТО `set_state(idol, destroyed)`, `counter(idols_destroyed, +1)`.
- КОЛИ `counter(idols_destroyed, >=, 3)` → ТО `win`; суперник `lose`.
- КОЛИ `input(hourglass)` або `custom: «90 с вичерпано»` → ТО `end_turn`.
- КОЛИ `custom: «3 однакові карти в колекції»` → ТО `merge(card, card, card_tier+1)` — колекційний крафт, не на полі.
- Перемога: 3 зруйновані ідоли суперника · Поразка: 3 свої · Рахунок: рейтинг у ranked.

## Керування і ввід
- Миша/тач: drag карти з руки на гекс (істота, споруда) або на ціль (закляття, зачарування).
- Drag власного юніта на сусідню клітину — рух (раз за хід).
- Жертва карти: drag на одну з іконок ресурсу (+1 max) або на «карти» (+2 карти).
- Кнопка-пісочний годинник унизу ліворуч — кінець ходу; атаки відбуваються самі.

## Вікна, меню, HUD
- `main-menu` (лобі): гра проти AI, мультиплеєр (ranked, швидка гра), Trials, Judgement, колода, магазин колекції (?).
- `+window:deck-builder` — колода ≥ 50 з колекції, ≤ 3 копії.
- `game-screen`: гексове поле обох половин, 5 ідолів з кожного боку з `+ui:idol-hp`, рука (`pocket`), `+ui:resource-pools` (поточне/max Energy, Order, Growth, Decay), `+ui:countdown-badge` на кожному юніті, `+ui:hourglass-button`, таймер ходу.
- `tutorial-window` — навчальні бої; `mode-select` — Trials (сценарії: розвʼязати ситуацію на дошці), Judgement (драфт).
- `end-screen` — переможець, нагороди.
- Переходи: лобі → вибір колоди → game-screen → end-screen → лобі.

## Фічі поза полем
- `online-multiplayer` + рейтингові ігри; `ai-opponent-levels` (?) для одиночної гри.
- `mode-puzzle`: «Trials» — 25 сценаріїв-випробувань (gamepressure).
- Judgement Mode: драфт карт із пулу, кілька ігор, карти лишаються за результатом (`+draft-mode`).
- Крафт тирів: 3 однакові карти → карта вищого тиру з ефектами; тир 2+ зберігає статистику матчів, тир 3 — бонус золота при доборі.
- Caller's Bane 2.0: безкоштовний клієнт + `+feature:server-rulesets` — власний Java-сервер з правкою карт і правил.

## Варіації й родичі
- **Scrolls → Caller's Bane**: та сама гра; після вимкнення офіційних серверів (2018) — безкоштовна з серверами спільноти.
- Родичі в корпусі: [inscryption](inscryption.md) (атака навпроти по колонці), [plants-vs-zombies](plants-vs-zombies.md) (5 рядів, ворог іде по ряду), [plants-vs-zombies-heroes](plants-vs-zombies-heroes.md), [wildfrost](wildfrost.md) (той самий лічильник до атаки), [mythgard](mythgard.md) (смуги + рух на сусідню), [castle-panic](castle-panic.md) (обʼєкти в кінці смуг).
- **Осі варіацій**: таймінг атаки — гравець наказує / автоатака за лічильником · ціль — навпроти / перша в ряду / за стрілкою · бар'єр — герой гравця / вежа в смузі / ідол у кожному ряду · ресурс — щохідний ріст / жертва карти за вибір «ресурс або карти».

## Цікавинки для курсу
- Countdown-автоатака: юніт «тікає» сам, гравець лише розставляє й рухає — 📎.
- Атака по ряду в першу ціль, інакше ідол цього ряду — 🌱.
- «3 з 5 ідолів» — перемога за кількістю зруйнованих цілей, а не сумою HP — 🌱.
- Жертва карти: вибір між +1 max ресурсу і +2 карти, чотири окремі пули — 📎.
- Гексова половина поля: рух на сусідню клітину змінює ряд атаки — 🥉 (гекс-сусідство).
- Сервер із ruleset-ами як дані — 🥇 (правила гри як конфіг).

## Мапа на каталог
- Є: `hp-damage` ↔ Health і ідоли · `cursor-place` / `drag-drop-piece` ↔ карта на гекс · `pocket` ↔ рука · `line-of-sight-attack` ↔ удар у першу ціль ряду · `move-timer` (90 с) · `ai-opponent` · `online-multiplayer`, `rating-system` · `tutorial-window`, `mode-select`.
- **Нема** → пропозиції карток:
  - `+lane-grid`, `+deck-draw`, `+deck-builder`, `+card-collection`, `+countdown-initiative`, `+draft-mode` — уже в корпусі.
  - `+idol-row-targets` «По цілі в кінці кожного ряду; порожній ряд → удар по цілі» · game-logic/lose · 🌱.
  - `+n-of-m-objectives` «Перемога — зруйнувати N з M цілей» · game-logic/win · 🌱.
  - `+sacrifice-for-resource` «Раз за хід жертва карти: +1 max ресурсу або +2 карти» · game-logic/economy · 📎.
  - `+multi-resource-max` «Окремі пули ресурсів з max, що поповнюються щохід» · game-logic/economy · 📎; `+wild-resource` «Ресурс-джокер» · 🌱.
  - `+immobile-structures` «Споруди без руху поруч із рухомими юнітами» · entities/move · 🌱; `+move-or-act` «Рух раз за хід на 1 клітину» · 🌱.
  - `+card-tier-crafting` «3 однакові → тир вище» · 🌱; `+trial-scenarios` «Задані ситуації на дошці» · levels/bank · 📎; `+self-hosted-server` «Свій сервер з правилами-даними» · 🥇.

## Пропозиції до словників
- `+effect:draw_card` — взяти карту (повтор; `draw` зайнятий нічиєю).
- `+effect:sacrifice_card` — пожертвувати карту з руки за вибір бонусу.
- `+effect:reset_countdown` — повернути лічильник до бази після дії.
- `+trigger:countdown_zero` — лічильник юніта дійшов до 0 (Wildfrost, Scrolls).
- `+role:card` — повтор; `+role:idol` — нерухома ціль-«життя» гравця в кінці ряду.
- `+ui:countdown-badge`, `+ui:idol-hp`, `+ui:resource-pools`, `+ui:hourglass-button`.
- `+window:deck-builder` — повтор.
- `+feature:server-rulesets` — власний сервер з редагованими картами й правилами.
- `+card:idol-row-targets`, `+card:sacrifice-for-resource`.

## Джерела
- ⭐ [Wikipedia: Caller's Bane](https://en.wikipedia.org/wiki/Caller%27s_Bane) — ідоли 10 HP, 3 з 5, типи карт, Attack/Countdown/Health (база 1–6, зазвичай 2), атака в кінці ходу, рух на сусідню порожню клітину, жертва за 2 карти або ресурс, Energy/Order/Growth/Decay + Wild, ціни 1–8, таймер 90 с, пісочний годинник, крафт тирів, Judgement Mode, історія релізів.
- [GameIndustry: рецензія](https://www.gameindustry.com/reviews/game-review/the-scrolls-foretell-a-great-future) — 5 рядів з ідолами в кінці, атака по прямій на нулі countdown, жертва за ресурс або 2 карти.
- [Technically, Scrolls (blog)](https://game-mechanics.blogspot.com/2013/07/scrolls-review.html) — колода ≥ 50, ≤ 3 копії, стартова рука 5, добір 1 за хід, стіни й катапульти.
- [Siliconera](https://www.siliconera.com/minecraft-studios-tactical-card-battler-scrolls-now/) — поле навпіл, 4 типи карт, жертва раз за хід (ранні дані про ідолів — див. «Непевне»).
- [gamepressure: Scrolls](https://gamepressure.com/games/scrolls/z32782) — 5 статуй, 3 з 5, туторіал, AI, ranked, 25 сценаріїв.
- [Архів сайту Caller's Bane](https://mojang.github.io/CallersBaneSiteArchive/) — клієнт і сервер 2.0.1.
- YouTube: пошук «Scrolls Mojang gameplay».

## Непевне
- (?) Розмір половини поля: у пошукових виписках — «6 стовпців × 5 рядів» і «30 гексів, навпіл» → 3 гекси в ряду на бік; першоджерела не відкрились.
- (?) Siliconera (ранній доступ) пише про 6 ідолів по 10 HP; Wikipedia і решта — 5.
- (?) GameIndustry: удар «може пройти» крізь блокера й поцілити ідола — ймовірно, здібність окремих карт (Relentless?), не базове правило.
- (?) Чи може юніт атакувати й рухатися в один хід; винятки з «countdown −1» (заморожування, прискорення) — лише загально.
- (?) Обмеження Wild («limits on when you can sacrifice for it») — подробиць нема.
- (?) Розташування ресурсів-цілей жертви в інтерфейсі; магазин колекції в Caller's Bane.
