---
title: Puzzle & Dragons (PAD, Пазли і Дракони)
slug: puzzle-and-dragons
family: falling-match
also: [roguelike]
klass: cursor
axes:
  field: square
  time: turn
  opponent: ai
  info: partial
  random: runtime
  goal: survive
year: 2012
platforms: [iOS, Android, Amazon Fire, 3DS (PAD Z/X), Switch (PAD GO)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Puzzle_%26_Dragons", best: true, note: "поле 6×5, перетягування з таймером, комбо, skyfall, команда, лідер-скіли, данжі"}
  - {kind: official, url: "https://www.puzzleanddragons.us/single-post/ver-21-7-update-241023", note: "NA-сайт: патч 21.7 — час руху 5 → 6 с, awoken skills"}
  - {kind: official, url: "https://www.puzzleanddragons.us/single-post/ninegaruda-tournament-orb-move-time-99-sec", note: "турнір з часом руху 99 с — приклад зміни правила"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=puzzle+and+dragons+combo+gameplay", note: "пошук; комбо і skyfall"}
stage: v1
coverage: 60
mechanics: [drag-drop-piece, gravity-fall, combo-multiplier, event-points, hp-damage, telegraphed-intents, enemy-waves, round-currency, shop-window, save-progress, +drag-path-swap, +line-match-clear, +chain-reaction, +cascade-gravity, +skyfall-refill, +move-timer-drag, +team-loadout, +leader-skill-rules, +active-skill-cooldown, +board-hazards, +gacha-draw, +stamina-energy]
proposes: ["+trigger:input", "+trigger:pattern", "+trigger:settled", "+trigger:turn_end", "+trigger:counter", "+cond:same", "+cond:chain", "+cond:timer", "+effect:swap", "+effect:clear", "+effect:spawn_at", "+effect:damage", "+effect:heal", "+effect:set_cell", "+effect:timer", "+role:tile", "+role:ally", "+role:boss", "+ui:hp-bar", "+ui:combo-meter", "+ui:drag-timer", "+ui:enemy-turn-counter", "+window:team-builder", "+window:dungeon-select", "+window:gacha-window", "+feature:stamina", "+axis:control"]
author: opus
date: 2026-11-02
---

# Puzzle & Dragons — тягни одну кулю шляхом по полю; усі збіги 3+ за хід — комбо, що б'є ворога

## Суть
Поле 6×5 кольорових куль. За хід гравець бере **одну** кулю й веде її пальцем довільним шляхом: кожна куля, через яку вона проходить, міняється з нею місцями — так за один хід переставляється пів поля. Хід обмежено часом (~5 с) з моменту першого обміну. Після відпускання всі лінії 3+ одного кольору зникають, згори падають нові (skyfall) і можуть дати ще збіги; кожна група — одне **комбо**. Кольори збігів визначають, які монстри команди атакують, серця лікують; кількість комбо множить шкоду. Гра — RPG-забіг по поверхах данжу проти ворогів із лічильниками атаки.

## Поле і час
- Поле 6 стовпців × 5 рядів; лідер-скіли деяких монстрів/данжів міняють його на 7×6 (і 5×4 у спец-данжах (?)). Над полем — сцена бою з ворогами.
- Покроково: хід гравця = одне перетягування (без ліміту на «думати» до першого дотику); від першого обміну — real-time таймер руху (база ~5 с за Wikipedia; змінюється скілами, awakenings, ворогами, патчами).
- Після ходу — фаза розвʼязання (каскад), потім атаки команди, потім ворогів з лічильником 0.
- Інформація часткова: майбутні кулі skyfall невідомі; лічильник ходів до атаки ворога видно (`telegraphed-intents`), а що саме він зробить — частково.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Куля Fire / Water / Wood / Light / Dark | tile | колір | зникає в лінії 3+; активує атаку монстрів свого атрибута |
| Серце (Heart) | tile | — | збіг лікує команду за RCV |
| Посилена куля (enhanced, «+») | tile | колір | кожна в збігу підсилює шкоду цієї атаки (?) |
| Jammer | hazard | — | займає місце, сама по собі нічого (зникає в збігу 3+) |
| Poison / Mortal poison | hazard | шкода | збіг ранить команду |
| Bomb orb | hazard | — | вибух/шкода (?) |
| Locked orb | tile | замок | рухається і зникає як звичайна, але скіли перефарбування її не змінюють (?) |
| Інші ворожі ефекти поля | hazard | — | blind (сховані кулі), tape (рядок/стовпець не рухається), cloud (закрита зона), spinner (клітина міняє колір), immovable cell |
| Ворог | enemy | HP, атрибут, лічильник ходів (CD), щити | атакує, коли CD = 0; навички змінюють поле/час |
| Бос поверху | boss | HP, фази (?) | останній поверх данжу |
| Монстр команди | ally | атрибут (осн./дод.), ATK/HP/RCV, active skill CD, awakenings | б'є, коли зібрано його колір |
| Лідер + хелпер | ally | leader skill | пасивно міняє правила для всієї команди (множник, +час, 7×6 поле…) |
| Команда HP | — | сума HP монстрів | 0 → поразка (continue за magic stone) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(touch orb)` → ТО куля «в руці» (`drag-ghost`); таймер ще не йде.
- КОЛИ `input(drag into neighbor cell)` → ТО `swap(held, neighbor)` (8 напрямків, діагоналі теж); перший обмін → `timer(start, move_time)`.
- КОЛИ `input(release)` або `timer(move, ==, 0)` → ТО хід закінчено, розвʼязання.
- КОЛИ `custom: «resolve»` → ЯКЩО `pattern(line(3+, same_color))` по горизонталі/вертикалі → ТО позначити; звʼязані однакові позначені клітини — **одне комбо**; `clear(all_marked)`, `combo(+1)` за кожну групу.
- КОЛИ `after(clear)` → ТО `fall(unsupported)`, `spawn_at(random_orb, top)` (skyfall); ЯКЩО новий `pattern(line(3+))` → ТО `clear`, `combo(+1)` (skyfall combo), доки поле не стабільне.
- КОЛИ `trigger:settled` → ТО для кожного монстра: шкода = ATK × Σ по його групах `(1 + 0.25·(n−3))` × `(1 + 0.25·(combos−1))` × лідер-множники × стихія (?); група 5+ куль → атака по всіх ворогах.
- Стихії: Fire > Wood > Water > Fire (×2 / ×0.5); Light ↔ Dark — взаємно сильні.
- КОЛИ `pattern(hearts)` → ТО `heal(team, RCV × …)`.
- КОЛИ `after(team_attack)` → ТО кожен ворог `counter(cd, −1)`; ЯКЩО `cd == 0` → ТО `damage(team, atk)` або навичка (змінити кулі, скоротити час, заблокувати скіл, поставити jammer/poison), `cd` скидається.
- КОЛИ `hp_zero(enemy)` для всіх ворогів поверху → ТО наступний поверх (`wave_cleared`); останній поверх (бос) → `win` данжу, дропи/досвід.
- КОЛИ `hp_zero(team)` → ТО `window(game-over-continue)`: continue за magic stone або `lose`.
- КОЛИ `input(tap monster)` → ЯКЩО `counter(skill_cd, ==, 0)` → ТО active skill: перефарбувати кулі, нове поле, затримати ворогів, +шкода, +час руху; `skill_cd` скидається.
- Лідер-скіли (пасивні): `multiplier(×k)` за умовою (колір, к-сть комбо, форма), `timer(+n)` до руху, поле 7×6, «no skyfall» (?) — правило гри залежить від складу команди.
- Посилені кулі: у збігу підсилюють шкоду групи (+% за кулю (?)); зʼявляються від скілів/awakenings.
- Перемога: пройти всі поверхи. Поразка: HP команди 0. Рахунок: у ранкінг-данжах — очки за час, комбо, склад (?).

## Керування і ввід
- Тач: торкнутись кулі і вести палець; куля «пливе» за пальцем, сусідні міняються місцями миттєво при перетині межі клітини. Відпустити — кінець ходу.
- Вісь керування — новий тип: `drag-path` (один жест = ланцюг обмінів), не `swap` двох сусідніх (Bejeweled).
- Тап по портрету монстра — active skill (з підтвердженням).
- Між ходами — без таймера; таймер лише під час перетягування.

## Вікна, меню, HUD
- `main-menu`/хаб: Dungeons · Monsters (команди) · Egg Machine · Shop · Friends · Info (?).
- `+window:dungeon-select` — список данжів (Normal, Technical, Special, Challenge, Ranking, Multiplayer) → поверхи; витрати stamina.
- `custom: «helper-select»` — вибір хелпера (монстр друга як другий лідер).
- `+window:team-builder` — 5 слотів команди + лідер, сумарні HP/RCV.
- `game-screen`: вороги зверху з `hp-bar`, атрибутом і лічильником ходів (`+ui:enemy-turn-counter`); портрети команди з готовністю скілів; `hp-bar` команди; поле; `+ui:drag-timer` (смужка часу при перетягуванні); `combo-meter` («N Combo») під час каскаду; номер поверху (`wave-counter`).
- `game-over-continue` — продовжити за magic stone.
- `end-screen` данжу: досвід, ранг, дропи монстрів, монети.
- `+window:gacha-window` — Egg Machine: витратити magic stones → випадковий монстр з анімацією яйця.
- `shop-window` — magic stones за реальні гроші; stamina, місце в «коробці», слоти друзів.
- Переходи: хаб → dungeon-select → helper-select → game-screen (поверхи) → end-screen → хаб; Monsters → team-builder / fuse / evolve.

## Фічі поза полем
- `meta-progression`: досвід і рівень монстрів, злиття (fuse) для досвіду й рівня скіла, еволюції з матеріалів, awakenings (пасивні бонуси), latent awakenings.
- `xp-level` гравця (Rank) → більше stamina і вартість команди.
- Енергія `stamina`, що відновлюється в реальному часі; `round-currency` (coins, pal points, monster points) + преміум magic stones.
- Гача (Egg Machine), `daily`/події, `online-multiplayer` (кооп, 4-гравці PvP), ранкінг-данжі з `leaderboard-online`.
- `cloud-save` (акаунт), `tutorial`.

## Варіації й родичі
- PAD Z (3DS, 2013), PAD Super Mario Bros. Edition (3DS, 2015), PAD GO (Switch, 2023), PAD Story (2022); численні клони: Monster Strike — інший жанр, Tower of Saviors — майже клон PAD (?).
- Родичі match-RPG: Puzzle Quest (swap 2 сусідніх, бій), Dungeon Raid (малювання шляху по сусідніх однакових), Marvel Puzzle Quest.
- **Осі варіацій**: перестановка (swap сусідніх / ланцюг обмінів шляхом / обертання 2×2) · обмеження ходу (без ліміту / таймер руху / ліміт обмінів) · одиниця атаки (група / комбо) · поповнення (skyfall випадковий / без skyfall / задане) · розмір поля (5×4 / 6×5 / 7×6) · правила від команди (лідер-скіли).

## Цікавинки для курсу
- Drag-шлях: куля «пливе», кожен перетин клітини — swap; таймер з першого обміну — 📎.
- Пошук усіх ліній 3+, обʼєднання звʼязаних у комбо (flood fill по позначених) — 📎.
- Каскад skyfall із підрахунком комбо — 🥉.
- Формула шкоди: колір × група × комбо × лідер × стихія як дані-таблиці — 📎.
- Вороги з лічильником ходів до атаки — `telegraphed-intents` 🥉.
- Лідер-скіли як модифікатори правил (час, поле 7×6, множники) — 🥈.
- Розвʼязувач «найкращий шлях за N обмінів» (beam search) — 👑.

## Мапа на каталог
- Є: `drag-drop-piece` (найближча: перетягування) · `gravity-fall` · `combo-multiplier` · `event-points` · `hp-damage` (команда і вороги) · `telegraphed-intents` (лічильник ходів ворога) · `enemy-waves` (поверхи) · `round-currency` + `shop-window` · `save-progress`.
- **Нема** → пропозиції карток:
  - `+drag-path-swap` «Перетягнути плитку шляхом, міняючись з кожною» · interface/input · 🥉 · слоти {diagonals: yes|no, max_swaps}.
  - `+line-match-clear` — ⏳ підтверджую (Dr. Mario, Magical Drop), тут {min: 3, merge_touching: yes}.
  - `+chain-reaction` · `+cascade-gravity` — ⏳ підтверджую.
  - `+skyfall-refill` «Поповнення поля згори випадковими» · entities/spawn · 🌱 (match-3 загалом).
  - `+move-timer-drag` «Таймер жесту з першої дії» · game-logic/opponent · 🌱.
  - `+team-loadout` «Склад команди перед рівнем» · game-logic/economy · 🥉.
  - `+leader-skill-rules` «Пасивні модифікатори правил від складу» · game-logic/difficulty · 🥈.
  - `+active-skill-cooldown` «Активна навичка з перезарядкою в ходах» · entities/state · 📎.
  - `+board-hazards` «Ворожі ефекти на клітинах поля» · entities/interact · 🥉 (jammer, poison, lock, blind, tape, spinner).
  - `+gacha-draw` «Випадкова винагорода за валюту» · game-logic/economy · 📎.
  - `+stamina-energy` «Енергія на вхід, відновлюється в реальному часі» · game-logic/economy · 🌱 (≈ `+turn-limit-energy` з Triple Town).

## Пропозиції до словників
- `+trigger:input` (drag/release) · `+trigger:pattern` · `+trigger:settled` · `+trigger:turn_end` · `+trigger:counter` (CD ворога = 0).
- `+cond:same` · `+cond:chain` (лідер-скіли «від N комбо») · `+cond:timer`.
- `+effect:swap` · `+effect:clear` · `+effect:spawn_at` (skyfall) · `+effect:damage` ✅ · `+effect:heal` · `+effect:set_cell` (перефарбування куль) · `+effect:timer` (±час руху).
- `+role:tile` · `+role:ally` (монстри команди) · `+role:boss`.
- `+ui:hp-bar` · `+ui:combo-meter` · `+ui:drag-timer` (смужка часу жесту) · `+ui:enemy-turn-counter`.
- `+window:team-builder` · `+window:dungeon-select` · `+window:gacha-window`.
- `+feature:stamina` — енергія, що відновлюється з часом.
- `+axis:control` — `drag-path`.

## Джерела
- ⭐ [Wikipedia: Puzzle & Dragons](https://en.wikipedia.org/wiki/Puzzle_%26_Dragons) — поле 6×5, кулі, перетягування з таймером (5 с), комбо, skyfall, 5+ куль — по всіх, стихії, команда з лідером, active skills, awakenings, данжі, stamina, Egg Machine.
- [PAD NA: Ver. 21.7](https://www.puzzleanddragons.us/single-post/ver-21-7-update-241023) — час руху 5 → 6 с, awoken skills від 14 комбо.
- [PAD NA: турнір з часом руху 99 с](https://www.puzzleanddragons.us/single-post/ninegaruda-tournament-orb-move-time-99-sec) — правило «час руху» як параметр події.
- YouTube: пошук «puzzle and dragons combo gameplay».

## Непевне
- (?) Базовий час руху: Wikipedia — 5 с, спільнота пам'ятає 4 с; Switch/3DS — інакше; патч 21.7 — «5 → 6» (контекст неясний).
- (?) Формула шкоди (+25 % за кулю понад 3, +25 % за комбо) і бонус посиленої кулі — з памʼяті, не перевірено.
- (?) Перелік ворожих ефектів (blind, tape, cloud, spinner, locked) і поле 5×4 — з памʼяті; Wikipedia згадує лише block і poison.
- (?) Чи рухається куля по діагоналі між клітинами — так з памʼяті.
- Фан-вікі (fandom) недоступні (402), WebSearch-бюджет вичерпано.
