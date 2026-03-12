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
    .row { display: flex; gap: 8px; margin-bottom: 12px; }
    input, select { padding: 8px; border-radius: 8px; border: 1px solid #ccc; width: 100%; }
    button { padding: 8px 10px; border-radius: 8px; border: none; background: #2f80ed; color: #fff; cursor: pointer; }
    .card { background: #fff; padding: 12px; border-radius: 10px; margin-bottom: 8px; box-shadow: 0 1px 3px rgba(0,0,0,.1); }
    .muted { color: #555; font-size: 14px; }
  </style>
</head>
<body>
  <h2>Home Services</h2>
  <div class=\"row\">
    <input id=\"q\" placeholder=\"Search by name or text\" />
    <input id=\"city\" placeholder=\"City\" />
  </div>
  <div class=\"row\">
    <select id=\"sort\">
      <option value=\"newest\">Newest</option>
      <option value=\"name_asc\">Name A-Z</option>
    </select>
    <button id=\"searchBtn\">Search</button>
  </div>

  <div id=\"list\">Loading masters...</div>

  <h3>Booking request</h3>
  <div class=\"card\">
    <div class=\"row\">
      <input id=\"clientTelegramId\" placeholder=\"Your Telegram ID\" />
      <input id=\"selectedMasterId\" placeholder=\"Master ID\" readonly />
    </div>
    <div class=\"row\">
      <input id=\"serviceName\" placeholder=\"Service name\" />
      <input id=\"scheduledFor\" type=\"datetime-local\" />
    </div>
    <div class=\"row\">
      <input id=\"notes\" placeholder=\"Notes\" />
      <button id=\"bookBtn\">Create Request</button>
    </div>
    <div id=\"bookingMsg\" class=\"muted\"></div>
  </div>

  <script>
    const tg = window.Telegram?.WebApp;
    if (tg) tg.ready();

    async function loadMasters() {
      const list = document.getElementById('list');
      const q = document.getElementById('q').value.trim();
      const city = document.getElementById('city').value.trim();
      const sort = document.getElementById('sort').value;

      const params = new URLSearchParams({ sort, limit: '20', offset: '0' });
      if (q) params.set('q', q);
      if (city) params.set('city', city);

      try {
        const res = await fetch('/catalog/masters?' + params.toString());
        const data = await res.json();
        if (!Array.isArray(data) || data.length === 0) {
          list.innerHTML = '<div class="card">No masters found</div>';
          return;
        }
        list.innerHTML = data
          .map((m) => `
            <div class=\"card\">
              <strong>${m.display_name}</strong>
              <div class=\"muted\">ID: ${m.id}</div>
              <div class=\"muted\">${m.city}, ${m.district}</div>
              <div class=\"muted\">Status: ${m.online_status ? 'Online' : 'Offline'}</div>
              <button onclick=\"selectMaster(${m.id}, '${m.display_name.replace(/'/g, "\\'")}')\">Choose</button>
            </div>
          `)
          .join('');
      } catch (e) {
        list.innerHTML = '<div class="card">Failed to load masters</div>';
      }
    }

    window.selectMaster = function (masterId, name) {
      document.getElementById('selectedMasterId').value = String(masterId);
      const msg = document.getElementById('bookingMsg');
      msg.textContent = `Selected master: ${name}`;
    }

    async function createBooking() {
      const msg = document.getElementById('bookingMsg');
      msg.textContent = '';

      const clientTelegramId = Number(document.getElementById('clientTelegramId').value);
      const masterId = Number(document.getElementById('selectedMasterId').value);
      const serviceName = document.getElementById('serviceName').value.trim();
      const scheduledForRaw = document.getElementById('scheduledFor').value;
      const notes = document.getElementById('notes').value.trim();

      if (!clientTelegramId || !masterId || !serviceName || !scheduledForRaw) {
        msg.textContent = 'Fill Telegram ID, master, service and date/time';
        return;
      }

      const scheduled_for = new Date(scheduledForRaw).toISOString();

      const res = await fetch('/bookings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          client_telegram_id: clientTelegramId,
          master_id: masterId,
          service_name: serviceName,
          scheduled_for,
          notes: notes || null,
        }),
      });

      if (!res.ok) {
        msg.textContent = 'Failed to create request';
        return;
      }

      const data = await res.json();
      msg.textContent = `Request #${data.id} created (${data.status})`;
    }

    document.getElementById('searchBtn').addEventListener('click', loadMasters);
    document.getElementById('bookBtn').addEventListener('click', createBooking);
    loadMasters();
  </script>
</body>
</html>
"""
