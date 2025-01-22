from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

app = Flask(__name__)

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

