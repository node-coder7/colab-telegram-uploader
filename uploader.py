import os
import requests
import telebot
from urllib.parse import urlparse

# Replace with your Telegram Bot Token and Target Chat ID
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID_HERE")

bot = telebot.TeleBot(BOT_TOKEN)

def get_filename_from_url(url: str) -> str:
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    return filename if filename else "downloaded_file"

def download_file(url: str, output_path: str):
    print(f"Downloading from: {url}")
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(output_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
    print(f"Download complete: {output_path}")

def send_to_telegram(file_path: str):
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > 50:
        print(f"Error: File is {file_size_mb:.2f} MB. Telegram Bot API limit is 50 MB.")
        return

    print(f"Uploading {file_path} ({file_size_mb:.2f} MB) to Telegram...")
    with open(file_path, "rb") as document:
        bot.send_document(CHAT_ID, document, caption=f"Uploaded: {os.path.basename(file_path)}")
    print("Upload complete!")

if __name__ == "__main__":
    download_url = input("Enter direct download link: ").strip()
    if download_url:
        filename = get_filename_from_url(download_url)
        download_file(download_url, filename)
        send_to_telegram(filename)
