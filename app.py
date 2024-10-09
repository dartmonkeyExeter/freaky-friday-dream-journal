from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/dream/<int:dream_id>')
def dream(dream_id):
    return render_template('dream.html', id=dream_id)

if __name__ == '__main__':
    app.run(debug=True)