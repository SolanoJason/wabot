import requests
import json
from environs import Env

env = Env()
env.read_env()

GUPSHUP_KEY = env("GUPSHUP_KEY")
APPNAME = env("APPNAME")
BOT_NUMBER = env("BOT_NUMBER")
MY_NUMBER = env("MY_NUMBER")
CREDS = (APPNAME, GUPSHUP_KEY)
url = "https://api.gupshup.io/wa/api/v1/msg"


def send_message(message_type, phone=None, **kwargs):
    if phone is None:
        phone = MY_NUMBER
    payload = {
        "message": json.dumps({"type": message_type, **kwargs}),
        "channel": "whatsapp",
        "source": BOT_NUMBER,
        "destination": phone,
        "src.name": APPNAME,
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "apikey": GUPSHUP_KEY,
    }

    response = requests.post(url, data=payload, headers=headers)

    print(response.text)


def send_text(text, phone=None):
    send_message("text", phone, text=text)

def send_image(original_url, caption, preview_url=None, phone=None):
    send_message("image", phone, originalUrl=original_url, previewUrl=preview_url, caption=caption)

def send_file(url, filename, phone=None):
    send_message("file", phone, url=url, filename=filename)

def send_audio(url, phone=None):
    send_message("audio", phone, url=url)

def send_video(url, phone=None):
    send_message("video", phone, url=url)

def send_sticker(url, phone=None):
    send_message("sticker", phone, url=url)

def send_list(body, global_button_title, items, footer=None, title=None, msg_id=None, phone=None):
    """
    Sends a list message via the Gupshup API.

    Parameters:
    - title (str): The title of the list.
    - body (str): The body text of the list message.
    - footer (str): The footer text of the list message.
    - msg_id (str): The message ID used to identify the list message.
    - sections (list): A list of sections, each containing options for the list.
    - global_button_title (str): The title of the global button for the list.
    - phone (int or str, optional): The phone number of the recipient. Defaults to None.

    The function constructs a list message with the provided content and sends it to
    the specified phone number via the Gupshup API using the `send_message` function.

    Example:
    sections = [{"title": "Section 1", "subtitle": "Subtitle 1", "options": [{"type": "text", "title": "Option 1", "description": "Description 1", "postbackText": "Postback 1"}]}]
    send_list_message("List Title", "Body text", "Footer text", "msg1", sections, "Global button")
    """
    message = {
        "title": title,
        "body": body,
        "footer": footer,
        "msgid": msg_id,
        "globalButtons": [
            {"type": "text", "title": global_button_title}
        ],
        "items": items
    }
    send_message("list", phone, **message)

def send_buttons(content, buttons, msg_id=None, phone=None):
    """
    Sends a quick reply message with buttons via the Gupshup API.

    Parameters:
    - content (dict): A dictionary containing the message content. This includes:
        - type (str): The type of content (e.g., 'text').
        - header (str): The header text for the quick reply message.
        - text (str): The main body text of the quick reply message.
        - caption (str): The footer text of the quick reply message.
    - buttons (list): A list of button options. Each option is a dictionary containing:
        - type (str): The type of button (e.g., 'text').
        - title (str): The display text for the button.
        - postbackText (str): The text sent back when the button is clicked.
    - msg_id (str, optional): A unique identifier for the message. Defaults to None.
    - phone (int or str, optional): The phone number of the recipient. Defaults to None.

    The function constructs a quick reply message with the provided content and buttons,
    then sends it to the specified phone number via the Gupshup API using the `send_message` function.

    Example:
    content = {
            "type": "text",
            "header": "this is the header",
            "text": "this is the body",
            "caption": "this is the footer"
        }
    buttons = [
            {"type": "text", "title": "First", "postbackText": "dev-defined-postback1"},
            {"type": "text", "title": "Second", "postbackText": "dev-defined-postback2"},
            {"type": "text", "title": "Third", "postbackText": "dev-defined-postback3"}
        ]
    send_buttons(content, buttons, msg_id="qr1")
    """
    message = {
        "msgid": msg_id,
        "content": content,
        "options": buttons
    }
    send_message("quick_reply", phone, **message)