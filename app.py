from flask import Flask, request, jsonify
import threading
from gapi import send_buttons, send_image, send_list, send_text, send_audio, send_file, send_message, send_sticker, send_video
from pprint import pprint
from environs import Env
from datetime import datetime
from bson.objectid import ObjectId
from db import user_exists, get_stage, create_user, update_stage, get_thread_and_assistant, update_thread_and_assistant
from gpt_api import client

env = Env()
env.read_env()

BLANK = "", 200
DEBUG = env("DEBUG")

app = Flask(__name__)

rex = client.beta.assistants.retrieve('asst_33AR9NhhBFoCysc0V37xZp5j')

@app.route("/receive_message", methods=["POST"])
def webhook():
    data = request.json
    print("\n \n")
    pprint(data, indent=4)
    event_type = data["type"]
    general_payload = data["payload"]
    general_payload_type = general_payload["type"]
    date = datetime.fromtimestamp(data["timestamp"] / 1000)

    match event_type:
        case "message":

            name = general_payload["sender"]["name"]
            phone = general_payload["sender"]["phone"]
            internal_payload = general_payload["payload"]

            if not user_exists(phone):
                create_user(name, phone, date)
                start_chat(phone)
                return BLANK

            stage = get_stage(phone)

            # Setting up variables
            match general_payload_type:
                case "text":
                    user_message = internal_payload["text"].lower()
                case "image":
                    pass
                case "file":
                    pass
                case "audio":
                    pass
                case "video":
                    pass
                case "contact":
                    pass
                case "location":
                    pass
                case "button_reply":
                    user_message = internal_payload["title"].lower()
                case "list_reply":
                    user_message = internal_payload["title"].lower()

            match stage:
                case "start":
                    match user_message:
                        case "tiranosaurio rex":
                            thread = client.beta.threads.create()
                            run = client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=rex.id, additional_instructions='Se breve y conciso')
                            messages = client.beta.threads.messages.list(thread_id=thread.id)
                            bot_message = messages.data[0].content[0].text.value
                            send_image("https://imagenes.elpais.com/resizer/v2/PFFAQ3CQUNFUPJACQ3XD7LE3JA.jpg?auth=e6e934a2867c98bfc5d4f490cba8d7867a5fd6c0b6cfc89cd36081ddd14545cd&width=414", caption=bot_message)
                            update_stage(phone, "dinasour_selected")
                            update_thread_and_assistant(phone, thread.id, "rex")
                        case "velociraptor":
                            send_text("Hola soy el velociraptor", phone=phone)
                            update_stage(phone, "dinasour_selected")
                        case "cuello largo":
                            send_text("Hola soy el cuello largo", phone=phone)
                            update_stage(phone, "dinasour_selected")
                        case "espinosaurus":
                            send_text("Hola soy el espinosaurus", phone=phone)
                            update_stage(phone, "dinasour_selected")
                        case "allosaurus":
                            send_text("Hola soy el allosaurus", phone=phone)
                            update_stage(phone, "dinasour_selected")
                        case "otros":
                            send_list(
                                body="Selecciona",
                                global_button_title="Ver mas dinosaurios",
                                phone=phone,
                                items=[
                                    {
                                        "title": "Herbivoros",
                                        "options": [
                                            {
                                                "type": "text",
                                                "title": "Cuello Largo",
                                                "description": "first row of first section description",
                                                "postbackText": "section 1 row 1 postback payload",
                                            },
                                        ],
                                    },
                                    {
                                        "title": "Carnivoros",
                                        "options": [
                                            {
                                                "type": "text",
                                                "title": "Espinosaurus",
                                                "description": "first row of first section description",
                                                "postbackText": "section 1 row 1 postback payload",
                                            },
                                            {
                                                "type": "text",
                                                "title": "Allosaurus",
                                                "description": "first row of first section description",
                                                "postbackText": "section 1 row 2 postback payload",
                                            },
                                        ],
                                    },
                                ],
                            )
                        case _:
                            start_chat(phone, content_text="Selecciona un dinosaurio valido")
                case "dinasour_selected":
                    thread_id, assistant_name = get_thread_and_assistant(phone)
                    if assistant_name == "rex":
                        dinosaur = rex
                    client.beta.threads.messages.create(thread_id, content=user_message, role="user")
                    run = client.beta.threads.runs.create_and_poll(thread_id=thread_id, assistant_id=dinosaur.id, additional_instructions='Se breve y conciso')
                    messages = client.beta.threads.messages.list(thread_id)
                    bot_message = messages.data[0].content[0].text.value
                    send_text(bot_message, phone=phone)

        case "user-event":
            pass
        case "template-event":
            pass
        case "message-event":
            pass
        case "billing-event":
            pass
    return BLANK

def start_chat(phone, content_text="Bienvenido, selecciona con que dinousaurio quieres interactuar"):
    content = {
        "type": "text",
        "text": content_text,
    }

    buttons = [
        {
            "type": "text",
            "title": "Tiranosaurio Rex",
            "postbackText": "postback_rex",
        },
        {
            "type": "text",
            "title": "Velociraptor",
            "postbackText": "postback_velociraptor",
        },
        {
            "type": "text",
            "title": "Otros",
            "postbackText": "postback_otros",
        },
    ]

    if DEBUG:
        content["caption"] = "stage is start"

    send_buttons(content, buttons, phone=phone)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=DEBUG)
