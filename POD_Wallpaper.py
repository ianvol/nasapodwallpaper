import requests
import ctypes
import os

# Replace this with your NASA API key if you wish to adapt this for your own use
NASA_API_KEY = "3tOoFEPcBizjtpBoxv5vZE2lRRRnhaWXZGeZaidL"

# Fetches data from API
def get_apod_data():
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch APOD data.")
        return None

# Method to download image, exception thrown if download failed
def download_image(url, save_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Failed to download image: {e}")

def set_wallpaper(image_path):
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)

# Main method that takes API data and locates relevant links
if __name__ == "__main__":
    apod_data = get_apod_data()
    if apod_data:
        image_url = apod_data.get("hdurl")
        image_title = apod_data.get("title")
        image_extension = os.path.splitext(image_url)[1]
        image_path = f"{image_title}{image_extension}"
        
        download_image(image_url, image_path)
        set_wallpaper(os.path.abspath(image_path))

        print(f"Set desktop background to NASA APOD: {image_title}")
