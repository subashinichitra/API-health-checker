
# API Health Checker ✅

A lightweight web app built with **Django** that continuously checks API endpoints and shows their real-time health, response time, and uptime.

---

## Features

- ✅ Check any HTTP/HTTPS endpoint
- ✅ Classify responses:
  - 2xx → **UP**
  - 3xx → **UP (Redirect)**
  - 4xx / 5xx / errors → **DOWN**
- ✅ Show status code + human-friendly meaning (OK, Not Found, Internal Server Error, …)
- ✅ Measure response time in milliseconds
- ✅ Recent checks table (URL, status, code, time, timestamp)
- ✅ Uptime summary per URL (total checks, UP count, uptime %)
- ✅ Detailed history page for each endpoint
- ✅ Favourite APIs (managed via Django admin) with one-click checks
- ✅ Handles timeouts / connection errors and stores the error message

---

## Prerequisites

Make sure you have:

- Python **3.10+** installed  
- `pip` available in your terminal  
- (Optional but recommended) **virtualenv** or `python -m venv`  

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/API-health-checker.git
   cd API-health-checker
````

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   venv\Scripts\activate    # Windows
   # source venv/bin/activate   # Linux / macOS
   ```

3. **Install dependencies**

   If you have `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

   Or at minimum:

   ```bash
   pip install django requests
   ```

4. **Apply database migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (for Django admin & favourite APIs)**

   ```bash
   python manage.py createsuperuser
   ```

---

## Development

Start the development server:

```bash
python manage.py runserver
```

Open:

* Dashboard: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* Admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

While developing, the server reloads on code changes.

---

## Building / Production (basic)

Minimal example for a simple production-like run (still using `runserver`):

1. Set `DEBUG = False` and configure `ALLOWED_HOSTS` in `api_health_checker/settings.py`.

2. Collect static files:

   ```bash
   python manage.py collectstatic
   ```

3. Use a proper server (e.g. `gunicorn` + Nginx) in real deployments.
   For college/demo projects, `runserver` is usually enough.

---

## Project Structure

```text
api_health_checker_project/
├─ manage.py
├─ README.md
├─ api_health_checker/
│  ├─ settings.py          # Django settings
│  ├─ urls.py              # root URL routes
│  └─ ...
└─ monitor/
   ├─ models.py            # HealthCheck, ApiEndpoint
   ├─ views.py             # home(), history()
   ├─ urls.py              # app URL routes
   ├─ templates/monitor/
   │  ├─ home.html         # main dashboard
   │  └─ history.html      # per-URL history
   └─ static/monitor/
      └─ style.css         # simple styling
```

---

## Usage

1. Open the **dashboard**.
2. Type an API URL (for example `https://jsonplaceholder.typicode.com/posts`) and click **Check Health**.
3. View:

   * Result card → current status, code, meaning, response time
   * **Recent Checks** → last N checks for all URLs
   * **Uptime Summary** → uptime statistics grouped by URL
4. To manage favourite endpoints:

   * Go to `/admin/`
   * Add `ApiEndpoint` entries (name + URL)
   * They appear as quick buttons on the dashboard.

---

## API Endpoints (of this app)

This project is mainly a **web UI**, but important routes are:

* `GET /`
  Dashboard. Accepts optional `?url=<encoded-url>` query parameter to trigger a health check.

* `GET /history/?url=<encoded-url>`
  Full history table for a single URL.

* `GET /admin/`
  Django admin panel for managing `HealthCheck`, `ApiEndpoint`, and users.

Internal checks are done from the backend using `requests.get()`.

---

## Performance Optimization (ideas)

The current version is synchronous and simple (perfect for learning).
Possible optimizations:

* Use a **session** from `requests` to reuse connections.
* Add a reasonable timeout (already using `timeout=5` to avoid hanging).
* Limit number of stored history rows or archive old data if the database grows.
* Offload scheduled checks to a background worker (Celery / cron) instead of running everything from the UI.

---

## Troubleshooting

**1. `ModuleNotFoundError: No module named 'django'`**
→ Install dependencies inside your virtual environment:

```bash
pip install django requests
```

**2. `python: command not found` or multiple Python versions**
→ Try:

```bash
py manage.py runserver       # Windows
python3 manage.py runserver  # Linux / macOS
```

**3. Static files (CSS) not loading**
→ In development, make sure `DEBUG = True` and you included:

```html
{% load static %}
<link rel="stylesheet" href="{% static 'monitor/style.css' %}">
```

**4. Database errors after changing models**
→ Run:

```bash
python manage.py makemigrations
python manage.py migrate
```

**5. Uptime always 0% or 100%**
→ Uptime is per URL:

* If all checks for a URL are UP → 100%
* If all are DOWN → 0%
* You will see in-between values only when the **same URL** has a mix of UP and DOWN over time (e.g. `https://httpbin.org/status/200,500`).

---


