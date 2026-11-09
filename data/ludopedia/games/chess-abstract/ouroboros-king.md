---
title: The Ouroboros King
slug: ouroboros-king
aka: [Ouroboros King, Ouroboros Chess]
family: chess-abstract
also: [roguelike]
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: both
  goal: state
year: 2023
platforms: [PC, macOS, Linux, Android, iOS, Switch, PS4, PS5, Xbox One, Xbox Series]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2096510", best: true, note: "класичні й казкові фігури + реліквії + витратні предмети; хід однією фігурою; забіг 15–45 хв; мета — Ковен"}
  - {kind: other, url: "https://kinuthedragon.github.io/OuroKing/howtoplay.html", note: "How to Play «Ouroboros Chess»: ~30 фігур з ходами, тайли Bomb/Portal/Rock, взяття короля замість мату, сід"}
  - {kind: other, url: "https://3rd-strike.com/?p=166866", note: "огляд: вибір 3 фігур зі старту, вузли мапи, боси наприкінці глави, рівні фігур"}
  - {kind: other, url: "https://www.devuego.es/en/fgame/the-ouroboros-king", note: "дати релізів на всіх платформах, same-device PvP"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=The+Ouroboros+King+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [piece-move-patterns, piece-capture, pawn-promotion, cell-transform, teleport-pair, explode-area, impassable-cells, hover-highlight, cell-click, ai-opponent, hot-seat, run-relics, shop-between-levels, round-currency, world-map, sequential-levels, permadeath, difficulty-levels, seed-share, game-screen, main-menu, map-window, shop-window, end-screen, +army-draft, +piece-level-up, +king-capture-win, +consumable-items, +transform-on-capture]
proposes: ["+effect:copy_pattern(a, b)", "+effect:infect(capturer)", "+cond:captured_by(kind)", "+window:army-draft", "+ui:move-pattern-hover", "+card:army-draft", "+card:piece-level-up", "+card:king-capture-win", "+card:transform-on-capture"]
author: opus
date: 2026-11-09
---

# The Ouroboros King — шаховий роглайк: збираєш армію з казкових фігур і реліквій і партія за партією йдеш мапою проти Ковену

## Суть
Роглайт Oriol Cosp Games (2023): кожен бій — шахова партія один-на-один проти ворожої армії, але фігури казкові (Princess, Assassin, Leper, Fool…), а поле має особливі тайли. Забіг: на старті обираєш 3 фігури з випадкового набору, далі йдеш мапою з вузлами, перемагаєш — нагорода (нова фігура, реліквія, предмет), фігури ростуть рівнями й перетворюються на сильніші. Наприкінці глави — бос-член Ковену; програв — новий «таймлайн» з іншою мапою, ворогами й нагородами.

## Поле і час
- Шахова дошка (розмір у джерелах не названо (?)); на ній тайли з ефектами.
- Розстановка: власний «лейаут» до 8 фігур (не більше одного короля), який ставиться на твій бік випадково за сідом (фан-сторінка) (?).
- Покроково, одна фігура за хід (Steam: «move only one piece per turn»).
- Забіг 15–45 хв; мапа з вузлами, глави закінчуються босом.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| King | piece | 1 на армію | на 1 у 8 напрямків; взяли — поразка |
| Mounted King | piece | — | король або кінь; взяли — поразка |
| Queen / Rook / Bishop / Knight | piece | — | класичні ходи |
| Marching Pawn | piece | — | до 2 вперед або 1 по діагоналі, бʼє лише по діагоналі; на останньому ряду — ферзь |
| Princess | piece | — | як король або 2 по діагоналі; після взяття — ферзь до кінця бою |
| Assassin | piece | — | як король; після взяття може ходити ще раз |
| Blade Dancer | piece | — | як Assassin + будь-яка клітина контуру квадрата 5×5 навколо |
| Leper | piece | — | як король; хто його візьме (крім короля), сам стає Leper |
| Immortal | piece | — | як король; убити може лише король |
| Fool | piece | — | ходить як фігура, якою суперник ходив востаннє; не в перший хід |
| Golem | piece | — | тура/король/кінь, але лише взяттям |
| Agent + / Agent X | piece | пара станів | хід як тура → стає X; хід як слон → стає + |
| Viking / Berserker | piece | — | до 3 / до 3 ходів по прямих, напрям можна міняти |
| Portal Mage | piece | — | на будь-яку порожню клітину; бʼє як король |
| Gryphon / Manticore | piece | — | 1 діагональ + промінь прямо / 1 прямо + промінь по діагоналі |
| Pegasus | piece | — | 1–2 стрибки коня в одному напрямку |
| Інші | piece | — | Cardinal, Bowman, Catapult, Crusader, Knight Templar, Unicorn Cavalry |
| Edea the Witch Queen / Andromeda of the Stars / Tabitha the Deceptive | boss | — | іменні фігури: тура+слон+кінь / Manticore або Gryphon / ходить як будь-яка фігура суперника, крім Portal Mage (?) |
| Bomb | hazard | — | тайл-фігура: коли її беруть, знищує все навколо, себе й того, хто взяв |
| Portal Gate | terrain | парні | увійшов в один — той самий рух продовжується з другого |
| Rock | static | — | блокує рух крізь себе, не береться |
| Реліквія | pickup | — | постійний бонус фігурам на забіг |
| Предмет | pickup | витратний | тимчасова перевага в бою («surprising gadgets») |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, piece, to)` → ЯКЩО `turn_of(player)` і `legal(move)` → ТО `move(piece, to)`, `end_turn` (одна фігура за хід).
- КОЛИ `input(move, piece, to)` → ЯКЩО `occupied(to, enemy)` → ТО `disappear_b`.
- КОЛИ `died(king)` → ТО `lose` тій стороні — мату й шаху нема, перемога взяттям короля (фан-сторінка) (?).
- КОЛИ `died(enemy_king)` → ТО `win` бою → `choose(rewards)`.
- КОЛИ `input(move, princess, to)` → ЯКЩО `occupied(to, enemy)` → ТО `transform(princess, queen)`.
- КОЛИ `reach(marching_pawn, last_row)` → ТО `transform(marching_pawn, queen)`.
- КОЛИ `input(move, assassin, to)` → ЯКЩО `occupied(to, enemy)` → ТО `extra_move`.
- КОЛИ `died(leper)` → ЯКЩО `custom: «узяв не король»` (`+cond:captured_by`) → ТО `transform(capturer, leper)` (`+effect:infect`).
- КОЛИ `input(move, piece, immortal_cell)` → ЯКЩО `custom: «piece — не король»` → ТО `block`.
- КОЛИ `input(move, fool, to)` → ЯКЩО `custom: «to за патерном останньої ходженої фігури суперника»` (`+effect:copy_pattern`) → ТО `move(fool, to)`.
- КОЛИ `input(move, agent_plus, to)` → ТО `move`, `transform(agent_plus, agent_x)`; і навпаки.
- КОЛИ `input(move, golem, to)` → ЯКЩО `not occupied(to, enemy)` → ТО `block`.
- КОЛИ `died(bomb)` → ТО `explode(3x3)`, `disappear_both` (бомба й той, хто взяв, + сусіди).
- КОЛИ `enter(piece, portal_gate)` → ТО `teleport(piece, pair)` і `custom: «рух продовжується з другого порталу»`.
- КОЛИ `input(move, piece, through_rock)` → ТО `block`.
- КОЛИ `counter(piece_xp, >=, n)` → ТО `custom: «фігура підвищує рівень, згодом перетворюється на сильнішу»` (`transform`).
- КОЛИ `input(use, item)` → ТО `custom: «тимчасовий ефект предмета в бою»` (`use`).
- КОЛИ `level_end` → ЯКЩО `custom: «бій виграно»` → ТО `window(map-window)`, `next_level`; бос глави → наступна глава.
- КОЛИ `custom: «бій програно»` → ТО `lose` забігу → новий таймлайн (`restart` з новою мапою).
- Перемога: перемогти весь Ковен · Поразка: втрата короля в будь-якому бою · Рахунок: — (вищі рівні складності).

## Керування і ввід
- Клік по фігурі → підсвітка її ходів (наведення показує патерн) → клік по клітині.
- Мапа: клік по наступному вузлу; магазин — клік по товару; предмети — з панелі.
- Тач на мобільних, геймпад на консолях (?).

## Вікна, меню, HUD
- `main-menu`: новий забіг, PvP на одному пристрої, налаштування (?), складність.
- `+window:army-draft` — старт забігу: випадковий набір фігур, обрати 3.
- `map-window`: вузли-бої, магазин, нагороди; бос у кінці глави.
- `game-screen`: дошка, тайли, обидві армії, панель предметів, `hover-highlight` патерну ходу (`+ui:move-pattern-hover`), опис фігури.
- `shop-window`: фігури/реліквії/предмети за валюту (?).
- `upgrade-window` / вибір нагороди після бою.
- `end-screen`: поразка → «новий таймлайн»; перемога над Ковеном.
- Переходи: main-menu → army-draft → map-window ⇄ game-screen / shop-window → … → end-screen.

## Фічі поза полем
- Усе розблоковано з першого запуску (без `meta-progression` — свідоме рішення).
- `difficulty-presets`: численні end-game опції підвищення складності.
- `local-multiplayer`: шахи з унікальними фігурами на одному пристрої (PvP і co-op за Steam-тегами).
- `seed-input`: сід визначає розстановку й тайли (фан-сторінка) (?).
- Демо, `localization` (12 мов).

## Варіації й родичі
- Родичі в корпусі: `shotgun-king.md` (один король проти армії, пари карт тобі+ворогу), `chess-survivors.md` (орда і виживання), `roguelike/pawnbarian.md` (карти-патерни героя), `passant.md` (модифікатори правил і магазин), `chess-with-different-armies.md`, `really-bad-chess.md` (нестандартні армії), `capablanca-chess.md` і `baroque-chess.md` (казкові фігури).
- **Відмінність від Shotgun King / Pawnbarian**: тут не аватар, а повна армія з королем (`klass: figure`), бій симетричний — партія проти армії Ковену.
- **Відмінність від Passant**: тут сила росте фігурами (рівні, перетворення, тайли), а не бейджами-змінами базових правил.
- Осі варіацій: **армія** (фіксована / драфт / купівля) · **ріст фігур** (рівні / реліквії / предмети) · **кінець бою** (мат / взяття короля) · **поле** (чисте / тайли-пастки й портали).

## Цікавинки для курсу
- Казкові фігури як дані: патерн = комбінація базових (король | кінь | промінь-тура…) + модифікатори («лише взяттям», «ще хід після взяття») — 🥈.
- Fool: патерн, що копіює останній хід суперника — потрібна історія ходів — 🥉.
- Leper: зараження того, хто бʼє, і Immortal «бʼє лише король» — правила взяття як таблиця — 🥉.
- Портали, що продовжують промінь руху з парного порталу — 🥈.
- Бомба-фігура з вибухом 3×3 при взятті — 📎.
- Драфт армії «3 з N» + мапа вузлів + рівні фігур — роглайк-оболонка над шахами — 🥉.
- AI проти казкових фігур і тайлів: мінімакс з оцінкою матеріалу — 🥇.

## Мапа на каталог
- Є в каталозі: `piece-move-patterns`, `piece-capture` ↔ ~30 фігур · `pawn-promotion` ↔ Marching Pawn · `cell-transform` (?) · `teleport-pair` ↔ Portal Gate · `explode-area` ↔ Bomb · `impassable-cells` ↔ Rock · `hover-highlight`, `cell-click` · `ai-opponent`, `hot-seat` · `run-relics`, `shop-between-levels`, `round-currency` (?) · `world-map` ↔ мапа вузлів · `sequential-levels`, `permadeath`, `difficulty-levels`, `seed-share` · `game-screen`, `main-menu`, `map-window`, `shop-window`, `end-screen`.
- **Нема** → пропозиції карток:
  - `+army-draft` «Драфт стартової армії: обрати k з N випадкових» · game-logic/economy · 📎 · слоти {k, n}.
  - `+piece-level-up` «Рівні фігур і еволюція в сильнішу» · entities/progression · 🥉.
  - `+king-capture-win` «Перемога взяттям короля (без мату)» · game-logic/win · 🌱.
  - `+consumable-items` «Витратні предмети в бою» · game-logic/economy · 📎.
  - `+transform-on-capture` «Перетворення від взяття (Princess → Queen, Leper заражає)» · entities/interact · 📎.

## Пропозиції до словників
- `+effect:copy_pattern(a, b)` — A ходить за патерном фігури B (Fool, Tabitha).
- `+effect:infect(capturer)` — той, хто взяв, перетворюється на взяту (Leper); частковий випадок `transform`.
- `+cond:captured_by(kind)` — фігуру взяв конкретний вид.
- `+window:army-draft` — вибір стартової армії з випадкового набору.
- `+ui:move-pattern-hover` — наведення на фігуру показує її патерн.
- `+card:army-draft`, `+card:piece-level-up`, `+card:king-capture-win`, `+card:transform-on-capture` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: The Ouroboros King](https://store.steampowered.com/app/2096510) — класичні + казкові фігури, реліквії, витратні предмети, «surprising gadgets», одна фігура за хід, забіг 15–45 хв, новий таймлайн після поразки, усе розблоковано, end-game складності, same-device PvP.
- [How to Play «Ouroboros Chess»](https://kinuthedragon.github.io/OuroKing/howtoplay.html) — повний список фігур з ходами, тайли Bomb/Portal Gate/Rock, взяття короля замість мату, лейаут до 8 фігур, сід розстановки.
- [3rd Strike: огляд](https://3rd-strike.com/?p=166866) — вибір 3 фігур з випадкового набору, нагороди й вузли мапи, боси наприкінці глави, Assassins/Princesses, рівні й апгрейд фігур.
- [Devuego: картка гри](https://www.devuego.es/en/fgame/the-ouroboros-king) — дати релізів: PC 27.02.2023, Android 09.2023, iOS 11.2023, Switch 06.2024, Xbox/PS 11.2024.

## Непевне
- (?) Сторінка kinuthedragon.github.io — не офіційна й не каже, чи повторює правила оригіналу (можливо, фан-ремейк/компаньйон); фігури, тайли, «взяття короля без мату» й ліміт 8 фігур треба звірити з грою.
- (?) Чи Edea, Andromeda, Tabitha — члени Ковену (боси) — висновок з назв.
- (?) Розмір дошки, валюта й ціни магазину, типи вузлів мапи, як саме фігури набирають рівні.
- (?) Скільки членів Ковену й глав; чи боси мають особливі правила бою.
- (?) Наявність undo.
