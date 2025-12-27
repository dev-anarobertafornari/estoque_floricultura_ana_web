# Autora: Ana Roberta Fornari

from flask import Flask, render_template, request, redirect, url_for
from estoque.database import estoque

app = Flask(__name__)

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Página para visualizar o estoque
@app.route('/estoque') 
def ver_estoque():
    return render_template('listar.html', flores=estoque)


# Página administrativa
@app.route('/admin')
def admin():
    return render_template('admin.html', flores=estoque)


# Adicionar nova flor ao estoque
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        nome = request.form.get('nome')
        quantidade = request.form.get('quantidade', type=int)
        preco = request.form.get('preco', type=float)
        
        if not nome or quantidade is None or preco is None:
            return render_template('adicionar.html', erro = "Preencha todos os campos.")

        estoque.append({
        'nome': nome.strip(),
        'quantidade': quantidade,
        'preco': preco
        })

        return redirect(url_for('ver_estoque'))
    return render_template('adicionar.html')


# Remover quantidade de uma flor
@app.route('/remover/<nome>', methods=['GET', 'POST'])
def remover(nome):
    nome = nome.strip().lower()

    # Encontrar flor
    flor = next((f for f in estoque if f['nome'].lower() == nome), None)
    if flor is None:
        return "Flor não encontrada",

    if request.method == 'POST':
        qtd_remover = request.form.get('quantidade', type=int)

        if qtd_remover is None or qtd_remover <= 0:
            return render_template('remover.html', flor=flor, erro = "Quantidade inválida.")

        # Atualizar quantidade
        flor['quantidade'] -= qtd_remover

        # Se acabar, remover do estoque
        if flor['quantidade'] <= 0:
            estoque.remove(flor)

        return redirect(url_for('ver_estoque'))
    return render_template('remover.html', flor=flor)
    

# Inicialização da aplicação
if __name__ == '__main__':
    app.run(debug=True)
