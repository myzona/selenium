from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.json.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    service = Service('/usr/bin/chromedriver')  # Path to ChromeDriver
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        title = driver.title
        driver.quit()
        return jsonify({'title': title})
    except Exception as e:
        driver.quit()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
