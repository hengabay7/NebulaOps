import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from services.weather import get_weather_and_activity


load_dotenv()

def create_app():
    """Flask application factory"""
    app = Flask(__name__)

    @app.get('/')
    def index():
        return render_template('index.html')

    @app.post('/recommend')
    def recommend():
        city = request.form.get('city', '').strip()
        if not city:
            return render_template('index.html', error="Please enter a city name")
        try:
            data = get_weather_and_activity(city)
            return render_template('result.html', **data)
        except Exception as e:
            return render_template('index.html', error=f"Error fetching weather data: {e}")

    @app.get('/health')
    def health():
        return {"status": "ok"}, 200

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=bool(int(os.getenv('FLASK_DEBUG', '1'))))
