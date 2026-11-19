---
title: An Architect's Adventure
slug: an-architects-adventure
aka: [建与远征]
family: push-slide
also: [thinky]
klass: avatar
axes:
  field: 3d
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2023
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1747510/An_Architects_Adventure/", best: true, note: "опис і відео: 3D-сокобан, ~130 рівнів по одному ключовому інсайту, блок за рівень → мости на мапі, підказки-мінірівні"}
  - {kind: other, url: "https://steamcommunity.com/app/1747510/reviews/?browsefilter=toprated&filterLanguage=schinese", note: "відгуки CN: ящики склеюються по горизонталі, колони — по вертикалі; група тримається, поки хоч один блок має опору; ящик у ямі з водою — сходинка"}
  - {kind: other, url: "https://steamcommunity.com/app/1747510/reviews/?browsefilter=toprated&filterLanguage=english", note: "відгуки EN: злипання при дотику, мета — клітина X, трофеї на мапі, Gain Insight, undo і reset"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=1747510&count=100&maxlength=0", note: "патчноути 2022–2024: insight-рівні, правило крижаних блоків, бомби й пастки, 138 рівнів, назви рівнів"}
  - {kind: steam, url: "https://store.steampowered.com/app/2113560", note: "безкоштовне демо (05.09.2022)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=An+Architect%27s+Adventure+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [move-4dir, keyboard-controls, push-object, stick-together, multi-cell-size, height-levels, gravity-fall, fill-hole, reach-exit, item-pickup, world-map, level-unlock, undo-unlimited, restart-level, theme-select, language-picker, +weld-adjacent, +directional-glue, +group-support, +level-reward-piece, +hint-ministage, +undo-through-restart, +open-world-puzzles, +fast-travel-points]
proposes: ["+feature:hint-ministage", "+window:hint-stage", "+ui:difficulty-stars", "+card:directional-glue", "+card:level-reward-piece"]
author: opus
date: 2026-11-19
---

# An Architect's Adventure — 3D-сокобан, де ящики злипаються в конструкції, а кожен пройдений рівень дає блок для мосту на мапі

## Суть
Інді-гра maou (кит. назва «建与远征» — «Будування й похід»): герой штовхає ящики, і ті, що торкнулись боками, **склеюються назавжди** в одну фігуру, яка далі рухається цілком. Мета рівня — дійти до клітини X, збудувавши з таких фігур мости через ями з водою, сходи чи «ручки», що відсувають перешкоди; кожен рівень тримається на одному ключовому інсайті. Зовнішній шар — мапа островів: кожен пройдений рівень матеріалізує біля свого входу новий блок, і з цих блоків склеюють мости до інших островів і до необовʼязкових трофеїв.

## Поле і час
- Сітка з висотою (3D, камеру можна трохи повертати); рівень — острівець із землею, стінами, ямами з водою й блоками.
- Покроково, без таймера; нескінченний undo і миттєвий reset.
- Висотна вісь важить: колони склеюються вгору-вниз, групи тримаються на опорі одним блоком і нависають над ямами.
- Мапа світу — окремий великий рівень-острови з бар'єрами між островами, входами рівнів (зірки складності) і власними пазлами.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой-архітектор | player | — | ходить, штовхає ящик чи склеєну групу; мета — клітина X |
| Ящик | object | — | склеюється з ящиком, якого торкнувся по горизонталі; у ямі з водою — сходинка-міст |
| Колона | object | — | штовхається (і по льоду); склеюється лише по вертикалі — з колоною над чи під собою |
| Склеєна група | object | форма з блоків | рухається цілком; тримається, якщо хоч один блок має опору |
| Яма з водою | terrain | — | непрохідна, дно теж; ящик у ній стає сходинкою |
| Земля / стіна | static | висота | опора й перешкода |
| Ціль X | static | на землі, на стіні або на ящику | герой на ній → рівень пройдено |
| Крижаний блок | object | — | «коли стаєш одночасно на кілька крижаних блоків вертикально — зникають усі» (патч); решта поведінки (?) |
| Бомба, пастка-плитка, пастка-стіна, рухомий вхід, помаранчева стіна-тригер, конвеєр | object / terrain | — | лише назви з патчноутів, поведінка (?) |
| Блок мапи світу | object | зʼявляється біля входу пройденого рівня | склеюється з іншими в мости між островами |
| Трофей | pickup | на мапі світу | необовʼязковий; для нього потрібні механіки, що є лише на мапі |
| Вхід рівня | gate | зірки складності | веде в рівень; правила відкриття змінювались патчами |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(architect, dir)`.
- КОЛИ `contact(architect, box)` → ЯКЩО `custom: «усі клітини перед склеєною групою вільні»` → ТО `push` — рушає вся група; інакше `block`.
- КОЛИ `adjacent(box, box)` по горизонталі → ТО `attach(a, b)` — назавжди; по вертикалі ящики не склеюються.
- КОЛИ `custom: «колона над іншою колоною чи під нею»` → ТО `attach(a, b)` — колони склеюються лише по вертикалі; так будують 3D-конструкції.
- КОЛИ `custom: «група зрушила»` → ЯКЩО `supported(group)` хоча б одним блоком → ТО `custom: «група стоїть цілком, решта блоків нависає»`.
- КОЛИ `custom: «група зрушила»` → ЯКЩО `not supported(group)` → ТО `fall(group)` (?).
- КОЛИ `enter(box, water_pit)` → ТО `custom: «ящик стає сходинкою-мостом, по якій ходять»`.
- КОЛИ `reach(architect, X)` → ТО `win`, `spawn_at(block, level_entrance)` — на мапі світу біля входу зʼявляється новий блок.
- КОЛИ `contact(architect, trophy)` → ТО `pickup`, `counter(trophies, +1)`.
- КОЛИ `custom: «герой стає одночасно на кілька крижаних блоків, складених вертикально»` → ТО `disappear` усіх цих блоків.
- КОЛИ `input(undo)` → ТО `undo(1)` — без ліміту.
- КОЛИ `input(reset)` → ТО `restart` — миттєво, і reset теж скасовується undo.
- КОЛИ `input(menu)` → ЯКЩО `custom: «рівень має Gain Insight»` → ТО `window(hint-stage)` — спрощена версія рівня, що підводить до ключової ідеї.
- Перемога: герой на клітині X; гра — дійти до фіналу мапи (досягнення ENDING). · Поразка: (?) не описана. · Рахунку нема; є трофеї.

## Керування і ввід
- Клавіатура або геймпад (повна підтримка); рух клітинами, поштовх — кроком у ящик.
- Undo без ліміту, reset рівня, ESC-меню з входом у підказку-мінірівень.
- Камеру можна трохи повертати (додано 24.02.2023).

## Вікна, меню, HUD
- `game-screen` мапи світу: острови, входи рівнів зі зірками складності, блоки за пройдені рівні, трофеї; швидке переміщення мапою (за відгуком).
- `game-screen` рівня: 3D-острівець; у паузі видно назву рівня.
- `pause-menu` (ESC): продовжити, Gain Insight (у складних рівнях), reset; кнопка «скинути всю мапу» — внизу меню.
- `hint-stage` (custom) — мінірівень-підказка.
- `settings-window`: стиль графіки (новий / старий), масштаб рендера (для 4K), мова (EN, 简, 繁, 日).
- Переходи: мапа → (вхід) → рівень → (X) → мапа з новим блоком; рівень → ESC → `hint-stage` → назад у рівень.

## Фічі поза полем
- `world-map` островів + `level-unlock`; мапа сама є мета-пазлом (мости з блоків, трофеї).
- `undo` ∞, `restart-level` зі скасуванням; «скинути всю мапу» — для патчів, що міняли рівні.
- `hint`: Gain Insight — система, за словами автора, натхненна Can of Wormholes; є, зокрема, у рівнях Filling, Grapple, Extend, Round trip, Conveyor belt.
- `autosave` при виході з мапи; збереження демо переходить у повну версію.
- `theme-select` (стиль графіки), `localization` (4 мови), `gamepad-support`, `achievements` (3: ENDING, EXPLORER, CRAFTSMAN).
- Острів «target on crate» — тема рівнів, де X стоїть на ящику, а не на стіні.

## Варіації й родичі
- Родичі: [sokobond](../thinky/sokobond.md) (злипання при контакті), [bonfire-peaks](../thinky/bonfire-peaks.md) (3D-ящики й будування), [stephens-sausage-roll](../thinky/stephens-sausage-roll.md) (з ним порівнюють у відгуках), [can-of-wormholes](../thinky/can-of-wormholes.md) (Gain Insight), [a-monsters-expedition](../thinky/a-monsters-expedition.md) (острови й мости), [infinifactory](../program-robots/infinifactory.md) (зварювання блоків), Block Buster Billy (за відгуком — схоже злипання; у корпусі нема).
- Осі варіацій:
  - **злипання**: нема / у всіх напрямах (Sokobond) / за типом і віссю — ящики по горизонталі, колони по вертикалі (тут);
  - **опора групи**: кожен блок окремо / група тримається, якщо хоч один блок на опорі (тут);
  - **нагорода за рівень**: зірки / ключ / будівельний блок на мапі світу (тут).

## Цікавинки для курсу
- Склеювання сусідів і рух групи цілком (BFS по компоненті, перевірка фронту) — 🥉.
- Склеювання за типом і віссю (ящики ↔ горизонталь, колони ↔ вертикаль) — 📎 поверх групи.
- Опора групи: падає, лише якщо жоден блок не спирається; консолі над ямами в 3D — 🥈.
- Ящик у ямі з водою → сходинка — 🌱 (`fill-hole`).
- Мапа світу, де нагорода за рівень — будівельний блок для мостів — 🥈.
- Підказка-мінірівень (Gain Insight) — 📎.
- Undo, що скасовує й reset — 🌱.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ кроки; `push-object` ↔ поштовх; `stick-together` ↔ склеювання; `multi-cell-size` ↔ склеєна фігура рухається як одна; `height-levels` + `gravity-fall` ↔ висоти й опора групи; `fill-hole` ↔ ящик у ямі з водою; `reach-exit` ↔ клітина X; `item-pickup` ↔ трофеї; `world-map` + `level-unlock` ↔ мапа островів; `undo-unlimited` + `restart-level` ↔ undo / reset; `theme-select` ↔ стиль графіки; `language-picker` ↔ 4 мови.
- **Нема** → пропозиції карток:
  - `+weld-adjacent` (є з Infinifactory) — склеювання назавжди.
  - `+directional-glue` «Склеювання лише вздовж осі, що залежить від типу блока» · entities/interact · 📎.
  - `+group-support` (є) — група тримається або падає цілком.
  - `+level-reward-piece` «Пройдений рівень дає будівельний блок на мапі світу» · levels/progression · 🥉.
  - `+hint-ministage` (є з Can of Wormholes) · `+undo-through-restart` (є) · `+open-world-puzzles` (є) · `+fast-travel-points` (є).

## Пропозиції до словників
- `+feature:hint-ministage`, `+window:hint-stage` — підказка як спрощений мінірівень (є з Can of Wormholes).
- `+ui:difficulty-stars` — зірки складності біля входу рівня (не оцінка проходження).
- `+card:directional-glue`, `+card:level-reward-piece` — див. «Мапа на каталог».
- ⏳-слова, вжиті тут: `input`, `adjacent`, `reach`, `supported`, `spawn_at`, `terrain`.

## Джерела
- ⭐ [Steam: An Architect's Adventure](https://store.steampowered.com/app/1747510/An_Architects_Adventure/) — опис («3D Sokoban», «Explore islands, build shapes»), блок за рівень → мости, «one key insight», підказки-мінірівні; maou, 25.03.2023, Windows.
- [Відгуки Steam CN](https://steamcommunity.com/app/1747510/reviews/?browsefilter=toprated&filterLanguage=schinese) — склеювання ящиків по горизонталі й колон по вертикалі, опора групи одним блоком, ями з водою, «ручки», трофеї з механіками лише на мапі.
- [Відгуки Steam EN](https://steamcommunity.com/app/1747510/reviews/?browsefilter=toprated&filterLanguage=english) — «blocks that stick together if their sides ever touch», мета — клітина X, блок біля входу пройденого рівня, Gain Insight, undo/reset, поворот камери.
- [Патчноути (Steam News API)](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=1747510&count=100&maxlength=0) — Gain Insight і рівні з ним, правило льоду, бомби, пастки, 139 → 138 рівнів, автосейв мапи.
- [Steam: демо](https://store.steampowered.com/app/2113560) — безкоштовне демо 2022 року.
- YouTube: пошук «An Architect's Adventure gameplay».

## Непевне
- (?) Що буває з групою без жодної опори і чи може загинути герой — відгуки описують лише «тримається, якщо хоч один блок на опорі».
- (?) Чи ящик у ямі лишається рухомим, чи стає частиною підлоги.
- (?) Крижані блоки, бомби, пастки, рухомий вхід, помаранчеві стіни-тригери, конвеєр, «Grapple»/«Extend» — відомі лише з назв у патчноутах.
- (?) Рух у 4 напрямки і чи герой лізе на блок висотою 1 — не перевірено.
- (?) Кількість рівнів: Steam — «about 130», патч — 138, відгуки — «100+» і «150».
