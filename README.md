# StockScope

FastAPI backend for tracking stocks, watchlists, price alerts, and notes. It uses PostgreSQL, JWT auth with email verification, [Finnhub](https://finnhub.io/) for market data, and [Alternative.me](https://alternative.me/crypto/fear-and-greed-index/) for market sentiment.

## Features

- Register, verify email, and log in with JWT
- Live quotes, company news, and insider transactions
- Fear & Greed market sentiment
- Watchlists with per-item quotes
- Price alerts (`ABOVE` / `BELOW`) with email when a target is hit
- Notes attached to a stock symbol

## Prerequisites

- Python 3.9 or newer
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- PostgreSQL
- A [Finnhub API key](https://finnhub.io/register)
- A Gmail account with an [App Password](https://support.google.com/accounts/answer/185833) (verification, welcome, and alert emails)

## Local setup

### 1. Clone and install

```bash
git clone https://github.com/Hydra016/StockScopeAPI.git
cd StockScopeAPI
uv sync
```

With pip instead of uv:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
```

### 2. Create a database

```bash
createdb stockscope
```

Or in `psql`:

```sql
CREATE DATABASE stockscope;
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
DB_CONNECTION=postgresql+psycopg2://USER:PASSWORD@localhost:5432/stockscope
SECRET_KEY=change-me
ALGORITHM=HS256
EXP_TIME=60
FINNHUB_API_KEY=your-finnhub-key
MAIL_USERNAME=you@gmail.com
MAIL_PASSWORD=your-gmail-app-password
```

| Variable | Description |
| --- | --- |
| `DB_CONNECTION` | SQLAlchemy URL for PostgreSQL |
| `SECRET_KEY` | Secret used to sign JWTs |
| `ALGORITHM` | JWT algorithm (`HS256`) |
| `EXP_TIME` | Access token lifetime in minutes |
| `FINNHUB_API_KEY` | API key from [finnhub.io](https://finnhub.io/) |
| `MAIL_USERNAME` | Gmail address that sends mail |
| `MAIL_PASSWORD` | Gmail App Password (not your normal Gmail password) |

### 4. Run database migrations

```bash
uv run alembic upgrade head
```

On first start the app also creates missing tables via SQLAlchemy `create_all`. Use Alembic for later schema changes.

### 5. Start the server

```bash
uv run server
```

The API is at [http://127.0.0.1:8000](http://127.0.0.1:8000). Interactive docs:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Auth

1. `POST /api/auth/register` stores a pending registration and emails a 6-character code (expires in 10 minutes).
2. `POST /api/auth/verify` creates the user and sends a welcome email.
3. `POST /api/auth/login` returns a JWT.

Send the token on protected routes:

```
Authorization: Bearer <token>
```

## API overview

| Prefix | Description |
| --- | --- |
| `/api/auth` | Register, verify email, login |
| `/api/user` | Current user |
| `/api/stocks` | Quote, news, insider data, market sentiment |
| `/api/watchlist` | Watchlists and symbols |
| `/api/alerts` | Price alerts and trigger check |
| `/api/notes` | Notes per stock |
| `/api/admin` | List and delete users |

### Alerts

Create an alert with a symbol, target price, and `ABOVE` or `BELOW`. `POST /api/alerts/check` compares each active alert to the live Finnhub quote. When it fires, the alert is marked inactive and an email is sent.

### Notes

Notes belong to the current user and a stock symbol. Title and content can be updated; the symbol is set on create.

## Project layout

```
controllers/   request handling and business rules
models/        SQLAlchemy tables
routes/        FastAPI routers
schemas/       Pydantic request/response models
services/      Finnhub, sentiment, mail, price checks
utils/         DB session, settings, auth helper
alembic/       migrations
```
