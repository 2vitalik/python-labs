# T179 · Тиждень студента v1 — сторінка, API, зведення — план

`2026-10-01` · ⚙️ задача · звіт — `report.md` (на завершенні)

Контекст:
- дизайн і обґрунтування кожного рішення — [T177](../T177-P--week-design.md): читати першим, тут — лише «що зробити»;
- відкриті вибори — [T178](../T178-Q--week-questions.md): план іде за рекомендаціями (a) в усіх питаннях; відповідь Vitalik інша → правка в межах кроку;
- запит Vitalik (чат, 2026-10-01): «сьогодні я хочу запустити це… щоб студенти могли це вносити», для викладача — «простий варіант, просто щоб можна було бачити загальну тенденцію»;
- виконавець — Opus із максимальним effort. **Свобода:** бачиш простіший або кращий спосіб у межах мети — роби його, а відхилення від плану занотуй у `report.md` розділом «Відхилення».

## Рамки

- Усе нове — в `core/` (бекенд `core/api/core/…`, фронт `core/ui/…`); сайт python лише реєструє маршрути, пункт меню і крок на домашній; `sites/ods/` не чіпаємо, його збірка має лишитись зеленою.
- Правила коду з `CLAUDE.md` і `core/README.md`: файл ≤ ~80 рядків (виріс — розбити), коментарі лише «чому», UI — UA, код — EN, Bootstrap 5, наявні помічники (`Crumbs`, `Avatar`, `GrowArea`, `useTitle`, `byGroup`, `query()` з `http.js`, `local.js`, `record()`/`record_new()`, `notify.send`, `stamp()`).
- Нічого з наявної поведінки не міняється; усі смоуки лишаються зеленими з тими самими числами; Telegram у смоуках — лише `FakeBot`.
- Пріоритет: кроки 1–5 (студент може заповнювати) → 6 (зведення) → 7 (доки) → 8 (за бажанням). Тисне час — 8 пропускаємо, 7 — ні.

## Рішення (стисло; деталі — T177)

- Блоки, не клітинки: `Mark(day, start, end, kind, why)`, `Week(user, marks, comment, done_at)`; одна колекція `weeks`, унікальний `user`.
- Рамка з конфігу ядра (`week_hours="15-23"`, `week_days=6`); API віддає `frame`, фронт констант годин не має.
- Порожнє = можу; три інструменти 🔴 🟡 🟢 + ⚪; жест — прямокутник; той самий інструмент по такій самій клітинці — стирає; телефон — потримати й вести.
- Автозбереження через 1 с; «Готово» — `done=true`, сервер вимагає причину для кожного 🔴.
- Зведення рахує фронт із `GET /api/weeks`: шари, пошук вікна, «хто саме», прогрес, тиждень викладача як виняток.
- Алерт `week` 🗓 — один раз на «Готово».

## Кроки

### 0. Базова лінія

- [ ] `cd app/api && DB_NAME=python_labs_smoke uv run python tests/smoke_*.py` — записати число перевірок кожного; `npm run build` в `app/vue` і `sites/ods/vue`. Перед `uv run` переконатися, що є `UV_PROJECT_ENVIRONMENT` (DEV.md «Venv»).

### 1. Конфіг і модель

- [ ] `core/api/core/config.py`: `week_hours: str = "15-23"`, `week_days: int = 6` — межі сітки «Мій тиждень» (T177), сайт міняє у `site.env`.
- [ ] `core/api/core/models/week.py`: `STEP = 15`; `Mark(BaseModel)`: `day: int`, `start: int`, `end: int`, `kind: Literal["no", "meh", "ok"]`, `why: str = ""`; `Week(Document)`: `user: Annotated[str, Indexed(unique=True)]`, `marks: list[Mark] = []`, `comment: str = ""`, `done_at: datetime | None = None`, `updated_at`, `created_at` (`Field(default_factory=…)`), `Settings.name = "weeks"`; `def frame() -> dict` → `{"days": 6, "from": 900, "to": 1380, "step": 15}` з `settings`; `api(self)` (часи через `stamp()`); `summary(self) -> str` → «🔴 3 · 🟡 2 · 🟢 4» — кількість блоків за видом, для `note` історії й алерту.
- [ ] `core/api/core/db.py`: `Week` у `MODELS`.

### 2. Перевірка і нормалізація (`core/api/core/week_marks.py`)

- [ ] `DAYS = ("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд")`; `hm(minutes) -> "18:00"`; `label(mark) -> "Пн 18:00–19:30"`.
- [ ] `clean(marks: list[Mark], frame) -> list[Mark]`: кожен блок у межах рамки, `start`/`end` кратні `step`, `start < end`, `day` у `0..days-1`; `why` — strip, ≤ 200 символів, лише для `no` (для інших видів стирається); сортування за `(day, start)`; перетин двох блоків → `HTTPException(422, "Позначки перетинаються: Пн 18:00–19:30 і Пн 19:00–20:00")`; сусідні блоки одного `kind` з однаковим `why` зливаються; понад 100 блоків → 422.
- [ ] `missing_why(marks) -> list[str]` → підписи 🔴 блоків без причини; текст 422 для «Готово»: «Поясни червоні слоти: Пн 18:00–19:30, Ср 16:00–17:30».

### 3. API студента (`core/api/core/routes/my_week.py`)

- [ ] `GET /api/my/week` (`active_user`): документ або порожній → `{"frame": frame(), "marks": [], "comment": "", "done_at": None, "updated_at": None}`.
- [ ] `PUT /api/my/week` (`active_user`, `BackgroundTasks`): `WeekIn(marks: list[Mark] = [], comment: str = "", done: bool = False)`; `clean()`; `done and missing_why()` → 422; `comment` — strip, ≤ 1000; документа нема → створити + `record_new`; є → `record(week, {"marks": cleaned, "comment": …, "done_at": …}, actor=user.email, note=summary)` — передавати **`list[Mark]`**, не dict-и: pydantic-моделі порівнюються за полями, і `record()` запише лише справжню зміну; `done_at`: `done` → лишити наявний або `now`; не `done` → `None`; `updated_at = now`, якщо щось змінилось; перший перехід `None → done_at` → `tasks.add_task(alerts.week, user, week)`; відповідь як GET.
- [ ] `core/api/core/bot/alerts.py`: `async def week(user, week)` → `notify.send("week", text, user.email)`; текст у стилі T109 (емодзі-роль на початку кожного рядка, коротко, без крапок): «🗓 Тиждень · <who(user)>» · `week.summary()` · 🔴 блоки, згруповані за причиною («🏫 пара за розкладом: пн 16:10–17:30, ср 14:45–16:05» · «🏋️ тренування: вт, чт 18:00–19:30»; причини без емодзі — під «❓») · «💬 коментар», якщо є. `notify.KINDS` після `"poll"`: `"week": "🗓 тиждень: студент позначив, коли може"`.
- [ ] `core/api/core/app.py`: роутер у `ROUTERS`; `QUIET`/`POLLED` не чіпати — PUT має лишатись у сліді `api`, це і є дія студента.

### 4. API викладача (`core/api/core/routes/weeks.py`)

- [ ] `GET /api/weeks` (`admin_user`): студенти `status == student`, `test != True`, відсортовані як у `/students`; їхні `Week` одним запитом → `{"frame": frame(), "students": [person() | {"tg_username", "week": week.api() | None}], "me": тиждень адміна .api() | None}`.
- [ ] Смоук `app/api/tests/smoke_week.py` (взірець — `smoke_activity.py`: `TestClient`, `FakeBot`, `check()`, вхід через `settings.fake_user_email` + `GET /api/auth/dev-login`, як у `smoke_view_as.sign_in`): GET порожній → `frame == {days 6, from 900, to 1380, step 15}`, `marks == []` · PUT два сусідні 🔴 з тією самою причиною → злилися в один · PUT `start=905` → 422 · PUT перетин → 422 з «перетинаються» · PUT 🟢 з `why` → `why` порожній у відповіді · PUT `done=true` без причини → 422 з «Пн 18:00–19:30», `done_at` досі `None` · PUT `done=true` з причиною → `done_at` є, в `alerts` один текст із «🗓 Тиждень» і «🏋️» · повторний PUT з іншим коментарем → алертів досі 1, у `history` рядок із `note` «🔴 1 …» · той самий PUT ще раз → рядків у `history` не додалось · PUT `done=false` → `done_at == None` · PUT 101 блок → 422 · студент на `GET /api/weeks` → 403 · адмін → `students[i].week.marks` є, `me` є після власного PUT · «Очима студента» (справжній студент) PUT → 403 (взірець — `smoke_view_as.py`).

### 5. Фронт студента (`core/ui`)

- [ ] `core/ui/api.js`: `getMyWeek`, `putMyWeek(data)`, `getWeeks`.
- [ ] `core/ui/week.js` — чиста логіка без Vue: `DAYS`, `KINDS = { no: {emoji: '🔴', text: 'Не можу'}, meh: {'🟡', 'Можу, але незручно'}, ok: {'🟢', 'Найзручніше'} }`, `REASONS = ['🏋️ тренування', '💼 робота', '📚 інші заняття', '🏫 пара за розкладом', '🚌 дорога', '👨‍👩‍👧 сімʼя']`; `rows(frame)` → початки рядків у хвилинах; `hm(min)`; `label(day, start, end)`; `toCells(marks, frame)` → `cells[day][row] = {kind, why} | null`; `toMarks(cells, frame)` → блоки (сусідні однакові `kind` + `why` зливаються); `carryWhy(prev, next)` → кожному новому 🔴 без `why` — причина старого 🔴 того ж дня з найбільшим перетином; `redRuns(marks)`; `rect(a, b)` → множина `[day, row]` між двома клітинками. Виросте за 80 рядків → розбити (`week.js` — рамка й перетворення, `weekSum.js` — зведення з кроку 6).
- [ ] `components/WeekFrame.vue` — розкладка сітки: підписи годин зліва (на кожній годині), шапка днів, слот на клітинку (`day`, `row`, `start`); CSS grid `grid-template-columns: 2.5rem repeat(days, 1fr)`; рядок 1rem; лінія години товща (`border-top` 2px), півгодини — звичайна, чверті — `--bs-border-color-translucent`; `touch-action: pan-y`; `user-select: none`; `contextmenu` глушиться. Використовують і студент, і зведення.
- [ ] `components/WeekPaint.vue` — малювання: пропси `frame`, `modelValue` (marks), `tool`; стан жесту `{anchor, current, erase}`; `pointerdown` → `mouse` одразу, `touch`/`pen` — таймер 250 мс без руху (>8 px до спрацювання = скрол, жест скасовано), спрацював → `navigator.vibrate?.(10)`, `setPointerCapture`; `pointermove` → клітинка через `document.elementFromPoint(x, y)?.closest('[data-cell]')`, превʼю = база з прямокутником; `pointerup`/`pointercancel` → `emit('update:modelValue', carryWhy(old, toMarks(preview)))`; поки жест активний — обробник `touchmove` з `{passive: false}` і `preventDefault()`. Клітинка: клас за `kind`, «?» на першому слоті 🔴 без `why`.
- [ ] `components/WeekTools.vue` — чотири кнопки (заливка виду + рамка `*-border-subtle` для активного; ⚪ — `btn-outline-secondary`), підпис «Порожня клітинка = можу» і на сенсорних (`matchMedia('(pointer: coarse)')`) — «Потримай і веди».
- [ ] `components/WeekReasons.vue` — картка «Чому не можеш»: рядок на кожен 🔴 блок — `label` · чипи `REASONS` (чип підставляє текст) · `<input maxlength="200">`; порожня причина — `border-start border-danger`; емітить оновлені marks. Не рендериться, якщо 🔴 нема.
- [ ] `pages/MyWeekPage.vue` (`/my/week`, `access: 'active'`): `Crumbs(['Мій тиждень'])`, h1 + рядок стану збереження справа; лід; `WeekTools` → `WeekPaint` → `WeekReasons` → «Коментар викладачу» (`GrowArea`) → картка «Готово» (кнопка `disabled`, поки є 🔴 без причини; тексти станів — T177 §«Що бачить» п. 7); автозбереження: `watch` на `marks`/`comment` → debounce 1000 мс → `putMyWeek({marks, comment, done: done && !missing.length})`; відповідь підставляє `done_at`/`updated_at`; помилка → показати текст, повторити з наступною зміною; `beforeunload`, поки є незбережене. Статус `pending` — як у `ProfilePage` («доступ зʼявиться, коли викладач додасть тебе до курсу»).
- [ ] Сайт python: `app/vue/src/router.js` — `/my/week` (`MyWeekPage`, `access: 'active'`), `/week` (`WeekPage`, `access: 'active'`); `site.js` — `['/week', 'Тиждень']` перед «Профіль»; `StartSteps.vue` — третій крок «Позначити тиждень — коли можеш бути на парі» → `/my/week`, done = є `done_at` (компонент сам викликає `getMyWeek()`, коли `active`).
- [ ] `core/ui/activity.js`: `COLLS.weeks = 'тиждень'`.
- [ ] Клік-тест на стенді 8031/5031 (памʼятка — памʼять агента «стенд для адмін-сторінок»; після себе відновити дев-вхід): мишею прямокутник, стерти тим самим інструментом, причина через чип, «Готово» без причини → підказка, з причиною → ✅; у DevTools режим телефона: свайп по сітці гортає, потримати → малює, тап — одна клітинка; темна тема.

### 6. Зведення для викладача

- [ ] `core/ui/weekSum.js`: `aggregate(students, frame)` → на кожну клітинку `{no, meh, ok, free}` (`free` — заповнив, клітинка порожня) + `filled`; `worst(marks, day, start, end)` → найгірший вид студента у вікні (`no > meh > free > ok`); `windows(students, frame, minutes, exclude)` → усі `(day, start)` з `end ≤ to`, що не перетинаються з `exclude` (🔴 блоки адміна), з рахунками `{no, meh, ok, free}`, відсортовані `(no, meh, -ok)`; `who(students, day, start, end)` → `{no: [{student, why}], meh: [student], ok: n, free: n}`, 🔴 згруповані за першим емодзі `why` (без емодзі — «❓ інше»).
- [ ] `components/WeekHeat.vue` — `WeekFrame` з клітинками: число (порожньо = 0) і фон `color-mix(in srgb, var(--bs-<layer>) <0–55>%, var(--bs-body-bg))` за часткою від `filled`; шар 🔴 — `danger`, 🟡 — `warning`, 🟢 — `success`, ⭐ — `success` за `score = (ok*2 + free) / filled`, 🔴 число — у кутку; штрихування клітинок із 🔴 адміна (`repeating-linear-gradient`); вибране вікно — рамка; клік → `emit('pick', {day, start})`.
- [ ] `components/WeekWindows.vue` — тривалість (`btn-group`: 1:20 · 1:30 · 2:00 · 2:40; `?len=` у URL, типово 90), перемикач «без моїх зайнятих» (увімкнено, якщо в адміна є 🔴), топ-10 рядків «Ср 18:00–19:30 · 🔴 3 · 🟡 12 · 🟢 40 · ⚪ 50» + «показати всі»; клік → `emit('pick', {day, start, end})`.
- [ ] `components/WeekWho.vue` — хто саме у вибраному вікні чи клітинці: заголовок «Ср 18:00–19:30»; 🔴 за причинами → усередині за групами: `Avatar` 20 + імʼя-лінк `/activity?user=` + група + `@tg` + текст причини; 🟡 іменами; 🟢/⚪ числами; кнопка «скопіювати @ніки» (🔴).
- [ ] `components/WeekProgress.vue` — «Заповнили N з M · почали K · не відкривали L» (почав = є документ без `done_at`, позначка ✍️), `<details>` «Хто ще не заповнив» по групах (імʼя · `@tg`), кнопка «скопіювати @ніки»; `<details>` «Коментарі студентів».
- [ ] `pages/WeekPage.vue` (`/week`): адмін → `Crumbs(['Тиждень потоку'])`, h1 з кнопкою «Мій тиждень» (`/my/week`), чипи груп (`byGroup`, `?group=`, як у `PollMatrixPage`), `WeekProgress`, перемикач шару (`?layer=`), `WeekHeat`, `WeekWindows`, `WeekWho`; `meta.wide` не потрібен — сітка вміщується в колонку. Студент на `/week` → той самий `MyWeekPage` (як `/students` показує різне адміну й студенту).
- [ ] Клік-тест на стенді: у скретч-базу вставити 5–6 тижнів руками (різні групи, 🔴 з причинами, один без «Готово», адмінів тиждень із 🔴), перевірити шари, пошук вікна, «хто саме», фільтр груп, копіювання @ніків, темну тему, порожню базу (нулі без помилок).

### 7. Доки і завершення

- [ ] `report.md` тут: що зроблено, числа смоуків, кроки клік-тесту для Vitalik (на деві: `/my/week` з телефона й миші → «Готово» → алерт у Telegram → `/week`), «Відхилення» від плану, хвости; текст-зразок оголошення студентам у гілки груп (2–3 рядки з лінком на `/my/week`).
- [ ] `.dev/schedule/README.md`: «Вирішено / реалізовано» — рішення T177 списком, «Інтегровано» + T177/T179, «Відкрите» — T178, «Наступний крок» — деплой і оголошення.
- [ ] `core/README.md`: рядок таблиці «Тиждень студента» (бекенд · фронт); `app/api/bot/README.md` — рядок у «Види алертів» (`week`).
- [ ] `.dev/CHANGELOG.md`: рядок дати з лінками T177–T179; `.dev/README.md` — оновити рядок у «Стан» і «Наступний крок»; `dev gen`; `dev status agent --agent claude`.
- [ ] Запропонувати коміт-меседж (`feat: add student week page and stream summary, t177-179`), коміт — Vitalik.

### 8. За бажанням (якщо лишився час; T178 Q9)

- [ ] «Два вікна»: `pairs(windows)` по топ-40 за 🔴 → пара з максимумом студентів, у яких хоча б одне вікно без 🔴 (тай-брейк — сума 🟡); `<details>` «Якщо одного вікна нема» під `WeekWindows` з 5 найкращими парами: «А: Ср 18:00–19:30 (64) · Б: Пт 16:00–17:30 (39) · ніде: 5»; клік по вікну пари — як по звичайному.

## Перевірка (визнання готовності)

- `smoke_week.py` зелений; решта смоуків — ті самі числа, що в кроці 0; обидва фронти збираються.
- Телефон у DevTools: свайп по сітці гортає сторінку, потримати → малює; тап — одна клітинка.
- «Готово» без причини неможливе; з причиною — рівно один алерт 🗓 у `events`.
- На `/week` при порожній базі — «Заповнили 0 з N», карта порожня, пошук вікна показує вікна з нулями без помилок.
