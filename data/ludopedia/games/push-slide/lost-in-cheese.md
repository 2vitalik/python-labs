---
title: Lost in Cheese
slug: lost-in-cheese
aka: [Загублені в сирі]
family: push-slide
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2026
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2341100/Lost_in_Cheese/", best: true, note: "опис (штовхай сир до великої червоної кнопки, мінімум перекатів, 80+ рівнів), скріншоти, геймплейний трейлер, демо"}
  - {kind: official, url: "https://www.snovittra.com/", note: "сайт студії: Mewton, Roll Island, «as few rolls as possible», нагороди, пресскіт"}
  - {kind: other, url: "https://playtester.io/lost-in-cheese", note: "картка гри: ті самі правила, 80+ рівнів, демо"}
  - {kind: youtube, url: "https://www.youtube.com/@LostinCheeseGame", note: "канал гри (з сайту студії)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Lost+in+Cheese+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [move-4dir, keyboard-controls, push-object, impassable-cells, button-toggle, reach-exit, move-counter, item-pickup, restart-level, level-select, level-unlock, avatar-picker, save-progress, movement-animation, +roll-block, +star-thresholds, +optional-collectibles, +hub-world, +npc-dialogue-hints]
proposes: ["+effect:tip", "+feature:roll-par", "+window:barbershop", "+card:roll-par"]
author: opus
date: 2026-11-19
---

# Lost in Cheese — кіт-кубик котиться островом, розштовхує сирні блоки й дістається великої червоної кнопки за мінімум перекатів

## Суть
Затишна 3D-головоломка на сітці: Mewton — кіт у формі кубика — подорожує островами Roll Island. У кожному рівні дорогу до **великої червоної кнопки** загороджують кубики сиру: їх треба розштовхати так, щоб прокласти шлях. Кожен хід — **перекат** кота на сусідню клітинку; що менше перекатів, то більша нагорода (три пороги), а нагороди відкривають нові рівні й світи. Між рівнями — хаб-острови з NPC-друзями, що дають натяки на таємницю сиру, і перукарня для зміни вигляду кота. 80+ рівнів.

## Поле і час
- Квадратна сітка кам'яних плиток з парканами по краях; рендер — 3D з камерою під кутом. Є підняті кам'яні блоки, дерев'яні містки, решітки, чорні діри, плитки зі стрілками (кадри трейлера).
- Хід = один перекат кота; лічильник перекатів угорі заповнює смугу з трьома порогами (наприклад, 14 / 18 / 30 перекатів на одному рівні).
- Без вводу нічого не відбувається (у Steam: «Playable without Timed Input»).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Mewton (кіт-кубик) | player | вигляд із перукарні | котиться на сусідню клітинку; штовхає сир |
| Кубик сиру | object | — | штовхається; загороджує дорогу |
| Велика червона кнопка | static | — | ціль рівня: кіт на ній — рівень пройдено |
| Кольорова кнопка (зелена, синя) | switch | колір | натискається перекатом на неї; опускає місток / відкриває прохід (?) |
| Решітка | gate | колір (світиться) | пара до кнопки того ж кольору (?) |
| Місток | terrain | опущений / піднятий | «roll over to the shiny button… to lower the bridge» |
| Кам'яний блок, паркан | static | — | непрохідні |
| Чорна діра | hazard | — | (?) поведінку не бачив |
| Плитка зі стрілками | terrain | напрям | (?) поведінку не бачив |
| Монета | pickup | — | збирається на рівні |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(mewton, dir)`, `rotate(mewton, 90)` (перекат кубика), `counter(rolls, +1)`.
- КОЛИ `input(dir)` → ЯКЩО `custom: «попереду паркан, кам'яний блок чи край»` → ТО `block` (?).
- КОЛИ `contact(mewton, cheese)` → ЯКЩО `free(cell_behind)` → ТО `push`, `move(mewton, dir)`; інакше `block`.
- КОЛИ `enter(mewton, coin)` → ТО `pickup`, `currency(+1)`.
- КОЛИ `enter(mewton, button)` → ТО `custom: «опускає місток / відкриває прохід свого кольору»` (?).
- КОЛИ `enter(mewton, red_button)` → ТО `win`, `custom: «нагорода за перекати: 1–3 значки за порогами»`.
- КОЛИ `input(restart)` → ТО `restart`, `counter(rolls, 0)`.
- Перемога: кіт на великій червоній кнопці. · Поразка: (?) — видно лише рестарт. · Рахунок: кількість перекатів проти трьох порогів; плюс монети й жетони.

## Керування і ввід
- Напрямки — перекат кота (клавіатура або геймпад, повна підтримка контролера); R — рестарт (кнопка на екрані).
- У хабі кіт ходить вільно; E — далі в діалозі (видно на скріншоті); у перукарні — сітка образів.

## Вікна, меню, HUD
- `game-screen` — рівень; HUD: смуга перекатів з трьома порогами-значками (`par-moves` + `move-counter`), лічильники значків-котів і жетонів-лапок, кнопка Restart.
- `map-window` / хаб — острови з будинками й порталами світів; на порталі — «зібрано / всього» значків і жетонів.
- `level-select` — картки рівнів світу (3-1, 3-2…) з трьома значками; замкнені потребують N значків («Unlock new levels»).
- `dialogue-window` — розмови з NPC (Parrot, Inventor Cat, Cheddarson) з натяками на таємницю сиру.
- `+window:barbershop` — перукарня: вибір вигляду кота (частина замкнена).
- Переходи: хаб → портал світу → вибір рівня → рівень → (кнопка) нагорода → вибір рівня.

## Фічі поза полем
- `+feature:roll-par` — 1–3 значки за перекати; значки відкривають рівні й світи (`level-unlock`).
- `collectibles` — монети й жетони на рівнях; `unlockables` — образи кота.
- `restart-level`; undo не видно на скріншотах (?).
- `save-progress` («Save Anytime»), `achievements` (29: «Pawprint on …» за світи, «Clever Cat», «Brie-lliant Mind»), `localization` (9 мов), `gamepad-support`, налаштування екрана (вікно / повний екран, FPS, VSync — з патча демо).

## Варіації й родичі
- Осі варіацій «котитися й штовхати»:
  - **тіло**: кубик 1×1×1 (тут, [Billy Bumbum](billy-bumbum.md)) / брусок 1×1×2 ([Bloxorz](bloxorz.md), [Bloxpath](bloxpath.md));
  - **мета**: стати на кнопку (тут) / упасти в дірку стоячи (Bloxorz) / сісти на ціль потрібною гранню (Billy Bumbum);
  - **рахунок**: нема / пороги за кількість ходів (тут, `move-limit`-родичі).
- Родичі: [Sokoban](sokoban.md) (штовхання), [Billy Bumbum](billy-bumbum.md), [Bloxpath](bloxpath.md).

## Цікавинки для курсу
- Перекат кубика + штовхання сиру: прокласти шлях до кнопки — 📎.
- Пороги «≤ N перекатів» → 1–3 значки й відкриття рівнів за сумою значків — 🌱.
- Кнопка, що опускає місток / відкриває решітку свого кольору — 🥉 (картка `button-toggle`).
- Хаб з порталами й лічильниками «зібрано / всього» — 🥉.
- BFS для мінімуму перекатів (щоб виставити пороги автоматично) — 🥈.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls`; `push-object` ↔ сир; `impassable-cells` ↔ паркани, блоки; `button-toggle` ↔ кнопка → місток; `reach-exit` ↔ червона кнопка; `move-counter` ↔ лічильник перекатів; `item-pickup` ↔ монети; `restart-level`; `level-select` + `level-unlock`; `avatar-picker` ↔ перукарня; `save-progress`; `movement-animation`.
- **Нема** → пропозиції карток:
  - `+roll-block` (є в корпусі) — тут кубик-кіт.
  - `+star-thresholds` (є в корпусі) — пороги за перекати замість очок.
  - `+optional-collectibles`, `+hub-world` (є в корпусі).
  - `+npc-dialogue-hints` «NPC у хабі дають натяки» · interface/menus · 🌱.
  - `+roll-par` «Нагорода за кількість ходів, що відкриває рівні» · game-logic/score · 🌱.

## Пропозиції до словників
- `+effect:tip` — перекид кубика через ребро (повтор; `roll` у словнику — інше).
- `+feature:roll-par` — 1–3 значки за кількість ходів, значки — валюта відкриття рівнів.
- `+window:barbershop` — магазин-гардероб вигляду персонажа без грошей (за прогрес).
- `+card:roll-par` — див. «Мапу на каталог».

## Джерела
- ⭐ [Steam: Lost in Cheese](https://store.steampowered.com/app/2341100/Lost_in_Cheese/) — опис («Push cheese and clear the path to the big red button», «least rolls possible to be rewarded», 80+ рівнів, монети й жетони, перукарня), 6 скріншотів і геймплейний трейлер (смуга перекатів, кнопки, решітки, містки, хаб, вибір рівнів, перукарня, діалог «roll over to the shiny button… to lower the bridge»), 29 досягнень, Steam News (демо 2025, бета, реліз 21 травня 2026).
- [Сайт SnøVittra](https://www.snovittra.com/) — «cube shaped cat», Roll Island, «as few rolls as possible», нагороди, пресскіт, канал YouTube.
- [Playtester.io](https://playtester.io/lost-in-cheese) — ті самі правила.

## Непевне
- (?) Чи важить орієнтація кота (як у Billy Bumbum) — у джерелах лише «roll» як назва ходу.
- (?) Поведінку чорних дір, плиток зі стрілками, решіток і кольорових кнопок видно лише на кадрах; правил не бачив.
- (?) Чи є undo і чи можна програти (впасти, застрягти) — на екрані лише Restart.
- (?) Рядок черги: «штовхає сир до кнопки» — за описом кіт сам іде до кнопки, а сир прибирає з дороги.
