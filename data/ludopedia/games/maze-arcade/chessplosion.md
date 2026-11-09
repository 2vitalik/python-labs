---
title: Chessplosion
slug: chessplosion
aka: []
family: maze-arcade
also: [chess-abstract]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: setup
  goal: state
year: 2021
platforms: [Windows (Steam, itch.io)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1571220/Chessplosion/", best: true, note: "режими Adventure / Dungeon / Puzzle / Survival / Battle, вороги-фігури, Assist Mode, редактор пазлів"}
  - {kind: itch, url: "https://ctmatthews.itch.io/chessplosion", note: "те саме + коментар автора: слон бʼє лише клітини свого кольору, кінь — протилежного"}
  - {kind: other, url: "https://lifeisxbox.eu/review-chessplosion", note: "огляд: патерни вибуху тури, слона, ферзя, коня; фітиль кілька секунд; бос із серцями"}
  - {kind: other, url: "https://gertlushgaming.co.uk/chessplosion-review-steam/", note: "огляд: кулдаун фігур, налаштування бою, Arcade-складності, опції"}
  - {kind: other, url: "https://gamermatters.com/chessplosion-is-like-bomberman-but-the-bombs-are-chess-pieces/", note: "кінь бʼє лише кінці L, король — як звичайна бомба; дошка 8×8 як мотив"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Chessplosion+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-by-input, bomb-fuse, piece-move-patterns, explode-area, blast-wave, chain-detonation, placement-cooldown, environment-death, destroy-all-enemies, hp-damage, projectile-shot, line-of-sight-attack, world-map, dungeon-generation, round-currency, in-round-upgrades, in-game-editor, level-exchange, ai-opponent, online-multiplayer, match-setup, difficulty-levels, skip-level, controls-remap, game-settings, tutorial-window, +piece-pattern-blast, +square-color-blast, +bomb-budget, +bomb-tennis, +team-battle]
proposes: ["+card:piece-pattern-blast", "+card:square-color-blast", "+card:bomb-budget", "+card:bomb-tennis", "+cond:square_color", "+trigger:blast", "+effect:throw"]
author: opus
date: 2026-11-09
---

# Chessplosion — Bomberman, де бомби — шахові фігури: кожна вибухає так, як ходить

## Суть
Качка бігає по шахівниці й кладе бомби у формі шахових фігур. За кілька секунд бомба вибухає за патерном ходу своєї фігури: тура — хрестом по рядку й стовпцю, слон — по діагоналях, ферзь — і так, і так, кінь — лише в кінцевих клітинах L-ходів. Вибухи підривають сусідні бомби, тож гра — це ланцюгові реакції в реальному часі й ухиляння від власних вибухів. Вороги теж поводяться як фігури: тури таранять, слони стріляють по діагоналях, коні тупотять.

## Поле і час
- Шахівниця (8×8 як мотив; арени Battle й етапи пригоди — свої розміри (?)). Колір клітини важливий: слон бʼє лише клітини свого кольору, кінь — протилежного.
- Real-time: фітиль — кілька секунд, кулдаун на фігури не дає засипати поле бомбами.
- Режими: Adventure (етапи з ворогами й босами на мапі-павутині), Dungeon (випадкові підземелля), Puzzle (обмежений набір бомб), Survival (ухилятися від хвиль вибухів), Battle (до 4 гравців).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Качка | player | здоровʼя / життя (Arcade — життя) | рух полем; кладе бомбу-фігуру на свою клітину; гине від будь-якого вибуху, і свого теж |
| Бомба-тура | object | фітиль кілька секунд | вибух по всьому рядку й стовпцю |
| Бомба-слон | object | — | вибух по діагоналях на всю дошку; лише клітини свого кольору |
| Бомба-ферзь | object | — | рядок + стовпець + діагоналі |
| Бомба-кінь | object | — | вибух лише в кінцевих клітинах L-ходів (протилежного кольору) |
| Бомба-король | object | — | «як звичайна бомба» — сусідні клітини (?) |
| Вибух | hazard | форма = патерн фігури | вбиває, ранить боса, підриває інші бомби, бʼє мішені |
| Ворог-тура | enemy | — | таранить по прямій |
| Ворог-слон | enemy | — | стріляє снарядами по діагоналі |
| Ворог-кінь | enemy | — | «тупотить» (stomp) |
| Снаряд слона | projectile | — | летить по діагоналі |
| Бос ×8 | boss | серця над головою (перший — 4) | кладе власні бомби й блокує гравця; −1 серце за влучання |
| Мішень (Puzzle) | object | — | розбивається вибухом |
| Монета (Dungeon) | resource | — | збирається; витрачається на апгрейди й зброю забігу |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО `move(duck, dir)`.
- КОЛИ `input(drop)` → ЯКЩО `custom: «фігура не на кулдауні»` → ТО `place(duck, piece_bomb)`, `timer(cooldown)`.
- КОЛИ `timer(fuse)` → ТО `explode(piece_pattern, board, blast)` — форма = патерн ходу фігури.
- КОЛИ `custom: «вибух слона»` → ЯКЩО `custom: «клітина того ж кольору, що й бомба»` → ТО `explode(diagonals, board, blast)`; кінь — лише клітини протилежного кольору, кінці L.
- КОЛИ `contact(blast, bomb)` → ТО `custom: «бомба детонує негайно»` — ланцюгова реакція.
- КОЛИ `contact(blast, duck)` → ТО `damage(duck, 1)` або `lives(-1)` — свої вибухи теж шкодять.
- КОЛИ `contact(blast, enemy)` → ТО `disappear(enemy)`; КОЛИ `contact(blast, boss)` → ТО `damage(boss, 1)`.
- КОЛИ `line_of_sight(rook_enemy, duck)` → ТО `custom: «тура таранить по прямій»` (?).
- КОЛИ `timer(n)` → ТО `spawn(projectile)` з ворога-слона по діагоналі.
- КОЛИ `contact(projectile|enemy, duck)` → ТО `damage(duck, 1)`.
- КОЛИ `timer(n)` → ТО `place(boss, piece_bomb)` — бос мінує поле (?).
- КОЛИ `all_gone(enemy)` або `hp_zero(boss)` → ТО `win`, `next_level` — вузол мапи відкриває сусідні.
- Puzzle: КОЛИ `all_gone(target)` → ТО `win`; КОЛИ `counter(bombs_left, ==, 0)` → ЯКЩО `count(target, >, 0)` → ТО `restart`.
- Dungeon: КОЛИ `picked(duck, coin)` → ТО `currency(+n)`; між кімнатами — `choose(upgrade|weapon)` (?).
- Survival: КОЛИ `schedule(waves)` → ТО `spawn(bomb_pattern)`; фінал — «bullet hell» вибухи ферзів.
- Battle: КОЛИ `custom: «лишився один гравець / одна команда»` → ТО `win` раунду; Tennis: `custom: «кожен на своїй половині, бомби перекидають через центральну лінію»` — `+effect:throw`.
- Перемога: зачистити етап / убити боса / розбити всі мішені / вижити. · Поразка: здоровʼя або життя скінчились (у пригоді — назад на старт етапу). · Рахунок: лише в Arcade (?).

## Керування і ввід
- Рух + кнопка бомби; клавіатура або геймпад (Xbox, PlayStation, будь-який), клавіші перепризначаються.
- Як обирається фігура для наступної бомби — не з'ясовано (?).
- Battle: локально 1–4 гравці, онлайн 1v1 з rollback-netcode (лише Steam).

## Вікна, меню, HUD
- `main-menu` → `mode-select`: Adventure · Dungeon · Puzzle · Survival · Battle · Arcade · Training.
- `world-map` (Adventure): павутина етапів, гравець обирає шлях.
- `game-screen`: шахівниця, вороги, бомби; HUD — `hp-bar` / `lives`, серця боса над головою.
- `match-setup` (Battle): режим (FFA, команди, Tennis), ліміт раундів, ліміт часу, sudden death, кількість бомб, здоровʼя, AI чи люди.
- `lobby-window` (онлайн): браузер серверів, швидке приєднання.
- `editor-window`: редактор пазлів зі збереженням і обміном.
- `tutorial-window`: інтерактивне навчання («How to play»).
- `settings-window`: кольори фігур і клітин, стиль клітин, тряска екрана, статичний фон, таймер спідрану, затримка вводу онлайн; графіка — повний екран, роздільність, FPS, масштабування, фільтр; перепризначення клавіш; музика.
- Переходи: main-menu → mode-select → (Adventure) world-map → game-screen → назад на мапу; Battle → match-setup → game-screen.

## Фічі поза полем
- `assist-mode`: здоровʼя, життя, швидкість гри, пропуск етапів.
- `difficulty-presets` в Arcade: beginner / advanced / expert.
- `level-editor` + `level-sharing` для пазлів; `puzzle-bank` понад 100 пазлів.
- `meta-progression` (?) / апгрейди й зброя, що міняються від забігу (Dungeon).
- `local-multiplayer` до 4, `online-multiplayer` 1v1, `ai-opponent-levels` (?); `achievements` (29 у Steam); `cloud-save`; `colorblind-palette`; локалізація 9 мов.

## Варіації й родичі
- Родичі: [`bomberman`](bomberman.md) (хрест вогню, ланцюг бомб, battle mode), [`bomberman-battle-mode`](bomberman-battle-mode.md), [`chess-survivors`](../chess-abstract/chess-survivors.md) (шахові фігури як вороги real-time-виживання), [`shotgun-king`](../chess-abstract/shotgun-king.md) (один гравець проти шахової армії).
- Осі варіацій «форма вибуху»: хрест на N (Bomberman) / квадрат-радіус / патерн шахової фігури (Chessplosion) / колір клітини як фільтр (слон, кінь). Вісь «ворог-фігура»: ходить за шаховими правилами покроково (Chess Survivors) / рухається real-time у стилі фігури (Chessplosion).

## Цікавинки для курсу
- Форма вибуху = патерн ходу фігури: одна функція «клітини атаки фігури» для руху й для вибуху — 🥉.
- Фільтр за кольором клітини (слон — свій колір, кінь — протилежний) — 📎.
- Ланцюгова детонація з різними формами вибухів — 🥉 (картка `chain-detonation` є, тут форми різні).
- Кулдаун на тип бомби замість ліміту бомб — 🌱.
- Пазл «розбий усі мішені обмеженим набором бомб» + редактор і обмін — 🥈.
- Tennis Battle: поле, поділене лінією, бомби перекидають на чужу половину — 🥉.

## Мапа на каталог
- Є: `move-by-input`; `bomb-fuse` ↔ фітиль; `piece-move-patterns` ↔ патерни фігур; `explode-area` + `blast-wave` ↔ форми вибуху; `chain-detonation` ↔ ланцюги; `placement-cooldown` ↔ кулдаун фігур; `environment-death` ↔ власний вибух; `destroy-all-enemies` ↔ зачистка; `hp-damage` ↔ серця боса; `projectile-shot` ↔ снаряди слона; `line-of-sight-attack` ↔ таран тури (?); `world-map` ↔ павутина етапів; `dungeon-generation` + `round-currency` + `in-round-upgrades` ↔ Dungeon; `in-game-editor` + `level-exchange` ↔ редактор пазлів; `ai-opponent` + `online-multiplayer` + `match-setup` ↔ Battle; `difficulty-levels` + `skip-level` ↔ Arcade і Assist; `controls-remap` + `game-settings`; `tutorial-window`.
- **Нема** → пропозиції карток:
  - `+piece-pattern-blast` «Вибух за патерном шахової фігури» · entities/combat · 🥉 · слот {piece} — дитина `explode-area`.
  - `+square-color-blast` «Вибух лише по клітинах певного кольору» · entities/combat · 📎.
  - `+bomb-budget` «Обмежений набір бомб на пазл» · game-logic/lose · 🌱 — родич `move-limit`.
  - `+bomb-tennis` «Бомби через центральну лінію» · game-logic/opponent · 🥉.
  - `+team-battle` «Командний бій» · game-logic/opponent · 📎.

## Пропозиції до словників
- `+cond:square_color` — колір клітини (свій / протилежний) як умова ураження.
- `+trigger:blast` — сутність потрапила під вибух (уже пропонував Bomberman); зараз — `contact(blast, x)`.
- `+effect:throw` — перекинути бомбу (уже ×6 🔥).
- `+card:piece-pattern-blast`, `+card:square-color-blast`, `+card:bomb-budget`, `+card:bomb-tennis` — див. вище.

## Джерела
- ⭐ [Steam: Chessplosion](https://store.steampowered.com/app/1571220/Chessplosion/) — опис режимів, вороги-фігури, 8 босів і 90+ етапів, редактор пазлів, Battle до 4 гравців, Assist Mode, 29 досягнень.
- [itch.io: Chessplosion](https://ctmatthews.itch.io/chessplosion) — те саме + коментар автора про кольори клітин для слона й коня, rollback-netcode, мови.
- [LifeisXbox: огляд](https://lifeisxbox.eu/review-chessplosion) — патерни тури, слона, ферзя, коня; фітиль; бос із 4 серцями, що кладе бомби.
- [Gertlush Gaming: огляд](https://gertlushgaming.co.uk/chessplosion-review-steam/) — кулдаун фігур, мапа-павутина, налаштування Battle, складності Arcade, опції.
- [GamerMatters](https://gamermatters.com/chessplosion-is-like-bomberman-but-the-bombs-are-chess-pieces/) — кінь бʼє лише кінці L, король — як звичайна бомба, шахівниця 8×8 як мотив.
- YouTube: пошук «Chessplosion gameplay».

## Непевне
- (?) Як гравець обирає фігуру для бомби (по черзі, вибір кнопкою, набір етапу) — джерела мовчать.
- (?) Патерн пішака й точна форма «звичайної» бомби короля (3×3 чи хрест на 1).
- (?) Чи рух качки клітинний чи вільний, а бомба прилипає до клітини — як у Bomberman (припущення).
- (?) Розміри арен і полів етапів; поведінка ворогів-фігур у деталях (таран тури — по лінії бачення?).
- (?) Огляди розходяться щодо режимів (Steam: Adventure/Dungeon/…; огляд: Arcade, Training) — можливо, різні версії гри.
