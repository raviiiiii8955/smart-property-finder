"""SQLite database setup and seed data"""
import sqlite3, json, os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'propfinder.db')

SEED_PROPERTIES = [
    {
        "title": "Luxurious 3 BHK Sea View Apartment",
        "price": 8500000,
        "location": "Bandra West, Mumbai",
        "city": "Mumbai",
        "bhk": 3,
        "type": "Apartment",
        "furnishing": "Furnished",
        "area_sqft": 1450,
        "description": "Stunning sea-view apartment in the heart of Bandra West. Includes modular kitchen, premium flooring, and 24/7 security. Walking distance to Linking Road and Bandstand.",
        "amenities": ["Swimming Pool", "Gym", "24/7 Security", "Covered Parking", "Club House", "Children's Play Area"],
        "images": [
            "https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?w=800",
            "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800",
            "https://images.unsplash.com/photo-1560185007-cde436f6a4d0?w=800"
        ],
        "lat": 19.0596, "lng": 72.8295,
        "owner_contact": "+91 98765 43210"
    },
    {
        "title": "Spacious 2 BHK in Prime Location",
        "price": 4200000,
        "location": "Andheri East, Mumbai",
        "city": "Mumbai",
        "bhk": 2,
        "type": "Apartment",
        "furnishing": "Semi-Furnished",
        "area_sqft": 980,
        "description": "Well-ventilated 2 BHK apartment near Metro Station. Close to business hubs and shopping malls. Society with 24/7 water supply.",
        "amenities": ["Gym", "24/7 Security", "Power Backup", "Covered Parking"],
        "images": [
            "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800",
            "https://images.unsplash.com/photo-1484154218962-a197022b5858?w=800"
        ],
        "lat": 19.1136, "lng": 72.8697,
        "owner_contact": "+91 98765 11111"
    },
    {
        "title": "Premium Villa with Private Pool",
        "price": 35000000,
        "location": "Juhu, Mumbai",
        "city": "Mumbai",
        "bhk": 5,
        "type": "Villa",
        "furnishing": "Furnished",
        "area_sqft": 4800,
        "description": "Exquisite standalone villa in Juhu with private swimming pool and landscaped garden. Just 2 minutes from Juhu Beach. Fully furnished with imported furniture.",
        "amenities": ["Private Pool", "Garden", "Home Theatre", "Servant Quarters", "5-Car Parking", "Solar Panels"],
        "images": [
            "https://images.unsplash.com/photo-1582268611958-ebfd161ef9cf?w=800",
            "https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800",
            "https://images.unsplash.com/photo-1592595896551-12b371d546d5?w=800"
        ],
        "lat": 19.1000, "lng": 72.8260,
        "owner_contact": "+91 98765 55555"
    },
    {
        "title": "Modern 1 BHK Studio Apartment",
        "price": 1800000,
        "location": "Worli, Mumbai",
        "city": "Mumbai",
        "bhk": 1,
        "type": "Apartment",
        "furnishing": "Furnished",
        "area_sqft": 560,
        "description": "Compact and stylish studio apartment in Worli. Perfect for young professionals. Great connectivity to BKC and Lower Parel.",
        "amenities": ["Security", "Elevator", "Power Backup"],
        "images": [
            "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800",
            "https://images.unsplash.com/photo-1536376072261-38c75010e6c9?w=800"
        ],
        "lat": 19.0177, "lng": 72.8155,
        "owner_contact": "+91 91234 56789"
    },
    {
        "title": "Elegant 4 BHK Penthouse",
        "price": 22000000,
        "location": "DLF Phase 5, Gurgaon",
        "city": "Gurgaon",
        "bhk": 4,
        "type": "Apartment",
        "furnishing": "Furnished",
        "area_sqft": 3200,
        "description": "Breathtaking penthouse with panoramic city views in DLF's most prestigious address. Private terrace, premium finishes, and direct access to club facilities.",
        "amenities": ["Private Terrace", "Swimming Pool", "Concierge", "Gym", "Jacuzzi", "Smart Home System"],
        "images": [
            "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800",
            "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800",
            "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800"
        ],
        "lat": 28.4421, "lng": 77.0949,
        "owner_contact": "+91 99887 66554"
    },
    {
        "title": "Affordable 2 BHK Builder Floor",
        "price": 3500000,
        "location": "Dwarka Sector 12, Delhi",
        "city": "Delhi",
        "bhk": 2,
        "type": "Apartment",
        "furnishing": "Unfurnished",
        "area_sqft": 900,
        "description": "Spacious builder floor in a prime residential locality. Easy access to metro and schools. Ready to move.",
        "amenities": ["Parking", "Security", "Lift"],
        "images": [
            "https://images.unsplash.com/photo-1555636222-cae831e670b3?w=800",
            "https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=800"
        ],
        "lat": 28.5906, "lng": 77.0516,
        "owner_contact": "+91 98112 34567"
    },
    {
        "title": "Luxe 3 BHK in Silicon Valley of India",
        "price": 9800000,
        "location": "Koramangala, Bangalore",
        "city": "Bangalore",
        "bhk": 3,
        "type": "Apartment",
        "furnishing": "Semi-Furnished",
        "area_sqft": 1620,
        "description": "Premium apartment in Koramangala with excellent connectivity to tech parks. Large balconies and open kitchen. Well-maintained society.",
        "amenities": ["Swimming Pool", "Gym", "Clubhouse", "CCTV", "Visitor Parking", "Rainwater Harvesting"],
        "images": [
            "https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?w=800",
            "https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?w=800"
        ],
        "lat": 12.9352, "lng": 77.6245,
        "owner_contact": "+91 96321 00000"
    },
    {
        "title": "Serene 2 BHK Near Whitefield IT Hub",
        "price": 5600000,
        "location": "Whitefield, Bangalore",
        "city": "Bangalore",
        "bhk": 2,
        "type": "Apartment",
        "furnishing": "Furnished",
        "area_sqft": 1100,
        "description": "Fully furnished apartment perfect for IT professionals. Walking distance to ITPL and major tech parks. Society has excellent amenities.",
        "amenities": ["Gym", "Swimming Pool", "Power Backup", "24/7 Security", "Clubhouse"],
        "images": [
            "https://images.unsplash.com/photo-1560448204-603b3fc33ddc?w=800",
            "https://images.unsplash.com/photo-1484154218962-a197022b5858?w=800"
        ],
        "lat": 12.9698, "lng": 77.7500,
        "owner_contact": "+91 97456 78901"
    },
    {
        "title": "Budget 1 BHK for Bachelors",
        "price": 1200000,
        "location": "Indiranagar, Bangalore",
        "city": "Bangalore",
        "bhk": 1,
        "type": "Apartment",
        "furnishing": "Semi-Furnished",
        "area_sqft": 480,
        "description": "Affordable 1 BHK apartment in the trendy Indiranagar neighbourhood. Close to 100-feet road, restaurants, and metro station.",
        "amenities": ["Security", "Power Backup", "Parking"],
        "images": [
            "https://images.unsplash.com/photo-1536376072261-38c75010e6c9?w=800"
        ],
        "lat": 12.9784, "lng": 77.6408,
        "owner_contact": "+91 80123 45678"
    },
    {
        "title": "Grand 5 BHK Villa with Garden",
        "price": 28000000,
        "location": "Banjara Hills, Hyderabad",
        "city": "Hyderabad",
        "bhk": 5,
        "type": "Villa",
        "furnishing": "Furnished",
        "area_sqft": 5200,
        "description": "Majestic villa in Banjara Hills — Hyderabad's most prestigious address. Features a landscaped garden, home theatre, and staff quarters.",
        "amenities": ["Private Garden", "Home Theatre", "Solar Power", "Generator", "Swimming Pool", "Staff Quarters"],
        "images": [
            "https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800",
            "https://images.unsplash.com/photo-1523217582562-09d0def993a6?w=800",
            "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=800"
        ],
        "lat": 17.4126, "lng": 78.4481,
        "owner_contact": "+91 40123 45678"
    },
    {
        "title": "Modern 3 BHK Near HITEC City",
        "price": 7200000,
        "location": "Hitech City, Hyderabad",
        "city": "Hyderabad",
        "bhk": 3,
        "type": "Apartment",
        "furnishing": "Semi-Furnished",
        "area_sqft": 1380,
        "description": "Well-designed 3 BHK apartment in one of Hyderabad's most happening tech corridors. Close to Cyber Towers and major MNCs.",
        "amenities": ["Gym", "Swimming Pool", "Clubhouse", "Security", "Power Backup"],
        "images": [
            "https://images.unsplash.com/photo-1560185007-cde436f6a4d0?w=800",
            "https://images.unsplash.com/photo-1600566752355-35792bedcfea?w=800"
        ],
        "lat": 17.4435, "lng": 78.3772,
        "owner_contact": "+91 40987 65432"
    },
    {
        "title": "Charming 2 BHK Apartment",
        "price": 4800000,
        "location": "Anna Nagar, Chennai",
        "city": "Chennai",
        "bhk": 2,
        "type": "Apartment",
        "furnishing": "Unfurnished",
        "area_sqft": 1050,
        "description": "Well-ventilated apartment in Anna Nagar with easy access to schools, hospitals, and shopping. North-facing with good natural light.",
        "amenities": ["Security", "Parking", "Lift", "Power Backup"],
        "images": [
            "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800"
        ],
        "lat": 13.0843, "lng": 80.2101,
        "owner_contact": "+91 44123 78900"
    },
    {
        "title": "Cozy 1 BHK Near T Nagar",
        "price": 2200000,
        "location": "T Nagar, Chennai",
        "city": "Chennai",
        "bhk": 1,
        "type": "Apartment",
        "furnishing": "Semi-Furnished",
        "area_sqft": 620,
        "description": "Compact 1 BHK in T Nagar, one of Chennai's most coveted commercial and residential zones. Walk to Pondy Bazaar.",
        "amenities": ["Security", "Lift"],
        "images": [
            "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800"
        ],
        "lat": 13.0418, "lng": 80.2341,
        "owner_contact": "+91 44345 67890"
    },
    {
        "title": "Upscale 3 BHK in Koregaon Park",
        "price": 11500000,
        "location": "Koregaon Park, Pune",
        "city": "Pune",
        "bhk": 3,
        "type": "Apartment",
        "furnishing": "Furnished",
        "area_sqft": 1800,
        "description": "Luxury apartment in Pune's most sought-after neighbourhood. Surrounded by premium restaurants, the German Bakery, and Osho Ashram.",
        "amenities": ["Swimming Pool", "Gym", "Club House", "Security", "Covered Parking", "Garden"],
        "images": [
            "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800",
            "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800"
        ],
        "lat": 18.5362, "lng": 73.8969,
        "owner_contact": "+91 20987 65432"
    },
    {
        "title": "Budget 2 BHK near Hinjawadi IT Park",
        "price": 3800000,
        "location": "Hinjawadi, Pune",
        "city": "Pune",
        "bhk": 2,
        "type": "Apartment",
        "furnishing": "Unfurnished",
        "area_sqft": 870,
        "description": "Affordable 2 BHK close to Phase 1 of Hinjawadi IT Park. Perfect for IT employees. Good connectivity via expressway.",
        "amenities": ["Security", "Parking", "Lift", "Power Backup"],
        "images": [
            "https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=800"
        ],
        "lat": 18.5912, "lng": 73.7383,
        "owner_contact": "+91 20555 12345"
    },
    {
        "title": "Independent House 4 BHK",
        "price": 15000000,
        "location": "Vasant Kunj, Delhi",
        "city": "Delhi",
        "bhk": 4,
        "type": "Villa",
        "furnishing": "Semi-Furnished",
        "area_sqft": 2800,
        "description": "Elegant independent house in Vasant Kunj with a beautiful courtyard. Close to DLF Promenade Mall and Indira Gandhi International Airport.",
        "amenities": ["Courtyard", "3-Car Parking", "Generator", "CCTV", "Servant Quarter"],
        "images": [
            "https://images.unsplash.com/photo-1523217582562-09d0def993a6?w=800",
            "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800"
        ],
        "lat": 28.5198, "lng": 77.1577,
        "owner_contact": "+91 11456 78900"
    },
    {
        "title": "Compact Studio in Noida Sector 62",
        "price": 1500000,
        "location": "Sector 62, Noida",
        "city": "Noida",
        "bhk": 1,
        "type": "Apartment",
        "furnishing": "Furnished",
        "area_sqft": 420,
        "description": "Studio apartment near metro station in Noida's IT hub. Excellent for single professionals. Society with 24-hour security.",
        "amenities": ["Gym", "Security", "Power Backup"],
        "images": [
            "https://images.unsplash.com/photo-1536376072261-38c75010e6c9?w=800"
        ],
        "lat": 28.6273, "lng": 77.3724,
        "owner_contact": "+91 120 234 5678"
    },
    {
        "title": "Spacious 3 BHK Family Apartment",
        "price": 6300000,
        "location": "Sector 137, Noida",
        "city": "Noida",
        "bhk": 3,
        "type": "Apartment",
        "furnishing": "Semi-Furnished",
        "area_sqft": 1440,
        "description": "Beautiful 3 BHK apartment in a premium township. Easy commute to Delhi via Expressway. Schools and hospitals within walking distance.",
        "amenities": ["Swimming Pool", "Gym", "Children's Play Area", "Badminton Court", "24/7 Security"],
        "images": [
            "https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?w=800",
            "https://images.unsplash.com/photo-1560448204-603b3fc33ddc?w=800"
        ],
        "lat": 28.5143, "lng": 77.3903,
        "owner_contact": "+91 120 678 9012"
    },
    {
        "title": "Penthouse 4 BHK with City View",
        "price": 19000000,
        "location": "Sector 150, Noida",
        "city": "Noida",
        "bhk": 4,
        "type": "Apartment",
        "furnishing": "Furnished",
        "area_sqft": 2900,
        "description": "Premium penthouse offering unobstructed views of the Yamuna Expressway greens. Rooftop garden and lounge included.",
        "amenities": ["Rooftop Garden", "Swimming Pool", "Gym", "Concierge", "Sky Lounge", "Smart Home"],
        "images": [
            "https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?w=800",
            "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800"
        ],
        "lat": 28.4819, "lng": 77.4099,
        "owner_contact": "+91 120 999 8877"
    },
    {
        "title": "Affordable Plot in Emerging Area",
        "price": 2000000,
        "location": "Sector 89, Gurgaon",
        "city": "Gurgaon",
        "bhk": 0,
        "type": "Plot",
        "furnishing": "Unfurnished",
        "area_sqft": 1200,
        "description": "Residential plot in a developing sector of Gurgaon. DDJAY scheme approved. Great investment opportunity.",
        "amenities": ["Corner Plot", "Wide Road Access", "Ready Registry"],
        "images": [
            "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=800"
        ],
        "lat": 28.3800, "lng": 76.9850,
        "owner_contact": "+91 99111 22233"
    },
    {
        "title": "Commercial Shop in Busy Market",
        "price": 5500000,
        "location": "Connaught Place, Delhi",
        "city": "Delhi",
        "bhk": 0,
        "type": "Commercial",
        "furnishing": "Unfurnished",
        "area_sqft": 350,
        "description": "Prime commercial shop on ground floor of CP's famous inner circle. High foot traffic location. Suitable for retail, restaurant, or office.",
        "amenities": ["Corner Unit", "High Foot Traffic", "Metro Nearby"],
        "images": [
            "https://images.unsplash.com/photo-1497366216548-37526070297c?w=800"
        ],
        "lat": 28.6315, "lng": 77.2167,
        "owner_contact": "+91 11111 22222"
    },
    {
        "title": "2 BHK Row House in Township",
        "price": 5200000,
        "location": "Wagholi, Pune",
        "city": "Pune",
        "bhk": 2,
        "type": "Villa",
        "furnishing": "Semi-Furnished",
        "area_sqft": 1150,
        "description": "Cozy row house in a gated township. Private small garden and parking. Close to Kharadi and Magarpatta IT hubs.",
        "amenities": ["Private Garden", "Parking", "Clubhouse", "Security", "Children's Area"],
        "images": [
            "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800",
            "https://images.unsplash.com/photo-1582063289852-62e3ba2747f8?w=800"
        ],
        "lat": 18.5698, "lng": 73.9867,
        "owner_contact": "+91 20321 09876"
    },
    {
        "title": "3 BHK Bungalow in ECR",
        "price": 13500000,
        "location": "ECR Road, Chennai",
        "city": "Chennai",
        "bhk": 3,
        "type": "Villa",
        "furnishing": "Unfurnished",
        "area_sqft": 2400,
        "description": "Beautiful bungalow on the East Coast Road with partial sea view from terrace. Ideal for weekend home or permanent residence.",
        "amenities": ["Sea View Terrace", "Private Parking", "Bore Well", "Vastu-Compliant"],
        "images": [
            "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=800",
            "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800"
        ],
        "lat": 12.8499, "lng": 80.2336,
        "owner_contact": "+91 44777 88900"
    },
    {
        "title": "Premium 3 BHK in Jubilee Hills",
        "price": 12000000,
        "location": "Jubilee Hills, Hyderabad",
        "city": "Hyderabad",
        "bhk": 3,
        "type": "Apartment",
        "furnishing": "Furnished",
        "area_sqft": 2000,
        "description": "Opulent 3 BHK in Jubilee Hills — home to Hyderabad's who's who. Premium finishes, high ceilings, and excellent social infrastructure.",
        "amenities": ["Concierge", "Swimming Pool", "Gym", "Squash Court", "Spa", "Covered Parking"],
        "images": [
            "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800",
            "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800"
        ],
        "lat": 17.4239, "lng": 78.4084,
        "owner_contact": "+91 40555 66677"
    },
    {
        "title": "1 BHK Affordable Flat near Airport",
        "price": 1650000,
        "location": "Devanahalli, Bangalore",
        "city": "Bangalore",
        "bhk": 1,
        "type": "Apartment",
        "furnishing": "Unfurnished",
        "area_sqft": 540,
        "description": "Budget apartment near Kempegowda International Airport. Great for airline staff or airport professionals. Ready to move.",
        "amenities": ["Security", "Lift", "Parking"],
        "images": [
            "https://images.unsplash.com/photo-1555636222-cae831e670b3?w=800"
        ],
        "lat": 13.2078, "lng": 77.7057,
        "owner_contact": "+91 80456 78901"
    },
    {
        "title": "4 BHK Ultra-Luxury Apartment",
        "price": 45000000,
        "location": "Worli Sea Face, Mumbai",
        "city": "Mumbai",
        "bhk": 4,
        "type": "Apartment",
        "furnishing": "Furnished",
        "area_sqft": 3800,
        "description": "Ultra-luxury apartment with unobstructed Arabian Sea views from every room. Private elevator lobby, butler service, and smart home automation.",
        "amenities": ["Private Lift", "Infinity Pool", "Butler Service", "Smart Home", "Wine Cellar", "Home Theatre"],
        "images": [
            "https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?w=800",
            "https://images.unsplash.com/photo-1571055107559-3e67626fa8be?w=800",
            "https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?w=800"
        ],
        "lat": 18.9940, "lng": 72.8129,
        "owner_contact": "+91 98899 11223"
    },
    {
        "title": "2 BHK Flat in DLF City",
        "price": 6800000,
        "location": "DLF City Phase 3, Gurgaon",
        "city": "Gurgaon",
        "bhk": 2,
        "type": "Apartment",
        "furnishing": "Semi-Furnished",
        "area_sqft": 1100,
        "description": "Ready-to-move 2 BHK in DLF City with spacious rooms and good ventilation. Walking distance to DLF Mega Mall.",
        "amenities": ["Gym", "Swimming Pool", "24/7 Security", "Club House"],
        "images": [
            "https://images.unsplash.com/photo-1560185007-cde436f6a4d0?w=800"
        ],
        "lat": 28.4822, "lng": 77.0880,
        "owner_contact": "+91 124 456 7890"
    },
    {
        "title": "Gated Community Villa",
        "price": 18500000,
        "location": "Sarjapur Road, Bangalore",
        "city": "Bangalore",
        "bhk": 4,
        "type": "Villa",
        "furnishing": "Unfurnished",
        "area_sqft": 3200,
        "description": "Spacious villa in a premium gated community on Sarjapur Road. 3 floors, terrace garden, and 3-car garage. Well-connected to Electronic City.",
        "amenities": ["Terrace Garden", "3-Car Garage", "Swimming Pool", "Gym", "24/7 Security", "Clubhouse"],
        "images": [
            "https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800",
            "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=800"
        ],
        "lat": 12.8700, "lng": 77.6944,
        "owner_contact": "+91 80789 01234"
    },
    {
        "title": "Ready-to-Move 2 BHK at Best Price",
        "price": 3200000,
        "location": "Thane West, Mumbai",
        "city": "Mumbai",
        "bhk": 2,
        "type": "Apartment",
        "furnishing": "Unfurnished",
        "area_sqft": 800,
        "description": "Simple and clean 2 BHK apartment in Thane West. Well-maintained building. Close to Viviana Mall and Jupiter Hospital.",
        "amenities": ["Security", "Parking", "Lift"],
        "images": [
            "https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=800"
        ],
        "lat": 19.2183, "lng": 72.9780,
        "owner_contact": "+91 22456 78900"
    },
    {
        "title": "Luxury 3 BHK with Lake View",
        "price": 8900000,
        "location": "Bellandur, Bangalore",
        "city": "Bangalore",
        "bhk": 3,
        "type": "Apartment",
        "furnishing": "Furnished",
        "area_sqft": 1700,
        "description": "Lake-facing luxury apartment in Bellandur. Close to Ecospace and RGA Tech Park. Surrounded by greenery.",
        "amenities": ["Lake View", "Swimming Pool", "Gym", "Jogging Track", "Kids Club", "Security"],
        "images": [
            "https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?w=800",
            "https://images.unsplash.com/photo-1600566752355-35792bedcfea?w=800"
        ],
        "lat": 12.9264, "lng": 77.6759,
        "owner_contact": "+91 80222 33444"
    }
]

def get_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    db = get_db()
    db.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price INTEGER NOT NULL,
            location TEXT NOT NULL,
            city TEXT NOT NULL,
            bhk INTEGER DEFAULT 0,
            type TEXT NOT NULL,
            furnishing TEXT DEFAULT 'Unfurnished',
            area_sqft INTEGER DEFAULT 0,
            description TEXT,
            amenities TEXT DEFAULT '[]',
            images TEXT DEFAULT '[]',
            lat REAL DEFAULT 0,
            lng REAL DEFAULT 0,
            owner_contact TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            property_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (property_id) REFERENCES properties(id),
            UNIQUE(user_id, property_id)
        );
    ''')

    # Seed properties if empty
    count = db.execute('SELECT COUNT(*) FROM properties').fetchone()[0]
    if count == 0:
        for p in SEED_PROPERTIES:
            db.execute('''
                INSERT INTO properties
                (title, price, location, city, bhk, type, furnishing, area_sqft,
                 description, amenities, images, lat, lng, owner_contact)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                p['title'], p['price'], p['location'], p['city'], p['bhk'],
                p['type'], p['furnishing'], p['area_sqft'], p['description'],
                json.dumps(p['amenities']), json.dumps(p['images']),
                p['lat'], p['lng'], p['owner_contact']
            ))
        print(f"✅ Seeded {len(SEED_PROPERTIES)} properties")

    # Seed admin user
    import bcrypt
    admin_exists = db.execute("SELECT id FROM users WHERE email = 'admin@propfinder.com'").fetchone()
    if not admin_exists:
        pw_hash = bcrypt.hashpw(b'admin123', bcrypt.gensalt()).decode()
        db.execute(
            "INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)",
            ('Admin', 'admin@propfinder.com', pw_hash, 'admin')
        )
        print("✅ Seeded admin user: admin@propfinder.com / admin123")

    db.commit()
    db.close()
