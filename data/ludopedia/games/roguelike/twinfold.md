---
title: Twinfold
slug: twinfold
aka: []
family: roguelike
also: [falling-match, thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: both
  goal: score
year: 2018
platforms: [Windows, macOS, iOS]
links:
  - {kind: other, url: "https://statelyplay.com/2018/12/07/twinfold-mashes-several-well-worn-mechanisms-into-a-unique-new-experience/", best: true, note: "огляд: свайп рухає все поле, злиття золота ×2, «зʼїв — наступні вдвічі дешевші», стіни бʼють, ями"}
  - {kind: steam, url: "https://store.steampowered.com/app/980880/Twinfold/", note: "Steam: 7 типів ворогів, 40+ навичок, процедурні мікро-пазли"}
  - {kind: other, url: "https://www.gamedeveloper.com/design/behind-the-mashed-up-roguelike-charm-of-i-twinfold-i-", note: "розробник: Threes! + Imbroglio, типи ворогів, мана з капом, лічильник небезпеки"}
  - {kind: other, url: "https://toucharcade.com/?p=245356", note: "огляд: XP-смуга, вибір 1 з 3 апгрейдів, кімнати й перебудова стін"}
  - {kind: other, url: "https://apps.apple.com/app/id1437168510", note: "App Store (iOS)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Twinfold+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [swipe-gestures, keyboard-controls, move-4dir, tile-merge, hp-damage, chase-player, spawn-random-cell, event-points, in-round-upgrades, run-relics, destroy-all-enemies, sequential-levels, environment-death, permadeath, +swipe-moves-all, +wall-crush-damage, +eat-merged-value, +merge-respawn-halving, +pit-knockoff, +level-up-pick-of-3, +wall-reshuffle-on-clear, +enemy-trait-immunity]
proposes: ["+effect:eat(b)", "+ui:danger-meter", "+ui:xp-bar", "+feature:quick-resume", "+card:swipe-moves-all", "+card:wall-crush-damage"]
author: opus
date: 2026-11-09
---

# Twinfold — Threes! у підземеллі: свайп рухає все, стіна — твоя зброя

## Суть
Kenny Sun (автор Yankai's Peak) звів **рух і злиття з Threes!** та **мету й перебудову стін з Imbroglio**. Свайп у бік зсуває на одну клітину **все** на полі — тебе, золоті фігурки й ворогів; нічого не рухається саме. Дві однакові золоті фігурки зливаються й дорожчають удвічі; зʼїси одну — отримаєш очки й досвід, але нові зʼявляться вдвічі дешевшими. Вороги зʼявляються з повітря, полюють на тебе і на золото, а гинуть, коли ти розбиваєш їх об стіни або скидаєш у ями.

## Поле і час
- Невелика квадратна кімната на один екран, випадкові стіни і ями; кімнати процедурні («мікро-пазли»).
- Хід = свайп у 4 напрямки; після свайпу деякі вороги ще й «підстрибують» (ходять самі).
- Очищена кімната перебудовує стіни — нова конфігурація, наступна кімната.
- Видно все; новачкам важко лише те, що здібності ворогів гра не пояснює.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой (fube) | player | HP сегментами, XP, мана (з капом) | зсувається разом з усім полем |
| Золота фігурка (baby / gold fube) | tile | значення | дві однакові при зіткненні → одна, значення ×2; зʼїсти — очки, XP, лікування |
| Ворог (bad fube) | enemy | HP сегментами | переслідує, нападає; їсть золото; удар об стіну — −1 сегмент |
| Сірий ворог | enemy | — | не рухається |
| Синій ворог | enemy | — | стіни на нього не діють |
| Фіолетовий ворог | enemy | — | не падає в ями |
| Червоний ворог | enemy | — | не отримує шкоди, коли його вдавлено в стіну |
| Зелений ворог | enemy | рідкісний | іде лише за золотом |
| Злий близнюк (evil twin) | enemy | рідкісний | сам рухає все поле |
| Стіна | static | — | упор: хто вдарився під час зсуву — втрачає HP |
| Яма | hazard | — | смертельна; скинутий туди ворог — гине |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(swipe dir)` → ТО `shift(all, dir)` на одну клітину: кожна сутність рухається, ЯКЩО `free(cell)`.
- КОЛИ `blocked(player)` (упор у стіну під час зсуву) → ТО `hp(player, −1)`.
- КОЛИ `blocked(enemy)` (вдавлено в стіну) → ЯКЩО `not state(enemy, wall_immune)` → ТО `hp(enemy, −1)`.
- КОЛИ `hp_zero(enemy)` → ТО `disappear_a`.
- КОЛИ `contact(gold, gold)` → ЯКЩО `same(a, b, value)` → ТО `merge(a, b → c)`, `set_value(c, 2×value)`.
- КОЛИ `contact(player, gold)` → ТО `score(value)`, `counter(xp, +value)` (?), `heal(player, n)`; `custom: «наступні фігурки зʼявляються з половинним значенням»`.
- КОЛИ `contact(enemy, gold)` → ТО `disappear_b` (ворог зʼїв золото).
- КОЛИ `contact(enemy, player)` → ТО `hp(player, −n)`.
- КОЛИ `enter(enemy, pit)` → ЯКЩО `not state(enemy, pit_immune)` → ТО `disappear_a`; КОЛИ `enter(player, pit)` → ТО `lose`.
- КОЛИ `turn_end(player)` → ЯКЩО `rng(p)` → ТО `spawn_at(enemy, random_cell)`; темп показує лічильник небезпеки.
- КОЛИ `turn_end(player)` → ТО `custom: «вороги-стрибуни роблять власний крок до цілі»`.
- КОЛИ `counter(xp, >=, bar)` → ТО `choose(3 random power-ups)`; обране діє до кінця забігу.
- КОЛИ `input(skill)` → ЯКЩО `has(player, mana ≥ cost)` (?) → ТО `freeze(enemies, 1)` / `heal(player, n)` / `set_state(player, float_over_pits)` / `set_cell(wall, floor)` / `custom: «відкласти спавн»`.
- КОЛИ `all_gone(enemy)` → ТО `custom: «кімнату очищено: стіни перебудовуються»`, `next_level`.
- КОЛИ `hp_zero(player)` → ТО `lose`; рахунок забігу — сума зʼїденого.

## Керування і ввід
- Тач: свайп у 4 напрямки; одна рука. PC: стрілки/WASD (?).
- Здібності — кнопки біля поля (?).
- Undo в ранніх версіях працював лише на хід, що вів до смерті; що лишилось у релізі — не перевірено.

## Вікна, меню, HUD
- `game-screen`: кімната; HP героя й ворогів сегментами; `xp-bar` зверху; мана; `danger-meter` (скоро новий ворог); `score`.
- `upgrade-window`: вибір 1 з 3 апгрейдів на підвищенні рівня.
- Повернення до забігу — одразу в гру, без титульного екрана (`quick-resume`).
- `end-screen`: рахунок; `achievements-window` (Steam).

## Фічі поза полем
- `permadeath`: забіг до смерті, потім заново.
- `achievements` (Steam); `leaderboard` — гравці порівнюють рахунки (2000 — 60 000), чи є табло в грі — (?).
- Локалізації: 8 мов.

## Варіації й родичі
- Threes! (рух на 1 і злиття) і `falling-match/2048` (зсув до упору); Imbroglio — у файлі `868-hack` (перебудова стін за скарб).
- Інші «зсув усього поля + вороги»: Dungeon Raid і Triple Town (`falling-match`), 868-HACK як broughlike-мала сітка.
- **Осі варіацій**: свайп рухає все / лише героя; злиття ×2 / +1 (ранній прототип); шкода — від зіткнення зі стіною / від атаки; ворог-імунітет — до стін / ям / рушіння.

## Цікавинки для курсу
- `shift(all)` на одну клітину з порядком обробки по напрямку — 📎 (класика Threes, але з кількома типами сутностей).
- Шкода від стіни під час зсуву: стіна як зброя гравця й ворога — 🌱.
- «Зʼїв — наступні вдвічі дешевші»: компроміс злиття проти швидкої вигоди — 🌱.
- Типи ворогів як імунітети до одного правила (стіни / ями / рух) — 📎 (таблиця прапорців).
- Вибір 1 з 3 апгрейдів на рівні — 🌱.
- Злий близнюк, що сам рухає поле, — 🥉 (вторинне джерело `shift`).

## Мапа на каталог
- Є: `swipe-gestures` · `keyboard-controls` · `move-4dir` · `tile-merge` · `hp-damage` · `chase-player` · `spawn-random-cell` · `event-points` (очки = значення) · `in-round-upgrades` · `run-relics` (пасивки до кінця забігу) · `destroy-all-enemies` (очистити кімнату) · `sequential-levels` (кімнати) · `environment-death` (ями) · `permadeath`.
- **Нема** → пропозиції карток:
  - `+swipe-moves-all` «Свайп зсуває всі сутності на 1» · entities/movement · 📎 · слот {step: 1|to-wall}.
  - `+wall-crush-damage` «Удар об стіну під час зсуву — шкода» · entities/combat · 🌱.
  - `+eat-merged-value` «Зʼїсти плитку — отримати її значення» · game-logic/score · 🌱.
  - `+merge-respawn-halving` «Після зʼїдання нові плитки дешевші» · game-logic/economy · 🌱.
  - `+pit-knockoff` «Скинути ворога в яму» · entities/combat · 🌱.
  - `+level-up-pick-of-3` «Рівень — вибір 1 з 3 апгрейдів» · game-logic/progression · 🌱.
  - `+wall-reshuffle-on-clear` «Очищена кімната перебудовує стіни» · levels/generation · 📎.
  - `+enemy-trait-immunity` «Тип ворога = імунітет до одного правила» · entities/ai · 📎.

## Пропозиції до словників
- `+effect:eat(b)` — зʼїсти плитку: значення → очки/XP/лікування (зараз `pickup` + `score`).
- `+ui:danger-meter` — наскільки близько новий спавн.
- `+ui:xp-bar` — смуга досвіду до наступного вибору.
- `+feature:quick-resume` — старт одразу в незакінчений забіг.
- `+card:swipe-moves-all` · `+card:wall-crush-damage`.

## Джерела
- ⭐ [Stately Play: огляд](https://statelyplay.com/2018/12/07/twinfold-mashes-several-well-worn-mechanisms-into-a-unique-new-experience/) — свайп на 1 клітину рухає все, злиття ×2, половинна ціна після зʼїдання, стіни й ями, здібності.
- [Game Developer: про дизайн](https://www.gamedeveloper.com/design/behind-the-mashed-up-roguelike-charm-of-i-twinfold-i-) — Threes! + Imbroglio, 6 описаних типів ворогів, мана, лічильник небезпеки.
- [TouchArcade: огляд](https://toucharcade.com/?p=245356) — XP-смуга, 3 апгрейди на вибір, сегменти HP, кімнати.
- [Steam](https://store.steampowered.com/app/980880/Twinfold/) — 7 типів ворогів, 40+ навичок, реліз 5.12.2018.
- [App Store](https://apps.apple.com/app/id1437168510).
- YouTube: [пошук «Twinfold gameplay»](https://www.youtube.com/results?search_query=Twinfold+gameplay).

## Непевне
- (?) Steam каже 7 типів ворогів, описані 6 (сірий, синій, фіолетовий, червоний, зелений, злий близнюк) — сьомий невідомий; чи «базовий» ворог — окремий тип.
- (?) Огляди розходяться: TouchArcade зве золоті фігурки «пасивними ворогами» і пише, що XP = значення; Stately Play — що значення = очки. Можливо, і те, і те.
- (?) Як мана повʼязана з навичками (ціна активних здібностей?) — не перевірено.
- (?) Чи кімната очищується «знищенням усіх ворогів» чи «злиттям усіх фігурок» — TouchArcade каже «defeating or combining all enemies».
- (?) Розмір кімнати, кількість HP героя, PC-керування — не бачив.
- (?) Чи падіння героя в яму — миттєва смерть, чи втрата HP.
