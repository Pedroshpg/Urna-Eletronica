# app.py
from flask import Flask, render_template, request, redirect
from conexao import conectar

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form['nome']
        partido = request.form['partido']
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO candidatos (nome, partido) VALUES (%s, %s)", (nome, partido))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('cadastrar.html')

@app.route('/votar', methods=['GET', 'POST'])
def votar():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM candidatos")
    candidatos = cursor.fetchall()

    if request.method == 'POST':
        cpf = request.form['cpf']
        candidato_id = request.form['candidato']
        cursor.execute("SELECT * FROM votacoes WHERE cpf = %s", (cpf,))
        if cursor.fetchone():
            conn.close()
            return "Você já votou!"
        cursor.execute("INSERT INTO votacoes (cpf, candidato_id) VALUES (%s, %s)", (cpf, candidato_id))
        cursor.execute("UPDATE candidatos SET votos = votos + 1 WHERE id = %s", (candidato_id,))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('votar.html', candidatos=candidatos)

@app.route('/resultado')
def resultado():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, partido, votos FROM candidatos ORDER BY votos DESC")
    resultados = cursor.fetchall()
    conn.close()
    return render_template('resultado.html', resultados=resultados)

if __name__ == '__main__':
    app.run(debug=True)
