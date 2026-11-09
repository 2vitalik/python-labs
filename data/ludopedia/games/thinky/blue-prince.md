---
title: Blue Prince
slug: blue-prince
aka: []
family: thinky
also: [roguelike, board-digital]
klass: hybrid
axes:
  field: square
  time: turn
  opponent: none
  info: hidden
  random: runtime
  goal: state
year: 2025
platforms: [PC, PS5, Xbox Series, macOS, Switch 2]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Blue_Prince_(video_game)", best: true, note: "суть: маєток 9×5, драфт 1 з 3 планів, кроки 50/день, ключі/самоцвіти/монети, щоденний скид, Room 46, постійні апгрейди"}
  - {kind: fandom, url: "https://blueprince.wiki.gg/wiki/Drafting", note: "повні правила драфту: пул, рідкість, вартість у самоцвітах, форми кімнат за позицією, орієнтація, барикади"}
  - {kind: fandom, url: "https://blueprince.wiki.gg/wiki/Room_Directory", note: "каталог кімнат: кольорові групи, Outer Rooms, Studio Additions, Found Floorplans"}
  - {kind: fandom, url: "https://blueprince.wiki.gg/wiki/Items", note: "ресурси й предмети: ключі, монети, самоцвіти, кості, їжа, інструменти"}
  - {kind: fandom, url: "https://blueprince.wiki.gg/wiki/Ivory_Dice", note: "кості слонової кістки: перетягнути три плани, скид щодня"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Blue+Prince", note: "пошук Steam"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Blue+Prince+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, key-and-door, item-pickup, inventory-items, round-currency, shop-window, shop-catalog, collect-quota, reach-exit, permadeath, run-relics, spawn-random-cell, map-window, minimap-radar, fog-of-war, save-progress, +room-draft, +draft-reroll, +door-alignment, +step-budget, +daily-reset-run, +meta-unlocks, +rank-by-row, +cross-room-clues, +notes-encouraged]
proposes: ["+effect:draft", "+cond:doors_align", "+cond:shape_fits_slot", "+trigger:out_of_steps", "+window:draft-window", "+ui:step-counter", "+card:room-draft", "+card:step-budget", "+feature:notebook", "+axis:session-daily-run"]
author: opus
date: 2026-11-09
---

# Blue Prince — щодня будуй маєток з кімнат-карток: відчини двері, обери 1 з 3 планів і шукай 46-ту кімнату

## Суть
Гравець від першої особи ходить маєтком-сіткою 9 рядів × 5 стовпців. Кожного разу, коли він відчиняє двері в ще не відкриту клітину, гра пропонує **три випадкові плани кімнат**; обраний план ставиться в цю клітину — так маєток драфтиться на ходу. Кожен перехід між кімнатами коштує крок (старт — 50 на день); кімнати дають ключі, самоцвіти, монети, їжу, інструменти й головоломки. Коли кроки скінчились або ходу нема, день завершується, маєток скидається, а наступного дня план інший. Мета — дістатися захованої Кімнати 46 за Антекамерою; поверх цього — велика мета-гра з підказками між кімнатами й днями.

## Поле і час
- Поле — сітка 9×5 = 45 клітин-кімнат; фіксовані: Entrance Hall (старт, нижній ряд) і Antechamber (верхній ряд, веде до Кімнати 46).
- Кожна клітина — кімната з дверима на 1–4 боки: тупик, пряма, L, T, хрест; двері мають збігатися з сусідами, інакше — барикада.
- Ранг (ряд) клітини визначає рідкість і силу кімнат: вищі ряди — складніші пазли й кращі нагороди.
- Тік = крок (перехід у сусідню кімнату); у межах кімнати — вільний 3D-рух від першої особи.
- Видно лише вже задрафтовані кімнати; решта — порожні клітини плану.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець (Simon) | player | кроки (50 на старт дня), інвентар | ходить між кімнатами; крок = −1 |
| Кімната (план) | tile | форма дверей, колір-група, рідкість, вартість у самоцвітах, ефект | ставиться драфтом у клітину; може давати ресурс, магазин, пазл, ефект на драфт |
| Entrance Hall | static | фіксована | старт дня |
| Antechamber | gate | фіксована, замкнена | веде до Кімнати 46 |
| Кімната 46 | static | — | головна мета |
| Двері-драфт | gate | незакриті / замкнені | відчинити → драфт у порожню клітину; замкнені — потрібен ключ або інструмент |
| Барикада | static | — | дверний отвір, що впирається в стіну сусіда або межу |
| Ключ | resource | к-сть | відмикає замкнені двері |
| Самоцвіт (gem) | resource | к-сть | оплачує спеціальні плани при драфті |
| Монета | resource | к-сть | купівля їжі й інструментів у кімнатах-магазинах |
| Кістка слонової кістки (ivory die) | resource | к-сть, скид щодня | перетягнути три плани драфту |
| Їжа | pickup | +N кроків | відновлює кроки |
| Інструмент | pickup | лопата, кувалда, відмичка, компас, детектор… | відкриває спеціальні місця / змінює драфт (компас — частіше двері на північ) |
| Спальня | tile | група Bedrooms | відновлює кроки при вході |
| Магазин | tile | група Shops | продає за монети |
| Червона кімната | tile | група Red Rooms | негативні або ризиковані ефекти (?) |
| Зелена кімната | tile | група Green Rooms (сади) | ефекти на ресурси (?) |
| Коридор | tile | група Hallways | багато дверей, сполучення |
| Зовнішня кімната | tile | Outer Rooms | драфтиться лише через двері зовнішнього шляху |
| Документ/підказка | mark | текст, картинка | підказки до мета-пазлів між кімнатами |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(open_door)` → ЯКЩО `custom: «за дверима порожня клітина»` і `not state(door, locked)` → ТО `choose(3 floorplans)` з пулу.
- КОЛИ `input(open_door)` → ЯКЩО `state(door, locked)` і `has(player, key)` → ТО `take(player, key)`, `set_state(door, open)`; інакше `block`.
- Генерація трійки: `custom: «3 різні плани; не всі тупики; перший слот — завжди безкоштовний»`; клітина на краю — без хрестів; кут — лише L і тупики.
- КОЛИ обрано план → ЯКЩО `custom: «вартість у самоцвітах ≤ наявних»` → ТО `take(player, gems)`, `place(room, cell)` з випадковою допустимою орієнтацією.
- КОЛИ `input(redraw)` → ЯКЩО `has(player, die)` → ТО `take(player, die)`, `custom: «скинути три плани й витягти нові»`.
- КОЛИ `place(room)` → для кожного отвору: ЯКЩО `custom: «веде в порожню клітину»` → ТО `spawn(draft_door)`; ЯКЩО `custom: «веде в двері сусіда»` → ТО `set_state(door, open)` (навіть замкнені); ЯКЩО `custom: «веде в стіну сусіда»` → ТО `set_cell(doorway, barricade)`.
- КОЛИ `place(room)` → ТО `custom: «спрацьовують ефекти кімнати й інших кімнат на драфт»`, потім `spawn_at(items, room)`.
- КОЛИ `enter(player, room)` → ТО `counter(steps, -1)`.
- КОЛИ `picked(player, food)` → ТО `counter(steps, +n)`; КОЛИ `enter(player, bedroom)` → ТО `counter(steps, +n)`.
- КОЛИ `contact(player, item)` → ТО `pickup` (ключ, самоцвіт, монета, інструмент).
- КОЛИ `counter(steps, <=, 0)` або `custom: «нема куди йти»` → ТО `custom: «день скінчено»`: `lose` дня, втрата зібраного, `restart` з новим маєтком.
- КОЛИ `custom: «день скінчено»` → ЯКЩО `custom: «здобуто постійний апгрейд»` → ТО `custom: «наступні дні починаються з +кроки/самоцвіти/монети»`.
- КОЛИ `enter(player, room_46)` → ТО `win` основної мети; `unlock(challenges)` для наступних днів.
- Пазли кімнат: частина — у межах кімнати, частина — вимагає поєднати підказки з кількох кімнат/днів (`custom`).
- Перемога: Кімната 46 · Поразка: кінець кроків = кінець дня (не гри) · Рахунку нема.

## Керування і ввід
- Перша особа: рух, огляд, взаємодія з дверима/предметами (миша+клавіатура, геймпад).
- Драфт: вибір 1 з 3 карток планів; опції драфту (перетягнути костями тощо) — до вибору; закрити вікно без вибору не можна.
- План маєтку з поточним станом сітки (?) — відкривається окремо.

## Вікна, меню, HUD
- `main-menu` — продовжити, налаштування (?).
- `game-screen` — від першої особи; HUD праворуч угорі — `coins`, ключі, самоцвіти, кості, кроки (`+ui:step-counter`).
- `custom-window` «драфт» (`+window:draft-window`) — три плани з формою дверей, кольором, вартістю; кнопка REDRAW Floorplans (кості).
- `map-window` — сітка 9×5 із задрафтованими кімнатами (?) деталі.
- `shop-window` — кімнати-магазини (Commissary, Locksmith, Gift Shop…).
- `inventory-window` — предмети й інструменти (?).
- `codex-window` — Room Directory: каталог відкритих планів за групами (?) чи це внутрішньоігровий екран.
- `end-screen` — кінець дня (?).
- Переходи: main-menu → game-screen (Entrance Hall) → [двері] draft → game-screen → … → кінець дня → новий день.

## Фічі поза полем
- `meta-progression`: постійні апгрейди (+кроки/самоцвіти/монети на старті), частина предметів переходить між днями; Drafting Studio додає нові плани в пул; знайдені плани (Found Floorplans).
- Знання переходить між днями — гра заохочує вести нотатки (`+feature:notebook`).
- Пост-гра: челенджі після Кімнати 46, трофеї, секрети, що відкриваються лише після неї (частина не розвʼязана спільнотою станом на 11.2025).
- `autosave` між днями; `achievements` (трофеї).

## Варіації й родичі
- Родичі: роглайк-драфт (Slay the Spire — вибір 1 з 3), Carcassonne/Kingdomino (`board-digital` — плитки з краями, що мають збігатися), Myst/The Witness/Outer Wilds (знання як прогрес), Betrayal at House on the Hill (кімнати відкриваються плитками).
- **Осі варіацій:** вибір плитки — 1 з 3 / з руки / випадкова; збіг країв — обовʼязковий / барикада; ресурс-ліміт — кроки / час / нема; що зберігається між забігами — нічого / апгрейди / знання.

## Цікавинки для курсу
- Драфт 1 з 3 зі зваженого пулу за рідкістю й рангом рядка, без дублів і «не всі тупики» — 🥉.
- Форми кімнат (dead end / straight / L / T / cross) як маски дверей + перевірка орієнтації для клітини на краю/куті — 🥉 (бітові маски, обертання).
- Розміщення кімнати: двері в порожнечу → нові двері драфту, двері в двері → відчинити, двері в стіну → барикада — 📎.
- Бюджет кроків + їжа/спальні як відновлення; кінець дня = рестарт із мета-апгрейдами — 🥉.
- Ефекти кімнат, що модифікують наступні драфти (пул, рідкість, вартість) — 🥈 (ланцюг модифікаторів).
- Мета-пазли з підказками між кімнатами — поза кодом: 👑 як дизайн, не як програма.

## Мапа на каталог
- Є: `move-4dir` ↔ переходи між клітинами; `key-and-door` ↔ замкнені двері; `item-pickup` + `inventory-items` ↔ інструменти; `round-currency` + `shop-window` + `shop-catalog` ↔ монети й магазини; `reach-exit` ↔ Кімната 46; `permadeath` ↔ день скидається (≈); `run-relics` ↔ предмети, що діють у забігу; `spawn-random-cell` ↔ предмети в кімнатах; `map-window` + `minimap-radar` + `fog-of-war` ↔ план маєтку; `collect-quota` (≈ — радше ні); `save-progress`.
- **Нема** → пропозиції карток:
  - `+room-draft` «Драфт клітини: 1 з 3 планів» · levels/generation · 🥉.
  - `+draft-reroll` «Перетягнути пропозиції за ресурс» · game-logic/economy · 🌱.
  - `+door-alignment` «Двері мають збігатися з сусідами, інакше барикада» · entities/legality · 📎.
  - `+step-budget` «Бюджет кроків на забіг з відновленням» · game-logic/lose · 📎.
  - `+daily-reset-run` «Забіг-день: усе скидається, лишаються апгрейди» · levels/progression · 🥉.
  - `+meta-unlocks` «Постійні апгрейди між забігами» · game-logic/economy · 🥉.
  - `+rank-by-row` «Рідкість/сила залежить від ряду» · levels/generation · 🌱.
  - `+cross-room-clues` «Підказки, розкидані по кімнатах і днях» · levels · 👑 (дизайн).
  - `+notes-encouraged` — гра заохочує зовнішні нотатки (не механіка, позначка).

## Пропозиції до словників
- `+effect:draft(slot, n)` — запропонувати N планів і поставити обраний у клітину (зараз — `choose` + `place`).
- `+cond:doors_align(room, cell)` — отвори кімнати узгоджені з сусідами/межею.
- `+cond:shape_fits_slot(shape, cell)` — форма дозволена для центру/краю/кута.
- `+trigger:out_of_steps` — бюджет кроків вичерпано (зараз `counter(steps, <=, 0)`).
- `+window:draft-window` — вікно вибору 1 з N плиток/карт (Blue Prince, роглайк-драфти).
- `+ui:step-counter` — лишок кроків на день.
- `+card:room-draft`, `+card:step-budget` — див. «Мапа на каталог».
- `+feature:notebook` — внутрішні/зовнішні нотатки гравця як частина гри.
- `+axis:session-daily-run` — нове значення осі `session`: `daily-run` (забіг = день із повним скидом поля).

## Джерела
- ⭐ [Wikipedia: Blue Prince](https://en.wikipedia.org/wiki/Blue_Prince_(video_game)) — сітка 9×5 = 45, фіксовані Entrance Hall і Antechamber, драфт 1 з 3, збіг дверей, ключі/самоцвіти/монети/інструменти, тири за рядом, 50 кроків, їжа й спальні, кінець дня з утратою предметів, постійні апгрейди, Room 46, пост-гра, Dogubomb / Raw Fury, дати.
- [Blue Prince Wiki: Drafting](https://blueprince.wiki.gg/wiki/Drafting) — пул, рідкість, вартість у самоцвітах, безкоштовний перший слот, форми за позицією, орієнтація, барикади, out-drafting.
- [Blue Prince Wiki: Room Directory](https://blueprince.wiki.gg/wiki/Room_Directory) — групи: Blueprints 001–046, Bedrooms, Hallways, Green Rooms, Shops, Red Rooms, Blackprints, Outer Rooms, Studio Additions, Found Floorplans.
- [Blue Prince Wiki: Items](https://blueprince.wiki.gg/wiki/Items) · [Ivory Dice](https://blueprince.wiki.gg/wiki/Ivory_Dice) — ресурси, інструменти, перетягування планів костями.
- Steam: [пошук «Blue Prince»](https://store.steampowered.com/search/?term=Blue+Prince) · YouTube: [пошук «Blue Prince gameplay»](https://www.youtube.com/results?search_query=Blue+Prince+gameplay).

## Непевне
- (?) Ефекти кольорових груп (червоні — «шкідливі», зелені — сади з ресурсами) — з памʼяті; вікі групує, але ефекти не описує.
- (?) Скільки кроків дає їжа/спальня; чи може крок коштувати більше 1.
- (?) Чи є в грі окремий екран плану маєтку й каталогу кімнат (чи вікі-каталог — лише фан-ресурс).
- (?) Вікна (меню, кінець дня, інвентар) — з загального досвіду.
- (?) Сімʼя: черга пропонує `board-digital` або `roguelike`; лишив `thinky`, бо головне — мета-пазли й відкриття правил, а драфт і забіги — в `also`.
