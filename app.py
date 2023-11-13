from flask import Flask
from prometheus_client import start_http_server, Counter, generate_latest

app = Flask(__name__)
# Prometheus metrics
counter = Counter('requests_total', 'Total number of requests.')

# Route 1: Home page
@app.route('/')
def home():
    counter.inc()
    return 'Welcome to the home page!'

# Route 2: About page
@app.route('/about')
def about():
    counter.inc()
    return 'This is the about page.'

# Route 3: Contact page
@app.route('/contact')
def contact():
    counter.inc()
    return 'Contact us at contact@example.com'

@app.route('/metrics')
def custom_metrics():
    # return str(counter)
    return generate_latest()


if __name__ == '__main__':
    # start_http_server(5000)
    app.run(debug=True)