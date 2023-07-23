from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search_item = request.form.get('search_item')
    if search_item:
        url = f"http://api.scraperapi.com?api_key=bd4c71356f9f72977ada71b9ba911ba5&url=https://www.google.com/search?q={search_item}&render=true"
        response = requests.get(url)
        # It would be better to parse this response and render it in a user-friendly way.
        # Just returning raw HTML won't give a good user experience.
        return response.text  
    else:
        return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
