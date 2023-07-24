from serpapi import GoogleSearch

params = {
  "engine": "google_lens",
  "url": "https://i.imgur.com/QgOimQh.jpg",
  "api_key": "0f27d0f205a1366cb097a52480fc6aaa37fb48b457056337d6354bb6cc9729ea"
}

search = GoogleSearch(params)
results = search.get_dict()
visual_matches = results["visual_matches"]
print(visual_matches)