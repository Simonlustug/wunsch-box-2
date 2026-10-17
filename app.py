import os
from flask import Flask, render_template_string, request
import tidalapi

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wunsch Box</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #121212; color: #ffffff; text-align: center; padding: 30px; }
        .container { max-width: 600px; margin: auto; background: #1e1e1e; padding: 25px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
        input[type="text"] { width: 80%; padding: 12px; margin: 10px 0; border: none; border-radius: 5px; font-size: 16px; }
        button { background-color: #1db954; color: white; border: none; padding: 12px 20px; font-size: 16px; border-radius: 5px; cursor: pointer; }
        button:hover { background-color: #1aa34a; }
        .result-item { background: #2a2a2a; margin: 10px 0; padding: 10px; border-radius: 5px; display: flex; justify-content: space-between; align-items: center; text-align: left; }
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
            <button type="submit">Song suchen</button>
        </form>

        {% if tracks %}
            <h3>Suchergebnisse:</h3>
            {% for track in tracks %}
                <div class="result-item">
                    <span>{{ track.name }} - <strong>{{ track.artist.name }}</strong></span>
                    <form method="POST" style="margin: 0;">
                        <input type="hidden" name="selected_track" value="{{ track.name }} - {{ track.artist.name }}">
                        <button type="submit" style="padding: 6px 12px; font-size: 14px;">Wählen</button>
                    </form>
                </div>
            {% endfor %}
        {% endif %}

        {% if message %}
            <p class="message">{{ message }}</p>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    tracks = None
    message = None
    
    if request.method == 'POST':
        if 'song_query' in request.form:
            query = request.form.get('song_query')
            try:
                session = tidalapi.Session()
                session.login_anonymous()
                search_results = session.search(query, models=[tidalapi.Track], limit=5)
                tracks = search_results.tracks if search_results and search_results.tracks else []
                if not tracks:
                    message = "Keine Songs gefunden."
            except Exception as e:
                message = f"Fehler bei der Suche: {str(e)}"
                
        elif 'selected_track' in request.form:
            chosen = request.form.get('selected_track')
            message = f"Vielen Dank! '{chosen}' wurde erfolgreich als Wunsch eingereicht!"

    return render_template_string(HTML_TEMPLATE, tracks=tracks, message=message)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
