---
title: Dissembler
slug: dissembler
aka: []
family: falling-match
also: [thinky]
klass: cursor
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: state
year: 2018
platforms: [PC (Windows, macOS, Linux), iOS, Android]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/797620/Dissembler/", best: true, note: "суть: обмін пари, групи кольору зникають без доливу, 170+ пазлів, free undo, daily, infinite, color-blind"}
  - {kind: itch, url: "https://ianmaclarty.itch.io/dissembler", note: "той самий опис, платформи, нагорода Freeplay 2018"}
  - {kind: other, url: "https://www.tapsmart.com/games/review-dissembler-match-three-tough-twist/", note: "огляд: обмін лише зі збігом, багатошарові плитки, Daily, Infinite, лінійна кампанія, оновлення +48 пазлів і 2 типи плиток"}
  - {kind: other, url: "https://www.appspy.com/news/dissembler-offers-a-colorful-twist-on-the-matching-puzzler-available-on-ios/", note: "шари кольору, кольорові точки на сторонах плиток, лідерборди Daily/Infinite"}
  - {kind: other, url: "https://www.pocketgamer.com/dissembler/dissembler-is-a-puzzling-new-indie-game-that-will-really-make-you-think", note: "перегляд результату ходу до підтвердження"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Dissembler+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [cell-click, selection-highlight, connectivity-check, completion-detection, undo-redo, undo-unlimited, sequential-levels, daily-puzzle, leaderboard, mode-select, game-screen, +match-3-swap, +connected-group-pop, +clear-all-goal, +no-refill-holes, +move-preview, +layered-tile, +edge-dot-match, +daily-solution-reveal, +colorblind-palette]
proposes: ["+cond:makes_match", "+effect:peel_layer", "+feature:daily-solution", "+card:no-refill-holes", "+card:layered-tile", "+card:edge-dot-match"]
author: opus
date: 2026-11-09
---

# Dissembler — міняй сусідні плитки лише так, щоб склалась група кольору; нічого не падає, треба розібрати картинку до нуля

## Суть
Кожен рівень — рукотворна абстрактна «аплікація» з кольорових плиток. Хід — обмін двох сусідніх плиток, і він дозволений **лише якщо дає збіг**: 3+ плиток одного кольору, що торкаються. Збіг зникає, а на його місці лишається **дірка** — ні гравітації, ні доливу, тож кожен хід незворотно змінює форму поля. Мета — прибрати всі плитки; це match-3, перевернутий у детермінований пазл із безкоштовним undo.

## Поле і час
- Квадратна сітка; поле — фігура з плиток довільного контуру (дірки й край — порожні клітини). Розмір — від рівня.
- Статика: нічого не відбувається без ходу; випадковості в кампанії нема («no randomness»).
- Ходом плитки не падають і не доливаються: пробіли розривають групи, і потрібну плитку доводиться «вести» до своїх обмінами, кожен з яких теж мусить дати збіг.
- Шари клітини: деякі плитки багатокольорові — після збігу знімається верхній колір і відкривається наступний.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка | tile | колір | міняється з сусідньою; у групі 3+ того ж кольору, що торкаються, зникає |
| Багатошарова плитка | tile | стек кольорів | збіг зовнішнього кольору знімає шар — плитка набуває кольору наступного; зникає з останнім шаром |
| Кольорова точка на стороні плитки | mark | колір, сторона | має збігтися вздовж сторін плиток (AppSpy); точна механіка — (?) |
| Порожня клітина (дірка) | static | — | лишається після збігу; не заповнюється; розриває групи |
| Курсор / виділення | player | вибрана пара | показує пару для обміну й превʼю результату |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(select_pair)` → ЯКЩО `custom: «дві плитки — сусіди по стороні»` and `custom: «після обміну є група 3+ одного кольору»` → ТО `swap(a, b)`; інакше `block`.
- КОЛИ `input(select_pair)` → ТО `custom: «превʼю — показати результат обміну до підтвердження»` (Pocket Gamer).
- КОЛИ `after(swap)` → ЯКЩО `pattern(group(3))` and `connected(same_color_tiles)` → ТО `clear(group)` (?) — уся звʼязна група кольору чи лише утворені 3+ — див. «Непевне».
- КОЛИ `after(clear)` → ТО `custom: «нічого не падає й не доливається — клітини лишаються порожніми»`.
- КОЛИ `pattern(group(3))` → ЯКЩО `state(tile, layered)` → ТО `custom: «peel_layer — зняти верхній колір, плитка лишається з кольором наступного шару»`; останній шар → `disappear`.
- КОЛИ `all_gone(tile)` → ТО `win`, `next_level`.
- КОЛИ `no_moves(player)` → ЯКЩО `count(tile, >, 0)` → ТО `custom: «глухий кут — лише undo або рестарт»` (?).
- КОЛИ `input(undo)` → ТО `undo(1)` — без ліміту й без штрафу.
- КОЛИ `input(restart)` → ТО `restart` (?).
- Infinite: КОЛИ `all_gone(tile)` → ЯКЩО `mode(infinite)` → ТО `custom: «нове поле з багатошаровими плитками»`, `score(+n)` (?) → онлайн-лідерборд.
- Перемога: поле порожнє. · Поразка: формально нема — лише глухий кут. · Рахунок: у кампанії нема (TapSmart: «lack of scoring»); очки — лише в Infinite/Daily для лідербордів.

## Керування і ввід
- Миша / тач: вибрати дві сусідні плитки (клік або перетягування) — обмін; спершу показується превʼю, підтвердження виконує хід (?).
- Кнопка undo — необмежено, будь-коли.
- Обмін, що не дає збігу, просто не виконується.

## Вікна, меню, HUD
- `main-menu` → `mode-select`: кампанія (лінійна, без пропуску рівнів) · Daily · Infinite.
- `game-screen`: поле-аплікація, `selection-highlight` вибраної пари, `undo-button`, `restart-button` (?); у Infinite — `score`.
- `leaderboard` — онлайн-таблиці Infinite і Daily (Steam Leaderboards).
- `daily-window`: кілька свіжих пазлів дня; покрокові розвʼязки показуються наступного дня.
- `settings-window`: color-blind mode, звук/музика (?).
- Переходи: main-menu → рівень → (поле порожнє) наступний рівень; Daily → пазли дня → лідерборд.

## Фічі поза полем
- `undo` ∞ без штрафу; `levels-sequential` — 170+ рукотворних пазлів, без пропуску (TapSmart); оновлення додало 48 пазлів і 2 нові типи плиток.
- `daily-puzzle` + `+feature:daily-solution` — розвʼязок покроково наступного дня.
- `mode-endless` (Infinite) з `leaderboard-online`.
- `colorblind-palette` — color-blind mode.
- `achievements` (4 у Steam), `cloud-save` (Steam Cloud).

## Варіації й родичі
- Автор — Ian MacLarty, видавець Shape Shop; Excellence in Design на Freeplay 2018.
- Родичі в корпусі: [Bejeweled](bejeweled.md) (обмін лише зі збігом, але з доливом), [SameGame / Flood](samegame-flood.md) (прибрати все, але з гравітацією), [Tumblestone](tumblestone.md) і [Trouballs](trouballs.md) (детермінована «зачистка до нуля»), [Panel de Pon](panel-de-pon.md) (обмін без умови).
- **Осі варіацій**:
  - **після збігу**: долив згори (Bejeweled) / падіння без доливу (SameGame) / нічого — дірка (Dissembler);
  - **умова обміну**: будь-який (Panel de Pon) / лише зі збігом (Bejeweled, Dissembler);
  - **збіг**: лінія 3 / група 3+, що торкається (Dissembler);
  - **плитка**: один колір / шари кольорів, що знімаються по одному.

## Цікавинки для курсу
- Обмін лише зі збігом: перевірка гіпотетичного стану (зробити обмін, BFS групи, відкотити) — 📎.
- Поле без гравітації й доливу: дірки, що розривають групи, «ведення» плитки ланцюгом легальних обмінів — 🌱.
- Багатошарові плитки (стек кольорів, знімається по одному) — 🌱.
- Undo без ліміту + превʼю ходу — 📎.
- Розвʼязувач: DFS по станах із запамʼятовуванням (стан = множина плиток і їхніх шарів), бо випадковості нема — 🥇.
- Генератор Infinite: розвʼязне поле «назад» — збирати плитки зворотними обмінами — 👑.

## Мапа на каталог
- Є: `cell-click` + `selection-highlight` ↔ вибір пари; `connectivity-check` ↔ група, що торкається; `completion-detection` ↔ порожнє поле; `undo-redo` / `undo-unlimited` ↔ free undo; `sequential-levels` ↔ лінійна кампанія; `daily-puzzle` ↔ Daily; `leaderboard` ↔ онлайн-таблиці; `mode-select` ↔ кампанія/Daily/Infinite; `game-screen`.
- **Нема** → пропозиції карток:
  - `+match-3-swap` (Bejeweled) {revert: no — неможливий обмін не виконується}; `+connected-group-pop` {min: 3, adjacency: 4}; `+clear-all-goal`; `+move-preview` (2048/Threes); `+colorblind-palette` (Hextris) — уже в корпусі.
  - `+no-refill-holes` «Після збігу клітина лишається порожньою: ні падіння, ні доливу» · entities/legality · 🌱.
  - `+layered-tile` «Плитка зі стеком кольорів, збіг знімає шар» · entities/state · 🌱 · слот {layers}.
  - `+edge-dot-match` «Кольорові точки на сторонах плиток мають збігтися» · entities/legality · 📎 (?).
  - `+daily-solution-reveal` «Розвʼязок пазла дня — наступного дня» · levels/bank · 🌱.

## Пропозиції до словників
- `+cond:makes_match` — хід легальний, лише якщо створює збіг (Dissembler, Bejeweled); відрізняється від `legal(text)` тим, що перевірка — на гіпотетичному стані.
- `+effect:peel_layer` — зняти верхній шар плитки, відкрити наступний колір.
- `+feature:daily-solution` — розвʼязок щоденного пазла відкривається наступного дня.
- `+card:no-refill-holes`, `+card:layered-tile`, `+card:edge-dot-match` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Dissembler](https://store.steampowered.com/app/797620/Dissembler/) — суть, «no tiles will drop in», 170+ пазлів без випадковості, free undo, Daily з розвʼязками наступного дня, Infinite з лідербордами, color-blind; дата 21–22.02.2018, 4 досягнення (Steam API).
- [itch.io: Dissembler](https://ianmaclarty.itch.io/dissembler) — той самий опис, Windows/macOS/Linux/Android, Freeplay 2018.
- [TapSmart: огляд](https://www.tapsmart.com/games/review-dissembler-match-three-tough-twist/) — обмін лише зі збігом 3+, плитки «як цибуля», Daily, Infinite, лінійна кампанія, оновлення 48 пазлів і 2 типи плиток.
- [AppSpy](https://www.appspy.com/news/dissembler-offers-a-colorful-twist-on-the-matching-puzzler-available-on-ios/) — шари кольорів, кольорові точки на сторонах плиток, лідерборди.
- [Pocket Gamer](https://www.pocketgamer.com/dissembler/dissembler-is-a-puzzling-new-indie-game-that-will-really-make-you-think) — превʼю ходу до підтвердження.
- YouTube: пошук «Dissembler gameplay».

## Непевне
- (?) Що саме зникає: уся звʼязна група кольору чи лише плитки, що утворили 3+; чи рахуються діагоналі (найімовірніше — 4-сусідство).
- (?) Чи можна міняти плитку з порожньою клітиною — джерела кажуть лише «пари плиток».
- (?) Механіка кольорових точок на сторонах плиток і назви двох типів плиток з оновлення (2020) — не знайдено.
- (?) Чи гра сама визначає глухий кут; чи є окрема кнопка рестарту; як нараховуються очки в Infinite/Daily.
- (?) Як саме працює превʼю (утримання / два кліки) — лише «view the result before you set it in stone».
