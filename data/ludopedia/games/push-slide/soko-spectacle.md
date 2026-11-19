---
title: Soko Spectacle
slug: soko-spectacle
aka: []
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
year: 2025
platforms: [Windows, Linux]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3359440/", best: true, note: "трейлер і скриншоти; «Move the fireworks next to the flames / Or use powder to connect them / Some crates will need to be assembled first»; 100+ рівнів, undo/redo, 6 вбрань; є демо"}
  - {kind: itch, url: "https://jebouin.itch.io/soko-spectacle", note: "три GIF механік (запалити, порохова доріжка, зібрати ящик), changelog 1.0.0–1.2.0 з назвами груп рівнів; демо для Windows/Linux"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3359440&count=20&maxlength=0", note: "новини Steam: 1.1.0 (правки рівнів Void, Stack, Brevi, Sea, Tower, Bomb), Halloween Update 1.2.0 — меню Extra, 10 демо- і 28 Halloween-рівнів, миша, 8 мов"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Soko+Spectacle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, keyboard-controls, push-object, tile-merge, item-pickup, goal-counter, objective-text, undo-unlimited, redo, restart-level, world-map, level-unlock, end-screen, event-effects, particles, sound-effects, background-music, main-menu, pause-menu, settings-window, stats-window, avatar-picker, controls-remap, language-picker, volume-control, save-progress, +skin-unlock-progression, +branching-campaign, +ignite-adjacent, +fuse-trail, +slot-merge]
proposes: ["+effect:ignite", "+ui:supply-counter", "+feature:undo-speed", "+feature:transparent-boxes", "+card:ignite-adjacent", "+card:fuse-trail", "+card:slot-merge"]
author: opus
date: 2026-11-19
---

# Soko Spectacle — штовхай ящики з феєрверками до вогню, тягни порохові доріжки й збирай ящики з частин, щоб засвітити нічне небо

## Суть
Сокобан Jérémy Bouin: піротехнік штовхає ящики з ракетами, і кожен треба запалити — підсунути впритул до полумʼя або зʼєднати з вогнем доріжкою пороху, яку герой сам розсипає за собою. Частина ящиків розбита на шматки (рамка на 4 ракети з порожніми гніздами) і зливається в цілий лише поштовхом шматка в шматок. Рівень пройдено, коли запалено потрібну кількість ящиків: настає ніч, і над містом розквітає салют.

Понад 100 рівнів у нелінійній мапі світу, групи з окремими механіками (прірва, вода, бомби, порохові блоки, вежа), пізніше — Halloween-рівні з павутиною й гарбузами.

## Поле і час
- Кожен рівень — сітка 17×10 клітин (редактор LDtk); тайли землі мають тип: земля, стіна, вода, прірва («Underground»).
- Хід = крок героя; без вводу світ стоїть, тож гра покрокова, а налаштування «Move speed» / «Undo speed» міняють лише швидкість анімацій.
- Шари: земля → доріжки пороху → обʼєкти (герой, ящики, полумʼя, купки пороху) → ефекти (вогонь, ракети).
- Біоми стін: ліс, пустеля, лід, вежа, Halloween; є нічні рівні (у коді — освітлення від вогнів) (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Піротехнік | player | вбрання (8 видів), запас пороху | рух 4 боки; штовхає ящики; ступивши на купку, бере порох |
| Ящик з феєрверком | object | рама 2×2 гнізд: порожня / 1 / 2 / 3 ракети / повна (16 видів) | штовхається; повний поруч із вогнем запалюється |
| Частина ящика | object | які гнізда зайняті | при поштовху в іншу частину зливається з нею |
| Запалений ящик | object | — | червоний з трикутником; рахується в мету; наприкінці злітає салютом |
| Полумʼя | source | горить / згасле | запалює повний ящик поруч і доріжку пороху |
| Купка пороху | pickup | кількість N (бувають 3, 5, 6, 9) | герой стає на неї → +N пороху в запас |
| Доріжка пороху | conduit | — | лягає на клітини за героєм, поки є запас; проводить вогонь; буває розсипана заздалегідь |
| Металевий ящик | object | — | сірий блок (той самий тип `Box`, що й пороховий); штовхається; (?) не горить |
| Пороховий блок | object | — | штовхається; (?) проводить вогонь далі, як доріжка |
| Вбрання | pickup | тип | у рівнях «Outfit»: зібрати = мета, відкриває скін |
| Стіни, дерева | static | біом | непрохідні |
| Вода | terrain | — | (?) обʼєкт у ній тоне |
| Прірва | hazard | — | (?) обʼєкт і герой, що туди потрапили, падають |
| Павутина (Halloween) | static | — | (?) згорає від вогню |
| Гарбуз (Halloween) | object | — | (?) росте / вибухає |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(hero, dir)`.
- КОЛИ `contact(hero, crate|metal_box|powder_block)` → ЯКЩО `free(cell_behind)` → ТО `push`; інакше `block`.
- КОЛИ `contact(crate_part, crate_part)` → ЯКЩО `custom: «зайняті гнізда двох частин не перетинаються»` → ТО `merge(a, b → crate)` — разом повна рама (4 ракети) або більша частина.
- КОЛИ `adjacent(full_crate, lit_flame)` → ТО `set_state(crate, lit)`, `counter(lit, +1)`.
- КОЛИ `enter(hero, powder_stack)` → ТО `pickup`, `counter(powder, +N)`.
- КОЛИ `leave(hero, cell)` → ЯКЩО `counter(powder, >, 0)` → ТО `place(hero, powder)`, `counter(powder, −1)` — герой лишає за собою доріжку.
- КОЛИ `adjacent(powder, full_crate)` → ЯКЩО `connected(powder)` and `custom: «доріжка торкається палаючого полумʼя»` → ТО `set_state(crate, lit)`, `counter(lit, +1)`.
- КОЛИ `counter(lit, >=, target)` → ТО `win`, `window(end-screen)` — «Level Cleared!» і салют над містом.
- КОЛИ `enter(hero, outfit)` → ТО `pickup`, `win`, `window(custom-window)` — «Outfit unlocked!»: Equip / Keep current.
- КОЛИ `enter(object, void)` → ТО `fall(object)` (?) — у коді є падіння ящика, пороху, ракети й самого героя.
- КОЛИ `input(undo)` → ТО `undo`.
- КОЛИ `input(redo)` → ТО `custom: «повернути скасований хід»`.
- КОЛИ `input(reset)` → ТО `restart`.
- Перемога: запалено `targetCount` ящиків (HUD «Goal: ☀ x/y»), або зібрано вбрання («Goal: Collect»), або нічна мета «Goal: ☾» (?). · Поразка: герой може загинути (досягнення «Dead: Find a way to die»), далі undo. · Рахунку нема.

## Керування і ввід
- Клавіатура (переназначувана), геймпад (Undo — B, Redo — Y, Reset — Select на підказках), з 1.2.0 — повністю мишею (?) (герой іде в бік курсора).
- Undo / redo без ліміту, Reset — рестарт рівня; Pause — меню.

## Вікна, меню, HUD
- `main-menu`: Play · Extra (світи «Demo» і «Halloween»; відкриваються вбраннями Classy і Mummy) · Settings · Stats · About · Quit.
- `map-window` — мапа світу: клітинки рівнів групами 2×2 / 2×3 з табличками («Intro», «Merge», «Void»…), вежа з дверима, руни на шляху; зіркові групи (★) — складніші.
- `game-screen`: рівень; угорі ліворуч `objective-text` «Goal: ☀ x/y» (☾ уночі, «Collect» для вбрання) і запас пороху (значок + число або ∞); праворуч підказки Undo / Redo / Reset.
- `pause-menu` «Paused» / «Solved x/y»: Continue · Quit (і Save and quit) to title / to level selection · Settings · Reset level · Change outfit.
- `settings-window`: мова; гучність загальна / музика / звуки; повний екран, масштаб, V-Sync; Show controls; тряска й спалахи екрана; мозаїчний фільтр і його сила; клавіші й геймпад; Move speed, Undo speed; вібрація; прозорі ящики; FPS; «DANGER»: скинути налаштування, прогрес, досягнення; приховати навчальний текст.
- `character-select` «Select an outfit»: Basic, Classy, Penguin, Mummy, Flower, Cosmic, Wizard, Robot (закриті — «???»).
- `end-screen` «Level Cleared!» — салют над нічним містом.
- `stats-window` — Stats з титулу; досягнення Steam (11).

## Фічі поза полем
- `undo` ∞ + `redo` + `restart-level`; налаштування швидкості ходу й undo.
- `world-map` з нелінійним відкриванням груп; «зіркові» групи; руни на мапі (?).
- `unlockables`: 6 вбрань за просування + 2 з Halloween; `achievements` (Start, Challenging, Dead, Outfit 1–5, Done, Demo, Halloween).
- `localization` 8 мов (з 1.2.0), `remap-controls`, `gamepad-support`, `mouse-and-keyboard`, `screen-shake-toggle`; приховати навчальний текст.
- `cloud-save` (Steam Cloud); збереження в AppData / ~/.local/share.

## Варіації й родичі
- Групи рівнів (назви з гри): Intro, Merge, Void, Stack, Trail, Powder Blocks, Tower, Entrance, Oasis, Bomb, Nox, Quadra Nox, Brevi, Lacus, Sea, Outfit; Halloween-світ — Web, Pumpkin, Halloween.
- Родичі: [sokoban](sokoban.md); [campfire-cooking](../thinky/campfire-cooking.md) і [bonfire-peaks](../thinky/bonfire-peaks.md) — вогонь як ціль штовхання; [kwirk](kwirk.md) — обʼєкт у дірці; [bombuzal](../thinky/bombuzal.md) — бомби на сітці.
- Осі варіацій:
  - **як запалити**: впритул до вогню / порохова доріжка, яку тягне герой / (?) пороховий блок;
  - **ціль штовхання**: сама ціль-клітина (Sokoban) / сусідство з джерелом (тут);
  - **цілісність ящика**: цілий / з частин, що зливаються.

## Цікавинки для курсу
- Запалення за сусідством: після кожного ходу перевірити 4 сусіди полумʼя — 🌱.
- Доріжка пороху з обмеженого запасу: клітини, які покинув герой, стають провідником — 📎.
- Поширення вогню доріжкою: пошук звʼязного шляху від полумʼя до ящика (BFS/flood fill) — 📎.
- Злиття частин ящика: маска 4 гнізд, обʼєднання, якщо маски не перетинаються — 🌱 (бітові операції).
- Мапа світу з групами, зірковими рівнями й відкриванням за умовою — 🥉.
- Фінальний салют: ракети злітають і розриваються частинками — 📎 (рендер, не логіка).

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ рух; `push-object` ↔ ящики; `tile-merge` ↔ злиття частин; `item-pickup` ↔ купки пороху, вбрання; `goal-counter` + `objective-text` ↔ «Goal: ☀ x/y»; `undo-unlimited` + `redo` + `restart-level` ↔ Undo / Redo / Reset; `world-map` + `level-unlock` ↔ мапа груп; `end-screen` + `event-effects` + `particles` ↔ «Level Cleared!» і салют; `main-menu`, `pause-menu`, `settings-window`, `stats-window`; `avatar-picker` ↔ вбрання; `controls-remap`, `language-picker`, `volume-control`; `save-progress`.
- **Нема** → пропозиції карток:
  - `+skin-unlock-progression` (є в корпусі) — вбрання за просування.
  - `+branching-campaign` (є в корпусі) — нелінійні групи рівнів.
  - `+ignite-adjacent` «Обʼєкт поруч із джерелом вогню запалюється» · entities/interact · 🌱.
  - `+fuse-trail` «Аватар розсипає провідну доріжку із запасу» · entities/spawn · 📎 · слот {supply: N|∞}.
  - `+slot-merge` «Частини з непересічними гніздами зливаються в одну» · entities/legality · 🌱 (дитина `tile-merge`).

## Пропозиції до словників
- `+effect:ignite` — запалити обʼєкт (ящик, доріжку); `set_state(crate, lit)` не каже про вогонь (повтор: кандидат у корпусі).
- `+ui:supply-counter` — запас ресурсу, що витрачається кроками (значок пороху + число / ∞).
- `+feature:undo-speed` — окрема швидкість анімації відкату; `+feature:transparent-boxes` — показувати, що під ящиками.
- `+card:ignite-adjacent`, `+card:fuse-trail`, `+card:slot-merge` — див. «Мапу на каталог».

## Джерела
- ⭐ [Steam: Soko Spectacle](https://store.steampowered.com/app/3359440/) — опис і три підписи механік, 100+ рівнів, undo/redo, нелінійна прогресія, 6 вбрань, трейлер, 8 скриншотів (HUD «Goal», мапа з групами, вікно вбрань, «Level Cleared!»).
- [itch.io: Soko Spectacle](https://jebouin.itch.io/soko-spectacle) — GIF: ящик до вогню, доріжка з купки «5», злиття частин ящика; changelog з групами Void, Stack, Brevi, Sea, Tower, Bomb.
- [Новини Steam](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3359440&count=20&maxlength=0) — 1.1.0 і Halloween Update 1.2.0.
- Демо (itch, Linux) — `res.pak`: проєкт LDtk (сутності `Hero`, `Box` Metal/Powder, `Grid` з 16 видами заповнення, `Flame` Lit/Unlit, `PowderStack` з кількістю, `SpiderWeb`, `Pumpkin`, `Rocket`, `Outfit`; поле рівня `targetCount`; 10 демо-рівнів 17×10) і тексти інтерфейсу (меню, налаштування, досягнення, назви груп).
- YouTube: пошук «Soko Spectacle gameplay».

## Непевне
- (?) Запалення «поруч» — лише 4 сусіди чи й діагональ; у GIF видно тільки бічне сусідство.
- (?) Як саме вогонь іде доріжкою (миттєво чи по клітині; чи згорає порох) і чи доріжка мусить торкатися полумʼя кінцем.
- (?) Металеві й порохові блоки: штовхання — з типу сутності `Box`, а чи горять і вибухають — не встановлено; «Tower 2 не пройти без порохових блоків» — з changelog.
- (?) Прірва й вода: у коді є падіння ящиків, пороху, ракет і героя у прірву та воду, а «Bomb 8» вимагає перейти воду бомбою; механіку бомби (окремої сутності в LDtk нема) не встановлено.
- (?) Нічні групи Nox / Quadra Nox мають мету «☾» і `targetCount` 0 — що треба зробити вночі, не зʼясовано.
- (?) Павутина, гарбузи, окремі ракети й «DropZone» — лише назви сутностей і анімацій (`SpiderWebBurn`, `PumpkinExplosion`, `FallingRocket`).
- (?) Керування мишею: у коді `heroToMouseDir` — герой іде в бік курсора; не перевірено.
