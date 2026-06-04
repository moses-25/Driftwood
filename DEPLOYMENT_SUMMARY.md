# Driftwood Café — Deployment Summary

## Services

| Service | Platform | URL | Branch |
|---------|----------|-----|--------|
| **Backend** (Flask API) | Render | https://driftwood-backend.onrender.com | `backup` |
| **Database** (PostgreSQL) | Render | Internal via `DATABASE_URL` | — |
| **Frontend** (React + Vite) | Vercel | https://driftwood-taupe.vercel.app | `backup` |

---

## Backend Fixes

### `server/database/connection.py`
- **Removed** hardcoded PostgreSQL credentials (`postgres:ochiengmose@localhost:5432`)
- Now reads `DATABASE_URL` from environment variables
- Added `postgres://` → `postgresql://` scheme conversion (Render provides `postgres://` but SQLAlchemy requires `postgresql://`)
- Gracefully handles missing `DATABASE_URL` (skips connection test instead of crashing)

### `server/config.py`
- Added `postgres://` → `postgresql://` scheme conversion for `SQLALCHEMY_DATABASE_URI`
- Removed debug `print()` statement

### `server/app.py`
- Connection test now uses Flask-SQLAlchemy's `db.engine` (not a separate raw engine from `connection.py`)
- Wrapped `db.engine` access inside `app.app_context()` to fix `"Working outside of application context"` error
- Connection test passes the `app` object for proper context

### Render Deployment
- Validated `server/render.yaml` Blueprint (2 resources: web service + database)
- Updated `CLIENT_ORIGIN` env var to `https://driftwood-taupe.vercel.app` for CORS
- Triggered redeploy after env var change

---

## Frontend Fixes

### `client/vercel.json`
- Removed SPA catch-all rewrites (app uses hash routing — server only sees `/`)
- Set `framework: "vite"` for `@vercel/vite` builder (handles static assets + SPA natively)
- Kept cache-control headers for `assets/` directory

### `client/index.html`
- Replaced external favicon files with inline emoji SVG data URI (`☕`)
- Removed OG/Twitter image meta tags referencing `/Driftwood.png` (not served by Vercel)
- Removed preload links for hero videos (`/2.mp4`, `/wood.mp4`)
- Removed unused Open Graph image references

### Asset imports (moved from `public/` to `src/assets/`)
| File | Moved To | Used By |
|------|----------|---------|
| `public/Driftwood.png` | `src/assets/logo.png` | `Navbar.jsx`, `Footer.jsx`, `Hero.jsx` (poster) |
| `public/2.mp4` | `src/assets/hero.mp4` | `Hero.jsx` (background video) |
| `public/wood.mp4` | Deleted | Was preloaded but unused at runtime |
| `public/icon.svg` | Deleted | Replaced by inline favicon |
| `public/favicon.ico` | Deleted | Replaced by inline favicon |
| `public/Driftwood.svg` | Deleted | Was unused |

### Component Changes
- **`Navbar.jsx`**: Added `import logo from '../assets/logo.png'`, changed `<img src="/Driftwood.png">` to `<img src={logo}>`
- **`Footer.jsx`**: Same import and src change
- **`Hero.jsx`**: Added `import logo from '../assets/logo.png'` and `import heroVideo from '../assets/hero.mp4?url'`, changed `src="/2.mp4"` to `src={heroVideo}`, changed `poster="/Driftwood.png"` to `poster={logo}`

### Why
Vercel's `@vercel/vite` builder does not serve files placed in the Vite `public/` directory (which end up at the root of `dist/`). Only files in `dist/assets/` are served correctly. Importing assets as JavaScript modules causes Vite to place them in `dist/assets/` with content hashes.

---

## Environment Variables

### Backend (Render)

| Variable | Status | Value |
|----------|--------|-------|
| `DATABASE_URL` | Auto-wired | Render Postgres connection string |
| `CLIENT_ORIGIN` | Set | `https://driftwood-taupe.vercel.app` |
| `SECRET_KEY` | Auto-generated | — |
| `JWT_SECRET_KEY` | Auto-generated | — |
| `APP_URL` | Set via Dashboard | `https://driftwood-backend.onrender.com` |
| `MPESA_CONSUMER_KEY` | Set via Dashboard | — |
| `MPESA_CONSUMER_SECRET` | Set via Dashboard | — |
| `MPESA_SHORTCODE` | Set via Dashboard | — |
| `MPESA_PASSKEY` | Set via Dashboard | — |

### Frontend (Vercel)

| Variable | Value |
|----------|-------|
| `VITE_API_URL` | `https://driftwood-backend.onrender.com` |

---

## Steps Applied

1. Fixed hardcoded localhost database credentials
2. Added `postgres://` → `postgresql://` scheme conversion
3. Fixed database connection test to use Flask-SQLAlchemy with app context
4. Updated Render `CLIENT_ORIGIN` for CORS
5. Removed SPA rewrites from Vercel config (hash routing doesn't need them)
6. Moved all public assets to JS module imports (Vercel `@vercel/vite` compatibility)
7. Replaced favicon with inline SVG data URI
8. Triggered successful deploys on both platforms
