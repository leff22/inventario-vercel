from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd

app = Flask(__name__)
app.secret_key = 'inventario123'  # necessário para session

@app.route('/')
def upload():
    return render_template('upload.html')

@app.route('/importar', methods=['POST'])
def importar():
    file = request.files['arquivo']
    df = pd.read_excel(file)

    if not all(col in df.columns for col in ['PN', 'DESCRIÇÃO', 'DEPÓSITO', 'QUANTIDADE SAP']):
        return "Planilha inválida. Certifique-se de que os campos sejam: PN, DESCRIÇÃO, DEPÓSITO, QUANTIDADE SAP."

    df['CONTADO'] = None
    session['inventario'] = df.to_dict(orient='records')
    return redirect(url_for('contagem'))

@app.route('/contagem', methods=['GET', 'POST'])
def contagem():
    inventario = session.get('inventario', [])

    if request.method == 'POST':
        for i, item in enumerate(inventario):
            contado = request.form.get(f'contado_{i}')
            try:
                inventario[i]['CONTADO'] = int(contado)
            except:
                inventario[i]['CONTADO'] = None
        session['inventario'] = inventario
        return redirect(url_for('relatorio'))

    return render_template('inventario.html', inventario=inventario)

@app.route('/relatorio')
def relatorio():
    inventario = session.get('inventario', [])
    df = pd.DataFrame(inventario)
    df['DIFERENÇA'] = df['CONTADO'] - df['QUANTIDADE SAP']
    relatorio = df.to_dict(orient='records')
    return render_template('relatorio.html', relatorio=relatorio)

if __name__ == '__main__':
    app.run(debug=True)