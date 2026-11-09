---
title: Taluva (Талува)
slug: taluva
aka: [Талува, Taluva Deluxe]
family: board-digital
also: [build-sim]
klass: cursor
axes:
  field: layers
  time: turn
  opponent: hotseat
  info: full
  random: runtime
  goal: race
year: 2006
platforms: [board, web]
links:
  - {kind: other, url: "https://www.ultraboardgames.com/taluva/game-rules.php", best: true, note: "повні правила: розширення/виверження, умови накриття, 4 будівельні дії, вибування, дострокова перемога, тайбрейки, варіант рангу"}
  - {kind: play, url: "https://en.boardgamearena.com/gamepanel?game=taluva", note: "BGA: 2–5 гравців, 20 хатин / 3 храми / 2 вежі, грати в браузері (3D)"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=Taluva", note: "пошук BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Taluva+how+to+play", note: "пошук; пояснення правил"}
stage: v1
coverage: 70
mechanics: [cell-click, drag-drop-piece, hover-highlight, legal-move-highlight, turn-enforcement, hot-seat, ai-opponent, online-multiplayer, no-moves-left, connectivity-check, game-settings, match-setup, game-screen, end-screen, help-window, +hex-grid-render, +tri-hex-tile, +tile-rotate, +connected-placement, +stack-over-rule, +support-rule, +cover-destroys, +protected-from-cover, +group-split, +flood-expand-group, +level-cost-placement, +group-size-gate, +one-per-group, +height-gate, +exhaust-two-types-win, +player-elimination, +tiebreak-chain, +camera-3d-orbit]
proposes: ["+cond:height", "+cond:group_has", "+cond:orientation_differs", "+effect:eliminate", "+trigger:tiles_exhausted", "+ui:height-badge", "+ui:piece-stock", "+ui:camera-orbit", "+card:flood-expand-group", "+card:cover-destroys", "+card:exhaust-two-types-win", "+axis:field=hex+layers"]
author: opus
date: 2026-11-09
---

# Taluva — тайли з трьох гексів з вулканом будують острів і вивергаються поверх: висота дає право на вежі, а виверження нищить чужі хатини

## Суть
Кожен хід — два кроки: витягти тайл (3 гекси: вулкан + дві місцевості) і покласти його або **поруч** (острів росте вшир), або **поверх** уже наявних тайлів (виверження: вулкан на вулкан, рівень +1). Потім гравець мусить поставити хоч одну будівлю: хатину на рівень 1, храм поруч зі своїм поселенням з ≥3 гексів, вежу на рівень ≥3 поруч із поселенням, або «розширити» поселення — заповнити хатинами всі сусідні гекси однієї місцевості (на кожен гекс — стільки хатин, який рівень). Хто першим виставить усі будівлі двох типів із трьох — виграє одразу; не можеш збудувати нічого — вибуваєш. Ядро — тривимірне гекс-поле, що росте й переписується, та групи-поселення, які виверження може розірвати.

## Поле і час
- Гекс-поле без меж, що будується з тайлів; кожен гекс має місцевість (вулкан, джунглі, галявина, пісок, скелі, озеро) і рівень = скільки тайлів під ним.
- Тайл — тріада з 3 гексів трикутником (як в Akropolis); вулкан має «напрям» (куди дивиться кратер) — важливий для виверження.
- Поселення = звʼязна група гексів з будівлями одного кольору; може зливатися й розпадатися.
- Хід = тайл + будівництво; ходять по черзі за годинниковою стрілкою; 48 тайлів — тривалість гри (2–5 гравців за BGA; 2–4 у коробці (?)).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Тайл вулкана | tile | 3 гекси: 1 вулкан + 2 місцевості; поворот | кладеться поруч або поверх; 48 штук у закритому стосі |
| Гекс вулкана | hazard | напрям кратера; рівень | будувати не можна; лише сюди лягає вулкан нового тайла |
| Гекс місцевості | terrain | 5 типів; рівень 1–n | приймає будівлі; рівень = ціна розширення й умова вежі |
| Хатина | piece | 20 на гравця (BGA) | рівень 1 — нове поселення; розширення — n хатин на гекс рівня n; накрита — у коробку |
| Храм | piece | 3 на гравця | поруч із поселенням ≥3 гексів без храму; не накривається |
| Вежа | piece | 2 на гравця | на гекс рівня ≥3 поруч із поселенням без вежі; не накривається |
| Поселення | zone | гекси; чи є храм / вежа | звʼязна група одного кольору; виверження може розділити |
| Стос тайлів | supply | 48 | тягнуть по одному; порожній → кінець гри |
| Запас будівель гравця | supply | хатини / храми / вежі | два типи вичерпано → перемога |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(player)` → ТО `custom: «витягти верхній тайл зі стосу»`.
- КОЛИ `input(place(tile, cells))` → ЯКЩО `custom: «перший тайл гри»` → ТО `place(tile, center)`.
- КОЛИ `input(place(tile, cells))` → ЯКЩО `custom: «розширення: хоч один бік торкається наявного тайла»` і `free(cells)` → ТО `place(tile, cells)` на рівень 1; дірки дозволені.
- КОЛИ `input(place(tile, cells))` → ЯКЩО `custom: «виверження: вулкан тайла лягає на гекс вулкана»` і `custom: «напрям нового вулкана інший, ніж у накритого»` (`+cond:orientation_differs`) і `supported(tile)` → ТО `place(tile, cells)`, `counter(level, +1)` для трьох гексів; інакше `block`.
- КОЛИ `input(place(tile, cells))` → ЯКЩО `occupied(cell, temple)` або `occupied(cell, tower)` → ТО `block`.
- КОЛИ `input(place(tile, cells))` → ЯКЩО `custom: «тайл накрив би всі гекси хоч одного поселення»` → ТО `block`.
- КОЛИ `after(place)` (виверження) → ТО `disappear(covered_huts)` — `custom: «у коробку, не в запас»`; ЯКЩО `not connected(settlement)` → ТО `custom: «поселення розпадається на два»`.
- КОЛИ `input(build(hut, cell))` → ЯКЩО `custom: «рівень гекса = 1»` (`+cond:height`) і `free(cell)` і `not cell(cell, volcano)` → ТО `place(hut, cell)` — нове поселення (або прилипає до наявного).
- КОЛИ `input(build(expand, settlement, terrain))` → ТО `custom: «на КОЖЕН вільний гекс місцевості terrain, сусідній з поселенням, — стільки хатин, який його рівень»`; ЯКЩО `not has(player, huts_needed)` → ТО `block`.
- КОЛИ `input(build(temple, cell))` → ЯКЩО `adjacent_count(cell, settlement, >=, 1)` і `region_size(settlement, >=3)` і `not custom: «у поселенні вже є храм»` (`+cond:group_has`) → ТО `place(temple, cell)`.
- КОЛИ `input(build(tower, cell))` → ЯКЩО `custom: «рівень гекса ≥ 3»` і `adjacent_count(cell, settlement, >=, 1)` і `not custom: «у поселенні вже є вежа»` → ТО `place(tower, cell)`.
- Злиття: КОЛИ `after(place)` → ЯКЩО `custom: «дві свої групи стали сусідами»` → ТО одне поселення (`connected`).
- КОЛИ `no_moves(player)` → ЯКЩО `custom: «після тайла нема жодної легальної будівлі»` → ТО `custom: «гравець вибуває; його будівлі лишаються»` (`+effect:eliminate`), `skip_turn(player)` до кінця.
- КОЛИ `custom: «у гравця вичерпано два з трьох типів будівель»` → ТО `win` одразу.
- КОЛИ `custom: «останній тайл покладено»` (`+trigger:tiles_exhausted`) → ТО `game_over`; переможець — більше храмів → веж → хатин (з накритими в коробці).
- Варіант рангу: КОЛИ `win` → ТО `custom: «переможець — перше місце, решта грає далі»`; вибулі — з кінця таблиці.
- Перемога: перший, хто збудував усі будівлі двох типів · Поразка: вибування (нема легальної будівлі) · Рахунок: — (лише порівняння кількостей при вичерпанні тайлів).

## Керування і ввід
- (цифрова версія) Тайл у «руці» курсора: обертання колесом/клавішею по 60°; наведення показує фантом на поточному рівні й підсвічує легальні позиції (і поруч, і виверження); клік — покласти.
- Потім вибір дії будівництва: тип будівлі → клік по гексу; для розширення — клік по поселенню й вибір місцевості (підсвічуються всі гекси, які заповняться, і ціна в хатинах).
- 3D-камера: обертання й нахил острова — без неї рівні не видно (BGA попереджає про повільний 3D).

## Вікна, меню, HUD
(цифрова версія; BGA)
- `main-menu` / `lobby-window`: створити стіл, 2–5 гравців.
- `match-setup`: кількість гравців, варіант рангу.
- `game-screen`: 3D-острів з `height-badge` на гексах; поточний тайл (`next-piece-preview`); лишилось тайлів (`remaining-counter`); `piece-stock` — запаси хатин/храмів/веж кожного гравця; `turn-indicator`; `legal-move-highlight` для тайла й для будівлі; `camera-orbit`.
- `confirm-dialog`: «закінчити хід» після будівництва.
- `end-screen`: переможець і причина (два типи / вичерпання тайлів з тайбрейками / решта вибула).
- `help-window`: правила виверження й 4 дії будівництва.
- Переходи: lobby-window → game-screen → end-screen.

## Фічі поза полем
- `online-multiplayer` (BGA), `hotseat` / `ai-opponent-levels` (?) у застосунках.
- `custom-rules`: ранговий варіант.
- `rules-page`; `stats` (ELO на BGA).

## Варіації й родичі
- Taluva Deluxe (?) — перевидання з іншими компонентами.
- Родичі: Akropolis (тріади гексів поверх, висота множить), NMBR 9 (стоси з опорою), Carcassonne (поле росте з тайлів), Kingdom Builder (поселення на гексах), Santorini (вежі за рівнями — chess-abstract).
- **Осі варіацій**: куди можна класти поверх (будь-де / лише вулкан на вулкан) · що стається з накритим (нищиться / лишається під) · як висота впливає (ціна / дозвіл / множник) · ціль (вичерпати запас / очки) · вибування (так / пас).

## Цікавинки для курсу
- Гекс-сітка з тріадою-тайлом: 6 поворотів, координати трьох гексів — 📎.
- Шари: рівень гекса = висота стосу тайлів; перевірка «нема порожнечі під тайлом» і «вулкан на вулкан з іншим напрямом» — 🥉.
- Поселення як компоненти звʼязності, що зливаються й **розпадаються** після виверження (перерахунок BFS) — 🥉.
- Розширення: «залити всі сусідні гекси однієї місцевості», ціна = сума рівнів — 📎.
- Вибування за відсутності легальної будівлі: перебір усіх дій — 🥉.
- 3D-рендер острова з камерою (або ізометрія з бейджами висоти) — 🥈.
- AI: виверження під суперника (зруйнувати хатини, розірвати поселення перед храмом) — 🥇.

## Мапа на каталог
- Є: `cell-click` · `drag-drop-piece` · `hover-highlight` · `legal-move-highlight` · `turn-enforcement` · `hot-seat` · `ai-opponent` · `online-multiplayer` ↔ BGA · `no-moves-left` ↔ вибування · `connectivity-check` ↔ поселення · `match-setup` · `game-screen`, `end-screen`, `help-window`.
- **Нема** → пропозиції карток:
  - `+tri-hex-tile` · `+hex-grid-render` · `+connected-placement` · `+support-rule` — як в Akropolis.
  - `+stack-over-rule` «Класти поверх: вулкан на вулкан, інший напрям» · entities/legality · 🥉.
  - `+cover-destroys` «Накрите нищиться (хатини — у коробку)» · entities/interact · 📎.
  - `+protected-from-cover` «Не можна накривати певне (храм, вежа, ціле поселення)» · entities/legality · 📎.
  - `+group-split` «Група розпадається після зміни поля» · game-logic/constraints · 🥉.
  - `+flood-expand-group` «Розширити групу на всі сусідні клітини типу» · entities/interact · 📎 · слоти {cost: level}.
  - `+level-cost-placement` · `+group-size-gate` (храм від 3 гексів) · `+one-per-group` · `+height-gate` (вежа від рівня 3) — по 🌱.
  - `+exhaust-two-types-win` «Перемога: вичерпати два з трьох запасів» · game-logic/win · 🌱.
  - `+player-elimination` «Вибування без легального ходу, решта грає» · game-logic/lose · 📎.
  - `+camera-3d-orbit` · interface/render · 🥈.

## Пропозиції до словників
- `+cond:height` — рівень (висота) клітини порівняно з N (Taluva, Akropolis, FFT).
- `+cond:group_has` — у групі/поселенні вже є сутність виду (храм, вежа).
- `+cond:orientation_differs` — нова плитка повернута інакше, ніж накрита.
- `+effect:eliminate` — гравець вибуває, його фігури лишаються на полі.
- `+trigger:tiles_exhausted` — стос плиток вичерпано (родич `+trigger:deck_empty`).
- `+ui:height-badge` — число рівня на гексі.
- `+ui:piece-stock` — запаси будівель кожного гравця за типами.
- `+ui:camera-orbit` — обертання/нахил 3D-поля.
- `+axis:field=hex+layers` — поле одночасно гекс і шари (як Akropolis).
- `+card:flood-expand-group` · `+card:cover-destroys` · `+card:exhaust-two-types-win` — див. «Мапа на каталог».

## Джерела
- ⭐ [UltraBoardGames: Taluva rules](https://www.ultraboardgames.com/taluva/game-rules.php) — 48 тайлів, 5 місцевостей, 12 храмів / 8 веж на коробку, правила розширення й виверження, 4 дії, вибування, дострокова перемога, тайбрейки, варіант рангу.
- [BGA: Taluva](https://en.boardgamearena.com/gamepanel?game=taluva) — 2–5 гравців, 20 / 3 / 2 будівлі на гравця, коротке резюме правил, 3D-інтерфейс.
- Wikipedia: сторінка `Taluva` (⭐ черги) віддала 404 — у шапку не клав.
- BGG: [пошук](https://boardgamegeek.com/geeksearch.php?action=search&q=Taluva); YouTube: пошук «Taluva how to play».

## Непевне
- (?) Чи нова хатина на рівні 1 може стояти поруч зі своїм поселенням (BGA: «away from your settlements», UBG вимоги не ставить).
- (?) Правило для 2 гравців (менше будівель?) — у джерелах нема; BGA каже 2–5 гравців, коробка — 2–4 (?).
- (?) Чи будівлі ставлять лише на гекси однієї місцевості при розширенні — так; але чи храм/вежа вимагають певної місцевості — ні (будь-яка, крім вулкана).
- (?) Чи можна накрити вулкан тайлом, коли під іншими двома гексами різні рівні — «no empty space beneath» тлумачу як «усі три гекси на одному рівні» (так у класичних правилах, тут не підтверджено).
- (?) Taluva Deluxe і мобільні застосунки не відкривав.
