---
title: Pight
slug: pight
aka: []
family: push-slide
also: [build-sim]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2026
platforms: [PC, Mac, Linux, Android, iOS]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2682270/", best: true, note: "опис: поршні штовхають і тягнуть, липкі блоки, динаміт, портали; 90 рівнів, 8 механік (нова кожні ~10 рівнів), необмежений undo, редактор, без тексту"}
  - {kind: steam, url: "https://store.steampowered.com/app/2779090/Pight_Demo", note: "безкоштовне демо (червень 2024)"}
  - {kind: official, url: "https://mindlabor.dev/pight", note: "сайт Mindlabor: Steam, Google Play, App Store, трейлер, прескіт"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=3784463919", note: "гайд досягнень: головний блок у фініш, липкі «grab»-поршні, твердий блок, TNT, енергоблок, портал, меню під білою точкою"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=3784977001", note: "китайсько-англійський гайд: сітка 7×11 вмикається в меню («#»), хід = клік по поршню"}
  - {kind: other, url: "https://apps.apple.com/us/app/pight/id6752226126", note: "App Store: «move a block toward the bulb», поршні, динаміт, портали"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=Lzw602VvR8s", note: "трейлер (посилання з офіційного сайту)"}
stage: v1
coverage: 45
mechanics: [cell-click, push-object, pull-object, impassable-cells, reach-exit, explode-area, teleport-pair, undo-unlimited, restart-level, level-select, sequential-levels, in-game-editor, achievements-window, sound-effects, background-music, +piston, +sticky-piston, +sticky-group, +powered-by-adjacent, +grid-overlay-toggle]
proposes: ["+role:actuator", "+cond:powered(a)", "+effect:extend(a, dir)", "+effect:retract(a)", "+card:piston"]
author: opus
date: 2026-11-09
---

# Pight — клацай поршні, щоб штовхати й тягнути блоки й довести головний блок до лампочки: редстоун Minecraft без коду

## Суть
Мінімалістичний пазл студії Mindlabor за мотивами поршнів Minecraft. Аватара нема: гравець клацає поршні на полі, кожен висувається чи втягується, штовхаючи або (липкий) тягнучи блоки. Мета — довести головний блок на клітину з лампочкою, щоб вона засвітилась. Кожні ~10 рівнів додається нова механіка (усього 8): липкі блоки, що рухаються групою, нерухомі «тверді» блоки, динаміт, енергоблоки, портали; навчання нема, правила відкриваються експериментом.

## Поле і час
- Квадратна сітка; гайд нумерує клітини 7 рядів × 11 стовпців, сітку можна показати кнопкою «#» у меню. Пунктирна рамка — межа рівня.
- Шари: підлога (порожня / лампочка) + блоки й поршні (один на клітину).
- Хід = один клік по поршню й анімація всіх наслідків; без вводу нічого не рухається (`time: turn`, «Playable without Timed Input»).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Поршень (сіре тіло, фіолетова грань) | switch | напрям грані; висунутий / втягнутий | клік → висувається на 1 і штовхає блок(и) перед гранню; ще клік → втягується (?) |
| Липкий поршень «grab» (зелена хвиляста грань) | switch | напрям | штовхає, а втягуючись — тягне прилиплий блок; два липкі поршні можуть тягати один одного |
| Головний блок (сірий з ромбами) | object | один на рівень | треба доставити на лампочку; знищений — рівень зіпсовано |
| Лампочка (іскра) | zone | клітина-фініш | головний блок на ній → світло, перемога |
| Звичайний блок (білий брук) | object | — | штовхається й тягнеться |
| Липкий блок (зелений) | object | — | зчіплює сусідів у «конструкцію», що рухається одним поштовхом |
| Твердий блок (жовто-чорний) | static | — | не рухається; поршень у нього впирається |
| Динаміт (TNT) | hazard | — | вибухає й руйнує блоки поруч, зокрема головний; умова підриву — (?) |
| Енергоблок (синій з блискавкою) | resource | — | живить сусідній «електричний» поршень; відсунути блок чи поршень → живлення зникає (?) |
| Портал | static | пара (?) | блок, що входить, виходить з іншого порталу |
| Межа рівня | static | пунктир | у неї можна заштовхнути блок (досягнення «Off the Grid»); що з ним стається — (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, piston)` → ЯКЩО `state(piston, retracted)` and `custom: «ряд перед гранню можна зсунути (нема твердого блока / упору)»` → ТО `set_state(piston, extended)`, `push`.
- КОЛИ `input(click, piston)` → ЯКЩО `custom: «перед гранню твердий блок або ряд упирається»` → ТО `block`.
- КОЛИ `input(click, piston)` → ЯКЩО `state(piston, extended)` → ТО `set_state(piston, retracted)` (?).
- КОЛИ `state_off(sticky_piston, extended)` → ЯКЩО `occupied(face_cell, block)` → ТО `pull(block)` — так липкий поршень тягне блоки й інші поршні.
- КОЛИ `custom: «рухається блок, зчеплений із липким»` → ТО `custom: «уся зчеплена група рухається разом»` (досягнення «Bulk Order» — посунути всю конструкцію одним поштовхом).
- КОЛИ `contact(piston_face, hard_block)` → ТО `block`.
- КОЛИ `custom: «динаміт підірвано»` → ТО `explode(area)`, `disappear` блоків поруч; ЯКЩО `custom: «зачепило головний блок»` → ТО `custom: «рівень не пройти — undo»`.
- КОЛИ `enter(block, portal)` → ТО `teleport(block, pair_portal)`.
- КОЛИ `custom: «енергоблок поруч з поршнем»` → ТО `set_state(piston, powered)`; відсунули — `clear_state(piston, powered)` (?).
- КОЛИ `enter(main_block, bulb)` → ТО `win`, `custom: «лампочка світиться»`, `next_level`.
- Перемога: головний блок на лампочці. · Поразка: формально нема; зруйнований головний блок чи глухий кут — undo/restart. · Рахунок: нема.

## Керування і ввід
- Клік / тап по поршню — єдина дія на полі; поршень, який варто натиснути, підсвічується під курсором.
- Іконки праворуч угорі: рестарт і undo (необмежений).
- Повна підтримка геймпада, «Keyboard Only», «Mouse Only», «Touch Only» (Steam-категорії); на мобільних — тап.

## Вікна, меню, HUD
- `game-screen`: поле, біла точка-меню ліворуч угорі, рестарт і undo праворуч; тексту нема.
- `pause-menu` (біла точка): стовпчик іконок — серед них «#» (показати сітку), Discord, внизу праворуч — вибір рівня.
- `level-select` — 90 рівнів (дев'ять десятків за механіками).
- `editor-window` — редактор рівнів.
- `achievements-window` — Steam-досягнення (15).
- Переходи: game-screen ⇄ pause-menu → level-select / редактор; лампочка засвітилась → наступний рівень.

## Фічі поза полем
- `levels-sequential` 90 рівнів, нова механіка кожні ~10; `undo` без ліміту, `restart-level`.
- `level-editor`; `achievements` (15); `cloud-save`, «Save Anytime»; `grid-toggle` (сітка «#»); налаштування гучності.
- Без тексту й туторіалів (`tutorial` свідомо відсутній).

## Варіації й родичі
- [build-sim/minecraft-redstone](../build-sim/minecraft-redstone.md) — першоджерело: звичайні й липкі поршні, живлення, ліміт ряду; [newtons-crates](newtons-crates.md) — поштовх ряду; [prickle](prickle.md) — липке зчеплення в одну групу; [block-in-the-lock](block-in-the-lock.md) — рух групою; [rush-hour](rush-hour.md) — довести один блок до виходу, розсуваючи інші.
- Осі варіацій: **хто рухає** (аватар / поршні, якими клацаєш / програма редстоуну); **тягнення** (нема / лише липкий поршень / липкі блоки тягнуть сусідів); **руйнування** (нема / динаміт / межа поля); **живлення** (завжди / лише поруч з енергоблоком).

## Цікавинки для курсу
- Поршень: висунути з поштовхом цілого ряду й втягнути з тягненням (липкий) — 🥉.
- Липкі блоки: пошук звʼязної групи й перевірка, що вся група може зсунутись, — 🥈.
- Головний блок → лампочка як умова перемоги без аватара — 🌱.
- Динаміт з радіусом і перевіркою «знищено ціль» — 📎.
- Портали для блоків (вхід з напрямом → вихід) — 📎.
- Розвʼязувач BFS по станах (позиції блоків + висунуті поршні) — 🥇.

## Мапа на каталог
- Є: `cell-click` ↔ клік по поршню; `push-object` + `pull-object` ↔ поршні; `impassable-cells` ↔ твердий блок; `reach-exit` ↔ лампочка; `explode-area` ↔ TNT; `teleport-pair` ↔ портали; `undo-unlimited` + `restart-level`; `level-select` + `sequential-levels`; `in-game-editor`; `achievements-window`; `sound-effects` + `background-music`.
- **Нема** → пропозиції карток:
  - `+piston` «Поршень: клік висуває й штовхає ряд, ще клік втягує» · entities/interact · 🥉 · слот {sticky: bool, limit}.
  - `+sticky-piston` — підтип із тягненням при втягуванні · 📎.
  - `+sticky-group` «Липкі блоки зчеплюють сусідів у групу» · entities/interact · 🥈.
  - `+powered-by-adjacent` «Механізм працює лише поряд з джерелом живлення» · entities/state · 📎.
  - `+grid-overlay-toggle` «Показати сітку поверх поля» · interface/settings · 🌱.

## Пропозиції до словників
- `+role:actuator` — механізм на полі, яким клацає гравець і який рухає інших (поршень), — ні `switch`, ні `player`.
- `+cond:powered(a)` — сутність живиться від сусіднього джерела.
- `+effect:extend(a, dir)` / `+effect:retract(a)` — висунути / втягнути поршень.
- `+card:piston`.

## Джерела
- ⭐ [Steam: Pight](https://store.steampowered.com/app/2682270/) — опис геймплею й фіч, 90 рівнів, 8 механік, 8 серпня 2026, Mindlabor.
- [Steam: Pight Demo](https://store.steampowered.com/app/2779090/Pight_Demo) — той самий опис, демо з 7 червня 2024.
- [Гайд досягнень](https://steamcommunity.com/sharedfiles/filedetails/?id=3784463919) — «push the sticky block, which holds the main block into the finish», «sticky grabs», «Hard Block», TNT знищує головний блок, енергоблок і «electric grab block», портал з рівня 77, меню під білою точкою.
- [Гайд 1–90](https://steamcommunity.com/sharedfiles/filedetails/?id=3784977001) — сітка 7×11 через іконку «#», хід = клік по поршню, «два поршні тягають один одного».
- [App Store](https://apps.apple.com/us/app/pight/id6752226126) — «move a block toward the bulb», динаміт, портали; версія 1.0 від 8 серпня.
- Скриншоти Steam — типи блоків (брук, липкий зелений, жовто-чорний, TNT, блискавка, головний з ромбами, лампочка), рестарт і undo праворуч угорі.

## Непевне
- (?) Чи поршень втягується другим кліком, чи сам після поштовху; скільки блоків у ряд він штовхає.
- (?) Як підривається динаміт (поштовх, контакт із поршнем, живлення?).
- (?) Що саме робить енергоблок і «electric grab block» («It's alive. Be careful.»); що стається з блоком, заштовхнутим у межу рівня.
- (?) Порядок механік за десятками (липкі поршні ≤8, липкі блоки ≤12, межа ~21, твердий ~31, TNT ~41, енергія ≤65, портали ~77) — з досягнень, не з гри.
- (?) Темний блок з точковим хрестом на одному скриншоті — можливо, портал.
