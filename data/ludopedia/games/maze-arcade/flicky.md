---
title: Flicky
slug: flicky
aka: [Фліккі, フリッキー]
family: maze-arcade
also: [grid-platformer]
klass: avatar
axes:
  field: free
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: collect
year: 1984
platforms: [arcade, SG-1000, MSX, Sega Genesis]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Flicky", best: true, note: "Chirps-ланцюжок, Tiger та Iggy, предмети для кидка, бонус-раунд, 48 рівнів, порти"}
  - {kind: other, url: "https://www.arcade-history.com/game/862/", note: "6/8 Chirps на раунд, контакт з котом = життя, Perfect у бонус-раунді, 2-way джойстик"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=flicky+arcade+gameplay", note: "пошук; геймплей аркади"}
stage: v1
coverage: 60
mechanics: [body-queue, item-pickup, collect-all, reach-exit, touch-death, player-death, wrap-edges, player-camera, gravity-fall, chase-player, random-walk, projectile-shot, event-points, escalating-kill-points, extra-life-threshold, sequential-levels, score-records, attract-demo, +follower-chain, +group-delivery-bonus, +chain-break-on-touch, +jump-to-throw, +catch-bonus-round, +difficulty-loop]
proposes: ["+effect:detach_all", "+trigger:chain_delivered", "+role:follower", "+card:follower-chain", "+card:group-delivery-bonus", "+card:catch-bonus-round", "+feature:difficulty-loop"]
author: opus
date: 2026-11-09
---

# Flicky — збери пташенят у ланцюжок за собою і доведи їх до дверей, поки коти не розірвали вервечку

## Суть
Пташка Flicky бігає ліворуч-праворуч і стрибає платформами екрана, що замикається по горизонталі. Торкнувшись пташеняти-Chirp, вона чіпляє його в хвіст ланцюжка; довести всіх до дверей «FLICKY» — пройти раунд. Коти Tiger розривають ланцюжок дотиком і вбивають Flicky; Iggy-ігуани додають тиску. Ядро — «змійка» з хвостом, який можна загубити, і бонус за велику групу, доставлену за раз.

## Поле і час
- Один рівень — замкнений по горизонталі екран (тор по X) з платформами на кількох висотах і дверима-виходом; камера тримає Flicky в центрі й прокручує поле.
- Рух вільний (піксельний), з гравітацією: стрибок вгору на платформу, падіння вниз крізь край.
- Real-time; 48 раундів, після останнього гра циклічно повторюється на вищій складності.
- Кожен четвертий раунд — бонус-раунд (ловля пташенят сіткою).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Flicky | player | життя | біг ліворуч/праворуч, стрибок; тягне ланцюжок Chirps |
| Chirp | object | вільний / у ланцюжку | вільний — блукає; торкнутий — чіпляється в хвіст і повторює шлях |
| Chirp у окулярах | object | — | розсипаний — поводиться непередбачуваніше (біжить геть) |
| Двері FLICKY | static | — | ланцюжок, що дійшов, зараховується і зникає |
| Tiger (кіт) | enemy | — | переслідує Flicky; дотик до Flicky — смерть, до ланцюжка — розсипає його |
| Iggy (ігуана) | enemy | — | повзає платформами; дотик — як у кота (?) |
| Предмет (телефон, вазон, чашка, пляшка, молоток) | pickup | одноразовий | береться дотиком, летить при стрибку, збиває ворогів |
| Діамант | pickup | — | бонусні очки; кинути не можна |
| Платформа | static | — | опора; Flicky стрибає на неї знизу |
| Кіт на гойдалці (бонус-раунд) | neutral | — | підкидає Chirps у повітря |
| Сітка (бонус-раунд) | player | — | ловить падаючі Chirps |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ТО `move(flicky, dir)`; КОЛИ `input(jump)` → ЯКЩО `supported(flicky)` → ТО `custom: «стрибок вгору»`.
- КОЛИ `tick` → ЯКЩО `not supported(flicky)` → ТО `fall(flicky)`.
- КОЛИ `edge(flicky)` → ТО `wrap(flicky)` (горизонталь).
- КОЛИ `contact(flicky, chirp)` → ЯКЩО `not state(chirp, chained)` → ТО `attach(chain_tail, chirp)`, `set_state(chirp, chained)`.
- КОЛИ `tick` → ТО ланцюжок: `custom: «кожен Chirp повторює шлях попереднього з затримкою»` (`body-queue`).
- КОЛИ `contact(chain, door)` → ТО `disappear_a` (усі Chirps ланцюжка), `score(f(n))` — бонус зростає з кожним наступним у групі.
- КОЛИ `contact(enemy, chirp)` → ЯКЩО `state(chirp, chained)` → ТО `custom: «ланцюжок розсипається — усі Chirps відчіплюються й розбігаються»` (`+effect:detach_all`).
- КОЛИ `contact(flicky, tiger)` → ТО `lose` (мінус життя).
- КОЛИ `contact(flicky, iggy)` → ТО `lose` (?).
- КОЛИ `contact(flicky, item)` → ТО `pickup`; КОЛИ `input(jump)` → ЯКЩО `has(flicky, item)` → ТО `throw(item, facing)`.
- КОЛИ `contact(item_thrown, enemy)` → ТО `disappear_b`, `score(n)`; ЯКЩО `chain(2)` (той самий предмет збив ще одного) → ТО `spawn(diamond)`.
- КОЛИ `contact(flicky, diamond)` → ТО `pickup`, `score(bonus)`.
- КОЛИ `all_gone(chirp)` → ТО `next_level`.
- КОЛИ `tick` → ТО Tiger: `custom: «рух до Flicky платформами, стрибки»` (`chase-player`); вільний Chirp: `move(chirp, rng_dir)`.
- Бонус-раунд: КОЛИ `contact(net, chirp_falling)` → ТО `pickup`, `score(n)`; КОЛИ `all_gone(chirp_falling)` → ЯКЩО `count(caught, ==, all)` → ТО `score(perfect)`.
- КОЛИ `counter(score, >=, threshold)` → ТО `lives(+1)`.
- КОЛИ `counter(lives, ==, 0)` → ТО `game_over`.
- Перемога: нема — рекорд (48 раундів по колу). Поразка: скінчились життя. Рахунок: Chirps × груповий бонус, збиті вороги, діаманти, бонус-раунд, Perfect.

## Керування і ввід
- Джойстик на 2 напрямки (ліво/право) + одна кнопка: стрибок; та сама кнопка кидає предмет, якщо він у руках.
- Ланцюжок керується лише непрямо — маршрутом Flicky.

## Вікна, меню, HUD
- `attract-demo` — демо-раунд, титул.
- `game-screen` — прокручуване поле; `score`, `hi-score`, `lives`, `level-number` (раунд).
- `custom-window` бонус-раунду — гойдалки й сітка, лічильник спійманих, напис «Perfect».
- `leaderboard` — рекорди з ініціалами (?).
- `end-screen` — GAME OVER → атракт.
- Переходи: атракт → (монета, Start) → раунд → (усі Chirps удома) наступний раунд / кожен 4-й — бонус → … → (0 життів) GAME OVER.

## Фічі поза полем
- `levels-sequential` 48 раундів + `difficulty-loop`: після 48-го гра йде по колу з вищою складністю.
- `operator-settings` — 8 DIP-перемикачів (зміст не бачив).
- 2 гравці по черзі (`hotseat`) (?).

## Варіації й родичі
- **SG-1000** — 40 рівнів, частина перебудована, нема Iggy, змінена поведінка Chirps; **Genesis** (1991) — близький порт; включення в Sega-збірки.
- Механіку «збирай тварин-хвіст і доставляй» успадкував **Sonic 3D Blast** (1996): Flickies-птахи слідують за Соніком до кільця-виходу.
- Родичі: Snake/Nibbler (хвіст = шлях голови, але тут хвіст — цінність, а не загроза), Libble Rabble, Ice Climber (платформи), Mario Bros. (однокімнатний платформер з тором), Pikmin, Lemmings-«конвой».
- **Осі варіацій:** ланцюжок (жорсткий / розсипається від дотику / Chirps тікають) · доставка (будь-коли / групою з бонусом за розмір) · захист (нема / предмети для кидка) · поле (екран / тор / прокрутка).

## Цікавинки для курсу
- Хвіст-ланцюжок за аватаром як цінний вантаж (`body-queue` навпаки) — 📎.
- Розсипання ланцюжка від дотику ворога: хвіст рветься, Chirps розбігаються — 🥉 (стан кожного елемента + повторне збирання).
- Бонус, що зростає з розміром групи, доставленої за раз — 🌱 (ризик: довший ланцюжок = більша мішень).
- Кинути взятий предмет стрибком; збити кількох одним кидком → діамант — 📎.
- Тор по горизонталі з камерою по центру — 📎 (обгортка координат + рендер з двох боків).
- Бонус-раунд ловлі як окрема міні-гра кожні N рівнів — 📎.

## Мапа на каталог
- Є: `body-queue` · `item-pickup` · `collect-all` · `reach-exit` · `touch-death` · `player-death` · `wrap-edges` · `player-camera` · `gravity-fall` · `chase-player` · `random-walk` (вільні Chirps) · `projectile-shot` (кинутий предмет) · `event-points` · `escalating-kill-points` (бонус за групу) · `extra-life-threshold` · `sequential-levels` · `score-records` · `attract-demo`.
- **Нема** → пропозиції карток:
  - `+follower-chain` «Підібрані йдуть хвостом за аватаром» · entities/move · 📎 · слот {gap} — Flicky, Sonic 3D Blast.
  - `+chain-break-on-touch` «Дотик ворога розриває ланцюжок» · entities/interact · 🥉.
  - `+group-delivery-bonus` «Бонус за розмір групи, доставленої разом» · game-logic/score · 🌱 · слот {curve}.
  - `+jump-to-throw` «Кнопка стрибка кидає взятий предмет» · entities/combat · 🌱.
  - `+catch-bonus-round` «Бонус-раунд: ловити падаюче» · levels/progression · 📎 · слот {every}.
  - `+difficulty-loop` «Після останнього рівня — коло на вищій складності» · levels/progression · 🌱.

## Пропозиції до словників
- `+effect:detach_all` — розчепити весь ланцюжок одразу (Flicky; `detach` лише пару).
- `+trigger:chain_delivered` — ланцюжок/вантаж дійшов до приймача (Flicky, Sonic 3D Blast).
- `+role:follower` — сутність, що йде слідом за аватаром (Chirps, Pikmin).
- `+card:follower-chain`, `+card:group-delivery-bonus`, `+card:catch-bonus-round`, `+feature:difficulty-loop` — див. вище.

## Джерела
- ⭐ [Wikipedia: Flicky](https://en.wikipedia.org/wiki/Flicky) — ланцюжок Chirps, Tiger та Iggy, предмети (телефон, вазон, чашка, пляшка), діаманти, бонус за кількох за раз, 48 раундів і цикл, бонус-раунд із сіткою, SG-1000 без Iggy, вплив на Sonic 3D Blast.
- [arcade-history: Flicky](https://www.arcade-history.com/game/862/) — 6 Chirps у перших двох раундах і 8 далі, контакт з котом = життя, кіт відриває Chirp, молоток серед предметів, «Perfect», 2-way джойстик + 1 кнопка, 8 DIP.
- YouTube: пошук «flicky arcade gameplay».

## Непевне
- (?) Шкала групового бонусу «від 100 до 5000 за останнього в групі» — з пошукового фрагмента (Sonic fandom), сторінку не відкрив.
- (?) Бонус-раунд «кожен четвертий», гойдалки з котами — з пошукового фрагмента.
- (?) Старт 3 життя і бонусні на 30 000 / 80 000 / 160 000 — один форумний допис.
- (?) Чи вбиває Iggy так само, як Tiger; чи Iggy розриває ланцюжок; японські імена Nyannyan / Choro / Piopio — з пошукових фрагментів.
- (?) Як саме тікають Chirps в окулярах; очки за збитого ворога.
