---
title: MinerVGA
slug: minervga
aka: [Miner VGA, Miner]
family: dig-gravity
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: hidden
  random: both
  goal: state
year: 1989
platforms: [DOS]
links:
  - {kind: other, url: "https://mail.dosgames.com/game/minervga", best: true, note: "DOSGames: опис, автор Harrell W. Stiles, грати в браузері; архів з MINERVGA.DOC"}
  - {kind: other, url: "https://mail.dosgames.com/files/minervga.zip", note: "архів гри: MINERVGA.DOC (мануал v1.1, 10.09.1989), тексти вікон у MINERVGA.EXE"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=MinerVGA+DOS+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, keyboard-controls, dig-terrain, impassable-cells, hidden-under-block, round-currency, shop-catalog, shop-window, inventory, inventory-items, hp-damage, environment-death, player-death, explode-area, save-single-slot, score-records, leaderboard, help-window, +sell-cargo, +hidden-hazard-cell, +light-source, +elevator-depth-upgrade, +random-cave-in, +tool-gated-cell, +paid-healing, +debt-risk-lose, +rumor-hints, +money-and-item-goal]
proposes: ["+effect:sell", "+feature:rumor-hints", "+card:elevator-depth-upgrade", "+card:random-cave-in", "+card:tool-gated-cell", "+card:debt-risk-lose", "+card:money-and-item-goal"]
author: opus
date: 2026-11-09
---

# MinerVGA — копай рідкісні метали за гроші: кожен крок у шахті коштує, обвали й джерела бʼють по здоровʼю, ліфт треба докуповувати

## Суть
Public-domain гра для DOS (FrodoSoft, Harrell W. Stiles, QuickBasic 4.0), переробка текстової «Miner» з Commodore PET кінця 70-х. Шахтар із $1500 на рахунку купує інструменти в місті, спускається ліфтом у шахту, клітина за клітиною прокопує ґрунт у пошуках срібла, золота й платини, здає їх у банк-пробірню і лікується в лікарні. Перемога — принести в салун міс Мімі $20 000 і діамантовий перстень. Ядро — економіка ризику: копання коштує грошей, вміст клітини невідомий, небезпеки (обвали, джерела, граніт) зʼясовуються лише при вході.

## Поле і час
- Двовимірний вертикальний розріз (VGA 640 × 480, 16 кольорів, спрайти); лише вгору/вниз/вліво/вправо, діагоналей нема.
- Згори — місто з будівлями; під ним непрохідний барʼєр ґрунтових вод («непробивний для всього, крім найпотужніших інструментів»); під барʼєром — шахта ≈ 240 футів завширшки × 960 футів углиб. Правий край шахти — шахта ліфта.
- Вміст непрокопаних клітин схований (`info: hidden`); світло підвищує шанс помітити мінерал чи небезпеку до кроку.
- Хід = одне натискання клавіші (`time: turn`, ?); випадковість — у вмісті клітин і подіях (обвали, згоряння світла).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Шахтар | player | здоровʼя %, рахунок $, мінерали (oz), предмети (≤ 1 кожного) | ходить 4 напрямки, копає, буре, качає воду, підриває |
| Пісковик | terrain | — | «легке копання» |
| Вулканічна порода | terrain | — | «важке копання» |
| Граніт | static | — | ногами не копається; бур (D) |
| Джерело | hazard | — | вода в шахті; качати відром (P) |
| Обвал | hazard | випадковий | шкода здоровʼю; можлива втрата мінералів чи предмета (?) |
| Срібло / золото / платина | resource | ціни «сьогоднішніх котирувань» | при прокопуванні → у мішок |
| Діамант | pickup | — | знахідка; потрібен для перстня, «не продавай» |
| Перстень | pickup | — | умова перемоги; добувається не в крамниці |
| Водяна помпа, конюшина | pickup | — | знахідки: помпа здешевлює відкачку, конюшина дає удачу |
| Ліфт | static | макс. глибина | єдиний шлях місто ↔ шахта; їде лише з шахтарем |
| Барʼєр ґрунтових вод | static | — | непрохідний |
| General Store (Enus) | static | 7 товарів | купівля спорядження й глибини ліфта |
| Community Bank | static | котирування | обмін мінералів на рахунок |
| St. Woody Memorial Hospital | static | $100/день, операція $300 | лікування |
| Miss Mimi's | static | їжа, пиво, нічліг | чутки-підказки; перемога |
| Туалет | static | — | колорит (за чутками там загубили перстень) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(miner, dir)`.
- КОЛИ `input(dir)` → ЯКЩО `cell(next, sandstone|volcanic)` → ТО `reveal(next)`, `set_cell(next, empty)`, `move(miner, dir)`, `currency(-cost)`; ціну знижують лопата й кирка (накопичувально), вулканічна — «важке копання».
- КОЛИ `custom: «відкрито клітину з мінералом»` → ТО `pickup(miner, silver|gold|platinum)`, `message(«You found streaks of Silver!!»)`.
- КОЛИ `input(dir)` → ЯКЩО `cell(next, granite)` → ТО `block`, `message(«Granite is too hard to dig!»)`.
- КОЛИ `input(D)` → ЯКЩО `has(miner, drill)` → ТО `message(«Press the direction?»)`, `set_cell(target, empty)`; інакше `message(«You have no drill.»)`.
- КОЛИ `custom: «відкрито джерело»` → ТО `custom: «вода заливає хід»`, `message(«You have found a Spring!»)`; КОЛИ `input(dir)` → ЯКЩО `cell(next, water)` → ТО `message(«You don't have gills!»)` (?).
- КОЛИ `input(P)` → ЯКЩО `has(miner, bucket)` → ТО `set_cell(target, empty)`, `currency(-cost)`; ЯКЩО `has(miner, pump)` → ціна менша; інакше `message(«You need a bucket.»)`.
- КОЛИ `rng(p)` при копанні → ТО `damage(miner, n)`, `message(«The mine is caving in on you!»)`; бур рятує, якщо обвал замкнув (порада з чуток).
- КОЛИ `rng(p)` → ЯКЩО `has(miner, torch|lantern)` → ТО `take(miner, torch|lantern)`, `message(«Lantern is used up.»)`; ліхтар живе довше за факел.
- КОЛИ `input(Y)` → ЯКЩО `has(miner, dynamite)` and `has(miner, torch)` → ТО `take(miner, dynamite)`, `explode(area, empty)`; ЯКЩО `custom: «праворуч нема шляху відступу»` → ТО `damage(miner, n)`, `message(«You were too close!»)`; без потрібного — `message(«You need a torch!»)` / `«You need Dynamite!»`.
- КОЛИ `input(T|B)` → ЯКЩО `custom: «шахтар у ліфті»` → ТО `teleport(miner, top|max_depth)`; у шахту ліфта можна ступити лише там, де стоїть кабіна.
- КОЛИ `input(E)` → ЯКЩО `custom: «шахтар перед дверима будівлі»` → ТО `window(shop-window|custom-window)`; поза містом — `message(«Only valid on surface»)`.
- Крамниця: КОЛИ `input(A…G)` → ЯКЩО `not has(miner, item)` → ТО `currency(-price)`, `give(miner, item)`; інакше `message(«You have it already»)`. КОЛИ `input(V)` → ТО `currency(-100)`, `counter(elevator_depth, +60 ft)`.
- Банк: КОЛИ `input(A|P|G|S|D)` → ТО `custom: «продати всі мінерали / лише платину / золото / срібло / самоцвіти за котируванням»` → `currency(+oz × quote)`.
- Лікарня: КОЛИ `input(D|A)` → ТО `currency(-100 × days)`, `heal(miner, n)`; КОЛИ `input(S)` → ТО `currency(-300)`, `heal(miner, n)` (при «immediate need of Surgery»).
- КОЛИ `counter(health, <, 20)` → ТО `custom: «показник здоровʼя червоніє»`; КОЛИ `counter(health, <, 0)` → ТО `lose`, `window(end-screen)` (надгробок).
- КОЛИ `counter(account, <, 0)` → ЯКЩО `prob(p)` → ТО `lose` («You ran out of money»); банк дає трохи в борг.
- КОЛИ `input(A)` у салуні → ЯКЩО `counter(account, >=, 20000)` and `has(miner, ring)` → ТО `win`; інакше `message(«She won't see you...»)`. Салун закритий на початку гри.
- Перемога: $20 000 і перстень у міс Мімі. · Поразка: здоровʼя < 0 або борг. · Рахунок: підсумковий рахунок у таблиці Top Ten.

## Керування і ввід
- Стрілки — рух у 4 напрямки (і копання, і вхід у ліфт).
- E — увійти в будівлю (стати перед дверима); T / B — ліфт угору / на максимальну глибину.
- D — бурити граніт, P — качати воду, Y — підрив; після D/P гра питає напрямок.
- H — довідка, S — зберегти й вийти, R — відновити, Q — вимкнути звук, X — вийти без збереження.
- У будівлях — літерні клавіші пунктів, X — вийти.

## Вікна, меню, HUD
- `splash-screen` — титул «MinerVGA by Harrell W. Stiles», завантаження спрайтів.
- `game-screen`: місто або шахта; HUD — `Health %` (`hp-bar` як число), `Bank Accnt` (`coins`), панель `Messages` з репліками на три рядки (`toast`).
- `help-window` (H): опис гри, клавіші, порада «лопата й кирка зменшують ціну, факел і ліхтар — шанс знайти».
- `shop-window` — General Store: 7 товарів $100–300 (лопата, кирка, бур, ліхтар, відро, факел, динаміт) + глибина ліфта (+60 ft за $100).
- `custom-window` — Community Bank: котирування, продаж по видах; St. Woody's: денний відпочинок, «поки не одужаю», операція; Miss Mimi's: аудієнція, пиво, їжа, нічліг (з чутками-підказками).
- `end-screen` — надгробок («Here lies a brave miner…») або сцена перемоги; підсумки здоровʼя й рахунку.
- `leaderboard` — «MinerVGA Top Ten Scores» з введенням імені.
- Переходи: титул → місто → (E) будівля → місто → ліфт → шахта → … → надгробок / перемога → Top Ten.

## Фічі поза полем
- `save-slots`-один слот (`MINERVGA.SAV`): S зберігає й виходить, R відновлює («Death is no spectre with a saved game!»).
- `leaderboard-local` (`MINERVGA.SCR`), `sound-toggle` (Q).
- `+feature:rumor-hints`: у салуні дівчата й бармен переказують чутки — справжні підказки (де шукати перстень, «носи і факел, і ліхтар», «не продавай діамант», «підрив банку може окупитись»).
- Нема рівнів, складності, редактора.

## Варіації й родичі
- Предок — текстова «Miner» для Commodore PET (кінець 70-х), окремий текстовий PC-варіант того ж автора.
- У сімʼї: [motherload.md](motherload.md) (та сама петля «копай → продай → апгрейд», але real-time з паливом), [steamworld-dig.md](steamworld-dig.md), [dig-dug.md](dig-dug.md); [infiniminer.md](infiniminer.md) — руда → гроші в мультиплеєрі.
- **Осі варіацій**: ціна копання — безкоштовно / гроші за крок / паливо; доступ углиб — вільний / ліфт, що докуповується / апгрейд бура; знання про клітину — видно все / приховано / світло дає шанс побачити; мета — очки / сума / сума + унікальний предмет.

## Цікавинки для курсу
- Економіка кроку: кожна прокопана клітина коштує, інструменти знижують ціну накопичувально — 🌱.
- Прихований вміст клітини з ймовірністю «помітити заздалегідь», що залежить від світла й удачі — 📎.
- Клітини, що потребують певного інструмента (граніт → бур, вода → відро, вибух → динаміт + факел) — 📎.
- Ліфт з купованою глибиною як прогресія доступу — 🌱.
- Місто як набір вікон-сервісів (крамниця, банк з котируваннями, лікарня, салун з чутками) — 🥉.
- Програш через борг з ймовірністю — 🌱.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` · `dig-terrain` · `impassable-cells` ↔ барʼєр, граніт без бура · `hidden-under-block` ↔ мінерали в породі · `round-currency` ↔ рахунок · `shop-catalog` + `shop-window` ↔ General Store · `inventory` + `inventory-items` ↔ предмети по одному · `hp-damage` ↔ здоровʼя % · `environment-death` ↔ обвали, джерела · `player-death` · `explode-area` ↔ динаміт · `save-single-slot` · `score-records` + `leaderboard` ↔ Top Ten · `help-window`.
- **Нема** → пропозиції карток:
  - `+elevator-depth-upgrade` «Доступна глибина купується кроками» · game-logic/economy · 🌱 · слот {step: 60 ft, price}.
  - `+random-cave-in` «Випадкова подія під час копання шкодить і забирає здобич» · entities/state · 📎 · слот {p}.
  - `+tool-gated-cell` «Клітина проходиться лише з потрібним предметом» · entities/legality · 🌱 · слот {cell → item} — родич `key-and-door`.
  - `+debt-risk-lose` «Відʼємний рахунок — щохід шанс програти» · game-logic/economy · 🌱.
  - `+money-and-item-goal` «Перемога: сума + унікальний предмет» · game-logic/win · 🌱.
  - `+rumor-hints` «NPC переказує випадкові підказки» · interface/hud · 🌱.
  - `+sell-cargo`, `+hidden-hazard-cell`, `+light-source`, `+paid-healing` — повтори з інших файлів.

## Пропозиції до словників
- `+effect:sell` — обміняти мінерали на валюту за курсом (банк; повтор).
- `+feature:rumor-hints` — чутки-підказки в будівлі-сервісі.

## Джерела
- ⭐ [DOSGames: MinerVGA](https://mail.dosgames.com/game/minervga) — опис, рік, автор, public domain, гра в браузері.
- [Архів minervga.zip](https://mail.dosgames.com/files/minervga.zip) — `MINERVGA.DOC` (мета, клавіші, місто, ліфт, лікарня, банк, крамниця, салун) і тексти вікон у `MINERVGA.EXE` (повідомлення клітин, ціни крамниці, лікарні й салуну, чутки).
- YouTube: пошук «MinerVGA DOS gameplay».

## Непевне
- (?) Чи гра справді покрокова (рух за натисканням без таймера) — мануал не каже про час, лише «дні» в лікарні.
- (?) Розмір клітини у футах (240 × 960 футів, ліфт кроками по 60 футів; рядок міста в коді — 40 клітин) — розмір шахти в клітинах не перевірено.
- (?) Відповідність літер A–G товарам: ціни ($100, $150, $250, $300, $200, $100, $300) і описи йдуть у тому самому порядку (лопата, кирка, бур, ліхтар, відро, факел, динаміт), але звʼязок вивів з порядку рядків.
- (?) Як саме добувається перстень (знайти в туалеті? оправити діамант?) — лише чутки.
- (?) Від чого втрачаються мінерали й предмети («Lost some Gold!», «You lost a possession») — найімовірніше обвали, не перевірено.
- (?) Чи можна підірвати будівлі міста («Blasting the bank could be a rewarding experience») і що це дає.
