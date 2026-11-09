---
title: The Snake Is the Tower
slug: the-snake-is-the-tower
aka: [TSITT]
family: maze-arcade
also: [tower-lanes]
klass: avatar
axes:
  field: free
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: survive
year: 2026
platforms: [Windows (Steam, Early Access), web (itch.io)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2957070/", best: true, note: "сегменти-гармати, злиття сусідніх Tier 1→4, захист яйця, реліквії, сітка навичок"}
  - {kind: itch, url: "https://happydistractionsstudio.itch.io/tsitt", note: "браузерне демо, типи веж, коментарі гравців і автора"}
  - {kind: other, url: "https://happydistractionsstudio.itch.io/tsitt/devlog/1522101/first-boss-fight-player-profiles-sharper-pacing", note: "девлог: ліміт сегментів, Reactor/Surge, Singularity, HP яйця, бос з Rage Meter"}
  - {kind: other, url: "https://happydistractionsstudio.itch.io/tsitt/devlog/1484164/patch-notes-march-24-to-april-8-2026", note: "девлог: 27 хвиль світу 1, смуги, орби за таймером, пул вузлів, складності"}
  - {kind: other, url: "https://happydistractionsstudio.itch.io/tsitt/devlog/1357058/demo-patch-1", note: "девлог: стіна й власне тіло — відскок замість смерті"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=The+Snake+Is+the+Tower", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [move-auto, body-queue, self-collision, item-pickup, inventory-limit, tile-merge, enemy-waves, enemy-reached-base, hp-damage, status-effects, drop-on-death, run-relics, in-round-upgrades, level-select, difficulty-levels, +body-turrets, +merge-tiers, +support-aura, +hybrid-merge, +boss-rage-meter, +spawn-warning]
proposes: ["+card:body-turrets", "+card:merge-tiers", "+card:support-aura", "+trigger:breach", "+window:draft-window", "+window:skill-tree", "+ui:base-hp"]
author: opus
date: 2026-11-09
---

# The Snake Is the Tower — змія-мати захищає яйце: кожен сегмент тіла — гармата, сусідні однакові зливаються

## Суть
Гравець веде змію, чиє тіло — батарея веж: кожен новий сегмент сам стріляє (лазер, гармата, ракети, уповільнення, щит, вибух площею). Хвилі «космічних загарбників» ідуть смугами до яйця, і змія мусить бути там, де тиск. Сусідні однакові сегменти автоматично зливаються в старший рівень (Tier 1 → 4), опорні вежі підсилюють сусідні бойові — тому важить не лише довжина, а й порядок сегментів у тілі. Межова гра сімʼї: рух вільний (мишею до курсора), клітинним є «шар тіла» — ланцюжок слотів, що працює як 2048 у лінію.

## Поле і час
- Арена з неоновою сіткою, що «прогинається» від ударів; вороги ходять смугами з напрямними плитками, смуги підсвічуються перед появою, є маркери ворогів поза екраном.
- Змія рухається безперервно, керування — миша (голова йде до курсора), клавіатура або геймпад.
- Тіло — послідовність слотів з лімітом сегментів; порожні слоти не підбирають орбів.
- Real-time; хвилі з паузами між ними (час на злиття). Світ 1 — 3 секції, 27 хвиль і бос; у ранньому доступі — 3 світи, 16 секцій.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Змія-мати (голова) | player | ліміт сегментів | рухається до курсора; від стін і власного тіла відскакує |
| Сегмент-вежа | ally | тип, Tier 1–4 | сам стріляє по ворогах; зливається з однаковим сусідом |
| Опорна вежа (Reactor, Surge) | ally | — | підсилює обмежену кількість сусідніх веж |
| Singularity | ally | — | шкодить і втягує ворогів; ставиться туди, де їх найбільше |
| Chill | ally | — | уповільнює ворогів (морозний відтінок) |
| Яйце | container | HP (плаваюча смуга) | ціль ворогів; HP 0 — поразка |
| Орб | pickup | зʼявляється за таймером | заповнює вільний слот тіла сегментом |
| Ворог (рій) | enemy | тип; Bruiser — 10 шкоди яйцю | іде смугою до яйця; розлітається від влучань |
| Бос світу 1 | boss | фази, Rage Meter | невразливий під час появи; кличе поміч зі своєї смуги |
| Валюта | resource | ≈25 % хвилі | випадає з ворогів, для апгрейдів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(steer)` → ТО `face(snake, cursor)`; КОЛИ `tick` → ТО `move(snake, facing)`, `custom: «тіло повторює шлях голови»`.
- КОЛИ `blocked(snake)` → ТО `bounce(snake)` — стіна без шкоди; КОЛИ `contact(snake_head, own_body)` → ТО `bounce(snake)` (з Demo Patch 1; раніше — смерть).
- КОЛИ `timer(orb_interval)` → ТО `spawn_at(orb, playable_area)`.
- КОЛИ `contact(head|segment, orb)` → ЯКЩО `custom: «є вільний слот у межах ліміту»` → ТО `transform(slot, tower)` — тип з пулу забігу (3 бойові + 2 опорні).
- КОЛИ `tick` → ТО `custom: «кожна вежа сама стріляє по ворогах у своєму радіусі»`.
- КОЛИ `adjacent(tower_a, tower_b)` → ЯКЩО `same(tower_a, tower_b, type_and_tier)` → ТО `merge(tower_a, tower_b, tier+1)` — до Tier 4.
- КОЛИ `adjacent(tower_a, tower_b)` → ЯКЩО `custom: «пара з гібридного рецепта»` → ТО `merge(tower_a, tower_b, hybrid)` (кулі + мороз → морозні міни, зі слів гравця (?)).
- КОЛИ `adjacent(support, tower)` → ТО `custom: «бафф обмеженій кількості сусідніх веж»`.
- КОЛИ `contact(chill_shot, enemy)` → ТО `set_state(enemy, slowed, dur)`; Singularity — `pull(enemy)`.
- КОЛИ `wave_start` → ТО `spawn_at(enemies, lane)` з поетапним попередженням.
- КОЛИ `reach(enemy, egg)` → ТО `damage(egg, n)`, `disappear(enemy)` (?).
- КОЛИ `hp_zero(egg)` → ТО `lose`.
- КОЛИ `destroyed(enemy)` → ЯКЩО `prob(25)` → ТО `spawn(currency)`.
- КОЛИ `destroyed(boss_minion)` → ТО `counter(rage, +1)`; КОЛИ `counter(rage, ==, max)` → ТО `custom: «бос обирає смугу й повзе до яйця»`.
- КОЛИ `wave_cleared` → ТО `choose(node | relic)` (?) — пропозиції з пулу забігу; щойно пропоновані випадають рідше.
- Перемога: пережити хвилі секції / убити боса. · Поразка: яйце зруйноване. · Рахунок: тег Score Attack, деталі (?).

## Керування і ввід
- Миша (змія повзе до курсора) або клавіатура/геймпад; повна підтримка геймпада в меню й драфтах.
- Утримання кнопки — «pickup» з індикатором: підібрати вежу (?).

## Вікна, меню, HUD
- `main-menu`: створення профілю гравця; мета-прогрес зберігається в профіль.
- `level-select`: вибір світу (2–4 ще закриті), список складності Easy / Medium / Hard.
- `game-screen`: арена, змія, смуги; HUD — `hp-bar` яйця над ним, зірки рівня веж, `spawn-indicator` смуг і маркери поза екраном, підказки (`tooltip`).
- `custom-window` → `+window:draft-window`: вибір вузлів/реліквій під час забігу.
- `custom-window` → `+window:skill-tree`: «skill matrix» — клітини постійних бонусів між забігами, «philosophies».
- Переходи: main-menu → level-select → game-screen ⇄ драфт → (кінець) skill-tree.

## Фічі поза полем
- `meta-progression`: сітка навичок (~100 вузлів), розблокування зброї й стилів між забігами; `difficulty-presets` (Easy / Medium / Hard); профілі гравців; `gamepad-support`.
- Перед забігом — набір: 6 зброй дальнього бою, 3 стилі ближнього, 9 пасивок; у забігу — драфт ~20 реліквій, що живляться злиттям веж.

## Варіації й родичі
- Родичі в сімʼї: [`snake`](snake.md) (тіло-черга), [`nimble-quest`](nimble-quest.md) (кожен сегмент — герой, що атакує сам), [`slither-io`](slither-io.md) (вільний рух змії до курсора).
- Родичі поза сімʼєю: [`random-dice`](../tower-lanes/random-dice.md) і [`merge-tactics`](../tower-lanes/merge-tactics.md) (злиття однакових веж у старший рівень), [`2048`](../falling-match/2048.md) (злиття сусідніх рівних у ряду).
- Осі варіацій «де стоять вежі»: на клітинах поля (TD) / у тілі аватара, що рухається (TSITT, Nimble Quest). «Що зливається»: плитки поля (2048) / кубики на дошці (Random Dice) / сусідні сегменти тіла (TSITT).

## Цікавинки для курсу
- Тіло змії як масив слотів-веж: кожен сегмент стріляє сам — 🥉.
- Злиття сусідніх однакових сегментів у тілі з каскадом (новий Tier може злитися з наступним) — 🥉 (2048 у лінію).
- Опорна вежа з аурою на N сусідів — 📎.
- Яйце з HP і смуги ворогів з попередженням про появу — 📎.
- Бос з Rage Meter: убиті поплічники наповнюють шкалу, на максимумі бос атакує — 🥉.

## Мапа на каталог
- Є: `move-auto` ↔ рух до курсора; `body-queue` ↔ тіло; `self-collision` ↔ відскок від себе; `item-pickup` + `inventory-limit` ↔ орби й ліміт сегментів; `tile-merge` ↔ злиття однакових; `enemy-waves` ↔ хвилі; `enemy-reached-base` + `hp-damage` ↔ HP яйця; `status-effects` ↔ уповільнення; `drop-on-death` ↔ валюта з ворогів; `run-relics` + `in-round-upgrades` ↔ драфт; `level-select` + `difficulty-levels` ↔ світи й складність.
- **Нема** → пропозиції карток:
  - `+body-turrets` «Сегменти тіла — вежі» · entities/combat · 🥉.
  - `+merge-tiers` «Злиття в старший рівень до межі» · entities/legality · 📎 · слот {max_tier: 4} — дитина `tile-merge`.
  - `+support-aura` «Опорна вежа підсилює сусідів» · entities/state · 📎 · слот {targets: n}.
  - `+hybrid-merge` «Злиття різних типів за рецептом» · entities/legality · 🥉.
  - `+boss-rage-meter` «Шкала люті боса від убитих поплічників» · entities/state · 📎.
  - `+spawn-warning` «Попередження про появу на смузі» · interface/hud · 🌱.

## Пропозиції до словників
- `+trigger:breach` — ворог дійшов до бази (тут — до яйця); уже ×3 🔥.
- `+window:draft-window` — вибір з пропозицій під час забігу (уже ×3 🔥); `+window:skill-tree` — сітка постійних апгрейдів (уже ×4 🔥).
- `+ui:base-hp` — HP цілі оборони над нею (уже пропонував Wall World).
- `+card:body-turrets`, `+card:merge-tiers`, `+card:support-aura` — див. вище.

## Джерела
- ⭐ [Steam: The Snake Is the Tower](https://store.steampowered.com/app/2957070/) — концепція «тіло з гармат», злиття Tier 1→4, яйце, реліквії, сітка навичок, теги, ранній доступ з 21.08.2026.
- [itch.io: TSITT](https://happydistractionsstudio.itch.io/tsitt) — демо (HTML5 і Windows), типи веж, орби «жадібність проти безпеки», коментарі.
- [Девлог: First Boss Fight](https://happydistractionsstudio.itch.io/tsitt/devlog/1522101/first-boss-fight-player-profiles-sharper-pacing) — ліміт сегментів, опорні вежі, Singularity, HP яйця, бос з Rage Meter, профілі.
- [Девлог: Patch Notes 24.03–08.04.2026](https://happydistractionsstudio.itch.io/tsitt/devlog/1484164/patch-notes-march-24-to-april-8-2026) — 27 хвиль, смуги, орби за таймером, валюта ≈25 %, пул 3+2 вузлів, складності.
- [Девлог: Demo Patch 1](https://happydistractionsstudio.itch.io/tsitt/devlog/1357058/demo-patch-1) — стіни й власне тіло: відскок замість смерті.
- YouTube: пошук «The Snake Is the Tower».

## Непевне
- (?) «Сусідні» — сусіди в тілі змії чи вежі, поставлені поруч на полі: девлоги згадують «розміщення веж», «вежу поза своєю територією» й утримання для «pickup» — можливо, сегменти можна скидати на поле й підбирати знову.
- (?) Скільки однакових треба для злиття (2 чи 3) і чи злиття ланцюгове.
- (?) Чи є «територія» гравця як механіка (опис гри на itch: «snake territory defense hybrid»).
- (?) Рух вільний чи по клітинах сітки — `field: free` за керуванням мишею й «протисканням у вузькі щілини».
- (?) Що дає драфт після хвилі (вузли, реліквії) і як рахуються очки.
