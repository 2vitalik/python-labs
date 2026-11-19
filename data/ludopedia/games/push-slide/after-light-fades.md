---
title: After Light Fades
slug: after-light-fades
aka: [ALF]
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
platforms: [PC (Windows, macOS, Linux), Steam Deck]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1717940/After_Light_Fades/", best: true, note: "опис: сім світів, 100+ пазлів, дзеркала, магніти, вогонь, ліани, клони; артефакт кожного світу віддаєш разом із його механікою; редактор і Steam Workshop; трейлер і 10 знімків"}
  - {kind: other, url: "https://gameluster.com/?p=114585", note: "огляд Gameluster: найповніший перелік обʼєктів і плиток (лід, мости, ріки, пілони, грудки землі, черепи й скарабеї)"}
  - {kind: other, url: "https://lastwordongaming.com/?p=15405", note: "огляд Last Word on Gaming (Steam Deck): камінь на ключ → двері → вихід; кристали тягнуть і перетворюють"}
  - {kind: other, url: "https://www.gamespress.com/After-Light-Fades-a-Magical-Puzzle-Journey-About-Letting-Go-Now-Availa", note: "прес-реліз: портали, духи-охоронці, ланцюги, перенаправлення вогню, ріст ліан, 7 механік, що відбирають"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=1717940", note: "новини Steam: патчі (дзеркала, бомби, жуки, тіні, безодні, верхня камера, перепризначення клавіш, редактор)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=After+Light+Fades+gameplay", note: "пошук; геймплей і серія розробника Puzzle Design Odyssey"}
stage: v1
coverage: 35
mechanics: [move-by-input, move-4dir, push-object, pull-object, impassable-cells, key-and-door, reach-exit, undo-unlimited, restart-level, inertia-slide, floor-types, one-way-cell, fill-hole, cell-transform, destructible-blocks, explode-area, teleport-pair, world-map, in-game-editor, editor-palette, editor-draw-tools, level-exchange, controls-remap, help-window, settings-window, volume-control, achievements-window, +ability-relinquish, +fire-spread, +crumbling-floor, +phase-blocks, +electric-signal, +avatar-clones, +auto-walkers, +collectible-secrets, +workshop-sharing, +camera-view-toggle]
proposes: ["+effect:burn", "+effect:attract", "+effect:break", "+effect:reflect", "+role:portal", "+feature:view-toggle", "+card:ability-relinquish", "+card:phase-blocks", "+card:avatar-clones", "+card:auto-walkers", "+card:camera-view-toggle"]
author: opus
date: 2026-11-19
---

# After Light Fades — Sokoban про горе: кожен світ дає Алісі нову силу, а наприкінці світу вона кидає артефакт у безодню й утрачає цю силу назавжди

## Суть
Аліса проходить сім світів-етапів горя (разом 100+ пазлів): штовхає й тягне ящики, камені, ключі, дзеркала, кристали в клітинних кімнатах і виходить з рівня. Кожен світ привʼязаний до **артефакту, що дає механіку**; наприкінці світу Аліса кидає артефакт у безодню й відмовляється від механіки назавжди. Довкола — шар «стихій»: вогонь, що горить травою, ріки, що несуть, лід, ліани, струм від пілонів, бомби, клони Аліси й самохідні жуки.

## Поле і час
- Квадратна сітка кімнати під фіксованою камерою 3/4 (ізометрія); з червня 2025 — перемикач камери «згори» (V / L2).
- Хід = крок Аліси; світ стоїть без вводу («Playable without Timed Input»); самохідні сутності (жуки, тіні) ходять своїми кроками (?).
- Шари: підлога з типами (трава, ріка, лід, міст, одностороння, крихка), обʼєкти (ящики, камені, ключі, дзеркала, бомби), безодні-ями.
- Рівні — вузли на мапі світу (острови з назвами «Crystal Lagoon», «Enigma Plateau»); проходження нелінійне (тег «Nonlinear»).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Аліса | player | напрям погляду | рух 4 напрямки; штовхає; тягне ключі й грудки |
| Клони Аліси | player | напрям погляду | кілька Аліс на полі (патч «Alice(s)»); як ними керують — (?) |
| Ящик | object | — | штовхається; горить і ламається (Gameluster) |
| Камінь / скеля | object | — | штовхається; підривається бомбою |
| Ключ | object | — | лише тягнеться Алісою; певні блоки можуть його штовхнути |
| Двері | gate | замкнено / відчинено | відчиняються ключем (камінь на ключі — LWOG) (?) |
| Крижаний блок | object | — | ковзає до нерухомої перешкоди |
| Грудка землі | object | — | «штовхається», лише коли Аліса відходить (тягнеться (?)); засипає яму; від кристала стає іншою плиткою |
| Кристал | object | — | тягне за собою камінь певного виду; перетворює обʼєкт на інший |
| Дзеркало | object | — | штовхається (патч); крізь дзеркала сутності переносяться (?) |
| Магніт | object | — | (?) — назване в описі й огляді, правило не знайдено |
| Бомба | object | — | вибух руйнує скелі (і дзеркала — як баг) |
| Блок, що ламається з одного боку | object | бік | розбивається лише з того боку |
| Блоки, що зникають і зʼявляються | gate | є / нема | перемикаються (тригер — (?)) |
| Факел, жаровня | hazard | — | джерело вогню |
| Трава | terrain | горить / ні | підпалена горить вічно; вогонь іде нею далі (трейлер) |
| Ріка | terrain | напрям течії | несе того, хто в ній |
| Міст | terrain | — | прохід над водою/ямою (?) |
| Одностороння плитка | terrain | напрям | прохід лише в один бік |
| Крихка плитка | terrain | — | після того, як з неї зійти, стає непрохідною |
| Безодня (яма) | hazard | — | сюди падають; сюди ж кидають артефакт |
| Джерело струму, пілон | switch | живлення | «connecting circuits» — живлять механізми (?) |
| Ліани | terrain | — | «growing vines» — ростуть (?) |
| Жук, тінь-двійник | neutral | — | самохідні (патч: «auto-moving types»); правило руху й чи шкодять — (?); патч згадує камінь, що «зсувається вниз через тінь» (?) |
| Снаряди | projectile | — | у рівнях розробника від них треба захищатись (?) |
| Особлива плитка | switch | — | у деяких рівнях вмикається окремою кнопкою |
| Артефакт | pickup | механіка світу | наприкінці світу — кинути в безодню |
| Череп, скарабей | pickup | — | колекційні: черепи — часто за альтернативний розвʼязок; скарабеї — за рівні-виклики |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(alice, dir)`.
- КОЛИ `contact(alice, box)` → ЯКЩО `free(cell_behind)` → ТО `push`; інакше `block` (так само камені, дзеркала).
- КОЛИ `input(dir)` → ЯКЩО `occupied(behind_alice, key)` → ТО `pull(key)` — ключ не штовхається Алісою.
- КОЛИ `contact(pusher_block, key)` → ЯКЩО `free(cell_behind)` → ТО `push` — особливі блоки штовхають ключ.
- КОЛИ `custom: «ключ / камінь на своєму місці»` → ТО `set_state(door, open)` (?).
- КОЛИ `enter(alice, exit)` → ТО `win`, `next_level`.
- КОЛИ `contact(alice, ice_block)` → ЯКЩО `free(cell_behind)` → ТО `slide(ice_block, dir)`.
- КОЛИ `input(dir)` → ЯКЩО `occupied(behind_alice, dirt)` → ТО `pull(dirt)` (?).
- КОЛИ `enter(dirt, hole)` → ТО `disappear_a`, `set_cell(hole, floor)`.
- КОЛИ `contact(crystal, dirt)` → ТО `transform(dirt, other_tile)`.
- КОЛИ `custom: «кристал рушає»` → ТО `pull(stone_kind)`.
- КОЛИ `contact(fire, box)` → ТО `custom: «ящик згорає»`.
- КОЛИ `contact(fire, grass)` → ТО `set_state(grass, burning)` — назавжди; вогонь іде сусідньою травою (?).
- КОЛИ `custom: «бомба детонує»` → ТО `explode(area)`; скелі в зоні → `disappear_b`.
- КОЛИ `contact(alice, one_side_block)` → ЯКЩО `facing(alice, weak_side)` → ТО `disappear_b`; інакше `block`.
- КОЛИ `leave(alice, fragile_tile)` → ТО `set_cell(fragile_tile, impassable)`.
- КОЛИ `enter(a, river)` → ТО `move(a, flow_dir)` — течія несе.
- КОЛИ `input(dir)` → ЯКЩО `cell(next, one_way)` і `custom: «проти напряму плитки»` → ТО `block`.
- КОЛИ `custom: «джерело зʼєднане з пілоном»` → ТО `set_state(pylon, powered)` (?).
- КОЛИ `enter(a, abyss)` → ТО `fall(a)` (?); для Аліси — `lose` (?).
- КОЛИ `custom: «сутність проходить дзеркалом»` → ТО `teleport(a, other_side)` (?) — з патча про жуків, що «телепортувались дзеркалами».
- КОЛИ `turn_end(alice)` → ТО `custom: «жуки й тіні роблять свій крок»` (?).
- КОЛИ `input(action)` → ЯКЩО `cell(under_alice, special_tile)` → ТО `custom: «активувати плитку»`.
- КОЛИ `input(undo)` → ТО `undo(1)` — без ліміту, «як завгодно далеко назад».
- КОЛИ `input(reset)` → ТО `restart`.
- КОЛИ `custom: «артефакт кинуто в безодню наприкінці світу»` → ТО `message("This memory is now released")`, `custom: «механіку артефакту вимкнено назавжди»`.
- Перемога: вийти з рівня (двері / вихід). · Поразка: (?) — у джерелах лише глухі кути, що лікуються undo / reset. · Рахунок: нема; колекційні черепи (альтернативні розвʼязки) і скарабеї (рівні-виклики).

## Керування і ввід
- Клавіатура (повністю, «Keyboard Only Option») або геймпад (частково; DualShock): хрестовина — крок, кнопки undo і reset.
- Особлива плитка — окрема кнопка дії в рівнях, де вона є.
- V / L2 — камера «згори»; повне перепризначення клавіш і кнопок (липень 2025, Options → Controls → Remap Controls).
- Оглядачі: Аліса рухається швидко, легко «проскочити» зайву клітину — звідси часте undo.

## Вікна, меню, HUD
- `splash-screen` — арт із героїнею й лого.
- `map-window`: мапа світу — острови-вузли з назвами; Аліса сідає, щоб увійти в рівень.
- `game-screen`: кімната під камерою 3/4; назва рівня внизу («• Dopplegangers I •»); вікно черепів (`custom-window`) вмикається окремо.
- `help-window`: що робить кожен предмет (без позначок прохідності — Gameluster).
- `dialogue-window`: сюжетні сцени (додано ще одну в першому світі).
- `custom-window`: «This memory is now released» — відпущений артефакт.
- `settings-window`: роздільність (випадний список), повноекранне вікно, гучність, Remap Controls, «About the Soundtrack».
- `editor-window`: редактор рівнів — вікно інструментів, малювання, підсвітка клітини, перемикач верхньої камери, вступна довідка з відео; Steam Workshop — завантажити й грати чужі рівні.
- `achievements-window`: 12 досягнень Steam.
- Переходи: мапа → рівень → (вихід) мапа; кінець світу → сцена з безоднею → наступний світ.

## Фічі поза полем
- `world-map` + нелінійні рівні: сім світів, 100+ пазлів; кінець світу забирає механіку.
- `undo` без ліміту, `restart-level`.
- `level-editor` з усіма елементами гри + `level-sharing` через Steam Workshop (з релізу; бета у квітні 2025).
- `remap-controls`, `gamepad-support` (частково), перемикач камери, `volume-sliders`.
- `collectibles`: черепи й скарабеї; `achievements` (12); Steam Cloud.
- Демо (Next Fest 2024, Box Pushing Fest 2025); стріми й відеосерія розробника.

## Варіації й родичі
- [Sokoban](sokoban.md) — основа; [Gentoo Rescue](gentoo-rescue.md) — лід і ковзання.
- [Magnet Block](magnet-block.md), [Kye](kye.md) — магніти в Sokoban.
- [Escape (Tom 7)](escape-tom7.md) — панелі, дроти, лазери в покроковому Sokoban.
- [Mirror Isles](../thinky/mirror-isles.md) — дзеркала як переміщення, а не відбивання променя.
- [Isles of Sea and Sky](../thinky/isles-of-sea-and-sky.md) — Sokoban-світ із мапою островів.
- [Stephen's Sausage Roll](../thinky/stephens-sausage-roll.md) — вогонь як стихія в пазлі.
- Осі варіацій:
  - **доля механіки**: дається назавжди (більшість ігор) / дається й забирається (After Light Fades);
  - **як рухають ключ**: штовхати / лише тягнути / іншим блоком;
  - **вогонь**: шкодить / поширюється травою / горить вічно.

## Цікавинки для курсу
- Відмова від механіки: набір правил рівня залежить від прогресу гравця — 🥈 (правила як дані, що вмикаються й вимикаються).
- Тягнути лише певні обʼєкти (ключ, грудка) і штовхати їх лише особливим блоком — 📎.
- Вогонь, що йде травою й горить вічно — 📎 (поширення по сусідах).
- Крихка плитка: зійшов — і клітина стала стіною — 🌱.
- Ріка-течія, що несе сутність щоходу — 📎.
- Undo без ліміту з утриманням кнопки — 🌱 (стек станів).
- Редактор із тими самими інструментами, що в розробника, + обмін рівнями — 🥈.

## Мапа на каталог
- Є: `move-by-input` + `move-4dir` ↔ крок; `push-object` / `pull-object` ↔ ящики / ключі й грудки; `impassable-cells` ↔ стіни й живопліт; `key-and-door` + `reach-exit` ↔ ключ → двері → вихід; `undo-unlimited` + `restart-level`; `inertia-slide` ↔ лід; `floor-types` ↔ ріка, трава, міст; `one-way-cell` ↔ односторонні плитки; `fill-hole` ↔ грудка в ямі; `cell-transform` ↔ кристал перетворює; `destructible-blocks` + `explode-area` ↔ бомби й скелі; `teleport-pair` ↔ портали з прес-релізу (?); `world-map`; `in-game-editor` + `editor-palette` + `editor-draw-tools` + `level-exchange` ↔ редактор і Workshop; `controls-remap`; `help-window`, `settings-window`, `volume-control`, `achievements-window`.
- **Нема** → пропозиції карток:
  - `+fire-spread`, `+crumbling-floor`, `+electric-signal`, `+collectible-secrets`, `+workshop-sharing` — уже в корпусі.
  - `+ability-relinquish` «Механіку дали, потім забрали назавжди» · game-logic/rules · 🥈 · слот {when: world_end}.
  - `+phase-blocks` «Блоки, що зникають і зʼявляються за перемиканням» · entities/state · 📎.
  - `+avatar-clones` «Кілька копій аватара на полі» · entities/move · 🥉 · слот {control: sync|switch}.
  - `+auto-walkers` «Самохідні сутності (жуки, тіні) крокують після гравця» · entities/move · 📎.
  - `+camera-view-toggle` «Перемикач камери 3/4 ↔ згори без зміни логіки» · interface/render · 🌱.

## Пропозиції до словників
- `+effect:burn` — обʼєкт згорає від вогню (ящик) або клітина загорається (трава).
- `+effect:attract` — магніт тягне обʼєкт (правило магнітів у грі не підтверджене).
- `+effect:break` — розбити блок (з одного боку, бомбою).
- `+effect:reflect` — дзеркальне перенесення / відбиття (тут дзеркало переносить сутність (?)).
- `+role:portal` — пара проходів (портали з прес-релізу).
- `+feature:view-toggle` — перемикання камери 3/4 ↔ згори.
- `+card:ability-relinquish`, `+card:phase-blocks`, `+card:avatar-clones`, `+card:auto-walkers`, `+card:camera-view-toggle` — див. «Мапу на каталог».

## Джерела
- ⭐ [Steam: After Light Fades](https://store.steampowered.com/app/1717940/After_Light_Fades/) — опис (артефакти й механіки, сім світів, 100+ пазлів, редактор і Workshop), категорії (12 досягнень, Keyboard Only, Playable without Timed Input, Camera Comfort), трейлер і 10 знімків (переглянуто: мапа світу, вогонь травою, ріки, ями, ящики «?»).
- [Gameluster: огляд](https://gameluster.com/?p=114585) — перелік обʼєктів і плиток, undo/reset, фіксована камера 3/4, довідка, черепи й скарабеї, грудки землі й глухі кути.
- [Last Word on Gaming: огляд](https://lastwordongaming.com/?p=15405) — базовий цикл «камінь на ключ, двері, вихід»; кристали; деякі обʼєкти штовхаються лише з вільною клітиною позаду; undo без ліміту.
- [Gamespress: прес-реліз](https://www.gamespress.com/After-Light-Fades-a-Magical-Puzzle-Journey-About-Letting-Go-Now-Availa) — дзеркала, магніти, трансмутація, духи-охоронці, клони, портали, ланцюги, вогонь, ліани; «each of the 7 key mechanics… is eventually relinquished».
- [Steam News API, app 1717940](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=1717940) — патчі: дзеркала, бомби, жуки й тіні, безодні, течія й снаряди в рівнях розробника, верхня камера, перепризначення, редактор.
- YouTube: пошук «After Light Fades gameplay».

## Непевне
- (?) Правила магнітів, дзеркал (переносять чи відбивають), порталів, духів-охоронців, ліан і струму — названі в джерелах, механізм не описано.
- (?) Як керують клонами Аліси (одночасно чи по черзі) і як ходять жуки й тіні.
- (?) Мета рівня: «камінь на ключ → двері → вихід» — зі слів одного огляду; чи всюди так.
- (?) Чи вбиває безодня, вогонь чи снаряд Алісу, чи це лише глухі кути.
- (?) Який артефакт дає яку механіку і в якому світі.
- (?) Підлога на частині рівнів виглядає гексагональною (восьмикутна бруківка) — логіка, за всіма описами, квадратна.
