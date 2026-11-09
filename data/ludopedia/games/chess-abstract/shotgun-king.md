---
title: "Shotgun King: The Final Checkmate"
slug: shotgun-king
aka: [Shotgun King]
family: chess-abstract
also: [roguelike]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: both
  goal: state
year: 2022
platforms: [PC, macOS, Linux, Switch, PS4, PS5, Xbox One, Xbox Series]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1972440", best: true, note: "ядро: хід королем або постріл, перезарядка ходом; пари карт «тобі + ворогу»; режими"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Shotgun_King:_The_Final_Checkmate", note: "Throne Mode 12 етапів, Endless, Chase; порти 2023"}
  - {kind: itch, url: "https://punkcake.itch.io/shotgun-king", note: "сторінка + changelog: таймери ходів фігур, гранати, folly shields, ALT-приціл"}
  - {kind: other, url: "https://gamepretty.com/shotgun-king-the-final-checkmate-card-review-and-enemy-guide/", note: "огляд карт і ворогів (WIP): HP фігур, Theocracy +2 HP слонам"}
  - {kind: other, url: "https://kosgames.com/?p=22805", note: "базовий гайд: souls для втечі, перезарядка кліком без руху, стратегії «вбий короля»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=shotgun+king+the+final+checkmate+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [piece-move-patterns, move-8dir, shoot-spread, hp-damage, explode-area, status-effects, threat-range, check-stalemate, checkmate, ai-opponent, reinforcements, pawn-promotion, run-relics, in-round-upgrades, permadeath, sequential-levels, difficulty-levels, mode-select, codex-window, achievements-window, game-screen, main-menu, end-screen, settings-window, cell-click, keyboard-controls, controls-remap, +ammo-reload, +enemy-move-timer, +paired-upgrade-choice, +knockback, +extra-life, +mod-support]
proposes: ["+effect:shoot_spread", "+effect:reload", "+effect:knockback", "+cond:ammo", "+trigger:move_timer", "+effect:choose_pair", "+ui:move-timer-badge", "+ui:ammo-counter", "+ui:threat-shield", "+card:ammo-reload", "+card:enemy-move-timer", "+card:paired-upgrade-choice", "+card:knockback"]
author: opus
date: 2026-11-09
---

# Shotgun King — чорний король сам проти білої армії: крок або постріл з дробовика, між поверхами — карта тобі й карта ворогу

## Суть
Гравець — чорний король на шаховій дошці; його армія перейшла до білих, лишився королівський дробовик. Кожного ходу або йде королем (як шаховий король), або стріляє віялом дробу; постріл витрачає набій, перезарядка потребує ходу. Білі фігури ходять за шаховими патернами, мають HP і **таймери ходу**; мета поверху — вбити білого короля, не отримавши мат. Між поверхами — вибір пари карт: апгрейд тобі + посилення ворогу (роглайт-забіг ~20 хв).

## Поле і час
- Шахова дошка 8×8 (?), вид зверху. Король гравця — одна клітина; білі — класичні фігури.
- Покроково: хід гравця (рух / постріл / перезарядка) → білі, чий таймер дійшов, ходять. Темп фігури — її швидкість (кінь і слон — раз на 3 ходи за changelog).
- Забіг = послідовність поверхів; Throne Mode — 12 етапів, далі нові білі фігури додаються з часом.
- Загроза видима: фігура, що б'є клітину короля, — «шах»; хід під удар веде до смерті.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Чорний король | player | набої, вогнева міць, дальність, кут дробу | хід на 1 у 8 напрямків або постріл віялом |
| Дробовик | — | firepower, range, arc, ємність (≤8 набоїв) | постріл = кілька дробин у секторі, шкода по HP |
| Граната | projectile | шкода 3 | вибух площею; може вбити й короля; кидок не витрачає хід (патч) |
| Білий пішак | enemy | HP | шаховий хід; дійшов до краю → перетворення |
| Білий кінь | enemy | HP, таймер 3 | L-хід раз на 3 ходи |
| Білий слон | enemy | HP, таймер 3 | діагональ; Theocracy дає +2 HP |
| Біла тура | enemy | HP | пряма; «замикає» край, бʼє зі звʼязки |
| Білий ферзь | enemy | HP | тура+слон, темп як у тури; зʼявляється з певного поверху |
| Білий король | boss | HP | вбити = поверх пройдено |
| Підкріплення | spawner | — | нові білі фігури за часом / картою |
| Soul | pickup | — | ресурс для втечі (?) |
| Folly shield | — | — | попереджає/блокує постріл, що лишає короля під шахом; Shift-клік ігнорує |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, king, to)` → ЯКЩО `free(to)` і `custom: «to — сусідня клітина»` → ТО `move(king, to)`, `end_turn`.
- КОЛИ `input(shoot, dir)` → ЯКЩО `custom: «є набій»` (`+cond:ammo`) → ТО `custom: «віяло дробин у секторі arc на range»` (`+effect:shoot_spread`), `damage(firepower)` кожній ураженій фігурі, `counter(shells, -1)`, `end_turn`.
- КОЛИ `input(reload)` → ЯКЩО `custom: «магазин не повний»` → ТО `custom: «перезарядка»` (`+effect:reload`), `end_turn` (клік по зброї — без руху).
- Стріляти до кінця перезарядки не можна (changelog).
- КОЛИ `hp_zero(white_piece)` → ТО `disappear_a`.
- КОЛИ `turn_end(player)` → ЯКЩО `custom: «таймер фігури = 0»` (`+trigger:move_timer`) → ТО `move(piece, to)` за шаховим патерном, таймер на початок.
- КОЛИ `state_on(piece, stun)` → ТО `custom: «таймер ходу не тікає»`.
- КОЛИ `move(piece, king_cell)` → ЯКЩО `in_check` → ТО `lose` (мат / взяття короля), крім `extra-life`-карти: `respawn(king, «≈2 клітини поруч»)` раз на поверх.
- КОЛИ `reach(white_pawn, last_row)` → ТО `transform(piece)`.
- КОЛИ `hp_zero(white_king)` → ТО `win` поверху → `window(upgrade-window)`.
- КОЛИ `level_end` → ТО `choose(pairs)` (`+effect:choose_pair`): кожна пара = карта гравцю (чорна) + карта білим (біла); обране діє до кінця забігу.
- КОЛИ `input(grenade, cell)` → ТО `explode(area)`, `damage(3)` усім у зоні, включно з королем.
- Knockback-карта: КОЛИ `damage(piece)` → ТО `custom: «відкинути фігуру»` (`+effect:knockback`) — може поставити її на лінію удару по королю.
- Перемога: пройти всі етапи Throne Mode · Поразка: мат чорному королю (останньому «лідеру») · Рахунок: ранг складності (20 рангів), досягнення.

## Керування і ввід
- Миша: клік по клітині — хід; приціл — напрям пострілу (ALT примусово перемикає на приціл), Enter — постріл; клік по зброї — перезарядка; Shift-клік — ігнорувати folly shield.
- Геймпад (Xbox/PS), Steam Deck; drag-n-drop фігур для карти King's Shoulders.

## Вікна, меню, HUD
- `main-menu`: Story / Throne / Endless / Chase / Charnier → `mode-select`; налаштування → `settings-window`; кодекс → `codex-window`; досягнення.
- `game-screen`: дошка, король, `ammo-counter` (набої), бейджі таймерів ходу на білих (`+ui:move-timer-badge`), HP фігур, `threat-range` / folly shield (`+ui:threat-shield`), анімація «пітніє король» при загрозі.
- `upgrade-window`: дві/три пари карт «тобі + ворогу», частину карт можна перевернути.
- `codex-window`: карти й умови їхньої появи (які білі фігури потрібні).
- `end-screen`: смерть / перемога забігу, ранг; `confirm-dialog` для «здатись».
- Переходи: main-menu → game-screen → (король убитий) upgrade-window → наступний поверх → … → end-screen.

## Фічі поза полем
- `meta-progression`: карти розблоковуються між забігами; 20 рангів складності (`difficulty-presets`), 100+ `achievements`.
- `mode-endless`, Chase (орди фігур), Charnier (рейд королівства), Story; `mod-support`; `localization` (18 мов).
- `permadeath` у межах забігу; `seed`-функцій не видно (?).

## Варіації й родичі
- Сусіди-роглайти «шахові патерни + забіг»: Pawnbarian (опис у сімʼї roguelike), Chess Survivors, The Ouroboros King, Passant, Usurper — див. `queue/chess-abstract.md` «Межові випадки».
- Родичі в корпусі: `chess.md` (патерни й шах), `chess-rule-twists.md` (асиметрія сторін), `tactics/*` (HP і загони), `roguelike/*` (реліквії забігу).
- Осі варіацій: **армія гравця** (одна фігура / набір) · **атака** (взяття ходом / дистанційний постріл з HP) · **темп ворога** (хід після кожного твого / таймер на фігуру / усі разом) · **апгрейди** (лише тобі / парні «тобі + ворогу»).

## Цікавинки для курсу
- Король проти армії з таймерами ходу: черга подій «чий таймер дійшов» — 🥉.
- Віяло дробу на сітці: промені в секторі, перетин з клітинами, розподіл шкоди — 🥈.
- Обчислення «шах»: чи атакує біла фігура клітину короля після її ходу; підсвітка небезпечних клітин — 🥉.
- Набої й перезарядка як ресурс темпу (постріл ↔ хід) — 📎.
- Парні карти «плюс тобі / плюс ворогу» як модифікатори правил на забіг — 🥈 (правила як дані, `run-relics`).
- AI білих: жадібно до клітини, що бʼє короля, з урахуванням таймерів — 🥉.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ білі фігури · `move-8dir` ↔ король · `shoot-spread` ↔ дріб · `hp-damage` ↔ HP фігур · `explode-area` ↔ граната · `status-effects` ↔ оглушення · `threat-range`, `check-stalemate`, `checkmate` ↔ шах/мат королю гравця · `ai-opponent`, `reinforcements` · `pawn-promotion` · `run-relics`, `in-round-upgrades` ↔ карти · `permadeath`, `sequential-levels`, `difficulty-levels`, `mode-select`, `codex-window`, `achievements-window` · `game-screen`, `main-menu`, `end-screen`, `settings-window`, `cell-click`, `keyboard-controls`, `controls-remap`.
- **Нема** → пропозиції карток:
  - `+ammo-reload` «Набої й перезарядка за хід» · entities/combat · 📎 · слоти {capacity, reload: turn|click}.
  - `+enemy-move-timer` «Таймер ходу на ворога» · game-logic/opponent · 🥉 · слоти {period per type} — ворог ходить раз на N ходів, бейдж з лічильником.
  - `+paired-upgrade-choice` «Пара апгрейдів: тобі + ворогу» · game-logic/economy · 🥉 — вибір з N пар між рівнями.
  - `+knockback` «Відкидання від удару» · entities/combat · 📎.
  - `+extra-life` «Друге життя на рівень» · game-logic/lose · 🌱 — відродження поруч.
  - `+mod-support` · code/packaging (?) · 🥈 — завантаження сторонніх карт/правил.

## Пропозиції до словників
- `+effect:shoot_spread` — постріл кількома снарядами-променями в секторі.
- `+effect:reload` — поповнити набої ціною ходу.
- `+effect:knockback` — відкинути сутність від джерела удару на N клітин.
- `+cond:ammo` — є набій для пострілу.
- `+trigger:move_timer` — лічильник ходу сутності дійшов до нуля (вона діє).
- `+effect:choose_pair` — обрати пару «бонус + штраф» (особливий випадок `choose`).
- `+ui:move-timer-badge` — число на ворогу «ходів до його дії»; `+ui:ammo-counter` — набої; `+ui:threat-shield` — попередження про хід під шах.
- `+card:ammo-reload`, `+card:enemy-move-timer`, `+card:paired-upgrade-choice`, `+card:knockback` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Shotgun King](https://store.steampowered.com/app/1972440) — хід або постріл, перезарядка ходом, мат = смерть, вибір з двох пар карт, 20 рангів, Endless/Chase/Charnier, моди, LD50 (1 місце Overall і Fun).
- [Wikipedia](https://en.wikipedia.org/wiki/Shotgun_King:_The_Final_Checkmate) — Throne Mode з 12 етапів, пари «тобі + ворогу» (одна з трьох), анлоки, порти й видавець.
- [itch.io: changelog](https://punkcake.itch.io/shotgun-king) — таймери ходу (кінь і слон раз на 3), оглушення зупиняє таймер, граната 3 шкоди без витрати ходу, ліміт 8 набоїв, folly shields, ALT/Enter/Shift.
- [GamePretty: карти й вороги](https://gamepretty.com/shotgun-king-the-final-checkmate-card-review-and-enemy-guide/) — Theocracy +2 HP слонам, ферзь з темпом тури, карта-воскресіння, knockback, гранати.
- [KosGames: базовий гайд](https://kosgames.com/?p=22805) — souls для втечі, перезарядка кліком по зброї, стратегія «вбий короля рано».

## Непевне
- (?) Розмір дошки (8×8?) і стартовий набір білих на поверсі.
- (?) Пари карт: Steam пише «з двох», Wikipedia — «з трьох пар»; можливо, залежить від версії/рангу.
- (?) Колір карт: гайд називає чорні — бафами гравцю, білі — посиленням ворогу; за назвами логічно, але не перевірено в грі.
- (?) Souls: що саме дають (втеча/телепорт?) — лише одна згадка в гайді.
- (?) Значення HP фігур, таймери інших фігур (пішак, тура, ферзь), базова ємність дробовика.
- (?) Чи білі ходять усі разом (Wikipedia) чи лише ті, чий таймер вийшов (changelog) — тут прийнято таймерну модель.
