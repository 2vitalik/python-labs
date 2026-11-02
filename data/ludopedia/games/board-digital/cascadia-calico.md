---
title: Cascadia + Calico (Каскадія, Калико)
slug: cascadia-calico
family: board-digital
also: []
klass: cursor
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: full
  random: runtime
  goal: score
year: 2021
platforms: [board, PC, macOS]
links:
  - {kind: official, url: "https://www.alderac.com/wp-content/uploads/2025/04/Cascadia_BaseGame_Rulebook_Optimized.pdf", best: true, note: "офіційні правила Cascadia (AEG): ринок 4 пар, перенаселення, шишки, коридори, усі 20 карт тварин A–D, соло, сценарії"}
  - {kind: official, url: "https://www.alderac.com/wp-content/uploads/2025/04/Calico_BaseGame_Rulebook_Optimized.pdf", note: "офіційні правила Calico: дизайн-цілі, ґудзики, 10 котів, фінал, соло, сімейний варіант"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Cascadia_(board_game)", note: "Randy Flynn, Flatout Games 2021, Spiel des Jahres 2022"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Calico_(board_game)", note: "Kevin Russ, Flatout Games / AEG 2020"}
  - {kind: steam, url: "https://store.steampowered.com/app/2438970/Cascadia/", note: "Dire Wolf, 2025: 15 соло-сценаріїв, 14 викликів, Daily Trek, Family Mode, онлайн, pass&play"}
  - {kind: steam, url: "https://store.steampowered.com/app/1993180/Quilts_and_Cats_of_Calico/", note: "Monster Couch, 2024: сюжетна кампанія, AI, рейтинговий онлайн, живі коти на полі"}
  - {kind: official, url: "https://www.flatout.games/cascadia", note: "сторінка видавця"}
  - {kind: bgg, url: "https://boardgamegeek.com/boardgame/283155/calico", note: "BGG: Calico"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Cascadia+board+game+how+to+play", note: "пошук; пояснення правил"}
stage: v1
coverage: 70
mechanics: [cell-click, drag-drop-piece, hover-highlight, legal-move-highlight, turn-enforcement, hot-seat, ai-opponent, event-points, round-currency, game-settings, daily-puzzle, leaderboard, +hex-grid-render, +connected-placement, +two-layer-placement, +paired-market, +market-wipe, +rule-bending-token, +connected-group-scoring, +corridor-majority-bonus, +shape-pattern-match, +line-of-sight-scoring, +neighbor-variety-scoring, +run-shape-scoring, +public-objectives, +scenario-goals, +hand-plus-market, +prefilled-border, +neighborhood-goal, +group-once-reward, +rainbow-set-bonus]
proposes: ["+trigger:placed", "+trigger:pattern", "+effect:place", "+effect:draft", "+effect:clear", "+cond:connected", "+cond:same", "+cond:adjacent_count", "+cond:line_of_sight", "+role:supply", "+role:tile", "+role:token", "+ui:opponent-boards", "+ui:score-preview", "+ui:market-pairs", "+ui:objective-cards", "+window:match-setup", "+window:scenario-select", "+feature:scenarios", "+feature:achievements", "+axis:turn-structure"]
author: opus
date: 2026-11-02
---

# Cascadia + Calico — гекс-пазли «поклади плитку так, щоб склались візерунки»: коридори, групи, лінії, коти

## Суть
Дві ігри одного видавця (Flatout Games) з однією душею: щоходу береш одну гекс-плитку з маленького ринку й кладеш у своє поле, щоб у кінці склались **просторові візерунки**, які оцінюють спільні картки. **Cascadia** (2021) — двошарове поле: плитка-місцевість (коридори одного типу) + жетон тварини на ній (ведмеді групами по парах, лосі лініями, лососі «змійками», яструби поодинці, лисиці серед різних сусідів). **Calico** (2020) — обмежена ковдра: кожна латка має колір і візерунок; колір дає ґудзики (групи ≥3), візерунок — котів (групи потрібного розміру чи форми), а три цілі-шестикутники вимагають певного складу шести сусідів.

## Поле і час
- **Cascadia**: особисте гекс-поле без меж, росте від стартової тріади з 3 плиток. Два шари: плитка (1–2 типи місцевості з 5: гори, ліси, прерії, болота, річки) і жетон тварини (≤1 на плитку). Плитку не можна класти поверх і не можна рухати.
- **Calico**: особиста ковдра — фіксоване гекс-поле з **надрукованими крайовими латками** (рахуються в групах), 22 порожні клітини + 3 клітини для дизайн-цілей.
- **Спільна зона**: Cascadia — 4 пари «плитка + жетон» (жетони з мішка 100 шт.); Calico — 3 відкриті латки + рука з 2 латок у кожного.
- Хід — один; Cascadia: рівно 20 ходів на гравця (плиток = 20×N + 3); Calico: 22 ходи, доки ковдра не заповнена.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка місцевості (Cascadia) | tile | 1–2 типи з 5; 1–3 символи дозволених тварин; 85 шт. | кладеться поруч хоча б одним боком; обертається; не рухається |
| Ключова плитка (keystone) | tile | 1 тип, 1 тварина; 25 шт. | тварина на ній → +1 шишка |
| Стартова тріада | static | 3 плитки | центр поля гравця |
| Жетон тварини | object | ведмідь / лось / лосось / яструб / лисиця, по 20 | кладеться на плитку з її символом без жетона; можна скинути в мішок |
| Шишка (nature token) | resource | 25 шт. | витратити: взяти будь-яку плитку + будь-який жетон АБО перетягнути будь-які жетони ринку; 1 очко в кінці; тай-брейк |
| Ринок пар | supply | 4 × (плитка + жетон) | хід бере пару; поповнюється зі стосу й мішка |
| Мішок жетонів | supply | 100 | поповнення й «перенаселення» |
| Картка тварини | zone | вид, варіант A/B/C/D | функція рахунку для цього виду на всю партію |
| Коридор | zone | тип місцевості, розмір | звʼязна група плиток одного типу через збіг сторін |
| Латка (Calico) | tile | колір (6) × візерунок (6), по 3 = 108 | з руки на будь-яку порожню клітину ковдри |
| Крайова латка | static | колір, візерунок | надрукована; входить у групи для ґудзиків і котів |
| Дизайн-ціль | zone | умова на 6 сусідів, очки (за колір АБО візерунок / за обидва) | займає клітину ковдри; рахується в кінці |
| Ґудзик | pickup | колір; веселковий | за звʼязну групу ≥3 латок одного кольору; 3 очки |
| Кіт (кіт-картка) | zone | 2 улюблені візерунки (з чорно-білих латок), розмір групи або форма, очки 3–11 | приходить, коли склалась група одного з його візерунків потрібного розміру/форми |
| Жетон кота | pickup | очки кота | кладеться на латку щойно утвореної групи |

## Правила (КОЛИ → ЯКЩО → ТО)
**Cascadia**
- КОЛИ `turn_start` → ЯКЩО на ринку 4 однакові жетони → ТО `clear(tokens)`, нові 4 з мішка (може повторюватись); ЯКЩО 3 однакові → гравець може раз за хід замінити ці 3.
- КОЛИ `input(pick(pair))` → ТО бере плитку й жетон пари; ЯКЩО `has(nature_token)` → може натомість `choose(any_tile, any_token)` або `clear(any tokens)` з поповненням, `take(nature_token)`; витрат за хід — без ліміту.
- КОЛИ `input(place(tile, cell, rot))` → ЯКЩО `free(cell)` and `adjacent(cell, environment)` → ТО `place`; збіг місцевості **не** обовʼязковий.
- КОЛИ `input(place(token, tile))` → ЯКЩО `not occupied(tile, token)` and `custom: «символ тварини є на плитці»` → ТО `place`; інакше або за бажанням — жетон у мішок. Жетон можна покласти на будь-яку свою плитку, не лише щойно покладену.
- КОЛИ `placed(token, keystone)` → ТО `give(nature_token)`.
- КОЛИ `turn_end` → ТО ринок дозаповнюється (стос + мішок), наявні пари не зсуваються.
- КОЛИ `custom: «нема плитки для поповнення»` → ТО `game_over` (кожен зробив рівно 20 ходів).
- Рахунок коридорів: для кожного типу місцевості 1 очко за плитку **найбільшого** коридору; бонус: 2 гравці — +2 найбільшому (нічия +1 кожному); 3–4 гравці — +3 / +1 (правила нічиїх у правилах); соло — +2 за кожен коридор ≥7.
- Рахунок тварин (картки A–D, по одній на вид):
  - ведмідь: групи точного розміру не торкаються одна одної — A: за кількість пар; B: 10 за кожну групу рівно з 3; C: групи 1–3 + бонус 3 за всі три розміри; D: групи 2–4.
  - лось: A — прямі лінії (сторона до сторони); B — точні фігури; C — будь-які звʼязні групи за розміром; D — кільцеві формації; кожен лось рахується раз, групи — найвигідніше трактування.
  - лосось: «run» — кожен лосось має ≤2 сусідів-лососів, до run не торкається інший лосось; A — до 7, B — до 5, C — 3–5, D — 1 за лосося + 1 за кожну сусідню тварину.
  - яструб: A — яструби без сусідів-яструбів; B — такі ж, але з лінією видимості до іншого; C — 3 за кожну лінію видимості між двома (перериває лише інший яструб); D — пари яструбів × кількість різних тварин між ними.
  - лисиця: A — кількість **різних** сусідніх видів; B — різних сусідніх пар; C — кількість найчастішого сусіднього виду; D — пари лисиць × різні пари довкола (8 клітин).
- Фінал: тварини + коридори + бонуси + шишки; нічия → більше шишок, далі — спільна перемога.

**Calico**
- КОЛИ `input(place(patch, cell))` (з руки 2) → ЯКЩО `free(cell)` → ТО `place`; потім `choose(market[1..3])` у руку, ринок поповнюється зі стосу.
- КОЛИ `placed(patch)` → ЯКЩО `connected(same colour) ≥ 3` and `custom: «група ще не має ґудзика»` → ТО `give(button[colour])`; розширення групи до 6 нового ґудзика не дає — потрібна окрема група.
- КОЛИ `custom: «є ґудзики всіх 6 кольорів»` → ТО `give(rainbow_button)`.
- КОЛИ `placed(patch)` → ЯКЩО група одного з 2 візерунків кота досягла `count ≥ n` (Millie 3+, Tibbit 4+, Coconut 5+, Cira 6+, Gwenivere 7+) або `custom: «збігає з формою кота (з поворотом)»` (Callie, Rumi, Tecolote, Almond, Leo) → ТО `give(cat_token)` на латку групи; одна група візерунка = один кіт; група, що торкається вже зарахованої, кота не дає.
- Дизайн-ціль (6 сусідів): `≠` — усі різні; `AAA-BBB` — дві трійки; `AA-BB-CC` — три пари; `AAAA-BB`; `AAA-BB-C`; `AA-BB-C-D`. Виконано за кольором АБО візерунком → менші очки; за обома → більші (напр. AA-BB-CC: 7 / 11, ≠: 10 / ?).
- КОЛИ `custom: «ковдра заповнена в усіх»` → ТО `game_over`; очки = цілі + коти + ґудзики (3 за кожен); нічия → більше котів → більше ґудзиків.

## Керування і ввід
- Цифрові версії: клік по парі/латці ринку → привид на полі; клік по клітині — плитка; кнопки поворот ↻/↺; другим кліком — жетон на дозволену плитку (підсвітка); «скинути жетон»; кнопка шишки → режим вільного вибору або вибір жетонів для заміни.
- Cascadia Steam: перегляд коридорів і груп тварин оверлеєм, прев'ю очок до підтвердження (?).
- Черга — по колу; у Calico Steam — живі коти на полі (погладити/прогнати) — косметика.

## Вікна, меню, HUD
- `main-menu`: Соло / Сценарії / Daily Trek / Онлайн / Pass & Play / Family Mode / Налаштування.
- `match-setup`: гравці, AI, вибір карток A–D або випадково; Calico — коти, цілі.
- `scenario-select` — 15 сценаріїв Cascadia (цілі 80–100 очок + 1–4 додаткові обмеження); Calico — соло-сценарії й кампанія.
- `game-screen`: поле гравця (pan/zoom), ринок пар (`market-pairs`), 5 карток тварин (`objective-cards`), лічильник шишок (`coins`), `remaining-counter` (ходи/плитки), `opponent-boards`, `score-preview`.
- `end-screen`: таблиця «тварини × 5 + коридори × 5 + бонуси + шишки» (як аркуш рахунку).
- `achievements-window` — «піший маршрут» досягнень (Cascadia) / ряд котиків (Calico) — уже в паперових правилах.
- Переходи: main-menu → match-setup/scenario-select → game-screen → end-screen → main-menu.

## Фічі поза полем
- `mode-daily` (Daily Trek — 3 виклики щодня), `mode-coop` (split-screen), `online-multiplayer` (крос-платформа), `hotseat`, `ai-opponent-levels` (Calico).
- `custom-rules`: варіанти карток A–D, Family/Intermediate варіант (одна картка для всіх тварин: група 1→2, 2→5, 3+→9), Calico — сімейний (цілі не рахуються), «2-гравці низька варіативність».
- Сценарії й досягнення: сценарій = набір карток + поріг очок + обмеження («тварини X і Y не поруч», «X лише поруч з Y», «місцевість не на місцевості») — паперовий `achievements`.
- Соло: ринок як конвеєр — після ходу найдальша від стосу пара скидається, решта зсуваються.

## Варіації й родичі
- Cascadia: Landmarks (орієнтири з бонусами), Rolling Hills/Rivers (roll-and-write), Cascadia Junior (?); Calico: Kickstarter-коти.
- Родичі: Kingdomino (групи місцевості), Isle of Cats (коти й форми), Akropolis (гекс-райони з умовами), Sagrada (ціль на сусідів), Dorfromantik (гекс-прибудова з квестами).
- **Осі варіацій**: межі поля (без меж / ковдра) · шари (1 / плитка + жетон) · одиниця рахунку (найбільша група / кожна група / лінія / сусідство / форма) · ринок (пари / рука + ринок / драфт) · хто визначає мету (картки на партію / дизайн-цілі гравця / сценарій).

## Цікавинки для курсу
- Двошарова клітина (місцевість + жетон з білим списком символів) — 📎.
- Набір функцій рахунку як «плагіни» (20 карток тварин): групи точного розміру, лінії, змійки з max 2 сусідами, лінія видимості на гекс-сітці, різноманіття сусідів — 🥈 за набір, кожна 📎–🥉.
- Розбиття звʼязної групи лосів на фігури «найвигідніше» (кожен лось один раз) — 🥇 (пошук оптимального покриття).
- Ринок з «перенаселенням»: 4 однакові → автозаміна, 3 → опційна — 🌱.
- Calico: розпізнавання форми з точністю до повороту на гекс-сітці (кіт-фігура) — 🥉.
- Calico: дизайн-ціль як мультимножина кольорів/візерунків 6 сусідів (≠, AA-BB-CC…) — 📎.
- Звʼязні групи з урахуванням надрукованих крайових латок і правила «одна група — один ґудзик/кіт» — 📎.

## Мапа на каталог
- Є: `cell-click` · `drag-drop-piece` · `hover-highlight` · `legal-move-highlight` · `turn-enforcement` · `hot-seat` · `ai-opponent` · `event-points` · `round-currency` (шишки) · `game-settings` · `daily-puzzle` (Daily Trek) · `leaderboard`.
- **Нема** → пропозиції карток:
  - `+hex-grid-render` — див. hex.md.
  - `+connected-placement` — як у Kingdomino; тут без збігу місцевості.
  - `+two-layer-placement` «Плитка + жетон на ній з білим списком» · entities/legality · 📎.
  - `+paired-market` «Ринок фіксованих пар плитка+жетон» · game-logic/economy · 🌱 · слоти {pairs: 4}.
  - `+market-wipe` «Перенаселення: однакові в ринку змиваються» · game-logic/economy · 🌱 · слоти {auto: 4, optional: 3}.
  - `+rule-bending-token` «Жетон, що дозволяє порушити правило вибору» · game-logic/economy · 🌱 — родич `+rule-bending-tools` (Sagrada).
  - `+connected-group-scoring` — як у Kingdomino; тут найбільший коридор кожного типу.
  - `+corridor-majority-bonus` «Бонус за найбільшу групу серед гравців» · game-logic/score · 🌱.
  - `+shape-pattern-match` — як у Tiny Towns; тут лосі/коти з поворотом на гексах.
  - `+line-of-sight-scoring` «Очки за лінії видимості між однаковими» · game-logic/score · 📎 — яструб C.
  - `+neighbor-variety-scoring` «Очки за різноманіття сусідів» · game-logic/score · 📎 — лисиця.
  - `+run-shape-scoring` «Ланцюг, де кожен має ≤2 однакових сусідів» · game-logic/score · 🥉 — лосось.
  - `+public-objectives` — як у Sagrada; тут одна картка на вид.
  - `+scenario-goals` «Сценарій = поріг очок + обмеження» · levels/bank · 📎.
  - `+hand-plus-market` «Рука з 2 + ринок з 3» · game-logic/economy · 🌱 — Calico.
  - `+prefilled-border` «Надруковані крайові клітини входять у групи» · entities/state · 🌱.
  - `+neighborhood-goal` «Ціль на склад 6 сусідів клітини» · game-logic/score · 📎 — дизайн-цілі.
  - `+group-once-reward` «Одна група — одна нагорода; торкання зарахованої не дає нової» · game-logic/score · 📎.
  - `+rainbow-set-bonus` «Бонус за повний набір кольорів» · game-logic/score · 🌱.

## Пропозиції до словників
- `+trigger:placed` · `+trigger:pattern(group(n)|shape|line)` — як у сусідах.
- `+effect:place` · `+effect:draft` · `+effect:clear` — змивання жетонів ринку.
- `+cond:connected` · `+cond:same` · `+cond:adjacent_count` · `+cond:line_of_sight` — уже ⏳, тут на гекс-сітці.
- `+role:supply` (ринок, мішок) · `+role:tile` · `+role:token` — другий шар на плитці (жетон тварини), відрізняється від `pickup`, бо кладеться гравцем.
- `+ui:opponent-boards` · `+ui:score-preview` · `+ui:market-pairs` (пари плитка+жетон) · `+ui:objective-cards` (картки рахунку на екрані).
- `+window:match-setup` · `+window:scenario-select` — сценарій з порогом і обмеженнями.
- `+feature:scenarios` · `+feature:achievements` (паперова мапа досягнень у правилах).
- `+axis:turn-structure` = `round-robin`.

## Джерела
- ⭐ [Cascadia: правила AEG (PDF)](https://www.alderac.com/wp-content/uploads/2025/04/Cascadia_BaseGame_Rulebook_Optimized.pdf) — склад (85 плиток, 25 ключових, 100 жетонів, 25 шишок, 21 картка), хід, перенаселення, розміщення, коридори й бонуси, усі картки A–D, соло, сценарії.
- [Calico: правила AEG (PDF)](https://www.alderac.com/wp-content/uploads/2025/04/Calico_BaseGame_Rulebook_Optimized.pdf) — 108 латок, дизайн-цілі з очками, 10 котів, ґудзики й веселковий, фінал, соло-конвеєр, варіанти.
- [Wikipedia: Cascadia](https://en.wikipedia.org/wiki/Cascadia_(board_game)) — автор, нагороди (SdJ 2022).
- [Wikipedia: Calico](https://en.wikipedia.org/wiki/Calico_(board_game)) — автор, ґудзики/коти коротко.
- [Steam: Cascadia](https://store.steampowered.com/app/2438970/Cascadia/) — режими цифрової версії.
- [Steam: Quilts and Cats of Calico](https://store.steampowered.com/app/1993180/Quilts_and_Cats_of_Calico/) — кампанія, AI, онлайн.
- [Flatout Games: Cascadia](https://www.flatout.games/cascadia) · [BGG: Calico](https://boardgamegeek.com/boardgame/283155/calico).

## Непевне
- (?) Таблиці очок карток тварин A–D (крім «ведмідь B = 10 за трійку», «яструб C = 3 за лінію», сімейна 2/5/9) — дрібний друк, не переписано.
- (?) Очки дизайн-цілей Calico, крім ≠ 10 (за колір), AA-BB-CC 7/11, AA-BB-C-D 5/7 — решта нечитабельні на скані.
- (?) Пари котів на двосторонніх картках і групи «за крапками» в стандартному сетапі — точно не звірено.
- (?) Прев'ю очок і оверлеї в Steam-версіях — з описів, не з запуску; консольні/мобільні версії не перевірено.
