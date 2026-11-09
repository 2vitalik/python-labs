---
title: Chroma Squad
slug: chroma-squad
aka: []
family: tactics
also: [build-sim]
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: runtime
  goal: score
year: 2015
platforms: [Windows, macOS, Linux, PS4, Xbox One, iOS, Android, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Chroma_Squad", best: true, note: "епізод = рівень, teamwork (далі, разом, спецатака), рейтинг → фани й гроші, меха-бій, сезони зі спонсорами"}
  - {kind: steam, url: "https://store.steampowered.com/app/251130/", note: "appid перевірено через appdetails: Behold Studios, 30.04.2015; актори, маркетинг, крафт, гігантський робот, три кінцівки"}
  - {kind: other, url: "https://www.destructoid.com/reviews/review-chroma-squad/", note: "огляд: стрибок через союзника, спільна атака сусідів, Director's Instructions, апгрейди студії, маркетингові агенції"}
  - {kind: other, url: "https://steamcommunity.com/app/251130/discussions/0/620712364026765678", note: "Steam: як працює Team Acrobatics — жовті клітини кидка"}
  - {kind: other, url: "https://steamcommunity.com/app/251130/discussions/0/620712364025654936", note: "Steam: розробник про Finishing Move — 4 у Teamwork + удар пʼятого"}
  - {kind: other, url: "https://www.touchtapplay.com/chroma-squad-cheats-tips-strategy-guide/", note: "гайд: пасиви ролей, Lasso, Stunning Pose, лічильник аудиторії, FINISH!"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Chroma+Squad+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [hp-damage, melee-vs-ranged, status-effects, temporary-modes, unit-xp-skills, ai-opponent, destroy-all-enemies, event-points, shop-between-levels, character-select, objective-text, popup-text, game-screen, end-screen, +team-jump, +team-attack, +team-finisher, +audience-meter, +bonus-objectives, +form-change, +crafting-recipes, +equip-loadout, +skill-tree, +studio-upgrades, +season-quota-lose, +multiple-endings, +mecha-duel, +pull-to-self]
proposes: ["+trigger:season_end", "+cond:in_throw_range", "+effect:team_attack", "+effect:finisher", "+ui:audience-meter", "+ui:finish-marker", "+window:studio-hub", "+window:crafting-window", "+window:marketing-select", "+window:episode-briefing", "+feature:show-customization", "+feature:audience-to-economy"]
author: opus
date: 2026-11-09
---

# Chroma Squad — тактика-телешоу «Power Rangers»: герої підкидають одне одного, бʼють разом, а глядачі платять за ефектність

## Суть
П'ятеро каскадерів відкривають студію і знімають власний серіал про рейнджерів: кожен **епізод** — тактичний бій загону з міньйонами й «монстром тижня». Перемога потрібна, але гроші дає **аудиторія**: її піднімають командні трюки, вказівки режисера і фінішер, а падає вона, коли героя вибили. Ядро — механіка **Teamwork**: герой у стійці підкидає союзника далі, ніж той дійде сам, бʼє разом із сусідом по цілі, а п'ятеро разом роблять Finishing Move. Між епізодами — менеджмент студії (актори, костюми, крафт, маркетинг, картонний робот).

## Поле і час
- Квадратна сітка знімального майданчика; загін героїв проти групи міньйонів і боса.
- Хід стороною: гравець ходить героями по одному (рух, потім дія), потім вороги.
- Деякі епізоди закінчуються **меха-боєм**: робот команди проти збільшеного монстра — окремий простіший режим.
- Випадковість — у бою (ухилення ворогів, лут матеріалів) і в напіввипадкових статах спорядження.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Lead | piece | пасив: +50 % здоровʼя | вміння Lasso — притягує ворога до себе |
| Assault | piece | пасив: +30 % атаки | головна шкода; великий радіус кидка в Teamwork |
| Techie | piece | пасив: регенерація навичок при застосуванні навички | активні навички, дальня зброя |
| Scout | piece | пасив: +1 рух | Stunning Pose — оглушує ворогів поруч |
| Assist | piece | пасив: +20 % регенерації навичок | великі лікування; лікує сусідів, коли бере Teamwork |
| Герой у стійці Teamwork | piece | стан `teamwork` | поза; кидає союзника на жовті клітини; долучається до атаки |
| Міньйон | enemy | HP | групи «гарматного мʼяса» |
| Монстр тижня | boss | HP | фінальна ціль епізоду; фінішер по ньому дає найбільше аудиторії |
| Меха команди | piece | апгрейди за гроші | бій з велетенським монстром |
| Збільшений монстр | boss | — | суперник меха-бою |
| Матеріали | pickup | тип | випадають з ворогів; на крафт |
| Аудиторія | resource | лічильник епізоду | після епізоду → гроші й фани |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, h, cell)` → ЯКЩО `custom: «клітина в радіусі руху»` → ТО `move(h, cell)`.
- КОЛИ `input(teamwork, h1)` → ТО `set_state(h1, teamwork)` — `custom: «герой стає в позу»`.
- КОЛИ `input(move, h2, cell)` → ЯКЩО `state(h1, teamwork)` and `custom: «h1 у радіусі руху h2, cell — у радіусі кидка h1 (жовті клітини)»` → ТО `throw(h2, cell)`, `counter(audience, +n)` — Team Acrobatics.
- КОЛИ `input(attack, h, e)` → ЯКЩО `custom: «союзники в стійці Teamwork поруч із ціллю»` → ТО `custom: «атакують разом із h»`, `counter(audience, +n)`.
- КОЛИ `input(teamwork, assist)` → ТО `heal(allies_nearby, n)`.
- КОЛИ `input(attack, h5, e)` → ЯКЩО `custom: «4 інші герої в Teamwork: усі поруч із ціллю (ближній) або в радіусі зброї без cooldown (дальній)»` and `state(team, chromatized)` → ТО `custom: «Finishing Move — спільна спецатака»`.
- КОЛИ `custom: «Finishing Move»` → ЯКЩО `custom: «ціль добита»` → ТО `counter(audience, +big)`; інакше `counter(audience, −big)`; `custom: «над ціллю видно FINISH!, коли фінішер її добʼє»`.
- КОЛИ `input(morph, h)` → ТО `transform(h, chroma_form)` — `custom: «відновлює HP, відкриває спецвміння»`.
- КОЛИ `input(lasso, lead, e)` → ТО `pull(e)` до Lead; КОЛИ `input(stunning_pose, scout)` → ТО `stun(enemies_nearby, n)`.
- КОЛИ `input(attack, h, e)` → ЯКЩО `prob(dodge)` → ТО `custom: «промах»`; інакше `damage(e, n)`; Assault — ×1.3.
- КОЛИ `hp_zero(h)` → ТО `custom: «героя вибито»`, `counter(audience, −n)`.
- КОЛИ `custom: «виконано вказівку режисера (добити боса фінішером; спершу міньйони, потім бос…)»` → ТО `counter(audience, +n)`.
- КОЛИ `died(enemy)` → ЯКЩО `prob(drop)` → ТО `give(team, material)`.
- КОЛИ `all_gone(villains)` → ТО `win`, `custom: «аудиторія конвертується в гроші й фанів»`.
- КОЛИ `custom: «бос виріс»` → ТО `custom: «меха-бій: робот команди проти велетенського монстра»`.
- КОЛИ `input(craft, recipe)` → ЯКЩО `has(team, materials)` → ТО `give(team, gear)` з напіввипадковими статами; `custom: «старе спорядження можна розібрати назад на матеріали»`.
- КОЛИ `input(upgrade_studio, u)` → ЯКЩО `custom: «вистачає грошей»` → ТО `currency(−n)`, `custom: «постійний бонус: медичне страхування акторів, світло знижує ухилення ворогів»`.
- КОЛИ `input(marketing, agency)` → ТО `custom: «нішева агенція — більше фанів за епізод, масова — ширша аудиторія»`.
- КОЛИ `custom: «кінець сезону»` → ЯКЩО `custom: «цілі спонсорів не виконано»` → ТО `game_over`.
- Перемога епізоду: усі лиходії переможені · Поразка: загін вибито / провал сезону · Рахунок: аудиторія епізоду → фани й гроші; гілки сюжету ведуть до трьох кінцівок.

## Керування і ввід
- Миша або геймпад: вибір героя → підсвічені клітини руху → клітина; кнопки дій: атака, навичка, Teamwork, Morph.
- Team Acrobatics: перший герой → Teamwork → другий герой рухається до нього → жовта клітина кидка.
- Фінішер: Teamwork чотирма героями біля цілі, атака пʼятим.

## Вікна, меню, HUD
- `main-menu`: нова гра, продовжити, налаштування.
- `+window:studio-hub` (`custom-window`): офіс студії — найм акторів (`character-select`: ролі й кольори костюмів назавжди), магазин (`shop-window`), `+window:crafting-window`, апгрейди студії, `+window:marketing-select`, пошта фанів, назви команди, робота й фрази.
- `+window:episode-briefing` — опис епізоду і список Director's Instructions (`objective-text`).
- `game-screen`: майданчик; `+ui:audience-meter` у правому верхньому куті; `hp-bar` героїв; `skill-bar` з cooldown; `+ui:finish-marker` над ціллю; `popup-text` трюків.
- `custom-window` — меха-бій.
- `end-screen` епізоду: аудиторія → гроші й фани; сезонний звіт зі спонсорами.

## Фічі поза полем
- Кампанія сезонами з ростером п'яти акторів; дерева навичок, випадкове спорядження, крафт, три кінцівки (`+multiple-endings`).
- Економіка шоу (`+feature:audience-to-economy`): аудиторія → фани → гроші → апгрейди студії, костюмів, зброї й меха.
- Кастомізація (`+feature:show-customization`): назви команди, робота, крилаті фрази.
- Нема збереження посеред місії й вибору епізоду (за оглядом Destructoid).

## Варіації й родичі
- Родичі: [Mario + Rabbids Kingdom Battle](mario-rabbids-kingdom-battle.md) — Team Jump від союзника-трампліна; [XCOM](xcom.md) — тактика + база між місіями; [Into the Breach](into-the-breach.md) — меха проти велетнів.
- **Осі варіацій** командної взаємодії: союзник-трамплін при проходженні ([mario-rabbids](mario-rabbids-kingdom-battle.md)) / союзник у стійці кидає (тут) · спільна атака сусідів / фінішер усіх пʼятьох · мета бою: знищити / знищити ефектно (аудиторія як рахунок).

## Цікавинки для курсу
- Team Acrobatics: досяжність = клітини руху до союзника в стійці + радіус його кидка — 🥉 (BFS у два етапи).
- Спільна атака: хто з союзників у стійці стоїть поруч із ціллю — долучається — 📎.
- Аудиторія як рахунок за стиль: трюки +, вибитий герой −, фінішер ± залежно від того, чи добив — 📎.
- Director's Instructions — додаткові умови епізоду з бонусом — 🌱 за кожну, 📎 за систему перевірок.
- Морф як тимчасова трансформація з відновленням HP і новими вміннями — 🌱.
- Цикл «епізод → аудиторія → гроші → апгрейд → наступний епізод» із сезонним планом спонсорів — 🥈.

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` ↔ ближній і дальній фінішер · `status-effects` ↔ оглушення · `temporary-modes` ↔ стійка Teamwork · `unit-xp-skills` ↔ дерева навичок · `ai-opponent` · `destroy-all-enemies` · `event-points` ↔ аудиторія · `shop-between-levels` · `character-select` ↔ кастинг акторів · `objective-text` ↔ вказівки режисера · `popup-text` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+team-jump`, `+bonus-objectives`, `+form-change`, `+crafting-recipes`, `+equip-loadout`, `+skill-tree`, `+multiple-endings` — уже в корпусі.
  - `+team-attack` «Союзники в стійці бʼють разом» · entities/combat · 📎 · слот {need: adjacent_to_target}.
  - `+team-finisher` «Спільна спецатака всього загону» · entities/combat · 📎 · слот {members: 5}.
  - `+audience-meter` «Рахунок за стиль, а не лише перемогу» · game-logic/score · 🌱.
  - `+studio-upgrades` «Постійні бонуси за гроші між рівнями» · game-logic/economy · 🌱 — родич `shop-between-levels`.
  - `+season-quota-lose` «Квота за сезон, інакше програш» · game-logic/lose · 🌱.
  - `+mecha-duel` «Окремий режим боєм гігантів» · game-logic/opponent · 📎.
  - `+pull-to-self` «Притягнути ворога до себе» · entities/combat · 🌱.

## Пропозиції до словників
- `+trigger:season_end` — кінець сезону епізодів (перевірка цілей спонсорів).
- `+cond:in_throw_range` — клітина в радіусі кидка союзника в стійці.
- `+effect:team_attack` — союзники в стійці долучаються до атаки; `+effect:finisher` — спільна спецатака з ризиком втрати аудиторії.
- `+ui:audience-meter` — лічильник глядачів; `+ui:finish-marker` — напис «FINISH!» над ціллю, яку фінішер добʼє.
- `+window:studio-hub` — офіс студії між епізодами; `+window:crafting-window`; `+window:marketing-select`; `+window:episode-briefing` — опис і вказівки режисера.
- `+feature:show-customization` — імена команди/робота/фрази; `+feature:audience-to-economy` — рахунок епізоду стає валютою.

## Джерела
- ⭐ [Wikipedia: Chroma Squad](https://en.wikipedia.org/wiki/Chroma_Squad) — студія й ролі акторів, епізоди, трансформація, teamwork (далі, разом, спецатака), рейтинг → фани й гроші, меха, сезони й спонсори.
- [Steam: Chroma Squad](https://store.steampowered.com/app/251130/) — опис: найм акторів, маркетинг, крафт, гігантський картонний робот, дерева навичок, три кінцівки.
- [Destructoid: огляд](https://www.destructoid.com/reviews/review-chroma-squad/) — стрибок через союзника, спільні атаки, Director's Instructions, апгрейди студії (світло проти ухилення), маркетинг, без сейву посеред місії.
- [Steam-обговорення: Team Acrobatics](https://steamcommunity.com/app/251130/discussions/0/620712364026765678) — жовті клітини кидка, радіус Assault.
- [Steam-обговорення: Finishing Move](https://steamcommunity.com/app/251130/discussions/0/620712364025654936) — розробник: 4 у Teamwork + атака пʼятого, дальній варіант без cooldown, Chromatized.
- [TouchTapPlay: гайд](https://www.touchtapplay.com/chroma-squad-cheats-tips-strategy-guide/) — пасиви 5 ролей, Lasso, Stunning Pose, лічильник аудиторії, FINISH!, крафт після першого епізоду.
- YouTube: пошук «Chroma Squad gameplay».

## Непевне
- (?) Скільки дій має герой за хід (рух + одна дія?) і чи Teamwork завершує хід героя.
- (?) Чи спільна атака вимагає сусідства з ціллю, чи з атакувальником — джерела формулюють по-різному.
- (?) Що саме означає «Chromatized» (усі в морф-формі?) — з коментаря гравця.
- (?) Правила меха-бою — у джерелах лише «спрощений».
- (?) Точні умови сезонних цілей спонсорів і наслідки поразки в епізоді.
- (?) Чи 5 ролей — це саме Lead/Assault/Techie/Scout/Assist для всіх версій (гайд 2015 року).
