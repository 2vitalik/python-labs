# T176 · Опитування v1 — шаблони, відправлення, збір голосів, таблиця — план

`2026-09-30` · ⚙️ задача · звіт — `report.md` (на завершенні)

Контекст:
- дизайн і обґрунтування кожного рішення — [T174](../T174-P--polls-design.md): читати першим, тут — лише «що зробити»;
- відкриті вибори — [T175](../T175-Q--polls-questions.md): план іде за рекомендаціями (a) в усіх питаннях; відповідь Vitalik інша → правка в межах кроку;
- запит Vitalik (чат, 2026-09-30): «просто якась перша версія… щось базове, надійне, гарантоване»; головне — «швидко створити опитування і зберігати всю інформацію, який студент, де, що і коли відповів».

## Рамки

- Усе нове — в `core/` (бекенд `core/api/core/…`, фронт `core/ui/…`); сайт python лише реєструє маршрути й пункт меню; `sites/ods/` не чіпаємо.
- Правила коду з `CLAUDE.md`: файл ≤ ~80 рядків (виріс — розбити), коментарі лише «чому», UI — UA, код — EN, Bootstrap 5, наявні компоненти (`Crumbs`, `Avatar`, `GrowArea`, `useTitle`, `byGroup`, `query()` з `http.js`).
- Нічого з наявної поведінки бота й сайту не міняється; усі 13 смоуків лишаються зеленими, кількість перевірок не падає.
- Telegram у смоуках — лише фейки (`notify.bot = lambda: FakeBot()`, як у `smoke_activity.py`); живий клік-тест — за Vitalik після деплою.
- Не робити: анонімні опитування, квізи, авто-закриття, розклад, імпорт старих, CSV, бали.

## Рішення (стисло; деталі — T174)

- Три сутності: `PollTemplate` → `Poll` (заморожена копія + короткий `title`) → `PollSend` (одне повідомлення в одному чаті/гілці); голоси — `Vote`, журнал лише дописується; цілі — `TgChat`, веде бот.
- Надійність: хендлери `poll` і `poll_answer` + лог `allowed_updates` на старті; `is_anonymous=False` завжди; `Vote.update_id` унікальний; сирий апдейт спершу в `logs/poll_updates.jsonl`, потім у Mongo; `PollSend` пишеться до виклику Telegram; звірка `state.total` ↔ наші голоси → ⚠️ на сайті і алерт при закритті.
- Людина за голосом шукається при читанні за `users.tg_chat_id` (T150); `Vote.user` — лише знімок на момент запису.
- Відправляє API-процес через `notify.bot()`; бот-процес збирає.

## Кроки

### 0. Базова лінія

- [ ] `DB_NAME=python_labs_smoke uv run python tests/smoke_*.py` в `app/api` — записати кількість перевірок кожного; `npm run build` в `app/vue` і `sites/ods/vue`.

### 1. Моделі

- [ ] `core/api/core/models/poll.py`: `Option(BaseModel)` (`emoji: str = ""`, `text: str`); `PollTemplate`, `Poll`, `PollSend`, `Vote`, `TgChat` — поля за T174 §«Моделі»; часи — `datetime.now(timezone.utc)` через `Field(default_factory=…)`, як у решті моделей. Файл виросте за 80 рядків → `models/poll.py` (шаблон, опитування, відправлення) + `models/vote.py` (`Vote`, `TgChat`).
  - `Vote.update_id: Annotated[int | None, Indexed(unique=True, sparse=True)]` — дубль доставки має впасти на індексі, а не на логіці; `Vote` індекси ще `tg_poll_id`, `poll`, `tg_id`, `at`.
  - `TgChat`: складений унікальний індекс `(chat_id, thread_id)` через `Settings.indexes = [IndexModel([("chat_id", 1), ("thread_id", 1)], unique=True)]`.
  - `PollSend.state: dict = {}` — `{"total": int, "counts": [int…], "is_closed": bool, "at": iso}`.
  - `api()`-методи повертають `id` рядком і часи через `stamp()` з `models/history.py` (зона потрібна браузеру).
- [ ] `core/api/core/db.py`: нові документи в `MODELS`.
- [ ] `.gitignore`: рядок `logs/` (страховий jsonl у теці сайту; ods матиме свій).

### 2. Бот: збір голосів і реєстр цілей

- [ ] `core/api/core/bot/chats.py`: `async def seen(message: Message)` — для `group`/`supergroup`: upsert `TgChat` за `(chat.id, message_thread_id if is_topic_message else None)`: `title=chat.title`, `topic` — з `reply_to_message.forum_topic_created.name` або `message.forum_topic_created/forum_topic_edited.name`, інакше лишити наявний або `f"#{thread_id}"`; `seen_at=now`; `active=True`. `async def status(event: ChatMemberUpdated)` — `my_chat_member`: `member`/`administrator` → `active=True` для всіх записів чату, `left`/`kicked` → `active=False`.
  - Виклик `seen()` — з `log.incoming` (після `save()`), `status()` — з `log.member()` для `my_chat_member` (там уже є хендлер: додати виклик, не дублювати роутер).
- [ ] `core/api/core/bot/polls.py`: `router = Router()`; `LOG = Path("logs/poll_updates.jsonl")` (шлях від cwd = тека сайту; смоук підміняє на тимчасовий).
  - `async def keep(update: Update) -> None` — `LOG.parent.mkdir(exist_ok=True)`, дописати рядок `json.dumps(dump(update), ensure_ascii=False)` (`dump` — з `log.py`).
  - `@router.poll_answer() async def answer(event: PollAnswer, event_update: Update)`: `await keep(event_update)`; `send = await PollSend.find_one(PollSend.tg_poll_id == event.poll_id)`; `poll = await Poll.get(send.poll) if send else None`; `text` — `f"{poll.title}: " + ", ".join(label(o) for o in chosen)` або `f"{poll.title}: ↩︎ відкликано"` (без `poll` — `"?"`); `Vote(update_id=event_update.update_id, tg_poll_id=…, poll=…, tg_id=event.user.id if event.user else None, username=(event.user.username if event.user else "") or "", user=await log.email(tg_id), option_ids=event.option_ids, text=…, raw=dump(event)).insert()` у `try/except DuplicateKeyError: pass` (pymongo) — повторна доставка того ж `update_id` мовчки пропускається.
  - `@router.poll() async def state(event: TgPoll, event_update: Update)`: `await keep(event_update)`; знайти `PollSend` за `event.id`; `set({"state": {"total": event.total_voter_count, "counts": [o.voter_count for o in event.options], "is_closed": event.is_closed, "at": now_iso}})`; `event.is_closed and send.status == "sent"` → `status="closed"`, `closed_at`. Невідомий `id` — лишити лише в jsonl (не наше опитування).
- [ ] `core/api/core/bot/run.py`: винести збирання в `def build() -> Dispatcher` (усе, що зараз між `Dispatcher()` і `set_my_commands`), `main()` викликає його; `dp.include_router(polls.router)` **до** `log.router`; після старту — `logging.info("allowed updates: %s", dp.resolve_used_update_types())`.
- [ ] `core/api/core/bot/notify.py`: у `KINDS` після `"msg"` — `"poll": "🗳 опитування: збій відправлення, розходження лічильників"`; `outgoing()` — `isinstance(method, (SendMessage, SendPoll))`; `log.save()` — `text=message.text or message.caption or (message.poll.question if message.poll else "")`.
- [ ] Смоук `app/api/tests/smoke_polls.py` (взірець — `smoke_log.py`): `polls.LOG = Path(tempdir)/…`; `build().resolve_used_update_types()` ⊇ `{"poll", "poll_answer", "message"}`; `PollSend(sent, tg_poll_id="p1")` + `Poll` у базі; `answer()` з `PollAnswer(poll_id="p1", option_ids=[1], user=TgUser(id=42…))` і `Update(update_id=1, …)` → один `Vote` з `user="vasya@nure.ua"`, `text="Пара 3: ✅ так"`, рядок у jsonl; той самий `update_id` ще раз → голосів досі 1; `option_ids=[]`, `update_id=2` → `text` з ↩︎; `PollAnswer` без `user` (`voter_chat`) → `tg_id=None`, не падає; `state()` з `TgPoll(id="p1", total_voter_count=3, options=[PollOption(voter_count=…)…], is_closed=False…)` → `PollSend.state.total == 3`; `is_closed=True` → `status == "closed"`; невідомий `poll_id` → лише jsonl, без `Vote`; `chats.seen()` на повідомленні з форуму → `TgChat` з назвою гілки; `status()` `kicked` → `active=False`.

### 3. Відправлення, закриття, шаблони, цілі (API)

- [ ] `core/api/core/polls_send.py`:
  - `label(o: Option) -> str` = `f"{o.emoji} {o.text}".strip()`; `check(question, options)` — 1–300 · 2–12 · кожен 1–100 → `HTTPException(422, UA-текст)`.
  - `async def send(poll: Poll, chat_id: int, thread_id: int | None, where: str, silent: bool) -> PollSend`: `PollSend(status="queued", …).insert()` → `kind_var.set("poll")` → `bot().send_poll(chat_id, poll.question, options=[label(o)…], is_anonymous=False, allows_multiple_answers=poll.multiple, message_thread_id=thread_id, disable_notification=silent)` → успіх: `status="sent"`, `tg_poll_id=m.poll.id`, `message_id`, `url=m.get_url(include_thread_id=True) or ""`, `option_ids=[o.persistent_id for o in m.poll.options]`, `sent_at`; `TelegramAPIError` → `status="failed"`, `error=e.message`, `notify.send("poll", "🗳 Не надіслав … · <b>{where}</b>: {error}")`. Перший `sent` → `Poll.status="open"`, `sent_at`.
  - `async def close(poll: Poll) -> list[PollSend]`: для кожного `sent` — `bot().stop_poll(chat_id, message_id)` → `state` з поверненого `Poll`, `status="closed"`, `closed_at`; помилка → `error`, статус лишається; `Poll.status="closed"`, `closed_at`; розходження (`mismatch()` з кроку 4) → `notify.send("poll", "🗳 ⚠️ … Telegram N · у нас M")`.
- [ ] `core/api/core/routes/poll_templates.py` (`/api/polls/templates`, `admin_user`): `GET` (усі, за `-created_at`) · `POST` · `PUT /{id}` · `DELETE /{id}`; `TemplateIn(title, question, options: list[Option], multiple, tags)`; `clean()` — strip, порожні варіанти викинути, `check()`; історія — `record_new`/`record`/`record_delete` з `actor=admin.email`.
- [ ] `core/api/core/routes/polls.py` (`/api/polls`, `admin_user`):
  - `GET ""` `?tag=`: `{polls: [poll.api() | {sends: n, votes: n_distinct_voters_with_choice, mismatch: bool}], tags: sorted(set)}` — рахунки одним проходом по `PollSend`/`Vote` (обсяги малі: сотні опитувань, тисячі голосів).
  - `POST ""`: `PollIn(title, question, options, multiple, tags, template: str = "")`; з `template` — поля беруться з шаблону, а передані непорожні їх перекривають; `status="draft"`, `by=admin.email`.
  - `PUT /{id}`: `draft` — усе; інакше лише `title`, `tags` (решта в тілі ігнорується з 422, якщо відрізняється — щоб помилка не була тихою).
  - `DELETE /{id}`: лише `draft` (409 інакше).
  - `POST /{id}/send` `{targets: [{chat_id, thread_id}], silent: bool}`: 409 для `closed`; для кожної цілі — `send()` з `where` із `TgChat` (`"{title} › {topic}"`) або `"мені особисто"` для `chat_id == admin.tg_chat_id`; відповідь — `{sends: [s.api()…]}` (з `failed` і `error`, без 5xx).
  - `POST /{id}/sends/{sid}/retry`: лише `failed` → `send()` тими ж координатами, старий рядок → `status="retried"`.
  - `POST /{id}/close` → `{poll, sends}`.
  - `GET /chats`: `{chats: [c.api()…] за title, topic, me: admin.tg_chat_id}` · `PUT /chats/{id}` `{active}`.
  - Порядок маршрутів: `/chats`, `/templates` (окремий роутер, включений першим) — до `/{id}`.
- [ ] Смоук `app/api/tests/smoke_polls_api.py` (взірець — `smoke_activity.py`, `TestClient` + `FakeBot` із `send_poll`, що повертає aiogram `Message(poll=Poll(id="p1", options=[PollOption(text, voter_count=0, persistent_id="a")…]…))`, і `stop_poll`, що повертає `Poll` з лічильниками; прапорець `broken` → `TelegramAPIError`): шаблон → `POST /api/polls` з `template` → чернетка з копією → `PUT` питання ок → `POST send` у дві цілі, одна `broken` → одна `sent`, одна `failed` з `error`, `Poll.status == "open"`, у `events` є `poll` → `retry` → `sent`; `PUT` питання на `open` → 422; `DELETE open` → 409; валідація: 1 варіант → 422, питання 301 символ → 422.

### 4. Результати й таблиця (читання)

- [ ] `core/api/core/polls_read.py`:
  - `def latest(votes) -> dict[(poll_id, tg_id), Vote]` — останній за `(at, id)` голос кожної людини в опитуванні (по всіх його відправленнях).
  - `def mismatch(send: PollSend, votes) -> int | None` — `state.total - len({tg_id: голоси з непорожнім option_ids по цьому tg_poll_id})`; `None`, якщо `state` ще нема; ⚠️ на сайті — при `> 0`.
  - `async def results(poll) -> dict`: `sends` (`api()` + `mismatch`); `options: [{emoji, text, count, voters: [{who, at}]}]` — `who` = `person()` привʼязаного (мапа `tg_chat_id → User` з `users`) або `{"tg_id", "username"}`; `retracted: [{who, at}]`; `missing: [{group, people: […]}]` — `User.status == student`, `test != True`, `tg_chat_id` є, без голосу з вибором; `timeline: [{at, who, ids, text}]` — усі голоси за часом.
  - `async def matrix(tag, template, days) -> dict`: `polls` (`open`/`closed`, фільтри, за `sent_at`); `rows` — активні студенти (`student`, не `test`) `person()` + `cells: {poll_id: {ids, at}}` з `latest()`; `strangers: [{tg_id, username, cells}]` — голоси без людини; тестових і адмінів у рядках нема, їхні голоси йдуть у `strangers` з `who`.
- [ ] `core/api/core/routes/poll_results.py`: `GET /api/polls/matrix?tag=&template=&days=` (до `/{id}`!) і `GET /api/polls/{id}` → `results()`.
- [ ] `core/api/core/activity_feed.py`: `SOURCES["vote"] = ("votes", {}, "user")`, `FIELDS["vote"] = ("tg_poll_id", "poll", "tg_id", "username", "text", "option_ids")`; `activity_link.BY_TG["vote"] = lambda ids: [{"tg_id": {"$in": ids}}]`, `tg_id()` уже читає `doc.get("tg_id")`; у `routes/activity.py` `DEFAULT` джерело не ховати.
- [ ] Дописати `smoke_polls_api.py`: після відправлення вставити `Vote`-и напряму (Вася 42 → [1]; Петро 43 → [0] потім [] ; чужий 99 → [1]) і `PollSend.state = {total: 3, …}` → `GET /api/polls/{id}`: `options[1].count == 2` (Вася і 99), Петро в `retracted`, Вася не в `missing`, третій студент у `missing`, `mismatch == 1` (Telegram нарахував 3, у нас з вибором 2 — один голос «загубився»); потім `state.total = 2` → `mismatch == 0`; `GET /api/polls/matrix` → клітинка Васі `ids == [1]`, Петро — `ids == []`, 99 у `strangers`; `?tag=` фільтрує; `GET /api/activity?src=vote&user=vasya` → рядок з `text`; `POST close` → `state` з `stop_poll`, `status == "closed"`.

### 5. Фронт (`core/ui`)

- [ ] `core/ui/api.js`: `getPolls(params)` · `getPoll(id)` · `postPoll` · `putPoll` · `deletePoll` · `sendPoll(id, data)` · `retrySend(id, sid)` · `closePoll(id)` · `getPollMatrix(params)` · `getPollTemplates` · `postPollTemplate` · `putPollTemplate` · `deletePollTemplate` · `getPollChats` · `putPollChat(id, data)`.
- [ ] `core/ui/activity.js`: `COLLS` + `polls: 'опитування', poll_templates: 'шаблон опитування'`; чип `tg` → `src: ['tg', 'vote']`; `ICONS.vote = '🗳'`. `ActivityRow.vue`: гілка `r.src === 'vote'` → `<span class="text">{{ r.text }}</span>`.
- [ ] Компоненти:
  - `components/PollOptions.vue` — рядки `emoji` (вузьке поле, 2–3 символи) + `text` (`GrowArea`), кнопки ✕ · ↑ · ↓ · «+ варіант»; лічильник `text.length/100`; `v-model` на масив.
  - `components/TagInput.vue` — чипи + поле; Enter/кома додає, Backspace на порожньому знімає останній; `<datalist>` з наявних тегів (проп `known`).
  - `components/PollForm.vue` — `title` · `question` (лічильник `/300`) · `PollOptions` · `multiple` (switch) · `TagInput`; валідація повторює `check()` — кнопка «Надіслати» неактивна, поки не проходить; `useForm` з `form.js`.
  - `components/PollTargets.vue` — чекбокси цілей із `getPollChats()` (`title › topic`), зверху «🧪 мені особисто (тест)» якщо `me`; switch «тихо, без сповіщення»; останній вибір — у `localStorage` через `local.js` (зручність, не істина).
  - `components/PollResults.vue` — варіанти як у Telegram: рядок = емодзі+текст, смужка (`width: count/max`), кількість, під ним люди (`Avatar` 18 + імʼя-лінк на `/students/<nick>`; чужі — `@нік` або `tg id` сірим); секції «Відкликали» і «Не відповіли» по групах (`<details>`); «Хід голосування» — `<details>`, рядки `час · хто · текст`.
  - `components/PollSends.vue` — рядок на відправлення: `where` · час · статус-бейдж (`queued`/`sent`/`failed`/`closed`) · лінк «повідомлення» (`url`) · ⚠️ `mismatch` з підказкою «Telegram нарахував N, у нас M — частина голосів могла загубитись, поки бот не працював» · «Повторити» для `failed`.
  - `components/PollMatrix.vue` — `<table>` як `StudentsTable` (рядки груп, `byGroup`), шапка — `title` опитування з `title`-підказкою (питання · дата), `RouterLink` на `/polls/:id`; клітинка — емодзі варіантів (`ids.map(i => options[i].emoji || i + 1).join(' ')`), порожня — `·` сірим, `[]` — `↩︎`; підказка — тексти варіантів і час; перша колонка `position: sticky; left: 0`, обгортка `overflow-x: auto`; підсумковий рядок «відповіли N»; блок «Без привʼязки» знизу.
- [ ] Сторінки:
  - `pages/PollsPage.vue` (`/polls`, `filters: true`): `Crumbs(['Опитування'])`, заголовок + кнопки «Нове опитування» (`/polls/new`) · «Шаблони» · «Таблиця»; чипи тегів у `?tag=`; список карток: `title` · статус-бейдж · питання · теги · «куди: …» · «голосів N» + ⚠️; `usePolling(load, 30)` — щоб під час пари рахунок оновлювався сам; знизу `<details>` «Куди бот може слати» — цілі з перемикачем `active`.
  - `pages/PollEditPage.vue` (`/polls/new`, `/polls/:id/edit`): на `new` — вибір шаблону (`<select>` або картки) заповнює форму; `title` за замовчуванням — назва шаблону + сьогоднішня дата `дд.мм`; `PollForm` + `PollTargets`; «Зберегти чернетку» → `POST`/`PUT` → `/polls/:id`; «Надіслати» → зберегти → `sendPoll` → `/polls/:id` (помилки відправлення видно там рядками `failed`). На `edit` для не-`draft` — форма лише `title`/`tags`, решта read-only з підписом «після відправлення питання не змінити».
  - `pages/PollPage.vue` (`/polls/:id`): шапка (`title`, статус, теги, питання, «хто створив · коли»), `PollSends`, `PollResults`; кнопки: «Надіслати ще в…» (розкриває `PollTargets` + кнопка) · «Закрити» (`confirm`) · «Повторити опитування» (→ `/polls/new?from=<id>` — форма копіює поля) · «Редагувати». `usePolling(load, 15)` поки `open`.
  - `pages/PollTemplatesPage.vue` (`/polls/templates`): картки шаблонів (назва, питання, варіанти в рядок, теги) з «Створити опитування» (→ `/polls/new?template=<id>`) · «Редагувати» (форма інлайн тією ж `PollForm`) · «Видалити» (`confirm`); форма «Новий шаблон» зверху.
  - `pages/PollMatrixPage.vue` (`/polls/matrix`, `wide: true`, `filters: true`): чипи тегів, `<select>` шаблону, період (`PERIODS` з `activity.js`); `PollMatrix`.
- [ ] Сайт python: `app/vue/src/router.js` — `/polls`, `/polls/new`, `/polls/templates`, `/polls/matrix`, `/polls/:id`, `/polls/:id/edit` (усі `access: 'admin'`, статичні — до `:id`); `app/vue/src/site.js` — `['/polls', 'Опитування']` після «Актив». `npm run build` в обох сайтах зелений.
- [ ] Клік-тест на стенді 8031/5031 (памʼятка — памʼять агента «стенд для адмін-сторінок»): без токена бота відправлення дає `failed` з текстом — цього достатньо, щоб пройти всі сторінки: шаблон → опитування → відправлення (failed) → повторити → результати порожні → таблиця порожня; голоси вставити в скретч-базу руками і побачити їх у результатах, таблиці та `/activity`.

### 6. Відновлення з jsonl

- [ ] `core/api/core/polls_replay.py`: `python -m core.polls_replay [logs/poll_updates.jsonl]` з теки сайту — `init_db()` ядра (моделі голосів — ядра), читає рядки, для `poll_answer` без `Vote` з таким `update_id` — вставляє через ту саму функцію, що й хендлер (винести з `polls.answer` тіло у `record_answer(event, update_id)`), для `poll` — оновлює `state`, якщо `at` новіший; друкує «додано N, було M». Смоук: видалити один `Vote`, прогнати → повернувся.

### 7. Доки і завершення

- [ ] `report.md` тут: що зроблено, кількості перевірок смоуків, що перевірити наживо Vitalik (кроки: тестовий бот у dev, `/polls` → шаблон «Хто на парі» → опитування → «мені особисто» → проголосувати → результат і таблиця → закрити → звірка), хвости.
- [ ] `.dev/tgbot/README.md`: аспект «Опитування» (рішення T174 списком з лінками), «Інтегровано» + T174/T175/T176, «Відкрите» — T175, «Наступний крок» — клік-тест наживо і деплой (перезапуск бота обовʼязковий: нові `allowed_updates` беруться лише при старті).
- [ ] `app/api/bot/README.md`: розділ «Опитування» (лише з сайту; неанонімні; бот має працювати постійно; dev — окремий токен; `logs/poll_updates.jsonl` і `polls_replay`), рядок у «Види алертів» (`poll`), «Де що в коді».
- [ ] `core/README.md`: рядок таблиці «Опитування» (бекенд · фронт).
- [ ] `.dev/CHANGELOG.md`: рядок дати з лінками T174–T176; `dev gen`; `dev status agent --agent claude`.
- [ ] Запропонувати коміт-меседж (`feat: add telegram polls on the site, t174-176`), коміт — Vitalik.

## Перевірка (визнання готовності)

- `smoke_polls.py` і `smoke_polls_api.py` зелені; решта смоуків — ті самі числа, що в кроці 0; обидва фронти збираються.
- У логу старту бота — `allowed updates: […, 'poll', 'poll_answer', …]`.
- Сценарій на стенді пройдено від шаблону до таблиці; голос, вставлений двічі з одним `update_id`, порахований один раз.
- Жодного `if site == …` у ядрі; жоден новий файл не більший за ~80 рядків без причини, записаної в `report.md`.
