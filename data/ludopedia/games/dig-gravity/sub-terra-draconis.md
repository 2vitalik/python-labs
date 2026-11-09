---
title: Sub Terra Draconis
slug: sub-terra-draconis
aka: [SubTerra Draconis]
family: dig-gravity
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: none
  goal: collect
year: 2019
platforms: [PC (Windows, Linux)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/781840/Sub_Terra_Draconis/", best: true, note: "опис: 120+ рівнів, перелік обʼєктів, «без удачі й прихованих стін», необовʼязкові ліміти часу, редактор + Workshop"}
  - {kind: official, url: "https://www.crystalshard.net/index.php?g=19", note: "Crystal Shard: історія — оновлений рушій SubTerra, предок Draconis (AGS)"}
  - {kind: itch, url: "https://radiant.itch.io/draconis", note: "itch: той самий опис, ввід, доступність, девлоги"}
  - {kind: other, url: "https://www.gog.com/en/game/sub_terra_draconis", note: "GOG: опис, DRM-free"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=781840&count=50&maxlength=0", note: "патчноути: перевертання гравітації, вибуховий голем, тернина, клон-стіна, кнопки големів"}
  - {kind: other, url: "https://store.steampowered.com/app/1344591/Sub_Terra_Draconis_The_Golemworks/", note: "DLC: кнопки големів — рух і штовхання / завмирання / повторення за гравцем"}
  - {kind: other, url: "https://steamcommunity.com/app/781840/reviews/?browsefilter=toprated&filterLanguage=all", note: "відгуки: дракон летить, подих замість штовхання, greed-самоцвіти, прапори, легка/важка версія рівня"}
  - {kind: other, url: "https://www.crystalshard.net/old/subterra.htm", note: "SubTerra (2001): обʼєкти предка — лазери, телепорти, дублікатори, черепи"}
  - {kind: other, url: "https://www.adventuregamestudio.co.uk/forums/ags-games-in-production/draconis-orow-puzzle-game-with-level-editor", note: "Draconis (AGS): прототип з драконом, вогнем і лицарями"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Sub+Terra+Draconis+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 35
mechanics: [move-4dir, dig-terrain, gravity-fall, item-pickup, collect-quota, reach-exit, key-and-door, thief, carrier-platform, cell-transform, inertia-slide, explode-area, spawner-entity, checkpoint, time-out, world-map, in-game-editor, level-exchange, leaderboard, keyboard-controls, controls-remap, tutorial-window, +shifting-gravity, +fire-breath, +flying-avatar, +push-chain, +four-element-blocks, +color-converter, +mimic-copy, +buoyant-rise, +optional-greed-quota, +hint-tile]
proposes: ["+trigger:smashed", "+effect:set_gravity", "+effect:breathe_fire", "+feature:optional-timer", "+feature:level-difficulty-pair", "+card:four-element-blocks", "+card:optional-greed-quota", "+card:flying-avatar"]
author: opus
date: 2026-11-09
---

# Sub Terra Draconis — rocks-and-diamonds з драконом: летиш крізь печери, дихаєш вогнем замість штовхання, каміння й самоцвіти падають

## Суть
Дракончик досліджує підземні лабіринти, збирає самоцвіти й виходить — канон rocks-and-diamonds від Crystal Shard на оновленому рушії їхньої SubTerra (2001). Незвичне: **дракон летить**, тож гравітація діє на каміння й самоцвіти, але не на героя, а дія біля сусідньої клітини — **вогняний подих** (за відгуком, він «замінив штовхання»). Обʼєкти здебільшого мають чотири стихійні «смаки» — вогонь, вода/лід, повітря, земля, — а поверх них: реплікатори, повітряні кулі, вогняні промені, ельфи-злодії, конвеєри, перемикачі гравітації, ключі з дверима, големи.

## Поле і час
- Квадратна сітка; рівні бувають високі (рівень «Waterfall» скролиться вниз); рівні згруповані на мапах, між мапами — подорож.
- Real-time: частина рівнів перевіряє реакцію, частина — планування; ліміти часу **усі необовʼязкові**.
- Прапори — чекпоінти: після рестарту з прапора час стоїть, доки дракон не рушить.
- Повна інформація: «без пазлів на удачу й без пошуку прихованих стін».

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Дракончик | player | — | летить у 4 напрямки (на нього гравітація не діє); дихає вогнем на сусідню клітину |
| Земля | terrain | — | копається (?) щодо способу: прохід чи подих |
| Камінь | object | — | падає без опори |
| Самоцвіт | pickup | звичайний / greed | падає, як камінь; збирається |
| Вихід | gate | — | після самоцвітів |
| Вогняний блок | object | — | може вибухнути |
| Крижаний блок | object | — | після поштовху їде далі |
| Повітряний блок | object | — | зсуваються кілька за раз |
| Земляний блок | container | — | містить самоцвіти |
| Скриня зі скарбом | container | — | скарб (?) щодо вмісту |
| Реплікатор · клон-стіна | spawner | — | копіює обʼєкти (?) щодо правила |
| Повітряна куля | object | — | пливе (?) щодо напрямку |
| Вогняний промінь | hazard | — | промінь-пастка (?) щодо умови спрацювання |
| Ельф-злодій | enemy | — | краде (?) щодо що саме |
| Гноми | enemy | — | «злі гноми» з опису (?) щодо поведінки |
| Конвеєр | terrain | напрямок | везе обʼєкти (?) |
| Перемикач гравітації | switch | — | розвертає гравітацію |
| Ключ ×кольори · двері ×кольори | pickup · gate | колір | ключ відмикає двері свого кольору; ключ — рухомий обʼєкт |
| Рожевий конвертер | terrain | — | ключ, що пройшов крізь нього, міняє колір |
| Світлячок (dragonfly) | neutral | текст | підказка в «бульбашці» |
| Голем | neutral | — | може вибухнути; з DLC — керується кнопками |
| Кнопка голема (DLC Golemworks) | switch | режим | големи рухаються й штовхають / завмирають / повторюють за драконом |
| Тернина (briar) | static | — | створюється під час гри (?) щодо джерела |
| Магічні камені | pickup | — | предмети-уміння (замість вогнегасника, ковзанів, щебеню оригіналу) |
| Прапор | switch | — | чекпоінт |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(target)` → ТО `move(dragon, dir)`; `custom: «дракон не падає»`.
- КОЛИ `tick` → ЯКЩО `not supported(rock|gem)` → ТО `fall(a)`; `custom: «більшість інших обʼєктів не падає»`.
- КОЛИ `custom: «smashed: камінь упав на дракона»` → ТО `lose` (?).
- КОЛИ `input(fire)` → ТО `custom: «опалити сусідню клітину»`.
- КОЛИ `custom: «вогонь у вогняному блоці»` → ТО `explode(area)` (?) щодо тригера.
- КОЛИ `custom: «крижаний блок зрушено»` → ТО `slide(ice_block, dir)`.
- КОЛИ `custom: «повітряний блок зрушено»` → ТО `push` ланцюгом сусідніх повітряних.
- КОЛИ `destroyed(earth_block)` → ТО `spawn(gem)` (?).
- КОЛИ `contact(dragon, gem)` → ТО `pickup`, `counter(gems, +1)`.
- КОЛИ `contact(dragon, exit)` → ЯКЩО `counter(gems, >=, quota)` → ТО `win`; ЯКЩО `counter(gems, >=, greed)` → ТО `custom: «greed-ціль виконано (зірка)»`.
- КОЛИ `contact(dragon, key[c])` → ТО `pickup`; КОЛИ `contact(dragon, door[c])` → ЯКЩО `has(dragon, key[c])` → ТО `disappear(door)`; інакше `block`.
- КОЛИ `enter(key, converter)` → ТО `transform(key[c], key[c'])`.
- КОЛИ `contact(dragon, gravity_switch)` → ТО `custom: «гравітація розвертається»`.
- КОЛИ `enter(a, conveyor)` → ТО `move(a, belt_dir)` (?).
- КОЛИ `contact(elf, dragon)` → ТО `take(dragon, item)` (?) щодо предмета.
- КОЛИ `contact(dragon, firefly)` → ТО `message(hint)`.
- КОЛИ `contact(dragon, golem_button)` → ТО `set_state(golems, move_push | freeze | imitate)`; `imitate` — `custom: «голем повторює хід дракона»`.
- КОЛИ `contact(dragon, flag)` → ТО `checkpoint`; КОЛИ `input(restart)` → ТО `respawn(dragon, flag)`, `custom: «таймер стоїть до першого руху»`.
- КОЛИ `counter(time_left, ==, 0)` → ЯКЩО `mode(timed)` → ТО `lose`.
- Перемога: самоцвіти → вихід; рівень оцінюється до 3 зірок (одна — за greed (?)). Поразка: смерть від обʼєкта/ворога або час (якщо увімкнено). Рахунок: самоцвіти сюжетного режиму (досягнення 250 → 10 000).

## Керування і ввід
- Клавіатура (стрілки або WSAD — підказка з v1.1) чи будь-який геймпад; перепризначення клавіш; Z — старт.
- Окрема дія вогню (?) щодо клавіші; рестарт з прапора.

## Вікна, меню, HUD
- `main-menu` → `map-window` (мапа рівнів, нелінійна; легка й важка версії того самого рівня; пауза показує мапу).
- `game-screen`: поле; самоцвіти й greed-ціль, `timer-countdown` (якщо увімкнено) (?) щодо складу HUD; `hint-text` від світлячків.
- `tutorial-window` — інтерактивне навчання; після нього відкриваються мапи DLC.
- `editor-window` — редактор рівнів (quicksave, кнопки керування големами) → публікація в Workshop.
- `end-screen` з зірками (?) · `leaderboard` (Steam).

## Фічі поза полем
- `world-map` з кількома мапами (основна + DLC Magma Grotto, The Golemworks, Hidden Glade — по 30 рівнів).
- `level-editor` + `level-sharing` (Steam Workshop; досягнення за чужий рівень) · `stars-rating` · `checkpoint`-прапори.
- Необовʼязковий таймер як налаштування (`+feature:optional-timer`); легка/важка версія рівня.
- `achievements`, `cloud-save`, `leaderboard-online`, `remap-controls`, `gamepad-support`, `localization` (7 мов), субтитри.

## Варіації й родичі
- Предки: SubTerra (2001, 500 рівнів, Challenge Mode, понад 100 обʼєктів: дублікатори, що копіюють усе, включно з гравцем, лазери, телепорти, черепи, бомби) і SubTerra II (логічні вентилі, собаки (?)); Draconis (AGS) — дракон-прототип: падаючі самоцвіти вбивали, брати можна лише нерухомі; лицарі вбивали, лише коли дивились на героя; рівні — у `customlevel.txt`.
- Родичі в корпусі: [Boulder Dash](boulder-dash.md), [Rocks'n'Diamonds](rocks-n-diamonds.md), [Emerald Mine](emerald-mine.md) (конвертери, ключі), [Supaplex](supaplex.md) (перемикач гравітації), [Bone Cruncher](bone-cruncher.md) і [Crystal Mines II](crystal-mines-ii.md) (`+shifting-gravity`).
- **Осі варіацій**: гравітація для героя — «падає (платформер) / не діє, бо летить (Draconis, BD)»; взаємодія з сусідньою клітиною — «штовхання / snap (BD) / вогняний подих»; ліміт часу — «жорсткий / необовʼязковий»; цілі — «квота / квота + greed-квота».

## Цікавинки для курсу
- Чотири стихійні блоки з різною фізикою поштовху (вибух / ковзання / ланцюг / схованка) — 🥉.
- Конвертер кольору ключа: обʼєкт-предмет, що змінює властивість, проходячи крізь клітину — 📎.
- Перемикач гравітації для всіх падаючих обʼєктів — 🥉.
- Кнопки голема: режими «штовхає / завмер / повторює за гравцем» — 🥈 (mimic-рух).
- Прапор-чекпоінт, після якого таймер стоїть до першого руху — 🌱.
- Greed-квота як необовʼязковий «hard mode» поверх тієї ж мапи — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `dig-terrain` · `gravity-fall` · `item-pickup` · `collect-quota` · `reach-exit` · `key-and-door` · `thief` (ельфи) · `carrier-platform` (конвеєр) · `cell-transform` (конвертер) · `inertia-slide` (лід) · `explode-area` (вогняний блок, голем) · `spawner-entity` (реплікатор, клон-стіна) · `checkpoint` (прапор) · `time-out` · `world-map` · `in-game-editor` + `level-exchange` · `leaderboard` · `keyboard-controls` + `controls-remap` · `tutorial-window`.
- **Нема** → пропозиції карток:
  - Повтори з корпусу: `+shifting-gravity` {by: switch}, `+fire-breath` (тут — лише сусідня клітина), `+push-chain` (повітряні блоки), `+color-converter`, `+mimic-copy` (голем), `+buoyant-rise` (кулі), `+hint-tile` (світлячок).
  - `+flying-avatar` «Аватар не підкоряється гравітації, обʼєкти — так» · entities/move · 🌱.
  - `+four-element-blocks` «Блоки чотирьох стихій з різною реакцією на поштовх» · entities/interact · 🥉 · слоти {fire: explode, ice: slide, air: chain, earth: holds_gem}.
  - `+optional-greed-quota` «Друга, вища квота — необовʼязкова ціль рівня» · game-logic/goals · 🌱.

## Пропозиції до словників
- `+trigger:smashed(a)` — на A впав обʼєкт (повтор корпусу).
- `+effect:set_gravity(dir)` — змінити напрям гравітації (повтор корпусу).
- `+effect:breathe_fire(cell)` — дія на сусідню клітину без руху: підпалити/зрушити.
- `+feature:optional-timer` — ліміт часу як перемикач.
- `+feature:level-difficulty-pair` — легка й важка версії одного рівня на мапі.
- `+card:four-element-blocks` · `+card:optional-greed-quota` · `+card:flying-avatar` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Sub Terra Draconis](https://store.steampowered.com/app/781840/Sub_Terra_Draconis/) — Crystal Shard, 8.12.2019; 120+ рівнів, перелік обʼєктів, редактор і Workshop, теги Grid-Based Movement, Mining.
- [Crystal Shard](https://www.crystalshard.net/index.php?g=19) — гра на оновленому рушії SubTerra; предок Draconis (AGS); обʼєкти SubTerra II увійшли в гру.
- [Steam News API](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=781840&count=50&maxlength=0) — патчі: «reversing gravity», «exploding golem, making briar, cloning wall», кольори ключів і дверей, підказки світлячків, кнопки големів у редакторі.
- [DLC The Golemworks](https://store.steampowered.com/app/1344591/Sub_Terra_Draconis_The_Golemworks/) — кнопки големів: «move and push things around, freeze in place, or imitate you».
- [Відгуки Steam](https://steamcommunity.com/app/781840/reviews/?browsefilter=toprated&filterLanguage=all) — дракон летить і не падає; подих замість штовхання; greed-самоцвіти; прапори; 3 зірки; магічні камені замість предметів оригіналу.
- Steam-обговорення [«More bugs (fireflies & keys)»](https://steamcommunity.com/app/781840/discussions/0/3938911974173167389/) — рожевий конвертер міняє колір ключа; світлячки з текстом.
- TVTropes `VideoGame/SubTerraDraconis` (бачив у пошуку, агентам 403) — сніпет: подих опалює сусідні клітини; падають лише каміння й самоцвіти; блоки чотирьох стихій.
- [SubTerra (старий сайт)](https://www.crystalshard.net/old/subterra.htm) і [AGS-форум: Draconis](https://www.adventuregamestudio.co.uk/forums/ags-games-in-production/draconis-orow-puzzle-game-with-level-editor) — предки.

## Непевне
- (?) Механіка блоків чотирьох стихій — з пошукового сніпета TVTropes; сторінка 403, перевірити не вдалось.
- (?) Як дракон взаємодіє з землею й каменем: копає проходом чи подихом; чи може штовхати без подиху.
- (?) Чи вбиває камінь, що впав на дракона (у прототипі Draconis — так, падаючі самоцвіти теж).
- (?) Поведінка реплікатора, кулі, вогняного променя, ельфа, гномів і конвеєра — лише назви з опису; правила взято за аналогією з SubTerra.
- (?) Критерії 3 зірок і чи зірка = greed.
- (?) Яка клавіша дихає вогнем; що роблять «магічні камені».
- (?) Рік: Steam/GOG — 2019; рушій і частина рівнів — із SubTerra II (рік не знайшов).
