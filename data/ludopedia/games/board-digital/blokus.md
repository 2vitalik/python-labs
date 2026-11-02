---
title: Blokus (Блокус)
slug: blokus
family: board-digital
also: [chess-abstract]
klass: cursor
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: territory
year: 2000
platforms: [board, PC, mobile, PSP, PS3]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Blokus", best: true, note: "правила, підрахунок, варіанти Duo/Trigon/Junior/3D, цифрові версії"}
  - {kind: other, url: "https://www.ultraboardgames.com/blokus/game-rules.php", note: "правила з прикладом підрахунку, склад набору фігур"}
  - {kind: play, url: "https://pentobi.sourceforge.io/", note: "Pentobi — відкритий движок і GUI: Classic, Duo, Trigon, Junior, сильний AI"}
  - {kind: wiki, url: "https://de.wikipedia.org/wiki/Blokus", note: "склад фігур 1+1+2+5+12, гра вдвох чотирма кольорами, нагороди"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Blokus+how+to+play", note: "пошук; пояснення правил"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Blokus", note: "пошук; офіційного Steam-видання не бачив"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=Blokus", note: "пошук BGG"}
stage: v1
coverage: 70
mechanics: [cell-click, drag-drop-piece, hover-highlight, legal-move-highlight, turn-enforcement, hot-seat, ai-opponent, ai-greedy, no-moves-left, event-points, completion-detection, save-game, replay, game-settings, field-size-picker, +polyomino-placement, +piece-rotate-flip, +corner-contact-rule, +start-cell-rule, +skip-blocked-player, +leftover-penalty, +multi-color-control]
proposes: ["+effect:place", "+cond:fits", "+cond:corner_touch", "+cond:edge_touch", "+role:supply", "+ui:piece-tray", "+window:match-setup", "+feature:rated-games", "+axis:turn-structure"]
author: opus
date: 2026-11-02
---

# Blokus — виклади якомога більше поліоміно, торкаючись свого кольору лише кутами

## Суть
Чотири кольори по 21 фігурі (усі вільні поліоміно з 1–5 клітин) по черзі викладаються на спільне поле 20×20. Своя нова фігура мусить торкатися своїх лише **кутом** і ніколи ребром; чужих кольорів правило не стосується. Хто не може походити — вибуває з черги; рахунок — мінус клітини, що лишились у лотку. Ядро — боротьба за «діагональні входи»: ти розширюєшся кутами й перекриваєш чужі кути.

## Поле і час
- Поле 20×20 = 400 клітин, без шарів; кожна клітина порожня або зайнята кольором. Фігура після викладання не рухається.
- Хід = викласти одну фігуру (або пропуск, якщо легального ходу нема). Порядок кольорів: синій → жовтий → червоний → зелений.
- Чотири кутові клітини поля — стартові: перша фігура кольору мусить накрити «свій» кут.
- Варіанти поля: Duo/Junior 14×14 зі стартовими клітинами ближче до центру; Trigon — шестикутне поле з трикутних клітин; Blokus 3D (Rumis) — полікуби з гравітацією.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фігура (поліоміно) | piece | колір, форма з 1–5 клітин, 8 орієнтацій | викладається один раз, не рухається |
| Лоток кольору | supply | 21 фігура: 1 моно, 1 доміно, 2 тріміно, 5 тетраміно, 12 пентаміно = 89 клітин | джерело фігур; залишок рахується в штраф |
| Клітина поля | static | порожня / колір | займається фігурою; не звільняється |
| Стартовий кут | static | один на колір (Classic) | перша фігура кольору мусить його накрити |
| Колір (сторона) | player | синій, жовтий, червоний, зелений; стан active/blocked | ходить у порядку; blocked — пропускає до кінця |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place(piece, cells))` → ЯКЩО `turn_of(color)` and `fits(piece, cells)` (у межах поля, без перекриття) → ТО `place(piece, cells)`, `end_turn`; інакше `block`.
- КОЛИ перший хід кольору → ЯКЩО `custom: «фігура накриває стартовий кут кольору»` → ТО `place`; інакше `block`.
- КОЛИ не перший хід → ЯКЩО `corner_touch(piece, own)` and `not edge_touch(piece, own)` → ТО `place`; інакше `block`.
- Контакт з чужими кольорами — будь-який (ребром і кутом), правило його не перевіряє.
- КОЛИ `turn_start(color)` → ЯКЩО `no_moves(color)` → ТО `set_state(color, blocked)`, `pass_turn` (до кінця гри).
- КОЛИ `custom: «усі кольори blocked або лотки порожні»` → ТО `game_over`.
- Рахунок (базовий): `score(-1)` за кожну клітину фігур у лотку; виклав усі 21 → `score(+15)`; останньою була мономіно → ще `score(+5)`. Максимум +20.
- Перемога: найбільший рахунок; удвох — кожен гравець веде два кольори (синій+червоний проти жовтого+зеленого), рахунки сумуються.
- Duo: перша фігура мусить накрити свою стартову клітину біля центру; далі ті самі правила кута/ребра.

## Керування і ввід
- Вибрати фігуру з лотка → повернути (90°) / віддзеркалити → навести на поле → клік або drag-drop; невдале розташування відхиляється.
- Пропуск — автоматичний, коли легальних ходів нема (у цифрових версіях) або оголошується вголос (настільна).
- Удвох: гравець по черзі керує двома своїми кольорами в загальному порядку синій → жовтий → червоний → зелений.

## Вікна, меню, HUD
(цифрова версія — за Pentobi та мобільними версіями)
- `main-menu` / меню-бар: Нова гра · вибір варіанта (Classic, Classic 2 гравці, Duo, Trigon, Junior) · Рейтингова гра · Відкрити/Зберегти · Вихід.
- `match-setup` (кандидат): варіант правил, хто якими кольорами грає (людина/компʼютер), рівень AI.
- `game-screen`: поле 20×20 з `grid-lines`; `piece-tray` для кожного кольору (лишились фігури); `score` кожного кольору наживо; `turn-indicator` (рамка навколо лотка кольору, що ходить); `selection-highlight` вибраної фігури; `drag-ghost`/`hover-highlight` — тінь фігури під курсором (червона, якщо нелегально); кнопки поворот/віддзеркалення; `move-counter`.
- `end-screen`: таблиця очок кольорів із розкладкою «залишок / +15 / +5», переможець.
- `stats-window` / рейтинг (Pentobi): Elo-подібний рейтинг за рейтингові партії проти AI.
- `replay-window` / аналіз (Pentobi): прокрутка ходів, граф оцінки позиції, варіації у SGF.
- `help-window`: правила; `about-window`.
- Переходи: main-menu → match-setup → game-screen → end-screen → (нова гра) match-setup.

## Фічі поза полем
- `ai-opponent-levels` (Pentobi: кілька рівнів), `hotseat` (кілька людей за одним пристроєм), `online-multiplayer` (історичні офіційні версії, закриті 2012–2018).
- `undo` (Pentobi: відмінити хід), `hint` («знайти хід» від AI), `save-slots`/`export-import` — партія у форматі SGF з коментарями й варіаціями.
- `custom-rules` як вибір варіанта (Classic/Duo/Trigon/Junior) — одна механіка на різних полях і наборах фігур.
- `stats` + рейтинг гравця (`+feature:rated-games`).

## Варіації й родичі
- **Blokus Duo** (2005): 14×14, 2 гравці, старт біля центру — фігури різних гравців стикаються вже з другого ходу.
- **Blokus Trigon** (2006): поліаманти на трикутній сітці шестикутного поля; дозволено контакт «кут-до-ребра».
- **Blokus Junior**: 14×14, 12 простіших фігур по 2 копії, пазл-аркуші для одного гравця.
- **Blokus 3D / Rumis**: полікуби 2–4, контакт гранню, заборона порожнечі під фігурою, фіксовані «будови» (вежа, піраміда).
- Родичі: Patchwork і Cathedral (поліоміно на сітці), пентаміно-пазли, Tetris (ті самі форми, але падіння).
- **Осі варіацій**: правило контакту зі своїми (лише кут / лише ребро / будь-яке) · тип клітини (квадрат / трикутник / куб) · старт (кути поля / біля центру) · сторона (гравець = колір / гравець = 2 кольори) · рахунок (залишок / покрита площа / видимі грані).

## Цікавинки для курсу
- Генерація 8 орієнтацій поліоміно (поворот + дзеркало) з нормалізацією й дедуплікацією — 📎 (класична вправа на множини координат).
- Перевірка легальності ходу: межі + перекриття + «кут так, ребро ні» — 🥉 (кілька шарів умов на одну дію).
- `no_moves`: перебір усіх фігур × орієнтацій × «кутових якорів» свого кольору — 🥈 (потрібна оптимізація через список діагональних точок-кандидатів).
- AI: жадібний (найбільша фігура / найбільше нових кутів) — 🥉; MCTS/minimax рівня Pentobi — 🥇.
- Режим «два кольори на гравця» і сумарний рахунок — 🌱, але гарна вправа на відокремлення «сторони» від «гравця».
- Варіант Trigon (трикутна сітка, інша суміжність) — 🥇 (зміна топології при тій самій логіці правил).

## Мапа на каталог
- Є: `cell-click` · `drag-drop-piece` · `hover-highlight` (тінь фігури) · `legal-move-highlight` · `turn-enforcement` (порядок кольорів) · `hot-seat` · `ai-opponent` + `ai-greedy` · `no-moves-left` (тут — вибування кольору, не програш) · `event-points` (+15/+5) · `completion-detection` (кінець гри, коли всі заблоковані) · `save-game` · `replay` · `game-settings` + `field-size-picker` (Classic 20×20 / Duo 14×14).
- **Нема** → пропозиції карток:
  - `+polyomino-placement` «Викладання поліоміно на сітку» · entities/legality · 🥉 · слот {shapes: list} — межі + перекриття (спільна з Patchwork, Tiny Towns).
  - `+piece-rotate-flip` «Поворот і дзеркало фігури» · entities/state · 📎 — 8 орієнтацій, нормалізація.
  - `+corner-contact-rule` «Контакт зі своїми лише кутом» · entities/legality · 🥉 · слот {contact: corner|edge|any}.
  - `+start-cell-rule` «Перша фігура на стартову клітину» · entities/legality · 🌱.
  - `+skip-blocked-player` «Заблокований вибуває з черги» · game-logic/opponent · 📎.
  - `+leftover-penalty` «Штраф за невикладене» · game-logic/score · 🌱 · слот {per_cell} — Blokus, Patchwork (порожні клітини), Tiny Towns.
  - `+multi-color-control` «Гравець веде кілька сторін» · game-logic/opponent · 🌱.

## Пропозиції до словників
- `+effect:place` — покласти фігуру на набір клітин поля (Blokus, Patchwork, Tiny Towns).
- `+cond:fits` — фігура в цій орієнтації вміщається: у межах поля, без перекриття.
- `+cond:corner_touch` / `+cond:edge_touch` — фігура торкається сутностей виду кутом / ребром.
- `+role:supply` — запас/лоток/вітрина, з якої беруть фігури чи ресурси (лоток Blokus, коло латок Patchwork, фабрики Azul).
- `+ui:piece-tray` — панель фігур, що лишились у гравця (з поворотом/дзеркалом).
- `+window:match-setup` — налаштування партії: варіант, хто якою стороною, рівень AI (вже пропонувалось іншими).
- `+feature:rated-games` — рейтинг гравця за рейтингові партії проти AI.
- `+axis:turn-structure` — `alternate` (по черзі, тут) · `time-track` (Patchwork) · `simultaneous` (Tiny Towns).

## Джерела
- ⭐ [Wikipedia: Blokus](https://en.wikipedia.org/wiki/Blokus) — поле 20×20, 84 фігури, кут/ребро, підрахунок +15/+5, Duo/Trigon/Junior/3D, історія цифрових версій.
- [UltraBoardGames: Blokus rules](https://www.ultraboardgames.com/blokus/game-rules.php) — склад набору (1/1/2/5/12), порядок кольорів, приклад підрахунку.
- [Wikipedia DE: Blokus](https://de.wikipedia.org/wiki/Blokus) — удвох чотирма кольорами (синій+червоний / жовтий+зелений), нагороди.
- [Pentobi](https://pentobi.sourceforge.io/) — відкрита реалізація з AI, рейтингом, аналізом партій і SGF.
- YouTube: пошук «Blokus how to play».

## Непевне
- (?) Точні стартові клітини Duo — (5,10) і (10,5) за нотацією Pentobi (e10, j5) — з памʼяті; сторінки правил Duo не дістав.
- (?) Деталі UI Pentobi (кнопки поворот/дзеркало, «знайти хід», undo) — з памʼяті, на головній сторінці не описані.
- (?) Правило для 3 гравців: Wikipedia — четвертий колір кладеться «не стратегічно»; поширений хатній варіант — гравці ходять ним по черзі.
- (?) Офіційного Steam-видання не перевірив; цифрові версії (Gameloft, Magmic, онлайн Mattel) закриті.
