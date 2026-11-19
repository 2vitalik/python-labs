---
title: Stamp Collecting on Planet Q
slug: stamp-collecting-on-planet-q
aka: [Stamp Collector Game]
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
year: 2025
platforms: [web]
links:
  - {kind: itch, url: "https://cassowary.itch.io/stamp-collecting-on-planet-q", best: true, note: "грати в браузері; рука тягнеться й втягується стрілками, пробіл — хват за сині планки, X — авто-втягування; Ludum Dare 58"}
  - {kind: other, url: "https://ldjam.com/events/ludum-dare/58/stamp-collecting-on-planet-q", note: "LD58 Compo, тема «Collector»: опис, керування; Overall #7, Fun #5, Innovation #4 (дані з API ldjam)"}
  - {kind: other, url: "https://github.com/cassowarii/ld58", note: "сирці (zucchinibread.js): game.js — рука, хват, планки, марки, перемога; levels.js — 12 рівнів 14×11"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Stamp+Collecting+on+Planet+Q", note: "пошук; геймплей"}
stage: v1
coverage: 80
mechanics: [move-4dir, move-by-input, keyboard-controls, self-collision, path-cut, pull-object, push-object, impassable-cells, undo-redo, undo-unlimited, restart-level, sequential-levels, save-progress, main-menu, end-screen, movement-animation, sound-effects, background-music, +push-chain, +extending-arm, +grip-hold, +auto-retract, +untouchable-object, +pull-out-edge-goal, +exhibit-collectible, +idle-hint-overlay, +undoable-restart]
proposes: ["+trigger:input_hold", "+cond:straight", "+ui:idle-instructions", "+card:extending-arm", "+card:grip-hold", "+card:untouchable-object", "+card:pull-out-edge-goal"]
author: opus
date: 2026-11-19
---

# Stamp Collecting on Planet Q — рука-шлях тягнеться з-за краю поля, чіпляється за планки й витягує радіоактивну марку назовні

## Суть
Гра Ludum Dare 58 (Compo, 48 год, тема «Collector»), подана як «порт» гри з планети Q: марки там радіоактивні й торкатись їх не можна, тож «колекціонувати марки» — витягти марку з поля посередником. Гравець керує рукою, що вилазить з-за краю екрана: кожен крок подовжує руку на клітину, крок назад — втягує її власним слідом. Тримаючи пробіл, кисть хапається за синю планку й, втягуючись, тягне її, а планка штовхає марку та інші планки. Рівень пройдено, коли марку підтягнуто до краю, а пряма рука тримає планку біля краю — тоді рука витягує все за екран.

## Поле і час
- Поле 14×11 клітин (тайл 16 px, масштаб ×3); тайли: 4 види стін (тверді) і 4 види декору (прохідні); 12 рівнів, у кожному одна марка й 1–3 планки.
- Рука стартує поза полем: точка старту на краю, гра одразу виводить кисть на 2 клітини всередину; «тіло» — за екраном. За межу поля кисть виходить щонайбільше на 1 клітину.
- Рука — стек сегментів (клітина + напрям входу й виходу); вигин — сегмент, де напрям змінився.
- Хід = одна анімована дія (100 мс на клітину; невдалий рух — смикнулась і повернулась, удвічі повільніше); часу як загрози нема (`time: turn`).
- Якщо 5 с нічого не робити — проявляється картинка-інструкція (на 1-му рівні — завжди).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кисть | player | стан: відкрита / хват / «ой» | крок уперед подовжує руку, крок назад — втягує; на власну руку не заходить |
| Рука | object | шлях сегментів від краю | непрохідна для кисті, планок і марок |
| Синя планка | object | 2–4 клітини, горизонтальна або вертикальна | кисть стає на неї лише впоперек; з хватом тягнеться впоперек осі; штовхає планки й марки ланцюгом |
| Марка | object | 1 на рівень; своя картинка | рухається лише від планки; дотик кистю — відскок і втрата хвата |
| Стіна | static | 4 види | непрохідна для всього |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(hand, dir)`, `grow(arm, 1)` — для будь-якого напрямку, крім «назад» по останньому сегменту.
- КОЛИ `input(dir)` → ЯКЩО `occupied(next_cell, arm)` → ТО `block`, `animate(bounce)`.
- КОЛИ `input(dir)` → ЯКЩО `occupied(next_cell, stamp)` → ТО `block`, `clear_state(hand, grip)`, `sound(ouch)` — радіоактивну марку торкатись не можна.
- КОЛИ `input(dir)` → ЯКЩО `occupied(next_cell, bar)` → ТО `move(hand, dir)` лише впоперек планки й без хвата; уздовж осі або з хватом — `block`.
- КОЛИ `input(dir)` → ЯКЩО `occupied(hand_cell, bar)` → ТО `block` для кроку вперед: з планки кисть лише повертається.
- КОЛИ `input(back)` → ЯКЩО `custom: «у руці більше 2 сегментів»` → ТО `move(hand, back)`, `shrink(arm, 1)` — кисть іде назад своїм слідом.
- КОЛИ `input(hold_space)` → ТО `set_state(hand, grip)`; відпущено — `clear_state(hand, grip)`.
- КОЛИ `input(back)` → ЯКЩО `state(hand, grip)` and `occupied(hand_cell, bar)` and `custom: «рух упоперек планки, останній сегмент руки прямий»` → ТО `pull(bar)`, `move(hand, back)`, `shrink(arm, 1)`.
- КОЛИ `custom: «планка або марка їде в клітину з іншою планкою чи маркою»` → ЯКЩО `custom: «увесь ланцюг може зсунутись: на шляху нема стіни чи руки»` → ТО `push(next)` ланцюгом; інакше `block` і відскок.
- КОЛИ `input(hold_x)` → ЯКЩО `custom: «у руці більше 2 сегментів»` → ТО `clear_state(hand, grip)`, `custom: «рука сама втягується слідом удвічі швидше, поки X натиснуто»`.
- КОЛИ `turn_end(hand)` → ЯКЩО `custom: «марка на крайньому ряду поля, тримана планка біля краю, рука без жодного вигину»` → ТО `pull(bar)`, `custom: «рука витягує планку з маркою за екран»`, `win`.
- КОЛИ `input(undo)` → ТО `undo` (утримання — повтор кожні 80 мс).
- КОЛИ `input(reset)` → ТО `restart` (рестарт кладе точку undo).
- Перемога: марка за краєм поля. · Поразки нема: дотик до марки — лише відскок; глухий кут — undo/рестарт. · Рахунку нема; за кожен рівень — своя велика марка на екрані перемоги.

## Керування і ввід
- Стрілки — крок кисті: у новий бік — подовжити руку, стрілкою проти останнього сегмента — втягнути.
- Пробіл (тримати) — хват; X (тримати) — авто-втягування; з хватом авто-втягування нема навмисно: воно повертає руку, не «відмотуючи» undo кожен крок (відповідь автора).
- Z — undo (утримання — повтор); R — рестарт; M — звук. Меню — мишею.

## Вікна, меню, HUD
- `main-menu`: титул (назва + графіка, що погойдується), кнопки «New game» і «Continue» (неактивна, якщо збережено 1-й рівень).
- `game-screen`: поле й рука; номер рівня — у куті того ж краю (верх / низ), що й старт руки, але з протилежного боку; картинка-інструкція (рівень 1 — завжди, далі — після 5 с бездіяльності, з проявом).
- `end-screen` рівня: «Level complete» виїжджає збоку, велика марка рівня піднімається знизу, «Press space to continue».
- Фінальний екран «You win» після 12-го рівня; збереження скидається на 1-й.
- Переходи: main-menu → (затемнення) game-screen → (марку витягнуто) end-screen → пробіл → наступний рівень → … → «You win».

## Фічі поза полем
- `undo` без ліміту (стек станів: рука, кисть, планки, марки) і `restart-level`, який сам скасовний.
- `continue`: номер рівня в localStorage; New game / Continue.
- `onboarding-hints`: інструкція після 5 с простою.
- Колекція: 12 унікальних великих марок — нагорода за рівні; написи «мовою Q» (коментатори: літери майже читаються як англійські, числа — шістнадцяткові, автор підтвердив).
- `sound-toggle` (M); музика «In the garden», звуки хвата, відпускання, «ой», тягнення, втягування й перемоги.
- Теги доступності itch: color-blind friendly, high-contrast (дизайн, не налаштування).

## Варіації й родичі
- Родичі в корпусі: [WOIM](woim.md), [Can of Wormholes](can-of-wormholes.md), [Snakebird](snakebird.md) — тіло-шлях як перешкода, але тіло там рухається цілим; [Heroes of Sokoban](heroes-of-sokoban.md) — тягнення як окреме дієслово.
- **Осі варіацій**: тіло — рухається цілим (змійка) / росте від якоря й втягується слідом (Stamp Collecting) · взаємодія — штовхати / тягнути лише з хватом і впоперек · ціль — на мітку / за край поля · дотик до цілі — дозволено / заборонено, лише через посередника.

## Цікавинки для курсу
- Рука як стек сегментів: крок уперед — push, назад — pop, заборона перетину себе — 📎.
- Тягнення планки з перевіркою ланцюга «планка → планка / марка» (рекурсивна перевірка, потім рух) — 🥉.
- Хват як стан, що живе, поки тримаєш клавішу; тягнути лише впоперек і на прямому сегменті — 📎.
- Обʼєкт, якого не можна торкатись (відскок + втрата хвата) — 🌱.
- Перемога «витягти за край»: умова на марку, планку й прямоту руки + анімація виходу — 📎.
- Авто-втягування утриманням клавіші як «не-undo» — 🌱.
- Розвʼязувач BFS зі станом «шлях руки + хват + планки + марка» — 🥇 (тіло-шлях роздуває простір станів).

## Мапа на каталог
- Є: `move-4dir` · `move-by-input` · `keyboard-controls` ↔ стрілки; `self-collision` ↔ кисть не заходить на руку; `path-cut` ↔ крок назад стирає хвіст руки; `pull-object` ↔ тягнення планки; `push-object` ↔ планка штовхає марку; `impassable-cells` ↔ стіни; `undo-redo` · `undo-unlimited` · `restart-level`; `sequential-levels` · `save-progress` · `main-menu` ↔ New game / Continue; `end-screen` ↔ «Level complete»; `movement-animation` ↔ плавний рух кисті; `sound-effects` · `background-music`.
- **Нема** → пропозиції карток:
  - `+extending-arm` «Рука-шлях росте з якоря за краєм і втягується слідом» · entities/move · 🥉.
  - `+grip-hold` «Хват, поки тримаєш клавішу; тягнути лише впоперек» · entities/interact · 📎.
  - `+auto-retract` «Утримання — рука сама повертається слідом» · entities/move · 🌱.
  - `+untouchable-object` «Обʼєкт, якого не можна торкатись — лише штовхати посередником» · entities/legality · 🌱.
  - `+pull-out-edge-goal` «Перемога: витягти обʼєкт за край поля» · game-logic/win · 📎.
  - `+idle-hint-overlay` «Інструкція проявляється після N с бездіяльності» · interface/hud · 🌱.
  - Уже в корпусі: `+push-chain` (планки й марки штовхають одна одну), `+exhibit-collectible` (картинка марки за рівень), `+undoable-restart` (рестарт скасовний).

## Пропозиції до словників
- `+trigger:input_hold` — дія, поки клавішу тримають (хват, авто-втягування), на відміну від натискання.
- `+cond:straight` — шлях-тіло без вигинів (умова тягнення й перемоги).
- `+ui:idle-instructions` — підказка, що зʼявляється після бездіяльності.
- `+card:extending-arm`, `+card:grip-hold`, `+card:untouchable-object`, `+card:pull-out-edge-goal` — див. вище.

## Джерела
- ⭐ [itch.io: Stamp Collecting on Planet Q](https://cassowary.itch.io/stamp-collecting-on-planet-q) — опис-«порт», керування, теги, коментарі (втягування з хватом заборонене навмисно; числа шістнадцяткові).
- [Ludum Dare 58](https://ldjam.com/events/ludum-dare/58/stamp-collecting-on-planet-q) — сторінка — JS-застосунок; той самий опис і місця взято з `api.ldjam.com` (Compo, опубліковано 05.10.2025; Overall #7, Fun #5, Innovation #4, Audio #8, Graphics #15).
- [GitHub: cassowarii/ld58](https://github.com/cassowarii/ld58) — `game.js` (стани руки, `bar_can_move_direction`, `check_victory`, undo, збереження), `levels.js` (12 рівнів 14×11, планки, марки, старти), `levels/mapcompile.py`.
- YouTube: пошук «Stamp Collecting on Planet Q».

## Непевне
- (?) Умова перемоги в коді трохи несиметрична: планка має бути у двох крайніх рядах зліва/згори, але в одному — справа/знизу; як це відчувається в грі — не перевіряв.
- (?) Код підтримує кілька марок і планок будь-якої довжини, але в 12 рівнях — одна марка й планки по 2–4 клітини.
- (?) У коді є плавна зміна відтінку полотна (hue-rotate), де вона вмикається — не знайшов.
