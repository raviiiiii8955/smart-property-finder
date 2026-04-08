"""
NLP Parser – converts natural-language property queries into filter dicts.
Uses simple regex + keyword matching (no external NLP libraries needed).
"""
import re


# ── helpers ──────────────────────────────────────────────────────────────────

def _extract_number(text: str, pattern: str) -> float | None:
    m = re.search(pattern, text, re.IGNORECASE)
    if m:
        raw = m.group(1).replace(",", "")
        try:
            return float(raw)
        except ValueError:
            return None
    return None


def _extract_range(text: str, unit_words: str) -> tuple[float | None, float | None]:
    """Return (min, max) from phrases like 'between 2 and 4 beds'."""
    pattern = rf"between\s+([\d,]+)\s+and\s+([\d,]+)\s*{unit_words}"
    m = re.search(pattern, text, re.IGNORECASE)
    if m:
        return float(m.group(1).replace(",", "")), float(m.group(2).replace(",", ""))
    return None, None


# ── main parser ───────────────────────────────────────────────────────────────

def parse_query(query: str) -> dict:
    """
    Parse a natural-language property search query.

    Returns a dict with optional keys:
        property_type, min_price, max_price, min_beds, max_beds,
        min_baths, max_baths, min_area, max_area, city,
        amenities (list), keywords (list)
    """
    text = query.lower().strip()
    filters: dict = {}

    # ── property type ─────────────────────────────────────────────────────────
    type_map = {
        "villa": "Villa",
        "apartment": "Apartment",
        "flat": "Apartment",
        "house": "House",
        "studio": "Studio",
        "penthouse": "Penthouse",
        "condo": "Condo",
        "townhouse": "Townhouse",
        "bungalow": "Bungalow",
        "duplex": "Duplex",
    }
    for kw, val in type_map.items():
        if kw in text:
            filters["property_type"] = val
            break

    # ── price ─────────────────────────────────────────────────────────────────
    # "under 50 lakh", "below 1 crore", "less than 80 lakhs"
    max_price = _extract_number(text, r"(?:under|below|less than|upto|up to)\s+([\d,]+)\s*(?:lakh|lac|cr|crore)?")
    if max_price:
        if re.search(r"crore|cr\b", text[text.find(str(int(max_price))):text.find(str(int(max_price)))+20]):
            max_price *= 100   # crore → lakh
        filters["max_price"] = max_price

    min_price = _extract_number(text, r"(?:above|over|more than|minimum|min)\s+([\d,]+)\s*(?:lakh|lac|cr|crore)?")
    if min_price:
        if re.search(r"crore|cr\b", text[text.find(str(int(min_price))):text.find(str(int(min_price)))+20]):
            min_price *= 100
        filters["min_price"] = min_price

    # "between 30 lakh and 70 lakh"
    bmin, bmax = _extract_range(text, r"(?:lakh|lac|crore|cr)?")
    if bmin is not None:
        filters["min_price"] = bmin
    if bmax is not None:
        filters["max_price"] = bmax

    # ── bedrooms ──────────────────────────────────────────────────────────────
    bed_match = re.search(r"(\d+)\s*(?:bhk|bed(?:room)?s?)", text)
    if bed_match:
        beds = int(bed_match.group(1))
        filters["min_beds"] = beds
        filters["max_beds"] = beds

    bmin2, bmax2 = _extract_range(text, r"(?:bhk|bed(?:room)?s?)")
    if bmin2 is not None:
        filters["min_beds"] = int(bmin2)
    if bmax2 is not None:
        filters["max_beds"] = int(bmax2)

    # ── bathrooms ─────────────────────────────────────────────────────────────
    bath_match = re.search(r"(\d+)\s*bath(?:room)?s?", text)
    if bath_match:
        baths = int(bath_match.group(1))
        filters["min_baths"] = baths

    # ── area ──────────────────────────────────────────────────────────────────
    area_min = _extract_number(text, r"(?:above|more than|min(?:imum)?)\s+([\d,]+)\s*(?:sq\.?\s?ft|sqft|sq\.?\s?m)")
    area_max = _extract_number(text, r"(?:under|below|less than|up to)\s+([\d,]+)\s*(?:sq\.?\s?ft|sqft|sq\.?\s?m)")
    if area_min:
        filters["min_area"] = area_min
    if area_max:
        filters["max_area"] = area_max

    # ── city / location ───────────────────────────────────────────────────────
    cities = [
        "mumbai", "delhi", "bangalore", "bengaluru", "hyderabad",
        "chennai", "kolkata", "pune", "ahmedabad", "jaipur",
        "gurgaon", "gurugram", "noida", "chandigarh", "kochi",
        "lucknow", "surat", "indore", "bhopal", "patna",
    ]
    for city in cities:
        if city in text:
            filters["city"] = city.capitalize().replace("Bengaluru", "Bangalore").replace("Gurugram", "Gurgaon")
            break

    # ── amenities ─────────────────────────────────────────────────────────────
    amenity_kws = {
        "pool": "Swimming Pool",
        "swimming": "Swimming Pool",
        "gym": "Gym",
        "fitness": "Gym",
        "garden": "Garden",
        "park": "Park",
        "parking": "Parking",
        "lift": "Elevator",
        "elevator": "Elevator",
        "security": "Security",
        "cctv": "Security",
        "balcony": "Balcony",
        "terrace": "Terrace",
        "furnished": "Furnished",
        "semi-furnished": "Semi-Furnished",
        "unfurnished": "Unfurnished",
        "school": "Near School",
        "hospital": "Near Hospital",
        "metro": "Near Metro",
    }
    amenities = []
    for kw, label in amenity_kws.items():
        if kw in text and label not in amenities:
            amenities.append(label)
    if amenities:
        filters["amenities"] = amenities

    # ── catch-all keywords ────────────────────────────────────────────────────
    stop_words = {
        "want", "looking", "for", "a", "an", "the", "with", "in",
        "and", "or", "of", "to", "near", "around", "find", "show",
        "me", "property", "properties", "home", "homes", "flat",
        "buy", "rent", "need", "like", "have",
    }
    keywords = [w for w in re.findall(r"\b[a-z]+\b", text) if w not in stop_words and len(w) > 2]
    if keywords:
        filters["keywords"] = list(dict.fromkeys(keywords))  # dedupe, preserve order

    return filters