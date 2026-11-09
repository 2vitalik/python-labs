---
title: Bao la Kiswahili (Бао)
slug: bao-la-kiswahili
aka: [Бао, Bao, Bau, Bao Ki Swahili, Mraha wa Tso, Bao la kujifunza]
family: chess-abstract
also: []
klass: cursor
axes:
  field: graph
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: state
year: 1820
platforms: [board, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bao_(game)", best: true, note: "правила: дошка 4×8, kichwa/kimbi/nyumba, фази namua і mtaji, естафетний розсів, takata, правила дому, кінець, Bao la kujifunza"}
  - {kind: other, url: "https://ludii.games/details.php?keyword=Bao%20Kiswahili%20(East%20Africa)", note: "Ludii: формалізовані правила (.lud), обмеження на одиночні лунки, джерела Sanderson 1913, Townshend 1986, Murray 1951"}
  - {kind: play, url: "https://boardgamearena.com/", note: "BGA — Bao онлайн (живі й покрокові партії); за зовнішніми лінками Wikipedia, сторінку гри не відкривав"}
  - {kind: other, url: "http://www.kibao.org", note: "KIBA — італійська асоціація: кореспонденційні партії й турніри (лінк зі статті, не відкривав)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Bao+la+Kiswahili+rules", note: "пошук; пояснення правил"}
stage: v1
coverage: 50
mechanics: [cell-click, hover-highlight, legal-move-highlight, last-move-highlight, movement-animation, turn-enforcement, hot-seat, ai-opponent, online-multiplayer, async-multiplayer, pocket, chain-reaction, rule-variants, mode-indicator, move-notation, state-as-data, game-screen, help-window, end-screen, +sowing, +relay-sowing, +opposite-pit-capture, +capture-resow, +must-capture-legality, +two-phase-game, +special-house-pit, +sowing-direction-choice]
proposes: ["+effect:sow", "+trigger:sown", "+cond:last_in(cell)", "+cond:can_capture", "+cond:marker(pit)", "+ui:pit-counts", "+ui:direction-picker", "+window:safari-choice", "+card:relay-sowing", "+card:opposite-pit-capture", "+card:capture-resow"]
author: opus
date: 2026-11-09
---

# Bao la Kiswahili — манкала 4×8: захоплене не йде в комору, а пересівається з «голови» ряду, і розсів біжить естафетою

## Суть
Найскладніша з поширених манкал, гра суахілі (Танзанія, Занзібар, Кенія). Кожен гравець має два ряди по 8 лунок і 32 насінини; на початку більшість насінин «у руці», і перша фаза — кладення по одній з руки. Захоплені насінини **не виходять з гри**: їх одразу пересівають на свою половину, починаючи з крайньої лунки kichwa, а розсів продовжується естафетою, доки остання насінина не впаде в порожню лунку. Програє той, у кого спорожнів внутрішній ряд або нема ходу; спільне ядро розсіву — у [oware.md](oware.md).

## Поле і час
- Дошка 4×8: кожному — два ближні ряди (зовнішній і внутрішній). Розсів іде **кільцем по 16 лунках своєї половини** (два ряди), у чужу половину насінини не потрапляють.
- Звʼязок між половинами — лише «навпроти»: лунка свого внутрішнього ряду дивиться на лунку внутрішнього ряду суперника → тому `field: graph` (два кільця + ребра «навпроти»).
- Особливі лунки внутрішнього ряду: **kichwa** (крайні), **kimbi** (kichwa + сусідні до них; деякі джерела — без самих kichwa), **nyumba** (4-та справа, зазвичай квадратна).
- Старт: у nyumba 6, у двох лунках поруч з нею з одного боку — по 2; решта 22 насінини — в руці (nemo). Малаві: 8 у nyumba, 20 у руці.
- Дві фази: **namua** (поки є насінини в руці) → **mtaji** (рука порожня). Хід за ходом, випадковості нема, усе відкрито.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Лунка (shimo) | container | власник, ряд (внутр./зовн.), кількість | джерело і ціль розсіву у своєму кільці з 16 |
| Kichwa («голова») | container | 2 на гравця, краї внутрішнього ряду | з неї починається розсів захоплених: з правої — проти годинникової, з лівої — за годинниковою |
| Kimbi | zone | kichwa + сусідні лунки | захоплення тут — розсів з найближчої kichwa, без вибору |
| Nyumba («дім») | container | 4-та справа у внутрішньому ряду; функціональна / звичайна | податок 2 насінини, зупинка takata, safari-вибір; втрачає статус назавжди |
| Маркер | zone | лунка свого внутрішнього ряду навпроти непорожньої лунки суперника | остання насінина тут → захоплення (у ході mtaji) |
| Насінина (kete) | object | 32 на гравця, 64 разом | переходить між лунками; захоплена — змінює власника, але лишається на дошці |
| Рука (nemo) | supply | 22 на старті | по одній на поле у фазі namua |

## Правила (КОЛИ → ЯКЩО → ТО)
Фаза namua (є насінини в руці):
- КОЛИ `input(pit)` → ЯКЩО `turn_of(side)` and `custom: «у руці є насінини»` and `custom: «лунка свого внутрішнього ряду непорожня»` → ТО `place(seed, pit)` з руки.
- КОЛИ `after(place)` → ЯКЩО `custom: «лунка — маркер»` → ТО хід **mtaji**: `custom: «забрати всі насінини з лунки суперника навпроти»` і сіяти їх з kichwa.
- КОЛИ `turn_start(side)` → ЯКЩО `custom: «є хід із захопленням»` → ТО `custom: «легальні лише захоплювальні ходи»` (захоплювати обовʼязково).
- КОЛИ `after(place)` → ЯКЩО `custom: «лунка не маркер»` → ТО хід **takata**: `custom: «весь вміст лунки сіється в обраному напрямку»`, захоплень цього ходу не буде.
- КОЛИ `input(pit)` → ЯКЩО `custom: «у лунці 1 насінина, а в ряду є лунки з кількома»` → ТО `block` (Ludii).
Захоплення й естафета (обидві фази):
- КОЛИ `custom: «захоплення»` → ЯКЩО `custom: «захоплено в kimbi»` → ТО `custom: «сіяти з найближчої kichwa»`; інакше першого разу за хід `choose(kichwa)`; з правої — проти годинникової, з лівої — за годинниковою.
- КОЛИ `custom: «остання насінина впала в маркер»` → ЯКЩО `custom: «хід mtaji»` → ТО нове захоплення: kimbi → найближча kichwa; інакше `custom: «з kichwa в поточному напрямку, без вибору»` (`chain(n)`).
- КОЛИ `custom: «остання насінина впала в непорожню лунку, захоплення нема»` → ТО `custom: «забрати весь вміст і сіяти далі в тому ж напрямку»` (естафета; у takata маркери — звичайні лунки).
- КОЛИ `custom: «остання насінина впала в порожню лунку»` → ТО `end_turn`.
Nyumba (лише Bao la Kiswahili, поки функціональна):
- КОЛИ `input(nyumba)` → ЯКЩО `custom: «фаза namua, хід takata, починається з nyumba»` → ТО `custom: «сіється лише 2 насінини»` (податок).
- КОЛИ `custom: «takata-розсів закінчився в nyumba»` → ТО `end_turn` (без естафети).
- КОЛИ `custom: «mtaji-розсів закінчився в nyumba, що не маркер»` → ТО `choose(continue|stop)` — продовжити естафету з дому (safari) або закінчити хід.
- КОЛИ `custom: «весь вміст nyumba вперше розсіяно естафетою в ході mtaji»` або `custom: «суперник захопив nyumba»` → ТО `set_state(nyumba, ordinary)` назавжди; податок статусу не знімає.
Фаза mtaji (рука порожня):
- КОЛИ `input(pit, dir)` → ЯКЩО `custom: «у руках нема насінин»` and `count(seeds_in_pit, >=, 2)` → ТО `custom: «забрати всі й сіяти в обраному напрямку»`.
- КОЛИ `custom: «перший розсів закінчився в маркері»` → ТО хід mtaji з тими самими правилами захоплення; захоплювати обовʼязково.
- КОЛИ `custom: «захоплення неможливе»` → ТО хід takata; ЯКЩО `custom: «є легальний старт із внутрішнього ряду»` → ТО `custom: «стартувати лише з внутрішнього ряду»`.
- КОЛИ `input(pit)` → ЯКЩО `count(seeds_in_pit, >, 15)` → ТО `custom: «розсів обходить обидва ряди й повертається до старту; хід завжди takata»`.
Кінець:
- КОЛИ `custom: «внутрішній ряд гравця порожній»` → ТО `lose`.
- КОЛИ `no_moves(side)` → ТО `lose`.
- Перемога: суперник без насінин у внутрішньому ряду або без ходу · Рахунку нема.

## Керування і ввід
- Дошка: рука бере насінини з лунки й розкладає по одній; напрямок і kichwa обирає гравець.
- Цифрова версія: клік по лунці → вибір напрямку стрілками біля лунки (`+ui:direction-picker`); при захопленні поза kimbi — клік по лівій/правій kichwa; у safari — діалог «продовжити / зупинитись».
- Анімація естафети по одній насінині, підсвітка маркерів і захоплених лунок.

## Вікна, меню, HUD
- (цифрова версія — BGA, Ludii; не відкривав)
- `main-menu`: гра з людиною / AI / онлайн, правила.
- `match-setup`: варіант (kiswahili / kujifunza / малавійський), хто ходить першим, AI-рівень, покрокова чи жива партія.
- `game-screen`: 4×8 лунок з числами (`+ui:pit-counts`), `pocket` — насінини в руці обох, `turn-indicator`, індикатор фази namua/mtaji і типу ходу mtaji/takata (`mode-indicator`), позначка функціональної nyumba, `legal-move-highlight`, `last-move-highlight`.
- `custom-window` / `+window:safari-choice` — продовжити естафету з дому чи ні; вибір kichwa.
- `help-window` — правила з анімацією естафети.
- `end-screen` — хто спорожнив внутрішній ряд суперника.
- `lobby-window` — онлайн і кореспонденційні турніри (KIBA).
- Переходи: main-menu → match-setup → game-screen ⇄ safari-choice → end-screen.

## Фічі поза полем
- `online-multiplayer`: BGA (живі й покрокові партії); кореспонденційні матчі й турніри KIBA.
- `ai-opponent-levels`: програма Jeroen Donkers для занзібарської версії (архівний лінк Wikipedia).
- `custom-rules`: Bao la kujifunza, малавійська розстановка, варіанти правил дому.
- Реальні турніри: Танзанія, Занзібар, Ламу (Кенія), Малаві; товариство Chama cha Bao (1966).

## Варіації й родичі
- **Bao la kujifunza** («Бао для початківців»): усі 64 насінини по 2 в кожній лунці, фази namua нема — одразу mtaji, правил nyumba нема.
- **Малаві (Bawo)**: 8 у nyumba, 20 у руці.
- Варіанти дому: податок лише коли нема іншого легального старту; естафета з дому в mtaji обовʼязкова.
- Родичі: **Hawalis** (Оман; на Занзібарі — Bao la kiarabu), **Omweso** (Уганда), **Isolo** (Танзанія) — подібне спорядження; [oware.md](oware.md) — дворядна манкала з коморою; [togyzkumalak.md](togyzkumalak.md) — туздик.
- **Осі варіацій** (манкала): рядів 2 / 4 · розсів однокруговий / естафетний · захоплене → комора / пересів на свою половину · умова захоплення: 2–3 (Oware) / маркер навпроти (Bao) / парне (Togyzkumalak) · фази: одна / з рукою · кінець: рахунок / порожній ряд.

## Цікавинки для курсу
- Дві половини як два кільця по 16 + ребра «навпроти» для внутрішніх рядів — 🌱.
- Естафетний розсів з перевіркою маркера й зупинкою на порожній лунці — 📎.
- Захоплення з пересівом із kichwa: правило kimbi, вибір напрямку лише першого разу, далі напрямок фіксований — 🥉.
- Машина станів ходу: фаза namua/mtaji × тип mtaji/takata × стан nyumba (функціональна/звичайна) — 🥈.
- Фільтр «захоплювати обовʼязково» через симуляцію кожного старту — 📎.
- AI для Bao: довгі естафети й обовʼязкові захоплення, оцінка за внутрішнім рядом — 🥇.

## Мапа на каталог
- Є: `cell-click` · `hover-highlight` · `legal-move-highlight` · `last-move-highlight` · `movement-animation` (насінини по одній) · `turn-enforcement` · `hot-seat` · `ai-opponent` · `online-multiplayer` / `async-multiplayer` (BGA, KIBA) · `pocket` (насінини в руці) · `chain-reaction` (захоплення ланцюгом в одному ході) · `rule-variants` · `mode-indicator` (фаза й тип ходу) · `move-notation` · `state-as-data` (64 числа + рука) · `game-screen` / `help-window` / `end-screen`.
- **Нема** → пропозиції карток:
  - `+relay-sowing` «Естафетний розсів» · entities/state · 📎 · слоти {stop_on: empty, continue_from: last_pit}.
  - `+opposite-pit-capture` «Захоплення лунки навпроти» · entities/combat · 🌱 · слоти {needs: own_nonempty|marker}.
  - `+capture-resow` «Захоплене пересівається на свою половину» · entities/combat · 🥉 · слоти {entry: end_pit, direction_rule}.
  - `+two-phase-game` «Фаза з руки → фаза на полі» · game-logic/opponent · 📎 (Bao, Nine Men's Morris).
  - `+special-house-pit` «Лунка з власними правилами, що втрачає статус» · entities/state · 📎.
  - `+sowing-direction-choice` — напрямок розсіву за вибором гравця.
  - `+sowing` (oware.md), `+must-capture-legality` (reversi.md).

## Пропозиції до словників
- `+effect:sow(pit, dir)` — розсіяти вміст по одній (спільне з Oware).
- `+trigger:sown` — розсів завершився (точка перевірки маркера/естафети).
- `+cond:last_in(cell)` — остання насінина впала в лунку виду (маркер, порожня, nyumba).
- `+cond:can_capture` — у гравця є хід із захопленням (обовʼязкове взяття).
- `+cond:marker(pit)` — своя лунка внутрішнього ряду навпроти непорожньої лунки суперника.
- `+ui:pit-counts` — числа над лунками; `+ui:direction-picker` — вибір напрямку руху/розсіву стрілками біля клітини.
- `+window:safari-choice` — модальний вибір «продовжити естафету з дому чи ні».
- `+card:relay-sowing` · `+card:opposite-pit-capture` · `+card:capture-resow`.

## Джерела
- ⭐ [Wikipedia: Bao (game)](https://en.wikipedia.org/wiki/Bao_(game)) — розділи Equipment, Setup, Namua, Capture and sowing, Mtaji phase, The nyumba, End; історія (Hyde 1658/1694, вірш Muyaka 1820-х, дошка ≥1896); Bao la kujifunza; зовнішні лінки (BGA, KIBA, Donkers, de Voogt).
- [Ludii: Bao Kiswahili (East Africa)](https://ludii.games/details.php?keyword=Bao%20Kiswahili%20(East%20Africa)) — формальні правила: заборона класти в одиночну лунку, квадратна лунка лише 2 насінини, перемога — спорожнити внутрішній ряд суперника; джерела.
- [BGA](https://boardgamearena.com/) — онлайн-гра (за статтею).
- [KIBA](http://www.kibao.org) — кореспонденційні турніри (за статтею).
- YouTube: пошук «Bao la Kiswahili rules».

## Непевне
- (?) Що саме сіється в takata-ході namua: Wikipedia лише каже, що естафета відбувається; Ludii — «сіяти в будь-якому напрямку» після кладення. Записано «весь вміст лунки в обраному напрямку».
- (?) Податок nyumba: Wikipedia — «якщо хід починається з nyumba, сіються 2», Ludii — «якщо nyumba — єдина зайнята лунка внутрішнього ряду»; формулювання різні.
- (?) Чи можливі нескінченні естафети і як їх обмежують — у джерелах не знайшов.
- (?) `year: 1820` — умовно: вірш Muyaka bin Haji про Bao (1820-ті); Hyde бачив гру на Анжуані 1658 (опубліковано 1694), але звʼязок із сучасним Bao непевний.
- (?) Інтерфейс BGA і програми Donkers — не відкривав; вікна «(цифрова версія)».
- (?) Ludii-сторінка через підсумовувач — деякі формулювання могли зміститися; .lud не читав.
