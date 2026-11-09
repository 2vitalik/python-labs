---
title: Bookworm Adventures
slug: bookworm-adventures
aka: [Bookworm Adventures Deluxe, Bookworm Adventures Volume 2, BWA]
family: word-number
also: [tactics]
klass: cursor
axes:
  field: square
  time: turn
  opponent: ai
  info: partial
  random: runtime
  goal: state
year: 2006
platforms: [Windows]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bookworm_Adventures", best: true, note: "бій словами, scramble, самоцвіти, атаки ворога, зілля, скарби, компаньйони Vol. 2, книги й глави, Arena, Tome of Knowledge, міні-ігри"}
  - {kind: other, url: "https://pixelpoppers.com/review/bookworm-adventures/", note: "огляд: менша сітка без сусідства, шкода = довжина й рідкість літер, ворог знецінює плитки, скарби на тему слів"}
  - {kind: strategywiki, url: "https://strategywiki.org/wiki/Bookworm_Adventures/Potions_and_Gem_Tiles", note: "таблиця самоцвітів і зілля; боту віддає 403, зміст — з пошукового фрагмента"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=bookworm+adventures", note: "пошук"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=bookworm+adventures+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [cell-click, word-validation, hp-damage, status-effects, temporary-modes, inventory-items, inventory-limit, sequential-levels, level-unlock, save-progress, codex-window, mode-select, game-screen, main-menu, end-screen, help-window, settings-window, event-effects, popup-text, +word-as-attack, +letter-weight-damage, +gem-tile-effects, +status-tile, +board-shuffle-penalty, +enemy-attack-list, +equip-loadout, +periodic-companion, +attack-timer-bar, +minigame-rewards, +theme-word-bonus]
proposes: ["+cond:word_weight", "+effect:reshuffle", "+ui:enemy-attack-list", "+ui:attack-timer-bar", "+ui:potion-shelf", "+window:treasure-select", "+feature:mode-survival", "+feature:adventure-replay"]
author: opus
date: 2026-11-09
---

# Bookworm Adventures — слово з літер сітки = удар по монстру; ворог відповідає атакою, псує плитки й накладає статуси

## Суть
Покрокова дуель Лекса (книжкового черв'яка) з монстрами: хід гравця — одне слово з літер невеликої сітки, слово б'є ворога, і що «важче» слово (довше, з рідкісними літерами), то більша шкода. Після кожного слова ворог виконує одну атаку зі свого видимого списку: шкодить, накладає статус на Лекса, лікується або псує плитки сітки. Сильні слова породжують плитки-самоцвіти з бойовими ефектами; між боями — зілля, скарби (пасивні бонуси) і боси наприкінці глав. Відмінність від [bookworm.md](bookworm.md): нема гравітації, вогню й рекорду — **сусідство літер не потрібне**, мета — перемогти, а не вижити якнайдовше.

## Поле і час
- Квадратна сітка літер, менша, ніж у Bookworm (розмір — у «Непевне»); використані плитки замінюються новими на тих самих місцях — падіння нема.
- Слово — довільна множина плиток сітки в будь-якому порядку; «поле» фактично є рукою літер, як у Scrabble.
- Час покроковий: хід Лекса (слово / scramble / зілля) → хід ворога. Arena — real-time: шкала над сіткою заповнюється, повна → удар ворога; гравець атакує, скільки встигне скласти слів.
- Шари: сітка плиток зі станом (звичайна / самоцвіт / зіпсована) + бойова сцена з HP обох сторін і списком атак ворога.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Лекс | player | HP-серця, статуси, екіпіровані скарби | складає слово = атака; програв бій → глава заново |
| Плитка-літера | tile | літера, вага за рідкістю | у слові → зникає, на її місці нова випадкова літера |
| Плитка Emerald | tile | — | у слові → лікує Лекса, як зілля здоровʼя |
| Плитка Garnet | tile | +30 % шкоди | у слові → ослаблює атаки ворога |
| Плитка Ruby | tile | +35 % шкоди | у слові → підпалює ворога; марна проти вогнетривких |
| Плитка Diamond | tile | +100 % шкоди | у слові → повне лікування й по зіллю кожного типу |
| Плитки Amethyst / Sapphire / Crystal | tile | ефекти — у «Непевне» | також самоцвіти; Amethyst — ще й приз міні-гри |
| Зіпсована плитка | tile | стан від атаки ворога | напр. знецінена: дає 0 у шкоду; інші стани — у «Непевне» |
| Ворог | enemy | HP, список атак, імунітети | після слова Лекса — одна атака: шкода / статус / самолікування / баф / псування плиток |
| Бос глави | boss | HP, сильніші атаки | наприкінці глави після серії боїв; перемога → скарб |
| Зілля здоровʼя | pickup | Vol. 2: ліміт 10 на тип | відновлює частину HP Лекса |
| Зілля сили | pickup | — | посилює наступну атаку |
| Зілля зцілення | pickup | — | знімає негативні стани з Лекса і/або сітки |
| Скарб | pickup | ≤3 на главу (Vol. 2 — ≤2) | пасивно: менше шкоди, більше шкоди за слова з певними літерами чи темою, стійкість до статусів; деякі — апгрейд наявного |
| Компаньйон (Vol. 2) | ally | спрацьовує кожні 4 ходи | Mother Goose дає зілля здоровʼя (чекає, якщо ліміт); Skeletrox покращує плитки до кращих самоцвітів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click tile)` → ТО `custom: «літера додається до слова; сусідство в сітці не перевіряється»`.
- КОЛИ `input(attack)` → ЯКЩО `in_dictionary(word)` → ТО `damage(enemy, custom: «з ваги слова: довжина × рідкість літер»)`, `clear(word tiles)`, `spawn_at(tile, cleared cells)`; інакше `block`.
- КОЛИ `after(attack)` → ЯКЩО `custom: «вага слова ≥ порогу»` → ТО `spawn_at(gem tile, grid)` — що сильніше слово, то цінніший камінь.
- КОЛИ `input(attack)` → ЯКЩО `has(word, emerald)` → ТО `heal(lex, n)`.
- КОЛИ `input(attack)` → ЯКЩО `has(word, garnet)` → ТО `set_state(enemy, weakened)`, `multiplier(×1.3)`.
- КОЛИ `input(attack)` → ЯКЩО `has(word, ruby)` і `not state(enemy, fire_immune)` → ТО `set_state(enemy, burning)`, `multiplier(×1.35)`.
- КОЛИ `input(attack)` → ЯКЩО `has(word, diamond)` → ТО `heal(lex, full)`, `give(lex, potion ×3 types)`, `multiplier(×2)`.
- КОЛИ `input(attack)` → ЯКЩО `has(lex, treasure)` і `custom: «слово містить літери / тему скарбу (напр. метали)»` → ТО `multiplier(×k)`.
- КОЛИ `turn_end(lex)` → ТО `custom: «ворог виконує одну атаку зі свого списку; деякі атаки поєднують кілька ефектів»`: `damage(lex, n)` · `set_state(lex, debuff)` · `heal(enemy, n)` · `set_state(enemy, buff)` · `set_state(tile, spoiled)`.
- КОЛИ `custom: «атака ворога знецінює плитки»` → ТО `set_value(tile, 0)` — плитка в слові не додає шкоди.
- КОЛИ `input(scramble)` → ТО `custom: «усі літери сітки замінено новими»`, `end_turn` — ворог б'є безкарно.
- КОЛИ `input(use potion)` → ЯКЩО `has(lex, potion)` → ТО `take(lex, potion)` і `heal(lex, n)` | `set_state(lex, empowered)` | `clear_state(lex|tiles, ailment)`.
- КОЛИ `hp_zero(enemy)` → ТО `give(lex, potion)` (не завжди), `custom: «наступний бій глави»`.
- КОЛИ `hp_zero(enemy)` → ЯКЩО `not mode(survival)` → ТО `heal(lex, full)`.
- КОЛИ `hp_zero(boss)` → ТО `choose(treasure)`, `next_level`.
- КОЛИ `hp_zero(lex)` → ТО `lose`, `restart` — глава з початку.
- КОЛИ `level_start` → ЯКЩО `counter(treasures, >, limit)` → ТО `choose(equipped treasures)`.
- КОЛИ `timer(4)` → ЯКЩО `has(lex, mother_goose)` і `counter(health_potions, <, 10)` → ТО `give(lex, health potion)`.
- КОЛИ `timer(4)` → ЯКЩО `has(lex, skeletrox)` → ТО `transform(tile, better gem)`.
- КОЛИ `tick` → ЯКЩО `mode(arena)` → ТО `counter(attack_bar, +1)`; КОЛИ `counter(attack_bar, >=, full)` → ТО `custom: «ворог атакує, шкала з нуля»`.
- КОЛИ `level_end` → ЯКЩО `mode(minigame)` → ТО `give(lex, potion|gem tile)` за місце (Amethyst — 3-тє, Ruby — 4-те).
- Перемога: пройти книги (оригінал — 3 × 10 глав) · Поразка: HP Лекса = 0 → переграти главу · Рахунку як мети нема.

## Керування і ввід
- Мишка: клік по плитках — додати до слова, клік по вибраній — прибрати (?); кнопки Attack і Scramble; клік по зіллю — вжити.
- Перед главою — вибір скарбів для екіпіровки.
- Arena: те саме, але під тиском шкали атаки ворога.

## Вікна, меню, HUD
- `main-menu`: Adventure · Tome of Knowledge (після Книги 1) · Mini-Games (після Книги 2) · Arena (після Книги 3) · Clips and Giggles (після Arena).
- `game-screen` (бій): сітка, поточне слово, Attack / Scramble, HP-серця Лекса й ворога (`hp-bar`), список атак ворога внизу праворуч (`enemy-attack-list`), полиця зілля (`potion-shelf`), іконки статусів, `popup-text` шкоди.
- `treasure-select`: вибір/заміна скарбів після боса і перед главою (`inventory-window`-подібне).
- `codex-window`: Tome of Knowledge — вороги та їхні атаки.
- `mode-select`: міні-ігри (3 в оригіналі, 6 у Vol. 2) — вгадати таємне слово / скласти якомога більше слів.
- `custom-window`: Clips and Giggles — комікс-інтро, музика, коментарі розробників.
- `end-screen`: перемога в бою/главі, нагороди.
- Переходи: глава → бої поспіль → бос → скарб → наступна глава.

## Фічі поза полем
- Прогресія: книги з главами, `level-unlock` режимів за пройдені книги; оригінальна пригода після проходження блокується, Vol. 2 додає Adventure Replay (після Книги 6) з бейджами.
- `mode-survival`: Survival Battles — серія ворогів без лікування між ними.
- Arena — real-time бої з босами (не з усіма).
- Міні-ігри як джерело зілля й самоцвітів.
- `save-progress` профілю.

## Варіації й родичі
- [bookworm.md](bookworm.md) — предок: шлях по сусідах, гравітація, вогонь; Adventures міняє «виживання на полі» на «дуель з HP».
- Bookworm Adventures Volume 2 (2009): книги 4–6, компаньйони, ліміт зілля 10, скарбів 2 на главу, Adventure Replay.
- Letter Quest: Grimm's Journey, Wordatro ([wordatro.md](wordatro.md)) — «слово = дія» з прокачкою; Puzzle Quest — той самий хід «пазл = удар» у match-3.
- Родичі за сіткою: [boggle.md](boggle.md), [spelltower.md](spelltower.md), [scrabble.md](scrabble.md) (вага рідкісних літер).
- **Осі варіацій:** сусідство (обовʼязкове / ні) · результат слова (очки / шкода / лікування) · відповідь світу (вогонь / хід ворога / шкала real-time) · підсилення (самоцвіт на полі / зілля / пасивний скарб / компаньйон за таймером).

## Цікавинки для курсу
- Таблиця ваги літер → шкода слова з порогом появи самоцвіту — 🌱 (одна функція й таблиця).
- Самоцвіти з ефектами в слові (лікування, підпал, ослаблення, множник) — 📎.
- Хід ворога зі списку атак: шкода, статус, самолікування, псування плиток — 🥉 (стани на плитках і на героях, комбіновані атаки).
- Scramble як хід зі штрафом «ворог б'є безкарно» — 🌱.
- Скарби-модифікатори за літерами/темою слова + ліміт екіпіровки — 📎.
- Arena: real-time шкала атаки поверх покрокової гри — 📎.

## Мапа на каталог
- Є: `cell-click` ↔ вибір плиток · `word-validation` ↔ слово в словнику · `hp-damage` ↔ HP Лекса й ворогів · `status-effects` / `temporary-modes` ↔ debuff, підпал, ослаблення · `inventory-items` / `inventory-limit` ↔ зілля з лімітом · `sequential-levels` / `level-unlock` ↔ глави й режими · `save-progress` · `codex-window` ↔ Tome of Knowledge · `mode-select` ↔ міні-ігри · `popup-text` ↔ шкода · `game-screen` · `main-menu` · `end-screen` · `help-window` · `settings-window` · `event-effects`.
- **Нема** → пропозиції карток:
  - `+word-as-attack`, `+status-tile`, `+board-shuffle-penalty` — див. bookworm.md.
  - `+letter-weight-damage` «Шкода/очки з ваги літер слова» · game-logic/score · 🌱 · слоти {weights, length_bonus}.
  - `+gem-tile-effects` «Плитки-самоцвіти з ефектом у слові» · entities/interact · 📎 · слоти {gem: effect, threshold}.
  - `+enemy-attack-list` «Ворог обирає атаку з видимого списку» · entities/combat · 🥉.
  - `+equip-loadout` «Екіпіровка обмеженої кількості пасивних бонусів перед рівнем» · game-logic/economy · 📎 · слоти {slots}.
  - `+periodic-companion` «Помічник з ефектом кожні N ходів» · entities/state · 🌱 · слоти {every}.
  - `+attack-timer-bar` «Шкала real-time атаки ворога в покроковій грі» · game-logic/opponent · 📎.
  - `+minigame-rewards` «Міні-ігри як джерело предметів» · levels/progression · 📎.
  - `+theme-word-bonus` «Бонус за слова теми/з літер» · game-logic/score · 📎.

## Пропозиції до словників
- `+cond:word_weight` — вага слова (довжина × рідкість) порівняно з порогом (самоцвіти тут, бонус-плитки в bookworm.md).
- `+effect:reshuffle` — перемішати/замінити всі плитки поля (scramble).
- `+ui:enemy-attack-list` — видимий перелік атак ворога; `+ui:attack-timer-bar` — шкала до удару ворога (Arena); `+ui:potion-shelf` — полиця зілля з лічильниками.
- `+window:treasure-select` — вибір пасивних бонусів у слоти перед рівнем.
- `+feature:mode-survival` — серія боїв без лікування; `+feature:adventure-replay` — повтор кампанії з бейджами.

## Джерела
- ⭐ [Wikipedia: Bookworm Adventures](https://en.wikipedia.org/wiki/Bookworm_Adventures) — бій, scramble, самоцвіти, атаки ворога, зілля трьох типів, скарби (ліміт), компаньйони, книги, режими й умови їх відкриття.
- [Pixel Poppers: огляд](https://pixelpoppers.com/review/bookworm-adventures/) — сітка менша, сусідство не потрібне, знецінення плиток, скарби за темою слів.
- [StrategyWiki: Potions and Gem Tiles](https://strategywiki.org/wiki/Bookworm_Adventures/Potions_and_Gem_Tiles) — 403 для бота; з пошукового фрагмента: Emerald, Garnet +30 %, Ruby +35 %, Diamond +100 %, поріг ваги 5.25.
- YouTube: пошук «bookworm adventures gameplay».

## Непевне
- (?) Розмір сітки: черга каже 4×4, джерела — лише «менша, ніж у Bookworm».
- (?) Ефекти Amethyst, Sapphire, Crystal; точна формула шкоди і поріг «вага ≥ 5.25» — з фрагмента пошуку, сторінку не відкрито.
- (?) Повний список станів плиток (замок, отрута тощо) — джерела підтверджують лише знецінення.
- (?) Чи витрачає хід вжиток зілля; як саме прибирається літера зі слова.
- (?) Платформи понад Windows (Mac, DS, мобільні версії) — не перевірено.
