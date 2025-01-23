import os
import base64
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

@app.route('/screenshot', methods=['POST'])
def screenshot():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)

    try:
        # Set extended timeouts
        driver.set_page_load_timeout(30)  # Set a 30-second timeout for page load
        driver.set_script_timeout(30)  # Set a 30-second timeout for script execution

        # Navigate to the URL
        driver.get(url)

        # Wait until the page is fully loaded (waiting for the body tag to be present)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Execute JavaScript to get the full page height
        total_height = driver.execute_script("return document.body.scrollHeight")

        # Set the browser window size to match the full page height
        driver.set_window_size(1024, total_height)  # 1920px width for desktop view

        # Take a screenshot and save it to a temporary file
        screenshot_path = "/tmp/full_screenshot.png"
        driver.save_screenshot(screenshot_path)

        # Read the screenshot file and encode it in base64
        with open(screenshot_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        return jsonify({
            'url': url,
            'screenshot': encoded_image
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
