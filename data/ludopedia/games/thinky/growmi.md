---
title: Growmi
slug: growmi
aka: []
family: thinky
also: [grid-platformer]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: collect
year: 2023
platforms: [web]
links:
  - {kind: itch, url: "https://carlospedroso.itch.io/growmi", best: true, note: "грати в браузері; керування (WASD / стрілки, Space — зменшитись після здобуття сили, R, U / Z, M — мапа); коментарі: «Snakebird + metroidvania», батареї, діаманти, бонусні зірки"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=Mj6IbDsByoI", note: "офіційне проходження (посилання зі сторінки itch)"}
  - {kind: play, url: "https://www.crazygames.com/game/growmi", note: "CrazyGames: «слиз, що в повітрі може рухатися обмежену кількість разів»; кнопка підказки внизу праворуч; сили й довше тіло з прогресом"}
  - {kind: play, url: "https://poki.com/en/g/growmi", note: "Poki: тягни тіло через прогалини й по стінах; на старті — лише 3 клітини"}
  - {kind: play, url: "https://html-classic.itch.zone/html/7612919/index.html", note: "веб-збірка (C++ / SDL / Emscripten): кімнати Tiled .tmx, world.csv, теги плиток і назви сил витягнуто з неї"}
stage: v1
coverage: 40
mechanics: [move-4dir, move-by-input, keyboard-controls, push-object, gravity-fall, multi-cell-size, impassable-cells, touch-death, button-toggle, undo-step, restart-level, world-map, map-window, save-progress, save-autosave, main-menu, settings-window, game-screen, sound-effects, background-music, movement-animation, +stretchy-body, +anchored-tether-body, +shrink-to-head, +ability-unlock, +sticky-surface, +self-cross-bridge, +color-battery-gates, +orb-gate, +progress-gate, +npc-fetch-quest, +bonus-stars-ending, +room-grid-world, +hint-solution-overlay, +body-length-upgrade]
proposes: ["+cond:anchored", "+effect:change_room", "+ui:body-counter", "+feature:ability-unlock", "+axis:gravity", "+card:anchored-tether-body", "+card:shrink-to-head", "+card:self-cross-bridge", "+card:room-grid-world", "+card:npc-fetch-quest"]
author: opus
date: 2026-11-19
---

# Growmi — слизик тягне тіло від опори клітинка за клітинкою, а з силою «зменшитись» стягує його до голови; світ із 49 кімнат-пазлів

## Суть
Growmi пройшов крізь портал, що забрав усі його сили, і тепер повертає їх у маленькому світі зʼєднаних кімнат. Це платформер-пазл на сітці: Growmi не стрибає, а **тягне тіло** — голова ходить на клітину, за нею росте тіло від опори, але довжина обмежена (на старті 3 клітини, далі більше). Тілом перекидаються мости через прогалини й шипи, ним штовхають ящики й кольорові батареї на кнопки, що відчиняють ворота. Сили на кшталт «зменшитись» (Space), магніту чи орба відкриваються по ходу, як у метроїдванії; зірки в кімнатах відчиняють далі світ, а бонусні — секретну кінцівку.

## Поле і час
- Вигляд збоку з гравітацією; кімната — 13×10 клітин по 32 px (карти Tiled: шари Game, Terrain, Bricks, іноді UnderGame / MiddleGame / AboveGame і Hint).
- Світ — 49 кімнат на сітці 8×13 (`world.csv`); сусідні кімнати зʼєднані отворами на краях, мапа відкривається клавішею M. Кімнати: tutorial ×3, easy ×2, hallway ×16, puzzle, battery, bridge ×2, magnet ×5, fivelock, orb ×4, orbgate ×2, purple ×3, space ×3, bonus ×4, checkpoint, end.
- Тіло — ланцюжок клітин від хвоста-опори (сіра «пружина») до голови з очима; HUD показує рядок квадратиків — довжину тіла (?) (5, 7, 8 на скриншотах).
- Покроково: одна клавіша — крок голови; undo і рестарт діють у межах кімнати.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Growmi (голова) | player | довжина тіла N (на старті 3) | крок у 4 напрямки; тягне за собою тіло; штовхає ящики й батареї |
| Тіло | segment | жовті / блакитні сегменти | лежить від опори до голови; проходить крізь дошки-платформи |
| Хвіст-опора | segment | сіра «пружина» | лишається там, звідки Growmi почав тягнутися (?) |
| Стіна / земля | static | — | непрохідна; опора |
| Дошка-платформа | terrain | ціла / лише ліва / права / обидві частини | тонка полиця; тіло проходить крізь неї (?) |
| Ящик | object | — | штовхається на 1 |
| Батарея червона / фіолетова | object | колір | штовхається; на кнопці свого кольору відчиняє ворота (?) |
| Кнопка червона / фіолетова | switch | колір | керує воротами свого кольору |
| Ворота червоні / фіолетові | gate | колір | зачинені — суцільний блок, відчинені — пунктирний контур |
| Шипи (підлога, стіни, висячі) | hazard | напрям | дотик — смерть (?) |
| Зірка | pickup | — | мета кімнати; лічильник зірок |
| Бонусна зірка | pickup | — | для секретної кінцівки |
| Орб (синя точка) | pickup | 67 у світі | потрібен силі «орб»; як діє — (?) |
| Орб-ворота (синій блок з колом) | gate | — | активуються дотиком із силою орба (?) |
| Хрестовина (плитка зі стрілками на 4 боки) | terrain | — | місце, де тіло може перетнути себе (?); туди можна вкинути батарею |
| Липка поверхня | terrain | бік L / R / U / D | з силою магніту тіло тримається за неї (?) |
| Ворота прогресу / бонусні / фінальні | gate | — | відчиняються зірками (?), бонусними зірками, кінцем гри |
| Мешканці лабіринту (5) | neutral | — | квести: шматки пазла, перлові сережки, діамант; дають нагороди |
| Табличка-урок | mark | — | у кімнаті показує урок: рух, undo, рестарт, батарея, зменшення, магніт, телепорт |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` і `counter(body, <, max_length)` → ТО `move(head, dir)`, `grow(growmi, 1)` — голова тягне тіло від опори.
- КОЛИ `input(dir)` → ЯКЩО `custom: «клітина в напрямку — попередній сегмент тіла»` → ТО `move(head, dir)`, `shrink(growmi, 1)` — «можна повернутися по собі без undo» (?).
- КОЛИ `input(dir)` → ЯКЩО `counter(body, ==, max_length)` → ТО `block` (?).
- КОЛИ `input(space)` → ЯКЩО `has(growmi, shrink_power)` → ТО `shrink(growmi, body)` — тіло стягується до голови (?).
- КОЛИ `after(move)` → ЯКЩО `not supported(growmi)` → ТО `fall(growmi)` (?) — гравітація платформера; ящики й батареї теж падають (?).
- КОЛИ `contact(head, box|battery)` → ЯКЩО `free(cell_behind)` → ТО `push`; інакше `block`.
- КОЛИ `enter(battery, button)` → ЯКЩО `same(battery, button, color)` → ТО `set_state(gate, open)` (?).
- КОЛИ `leave(battery, button)` → ТО `clear_state(gate, open)` (?).
- КОЛИ `contact(growmi, spikes)` → ТО `lose` (?) → undo або рестарт кімнати.
- КОЛИ `contact(head, star)` → ТО `pickup`, `counter(stars, +1)`.
- КОЛИ `counter(stars, >=, N)` → ТО `set_state(progress_gate, open)` (?).
- КОЛИ `contact(growmi, sticky)` → ЯКЩО `has(growmi, magnet_power)` → ТО `custom: «тіло прилипає й тримається, як на опорі»` (?).
- КОЛИ `contact(growmi, orb_gate)` → ЯКЩО `has(growmi, orb_power)` → ТО `set_state(orb_gate, activated)` (?).
- КОЛИ `contact(growmi, npc)` → ЯКЩО `has(growmi, quest_item)` → ТО `message(npc_text)`, `give(growmi, reward)` — сила (зменшення, магніт, орб, телепорт до мешканця) або довше тіло.
- КОЛИ `edge(growmi)` → ТО `custom: «перехід у сусідню кімнату світу»`.
- Перемога: пройти фінальні ворота (звичайна кінцівка); зібрати бонусні зірки — секретна кінцівка. · Поразка: лише в межах кімнати (шипи, глухий кут) → undo / рестарт. · Рахунку нема; лічильник зірок.

## Керування і ввід
- WASD / стрілки — крок голови; Space — зменшитись (після здобуття сили); R — рестарт кімнати; U або Z — undo; M — мапа.
- Мишею — кнопка мапи (вгорі ліворуч) і кнопка підказки «?» (внизу праворуч).
- Тач (CrazyGames, Poki): екранний D-pad і кнопки undo, рестарт, зменшення.

## Вікна, меню, HUD
- Вступ — портал і текст «The brightest one always starts small, prove me right and be the smartest of them all.»
- `main-menu`: Play · Settings · Credits · Quit; скидання прогресу з `confirm-dialog` «Are you sure?».
- `settings-window` — звук і музика.
- `game-screen`: кімната; HUD — кнопка мапи, рядок квадратиків довжини тіла (`+ui:body-counter`), кнопка підказки «?».
- `map-window` — сітка кімнат з маркером, де ти зараз.
- `dialogue-window` — репліки мешканців («Noo! I'm missing the last two pieces of my puzzle!», «I am the shiny gatekeeper. Nobody will pass this gate.»).
- Підказка — шар Hint поверх кімнати: розвʼязок кімнати (є в 19 кімнатах).
- `credits-window`; `end-screen` — текст звичайної кінцівки й окремий текст бонусної.
- Переходи: вступ → main-menu → game-screen ↔ map-window; край кімнати → сусідня кімната; фінальні ворота → end-screen.

## Фічі поза полем
- `undo`, `restart-level` у межах кімнати; `hint` / `show-solution` — розвʼязок кімнати поверх поля.
- `world-map` + сили як ключі (`+feature:ability-unlock`): зменшення, магніт, орб, телепорт до мешканця («Use this whenever you want to come back to visit me»); довжина тіла росте з прогресом.
- `collectibles`: зірки, бонусні зірки, предмети квестів; дві кінцівки.
- `autosave` у localStorage браузера (заблоковані cookies — повідомлення, що прогрес не збережеться); скидання прогресу.
- `touch-controls` на мобільних порталах.

## Варіації й родичі
- [Snakebird](snakebird.md) — тіло з гравітацією, але рухається чергою; тут тіло росте від опори (гравці: «Snakebird + metroidvania», «sentient Tetris piece»).
- [BoxBoy!](../grid-platformer/boxboy.md) — видавлює з себе ланцюжок коробок; [Soliquid](soliquid.md) — тіло тягнеться до трьох клітин; [GRAB-O](grab-o.md) — кінцівки тягнуться клітинками; [Handshakes](handshakes.md) — руки з бюджетом довжини.
- **Осі варіацій:** тіло — черга (Snakebird) / росте від опори (тут) · довжина — стала / росте з прогресом (тут) · як стиснутись — крок назад / сила «зменшитись» / ніколи · світ — список рівнів / сітка кімнат з мапою (тут).

## Цікавинки для курсу
- Тіло, що росте від опори з бюджетом довжини, і крок назад як скорочення — 🥉.
- Стиснути тіло до голови й потім застосувати гравітацію до всього — 🥈 (порядок: стиснення → перевірка опори → падіння).
- Кольорові батареї, кнопки й ворота — 📎.
- Світ із CSV-сітки кімнат, переходи через краї, мапа з маркером — 🥉.
- Сили-ключі метроїдванії, що відкривають нові дії в старих кімнатах — 📎.
- Квести мешканців: принеси предмет — отримай силу — 🌱.

## Мапа на каталог
- Є: `move-4dir` + `move-by-input` + `keyboard-controls`; `push-object` ↔ ящики й батареї; `gravity-fall`; `multi-cell-size` ↔ тіло на кілька клітин; `impassable-cells`; `touch-death` ↔ шипи; `button-toggle` ↔ батарея на кнопці й ворота; `undo-step`, `restart-level`; `world-map` + `map-window` ↔ сітка кімнат і мапа; `save-progress` + `save-autosave`; `main-menu`, `settings-window`, `game-screen`, `sound-effects`, `background-music`, `movement-animation`.
- **Нема** → пропозиції карток:
  - `+stretchy-body` (вже пропонована Soliquid) — тіло тягнеться за рухом.
  - `+anchored-tether-body` «Тіло росте від закріпленого хвоста» · entities/move · 🥉 · слот {max_length: N}.
  - `+shrink-to-head` «Стиснути тіло до голови» · entities/move · 📎.
  - `+ability-unlock` «Сила-ключ відкриває нову дію» · levels/progression · 📎.
  - `+sticky-surface` «Липка поверхня тримає тіло» · entities/interact · 📎.
  - `+self-cross-bridge` «Клітина, де тіло може перетнути себе» · entities/legality · 📎.
  - `+color-battery-gates` «Кольорові батареї на кнопках свого кольору» · entities/interact · 📎 (дитина `button-toggle`).
  - `+orb-gate` «Ворота, що відкриває зібране / сила» · entities/interact · 🌱.
  - `+progress-gate` «Ворота за кількість зірок» · levels/progression · 🌱.
  - `+npc-fetch-quest` «Принеси предмет мешканцю — отримай нагороду» · levels/progression · 🌱.
  - `+bonus-stars-ending` «Секретна кінцівка за бонусні зірки» · game-logic/win · 🌱.
  - `+room-grid-world` «Світ — сітка кімнат, перехід через край» · levels/progression · 🥉.
  - `+hint-solution-overlay` «Підказка малює розвʼязок поверх кімнати» · interface/hud · 🌱.
  - `+body-length-upgrade` «Нагорода — довше тіло» · entities/state · 🌱.

## Пропозиції до словників
- `+cond:anchored` — тіло чи кінцівка закріплені за опору (хвіст Growmi).
- `+effect:change_room` — перехід у сусідню кімнату світу через край поля.
- `+ui:body-counter` — рядок квадратиків: довжина тіла / лишок.
- `+feature:ability-unlock` — сили, що відкривають нові дії (метроїдванія).
- `+axis:gravity` — `down`: гравітація діє на тіло, ящики й батареї (?).
- `+card:anchored-tether-body`, `+card:shrink-to-head`, `+card:self-cross-bridge`, `+card:room-grid-world`, `+card:npc-fetch-quest` — див. «Мапа на каталог».

## Джерела
- ⭐ [itch: Growmi](https://carlospedroso.itch.io/growmi) — опис («Start small and grow big»), керування, автори (Carlos Pedroso, Inês Ribeiro — bedbed), девлог 22.03.2023, коментарі (батарея в «four-way», «self-cross», діаманти, бонусні зірки, «go back on yourself without undoing», «sentient Tetris piece»).
- [YouTube: офіційне проходження](https://www.youtube.com/watch?v=Mj6IbDsByoI).
- [CrazyGames](https://www.crazygames.com/game/growmi) — «a slime that can only move a limited number of times when off the ground», кнопка підказок, «unlock more abilities and a longer Growmi».
- [Poki](https://poki.com/en/g/growmi) — «stretch your body to cross wide gaps, scale walls», «at the beginning, you can only move 3 spaces any direction».
- [Веб-збірка](https://html-classic.itch.zone/html/7612919/index.html) — `world.csv` (49 кімнат), карти `.tmx` 13×10, теги плиток `Game.tsx` (player, box, goal, bridge, battery, button, gate, батареї / кнопки / ворота фіолетові, orb, orbGate, spikes, platform, progressGate, endGate, bonusGate, npc1–5), рядки коду (`shrinkAbility`, `magnetAbility`, `orbAbility`, `checkpointAbility`, `bodyIncreased`, `starCount`, репліки мешканців, назви кімнат «Self Cross», «Safe Fall», «Bridge Builder», «Spike-walker»).

## Непевне
- (?) Точна модель руху: чи тіло завжди росте від опори, чи на землі Growmi повзе цілим; CrazyGames каже про обмеження ходів саме «в повітрі».
- (?) Що робить Space: стягує тіло до голови чи хвіст підтягується до голови, і що далі — падіння.
- (?) Хрестовина як місце самоперетину — за назвою кімнати «Self Cross», плиткою зі стрілками й скриншотом; у грі не перевірено.
- (?) Як діють орби й чому частина тіла й лічильника стає блакитною; як працюють магніт і липкі поверхні.
- (?) Чи батарея тримає ворота відчиненими лише поки стоїть на кнопці; чи шипи вбивають від будь-якого дотику.
- (?) Скільки зірок треба для воріт прогресу.
- (?) Рік 2023 — девлог 22.03.2023; CrazyGames дає березень / квітень 2023, Poki — червень 2023.
