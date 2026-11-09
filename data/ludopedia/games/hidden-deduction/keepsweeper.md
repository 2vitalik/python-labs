---
title: Keepsweeper
slug: keepsweeper
aka: []
family: hidden-deduction
also: [build-sim]
klass: hybrid
axes:
  field: square
  time: realtime
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2026
platforms: [web (HTML5), iOS, Android]
links:
  - {kind: itch, url: "https://flarup.itch.io/keepsweeper", best: true, note: "грати в браузері; режими, керування, Royal Seals, скарби; коментарі про ферми, ліси, портали скелетів"}
  - {kind: official, url: "https://keepsweeper.com/about/", note: "що під клітинами (золото, скрині, лігва гоблінів, крипти, сплячі дракони), будівлі, армія"}
  - {kind: official, url: "https://keepsweeper.com", note: "«Minesweeper meets real-time strategy»; трейлер, сторінки сторів"}
  - {kind: other, url: "https://flarup.itch.io/keepsweeper/devlog", note: "збірки 20–28 (вересень–жовтень 2026): погода, Daily Realm, пустелі, боги"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Keepsweeper+gameplay", note: "пошук; геймплей і трейлер"}
stage: v1
coverage: 30
mechanics: [cell-click, neighbor-count-clue, hidden-under-block, round-currency, enemy-waves, tower-placement, online-multiplayer, in-game-editor, daily-puzzle, mode-select, game-pause, save-progress, language-picker, run-relics, hover-highlight, game-screen, +worker-dig-queue, +reveal-builds-land, +hidden-lairs-spawn, +weather-changes-routes, +daily-shared-realm]
proposes: ["+trigger:dug(c)", "+effect:assign_worker", "+effect:build", "+role:worker", "+role:building", "+window:realm-journal", "+window:research-tree", "+feature:royal-seals", "+card:worker-dig-queue", "+card:reveal-builds-land", "+card:hidden-lairs-spawn", "+card:weather-changes-routes", "+card:daily-shared-realm"]
author: opus
date: 2026-11-09
---

# Keepsweeper — сапер як RTS: читаєш числа, посилаєш робітників копати клітини й будуєш королівство на відвойованій землі

## Суть
Гібрид `cursor`-сапера і стратегії в реальному часі: гравець читає числові підказки, вирішує, які клітини безпечно розкопати, і посилає туди робітників. Розкопана земля стає місцем для ферм, будинків і оборони, а під клітинами ховаються золото, скрині, лігва гоблінів, крипти і сплячі дракони. Ризик кожної «експедиції» обирає сам гравець; армія й оборона захищають замок від того, що вилізло з-під землі.

## Поле і час
- Квадратна сітка-мапа (за скріншотами й описом (?)); процедурна генерація у Wilds, задані мапи в Quests і редакторі.
- Реальний час із паузою в соло-грі для планування.
- Погода (дощ, сніг, туман, блискавка) змінює мапу: замерзлі ріки відкривають нові маршрути, робітники відновлюють роботу після відлиги (Build 21).
- Біоми: ліс (можна рубати), пустеля з оазами, кактусами й пірамідами (1.1), острів Castaway Isle (Build 24).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Робітник | ally | — | іде розкопувати клітину з черги; збирає ресурси |
| Солдат | ally | спорядження | захищає замок; казарма вміщує більше солдатів (Build 25) |
| Замок (Keep) | static | — | те, що треба вберегти (назва гри) |
| Закрита клітина | static | прихований вміст | відкривається робітником |
| Число-підказка | mark | n | підказка про небезпеку довкола (?) |
| Золото / скриня / скарб | pickup | — | ресурс або скарб, що змінює правила забігу |
| Лігво гоблінів · крипта · портал | spawner | — | породжує ворогів (портали — скелетів) |
| Сплячий дракон | boss | — | ціль режиму Dragon Hunt (?) |
| Ферма · будинок · вітряк | static | — | економіка; вітряк підтримує ферми |
| Коваль · каплиця · казарма · гарнізон | static | — | спорядження і підтримка армії |
| Вежа | tower | — | оборона; в Siege — уздовж дороги проти хвиль |
| Ліс | terrain | — | рубається; ферма на лісі блокує його вирубку (баг-репорт) |
| Суперницьке королівство | enemy | — | AI-суперник у Quests, Wilds |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dig, c)` → ТО `custom: «робітник іде до клітини й розкопує»`; drag — поставити кілька клітин у чергу.
- КОЛИ `custom: «клітину розкопано»` → ЯКЩО `occupied(c, gold)` → ТО `currency(+n)`.
- КОЛИ `custom: «клітину розкопано»` → ЯКЩО `occupied(c, chest)` → ТО `give(player, treasure)` — скарб змінює правила поточного забігу.
- КОЛИ `custom: «клітину розкопано»` → ЯКЩО `occupied(c, lair|crypt)` → ТО `custom: «відкрито джерело ворогів»`, далі `spawn(goblin|skeleton)` (?).
- КОЛИ `custom: «клітину розкопано»` → ЯКЩО `occupied(c, dragon)` → ТО `custom: «дракон прокидається»` (?).
- КОЛИ `after(reveal(c))` → ТО `reveal(c)` з числом `custom: «кількість небезпек довкола»` (?).
- КОЛИ `input(build, c, building)` → ЯКЩО `state(c, revealed)` and `custom: «вистачає ресурсів»` → ТО `place(player, building)`, `currency(-cost)`.
- КОЛИ `input(attack, enemy)` → ТО `custom: «солдати атакують ціль»`.
- КОЛИ `schedule(waves)` → ЯКЩО `mode(siege)` → ТО `spawn_at(enemy, road_start)` — нескінченні хвилі, вежі вздовж дороги.
- КОЛИ `custom: «погода: мороз»` → ТО `set_cell(river, frozen)` — новий маршрут; відлига → робітники відновлюють.
- КОЛИ `custom: «ціль квесту виконано»` → ТО `win`, `give(player, royal_seal)` (перше проходження).
- Перемога: ціль квесту / Daily Realm (полювання на драконів, скарбниця, повернення земель, розгром суперника). · Поразка: (?) імовірно, втрата замку. · Рахунок: —.

## Керування і ввід
- Клік / тап — копати, будувати, атакувати; drag — черга розкопок.
- Навести (або утримати на тачі) — деталі клітини чи будівлі (`tooltip`).
- Пауза в соло-грі для планування.

## Вікна, меню, HUD
- `main-menu` → `mode-select`: Quests, Daily Realm, Wilds, Siege, Multiplayer, Map Editor.
- `level-select` / `world-map`: чотири шляхи квестів по двадцять рівнів (?) — точний вигляд не бачив.
- `game-screen`: мапа, ресурси (діаманти при копанні, монети при купівлі), меню будівель, «Windows-style» інтерфейс.
- `daily-window` + `custom-window` «Realm Journal» — журнал перемог Daily Realm.
- `upgrade-window` / `custom-window` Research — дослідження будівель, апгрейдів і пасивок за Royal Seals; звʼязки дерева розкладаються самі (Build 20).
- `lobby-window` для мультиплеєра; `editor-window` — редактор сценаріїв; `settings-window` (мова EN/JP); вікно перемоги з анімацією (Build 21).

## Фічі поза полем
- `meta-progression`: Royal Seals відкривають будівлі, апгрейди й пасивки на майбутні забіги; скарби — `run-relics` поточного забігу.
- `mode-daily` (Daily Realm: спільне на день королівство з ціллю) · `mode-endless`-подібний Siege · `online-multiplayer` 2–4 гравці, команди, проти AI-королівств, co-op Siege.
- `level-editor` (Map Editor) · `autosave` у браузері без синхронізації · `localization` (EN, JP за мовою браузера).
- 16 богів і пам'ятки (Build 20) — призначення (?).

## Варіації й родичі
- Сапер з економікою: [dynamine](dynamine.md); сапер з бійкою за рівнями: [mamono-sweeper](mamono-sweeper.md).
- Сусідні сімʼї: build-sim (ферми, ресурси), tower-lanes (Siege — вежі вздовж дороги).
- **Осі варіацій**: хто відкриває = курсор / робітник з чергою; відкрита клітина = лише інформація / будівельна ділянка; небезпека = миттєвий програш / джерело ворогів.

## Цікавинки для курсу
- Черга розкопок для робітників (drag додає клітини) — 📎.
- Відкрита клітина як ресурс простору: будувати можна лише на розкопаному — 🌱.
- Приховані лігва, що після відкриття стають спавнерами — 📎.
- Погода як таймерна зміна типів клітин (ріка ↔ лід) — 🥉.
- Спільний «реалм дня» з фіксованим seed і журналом — 📎.

## Мапа на каталог
- Є: `cell-click` · `neighbor-count-clue` (?) · `hidden-under-block` ↔ скарби під клітинами · `round-currency` · `enemy-waves` + `tower-placement` ↔ Siege · `run-relics` ↔ скарби · `online-multiplayer` · `in-game-editor` · `daily-puzzle` ↔ Daily Realm · `game-pause` · `save-progress` · `language-picker` · `hover-highlight`.
- **Нема** → пропозиції карток:
  - `+worker-dig-queue` «Робітники розкопують клітини з черги» · entities/move · 📎.
  - `+reveal-builds-land` «Відкрита клітина стає ділянкою для будівлі» · entities/interact · 🌱.
  - `+hidden-lairs-spawn` «Прихована клітина-лігво стає спавнером після відкриття» · entities/spawn · 📎.
  - `+weather-changes-routes` «Погода змінює прохідність клітин» · entities/state · 🥉.
  - `+daily-shared-realm` «Спільна мапа дня з журналом» · levels/bank · 📎.

## Пропозиції до словників
- `+trigger:dug(c)` — клітину розкопано (відкриття не миттєве, а наприкінці роботи робітника).
- `+effect:assign_worker(c)` — поставити робітника/чергу на клітину.
- `+effect:build(c, building)` — звести будівлю (від `place` відрізняє ціна й час будівництва).
- `+role:worker` — підконтрольний NPC, що виконує накази-черги.
- `+role:building` — будівля гравця з функцією (економіка, армія).
- `+window:realm-journal` · `+window:research-tree`.
- `+feature:royal-seals` — валюта мета-прогресії за перші проходження.

## Джерела
- ⭐ [itch.io: Keepsweeper](https://flarup.itch.io/keepsweeper) — опис, режими, керування, коментарі гравців.
- [keepsweeper.com/about](https://keepsweeper.com/about/) — що ховається під клітинами, будівлі, армія, режими; автор Michael Flarup.
- [keepsweeper.com](https://keepsweeper.com) — слоган, трейлер, стори.
- [Девлог](https://flarup.itch.io/keepsweeper/devlog) — збірки 20–28, Daily Realm 1.1.

## Непевне
- (?) Що саме рахують числа (небезпеки? усі приховані обʼєкти?) — у джерелах лише «read the number clues».
- (?) Що стається, коли робітник розкопує лігво чи дракона; умова поразки.
- (?) Форма поля (квадрат чи інше) — за описом «tiles», без перевірки.
- (?) Рік 2026 — за датами девлогу (вересень–жовтень 2026), гра «In development»; перша публічна збірка може бути раніше.
- (?) Сімʼя: економіка й армія можуть переважати дедукцію — тоді `build-sim`.
