---
title: Tumbleweed
slug: tumbleweed
aka: [Перекотиполе]
family: chess-abstract
also: []
klass: figure
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: territory
year: 2020
platforms: [board, web]
links:
  - {kind: other, url: "https://ludii.games/details.php?keyword=Tumbleweed", best: true, note: "Ludii: правила, лінія видимості, висота = кількість своїх, що бачать, перезаселення вищим; Mike Zapawa, 2020"}
  - {kind: other, url: "https://www.boardspace.net/tumbleweed/english/Rules.html", note: "повні правила Boardspace: старт, swap, хід, заміна, кінець"}
  - {kind: play, url: "https://www.boardspace.net/english/about_tumbleweed.html", note: "онлайн-партія, роботи, архів партій"}
  - {kind: other, url: "https://docs.littlegolem.net/games/tumbleweed/", note: "Little Golem: розміри 4/6/8/11, підрахунок «зайняті + контрольовані впливом», нічия"}
  - {kind: other, url: "https://rulespal.com/tumbleweed/rulebook", note: "правила, розміри 6/8/10/11, пояснення swap, стратегія «очей»"}
  - {kind: bgg, url: "https://boardgamegeek.com/game/318702", note: "BGG (HTML агентам не відкривається)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Tumbleweed+board+game+Zapawa", note: "пошук; партії"}
stage: v1
coverage: 75
mechanics: [piece-capture, pass-turn, no-moves-left, hot-seat, turn-enforcement, ai-opponent, online-multiplayer, rating-system, field-size-picker, cell-click, hover-highlight, legal-move-highlight, last-move-highlight, replay, move-notation, match-setup, game-screen, main-menu, end-screen, help-window, state-as-data, unit-tests, +hex-grid-render, +place-stone, +swap-rule, +sight-count-height, +replace-taller, +influence-scoring, +territory-scoring, +majority-win, +pass-end, +shared-neutral-piece]
proposes: ["+cond:sight_count", "+cond:taller", "+effect:influence_count", "+trigger:passes", "+ui:sight-lines", "+ui:height-preview", "+ui:stack-height-label", "+ui:territory-overlay", "+window:swap-dialog", "+card:sight-count-height", "+card:replace-taller", "+card:influence-scoring"]
author: opus
date: 2026-11-09
---

# Tumbleweed — став стос туди, куди бачать твої: його висота = скільки твоїх стосів дивляться на клітину

## Суть
Гра на територію з постановкою стосів на гекс-полі. Хід — поставити новий стос на клітину, яку бачить хоча б один твій стос по прямій без перешкод; висота стосу дорівнює кількості твоїх стосів, що бачать цю клітину. Зайняту клітину можна перезаселити лише вищим стосом: так бʼють чужий стос або підсилюють свій. Коли обидва пасують поспіль, рахують зайняті й контрольовані клітини; більше половини поля — перемога. Автор — Mike Zapawa (2020, «під час COVID»).

## Поле і час
- Гекс-гекс (шестикутник із шестикутників), розмір за довжиною сторони: Little Golem — 4 / 6 / 8 / 11; RulesPal — 6 (новачки, бліц), 8 (стандарт змагань), 10 (листування), 11 (найглибший). Офіційного одного розміру нема.
- Лінія видимості — 6 гекс-напрямків; будь-який стос (свій, чужий, нейтральний) закриває огляд далі.
- У центрі — нейтральний стос висоти 2; він не належить нікому, але блокує огляд.
- Хід = одна постановка або пас; часу нема (онлайн — звичайний годинник сервера).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Стос гравця | piece | колір red / white, висота h ≥ 1 | не рухається; бачить по 6 прямих до першого стосу; може бути замінений вищим |
| Нейтральний стос | neutral | висота 2, центр | блокує огляд, нічий (?) чи можна перезаселити |
| Клітина | terrain | порожня / зайнята | ціль постановки, якщо її бачить хоч один свій стос |
| Лінія видимості | zone | 6 променів від клітини | рахує «своїх, що бачать» → висота нового стосу |
| Контрольована клітина | zone | порожня, бачать більше своїх, ніж чужих | іде в рахунок власникові впливу |
| Запас фішок | zone | фактично необмежений | — |

## Правила (КОЛИ → ЯКЩО → ТО)
- Старт: КОЛИ `game_start` → ТО `spawn_at(neutral_stack_h2, center)`.
- Перший хід (господар): КОЛИ `input(place, cell_red, cell_white)` → ЯКЩО `free(cell_red)` and `free(cell_white)` → ТО `place(red_stack_h1, cell_red)`, `place(white_stack_h1, cell_white)` — єдина постановка поза лінією видимості.
- Swap: КОЛИ `turn_start(guest)` → ТО `choose(колір)` — гість обирає сторону (pie rule); далі ходить red.
- КОЛИ `input(place, cell)` → ЯКЩО `custom: «n = кількість моїх стосів, що бачать cell»` (`+cond:sight_count`) and `custom: «n ≥ 1»` → ТО продовжити; інакше `block` (нульова видимість — нелегально).
- КОЛИ `input(place, cell)` → ЯКЩО `free(cell)` → ТО `place(stack_h_n, cell)`.
- КОЛИ `input(place, cell)` → ЯКЩО `occupied(cell, enemy_stack)` and `custom: «n > висоти наявного стосу»` (`+cond:taller`) → ТО `disappear(enemy_stack)`, `place(stack_h_n, cell)` — взяття.
- КОЛИ `input(place, cell)` → ЯКЩО `occupied(cell, own_stack)` and `custom: «n > висоти наявного»` → ТО `set_value(own_stack, n)` — підсилення.
- КОЛИ `input(place, cell)` → ЯКЩО `occupied(cell, stack)` and `not custom: «n > висоти»` → ТО `block`.
- КОЛИ `input(pass)` → ТО `pass_turn` — пас дозволено завжди.
- КОЛИ `custom: «два паси поспіль»` (`+trigger:passes`) або `no_moves(both)` → ТО `game_over`.
- КОЛИ `game_over` → ТО `custom: «рахунок = зайняті клітини + порожні, які бачить більше моїх стосів, ніж чужих»` (`+effect:influence_count`).
- Перемога: зайняти або контролювати більше половини поля · Поразка: менше · Рівний рахунок — нічия (Little Golem).

## Керування і ввід
- Настільна: поставити стос із потрібної кількості фішок свого кольору.
- (цифрова версія) Наведення на клітину → `height-preview` (якої висоти вийде стос) і `sight-lines` (які свої стоси бачать); клік — постановка; окрема кнопка «пас».
- Swap: на другому ході гостя — клік по фішці іншого кольору (Ludii) або кнопка swap (Little Golem).

## Вікна, меню, HUD
- `main-menu` / лобі (Boardspace, Little Golem): партія з людиною або роботом.
- `match-setup`: розмір поля (4–11), хто господар.
- `swap-dialog`: гість приймає кольори або міняє.
- `game-screen`: гекс-поле, `stack-height-label` на кожному стосі, `height-preview` і `sight-lines` під курсором, `legal-move-highlight` (усі клітини з n ≥ 1, на зайнятих — лише де n більше), `territory-overlay` (поточний вплив), `score` обох, `turn-indicator`, `last-move-highlight`, `move-list`.
- `end-screen`: зайняті + контрольовані, поріг «понад половину».
- `replay-window`: архів партій Boardspace.
- Переходи: main-menu → match-setup → game-screen (swap-dialog на 2-му ході) → end-screen.

## Фічі поза полем
- `online-multiplayer` — Boardspace (з 2021, турнір 2022), Little Golem, iggamecenter, BGA (за результатами пошуку).
- `ai-opponent-levels` — робот Boardspace («adequate, if not stellar»).
- `custom-difficulty` ↔ розмір поля; `swap-rule`; рейтинги й архіви (`history`, `replay`).
- Little Golem автоматично рахує контрольовані клітини.

## Варіації й родичі
- Постановка без руху з рахунком території — [go](go.md); лінії видимості й «блокування поглядом» — [amazons](amazons.md) (королеви бʼють по прямих до перешкоди).
- Стоси без руху, висота як сила — інший тип стосів, ніж у [dvonn](dvonn.md) і [tak](tak.md) (там стоси ходять).
- Swap-правило — як у [hex](hex.md) і [twixt](twixt.md).
- Осі варіацій: **висота нового стосу** (= кількість своїх, що бачать / фіксована) · **заміна** (лише вищий / рівний теж) · **що блокує огляд** (усі стоси / лише чужі) · **рахунок** (лише зайняті / + вплив).

## Цікавинки для курсу
- Гекс-координати і промені в 6 напрямках до першої перешкоди — 📎.
- Генерація ходів: для кожної клітини порахувати своїх, що бачать, і порівняти з наявною висотою — 📎 (інкрементно після кожної постановки — 🥉).
- Підрахунок впливу на порожніх клітинах наприкінці — 🌱 (той самий підрахунок, що й для ходу).
- Swap / pie rule і кінець двома пасами — 🌱.
- AI: розгалуження = майже вся дошка; оцінка через карту впливу, MCTS — 🥇.

## Мапа на каталог
- Є: `piece-capture` ↔ заміна чужого стосу · `pass-turn`, `no-moves-left` · `hot-seat`, `turn-enforcement`, `ai-opponent`, `online-multiplayer`, `rating-system` · `field-size-picker` ↔ 4–11 · `cell-click`, `hover-highlight`, `legal-move-highlight`, `last-move-highlight` · `replay`, `move-notation`, `match-setup` · `game-screen`, `main-menu`, `end-screen`, `help-window` · `state-as-data`, `unit-tests`.
- **Нема** → пропозиції карток:
  - `+hex-grid-render`, `+place-stone`, `+swap-rule` (див. hex.md); `line-of-sight-attack` у каталозі — атака ворога по лінії, тут промінь дає дозвіл і силу ходу, тож не тегую.
  - `+sight-count-height` «Сила постановки = кількість своїх, що бачать клітину» · entities/legality · 📎.
  - `+replace-taller` «Зайняте можна перезаселити лише сильнішим» · entities/combat · 🌱 · слот {own: reinforce}.
  - `+influence-scoring` «Порожня клітина — тому, чиїх більше бачить» · game-logic/score · 🌱.
  - `+territory-scoring`, `+pass-end` (див. go.md) · `+majority-win` (є в сімʼї) · `+shared-neutral-piece` (нейтральний стос у центрі).

## Пропозиції до словників
- `+cond:sight_count` — кількість своїх сутностей, що бачать клітину по прямих без перешкод (порівняння з n).
- `+cond:taller` — нова сутність сильніша/вища за наявну в клітині.
- `+effect:influence_count` — підрахунок клітин за впливом (бачить більше своїх).
- `+trigger:passes` — два паси поспіль (уже пропонувалось у go).
- `+ui:sight-lines` — промені видимості від клітини під курсором; `+ui:height-preview` — висота стосу, що вийде; `+ui:stack-height-label` (уже пропонувалось у dvonn); `+ui:territory-overlay` (уже пропонувалось у go).
- `+window:swap-dialog` (уже пропонувалось у hex).
- `+card:sight-count-height`, `+card:replace-taller`, `+card:influence-scoring` — див. «Мапа на каталог».

## Джерела
- ⭐ [Ludii: Tumbleweed](https://ludii.games/details.php?keyword=Tumbleweed) — гекс-гекс, нейтральний 2-стос, перші два 1-стоси, вибір сторони, висота за видимістю, перезаселення вищим, кінець двома пасами, «понад половину поля»; Mike Zapawa, 2020.
- [Boardspace: правила Tumbleweed](https://www.boardspace.net/tumbleweed/english/Rules.html) — повні правила, приклад swap, «зайняти або контролювати понад половину».
- [Boardspace: про Tumbleweed](https://www.boardspace.net/english/about_tumbleweed.html) — онлайн з 2021, турнір 2022, робот.
- [Little Golem: Tumbleweed](https://docs.littlegolem.net/games/tumbleweed/) — розміри 4/6/8/11, нульова видимість нелегальна, контроль порожньої = більше своїх бачить, рівно — нічия.
- [RulesPal: Tumbleweed](https://rulespal.com/tumbleweed/rulebook) — розміри 6/8/10/11, swap як pie rule, поради про «очі».

## Непевне
- (?) Чи можна перезаселити нейтральний стос (висотою ≥ 3) — джерела не кажуть.
- (?) Розміри поля розходяться: Little Golem 4/6/8/11, RulesPal 6/8/10/11; «8 — стандарт, 11 — для сильних» — зі звітів пошуку (BGA, Sask Today), сторінок не відкривав.
- (?) Порожня клітина, яку бачить порівну своїх і чужих, — нічия (не рахується нікому) — висновок з формулювання Little Golem.
- (?) Boardspace: «стартові фішки — на клітинах на вибір господаря» vs «будь-де» — суперечність у самих правилах, сенс однаковий.
- (?) Наявність Tumbleweed на BGA і iggamecenter — лише з результатів пошуку.
