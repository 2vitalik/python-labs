---
title: Chronescher
slug: chronescher
aka: []
family: thinky
also: []
klass: avatar
axes:
  field: iso
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2022
platforms: [PC, Mac, Linux, Android, iOS]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1911170/Chronescher/", best: true, note: "три здібності (портал, якір часу, ракурс), трейлер, 12 скриншотів з HUD, мапою й книгою історії"}
  - {kind: official, url: "https://purplesloth.studio/games/chronescher/", note: "сторінка студії: 6 біомів, механіки, скриншоти зі штовхуваним блоком"}
  - {kind: other, url: "https://purplesloth.studio/presskits/chronescher/en", note: "прескіт: 50+ пазлів, 10 панелей історії, опційні виклики → альтернативна кінцівка, натхнення Dungeon Break"}
  - {kind: itch, url: "https://purplesloth.itch.io/chronescher", note: "збірки Win/Mac/Linux/Android, девлоги"}
  - {kind: other, url: "https://purplesloth.itch.io/chronescher/devlog/423016/chronescher-update-v11", note: "v1.1: Q/W — здібності, E — undo, R — redo, T — скидання, A/D і стрілки — поворот камери"}
  - {kind: other, url: "https://purplesloth.itch.io/dungeon-break", note: "Dungeon Break (Ludum Dare 47) — попередник: прокляття повертає на старт за N кроків"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Chronescher+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [cell-click, keyboard-controls, reach-exit, push-object, button-toggle, gravity-fall, teleport, undo-redo, redo, restart-level, world-map, level-unlock, sequential-levels, achievements-window, settings-window, language-picker, volume-control, game-screen, map-window, +perspective-alignment, +rotate-view-to-solve, +camera-orbit, +placeable-portal, +level-snapshot-restore, +per-level-abilities, +optional-challenges, +multiple-endings, +story-panels, +seasonal-event-levels, +colorblind-palette]
proposes: ["+effect:restore_snapshot", "+ui:view-dots", "+window:story-panels", "+card:level-snapshot-restore", "+card:placeable-portal", "+feature:seasonal-event"]
author: opus
date: 2026-11-19
---

# Chronescher — покроковий «ешерівський» ізометричний пазл: поверни камеру, щоб зійшлися шляхи, постав портал-закладку і відкоти рівень до знімка, лишившись на місці

## Суть
Героїня в плащі піднімається дахами міста до вершини вежі; кожен рівень — ізометрична конструкція з блоків, сходів, плит-перемикачів і штовхуваних кубів, мета — дійти до сяючої клітини. Головні інструменти — три здібності: поворот ракурсу (у новому ракурсі відкриваються шляхи й сховані проходи — «неможлива геометрія»), портал (поставити й повернутися до нього будь-коли) і якір часу (знімок стану рівня, який можна відновити, не зрушивши героїні). Найважчі рівні вимагають поєднати всі три.

## Поле і час
- Ізометрична сітка блоків з висотами; 6 біомів: Tutorial, Timber, Overgrowth, Docks, Nightsky, Uptown; сезонний Halloween (6 рівнів); разом 50+ пазлів.
- Ракурси: у рівня 2–4 положення камери (кружечки внизу екрана, заповнений — поточний).
- Покроково («turn-based», «Playable without Timed Input»); є undo/redo, тож хід — дискретний.
- Здібності дає рівень: на одних скриншотах доступний лише портал, на інших — портал і якір; патч 1.1 прибрав якір з рівня, де його не мало бути.
- Стан рівня = положення блоків, плит і платформ; героїня — окремо (якір відновлює все, крім неї).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Героїня в плащі | player | — | ходить верхніми гранями блоків і сходами |
| Ціль | static | — | сяюча клітина з шаховим візерунком; дійти — рівень пройдено |
| Плита / доріжка | terrain | висота | шлях; сходи зʼєднують висоти |
| Штовхуваний блок | object | — | бірюзовий куб (Nightsky), у прескіті — «pushable block» |
| Тригер-плита | switch | — | квадратна вставка в плиті; (?) запускає рух платформ |
| Тригер-плита, що рухається сама | switch | маршрут | згадана в патчі Halloween (знімок ламався, якщо стояти на ній) |
| Платформа, що відкривається | gate | відкрита / закрита | з баг-репорту: героїня мала б падати, коли під нею відкрилась платформа |
| Портал | terrain | один (?) | фіолетове кільце на клітині, яке ставить гравець; пізніше — точка повернення |
| Знімок рівня (якір часу) | mark | один (?) | збережений стан рівня без героїні |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click_tile)` → ЯКЩО `path_exists(hero, tile)` → ТО `move(hero, tile)` (?) — режими «лише миша» й «лише тач» означають клік/тап по клітині.
- КОЛИ `input(rotate_view)` (A/D, стрілки або кнопки) → ТО `camera(rotate)` — наступний ракурс рівня.
- КОЛИ `custom: «ракурс змінено»` → ТО `custom: «клітини, що в новому ракурсі зійшлися на екрані, стають сусідніми; відкриваються шляхи й сховані проходи»` (?) точний механізм.
- КОЛИ `input(portal)` (Q або значок) → ЯКЩО `not state(portal, placed)` → ТО `place(hero, portal)` на свою клітину; інакше `teleport(hero, portal)` (?).
- КОЛИ `input(anchor)` (W або значок) → ЯКЩО `not state(anchor, set)` → ТО `checkpoint` — знімок стану рівня; інакше `custom: «рівень повертається до знімка, героїня лишається там, де стоїть»`.
- КОЛИ `contact(hero, block)` → ЯКЩО `free(cell_behind)` → ТО `push` (?).
- КОЛИ `enter(hero, plate)` → ТО `set_state(platform, moving)` (?).
- КОЛИ `custom: «під героїнею відкрилась платформа»` → ТО `fall(hero)`.
- КОЛИ `enter(hero, goal)` → ТО `win`, `next_level`.
- КОЛИ `input(undo)` (E) → ТО `undo(1)`.
- КОЛИ `input(redo)` (R) → ТО `custom: «повернути скасований хід»`.
- КОЛИ `input(reset)` (T) → ТО `restart`.
- КОЛИ `custom: «виконано опційний виклик рівня»` → ТО `unlock(alt_ending)` (?) — виклики відкривають альтернативну кінцівку.
- Перемога: дійти до цілі · Поразки нема (?) · Рахунку нема; опційні виклики → альтернативна кінцівка.

## Керування і ввід
- Миша або тач: клік/тап по клітині — йти (?); значки зліва — здібності, undo, скидання, мапа.
- Клавіатура (з v1.1): Q, W — здібності; E — undo; R — redo; T — скидання; A/D або стрілки — поворот камери.
- Steam Deck і тач: курсор ховається при дотику, зʼявляється від руху миші (v1.2).

## Вікна, меню, HUD
- `game-screen`: рівень у центрі; зліва колонка значків — ☆ (виклик рівня), штатив із камерою (якір часу), кільце з антенами (портал), стрілка (undo), коло-стрілки (скидання), мапа; внизу — кружечки ракурсів; опційно — назва рівня.
- `map-window` (вкладка «мапа»): панелі біомів з вузлами-рівнями на лініях; замкнені — замки; ромби й зірочки — (?) опційні вузли; угорі праворуч — три значки прогресу (?); кнопки «назад» і «вийти».
- `custom-window` «книга»: 10 мальованих панелей історії, що відкриваються проходженням; гортання стрілками й крапками.
- `settings-window`: повноекранний режим, показ назв рівнів, гучність, мова (9 мов інтерфейсу; турецьку, нідерландську й китайську додано патчами 2023).
- `achievements-window` (Steam).
- Переходи: мапа → рівень → (ціль) → наступний вузол; між рівнями — діагональна шторка.

## Фічі поза полем
- `undo` / `redo` / `restart-level` (E / R / T).
- `world-map` з `level-unlock`; опційні виклики → альтернативна кінцівка; кілька кінцівок.
- Історія: 10 мальованих панелей у «книзі».
- Сезонна подія: біом Halloween (6 рівнів, 13.10–13.11.2022, повернувся 2023).
- Доступність: «Color Alternatives», «Camera Comfort», «Mouse Only», «Touch Only», власні повзунки гучності.
- `achievements`; `localization`.

## Варіації й родичі
- [Monument Valley](monument-valley.md) — той самий ізометричний «ешерівський» стиль; огляди й гравці порівнюють прямо; різниця — покрокова логіка, портал і знімок рівня.
- Шлях залежить від ракурсу: [Echochrome](echochrome.md), [A Little Perspective](a-little-perspective.md), [M.C. Escher's Equestrian Armageddon](mc-eschers-equestrian-armageddon.md).
- Здібності над історією ходів: [Tres Undos](tres-undos.md) (undo як механіка).
- Попередники студії: Dungeon Break (Ludum Dare 47) — прокляття повертає на старт за N кроків, рятує портал; What's Your Gender? — неможлива геометрія рівнів.
- **Осі варіацій** «знімок часу»: що відкочується — усе / усе, крім героя (якір) / лише герой (портал); скільки точок — одна / кілька; ракурс — вільне обертання / 2–4 фіксованих / один.

## Цікавинки для курсу
- Знімок стану без героя: `snapshot = state − hero`; відновлення накладає знімок і лишає героя — 🥉 (розділення стану на «світ» і «героя»).
- Портал-закладка: одна точка повернення, телепорт на неї — 🌱.
- Сусідство за ракурсом: для кожного з 2–4 положень камери будувати граф «що з чим зійшлося на екрані» — 🥈 (проєкція 3D-сітки на 2D і пошук збігів ребер).
- Undo/redo поверх здібностей (портал і якір теж ідуть у стек) — 📎.
- Мапа біомів із замками й опційними вузлами — 📎.

## Мапа на каталог
- Є: `cell-click`, `keyboard-controls` ↔ ввід · `reach-exit` ↔ ціль · `push-object` ↔ блок · `button-toggle` ↔ тригер-плити · `gravity-fall` ↔ падіння з відкритої платформи · `teleport` ↔ повернення в портал · `undo-redo`, `redo`, `restart-level` ↔ E/R/T · `world-map`, `level-unlock`, `sequential-levels`, `map-window` · `achievements-window`, `settings-window`, `language-picker`, `volume-control`, `game-screen`.
- **Нема** → пропозиції карток:
  - `+level-snapshot-restore` «Знімок рівня й відновлення без руху героя» · game-logic/history · 🥉.
  - `+placeable-portal` «Гравець ставить портал і повертається до нього» · entities/interact · 📎.
  - `+per-level-abilities` «Набір здібностей задає рівень» · levels/format · 🌱.
  - `+story-panels` «Панелі історії відкриваються проходженням» · interface/menus · 🌱.
  - `+seasonal-event-levels` «Сезонні рівні на обмежений час» · levels/bank · 📎.
  - `+perspective-alignment`, `+rotate-view-to-solve`, `+camera-orbit`, `+optional-challenges`, `+multiple-endings`, `+colorblind-palette` — уже пропоновані в корпусі.

## Пропозиції до словників
- `+effect:restore_snapshot` — відновити збережений стан рівня, не чіпаючи вибраних сутностей (героя).
- `+ui:view-dots` — індикатор доступних ракурсів камери (кружечки, поточний заповнений).
- `+window:story-panels` — вкладка з мальованими панелями історії.
- `+card:level-snapshot-restore`, `+card:placeable-portal` — див. Мапу на каталог.
- `+feature:seasonal-event` — рівні, доступні лише в період події.

## Джерела
- ⭐ [Steam: Chronescher](https://store.steampowered.com/app/1911170/Chronescher/) — опис здібностей («place portals and return to them at a whim», «timeanchor … without moving yourself», «change your perspective … hidden passages»), трейлер (дивився кадрами), 12 скриншотів: HUD, мапа, книга.
- [PurpleSloth: Chronescher](https://purplesloth.studio/games/chronescher/) і [прескіт](https://purplesloth.studio/presskits/chronescher/en) — 50+ пазлів, 6 біомів, 10 панелей, альтернативна кінцівка, кооператив-студія, натхнення Dungeon Break і What's Your Gender?
- [itch.io](https://purplesloth.itch.io/chronescher) і девлоги: [v1.1](https://purplesloth.itch.io/chronescher/devlog/423016/chronescher-update-v11) (гарячі клавіші), v1.2 (тач), Halloween (6 рівнів), v1.7; баг-репорт «Character does not fall when a platform is open below».
- Steam News (`ISteamNews/GetNewsForApp`, appid 1911170) — ті самі патчі: тригер-плити, що рухаються самі, pushblock з Nightsky, знімок недоступний на окремих рівнях.
- [Dungeon Break](https://purplesloth.itch.io/dungeon-break) — гра студії на Ludum Dare 47.
- Thinky Games: огляд «Chronescher — Which Way Should I Be Looking?» (жовтень 2022) — у фетчі 403, бачив лише фрагмент у пошуку.

## Непевне
- (?) Як саме ходить героїня: клік по клітині з автошляхом чи крок за кроком (Steam: «Grid-Based Movement», «Mouse Only», «Touch Only»).
- (?) Правило «сусідство за ракурсом» — з опису й порівняння з Monument Valley; точного механізму в джерелах нема.
- (?) Скільки порталів і знімків можна мати; чи можна переставити портал; чи якір одноразовий.
- (?) Що саме роблять тригер-плити й платформи; чи можна впасти в порожнечу.
- (?) Значення ромбів і зірочок на мапі, значка ☆ і трьох значків угорі праворуч.
- (?) Скільки ракурсів у рівня — на скриншотах 2–4 кружечки; кут повороту не підтверджено.
