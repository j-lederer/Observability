from flask import Flask

app = Flask(__name__)

# Route 1: Home page
@app.route('/')
def home():
    return 'Welcome to the home page!'

# Route 2: About page
@app.route('/about')
def about():
    return 'This is the about page.'

# Route 3: Contact page
@app.route('/contact')
def contact():
    return 'Contact us at contact@example.com'

if __name__ == '__main__':
    app.run(debug=True)