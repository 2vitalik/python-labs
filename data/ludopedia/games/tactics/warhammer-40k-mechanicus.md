---
title: "Warhammer 40,000: Mechanicus"
slug: warhammer-40k-mechanicus
aka: [Mechanicus, "WH40K Mechanicus"]
family: tactics
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: partial
  random: both
  goal: state
year: 2018
platforms: [PC, macOS, Linux, PS4, Xbox One, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Warhammer_40,000:_Mechanicus", best: true, note: "XCOM-подібна тактика, Cognition Points визначають дії, Bulwark Studios, DLC Heretek, релізи"}
  - {kind: steam, url: "https://store.steampowered.com/app/673880/Warhammer_40000_Mechanicus/", note: "Cognition для найсильнішої зброї й навичок, дослідження гробниць підвищує загрозу, 50 місій, досягнення = навички раз за місію"}
  - {kind: other, url: "https://www.nintendoworldreport.com/review/54603/warhammer-40000-mechanicus-switch-review", note: "огляд: кімнати місії, Awakening ~70 % / 100 %, відродження ворогів за 3 ходи, Canticles, Blackstone, лише техножерці = поразка"}
  - {kind: other, url: "https://www.4p.de/test/warhammer_40000_mechanicus/83573", note: "4Players (DE): голокарта кімнат, події з 3 виборами, локальне й глобальне Awakening"}
  - {kind: steam, url: "https://store.steampowered.com/app/1049290/Warhammer_40000_Mechanicus_Heretek/", note: "DLC Heretek (2019)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Warhammer+40000+Mechanicus+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [hp-damage, melee-vs-ranged, line-of-sight-attack, unit-xp-skills, inventory-items, ai-opponent, destroy-all-enemies, reach-exit, reinforcements, enemy-waves, round-currency, map-window, world-map, save-autosave, achievements-window, +shared-action-pool, +resource-from-objects, +pay-for-extra-move, +room-crawl-events, +doom-clock, +enemy-revive-timer, +finish-downed, +once-per-mission-powers, +talent-trees, +hit-chance, +action-points]
proposes: ["+effect:revive", "+cond:downed", "+role:obelisk", "+ui:cognition-counter", "+ui:awakening-meter", "+ui:revive-countdown", "+window:noctis-map", "+window:event-choice", "+window:ark-ship", "+window:canticle-select", "+feature:doom-clock", "+axis:session"]
author: opus
date: 2026-11-09
---

# Warhammer 40,000: Mechanicus — тактика, де дії загону оплачуються спільним «пізнанням», яке треба збирати з обʼєктів поля

## Суть
Загін техножерців Адептус Механікус спускається в гробниці некронів. У бою кожна сильна дія — зброя, навичка, а часто й додатковий рух — коштує **Cognition Points (CP)**, а CP поповнюються головно взаємодією з обʼєктами мапи (обеліски, «багаті на пізнання» предмети), тож позиціонування — це ще й економіка. Поза боєм місія — це «підземелля» з кімнат: кожен вхід у кімнату — подія з вибором, але й зростання шкали **Awakening**, яка посилює некронів і наближає фінал кампанії. Вбиті некрони не мертві: через кілька ходів вони встають, якщо їх не добити.

## Поле і час
- Бій: квадратна сітка, покрокові ходи сторонами в стилі XCOM; укриття майже прибране (на відміну від XCOM).
- Місія: голографічна карта-граф кімнат (Noctis) (?); кожна кімната — подія, частина з боєм; у кожній зоні щонайменше один бій.
- Темп кампанії: кожна місія додає ≥ 3 пункти глобальної шкали Awakening; ~70 % відкриває фінального боса, на 100 % бій з ним примусовий.
- Інформація часткова: вміст кімнат і наслідки виборів невідомі заздалегідь; випадковість — у подіях і бою.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Техножрець (Tech-Priest) | piece | HP, рух, зброя, підтримка, сервочерепи, аугментації, дисципліна | головний юніт; усі техножерці вибули = місія провалена |
| Війська (servitors, skitarii та ін.) | ally | дешеві, витратні | «мʼясний щит»; відкриваються за сюжетом |
| Сервочереп | object | — | інструмент техножерця: сканування, бонуси (?) |
| Обеліск / джерело пізнання | resource | — | взаємодія → +CP загону (?) |
| Некрон-воїн, скарабеї, елітні некрони | enemy | HP | AI; після «смерті» лежить і встає через N ходів |
| Повалений некрон | enemy | лічильник відродження | встає за 3 ходи (на високому Awakening — одразу); добивається одним гарантованим ударом |
| Бос (Necron Overlord тощо) | boss | — | фінальні та сюжетні бої |
| Кімната гробниці | zone | подія, Awakening +N | вхід → подія з вибором або бій |
| Вихід / евакуація | zone | — | дійти, щоб завершити бій (?) |
| Blackstone | resource | — | валюта прокачки й ремонту між місіями |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(player)` → ТО `custom: «кожен техножрець і військо: рух і дії»`.
- КОЛИ `input(move, tp, cell)` → ЯКЩО `custom: «шлях ≤ безкоштовного руху»` → ТО `move(tp, cell)`; інакше `custom: «кожна зайва клітина −1 CP»` (?).
- КОЛИ `input(ability, tp)` → ЯКЩО `custom: «CP загону ≥ ціни»` → ТО `counter(CP, -cost)` + ефект; інакше `block`.
- КОЛИ `custom: «техножрець поруч з обеліском / джерелом пізнання»` → ТО `counter(CP, +n)` (?).
- КОЛИ `custom: «подія в кімнаті дала пізнання»` → ТО `counter(CP, +n)` на наступний бій (?).
- КОЛИ `hp_zero(necron)` → ТО `set_state(necron, downed)` + `counter(revive, 3)`.
- КОЛИ `turn_end(enemy)` → ЯКЩО `state(necron, downed)` → ТО `counter(revive, -1)`; КОЛИ `counter(revive, ==, 0)` → ТО `custom: «некрон встає»`.
- ЯКЩО `counter(Awakening, >=, high)` → ТО `custom: «відродження одразу»`.
- КОЛИ `input(attack, tp, downed_necron)` → ТО `custom: «гарантоване влучання»` + `disappear(downed_necron)`; критичне вбивство теж не дає встати.
- КОЛИ `enter(cohort, room)` → ТО `counter(Awakening_local, +1)` + `counter(Awakening_global, +n)` + `window(event-choice)` + `choose(ігнорувати | вивчити | знищити …)`.
- КОЛИ `input(choice, event)` → ТО `custom: «наслідок обраного варіанту (ігнорувати / вивчити / знищити …)»`; наслідки: `currency(+n)` (Blackstone), `counter(CP, +n)`, `damage(tp, n)` або `counter(Awakening, +n)`.
- ЯКЩО `counter(Awakening_local, >=, n)` → ТО `custom: «бої в гробниці важчі: більше некронів, модифікатори»`.
- КОЛИ `level_end` → ТО `counter(Awakening_global, +3)` (мінімум); КОЛИ `counter(Awakening_global, >=, 100)` → ТО `custom: «примусовий фінальний бій»`.
- КОЛИ `custom: «досягнення виконано»` → ТО `unlock(canticle)`; КОЛИ `input(canticle)` → ЯКЩО `first_time` за місію → ТО `custom: «глобальний бонус: шкода / лікування / рух»`.
- КОЛИ `all_gone(tech_priest)` → ТО `lose` (місія); КОЛИ `custom: «ціль бою виконано (знищити всіх / дійти до виходу / вижити)»` → ТО `win` (?).
- КОЛИ `custom: «техножрець вибув у бою»` → ТО `custom: «permadeath нема; ремонт після місії коштує Blackstone»`.

## Керування і ввід
- Клік по юніту → досяжні клітини (окремо безкоштовні й за CP) (?) → клік по клітині; панель зброї/навичок з ціною в CP.
- Карта місії: вибір наступної кімнати; вікно події з 2–3 варіантами.
- Між місіями: кораблик-ковчег — розподіл Blackstone по деревах дисциплін, спорядження, вибір Canticles і загону.

## Вікна, меню, HUD
- `main-menu`: Campaign / Continue / Options.
- `ark-ship` — хаб між місіями: дерево дисциплін, арсенал, вибір загону, рішення радників (впливають на кінцівку).
- `map-window` — карта планети з місіями й глобальною шкалою Awakening.
- `noctis-map` — карта кімнат гробниці; `awakening-meter` локальний і глобальний.
- `event-choice` — подія кімнати з картинкою й варіантами.
- `canticle-select` — вибір навичок раз-за-місію перед висадкою.
- `game-screen` бою: сітка, `cognition-counter` (?), `hp-bar`, `revive-countdown` над поваленими некронами, `ability-buttons` з ціною CP, `hit-chance` (?).
- `end-screen` місії з нагородою; `achievements-window`.

## Фічі поза полем
- `talent-trees`: 7 гілок прокачки за Blackstone (ближній бій, дальній, лікування, рух, бафи/дебафи…), розблокування броні.
- `doom-clock`: глобальна шкала Awakening як таймер кампанії — баланс «зачистити все» проти «встигнути».
- Досягнення відкривають Canticles; рішення на кораблі ведуть до однієї з кінцівок.
- `autosave`; DLC Heretek (нова сюжетна лінія). Сиквел Mechanicus II оголошено у 2024.

## Варіації й родичі
- [XCOM](xcom.md) — прообраз бою; [Invisible, Inc.](invisible-inc.md) — тиск таймера тривоги на розвідку; [Into the Breach](into-the-breach.md) — обʼєкти поля як ресурс.
- Осі варіацій:
  - **бюджет дій**: окремі AP на юніта (XCOM) / спільний пул загону, що поповнюється з поля (Mechanicus);
  - **смерть ворога**: остаточна / відроджується за таймером, якщо не добити (Mechanicus);
  - **таймер кампанії**: нема / шкала, що росте від кожної кімнати й місії (Mechanicus, Invisible Inc).

## Цікавинки для курсу
- Спільний пул CP: ціни дій + поповнення з обʼєктів поля — 📎.
- Рух у кредит: безкоштовні N клітин + 1 CP за кожну зайву — 🌱.
- Відродження ворога за лічильником і «добивання» поваленого — 🌱.
- Карта кімнат з подіями і шкалою Awakening як ціною досліджень — 🥉 (граф + події + глобальний таймер).
- Навички раз за місію, що відкриваються досягненнями — 🌱.

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` · `line-of-sight-attack` · `unit-xp-skills` · `inventory-items` · `reinforcements`/`enemy-waves` ↔ некрони прибувають · `round-currency` ↔ Blackstone · `map-window`/`world-map` · `achievements-window`.
- **Нема** → пропозиції карток:
  - `+shared-action-pool` «Спільний пул дій загону» · entities/combat · 📎 · слоти {start, max}.
  - `+resource-from-objects` «Ресурс з обʼєктів поля» · entities/cells · 📎.
  - `+pay-for-extra-move` «Рух за ресурс понад норму» · entities/legality · 🌱.
  - `+room-crawl-events` «Підземелля кімнат з подіями» · levels/progression · 🥉.
  - `+doom-clock` «Шкала загрози кампанії» · levels/progression · 📎.
  - `+enemy-revive-timer` · `+finish-downed` «Відродження і добивання» · entities/death · 🌱.
  - `+once-per-mission-powers` · `+talent-trees` · levels/progression · 📎.

## Пропозиції до словників
- `+effect:revive(a)` — повалений встає; `+cond:downed(a)` — сутність повалена, не знищена.
- `+role:obelisk` — обʼєкт-джерело ресурсу, з яким взаємодіють юніти (відрізняти від `resource`, бо не підбирається).
- `+ui:cognition-counter` — спільний пул CP; `+ui:awakening-meter`; `+ui:revive-countdown`.
- `+window:noctis-map` (карта кімнат місії), `+window:event-choice`, `+window:ark-ship` (хаб), `+window:canticle-select`.
- `+feature:doom-clock`; `+axis:session` = `campaign`.

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/Warhammer_40,000:_Mechanicus) — XCOM-стиль, CP визначають дії, розробник, DLC, консолі, сиквел.
- [Steam](https://store.steampowered.com/app/673880/Warhammer_40000_Mechanicus/) — CP для зброї й навичок, гробниці: більша нагорода — більша загроза, 50 місій, досягнення → навички раз за місію, кінцівки.
- [Nintendo World Report](https://www.nintendoworldreport.com/review/54603/warhammer-40000-mechanicus-switch-review) — кімнати, Awakening (≥3 за місію, ~70 % бос, 100 % примусово), відродження за 3 ходи і добивання, Canticles, Blackstone, 7 гілок, поразка = усі техножерці.
- [4Players](https://www.4p.de/test/warhammer_40000_mechanicus/83573) — голокарта кімнат, 3 варіанти в подіях, локальне й глобальне Awakening.
- [Wikipedia (ru)](https://ru.wikipedia.org/wiki/Warhammer_40,000:_Mechanicus) — 4 техножерці + сервітори, маршрут між боями, апгрейд ковчега.

## Непевне
- (?) CP — спільний пул загону чи окремий у кожного (NWR пише про «метр» у кожного; черга й памʼять — спільний); фан-вікі (402) і Steam-гайди (429) не відкрились.
- (?) Як саме набираються CP у бою (обеліски, сканування сервочерепом, вбивства, навички) і чи платиться CP за зайвий рух.
- (?) Умови перемоги в бою (знищити всіх / дійти до виходу / протриматись) і правила прибуття некронів.
- (?) Назва «Noctis» для карти кімнат — з памʼяті.
