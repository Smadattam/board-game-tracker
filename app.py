import json
from flask import Flask, jsonify
from requests import get
from xml.etree import ElementTree as et

app = Flask(__name__)

sample_xml = ''

# I've only tested with an entry of "gloomhaven" up to this point. You may need to adjust the XML parsing
# based on the actual structure returned by the API.

@app.route('/api/get_url/<search_string>', methods=['GET'])
def get_url(search_string):
    # Step 1: Send a GET request with the provided search string
    search_url = f"https://boardgamegeek.com/xmlapi2/search?query={search_string}"
    search_response = get(search_url)
    print(f"Response from search API: {search_response.text}")

    # Step 2: Parse the response for an acceptable id key. This section may need to be adjusted based
    # on the actual XML structure returned by the API.
    xml_data = et.fromstring(search_response.content)
    id_key = xml_data.find('.//item').get('id') if xml_data.find('.//item') is not None else None
    print(f"Extracted id: {id_key}")

    # Step 3: Send another GET request with the id key
    id_url = f"https://boardgamegeek.com/xmlapi2/thing?id={id_key}"
    response = get(id_url)
    print(f"Response from thing API: {response.text}")

    # Step 4: Parse the response for a image URL
    xml_data = et.fromstring(response.content)
    image_url = xml_data.find('.//image').text if xml_data.find('.//image') is not None else None
    print(f"Extracted image URL: {image_url}")

    return jsonify({"url": image_url})

if __name__ == '__main__':
    app.run(debug=True)