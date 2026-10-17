import os
from flask import Flask, render_template_string, request, redirect, url_for
import tidalapi

app = Flask(__name__)

# HTML-Template für die Wunschbox (direkt eingebunden, damit keine extra Ordner nötig sind)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wwunsch Box</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #121212; color: #ffffff; text-align: center; padding: 50px; }
        .container { max-width: 500px; margin: auto; background: #1e1e1e; padding: 30px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
        input[type="text"] { width: 80%; padding: 12px; margin: 10px 0; border: none; border-radius: 5px; font-size: 16px; }
        button { background-color: #1db954; color: white; border: none; padding: 12px 20px; font-size: 16px; border-radius: 5px; cursor: pointer; }
        button:hover { background-color: #1aa34a; }
        .message { margin-top: 15px; color: #1db954; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🎵 Wunsch Box 🎵</h2>
        <p>Wünsch dir einen Song für die Playlist!</p>
        <form method="POST">
            <input type="text" name="song_query" placeholder="Interpret & Songtitel..." required>
            <br>
            <button type="submit">Wunsch abschicken</button>
        </form>
        {% if message %}
            <p class="message">{{ message }}</p>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    if request.method == 'POST':
        song_query = request.form.get('song_query')
        # Hier greift später die Tidal-Logik
        message = f"Vielen Dank! '{song_query}' wurde als Wunsch aufgenommen."
    return render_template_string(HTML_TEMPLATE, message=message)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)