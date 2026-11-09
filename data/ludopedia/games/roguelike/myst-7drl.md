---
title: Myst (7DRL)
slug: myst-7drl
aka: [Myst (watabou)]
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2017
platforms: [web, Windows, macOS, Android]
links:
  - {kind: itch, url: "https://watabou.itch.io/myst", best: true, note: "сторінка гри: туман, факел, духи, руни трьох видів, Spirit King; грати в браузері"}
  - {kind: other, url: "https://roguetemple.com/7drl/2017", note: "оцінки 7DRL 2017: мапа перегенеровується під туманом, видно лише поруч, слабкий/сильний стан ворогів щоходу"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=myst+watabou+7drl", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-4dir, fog-of-war, dungeon-generation, chase-player, hunger-clock, hp-damage, item-pickup, permadeath, sequential-levels, collect-quota, telegraphed-intents, gui-render, +regen-unseen-map, +torch-radius-clock, +enemy-strong-weak-cycle, +no-free-attack-on-forced-move, +kill-refills-clock]
proposes: ["+trigger:out_of_sight(cell)", "+effect:regen(cells)", "+cond:visible(cell)", "+card:regen-unseen-map", "+card:enemy-strong-weak-cycle"]
author: opus
date: 2026-11-09
---

# Myst (7DRL) — лабіринт у тумані, що перебудовується скрізь, де ти його не бачиш

## Суть
Мінімальний покроковий роглайт від watabou (автор Pixel Dungeon) для 7DRL 2017. Ліс накрив проклятий туман: гравець бачить лише клітини біля себе, поки горить магічний факел. Ключова механіка — **все, що вкрив туман, перегенеровується**: стіни, вороги й предмети зникають і зʼявляються по-новому навіть у вже відвіданих місцях. Мета — зібрати руни, викликати Spirit King і вбити його, щоб розвіяти туман.

## Поле і час
- Клітинний лабіринт (квадратна сітка (?)); відомо лише найближче оточення в радіусі світла факела.
- Поза видимістю мапа «нестабільна»: щохід невидима частина може змінитись — гравець завжди трохи загублений.
- Покроково: хід гравця — хід духів; кнопки пропуску ходу нема.
- Рівні (поверхи) зі зростанням складності (рецензент дійшов до рівня 3).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець з факелом | player | HP, рівень факела | рух клітинами; атака — рух у духа |
| Факел | object | рівень, падає щохід | поки горить — туман не забирає гравця; освітлює радіус |
| Туман | zone | усе поза світлом | ковтає того, хто в нього ступить; під ним мапа перебудовується |
| Дух туману | enemy | очі: спокій / світяться / червоні | переслідує, заганяє в кут; стан слабкий/сильний змінюється щоходу |
| Руна вогню | pickup | — | відновлює факел |
| Руна крові | pickup | — | відновлює HP |
| Руна шляху | pickup | 5 потрібно | 5 рун → зʼявляється Guardian Spirit |
| Guardian Spirit | neutral | — | зʼявляється після 5 рун шляху (?) |
| Spirit King | boss | — | вбити → туман розвіюється (перемога) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell)` → ТО `move(player, dir)`; ЯКЩО `occupied(cell, spirit)` → ТО `custom: «атака духа»`.
- КОЛИ `turn_end(player)` → ТО `custom: «клітини поза видимістю перегенеровуються»` (`+effect:regen`).
- КОЛИ `turn_end(player)` → ТО `counter(torch, -1)`; ЯКЩО `counter(torch, ==, 0)` → ТО `custom: «туман поглинає гравця»` (`lose`) (?).
- КОЛИ `contact(player, fire_rune)` → ТО `pickup`, `counter(torch, +n)`.
- КОЛИ `contact(player, blood_rune)` → ТО `pickup`, `heal(player, n)`.
- КОЛИ `contact(player, way_rune)` → ТО `pickup`, `counter(way, +1)`; КОЛИ `counter(way, ==, 5)` → ТО `spawn(guardian_spirit)`.
- КОЛИ `turn_start(spirits)` → ТО `custom: «стан духа перемикається слабкий ↔ сильний; сильний — очі світяться (червоні — найнебезпечніше)»`.
- КОЛИ `custom: «гравець атакує духа»` → ЯКЩО `state(spirit, weak)` → ТО `damage(n)`; ЯКЩО `state(spirit, strong)` → ТО `custom: «шкода гравцю»` (?).
- КОЛИ `died(spirit)` → ТО `counter(torch, +n)` (рецензія: вбивство відновлює «їжу») (?).
- КОЛИ `custom: «гравця змусили стати поруч з духом»` → ТО `custom: «дух не отримує безкоштовної атаки»`.
- КОЛИ `died(spirit_king)` → ТО `win`.
- КОЛИ `hp_zero(player)` → ТО `game_over` (permadeath).
- Перемога: вбити Spirit King. Поразка: HP або факел вичерпано (?). Рахунок: — (поступ — рівні).

## Керування і ввід
- Рух по клітинах (клавіші / тап на мобільних (?)); атака — рух у ворога; пропуску ходу нема.

## Вікна, меню, HUD
- `game-screen` — освітлена пляма навколо гравця, `hp-bar`, рівень факела (`energy-bar`), лічильник рун шляху (?).
- `end-screen` — смерть / перемога (?).

## Фічі поза полем
- `permadeath`, нова генерація кожного забігу.
- Мульти-платформа: HTML5, Windows, macOS, Android (Haxe + OpenFL).

## Варіації й родичі
- [Brogue](brogue.md), [Rogue](rogue.md) — запамʼятована мапа: відвідане лишається; тут памʼять навмисно не діє — забуте змінюється.
- Pixel Dungeon — інша гра того ж автора.
- [Dungeon Master](dungeon-master.md), [Legend of Grimrock](legend-of-grimrock.md) — світло-факел як ресурс видимості.
- **Осі варіацій:** памʼять мапи (повна / туман війни з памʼяттю / перегенерація невидимого); ресурс-таймер (їжа / факел / нічого); загроза ворога (постійна / циклічна і показана).

## Цікавинки для курсу
- Перегенерація всього поза видимістю — 🥈 (FOV + локальна генерація, що не ламає видиму частину і звʼязність).
- Факел як таймер і радіус видимості одночасно — 📎.
- Стан ворога слабкий/сильний, що чергується щоходу і показаний очима, — 🌱 (телеграф наміру).
- Квота рун шляху → поява боса — 🌱.
- Вбивство відновлює таймер: ризик заради ресурсу — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `fog-of-war` (без памʼяті) · `dungeon-generation` · `chase-player` · `hunger-clock` (факел) · `hp-damage` · `item-pickup` · `permadeath` · `sequential-levels` · `collect-quota` (5 рун) · `telegraphed-intents` (очі) · `gui-render`.
- **Нема** → пропозиції карток:
  - `+regen-unseen-map` «Невидима частина мапи перегенеровується» · levels/generation · 🥈.
  - `+torch-radius-clock` «Світло = таймер і радіус видимості» · entities/state · 📎.
  - `+enemy-strong-weak-cycle` «Ворог чергує слабкий і сильний стан щоходу» · entities/ai · 🌱.
  - `+no-free-attack-on-forced-move` «Вимушене зближення не дає ворогу атаки» · entities/combat · 🌱.
  - `+kill-refills-clock` «Вбивство відновлює таймер-ресурс» · game-logic/economy · 🌱.

## Пропозиції до словників
- `+trigger:out_of_sight(cell)` — клітина вийшла з поля зору.
- `+effect:regen(cells)` — перегенерувати клітини.
- `+cond:visible(cell)` — клітина в полі зору гравця.
- `+card:regen-unseen-map`, `+card:enemy-strong-weak-cycle` — див. вище.

## Джерела
- ⭐ [itch.io: Myst by watabou](https://watabou.itch.io/myst) — туман і факел, мінливий лабіринт (стабільне лише поза туманом), духи не атакують, але заганяють у кут, очі як сигнал небезпеки, руни вогню/крові/шляху, 5 рун → Guardian Spirit, Spirit King, платформи, Haxe/OpenFL.
- [Roguetemple: 7DRL 2017](https://roguetemple.com/7drl/2017) — оцінки й рецензії: мапа перегенеровується під туманом навіть відвідана, видно лише поруч, покрокова, permadeath, нема пропуску ходу, вимушене зближення без безкоштовної атаки, суворий таймер «їжі», вбивство його поповнює, стан ворога слабкий/сильний щоходу.
- YouTube: пошук «myst watabou 7drl».

## Непевне
- (?) Сторінка каже «духи не атакують», рецензія — «вороги не отримують безкоштовної атаки»; як саме гравець втрачає HP (атака сильного духа?) — не перевірено.
- (?) «Їжа» з рецензії = рівень факела зі сторінки — припущення.
- (?) Що буде, коли факел згасне; роль Guardian Spirit щодо Spirit King.
- (?) Форма сітки, радіус світла, кількість рівнів, керування.
