"""
Live property routes backed by housing-api.p.rapidapi.com
All routes are under /api/live/
"""
from flask import Blueprint, request, jsonify
from housing_service import (
    get_property_listing,
    get_property_detail,
    get_city_overview,
    get_price_trends,
    CITY_SLUGS,
)

live_bp = Blueprint("live", __name__)


@live_bp.route("/properties", methods=["GET"])
def live_properties():
    """
    GET /api/live/properties
    Query params:
      city        – city name (default: mumbai)
      type        – apartment | villa | plot | commercial (optional)
      transaction – buy | rent (default: buy)
      page        – page number (default: 1)
    """
    city        = request.args.get("city", "mumbai").strip()
    prop_type   = request.args.get("type", "").strip()
    transaction = request.args.get("transaction", "buy").strip()
    page        = int(request.args.get("page", 1))

    result = get_property_listing(city, prop_type, transaction, page)

    if "error" in result:
        return jsonify(result), 502

    return jsonify(result)


@live_bp.route("/property", methods=["GET"])
def live_property_detail():
    """
    GET /api/live/property?url=<housing.com_url>
    Returns full details for a single property.
    """
    url = request.args.get("url", "").strip()
    if not url:
        return jsonify({"error": "url parameter is required"}), 400

    result = get_property_detail(url)
    if result and "error" in result:
        return jsonify(result), 502

    return jsonify(result)


@live_bp.route("/city-overview", methods=["GET"])
def live_city_overview():
    """
    GET /api/live/city-overview?city=mumbai
    Returns market overview stats for the city.
    """
    city   = request.args.get("city", "mumbai").strip()
    result = get_city_overview(city)

    if "error" in result:
        return jsonify(result), 502

    return jsonify(result)


@live_bp.route("/price-trends", methods=["GET"])
def live_price_trends():
    """
    GET /api/live/price-trends?city=mumbai&locality=bandra
    Returns historical price trend data.
    """
    city     = request.args.get("city", "mumbai").strip()
    locality = request.args.get("locality", "").strip()
    result   = get_price_trends(city, locality)

    if "error" in result:
        return jsonify(result), 502

    return jsonify(result)


@live_bp.route("/cities", methods=["GET"])
def supported_cities():
    """
    GET /api/live/cities
    Returns the list of cities supported by this integration.
    """
    cities = [c.title() for c in CITY_SLUGS.keys()]
    return jsonify({"cities": sorted(set(cities))})
