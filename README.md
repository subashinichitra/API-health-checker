````markdown
# API Health Checker ✅

A simple Django web app that checks the health of API endpoints in real time.  
It sends an HTTP request to a URL and shows the status, status code, response time, and uptime.

---

## API HEALTH CHECKER

- Backend: **Python 3 + Django**
- Frontend: **HTML + CSS**
- Database: **SQLite** (default Django database)
- HTTP client: **requests** library

The app is designed as a small, readable project that is easy to explain in a viva or interview.

---

## FEATURES

- ✅ Check any HTTP/HTTPS endpoint
- ✅ Classify responses:
  - 2xx → **UP**
  - 3xx → **UP (Redirect)**
  - 4xx / 5xx / network error → **DOWN**
- ✅ Show HTTP status code and short meaning  
  (e.g. 200 OK, 404 Not Found, 500 Internal Server Error)
- ✅ Measure and display response time in milliseconds
- ✅ Recent checks table  
  (URL, Status, Status Code, Response Time, Checked At)
- ✅ Uptime summary per URL  
  (Total Checks, UP Count, Uptime %, Last Checked)
- ✅ History page for each URL
- ✅ Favourite endpoints (managed via Django admin)
- ✅ Error handling for timeouts, connection errors, and no response

---

## PREREQUISITES

- Python **3.10+**
- `pip` installed
- (Recommended) Virtual environment using `python -m venv`
- Git (if you want to clone from GitHub)

---

## INSTALLATION

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/API-health-checker.git
   cd API-health-checker
````

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   venv\Scripts\activate          # Windows
   # source venv/bin/activate     # Linux / macOS
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   # or at minimum:
   # pip install django requests
   ```

4. **Apply database migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (for Django admin and favourite APIs)**

   ```bash
   python manage.py createsuperuser
   ```

---

## DEVELOPMENT

Run the development server:

```bash
python manage.py runserver
```

Open the app in your browser:

* Dashboard: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* Admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

While developing, Django will automatically reload the server when you change code.

---

## BUILDING

For simple college/demo usage, `runserver` is enough.
For a more “production-like” setup:

1. Set `DEBUG = False` and update `ALLOWED_HOSTS` in `api_health_checker/settings.py`.

2. Collect static files:

   ```bash
   python manage.py collectstatic
   ```

3. Deploy with a proper server (e.g. Gunicorn + Nginx) if needed.

---

## PROJECT STRUCTURE

```text
api_health_checker_project/
├─ manage.py
├─ README.md
├─ api_health_checker/
│  ├─ settings.py          # Django settings
│  ├─ urls.py              # Root URL configuration
│  └─ ...
└─ monitor/
   ├─ models.py            # HealthCheck, ApiEndpoint
   ├─ views.py             # home(), history()
   ├─ urls.py              # App URL routes
   ├─ templates/monitor/
   │  ├─ home.html         # Main dashboard
   │  └─ history.html      # Per-URL history
   └─ static/monitor/
      └─ style.css         # Simple styling
```

---

## USAGE

1. Open the **dashboard** (`/`).
2. Enter an API URL (for example `https://jsonplaceholder.typicode.com/posts`) and click **Check Health**.
3. Read the **Result** card:

   * Status (UP / DOWN / UP (Redirect))
   * Status code
   * Meaning
   * Response time (ms)
4. Scroll down to:

   * **Recent Checks** – last few checks for all URLs.
   * **Uptime Summary** – uptime statistics grouped by URL.
5. To manage favourite APIs:

   * Go to `/admin/`
   * Add `ApiEndpoint` objects (name + URL)
   * They appear as quick buttons on the dashboard.

---

## API ENDPOINTS (OF THIS APP)

This project mainly provides a web UI. Important routes:

* `GET /`
  Main dashboard. Optional `?url=<encoded-url>` query runs a health check.

* `GET /history/?url=<encoded-url>`
  Shows full history for a single URL.

* `GET /admin/`
  Django admin panel for users, HealthCheck, and ApiEndpoint models.

All external checks are done internally using `requests.get()`.

---

## PERFORMANCE OPTIMIZATION

Current design is simple and synchronous (good for learning).
Ideas to improve performance if needed:

* Use a shared `requests.Session` to reuse HTTP connections.
* Tune timeouts (already using a small timeout to avoid hanging).
* Limit or archive very old `HealthCheck` rows if the database becomes large.
* Move scheduled/automatic checks into a background worker
  (Celery, cron job, or a separate script).

---

## TROUBLESHOOTING

**1. `ModuleNotFoundError: No module named 'django'`**

Install dependencies inside the virtual environment:

```bash
pip install django requests
```

---

**2. `python: command not found` or multiple Python versions**

Try one of:

```bash
py manage.py runserver          # Windows (py launcher)
python3 manage.py runserver     # Linux / macOS
```

---

**3. CSS not loading**

* Make sure `DEBUG = True` in `settings.py` (for development).
* Check that your template has:

  ```html
  {% load static %}
  <link rel="stylesheet" href="{% static 'monitor/style.css' %}">
  ```

---

**4. Database / migration errors**

Run:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

**5. Uptime always 0% or 100%**

Uptime is calculated per URL:

* If every check for that URL is UP → **100%**
* If every check is DOWN → **0%**
* You get values in between only when the **same URL** has both UP and DOWN results.
  Example test URL:

  ```text
  https://httpbin.org/status/200,500
  ```

This endpoint randomly returns 200 or 500, so uptime will be around 40–60%.

---

```
```
