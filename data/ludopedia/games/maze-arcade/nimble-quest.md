---
title: Nimble Quest
slug: nimble-quest
aka: []
family: maze-arcade
also: [roguelike]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: score
year: 2013
platforms: [iOS, Android, Ouya, Steam]
links:
  - {kind: other, url: "https://games.jayisgames.com/review/nimble-quest.php", best: true, note: "огляд: ланцюг до 15 героїв, свайпи, ближній/дальній бій, дропи, геми й жетони, смерть → етап 1"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Nimble_Quest", note: "суть, герої з дропу, умови поразки, платформи"}
  - {kind: steam, url: "https://store.steampowered.com/app/259780/", note: "опис: «conga line of heroes», гільдії й Guild Quests"}
  - {kind: other, url: "https://www.pocketgamer.com/nimble-quest/nimble-quest-review/", note: "огляд: поразка від краю/ворога/власного хвоста, баффи, Arena"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/MageTrain", note: "MageTrain (2025): здібності за позицією в ланцюгу"}
  - {kind: other, url: "https://www.pocketgamer.com/magetrain/official-launch-android-ios/", note: "MageTrain: роль героя залежить від місця в поїзді, розгалужені забіги"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Snake_Core", note: "Snake Core (2020): лінія солдатів з автострільбою"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Nimble+Quest+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-auto, body-queue, self-collision, touch-death, environment-death, swipe-gestures, hp-damage, melee-vs-ranged, projectile-shot, drop-on-death, item-pickup, temporary-modes, round-currency, shop-between-levels, shop-window, character-select, game-over-continue, mode-select, leaderboard, sequential-levels, world-map, +party-snake, +auto-attack-in-range, +position-ability, +escalating-continue-cost, +kill-quota, +item-magnet]
proposes: ["+card:party-snake", "+card:auto-attack-in-range", "+card:position-ability", "+card:escalating-continue-cost", "+card:kill-quota", "+card:item-magnet", "+feature:guild-quests"]
author: opus
date: 2026-11-09
---

# Nimble Quest — змійка з героїв: кожен сегмент сам бʼє ворогів у радіусі, а ти лише кермуєш головою

## Суть
Класична змійка, де тіло — не рахунок, а **загін**: гравець лише повертає голову-лідера свайпом, а кожен герой у ланцюгу сам атакує ворогів у своєму радіусі — лицарі впритул, лучники й маги здалеку. Загін росте, коли вбиті вороги лишають героя, що стає в хвіст; врізатися лідером у край арени, у ворога (до того, як його вбито) чи у власний хвіст — кінець забігу. Огляд-файл: нижче ще MageTrain (2025), де **позиція в ланцюгу вмикає здібність**, і Snake Core (2020) — та сама ідея зі стрільбою.

## Поле і час
- Закриті арени на один екран з краями-стінами; загін рухається безперервно й повертає під прямим кутом (?) щодо клітинної сітки — див. «Непевне».
- Real-time; етапи йдуть один за одним (від Лісу до «Безодні»), етап закривається, коли вбито досить ворогів.
- Смерть повертає на етап 1 і скидає загін (без жетонів).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Лідер (голова) | player | герой; HP | рухається безперервно; свайп — поворот; врізався — кінець забігу |
| Герой у ланцюгу | ally | HP, тип атаки, радіус | іде слідом за попереднім; сам атакує ворога в радіусі |
| Ближні герої (лицар тощо) | ally | атака впритул, міцніші | краще в голові ланцюга (PocketGamer) |
| Дальні герої (лучник, маг, бомбометальник) | ally | снаряди, крихкіші, більша шкода | бʼють здалеку |
| Ворог | enemy | HP, сила, здібність | теж рухається «змійкою», може повернути в загін; панцерні солдати, павуки з павутиною (сповільнює) |
| Герой-дроп | pickup | — | випадає з убитого ворога; підібрав — стає в хвіст |
| Гем | resource | — | падає з ворогів; валюта апгрейдів |
| Павер-ап | pickup | тривалість | магніт (геми летять до тебе), щит лідера, швидша/сильніша атака, бомба, лід, зілля |
| Край арени | static | — | дотик лідера — кінець забігу |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `move(leader, facing)`, `custom: «герої йдуть слідом — тіло-черга»`.
- КОЛИ `input(swipe_dir)` → ТО `face(leader, dir)`.
- КОЛИ `timer(cooldown)` → ЯКЩО `in_range(hero, enemy, range)` → ТО `damage(enemy, atk)`; дальній герой — через `spawn(projectile)`.
- КОЛИ `hp_zero(enemy)` → ТО `disappear(enemy)`, `spawn(gem)`, `counter(kills, +1)`.
- КОЛИ `died(enemy)` → ЯКЩО `prob(p)` → ТО `spawn(hero_drop)` або `spawn(power_up)`.
- КОЛИ `contact(leader, hero_drop)` → ТО `attach(hero, tail)`.
- КОЛИ `contact(leader, gem)` → ТО `currency(+1)`.
- КОЛИ `picked(leader, power_up)` → ТО `set_state(party, buff, dur)` — магніт / щит лідера / сила / швидкість атаки; зілля — `heal(party, n)`.
- КОЛИ `contact(leader, edge)` → ТО `lose`.
- КОЛИ `contact(leader, enemy)` → ЯКЩО `not state(leader, shield)` → ТО `lose`.
- КОЛИ `contact(leader, own_body)` → ТО `lose`.
- КОЛИ `contact(enemy_attack, hero)` → ТО `damage(hero, n)`; павутина — `speed(party, -n)`.
- КОЛИ `custom: «здоровʼя загону вичерпано»` → ТО `lose`.
- КОЛИ `counter(kills, >=, quota)` → ТО `next_level`.
- КОЛИ `level_start` → ТО `choose(heroes_or_buffs_for_tokens)`.
- КОЛИ `died(party)` → ЯКЩО `custom: «гравець платить жетони»` → ТО `restart` — ціна різко росте, якщо вже вмирав на цьому етапі; інакше `custom: «етап 1, загін скинуто»`.
- MageTrain: КОЛИ `custom: «герой на позиції k у поїзді»` → ТО `set_state(hero, ability_k)`.
- Snake Core: КОЛИ `contact(soldier, wall)` → ТО `custom: «солдат гине»`.
- Перемога: нема (нескінченні етапи). Поразка: лідер врізався або здоровʼя вичерпано. Рахунок: етапи/вбивства; в Arena — очки на рекорд.

## Керування і ввід
- Свайп у бік, куди повернути (Steam — клавіатура/геймпад (?)); загін не зупиняється, рухається вперед незалежно від перешкод.
- Атака повністю автоматична: ввід — лише маршрут, тобто розвести дистанцію (дальні) і зближення (ближні) з напрямком удару.
- Перед етапом — витратити жетони на героїв чи баффи.

## Вікна, меню, HUD
- `main-menu` (?) → вибір режиму: Quest / Arena (`mode-select`).
- `character-select` — вибір лідера й стартових героїв (на старті 3 відкриті).
- `shop-window` — апгрейди героїв і павер-апів за геми.
- `game-screen`: арена, ланцюг героїв; HUD — геми, етап, HP героїв (?).
- `game-over-continue` — продовжити за жетони (ціна росте).
- `leaderboard` — глобальні таблиці, гільдії (Steam).
- Переходи: меню → вибір загону → етап → (квота вбивств) наступний етап → … → смерть → продовжити за жетони / назад до меню.

## Фічі поза полем
- `meta-progression` — герої відкриваються за пройдені рівні й прокачуються гемами; апгрейди павер-апів у магазині.
- Дві валюти: геми (з ворогів) і рідкісні жетони (продовження, герої/баффи перед етапом); free-to-play з покупками (мобільна версія), Steam — платна.
- `mode-*`: Arena — гра на очки; `+feature:guild-quests` — гільдії з обмеженими в часі квестами й глобальним рейтингом.
- `leaderboard-online`.

## Варіації й родичі
- **MageTrain** (Tidepool Games, 2025; iOS/Android): поїзд із 9 героїв з автоатакою; **позиція в ланцюгу визначає роль і вмикає здібність** (фронт — атака, решта — підтримка); забіги роглайт-структури з розгалуженою мапою (золото, павер-апи, випадкові випробування), 8 типів підземель, 30 навичок за золото. Вісь «що дає місце в ланцюгу».
- **Snake Core** (OrangePixel, 2020; mobile, PC, Switch): лінія солдатів з автострільбою; удар об стіну вбиває солдатів; знешкоджувати бомби й обороняти точки; маршрут через вузлову мапу; фінальний бос.
- [`snake`](snake.md) — предок; [`jungler`](jungler.md), [`serpentine`](serpentine.md) — змійки-бійці; [`slither-io`](slither-io.md) — змійка проти змійок.
- **Осі варіацій**: сегмент тіла — «просто тіло / юніт з атакою (NQ) / юніт, чия здібність залежить від позиції (MageTrain)»; ріст — «їжа / найманий з дропу»; смерть — «кінець / назад на етап 1 / продовження за валюту».

## Цікавинки для курсу
- Сегменти змійки як юніти з HP і власною авто-атакою в радіусі — 🥉.
- Ближні й дальні герої: порядок у ланцюгу як тактика (міцні спереду) — 📎.
- Позиція в ланцюгу вмикає здібність (MageTrain) — 🥉.
- Дроп героя з ворога → приєднання в хвіст — 🌱.
- Магніт для предметів (притягувати пікапи в радіусі) — 🌱.
- Етап закривається квотою вбивств, смерть — назад на етап 1 або продовження з ціною, що росте — 📎.

## Мапа на каталог
- Є: `move-auto` · `body-queue` · `self-collision` · `touch-death` · `environment-death` (край) · `swipe-gestures` · `hp-damage` · `melee-vs-ranged` · `projectile-shot` · `drop-on-death` · `item-pickup` · `temporary-modes` (баффи) · `round-currency` (геми) · `shop-between-levels` · `shop-window` · `character-select` · `game-over-continue` · `mode-select` · `leaderboard` · `sequential-levels` · `world-map` (MageTrain, Snake Core).
- **Нема** → пропозиції карток:
  - `+party-snake` «Ланцюг-загін: кожен сегмент — юніт» · entities/move · 🥉.
  - `+auto-attack-in-range` «Автоатака в радіусі за кулдауном» · entities/combat · 📎 · слоти {range, cooldown}.
  - `+position-ability` «Здібність залежить від позиції в ланцюгу» · entities/state · 🥉.
  - `+escalating-continue-cost` «Продовження за валюту з ростом ціни» · game-logic/economy · 🌱.
  - `+kill-quota` «Рівень закінчується після N вбивств» · game-logic/win · 🌱.
  - `+item-magnet` «Магніт притягує предмети» · entities/interact · 🌱.

## Пропозиції до словників
- `+feature:guild-quests` — гільдії гравців із тимчасовими спільними квестами й рейтингом (Nimble Quest).

## Джерела
- ⭐ [JayIsGames: Nimble Quest](https://games.jayisgames.com/review/nimble-quest.php) — до 15 героїв у ланцюгу, свайпи, ближні/дальні, дроп героїв, павер-апи (магніт, щит, бомба, лід, зілля), геми й жетони, смерть → етап 1, ціна повтору росте.
- [Wikipedia: Nimble Quest](https://en.wikipedia.org/wiki/Nimble_Quest) — героїв з дропу, квота вбивств для переходу, поразка від стіни/ворога/здоровʼя, 16 героїв, старт з 3, платформи.
- [Pocket Gamer: Nimble Quest review](https://www.pocketgamer.com/nimble-quest/nimble-quest-review/) — свайп = поворот, кінець від краю/ворога/власного хвоста, ближні краще спереду, баффи, Arena.
- [Steam: Nimble Quest](https://store.steampowered.com/app/259780/) — опис, гільдії й Guild Quests.
- [Wikipedia: MageTrain](https://en.wikipedia.org/wiki/MageTrain) і [Pocket Gamer: запуск MageTrain](https://www.pocketgamer.com/magetrain/official-launch-android-ios/) — позиція в поїзді, 9 героїв, 8 підземель, 30 навичок, розгалужені забіги.
- [Wikipedia: Snake Core](https://en.wikipedia.org/wiki/Snake_Core) — солдати з автострільбою, стіни вбивають, вузлова мапа.
- YouTube: пошук «Nimble Quest gameplay».

## Непевне
- (?) Чи рух прив'язаний до клітинної сітки (повороти під прямим кутом — так, але снеп до клітин — не бачив); `field: square` — припущення.
- (?) Що відбувається, коли гине окремий герой (випадає з ланцюга?) і як рахується «здоровʼя загону»; що саме роблять бомба й лід.
- (?) Кількість героїв: Wikipedia — 16, Pocket Gamer — 15.
- (?) Розміри квот, ціни жетонів, керування на Steam, склад HUD.
- (?) Які саме здібності дає кожна позиція в MageTrain — джерела не називають.
