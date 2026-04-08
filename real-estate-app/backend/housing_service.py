"""
Housing.com API Service (via RapidAPI)
Host: housing-api.p.rapidapi.com

Endpoints used:
  POST /property/listing-by-url  → Get property list from a housing.com search URL
  POST /property/get-by-url      → Get full details for a single property
  POST /city-overview/get-by-url → City stats and overview
  POST /price-trends/get-by-url  → Price trend data for a locality
"""

import os
import requests
import time
import hashlib
import json
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY  = os.environ.get("RAPIDAPI_KEY", "")
RAPIDAPI_HOST = "housing-api.p.rapidapi.com"
BASE_URL      = f"https://{RAPIDAPI_HOST}"

HEADERS = {
    "x-rapidapi-key":  RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST,
    "Content-Type":    "application/json",
}

# ── Simple in-memory TTL cache (avoids repeat API calls) ─────────────────────
_cache: dict = {}
CACHE_TTL = 300  # 5 minutes


def _cache_get(key: str):
    entry = _cache.get(key)
    if entry and (time.time() - entry["ts"]) < CACHE_TTL:
        return entry["data"]
    return None


def _cache_set(key: str, data):
    _cache[key] = {"data": data, "ts": time.time()}


def _cache_key(endpoint: str, payload: dict) -> str:
    raw = endpoint + json.dumps(payload, sort_keys=True)
    return hashlib.md5(raw.encode()).hexdigest()


# ── Housing.com search URL builder ──────────────────────────────────────────
CITY_SLUGS = {
    "mumbai":    "mumbai",
    "delhi":     "delhi-ncr",
    "bangalore": "bengaluru",
    "bengaluru": "bengaluru",
    "hyderabad": "hyderabad",
    "chennai":   "chennai",
    "pune":      "pune",
    "kolkata":   "kolkata",
    "ahmedabad": "ahmedabad",
    "noida":     "noida",
    "gurgaon":   "gurugram",
    "gurugram":  "gurugram",
    "thane":     "thane",
    "navi mumbai": "navi-mumbai",
}

PROPERTY_TYPE_MAP = {
    "apartment": "residential-apartment",
    "villa":     "villa",
    "plot":      "residential-land",
    "commercial":"commercial",
    "":          "",
}


def build_search_url(city: str = "mumbai", prop_type: str = "",
                     transaction: str = "buy", locality: str = "") -> str:
    """
    Constructs a housing.com search URL.
    e.g. https://housing.com/in/buy/apartments/mumbai-city
    """
    slug = CITY_SLUGS.get(city.lower().strip(), city.lower().strip().replace(" ", "-"))
    tx   = "buy" if transaction in ("buy", "sale", "") else "rent"

    type_slug = PROPERTY_TYPE_MAP.get(prop_type.lower(), "")
    if type_slug:
        path = f"https://housing.com/in/{tx}/{type_slug}s/{slug}-city"
    else:
        path = f"https://housing.com/in/{tx}/projects/{slug}-city"

    return path


# ── Core API caller ──────────────────────────────────────────────────────────
def _post(endpoint: str, payload: dict) -> dict:
    key = _cache_key(endpoint, payload)
    cached = _cache_get(key)
    if cached is not None:
        return cached

    if not RAPIDAPI_KEY or RAPIDAPI_KEY == "your_rapidapi_key_here":
        return {"error": "RAPIDAPI_KEY not configured in .env"}

    try:
        resp = requests.post(
            f"{BASE_URL}{endpoint}",
            headers=HEADERS,
            json=payload,
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        _cache_set(key, data)
        return data
    except requests.exceptions.Timeout:
        return {"error": "Housing API request timed out"}
    except requests.exceptions.HTTPError as e:
        return {"error": f"Housing API error: {e.response.status_code} — {e.response.text[:200]}"}
    except Exception as e:
        return {"error": str(e)}


# ── Public service functions ────────────────────────────────────────────────
def get_property_listing(city: str = "mumbai", prop_type: str = "",
                          transaction: str = "buy", page: int = 1) -> dict:
    """Fetch a list of properties for a city from housing.com."""
    url = build_search_url(city, prop_type, transaction)
    raw = _post("/property/listing-by-url", {"url": url})
    if "error" in raw:
        return raw
    return normalize_listing(raw, city)


def get_property_detail(housing_url: str) -> dict:
    """Fetch full details for a single property by its housing.com URL."""
    raw = _post("/property/get-by-url", {"url": housing_url})
    if "error" in raw:
        return raw
    return normalize_detail(raw)


def get_city_overview(city: str = "mumbai") -> dict:
    """Fetch city-level real estate overview from housing.com."""
    slug = CITY_SLUGS.get(city.lower().strip(), city.lower().strip().replace(" ", "-"))
    url  = f"https://housing.com/in/buy/projects/{slug}-city"
    return _post("/city-overview/get-by-url", {"url": url})


def get_price_trends(city: str = "mumbai", locality: str = "") -> dict:
    """Fetch price trend data for a city/locality."""
    slug = CITY_SLUGS.get(city.lower().strip(), city.lower().strip().replace(" ", "-"))
    if locality:
        loc_slug = locality.lower().strip().replace(" ", "-")
        url = f"https://housing.com/in/buy/projects/{loc_slug}-{slug}"
    else:
        url = f"https://housing.com/in/buy/projects/{slug}-city"
    return _post("/price-trends/get-by-url", {"url": url})


# ── Response normalizers ─────────────────────────────────────────────────────
def normalize_listing(raw, city: str) -> dict:
    """
    Map the Housing API listing response to our internal property format.
    The API returns: {statusCode, messageCode, data: [list of items]}
    """
    properties = []

    # Handle both list and dict top-level responses
    if isinstance(raw, list):
        listings = raw
    elif isinstance(raw, dict):
        data = raw.get("data", [])
        if isinstance(data, list):
            listings = data
        elif isinstance(data, dict):
            listings = (data.get("listings") or data.get("projects") or
                        data.get("results") or [])
        else:
            listings = []
    else:
        listings = []

    for item in listings:
        prop = _map_item(item, city)
        if prop:
            properties.append(prop)

    return {
        "properties": properties,
        "total":      len(properties),
        "source":     "housing.com",
        "city":       city,
    }


def normalize_detail(raw) -> dict:
    """Map a single property detail response to our internal format."""
    if isinstance(raw, dict):
        data = raw.get("data") or raw
    else:
        data = raw
    if isinstance(data, list) and data:
        data = data[0]
    return _map_item(data, "")


def _map_item(item: dict, default_city: str) -> dict | None:
    """Convert one Housing.com listing item to our PropFinder schema.

    Real API fields (from live inspection):
      id, name, url, image_url, min_price, max_price, price_display_value,
      coords: [lat, lng],
      address: {address, long_address},
      details.config.property_config: [{label:"2 BHK Apartment", data:[{price:{value}, area_config:[{area_info:{value,unit}}]}]}]
      features: [{id, label, description}],
      seller: [{name, phone:{partial_value}}]
    """
    if not item or not isinstance(item, dict):
        return None

    # ── Price ────────────────────────────────────────────────────────────────
    price = 0
    min_p = item.get("min_price")
    max_p = item.get("max_price")
    if min_p is not None:
        try: price = int(float(str(min_p).replace(",", "")))
        except Exception: pass
    elif max_p is not None:
        try: price = int(float(str(max_p).replace(",", "")))
        except Exception: pass

    # Also try getting price from details.config
    if price == 0:
        try:
            configs = item.get("details", {}).get("config", {}).get("property_config", [])
            for cfg in configs:
                for d in cfg.get("data", []):
                    v = d.get("price", {}).get("value")
                    if v:
                        price = int(float(v))
                        break
                if price: break
        except Exception:
            pass

    # ── Area (sqft) ──────────────────────────────────────────────────────────
    area = 0
    try:
        configs = item.get("details", {}).get("config", {}).get("property_config", [])
        for cfg in configs:
            for d in cfg.get("data", []):
                for ac in d.get("area_config", []):
                    v = ac.get("area_info", {}).get("value")
                    if v:
                        area = int(float(v))
                        break
                if area: break
            if area: break
    except Exception:
        pass

    # ── BHK from label e.g. "2 BHK Apartment" ───────────────────────────────
    bhk = 0
    ptype = "Apartment"
    try:
        configs = item.get("details", {}).get("config", {}).get("property_config", [])
        if configs:
            label = configs[0].get("label", "")
            import re
            m = re.search(r"(\d+)\s*BHK", label, re.I)
            if m:
                bhk = int(m.group(1))
            type_name = configs[0].get("property_type_name", "")
            if type_name:
                ptype = "Villa"      if "villa"      in type_name.lower() else \
                        "Plot"       if "land"       in type_name.lower() or "plot" in type_name.lower() else \
                        "Commercial" if "commercial" in type_name.lower() else "Apartment"
    except Exception:
        pass

    # ── Image ────────────────────────────────────────────────────────────────
    images = []
    img = item.get("image_url")
    if img:
        images = [img]
    else:
        raw_imgs = item.get("images") or item.get("photos") or []
        if isinstance(raw_imgs, str):
            images = [raw_imgs]
        elif isinstance(raw_imgs, list):
            images = [i if isinstance(i, str) else (i.get("url") or i.get("src") or "") for i in raw_imgs]
        images = [i for i in images if i]

    # ── Location ─────────────────────────────────────────────────────────────
    addr_obj  = item.get("address") or {}
    locality  = addr_obj.get("address") or addr_obj.get("long_address") or ""
    city_name = default_city.title() if default_city else "India"
    location  = locality if locality else city_name

    # ── Amenities from features list ─────────────────────────────────────────
    amenities = []
    for f in (item.get("features") or []):
        if isinstance(f, dict):
            desc = f.get("description") or f.get("label") or ""
            if desc:
                amenities.append(desc)
        elif isinstance(f, str):
            amenities.append(f)

    # ── Seller contact ───────────────────────────────────────────────────────
    contact = ""
    sellers = item.get("seller") or []
    if sellers and isinstance(sellers, list):
        phone = sellers[0].get("phone") or {}
        contact = phone.get("partial_value") or sellers[0].get("name") or ""

    # ── Coordinates ──────────────────────────────────────────────────────────
    coords = item.get("coords") or []
    lat, lng = 0.0, 0.0
    try:
        if len(coords) >= 2:
            lat = float(coords[0])
            lng = float(coords[1])
    except Exception:
        pass

    # ── Source URL ───────────────────────────────────────────────────────────
    rel_url = item.get("url") or ""
    source_url = f"https://housing.com{rel_url}" if rel_url and not rel_url.startswith("http") else rel_url

    # ── Title ────────────────────────────────────────────────────────────────
    title = item.get("name") or item.get("title") or ""
    if not title:
        bhk_str = f"{bhk} BHK " if bhk else ""
        title = f"{bhk_str}{ptype} in {location}"

    prop_id = str(item.get("id") or abs(hash(title + str(price))))

    return {
        "id":            f"live_{prop_id}",
        "title":         title,
        "price":         price,
        "location":      location,
        "city":          city_name,
        "bhk":           bhk,
        "type":          ptype,
        "furnishing":    "Unfurnished",
        "area_sqft":     area,
        "description":   item.get("description") or item.get("subtitle") or "",
        "amenities":     amenities[:10],
        "images":        images[:5],
        "lat":           lat,
        "lng":           lng,
        "owner_contact": contact,
        "is_favorited":  False,
        "source":        "housing.com",
        "source_url":    source_url,
        "price_label":   item.get("price_display_value") or "",
    }
