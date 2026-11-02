---
title: Stratego (Стратего)
slug: stratego
family: hidden-deduction
also: [chess-abstract, tactics]
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: hidden
  random: none
  goal: state
year: 1946
platforms: [board (Smeets & Schippers 1946, Milton Bradley 1961, Jumbo), Electronic Stratego (1982), TI-99/4 (1979), PC (Accolade 1990), Nintendo DS, web, mobile]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Stratego", best: true, note: "правила, склад 40 фігур, нумерації рангів, two-square rule, варіанти, DeepNash"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Stratego_(video_game)", note: "Accolade 1990 — однокористувацька комп'ютерна версія"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Gunjin_Sh%C5%8Dgi", note: "японський родич з суддею: ранги не розкриваються навіть при бою"}
  - {kind: other, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=stratego", note: "пошук BGG; видання й варіанти"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=stratego", note: "пошук; цифрові видання"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=stratego+rules+how+to+play", note: "пошук; правила"}
  - {kind: other, url: "https://en.wikipedia.org/w/index.php?search=DeepNash&ns0=1", note: "пошук; AI DeepNash (DeepMind, 2022)"}
stage: v1
coverage: 75
mechanics: [piece-move-patterns, piece-capture, impassable-cells, legal-move-highlight, drag-drop-piece, cell-click, hot-seat, turn-enforcement, ai-opponent, ai-random, ai-greedy, no-moves-left, game-screen, end-screen, main-menu, settings-window, help-window, save-game, replay, sound-effects, +hidden-rank-reveal, +rank-combat, +bomb-defuse, +spy-assassin, +any-distance-slide, +capture-flag, +repetition-limit, +setup-zone-placement, +setup-presets, +dual-board-view]
proposes: ["+trigger:attack", "+trigger:placement_done", "+cond:rank_cmp", "+cond:repetition", "+effect:reveal", "+effect:disappear_both", "+role:piece", "+ui:piece-rank-reveal", "+ui:graveyard", "+ui:last-move-arrow", "+window:placement-screen", "+window:pass-device", "+feature:setup-presets", "+feature:fog-of-ranks", "+card:hidden-rank-reveal", "+card:rank-combat", "+card:bomb-defuse", "+card:spy-assassin", "+card:any-distance-slide", "+card:capture-flag", "+card:repetition-limit", "+card:setup-zone-placement", "+card:setup-presets"]
author: opus
date: 2026-11-02
---

# Stratego — армії з прихованими рангами: атакуй, щоб дізнатися, і захопи прапор

## Суть
Двоє гравців розставляють по 40 фігур у своїх 4 рядах обличчям до себе — супротивник бачить лише «спинки». Фігури ходять на 1 клітину, атака розкриває обидва ранги, слабша фігура гине (рівні — обидві). Мета — захопити прапор суперника або лишити його без ходів. Ядро — дедукція і блеф: ти стежиш, які фігури рухались (значить, не бомби і не прапор), які виграли бій, і підставляєш «наживку», щоб викрити маршала.

## Поле і час
- Дошка 10×10, у центрі два «озера» 2×2 (ряди 5–6, стовпці 3–4 і 7–8) — непрохідні; між ними три «коридори» по 2 клітини.
- Зони розстановки: 4×10 біля кожного гравця; два центральні ряди порожні на старті.
- Шари: фігура (сторона + ранг) + стан «розкрито / приховано для суперника»; у настолці — фізично «спинка», у цифровій — `fog-of-ranks`.
- Покроково: хід = рух однією фігурою (зокрема атака). Дві фази: розстановка (одночасна, прихована) → гра. Середня партія — ~381 хід.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Маршал | piece | ранг 10 (стара США: 1), ×1 | найсильніший; гине лише від бомби, рівного маршала або шпигуна, що атакує |
| Генерал | piece | 9, ×1 | рух 1 ортогонально |
| Полковник | piece | 8, ×2 | те саме |
| Майор | piece | 7, ×3 | те саме |
| Капітан | piece | 6, ×4 | те саме |
| Лейтенант | piece | 5, ×4 | те саме |
| Сержант | piece | 4, ×4 | те саме |
| Сапер (Miner) | piece | 3, ×5 | рух 1; атакуючи бомбу — знешкоджує її |
| Розвідник (Scout) | piece | 2, ×8 | будь-яку відстань по прямій без перескоків (як тура) |
| Шпигун (Spy) | piece | S (2000-нумерація: 1), ×1 | атакуючи маршала — вбиває; будь-яка інша атака на нього або ним — гине |
| Бомба | piece | B, ×6, нерухома | будь-який атакувальник, крім сапера, гине; бомба лишається |
| Прапор | piece | F, ×1, нерухомий | захоплення = перемога |
| Озеро | static | 2×2 ×2 | непрохідне для всіх, розвідник не перелітає |
| Порожня клітина | static | — | хід лише на порожню або ворожу |

## Правила (КОЛИ → ЯКЩО → ТО)
- Розстановка: КОЛИ `input(place, piece, cell)` → ЯКЩО клітина у своїй зоні 4×10 і `free(cell)` → ТО фігура стає; КОЛИ всі 40 стоять → `custom: «Готово»`; КОЛИ обидві сторони готові → `turn_start(red)` (червоні ходять першими).
- КОЛИ `input(move, piece, to)` → ЯКЩО `turn_of(side)` і фігура не бомба/прапор → далі:
  - ЯКЩО звичайна фігура → `legal(to)` = сусідня ортогональна клітина; розвідник — будь-яка по прямій, `free` усі проміжні (без озер і фігур).
  - ЯКЩО `occupied(to, own)` або `cell(to, lake)` → `block`.
  - ЯКЩО `free(to)` → `move(piece, to)`; ЯКЩО `occupied(to, enemy)` → атака.
- Атака: КОЛИ `custom: «атака A на D»` → ТО `reveal(A)`, `reveal(D)`, далі:
  - ЯКЩО D — прапор → `win`.
  - ЯКЩО D — бомба → ЯКЩО A — сапер → `disappear_b`, `move(A, to)`; інакше `disappear_a`.
  - ЯКЩО A — шпигун і D — маршал → `disappear_b`, `move(A, to)`.
  - ЯКЩО `rank(A) > rank(D)` → `disappear_b`, `move(A, to)`; ЯКЩО менше → `disappear_a`; ЯКЩО рівні → `disappear_both`.
- Розвідник: у старих правилах не міг рухатись і атакувати за один хід (атакував лише на сусіда); у нових — може атакувати в кінці дальнього ходу.
- Переможець бою лишається розкритим для суперника до кінця (у настолці гравець просто памʼятає; у цифровій — фігура показує ранг).
- Two-square rule: КОЛИ `input(move)` → ЯКЩО `custom: «фігура ходить туди-сюди між тими самими двома клітинами більше ніж 3 ходи поспіль»` → ТО `block`. More-square rule: заборона нескінченно переслідувати фігуру, яку не можеш атакувати.
- КОЛИ `turn_start(side)` → ЯКЩО `no_moves(side)` (лишились лише бомби і прапор або всі заблоковані) → ТО `lose(side)`.
- Нічия: рідкісні випадки (обидва прапори за бомбами, а в кожного лишилась одна не-сапер фігура) — `draw`.
- Перемога: захопити прапор або лишити суперника без ходів · Поразка: навпаки · Рахунок: нема (турніри — очки за партії).

## Керування і ввід
- Розстановка (цифрова версія): drag фігури з лотка на клітину зони, swap двох фігур кліком, кнопки «Випадково» і «Завантажити розстановку».
- Хід: клік по своїй фігурі → підсвітка легальних клітин → клік по цілі (або drag). Атака — той самий ввід на ворожу клітину; потім анімація розкриття обох фігур.
- Hotseat: між ходами завіса, щоб суперник не бачив твої ранги. Настолка — розв'язує це фізичними «спинками».

## Вікна, меню, HUD
- `main-menu` (цифрова версія): Грати з AI → `difficulty-select`; Онлайн → `lobby-window`; Удвох (hotseat); Правила → `help-window`; Налаштування → `settings-window` (класичні / нові ранги, правило розвідника, two-square rule).
- `placement-screen` (кандидат): своя зона 4×10, лоток фігур з лічильниками, збережені розстановки (`setup-presets`), «Випадково», «Готово».
- `game-screen`: дошка з озерами; свої фігури з рангами, ворожі — спинки (розкриті — з рангом); `turn-indicator`; `graveyard` (вбиті фігури обох сторін з лічильниками «лишилось 3 сапери»); `last-move-arrow`; `legal-move-highlight`; `message-log` боїв («Капітан → Лейтенант: переміг»).
- Бій: `toast`/модал розкриття двох фігур з результатом.
- `pass-device` (кандидат, hotseat).
- `end-screen`: переможець, причина (прапор / нема ходів), повне розкриття армії суперника, `replay-window`.
- Переходи: main-menu → placement-screen → game-screen ↔ pass-device → end-screen → replay / main-menu.

## Фічі поза полем
- `ai-opponent-levels`; сучасна вершина — DeepNash (DeepMind, 2022: 84 % перемог у 50 рейтингових онлайн-іграх проти людей; ≥97 % проти попередніх програм на кшталт Probe); 2026 — Ataraxos обіграв чемпіона світу 15–1 (?).
- `setup-presets`: збережені розстановки — у Stratego це окрема «мета-гра» (прапор у кутку за бомбами, блеф-бомби).
- `custom-rules`: нумерація рангів, правило розвідника, варіанти складу армії (Ultimate Lightning — 20 фігур, Duel — 10 фігур на 8×10, Barrage — 8 фігур).
- `online-multiplayer`, `hotseat`, `replay`, `save-game`, `turn-timer` (турніри), `stats`.
- Electronic Stratego (1982): поле 8×10, 24 фігури, сенсорна дошка, кнопка «probe» — компʼютер сам вирішує бої (приховані бомби — у кілочках).

## Варіації й родичі
- L'Attaque (Hermance Edan, патент 1908, продаж 1910) → Stratego (Mogendorff, до 1942; ліцензія 1946) → Milton Bradley (США, 1961) → Jumbo (з 2009).
- Варіанти: Ultimate Lightning, Duel (8×10), Barrage (8 фігур, турнірні тайбрейки), Waterloo, Fire and Ice, Conquest, Fortress — нові фігури зі спецздібностями.
- Gunjin Shōgi (Японія): потрібен суддя, який порівнює ранги таємно — гравці навіть після бою не бачать, хто це був. Jungle (Dou Shou Qi, Китай): та сама ієрархія рангів, але все відкрито.
- **Осі варіацій**: розкриття рангу при бою «обом / лише результат (суддя) / все відкрито»; рух розвідника «як тура / 1 клітина»; бій «більший виграє / цикл (шпигун-маршал) / спецфігури»; нерухомі фігури «бомби + прапор / лише прапор».
- Родичі за прихованістю: Battleship (приховане розміщення без руху), Kriegspiel (шахи наосліп з суддею).

## Цікавинки для курсу
- Туман рангів: дві проєкції одного стану (своя армія з рангами / чужа — спинки + розкриті) — 🥉.
- Таблиця бою з винятками (шпигун-атакує-маршала, сапер-бомба, рівні гинуть обидві) — 📎, добрий кандидат на `interaction-table`.
- Розвідник «як тура» з перевіркою проміжних клітин і озер — 📎.
- Фаза розстановки в зоні 4×10 з лотком, «Випадково» і збереженими пресетами — 🥉.
- Two-square rule: історія ходів фігури і заборона повтору — 🥉.
- AI з моделлю переконань («ця фігура не рухалась → ймовірно бомба/прапор») — 🥇; рівня DeepNash — 👑.
- Hotseat із завісою між ходами — 📎.

## Мапа на каталог
- Є: `piece-move-patterns` (1 клітина / розвідник) · `piece-capture` (бій) · `impassable-cells` (озера) · `legal-move-highlight` · `drag-drop-piece` + `cell-click` · `hot-seat` + `turn-enforcement` · `ai-opponent` / `ai-random` / `ai-greedy` · `no-moves-left` (поразка без ходів) · `save-game` · `replay` · `sound-effects` · `game-screen` / `end-screen` / `main-menu` / `settings-window` / `help-window`.
- **Нема** → пропозиції карток:
  - `+hidden-rank-reveal` «Прихований ранг, розкриття в бою» · entities/state · 🥉 · слот {reveal: both|result-only}.
  - `+rank-combat` «Бій за рангом» · entities/combat · 📎 · слот {tie: both-die|defender-wins}.
  - `+bomb-defuse` «Нерухома пастка і фігура-знешкоджувач» · entities/combat · 🌱.
  - `+spy-assassin` «Слабка фігура вбиває найсильнішу лише атакуючи» · entities/combat · 🌱.
  - `+any-distance-slide` «Хід на будь-яку відстань по прямій» · entities/move · 📎 (розвідник; тура в шахах — `piece-move-patterns`).
  - `+capture-flag` «Захопити прапор» · game-logic/win · 🌱.
  - `+repetition-limit` «Заборона повтору ходів» · game-logic/constraints · 🥉 · слот {max: 3}.
  - `+setup-zone-placement` «Розстановка у своїй зоні перед грою» · entities/legality · 📎.
  - `+setup-presets` «Збережені розстановки» · game-logic/save · 📎.
  - `+dual-board-view` — див. Battleship.

## Пропозиції до словників
- `+trigger:attack` — фігура пішла на ворожу клітину (окремо від `contact`, бо результат вирішує таблиця бою, а не сам дотик).
- `+trigger:placement_done` — кінець фази розстановки (див. Battleship).
- `+cond:rank_cmp` — порівняння рангів двох фігур з винятками.
- `+cond:repetition` — хід повторює попередні N ходів (two-square rule, шахове троєкратне).
- `+effect:reveal` — ⏳, тут: відкрити ранг фігури супернику; `+effect:disappear_both` — ✅, рівні ранги.
- `+role:piece` — усі фігури.
- `+ui:piece-rank-reveal` — фігура суперника показує ранг після бою; `+ui:graveyard` — вбиті фігури з лічильниками за рангами; `+ui:last-move-arrow` — стрілка останнього ходу суперника.
- `+window:placement-screen` · `+window:pass-device` — див. Battleship.
- `+feature:setup-presets` — збережені розстановки; `+feature:fog-of-ranks` — режим прихованих рангів у цифровій версії.

## Джерела
- ⭐ [Wikipedia: Stratego](https://en.wikipedia.org/wiki/Stratego) — історія, дошка й озера, склад армії, обидві нумерації, рух, бій, бомби/сапери/шпигун, two-square і more-square rule, варіанти, Electronic Stratego, DeepNash.
- [Wikipedia: Stratego (video game)](https://en.wikipedia.org/wiki/Stratego_(video_game)) — Accolade 1990.
- [Wikipedia: Gunjin Shōgi](https://en.wikipedia.org/wiki/Gunjin_Sh%C5%8Dgi) — родич із суддею.
- [BGG пошук](https://boardgamegeek.com/geeksearch.php?action=search&q=stratego) · [Steam пошук](https://store.steampowered.com/search/?term=stratego) — видання, цифрові версії.
- YouTube: пошук «stratego rules how to play»; Wikipedia-пошук «DeepNash».

## Непевне
- (?) Точні позиції озер (стовпці 3–4 і 7–8) — з памʼяті про дошку; Wikipedia каже лише «два 2×2 у центрі».
- (?) Хто ходить першим (червоні) — за класичними правилами, не перевірено цього разу.
- (?) Ataraxos 2026 — згадка у Wikipedia, деталей не дивився.
- (?) Сучасні офіційні цифрові видання Jumbo (Steam, мобільні) — лише пошукові лінки.
