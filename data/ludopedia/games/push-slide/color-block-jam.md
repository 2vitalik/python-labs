---
title: Color Block Jam
slug: color-block-jam
aka: [Color Block Jam (Rollic), Колірний блок-джем]
family: push-slide
also: []
klass: figure
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: none
  goal: state
year: null
platforms: [iOS, Android]
links:
  - {kind: other, url: "https://rollic.helpshift.com/hc/en/24-color-block-jam/faq/1234-obstacles-in-color-block-jam/", best: true, note: "офіційний FAQ: 38 перешкод і їхня поведінка — найповніший опис механіки"}
  - {kind: official, url: "https://apps.apple.com/us/app/color-block-jam/id6504332779", note: "App Store: «Slide the blocks to match them with the colored doors», таймер, нові блокери; відгуки — 5 життів, бустери, монети"}
  - {kind: other, url: "https://rollic.helpshift.com/hc/en/24-color-block-jam/faq/1222-how-do-i-play-color-block-jam", note: "як грати: мета, програш (час / блок без дверей) → мінус життя, поповнення життів"}
  - {kind: other, url: "https://rollic.helpshift.com/hc/en/24-color-block-jam/faq/1232-what-is-a-booster-what-are-they-for/", note: "4 бустери: Time Freeze, Hammer, Rocket, Color Vacuum"}
  - {kind: other, url: "https://rollic.helpshift.com/hc/en/24-color-block-jam/", note: "довідка: події (Leaderboard, Rainbow Fest, Daily Quest), Block Collection, Captain Stu, профіль, налаштування"}
  - {kind: other, url: "https://www.bluestacks.com/apps/puzzle/color-block-jam-on-pc.html", note: "Android-пакет com.GybeGames.ColorBlockJam, «hundreds of levels»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Color+Block+Jam+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [multi-cell-size, impassable-cells, drag-drop-piece, time-out, key-and-door, button-toggle, hidden-under-block, move-limit, collect-all, sequential-levels, round-currency, shop-window, leaderboard, game-settings, sound-effects, music-toggle, avatar-picker, save-progress, +color-exit-door, +exit-triggered-toggle, +clear-countdown-lock, +multi-hit-block, +color-filter, +booster-items, +lives-energy, +rewarded-ad, +time-pickup, +linked-blocks, +daily-quests, +collection-album, +reward-wheel]
proposes: ["+trigger:exited", "+effect:exit", "+effect:toggle_state", "+cond:width_fits", "+role:door", "+feature:boosters", "+feature:lives-regen", "+feature:rewarded-ad", "+feature:daily-quests", "+feature:collection-album", "+window:event-window", "+window:reward-wheel", "+ui:booster-bar", "+card:color-exit-door", "+card:exit-triggered-toggle", "+card:clear-countdown-lock"]
author: opus
date: 2026-11-09
---

# Color Block Jam — тягни кольорові блоки-поліоміно крізь затор до дверей свого кольору, поки не скінчився час

## Суть
Мобільна «jam»-головоломка: на дошці тісно стоять кольорові блоки різної форми, по краях — кольорові двері. Гравець тягне блок пальцем; блок, підведений до дверей **свого кольору**, виходить з поля й «подрібнюється». Мета — вивести всі блоки до кінця таймера, а порядок ходів вирішує все: блоки заважають один одному. Ядро швидко обростає **десятками перешкод** (лід, мотузки, бомби, двері, що перемикаються після кожного виходу), тож це радше «Unblock Me з кольоровими виходами + конструктор правил».

## Поле і час
- Квадратна сітка зі стінами довільної форми; двері — відрізки на межі поля, кожні двері мають колір (і ширину — див. Size-Changing Door) (?).
- Блоки — поліоміно з кількох клітин; рухаються лише вільними клітинами, крізь інші блоки й стіни не проходять.
- Час іде в реальному часі (зворотний відлік рівня); саме поле змінюється лише від дій гравця та від подій «блок вийшов» (на них реагує більшість перешкод).
- Частина вмісту схована: блоки під ящиками, льодом, ланцюгами, мотузками; «приховані блоки» невидимі, доки не прибрано певний видимий блок → `info: partial`.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кольоровий блок | piece | колір, форма-поліоміно | тягнеться пальцем по вільних клітинах; виходить крізь двері свого кольору |
| Двері | gate | колір, ширина (?) | пропускають лише блоки свого кольору |
| Стіна | static | — | непрохідна |
| Arrow (блок-стрілка) | piece | напрямок | рухається лише у вказаному напрямку |
| Turn Based Arrow | piece | число N, напрямок | заблокована, доки не вийде N блоків; потім лише вздовж своєї осі в обидва боки |
| Layer (шаровий блок) | piece | шари кольорів | знімається по шару, зовнішній — першим |
| Color-Switching Block | piece | зовнішній і внутрішній колір | вихід блока кольору зовнішнього шару знімає шар; вихід іншого кольору міняє шари місцями |
| Combined (зчеплені) | piece | 2 частини | спершу треба прибрати одну частину, щоб розʼєднати |
| Combined Locked Blocks | piece | 2 частини | не пройдуть двері навіть свого кольору, доки інші блоки не розірвуть звʼязок проходами |
| Star (зірковий блок) | piece | — | виходить лише крізь зіркові двері; звичайні блоки теж можуть ними виходити |
| Moving Blocks | object | — | рухаються вільно (якщо не замкнені/звʼязані/прикручені), але вийти не можуть — лише заважають |
| Color Swapping Blocks | piece | — | рухаються як звичайні; вихід міняє кольори блоків на полі |
| Ice (крижаний блок) | piece | лічильник N | заморожений, доки з поля не вийде N інших блоків |
| Chained Blocks | piece | потрібна кількість ключів | нерухомі, доки не прибрано потрібну кількість блоків-ключів |
| Ropes + Scissors | piece | колір ножиць | блок у мотузках застряг; вихід ножиць того ж кольору перерізає мотузку |
| Bomb | hazard | таймер | вибухає (поразка), якщо її не прибрати вчасно (?) |
| Dynamite | hazard | ліміт ходів N | треба вивести за N ходів; рух іншого блока понад ліміт — вибух і кінець рівня |
| Crate | container | — | ховає вміст (блок або бомбу); відкривається після прибирання потрібних блоків |
| Moveable Crate | container | число N | −1 за кожен прохід крізь двері; на 0 зникає й відкриває блок під собою |
| Flower Crate | container | листки | рухається як блок; відмикається, коли прибрано повʼязані «світні листки»; ховає блоки, бомби тощо |
| Colorful Crate | container | колір | зникає, коли з поля прибрано всі блоки його кольору |
| Hidden Blocks | piece | — | невидимі, доки не прибрано певний видимий блок; відкритий блок теж треба вивести |
| Elevator | container | стос із N блоків | зверху один блок; вивів верхній — підіймається наступний |
| Time Capsule | pickup | +10 / +15 с | блок; вихід крізь двері свого кольору додає час |
| Door (що відчиняється) | gate | стан | відчиняється/зачиняється після кожного прибраного блока |
| Iced Door | gate | лічильник N | замкнені льодом, доки не вийде N блоків |
| Locked Door | gate | колір ланцюга | відмикаються, коли блоки-ключі пройдуть двері відповідного кольору |
| Colorful Door | gate | черга кольорів | пропускає один колір; після проходу показує наступний потрібний |
| Size-Changing Door | gate | розмір | звужується/розширюється після кожного прибраного блока; розмір вирішує, що пройде |
| Moving Door Lock | gate | напрямок | замок переїжджає на наступні двері в заданому напрямку |
| Jumping Single Door | gate | — | закриває одне місце виходу й перестрибує на нове після кожного проходу |
| Colorful Jumping Door | gate | — | перестрибує після кожного прибраного блока й перефарбовує двері, на які впав |
| Curtain | gate | відкрита/закрита | вихід лише при відкритій завісі; перемикається після кожного проходу будь-якого блока; блоки на полі рухаються далі |
| Color-Switcher | gate | 2 кольори | після кожного проходу перемикає колір; пройде лише блок поточного кольору |
| Button Doors | switch | колір кнопки | двері відчиняються, коли на кнопку поставлено блок того ж кольору |
| Laser Door | gate | лазер → приймач | відчинені, лише поки промінь дістає приймача; перекрив — зачинились |
| Barrier | gate | — | відкривається/закривається після кожного прибраного блока, відкриваючи чи перекриваючи шляхи |
| Colorful Path | terrain | колір | ним можуть їхати лише блоки цього кольору |
| Colorful Moving Path | terrain | колір | зсувається, коли на нього заїжджає блок, змінюючи розкладку поля |
| Ivy (плющ) | terrain | розмір | перекриває ділянку; кожен прохід крізь двері зменшує на 1 клітину |
| Magnet Block | piece | колір | зʼєднується з магнітом того ж кольору при правильному вирівнюванні й відмикає шлях (?) |
| Rainbow Block | piece | — | (подія з рівня 200) випадковий блок отримує право пройти будь-які двері |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag)` → ЯКЩО `path_exists(block, cell)` → ТО `move(block, cell)` — блок їде за пальцем вільними клітинами (?).
- КОЛИ `input(drag)` → ЯКЩО `state(block, frozen|chained|roped)` → ТО `block`.
- КОЛИ `input(drag)` → ЯКЩО `custom: «блок — Arrow»` і `not moving(block, arrow_dir)` → ТО `block`.
- КОЛИ `contact(block, door)` → ЯКЩО `same(block, door, color)` і `custom: «блок вміщується в розмір дверей»` → ТО `custom: «блок виходить крізь двері»`, `disappear`; інакше `block`.
- КОЛИ `custom: «будь-який блок вийшов»` → ТО `custom: «перемкнути Door / Curtain / Barrier / Color-Switcher, перестрибнути Jumping Door, зсунути Moving Door Lock, змінити Size-Changing Door»`.
- КОЛИ `custom: «будь-який блок вийшов»` → ТО `counter(ice, -1)`, `counter(iced_door, -1)`, `counter(moveable_crate, -1)`, `counter(ivy, -1)`, `counter(turn_arrow, -1)`.
- КОЛИ `counter(ice, =, 0)` → ТО `clear_state(block, frozen)` · КОЛИ `counter(iced_door, =, 0)` → ТО `set_state(door, open)`.
- КОЛИ `counter(moveable_crate, =, 0)` → ТО `disappear`, `reveal(cell)` (блок під ящиком).
- КОЛИ `custom: «вийшли ножиці кольору c»` → ТО `clear_state(blocks_of_c, roped)`.
- КОЛИ `custom: «ключові блоки пройшли двері свого кольору»` → ЯКЩО `counter(keys, >=, n)` → ТО `clear_state(target, chained)`.
- КОЛИ `custom: «вийшов зовнішній шар Layer-блока»` → ТО `transform(block, inner_layer)`.
- КОЛИ `custom: «прохід блока іншого кольору»` → ЯКЩО `custom: «блок — Color-Switching»` → ТО `custom: «поміняти зовнішній і внутрішній колір»`.
- КОЛИ `custom: «вийшов Color Swapping Block»` → ТО `custom: «поміняти кольори блоків на полі»`.
- КОЛИ `custom: «вийшла Time Capsule»` → ТО `timer(+n)`.
- КОЛИ `enter(block, button)` → ЯКЩО `same(block, button, color)` → ТО `set_state(button_door, open)`.
- КОЛИ `custom: «промінь лазера перекрито»` → ТО `set_state(laser_door, closed)`; відкрито — `set_state(laser_door, open)`.
- КОЛИ `enter(block, colorful_path)` → ЯКЩО `not same(block, colorful_path, color)` → ТО `block`.
- КОЛИ `custom: «прибрано певний видимий блок»` → ТО `reveal(hidden_block)`.
- КОЛИ `custom: «прибрано всі блоки кольору c»` → ТО `disappear` (Colorful Crate), `reveal(cell)`.
- КОЛИ `input(drag)` → ЯКЩО `custom: «рухається не Dynamite»` → ТО `counter(dynamite, -1)`; КОЛИ `counter(dynamite, =, 0)` → ТО `explode`, `lose`.
- КОЛИ `all_gone(block)` → ТО `win`, `currency(+n)`, `next_level`.
- КОЛИ `counter(time, =, 0)` → ТО `lose`, `lives(-1)`.
- КОЛИ `custom: «на полі блок, для якого не лишилось дверей його кольору»` → ТО `lose`, `lives(-1)`.
- Перемога: усі блоки виведено до кінця таймера. · Поразка: вийшов час, блок без можливих дверей, вибух бомби/динаміту → мінус життя. · Рахунок: монети за рівень, очки рівнів для лідерборду.

## Керування і ввід
- Тач: затиснути блок і тягнути; блок іде за пальцем, упираючись у перешкоди (тому `klass: figure`, як Rush Hour).
- Бустер: тап по кнопці бустера → тап по цілі (блок / колір) (?).
- Undo нема (у джерелах не згадано) — помилку виправляє лише рестарт або бустер.

## Вікна, меню, HUD
- `game-screen`: поле з дверима; HUD — `timer-countdown`, `level-number`, `+booster-bar` (Time Freeze, Hammer, Rocket, Color Vacuum), `pause-button`.
- `main-menu` (головний екран): кнопка наступного рівня (?), `lives` з відліком відновлення, `coins`, входи в події.
- `end-screen`: перемога — монети, подвоєння за рекламу (відгук); поразка — `game-over-continue`: купити час за монети / втратити життя.
- `shop-window`: монети, набори, «No Ads Bundle».
- `settings-window`: звук, музика, вібрація, сповіщення.
- `profile-window`: імʼя, аватар, рамка; Elephant ID / Player ID.
- `leaderboard`: глобальна таблиця на обмежений період.
- `daily-window`: Daily Quest — набір завдань на добу.
- `+event-window`: Captain Stu (маршрут до корабля), Rainbow Fest, Canyon Chase (відгук).
- `+reward-wheel`: колесо Captain Stu — 8 слотів; дерево (етапи 1–3) / бронза (4–6) / срібло (7–9) / золото (10).
- `custom-window`: Block Collection — коробки, блоки з рідкістю 1–5 зірок, альбоми, головний приз.
- Переходи: головний → `game-screen` → `end-screen` → головний; без життів — `confirm-dialog`/`shop-window` (поповнити).

## Фічі поза полем
- `+feature:lives-regen`: до 5 життів, відновлюються з часом; поповнити за монети або 1 життя за рекламу.
- `+feature:boosters`: Time Freeze — зупиняє відлік і дає +10 с; Hammer — розбиває один блок або зменшує вимогу перешкоди на 1; Rocket — розбиває обраний блок; Color Vacuum — прибирає всі блоки обраного кольору. Розділ «Pre-Boosters» є в довідці, вміст не описано (?).
- `levels-sequential` (нумеровані рівні, «hundreds of levels»), нові рівні з оновленнями; кожен рівень можна пройти без бустерів (FAQ).
- Події: `leaderboard-online` (очки за пройдені рівні, періодичне скидання), `+feature:daily-quests`, Rainbow Fest (Rainbow Block з рівня 200, активація після 10 перемог), Captain Stu з колесом, `+feature:collection-album` (Block Collection з рівня 63).
- `save-progress` / `cloud-save` між пристроями; переривання дзвінком перезапускає рівень (заголовок FAQ).
- Монетизація: `+feature:rewarded-ad`, покупки монет, реклама.

## Варіації й родичі
- Найближчий родич у корпусі — `unblock-me` / `rush-hour` (затор поліоміно, вихід крізь отвір), але тут виходів багато й вони кольорові; `klotski` — без кольорів.
- Клони жанру «Color Block Jam / Block Jam» — масові мобільні копії від інших студій (?).
- **Осі варіацій**:
  - **хто може вийти**: один «головний» блок (Rush Hour) / кожен блок у двері свого кольору (тут) / за порядком (Colorful Door);
  - **як рухається блок**: лише вздовж осі (Rush Hour) / вільно за пальцем (тут) / лише вперед (Arrow);
  - **що реагує на вихід**: нічого / лічильники (лід, ящики, плющ) / перемикачі (двері, завіса, барʼєр);
  - **обмеження**: без ліміту / таймер (тут) / ліміт ходів (Dynamite).

## Цікавинки для курсу
- Рух поліоміно за пальцем з перевіркою колізій усіма клітинами фігури — 🥉.
- Вихід крізь двері: колір + «чи вміщується» фігура в отвір + напрям виходу — 📎.
- Подієва шина «блок вийшов» → десяток підписників (лічильники, перемикачі, стрибаючі двері) — 🥈 (гарний урок patterns Observer/таблиця реакцій).
- Шаровий і двоколірний блок (стек кольорів, swap) — 🌱.
- Приховані вмісти (ящики, елеватор, приховані блоки) — 📎.
- Життя з відновленням за реальним часом, бустери, монети — 🥉 (економіка поза полем).
- Перевірка «блок без можливих дверей» як ранній програш — 🥈 (аналіз досяжності з урахуванням майбутніх змін).

## Мапа на каталог
- Є: `multi-cell-size` ↔ блоки-поліоміно; `impassable-cells` ↔ стіни; `drag-drop-piece` ↔ перетягування; `time-out` ↔ таймер; `key-and-door` ↔ Locked Door і ключові блоки; `button-toggle` ↔ Button Doors; `hidden-under-block` ↔ Crate / Moveable Crate; `move-limit` ↔ Dynamite; `collect-all` ↔ вивести всі блоки; `sequential-levels`; `round-currency` ↔ монети; `shop-window`; `leaderboard`; `game-settings` + `sound-effects` + `music-toggle`; `avatar-picker` ↔ профіль; `save-progress`.
- **Нема** → пропозиції карток:
  - `+color-exit-door` «Блок виходить крізь двері свого кольору (і розміру)» · entities/interact · 📎.
  - `+exit-triggered-toggle` «Перешкоди перемикаються/стрибають після кожного виходу блока» · entities/state · 🥉 · слот {kind: toggle|jump|shift|resize}.
  - `+clear-countdown-lock` «Замок знімається після N прибраних обʼєктів» (лід, крижані двері, плющ, Turn Based Arrow) · entities/state · 🌱.
  - `+multi-hit-block` (уже пропонована) ↔ Layer; `+color-filter` (уже пропонована) ↔ Colorful Path.
  - `+linked-blocks` «Зчеплені блоки, що розʼєднуються умовою» · entities/legality · 📎.
  - `+time-pickup` «Обʼєкт додає час до таймера» · game-logic/score · 🌱.
  - `+booster-items`, `+lives-energy`, `+rewarded-ad`, `+daily-quests`, `+collection-album`, `+reward-wheel` — мобільна мета-економіка.

## Пропозиції до словників
- `+trigger:exited` — сутність покинула поле через вихід (тут — тригер для половини перешкод; Unblock Me).
- `+effect:exit` — сутність виходить з поля крізь двері (≠ `disappear`: є напрям і місце).
- `+effect:toggle_state` — перемкнути двостанову сутність (двері, завіса, барʼєр) без явного стану.
- `+cond:width_fits` — фігура проходить у отвір заданої ширини (`fits` — про вміщення в клітини поля).
- `+role:door` — вихід з поля з фільтром (колір), відмінний від `gate` всередині поля.
- `+feature:boosters`, `+feature:lives-regen`, `+feature:rewarded-ad`, `+feature:daily-quests`, `+feature:collection-album`.
- `+window:event-window` — екран тимчасової події; `+window:reward-wheel` — колесо нагород.
- `+ui:booster-bar` — ряд кнопок бустерів на ігровому екрані.
- `+card:color-exit-door`, `+card:exit-triggered-toggle`, `+card:clear-countdown-lock` — див. вище.

## Джерела
- ⭐ [Rollic FAQ: Obstacles in Color Block Jam](https://rollic.helpshift.com/hc/en/24-color-block-jam/faq/1234-obstacles-in-color-block-jam/) — 38 елементів (Arrow, Layer, Ice, Star, Combined, Chained, Door, Bomb, Ropes, Iced Door, Moving Door Lock, Colorful Path, Crate, Moving Blocks, Colorful Door, Locked Door, Size-Changing Door, Combined Locked, Hidden, Dynamite, Curtain, Moveable Crate, Color-Switcher, Time Capsule, Color-Switching Block, Jumping Single Door, Flower Crate, Color Swapping Blocks, Barrier, Colorful Jumping Door, Colorful Crate, Colorful Moving Path, Button Doors, Turn Based Arrow, Ivy, Elevator, Laser Door, Magnet Block).
- [App Store](https://apps.apple.com/us/app/color-block-jam/id6504332779) — опис, Rollic Games, iOS 15+; відгуки: 5 життів, rainbow і vacuum, монети, «canyon chase», «daily challenge».
- [FAQ: How do I play](https://rollic.helpshift.com/hc/en/24-color-block-jam/faq/1222-how-do-i-play-color-block-jam) — мета, поразка (час або блок без дверей) → мінус життя, поповнення до 5, сховані під ящиками/льодом/ланцюгами/мотузками.
- [FAQ: Boosters](https://rollic.helpshift.com/hc/en/24-color-block-jam/faq/1232-what-is-a-booster-what-are-they-for/) — 4 бустери з ефектами.
- [Довідковий центр](https://rollic.helpshift.com/hc/en/24-color-block-jam/) і статті Leaderboard, Daily Quest, Rainbow Fest, Block Collection, Captain Stu Reward Wheel, Tips for Hard Levels.
- [BlueStacks](https://www.bluestacks.com/apps/puzzle/color-block-jam-on-pc.html) — пакет Android, «Slide-and-Match Gameplay».

## Непевне
- (?) Рік виходу: перша версія в історії App Store — 1.45.0 «Jun 25» без року; сторонній сайт каже 2025 (лютий/березень) — не підтверджено.
- (?) Чи блок за пальцем повертає кути, чи рух лише по прямій; чи важлива ширина дверей для звичайних (не Size-Changing) дверей.
- (?) Як саме працює Bomb (таймер у секундах чи в ходах) і Magnet Block — FAQ описує одним реченням.
- (?) «близько хвилини на рівень», ціни бустерів (1900 монет), «900 points» — лише з відгуків.
- (?) Вміст Pre-Boosters, наявність кнопки паузи і точний склад HUD — не бачив скріншотів.
