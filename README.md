# 🏠 PropFinder — Smart Real Estate Platform

A full-stack real estate web application inspired by 99acres/housing.com, built with **React + Flask**, featuring live property listings via the Housing API.

![PropFinder Screenshot](./screenshot.png)

---

## ✨ Features

- 🔍 **Property Search** — Filter by city, BHK, type, price range, furnishing
- ⚡ **Live Listings** — Real-time property data from housing.com via RapidAPI
- 🗺️ **Map View** — Interactive property map
- ❤️ **Wishlist** — Save favorite properties (login required)
- 🔐 **Authentication** — JWT-based signup/login
- 👑 **Admin Panel** — Full CRUD for property management
- 📱 **Responsive** — Works on all screen sizes

---

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, TailwindCSS |
| Backend | Python Flask, Flask-JWT-Extended |
| Database | SQLite (local dev) |
| Live Data | Housing API via RapidAPI |
| Auth | JWT tokens + bcrypt |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- A [RapidAPI](https://rapidapi.com) account with the [Housing API](https://rapidapi.com/clevo/api/housing-api) subscribed

---

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/smart-property-finder.git
cd smart-property-finder
```

### 2. Backend Setup

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install dependencies
cd real-estate-app/backend
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your RAPIDAPI_KEY

# Start the backend
python app.py
# → Running at http://localhost:5001
```

### 3. Frontend Setup

```bash
cd real-estate-app/frontend
npm install
npm run dev
# → Running at http://localhost:3000
```

---

## 🔑 Environment Variables

Create `real-estate-app/backend/.env` based on `.env.example`:

```env
RAPIDAPI_KEY=your_rapidapi_key_here
RAPIDAPI_HOST=housing-api.p.rapidapi.com
```

Get your key from [rapidapi.com](https://rapidapi.com/developer/apps).

---

## 🗂️ Project Structure

```
smart-property-finder/
├── real-estate-app/
│   ├── backend/
│   │   ├── app.py              # Flask entry point
│   │   ├── database.py         # SQLite setup + seed data
│   │   ├── housing_service.py  # Housing API integration
│   │   ├── routes/
│   │   │   ├── auth.py         # Login/signup routes
│   │   │   ├── properties.py   # Local property CRUD
│   │   │   ├── favorites.py    # Wishlist routes
│   │   │   └── live.py         # Live API routes (/api/live/*)
│   │   ├── requirements.txt
│   │   └── .env.example        # Environment template
│   └── frontend/
│       ├── src/
│       │   ├── pages/          # React pages
│       │   ├── components/     # Reusable UI components
│       │   ├── context/        # Auth & Wishlist providers
│       │   └── api/            # Axios config
│       ├── package.json
│       └── vite.config.js
└── README.md
```

---

## 🔐 Default Admin Credentials

After first backend start, a seed admin is created:

| Field | Value |
|---|---|
| Email | admin@propfinder.com |
| Password | admin123 |

> ⚠️ Change these in production!

---

## 📡 Live API Endpoints

| Method | Route | Description |
|---|---|---|
| GET | `/api/live/properties?city=mumbai` | Live property listings |
| GET | `/api/live/property?url=<url>` | Single property detail |
| GET | `/api/live/city-overview?city=mumbai` | City market overview |
| GET | `/api/live/price-trends?city=mumbai` | Price trend data |
| GET | `/api/live/cities` | Supported cities list |

---

## 📄 License

MIT License — feel free to use, modify, and share.
