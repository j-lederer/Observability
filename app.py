from flask import Flask
from prometheus_client import start_http_server, Counter, generate_latest
from elasticapm.contrib.flask import ElasticAPM

app = Flask(__name__)

app.config['ELASTIC_APM'] = {
    'SERVICE_NAME': 'my-service-name',
    'SECRET_TOKEN': 'LWQFBZ2N2oc3OnfyyS',
    #SEpvTDY0c0Jfd1dsbzBfTV9kZXY6dmlzNWFlWVVRdnk5bDdvcTUwTmF5QQ==
    'SERVER_URL': 'https://7673dedfc3414efab4f5b8be08ea8efa.apm.us-central1.gcp.cloud.es.io:443',

    'ENVIRONMENT': 'my-environment',
    'DEBUG': True
}
apm = ElasticAPM(app)

import logging
import ecs_logging

# Get the Logger
logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

# Add an ECS formatter to the Handler
# handler = logging.StreamHandler()
handler = logging.FileHandler('apps_log.json')  # Log to a file
handler.setFormatter(ecs_logging.StdlibFormatter())
app.logger.addHandler(handler)



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

@app.route('/exception')
def exception():
    try:
        1 / 0
    except ZeroDivisionError:
        apm.capture_exception()
    return 'Exception'
    

@app.route('/log')
def log():
    apm.capture_message('hello, world!')   
    return 'Log'    

from elasticapm.traces import capture_span
from flask import jsonify

@app.route('/manual_instrumentation')
def manual_instrumentation():
    with capture_span('custom_span', span_type='custom', labels ={ "attribute1": 'value1',
        "attribute2": 'value2'} ):
        # Your code here
       
        # Add attributes to the span
        return jsonify({'message': 'Manual instrumentation done!'})


@app.route('/ecs_logging')
def ecs_logging():
    # Emit a log!
    app.logger.debug("Example message!", extra={"http.request.method": "get"})
    return 'ecs_logging'

if __name__ == '__main__':
    # start_http_server(5000)
    app.run(debug=True)