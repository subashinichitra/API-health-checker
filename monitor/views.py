from django.shortcuts import render
import time
import requests
from .models import HealthCheck, ApiEndpoint


def get_status_text(status_code: int) -> str:
    """
    Map status code to human readable text.
    """
    names = {
        200: "OK",
        201: "Created",
        204: "No Content",
        301: "Moved Permanently",
        302: "Found (Redirect)",
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        500: "Internal Server Error",
        502: "Bad Gateway",
        503: "Service Unavailable",
        0:   "No HTTP response",  # our custom code for connection errors
    }
    if status_code in names:
        return names[status_code]
    if 200 <= status_code < 300:
        return "Success"
    if 300 <= status_code < 400:
        return "Redirection"
    if 400 <= status_code < 500:
        return "Client Error"
    if 500 <= status_code < 600:
        return "Server Error"
    return "Unknown Status"


def get_health_category(status_code: int) -> str:
    """
    Real-time monitoring style:
    - 2xx  -> Healthy / UP
    - 3xx  -> UP but Redirected
    - 4xx+ or 0 -> DOWN / Error
    """
    if 200 <= status_code < 300:
        return "UP"
    if 300 <= status_code < 400:
        return "UP (Redirect)"
    return "DOWN"


def home(request):
    """
    API health checker:
    - If ?url=... is given, we call that URL and store the result.
    - We show the last 10 checks in a table.
    - We show favourite APIs from ApiEndpoint.
    - We show uptime summary for each URL.
    """
    result = None
    url = request.GET.get('url')

    if url:
        # measure time ourselves so we also get timing for failures
        start = time.perf_counter()
        try:
            response = requests.get(url, timeout=5)
            elapsed_ms = (time.perf_counter() - start) * 1000
            status_code = response.status_code

            health_category = get_health_category(status_code)
            status_text = get_status_text(status_code)
            is_up = health_category.startswith("UP")  # 2xx and 3xx

            result = {
                "url": url,
                "status_code": status_code,
                "is_up": is_up,
                "health_category": health_category,
                "status_text": status_text,
                "response_time_ms": elapsed_ms,
            }

            # Save to database
            HealthCheck.objects.create(
                url=url,
                status_code=status_code,
                is_up=is_up,
                response_time_ms=elapsed_ms,
            )

        except requests.exceptions.RequestException as e:
            elapsed_ms = (time.perf_counter() - start) * 1000

            # no HTTP response -> use custom status code 0
            status_code = 0
            health_category = "DOWN"
            status_text = get_status_text(status_code)
            error_text = str(e)

            result = {
                "url": url,
                "status_code": status_code,
                "is_up": False,
                "health_category": health_category,
                "status_text": status_text,
                "error": error_text,
                "response_time_ms": elapsed_ms,
            }

            # Save failure to database (still record time and code 0)
            HealthCheck.objects.create(
                url=url,
                status_code=status_code,
                is_up=False,
                response_time_ms=elapsed_ms,
                error_message=error_text,
            )

    # Get last 10 checks (newest first)
    recent_checks = HealthCheck.objects.order_by('-checked_at')[:10]

    # Get favourite APIs
    favorite_apis = ApiEndpoint.objects.all()

    # --- UPTIME STATS (very simple) ---
    all_checks = HealthCheck.objects.order_by('-checked_at')

    stats_by_url = {}
    for check in all_checks:
        url_key = check.url
        if url_key not in stats_by_url:
            stats_by_url[url_key] = {
                "url": url_key,
                "total": 0,
                "up": 0,
                "last_checked": check.checked_at,
            }
        stats_by_url[url_key]["total"] += 1
        if check.is_up:
            stats_by_url[url_key]["up"] += 1

    uptime_stats = []
    for data in stats_by_url.values():
        total = data["total"]
        up = data["up"]
        uptime_percent = (up / total) * 100 if total > 0 else 0
        uptime_stats.append({
            "url": data["url"],
            "total": total,
            "up": up,
            "uptime_percent": uptime_percent,
            "last_checked": data["last_checked"],
        })

    uptime_stats.sort(key=lambda x: x["last_checked"], reverse=True)

    return render(
        request,
        "monitor/home.html",
        {
            "result": result,
            "recent_checks": recent_checks,
            "favorite_apis": favorite_apis,
            "uptime_stats": uptime_stats,
        },
    )


def history(request):
    """
    Show full history for a single URL.
    URL expected as query parameter: /history/?url=...
    """
    url = request.GET.get('url')
    checks = []
    if url:
        checks = HealthCheck.objects.filter(url=url).order_by('-checked_at')

    context = {
        "url": url,
        "checks": checks,
    }
    return render(request, "monitor/history.html", context)
