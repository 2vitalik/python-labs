---
title: Mirror Isles
slug: mirror-isles
aka: []
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2014
platforms: [web]
links:
  - {kind: play, url: "https://alan.draknek.org/games/puzzlescript/mirrors.php", best: true, note: "грати в браузері; керування, автори, звʼязок з A Monster's Expedition"}
  - {kind: official, url: "https://alan.draknek.org/games/", note: "каталог ігор Alan Hazelden: Mirror Isles, жовтень 2014"}
  - {kind: other, url: "https://www.puzzlescript.net/editor.html?hack=219a7db6511dad557b84", note: "вихідний код у редакторі PuzzleScript"}
  - {kind: other, url: "https://api.github.com/gists/219a7db6511dad557b84", note: "сирий gist з кодом: OBJECTS, RULES, WINCONDITIONS, 22 рівні"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Mirror+Isles+puzzlescript", note: "пошук; проходження"}
stage: v1
coverage: 70
mechanics: [move-4dir, move-by-input, push-object, mirror-reflect, beam-tracing, teleport, fill-hole, impassable-cells, environment-death, undo-unlimited, restart-level, sequential-levels, keyboard-controls, sound-effects, +mirror-image-swap, +reflectable-object]
proposes: ["+role:image", "+effect:cast_image", "+card:mirror-image-swap", "+card:reflectable-object", "+window:message-screen", "+window:title-screen"]
author: opus
date: 2026-11-09
---

# Mirror Isles — дивишся в дзеркало, бачиш себе за ним і міняєшся місцями зі своїм відображенням

## Суть
Острівний Sokoban у PuzzleScript: герой ходить сіткою, штовхає ящики й діагональні дзеркала. Кожне дзеркало, у яке «дивиться» герой по прямій, кидає його **відображення** на клітину за дзеркалом; кнопка дії міняє героя місцями з відображенням — це єдиний спосіб перетнути воду. Далі відображатися починають і ящики, тож ту саму дію отримують обʼєкти. Ядро — телепорт, ціль якого задає геометрія (відстань до дзеркала й кут), а не пара порталів.

## Поле і час
- Квадратна сітка, один екран на рівень; острови суші серед води (`Hole`). 22 активні рівні в коді.
- Шари колізій (з коду): фон → ціль / вода / ящик-у-воді → підказка → берегові декорації → тверді обʼєкти й промінь → лічильник → відображення.
- Покроково: тік = ввід гравця. `realtime_interval 0.5` у коді — лише анімація хвиль води.
- Промінь видимості — службовий обʼєкт `LOS` з лічильником кроків `00…09` і напрямком `North/East/South/West`; гравець його не бачить, бачить лише результат — відображення.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой (`Player`) | player | — | рух 4 напрямки; штовхає ящики й дзеркала; у воду не заходить |
| Відображення (`Reflection`) | image | — | безтілесне: нічого не штовхає й не блокує; зʼявляється в кінці променя після дзеркала |
| Дзеркало ×4 (`MirrorUL/UR/DL/DR`) | object | орієнтація діагоналі | одностороннє: повертає промінь на 90° лише з двох боків; з інших — промінь зупиняється; штовхається, але не у воду |
| Ящик звичайний (`NormalCrate`) | object | — | штовхається; у воді стає `CrateInHole`; не відображається |
| Ящик-дзеркальний (`ReflectableCrate`) | object | — | як звичайний, але кидає власні промені й має відображення `CrateReflection` |
| Відображення ящика (`CrateReflection`) | image | — | місце, куди ящик перескочить при дії |
| Ящик у воді (`CrateInHole`) | terrain | — | заповнена вода; лишається окремим обʼєктом у шарі води |
| Вода (`Hole`) | terrain | анімована | герой не входить; відображення на воду не ставиться (`CantMove`) |
| Стіна (`Wall`) | static | — | непрохідна; зупиняє промінь |
| Ціль (`Target`) | static | — | клітина, на якій має стояти герой |
| Підказка (`Hint`) | static | — | невидима клітина рівня 5: виводить повідомлення про ящики, що відображаються |
| Берег (`AddLand*/RemoveLand*`) | static | — | лише малювання краю острова, на правила не впливає |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell_ahead)` → ТО `move(player, dir)`.
- КОЛИ `input(dir)` → ЯКЩО `cell(cell_ahead, water)` → ТО `block`, `sound(blocked)`.
- КОЛИ `contact(player, crate)` → ЯКЩО `free(cell_behind)` → ТО `push`; інакше `block`.
- КОЛИ `contact(player, mirror)` → ЯКЩО `free(cell_behind)` and not `cell(cell_behind, water)` → ТО `push`; інакше `block`.
- КОЛИ `contact(crate, water)` → ТО `transform(crate_in_hole)` — вода заповнена.
- КОЛИ `after(move)` → ТО `custom: «кожен Player і ReflectableCrate пускає промінь у 4 напрямки»`.
- КОЛИ `custom: «промінь входить у клітину з дзеркалом з робочого боку»` → ТО `rotate(beam, 90)`; з неробочого боку — `custom: «промінь гасне»`.
- КОЛИ `custom: «промінь упирається в тверде»` → ТО `custom: «промінь гасне без відображення»`.
- КОЛИ `custom: «промінь пройшов після дзеркала стільки ж кроків, скільки до нього»` → ЯКЩО not `occupied(cell, solid)` → ТО `custom: «поставити образ героя / ящика в цю клітину»`.
- КОЛИ `custom: «відображення падає на воду»` → ТО `set_state(image, cant_move)`, відображення знімається.
- КОЛИ `input(action)` → ЯКЩО `count(reflection, >, 0)` → ТО `swap(player, reflection)`.
- КОЛИ `input(action)` → ЯКЩО `count(crate_reflection, >, 0)` → ТО `swap(crate, crate_reflection)` — ящики перескакують разом із героєм.
- КОЛИ `contact(player, hint)` → ТО `message(«ящики тепер відображаються»)`, `disappear_b`.
- КОЛИ `level_start` → ТО `custom: «правила проганяються до першого ходу»` (`run_rules_on_level_start`): відображення видно одразу.
- КОЛИ `all_on(player, target)` → ТО `win`, `next_level` (умови коду: «All Target on Player» і «All Player on Target»).
- Перемога: герой на цілі · Поразки нема: глухий кут знімається `undo`/`restart` · Рахунку нема.

## Керування і ввід
- Стрілки — рух; `Space` — обмін зі своїм відображенням (і ящиків з їхніми); `Z` — undo; `R` — рестарт рівня.
- `norepeat_action` у коді: утримання `Space` не повторює дію.

## Вікна, меню, HUD
- `title-screen` (custom, стандарт PuzzleScript): назва, автор, «start game» / «continue».
- `game-screen`: лише поле, без HUD; відображення — напівпрозорі сірі фігури.
- `message-screen` (custom): текст між рівнями — після рівня 14 «Something... has changed», фінал «Thanks for playing :)»; підказка рівня 5.
- Переходи: title → game-screen; рівень пройдено → (повідомлення) → наступний рівень; останній → фінальне повідомлення → title.

## Фічі поза полем
- `undo` ∞ і `restart-level` — стандарт PuzzleScript.
- `levels-sequential`: 22 рівні підряд, без вибору; збереження прогресу — `continue` на титулі (?).
- Звук `sfx` на блок, обмін, ящик; аудіо — dloot.
- Відкритий код: будь-хто відкриває його в редакторі PuzzleScript і робить свої рівні (`mod-support` через «hack»).

## Варіації й родичі
- Сам автор: A Monster's Expedition — «духовний наступник»; Mirror Isles — одне з джерел Order of the Sinking Star.
- Родичі: Sokoban (штовхання), LaserTank / Deflektor (дзеркало крутить промінь), Toodee and Topdee і Patrick's Parabox (гравець з'являється в «іншому місці» за правилом простору).
- Осі варіацій: **що дзеркало робить** — відбиває снаряд / кидає копію / дає телепорт; **хто відображається** — лише герой / ящики теж; **дистанція образу** — фіксована / дзеркальна (рівна відстань) / до упору; **дзеркало** — двостороннє / одностороннє / рухоме.

## Цікавинки для курсу
- Відображення як образ за дзеркалом на рівній відстані зі зломом променя на 90° — 🥉 (трасування з лічильником кроків).
- Обмін героя з образом — телепорт, ціль якого обчислюється з поля щоходу — 🥉.
- Одностороннє діагональне дзеркало, що ще й штовхається, — 📎.
- Ящики з власними образами, що стрибають тим самим `Space` синхронно з героєм — 🥈 (кілька незалежних променів, конфлікти цілей).
- Ящик у воді як міст — 🌱.
- Порт на PuzzleScript-подібний рушій правил «шаблон → заміна» — 🥇 (саме так гра й написана).

## Мапа на каталог
- Є: `move-4dir` · `push-object` (ящики, дзеркала) · `mirror-reflect` + `beam-tracing` (промінь видимості, злам на дзеркалі) · `teleport` (обмін з образом) · `fill-hole` (ящик у воді) · `impassable-cells` · `environment-death` (вода) · `undo-unlimited` · `restart-level` · `sequential-levels` · `keyboard-controls` · `sound-effects`.
- **Нема** → пропозиції карток:
  - `+mirror-image-swap` «Двійник за дзеркалом і обмін з ним» · entities/interact · 🥉 · слоти {distance: mirror|fixed, swap: action|auto}.
  - `+reflectable-object` «Обʼєкт, що має власне відображення» · entities/state · 🥈 — дитина попередньої картки.

## Пропозиції до словників
- `+role:image` — безтілесний образ сутності: видно, не штовхає, не блокує (відображення, привид-прогноз).
- `+effect:cast_image` — поставити образ сутності в обчислену клітину.
- `+card:mirror-image-swap`, `+card:reflectable-object` — див. вище.
- `+window:title-screen` — титульний екран PuzzleScript (назва + start/continue); `+window:message-screen` — повноекранний текст між рівнями.
- ⏳-слова, вжиті тут: `input`, `free`, `cell`, `occupied`, `count`, `move`, `rotate`, `swap`, `set_state`, `message`, `sound`, `after`, `level_start`, `all_on`, `next_level`, `terrain`.

## Джерела
- ⭐ [Mirror Isles на сайті автора](https://alan.draknek.org/games/puzzlescript/mirrors.php) — гра, керування (стрілки, Space swap, Z, R), аудіо dloot, звʼязок з A Monster's Expedition і Order of the Sinking Star.
- [Каталог ігор Alan Hazelden](https://alan.draknek.org/games/) — дата (жовтень 2014), лінк на код.
- [Код у редакторі PuzzleScript](https://www.puzzlescript.net/editor.html?hack=219a7db6511dad557b84) і [gist через GitHub API](https://api.github.com/gists/219a7db6511dad557b84) — обʼєкти, шари, правила, умови перемоги, 22 рівні, повідомлення.

## Непевне
- (?) Чи образ стоїть на рівній відстані за дзеркалом, виведено з логіки лічильника `00…09` у коді (рахунок уперед до дзеркала й назад після нього) — у грі не перевірено.
- (?) Максимальна довжина променя — у коді лічильник до 9, звідси межа близько 9 клітин.
- (?) Чи по `CrateInHole` можна ходити — з коду: герой блокується лише `Hole`, тож, найпевніше, так.
- (?) Як працюють рівні з кількома цілями: умова «All Target on Player» вимагає героя на кожній цілі — можливо, у таких рівнях кілька героїв.
- (?) Черга дав рік 2016 — і сайт автора, і код кажуть жовтень 2014.
- (?) Чи `continue` на титулі зберігає прогрес між сесіями (стандарт PuzzleScript — так, через localStorage).
