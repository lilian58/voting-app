from flask import Flask, render_template, request, make_response, g
import os
import socket
import random
import json
import psycopg2
import logging

# Configurer les options de vote
option_a = os.getenv('OPTION_A', "Cats")
option_b = os.getenv('OPTION_B', "Dogs")
hostname = socket.gethostname()

app = Flask(__name__)

# Logger Gunicorn
gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.INFO)

# Connexion à PostgreSQL
def get_db():
    if not hasattr(g, 'db'):
        db_host = os.getenv('POSTGRES_HOST', 'localhost')
        db_port = os.getenv('POSTGRES_PORT', '5432')
        db_user = os.getenv('POSTGRES_USER', 'postgres')
        db_password = os.getenv('POSTGRES_PASSWORD', 'postgres')
        db_name = os.getenv('POSTGRES_DB', 'voting_app')

        g.db = psycopg2.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            dbname=db_name
        )
    return g.db

# Créer la table de votes si elle n'existe pas encore
def create_votes_table():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS votes (
        id SERIAL PRIMARY KEY,
        voter_id TEXT NOT NULL,
        vote TEXT NOT NULL
    );
    """)
    db.commit()

@app.route("/", methods=['POST','GET'])
def hello():
    # Identifier un voteur
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    vote = None

    if request.method == 'POST':
        # Enregistrer le vote dans la base de données
        db = get_db()
        cursor = db.cursor()
        vote = request.form['vote']
        app.logger.info('Received vote for %s', vote)

        # Insérer le vote dans la base de données
        cursor.execute("INSERT INTO votes (voter_id, vote) VALUES (%s, %s)", (voter_id, vote))
        db.commit()

    resp = make_response(render_template(
        'index.html',
        option_a=option_a,
        option_b=option_b,
        hostname=hostname,
        vote=vote,
    ))
    resp.set_cookie('voter_id', voter_id)
    return resp

if __name__ == "__main__":
    create_votes_table()  # Créer la table lors du démarrage de l'application
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)

