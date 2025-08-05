import requests

def main():
    while True:
        search_string = input("/nEnter a search string (or 'x' to quit): ")
        if search_string.lower() == 'x':
            break
        response = requests.get(f"http://localhost:5000/api/get_url/{search_string}")
        url_string = response.json().get('url')
        print(f"image url: {url_string}")

if __name__ == '__main__':
    main()