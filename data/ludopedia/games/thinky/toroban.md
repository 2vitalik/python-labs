---
title: Toroban
slug: toroban
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
year: 2025
platforms: [PC, Mac, Linux]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1961850/", best: true, note: "опис: нескінченно загорнуте поле, нелінійний оверворлд, 6 біомів з механіками, 270 пазлів"}
  - {kind: official, url: "https://toroban.com/", note: "сайт: Hebert Games, Discord, YouTube, форма відгуків"}
  - {kind: other, url: "https://steamcommunity.com/app/1961850/reviews/?browsefilter=toprated&l=english", note: "відгуки: offset-блоки, регіони, злипання торо одного кольору, рестарт як частина розвʼязку, інвертований світ"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=1961850&count=15&maxlength=4000", note: "новини Steam: Floating Toros (2026), меню рестартів, сітка G, кнопки регіонів/кольору, портали"}
  - {kind: other, url: "https://ayebear.com/", note: "сайт автора (Eric Hebert): Toroban — проєкт з 2019"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Toroban+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-4dir, keyboard-controls, push-object, impassable-cells, wrap-edges, button-toggle, stick-together, teleport, reach-exit, undo-redo, redo, restart-level, +open-world-puzzles, field-scaling, achievements-window, stats-window, save-progress, +offset-wrap, +infinite-tiling-view, +region-transfer, +multi-agent-sync, +restart-as-move, +float-state, +inverted-world, +collectible-secrets]
proposes: ["+effect:offset_wrap", "+trigger:landed", "+role:region", "+window:restart-menu", "+ui:tile-grid-toggle", "+card:offset-wrap", "+card:region-transfer", "+card:restart-as-move", "+card:infinite-tiling-view"]
author: opus
date: 2026-11-09
---

# Toroban — сокобан на торі: поле нескінченно повторюється, блоки виходять за край і повертаються з протилежного

## Суть
Кожен пазл — сокобан на торі: правий край склеєний з лівим, верхній — з нижнім, і камера показує пазл як нескінченну плитку з копій. Гравець (торо) штовхає блоки на кнопки, тримає ворота відчиненими й ходить «за край», щоб зайти з іншого боку. Біоми додають механіки: регіони (обʼєкти переходять між тор-пазлом і зовнішнім світом), offset-блоки (зсувають склейку країв), кілька торо одночасно, ширяння. Пазли вбудовані в нелінійний оверворлд, де розвʼязані зони віддають блоки в хаб.

## Поле і час
- Квадратна сітка-тор (`wrap-edges`); склейка може бути **зі зсувом**: offset-блоки X/Y міняють вирівнювання (відгук: зсув на 8 на полі шириною 11, повторений 6 разів, дає зсув 4).
- 2.5D, мальована графіка; зум камери (у меню — керування зумом); зум «за межу» перемикає інвертований світ.
- Покроково; анімація переходу через край повільна (відгук).
- Оверворлд нелінійний: біоми Grass (туторіал), Ruins (регіони), Snow (offset), Fall (кілька торо), Desert (комбінації), Cosmic (механіки оверворлду в пазлах). На старті 270 пазлів (Steam), ~27 год (відгук).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Торо | player | колір | крок за вводом; кілька торо рухаються разом; однокольорові злипаються |
| Блок | object | — | штовхається; через край тора виходить з протилежного боку |
| Кнопка | switch | — | блок чи торо на ній → ворота відчинені, поки тримають |
| Ворота | gate | open / closed | прохід лише відчиненими |
| Кнопка регіону | switch | — | активує регіон-пазл; без регіону — повідомлення «region not found» |
| Кнопка кольору | switch | колір | реагує на торо/колір (?) |
| Зруйнована стіна | terrain | — | отвір пазла: обʼєкти ходять між тором і зовнішнім світом |
| Offset-блок X / Y | object | вісь | штовхнутий → зсуває склейку країв тора по своїй осі |
| Обертовий блок | object | — | згадано у відгуку (?) |
| Ціль | static | — | приземлення на неї зараховує (?) |
| Портал оверворлду | terrain | активний / ні | переносить між зонами; неактивний — повідомлення |
| Регіон-пазл | zone | тор | окремий загорнутий простір усередині оверворлду; блоки-нагороди з нього йдуть у хаб |
| Туман | static | — | закриває недоступні зони |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО `move(toro, dir)` для всіх торо пазла.
- КОЛИ `edge(a)` → ТО `wrap(a)` — і торо, і блоки.
- КОЛИ `contact(toro, block)` → ЯКЩО `free(cell_behind)` → ТО `push(block)`; інакше `block`.
- КОЛИ `edge(block)` → ТО `wrap(block)`; блок може обійти тор і впертися у штовхача ззаду (?).
- КОЛИ `enter(block|toro, button)` → ТО `set_state(gate, open)`; КОЛИ `leave(block|toro, button)` → ТО `clear_state(gate, open)`.
- КОЛИ `after(push(offset_block))` → ТО `custom: «склейка країв тора зсувається на 1 по осі блока»`.
- КОЛИ `adjacent(toro, toro)` → ЯКЩО `same(toro, toro, color)` → ТО `attach(toro, toro)`.
- КОЛИ `custom: «обʼєкт перетнув зруйновану стіну регіону»` → ТО `custom: «переходить з тор-пазла у зовнішній світ або навпаки»`.
- КОЛИ `input(restart)` → ТО `restart`; сам рестарт — крок історії, його можна скасувати undo (рестарт як частина розвʼязку).
- КОЛИ `input(float)` → ТО `set_state(toro, floating)` — ширяння над перешкодами, менше тертя (оновлення 2026).
- КОЛИ `enter(toro, button)` → ЯКЩО `state(toro, floating)` → ТО нічого; кнопки, портали й цілі спрацьовують при приземленні.
- КОЛИ `enter(toro, portal)` → ЯКЩО `state(portal, active)` → ТО `teleport(toro, linked_portal)`; інакше `message(«portal inactive»)`.
- КОЛИ `custom: «зум за межу»` → ТО `custom: «світ інвертується; видно секретні пазли»`.
- КОЛИ `custom: «умову пазла виконано»` → ТО `win`; `spawn(reward_block, hub)` для зони (кожна підзона віддає один блок у хаб).
- КОЛИ `counter(hub_blocks, ==, 37)` → ТО `unlock(post_game)` (відгук: 37 блоків до певного місця).
- Перемога пазла: стан цілей (?). Поразки нема; глухий кут → undo/рестарт. Рахунку нема.

## Керування і ввід
- Клавіатура або геймпад (повна підтримка контролера, Steam): рух, undo, redo, рестарт, зум, ширяння; G — сітка суші й води.
- Кілька торо не вибираються окремо — рухаються разом; розлучені торо збирають, вийшовши й зайшовши в пазл (відгук) (?).

## Вікна, меню, HUD
- `game-screen`: оверворлд і пазли в одному світі; пазл-тор показаний нескінченною плиткою.
- `pause-menu` з гайдом керування (`help-window`) і **меню рестартів**: звичайний, оверворлду, «нерозвʼязані пазли» (захист від випадкового скидання).
- `settings-window`: перемикач сітки (G), захист «unsolve».
- `toast`-повідомлення: неактивний портал, кнопка без регіону.
- `achievements-window`, `stats-window` (Steam Achievements, Stats).

## Фічі поза полем
- `undo`, `redo` (зокрема скасування рестарту й ширяння), `restart-level` у трьох масштабах.
- `world-map` як нелінійний оверворлд; `collectibles`-подібні секретні пазли в інвертованому світі.
- `cloud-save`; `gamepad-support`; Cosmic-зона — у розробці на реліз 01.12.2025.

## Варіації й родичі
- Родичі: [Patrick's Parabox](patricks-parabox.md) (пазли в пазлах; відгук: «Toroban важчий»), [Recursed](recursed.md), [A Monster's Expedition](a-monsters-expedition.md) (оверворлд), [Arranger](arranger.md) і [Gridmount](gridmount.md) (загортання), Manifold Garden (відгук).
- **Осі варіацій**: склейка країв — нема / тор / тор зі зсувом (offset) · пазл — замкнений / з отворами в зовнішній світ (регіони) · аватарів — один / кілька синхронних / злиплі за кольором.

## Цікавинки для курсу
- Тор: `wrap` для руху й штовхання; блок, що обходить тор і впирається в самого штовхача — 📎.
- Склейка зі зсувом (offset): координати за модулем зі зміщенням, яке змінює гра — 🥉.
- Нескінченна плитка-рендер тора: камера показує копії поля — 📎.
- Регіони: обʼєкт переходить між двома топологіями (тор ↔ звичайна площина) — 🥈.
- Рестарт як звичайний хід в історії undo — 🌱 (стек станів містить і рестарт).
- Ширяння: стан, при якому вхід у клітину не тригерить кнопку до приземлення — 📎.

## Мапа на каталог
- Є: `move-4dir`, `keyboard-controls` · `push-object` · `impassable-cells` · `wrap-edges` ↔ тор · `button-toggle` ↔ кнопка й ворота · `stick-together` ↔ однокольорові торо · `teleport` ↔ портали · `reach-exit` ↔ ціль (?) · `undo-redo`, `redo`, `restart-level` · `field-scaling` ↔ зум · `achievements-window`, `stats-window`, `save-progress`.
- **Нема** → пропозиції карток:
  - `+offset-wrap` «Тор зі зсувом склейки, що змінюється в грі» · entities/move · 🥉 · слоти {axis, offset}.
  - `+region-transfer` «Обʼєкти переходять між вкладеним пазлом і зовнішнім світом» · levels/progression · 🥈.
  - `+restart-as-move` «Рестарт — крок історії, який можна скасувати» · game-logic/history · 🌱.
  - `+infinite-tiling-view` «Тор показано нескінченною плиткою копій» · interface/render · 📎.
  - `+open-world-puzzles`, `+multi-agent-sync`, `+float-state`, `+inverted-world`, `+collectible-secrets`.

## Пропозиції до словників
- `+effect:offset_wrap` — змінити зсув склейки країв тора.
- `+trigger:landed` — сутність приземлилась після ширяння/стрибка (підтверджую; у `vocab/` ще нема).
- `+role:region` — вкладений пазл-простір у світі зі своєю топологією.
- `+window:restart-menu` — меню вибору масштабу рестарту (рівень / світ / нерозвʼязані).
- `+ui:tile-grid-toggle` — показ сітки клітин клавішею.
- `+card:offset-wrap`, `+card:region-transfer`, `+card:restart-as-move`, `+card:infinite-tiling-view` — див. вище.

## Джерела
- ⭐ [Steam](https://store.steampowered.com/app/1961850/) — «infinitely wrapping puzzle game», біоми й механіки (блоки, кнопки, ворота, регіони, offset X/Y, торо), 270 пазлів, реліз 01.12.2025, контролер.
- [toroban.com](https://toroban.com/) — Hebert Games LLC, Discord, YouTube, форма відгуків.
- [Відгуки Steam](https://steamcommunity.com/app/1961850/reviews/?browsefilter=toprated&l=english) — offset-арифметика, регіони, злипання однокольорових торо, рестарт як частина розвʼязку, інвертований світ через зум, 37 блоків у хаб, Cosmic-портали й паралельні версії рівня.
- [Новини Steam (API)](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=1961850&count=15&maxlength=4000) — Floating Toros (10.06.2026), меню рестартів, сітка G, повідомлення порталів і регіонів.
- [ayebear.com](https://ayebear.com/) — автор, проєкт з 2019.
- YouTube: пошук «Toroban gameplay».

## Непевне
- (?) Точна умова розвʼязання пазла: блоки на кнопках, торо на цілі чи відчинені ворота.
- (?) Як діють кнопки кольору й обертові блоки.
- (?) Чи блок, обійшовши тор, може впертися в самого штовхача (логічно, але не підтверджено).
- (?) Що означає «multiplayer» у новинах (кілька торо чи локальна гра вдвох); Steam перелічує лише Single-player.
- (?) Cosmic: «паралельні світи» — перемикання між двома версіями рівня; деталі відсутні.
