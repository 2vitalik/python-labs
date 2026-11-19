---
title: Pup Champs
slug: pup-champs
aka: []
family: thinky
also: [tactics]
klass: figure
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2025
platforms: [PC (Windows/macOS), Steam Deck, Android, iOS]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2848800/Pup_Champs/", best: true, note: "опис і трейлер: розстановка, лінії пасу, бруд, мавпи, кролики; 170+ пазлів; є демо"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=2848800&count=30&maxlength=0", note: "патчноути демо й релізу: удари цуценят, кроти, бруд, мавпи, undo по клітині, підказки"}
  - {kind: itch, url: "https://afterburn.itch.io/pup-champs", note: "Windows/macOS/Android; у коментарях — розкладка клавіш"}
  - {kind: other, url: "https://www.pocketgamer.com/pup-champs/review/", note: "огляд: обмежені ходи кожного цуценяти, удар по прямій і через клітину, кріт, кущ, суперники"}
  - {kind: other, url: "https://indiegamesplus.com/pup-champs-review/", note: "огляд: три удари (2 клітини дугою, 4 клітини дугою, по прямій), кроти в норах, листя"}
  - {kind: other, url: "https://www.pocketgamer.com/pup-champs/app-army-assemble/", note: "враження гравців: «кроки» на собаку, кроти перехоплюють паси"}
  - {kind: other, url: "https://steamcommunity.com/app/2848800/discussions/0/596280900527862796/", note: "«The Golden needs a target to kick to — either another doggo or the goal»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Pup+Champs+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-by-input, path-drawing, keyboard-controls, party-switch, move-limit, piece-move-patterns, inertia-slide, impassable-cells, undo-unlimited, restart-level, level-select, level-unlock, world-map, achievements-window, save-progress, game-settings, sound-effects, background-music, +ball-pass, +kick-patterns, +pass-needs-receiver, +ball-trap-tile, +mimic-copy, +switching-blocker, +hint-solution-steps]
proposes: ["+trigger:kicked", "+trigger:ball_stopped", "+cond:has_ball", "+cond:receiver_on_path", "+effect:kick", "+effect:lob", "+role:ball", "+ui:unit-cards", "+ui:kick-trajectory", "+feature:hint-solution-steps", "+feature:auto-switch-after-pass", "+card:kick-patterns", "+card:pass-needs-receiver", "+card:ball-trap-tile", "+card:switching-blocker"]
author: opus
date: 2026-11-19
---

# Pup Champs — тренуєш цуценят-футболістів: розстав, віддай пас і заведи мʼяч у ворота за обмежену кількість кроків

## Суть
Покрокова головоломка від Afterburn (автори Railbound та inbento): гравець — тренер, який водить команду цуценят полем-сіткою і має закотити мʼяч у ворота. Кожне цуценя має обмежений запас кроків на рівень і **власний удар**: одне бʼє по землі до першого приймача, інше перекидає мʼяч через клітину, ще інше — лише на клітину назад. Розвʼязок — розставити гравців так, щоб звільнити лінії пасу повз суперників, бруд, листя, кротів і мавп, що копіюють рухи.

## Поле і час
- Квадратна сітка-поле з воротами; з демо 0.5 — перспективна камера: панорама (середня кнопка миші / правий стік) і зум.
- Покроково: кожен крок цуценяти — окрема дія; undo скасовує по одній клітині. Таймерів нема («Playable without Timed Input»).
- Суперники й тварини — детерміновані елементи пазлу, без власної стратегії: реагують на рух цуценят або на пас.
- Глави (8) з рівнями `1-1 … 8-N`, бонусні рівні й секретний рівень.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Цуценя | piece | порода, запас кроків, напрям погляду | ходить 4 напрямками; повертається на 4 боки; бʼє мʼяч своїм ударом |
| Золотистий ретривер | piece | удар по прямій без ліміту | мʼяч котиться в напрямку погляду, доки його не прийме інше цуценя чи ворота; без приймача удар заборонено |
| Цуценя з ударом через клітину | piece | удар на 2 клітини (дугою) | мʼяч перелітає сусідню клітину й падає на другу |
| Цуценя з далеким ударом | piece | удар на 4 клітини (дугою) | мʼяч падає за 4 клітини, «чи це добра ідея, чи ні» |
| Мопс | piece | удар назад на 1 | відкидає мʼяч на одну клітину позаду себе |
| Бик (bull) | piece | — | ходить на клітину (у розвʼязках гравців); роль і удар — (?) |
| Мʼяч | object | — | лежить у клітині або в цуценяти; летить після удару |
| Ворота | static | — | мʼяч у воротах — перемога |
| Бруд | terrain | — | мʼяч, що потрапив у бруд, зупиняється; забрати його звідти можна лише ударом |
| Купа листя | terrain | — | перегороджує шлях; мʼяч у листі застрягає |
| Кущ | terrain | — | цуценя може зайти (окремий ефект входу); що робить — (?) |
| Кріт | enemy | дві нори: голова / вихід | голова займає одну нору й блокує клітину; коли наступають на іншу нору, кріт переходить туди; може перехопити пас |
| Мавпа | enemy | привʼязана до цуценяти | рухається синхронно зі «своїм» цуценям; упершись, стоїть |
| Кролик | neutral | — | реагує на паси (?) |
| Суперники (інша команда) | enemy | — | зʼявляються в пізніх главах; заважають ударам (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` (або крок намальованого шляху) → ЯКЩО `free(next_cell)` and `counter(steps[pup], >, 0)` → ТО `move(pup, dir)`, `counter(steps[pup], -1)`; інакше `block` — двоє цуценят в одній клітині не стоять.
- КОЛИ `input(turn, dir)` → ТО `face(pup, dir)`; чи коштує поворот крок — (?).
- КОЛИ `enter(pup, ball_cell)` → ЯКЩО `not state(ball, stuck)` → ТО `carry` — мʼяч рухається разом із цуценям (?).
- КОЛИ `input(kick)` → ЯКЩО `has(pup, ball)` and `custom: «на траєкторії удару є приймач — інше цуценя або ворота»` → ТО `custom: «удар за типом цуценяти у напрямку погляду»`; інакше `block` (кнопку удару не приймає).
- КОЛИ `custom: «удар ретривера»` → ТО `slide(ball, dir)` до першої клітини з цуценям, воріт або бруду.
- КОЛИ `custom: «удар через клітину»` → ТО `custom: «мʼяч перелітає 1 клітину й падає на 2-гу»`; далекий удар — на 4-ту.
- КОЛИ `custom: «удар мопса»` → ТО `move(ball, back)`.
- КОЛИ `custom: «мʼяч зупинився в клітині цуценяти»` → ТО `custom: «пас прийнято»`.
- КОЛИ `custom: «пас прийнято»` → ЯКЩО `mode(auto_switch)` → ТО `custom: «керування переходить до приймача»`.
- КОЛИ `enter(ball, mud)` → ТО `set_state(ball, stuck)`.
- КОЛИ `input(dir)` → ЯКЩО `has(pup, ball)` and `state(ball, stuck)` → ТО `custom: «мʼяч лишається в клітині — рушає лише від удару»`.
- КОЛИ `enter(ball, leaves)` → ТО `set_state(ball, stuck)` (?).
- КОЛИ `enter(pup, mole_exit_hole)` → ТО `custom: «кріт переходить у цю нору, стара нора звільняється»`; голова крота — `block` для руху.
- КОЛИ `custom: «мʼяч проходить клітину з головою крота»` → ТО `custom: «перехоплення»`.
- КОЛИ `input(dir)` → ЯКЩО `custom: «у цуценяти є своя мавпа»` and `free(monkey_next_cell)` → ТО `move(monkey_of_pup, dir)`; інакше мавпа стоїть (`block`).
- КОЛИ `custom: «пас»` → ТО `custom: «кролики реагують»` (?).
- КОЛИ `enter(ball, goal)` → ТО `win`, `window(end-screen)`.
- КОЛИ `input(undo)` → ТО `undo(1)` — на одну клітину.
- КОЛИ `input(restart)` → ТО `restart`.
- КОЛИ `input(hint)` → ТО `custom: «показати наступний крок задуманого розвʼязку»`.
- Перемога: мʼяч у воротах. · Поразка: формально нема — закінчились кроки чи мʼяч застряг → undo / рестарт. · Рахунку нема; є досягнення.

## Керування і ввід
- Миша / тач: виділити цуценя (картки внизу екрана), **намалювати шлях** — цуценя йде вже під час малювання (з демо 0.4); удар — однією дією.
- Клавіатура (з коментаря на itch): стрілки — рух, Enter — дія, Q / E — інше цуценя, Z — undo, R — рестарт, Esc — вихід, H / F1 / F2 — додаткові (підказка?).
- Геймпад — повна підтримка; Steam Deck Verified.

## Вікна, меню, HUD
- `main-menu` → `level-select`: мапа глав із дудлами, основна стежка й необовʼязкові гілки, бонусні рівні.
- `custom-window` — інтерактивні комікси без слів між рівнями (історія тренера на пенсії й цуценят).
- `game-screen`: поле, `unit-cards` (портрети цуценят із запасом кроків) внизу, лінія траєкторії удару, кнопки undo / restart / hint.
- `settings-window` → Accessibility: Hint System (вимкнути), «Switch unit after passing», розблокування рівнів, розмір тексту, комфорт камери, альтернативні кольори.
- `end-screen` — екран перемоги після того, як мʼяч долетів до воріт.
- Переходи: level-select → (комікс) → game-screen → end-screen → level-select.

## Фічі поза полем
- `levels-sequential` у 8 главах + `level-unlock`; бонусні рівні й секретний рівень; `achievements`.
- `undo` по клітині без ліміту (?), `restart-level`.
- `hint` (з v1.20): показує задуманий розвʼязок частинами, «щоб не зіпсувати все одразу»; вимикається.
- Доступність: розблокування рівнів, клавіатура / лише миша / лише тач, розмір тексту, кольори, авто-перемикання на приймача; `cloud-save`, `localization` (11 мов).

## Варіації й родичі
- Родичі в корпусі: [Railbound](../connect-rotate/railbound.md) та [inbento](inbento.md) (ті самі автори), [Diaballik](../chess-abstract/diaballik.md) (пас мʼяча по лінії між своїми фішками), [Blood Bowl](../tactics/blood-bowl.md) (пас і перехоплення на сітці), [Ice-sliding puzzles](../push-slide/ice-sliding-puzzles.md) (мʼяч котиться до упору), [DROD](drod.md) (мімік повторює ходи).
- Осі варіацій:
  - **дальність удару**: по прямій до приймача / фіксовано через 1 або 3 клітини / назад на 1;
  - **що перехоплює**: свої цуценята, кроти, суперники, бруд;
  - **ресурс ходу**: кроки на кожне цуценя окремо (тут) / спільний ліміт ходів (Helltaker);
  - **хто ходить разом із тобою**: ніхто / мавпа-двійник свого цуценяти.

## Цікавинки для курсу
- Удари різних типів як «патерни ходу» мʼяча (котиться до приймача / перелітає / назад) — 📎.
- Перевірка легальності удару: шлях мʼяча має закінчитись у приймача чи воротах — 🥉 (симуляція траєкторії до ходу).
- Бюджет кроків на кожну фігуру окремо + перемикання фігур — 📎.
- Кріт із двома норами: наступив на вільну нору — голова переїхала — 🌱.
- Мавпа-двійник, привʼязана до конкретного цуценяти — 🥉.
- Підказка «наступний крок задуманого розвʼязку» з покроковим відкриттям — 🥈, якщо рахувати розвʼязувачем, а не зберігати.

## Мапа на каталог
- Є: `move-by-input` · `path-drawing` · `keyboard-controls` · `party-switch` (Q / E, картки) · `move-limit` (кроки на цуценя) · `piece-move-patterns` (тип удару) · `inertia-slide` (мʼяч котиться до приймача) · `impassable-cells` · `undo-unlimited` · `restart-level` · `level-select` · `level-unlock` · `world-map` · `achievements-window` · `save-progress` · `game-settings` · `sound-effects` · `background-music`.
- **Нема** → пропозиції карток:
  - `+ball-pass` (вже в корпусі, Diaballik) — тут слоти {dirs: 4, receiver: teammate|goal, blockers: mole|rival|mud}.
  - `+kick-patterns` «Удар за типом фігури» · entities/move · 📎 · слот {kind: roll|lob2|lob4|back1}.
  - `+pass-needs-receiver` «Удар лише за наявності приймача» · entities/legality · 🥉.
  - `+ball-trap-tile` «Клітина тримає мʼяч до удару» · entities/interact · 🌱 — бруд, листя.
  - `+mimic-copy` (вже в корпусі) — мавпа повторює рухи свого цуценяти.
  - `+switching-blocker` «Перешкода перескакує між двома норами» · entities/interact · 🌱 — кріт.
  - `+hint-solution-steps` (вже в корпусі).

## Пропозиції до словників
- `+trigger:kicked` — цуценя вдарило мʼяч (на нього реагують кролики); `+trigger:ball_stopped` — мʼяч зупинився (прийом, бруд, ворота).
- `+cond:has_ball` — у цуценяти мʼяч; `+cond:receiver_on_path` — на траєкторії є приймач.
- `+effect:kick` — удар за типом; `+effect:lob` — політ через клітини.
- `+role:ball` — мʼяч як окрема роль (не `object`: має власника й траєкторію).
- `+ui:unit-cards` — картки фігур із запасом кроків; `+ui:kick-trajectory` — лінія удару.
- `+feature:hint-solution-steps` — розвʼязок частинами; `+feature:auto-switch-after-pass`.
- `+card:kick-patterns`, `+card:pass-needs-receiver`, `+card:ball-trap-tile`, `+card:switching-blocker` — див. «Мапа на каталог».
- ⏳-слова, вжиті тут: `input`, `enter`, `free`, `counter`, `has`, `state`, `occupied`, `mode`, `move`, `face`, `slide`, `carry`, `set_state`, `undo`, `restart`.

## Джерела
- ⭐ [Steam: Pup Champs](https://store.steampowered.com/app/2848800/Pup_Champs/) — «Position your players just right, clear their passing lanes, avoid hazards, outsmart the opponents», бруд / мавпи / кролики, 170+ пазлів, бонусні рівні, демо.
- [Steam News API](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=2848800&count=30&maxlength=0) — удар ретривера «someone needs to intercept it or it needs to land inside of the goal», кріт на двох клітинах, бруд, удар мопса назад, мавпи синхронно, undo по клітині, поворот на 4 боки, система підказок 1.20, глава 8.
- [Pocket Gamer](https://www.pocketgamer.com/pup-champs/review/) і [App Army](https://www.pocketgamer.com/pup-champs/app-army-assemble/) — обмежені кроки на цуценя, удар через клітину, кріт перехоплює пас, суперники й бик.
- [Indie Games Plus](https://indiegamesplus.com/pup-champs-review/) — удари на 2 і 4 клітини дугою та по прямій, кроти в норах, листя.
- [itch.io](https://afterburn.itch.io/pup-champs) — платформи й розкладка клавіш (коментар).
- [Steam-форум](https://steamcommunity.com/app/2848800/discussions/0/596280900527862796/) — ретриверу потрібна ціль: інше цуценя або ворота.

## Непевне
- (?) Чи цуценя носить мʼяч (дриблінг) — висновок із правила бруду («не можна прибрати з клітини без удару»).
- (?) Що саме роблять кролики, суперники, бик і кущ; чи кріт перехоплює і наземний, і верхній удар.
- (?) Хто з цуценят має удар на 2 і на 4 клітини (огляди називають кольори, а не породи).
- (?) Чи поворот коштує крок і що буває, коли кроки скінчились.
- (?) Кількість глав у оглядах — «чотири сезони» (Pocket Gamer до 1.10) проти 8 глав у патчах; тут — 8.
