# StockScope

FastAPI backend for tracking stocks, watchlists, and market sentiment. It uses PostgreSQL, JWT auth with email verification, and [Finnhub](https://finnhub.io/) for market data.

## Prerequisites

- Python 3.9 or newer
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- PostgreSQL
- A [Finnhub API key](https://finnhub.io/register)
- A Gmail account with an [App Password](https://support.google.com/accounts/answer/185833) (used to send verification emails)

## Local setup

### 1. Clone and install

```bash
git clone <repo-url>
cd StockScope
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

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

| Variable | Description |
| --- | --- |
| `DB_CONNECTION` | SQLAlchemy URL, e.g. `postgresql+psycopg2://USER:PASSWORD@localhost:5432/stockscope` |
| `SECRET_KEY` | Secret used to sign JWTs |
| `ALGORITHM` | JWT algorithm (use `HS256`) |
| `EXP_TIME` | Access token lifetime in minutes |
| `FINNHUB_API_KEY` | API key from [finnhub.io](https://finnhub.io/) |
| `MAIL_USERNAME` | Gmail address that sends verification emails |
| `MAIL_PASSWORD` | Gmail App Password (not your normal Gmail password) |

The app loads `.env` from the project root.

### 4. Run database migrations

```bash
uv run alembic upgrade head
```

On first start the app also creates missing tables via SQLAlchemy `create_all`. Alembic is still the way to apply later schema changes.

### 5. Start the server

```bash
uv run server
```

The API is at [http://127.0.0.1:8000](http://127.0.0.1:8000). Interactive docs:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## API overview

| Prefix | Description |
| --- | --- |
| `/api/auth` | Register, verify email, login |
| `/api/user` | Current user |
| `/api/stocks` | Quotes, news, insider data |
| `/api/watchlist` | Watchlist CRUD |
| `/api/admin` | Admin endpoints |

Registration sends a 6-digit code to the user’s email. Confirm it with `POST /api/auth/verify` before logging in.
