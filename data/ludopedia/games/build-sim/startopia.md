---
title: Startopia
slug: startopia
aka: [StarTopia, スタートピア]
family: build-sim
also: []
klass: cursor
axes:
  field: layers
  time: realtime
  opponent: ai
  info: partial
  random: runtime
  goal: state
year: 2001
platforms: [Windows, GOG (2012), Steam (2013)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Startopia", best: true, note: "станція-тор із секторів, 3 палуби, тераформінг біопалуби (температура, вологість, вода, висота), scuzzer-и, відкриття секторів за енергію, злам дверей суперника, цілі сценаріїв"}
  - {kind: wiki, url: "https://de.wikipedia.org/wiki/Startopia", note: "DE: до 16 секторів × 3 палуби, до 40 кімнат, 14 місій кампанії, нескінченний режим, до 4 гравців"}
  - {kind: steam, url: "https://store.steampowered.com/app/243040/Startopia/", note: "16 житлових секцій на трьох палубах, біопалуба з редагованим ландшафтом, мультиплеєр до 3 інших stationmaster-ів, від sandbox до мікроменеджменту"}
  - {kind: other, url: "https://www.gog.com/en/game/startopia", note: "GOG: 9 рас, загрози (метеори, паразити, пірати, чума), тераформінг біопалуби"}
  - {kind: steam, url: "https://store.steampowered.com/app/840390/Spacebase_Startopia/", note: "ремейк 2021: Sub / Fun / Bio Deck, дріади, RTS-сутички"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Startopia+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 30
mechanics: [wrap-edges, cursor-place, multi-cell-size, round-currency, spawn-random-cell, ai-opponent, online-multiplayer, sequential-levels, mode-select, tutorial-window, save-game, +ring-sectors, +sector-unlock, +biome-terraform, +habitat-requirements, +visitor-needs, +labor-pool, +door-hacking, +disguised-agent, +harvest-to-crates]
proposes: ["+card:ring-sectors", "+card:sector-unlock", "+card:visitor-needs", "+card:door-hacking", "+card:disguised-agent", "+card:harvest-to-crates", "+card:biome-terraform", "+card:habitat-requirements", "+window:advisor-window"]
author: opus
date: 2026-11-09
---

# Startopia — станція-бублик із секторів на три палуби: кімнати для прибульців знизу, тераформований сад нагорі

## Суть
Гравець — Stationmaster (Mucky Foot, ексбулфроґівці, 2001): відбудовує зруйновану станцію-тор, ставить кімнати й наймає прибульців, але прямо ними не керує — кожен має статистики, настрій і бажання. Сітковий шар — це **топологія станції** (кільце секторів × три палуби, сектори відкриваються за енергію) і **біопалуба**, ландшафт якої тераформується чотирма параметрами: температура, вологість, рівень води, висота. Решта — економіка й соціальна симуляція прибульців — коротко, бо джерела описують її загально.

## Поле і час
- Станція — тор (бублик) до 16 секторів; кожен сектор має три палуби: інженерна (найбільша, найбільше типів будівель), розважальна і біопалуба.
- Сектори відкриваються ремонтом за енергію; сусідні сектори двох гравців можна зʼєднати, щоб відвідувачі ходили між ними.
- Біопалуба — рельєф із висотою, водою, вологістю й температурою, на ньому ростуть рослини.
- Real-time; камера — 3D-вид станції зсередини («небачена досі точка зору» на тор).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Сектор (до 16) | zone | закритий / відкритий / чужий | відкривається за енергію; сусіди по кільцю |
| Двері сектора | gate | власник | між секторами; security scuzzer може зламати двері суперника |
| Інженерна палуба | zone | — | найбільша; найбільше типів будівель |
| Розважальна палуба | zone | — | розваги й «любов» для відвідувачів |
| Біопалуба | zone | температура, вологість, рівень води, висота | тераформується гравцем; на ній ростуть рослини |
| Рослина | resource | — | росте за клімату палуби, збирається → припаси |
| Кімната | object | до 40 типів: їжа, санітарія, медицина, розваги, лабораторія, аналізатор, зоряний док, центр звʼязку | обслуговує потреби прибульців або дає функцію станції |
| Прибулець (9 рас) | neutral | статистики, настрій, бажання, історія | сам обирає дії; найнятий працює за типом раси |
| Scuzzer | ally | — | прибирає, будує, ремонтує, носить ящики |
| Security scuzzer | ally | — | затримує чи виганяє злочинців, зламує двері суперника |
| Turakken | ally | — | працює в дослідницькій лабораторії |
| Arona Daal | neutral | — | торговець, доступний від початку |
| Ворожий агент | enemy | замаскований | під виглядом звичайного прибульця або «підозрілої людини» |
| Ящик | resource | — | припаси й товари; їх носять scuzzer-и |
| Метеори, паразити, пірати, чума | hazard | — | випадкові загрози станції |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(open_sector, door)` → ЯКЩО `counter(energy, >=, cost)` → ТО `currency(-cost)`, `set_state(sector, open)`; інакше `block`.
- КОЛИ `input(place_room, deck)` → ЯКЩО `custom: «тип кімнати дозволений на цій палубі й місце вільне»` → ТО `place(player, room)`.
- КОЛИ `input(terraform, area)` → ТО `custom: «змінити висоту землі, рівень води, вологість або температуру біопалуби»`.
- КОЛИ `tick` → ЯКЩО `custom: «клімат ділянки підходить рослині»` → ТО `grow(plant, 1)`; інакше `custom: «не росте»`.
- КОЛИ `custom: «рослину зібрано»` → ТО `spawn(crate)` — припаси.
- КОЛИ `custom: «у прибульця потреба (їжа, санітарія, здоровʼя, розвага, любов)»` → ЯКЩО `custom: «є кімната, що її закриває»` → ТО `custom: «іде туди»`; інакше `custom: «настрій падає»`.
- КОЛИ `input(hire, alien)` → ТО `set_state(alien, employee)` — робота за типом раси.
- КОЛИ `contact(security_scuzzer, criminal)` → ТО `custom: «затримати або вигнати зі станції»`.
- КОЛИ `contact(security_scuzzer, rival_door)` → ТО `custom: «зламати двері»`, `set_side(sector, player)` — захоплення сектора.
- КОЛИ `input(trade, merchant)` → ЯКЩО `custom: «для купців інших рас — є зоряний док і активний центр звʼязку»` → ТО `custom: «купівля / продаж ящиків»`.
- КОЛИ `input(research, analyzer)` → ЯКЩО `counter(energy, >=, cost)` → ТО `unlock(tech)`; аналізатор також `custom: «знешкоджує бомби»`.
- КОЛИ `rng(p)` → ТО `spawn_at(meteor|vermin|pirates|plague, sector)`.
- КОЛИ `custom: «прибулець іде по кільцю за останній сектор»` → ТО `wrap(alien)`.
- Перемога: мета сценарію — економічна ціль, навернути N прибульців або силою захопити всю станцію; є sandbox без мети.

## Керування і ввід
- Миша: камера по станції, вибір палуби й сектора, розміщення кімнат курсором, найм прибульців кліком; прибульцями напряму не керують.
- Тераформінг біопалуби — інструменти зміни чотирьох параметрів (як саме — пензлем чи повзунком на сектор — не підтверджено).

## Вікна, меню, HUD
- `game-screen`: 3D-вид станції, повідомлення помічника VAL (пародія на HAL 9000) — `+window:advisor-window`.
- `mode-select`: кампанія (14 місій), sandbox / нескінченний режим, мультиплеєр.
- `tutorial-window` — навчальні місії: камера, будування, торгівля.
- Збереження гри (`save-game`).

## Фічі поза полем
- `levels-sequential` — кампанія з 14 місій; `mode-sandbox`; мультиплеєр — до 4 stationmaster-ів на одній станції (конкуренція за сектори; LAN чи інтернет — не перевірив).
- Перевидання: GOG (2012), Steam (2013).

## Варіації й родичі
- **Spacebase Startopia** (2021, Realmforge / Kalypso) — ремейк: Sub Deck, Fun Deck, Bio Deck з дріадами, енергію дають відвідувачі, RTS-сутички з мехами, кооп і змагальний мультиплеєр до 4.
- Родичі в корпусі: `theme-hospital` і `two-point-hospital` (кімнати під потреби відвідувачів), `fallout-shelter` і `space-haven` (станція-сховище з шарами), `terra-nil` і `reus` (тераформінг клітин).
- **Осі варіацій**: топологія мапи — прямокутник / кільце секторів / кілька палуб; клімат — глобальний / на ділянку; відвідувачі — керовані / автономні з потребами.

## Цікавинки для курсу
- Кільце секторів × 3 палуби: індекс сектора по модулю, перехід між палубами — 🌱.
- Відкриття ділянок мапи за валюту — 🌱.
- Клімат ділянки (4 параметри) × уподобання рослин і рас — 📎.
- Автономні відвідувачі з потребами, що самі шукають кімнату — 🥉.
- Замаскований агент: сутність виглядає як інша, доки не викрита — 📎.

## Мапа на каталог
- Є: `wrap-edges` (кільце) · `cursor-place` + `multi-cell-size` (кімнати) · `round-currency` (енергія) · `spawn-random-cell` (загрози) · `ai-opponent` + `online-multiplayer` · `sequential-levels` + `mode-select` + `tutorial-window` · `save-game`.
- **Нема** → пропозиції карток:
  - `+ring-sectors` «Поле-кільце із секторів і палуб» · entities/move · 🌱.
  - `+sector-unlock` «Відкрити ділянку мапи за валюту» · game-logic/economy · 🌱.
  - `+visitor-needs` «Відвідувачі з потребами самі обирають споруду» · entities/move · 🥉.
  - `+door-hacking` «Захоплення сектора зламом дверей» · entities/interact · 📎.
  - `+disguised-agent` «Ворог під виглядом нейтрала» · entities/state · 📎.
  - `+harvest-to-crates` «Урожай стає ящиками, які носять робітники» · game-logic/economy · 📎.
  - `+biome-terraform`, `+habitat-requirements`, `+labor-pool` — підтвердження (Reus, Terra Nil, Caesar III).

## Пропозиції до словників
- `+card:ring-sectors`, `+card:sector-unlock`, `+card:visitor-needs`, `+card:door-hacking`, `+card:disguised-agent`, `+card:harvest-to-crates` — див. вище.
- `+card:biome-terraform`, `+card:habitat-requirements` — підтвердження.
- `+window:advisor-window` — помічник-коментатор (VAL; підтвердження з Caesar III).

## Джерела
- ⭐ [Wikipedia: Startopia](https://en.wikipedia.org/wiki/Startopia) — тор із секторів, 3 палуби, тераформінг біопалуби, рослини → припаси, scuzzer-и, торгівля, відкриття й злам секторів, VAL, цілі сценаріїв.
- [Wikipedia DE](https://de.wikipedia.org/wiki/Startopia) — 16 секторів × 3 палуби, 40 кімнат, 14 місій, нескінченний режим, 4 гравці.
- [Steam](https://store.steampowered.com/app/243040/Startopia/) — 16 секцій, біопалуба, мультиплеєр, sandbox.
- [GOG](https://www.gog.com/en/game/startopia) — 9 рас, загрози, тераформінг.
- [Steam: Spacebase Startopia](https://store.steampowered.com/app/840390/Spacebase_Startopia/) — ремейк.
- Фрагменти пошуку з фан-вікі Startopia (fandom не відкривається) — «nanosoil», пресети клімату, кущі й дерева, фермери Karmarama; у файлі лише в «Непевне».

## Непевне
- (?) Біопалуба як сітка клітин: чи висота/вода/вологість/температура задаються на клітину (пензлем) чи на весь сектор (повзунками) — джерела не кажуть.
- (?) За фрагментом фан-вікі: підлога біопалуби — «nanosoil»; пресети «Moderate and medium», «Moderate and wet», «Hot and dry»; рослини Lillith (кущ, 1 ящик) і Elderbaran (дерево, 2 ящики); рослини саджають фермери Karmarama; Zedem Monks ставлять Star Temple.
- (?) AI-суперники в одиночних місіях — джерела певно кажуть лише про мультиплеєр і захоплення секторів.
- (?) Енергія як валюта (плата відвідувачів за послуги) — для оригіналу не підтверджено, лише для ремейку.
- (?) Можна обійти все кільце без розриву — з топології тора, у джерелах не сказано.
