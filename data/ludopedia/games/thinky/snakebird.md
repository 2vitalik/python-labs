---
title: Snakebird
slug: snakebird
family: thinky
also: [push-slide, grid-platformer]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: collect
year: 2015
platforms: [PC, Android, iOS, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Snakebird_(video_game)", best: true, note: "суть: Snake + гравітація по Y, фрукти подовжують, 53 рівні; Primer і Complete"}
  - {kind: steam, url: "https://store.steampowered.com/app/357300/Snakebird/", note: "опис: три птахи, нелінійна мапа, «fruit-powered length gain»"}
  - {kind: steam, url: "https://store.steampowered.com/app/1014140/Snakebird_Primer/", note: "легша версія, 70 рівнів"}
  - {kind: other, url: "https://www.movingai.com//snakebird/study/begin.html", note: "Anhinga — дослідницький клон Snakebird (Nathan Sturtevant), правила й тренувальні рівні в браузері"}
  - {kind: other, url: "https://tasvideos.org/Forum/Posts/534620", note: "TAS-нотатки: гравітація після кожного ходу, падіння блокують ввід, death cancel, star-рівні"}
  - {kind: other, url: "https://thinkygames.com/games/snakebird", note: "Thinky Games — картка гри"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=snakebird+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [move-4dir, body-queue, gravity-fall, push-object, multi-cell-size, collect-quota, reach-exit, touch-death, environment-death, teleport-pair, keyboard-controls, cell-click, swipe-gestures, sequential-levels, level-unlock, save-progress, movement-animation, +undo-redo, +grow-on-eat, +segment-support, +multi-avatar-switch, +auto-undo-on-death, +exit-all-actors, +world-map]
proposes: ["+trigger:input", "+trigger:after", "+cond:supported", "+effect:grow", "+effect:fall", "+effect:move", "+effect:undo", "+role:terrain", "+role:hazard", "+window:map-window", "+feature:undo", "+feature:world-map", "+axis:actors", "+axis:undo"]
author: opus
date: 2026-11-02
---

# Snakebird — змійка з гравітацією: з'їж усі фрукти й залети в портал, не впавши

## Суть
Snake, повернутий набік і покроковий: птах-змійка ходить головою в 4 напрямки, тіло тягнеться слідом, а після кожного ходу діє **гравітація** — якщо жоден сегмент не спирається на опору, птах падає. Фрукти подовжують тіло на 1, що змінює, на чому можна повиснути і через що перелізти. Коли зʼїдено всі фрукти, відкривається веселковий портал; усі птахи мають залетіти в нього головою. Головоломка — знайти точну послідовність ходів, де форма тіла стає інструментом: місток, драбина, підпора для іншого птаха.

## Поле і час
- Квадратна сітка, вигляд збоку (вертикаль = гравітація); рівень — один екран-острів у морі. Низ екрана — вода/порожнеча: падіння туди = смерть.
- Покроково: хід = один крок голови активного птаха; далі гравітація застосовується до всіх птахів і блоків, доки все не спиниться. Під час падіння ввід заблоковано.
- Один шар обʼєктів; клітина — або земля, або шип, або обʼєкт (сегмент, блок, фрукт), або порожньо.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Snakebird (червоний/зелений/синій) | player | довжина N сегментів, голова | голова крок у 4 напрямки, тіло — `body-queue`; не входить у власне тіло |
| Сегмент тіла | player | — | опора для себе й інших; рухається за головою |
| Фрукт | pickup | — | голова входить → зʼїдено, +1 сегмент; поки лежить — тверда опора |
| Земля | static | — | непрохідна, опора |
| Шипи | hazard | — | птах, що опинився опертим на шипи → смерть; блоки на шипах лежать безпечно (?) |
| Блок (кольорові фігури) | object | форма з кількох клітин | штовхається на 1 як ціле, підкоряється гравітації, падає у воду (зникає) |
| Портал-вихід | static | неактивний / активний | активний після останнього фрукта; голова входить → птах покидає рівень |
| Телепорт | terrain | пара | обʼєкт/птах, що потрапив на один, переноситься на другий із збереженням форми (?) |
| Вода / низ екрана | hazard | — | падіння за нижній край = смерть |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(head+dir)` і `not occupied(head+dir, own_body)` → ТО `move(head, dir)`, тіло `custom: «кожен сегмент на місце попереднього»`.
- КОЛИ `contact(head, fruit)` → ТО `pickup`, `grow(bird, 1)` (хвіст лишається на місці), `counter(fruit_left, -1)`.
- КОЛИ `contact(head, block|other_bird)` → ЯКЩО `custom: «увесь штовханий ланцюг може зсунутися на 1»` → ТО `push` (зокрема вгору — підняти); інакше `block`.
- Свого тіла птах штовхнути не може; птах може штовхати іншого птаха, а той — блок (ланцюг).
- КОЛИ `after(move)` → ЯКЩО `not supported(x)` для птаха/блока → ТО `fall(x)` на 1 і повторити, доки все не оперте.
- `supported(x)` = `custom: «хоч один сегмент/клітина x стоїть над землею, фруктом, блоком, іншим птахом або шипами»`; висіти на одному сегменті — законно.
- КОЛИ `fall` закінчилось → ЯКЩО `custom: «птах оперся на шипи»` → ТО `lose` + `undo` (гра сама відкочує хід).
- КОЛИ `edge(bird, bottom)` → ТО `lose` + `undo`; КОЛИ `edge(block, bottom)` → ТО `disappear_a`.
- КОЛИ `counter(fruit_left, ==, 0)` → ТО `set_state(exit, active)`.
- КОЛИ `contact(head, exit)` → ЯКЩО `state(exit, active)` → ТО `disappear_a` (птах вилітає з рівня).
- КОЛИ `enter(x, teleport)` → ЯКЩО `free(destination)` → ТО `teleport(x, pair)` (?).
- КОЛИ `all_gone(bird)` → ТО `win`, повернення на мапу, `unlock(neighbors)`.
- Поразка — лише тимчасова (автоматичний undo); рахунку нема.

## Керування і ввід
- Стрілки/WASD — крок голови активного птаха; клік мишею по птаху — зробити активним; клавіша-перемикач між птахами (?).
- Z — undo без ліміту; R — рестарт рівня (?); Esc — меню/мапа.
- Миша: клік по сусідній клітині — крок (TAS-нотатки описують «подвійний хід» мишею+клавіатурою як баг).
- Мобільні: свайп у напрямку, тап по птаху — вибір.

## Вікна, меню, HUD
- `splash-screen` — назва, птахи.
- `main-menu` — Play (продовжити) · Options · Exit (?).
- `map-window` — нелінійна мапа-острів: вузли рівнів, пройдені позначені; зони; 6 «star»-рівнів окремо, фінальний відкривається після них.
- `game-screen` — поле на весь екран; HUD майже порожній: кнопки undo/restart/меню (мобільні), активний птах підсвічений. Лічильника фруктів нема — їх видно на полі.
- `pause-menu` — повернутись, рестарт, на мапу, налаштування (?).
- `settings-window` — звук, музика, повноекранний режим (?).
- `end-screen` — короткий виліт птахів у портал → повернення на мапу.
- Переходи: main-menu → map-window → (вузол) game-screen → (усі вилетіли) map-window з відкритими сусідами.

## Фічі поза полем
- `undo` ∞, автоматичний undo після смерті — смерть не карає, лише повертає.
- `world-map` + `level-unlock`: пройдений рівень відкриває сусідні; star-рівні після всіх звичайних.
- `autosave` прогресу; `achievements` (Steam).
- Snakebird Primer — легший вхід (70 рівнів); Snakebird Complete (2023) — обидві гри разом.
- Редактора, підказок, рахунку в оригіналі нема (?).

## Варіації й родичі
- Snake (рух тіла) × Sokoban (штовхання) × платформер (гравітація) — три предки в одній механіці.
- Родичі: Snakebird Primer; Anhinga (дослідницький клон для вивчення розвʼязувачів); Sokobond (тіло з кількох клітин зчеплене); A Monster's Expedition (колоди 1×2 перекидаються й падають мостами).
- **Осі варіацій:** опора — «будь-який сегмент» (Snakebird) / «голова» / «увесь низ»; ріст — від фрукта / за часом / ніколи; гравітація — щоходу до упору / по 1 клітині за тік; смерть — автo-undo / рестарт / життя; кілька аватарів — по черзі (Snakebird) / синхронно (Parabox, Baba).

## Цікавинки для курсу
- Гравітація для багатоклітинного тіла: «падає, якщо жодна клітина не оперта» + падіння всіх обʼєктів до стабілізації — 🥈 (ітерація до нерухомої точки, порядок падіння).
- Ланцюгове штовхання різнорідних обʼєктів (птах → птах → блок) з перевіркою «весь ланцюг може зсунутись» — 🥈.
- Ріст від фрукта поверх `body-queue` — 📎.
- Кілька аватарів із перемиканням активного — 📎.
- Автоматичний undo після смерті замість «Game Over» — 🌱, але змінює відчуття гри.
- Розвʼязувач рівня (BFS по станам «позиції всіх птахів + блоків + фрукти») — 🥇; є дослідження Sturtevant (Anhinga).

## Мапа на каталог
- Є: `move-4dir` ↔ крок голови; `body-queue` ↔ тіло; `gravity-fall` ↔ падіння; `push-object` ↔ блоки й птахи; `multi-cell-size` ↔ блоки-фігури; `collect-quota` ↔ фрукти відкривають портал; `reach-exit` ↔ портал; `touch-death` ↔ шипи; `environment-death` ↔ падіння у воду; `teleport-pair` ↔ телепорти; `keyboard-controls` + `cell-click` + `swipe-gestures` ↔ ввід ПК/мобільний; `sequential-levels` + `level-unlock` + `save-progress` ↔ мапа; `movement-animation` ↔ анімації кроку й падіння.
- **Нема** → пропозиції карток:
  - `+undo-redo` «Undo ходів у грі» · game-logic/flow · 📎 · слот {depth: ∞}.
  - `+grow-on-eat` «Тіло росте від їжі» · entities/state · 📎 — для класичного Snake теж.
  - `+segment-support` «Опора будь-якою клітиною тіла» · entities/move · 🥈 · слот {support: any|head|bottom} — дитина `gravity-fall`.
  - `+multi-avatar-switch` «Кілька аватарів, перемикання активного» · interface/input · 📎.
  - `+auto-undo-on-death` «Смерть = відкат ходу» · game-logic/lose · 🌱.
  - `+exit-all-actors` «Рівень пройдено, коли всі аватари вийшли» · game-logic/win · 🌱.
  - `+world-map` «Мапа світу з вузлами-рівнями» · levels/progression · 🥉 — також у Baba Is You.

## Пропозиції до словників
- `+trigger:input` — крок голови; `+trigger:after(move)` — фаза гравітації після ходу.
- `+cond:supported(x)` — сутність має опору хоч однією клітиною (ключ до всієї гравітаційної сімʼї).
- `+effect:grow`, `+effect:fall`, `+effect:move` — кандидати, тут основні.
- `+effect:undo` — гра сама відкочує останній хід (реакція на смерть).
- `+role:terrain` (телепорт), `+role:hazard` (шипи, вода).
- `+window:map-window` — мапа світу з вузлами; `+feature:undo`, `+feature:world-map`.
- `+axis:actors` — `party` (2–3 птахи, по черзі); `+axis:undo` — `unlimited` + авто-undo на смерть.

## Джерела
- ⭐ [Wikipedia: Snakebird](https://en.wikipedia.org/wiki/Snakebird_(video_game)) — суть механіки, 53 рівні, Primer (70), Complete, дати й платформи.
- [Steam: Snakebird](https://store.steampowered.com/app/357300/Snakebird/) — три птахи, нелінійна мапа, зони, «pushing, lifting, teleporting».
- [Steam: Snakebird Primer](https://store.steampowered.com/app/1014140/Snakebird_Primer/).
- [Anhinga study (movingai.com)](https://www.movingai.com//snakebird/study/begin.html) — правила клону: фрукти обовʼязкові, на фрукті можна стояти, шипи → авто-undo.
- [TASVideos: Snakebird](https://tasvideos.org/Forum/Posts/534620) — гравітація після кожного ходу, ввід під час падіння заблоковано, star-рівні, death cancel.
- [Thinky Games: Snakebird](https://thinkygames.com/games/snakebird) — картка в базі thinky-ігор.
- YouTube: [пошук «snakebird gameplay»](https://www.youtube.com/results?search_query=snakebird+gameplay).

## Непевне
- (?) Рік: Steam/ПК — 2015 (Wikipedia, Steam); у брифі куратора 2016 — це мобільний реліз.
- (?) Телепорт: що саме спрацьовує (голова чи будь-який сегмент) і чи зберігається форма тіла — з памʼяті; Steam лише згадує «teleporting».
- (?) Шипи: смерть при спиранні на них після падіння (джерела), але чи вбиває крок голови в шип — не перевірено; чи безпечні шипи для блоків — з памʼяті.
- (?) Клавіші undo/restart/перемикання птахів і пункти меню — з памʼяті.
- (?) Чи можна голові ступити на клітину, яку щойно звільняє хвіст — не перевірено.
