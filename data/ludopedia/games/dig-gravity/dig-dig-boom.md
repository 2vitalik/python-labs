---
title: Dig Dig Boom
slug: dig-dig-boom
aka: [DDB]
family: dig-gravity
also: [roguelike]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: setup
  goal: collect
year: 2027
platforms: [PC (Windows, Linux/SteamOS)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2026040/Dig_Dig_Boom/", best: true, note: "опис: час і гравітація йдуть лише з твоїм ходом; усе копається, підривається, штовхається, падає; бій як шаховий пазл; безкоштовне демо"}
  - {kind: other, url: "https://playtester.io/dig-dig-boom", note: "плейтест: бій на сітці без випадковості, втрата предметів при смерті, мета-відкриття, сітковий інвентар, підписи скриншотів (хрест-вибух, Heavy Pickaxe, сітка проти ящірки)"}
  - {kind: other, url: "https://www.gamingonlinux.com/2023/12/dig-dig-boom-is-a-charming-looking-turn-based-puzzle-mining-roguelike/", note: "2023: ручні рівні + процедурні печери, запланований редактор, Godot, натхнення Spelunky/NecroDancer/Noita"}
  - {kind: other, url: "https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1830797770240274", note: "девлог GodotCon 2026: превʼю атак ворогів як перемикач"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Dig+Dig+Boom+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [move-by-input, dig-terrain, gravity-fall, push-object, destructible-blocks, blast-wave, item-pickup, inventory, inventory-items, in-round-upgrades, round-currency, pattern-automaton, telegraphed-intents, telegraph-marker, dungeon-generation, player-death, permadeath, +turn-based-dungeon, +turn-based-gravity, +crush-by-fall, +deterministic-combat, +meta-unlocks, +grid-inventory, +depth-biomes]
proposes: ["+card:turn-based-gravity", "+card:grid-inventory", "+card:depth-biomes", "+feature:telegraph-toggle"]
author: opus
date: 2026-11-09
---

# Dig Dig Boom — покроковий роглайт-копач: світ, вороги й гравітація роблять крок лише разом із тобою

## Суть
Гном-підривник (Dynaminer (?)) копає, підриває й прокладає тунелі крізь процедурні печери по золото, спускаючись у нові біоми. Ключ гри: **час іде лише з твоїм ходом**, і гравітація теж — камінь падає, вороги атакують, вогонь (?) поширюється тільки після твоєї дії. Світ повністю руйнівний: усе можна викопати, підірвати, штовхнути або обвалити, тож ворога можна оминути тунелем чи розчавити каменем. Бій — «шаховий пазл» без випадковості: вороги мають фіксовані патерни атак, які треба вивчити.

## Поле і час
- Квадратна сітка печери, вид збоку; гравітація вниз. Камера / розмір мапи — (?).
- Хід = одна дія гравця (крок, копання, інструмент); після неї світ робить один тік: падіння, вороги, інші процеси (`time: turn`). Без вводу нічого не рухається.
- Забіг — спуск углиб; на глибині — нові біоми (покинуті шахти, грибні печери). Печери процедурні; у версії 2023 — ще й ручні рівні, що вводять механіки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гном (Dynaminer?) | player | інвентар-сітка | крок, копання, застосування інструмента; гине → забіг скінчено |
| Земля / порода | terrain | твердість (?) | копається або підривається → порожня клітина |
| Валун | object | — | без опори падає на тік; розчавлює того, хто під ним; штовхається (?) |
| Золото | resource | — | збирається; головна ціль забігу |
| Вороги (ящірка та ін.) | enemy | фіксований патерн атаки | атакують за патерном, без випадковості; превʼю атаки — перемикач |
| Вибухівка | object | форма — хрест | руйнує клітини хрестом (підпис скриншота) |
| Heavy Pickaxe | pickup | рівень апгрейду, статистика | посилене копання (?) |
| Сітка (net) | pickup | — | застосовується проти ворога-ящірки; ефект (?) |
| Інші інструменти | pickup | «десятки», кожен — кілька застосувань | унікальні ефекти; губляться зі смертю |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, dir)` → ЯКЩО `free(target)` → ТО `move(dwarf, dir)`; інакше `block`.
- КОЛИ `input(dig, dir)` → ЯКЩО `cell(target, dirt)` → ТО `set_cell(target, empty)`.
- КОЛИ `input(push, dir)` → ЯКЩО `occupied(target, boulder)` і `free(cell_behind)` → ТО `push` (?).
- КОЛИ `turn_end(dwarf)` → ТО `custom: «світ робить один тік: гравітація, вороги, процеси»`.
- КОЛИ `turn_end(dwarf)` → ЯКЩО `not supported(boulder)` → ТО `fall(boulder)` — лише в тік, не в реальному часі.
- КОЛИ `contact(boulder, enemy)` згори → ТО `damage(enemy, n)` (?) — «засідка каменепадом».
- КОЛИ `input(use, bomb)` → ТО `use(dwarf, bomb)`, `explode(cross, n, empty)` — руйнує клітини хрестом.
- КОЛИ `input(use, net)` → ЯКЩО `in_range(dwarf, lizard, n)` → ТО `custom: «сітка знешкоджує ящірку»` (?).
- КОЛИ `input(use, tool)` → ТО `use(dwarf, tool)` → ефект інструмента (`custom`; десятки видів).
- КОЛИ `turn_end(dwarf)` → ТО `custom: «кожен ворог робить крок свого фіксованого патерну атаки»`.
- КОЛИ `turn_start(dwarf)` → ЯКЩО `mode(attack_preview)` → ТО `custom: «підсвітити клітини, куди вдарять вороги»` (перемикач, у тестуванні 2026).
- КОЛИ `contact(dwarf, gold)` → ТО `pickup`, `currency(+n)`.
- КОЛИ `reach(dwarf, deeper_layer)` → ТО `custom: «новий біом»`.
- КОЛИ `died(dwarf)` → ТО `game_over`, `take(dwarf, all_items)` (предмети втрачено), `unlock(items|cosmetics)` (мета).
- Перемога: (?) — мета забігу — золото й глибина · Поразка: смерть гнома, забіг з нуля · Рахунок: золото (?).

## Керування і ввід
- Покроковий аватар на сітці: напрямок = крок або дія в той бік; вибір інструмента з інвентаря — (?).
- Повна підтримка контролера (playtester.io); клавіатура — (?).
- Темп задає гравець: можна думати скільки завгодно, бо світ стоїть.

## Вікна, меню, HUD
- `game-screen`: печера + HUD; `telegraph-marker` — превʼю атак ворогів (перемикач, 2026).
- `inventory-window` — сітковий інвентар інструментів.
- `upgrade-window` / панель статистики інструмента (Heavy Pickaxe: апгрейд, характеристики).
- `settings-window`: мова (20 мов), перемикач превʼю атак (?).
- `end-screen` після смерті — (?); `main-menu` — (?).
- `editor-window` — запланований у 2023 (?).

## Фічі поза полем
- `meta-progression`: між забігами відкриваються нові предмети й косметика; предмети забігу губляться зі смертю.
- `mode-hardcore`-подібно за замовчуванням: смерть = новий забіг (`permadeath`).
- `localization` (20 мов), `gamepad-support`.
- `level-editor` — обіцяний у 2023 (?).

## Варіації й родичі
- У сімʼї: [boulder-dash](boulder-dash.md) і [emerald-mine](emerald-mine.md) (камені, що падають, але в реальному часі), [mr-driller](mr-driller.md), [spelunky](spelunky.md) (роглайт-копач real-time), [noita](noita.md) (руйнівний світ, роглайт), [steamworld-dig](steamworld-dig.md), [dome-keeper](dome-keeper.md).
- Поза сімʼєю: [hoplite](../tactics/hoplite.md) і [into-the-breach](../tactics/into-the-breach.md) — детермінований бій з видимими намірами; [crypt-of-the-necrodancer](../roguelike/crypt-of-the-necrodancer.md) — вороги з патернами.
- **Осі варіацій**: коли діє гравітація — щотіку таймера (Boulder Dash) / лише після ходу гравця (Dig Dig Boom, Subterrarium) / ніколи (Dig Dug без каменів); бій — кубики / детермінований з превʼю / детермінований без превʼю.

## Цікавинки для курсу
- Гравітація як фаза покрокового тіку: гравець → падіння → вороги — 🥉 (порядок фаз вирішує, хто кого розчавить).
- Вороги з фіксованими патернами + підсвітка майбутніх ударів — 🥉 (окремий прохід «що станеться наступного тіку» без зміни стану).
- Повністю руйнівна сітка + хрест-вибух + каскад падінь після вибуху — 🥈.
- Процедурні печери з біомами за глибиною — 🥇.
- Сітковий інвентар (предмети різної форми?) — 🥈; мета-відкриття між забігами — 🌱.

## Мапа на каталог
- Є: `move-by-input` · `dig-terrain` · `gravity-fall` · `push-object` (?) · `destructible-blocks` · `blast-wave` ↔ хрест · `item-pickup` · `inventory` + `inventory-items` · `in-round-upgrades` ↔ апгрейд кайла (?) · `round-currency` ↔ золото · `pattern-automaton` ↔ патерни ворогів · `telegraphed-intents` + `telegraph-marker` ↔ превʼю атак · `dungeon-generation` ↔ процедурні печери · `player-death` + `permadeath`.
- Повтори з корпусу: `+turn-based-dungeon` · `+crush-by-fall` · `+deterministic-combat` · `+meta-unlocks`.
- **Нема** → пропозиції карток:
  - `+turn-based-gravity` «Гравітація діє лише в тік ходу гравця» · entities/move · 🥉 · слот {fall: one_cell|to_floor} — Dig Dig Boom, Subterrarium.
  - `+grid-inventory` «Інвентар-сітка» · entities/state · 🥈 · слот {shapes: bool}.
  - `+depth-biomes` «Біоми змінюються з глибиною» · levels/generation · 🥉 · слоти {biomes, depth_step}.

## Пропозиції до словників
- `+card:turn-based-gravity` — гравітація як фаза тіку ходу (Dig Dig Boom, Subterrarium).
- `+card:grid-inventory` — інвентар як сітка клітин.
- `+card:depth-biomes` — нові біоми на глибині.
- `+feature:telegraph-toggle` — перемикач підсвітки намірів ворогів як налаштування доступності.

## Джерела
- ⭐ [Steam: Dig Dig Boom](https://store.steampowered.com/app/2026040/Dig_Dig_Boom/) — час і гравітація лише з твоїм ходом; усе копається, підривається, штовхається, падає; бій як шаховий пазл; десятки інструментів; процедурні печери; золото; біоми; демо; 2027.
- [playtester.io](https://playtester.io/dig-dig-boom) — бій на сітці без випадковості, патерни атак, предмети губляться зі смертю, мета-відкриття предметів і косметики, сітковий інвентар, підписи скриншотів.
- [GamingOnLinux, 2023](https://www.gamingonlinux.com/2023/12/dig-dig-boom-is-a-charming-looking-turn-based-puzzle-mining-roguelike/) — ручні рівні + процедурні печери, запланований редактор, Godot.
- [Девлог «GodotCon 2026 — Enemy attack indicators»](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1830797770240274) — плейтестерам незрозуміло, коли й куди бʼють вороги → перемикач превʼю атак.
- YouTube: пошук «Dig Dig Boom gameplay».

## Непевне
- (?) Пошуковий сніпет (не підтверджений сторінками) згадує вогонь, що поширюється, і приклади інструментів: арбалетні болти для лазіння, драбина, феєрверки, що оглушують ворогів, кувалда.
- (?) Чи валун падає на одну клітину за тік чи до дна; чи гном має HP; чи гравець штовхає камені сам.
- (?) Імʼя героя Dynaminer — з коментаря читача GamingOnLinux.
- (?) Дата: Steam — «2027» / «To be announced», демо — версія 2024, застаріла (девлог березня 2026: нові інструменти, бій, біоми, прогресія).
- (?) Чи є перемога забігу (дно, квота золота) — не описано.
