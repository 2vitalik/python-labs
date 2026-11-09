---
title: Boulder Dash — DOS-клони (bd-fans)
slug: boulder-dash-dos-clones
aka: [Boulder Dash Professional, Terra Probe, Terra-Probe, Crystal Mine, RockRush, Gold Hunt, Boulder Dazz 256]
family: dig-gravity
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: both
  goal: collect
year: 1996
platforms: [DOS]
links:
  - {kind: other, url: "https://www.artsoft.org/rocksndiamonds/levels/martijnmooij/2010-03-16/www.bd-fans.com/FreewareMSDOS.html", best: true, note: "bd-fans: каталог freeware-клонів BD для DOS, по абзацу на гру — єдине джерело для чотирьох із шести"}
  - {kind: other, url: "https://www.artsoft.org/rocksndiamonds/levels/martijnmooij/2012-11-07/www.bd-fans.com/FreewareMSDOS.html", note: "той самий каталог, знімок 2012 — тексти збігаються"}
  - {kind: other, url: "https://homeoftheunderdogs.net/game.php?id=2539", note: "Terra Probe: рецензія HOTU, 1996, Derrick Dixon"}
  - {kind: other, url: "https://www.dosgamesarchive.com/download/terra-probe", note: "Terra Probe: опис, freeware, грати в браузері"}
  - {kind: other, url: "https://www.myabandonware.com/game/terra-probe-bxc", note: "Terra Probe: картка Dodgy Posse, 1999"}
  - {kind: other, url: "https://www.dosgamesarchive.com/download/rockrush", note: "RockRush: 30 рівнів, DIV Games Studio, Ctrl+стрілка"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Terra+Probe+DOS+gameplay", note: "пошук; геймплей Terra Probe"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=RockRush+Ian+Price+DOS+gameplay", note: "пошук; геймплей RockRush"}
stage: v1
coverage: 45
mechanics: [move-4dir, gravity-fall, dig-terrain, roll-off-rounded, push-object, collect-quota, reach-exit, environment-death, touch-death, chase-player, cell-transform, temporary-modes, blob-growth, in-game-editor, sequential-levels, keyboard-controls, +snap-action, +gravity-toggle, +permeable-cell, +no-walk-under-falling, +solvable-random-cave]
proposes: ["+card:no-walk-under-falling", "+card:solvable-random-cave", "+card:size-coding-clone"]
author: opus
date: 2026-11-09
---

# Boulder Dash — DOS-клони: шість маловідомих freeware-варіацій, кожна з одним новим правилом

## Суть
Зведений файл для шести DOS-клонів [Boulder Dash](boulder-dash.md) з каталогу bd-fans: про кожен відомо по 1–4 речення, на окремий файл матеріалу нема. База в усіх — ядро BD (копати землю, камені падають і скочуються, квота алмазів → вихід); цінність — у **дельті**: що саме кожен клон додав чи змінив. Разом вони — готова «таблиця модифікаторів» до BD-ядра для курсу: гравітація для аватара, перетворювач ворогів, тимчасова невидимість, заборона ступати під падаюче, генерація з гарантією розвʼязності.

| Клон | Рік | Автор | Що нового проти BD |
|---|---|---|---|
| Boulder Dash Professional | 1996 | невідомий | герой Willy; елементи BD **змішані з Supaplex**; **режим гравітації**; редактор рівнів |
| Terra Probe | 1996 / 1999 (?) | Derrick Dixon (Dodgy Posse) | гравець — **кулька-зонд**; **шипасті кулі переслідують**; **купол-зепер перетворює ворогів на алмази**; **приховані предмети** |
| Crystal Mine | 1994 (?) | Andreas Lange | бомби, **яйця з алмазами**, **болото**; бонуси **невразливості й невидимості** |
| RockRush | 2001 | Ian Price | точна копія C64-механіки, але **слиз і амеба в одній печері**; 30 рівнів; прихований редактор (F1+F11 на титулі); snap Ctrl+стрілка |
| Gold Hunt | 2007 | JALI Software | **не можна пройти під каменем, що падає**; **усі 10 рівнів генеруються** |
| Boulder Dazz 256 | 1999 | невідомий | гра в **256 байтах**; випадкова печера: 512 каменів і 100 самоцвітів, **гарантовано розвʼязна** |

## Поле і час
- Усі — прямокутна клітинна печера BD, один обʼєкт у клітині, real-time з дискретним тіком-сканом (успадковано; подробиці — [boulder-dash.md](boulder-dash.md)).
- Скрол чи один екран — для жодного клону джерела не кажуть (?).
- Генерація: Gold Hunt і Boulder Dazz 256 будують печеру на старті (випадковість setup); амеба/слиз RockRush дають випадковість під час гри (runtime) — звідси `random: both`.

## Сутності
Лише нове проти BD; базові камінь, алмаз, земля, стіна, вихід, вороги, амеба, слиз — у [boulder-dash.md](boulder-dash.md).

| Сутність | Клон | Роль | Параметри | Поведінка |
|---|---|---|---|---|
| Willy | BD Professional | player | падає в режимі гравітації | аватар; у gravity-режимі на нього діє падіння, як у Мерфі з [Supaplex](supaplex.md) |
| Елементи Supaplex | BD Professional | object | — | «мікс елементів BD і Supaplex»; які саме — невідомо (?) |
| Кулька-зонд | Terra Probe | player | — | котиться тунелями, копає, збирає алмази; камінь згори розчавлює |
| Шипаста куля | Terra Probe | enemy | «tenacious» | переслідує гравця по екрану |
| Конкурентні зонди | Terra Probe | enemy | — | «probes from rival mining companies» — ворожі зонди (?) |
| Купол-зепер | Terra Probe | switch | — | ворог, що в нього потрапив, стає алмазом |
| Прихований предмет | Terra Probe | pickup | невидимий | лежить прихованим, поки його не знайдуть (?) |
| Бомба | Crystal Mine | object | — | вибухає (механіка не описана) (?) |
| Яйце з алмазами | Crystal Mine | container | вміст: алмази | розбите — випускає алмази (?) |
| Болото | Crystal Mine | terrain | — | поведінка не описана (?) |
| Бонус невразливості | Crystal Mine | pickup | тривалість (?) | гравець тимчасово не гине |
| Бонус невидимості | Crystal Mine | pickup | тривалість (?) | гравець тимчасово невидимий для ворогів (?) |
| Слиз + амеба | RockRush | terrain / hazard | обидва в одній печері | кожен поводиться як у BD; новизна — лише поєднання |
| Падаючий камінь | Gold Hunt | object | стан falling | клітина під ним для гравця непрохідна |
| Генератор печери | Gold Hunt, Dazz 256 | — | Dazz: 512 каменів, 100 самоцвітів | будує рівень на старті; Dazz гарантує розвʼязність |

## Правила (КОЛИ → ЯКЩО → ТО)
Базові правила BD (падіння, скочування, вибухи 3×3, амеба, слиз) — у [boulder-dash.md](boulder-dash.md); тут лише дельти.
- BD Professional: КОЛИ `tick` → ЯКЩО `mode(gravity)` and `free(below willy)` → ТО `fall(willy)`.
- BD Professional: КОЛИ `input(dir)` → ЯКЩО `mode(gravity)` and `custom: «dir = вгору і нема опори для підйому»` → ТО `block` (?).
- Terra Probe: КОЛИ `tick` → ТО `move(spiky_ball, toward player)` (`custom: «переслідує гравця»`).
- Terra Probe: КОЛИ `contact(spiky_ball, probe)` → ТО `lose` (?).
- Terra Probe: КОЛИ `contact(enemy, zapper_dome)` → ТО `transform(diamond)`.
- Terra Probe: КОЛИ `enter(probe, hidden_item_cell)` → ТО `reveal(hidden_item)`, `pickup` (?).
- Terra Probe: КОЛИ `counter(diamonds, ==, quota)` → ТО `next_level` (за описом MyAbandonware «діаманти відкривають наступний рівень»).
- Crystal Mine: КОЛИ `custom: «яйце розбито (камінь / вибух)»` → ТО `spawn(diamond)` (?).
- Crystal Mine: КОЛИ `contact(player, invulnerability)` → ТО `pickup`, `set_state(player, invulnerable, duration)`.
- Crystal Mine: КОЛИ `contact(falling boulder|enemy, player)` → ЯКЩО `state(player, invulnerable)` → ТО `block`; інакше `lose`.
- Crystal Mine: КОЛИ `contact(player, invisibility)` → ТО `pickup`, `set_state(player, invisible, duration)`; ЯКЩО `state(player, invisible)` → вороги `custom: «не бачать гравця»` (?).
- RockRush: КОЛИ `level_start` → ЯКЩО `count(amoeba, >, 0)` and `count(slime, >, 0)` → ТО обидва діють за правилами BD (у C64-версії — або одне, або інше).
- RockRush: КОЛИ `input(ctrl+dir)` → ТО `custom: «snap: прибрати землю / взяти алмаз у сусідній клітині, не рухаючись»`.
- Gold Hunt: КОЛИ `input(dir)` → ЯКЩО `custom: «над цільовою клітиною камінь у стані falling»` → ТО `block`.
- Gold Hunt / Dazz 256: КОЛИ `level_start` → ТО `custom: «згенерувати печеру»`; Dazz: `spawn_at(boulder ×512, rng)`, `spawn_at(gem ×100, rng)` з перевіркою розвʼязності (`custom`).
- Перемога (усі): квота алмазів/самоцвітів → вихід (успадковано від BD). Поразка: камінь згори, ворог, вибух → −1 життя. Рахунок — як у BD (?).

## Керування і ввід
- Клавіатура, стрілки — 4 напрямки (усі).
- RockRush: Ctrl + стрілка — копати / брати алмаз у напрямку без руху (snap, як fire+напрямок у C64-оригіналі).
- RockRush: F1 і F11 на титульному екрані — вхід у прихований редактор.

## Вікна, меню, HUD
- `main-menu` / титульний екран — старт; у RockRush з нього ж прихований вхід в `editor-window`.
- `editor-window` — BD Professional (входить у комплект), RockRush (F1+F11).
- `game-screen` — печера; HUD як у BD: алмази/квота, час, життя, очки (?) — джерела HUD не описують.
- `end-screen` — game over (?).

## Фічі поза полем
- `level-editor`: BD Professional, RockRush.
- `levels-sequential`: RockRush — 30 рівнів; Gold Hunt — 10 згенерованих.
- Генерація рівнів: Gold Hunt (10 рівнів), Boulder Dazz 256 (кожен рівень випадковий, гарантовано розвʼязний).
- Розмір як обмеження: Boulder Dazz 256 — уся гра 256 байт; «можливі глюки» за словами каталогу.
- RockRush написаний у DIV Games Studio.

## Варіації й родичі
- Корінь — [Boulder Dash](boulder-dash.md); BD Professional бере з [Supaplex](supaplex.md) (там гравітація — властивість рівня й порти-перемикачі).
- Тимчасові бонуси захисту — як у [Crystal Mines II](crystal-mines-ii.md) (невидимість, захисти); яйця — як у [Dot Valley](dot-valley.md) і [Repton](repton.md), але тут з алмазами, а не з монстром.
- Перетворення ворога на алмази — родич метелика BD (вибух → 9 алмазів) і клітин-перетворювачів [Emerald Mine](emerald-mine.md), але без вибуху.
- Великі клони того ж каталогу — [Rocks'n'Diamonds](rocks-n-diamonds.md), [Emerald Mine](emerald-mine.md), [Dot Valley](dot-valley.md), [Earth Shaker](earth-shaker.md).
- **Осі варіацій**: гравітація — «лише обʼєкти (BD) / і аватар у режимі (BD Professional, Supaplex)»; безпека під каменем — «можна підставитись (BD) / рух під падаюче заборонено (Gold Hunt) / тимчасова невразливість (Crystal Mine)»; рівні — «ручні (BD) / генеровані (Gold Hunt) / генеровані з гарантією (Dazz 256)»; вороги → алмази — «через вибух (BD) / через клітину-зепер (Terra Probe)».

## Цікавинки для курсу
- Заборона ступати під падаючий камінь — одна умова в легальності ходу міняє стиль гри — 🌱.
- Купол-зепер: клітина, що перетворює ворога в алмаз, — ворог стає ресурсом — 📎.
- Невразливість / невидимість як тимчасовий стан, що вимикає правило смерті чи погоню — 📎.
- Режим гравітації для аватара поверх BD-фізики — 🥉: та сама `fall` на гравця, підйом лише через копання.
- Слиз + амеба разом: дві «клітинні» системи в одному скані — 📎.
- Генерація печери з гарантією розвʼязності (512 каменів, 100 самоцвітів) — 🥇: перевірка досяжності з урахуванням падінь — нетривіальна.
- «BD у 256 байтах» — 🥈 як вправа на мінімальне ядро правил (size-coding).

## Мапа на каталог
- Є: `move-4dir` · `gravity-fall` · `dig-terrain` · `roll-off-rounded` · `push-object` · `collect-quota` · `reach-exit` · `environment-death` · `touch-death` · `chase-player` ↔ шипасті кулі Terra Probe · `cell-transform` ↔ купол-зепер · `temporary-modes` ↔ невразливість/невидимість Crystal Mine · `blob-growth` ↔ амеба RockRush · `in-game-editor` ↔ BD Professional, RockRush · `sequential-levels` · `keyboard-controls`.
- Уже запропоновані корпусом: `+snap-action` (RockRush Ctrl+стрілка), `+gravity-toggle` (BD Professional), `+permeable-cell` (слиз RockRush).
- **Нема** → пропозиції карток:
  - `+no-walk-under-falling` «Не ступити під падаюче» · entities/legality · 🌱 — хід у клітину під падаючим обʼєктом блокується (Gold Hunt).
  - `+solvable-random-cave` «Випадкова печера з гарантією розвʼязності» · levels/generation · 🥇 · слоти {rocks, gems} — генерація + перевірка, що квоту можна зібрати (Boulder Dazz 256).
  - `+size-coding-clone` «Гра в N байтах» · code · 🥈 · слот {bytes} — мінімальне ядро правил (Boulder Dazz 256).

## Пропозиції до словників
- `+card:no-walk-under-falling` — легальність ходу залежить від стану обʼєкта над ціллю (Gold Hunt).
- `+card:solvable-random-cave` — генерація фізичної печери з перевіркою розвʼязності (Boulder Dazz 256).
- `+card:size-coding-clone` — гра як вправа на мінімальний розмір коду (Boulder Dazz 256).

## Джерела
- ⭐ [bd-fans: Freeware Boulder Dash Clones — MS DOS](https://www.artsoft.org/rocksndiamonds/levels/martijnmooij/2010-03-16/www.bd-fans.com/FreewareMSDOS.html) — абзаци про всі шість: Willy і gravity mode, шипасті кулі й зепери, яйця/болото/невидимість, slime AND amoeba, F1+F11, «cannot walk under falling boulders», 512 rocks / 100 gems / guaranteed solvable.
- [bd-fans, знімок 2012](https://www.artsoft.org/rocksndiamonds/levels/martijnmooij/2012-11-07/www.bd-fans.com/FreewareMSDOS.html) — ті самі тексти (звірено).
- [Home of the Underdogs: Terra Probe](https://homeoftheunderdogs.net/game.php?id=2539) — 1996, Derrick Dixon, кулька замість Рокфорда, шипасті кулі переслідують, приховані предмети; «one of the better» клонів.
- [DOS Games Archive: Terra Probe](https://www.dosgamesarchive.com/download/terra-probe) — 1999, Dod-G Pos-E, зонд-копач, «probes from rival mining companies», freeware.
- [MyAbandonware: Terra Probe](https://www.myabandonware.com/game/terra-probe-bxc) — Dodgy Posse, 1999; діаманти відкривають наступний рівень; камінь розчавлює.
- [DOS Games Archive: RockRush](https://www.dosgamesarchive.com/download/rockrush) — 2001, Ian Price, DIV Games Studio, 30 рівнів, Ctrl+стрілка = snap, «apparently» прихований редактор.

## Непевне
- (?) Terra Probe: рік 1996 (bd-fans, HOTU) проти 1999 (DGA, MyAbandonware) — можливо, різні версії; автор Derrick Dixon під лейблом Dodgy Posse.
- (?) Terra Probe: як працюють приховані предмети (під землею? видно після копання?) і чи «rival probes» — окремий тип ворога чи ті самі кулі.
- (?) Crystal Mine: рік 1994 — лише зі сніпета пошуку, сторінку не відкрив; поведінка бомб, яєць і болота не описана ніде.
- (?) Crystal Mine: що саме дає невидимість (вороги не переслідують? проходять крізь?).
- (?) BD Professional: які елементи Supaplex (порти? дискети? інфотрони?) і як вмикається gravity mode (на весь рівень чи клітиною); файла на bd-fans не викладено.
- (?) Gold Hunt: чи «falling» означає лише камінь у русі, чи й той, що висить над порожнечею; як генеруються рівні.
- (?) Boulder Dazz 256: як забезпечено розвʼязність у 256 байтах (конструктивно, напр. шлях прокладається першим?) — джерело не пояснює.
- (?) Домашня сторінка RockRush (iprice.remakes.org) не відкрилась; архівний README Terra Probe (archived.software) — прострочений сертифікат, не прочитано.
- Boulder Dash 2000 (Magnetiq) з того ж каталогу — опису нема взагалі, тому не включено.
