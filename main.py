from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from pathlib import Path

app = Flask(__name__)

rosetta_stone = pd.read_csv(Path(__file__).parent / "data" / "morse_code.csv")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/translation", methods=['POST'])
def translation():
    direction = request.form.get("direction")
    raw_input = (request.form.get("input") or "")

    if direction == 'text_to_morse':
        user_text = raw_input.upper().strip()
        translated_text = ""
        for letter in user_text:
            if letter.isspace():
                translated_text += "/ "
            else:
                translated_text += (rosetta_stone.loc[rosetta_stone['character'] == letter, 'morse'].iloc[0]) + " "
        return render_template('index.html', input_value=raw_input, translation=translated_text)
        
    if direction == 'morse_to_text':
        user_text = raw_input.strip().split()
        translated_text = ""
        for letter in user_text:
            if letter == "/":
                translated_text += " "
            else:
                translated_text += (rosetta_stone.loc[rosetta_stone['morse'] == letter, 'character'].iloc[0])
        return render_template('index.html', input_value=raw_input, translation=translated_text)

    return render_template("index.html")

@app.route("/clear", methods=['POST'])
def clear():
    return render_template("index.html", input_value="", translation="")

if __name__ == '__main__':
    app.run(debug=True)