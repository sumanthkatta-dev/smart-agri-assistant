import json
import re
import base64
import requests
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from bs4 import BeautifulSoup

app = Flask(__name__)

# API keys (for demo purposes)
GEMINI_API_KEY = "AIzaSyCsSDTYO6MH2pYqjnvDeNkVOG-O2DxwM8A"
WEATHER_API_KEY = "8dbb52e717a0816fde006a7e4189bb20"

# Plant.id API Configuration (using v2 endpoint)
PLANT_ID_API_URL = "https://api.plant.id/v2/identify"
PLANT_ID_API_KEY = "4emofitN59GrMqRkhLrLA4GNspZLfRru2bYRdOXQKeWZkjCVnF"

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def get_precise_location(lat, lon):
    url = f"http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=1&appid={WEATHER_API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data:
            info = data[0]
            city = info.get("name", "")
            state = info.get("state", "")
            country = info.get("country", "")
            parts = [city, state, country]
            return ", ".join([p for p in parts if p])
        return "your location"
    except Exception:
        return "your location"

def get_weather(city):
    if "," not in city:
        city = city + ",IN"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        description = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        return (f"Weather in {data.get('name', city.title())}:\n"
                f"Description: {description}\n"
                f"Temperature: {temp}°C\n"
                f"Humidity: {humidity}%\n"
                f"Wind Speed: {wind} m/s")
    except Exception as e:
        return f"Error retrieving weather data: {e}"

def get_weather_by_coordinates(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        description = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        location = get_precise_location(lat, lon)
        return (f"Weather in {location}:\n"
                f"Description: {description}\n"
                f"Temperature: {temp}°C\n"
                f"Humidity: {humidity}%\n"
                f"Wind Speed: {wind} m/s")
    except Exception as e:
        return f"Error retrieving weather data by coordinates: {e}"

def call_gemini(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        config = {"temperature": 0.7, "top_p": 0.95, "top_k": 64, "max_output_tokens": 8192}
        response = model.generate_content(prompt, generation_config=config)
        if hasattr(response, "text"):
            return response.text
        elif hasattr(response, "candidates") and response.candidates:
            return response.candidates[0].content.parts[0].text
        else:
            return str(response)
    except Exception as e:
        return f"Error calling Gemini: {e}"

def call_gemini_for_farmers(user_query):
    prompt = f"""As an agricultural assistant, provide information to help farmers with the following query:
    
{user_query}

Structure your response with a summary, key information, recommendations, and next steps."""
    return call_gemini(prompt)

def get_crop_rotation_advice(user_query):
    prompt = f"""As an agricultural advisor, provide detailed crop rotation advice based on the following context:
    
{user_query}

Include recommendations on which crops to rotate, the benefits of proper rotation, and actionable next steps."""
    return call_gemini(prompt)

def get_fertilizer_recommendation(user_query):
    prompt = f"""As an agricultural advisor, provide detailed fertilizer recommendations based on the following context:
    
{user_query}

Include advice on types of fertilizers, application rates, timing, and any safety or environmental considerations."""
    return call_gemini(prompt)

# -------------------------------
# Agricultural Schemes Scraper (for https://agriwelfare.gov.in/en/)
# -------------------------------
def scrape_gov_schemes():
    """
    Scrapes available agricultural schemes from https://agriwelfare.gov.in/en/ by extracting 
    scheme titles from <h3> tags and their following <p> (if available) as a brief description.
    """
    url = "https://agriwelfare.gov.in/en/"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        schemes = []
        for h3 in soup.find_all("h3"):
            title = h3.get_text(strip=True)
            description = ""
            sibling = h3.find_next_sibling("p")
            if sibling:
                description = sibling.get_text(strip=True)
            if title:
                schemes.append({"scheme_name": title, "description": description})
        # Remove duplicates based on scheme name
        unique = {scheme['scheme_name']: scheme for scheme in schemes}
        return list(unique.values())
    except Exception as e:
        return [{"error": f"Failed to fetch schemes: {e}"}]

@app.route("/subsidy", methods=["GET"])
def subsidy():
    schemes = scrape_gov_schemes()
    return jsonify({"agricultural_schemes": schemes})

# -------------------------------
# Video Tutorials Mapping (Using YouTube)
# -------------------------------
VIDEO_TUTORIALS = [
    {
        "title": "Sri Method of Rice Cultivation | Eco Friendly Agriculture",
        "description": "Learn the basics of the Sri Method of Rice Cultivation for eco-friendly and sustainable agriculture.",
        "youtube_id": "dv9iY52cTCM"
    },
    {
        "title": "How to Start a Farm From Scratch (Beginner's Guide)",
        "description": "A comprehensive beginner's guide to starting a farm from scratch.",
        "youtube_id": "fRlUhUWS0Hk"
    },
    {
        "title": "System of Rice Intensification (SRI) Method Explained",
        "description": "Detailed explanation of the System of Rice Intensification (SRI) method to boost productivity.",
        "youtube_id": "TkHgAkJhtqw"
    },
    {
        "title": "Organic Rice Farming - Regenerative Paddy Cultivation",
        "description": "An in-depth look at organic rice farming practices using regenerative methods.",
        "youtube_id": "FVtmRf_awBU"
    },
    {
        "title": "Advanced SRI: Increase Rice Productivity",
        "description": "Advanced techniques in the System of Rice Intensification to increase yield significantly.",
        "youtube_id": "DEv_rflMhZ8"
    },
    {
        "title": "Multi Layer Farming | SSIAST | Art of Living",
        "description": "Learn about multi-layer farming techniques from SSIAST at the Art of Living International Center.",
        "youtube_id": "6NUJMq5LVZs"
    },
    {
        "title": "SRI Method of Paddy Cultivation | Bhaskar Padire",
        "description": "A practical demonstration of the SRI method for paddy cultivation by Bhaskar Padire.",
        "youtube_id": "ECWNV7IeU34"
    },
    {
        "title": "The #1 Secret to Farming Success: Learn Before You Start",
        "description": "Insights into farming success with emphasis on learning and preparation.",
        "youtube_id": "hB_TedigKz8"
    },
    {
        "title": "How to Start a Small Farm | A Step-by-Step Guide",
        "description": "Step-by-step guide for starting a small farm and managing it efficiently.",
        "youtube_id": "heTxEsrPVdQ"
    },
    {
        "title": "Increasing SRI-Organic Rice Yields through Double Rows Planting",
        "description": "Techniques for increasing rice yields using double rows planting under SRI.",
        "youtube_id": "wFSJnKmzPjE"
    }
]

@app.route("/video_tutorials", methods=["GET"])
def video_tutorials():
    return jsonify({"video_tutorials": VIDEO_TUTORIALS})

# -------------------------------
# Existing Endpoints (Chat, Weather, Crop Rotation, Fertilizer, Pest Detection)
# -------------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/weather", methods=["GET"])
def weather():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    if lat and lon:
        return get_weather_by_coordinates(lat, lon)
    else:
        return get_weather("Delhi")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form.get("message", "")
    lat = request.form.get("lat")
    lon = request.form.get("lon")
    lower_msg = user_message.lower()
    if "weather" in lower_msg:
        m = re.search(r"weather in ([\w\s,]+)", lower_msg)
        if m:
            city = m.group(1).strip()
            return get_weather(city)
        elif lat and lon:
            return get_weather_by_coordinates(lat, lon)
        else:
            return get_weather("Delhi")
    else:
        return call_gemini_for_farmers(user_message)

@app.route("/crop_rotation", methods=["POST"])
def crop_rotation():
    if request.is_json:
        data = request.get_json()
        user_message = data.get("message", "")
    else:
        user_message = request.form.get("message", "")
    response_text = get_crop_rotation_advice(user_message)
    if request.is_json:
        return jsonify({"response": response_text})
    else:
        return response_text

@app.route("/fertilizer", methods=["POST"])
def fertilizer():
    if request.is_json:
        data = request.get_json()
        user_message = data.get("message", "")
    else:
        user_message = request.form.get("message", "")
    response_text = get_fertilizer_recommendation(user_message)
    if request.is_json:
        return jsonify({"response": response_text})
    else:
        return response_text

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json()
    user_message = data.get("message", "")
    lat = data.get("lat")
    lon = data.get("lon")
    lower_msg = user_message.lower()
    if "weather" in lower_msg:
        m = re.search(r"weather in ([\w\s,]+)", lower_msg)
        if m:
            city = m.group(1).strip()
            response_text = get_weather(city)
        elif lat and lon:
            response_text = get_weather_by_coordinates(lat, lon)
        else:
            response_text = get_weather("Delhi")
        return jsonify({"response": response_text})
    else:
        response_text = call_gemini_for_farmers(user_message)
        return jsonify({"response": response_text})

@app.route("/detect_pest", methods=["POST"])
def detect_pest():
    if "image" not in request.files:
        return "No image uploaded", 400
    image = request.files["image"]
    image_bytes = image.read()
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
    headers = {
        "Content-Type": "application/json",
        "Api-Key": PLANT_ID_API_KEY
    }
    payload = {
        "images": [encoded_image],
        "modifiers": ["crops_fast"],
        "plant_details": ["diseases"]
    }
    response = requests.post(PLANT_ID_API_URL, headers=headers, json=payload)
    try:
        response.raise_for_status()
        result = response.json()
        if result.get("suggestions"):
            output = "<h2>Pest Detection Results:</h2><ul>"
            for suggestion in result["suggestions"]:
                name = suggestion.get("plant_name", "Unknown Pest")
                probability = suggestion.get("probability", 0) * 100
                output += f"<li>{name}: {probability:.2f}% confidence</li>"
            output += "</ul>"
            return output
        else:
            return "No pests detected."
    except Exception as e:
        return f"Error calling Plant.id API: {e}"

if __name__ == "__main__":
    app.run(debug=True)
