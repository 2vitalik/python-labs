---
title: Sokobos 2
slug: sokobos-2
aka: []
family: push-slide
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2025
platforms: [Windows, macOS, Linux, web (демо)]
links:
  - {kind: itch, url: "https://martin-games.itch.io/sokobos-2-demo", best: true, note: "демо в браузері (Godot): гілки рівнів — основи, лід, течії; undo кнопкою чи Y/Z; коментарі автора про відмінності від Sokobos 1"}
  - {kind: steam, url: "https://store.steampowered.com/app/3422180/", note: "повна версія 19.09.2025: «pushing vases into a cart, but you can push the cart too!», вода-міст і течія, ворота, плити; 2–3 години"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3422180&count=20&maxlength=0", note: "новини Steam: патчі 1.0.1–1.0.3 (рівні Bridges 4 і 10, крижаний блок над затопленим каменем), геймпад і мови в демо"}
  - {kind: other, url: "https://3rd-strike.com/sokobos-2-review/", note: "огляд: 65 пазлів кампанії, ящик штовхають і зсередини, лід ковзає і в воді стає тимчасовим шляхом, течія несе вази, не валуни, плити тримають ворота"}
  - {kind: other, url: "https://ladiesgamers.com/sokobos-2-review/", note: "огляд: нелінійна мапа з гілками, після гілки — рівень із золотим уламком"}
  - {kind: other, url: "https://www.gamingcouchpotato.co.uk/search/label/Sokobos%202", note: "огляд: одні обʼєкти тонуть, інші пливуть, мости з них — одноразові"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Sokobos+2+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-4dir, keyboard-controls, push-object, multi-cell-size, carrier-platform, inertia-slide, fill-hole, button-toggle, goal-counter, move-counter, undo-unlimited, restart-level, world-map, level-unlock, main-menu, pause-menu, settings-window, controls-remap, language-picker, volume-control, save-progress, movement-animation, particles, sound-effects, background-music, +transport-load, +push-from-inside, +pressure-plate, +branching-campaign, +intermission-cutscene, +float-drift, +ice-floe]
proposes: ["+effect:sink", "+effect:drift", "+trigger:stream_tick", "+feature:grid-visibility", "+card:float-drift", "+card:ice-floe", "+card:cargo-push"]
author: opus
date: 2026-11-19
---

# Sokobos 2 — грецький сокобан: завантаж усі вази у візок, який теж штовхається, а камінь, лід і течія вирішують, як перейти воду

## Суть
Покараний богами герой Стародавньої Греції мусить вічно збирати вази. У кожній невеликій кімнаті всі вази треба заштовхати у візок 2×2 — а візок і сам їде, коли його штовхнути ззовні або зсередини, везучи вантаж (і героя). Довкола — вода: камінь тоне й стає опорою, ваза пливе й дрейфує течією, крижаний блок ковзає до упору, а у воді стає тимчасовим плотом; плити відчиняють ворота.

Martin Games (Godot), сиквел Sokobos (2021): менші, сфокусовані рівні, сюжет «трагедії» з персонажами між рівнями, нелінійна мапа.

## Поле і час
- Квадратна сітка клітин 18 px; кімнати невеликі (у демо — кілька десятків клітин підлоги); тайли: стіна, підлога, вода, течія вгору / вниз / ліворуч / праворуч.
- Хід = крок героя; після кожного кроку гра доводить світ до спокою: ковзання льоду, тонення, дрейф течією, плити й ворота, танення.
- Поверхні підлоги (трава, дерево, камінь, лід) — лише для звуку кроків.
- Налаштування сітки: лінії між клітинами вимкнені / слабкі / середні / яскраві.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | напрям | рух 4 боки; штовхає по одному обʼєкту; може стояти у візку |
| Ваза | object | плавуча | штовхається; у воді пливе й дрейфує течією; розбита — герой плаче |
| Візок | container | 2×2 клітини, борти | вантаж усередині — пасажири; штовхається ззовні й зсередини, везе все, що в ньому |
| Камінь (валун) | object | тоне | штовхається; у воді тоне й стає опорою; течія його не несе |
| Крижаний блок | object | ковзає, тане | штовхнутий ковзає до упору; у воді замерзає плотом, потім тане (?) |
| Плита | switch | натиснута / ні | натиснута, поки на ній ваза, камінь чи герой; тримає свої ворота відчиненими |
| Ворота | gate | відчинені / зачинені | відчиняються від плит; зачиняються, коли плиту звільнено |
| Вода | hazard | — | герою непрохідна; обʼєкт у ній тоне або пливе |
| Течія | terrain | напрям | зсуває плавуче на клітину в своєму напрямку |
| Міст | terrain | цілий / зламаний | (?) ламається після використання |
| Бомба | hazard | — | не штовхається; (?) вибухає, коли в неї штовхнуть обʼєкт, нищить сусідів |
| Золотий уламок | object | плавучий | як ваза; у спецрівні після гілки — замість ваз |
| Стіна | static | — | непрохідна |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(hero, dir)`.
- КОЛИ `contact(hero, vase|stone|ice)` → ЯКЩО `free(cell_behind)` → ТО `push`; інакше `block` (?) — ряд, схоже, не штовхається.
- КОЛИ `contact(hero, vase)` → ЯКЩО `occupied(cell_behind, cart)` → ТО `push` — ваза заїжджає у візок і стає пасажиром.
- КОЛИ `contact(hero, cart)` → ЯКЩО `custom: «усі клітини перед візком вільні»` → ТО `push`, `carry(cart, passengers)` — візок їде на клітину разом з усім усередині.
- КОЛИ `input(dir)` → ЯКЩО `state(hero, in_cart)` and `custom: «герой впирається в борт»` → ТО `move(cart, dir)`, `carry(cart, passengers)` — штовхання зсередини везе й героя.
- КОЛИ `enter(stone, water)` → ТО `set_cell(water, sunk_stone)` — затоплений камінь: по ньому ходять і на нього кладуть інше.
- КОЛИ `enter(vase, water)` → ТО `set_state(vase, floating)`.
- КОЛИ `after(move)` → ЯКЩО `state(item, floating)` and `cell(item_cell, stream)` → ТО `move(item, stream_dir)` — течія несе плавуче, камінь — ні.
- КОЛИ `contact(hero, ice)` → ЯКЩО `free(cell_behind)` → ТО `slide(ice, dir)` — до першої перешкоди.
- КОЛИ `enter(ice, water)` → ТО `transform(ice, floe)` — тимчасовий плаский шлях; (?) згодом тане (`disappear`).
- КОЛИ `enter(any, plate)` → ТО `set_state(linked_gates, open)`; КОЛИ `leave(any, plate)` → ТО `set_state(linked_gates, closed)`.
- КОЛИ `custom: «ваза розбита (вибух)»` → ТО `set_state(hero, crying)` — рівень не пройти, лише undo.
- КОЛИ `all_on(vase, cart)` → ТО `win`, `next_level` — герой радіє, назад на мапу.
- КОЛИ `input(undo)` → ТО `undo`; КОЛИ `input(restart)` → ТО `restart`.
- Перемога: усі вази (чи золотий уламок) у візку. · Поразка: формально нема — розбита ваза чи глухий кут лише просять undo. · Рахунок: лічильник ходів «Moves N» без оцінки.

## Керування і ввід
- Стрілки — рух; undo — клавіша Y/Z (обидві, під різні розкладки) або кнопка внизу ліворуч; рестарт — клавіша й кнопка на HUD.
- Геймпад Xbox / PlayStation (з демо-оновлення 24.07.2025), переназначення клавіш (рух, undo, рестарт, підтвердження, скасування).
- На мапі світу герой ходить між вузлами-рівнями тими самими стрілками.

## Вікна, меню, HUD
- `main-menu`: Continue · New Game (з попередженням про перезапис) · Settings · Credits · Discord · (у демо) Wishlist.
- `dialogue-window` — сцени між рівнями: вступ і розмови з персонажами (бабуся, дідусь, солдат, молода жінка, «підозрілі чоловіки», торговець).
- `map-window` — мапа світу: вузли-рівні (закритий / відкритий / пройдений), гілки, золоті уламки.
- `game-screen`: кімната; HUD — «Moves N» (`move-counter`), лічильник ваз `x/y` (`progress-bar`), кнопки undo, рестарт, пауза; назва рівня на вході; у навчальних рівнях — підказки клавіш.
- `pause-menu` (на мапі й у рівні); `settings-window`: Audio (загальна, звуки, музика) · Game (тряска камери, видимість сітки 4 рівні, показ HUD) · Controls (клавіатура, геймпад) · Language (EN, 简体中文, 日本語) · екран (повний / без рамки / вікно, роздільність, FPS).
- Переходи: титул → вступна сцена → мапа → рівень → (усі вази у візку) мапа → … → фінал історії.

## Фічі поза полем
- `undo` (кнопка, Y/Z) і `restart-level`; `autosave` прогресу на мапі.
- `world-map` з гілками в довільному порядку; кінець гілки відкриває рівень із золотим уламком (досягнення «Legendary Vase»).
- `achievements` (12): персонажі історії, «Riddle», «This Was His Story», «Hi :)»…
- `localization` EN / JA / ZH, `remap-controls`, `gamepad-support`, `screen-shake-toggle`, видимість сітки.
- Повна гра ~2–3 год, 65 пазлів кампанії (за оглядом 3rd Strike); демо — 13 рівнів у групах «Beginning», «Streams», «Ice», «Trial A».

## Варіації й родичі
- Sokobos (2021) — попередник: більші рівні старого зразка, без візка, тонення, плавання й течій (слова автора на itch).
- Родичі: [sokoban](sokoban.md); [a-monsters-expedition](../thinky/a-monsters-expedition.md) — колоди у воді як плоти; [kwirk](kwirk.md) і [chips-challenge](../maze-arcade/chips-challenge.md) — блок у воді стає підлогою; [ice-sliding-puzzles](ice-sliding-puzzles.md) і [pokemon-overworld-puzzles](pokemon-overworld-puzzles.md) — лід і валуни.
- Осі варіацій:
  - **ціль**: клітини-цілі (Sokoban) / рухомий контейнер, що теж штовхається (тут);
  - **обʼєкт у воді**: тоне й стає опорою (камінь) / пливе за течією (ваза) / замерзає тимчасовим плотом (лід);
  - **хто везе**: ніхто / візок везе вантаж і героя, якщо той штовхає зсередини.

## Цікавинки для курсу
- Візок 2×2 як рухомий контейнер: пасажири зсуваються разом з ним, перевірка всіх клітин фронту — 🥉.
- Штовхання зсередини: герой у візку впирається в борт — і їде разом з ним — 📎.
- Вода з трьома відповідями: тоне / пливе / замерзає — 📎 (таблиця «обʼєкт × клітина»).
- Течія після кожного ходу зсуває плавуче; порядок обробки, коли дві вази пливуть одна за одною, — 📎.
- Лід ковзає до упору, у воді стає тимчасовим плотом — 🌱.
- Плити й ворота з «доки натиснуто» — 🌱.
- Мапа світу з гілками й нагородою за гілку — 🥉.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ рух; `push-object` ↔ вази, каміння, лід; `multi-cell-size` ↔ візок 2×2; `carrier-platform` ↔ візок везе вантаж і героя; `inertia-slide` ↔ лід; `fill-hole` ↔ камінь у воді стає опорою; `button-toggle` ↔ плита → ворота; `goal-counter` ↔ вази `x/y`; `move-counter` ↔ «Moves N»; `undo-unlimited` + `restart-level`; `world-map` + `level-unlock` ↔ мапа; меню, налаштування, мова, клавіші, гучність; `save-progress`; анімація руху, частинки (вибух, міст), звуки й музика.
- **Нема** → пропозиції карток:
  - `+transport-load` (є в корпусі) — візок з місткістю 2×2.
  - `+push-from-inside` (є в корпусі) — тут візок їде і від поштовху ззовні, і зсередини.
  - `+pressure-plate` (є в корпусі) — плита тримає ворота.
  - `+branching-campaign` (є в корпусі) — гілки мапи в довільному порядку.
  - `+intermission-cutscene` (є в корпусі) — сцени з персонажами між рівнями.
  - `+float-drift` «Плавучий обʼєкт у воді зсувається течією щохід» · entities/move · 📎 · слот {dir: per-tile}.
  - `+ice-floe` «Ковзний блок у воді стає тимчасовою підлогою» · entities/interact · 🌱 (родич `fill-hole`).
  - `+cargo-push` «Контейнер везе все, що в ньому, при поштовху» · entities/move · 📎.

## Пропозиції до словників
- `+effect:sink` — обʼєкт іде під воду й стає опорою (повтор: кандидат у корпусі); `set_cell` не каже, що обʼєкт зник.
- `+effect:drift` — зсув течією (повтор).
- `+trigger:stream_tick` — фаза «після ходу» для течій; зараз записано як `after(move)` + `cell(…, stream)`.
- `+feature:grid-visibility` — лінії сітки з кількома рівнями яскравості (не просто вкл/викл, як `grid-toggle`).
- `+card:float-drift`, `+card:ice-floe`, `+card:cargo-push` — див. «Мапу на каталог».

## Джерела
- ⭐ [itch.io: Sokobos 2 Demo](https://martin-games.itch.io/sokobos-2-demo) — гра в браузері; коментарі автора: гілки демо, нові механіки (тонення, плавання, течії), undo кнопкою чи Y/Z.
- [Steam: Sokobos 2](https://store.steampowered.com/app/3422180/) — опис, особливості (візок як частина пазла, ворота, плити, вода), 2–3 год, 12 досягнень.
- [Новини Steam](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3422180&count=20&maxlength=0) — патчі (Bridges 4/10, крижаний блок над затопленим каменем), демо-оновлення з геймпадом і мовами.
- [3rd Strike](https://3rd-strike.com/sokobos-2-review/), [LadiesGamers](https://ladiesgamers.com/sokobos-2-review/), [Gaming Couch Potato](https://www.gamingcouchpotato.co.uk/search/label/Sokobos%202) — огляди з описом механік і структури.
- Демо `index.pck` (Godot 3.5): назви сцен і скриптів (`cart`, `vase`, `stone`, `ice`, `plate`, `gate`, `bridge`, `bomb`, `gold_part`, `water`), прапорці обʼєктів (`sink_flag`, `swim_flag`, `slide_flag`, `melt_flag`, `bomb_flag`, `cry_flag`), тайли течій, HUD «Moves» і лічильник ваз, налаштування.
- YouTube: пошук «Sokobos 2 gameplay».

## Непевне
- (?) Коли тане крижаний пліт (після першого проходу, за N ходів чи інакше) — огляд каже «тимчасовий», механіку не перевірено.
- (?) Візок «не можна штовхнути, якщо перевантажений» (3rd Strike) — що саме вважається перевантаженням, не зʼясовано; так само — з яких боків візок приймає вантаж (у коді є «заборонені напрями» секцій).
- (?) Мости (`bridge`) ламаються — коли саме; бомби є в коді демо, але в жодному з 13 демо-рівнів; чи є в повній грі — не перевірено.
- (?) Розкладка за замовчуванням (WASD чи лише стрілки, клавіша рестарту) не перевірена.
- (?) Чи штовхається ряд з двох обʼєктів — у коді перевіряється лише одна клітина за обʼєктом (`node_in_push_cell`), у грі не перевірено.
