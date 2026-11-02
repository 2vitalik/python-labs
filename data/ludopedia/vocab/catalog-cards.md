# Картки каталогу (автоген)

Джерело: `data/catalog/tasks.yaml` · 209 карток. Теги `mechanics` у шапці гри — ці slug-и; нове — з `+`.

| slug | Назва | Зона/підзона | Монетка | Батько | Слоти | Опис |
|---|---|---|---|---|---|---|
| `projectile-shot` | Постріл | entities/combat | bronze |  |  | Снаряд як сутність, летить по прямій. |
| `shoot-modes` | Режими стрільби | entities/combat | tin |  |  | Сімʼя: вперед / черга / дріб / cooldown. |
| `shoot-forward` | Вперед | entities/combat | tin | shoot-modes |  |  |
| `shoot-burst` | Черга | entities/combat | tin | shoot-modes | shots |  |
| `shoot-spread` | Дріб | entities/combat | tin | shoot-modes | rays |  |
| `shoot-cooldown` | Cooldown | entities/combat | tin | shoot-modes | cooldown |  |
| `projectile-collision` | Зіткнення снарядів | entities/combat | tin |  |  | Анігіляція чи проліт. |
| `blast-wave` | Вибухова хвиля | entities/combat | bronze |  | radius | Хрест на N клітин. |
| `chain-detonation` | Ланцюгова детонація | entities/combat | bronze |  | delay | Вибух підриває сусідні бомби. |
| `piece-capture` | Взяття фігури | entities/combat | tin |  |  | Зняття з поля при ході на зайняту клітину. |
| `melee-vs-ranged` | Атака впритул проти дистанційної | entities/combat | bronze |  |  | Правила по типу ворога. |
| `touch-death` | Смерть від дотику | entities/death | wood |  |  | Ворог/пастка вбиває. |
| `environment-death` | Смерть від середовища | entities/death | tin |  |  | Вода без колоди, вибух, камінь згори. |
| `respawn` | Респавн | entities/death | tin |  | delay | Повернення після смерті (дім привидів, checkpoint). |
| `timed-despawn` | Зникнення за часом | entities/death | wood |  | lifetime | Тимчасові предмети і платформи. |
| `death-animation` | Анімація смерті | entities/death | tin |  |  | Ефект перед зникненням. |
| `item-pickup` | Збирання | entities/interact | tin |  |  | Предмет зникає, ефект гравцеві. |
| `interaction-table` | Таблиця взаємодій | entities/interact | silver |  |  | «Що стається, коли X наступає на Y» як дані. |
| `key-and-door` | Ключ і двері | entities/interact | bronze |  |  | Сімʼя способів відкриття. |
| `teleport` | Телепорт | entities/interact | bronze |  |  | Парні портали. |
| `teleport-pair` | Парні портали | entities/interact | bronze | teleport |  |  |
| `teleport-one-way` | Односторонні | entities/interact | tin | teleport |  |  |
| `teleport-cooldown` | З cooldown | entities/interact | tin | teleport |  |  |
| `teleport-random-exit` | Випадковий вихід | entities/interact | tin | teleport |  |  |
| `floor-types` | Типи підлоги | entities/interact | silver |  |  | Лід (ковзання), вода (потрібні ласти), вогонь (Chip's Challenge). |
| `stick-together` | Злипання | entities/interact | silver |  |  | Сутності зчіплюються при контакті і рухаються разом (Sokobond). |
| `cell-transform` | Трансформація | entities/interact | tin |  |  | Клітина-перетворювач змінює тип обʼєкта (Emerald Mine). |
| `impassable-cells` | Непрохідні клітини | entities/legality | wood |  |  | Стіни для всіх або для типу сутності. |
| `piece-move-patterns` | Патерни ходів фігур | entities/legality | bronze |  |  | Кінь/тура/слон як правила на сітці. |
| `legal-move-highlight` | Підсвітка легальних ходів | entities/legality | tin |  |  | Показати дозволені клітини обраної фігури. |
| `no-move-into-check` | Заборона ходу під шах | entities/legality | gold |  |  | Хід, що підставляє короля, недопустимий. |
| `tile-merge` | Злиття однакових | entities/legality | bronze |  |  | Плитки обʼєднуються за правилом. |
| `push-object` | Штовхання | entities/legality | bronze |  |  | Обʼєкт зсувається, якщо за ним вільно. |
| `move-by-input` | Рух за вводом | entities/move | bronze |  |  | 4 напрямки; ввід керує переміщенням аватара. |
| `move-4dir` | 4 напрямки | entities/move | bronze | move-by-input |  |  |
| `move-8dir` | 8 напрямків (діагоналі) | entities/move | bronze | move-by-input |  |  |
| `move-auto` | Автоматичний рух, ввід змінює напрям | entities/move | bronze | move-by-input |  |  |
| `inertia-slide` | Інерція | entities/move | bronze |  |  | Ковзання до упору. |
| `gravity-fall` | Гравітація | entities/move | bronze |  |  | Падіння без опори. |
| `enemy-patrol` | Патрулювання | entities/move | bronze |  |  | Ворог туди-сюди / по маршруту. |
| `random-walk` | Випадкове блукання | entities/move | tin |  |  | З забороною розвороту на місці. |
| `chase-player` | Погоня за гравцем | entities/move | bronze |  |  | Жадібна (крок у бік цілі). |
| `chase-greedy` | Жадібна (крок у бік цілі) | entities/move | bronze | chase-player |  |  |
| `chase-bfs` | Пошук шляху BFS/A* | entities/move | gold | chase-player |  |  |
| `chase-double-move` | Два ходи ворога на один хід гравця (Theseus) | entities/move | bronze | chase-player |  |  |
| `pattern-automaton` | Патерн-автомат | entities/move | bronze |  | pattern | Жорсткий цикл ходів (слайм квадратом, скелет через такт). |
| `row-conveyor` | Конвеєрний рух ряду | entities/move | bronze |  |  | Вся смуга зсувається разом. |
| `body-queue` | Тіло-черга | entities/move | bronze |  |  | Хвіст повторює шлях голови. |
| `spawn-random-cell` | Спавн у випадковій клітині | entities/spawn | wood |  |  | З перевіркою, що клітина вільна. |
| `spawn-schedule` | Спавн за розкладом | entities/spawn | tin |  | every, max_alive | Кожні N тіків / за подією. |
| `spawn-points` | Точки спавну | entities/spawn | wood |  |  | Фіксовані місця рівня (дім привидів). |
| `spawn-animation` | Поява з анімацією | entities/spawn | tin |  |  | Сутність «проявляється» кілька тіків. |
| `hp-damage` | HP і шкода | entities/state | tin |  | hp, who | Замість миттєвої смерті. |
| `inventory` | Інвентар | entities/state | bronze |  |  | Предмети з застосуванням. |
| `inventory-items` | Предмети з застосуванням | entities/state | bronze | inventory |  |  |
| `inventory-limit` | Ліміт місткості | entities/state | silver | inventory | capacity |  |
| `inventory-duration` | Час дії | entities/state | bronze | inventory | duration |  |
| `temporary-modes` | Тимчасові режими | entities/state | bronze |  | duration | Сила після енерджайзера, щит, переляк ворогів. |
| `speed-per-type` | Швидкість за типом | entities/state | tin |  |  | Різний темп сутностей (тіки через раз). |
| `multi-cell-size` | Розмір понад клітину | entities/state | gold |  |  | Обʼєкт 1×2/2×2, рух уздовж осі (Rush Hour). |
| `orientation-state` | Орієнтація як стан | entities/state | gold |  |  | Обʼєкт перекочується, боки різні (Sausage Roll). |
| `markup-validity` | Валідність розмітки | game-logic/constraints | bronze |  |  | Конфлікти рядка/стовпця/регіону. |
| `completion-detection` | Виявлення завершення | game-logic/constraints | tin |  |  | Всі обмеження виконані. |
| `check-stalemate` | Шах / пат | game-logic/constraints | gold |  |  | Виявлення загрози і безвиході. |
| `deadlock-detection` | Виявлення deadlock | game-logic/constraints | gold |  |  | Ящик у глухому куті. |
| `difficulty-levels` | Рівні складності | game-logic/difficulty | tin |  |  | Розмір поля, кількість мін/ворогів. |
| `cheat-codes` | Чіт-коди | game-logic/difficulty | tin |  |  | Безсмертя, відкриття рівнів (для демонстрації і налагодження). |
| `game-pause` | Пауза | game-logic/difficulty | wood |  |  | Заморозка тіків. |
| `round-currency` | Валюта в раунді | game-logic/economy | bronze |  |  | Сонця/монети: генерація і витрати. |
| `shop-between-levels` | Магазин між рівнями | game-logic/economy | bronze |  |  | Покупка апгрейдів. |
| `shop-catalog` | Вітрина товарів | game-logic/economy | wood | shop-between-levels |  | Список із цінами й описами. |
| `shop-preview` | Превʼю товару | game-logic/economy | tin | shop-between-levels |  | Що дасть покупка, до покупки. |
| `shop-sales` | Знижки й розпродажі | game-logic/economy | tin | shop-between-levels |  | Тимчасові ціни, акції. |
| `shop-buyback` | Продаж назад | game-logic/economy | tin | shop-between-levels |  | Повернути куплене за частину ціни. |
| `in-round-upgrades` | Апгрейди в раунді | game-logic/economy | tin |  |  | Радіус вибуху, кількість бомб. |
| `player-death` | Смерть гравця | game-logic/lose | wood |  | lives | З варіантом кількох життів. |
| `time-out` | Вичерпано час | game-logic/lose | wood |  | limit | Таймер рівня. |
| `enemy-reached-base` | Ворог дійшов до краю/бази | game-logic/lose | wood |  |  |  |
| `no-moves-left` | Нема ходів | game-logic/lose | tin |  |  | Глухий кут. |
| `wrong-mark-lose` | Помилкова розмітка | game-logic/lose | tin |  |  | Поразка при невірно заповненій клітині (режим «like paper»). |
| `hot-seat` | Hot-seat на двох | game-logic/opponent | tin |  |  | Черга ходів за однією клавіатурою. |
| `turn-enforcement` | Заборона позачергового ходу | game-logic/opponent | wood |  |  | Контроль сторони. |
| `move-timer` | Таймер ходу / шаховий годинник | game-logic/opponent | tin |  | per_move |  |
| `ai-opponent` | AI-суперник | game-logic/opponent | tin |  |  | Сімʼя за силою: випадковий → жадібний → minimax. |
| `ai-random` | Випадковий | game-logic/opponent | tin | ai-opponent |  |  |
| `ai-greedy` | Жадібний | game-logic/opponent | bronze | ai-opponent |  |  |
| `ai-minimax` | Minimax | game-logic/opponent | gold | ai-opponent | depth |  |
| `realtime-ai` | AI в реальному часі | game-logic/opponent | gold |  |  | Виживання проти Tron-змійки. |
| `save-game` | Збереження гри | game-logic/save | silver |  |  | Продовжити пізніше. |
| `save-single-slot` | Один слот | game-logic/save | silver | save-game |  |  |
| `save-multi-slot` | Кілька слотів | game-logic/save | silver | save-game |  |  |
| `save-autosave` | Автосейв | game-logic/save | silver | save-game |  |  |
| `save-progress` | Збереження рекордів і прогресу | game-logic/save | bronze |  |  | Між сесіями. |
| `event-points` | Очки за події | game-logic/score | wood |  |  | Таблиця вартостей дій. |
| `combo-multiplier` | Комбо-серії | game-logic/score | tin |  |  | Множник за неперервність (Mr. Do!). |
| `time-bonus` | Бонус за час | game-logic/score | wood |  |  | Швидше = більше. |
| `score-records` | Рекорди | game-logic/score | tin |  |  | Локальна таблиця найкращих. |
| `enemy-waves` | Хвилі ворогів | game-logic/waves | bronze |  | waves, final_wave | Розклад появи, фінальна хвиля. |
| `reinforcements` | Підкріплення | game-logic/waves | wood |  |  | +1 ворог за знищеного. |
| `progress-acceleration` | Прискорення прогресу | game-logic/waves | wood |  |  | Темп росте з рівнем/довжиною. |
| `collect-all` | Зібрати все | game-logic/win | wood |  |  | Точки/призи/золото. |
| `collect-quota` | Зібрати квоту | game-logic/win | wood |  | quota | N алмазів відкривають вихід. |
| `reach-exit` | Дійти до фінішу | game-logic/win | wood |  |  | Клітина виходу. |
| `destroy-all-enemies` | Знищити всіх ворогів | game-logic/win | wood |  |  |  |
| `all-on-targets` | Усі обʼєкти на цілях | game-logic/win | wood |  |  |  |
| `satisfy-constraints` | Задовольнити всі обмеження | game-logic/win | tin |  |  | Пазл розвʼязано. |
| `checkmate` | Мат | game-logic/win | gold |  |  | Король суперника без порятунку. |
| `level-bank` | Банк рівнів із прогресом | levels/bank | bronze |  |  | Список «розвʼязано / ні». |
| `daily-puzzle` | Щоденний пазл | levels/bank | tin |  |  | Рівень дня з фіксованим seed. |
| `level-rating` | Рейтинг рівнів | levels/bank | tin |  |  | Сортування за складністю в банку. |
| `in-game-editor` | Редактор у грі | levels/editor | silver |  |  | Розстановка елементів курсором, збереження у файл. |
| `editor-palette` | Палітра елементів | levels/editor | wood | in-game-editor |  | Вибір елемента для розстановки. |
| `editor-draw-tools` | Інструменти малювання | levels/editor | bronze | in-game-editor |  | Прямокутник, лінія, заливка — не лише по клітині. |
| `editor-erase` | Гумка | levels/editor | wood | in-game-editor |  | Видалення елементів з мапи. |
| `editor-undo` | Undo/redo | levels/editor | bronze | in-game-editor |  | Скасування і повернення дій. |
| `editor-playtest` | Плейтест | levels/editor | bronze | in-game-editor |  | Запуск рівня одразу з редактора. |
| `editor-map-check` | Перевірка мапи редактором | levels/editor | bronze |  |  | Не дає зберегти непрохідне. |
| `level-exchange` | Обмін рівнями | levels/editor | tin |  |  | Експорт/імпорт файла іншому студенту. |
| `level-from-txt` | Рівень із txt-файла | levels/format | bronze |  |  | Символьна мапа, парсер. |
| `import-open-formats` | Імпорт відкритих форматів | levels/format | bronze |  |  | .xsb, судоку-стрічки, формати Tatham. |
| `map-validation` | Валідація мапи | levels/format | tin |  |  | Зрозуміла помилка на битому файлі. |
| `level-metadata` | Метадані рівня | levels/format | wood |  |  | Назва, автор, складність у заголовку файла. |
| `maze-generation` | Генерація лабіринту | levels/generation | gold |  | algo | Прохідний лабіринт (DFS/Прима). |
| `mines-after-first-click` | Розкидання мін після першого кліку | levels/generation | tin |  |  | Перший клік завжди безпечний. |
| `dungeon-generation` | Генерація підземель | levels/generation | gold |  |  | Кімнати + коридори (роглайк). |
| `unique-puzzle-generation` | Генерація пазла з унікальним розвʼязком | levels/generation | crown |  |  | Головне золото пазл-гілки. |
| `infinite-field` | Нескінченне поле вперед | levels/generation | gold |  |  | Генерація на льоту (Crossy Road). |
| `difficulty-rating` | Оцінка складності згенерованого | levels/generation | gold |  |  | Рейтинг за технікою розвʼязання. |
| `sequential-levels` | Кілька рівнів послідовно | levels/progression | tin |  |  | Перехід після перемоги. |
| `level-unlock` | Розблокування | levels/progression | tin |  |  | Наступний відкривається після попереднього. |
| `level-select` | Вибір рівня | levels/progression | tin |  |  | Меню зі списком і статусом. |
| `checkpoint` | Checkpoint | levels/progression | bronze |  |  | Продовження з середини після смерті. |
| `reachability-check` | Перевірка досяжності | levels/solvability | gold |  |  | Чи існує шлях до всіх цілей (flood fill / BFS). |
| `level-solver` | Розвʼязувач | levels/solvability | gold |  |  | Авторозвʼязання рівня (Sokoban, судоку). |
| `unsolvable-states` | Виявлення нерозвʼязних станів | levels/solvability | gold |  |  | Deadlock під час гри. |
| `movement-animation` | Анімація руху | interface/graphics | bronze |  |  | Плавний зсув між клітинами (GUI). |
| `event-effects` | Ефекти подій | interface/graphics | tin |  |  | Вибух, збирання, відкриття дверей. |
| `idle-animation` | Анімація очікування | interface/graphics | tin |  |  | «Дихання» спрайтів на місці. |
| `particles` | Частинки | interface/graphics | bronze |  |  | Прості системи часток на подіях. |
| `status-panel` | Панель стану | interface/hud | tin |  |  | Життя, рахунок, час, запас бомб/щитів. |
| `goal-counter` | Лічильник цілей | interface/hud | wood |  |  | Скільки лишилось зібрати/знищити. |
| `mode-indicator` | Індикатор режиму | interface/hud | wood |  |  | Енерджайзер активний, чий хід. |
| `telegraphed-intents` | Телеграфовані наміри | interface/hud | bronze |  |  | Показати наступний хід ворога (Into the Breach). |
| `keyboard-controls` | Керування клавіатурою | interface/input | bronze |  |  | Рух, дії, перепризначення клавіш. |
| `cell-click` | Клік по клітині | interface/input | wood |  |  | Базова курсорна дія. |
| `hover-highlight` | Виділення і наведення | interface/input | tin |  |  | Підсвітка клітини під курсором. |
| `drag-drop-piece` | Drag-n-drop фігури | interface/input | bronze |  |  | Перетягнути на легальну клітину. |
| `pencil-marks` | Олівцеві нотатки | interface/input | bronze |  |  | Pencil marks: кандидати в клітині. |
| `chord-click` | Акорд-клік | interface/input | tin |  |  | Комбінована дія на числі. |
| `swipe-gestures` | Жести-свайпи | interface/input | bronze |  |  | Хід свайпом (тач/мобільний варіант). |
| `main-menu` | Головне меню | interface/menus | tin |  |  | Нова гра, продовжити, вихід. |
| `pause-menu` | Пауза-меню | interface/menus | tin |  |  | З продовженням і рестартом. |
| `confirm-dialog` | Діалог підтвердження | interface/menus | wood |  |  | Вихід без збереження. |
| `end-screen` | Екран перемоги/поразки | interface/menus | tin |  |  | З підсумком і переходом далі. |
| `game-screen` | Ігровий екран | interface/menus | wood |  |  | Головне вікно з полем гри; сам рендер поля — картки підзони «Поле і рендер». |
| `splash-screen` | Заставка/лого | interface/menus | tin |  |  | Екран із назвою і логотипом при запуску. |
| `settings-window` | Вікно налаштувань | interface/menus | tin |  |  | Окреме вікно під елементи налаштувань. |
| `shop-window` | Вікно магазину | interface/menus | tin |  |  | Вітрина крамниці; сама механіка покупок — у «Економіці». |
| `help-window` | Вікно довідки | interface/menus | tin |  |  | Правила гри і керування зсередини гри. |
| `about-window` | Вікно «Про гру» | interface/menus | wood |  |  | Автор, версія, подяки. |
| `custom-window` | Нестандартне вікно | interface/menus |  |  |  | Вікно поза типами; ціну і зарахування уточнює викладач. |
| `console-render` | Консольний рендер | interface/render | bronze |  |  | Поле символами/емодзі, перемальовка кадру. |
| `gui-render` | GUI-рендер | interface/render | silver |  |  | Те саме поле спрайтами; спільний двіжок із консоллю. |
| `field-scaling` | Масштабування поля | interface/render | bronze |  |  | Розмір під вікно, скрол великих мап. |
| `player-camera` | Камера за гравцем | interface/render | bronze |  |  | Вʼюпорт менший за мапу. |
| `minimap-radar` | Мінімапа/радар | interface/render | bronze |  |  | Огляд великої мапи або невидимих ворогів. |
| `leaderboard` | Таблиця рекордів | interface/results | tin |  |  | Топ-N з іменами. |
| `profile-stats` | Статистика профілю | interface/results | tin |  |  | Партії, перемоги, найкращий час. |
| `replay` | Replay | interface/results | silver |  |  | Перегляд запису проходження. |
| `game-settings` | Налаштування гри | interface/settings | bronze |  |  | Складність, розмір поля, звук; збереження між сесіями. |
| `theme-select` | Вибір теми | interface/settings | tin |  |  | Набори символів/спрайтів. |
| `settings-elements` | Елементи налаштувань | interface/settings | tin |  |  | Сімʼя інтерфейсних контролів; кожен елемент у вікні — окрема заявка. |
| `volume-control` | Гучність | interface/settings | tin | settings-elements |  | Слайдер або кнопки рівня звуку. |
| `music-toggle` | Перемикач музики | interface/settings | wood | settings-elements |  | Увімк/вимк фонової музики. |
| `avatar-picker` | Вибір аватару | interface/settings | tin | settings-elements |  | Персонаж/скін гравця. |
| `field-size-picker` | Розмір поля | interface/settings | tin | settings-elements |  | Розмір або масштаб поля. |
| `language-picker` | Вибір мови | interface/settings | tin | settings-elements |  | Перемикання мови інтерфейсу. |
| `controls-remap` | Перепризначення клавіш | interface/settings | bronze | settings-elements |  | Зміна розкладки керування. |
| `sound-effects` | Звукові ефекти подій | interface/sound | tin |  |  | Кроки, постріл, збирання. |
| `background-music` | Фонова музика | interface/sound | tin |  |  | З вимикачем у налаштуваннях. |
| `sound-volume` | Застосування гучності | interface/sound | wood |  |  | Рівень звуку реально впливає на ефекти й музику. |
| `sound-warnings` | Звукові попередження | interface/sound | wood |  |  | Таймер добігає, шах. |
| `logic-render-split` | Розділення логіки і рендера | code/architecture | bronze |  |  | Двіжок не знає, консоль це чи GUI (вимога спільного двіжка). |
| `dual-frontends` | Два фронтенди на одному двіжку | code/architecture | silver |  |  | Консоль + GUI перемикаються. |
| `state-as-data` | Стан гри як дані | code/architecture | bronze |  |  | Серіалізований стан (основа збережень і replay). |
| `game-loop` | Цикл tick/update/render | code/architecture | tin |  |  | Явний ігровий цикл. |
| `commit-history` | Історія комітів | code/git | wood |  |  | Осмислені повідомлення, без сміття в репо. |
| `project-readme` | README проєкту | code/git | wood |  |  | Як запустити, керування, скриншоти. |
| `version-tags` | Теги версій | code/git | wood |  |  | Зріз на кожну лабораторну. |
| `requirements-pyproject` | Requirements/pyproject | code/packaging | wood |  |  | Відтворюване середовище. |
| `single-command-run` | Запуск однією командою | code/packaging | wood |  |  | python -m game без танців. |
| `exe-build` | Збірка в exe | code/packaging | tin |  |  | pyinstaller для демонстрації без Python. |
| `typing-mypy` | Типізація | code/python | bronze |  |  | Анотації + перевірка mypy. |
| `dataclass-entities` | Dataclass-сутності | code/python | tin |  |  | Моделі елементів поля. |
| `generators-iterators` | Генератори та ітератори | code/python | tin |  |  | Обхід поля, хвилі. |
| `custom-exceptions` | Виключення | code/python | tin |  |  | Власні класи помилок, охайна обробка. |
| `std-collections` | Стандартні колекції | code/python | tin |  |  | deque для тіла змійки, heapq для A*. |
| `unit-tests` | Юніт-тести логіки | code/tests | bronze |  |  | Рух, взаємодії, перемога без рендера. |
| `fixture-level-tests` | Тест на рівнях-фікстурах | code/tests | bronze |  |  | Мапа з очікуваним результатом. |
| `property-tests` | Property-тести | code/tests | gold |  |  | Генератор завжди видає розвʼязне. |
| `player-guide` | Інструкція гравця | support/docs | wood |  |  | Правила і керування. |
| `architecture-doc` | Опис архітектури | support/docs | tin |  |  | Схема модулів для захисту. |
| `dev-log` | Журнал розробки | support/docs | tin |  |  | Короткий devlog по тижнях. |
| `game-page` | Сторінка гри | support/sites | tin |  |  | Опис, скриншоти, посилання на репозиторій. |
| `video-channel` | Канал/плейліст | support/sites | tin |  |  | Зібрані демки по лабораторних. |
| `itchio-publish` | Itch.io-публікація | support/sites | bronze |  |  | Гра, доступна для запуску іншим. |
| `feature-demo` | Демка фічі | support/video | tin |  |  | Короткий запис однієї можливості до захисту. |
| `game-trailer` | Трейлер гри | support/video | bronze |  |  | Зведене відео з монтажем. |
| `demo-effects` | Ефекти демки | support/video | tin |  |  | Титри, прискорення, зум на момент. |
