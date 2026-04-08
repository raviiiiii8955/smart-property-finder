"""
Property data + ML-based scoring model.
Real-life grade: actual Indian builders, locality-aware pricing, agent info, RERA, descriptions.
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# ── Constants ─────────────────────────────────────────────────────────────────

CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai",
    "Pune", "Kolkata", "Ahmedabad", "Jaipur", "Gurgaon",
    "Noida", "Kochi", "Chandigarh", "Lucknow", "Surat",
]

CITY_LOCALITIES = {
    "Mumbai":    ["Bandra West", "Andheri East", "Powai", "Worli", "Juhu", "Malad West", "Lower Parel"],
    "Delhi":     ["Dwarka", "Vasant Kunj", "Saket", "Rohini", "Janakpuri", "Lajpat Nagar", "Hauz Khas"],
    "Bangalore": ["Whitefield", "Koramangala", "Indiranagar", "HSR Layout", "Electronic City", "Sarjapur Road", "Hebbal"],
    "Hyderabad": ["Gachibowli", "Hitech City", "Banjara Hills", "Jubilee Hills", "Madhapur", "Kondapur", "Manikonda"],
    "Chennai":   ["Anna Nagar", "OMR", "Velachery", "Adyar", "Nungambakkam", "Sholinganallur", "Porur"],
    "Pune":      ["Kharadi", "Wakad", "Hinjewadi", "Baner", "Aundh", "Viman Nagar", "Hadapsar"],
    "Kolkata":   ["Salt Lake", "New Town", "Ballygunge", "Rajarhat", "Behala", "Park Street", "Alipore"],
    "Ahmedabad": ["Prahlad Nagar", "Satellite", "Bodakdev", "Vastrapur", "Thaltej", "Bopal", "SG Highway"],
    "Jaipur":    ["Vaishali Nagar", "Malviya Nagar", "C-Scheme", "Mansarovar", "Jagatpura", "Tonk Road", "Ajmer Road"],
    "Gurgaon":   ["DLF Phase 1", "Sohna Road", "Golf Course Road", "Sector 57", "Sector 82", "Palam Vihar", "MG Road"],
    "Noida":     ["Sector 137", "Sector 150", "Sector 62", "Expressway", "Greater Noida West", "Sector 78", "Sector 44"],
    "Kochi":     ["Marine Drive", "Kakkanad", "Edappally", "Vytilla", "Kalamassery", "Thrippunithura", "Aluva"],
    "Chandigarh":["Sector 17", "Sector 22", "Sector 35", "Sector 43", "Sector 8", "Manimajra", "Zirakpur"],
    "Lucknow":   ["Gomti Nagar", "Hazratganj", "Alambagh", "Indira Nagar", "Aliganj", "Sushant Golf City", "LDA Colony"],
    "Surat":     ["Vesu", "Althan", "Adajan", "Pal", "Dumas Road", "Bhatar", "Ghod Dod Road"],
}

BUILDERS = [
    "DLF Limited", "Godrej Properties", "Prestige Group", "Sobha Developers",
    "Lodha Group", "Brigade Group", "Mahindra Lifespaces", "Oberoi Realty",
    "Tata Housing", "Shapoorji Pallonji", "Embassy Group", "Puravankara",
    "Hiranandani Group", "Raheja Developers", "Omaxe Group",
]

PROPERTY_TYPES = [
    "Apartment", "Villa", "House", "Studio",
    "Penthouse", "Condo", "Townhouse", "Bungalow", "Duplex",
]

AMENITIES_POOL = [
    "Swimming Pool", "Clubhouse", "Gym", "Jogging Track", "Children's Play Area",
    "Parking", "Elevator", "24/7 Security", "CCTV Surveillance", "Intercom",
    "Balcony", "Terrace", "Garden", "Landscaped Gardens", "Indoor Games Room",
    "Squash Court", "Badminton Court", "Basketball Court", "Tennis Court",
    "Air Conditioning", "Modular Kitchen", "Video Door Phone",
    "Power Backup", "Rainwater Harvesting", "Solar Panels", "EV Charging",
    "Co-working Space", "Party Hall", "Theatre Room", "Spa & Sauna",
    "Near Metro", "Near School", "Near Hospital", "Near Mall",
    "Furnished", "Semi-Furnished", "Vastu Compliant",
]

TAGS = ["Hot Deal", "New Launch", "Price Drop", "Ready to Move",
        "Top Rated", "Verified", "RERA Registered", "Investment Pick"]

STATUS_OPTIONS = ["Ready to Move", "Under Construction", "New Launch", "Resale"]

AGENT_NAMES = [
    "Rajesh Kumar", "Priya Sharma", "Amit Verma", "Sunita Reddy", "Arjun Mehta",
    "Kavitha Nair", "Suresh Iyer", "Deepa Pillai", "Rohit Gupta", "Ananya Singh",
    "Vikram Patel", "Meera Joshi", "Sanjay Bansal", "Pooja Krishnan", "Nikhil Das",
]

DESCRIPTION_TEMPLATES = [
    "A luxurious {beds} BHK {ptype} located in the heart of {locality}, {city}. "
    "Built by the renowned {builder}, this property offers world-class amenities and stunning views. "
    "Spacious {area} sq.ft carpet area with premium fittings throughout.",

    "Welcome to your dream home — a beautifully crafted {beds} BHK {ptype} in {locality}, {city}. "
    "Developed by {builder}, this project combines modern architecture with serene living. "
    "RERA approved project with possession in {year}.",

    "Strategically located {beds} BHK {ptype} in {locality}, {city} by {builder}. "
    "An ideal blend of comfort and luxury offering {area} sq.ft of well-designed living space. "
    "Easy connectivity to IT corridors, schools and hospitals.",

    "Elegant {beds} BHK {ptype} in the premium enclave of {locality}, {city}. "
    "Crafted with attention to detail by {builder}, featuring high-end fittings, modular kitchen "
    "and exclusive amenities. Perfect for families seeking quality living.",

    "Investment opportunity: {beds} BHK {ptype} in {locality}, {city} — one of the fastest appreciating "
    "micro-markets. Developed by {builder}. Price per sq.ft significantly below market average.",
]

# High-quality Unsplash property images
IMAGES = [
    "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&q=90",
    "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&q=90",
    "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=800&q=90",
    "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&q=90",
    "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&q=90",
    "https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=800&q=90",
    "https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800&q=90",
    "https://images.unsplash.com/photo-1605276374104-dee2a0ed3cd6?w=800&q=90",
    "https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?w=800&q=90",
    "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=90",
    "https://images.unsplash.com/photo-1523217582562-09d0def993a6?w=800&q=90",
    "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800&q=90",
    "https://images.unsplash.com/photo-1599427303058-f04cbcf4756f?w=800&q=90",
    "https://images.unsplash.com/photo-1583608205776-bfd35f0d9f83?w=800&q=90",
    "https://images.unsplash.com/photo-1592595896551-12b371d546d5?w=800&q=90",
    "https://images.unsplash.com/photo-1487958449943-2429e8be8625?w=800&q=90",
    "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800&q=90",
    "https://images.unsplash.com/photo-1494526585095-c41746248156?w=800&q=90",
    "https://images.unsplash.com/photo-1416331108676-a22ccb276e35?w=800&q=90",
    "https://images.unsplash.com/photo-1598228723793-52759bba239c?w=800&q=90",
]

# City-tier price multipliers (₹ Lakhs per BHK base)
CITY_PRICE = {
    "Mumbai":    (85, 220),   # Very high
    "Delhi":     (60, 160),
    "Gurgaon":   (65, 180),
    "Noida":     (40, 110),
    "Bangalore": (55, 150),
    "Hyderabad": (45, 120),
    "Chennai":   (45, 115),
    "Pune":      (40, 100),
    "Kolkata":   (35, 80),
    "Ahmedabad": (30, 75),
    "Kochi":     (40, 95),
    "Jaipur":    (30, 70),
    "Chandigarh":(40, 90),
    "Lucknow":   (25, 60),
    "Surat":     (28, 65),
}


def _gen_properties(n: int = 200) -> pd.DataFrame:
    rng = np.random.default_rng(42)

    prop_types  = rng.choice(PROPERTY_TYPES, n)
    cities      = rng.choice(CITIES, n)
    builders    = rng.choice(BUILDERS, n)
    beds        = rng.integers(1, 6, n)
    baths       = np.clip(beds - rng.integers(0, 2, n), 1, 5)
    area        = (beds * rng.uniform(350, 700, n)).astype(int)
    year_built  = rng.integers(2015, 2027, n)
    floor       = rng.integers(0, 40, n)
    rating      = (rng.uniform(3.5, 5.0, n)).round(1)

    # Realistic price based on city range
    prices = []
    for i in range(n):
        low, high = CITY_PRICE[cities[i]]
        base = rng.uniform(low, high)
        bed_mult = 1 + (beds[i] - 1) * 0.55
        prices.append(round(base * bed_mult, 2))
    prices = np.array(prices)

    # Localities
    localities = [rng.choice(CITY_LOCALITIES[c]) for c in cities]

    # Amenities (6–14 per property, realistic)
    amenities = [
        sorted(set(rng.choice(AMENITIES_POOL, rng.integers(6, 15), replace=False).tolist()))
        for _ in range(n)
    ]

    # Images
    images = [IMAGES[i % len(IMAGES)] for i in range(n)]

    # Status & Tags
    statuses = rng.choice(STATUS_OPTIONS, n, p=[0.45, 0.30, 0.15, 0.10])
    tag_list = []
    for i in range(n):
        chosen = []
        if statuses[i] == "Ready to Move":
            chosen.append("Ready to Move")
        if statuses[i] == "New Launch":
            chosen.append("New Launch")
        if prices[i] < CITY_PRICE[cities[i]][0] * 1.2 * (1 + (beds[i]-1)*0.55):
            chosen.append("Hot Deal")
        if rating[i] >= 4.5:
            chosen.append("Top Rated")
        if rng.random() > 0.7:
            chosen.append("RERA Registered")
        tag_list.append(chosen[:3])

    # RERA numbers
    rera = [
        f"RERA-{cities[i][:3].upper()}-{2020+rng.integers(0,5)}-{rng.integers(10000,99999)}"
        if "RERA Registered" in tag_list[i] else "Not Registered"
        for i in range(n)
    ]

    # Agent info
    agents = [rng.choice(AGENT_NAMES) for _ in range(n)]
    agent_phones = [f"+91 {rng.integers(70000,99999):05d} {rng.integers(10000,99999):05d}" for _ in range(n)]

    # Descriptions
    descriptions = [
        rng.choice(DESCRIPTION_TEMPLATES).format(
            beds=beds[i], ptype=prop_types[i], locality=localities[i],
            city=cities[i], builder=builders[i], area=area[i], year=year_built[i]
        )
        for i in range(n)
    ]

    # Title — builder-brand style
    project_suffixes = ["Heights", "Gardens", "Residency", "Towers", "Avenue",
                        "Enclave", "Grande", "Skyline", "Park", "Greens", "Vistas"]
    titles = [
        f"{builders[i].split()[0]} {rng.choice(project_suffixes)} — {beds[i]} BHK {prop_types[i]}"
        for i in range(n)
    ]

    # Price per sqft
    price_psf = (prices * 100000 / area).round(0).astype(int)

    df = pd.DataFrame({
        "id":           range(1, n + 1),
        "title":        titles,
        "property_type":prop_types,
        "city":         cities,
        "locality":     localities,
        "builder":      builders,
        "beds":         beds,
        "baths":        baths,
        "area_sqft":    area,
        "price_lakh":   prices,
        "price_psf":    price_psf,
        "amenities":    amenities,
        "image_url":    images,
        "rating":       rating,
        "year_built":   year_built,
        "floor":        floor,
        "status":       statuses,
        "tags":         tag_list,
        "rera":         rera,
        "agent":        agents,
        "agent_phone":  agent_phones,
        "description":  descriptions,
    })
    return df


_PROPERTIES: pd.DataFrame | None = None


def get_properties() -> pd.DataFrame:
    global _PROPERTIES
    if _PROPERTIES is None:
        _PROPERTIES = _gen_properties()
    return _PROPERTIES.copy()


# ── ML scoring ────────────────────────────────────────────────────────────────

class PropertyScorer:
    """Feature-weighted cosine similarity scorer."""

    FEATURE_COLS = ["beds", "baths", "area_sqft", "price_lakh", "rating", "year_built"]
    WEIGHTS      = np.array([0.15, 0.08, 0.15, 0.28, 0.22, 0.12])

    def __init__(self):
        self.scaler = MinMaxScaler()
        df = get_properties()
        self.scaler.fit(df[self.FEATURE_COLS].values.astype(float))

    def score(self, df: pd.DataFrame, filters: dict) -> pd.Series:
        if df.empty:
            return pd.Series(dtype=float)

        all_props = get_properties()
        scaled = self.scaler.transform(df[self.FEATURE_COLS].values.astype(float))

        ideal = np.array([
            all_props["beds"].median(),
            all_props["baths"].median(),
            all_props["area_sqft"].median(),
            all_props["price_lakh"].median(),
            5.0,
            2025.0,
        ], dtype=float)

        if "min_beds" in filters:
            ideal[0] = (filters.get("min_beds", 2) + filters.get("max_beds", filters["min_beds"])) / 2
        if "max_price" in filters:
            ideal[3] = (filters.get("min_price", 0) + filters["max_price"]) / 2
        if "min_area" in filters:
            ideal[2] = (filters.get("min_area", 0) + filters.get("max_area", filters["min_area"] * 1.5)) / 2

        ideal_scaled = self.scaler.transform([ideal])[0]
        distances = np.sqrt(((scaled - ideal_scaled) ** 2 * self.WEIGHTS).sum(axis=1))
        scores = 1 - distances / (distances.max() + 1e-9)

        req_amenities = set(filters.get("amenities", []))
        if req_amenities:
            amenity_scores = df["amenities"].apply(
                lambda a: len(req_amenities & set(a)) / len(req_amenities)
            ).values
            scores = scores * 0.70 + amenity_scores * 0.30

        return pd.Series((scores * 10).round(1), index=df.index)


_SCORER: PropertyScorer | None = None


def get_scorer() -> PropertyScorer:
    global _SCORER
    if _SCORER is None:
        _SCORER = PropertyScorer()
    return _SCORER


# ── filtering ─────────────────────────────────────────────────────────────────

def filter_properties(filters: dict) -> pd.DataFrame:
    df = get_properties()

    if "property_type" in filters:
        df = df[df["property_type"].str.lower() == filters["property_type"].lower()]
    if "city" in filters:
        df = df[df["city"].str.lower() == filters["city"].lower()]
    if "min_beds" in filters:
        df = df[df["beds"] >= filters["min_beds"]]
    if "max_beds" in filters:
        df = df[df["beds"] <= filters["max_beds"]]
    if "min_baths" in filters:
        df = df[df["baths"] >= filters["min_baths"]]
    if "min_price" in filters:
        df = df[df["price_lakh"] >= filters["min_price"]]
    if "max_price" in filters:
        df = df[df["price_lakh"] <= filters["max_price"]]
    if "min_area" in filters:
        df = df[df["area_sqft"] >= filters["min_area"]]
    if "max_area" in filters:
        df = df[df["area_sqft"] <= filters["max_area"]]
    if "amenities" in filters:
        req = set(filters["amenities"])
        df = df[df["amenities"].apply(lambda a: bool(req & set(a)))]

    return df.reset_index(drop=True)