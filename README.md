# ManhwaFlare

Telegram manhwa PDF bot · multi-source · premium plans

**Owner:** @flexyy · **Network:** @DragonByte_network

## Deploy (Heroku)

1. Set config vars: `BOT_TOKEN`, `OWNER_ID`, `MONGODB_URI`
2. Optional: `LOG_CHANNEL_ID`, `SUPPORT_GROUP`, `SUPPORT_CHANNEL`
3. Deploy worker dyno (`Procfile`)

```
worker: PYTHONPATH=. python -m Manhwaflare.main
```

## Package

`Manhwaflare/` — core · handlers · scrapers · plugins · ui

Do not remove credits.


## Render (free plan)

1. New → Web Service (not Background Worker — free workers are paid)
2. Connect repo · Runtime Python
3. Build: `pip install -r requirements.txt`
4. Start: `PYTHONPATH=. python -m Manhwaflare.main`
5. Env: `BOT_TOKEN` `OWNER_ID` `MONGODB_URI` + set `RENDER=true`
6. Health path: `/health`

Bot polls Telegram + serves `/health` on `$PORT` so free web service stays valid.

For ffmpeg (AI videos): use the included `Dockerfile` (Docker runtime on Render).
