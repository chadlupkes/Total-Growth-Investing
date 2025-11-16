```markdown
# Plan & Next Steps

Goal
- Start by automating raw-data collection reliably with free sources.
- Then normalize and version the raw data, map your Sheets formulas to code, and expose an API to feed web/mobile apps.

Roadmap (short)
1. Raw data: script (done)
2. Data model: pick canonical CSV/JSON fields and document required keys
3. Normalization: handle missing values, types, currencies
4. Ranking implementation: translate Sheets formulas into unit-tested functions (Python/JS)
5. Persistence & API: small backend (FastAPI or Node) + SQLite or small DB
6. Frontend: React web + Expo React Native for mobile
7. Cron/scheduler: GitHub Actions schedule or Cloud function

Hosting ideas (free/low cost)
- Backend: Render free tier, Railway free tier, or GitHub Actions + artifacts for scheduled runs
- Frontend: Vercel / Netlify for static React app
- Mobile: Expo (free) to publish/test easily

Data source considerations
- yfinance (used here) — practical and free but not an official API
- Alpha Vantage, Finnhub — free tiers, may require API key and have limits
- Paid feeds only when you need high availability / wider coverage

Security
- Never commit API keys or Google credentials. Use GitHub Secrets or cloud secret stores.
```
