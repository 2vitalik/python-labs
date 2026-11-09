---
title: Toki Tori 2 / Toki Tori 2+
slug: toki-tori-2
aka: [Toki Tori 2+, TT2]
family: grid-platformer
also: [thinky]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: collect
year: 2013
platforms: [Wii U, PC (Steam), macOS, Linux, PS4, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Toki_Tori_2", best: true, note: "без інструментів: свист притягує істот, топ відлякує й ламає; мокре пірʼя і трава; Tokidex; платформи й дати"}
  - {kind: steam, url: "https://store.steampowered.com/app/201420/", note: "Toki Tori 2+: «Metroidbrainia», пісні rewind і fast travel, сотні золотих крил, редактор і Steam Workshop"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Toki_Tori", note: "база: інструменти з зарядами"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=toki+tori+2+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-4dir, gravity-fall, player-camera, checkpoint, rewind, in-game-editor, level-exchange, codex-window, map-window, +two-verb-control, +lure-and-scare, +creature-behavior-tools, +knowledge-gating, +input-sequence-song, +fast-travel, +state-from-terrain, +creature-photo-codex, +optional-collectibles]
proposes: ["+trigger:song(seq)", "+effect:attract(a, to)", "+effect:repel(a, from)", "+feature:fast-travel", "+window:camera-mode", "+axis:progression", "+card:lure-and-scare", "+card:knowledge-gating"]
author: opus
date: 2026-11-09
---

# Toki Tori 2 — курча має лише дві дії: свист кличе істот, топ лякає; уся гра — вивчити, як кожна істота на них реагує

## Суть
Від [toki-tori](toki-tori.md) лишилось курча, яке не стрибає по-справжньому, і бічна клітинна головоломка. Зникли **інструменти з зарядами** — головна механіка першої частини. Замість них дві кнопки-дієслова: **свист** (істоти, загалом, ідуть до курчати) і **топ** (тікають від нього; ламає деякі елементи оточення). Головоломка — використати істоти як транспорт, міст, зброю чи двері; прогресія — не нові предмети, а **знання**, як поводиться кожна істота (гравці називають жанр «Metroidbrainia»). Світ відкритий, без тексту-навчання.

## Поле і час
- Бічний вид, суцільний відкритий світ-острів замість окремих рівнів (метроїдванія); камера слідує (`player-camera`).
- Гравітація, як у першій частині; «стрибка» нема (?), підйом — через істоти й оточення.
- Real-time, без випадковості: реакції істот детерміновані.
- Стани від оточення: вода намочує пірʼя курчати; мокре курча, пройшовши по скошеній траві, змушує її вирости.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Toki Tori | player | сухий / мокрий | ходить, свистить, топає; не має інструментів |
| Істота (багато видів) | neutral | вид | на свист — загалом іде до курчати; на топ — тікає; вид визначає, що вона робить далі (несе, їсть, штовхає, світить (?)) |
| Ворожа істота | enemy | вид | шкодить дотиком або поведінкою (?) |
| Ламкий елемент оточення | static | — | руйнується від топу |
| Вода | terrain | — | робить курча мокрим |
| Скошена трава | terrain | низька / висока | росте, коли через неї проходить мокре курча |
| Чекпоінт (?) | static | — | точка, до якої повертає пісня rewind |
| Точка швидкої подорожі | static | — | ціль пісні fast travel |
| Золоте крило | pickup | «сотні» | необовʼязковий колекційний предмет за нестандартне використання механік |
| Камера / Tokidex | — (здібність) | — | викликається піснею; фото кожної істоти заповнює довідник |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(toki, dir)`; КОЛИ `tick` → ЯКЩО `not supported(toki)` → ТО `fall(toki)`.
- КОЛИ `input(whistle)` → ЯКЩО `in_range(creature, toki, r)` → ТО `custom: «істота рухається до курчати»` (`+effect:attract`).
- КОЛИ `input(stomp)` → ЯКЩО `in_range(creature, toki, r)` → ТО `custom: «істота тікає від курчати»` (`+effect:repel`).
- КОЛИ `input(stomp)` → ЯКЩО `cell(below|near, breakable)` → ТО `set_cell(target, empty)`.
- КОЛИ `enter(toki, water)` → ТО `set_state(toki, wet)`.
- КОЛИ `enter(toki, cut_grass)` → ЯКЩО `state(toki, wet)` → ТО `set_cell(grass, tall_grass)`.
- КОЛИ `custom: «введено послідовність свистів і топів»` (`+trigger:song`) → ТО за піснею: `custom: «rewind до чекпоінту»` · `teleport` (fast travel) · `window(+camera-mode)`.
- КОЛИ `input(photo)` → ЯКЩО `custom: «істота в кадрі вперше»` → ТО `custom: «запис у Tokidex»`; КОЛИ `custom: «сфотографовано всіх»` → ТО `custom: «нагорода»`.
- КОЛИ `contact(toki, golden_wing)` → ТО `pickup`, `counter(wings, +1)`.
- КОЛИ `contact(toki, enemy)` (?) → ТО `custom: «смерть / повернення до чекпоінту»`.
- Мета: дістатися до плаваючого кристала й знищити його (за сюжетом); `collect` — золоті крила як необовʼязкова повнота. Поразки в класичному сенсі нема — помилку виправляє rewind.

## Керування і ввід
- Дві дії + рух: свист, топ. Пісні — **послідовності** цих самих двох дій (як комбо-ввід), тож нових кнопок не додається.
- Геймпад рекомендовано (Steam: «Full Controller Support»; у системних вимогах — геймпад).

## Вікна, меню, HUD
- `game-screen` — світ без HUD-підказок (?).
- `map-window` — карта острова з точками швидкої подорожі (?).
- `codex-window` — Tokidex: фото й записи істот.
- `+window:camera-mode` — видошукач камери.
- `editor-window` (Toki Tori 2+, PC) — редактор рівнів.
- `main-menu`, `pause-menu`, `settings-window` — стандартні (?).

## Фічі поза полем
- `rewind` — піснею, до останнього чекпоінту (а не покроковий, як у першій частині на PC).
- `+feature:fast-travel` — піснею між точками.
- `level-editor` + `level-sharing` через Steam Workshop (2+ на Steam); 38 досягнень Steam; хмарні збереження.
- Toki Tori 2+ (Wii U, вересень 2013) — нова музика й пазли; Switch (2018) — нові секрети, 60 fps.

## Варіації й родичі
- Попередник: [toki-tori](toki-tori.md) — інструменти з зарядами на рівень; тут той самий герой, але **ні одного інструмента**.
- Родичі у «знанні як прогресії»: Outer Wilds, Tunic, Fez (поза корпусом); у сімʼї — [troddlers](troddlers.md), [catrap](catrap.md) (керування не собою, а іншими).
- **Осі варіацій:** звідки сила гравця (інструменти з зарядами / нескінченні дієслова + знання світу); що відкриває нові місця (предмет / розуміння правила); як виправити помилку (рестарт рівня / покроковий rewind / rewind до чекпоінту).

## Цікавинки для курсу
- Дві дії, від яких залежить поведінка всіх істот (`attract` / `repel` за радіусом) — 📎.
- Кожен вид істоти — свій автомат станів на ті самі два стимули — 🥉 (таблиця «вид × стимул → поведінка»).
- Пісня як послідовність двох кнопок — розпізнавання вводу-комбо — 🌱.
- Стан від клітини (мокрий) змінює інші клітини (трава росте) — 🌱.
- Довідник-фотоапарат: перше фото виду → запис — 📎.
- Rewind до чекпоінту замість рестарту рівня у відкритому світі — 📎.

## Мапа на каталог
- Є: `gravity-fall` · `player-camera` · `checkpoint` · `rewind` · `in-game-editor` + `level-exchange` (Workshop) · `codex-window` (Tokidex) · `map-window`.
- **Нема** → пропозиції карток:
  - `+two-verb-control` «Уся гра на двох діях» · interface/input · 🌱.
  - `+lure-and-scare` «Дія приманює або відлякує сутності в радіусі» · entities/interact · 📎.
  - `+creature-behavior-tools` «Істоти — інструменти гравця» · entities/interact · 🥉.
  - `+knowledge-gating` «Прогрес відкриває знання, а не предмет» · levels/progression · 🥈.
  - `+input-sequence-song` «Послідовність дій = здібність» · interface/input · 🌱.
  - `+fast-travel` «Швидка подорож між точками» · levels/progression · 🌱.
  - `+state-from-terrain` «Клітина дає стан, стан змінює інші клітини» · entities/state · 🌱.
  - `+creature-photo-codex` «Фото заповнює довідник» · interface/menus · 📎.
  - `+optional-collectibles` «Необовʼязкові колекційні предмети» · levels/progression · 🌱.

## Пропозиції до словників
- `+trigger:song(seq)` — введено задану послідовність дій (пісня, чит-код, комбо).
- `+effect:attract(a, to)` / `+effect:repel(a, from)` — сутність рухається до / від джерела стимулу.
- `+feature:fast-travel` — переміщення між відкритими точками світу.
- `+window:camera-mode` — видошукач фотоапарата поверх поля (Tokidex).
- `+axis:progression` — `items` · `knowledge` · `levels` — що відкриває нову частину гри.
- `+card:lure-and-scare`, `+card:knowledge-gating` — див. вище.

## Джерела
- ⭐ [Wikipedia: Toki Tori 2](https://en.wikipedia.org/wiki/Toki_Tori_2) — відсутність предметів, свист/топ, пісні, вода й трава, Tokidex, версії й дати.
- [Steam: Toki Tori 2+](https://store.steampowered.com/app/201420/) — «Metroidbrainia», rewind і fast travel піснями, сотні золотих крил, редактор, Workshop, 38 досягнень.
- [Wikipedia: Toki Tori](https://en.wikipedia.org/wiki/Toki_Tori) — база.
- YouTube: пошук «toki tori 2 gameplay».

## Непевне
- (?) Конкретні види істот і їхні реакції (жаби, краби-відлюдники, птахи тощо) — відкриті джерела їх не перелічують; таблицю «вид × стимул» не заповнено.
- (?) Чи є в курчати хоч якийсь стрибок або підйом на уступ, як у першій частині.
- (?) Як саме карається смерть (повернення до чекпоінту?) і чи є вороги в класичному сенсі.
- (?) Склад пісень (які послідовності) і чи є карта світу окремим вікном.
- (?) `field: square` — клітинність світу TT2 не перевірено, перша частина — сітка.
