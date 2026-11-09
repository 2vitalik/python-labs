---
title: One More Button
slug: one-more-button
aka: []
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2018
platforms: [iOS, Android, PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3623490/", best: true, note: "опис: ти — кнопка, рівень — контролер; рух лише стрілками, що є на екрані; undo/redo"}
  - {kind: official, url: "https://tommykjaer.com/onemorebutton", note: "сторінка автора: стрілки можна повертати (UP → RIGHT), лінки на всі магазини, прескіт"}
  - {kind: other, url: "https://apps.apple.com/us/app/one-more-button/id1363492038", note: "App Store: v1.0 від 27.07.2018, undo з v2.0 (2025), лід, секретні рівні й таємна кінцівка"}
  - {kind: other, url: "https://play.google.com/store/apps/details?id=com.tommysoereide.onemorebutton", note: "Google Play"}
  - {kind: other, url: "https://steamcommunity.com/app/3623490/reviews/?browsefilter=toprated&l=english", note: "відгуки: undo/redo/reset теж блоки на полі, 84 рівні в 13 розділах, лід, колеса, темрява, стелс"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=One+More+Button+Tommy+Kjaer+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [move-4dir, keyboard-controls, push-object, impassable-cells, reach-exit, inertia-slide, floor-types, undo-step, redo, restart-level, sequential-levels, achievements-window, save-progress, +controls-as-objects, +ui-as-object, +rotatable-control, +stealth-detection, +dark-zone, +secret-levels, +multiple-endings]
proposes: ["+cond:control_present", "+role:control", "+card:controls-as-objects", "+card:ui-as-object", "+card:rotatable-control", "+axis:undo-on-field"]
author: opus
date: 2026-11-09
---

# One More Button — ти кругла кнопка, а рівень — твій геймпад: ходиш лише туди, куди лежить стрілка

## Суть
Гравець — кругла кнопка контролера, що «вистрибнула в екран»; кнопки-стрілки лежать на полі як звичайні блоки. Рух у напрямку можливий, лише поки на екрані є стрілка цього напрямку: штовхнувши, повернувши чи сховавши стрілку, гравець змінює власне керування. Так само на полі лежать кнопки undo, redo і reset — скасування ходу є не сервісом, а ресурсом рівня. Ядро — «керування як обʼєкти» (родич [Baba Is You](baba-is-you.md), де правила — блоки).

## Поле і час
- Квадратна сітка, вигляд згори, мальована графіка; покрокова гра (Steam-тег Grid-Based Movement).
- Світи-розділи, кожен зі своїми «гімміками»: лід, колеса, темрява, стелс (відгуки Steam). За відгуком — 84 рівні в 13 розділах, основний шлях ~70; є прихована гілка з додатковими рівнями й другою кінцівкою.
- Мобільна версія — 2018 (iOS 1.0), Steam-версія з новими рівнями й графікою — 25.08.2025.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кругла кнопка | player | 1 | рухається на клітину в напрямку, для якого на екрані є стрілка; штовхає обʼєкти |
| Кнопка-стрілка ↑ ↓ ← → | object | напрям (орієнтація) | штовхається як ящик; поки видна — дозволяє рух у свій напрям; поворот змінює напрям |
| Кнопка undo | object | — | поки є на полі — доступний крок назад; сама штовхається |
| Кнопка redo | object | — | поки є на полі — доступний крок уперед |
| Кнопка reset | object | — | поки є на полі — доступний рестарт рівня (?) |
| Ціль | static | — | дійти — рівень пройдено |
| Стіна | static | — | непрохідна |
| Лід | terrain | — | кнопки на ньому ковзають (App Store) |
| Колеса | terrain | — | «rolling on wheels» — котіння (?) |
| Темрява / тіньові рівні | zone | — | обмежена видимість (?) |
| Вартові стелс-рівнів | enemy | — | помітили — миттєвий рестарт (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `custom: «на екрані є кнопка-стрілка напрямку dir»` → ТО `move(player, dir)`; інакше `block`.
- КОЛИ `contact(player, arrow_button)` → ЯКЩО `free(cell_behind)` → ТО `push(arrow_button)`; інакше `block`.
- КОЛИ `contact(player, undo_button|redo_button|reset_button)` → ЯКЩО `free(cell_behind)` → ТО `push(button)` — службові кнопки теж обʼєкти поля.
- КОЛИ `after(rotate(arrow_button, 90))` → ТО `custom: «кнопка дозволяє вже новий напрям (UP за годинниковою → RIGHT)»`.
- КОЛИ `custom: «стрілку напрямку прибрано з екрана»` → ТО `custom: «рух у цей напрям недоступний»` (?).
- КОЛИ `input(undo)` → ЯКЩО `custom: «кнопка undo є на полі»` → ТО `undo(1)`; інакше `block`.
- КОЛИ `input(redo)` → ЯКЩО `custom: «кнопка redo є на полі»` → ТО `custom: «повернути скасований хід»`.
- КОЛИ `input(reset)` → ЯКЩО `custom: «кнопка reset є на полі»` → ТО `restart`.
- КОЛИ `enter(arrow_button, ice)` → ТО `slide(arrow_button, dir)`.
- КОЛИ `custom: «гравця помітили в стелс-рівні»` → ТО `restart` (за відгуком — миттєво).
- КОЛИ `reach(player, goal)` → ТО `win`, `next_level`.
- Перемога: дійти до цілі. Поразки нема, крім стелс-рестарту; глухий кут без кнопки undo/reset на полі вимагає виходу з рівня (?). Рахунку нема.

## Керування і ввід
- WASD або стрілки — рух, але **лише коли відповідна кнопка є на екрані** (Steam).
- Undo/redo — клавішами, але, за відгуками, «не завжди доступні»: залежать від кнопок на полі. Мобільна версія — дотик (?).
- Кілька агентів одночасно в деяких рівнях — згадано у відгуку без деталей (?).

## Вікна, меню, HUD
- `game-screen`: поле-«контролер» з кнопками; окремого HUD-керування нема — кнопки є частиною рівня.
- `level-select` / вибір світу — рівні нумеруються «Світ N, Рівень M» (сторінка підказок автора) (?).
- `settings-window`: аудіо й музика (додано в 3.0.2).
- `custom-window`: катсцени (оновлено в 3.0.2).
- `achievements-window` (Steam Achievements).
- Переходи: світ → рівень → (ціль) → наступний рівень; таємна гілка → друга кінцівка.

## Фічі поза полем
- `undo`, `redo`, `restart-level` — як кнопки на полі, а не постійні сервіси (недолік за відгуком: «restart хочеться завжди»).
- `levels-sequential`, `collectibles`-подібні секретні рівні, друга кінцівка (`multiple-endings`).
- `cloud-save` (Steam Cloud), `localization` (103 мови на Steam).
- Сторінка автора з розвʼязками найважчих рівнів (`show-solution` поза грою).

## Варіації й родичі
- Мобільна One More Button (2018) → Steam-версія (2025) з новими рівнями; автор має й No More Buttons (App Store) (?).
- Родичі: [Baba Is You](baba-is-you.md) (правила як блоки), [Push The Cat with WASD](push-the-cat-with-wasd.md) (керування — літери в тексті), [Pushtool](pushtool.md), Sokoban.
- **Осі варіацій**: керування як обʼєкт — напрям-стрілка / сервісна кнопка (undo, reset) / правило-слово; що вимикає керування — поза екраном / повернуто / закрито темрявою (?).

## Цікавинки для курсу
- Рух дозволено лише в напрямках наявних стрілок: перевірка `any(arrow.dir == d)` перед кроком — 🌱.
- Стрілки-ящики, що штовхаються й повертаються, змінюючи керування — 📎.
- Undo/redo/reset як обʼєкти рівня: стек історії, доступ до якого залежить від стану поля — 🥉 (undo мусить скасовувати й переміщення самої кнопки undo).
- Лід для кнопок-стрілок: ковзання до упору — 🌱.
- Розвʼязувач BFS зі станом «позиції всіх кнопок» — 🥈 (простір станів з undo як ходом).

## Мапа на каталог
- Є: `move-4dir`, `keyboard-controls` · `push-object` ↔ стрілки й службові кнопки · `impassable-cells` · `reach-exit` · `inertia-slide`, `floor-types` ↔ лід · `undo-step`, `redo`, `restart-level` ↔ кнопки undo/redo/reset · `sequential-levels` · `achievements-window`, `save-progress`.
- **Нема** → пропозиції карток:
  - `+controls-as-objects` «Керування — обʼєкти на полі» · entities/legality · 📎 · слоти {dirs}: дія доступна, поки на полі є її кнопка.
  - `+ui-as-object` «Службова кнопка (undo/reset) — обʼєкт рівня» · game-logic/history · 🥉.
  - `+rotatable-control` «Поворот кнопки-напрямку змінює дозволений рух» · entities/state · 🌱.
  - `+stealth-detection`, `+dark-zone`, `+secret-levels`, `+multiple-endings` — за відгуками, без деталей.

## Пропозиції до словників
- `+cond:control_present` — на полі є обʼєкт-кнопка для цієї дії (One More Button; літери в Push The Cat).
- `+role:control` — сутність-кнопка керування, що дозволяє дію гравця.
- `+card:controls-as-objects`, `+card:ui-as-object`, `+card:rotatable-control` — див. вище.
- `+axis:undo-on-field` — значення осі `undo`: доступність undo задає обʼєкт на полі.

## Джерела
- ⭐ [Steam](https://store.steampowered.com/app/3623490/) — «You are a Button. The level is your controller»; рух стрілками, розкиданими по світу; «push, press, and twist»; undo/redo; WASD лише за наявності кнопки.
- [Сторінка автора](https://tommykjaer.com/onemorebutton) — поворот кнопок (UP → RIGHT), реліз Steam 25.08.2025, магазини, сторінка розвʼязків.
- [App Store](https://apps.apple.com/us/app/one-more-button/id1363492038) — v1.0 27.07.2018; undo з v2.0.2 (2025); лід для кнопок; секретні рівні й таємна кінцівка (3.0.2); відповідь автора про reset.
- [Відгуки Steam](https://steamcommunity.com/app/3623490/reviews/?browsefilter=toprated&l=english) — undo/redo/reset як блоки; поворот стрілки; 84 рівні / 13 розділів; лід, колеса, темрява, стелс; друга кінцівка.
- YouTube: пошук «One More Button gameplay».

## Непевне
- (?) Чим саме повертають стрілку («twist»): поворотна плита, окрема дія чи обертовий механізм.
- (?) Що таке «press» — натискання кнопок наїздом, чи це лише undo/redo/reset.
- (?) Чи ланцюгове штовхання (кілька кнопок в ряд) дозволене.
- (?) Як працюють колеса, темрява й стелс; чи стрілка в темряві «не на екрані».
- (?) Кількість рівнів: 84/13 розділів (один відгук) vs 70 на основному шляху (інший); точне число не підтверджено офіційно.
- (?) Чи є вихід у меню / рестарт поза кнопкою на полі.
- Лінк itch.io з черги (swiftified) — інша гра (інкрементальний клікер), у шапку не взято.
