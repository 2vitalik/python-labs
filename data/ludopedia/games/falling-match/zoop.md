---
title: Zoop
slug: zoop
aka: [ZOOP]
family: falling-match
also: [tower-lanes]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: survive
year: 1995
platforms: [SNES, Genesis, MS-DOS, Mac, PlayStation, Game Gear, Game Boy, Saturn, Jaguar]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Zoop", best: true, note: "правила: центр, 4 сторони, стрілок-трикутник, обмін кольором, бомби, квота, програш"}
  - {kind: other, url: "https://gamesdatabase.org/Media/SYSTEM/Microsoft_DOS//Manual/formated/Zoop.htm", note: "мануал DOS-версії (403 при перевірці)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=zoop+1995+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [projectile-shot, shoot-forward, move-4dir, keyboard-controls, chain-reaction, event-points, collect-quota, progress-acceleration, enemy-reached-base, spawn-schedule, explode-area, score-records, game-pause, difficulty-levels, +radial-lanes, +shoot-swap-color, +lane-push-advance, +line-bomb, +color-clear-item, +lane-overflow-lose]
proposes: ["+effect:shoot", "+cond:frontmost", "+card:shoot-swap-color", "+card:lane-push-advance", "+ui:quota-meter"]
author: opus
date: 2026-11-09
---

# Zoop — стрілок у центральному квадраті збиває ряди фігур, що повзуть з чотирьох боків

## Суть
Гравець керує трикутником усередині центрального квадрата; з чотирьох боків до центру смугами повзуть кольорові фігури. Постріл у бік смуги влучає у найближчу до центру фігуру: якщо колір збігається з кольором трикутника — вона зникає («zoop»), і постріл летить далі до наступної того самого кольору; на першій фігурі іншого кольору трикутник **обмінюється з нею кольором** і постріл зупиняється. Ядро — колір стрілка як змінний ресурс: кожен «невдалий» постріл перефарбовує тебе, і це треба планувати. Програш — фігура дійшла до центрального квадрата.

## Поле і час
- Хрестоподібне поле: центральний квадрат (зона стрілка) + чотири прямокутні поля-«смуги» зліва, справа, згори, знизу; кожен ряд/стовпець бокового поля — окрема смуга, що веде до центру.
- Фігури входять із зовнішнього краю смуги й штовхають уже наявні фігури цієї смуги ближче до центру.
- Real-time: нова фігура — щосекунди, на пізніх рівнях частіше; дві фігури поспіль ніколи не входять з одного боку (квадранта).
- Камера фіксована, усе поле видно; фони рівнів змінюються, пізні — «Opti-Challenge» з оптичними ілюзіями, що відволікають.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Трикутник-стрілок | player | колір, позиція в центрі, напрям | рух по клітинах центру, поворот до смуги, постріл по прямій |
| Фігура (shape) | tile | колір, смуга, позиція | входить з краю смуги, штовхається новою фігурою до центру |
| Смуга | zone | бік, номер ряду/стовпця | черга фігур; найближча до центру — ціль пострілу |
| Центральний квадрат | zone | — | зона стрілка; фігура в ньому → програш |
| Proximity Bomb (блискавка) | pickup | — | зчищає фігури довкола цілі (3×3 за Wikipedia) |
| Line Bomb (шестірня) | pickup | — | зчищає всю смугу цілі |
| Color Bomb (клякса) | pickup | — | (?) зчищає фігури одного кольору |
| Bonus Spring (пружина) | pickup | — | (?) бонус очок; спецфігури не закінчують гру в центрі |
| Генератор фігур | spawner | темп рівня | щотік-період додає фігуру в смугу, не з того самого боку |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `timer(spawn_rate)` → ЯКЩО `custom: «бік ≠ бік попередньої фігури»` → ТО `spawn_at(shape, outer_edge(lane))`, `push(shapes_in_lane, toward_center)`.
- КОЛИ `input(arrow)` → ЯКЩО `free(cell)` у центрі → ТО `move(player, dir)`, `face(player, dir)`.
- КОЛИ `input(fire)` → ТО `custom: «shoot — постріл уздовж ряду/стовпця, куди дивиться стрілок»`.
- КОЛИ `contact(shot, shape)` → ЯКЩО `custom: «frontmost — найближча до центру фігура смуги»` and `same(player, shape, color)` → ТО `disappear_b`, `score(n)`, `counter(quota, +1)`, постріл летить до наступної фігури.
- КОЛИ `contact(shot, shape)` → ЯКЩО `not same(player, shape, color)` → ТО `swap(player.color, shape.color)`, `disappear_a` (постріл зупиняється).
- КОЛИ `after(clear)` ланцюга → ЯКЩО `chain(n)` → ТО `score(bonus × n)` (?) — довший ланцюг дорожчий.
- КОЛИ `contact(shot, proximity_bomb)` → ТО `explode(area_3x3)`, `score(n)`.
- КОЛИ `contact(shot, line_bomb)` → ТО `clear(lane)`.
- КОЛИ `contact(shot, color_bomb)` → ТО `custom: «зчищає всі фігури кольору стрілка»` (?).
- КОЛИ `reach(shape, center_square)` → ЯКЩО `not state(shape, special)` → ТО `lose`.
- КОЛИ `counter(quota, ≥, level_quota)` → ТО `next_level`, `speed(spawn_rate, ×k)`, `custom: «зміна фону; пізні — Opti-Challenge»`.
- Перемога: нема — гра на виживання. Поразка: фігура в центрі. Рахунок: очки за кожен zoop, бонуси ланцюга й спецфігур (?).

## Керування і ввід
- Хрестовина/стрілки — рух трикутника по клітинах центрального квадрата; трикутник розвертається в бік руху.
- Кнопка Fire — постріл у напрямку, куди дивиться трикутник; натискання у бік стіни квадрата без руху — лише поворот (?).
- DOS: стрілки + Ctrl як «Fire» в меню (readme).

## Вікна, меню, HUD
- `splash-screen` → `main-menu`: Start · Options (`settings-window`: складність, тип гри, музика/звук (?)) · High Scores (`leaderboard`).
- `game-screen`: хрест смуг із центром; `score`, `level-number`, `custom: «quota-meter» — скільки фігур лишилось до наступного рівня`, мініатюра поточного кольору стрілка (сам трикутник).
- `pause-menu`.
- `end-screen` Game Over → введення імені в `leaderboard`.
- Переходи: main-menu → game-screen → (квота) зміна рівня/фону без окремого екрана (?) → (фігура в центрі) end-screen → leaderboard.

## Фічі поза полем
- `levels-sequential` з `mode-endless`: рівні = квоти, швидкість росте; фони змінюються до 10-го рівня, далі — Opti-Challenge.
- `difficulty-presets`, `pause`, `leaderboard-local`.
- (?) Два типи гри: «Level» (рівні з квотою) і «Continuous» (без пауз між рівнями).
- Мультиплеєр — лише у версії Game Boy.

## Варіації й родичі
- Родичі: Plotting / Quarth (стріляєш блоками в стіну), Puzzle Bobble (постріл кольором), Magical Drop (стрілок під стовпцями бере й кидає), Zuma (потік куль до центру/лунки), Klax.
- **Осі варіацій**: звідки йде загроза (згори / знизу / з 4 боків до центру) · що робить постріл з іншим кольором (нічого / прилипає / **міняє колір стрілка**) · ланцюг (одна ціль / до першого іншого кольору) · програш (стеля / центр).

## Цікавинки для курсу
- Обмін кольором при «промаху»: стан стрілка як ресурс, який змінює сам постріл — 📎.
- Чотири черги-смуги до центру з push при вході нової фігури — 📎 (deque на смугу, перевірка «дійшла до центру»).
- Постріл, що проходить ланцюг однакових і зупиняється на першому іншому — 🌱.
- Генератор із забороною повторного боку поспіль — 🌱.
- Спецфігури (вибух 3×3, вся смуга, колір) як окремий тип у смузі — 📎.
- Opti-Challenge-фони як складність через рендер — 🥉 у GUI.

## Мапа на каталог
- Є: `projectile-shot` + `shoot-forward` (постріл по прямій) · `move-4dir` · `keyboard-controls` · `chain-reaction` (ланцюг zoop) · `event-points` · `collect-quota` (квота рівня) · `progress-acceleration` · `enemy-reached-base` (фігура в центрі) · `spawn-schedule` · `explode-area` (Proximity Bomb) · `score-records` · `game-pause` · `difficulty-levels`.
- **Нема** → пропозиції карток:
  - `+radial-lanes` «Смуги з усіх боків до центру» · world/field · 📎 (тег уже є в корпусі).
  - `+shoot-swap-color` «Постріл у чужий колір міняє колір стрілка» · entities/combat · 📎.
  - `+lane-push-advance` «Нова фігура штовхає чергу смуги вперед» · entities/move · 🌱 · слот {lanes}.
  - `+line-bomb` «Спецплитка зчищає свою лінію» · entities/combat · 🌱.
  - `+color-clear-item` · `+lane-overflow-lose` — теги вже є в корпусі.

## Пропозиції до словників
- `+effect:shoot` — постріл уздовж лінії з першою ціллю (є в інших файлах як пропозиція — підтверджую).
- `+cond:frontmost` — сутність найближча до гравця/центру у своїй смузі (підтверджую).
- `+card:shoot-swap-color` · `+card:lane-push-advance` — див. «Мапу».
- `+ui:quota-meter` — лічильник «скільки ще до наступного рівня» (родич `remaining-counter`, але для квоти рівня).

## Джерела
- ⭐ [Wikipedia: Zoop](https://en.wikipedia.org/wiki/Zoop) — центр, сторони, постріл, обмін кольором, ланцюг, Proximity/Line Bomb, квота й прискорення, Opti-Challenge, програш, платформи.
- [Мануал DOS-версії (gamesdatabase.org)](https://gamesdatabase.org/Media/SYSTEM/Microsoft_DOS//Manual/formated/Zoop.htm) — знайдено пошуком; відкрити не вдалося (403). З пошукового сніпета: назви Bonus Springs, Color Bombs; Proximity Bomb «знищує всі фігури, що торкаються наступної влученої»; спецфігури не закінчують гру в центрі.
- YouTube: пошук «zoop 1995 gameplay».

## Непевне
- (?) Розміри: центр 4×4, бокові поля 8 клітин завглибшки зліва/справа і 7 згори/знизу — з памʼяті, не перевірено.
- (?) Proximity Bomb: Wikipedia — «3×3 навколо цілі», мануал (сніпет) — «усі, що торкаються наступної влученої фігури».
- (?) Ефекти Color Bomb і Bonus Spring — лише назви з мануалу; точна дія не підтверджена.
- (?) Сніпет: «фігура, проштовхнута впритул до центру, одразу зникає» — у деяких версіях; не зрозуміло, як це узгоджується з програшем.
- (?) Режими «Level» / «Continuous», пункти Options, кількість фігур у квоті, очки й бонус ланцюга — з памʼяті або не знайдено.
- SegaRetro, StrategyWiki, Giant Bomb — 403/Anubis при перевірці.
