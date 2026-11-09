---
title: "Might & Magic: Clash of Heroes"
slug: clash-of-heroes
aka: [Clash of Heroes, "Might & Magic: Clash of Heroes HD", "Might & Magic: Clash of Heroes – Definitive Edition", CoH]
family: falling-match
also: [tactics]
klass: hybrid
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 2009
platforms: [Nintendo DS, PS3, Xbox 360, PC, iOS, Android, Switch, PS4]
links:
  - {kind: other, url: "https://www.videogamer.com/reviews/might-and-magic-clash-of-heroes-review", best: true, note: "огляд DS: 3 очки руху за хід, вертикаль = атака, горизонталь = стіна, лінки, фʼюжни, core/elite/champion, видалення без витрати ходу"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Might_%26_Magic:_Clash_of_Heroes", note: "дві сітки, ~3 ходи, заряд і постріл по стовпцю, фракції, базові й елітні юніти, артефакти, платформи, HD і Definitive"}
  - {kind: other, url: "https://critical-gaming.squarespace.com/blog/2010/12/15/review-repair-clash-of-heroes-pt1.html", note: "розбір дизайну: поле 8×6, ціна дій, підкріплення, HP заряду, MP-шкала"}
  - {kind: steam, url: "https://store.steampowered.com/app/2213300/Might_Magic_Clash_of_Heroes_Definitive_Edition/", note: "Definitive Edition: 15 героїв 5 фракцій, 1v1 і 2v2, ladder"}
  - {kind: other, url: "https://www.gamepressure.com/mightandmagicclashofheroes", note: "гайд: проходження, бойові пазли, спецюніти, артефакти"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=might+and+magic+clash+of+heroes+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [gravity-fall, chain-reaction, multi-cell-size, hp-damage, status-effects, destructible-blocks, spawn-random-cell, telegraphed-intents, telegraph-marker, ai-opponent, turn-enforcement, cell-click, drag-drop-piece, unit-xp-skills, character-select, world-map, map-window, online-multiplayer, mode-select, end-screen, game-screen, main-menu, save-game, tutorial-window, +vertical-attack-horizontal-wall, +charge-countdown, +formation-link-fuse, +free-move-on-chain, +reinforcement-call, +mirrored-dual-boards, +hero-special-meter, +battle-puzzles]
proposes: ["+cond:orientation(shape, dir)", "+cond:rear_of_column(a)", "+effect:launch(a)", "+effect:reinforce(n)", "+role:formation", "+ui:charge-countdown", "+window:battle-setup"]
author: opus
date: 2026-11-09
---

# Clash of Heroes — match-3 як дуель армій: 3 у стовпець заряджають атаку, 3 у ряд стають стіною

## Суть
У кожного гравця своє поле з юнітами трьох кольорів; два поля дивляться одне на одне (DS: верхній і нижній екран). За хід — 3 дії: перенести юніт, видалити юніт або покликати підкріплення. Три однакові **вертикально** — формація атаки: вона кілька ходів заряджається, а тоді летить своїм стовпцем у ворожу армію і, пробивши юніти й стіни, бʼє героя. Три однакові **горизонтально** — стіна, що поглинає ворожі атаки. Перемога — HP ворожого героя на нулі. Клас `hybrid`: `cursor` на бойовому полі + `avatar` (герой) на мапі кампанії.

## Поле і час
- Поле кожного гравця 8×6 (critical-gaming); юніти тягнуться до переднього краю — «гравітація» в бік супротивника.
- Стовпці двох полів стоять навпроти: атака зі стовпця свого поля влітає у відповідний стовпець чужого (?).
- Покроково: хід = 3 очки дії (videogamer, Wikipedia «generally three»); потім хід супротивника.
- Час заряду формації рахується ходами; обидва гравці бачать відлік, бо заряджену формацію не можна зрушити.
- Поза боєм — мапа регіону з вузлами-шляхами, міні-пазлами, скринями й квестами.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | HP, MP-шкала, рівень, артефакт, спецздібність | не стоїть на полі; отримує урон від атак, що пробили армію |
| Ворожий герой | enemy | HP, MP, спецздібність | дзеркальний гравцю: те саме поле й ті самі дії |
| Core-юніт ×3 кольори | tile | 1×1, колір, сила | безлімітний запас; 3 вертикально = атака, 3 горизонтально = стіна |
| Elite-юніт | tile | 1×2 (?), заряд довший | рахунок обмежений; заряджається, коли позаду 2 core того ж кольору; часто накладає статус |
| Champion-юніт | tile | 2×2 | потребує 4 core того ж кольору позаду (2 стовпці × 2); сильний спецефект (вампіризм, щит) |
| Формація атаки | object | відлік ходів, сила (росте із зарядом), HP | нерухома до пострілу; поглинає ворожу атаку, як юніт |
| Стіна | static | HP | стає в передній ряд; поглинає атаки; у Sylvan відростає щоходу |
| Резерв підкріплень | — | лічильник | росте, коли юніти атакують, гинуть або видаляються |
| Артефакт | pickup | бонус | екіпірується перед боєм, змінює юнітів чи героя |
| Мапа регіону | zone | вузли, шляхи | рух між вузлами; бої, пазли, квести, скрині |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(side)` → ТО `counter(moves, 3)`.
- КОЛИ `input(pick(unit))` → ЯКЩО `custom: «юніт останній у своєму стовпці»` → ТО `move(unit, rear_of_other_column)`, `counter(moves, −1)`.
- КОЛИ `input(delete(unit))` → ТО `disappear(unit)`, `move(units_behind, front)`, `counter(moves, −1)`, `counter(reserve, +1)`.
- КОЛИ `pattern(match(color, 3))` → ЯКЩО `custom: «три core в стовпці»` → ТО `transform(three, formation)`, `set_state(formation, charging, n_turns)`.
- КОЛИ `pattern(match(color, 3))` → ЯКЩО `custom: «три core в ряду»` → ТО `transform(three, wall)`, `move(wall, front)`.
- КОЛИ `custom: «за elite стоять 2 core його кольору»` → ТО `set_state(elite, charging, n)`; для champion — 4 core.
- КОЛИ `after(move|delete)` → ЯКЩО `chain(2)` (утворились 2+ формації одним ходом) → ТО `extra_move`.
- КОЛИ `input(delete(unit))` → ЯКЩО `custom: «видалення відкрило стіну або формацію»` → ТО `custom: «хід не витрачається»`.
- КОЛИ `turn_start(side)` → ЯКЩО `state(formation, charging)` → ТО `counter(charge, −1)`, `custom: «сила й HP формації ростуть»`.
- КОЛИ `state_off(formation, charging)` → ТО `custom: «launch — формація летить стовпцем у ворожу армію»`.
- КОЛИ `contact(attack, enemy_unit|wall|formation)` → ТО `damage(target, power)`, `custom: «сила атаки −HP цілі»`; ціль з HP 0 — `disappear`.
- КОЛИ `reach(attack, enemy_back_edge)` → ЯКЩО `custom: «сила > 0»` → ТО `damage(enemy_hero, power)`.
- КОЛИ `custom: «дві формації одного кольору стріляють в один хід»` → ТО `multiplier(link)` (link).
- КОЛИ `custom: «нова формація склалась позаду зарядженої того ж кольору в стовпці»` → ТО `merge(formation, new → stronger_formation)` (fusion).
- КОЛИ `input(call_reinforcements)` → ЯКЩО `counter(reserve, >, 0)` → ТО `spawn_at(units, random_free_rear)`, `counter(moves, −1)`; нові юніти самі формацію не складають.
- КОЛИ `state_off(formation, charging)` → ТО `counter(mp_attacker, +n)`, `counter(mp_defender, +m)` (атакувальнику більше).
- КОЛИ `input(hero_special)` → ЯКЩО `counter(mp, =, max)` → ТО `custom: «спецздібність героя»`, `counter(mp, 0)`.
- КОЛИ `turn_end(side)` → ТО `pass_turn`.
- КОЛИ `hp_zero(enemy_hero)` → ТО `win`, `give(hero, xp)`; КОЛИ `hp_zero(hero)` → ТО `lose`.
- КОЛИ `enter(hero, node)` → ЯКЩО `occupied(node, enemy)` → ТО `window(battle)`.
- Перемога: HP ворожого героя = 0 · Поразка: твоє HP = 0 · Рахунку нема, прогрес — XP, золото, артефакти.

## Керування і ввід
- DS: стилусом взяти останній юніт стовпця і перетягнути в інший стовпець; подвійний тап (?) — видалити.
- Кнопки збоку: виклик підкріплень, спецздібність героя (коли MP повна), кінець ходу (?).
- PC/консолі (HD): одне поле на екрані, курсор/миша; гравець бачить відліки ворожих формацій і планує стіни.

## Вікна, меню, HUD
- `main-menu`: Campaign · Multiplayer · Options (?).
- `map-window` — регіон кампанії з вузлами, NPC, скринями, квестами.
- `custom: «battle-setup»` перед боєм: вибір типів юнітів армії, артефакту (Steam: «units for your troops, artifact and spell for your hero»).
- `game-screen` (бій): два поля, портрети й `hp-bar` героїв, `energy-bar` (MP), лічильник ходів (`move-counter`), лічильник резерву, `custom: «charge-countdown»` над кожною формацією, `telegraph-marker` — що влетить куди.
- `character-select` у мультиплеєрі — герой із 10 (DS) / 15 (Definitive) (?).
- `end-screen`: перемога/поразка, XP.
- `tutorial-window` — навчальні бої на початку кампанії (?).

## Фічі поза полем
- Кампанія: 5 героїв по черзі (Godric, Aidan, Anwen, Nadia, Fiona), 5 фракцій, регіони, сюжетні й побічні квести.
- `xp-level` героя; юніти теж рівняються (Steam); артефакти й найманці.
- `mode-puzzle` — бойові пазли з заданою дошкою й особливою вимогою (gamepressure).
- `mode-versus`: DS Download/Wireless Play; HD — онлайн; iOS — асинхронний; Definitive — 1v1 і 2v2, боти, ladder.
- Спецюніти фракцій розблоковуються в печерах і житлах на мапі (gamepressure).

## Варіації й родичі
- DS (2009) → HD (2011, одне поле на екрані, баланс) → iOS/Android (2013, асинхронний мультиплеєр) → Definitive Edition (2023, Dotemu, DLC «I Am the Boss»).
- Родичі: [puzzle-quest](puzzle-quest.md) — дуель на спільній дошці; [puzzle-and-dragons](puzzle-and-dragons.md) — матч → урон загону; [gyromancer](gyromancer.md); Legend of Solgard (наступник ідеї, ?).
- **Осі варіацій**: поле (спільне / два дзеркальних) · що дає орієнтація (вертикаль атака, горизонталь стіна / усі однакові) · коли спрацьовує збіг (одразу / після заряду N ходів) · розмір юніта (1×1 / 1×2 / 2×2) · запас (безлімітні core / обмежені elite).

## Цікавинки для курсу
- Орієнтація збігу визначає ефект: вертикаль → атака, горизонталь → стіна — 🌱.
- Заряд із відліком, видимим обом: телеграфована атака, проти якої будують стіни — 📎.
- Атака по стовпцю, що віднімає HP кожної цілі зі своєї сили, залишок — герою — 📎.
- Elite 1×2 і champion 2×2, яким потрібні core позаду: шаблон збігу для багатоклітинних юнітів — 🥉.
- Link і fusion: два заряди одного кольору синхронно / злиття в стовпці — 🥉.
- Безкоштовний хід, якщо видалення спричинило формацію (ланцюг дій) — 📎.
- AI для дуелі: оцінити ворожі відліки й вибрати між стіною та атакою — 🥇.

## Мапа на каталог
- Є: `gravity-fall` (юніти підтягуються вперед) · `chain-reaction` (видалення → нові формації → бонус) · `multi-cell-size` (elite/champion) · `hp-damage` · `status-effects` (elite) · `destructible-blocks` (стіни) · `spawn-random-cell` (підкріплення) · `telegraphed-intents`/`telegraph-marker` (відліки) · `ai-opponent` · `turn-enforcement` · `drag-drop-piece` · `unit-xp-skills` · `character-select` · `world-map`/`map-window` · `online-multiplayer` · `mode-select` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+vertical-attack-horizontal-wall` «Орієнтація збігу = тип дії» · entities/interact · 🌱.
  - `+charge-countdown` «Збіг заряджається N ходів, потім спрацьовує» · entities/state · 📎.
  - `+formation-link-fuse` «Синхронні й злиті формації сильніші» · game-logic/score · 🥉.
  - `+free-move-on-chain` «Ланцюг дій повертає очко руху» · game-logic/opponent · 🌱.
  - `+reinforcement-call` «Дія: дозаповнити поле з резерву» · entities/spawn · 📎.
  - `+mirrored-dual-boards` «Два поля навпроти, атака перетинає межу» · game-logic/opponent · 🥈.
  - `+hero-special-meter` «Шкала від атак → ультимейт» · entities/state · 🌱.
  - `+battle-puzzles` «Задана позиція з вимогою» · levels/bank · 📎.

## Пропозиції до словників
- `+cond:orientation(shape, dir)` — збіг вертикальний чи горизонтальний (CoH: атака/стіна).
- `+cond:rear_of_column(a)` — сутність остання у своєму стовпці (лише її можна взяти).
- `+effect:launch(a)` — заряджена формація вилітає вздовж стовпця, пробиваючи цілі зі своєю силою.
- `+effect:reinforce(n)` — дозаповнити поле юнітами з резерву у випадкові вільні місця.
- `+role:formation` — група плиток, що стала однією сутністю з HP і відліком.
- `+ui:charge-countdown` — число ходів до спрацювання над сутністю.
- `+window:battle-setup` — екран перед боєм: склад армії, артефакт (є й у Puzzle Quest).

## Джерела
- ⭐ [VideoGamer: огляд](https://www.videogamer.com/reviews/might-and-magic-clash-of-heroes-review) — 3 очки руху, вертикаль/горизонталь, лінки, фʼюжни, core/elite/champion (champion — 4 core позаду), безкоштовне видалення, мапа з вузлами.
- [Wikipedia](https://en.wikipedia.org/wiki/Might_%26_Magic:_Clash_of_Heroes) — дві сітки, ~3 ходи, заряд і постріл стовпцем, фракції, артефакти, мультиплеєр, версії.
- [Critical Gaming: Review & Repair pt.1](https://critical-gaming.squarespace.com/blog/2010/12/15/review-repair-clash-of-heroes-pt1.html) — поле 8×6, ціна дій, підкріплення з резерву, HP заряду, MP-шкала, відліки видно до 6 ходів.
- [Steam: Definitive Edition](https://store.steampowered.com/app/2213300/Might_Magic_Clash_of_Heroes_Definitive_Edition/) — режими, 15 героїв, 1v1/2v2.
- [GamePressure: гайд](https://www.gamepressure.com/mightandmagicclashofheroes) — бойові пазли, спецюніти, артефакти.

## Непевне
- (?) Elite — 1×2 вертикально і потребує 2 core позаду (одне джерело каже «пару»); champion 2×2 з 4 core — підтверджено двома.
- (?) Точна тривалість заряду для core/elite/champion; як саме ростуть сила й HP за хід заряду.
- (?) Як працює fusion (сумуються сили чи скидається відлік) і бонус лінку.
- (?) Як саме стовпці свого поля відповідають стовпцям ворожого (дзеркально чи напряму).
- (?) Чи стіни можна складати з будь-яких core і скільки шарів стіни в стовпці.
- (?) Жест видалення на DS, наявність кнопки «кінець ходу», пункти головного меню.
- (?) Legend of Solgard як ідейний наступник.
