---
title: Gentoo Rescue
slug: gentoo-rescue
aka: []
family: push-slide
also: [thinky]
klass: figure
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2025
platforms: [PC, macOS, Linux]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2830480/", best: true, note: "опис: ковзні пінгвіни й моржі, предмети push/pull/bounce/swap/stop/steal/explode, журнал, підказки, редактор, доступність"}
  - {kind: itch, url: "https://jagriff.itch.io/gentoo-rescue", note: "сторінка гри й девлоги (1.1.5, 1.2)"}
  - {kind: itch, url: "https://jagriff.itch.io/gentoo-rescue-demo", note: "старе демо: 20 пазлів у світах Ground Rules, Progression, Teaser"}
  - {kind: other, url: "https://thinkygames.com/features/gentoo-rescue-may-look-cute-but-this-challenging-puzzle-game-hides-all-sorts-of-metagame-twists", note: "рецензія Thinky Games (2025); для агента — 403, зміст лише з пошуку"}
  - {kind: other, url: "https://steamcommunity.com/app/2830480/guides/", note: "гайди спільноти: відеорозвʼязки, ачівки, Workshop"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=gentoo+rescue+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 30
mechanics: [inertia-slide, impassable-cells, push-object, pull-object, item-pickup, all-on-targets, undo-redo, redo, restart-level, skip-level, in-game-editor, level-exchange, world-map, codex-window, controls-remap, save-progress, keyboard-controls, +typed-targets, +rule-changing-items, +tiered-hints, +undo-through-reset]
proposes: ["+window:journal-window", "+feature:warp-navigation", "+card:rule-changing-items", "+card:tiered-hints", "+card:undo-through-reset"]
author: opus
date: 2026-11-09
---

# Gentoo Rescue — Sokoban на льоду: ковзні пінгвіни до кіл свого кольору, моржі у воду, предмети ламають правила

## Суть
Пазл Jagriff про ковзних тварин: пінгвіни й моржі на льоду ковзають до упору — до стіни, до іншої тварини або в діру. Пінгвіни мають стати на кола свого кольору, моржі — втекти у воду, риби додають ще одну, протилежну мету. Ядро гри — предмети (молот, пружина, магніт та інші), що міняють правило руху: штовхнути, потягнути, відбити, обміняти, зупинити, вкрасти, підірвати; світ — мережа пазлів усередині пазлів з мета-поворотами.

## Поле і час
- Квадратна сітка-льодовий острів у кожному пазлі; 300+ пазлів у 16 біомах, кожен біом зі своїми механіками.
- Покроково: таймінгів нема («No time-sensitive inputs»); хід = одне ковзання до упору.
- Відкритий світ із вкладених пазлів: деякі пазли — частини інших (мета-рівень) (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Пінгвін | piece | колір | ковзає до упору; ціль — коло свого кольору |
| Морж | piece | — | ковзає до упору; ціль — вода |
| Риба | piece | — | третя тварина з протилежною метою (?) |
| Стіна | static | — | зупиняє ковзання |
| Діра | hazard | — | тварина падає в неї — ковзання закінчується (?) |
| Вода | terrain | — | мета моржа |
| Коло кольору | terrain | колір | мета пінгвіна того ж кольору |
| Молот · пружина · магніт та ін. | pickup | дія | змінює правило руху: push / pull / bounce / swap / stop / steal / explode |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО `slide(animal, dir)` — обрана тварина ковзає до упору (?).
- КОЛИ `contact(animal, wall)` або `contact(animal, animal)` → ТО `block` — тварина зупиняється перед перешкодою.
- КОЛИ `enter(animal, hole)` → ТО `custom: «тварина падає в діру, ковзання зупиняється»` (?).
- КОЛИ `enter(walrus, water)` → ТО `custom: «морж утік»`.
- КОЛИ `picked(animal, item)` → ТО `custom: «предмет змінює правило руху: push / pull / bounce / swap / stop / steal / explode»` (відповідність предмет → дія — (?)).
- КОЛИ `all_on(penguin, circle)` → ЯКЩО `same(penguin, circle, color)` і `custom: «моржі у воді, вимоги риб виконані»` → ТО `win`.
- КОЛИ `input(undo)` → ТО `undo(1)` · КОЛИ `input(redo)` → ТО `custom: «redo»` · КОЛИ `input(reset)` → ТО `restart` — і сам рестарт скасовується undo.
- Перемога: усі цілі тварин виконано. · Поразка: нема (глухий кут → undo). · Рахунок: нема; мета-цілі світу зараховують збережені розвʼязки.

## Керування і ввід
- Контролер, клавіатура або миша, клавіші перепризначаються; редактор пазлів — лише мишею.
- Undo і redo працюють і крізь рестарти; таймінгів нема.
- Як саме обирається тварина (курсор, перемикання, аватар) — (?).

## Вікна, меню, HUD
- `game-screen` — пазл; мета кожної тварини видно на полі (кола, вода).
- `map-window` — відкритий світ пазлів із варп-навігацією в будь-яке відвідане місце.
- `codex-window` (журнал) — відкриті механіки й взаємодії; для поточного пазла показує потрібні записи.
- `hints-window` — багаторівневі підказки, що вчать дедукції.
- `editor-window` — редактор пазлів; публікація левелпаків у Steam Workshop.
- `settings-window` — керування, кольори для дальтоніків, перемикач «будь-який пазл можна пропустити».
- Переходи: світ → пазл → (розвʼязано) світ; світ → журнал / підказки; головне меню → редактор (?).

## Фічі поза полем
- `undo` / `redo` без ліміту, крізь `restart-level`.
- `skip-level` як налаштування (без ліміту); більшість пазлів необовʼязкові для проходження.
- `level-editor` + `level-sharing` через Steam Workshop; `cloud-save`, збереження розвʼязків для мета-цілей.
- `colorblind-palette` (кольори налаштовуються), `remap-controls`, `achievements` (Steam).

## Варіації й родичі
- Осі варіацій:
  - **рух**: крок (`sokoban`) / ковзання до упору (Gentoo Rescue, `ice-sliding-puzzles`, `ricochet-robots`);
  - **що зупиняє**: стіна / інша фігура / діра (Gentoo Rescue) / клітина-гальмо;
  - **мета**: одна для всіх / своя для кожного виду тварин (кола кольору, вода);
  - **правила**: фіксовані / змінюються предметами (Gentoo Rescue) / словами-блоками (`thinky/baba-is-you`).
- Родичі: `ricochet-robots`, `ice-sliding-puzzles`, `pengo`, `quell`, `thinky/patricks-parabox` (вкладені пазли).

## Цікавинки для курсу
- Ковзання до упору кількох фігур із зупинкою об стіну, фігуру й діру — 📎.
- Типізовані цілі: колір пінгвіна = колір кола, морж — у воду — 🌱.
- Предмет, що підміняє правило руху (push/pull/bounce/swap) як стратегія в коді — 🥈.
- Undo, що переживає рестарт (рестарт — теж запис у стеку) — 📎.
- Журнал механік зі списком потрібних для пазла записів — 🥉.

## Мапа на каталог
- Є: `inertia-slide` ↔ ковзання до упору; `impassable-cells` ↔ стіни; `push-object` + `pull-object` ↔ дії предметів; `item-pickup` ↔ «pick up items»; `all-on-targets` ↔ тварини на своїх цілях; `undo-redo` + `redo` + `restart-level` ↔ undo/redo крізь рестарти; `skip-level` ↔ налаштування пропуску (тут без ліміту); `in-game-editor` + `level-exchange` ↔ редактор і Workshop; `world-map` ↔ відкритий світ пазлів; `codex-window` ↔ журнал; `controls-remap`, `save-progress`, `keyboard-controls`.
- **Нема** → пропозиції карток:
  - `+typed-targets` «Цілі свого типу для кожного виду» · game-logic/win · 🌱.
  - `+rule-changing-items` «Предмет змінює правило руху фігури» · entities/state · 🥈 · слот {verb: push|pull|bounce|swap|stop|steal|explode}.
  - `+tiered-hints` «Підказки рівнями: від натяку до розвʼязку» · game-logic/difficulty · 📎.
  - `+undo-through-reset` «Рестарт як скасовний хід» · game-logic/history · 🌱 — дитина `undo-redo`.

## Пропозиції до словників
- `+window:journal-window` — журнал відкритих механік із вимогами поточного пазла.
- `+feature:warp-navigation` — швидкий перехід у будь-яке відвідане місце світу.
- `+card:rule-changing-items` · `+card:tiered-hints` · `+card:undo-through-reset` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Gentoo Rescue](https://store.steampowered.com/app/2830480/) — «Slide animals to save baby penguins and escape with walruses», дії предметів, 300+ рівнів, 16 біомів, журнал, підказки, редактор + Workshop, доступність; реліз 22.05.2025.
- [itch.io: Gentoo Rescue](https://jagriff.itch.io/gentoo-rescue) — той самий опис, девлоги 1.1.5 і 1.2.
- [itch.io: Gentoo Rescue Demo](https://jagriff.itch.io/gentoo-rescue-demo) — «puzzle metroidvania about sliding penguins and walruses», 20 пазлів, позначено як застаріле.
- [Thinky Games: рецензія](https://thinkygames.com/features/gentoo-rescue-may-look-cute-but-this-challenging-puzzle-game-hides-all-sorts-of-metagame-twists) — для агента 403; з пошукового витягу: пінгвіни стають на кола свого кольору, моржі — у воду; тварини зупиняються об стіну, діру чи одна об одну.
- [Steam: гайди](https://steamcommunity.com/app/2830480/guides/) — відеорозвʼязки, ачівки, інструкція Workshop від автора.
- YouTube: пошук «gentoo rescue gameplay».

## Непевне
- (?) Правило ковзання (зупинка об стіну / тварину / діру) і цілі тварин — лише з пошукових витягів Thinky Games; першоджерела правил не відкрились.
- (?) Хто діє: курсор обирає тварину чи є аватар; хто «підбирає» предмет — тварина чи гравець; що буде з твариною в дірі.
- (?) Що саме роблять молот, пружина й магніт і які предмети відповідають swap/stop/steal/explode; ціль риб.
- (?) Структура «пазлів усередині пазлів» (мета-рівень світу чи рекурсивні поля) не зʼясована.
