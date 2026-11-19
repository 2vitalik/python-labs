---
title: A Monster's Snowball
slug: a-monsters-snowball
aka: [A monster's snowball]
family: push-slide
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2021
platforms: [web]
links:
  - {kind: itch, url: "https://competor.itch.io/a-monsters-snowball", best: true, note: "грати в браузері; «open-world style simple sticky sokoban», керування WASD/Z/R/X, GMTK Game Jam 2021, девлоги v1.1.0"}
  - {kind: other, url: "https://api.github.com/gists/75bc29a8623bf75c396199e57aa2200a", note: "сирці PuzzleScript: липкі сніжки, сніжка у воді → суша, чекпойнти, мапа 77×73; невикористані лід і ящик"}
  - {kind: other, url: "https://gomamisomix.hatenadiary.com/entry/2021/06/14/130249", note: "блог автора (JA): тема «Joined Together», відрив сніжки з групи, вирізаний лід, натхнення A Monster's Expedition"}
  - {kind: other, url: "https://www.bontegames.com/2021/06/a-monsters-snowball-browser.html", note: "Bart Bonte: «зʼєднай острови, ліплячи сніжки»; коментарі гравців про чекпойнти"}
  - {kind: other, url: "https://sftrabbit.github.io/PuzzleScript-smoothscreen/editor.html?hack=75bc29a8623bf75c396199e57aa2200a", note: "гра в редакторі форку PuzzleScript-smoothscreen"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=A+Monster%27s+Snowball+puzzlescript", note: "пошук; геймплей"}
stage: v1
coverage: 85
mechanics: [move-4dir, keyboard-controls, push-object, stick-together, fill-hole, impassable-cells, reach-exit, checkpoint, restart-level, undo-unlimited, player-camera, level-from-txt, sound-effects, +push-chain, +group-split, +open-world-puzzles, +checkpoint-reveal]
proposes: ["+feature:checkpoint-reveal", "+card:group-split", "+card:checkpoint-reveal"]
author: opus
date: 2026-11-19
---

# A Monster's Snowball — штовхай липкі сніжки в море, щоб із них виросли мости до синього друга

## Суть
Джем-гра competor (GMTK Game Jam 2021, тема «Joined Together», 48 годин, PuzzleScript): червоний монстрик має дійти до синього друга через архіпелаг. Єдиний інструмент — сніжки: що торкаються боками, ті злипаються в групу, і поштовх однієї рушить усю групу. Сніжка, зіштовхнута в море, тоне й стає сушею — так острови «зʼєднуються» (авторський опис: «Attaching snowballs, attaching islands»).

Замість рівнів — одна велика відкрита мапа, натхненна A Monster's Expedition: острови-пазли, до яких повертаєшся, і фінальний найбільший острів.

## Поле і час
- Квадратна сітка; одна мапа 77×73 клітини (v1.1.0): море, сніжні острови, скелі в морі, засніжені ялинки на суші.
- Видно вікно 25×25 клітин навколо гравця (форк PuzzleScript smoothscreen).
- Шари: фон (сніг / море / затоплена сніжка) → чекпойнти й ціль → гравець, ялинки, скелі, сніжки.
- Покроково: тік = одне натискання; падіння у воду й злипання стаються в тому самому ході. Хвилі анімуються лише, поки гравець стоїть (realtime-тік 1 с).
- На мапі 117 сніжок і 29 чекпойнтів (16 на суші, 13 у воді).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Червоний монстрик | player | напрям погляду | рух 4 напрямки; штовхає сніжку перед собою; у воду не заходить |
| Синій друг | static | — | ціль: стати на його клітину = кінець гри |
| Сніжка | object | — | зсувається на 1; штовхає сніжку попереду; злипається з сусідами по боках |
| Група сніжок | object | звʼязна за 4 сусідами | рухається разом; сніжка, що вперлася, відривається й лишається |
| Море | terrain | — | непрохідне для гравця; сніжка в ньому тоне й стає сушею |
| Сніг | terrain | — | звичайна підлога |
| Затоплена сніжка | terrain | — | колишнє море, тепер суша-міст: по ній ходять і котять інші сніжки |
| Ялинка | static | — | непрохідна стіна на суші |
| Скеля | static | — | непрохідна стіна в морі |
| Чекпойнт | terrain | на суші / у воді | наступив — збереження, клітина-чекпойнт зникає; у воді досяжний лише після засипання |
| Мітка підказки | mark | — | X показує / ховає всі ще не взяті чекпойнти |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(monster, dir)`, `face(monster, dir)`.
- КОЛИ `input(dir)` → ЯКЩО `cell(next_cell, sea)` → ТО `block` — у воду не ступити, утопитись не можна.
- КОЛИ `contact(monster, snowball)` → ЯКЩО `free(cell_behind)` → ТО `push`, `move(monster, dir)`; інакше `block` для гравця.
- КОЛИ `custom: «сніжка рушила»` → ЯКЩО `occupied(cell_ahead, snowball)` → ТО `push` — ряд сніжок попереду їде весь.
- КОЛИ `adjacent(snowball, snowball)` → ТО `attach(a, b)`: сусід з будь-якого боку отримує той самий рух — рушає вся звʼязна група.
- КОЛИ `blocked(snowball)` → ЯКЩО `custom: «сніжка — член групи, яку тягне інша сніжка»` → ТО `detach(snowball, group)`: вона лишається, решта групи їде (автор лишив цю неінтуїтивну поведінку й поставив навчальний острів).
- КОЛИ `enter(snowball, sea)` → ТО `disappear(snowball)`, `set_cell(sea, land)`, `sound(splash)` — клітина стає сушею, межі з сусідньою сушею зникають.
- КОЛИ `enter(monster, checkpoint)` → ТО `checkpoint`, `disappear(checkpoint)`, `sound(save)`.
- КОЛИ `input(X)` → ТО `custom: «показати / сховати мітки на всіх ще не взятих чекпойнтах»`, `sound(hint)`.
- КОЛИ `input(Z)` → ТО `undo(1)` — без ліміту.
- КОЛИ `input(R)` → ТО `restart` — від останнього чекпойнта, а не від початку мапи.
- КОЛИ `all_on(monster, blue_friend)` → ТО `win`, `message(«Congratulations! You beat the game!»)`.
- Перемога: дійти до синього друга. · Поразка: нема (у v1.1.0 гравець не може потрапити у воду). · Рахунку нема.

## Керування і ввід
- Стрілки / WASD — крок або поштовх; окремої дії «штовхнути» нема.
- Z — undo без ліміту; R — повернення до останнього чекпойнта (автосейв); X — показати/сховати чекпойнти, «коли не знаєш, куди йти».
- X не повторюється від утримання (`norepeat_action`).

## Вікна, меню, HUD
- `main-menu` — титул PuzzleScript: назва, автор, «start game» / «continue» (стандарт рушія).
- `game-screen` — вікно 25×25 клітин мапи без HUD; мітки чекпойнтів (`hint-marker`) за X.
- `custom-window` — фінальне повідомлення «Congratulations! You beat the game!» з подякою джему.
- Переходи: титул → мапа (з останнього чекпойнта) → синій друг → фінальне повідомлення.

## Фічі поза полем
- Відкрита мапа замість `levels-sequential`: острови-пазли без меню вибору; маршрут — ногами.
- `autosave` чекпойнтами + `restart-level` до чекпойнта; `undo` ∞.
- `hint`: X показує ще не відвідані чекпойнти як напрям далі.
- Версії: jam v1.0.0 (48 год) і v1.1.0 (17–20.06.2021: нові пазли, прибрано знайдене в проходженні обхідне рішення, виправлено застрягання на чекпойнті); jam-мапа лишилась у коді закоментованою.

## Варіації й родичі
- Є в коді, але не на мапі: **крижана підлога** (ковзання до упору; поштовх, стоячи на льоду, відкидає гравця назад — віддача), **неліпкий ящик**, утоплення гравця, що ковзнув у воду. Автор прибрав лід через помилки, а утоплення — за порадою гравця.
- Родичі: [a-monsters-expedition](../thinky/a-monsters-expedition.md) (острови й колоди-мости — пряме натхнення), [a-good-snowman-is-hard-to-build](../thinky/a-good-snowman-is-hard-to-build.md) (сніжки), [sokobond](../thinky/sokobond.md) (злипання), [sokoban](sokoban.md), [newtons-crates](newtons-crates.md) (інша фізика ряду).
- Осі варіацій:
  - **злипання**: нема (Sokoban) / назавжди за контактом (Sokobond) / за суміжністю в момент поштовху, з відривом того, хто вперся (тут);
  - **що стає з обʼєктом у воді**: зникає / засипає яму ([kwirk](kwirk.md)) / міст чи пліт (A Monster's Expedition) / продовження острова (тут);
  - **скидання**: увесь рівень / зона / до чекпойнта (тут).

## Цікавинки для курсу
- Липка група: BFS по сусідах від штовхнутої сніжки, рух усієї компоненти — 🥉.
- Відрив члена групи, що вперся (група не жорстка) — 📎 поверх групи.
- Сніжка у воді → суша, по якій далі ходять і котять — 🌱 (`fill-hole`).
- Чекпойнт-клітина: R повертає до збереженого стану світу, а не на старт — 📎.
- Підказка «покажи всі не взяті чекпойнти» — 🌱.
- Вирізана механіка: віддача на льоду (поштовх відкидає гравця назад до упору) — 🥉.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ стрілки/WASD; `push-object` ↔ сніжка; `stick-together` ↔ злипання груп; `fill-hole` ↔ сніжка в морі → суша; `impassable-cells` ↔ ялинки, скелі, море; `reach-exit` ↔ синій друг; `checkpoint` + `restart-level` ↔ R до чекпойнта; `undo-unlimited` ↔ Z; `player-camera` ↔ вікно 25×25; `level-from-txt` ↔ ASCII-мапа; `sound-effects` ↔ сплеск, збереження, підказка.
- **Нема** → пропозиції карток:
  - `+push-chain` (є в корпусі) — ряд сніжок попереду їде весь.
  - `+group-split` «Член групи, що вперся, відривається» · entities/interact · 📎 (дитина `stick-together`).
  - `+open-world-puzzles` (є з A Monster's Expedition).
  - `+checkpoint-reveal` «Показати не взяті чекпойнти» · interface/hud · 🌱.

## Пропозиції до словників
- `+feature:checkpoint-reveal` — кнопка, що позначає всі ще не відвідані чекпойнти як підказку напряму.
- `+card:group-split`, `+card:checkpoint-reveal` — див. «Мапа на каталог».
- ⏳-слова, вжиті тут: `input`, `adjacent`, `blocked`, `enter`, `cell`, `face`, `detach`, `checkpoint`, `terrain`, `mark`.

## Джерела
- ⭐ [itch.io: A monster's snowball](https://competor.itch.io/a-monsters-snowball) — гра в браузері, опис, керування, девлоги v1.1.0, лінк на сирці.
- [GitHub Gist (API)](https://api.github.com/gists/75bc29a8623bf75c396199e57aa2200a) — сирці (27.06.2021): `rigid`-злипання сніжок, `[ IceCrate Water ] -> [ exIceCrate exWater ]`, `checkpoint` на клітині `saveme`, X → мітки чекпойнтів, перемога `all Player on goal`.
- [Блог автора (JA)](https://gomamisomix.hatenadiary.com/entry/2021/06/14/130249) — тема джему, відрив сніжки, вирізані лід і утоплення, будова островів, натхнення.
- [Bart Bonte](https://www.bontegames.com/2021/06/a-monsters-snowball-browser.html) — короткий опис і коментарі гравців.
- YouTube: пошук «A Monster's Snowball puzzlescript».

## Непевне
- (?) Коли вперлася саме сніжка, яку штовхає гравець: гравець не рушає, але чи їдуть вільні сусіди її групи — з коду (`rigid` у PuzzleScript) не очевидно, у грі не перевірено.
- (?) «Continue» з останнього чекпойнта після перезапуску браузера — стандарт PuzzleScript, не перевірено.
- (?) 117 сніжок і 29 чекпойнтів пораховано з ASCII-мапи v1.1.0 у гісті; збірка на itch могла мати пізніші правки.
