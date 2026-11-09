---
title: Imogen
slug: imogen
aka: []
family: grid-platformer
also: [thinky]
klass: avatar
axes:
  field: free
  time: realtime
  opponent: none
  info: partial
  random: setup
  goal: collect
year: 1986
platforms: [BBC Micro, Acorn Electron (1988), Windows (2003)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Imogen_(video_game)", best: true, note: "16 рівнів по 4 екрани у випадковому порядку, форми маг / кіт / мавпа (+ птах на одному рівні), ліміт 150 перетворень, смерті нема"}
  - {kind: other, url: "https://everygamegoing.com/litem/Imogen-V2/6724", note: "текст вкладки: клавіші Z/X/RETURN, уміння кожної форми, панель іконок, предмети, паролі секцій, сейв на диск"}
  - {kind: other, url: "https://everygamegoing.com/larticle/Imogen-000/18658", note: "огляд The Micro User: 4 екрани на секцію, падіння без шкоди, паролі, сейв"}
  - {kind: other, url: "https://everygamegoing.com/larticle/Imogen-000/17879", note: "огляд A&B Computing: мавпа лазить по мотузках і деревах, кіт перестрибує скелі й прірви"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Imogen+BBC+Micro+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [gravity-fall, item-pickup, inventory, inventory-items, interaction-table, level-password, save-game, save-multi-slot, keyboard-controls, game-screen, sequential-levels, +shape-shift-forms, +global-action-budget, +icon-bar-commands, +variable-jump-hold, +flip-screen-rooms, +softlock-possible]
proposes: ["+effect:shapeshift", "+cond:form", "+ui:icon-bar", "+feature:mono-display", "+card:shape-shift-forms", "+card:global-action-budget", "+card:icon-bar-commands"]
author: opus
date: 2026-11-09
---

# Imogen — чарівник перетворюється на кота й мавпу, щоб дістати фрагмент заклинання, але перетворень на всю гру лише 150

## Суть
Пазл-платформер BBC Micro: кожна з 16 секцій — замкнена печера з чотирьох екранів, де фрагмент заклинання спершу недосяжний. Гравець перемикає форму героя: **маг** бере й застосовує предмети, **кіт** далеко стрибає, **мавпа** лазить по мотузках і деревах. Кожне перетворення витрачає спільний на всю гру ліміт — 150; вичерпав до кінця — гра стає непрохідною. Загинути не можна: уся складність — у порядку дій і виборі форми.

## Поле і час
- Межа сімʼї `grid-platformer`: рух вільний, не по клітинах (?); екрани зібрані з плиток-перешкод (стіни, мотузки, дерева, скелі, прірви) — родич [treasure-island-dizzy](treasure-island-dizzy.md).
- Секція = 4 зв'язані екрани (flip-screen); видно лише поточний.
- Real-time, гравітація; падіння з будь-якої висоти без шкоди.
- 16 секцій у випадковому порядку (Wikipedia); вантажаться з касети/диска на вимогу.
- Глобальний стан поверх секцій: лічильник перетворень (150 на всю гру, кожна зміна форми −1) і набір зібраних фрагментів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Imogen — маг | player | форма | ходить; RETURN у русі — стрибок; стоячи — застосувати предмет у руці |
| Imogen — мавпа | player | форма | стрибок на місці; лізе по мотузці (RETURN — угору, відпустив — з'їжджає), висить; зістрибує лише в бік, куди дивиться |
| Imogen — кіт | player | форма | стрибок вищий і довший за мага; тримаєш напрям у польоті — довше, відпустив — коротко |
| Imogen — птах | player | лише на одному рівні | літає |
| Предмет (револьвер, лійка, цибулина тюльпана, лук, рідина…) | pickup | ікона в панелі | береться дотиком; маг застосовує: летить, шумить, спалахує, щось інше або нічого |
| Мотузка, дерево | terrain | — | по них лазить лише мавпа |
| Скеля, прірва, висока стіна | static | — | долає кіт стрибком або обхідний шлях |
| Мотузка на повітряній кулі | object | — | везе того, хто вчепився (?) |
| Істота-сторож (бульдог, «маленький гидкий» імп) | enemy | — | не вбиває, але заступає шлях; прибирається правильним предметом |
| Миловидні тварини (кролики, мавпи, папуги, жаби) | neutral | — | персонажі секцій (?) |
| Фрагмент заклинання | pickup | 1 на секцію | застосувати — перенестися в наступну секцію |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ТО `move(imogen, dir)`; КОЛИ `tick` → ЯКЩО `not supported(imogen)` → ТО `fall(imogen)` — без шкоди з будь-якої висоти.
- КОЛИ `input(form_icon)` → ЯКЩО `counter(transformations, <, 150)` → ТО `transform(imogen, form)`, `counter(transformations, +1)`.
- КОЛИ `counter(transformations, ==, 150)` → ТО `custom: «форма зафіксована назавжди; якщо потрібна інша — гру не пройти»`.
- КОЛИ `input(return)` → ЯКЩО `state(imogen, wizard)` і `moving(imogen, dir)` → ТО `custom: «стрибок мага»`.
- КОЛИ `input(return)` → ЯКЩО `state(imogen, wizard)` і `has(imogen, item)` і `custom: «стоїть»` → ТО `use(imogen, item)`.
- КОЛИ `input(return)` → ЯКЩО `state(imogen, monkey)` і `occupied(here, rope)` → ТО `custom: «лізти вгору; відпустив — з'їжджає»`; без мотузки — стрибок на місці.
- КОЛИ `input(return)` → ЯКЩО `state(imogen, monkey)` і `custom: «висить на мотузці»` → ТО `custom: «зістрибнути»` лише якщо `facing(imogen, dir)`.
- КОЛИ `input(return)` → ЯКЩО `state(imogen, cat)` → ТО `custom: «довгий стрибок; довжина = скільки тримаєш напрям у польоті»`.
- КОЛИ `contact(imogen, item)` → ТО `pickup(imogen, item)`; ікона предмета з'являється вгорі.
- КОЛИ `input(object_icon)` → ЯКЩО `state(imogen, wizard)` → ТО `custom: «взяти предмет у руку / відпустити»`.
- КОЛИ `custom: «застосовано предмет у потрібному місці або біля сторожа»` → ТО `custom: «світ змінюється: сторож усунутий, куля лопнула, шлях відкрито»` — таблиця «предмет × місце».
- КОЛИ `input(return)` → ЯКЩО `state(imogen, wizard)` і `has(imogen, spell_fragment)` → ТО `use(imogen, spell_fragment)`, `counter(fragments, +1)`, `next_level`.
- КОЛИ `input(return)` → ЯКЩО `has(imogen, spell_fragment)` і `counter(fragments, ==, 16)` → ТО `win` — повне заклинання виводить назовні.
- КОЛИ `input(password)` → ЯКЩО `custom: «пароль секції правильний»` → ТО `custom: «старт із цієї секції»`; 4 паролі дано в інструкції.
- Перемога: 16 фрагментів · Поразка: нема (герой не гине); фактична — вичерпані 150 перетворень · Рахунку нема (?).

## Керування і ввід
- Z — ліворуч, X — праворуч, RETURN — дія (стрибок / лізти / застосувати предмет).
- Курсорні стрілки ←/→ водять вказівник по панелі іконок угорі, SPACE — вибрати іконку.
- Через «?» вводяться паролі та текстові команди: QUIT (почати знову), MONO (білий екран), COLOUR.

## Вікна, меню, HUD
- `loading-screen` — секції підвантажуються з касети/диска.
- `game-screen`: екран печери + `+ui:icon-bar` угорі: диск (save/load), звук, «?» (пароль/команди), «!» (пароль поточної секції), маг / мавпа / кіт (зміна форми), ікона предмета (взяти/відпустити).
- `save-slots`: ім'я файла до 7 літер/цифр, окремий відформатований диск.
- `level-password`: введення через «?».
- «!» вдруге — `puzzle-select`-подібний огляд: усі 16 секцій і які пройдено.
- `end-screen` — вихід у зовнішній світ (?).

## Фічі поза полем
- `save-slots` на диск — кілька незавершених ігор одночасно; `level-password` на кожну секцію; `sound-toggle`; MONO/COLOUR — `+feature:mono-display`.
- Прогрес: 16 секцій, перехід лише фрагментом або паролем; порядок секцій випадковий (Wikipedia).
- Windows-порт 2003 — «16 рівнів поліморфних головоломок».

## Варіації й родичі
- Родичі: [treasure-island-dizzy](treasure-island-dizzy.md) (предмет як ключ до місця), [head-over-heels](head-over-heels.md) (два герої з різними вміннями), The Lost Vikings, Trine — команда з різних умінь замість однієї зміни форми.
- Осі варіацій: **як дістаєш уміння** (зміна форми одного героя / кілька героїв з перемиканням); **ціна зміни** (безкоштовно / ліміт на гру / ліміт на рівень); **чи можна загинути** (ні — Imogen; так — Dizzy).

## Цікавинки для курсу
- Форми як стани одного героя: та сама кнопка RETURN дає різну дію за станом — 🥉.
- Глобальний бюджет перетворень (150 на всю гру) і виявлення «гра вже непрохідна» — 🌱 лічильник, 🥇 перевірка непрохідності.
- Панель іконок угорі як меню команд, кероване стрілками й пробілом — 📎.
- Таблиця «предмет × місце/істота → ефект» з реакціями «летить / горить / нічого» — 🥉.
- Довжина стрибка кота від утримання клавіші — 📎.
- Паролі секцій + огляд «пройдено / ні» для 16 секцій — 📎.

## Мапа на каталог
- Є: `gravity-fall` · `item-pickup` · `inventory` + `inventory-items` · `interaction-table` · `level-password` · `save-game` + `save-multi-slot` (файли на диску) · `keyboard-controls` · `game-screen` · `sequential-levels` (секції через фрагмент).
- **Нема** → пропозиції карток:
  - `+shape-shift-forms` «Герой міняє форму з окремим набором дій» · entities/state · 🥉.
  - `+global-action-budget` «Ліміт дії на всю гру» · game-logic/lose · 🌱.
  - `+icon-bar-commands` «Панель іконок з вибором стрілками» · interface/input · 📎.
  - `+variable-jump-hold` «Довжина стрибка від утримання» · entities/move · 📎.
  - `+flip-screen-rooms` — як у treasure-island-dizzy.
  - `+softlock-possible` «Гру можна зробити непрохідною» · game-logic/lose · 🌱.

## Пропозиції до словників
- `+effect:shapeshift(a, form)` — зміна форми зі зміною набору дій (зараз — `transform`, але тут сутність лишається тією самою).
- `+cond:form(a, f)` — герой у формі f (окремо від `state`, бо визначає набір дій).
- `+ui:icon-bar` — рядок іконок-команд угорі екрана.
- `+feature:mono-display` — перемикач кольорового/монохромного екрана.
- `+card:shape-shift-forms`, `+card:global-action-budget`, `+card:icon-bar-commands` — див. вище.

## Джерела
- ⭐ [Wikipedia: Imogen (video game)](https://en.wikipedia.org/wiki/Imogen_(video_game)) — 16 рівнів по 4 екрани у випадковому порядку, фрагменти заклинання, форми маг / кіт / мавпа / птах, ліміт 150, смерті нема, Micro Power, Michael St Aubyn, порти.
- [Everygamegoing: вкладка Imogen](https://everygamegoing.com/litem/Imogen-V2/6724) — клавіші, уміння форм, панель іконок, предмети та їхні реакції, паролі, сейв, «персонажа не можна вбити».
- [The Micro User: огляд](https://everygamegoing.com/larticle/Imogen-000/18658) — 4 екрани на секцію, падіння без шкоди, паролі, сейв, приклад з повітряною кулею.
- [A&B Computing: огляд](https://everygamegoing.com/larticle/Imogen-000/17879) — мавпа лазить по мотузках і деревах, кіт — через скелі й прірви, перемикання форм будь-коли.
- YouTube: пошук «Imogen BBC Micro gameplay».

## Непевне
- (?) Число 150 — лише з Wikipedia; вкладка каже «кількість змін обмежена» без числа; чи видно лічильник на екрані — не перевірено.
- (?) Чи рух прив'язаний до знакомісць BBC Micro (клітинний) — не перевірено; тому `field: free`.
- (?) Чи можуть кіт і мавпа брати предмети, чи лише маг; чи предмет губиться при зміні форми.
- (?) Випадковий порядок секцій (Wikipedia) проти вкладки, де перехід — фрагментом у «наступну» секцію і паролями; як саме порядок випадковий.
- (?) Мотузка на кулі як рухома платформа — з опису одного рівня; загальної сутності «платформа» джерела не називають.
