---
title: Tumblestone
slug: tumblestone
aka: []
family: falling-match
also: [thinky]
klass: cursor
axes:
  field: square
  time: turn
  opponent: online
  info: full
  random: both
  goal: state
year: 2016
platforms: [PC, Mac, Linux, Wii U, Xbox One, PS4, Switch, iOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tumblestone", best: true, note: "правило трійок, togglers, wildcards, сюжет на 12 світів, puzzle race, аркадні режими"}
  - {kind: steam, url: "https://store.steampowered.com/app/269710/", note: "режими, 10+ модифікаторів, 1–4 гравці локально, ranked online"}
  - {kind: other, url: "https://www.nintendo.com/us/store/products/tumblestone-switch/", note: "eShop: режими, квести, бот Nightmare, 1–4 гравці"}
  - {kind: other, url: "https://purenintendo.com/review-tumblestone/", note: "огляд: «думай наперед, інакше без ходів», токени пропуску, колірна сліпота"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=tumblestone+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [cell-click, keyboard-controls, line-match-clear, no-moves-left, unsolvable-states, restart-level, completion-detection, skip-level, world-map, mode-select, simultaneous-versus, online-multiplayer, ai-opponent, leaderboard, profile-stats, level-bank, +bottom-pick-triple, +clear-all-goal, +wildcard-tile, +toggle-block, +puzzle-race, +rising-stack, +colorblind-shapes]
proposes: ["+cond:exposed", "+effect:take_into_hand", "+card:bottom-pick-triple", "+card:toggle-block", "+card:puzzle-race", "+ui:hand-slots"]
author: opus
date: 2026-11-09
---

# Tumblestone — бери нижні блоки стовпців по три однакові поспіль, доки поле не порожнє

## Суть
Поле — стовпці кольорових блоків над гравцем; гравець ходить уздовж низу і «стріляє» вгору, знімаючи найнижчий блок обраного стовпця. Блоки треба брати трійками одного кольору підряд: три однакові — зникають, і починається наступна трійка. Падіння й злиття нема — тільки **порядок знімання**: щоб скласти трійку, потрібні три відкриті блоки одного кольору, тож кожен вибір відкриває нові нижні блоки й може завести в глухий кут. Мета пазла — зчистити поле повністю.

## Поле і час
- Прямокутна сітка: стовпці блоків, доступний лише нижній («відкритий») блок кожного стовпця; гравець — у рядку під полем.
- Сюжетні пазли — покрокові й статичні (без таймера), заздалегідь задані; аркадні режими — real-time: Heartbeat (стіна блоків опускається), Marathon (скляна стіна), Infinipuzzle (нескінченна сітка).
- Колір — головна властивість; гра має режим для дальтоніків (символи на блоках).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець (персонаж унизу) | player | стовпець | рух ліворуч/праворуч уздовж низу, постріл угору |
| Блок (tumblestone) | tile | колір | знімається лише як нижній у стовпці; входить у поточну трійку |
| Рука-трійка | supply | 3 слоти, колір трійки | збирає зняті блоки; 3 однакові → зникають |
| Wildcard | tile | різнокольоровий | парується з будь-яким кольором при виборі |
| Toggler | tile | стан on/off | сірий блок, що вмикається й вимикається (?) — у стані «on» закриває стовпець |
| Скляна стіна (Marathon) | zone | — | (?) головна особливість режиму Marathon |
| Опускна стіна (Heartbeat) | zone | темп | стіна блоків рухається до гравця; блоки треба знімати швидше, ніж вона йде |
| Суперник / бот | enemy | рівень, напр. Nightmare | розвʼязує ту саму головоломку паралельно |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ТО `move(player, dir)` уздовж нижнього рядка.
- КОЛИ `input(fire)` → ЯКЩО `custom: «exposed — блок найнижчий у стовпці»` and (`counter(hand, ==, 0)` or `same(block, hand, color)` or `state(block, wildcard)`) → ТО `pickup(block)`, `counter(hand, +1)`.
- КОЛИ `input(fire)` → ЯКЩО `not same(block, hand, color)` → ТО `custom: «помилка: трійку зламано»`, `restart` пазла (сюжет) (?) / штраф часу у versus (?).
- КОЛИ `counter(hand, ==, 3)` → ТО `clear(hand)`, `counter(hand, =0)`.
- КОЛИ `state_on(toggler, on)` → ТО `block` для стовпця (?); `state_off` → блок знову доступний (?).
- КОЛИ `all_gone(blocks)` → ТО `win`, `next_level`.
- КОЛИ `no_moves(player)` → ЯКЩО `count(blocks, >, 0)` → ТО `restart` (глухий кут — пазл з початку).
- КОЛИ `input(undo)` → ТО `undo` останнього знімання (?).
- Puzzle race (кінець світу): КОЛИ `counter(cleared_grids, ==, 3)` → ЯКЩО `custom: «раніше за суперника»` → ТО `win`; інакше `lose`.
- Heartbeat: КОЛИ `tick` → ТО `move(wall, toward_player)`; КОЛИ `reach(wall, player_row)` → ТО `lose` (?).
- Infinipuzzle: КОЛИ `after(clear)` → ТО `spawn_at(blocks, top)` (?) — поле не закінчується, мета — протриматись.
- Перемога: поле порожнє (сюжет) / перший у перегонах (versus). Поразка: глухий кут, програні перегони, стіна дійшла (аркада). Рахунок: аркадні режими й квести мають рекорди й таблиці.

## Керування і ввід
- Геймпад/клавіатура: ←/→ — вибір стовпця, кнопка — зняти нижній блок; є гарячі клавіші для швидкого переходу між стовпцями (огляд).
- Кожен хід — один дискретний вибір стовпця: гра покрокова в пазлах навіть без таймера.
- Локально до 4 гравців на одному екрані з окремими полями.

## Вікна, меню, HUD
- `main-menu`: Story · Arcade (`mode-select`: Heartbeat / Marathon / Infinipuzzle) · Multiplayer (`lobby-window` для ranked online, локальний `match-setup`) · Quests · Options.
- `map-window` — мапа 12 світів сюжету, вузли-пазли; токени пропуску.
- `character-select` — дюжина персонажів і середовищ.
- `game-screen`: стовпці блоків, персонаж унизу, `custom: «hand-slots» — 3 слоти поточної трійки`; у versus — `opponent-boards` поруч.
- `end-screen` пазла/перегонів; `leaderboard` для аркадних режимів; `stats-window` (статистика за режимами).
- `settings-window`: `colorblind-palette`, керування.
- Переходи: main-menu → map-window → game-screen → (поле порожнє) наступний пазл; кінець світу → puzzle race → наступний світ.

## Фічі поза полем
- `world-map` 12 світів, `levels-sequential` + `skip-level` (токени, зароблені посеред світу).
- Боси наприкінці світів — puzzle race проти персонажа (3 сітки).
- `mode-endless` (Infinipuzzle), `mode-time-attack`-подібні Heartbeat і Marathon; квести (сотні) як `achievements`.
- `local-multiplayer` 1–4, `online-multiplayer` ranked, `ai-opponent-levels` (бот Nightmare).
- `colorblind-palette`, `leaderboard-online`, `stats`; 10+ модифікаторів сюжету відкриваються поступово.

## Варіації й родичі
- Родичі: Dr. Mario/Puyo (колір як матч-ключ, але з падінням), Mahjong Solitaire та Shisen-Sho (знімаєш лише «відкриті» плитки — тут відкритий = нижній), SameGame (порядок знімання визначає розвʼязність), Magical Drop (стрілок під стовпцями).
- **Осі варіацій**: що доступне (нижній блок стовпця / вільна плитка / будь-яка) · група (пара / трійка / N) · помилка (рестарт / штраф / нічого) · поле (статичний пазл / опускна стіна / нескінченне).

## Цікавинки для курсу
- Знімання лише нижнього блоку стовпця + трійка одного кольору — 🌱 (стек на стовпець, лічильник руки).
- Розвʼязувач пазла: пошук порядку знімань (DFS з відсіканням за кольором руки) — 🥇 (генерація пазлів з гарантованим розвʼязком — 👑).
- Виявлення глухого кута: нема трьох відкритих блоків потрібного кольору — 📎.
- Wildcard як «будь-який колір» у руці — 🌱.
- Puzzle race: два гравці, одна головоломка, перегони на 3 сітки — 🥈 (паралельні поля + синхронізація).
- Toggler-блоки зі станом, що змінюється в часі/за ходами — 📎.

## Мапа на каталог
- Є: `cell-click`/`keyboard-controls` (вибір стовпця) · `line-match-clear` (трійка одного кольору; тут не в лінію поля, а в «руці») · `no-moves-left` · `unsolvable-states` · `restart-level` · `completion-detection` · `skip-level` · `world-map` · `mode-select` · `simultaneous-versus` · `online-multiplayer` · `ai-opponent` · `leaderboard` · `profile-stats` · `level-bank`.
- **Нема** → пропозиції карток:
  - `+bottom-pick-triple` «Бери нижні блоки стовпців трійками одного кольору» · entities/interact · 📎 · слот {group: 3}.
  - `+toggle-block` «Блок, що вмикається/вимикається» · entities/state · 📎.
  - `+puzzle-race` «Перегони на тій самій головоломці» · multiplayer · 🥈 · слот {grids: 3}.
  - `+clear-all-goal` · `+wildcard-tile` · `+rising-stack` (Heartbeat) · `+colorblind-shapes` — теги вже є в корпусі.

## Пропозиції до словників
- `+cond:exposed` — сутність доступна для взяття (нижня в стовпці; підтверджую наявну пропозицію).
- `+effect:take_into_hand` — блок переходить у руку-трійку, а не в інвентар (відмінне від `pickup`: рука має дисципліну «лише один колір»).
- `+card:bottom-pick-triple` · `+card:toggle-block` · `+card:puzzle-race` — див. «Мапу».
- `+ui:hand-slots` — індикатор зібраних блоків поточної трійки (родич `pocket`).

## Джерела
- ⭐ [Wikipedia: Tumblestone](https://en.wikipedia.org/wiki/Tumblestone) — правило «три однакові, доки поле не порожнє», togglers, wildcards, 12 світів, токени пропуску, puzzle race на 3 сітки, Heartbeat/Marathon/Infinipuzzle.
- [Steam](https://store.steampowered.com/app/269710/) — 40+ годин сюжету, 10+ модифікаторів, режими, 1–4 локально, ranked online, боти.
- [Nintendo eShop](https://www.nintendo.com/us/store/products/tumblestone-switch/) — квести, бот Nightmare, дюжина персонажів.
- [Pure Nintendo: огляд](https://purenintendo.com/review-tumblestone/) — «будь вибірковим, інакше без ходів», статистика й таблиці, колірна сліпота.
- YouTube: пошук «tumblestone gameplay».

## Непевне
- (?) Що саме відбувається при спробі взяти блок іншого кольору (заборона / рестарт / штраф у versus) — жодне відкрите джерело не описує; з памʼяті: у сюжеті пазл перезапускається.
- (?) Undo останнього знімання — з памʼяті.
- (?) Поведінка toggler-ів («вмикаються й вимикаються» — так у Wikipedia) і решти з 10+ модифікаторів — не знайдено описів; огляди кажуть, що гра їх майже не пояснює.
- (?) Деталі Heartbeat (темп, умова програшу), Marathon («скляна стіна»), поповнення Infinipuzzle — лише назви.
- Офіційний сайт за назвою не знайдено (tumblestone.com — інша компанія); Nintendo Life — 403.
