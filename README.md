API Health Checker 

A simple web application built with Python (Django) that checks the health of any API endpoint in real time.  
It sends HTTP requests to a given URL, records the response, and shows you status, response time, and uptime statistics.

FEATURES

- ✅ Check Any API Endpoint
  - Enter any HTTP/HTTPS URL and check its health instantly.
  - Works with REST APIs, websites, and test URLs.

- ✅ Real-Time Status Classification
  - 2xx → UP (Healthy)
  - 3xx → UP (Redirect) – service reachable but redirected
  - 4xx / 5xx → DOWN (Error)

- ✅ HTTP Status Details
  - Shows HTTP status code (200, 301, 404, 500, …)
  - Shows status meaning (OK, Not Found, Internal Server Error, etc.)
  - Handles “no response” cases with a custom status code (0 – No HTTP response).

- ✅ Response Time Monitoring
  - Measures and displays response time in milliseconds for each request.

- ✅ Recent Checks Table
  - Shows the latest checks with:
    - URL  
    - Status (UP / DOWN / UP (Redirect))  
    - Status code  
    - Response time  
    - Checked at (timestamp)

- ✅ Uptime Summary
  - Groups checks by URL.
  - Calculates:
    - Total checks  
    - UP count  
    - Uptime percentage (UP count / Total * 100)  
    - Last checked time  

- ✅ Per-URL History Page
  - Click on a URL in the Uptime Summary to open the full history for that endpoint.
  - Shows status, code, response time, error (if any), and time for each check.

- ✅ Favourite Endpoints
  - Manage favourite APIs using Django admin (`ApiEndpoint` model).
  - Quick buttons on the dashboard let you check them with one click.

- ✅ Error Handling
  - Handles:
    - Timeouts
    - Connection errors
    - Remote server closing connection without response
  - Marks them as DOWN, records response time, and stores error message.

- ✅ Simple & Clean UI
  - Minimal HTML + CSS design.
  - Dark outer background with a centered white card.
  - Easy to understand and perfect for academic/demo projects.


 Tech Stack

- Language: Python 3  
- Framework:  Django  
-  Frontend: HTML, CSS (custom)  
- HTTP Client: `requests` library  
- Database: SQLite (default Django database)  

PROJECT STRUCTURE 

api_health_checker_project/
├─ manage.py
├─ README.md
├─ README.txt
├─ api_health_checker/
│  ├─ settings.py
│  ├─ urls.py
│  ├─ wsgi.py
│  └─ ...
└─ monitor/
   ├─ models.py            # HealthCheck, ApiEndpoint
   ├─ views.py             # home, history
   ├─ urls.py              # app-level URLs
   ├─ templates/monitor/
   │  ├─ home.html         # main dashboard
   │  └─ history.html      # per-URL history
   └─ static/monitor/
      └─ style.css         # basic styling
