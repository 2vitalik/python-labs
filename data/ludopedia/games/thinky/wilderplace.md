---
title: Wilderplace
slug: wilderplace
aka: []
family: thinky
also: []
klass: avatar
axes:
  field: iso
  time: turn
  opponent: ai
  info: full
  random: none
  goal: state
year: 2022
platforms: [PC (Windows/macOS/Linux), Steam Deck]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1769640/Wilderplace/", best: true, note: "опис, трейлер, 8 скриншотів (ізометрична сітка, HUD зі статистикою гаю)"}
  - {kind: official, url: "https://wilderplace.place/", note: "сайт гри: бестіарій — духи, лісоруби, роботи, демони, автомати, жаболюди"}
  - {kind: other, url: "https://wilderplace.place/presskit", note: "прескіт: історія розробки, факти, відео"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=xYu0WtqaIzY", note: "«5 minutes with Wilderplace Beta 2» — геймплей (з прескіту)"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=TzveRYP1tUA", note: "трейлер (з прескіту)"}
  - {kind: other, url: "https://indiegamereviewer.com/?p=50335", note: "огляд: три ходи з духом у руках, дух у рослині стає деревом, лісоруби, click-and-drag"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=1769640&count=30&maxlength=0", note: "патчноути: гай зачищено лише з відкритим монументом, швидке переміщення"}
stage: v1
coverage: 45
mechanics: [move-by-input, cell-click, keyboard-controls, push-object, cell-transform, world-map, restart-level, undo-step, sound-effects, background-music, +carry-object, +death-countdown, +spirit-parasite, +npc-own-goals, +world-shift-layer, +tool-gated-cell, +solved-level-freeze, +fast-travel-points, +multiple-endings, +placate-or-banish]
proposes: ["+trigger:carry_expired", "+cond:carrying", "+effect:possess", "+effect:rehome", "+role:vessel", "+ui:carry-counter", "+ui:grove-stats", "+feature:undo-as-unlock", "+feature:level-freeze-on-solve", "+card:spirit-parasite", "+card:world-shift-layer", "+card:solved-level-freeze", "+card:npc-own-goals", "+card:placate-or-banish"]
author: opus
date: 2026-11-19
---

# Wilderplace — шаман на ізометричній сітці переселяє неслухняних духів, доки ті не перетворили його на дерево

## Суть
Покрокова просторова головоломка-пригода (Saman Bemel-Benrud, Micah Fitch, Tom Lubanovic): шаман відновлює рівновагу Божественного саду. Духи — паразити: шукають найближчу істоту й роблять її своєю домівкою; шаман бере духа й має лише кілька ходів, щоб оселити його в рослину чи посудину, інакше сам стане деревом. Поруч живуть «непрохані гості» з власними цілями — лісоруби рубають дерева й випускають духів, роботи добувають руду, демони світу снів виривають посудини. Гра «про допомогу, а не про бій»; рівні-гаї звʼязані в розгалужену мапу в дусі метроїдванії, інструменти відкривають нові способи пройти старі місця.

## Поле і час
- Ізометрична «ромбова» сітка невеликих гаїв (на скриншотах — 5×5…7×7 клітин (?)); теги Steam: Isometric, 2.5D, Grid-Based Movement.
- Покроково: кожен хід шамана — і NPC роблять свій хід за власними цілями.
- Два шари світу: звичайний (світле тло) і світ снів (темне тло, «dark world»), куди шаман може переходити; там чатують демони.
- Розвʼязаний гай застигає в кінцевому стані; гай вважається зачищеним, лише коли відкрито його монумент (якщо він є).
- Мапа: 150+ повʼязаних гаїв, розгалужена, з монументами швидкого переміщення.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Шаман | player | посох; несе духа або ні; інвентар артефактів | ходить сіткою; бере й кладе духів; викликає посудини (?) |
| Дух | enemy | вид (рослинний, деревний, грибний…) | «шукає найближчу істоту й перетворює її на нову домівку, як паразит» |
| Посудина | container | — | дім для духа, викликаний шаманом; демони її виривають |
| Рослина / дерево | terrain | — | у рослину можна оселити духа; оселений дух стає деревом, що займає клітину |
| Лісоруб (woodsman) | enemy | — | ходить сам, рубає дерева, змінює мапу; зрубане дерево випускає духа |
| Гірничий робот | enemy | — | добуває руду, «рослини й гриби не чіпає» |
| Охоронний робот | enemy | — | захищає майно «будь-якими засобами»; небезпечний (?) |
| Збирачі (foragers) | neutral | — | збирають гриби й лікують хворих істот; що стається з духами після лікування — загадка |
| Жаболюди (toadmen) | neutral | — | тубільці саду, дружні, часом шкодять |
| Автомати | neutral | — | «не мають свідомості, але вміють штовхати речі» |
| Демони | enemy | лише у світі снів | «виривають посудини й переселяють духів до найближчої істоти» |
| Варден (The Warden) | neutral | — | підтримує порядок і проганяє непроханих (сюжетний) |
| Дикі тварини | neutral | одержима / вільна | духи вселяються в тварин; шаман їх визволяє |
| Скелі, камені | static | — | непрохідні; камінь може перекрити шлях назад |
| Монумент | static | прихований / відкритий | відкритий — гай зачищено; деякі вмикають швидке переміщення |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, cell)` → ЯКЩО `free(cell)` → ТО `move(shaman, dir)`; інакше `block`.
- КОЛИ `input(pick, spirit)` → ЯКЩО `in_range(shaman, spirit, 1)` (?) → ТО `carry`, `set_state(shaman, carrying, 3)`.
- КОЛИ `turn_end(shaman)` → ЯКЩО `state(shaman, carrying)` → ТО `counter(carry_moves, -1)`.
- КОЛИ `counter(carry_moves, ==, 0)` → ЯКЩО `state(shaman, carrying)` → ТО `transform(shaman, tree)`, `lose` — «залишиш духа надовго — він візьме гору».
- КОЛИ `input(place, cell)` → ЯКЩО `cell(target, plant)` or `cell(target, vessel)` → ТО `custom: «дух оселяється»`, `transform(target, tree)` — дерево займає клітину; `clear_state(shaman, carrying)`.
- КОЛИ `turn_end(shaman)` → ТО вільний дух `custom: «рухається до найближчої істоти й перетворює її на домівку»`.
- КОЛИ `turn_end(shaman)` → ТО лісоруб `custom: «іде до дерева»`.
- КОЛИ `custom: «лісоруб рубає дерево»` → ТО `disappear_b`, `spawn_at(spirit, cell)` — дух на волі.
- КОЛИ `turn_end(shaman)` → ТО автомат `push` речі на своєму шляху (?); гірничий робот `custom: «добуває руду»`.
- КОЛИ `input(shift_world)` → ТО `set_state(world, dream)`.
- КОЛИ `turn_end(shaman)` → ЯКЩО `state(world, dream)` → ТО демон `custom: «вириває посудину й переселяє духа до найближчої істоти»`.
- КОЛИ `custom: «монумент гаю відкрито»` → ТО гай зачищено й застигає; монумент на краю Dreamer's Grounds відкриває швидке переміщення.
- КОЛИ `leave(shaman, grove)` → ЯКЩО `custom: «монумент гаю не відкрито»` → ТО стан гаю не зберігається: наступний запуск — з початку гаю.
- КОЛИ `input(restart)` → ТО `restart` — гай з моменту входу, шамана переставлено в безпечне місце.
- КОЛИ `input(undo)` → ЯКЩО `has(shaman, undo_skill)` → ТО `undo(1)` — undo відкривається як уміння пізніше.
- Перемога: гай у рівновазі (духи переселені / вигнані), монумент відкрито. · Поразка: шаман став деревом (?). · Рахунку нема; статистика гаю: ходи, спроби, ходи до зачистки, духів умиротворено / вигнано.

## Керування і ввід
- Миша / тач: click-and-drag — рух і перенесення духа; довше утримання кнопки перед перетягуванням — рух без розміщення духа.
- Клавіатура й геймпад (повна підтримка, Steam Deck).
- Кнопки в куті: рестарт, undo, ще одна дія (?); меню праворуч; іконки артефактів унизу ліворуч.

## Вікна, меню, HUD
- `game-screen`: ізометричний гай; ліворуч угорі — `restart-button`, `undo-button`; праворуч — меню; унизу ліворуч — значки артефактів (`inventory-bar`).
- `dialogue-window`: репліки NPC з іменами (Yunker, Forager Lada) поверх поля.
- `custom-window` — підсумок гаю: «Balanced», назва, Moves, Retries, Moves to clear, Spirits placated, Spirits banished.
- `map-window` — розгалужена мапа гаїв (?), монументи швидкого переміщення.
- `pause-menu` / `settings-window` — (?).
- Переходи: гай → (вихід краєм) сусідній гай; монумент → швидке переміщення.

## Фічі поза полем
- `world-map` у стилі метроїдванії: інструменти й «movement options» з інвентаря відкривають нові проходи старими гаями.
- Розвʼязані гаї застигають; `restart-level` гаю; `undo` — уміння, що відкривається по ходу гри.
- Моральний вибір: духів можна умиротворити чи вигнати; теги Steam — Multiple Endings.
- `cloud-save`, `gamepad-support`, `touch-controls`, 10–15 годин, 2000+ олівцевих малюнків.

## Варіації й родичі
- Родичі в корпусі: [Sokoban](../push-slide/sokoban.md) (огляди порівнюють), [A Monster's Expedition](a-monsters-expedition.md) (мапа повʼязаних островів), [Snakebird](snakebird.md), [Into the Breach](../tactics/into-the-breach.md) (NPC з відомими намірами), [DROD](drod.md) (істоти зі своїми правилами).
- Осі варіацій:
  - **що несе аватар**: нічого / обʼєкт без ліміту / ношу з таймером, після якого аватар гине (тут);
  - **противники**: вороги, що полюють на гравця / NPC зі своїми цілями, які змінюють мапу (тут);
  - **шари світу**: один / два перемикані (світ снів зі своїми істотами);
  - **доля розвʼязаного рівня**: скидається / застигає (тут).

## Цікавинки для курсу
- Ноша з таймером на 3 ходи: стан «несе» + лічильник + перетворення аватара в перешкоду — 📎.
- Дух-паразит: щотіку йде до найближчої істоти й заміняє її деревом — 🥉 (пошук найближчої цілі + перетворення).
- NPC з власними цілями (лісоруб рубає дерево → дух на волі) — ланцюг взаємодій — 🥈.
- Світ снів як другий шар зі своїми сутностями (демони) — 🥉.
- Застигання розвʼязаного рівня й монумент як умова зачистки — 🌱.
- Статистика гаю (ходи, спроби, умиротворено / вигнано) — 🌱.

## Мапа на каталог
- Є: `move-by-input` · `cell-click` (click-and-drag) · `keyboard-controls` · `push-object` (автомати) · `cell-transform` (дух → дерево) · `world-map` · `restart-level` · `undo-step` · `sound-effects` · `background-music`.
- **Нема** → пропозиції карток:
  - `+carry-object` (вже в корпусі) — дух у руках шамана.
  - `+death-countdown` (вже в корпусі) — слоти {turns: 3, leaves: tree}.
  - `+spirit-parasite` «Дух робить найближчу істоту домівкою» · entities/move · 🥉.
  - `+npc-own-goals` «NPC зі своєю метою змінює мапу» · entities/move · 🥈.
  - `+world-shift-layer` «Перемикання на світ-двійник» · levels/progression · 🥉.
  - `+tool-gated-cell` (вже в корпусі) — нові інструменти відкривають проходи.
  - `+solved-level-freeze` «Розвʼязаний рівень застигає» · levels/progression · 🌱.
  - `+fast-travel-points`, `+multiple-endings` — вже в корпусі.
  - `+placate-or-banish` «Два способи впоратися з ворогом з різними наслідками» · game-logic/win · 📎.

## Пропозиції до словників
- `+trigger:carry_expired` — скінчився час ноші; `+cond:carrying` — аватар несе сутність.
- `+effect:possess` — дух вселяється в істоту; `+effect:rehome` — переселення духа в посудину.
- `+role:vessel` — посудина для духа (поки — `container`).
- `+ui:carry-counter` — ходи, що лишились із ношею (серця над шаманом (?)); `+ui:grove-stats` — підсумок гаю.
- `+feature:undo-as-unlock` — undo як уміння, яке треба знайти; `+feature:level-freeze-on-solve`.
- `+card:spirit-parasite`, `+card:world-shift-layer`, `+card:solved-level-freeze`, `+card:npc-own-goals`, `+card:placate-or-banish` — див. «Мапа на каталог».
- ⏳-слова, вжиті тут: `input`, `turn_end`, `counter`, `leave`, `adjacent`, `free`, `state`, `cell`, `has`, `move`, `carry`, `set_state`, `clear_state`, `transform`, `spawn_at`, `undo`, `restart`.

## Джерела
- ⭐ [Steam: Wilderplace](https://store.steampowered.com/app/1769640/Wilderplace/) — опис («wrangle restless spirits and evade dangerous intruders», «levels… become frozen in place», «start… with nothing but your trusty staff»), 150+ гаїв, керування, скриншоти HUD і світу снів.
- [Офіційний сайт](https://wilderplace.place/) — бестіарій дослівно: духи-паразити, посудини, лісоруби, роботи, збирачі, жаболюди, автомати, демони, Варден.
- [Indie Game Reviewer](https://indiegamereviewer.com/?p=50335) — «three moves» з духом, дух у рослині → дерево, стати деревом = програти рівень, лісоруби, click-and-drag.
- [Прескіт](https://wilderplace.place/presskit) — історія (з 2019), відео [геймплей](https://www.youtube.com/watch?v=xYu0WtqaIzY) і [трейлер](https://www.youtube.com/watch?v=TzveRYP1tUA).
- [Steam News API](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=1769640&count=30&maxlength=0) — монумент як умова зачистки гаю, незбережений гай, швидке переміщення з 1.1.0.
- Steam-форум — undo як уміння, яке відкривається пізніше; рестарт ставить у безпечне місце; скидання до стану при останньому вході.

## Непевне
- (?) Точний перелік артефактів і «способів руху» (час, простір, середовище), що робить персонаж Sabi; що за третя кнопка біля undo.
- (?) Чи брати духа можна лише з сусідньої клітини; чи посудину викликає шаман будь-де.
- (?) Що роблять охоронні роботи шаманові (поразка?) і як збирачі «лікують» одержимих.
- (?) Як рахуються «умиротворені» та «вигнані» духи й як це впливає на кінцівки.
- (?) Серця над шаманом на скриншоті — лічильник ходів із духом (висновок із картинки).
