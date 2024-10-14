from flask import Flask, request, render_template, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
db = sqlite3.connect('dreams_db.sqlite', check_same_thread=False)
cursor = db.cursor()

@app.route('/dream/<int:dream_id>')
def dream(dream_id):
    with db:
        cursor.execute("SELECT * FROM dreams WHERE id = ?", (dream_id,))
        dream = cursor.fetchone()
        if dream is None:
            return "Dream not found", 404
        else:
            content = dream[1]
            title = dream[2]
            author = dream[3]
            tag = dream[4]
            upload_date = dream[5]
            upload_date = datetime.strptime(upload_date, '%Y-%m-%d %H:%M:%S')
            upload_date = upload_date.strftime('%d.%m.%Y')
            # likes = dream[6] im not using this yet (maybe never)
            description = dream[7]

    user_is_author = True # will eventually check session for this

    return render_template('dream.html', id=dream_id, title=title, content=content, author=author, tag=tag, upload_date=upload_date, description=description, user_is_author=user_is_author)

if __name__ == '__main__':
    app.run(debug=True)