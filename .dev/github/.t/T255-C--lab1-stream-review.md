# T255 · Лаба 1 на зрізі: що здав потік — звіти агента по 82 репозиторіях

`2026-11-02` · 🔆 clarification · прогін — [T254](T254--reviews-lab1/report.md) · бриф — [review.md](../review.md) · поля — [T248](T248-P--review-spec.md) · питання після — [T256](T256-Q--lab1-review-followup.md)

Зріз — останній коміт до дедлайну студента (27.10 23:59 для всіх; 22 подовження до 28.10–01.11 враховані, усі минули). 84 студенти з посиланням: **82 звіти** (80 на зрізі + 2 лише по HEAD — до дедлайну комітів не було), 2 репозиторії порожні — звіту нема (vladyslav.petrenko6, anna.kolesnyk). Файли — `data/reviews/<нік>/lab1.md` + `lab1.profile.json` + `lab1.facts.json` (поза git); **на сайт ще не надіслано**. Таблиця з шапок — `bin/repos reviews --dry`, зведення — `bin/repos digest 1`.

## Коротко

- **79 з 82 — гра на клітинках**, як просить лаба. 3 — інший код (`other`): anna.ievsovych (описова статистика вибірки — лаба іншого курсу), mykyta.andreienkov (уривок RTS на pygame без `main`, карти й циклу), anastasiia.plokhotnikova (Hill Climb на pygame+pymunk, не клітинки). Жодного «вправи без гри» (`tasks`) — трек «60» ніхто не обрав.
- **62 — усі 6 обовʼязкових на зрізі** (`done`); 16 — частково; 4 — на зрізі нічого, а на HEAD 6/6 після дедлайну (у клітинці буде 🕒): denys.konyshev (28.10), andrii.khyzhniak (31.10), emiliia.vovchenko (на зрізі лише `.gitignore`), andrii.lozovyi (на зрізі порожній `main.py`, код 30.10).
- Типова «часткова» робота — **5/6 без програшу** (bohdan.lysun, denys.sydorenko, vladyslav.dudenko, volodymyr.leonov, yehor.zadorozhnyi) або **одна-дві функції** замість кількох (oleh.sheremet, vladyslav.dudenko, volodymyr.leonov); roman.voloshyn1 — клітинка перевіряється лише при будівництві; yelyzaveta.terekhova — стін і меж поля нема; nadiia.morhun — 2048 без гравця на полі. Нижче: bohdan.kolkov 4/6 (платформер arcade+pymunk без виграшу/програшу), oleksandr.ivaniuk 4/6 (сапер мишею — гравця й руху нема), maksym.naberezhnykh 2/6 (логіка повна, але `keyboard_layout` не визначено — NameError на першому ході), daniil.dovhal 1/6 (сапер-заготовка без вікна, вводу й циклу).
- **Консоль 62 · pygame 13 · tkinter 4 · arcade 2 · curses 1.** Клавіша: `input()` 34 · `msvcrt` 22 (лише Windows — на Mac не запуститься) · pygame 11 · tkinter 4 · keyboard 2 · curses/termios по 1.
- **Процес:** 42 з 82 завантажили весь код **одним комітом**; 18 — однією сесією кількома комітами; 20 — кількома сесіями; 2 — пачкою за хвилини перед дедлайном. 17 — шаблонні повідомлення («update», «...», «123»); 3 — підозрілі дати. Веб-завантаження через GitHub замість `git push` — часто (комітер `GitHub <noreply>`).
- **Ознаки згенерованого коду:** strong 32 · weak 43 · none 7. Типове: докстрінги й коментарі «під список лаби» («Етап 2–5», `# elif для…`), README-шпаргалка для захисту, один ідеальний коміт на 200–600 рядків, трейлер `Co-Authored-By: Claude` у коміті (anatolii.herasymenko). Це сигнал на захист, не вирок ([T16](T16-Q--github-open-questions.md) Q4); у кожному звіті — 3–5 питань по їхньому коду.
- **Чого найчастіше бракує з додаткових:** `nonlocal` 55 · `*` 53 · `/` 52 · вкладені функції 49 · `for-else` 47 · `global` 44 · `lambda` 44 · kwargs 34 · `float` 33 · `or` 27. Групи «функції» й «область видимості» — найслабші; типи, умови, цикли — майже у всіх.
- **Рівень робіт** (1 заготовка … 5 значно понад лабу): 5 — 5 (artem.bondar: 2048 з режимами й undo; yelyzaveta.iatsiuk: тести й доки; mykhailo.berkuta: Pac-Man ООП з тестами; tetiana.bondarenko3: roguelite із збереженням; kyrylo.fedorov: клієнт/сервер), 4 — 40, 3 — 24, 2 — 11, 1 — 2.

## По групах

| Група | Звітів | game | tasks | other | none | done | partial | none | 6/6 | 4–5 | ≤3 | рівень | ШІ strong/weak |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| ПЗПІ-25-1 | 18 | 16 | 0 | 2 | 0 | 14 | 3 | 1 | 14 | 1 | 3 | 3.5 | 7/11 |
| ПЗПІ-25-2 | 12 | 11 | 0 | 1 | 0 | 9 | 2 | 1 | 9 | 1 | 2 | 3.0 | 7/4 |
| ПЗПІ-25-3 | 16 | 16 | 0 | 0 | 0 | 14 | 2 | 0 | 14 | 2 | 0 | 3.6 | 6/7 |
| ПЗПІ-25-4 | 20 | 20 | 0 | 0 | 0 | 14 | 6 | 0 | 14 | 5 | 1 | 3.4 | 6/13 |
| ПЗПІ-25-5 | 7 | 7 | 0 | 0 | 0 | 6 | 0 | 1 | 6 | 0 | 1 | 3.9 | 3/3 |
| ПЗПІ-25-6 | 9 | 9 | 0 | 0 | 0 | 5 | 3 | 1 | 5 | 2 | 2 | 3.3 | 3/5 |

Без репозиторію на сайті — 25 (з них ПЗПІ-25-6 — 7, ПЗПІ-25-2 і 25-5 — по 4); порожні репозиторії — petrenko6 (25-1), kolesnyk (25-6).

## Гілки поза `main` — нова пастка

- tymofii.taratorin: у `main` лише README; лаба на 244 рядки — у гілці `Lab1`, коміт 25.10 (до дедлайну), не злита. Рецензент оцінив гілку (6/6, ознаки генерації сильні, програти неможливо); `commit`/`head` у шапці — sha гілки, тож у клітинці буде «зріз інший». Факти сайту (`Repo.commits` з `origin/HEAD`) гілки не бачать.
- mykhailo.berkuta: `main` сам 6/6, гілки `lab1`–`lab4` по одному незлитому коміту; vsevolod.kozyr — гілки `refactor`, `scenes` без своїх комітів.
- `bin/repos facts` тепер пише `git.other_branches` (гілка → комітів поза `origin/HEAD`). Зараховувати роботу в гілці чи ні — [T256](T256-Q--lab1-review-followup.md) Q1.

## Надійність методу (експеримент, 16 додаткових агентів)

- **Друга незалежна думка Opus** на 8 межових репозиторіях (5/6, «інший код», заготовки, arcade/tkinter): `kind` 8/8, `verdict` 8/8, пунктів `required` 46/48, рівень у межах ±1 — 8/8, ШІ-ознаки 6/8. Розходження: daniil.dovhal (1/6 проти 0/6 — чи 6 допоміжних функцій без гри є «кілька власних функцій») і roman.voloshyn1 (див. калібрування).
- **Sonnet** на тих самих 8: `kind` 7/8 (dovhal → `other`), `verdict` 7/8, пунктів 45/48, рівень ±1 — 8/8; але **доказів `файл:рядок` удвічі менше** (медіана 24 проти 45) і коротші «питання на захист»; 40–57 с проти 75–150 с на звіт. Для `kind`/`required` Sonnet майже не гірший; для тексту звіту — Opus.
- **Калібрування руками (одне):** roman.voloshyn1 п. 4 ✅ → 🟡 — усі три рецензенти знайшли той самий факт (клітинка перевіряється лише при побудові, рух курсора по скелях не блокується), двоє назвали це `partial`, і бриф каже буквально «рух без перевірки клітинки — partial». Позначка в кінці файлу; `verdict` → `partial`. Решту розходжень не чіпав.
- **Старі 13 звітів** (26.10 на HEAD + пілот 31.10, `data/reviews/.v1/`): вердикт збігається 12/13; andrii.romanenko2 тоді 2/6, зараз 6/6 — дописав 27.10 до дедлайну (11 комітів).
- **AST проти агента:** `extra_missing` розходиться з лічильниками у 3 випадках з 82 (`None`/`nested` є в інших файлах або в коді, який агент не вважає лабою) — решта 79 узгоджені.
- Файли експерименту — `data/reviews/.second/`, `.sonnet/`; порівняння — [compare.py](T254--reviews-lab1/compare.py).

## Що це дає далі

- Після `bin/repos reviews`: у `/deadlines` 62 клітинки стануть ✅, 16 🟡, 4 🕒; на `/table?view=lab1` — колонки «що за код» і «✔/6»; у картці студента — «частково · 4/6 · гра» і звіт.
- На захистах: 22 Windows-only (`msvcrt`) — просити запуск у себя; 32 зі strong-ознаками — питання вже в звітах; 42 «одним комітом» — спитати про процес.
- Лаба 2: той самий конвеєр (`cut` → `facts` → субагенти → `digest` → `--dry`); у бриф додати правило про гілки (T256 Q1) і приклад «клітинка лише при дії = partial».

## Усі (зріз) — kind · ✔/6 · вердикт зріз/HEAD · ui · рівень · якість (структура/імена/читабельність) · ШІ · ритм · комітів до+після


| Нік | Група | kind | ✔/6 | зріз | HEAD | ui | рівень | якість | ШІ | ритм | комітів | summary |
|:--|:--|:--|:--|:--|:--|:--|--:|:--|:--|:--|--:|:--|
| alina.nestohina | ПЗПІ-25-1 | game | 6/6 | done | done | console | 2 | 3/4/4 | weak | session | 6+0 | 6/6, програшу нема; додаткові частково; 4 коміти коду за 6 хв |
| andrii.romanenko2 | ПЗПІ-25-1 | game | 6/6 | done | done | console | 4 | 4/4/4 | weak | even | 11+0 | 6/6, консольна змійка у 6 модулях; нема None, a<b<c, lambda, nonlocal; 11 веб-комітів, 3 сесії |
| anna.ievsovych | ПЗПІ-25-1 | other | 0/6 | partial | partial | console | 1 | 4/4/4 | weak | single | 1+0 | не гра: описова статистика вибірки (середнє, медіана, квантилі); 1 коміт «lab1» 29.10 |
| anna.kutsevych | ПЗПІ-25-1 | game | 6/6 | done | done | console | 4 | 4/4/4 | strong | single | 1+0 | 6/6, ultimate tic-tac-toe 9×9 на двох; без scope і */; 1 коміт на 203 рядки |
| arsen.saribehian | ПЗПІ-25-1 | game | 6/6 | done | done | console | 4 | 3/4/4 | strong | session | 4+0 | 6/6, додаткові всі крім *; лабіринт з ключем і дверима з level1.txt; 4 коміти за 3,4 год |
| artem.bondar | ПЗПІ-25-1 | game | 6/6 | done | done | console | 5 | 4/4/4 | strong | even | 6+0 | 6/6, додаткові всі; 2048 з 3 режимами, undo, чітами, меню; 6 комітів за 21 год |
| denys.konyshev | ПЗПІ-25-1 | game | 0/6 | none | done | pygame | 2 | 3/4/4 | weak | single | 0+1 | зрізу нема; на HEAD 6/6 — pygame Pac-Man 5×5, один коміт 28.10 після дедлайну |
| denys.potsebin | ПЗПІ-25-1 | game | 6/6 | done | done | pygame | 4 | 5/5/5 | strong | session | 9+0 | 6/6 pygame survivor на тайлах; додаткові частково; 4 коміти коду за 52 хв |
| denys.zghonnyk | ПЗПІ-25-1 | game | 6/6 | done | done | console | 4 | 3/4/3 | weak | session | 2+0 | 6/6, односторонні дороги; нема float, kwargs, *; код одним комітом |
| ivan.holik | ПЗПІ-25-1 | game | 6/6 | done | done | console | 3 | 3/4/4 | weak | single | 2+0 | 6/6, додаткові всі крім or; лабіринт з ключами; код одним upload-комітом через веб |
| ivanna.kryzka | ПЗПІ-25-1 | game | 6/6 | done | done | console | 4 | 3/4/3 | weak | even | 5+0 | 6/6, лабіринт з ключами й дверима; нема or і *; дати комітів підправлені |
| mariia.ryzhova | ПЗПІ-25-1 | game | 6/6 | done | done | console | 4 | 4/4/4 | strong | single | 3+0 | 6/6; додаткові частково (нема for/range/lambda/bool); весь код одним веб-комітом |
| mykyta.andreienkov | ПЗПІ-25-1 | other | 1/6 | partial | partial | pygame | 2 | 4/3/4 | weak | single | 1+0 | 1/6, уривок RTS на pygame без main, карти й циклу; 1 коміт з вебу на 682 рядки |
| roman.voloshyn1 | ПЗПІ-25-1 | game | 5/6 | partial | partial | arcade | 4 | 4/4/4 | weak | even | 20+0 | 5/6, клітинка перевіряється лише при будівництві; arcade-стратегія 20×20; 20 комітів за 9 днів |
| sofiia.havryliuk | ПЗПІ-25-1 | game | 6/6 | done | done | pygame | 4 | 3/4/4 | weak | session | 7+0 | 6/6, змійка на pygame; бракує break і lambda; 7 комітів за 2 год, за добу до дедлайну |
| sofiia.mizyna | ПЗПІ-25-1 | game | 6/6 | done | done | tkinter | 3 | 4/4/4 | weak | single | 3+0 | 6/6: шахи на tkinter, правила з python-chess; додаткові частково; 1 коміт з кодом |
| yelyzaveta.iatsiuk | ПЗПІ-25-1 | game | 6/6 | done | done | console | 5 | 4/5/4 | strong | session | 21+0 | 6/6, додаткові всі крім or; меню, теми, 13 тестів; 21 коміт за день, доки за 3 хв |
| yevhenii.koval1 | ПЗПІ-25-1 | game | 6/6 | done | done | console | 4 | 4/4/4 | strong | session | 3+0 | 6/6, консольний PvZ на 7 модулях; 3 коміти з вебу за 33 хв, README зі шпаргалкою |
| anastasiia.plokhotnikova | ПЗПІ-25-2 | other | 2/6 | partial | partial | pygame | 3 | 5/5/4 | strong | single | 1+0 | 2/6, Hill Climb на pygame+pymunk без клітинок і виграшу; 1 upload з __pycache__ |
| anatolii.herasymenko | ПЗПІ-25-2 | game | 6/6 | done | done | console | 3 | 4/5/5 | strong | single | 1+0 | 6/6, Sokoban у консолі; додаткові частково; 1 коміт з трейлером Co-Authored-By: Claude |
| andrii.khyzhniak | ПЗПІ-25-2 | game | 0/6 | none | done | console | 3 | 4/4/4 | weak | single | 0+2 | до дедлайну пусто; на HEAD 6/6, гра «Inertia»; 1 upload з вебу 31.10 |
| danylo.petrov | ПЗПІ-25-2 | game | 6/6 | done | done | console | 4 | 4/4/4 | strong | burst | 8+0 | 6/6, гра «бургери», додаткові всі; 8 комітів за 5 хв, README-шпаргалка |
| oleh.sheremet | ПЗПІ-25-2 | game | 5/6 | partial | partial | curses | 2 | 2/4/3 | weak | even | 7+0 | 5/6, лише одна функція main; curses-«frogger», гра одним комітом у день дедлайну |
| oleksandr.petruk | ПЗПІ-25-2 | game | 6/6 | done | done | console | 4 | 3/4/4 | strong | single | 3+0 | 6/6, додаткові всі 5 груп; Sokoban у консолі; код одним комітом 228 рядків |
| ruslan.usatenko | ПЗПІ-25-2 | game | 6/6 | done | done | console | 4 | 3/4/4 | strong | single | 2+0 | 6/6, додаткові всі крім or; гра одним комітом 174 рядки за 24 хв до дедлайну |
| taisiia.kostikova | ПЗПІ-25-2 | game | 6/6 | done | done | console | 3 | 4/4/4 | strong | single | 1+1 | 6/6, усі додаткові; код одним комітом за 12 год до дедлайну, після — README |
| vladyslav.martovytskyi | ПЗПІ-25-2 | game | 6/6 | done | done | console | 2 | 3/4/4 | weak | even | 8+0 | 6/6, ключ-двері-ворог; додаткові частково; 8 комітів за день дедлайну, логіка в останньому |
| yehor.bilokon | ПЗПІ-25-2 | game | 6/6 | done | done | console | 3 | 3/4/4 | weak | session | 3+0 | 6/6, карта з файлу, keyboard; додаткові частково; 3 веб-коміти за 5 хв |
| yelyzaveta.plyha | ПЗПІ-25-2 | game | 6/6 | done | done | console | 3 | 4/4/4 | strong | single | 1+0 | 6/6, консольне судоку; додаткові частково; 1 коміт-завантаження з вебу за 2 год до дедлайну |
| yuliia.panasenko | ПЗПІ-25-2 | game | 6/6 | done | done | console | 2 | 3/4/4 | none | single | 4+0 | 6/6, додаткові частково; весь код одним комітом за 19 хв до дедлайну |
| anastasiia.dobroskokina | ПЗПІ-25-3 | game | 6/6 | done | done | console | 3 | 4/4/4 | strong | single | 2+0 | 6/6, додаткові всі; гра одним комітом 174 рядки, коментарі-чекліст лаби |
| arsenii.hladkykh | ПЗПІ-25-3 | game | 6/6 | done | done | console | 4 | 4/4/4 | weak | session | 4+0 | 6/6, консольний osu! (msvcrt); нема or/not, for-else, * /, scope; код одним комітом |
| bohdan.lysun | ПЗПІ-25-3 | game | 5/6 | partial | partial | tkinter | 3 | 3/4/4 | weak | single | 1+0 | 5/6, нема виграшу/програшу; tkinter-ферма, save/load JSON; 1 коміт upload |
| dmytro.krutko | ПЗПІ-25-3 | game | 6/6 | done | done | tkinter | 4 | 4/4/4 | strong | single | 1+0 | 6/6, PvZ-lite на tkinter; нема while/continue/break/*/вкладених/nonlocal; 1 веб-коміт |
| illia.alieksieiev | ПЗПІ-25-3 | game | 6/6 | done | done | console | 4 | 4/5/4 | strong | single | 1+0 | 6/6, додаткові всі; Battle City з туманом і хаком, 1 коміт 469 рядків «Initial commit» |
| ivan.hordiienko | ПЗПІ-25-3 | game | 6/6 | done | done | console | 4 | 4/3/3 | weak | even | 3+0 | 6/6, Boulder Dash з фізикою каменів; нема None, a<b<c, break, lambda, nonlocal; 3 коміти |
| kyrylo.fedorov | ПЗПІ-25-3 | game | 6/6 | done | done | pygame | 5 | 4/4/4 | none | even | 3+0 | 6/6 на pygame, ООП клієнт/сервер/спільне; гра — одним squash-PR за день до дедлайну |
| mykhailo.pavlenko | ПЗПІ-25-3 | game | 6/6 | done | done | console | 4 | 4/4/4 | none | even | 8+0 | 6/6, Pac-Race із суперником і стартом-світлофором; без * / lambda scope; 8 комітів, 4 сесії |
| nikita.petrushenko | ПЗПІ-25-3 | game | 6/6 | done | done | console | 4 | 4/4/4 | strong | single | 2+0 | 6/6, змійка в консолі; додаткові частково; код одним веб-завантаженням 29.10 |
| viktoriia.iermolova | ПЗПІ-25-3 | game | 6/6 | done | done | console | 4 | 4/4/4 | strong | single | 1+0 | 6/6, додаткові всі (nonlocal формально); 1 коміт на 189 рядків |
| vitalii.ilchenko | ПЗПІ-25-3 | game | 6/6 | done | done | console | 3 | 3/4/4 | weak | single | 2+0 | 6/6, програшу нема; додаткові всі, крім or; один коміт коду на 106 рядків |
| vladyslav.kysil | ПЗПІ-25-3 | game | 6/6 | done | done | console | 4 | 3/4/4 | weak | even | 7+0 | 6/6, додаткові всі (частина «для галочки»); Worms на двох, 7 комітів за 2 дні |
| vladyslava.hyrenko | ПЗПІ-25-3 | game | 6/6 | done | done | console | 3 | 4/4/4 | weak | session | 4+0 | 6/6, Sokoban у консолі; нема elif/else, range, lambda; 4 коміти за 1 год |
| yehor.stohnii | ПЗПІ-25-3 | game | 6/6 | done | done | pygame | 4 | 4/4/4 | strong | session | 5+0 | 6/6 на pygame (Mined-Out), додаткові частково; 4 коміти за 19 хв, pygame +163 за 6 хв |
| yelyzaveta.holovko | ПЗПІ-25-3 | game | 6/6 | done | done | console | 3 | 3/4/4 | weak | single | 5+0 | 6/6, лабіринт з коргі: 3 рівні, життя, кісточки; уся гра одним комітом на 117 рядків |
| yelyzaveta.terekhova | ПЗПІ-25-3 | game | 5/6 | partial | partial | console | 2 | 2/3/3 | none | session | 5+0 | 5/6: приз є, стін і меж поля нема; додаткові частково; код у 2 комітах 27.10 |
| artem.rohozian | ПЗПІ-25-4 | game | 6/6 | done | done | console | 4 | 3/4/4 | weak | single | 1+0 | 6/6, консольна змійка (msvcrt, лише Windows); додаткові частково; 1 коміт за добу до дедлайну |
| bohdan.kolkov | ПЗПІ-25-4 | game | 4/6 | partial | partial | arcade | 3 | 4/3/3 | weak | even | 9+0 | 4/6, платформер arcade+pymunk на TMX-мапі; без виграшу/програшу, шипи й кільця не діють |
| daniil.dovhal | ПЗПІ-25-4 | game | 1/6 | partial | partial | pygame | 1 | 3/4/3 | weak | single | 2+0 | 1/6, сапер-заготовка: логіка поля без вікна, вводу й циклу; 1 коміт коду |
| daniil.voloshko | ПЗПІ-25-4 | game | 6/6 | done | done | console | 2 | 3/4/4 | weak | session | 3+0 | 6/6, консольний лабіринт до виходу E за 30 ходів; додаткові частково; код одним комітом |
| denys.sydorenko | ПЗПІ-25-4 | game | 5/6 | partial | partial | tkinter | 3 | 4/4/4 | weak | single | 2+0 | 5/6, tkinter, BFS для монет; програшу нема; весь код одним комітом за 10 год до дедлайну |
| dmytro.hokov | ПЗПІ-25-4 | game | 6/6 | done | done | console | 4 | 4/4/4 | strong | single | 2+0 | 6/6, додаткові всі; 244 рядки одним комітом за 2 год до дедлайну |
| hlib.baistov | ПЗПІ-25-4 | game | 6/6 | done | done | console | 3 | 3/4/4 | weak | session | 2+0 | 6/6, лабіринт з ключем і дверима; код одним веб-комітом за 2 дні до дедлайну |
| kostiantyn.nikonov | ПЗПІ-25-4 | game | 6/6 | done | done | console | 4 | 3/3/4 | weak | even | 4+0 | 6/6, консольний Sokoban на класах; без float, lambda, for-else, scope; 4 коміти за 3 дні |
| kseniia.platitsyna | ПЗПІ-25-4 | game | 6/6 | done | done | console | 4 | 3/4/4 | weak | even | 5+0 | 6/6, тамагочі-капібара з меню, сейвом і магазином; виграшу нема; 5 комітів за 2 сесії |
| matvii.kuprin | ПЗПІ-25-4 | game | 6/6 | done | done | console | 4 | 4/4/4 | weak | session | 2+0 | 6/6, Lode Runner з драбинами й копанням; нема or/range/lambda/scope; 2 коміти за 43 хв |
| nadiia.morhun | ПЗПІ-25-4 | game | 5/6 | partial | partial | console | 4 | 4/4/4 | strong | single | 1+0 | 2048 з Undo, гравця нема; додаткові майже всі (без elif, lambda); 1 коміт з вебу |
| oleksandr.starchenko | ПЗПІ-25-4 | game | 6/6 | done | done | console | 4 | 4/4/4 | weak | even | 10+3 | 6/6 Sokoban, додаткові всі; 10 комітів за 3 дні; на HEAD життя й пастки |
| tetiana.bondarenko3 | ПЗПІ-25-4 | game | 6/6 | done | done | console | 5 | 4/4/4 | strong | session | 4+0 | 6/6, roguelite з хабом, розведенням і збереженням; код одним вебзавантаженням 635 рядків |
| tymofii.taratorin | ПЗПІ-25-4 | game | 6/6 | done | done | console | 3 | 4/4/4 | strong | single | 1+0 | 6/6 у гілці Lab1 (main — лише README), додаткові майже всі; 1 коміт з вебу GitHub |
| vladyslav.dudenko | ПЗПІ-25-4 | game | 5/6 | partial | partial | console | 2 | 2/4/3 | none | even | 6+0 | 5/6: лише 2 функції, клавіша й рух у main; виграш є, програшу нема; 6 комітів, 4 сесії |
| vladyslav.trykula | ПЗПІ-25-4 | game | 6/6 | done | done | console | 3 | 4/4/4 | strong | single | 1+0 | 6/6, додаткові без функц. можливостей і scope; 1 коміт на 186 рядків |
| volodymyr.leonov | ПЗПІ-25-4 | game | 5/6 | partial | partial | console | 2 | 2/3/4 | weak | single | 3+0 | 5/6: лабіринт з ключами й дверима, одна функція draw, програшу нема; 1 upload з вебу |
| yaroslav.mohyla | ПЗПІ-25-4 | game | 6/6 | done | done | console | 4 | 4/4/4 | weak | session | 2+0 | 6/6, «Танчики» з генерацією лабіринту; бракує /, вкладених, global/nonlocal; 2 коміти за 1 год |
| yeva.samburina | ПЗПІ-25-4 | game | 6/6 | done | done | console | 4 | 4/5/4 | weak | single | 1+4 | 6/6, додаткові всі; гра одним комітом 251 рядок; після зрізу 4 коміти — модулі, рівень з файлу |
| zlata.mykhailichenko | ПЗПІ-25-4 | game | 6/6 | done | done | console | 4 | 4/4/4 | strong | single | 12+0 | 6/6, додаткові всі крім float; код одним комітом, 5 порожніх комітів |
| albina.zhakun | ПЗПІ-25-5 | game | 6/6 | done | done | pygame | 4 | 4/4/4 | weak | even | 3+0 | 6/6, pygame «Coldly»: 2 локації, тепло/дрова/ковзани/міст; 3 коміти за 6 днів |
| artem.charyiarov | ПЗПІ-25-5 | game | 6/6 | done | done | console | 4 | 3/4/3 | strong | single | 4+0 | 6/6, змійка на msvcrt (лише Windows), додаткові майже всі; код одним upload з вебу |
| emiliia.vovchenko | ПЗПІ-25-5 | game | 0/6 | none | done | console | 3 | 4/4/4 | weak | single | 1+3 | на зрізі лише .gitignore; на HEAD змійка 6/6 без виграшу, код одним upload після дедлайну |
| mykhailo.berkuta | ПЗПІ-25-5 | game | 6/6 | done | done | pygame | 5 | 5/5/4 | weak | even | 30+2 | 6/6, Pac-Man на pygame+ООП з тестами; нема lambda/nested/global/nonlocal; 30 комітів, 9 сесій |
| vladyslav.nyzhnyk | ПЗПІ-25-5 | game | 6/6 | done | done | console | 4 | 5/5/4 | strong | burst | 6+0 | 6/6 + меню, вартовий, тести; нема for-else, * /, lambda, вкладених, global; 4 коміти за 10 с |
| vladyslav.sotsenko | ПЗПІ-25-5 | game | 6/6 | done | done | console | 4 | 4/4/4 | strong | single | 1+0 | 6/6, гра з ковзанням; додаткові частково; 1 коміт за ~3 год до дедлайну |
| vsevolod.kozyr | ПЗПІ-25-5 | game | 6/6 | done | done | console | 3 | 4/3/3 | none | even | 9+0 | 6/6, ловля предметів до 100 очок, ООП; програшу нема; додаткові частково; 4 коміти 29–30.10 |
| andrii.lozovyi | ПЗПІ-25-6 | game | 0/6 | none | done | console | 2 | 3/4/3 | weak | single | 1+1 | зріз: main.py порожній (0 байт); HEAD 30.10 — змійка 6/6 одним комітом після дедлайну |
| artem.bilous1 | ПЗПІ-25-6 | game | 6/6 | done | done | console | 4 | 4/4/4 | strong | session | 12+0 | 6/6, додаткові всі; 12 комітів за 2 год, 10 з однаковою секундою |
| danylo.voloshyn | ПЗПІ-25-6 | game | 6/6 | done | done | console | 4 | 3/4/3 | strong | single | 1+0 | 6/6, консольний Bomberman; додаткові майже всі (нема параметрів за замовч.); 1 коміт |
| kyrylo.omelianenko | ПЗПІ-25-6 | game | 6/6 | done | done | console | 3 | 4/4/4 | weak | single | 1+0 | 6/6, консольна змійка; додаткові частково; 1 коміт на 120 рядків |
| maksym.naberezhnykh | ПЗПІ-25-6 | game | 2/6 | partial | partial | console | 4 | 4/4/4 | weak | single | 1+0 | логіка 6/6, але keyboard_layout не визначено — NameError на 1-му ході; 1 коміт «123» |
| oleksandr.ivaniuk | ПЗПІ-25-6 | game | 4/6 | partial | partial | pygame | 3 | 3/4/3 | weak | single | 1+0 | сапер на pygame мишею, гравця й руху нема — 4/6; 1 коміт на 190 рядків |
| viktoriia.patoka | ПЗПІ-25-6 | game | 6/6 | done | done | pygame | 4 | 3/4/3 | none | even | 12+0 | Судоку на pygame, 6/6; додаткові частково, scope нема; 12 комітів за 3 сесії |
| vladyslav.myrnyi | ПЗПІ-25-6 | game | 6/6 | done | done | console | 3 | 4/4/4 | weak | single | 3+0 | 6/6, консоль, додаткові частково; 99% коду одним комітом за день до дедлайну |
| yehor.zadorozhnyi | ПЗПІ-25-6 | game | 5/6 | partial | partial | pygame | 3 | 4/4/4 | strong | even | 2+0 | 5/6, pygame Pac-Man з привидами; виграш лише напис, програшу нема; 2 коміти |


## Твої думки та питання

> 
