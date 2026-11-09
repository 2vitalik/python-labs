---
title: Starseed Pilgrim
slug: starseed-pilgrim
aka: []
family: thinky
also: [grid-platformer, build-sim]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: runtime
  goal: collect
year: 2013
platforms: [PC, Mac]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Starseed_Pilgrim", best: true, note: "розділ Gameplay: хаб, насіння за кольором, рожеві блоки дають насіння, ключі, корупція, інвертований світ"}
  - {kind: steam, url: "https://store.steampowered.com/app/230980/Starseed_Pilgrim/", note: "опис («symphonic garden», «spreading darkness»), реліз 16.04.2013, droqen"}
  - {kind: official, url: "https://www.starseedpilgrim.com/", note: "сайт гри; автори: droqen (гра), Mert Batirbaygil (арт), Ryan Roth (звук)"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=167559012", note: "гайд спільноти «Basic Block Mechanics» (знятий, застарілий): кольори блоків, клавіші, H — додому"}
  - {kind: other, url: "https://www.popmatters.com/the-mis-education-of-the-player-2495694290.html", note: "есей: блоки руйнуються ходом у них, темрява розповзається, інверсія світу, ключі в білій безодні"}
  - {kind: other, url: "https://www.4p.de/test/starseed_pilgrim/79659", note: "рецензія 4Players (DE): рожеві кубики → насіння, патерни росту, пружини, частковий випадок"}
  - {kind: other, url: "https://www.commonsensemedia.org/game-reviews/starseed-pilgrim", note: "рецензія: порядок посадки, інвертований світ, повернення з насінням"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Starseed+Pilgrim+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [move-by-input, keyboard-controls, gravity-fall, dig-terrain, destructible-blocks, inventory-items, blob-growth, explode-area, key-and-door, collect-quota, player-camera, environment-death, save-progress, +plant-seed-growth, +seed-queue, +world-inversion, +spreading-terrain, +jump-booster-block, +no-jump-surface, +hub-world, +carry-over-between-worlds]
proposes: ["+effect:grow_pattern", "+effect:invert_world", "+role:seed", "+ui:seed-queue", "+feature:return-home", "+card:plant-seed-growth", "+card:world-inversion", "+card:seed-queue"]
author: opus
date: 2026-11-09
---

# Starseed Pilgrim — сади з насіння-блоків: посади насіння, кожен колір росте за своїм правилом, тікай від темряви, що інвертує світ

## Суть
Двовимірний пазл-платформер droqen: пілігрим стоїть на платформі з блоків, отримує кілька насінин випадкових кольорів і садить їх у блоки — кожен колір вирощує рослину зі своїм патерном росту й властивістю. Вирощеними блоками треба добудуватись до ключів, що висять над безоднею, поки від стартової платформи розповзається темрява. Дотик до темного блока **інвертує** світ: блоки стають порожнечею, порожнеча — твердю; у такому світі треба дійти до місця старту й ключем повернутись у хаб. Правила гра майже не пояснює — їх відкривають, тому вона й стала класикою thinky.

## Поле і час
- Квадратна сітка блоків, вид збоку, гравітація; камера стежить за пілігримом (у темному світі — центрована на останній точці опори (?)).
- Real-time: біг, стрибок, ріст рослин іде з часом; темрява поширюється поступово.
- Два стани світу: звичайний (блоки на тлі білої безодні) й інвертований (усе навпаки).
- Структура: хаб із плавучих платформ → на кожній платформі вхід у свій світ-сад.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Пілігрим | player | черга насіння | біжить, стрибає, копає блоки поруч і під собою, садить насіння |
| Стартова платформа (сіра) | static | — | точка входу; джерело темряви |
| Рожевий блок | object | ріст повільний | вертикальна вежа; викопаний дає нову насінину (старсід) |
| Помаранчевий блок | object | ріст швидкий, до ~10 угору (?) | росте прямо вгору, іноді вбік — напрям залежить від місця посадки (?) |
| Зелений блок | object | ріст швидкий | великі маси (?) |
| Фіолетовий блок | object | ріст повільний | галузиться, якщо поруч 1–3 порожні клітини, інакше росте суцільною масою (?) |
| Блакитний блок | object | — | хрест із 5 клітин; перетворює сусідні блоки на блакитні, сповільнює ріст (?) |
| Синій блок | object | 1 клітина заввишки, швидкий | пружина: допомагає стрибнути вище (?) |
| Жовтий блок («сипучий пісок») | terrain | 1 клітина заввишки | для руху вбік; з нього не стрибнеш (?) |
| Червоний блок | object | — | «бомба»: натиснути вниз — вибух руйнує блоки поруч (?) |
| Темний блок | hazard | — | розповзається по блоках від старту; дотик — інверсія світу |
| Ключ | pickup | — | висить над безоднею; потрібен, щоб вийти з інвертованого світу в хаб |
| Двері / замок | gate | 1 або 3 ключі (?) | вихід зі світу; потрійний замок веде до іншого виходу (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ТО `move(pilgrim, dir)`; КОЛИ `input(jump)` → ЯКЩО `supported(pilgrim)` and `not occupied(cell_below, quicksand)` → ТО `custom: «стрибок»`.
- КОЛИ `tick` → ЯКЩО `not supported(pilgrim)` → ТО `fall(pilgrim)`.
- КОЛИ `input(dig_dir)` → ЯКЩО `occupied(cell_dir, block)` → ТО `disappear(block)` (у ранніх описах — блок руйнується, коли в нього йдеш).
- КОЛИ `destroyed(pink_block)` → ТО `give(pilgrim, custom: «випадкова насінина»)` — нова стає в кінець черги.
- КОЛИ `input(plant)` → ЯКЩО `has(pilgrim, seed)` → ТО `place(pilgrim, seed)` у блок поруч, `custom: «з цієї клітини починає рости рослина кольору насінини»`.
- КОЛИ `timer(growth)` → ТО `custom: «рослина додає блок за патерном свого кольору»`; ріст частково випадковий (`rng`).
- КОЛИ `input(down)` → ЯКЩО `occupied(cell_below, red_block)` → ТО `explode(area)` (?).
- КОЛИ `timer(spread)` → ЯКЩО `adjacent_count(block, dark, >=, 1)` → ТО `transform(block, dark)` — темрява йде від стартової платформи по блоках.
- КОЛИ `contact(pilgrim, dark_block)` → ТО `custom: «інверсія світу: блоки й рослини → порожнеча, порожнеча → тверді блоки»`.
- КОЛИ `contact(pilgrim, key)` → ТО `pickup`.
- КОЛИ `reach(pilgrim, start_place)` → ЯКЩО `custom: «світ інвертований»` and `has(pilgrim, key)` → ТО `custom: «повернення в хаб; невикористане насіння й старсіди з темного світу лишаються»`.
- КОЛИ `custom: «насіння закінчилось»` → ТО `custom: «перехід в інвертований світ»` (рецензія Common Sense (?)).
- КОЛИ `input(place, hub)` → ЯКЩО `has(pilgrim, seed)` → ТО `place(pilgrim, seed)` — рослини на платформах хабу дають дістатися нових платформ і світів.
- КОЛИ `custom: «падіння з завеликої висоти»` або `input(hold_H)` → ТО `teleport(pilgrim, home)` (?).
- Мета: ключі й нові світи · Поразки як такої нема: втеча від темряви й повернення додому · Рахунку нема.

## Керування і ввід
- Клавіатура: ← → — біг, стрибок (?), ← → ↓ — копати в той бік, пробіл — посадити вибрану насінину.
- Утримання H — повернення в постійний світ; там H пропонує видалити збереження (?).
- Пояснень майже нема: на стіні першого екрана лише «стрибати», «рухатись», «копати».

## Вікна, меню, HUD
- `game-screen`: поле; HUD — `inventory-bar` (черга насінин іконками кольорів), у темних рівнях — число поруч із чергою (лишилось стрибків (?)).
- `map-window`-подібний хаб — сам світ із плавучими платформами, а не окреме вікно.
- `confirm-dialog`: видалити збереження (через H удома) (?).
- `splash-screen` (?): титул. Окремих меню налаштувань у джерелах нема.
- Переходи: хаб → платформа → світ-сад → (темрява) інвертований світ → (ключ на місці старту) хаб.

## Фічі поза полем
- Постійний хаб («permanent world»), де посаджене лишається між забігами; `autosave` (?).
- `meta-progression`: перенесене насіння відкриває нові платформи й світи.
- Музика: кожна посадка й ріст звучить — «symphonic garden» (Steam); деталі (?).

## Варіації й родичі
- Terraria / Minecraft (блоки), Spelunky (короткі забіги), Noita (живий матеріал), Baba Is You і The Witness (правила відкриваєш сам), Hexcells (мінімум пояснень).
- Осі варіацій:
  - **як росте блок**: детерміновано за патерном / з випадком (тут) / залежно від сусідів (фіолетовий, помаранчевий);
  - **загроза**: таймер / темрява, що розповзається (тут) / вороги;
  - **поразка**: смерть / перехід в інвертований світ (тут) / втрата ресурсу.

## Цікавинки для курсу
- Ріст рослини за правилом кольору: клітинний автомат на одну рослину з чергою росту — 🥉.
- Ріст, залежний від сусідів (галуження фіолетового при 1–3 порожніх сусідах) — 🥉.
- Темрява, що розповзається по блоках від джерела (BFS по таймеру) — 📎.
- Інверсія світу: тверде ↔ порожнє одним проходом по сітці — 🌱.
- Черга насіння з випадковими кольорами, нове — в кінець — 🌱.
- Хаб з постійним станом між забігами — 📎.

## Мапа на каталог
- Є: `move-by-input` · `keyboard-controls`; `gravity-fall`; `dig-terrain` · `destructible-blocks` ↔ копання; `inventory-items` ↔ насіння; `blob-growth` ↔ випадковий ріст рослини; `explode-area` ↔ червоний блок; `key-and-door` · `collect-quota` ↔ ключі й потрійний замок; `player-camera`; `environment-death` ↔ завелике падіння → додому; `save-progress`.
- **Нема** → пропозиції карток:
  - `+plant-seed-growth` «Посаджене насіння росте блоками за патерном типу» · entities/spawn · 🥉 · слоти {pattern, speed, rng}.
  - `+seed-queue` «Черга насіння: нове — в кінець» · entities/state · 🌱.
  - `+world-inversion` «Інверсія світу: тверде ↔ порожнє» · entities/interact · 📎.
  - `+spreading-terrain` (уже в корпусі) — темрява по блоках.
  - `+jump-booster-block` «Блок-пружина» · entities/move · 🌱; `+no-jump-surface` «Поверхня, з якої не стрибнеш» · entities/legality · 🌱.
  - `+hub-world` «Хаб із постійним станом» · levels/progression · 📎; `+carry-over-between-worlds` «Ресурс переноситься між світами» · levels/progression · 🌱.

## Пропозиції до словників
- `+effect:grow_pattern` — рослина додає клітину за патерном свого типу (зараз `custom`).
- `+effect:invert_world` — тверде ↔ порожнє по всьому полю.
- `+role:seed` — насінина в запасі, що стає рослиною після посадки.
- `+ui:seed-queue` — черга насіння іконками; `+feature:return-home` — миттєве повернення в хаб клавішею.
- `+card:plant-seed-growth`, `+card:world-inversion`, `+card:seed-queue` — див. вище.
- ⏳-слова, вжиті тут: `input`, `tick`, `timer`, `destroyed`, `contact`, `reach`, `supported`, `occupied`, `has`, `adjacent_count`, `move`, `fall`, `give`, `place`, `explode`, `transform`, `teleport`, `pickup`.

## Джерела
- ⭐ [Wikipedia: Starseed Pilgrim](https://en.wikipedia.org/wiki/Starseed_Pilgrim) — Gameplay: хаб, випадкові старсіди, колір = патерн росту, рожеві блоки → нове насіння, ключі, корупція від старту, інверсія при дотику, вихід з ключем на місці старту, перенесення насіння; розробка й реліз.
- [Steam](https://store.steampowered.com/app/230980/Starseed_Pilgrim/) — опис, Windows / macOS, 16.04.2013, droqen.
- [Сайт гри](https://www.starseedpilgrim.com/) — автори, цитата Bennett Foddy.
- [Steam-гайд «Basic Block Mechanics»](https://steamcommunity.com/sharedfiles/filedetails/?id=167559012) — кольори блоків і їхні властивості, клавіші (пробіл, стрілки, H), черга насіння, коментарі про ключі 1/3 і темний світ; гайд знятий і сам автор каже, що застарів.
- [PopMatters](https://www.popmatters.com/the-mis-education-of-the-player-2495694290.html) — руйнування блоків ходом, розповзання чорного, інверсія, ключ і замкова щілина.
- [4Players](https://www.4p.de/test/starseed_pilgrim/79659) — рожеві кубики → насіння, зірчасті й прямі патерни, пружини, частковий випадок, підказки на стіні.
- [Common Sense Media](https://www.commonsensemedia.org/game-reviews/starseed-pilgrim) — порядок посадки, інвертований світ, повернення з насінням.

## Непевне
- (?) Усе про кольори, крім рожевого, — лише зі знятого й застарілого гайду спільноти; назви кольорів і властивості могли змінитися в релізі.
- (?) Як саме настає перехід в інвертований світ — дотиком до темряви (Wikipedia) чи також коли закінчилось насіння (Common Sense).
- (?) Клавіша стрибка, число «лишилось стрибків» у темному світі, смерть від стрибка за межі камери — з коментарів до гайду.
- (?) Швидкість темряви, висота росту помаранчевого (~10), радіус вибуху червоного — не перевірено.
- (?) Що буває, якщо повернутися на місце старту без ключа.
