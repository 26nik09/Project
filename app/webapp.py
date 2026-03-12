from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["webapp"])


@router.get("/webapp", response_class=HTMLResponse)
async def webapp_index() -> str:
    return """
<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>Home Services</title>
  <script src=\"https://telegram.org/js/telegram-web-app.js\"></script>
  <style>
    body { font-family: Arial, sans-serif; padding: 16px; background: #f7f7f7; color: #111; }
    .card { background: #fff; padding: 12px; border-radius: 10px; margin-bottom: 8px; box-shadow: 0 1px 3px rgba(0,0,0,.1); }
    .muted { color: #555; font-size: 14px; }
  </style>
</head>
<body>
  <h2>Home Services</h2>
  <p class=\"muted\">Telegram WebApp is connected. Categories:</p>
  <div id=\"list\">Loading...</div>

  <script>
    const tg = window.Telegram?.WebApp;
    if (tg) tg.ready();

    async function loadCategories() {
      const list = document.getElementById('list');
      try {
        const res = await fetch('/taxonomy/categories');
        const data = await res.json();
        if (!Array.isArray(data) || data.length === 0) {
          list.innerHTML = '<div class="card">No categories yet</div>';
          return;
        }
        list.innerHTML = data
          .map((c) => `<div class=\"card\"><strong>${c.name_en}</strong><div class=\"muted\">${c.slug}</div></div>`)
          .join('');
      } catch (e) {
        list.innerHTML = '<div class="card">Failed to load categories</div>';
      }
    }

    loadCategories();
  </script>
</body>
</html>
"""
