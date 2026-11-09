---
title: "Dupery: A Game of Solo Deduction"
slug: dupery
aka: [Dupery]
family: hidden-deduction
also: [roguelike]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: hidden
  random: both
  goal: state
year: 2026
platforms: [PC (Windows), Mac]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3845070/Dupery_A_Game_of_Solo_Deduction/", best: true, note: "опис: сітка ролей Innocent / Meddler / Underling / Traitor, брехня, арешти й репутація, 3 регіони, бос, дошка детектива"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3845070&count=40&maxlength=8000", note: "девлоги й патчноути (JSON): ролі з текстами здібностей, годинникова вежа, Casino і фішки, ліди, квірки, інструменти дошки, натхнення Blood on the Clocktower"}
  - {kind: official, url: "https://gildedrunegames.com/press/dupery", note: "прес-кіт: «clock-like» дедукція, 200+ ролей, 50+ квірків, Daily / Endless, режими на 2 і 3 гравців"}
  - {kind: other, url: "https://www.gamespress.com/Dupery-A-Game-Of-Solo-Deduction-Out-Now-On-Steam", note: "реліз-прес 15.10.2026: сітка, репутація, 175+ ролей, 3 регіони"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Dupery+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 35
mechanics: [cell-click, codex-window, daily-puzzle, difficulty-levels, achievements-window, stats-window, game-screen, end-screen, main-menu, +hidden-roles, +lying-informants, +role-statements, +arrest-with-penalty, +reputation-meter, +clock-tower-events, +case-quirks, +boss-fight, +run-meta-carry, +evidence-board, +lead-select]
proposes: ["+trigger:clock_ring", "+cond:tainted", "+cond:alignment", "+effect:arrest", "+effect:taint", "+effect:announce", "+role:informant", "+ui:reputation-bar", "+ui:evidence-board", "+window:lead-select", "+window:event-choice", "+feature:free-draw-notes", "+card:lying-informants", "+card:role-statements", "+card:arrest-with-penalty", "+card:reputation-meter", "+card:clock-tower-events", "+card:case-quirks", "+card:evidence-board", "+card:lead-select"]
author: opus
date: 2026-11-09
---

# Dupery — соло-«Blood on the Clocktower» на сітці підозрюваних: допитуй, кому віриш, і заарештуй усіх злих, не втративши репутацію

## Суть
Соло-роглайт дедукції: кожна справа — процедурна сітка мешканців, у кожного таємна роль одного з чотирьох типів — Innocent, Meddler, Underling, Traitor. Детектив розслідує мешканців і чує їхні заяви (роль, яку вони називають, і інформацію здібності), але Underling-и брешуть, Traitor-и ще гірші, а навіть добрих можуть «заплямувати» (tainted) — тоді вони кажуть неправду. Справу розкрито, коли заарештовано всіх злих; арешт доброго знижує репутацію, а замала репутація — звільнення. Як [Clues by Sam](clues-by-sam.md), але з брехунами й подіями годинникової вежі.

## Поле і час
- Сітка мешканців з «адресами» (позиціями); у демо згадано дошки 3×3, обговорювалась 5×5 — розмір у повній грі (?).
- Сусідство важливе (ролі «поруч з невинним», «найдальший від…»); з діагоналями чи ні — (?).
- Час справи — години; годинникова вежа бʼє у випадкову годину (за замовчуванням один раз), деякі ролі додають дзвони; дзвін запускає здібності.
- Забіг: 3 регіони, у кожному серія справ і фінальна з генералом синдикату; потім фінальний забіг проти боса синдикату.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Мешканець | tile | адреса; таємна роль; розслідуваний / ні; заарештований / мертвий | розслідування → заява (названа роль + інформація) |
| Innocent | neutral | добрий | каже правду, якщо не заплямований |
| Meddler | neutral | розлад | власні шкідливі ефекти; брехня не головна |
| Underling | enemy | злий | бреше, видаючи себе за підозрювану роль |
| Traitor | boss | злий | бреше й ламає правила справи (ховає репутацію, нищить її за таймером) |
| Годинникова вежа | switch | година дзвону | дзвін запускає здібності ролей |
| Репутація | resource | рівень | падає за хибний арешт; низька → звільнення; між справами відновлюється |
| Фішки (регіон Casino) | resource | старт 175 | розслідування −2, арешт доброго −30; закінчились → звільнення |
| Квірк | mark | — | модифікатор правил справи (Lost at Sea, Poker Face, Haunted, Public Unrest…) |
| Лід | pickup | головні підозрювані | обирається на старті забігу (1 з 3); його підозрювані завжди «під підозрою» |

Приклади ролей (з патчноутів): Good Cop (робить роль доброю; в парі з Bad Cop), Bad Cop (Underling, видає себе за Good Cop), Plant (Meddler, копіює чужу брехню, розкривається після 18-ї години), Sniper (Underling біля вежі: на дзвін убиває найдальшого живого), Fearmonger (Traitor: дзвін кожні 6 год, після 5-го — репутації кінець), Journalist (каже статус репутації; брехун/заплямований — хибний), Publisher (каже адресу нерозслідуваного доброго), Sawbones (Meddler: при поганій репутації вбиває випадкового), Detractor (заплямовує невинних), Smoker (Traitor: ховає репутацію, Underling-и не розкриваються при арешті), Gentleman, Gargoyle (на дзвін називає злу роль у грі), Belfry (додатковий дзвін), Maid (на дзвін заплямовує наступного невинного), Mathematician (сума адрес злих ролей), Critic (подвоює втрату репутації).

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` (справа) → ТО `custom: «згенерувати сітку ролей за пулом забігу й квірками»`; частина ролей стартує розслідуваними (Publisher, Gentleman).
- КОЛИ `input(investigate, citizen)` → ЯКЩО `custom: «роль добра й не заплямована»` → ТО `reveal(citizen)`, `message(правдива заява)`.
- КОЛИ `input(investigate, citizen)` → ЯКЩО `custom: «роль Underling / Traitor»` → ТО `message(хибна заява)` — видає себе за підозрювану роль.
- КОЛИ `input(investigate, citizen)` → ЯКЩО `state(citizen, tainted)` → ТО `message(хибна заява)`.
- КОЛИ `custom: «дзвін годинникової вежі»` → ТО `custom: «здібності ролей, що діють на дзвін»` — напр., Sniper: `custom: «найдальший живий незаарештований мешканець»` → `disappear`; Maid: `set_state(next_innocent, tainted)`.
- КОЛИ `input(arrest, citizen)` (Shift+ЛКМ) → ЯКЩО `custom: «роль зла»` → ТО `set_state(citizen, arrested)`.
- КОЛИ `input(arrest, citizen)` → ЯКЩО `custom: «роль добра»` → ТО `counter(reputation, -n)` (Critic у грі — ×2).
- КОЛИ `counter(reputation, <=, fired)` → ТО `lose` (звільнено).
- КОЛИ `custom: «усі злі ролі заарештовано»` → ТО `win` (справа), `counter(reputation, +n)`, `next_level`.
- КОЛИ `custom: «5-й дзвін»` → ЯКЩО `custom: «Fearmonger живий і на волі»` → ТО `lose`.
- КОЛИ `level_end` → ТО `choose(1 з 3 подій)` (позначаються штампами), `custom: «додати ролі в пул, отримати квірки й модифікатори»`.
- КОЛИ `game_start` (забіг) → ТО `choose(1 з 3 лідів)`.
- КОЛИ `input(middle_click, investigated_citizen)` → ТО `window(codex-window)` — опис ролі.
- Перемога: заарештувати всіх злих у кожній справі, пройти 3 регіони й боса · Поразка: репутація (або фішки) до нуля, умови Traitor-ів · Рахунок: репутація.

## Керування і ввід
- ЛКМ по мешканцю — розслідувати; Shift+ЛКМ — арешт; середня кнопка — довідка ролі.
- Дошка детектива: перо (малювати будь-де, гумка), шпильки, нитка між шпильками, ножиці; гарячі клавіші для нитки й ножиць.
- Опції: лише клавіатура / лише миша; без таймінгового вводу.

## Вікна, меню, HUD
- `main-menu`: новий забіг, режими (Daily Challenges, Endless — за прес-кітом), статистика, налаштування.
- `lead-select`: 3 ліди з головними підозрюваними.
- `game-screen`: сітка мешканців з адресами, `evidence-board` (перо, шпильки, нитки), `reputation-bar` (Smoker її ховає), годинник/вежа, позначки «розслідуваний / заарештований / мертвий».
- `codex-window`: опис ролі (середня кнопка).
- `event-choice`: 1 з 3 подій після справи; вибір ролей, квірків і модифікаторів.
- `end-screen`: справу розкрито / звільнено.
- `stats-window` (Steam Stats), `achievements-window`.

## Фічі поза полем
- Прогресія: 9 рівнів ролей по регіонах відкриваються перемогами над генералами; фінальний забіг із босом.
- `difficulty-presets`: на вищих складностях репутація не росте (лише штампами).
- `mode-daily`, `mode-endless`; режими на 2 гравці (спланувати злочин) і 3 гравці (знайти, хто працює на синдикат) — за прес-кітом.
- `codex`, `achievements`, `stats`, `cloud-save`, `localization` (11 мов).

## Варіації й родичі
- [Clues by Sam](clues-by-sam.md) — сітка «хто злочинець», але всі кажуть правду й вгадувати не дають; тут брехуни, арешт — ризик, і є події часу.
- Blood on the Clocktower (соціальна дедукція, сімʼя поза сітками) — пряме натхнення розробника: ролі зі здібностями, брехня злих, «отруєні» добрі (тут tainted).
- [Cluedo](cluedo.md), [Mr. Jack](mr-jack.md) — дедукція особи; [Minesweeper](minesweeper.md) — «сусіди» як інформація.
- **Осі варіацій**: правдивість «усі правдиві / злі брешуть / добрі можуть бути заплямовані»; ціна помилки «блок (Clues by Sam) / втрата репутації або фішок»; час «статичний / дзвони вежі запускають події»; пул ролей «фіксований / росте протягом забігу».

## Цікавинки для курсу
- Модель ролей: тип × здібність × правдивість, генерація справи з пулу — 📎.
- Заяви брехунів: Underling видає себе за підозрювану роль і генерує хибну, але правдоподібну інформацію — 🥉.
- Розвʼязувач: перебрати розподіли злих, лишити сумісні з усіма заявами (з урахуванням брехні й taint) — 🥈.
- Годинникова вежа як планувальник подій із ролями, що змінюють розклад дзвонів — 📎.
- Репутація як HP детектива, Critic-множник втрат — 🌱.
- Дошка доказів: вільне малювання, шпильки й нитки поверх сітки — 🥉.

## Мапа на каталог
- Є: `cell-click` ↔ розслідування; `codex-window` ↔ довідка ролі; `daily-puzzle` ↔ Daily Challenges; `difficulty-levels`; `achievements-window`; `stats-window`; `game-screen` / `end-screen` / `main-menu`.
- **Нема** → пропозиції карток:
  - `+hidden-roles`, `+boss-fight`, `+run-meta-carry` — уже пропоновані в корпусі.
  - `+lying-informants` «Інформатори, частина з яких бреше за роллю» · game-logic/info · 🥉.
  - `+role-statements` «Розслідування дає заяву ролі (назва + інформація здібності)» · game-logic/info · 📎.
  - `+arrest-with-penalty` «Звинувачення без блоку, хибне — штраф ресурсу» · game-logic/lose · 🌱.
  - `+reputation-meter` «Репутація як життя детектива між справами» · entities/state · 🌱.
  - `+clock-tower-events` «Дзвін у випадкову годину запускає здібності» · game-logic/turns · 📎.
  - `+case-quirks` «Модифікатори правил справи, що накопичуються» · game-logic/progression · 📎.
  - `+evidence-board` «Дошка нотаток: перо, шпильки, нитки поверх поля» · interface/input · 🥉.
  - `+lead-select` «Вибір стартового ліду з наслідком для всього забігу» · game-logic/progression · 🌱.

## Пропозиції до словників
- `+trigger:clock_ring` — дзвін годинникової вежі (випадкова година або за правилом ролі).
- `+cond:tainted(a)` — добра роль заплямована й видає хибне; `+cond:alignment(a, good|evil)` — сторона ролі.
- `+effect:arrest(a)` — арешт з перевіркою сторони; `+effect:taint(a)` — заплямувати; `+effect:announce` (уже пропонований у сімʼї) — роль оголошує інформацію.
- `+role:informant` — сутність, що видає (можливо хибну) інформацію про інших.
- `+ui:reputation-bar`; `+ui:evidence-board` — шар нотаток гравця.
- `+window:lead-select`; `+window:event-choice` — подія 1 з 3 між справами.
- `+feature:free-draw-notes` — вільне малювання поверх поля (уже пропонований у сімʼї).

## Джерела
- ⭐ [Steam: Dupery](https://store.steampowered.com/app/3845070/Dupery_A_Game_of_Solo_Deduction/) — опис: типи ролей, брехня, taint, Mathematician і Critic, арешт усіх злих, репутація, 3 регіони, бос, дошка детектива; Gilded Rune Games, Yogscast Games, 15.10.2026.
- [Steam News API](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3845070&count=40&maxlength=8000) — тексти ролей, вежа, Casino і фішки, ліди й події, квірки, інструменти дошки, Shift+ЛКМ, 3×3 у демо, цитата про Blood on the Clocktower.
- [Gilded Rune Games: прес-кіт](https://gildedrunegames.com/press/dupery) — «clock-like» дедукція, 200+ ролей, 50+ квірків, Daily / Endless / режими на 2–3 гравців.
- [Gamespress: реліз](https://www.gamespress.com/Dupery-A-Game-Of-Solo-Deduction-Out-Now-On-Steam) — сітка, репутація, 175+ ролей, 3 регіони.
- YouTube: пошук «Dupery gameplay».

## Непевне
- (?) Розмір сітки в повній грі і чи сусідство включає діагоналі.
- (?) Чи розслідування коштує годину (і скільки годин у справі); фішки за розслідування — лише в регіоні Casino.
- (?) Умова розкриття: Steam — «арештувати всіх злих», девлог — «усіх Traitor-ів»; чи Meddler-и злі — неясно.
- (?) Розмір втрати/приросту репутації і поріг звільнення.
- (?) Режими на 2–3 гравці й Daily/Endless — з прес-кіту; у Steam-описі їх нема, можливо, ще не вийшли.
- (?) Кількість ролей: Steam — 175+, прес-кіт — «понад 100» і «200+».
