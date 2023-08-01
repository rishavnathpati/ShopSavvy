import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from serpapi import GoogleSearch

UPLOAD_FOLDER = "uploads"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def upload_image(image_path):
    try:
        result = subprocess.run(
            ["images-upload-cli", "-h", "imgur", image_path],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            image_url = result.stdout.strip()
            print(f"Image uploaded successfully: {image_url}")
            return image_url
        else:
            print(f"Error uploading image: {result.stderr.strip()}")
            return None
    except Exception as e:
        print(f"Error uploading image: {str(e)}")
        return None


@app.route("/")
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/index")
def index():
    return render_template("index.html")


# @app.route('/search', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return redirect(request.url)
#     file = request.files['file']
#     if file.filename == '':
#         return redirect(request.url)
#     if file:
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(file_path)
#         image_url = upload_image(file_path)
#         if image_url is not None:
#             params = {
#                 "q": "shopping",
#                 "engine": "google_reverse_image",
#                 "image_url": image_url,
#                 "location_requested": "Delhi, India",
#                 "google_domain": "google.com",
#                 "hl": "en",
#                 "gl": "in",
#                 "start": 0,
#                 "device": "desktop",
#                 "api_key": "0f27d0f205a1366cb097a52480fc6aaa37fb48b457056337d6354bb6cc9729ea"
#             }
#             search = GoogleSearch(params)
#             results = search.get_dict()
#             visual_matches = results["image_results"]
#             return render_template('results.html', results=visual_matches)
#         else:
#             return "Error uploading image"
#     return redirect(request.url)


@app.route('/search', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        image_url = upload_image(file_path)
        if image_url is not None:
            params = {
                "q": "shopping,india",
                "engine": "google_lens",
                "url": image_url,
                "api_key": "0f27d0f205a1366cb097a52480fc6aaa37fb48b457056337d6354bb6cc9729ea"
            }
            search = GoogleSearch(params)
            results = search.get_dict()
            visual_matches = results["visual_matches"]
            
            # Split results into ones with price and ones without
            without_price = [result for result in visual_matches if 'price' not in result or 'value' not in result['price']]
            with_price = [result for result in visual_matches if 'price' in result and 'value' in result['price']]

            # Convert price to float
            for result in with_price:
                result['price']['extracted_value'] = float(result['price']['extracted_value'])

            # Sort ones with price by price (lowest to highest)
            with_price = sorted(with_price, key=lambda k: k['price']['extracted_value'])

            # Concatenate the ones without price at the start and the top 20 ones with price
            visual_matches = without_price + with_price[:20]

            return render_template('results.html', results=visual_matches)
        else:
            return "Error uploading image"
    return redirect(request.url)



if __name__ == "__main__":
    app.run(debug=True)
