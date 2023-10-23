import os
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

# Setting the API key
openai.api_key = "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"

# Testing OpenAI API key by printing using it to print list all OpenAI models
# print(openai.Model.list()) 

messages = [{"role": "system", "content": "You are an expert assistant to Deloitte Audit team to assist them with US Tax law related queries. Only answer questions if they are related to tax. Otherwise respond that you cannot answer outside tax domain questions."},{"role": "assistant", "content": "How can I help you with your tax related queries?"}]

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        userQuery = request.form["userQuery"]
        messages.append({"role": "user", "content": userQuery})
        response = get_assistant_response(messages)
        messages.append({"role": "assistant", "content": response})
        return render_template("index.html", results=display_chat_history(messages))
    return render_template("index.html", results=display_chat_history(messages))

def get_assistant_response(messages):
    r = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": m["role"], "content": m["content"]} for m in messages],
    )
    response = r.choices[0].message.content
    return response

def display_chat_history(messages):
    results = []
    for message in messages:
        if message["role"] != "system":
            newReply = "{}: {}".format(message['role'].capitalize(), message['content'])
            results.append(newReply)
    return results




