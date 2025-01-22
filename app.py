import os
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

app = Flask(__name__)

# Fetch the API token from the environment variable
API_TOKEN = os.getenv("API_TOKEN")

@app.before_request
def check_token():
    # Extract token from the Authorization header
    token = request.headers.get('Authorization')
    if not token or token != f"Bearer {API_TOKEN}":
        return jsonify({'error': 'Unauthorized'}), 401

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        html_content = driver.page_source  # Get the page's HTML content
        return jsonify({
            'url': url,
            'html': html_content
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


