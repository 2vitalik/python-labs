---
title: Bee Magic
slug: bee-magic
aka: []
family: thinky
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: collect
year: 2024
platforms: [web (HTML5), Windows]
links:
  - {kind: itch, url: "https://epicpikaguy.itch.io/bee-magic", best: true, note: "грати в браузері; «A game about moving around to cast spells»; коментарі з підказками (rot13)"}
  - {kind: other, url: "https://www.bontegames.com/2024/08/bee-magic-browser.html", note: "анонс Bart Bonte (серпень 2024) і коментарі гравців про трофеї"}
  - {kind: other, url: "https://epicpikaguy.itch.io/sea-magic", note: "сиквел Sea Magic: те саме чаклування рухом + оптимізація очок"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Bee+Magic+epicpikaguy", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-by-input, move-4dir, keyboard-controls, push-object, destructible-blocks, height-levels, button-toggle, collect-all, remaining-counter, undo-unlimited, restart-level, save-autosave, save-progress, controls-remap, game-settings, volume-control, cheat-codes, field-scaling, +move-sequence-spell, +spell-orb-learn, +shapeshift-form, +gate-climb, +challenge-modes, +used-set-tracker, +multiple-endings, +undo-redo]
proposes: ["+trigger:move_sequence", "+cond:spell_known", "+cond:form", "+effect:cast", "+effect:burn", "+effect:bloom", "+effect:toggle_gates", "+role:spell-orb", "+window:trophy-room", "+ui:spell-list", "+ui:used-spells-rose", "+feature:restricted-run-trophies", "+feature:diegetic-notes", "+card:move-sequence-spell", "+card:spell-orb-learn", "+card:shapeshift-form", "+card:gate-climb", "+card:used-set-tracker"]
author: opus
date: 2026-11-19
---

# Bee Magic — закляття твориться маршрутом: певна послідовність кроків сама спрацьовує як вогонь, ключ чи квітка

## Суть
Безкоштовна браузерна головоломка Ethan Clark (EPICPIKAGUY): уся гра — **одна мапа**, на якій треба зібрати всі зірки. Чаклунство тут — це рух: кожне закляття — коротка послідовність кроків (напр. Key = ←↑, Home = ↑→→↓), і щойно останні кроки гравця збігаються з візерунком вивченого закляття, воно спрацьовує саме — навіть коли гравець цього не хотів. Закляття вчаться, підбираючи кулі на мапі (частину візерунків — Goat, Bee, Fog — показують малюнки-записки); вони палять кущі, ламають стіни квітами, перемикають ворота, повертають додому, перетворюють на козу чи бджолу. Після перемоги відкривається кімната трофеїв: пройти гру знову, користуючись **лише** певним набором заклять.

## Поле і час
- Квадратна сітка, вид згори; рівень у даних гри — 27×27 клітин (файли `levels/0–5.txt`), камера показує частину, пробіл — зум.
- Дві висоти: земля й верх стін. На верх стін потрапляють «підйомом на воротах» (ворота зачиняються під гравцем), зійшовши з краю — падають донизу (з коментарів).
- Покроково: хід = крок на одну клітину (утримання — повтор зі швидкістю з налаштувань); світ змінюється лише від кроків і заклять.
- Туман — необовʼязковий шар: окремий візерунок його розвіює («if fog is present»).
- Праворуч від поля — панель: вивчені закляття з візерунками і «Remaining stars: N».

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець (людинка-бджілка) | player | форма: звичайна / коза / бджола; розмір: звичайний / маленький | крок 4 напрямки; кроки накопичуються в історії для розпізнавання заклять |
| Куля закляття (orb) | pickup | закляття: Fire, Key, Flower, Flip, Size, Bush, Home, Cancel… | підібрана — закляття вивчене, його візерунок зʼявляється в панелі |
| Зірка | pickup | — | зібрати всі = перемога; коза може її штовхати |
| Записка (note) | object | малюнок-підказка | Enter показує / ховає; коза штовхає |
| Камінь | object | — | непрохідний; штовхає лише коза; падає згори (?) |
| Кущ / живопліт | static | — | непрохідний; горить від Fire |
| Стіна (темно-зелена) | static | висота | непрохідна з землі; по верху можна ходити; квіти її ламають |
| Тріснута стіна | static | — | «можна зламати лише згори» |
| Ворота (хрест) | gate | відчинені / зачинені | перемикаються закляттям Key; квіти не дають їм зачинитися |
| Квіти | terrain | — | результат Flower; блокують зачинення воріт |
| Вогонь | hazard | — | лінія полумʼя від Fire; палить кущі |
| Перемикач | switch | — | раз перемкнутий — назавжди; бджола перемикати не може |
| Дім (центр мапи) | zone | значки використаних заклять | Home повертає сюди; центр показує, які закляття вжито в цьому забігу |
| Трофей | static | дозволений набір заклять | кімната трофеїв: трофей відкривається, якщо гру пройдено лише з його набором |
| Вода, пісок, порожнеча, фальшива порожнеча | terrain | — | ландшафт; фальшива порожнеча — секрет (?) |
| Фінішні плитки, «press return to see the ending» | zone | — | кінцівка; прихована кінцівка — пляж за тріснутою стіною |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(player, dir)`, `custom: «крок дописано в історію ходів»`; інакше `block`.
- КОЛИ `contact(player, orb)` → ТО `pickup`, `custom: «закляття вивчене; візерунок — у панелі»`.
- КОЛИ `custom: «останні кроки збіглися з візерунком вивченого закляття»` → ТО `custom: «закляття спрацьовує»`, `custom: «значок закляття в домі позначено використаним»`; «•» у візерунку — будь-який крок.
- Шлях із поверненням назад і прямий шлях — різні послідовності («these two paths are not the same»): важать кроки, а не намальована фігура.
- Візерунок треба фізично пройти: якщо фігура кроків не вміщається між стінами, закляття не скласти; є «звичайна» й «перевернута» форма (?).
- КОЛИ `custom: «спрацював Fire (→•↓↑•)»` → ТО `custom: «полумʼя лінією»`.
- КОЛИ `contact(fire, bush)` → ТО `disappear_b`.
- КОЛИ `custom: «спрацював Flower»` → ТО `set_cell(area, flowers)` — стіни в зоні візерунка ламаються («use flowers to break walls»).
- КОЛИ `custom: «спрацював Key (←↑)»` → ТО `set_state(gates, toggle)`.
- КОЛИ `custom: «ворота зачиняються під гравцем»` → ТО `custom: «гравець опиняється на верху стіни»`.
- КОЛИ `custom: «Key зачиняє ворота»` → ЯКЩО `cell(gate, flowers)` → ТО `block` — квіти не дають воротам зачинитися.
- КОЛИ `custom: «спрацював Home (↑→→↓)»` → ТО `teleport(player, home)`.
- КОЛИ `custom: «спрацював Goat (візерунок-«роги»)»` → ТО `transform(player, goat)`.
- КОЛИ `contact(goat, rock|note|star|orb)` → ЯКЩО `free(cell_behind)` → ТО `push`.
- КОЛИ `custom: «спрацював Bee (петля в квадраті 3×3)»` → ТО `transform(player, bee)`.
- КОЛИ `contact(bee, switch)` → ТО `block` («Bees can't flip switches»).
- КОЛИ `custom: «спрацював Size»` → ТО `custom: «гравець стає маленьким або великим»` — дістатися туди, куди звичайний не пролазить (?).
- КОЛИ `custom: «спрацював Bush»` → ТО `custom: «прохід крізь кущі й стіни»` (?) — розробник: проходження крізь стіни задумане.
- КОЛИ `custom: «спрацював Flip»` → ТО `custom: «перевертає (?)»` — гравці кажуть «right side up» і «inverted».
- КОЛИ `custom: «складено ↑↑↓↓←→←→↓↓↓»` → ЯКЩО `custom: «є туман»` → ТО `reveal(all)`.
- КОЛИ `contact(player, switch)` → ЯКЩО `not state(player, bee)` → ТО `set_state(switch, on)` — назавжди.
- КОЛИ `custom: «гравець на тріснутій стіні згори»` → ТО `disappear_b` (?).
- КОЛИ `contact(player, star)` → ТО `pickup`, `counter(remaining_stars, -1)`.
- КОЛИ `counter(remaining_stars, ==, 0)` → ТО `win`.
- КОЛИ `level_end` → ЯКЩО `custom: «використані закляття ⊆ набір трофея»` → ТО `unlock(trophy)` — кілька трофеїв за раз.
- КОЛИ `input(undo)` → ТО `undo(1)`.
- Перемога: усі зірки. · Поразка: нема — глухий кут знімає undo («Stuck? use Z to undo!»). · Рахунку нема; мета другого рівня — трофеї й прихована кінцівка.

## Керування і ввід
- Стрілки / WASD — крок; Enter — дія (показати / сховати записки, «see the ending»); Z — undo; пробіл — зум; Esc — пауза.
- Утримання руху й undo повторює дію (швидкість — у налаштуваннях); геймпад і тач (смартфон); усе перепризначається.
- Чаклування окремої кнопки не має: закляття — це сам маршрут.

## Вікна, меню, HUD
- `main-menu`: «Bee Magic, Version 1.4» — Play / Start Game, Settings, Credits, Quit (Windows).
- `custom-window` Play: Continue, New run («Unlocked trophies will be kept»), Reset all progress («Trophies won't be kept») + `confirm-dialog` з трьома «No» і одним «Yes».
- `game-screen`: мапа + права панель `spell-list` (назва закляття, стрілки візерунка, підсвічено вже пройдений префікс), `remaining-counter` «Remaining stars».
- Записки-малюнки (`help-window`-подібні): керування, «pro tip», трофеї, кінцівка.
- Кімната трофеїв (custom-window): трофеї з дозволеними наборами, warp туди.
- `pause-menu`: Resume, Restart, Settings, Main menu.
- `settings-window`: Audio, Video (fullscreen, pixel perfect, particles, text effect, big text, post processing), Gameplay (hold to move, hold to undo, autosave), Remap controls, Developer settings (gameplay fuzzer, «diagetic cheat code», view offscreen textures).
- `end-screen`: «congrats! you beat the game!», титри; прихована кінцівка — пляж.

## Фічі поза полем
- Одна мапа, «забіг» = проходження до всіх зірок; `autosave`, `continue`, New run зі збереженням трофеїв.
- Трофеї-обмеження: пройти гру лише з дозволеними закляттями (`custom-rules` у формі челенджу); центр мапи показує використані.
- `undo` без ліміту з повтором при утриманні; `restart-level`.
- `remap-controls`, `gamepad-support`, `touch-controls`, `font-scale` (big text), чіт-код у налаштуваннях розробника (заважає трофеям).
- Версія для coolmathgames.com; сиквел Sea Magic.

## Варіації й родичі
- Сиквел **Sea Magic** (той самий автор): кулі показують кроки сили праворуч, мета — очки й ранги (Dolphin від 5000), «бокси» як ресурс.
- Родичі в корпусі: [Baba Is You](baba-is-you.md) (правила, що спрацьовують від розташування), [5 Step Steve](5-step-steve.md) (той самий автор), [Starseed Pilgrim](starseed-pilgrim.md) (вивчення правил на одній мапі), [Islands of Insight](islands-of-insight.md), [Lightbot](../program-robots/lightbot.md) (послідовність команд як програма).
- Осі варіацій:
  - **як твориться закляття**: кнопкою / жестом / маршрутом кроків (тут);
  - **чи можна скласти випадково**: ні / так — маршрут сам спрацьовує (тут: «шлях змушує»);
  - **обмеження реіграбельності**: нема / трофеї «лише ці закляття».

## Цікавинки для курсу
- Розпізнавання закляття: буфер останніх кроків + збіг із візерунками з wildcard «•» — 📎.
- Візерунок має вміститися на мапі: перевірка, чи послідовність кроків фізично проходима, — 🥉.
- Ворота за Key і «підйом на воротах» на верх стіни (дві висоти) — 🥉.
- Форми гравця (коза штовхає камені, бджола не перемикає) як набір дозволених дій — 📎.
- Трофеї-обмеження: відстежити множину використаних заклять і відкрити всі трофеї, чий набір її покриває, — 🌱.
- Розвʼязувач «чи можна зібрати всі зірки лише з набором S» — 👑 (стан = позиція + історія кроків + мапа).

## Мапа на каталог
- Є: `move-by-input` · `move-4dir` · `keyboard-controls` · `push-object` (коза) · `destructible-blocks` (кущі, стіни) · `height-levels` (верх стін) · `button-toggle` (ворота за Key, перемикачі) · `collect-all` (зірки) · `remaining-counter` · `undo-unlimited` · `restart-level` · `save-autosave` · `save-progress` · `controls-remap` · `game-settings` · `volume-control` · `cheat-codes` · `field-scaling` (зум).
- **Нема** → пропозиції карток:
  - `+move-sequence-spell` «Закляття = послідовність кроків» · entities/state · 🥉 · слоти {pattern, wildcard: any}.
  - `+spell-orb-learn` «Куля вчить закляття» · entities/interact · 🌱.
  - `+shapeshift-form` «Форма гравця змінює дозволені дії» · entities/state · 📎 · слот {forms: goat|bee|tiny}.
  - `+gate-climb` «Ворота зачиняються під гравцем і піднімають його» · entities/move · 📎.
  - `+challenge-modes` (вже в корпусі) — тут трофеї «лише ці закляття».
  - `+used-set-tracker` «Табло використаних можливостей» · interface/hud · 🌱.
  - `+multiple-endings`, `+undo-redo` — вже в корпусі.

## Пропозиції до словників
- `+trigger:move_sequence` — останні кроки збіглися з візерунком.
- `+cond:spell_known` — закляття вивчене; `+cond:form` — форма гравця (коза, бджола, малий).
- `+effect:cast` — спрацювання закляття; `+effect:burn` — вогонь палить кущі; `+effect:bloom` — квіти на місці стін; `+effect:toggle_gates` — перемкнути всі ворота.
- `+role:spell-orb` — куля, що вчить (поки — `pickup`).
- `+window:trophy-room` — кімната трофеїв; `+ui:spell-list` — закляття з візерунками й підсвіченим префіксом; `+ui:used-spells-rose` — «троянда» використаних заклять у домі.
- `+feature:restricted-run-trophies` — трофеї за проходження з обмеженим набором; `+feature:diegetic-notes` — підказки-записки на самій мапі.
- `+card:move-sequence-spell`, `+card:spell-orb-learn`, `+card:shapeshift-form`, `+card:gate-climb`, `+card:used-set-tracker` — див. «Мапа на каталог».
- ⏳-слова, вжиті тут: `input`, `counter`, `level_end`, `free`, `cell`, `state`, `move`, `set_cell`, `set_state`, `reveal`, `unlock`, `undo`.

## Джерела
- ⭐ [itch.io: Bee Magic](https://epicpikaguy.itch.io/bee-magic) — гра в браузері, керування (стрілки, Enter, Z), «Made with SDL», версія 1.4; коментарі: трофеї як «лише ці закляття», коза штовхає записки / камені / зірки / кулі, Key і «gate climbs», Home, проходження крізь стіни задумане (розробник), прихована кінцівка, coolmathgames.
- [Збірка гри HTML5](https://html-classic.itch.zone/html/11722804/index.html) (`index.data`): прочитано файли меню й налаштувань, розмір мапи 27×27 і записки-малюнки — «symbolGuide» (Key, Fire, Flower, Flip, Size, Bush, дім у центрі), «use flowers to break walls», «Flowers prevent Gates from closing», «this can only be broken from above», «Once you flip a switch, it will stay flipped forever», «goat (can push rocks)», «fog» з візерунком, трофеї («you can ONLY use the spells depicted below the trophy»).
- Скриншоти itch — панель «Home ↑→→↓», «Fire →•↓↑•», «Key ←↑», «Remaining stars: 4», полумʼя лінією крізь кущі.
- [Bonte Games](https://www.bontegames.com/2024/08/bee-magic-browser.html) — «A game about moving around to cast spells», коментарі про трофеї й команду cancel.
- [Sea Magic](https://epicpikaguy.itch.io/sea-magic) — сиквел: кулі показують кроки сили, ранги очок.

## Непевне
- (?) Точні ефекти Flip, Bush, Size і кулі Cancel; що робить «Gravity» (є значок у ресурсах) — у записках гри не пояснено.
- (?) Форма зони Flower і лінії Fire відносно візерунка; чи перевернуті візерунки — окремі закляття.
- (?) Як саме ламається тріснута стіна «згори» і як падають камені.
- (?) Візерунки Goat і Bee відомі лише як малюнки; Tiny — окреме закляття чи режим Size.
- (?) Рік: анонс Bonte — серпень 2024; дата на itch не вказана.
