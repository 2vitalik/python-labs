# T221 · Відвідування із Zoom: що дає API, як автоматизувати

`2026-10-14` · 🔆 clarification

Контекст:
- запит Vitalik (чат, 2026-10-14): «чи можна автоматично витягувати із Zoom, хто був на ПЗ, скільки часу він був, коли він був»; «не хочеться зчитувати дані з CSV»; показувати на сторінках занять, і окрема сторінка статистики по студентах; «поки що лише спроєктуй» — якщо реально, задача окремою сесією → [T222](T222--zoom-attendance-v1/plan.md);
- опора: заняття на сайті вже є ([T218](T218--lessons-v1/report.md)), зіставлення «імʼя в Zoom → студент» теж (`User.aliases`, `lesson_people.py`) — відвідування сяде на те саме;
- джерела — пошук і документація Zoom 2026-10-14 (список унизу); точні назви полів і скоупів перед кодом звірити з живим довідником — форумні дописи можуть бути застарілі.

## Коротко

- **Так, реально автоматично, без CSV.** Zoom після кожної зустрічі віддає через REST API список учасників із часом входу/виходу й тривалістю. Один виклик на заняття — і на сайті є «хто був і скільки».
- **Умова — платний акаунт Zoom** (Pro і вище; безкоштовний не має ні звітів, ні минулих учасників) і **право створити Server-to-Server-застосунок** у Marketplace (вмикає власник або адміністратор акаунта). Якщо зустрічі йдуть з університетського акаунта і адміністратор не дасть — запасний шлях є (нижче), але гірший.
- **Розмір — M, одна сесія**, коли є облікові дані застосунку й ID зустрічі. Тому T222 починається з двох речей від тебе, не від коду.

## Що саме дає Zoom

- **Учасники минулої зустрічі** — `GET /past_meetings/{meetingId}/participants`: кожен сегмент присутності окремим рядком — `name` (як людина підписана), `user_email` (лише якщо вона увійшла в акаунт Zoom; за посиланням без входу — порожньо), `join_time`, `leave_time`, `duration` у секундах; хто вийшов і зайшов знову — кілька рядків. Пагінація по 300. Скоупи: класичні `meeting:read:admin` / `meeting:read`, гранулярний для S2S — `meeting:read:list_past_participants:admin`. Вимога — Pro+.
- **Той самий звіт із «Reports»** — `GET /report/meetings/{meetingId}/participants` (`report:read:list_meeting_participants:admin`): ті самі поля плюс `registrant_id`, `status`; широкий `report:read:admin` новим застосункам з травня 2024 не дають — лише гранулярні. «Dashboard» (`/metrics/…`) потребує Business+ — не наш випадок.
- **Екземпляри постійної зустрічі** — `GET /past_meetings/{meetingId}/instances`: якщо посилання на пару одне (recurring), кожне проведення має свій `uuid` і `start_time` — за датою заняття знаходимо потрібний; UUID із `/` або `//` треба двічі URL-кодувати. Глибина — до 15 місяців.
- **Бонус — хмарний запис** — `GET /meetings/{meetingId}/recordings` (`cloud_recording:read:list_recording_files[:admin]`): файли `MP4`, `M4A`, `TRANSCRIPT` (VTT з іменами й часом — те саме, що зараз руками зберігається як `zoom.txt`), `CHAT`, `CC`, `SUMMARY` (AI Companion), `download_url` (+ `download_access_token`), посилання на перегляд. Тобто **той самий виклик після заняття може принести і джерело для злиття, і чат, і лінк на відео, і відвідування** — якщо запис іде в хмару. Є й вебхуки `recording.completed` / `recording.transcript_completed` — для серверної автоматизації пізніше.
- Вебхуки `meeting.participant_joined/left` **не потрібні**: звіт після зустрічі повніший, а в цих подіях для неувійшлих учасників часто немає ні пошти, ні імені.

## Доступ: як підключитись

- **Server-to-Server OAuth** (рекомендований шлях): Marketplace → Develop → Build App → Server-to-Server OAuth; дає `Account ID`, `Client ID`, `Client Secret`; токен — `POST https://zoom.us/oauth/token?grant_type=account_credentials&account_id=…` з Basic-авторизацією, живе годину. Ніякого браузерного входу, працює з сервера й з Mac однаково. Увімкнути право на такі застосунки має власник/адмін акаунта (Role Settings → Advanced features).
- **Запасний шлях** — user-managed OAuth-застосунок (класичний): створює сам користувач, працює для його акаунта в режимі розробки без публікації; на форумі підтверджують, що `past_meetings/…/participants` ним доступний. Мінус — одноразова авторизація через браузер і refresh-токени; плюс — не треба адміністратора.
- Ключі — у `.env` сайту (`ZOOM_ACCOUNT_ID`, `ZOOM_CLIENT_ID`, `ZOOM_CLIENT_SECRET`), у git — нічого; локально — ті самі змінні для `bin/zoom`.

## Звʼязка «учасник → студент»

- `user_email` буде лише в тих, хто входить у Zoom з акаунтом (рідко); основа — **імʼя як підписано**, і це вже вирішено для транскриптів: `User.aliases` + ПІБ у двох порядках (`lesson_people.match`). Невідомі імена — у ту саму картку «хто це?» на сторінці заняття; привʼязав раз — працює і для реплік, і для відвідування, і для `roster` злиття.
- Викладач і співведучі — не рахуються; двоє з однаковим підписом — «невідомо», не вгадувати; телефонні учасники без імені — окремим рядком «без імені».
- «Був» — поріг: наприклад ≥ 25 % тривалості зустрічі або ≥ 20 хв (вибір — у T222); сегменти одного імені зливаються, перекриття — рахується раз; «запізнився на N хв» — від старту зустрічі (сегмент ведучого) до першого входу.

## Де показувати

- **На сторінці заняття** (`/lessons/pz1`) — блок «👥 Були · 48 із 57 · у середньому 1 год 12 хв»: аватарки за групами, під кожною хвилини, бліді — хто був менше порогу; викладачу — ще «невідомі» з «хто це?» і кнопка «Оновити із Zoom».
- **Окрема сторінка `/attendance`** (викладачу): матриця студенти × заняття, у клітинці хвилини як теплокарта (стиль `WeekHeat`), фільтри — група, вид заняття; підсумок на студента (занять, годин, частка); клік по заголовку — на заняття, по імені — на студента. Студентові — лише свій рядок, у профілі (пізніше, окремим вибором).
- Сховище — `attendance`: `lesson` (slug), `name` (як у Zoom), `nick` («» = невідомий), `segments: [{join, leave}]`, `seconds`, `late`, `meeting_uuid`, `fetched_at`; повторний забір замінює рядки заняття.

## Автоматизація — сходинки

1. **v1 (T222):** `bin/zoom pull pz1 --meeting <id|uuid>` з Mac (або кнопка на сторінці заняття → той самий код на сервері): учасники → `attendance`; за бажанням разом — VTT-транскрипт, чат і лінк на запис у джерела заняття. Запуск — руками після пари, 10 секунд.
2. **v2:** сервер сам після пари — за розкладом (ID зустрічі відомий) або за вебхуком `recording.completed`; алерт адміну «ПЗ 5: 44 учасники, 3 невідомі».
3. **v3:** після забору — одразу злиття на сервері (T182 етап 3) і конспект у бот — повний цикл «пара → сторінка» без рук.

## Обмеження й ризики

- Безкоштовний акаунт — нічого з цього не працює; університетський — залежить від адміністратора.
- Точні назви гранулярних скоупів і полів відповіді треба звірити в живому довіднику API перед кодом (форумні дописи 2019–2024).
- Zoom зберігає звіти ~рік, екземпляри — 15 місяців: забирати в тиждень після пари, не наприкінці семестру.
- Імена в Zoom люди міняють: аліасів у студента може бути кілька — це передбачено.
- Нічого персонального в URL і в git: ID зустрічі й ключі — лише в `.env`.

## Джерела

- [Zoom Meetings API (довідник)](https://developers.zoom.us/docs/api/meetings/) — `GET /meetings/{meetingId}/recordings`, типи файлів `TRANSCRIPT`/`CHAT`/`SUMMARY`, скоупи `cloud_recording:read:list_recording_files`.
- [Server-to-Server OAuth](https://developers.zoom.us/docs/internal-apps/s2s-oauth/) і [Why use server-to-server OAuth](https://developers.zoom.us/blog/why-use-server-to-server-oauth/) — створення застосунку, `account_credentials`, права ролі.
- [Zoom past meeting participants query](https://devforum.zoom.us/t/zoom-past-meeting-participants-query/121823), [Get list of zoom meeting participants](https://devforum.zoom.us/t/get-list-of-zoom-meeting-participants/52617), [API call to get meeting participants info including joined/leave time](https://devforum.zoom.us/t/api-call-to-get-meeting-participants-info-including-joined-leave-time/62294) — Pro+, поля часу, обмеження.
- [Getting Participants For All Past Meetings](https://devforum.zoom.us/t/getting-participants-for-all-past-meetings/10205), [Get User's Meetings, Past Instances and Participants](https://devforum.zoom.us/t/get-users-meetings-meetings-past-instances-and-past-meeting-instances-participants/37995) — екземпляри recurring-зустрічі, UUID.
- [Is it possible to get participants details and recordings in user level app](https://devforum.zoom.us/t/is-it-possible-to-get-participants-details-and-recordings-in-user-level-app/57490), [API access to user report for past participants](https://devforum.zoom.us/t/api-access-to-user-report-for-past-participants/42380) — user-level застосунок як запасний шлях; звіти — адмінський скоуп.
- [Cannot access report:read:admin scope](https://devforum.zoom.us/t/cannot-access-reportadmin-or-equivalent-scope-access-for-zoom-api-account-level-reporting/138102), [Worklytics: Zoom scopes](https://docs.worklytics.co/psoxy/sources/zoom) — гранулярні скоупи замість `report:read:admin`.
- [No way to identify a participant in the meeting.participant_joined webhook](https://devforum.zoom.us/t/no-way-to-identify-a-participant-in-the-meeting-participant-joined-webhook/10973), [Email … is now blank](https://devforum.zoom.us/t/email-passed-when-participant-joins-a-meeting-is-now-blank-since-yesterday/65066) — чому вебхуки не опора.
- [zoomR: getPastMeetingParticipants](https://samterfa.github.io/zoomR/reference/getPastMeetingParticipants.html) — «Paid account on a Pro or higher plan», скоупи `meeting:read:admin meeting:read`.

## Твої думки та питання

> 
