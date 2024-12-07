from flask import Flask, request, render_template, jsonify
import pandas as pd

app = Flask(__name__)

# Carregar dados do CSV
DATA_PATH = 'MICRODADOS_ED_SUP_IES_2023.CSV'
data = pd.read_csv(DATA_PATH, sep=';', encoding='latin-1')

# Obter lista de estados únicos
estados = data['SG_UF_IES'].dropna().unique()

@app.route('/')
def index():
    return render_template('index.html', estados=sorted(estados))

@app.route('/get_municipios', methods=['POST'])
def get_municipios():
    estado = request.form.get('estado')
    municipios = data[data['SG_UF_IES'] == estado]['NO_MUNICIPIO_IES'].dropna().unique()
    return jsonify(sorted(municipios.tolist()))

@app.route('/resultados', methods=['POST'])
def resultados():
    estado = request.form.get('estado')
    municipio = request.form.get('municipio')

    resultados = data
    if estado:
        resultados = resultados[resultados['SG_UF_IES'] == estado]
    if municipio:
        resultados = resultados[resultados['NO_MUNICIPIO_IES'] == municipio]

    # Exibir as colunas desejadas
    resultados = resultados[['NO_IES', 'NO_BAIRRO_IES']].rename(
        columns={'NO_IES': 'Nome', 'NO_BAIRRO_IES': 'Bairro'}
    )

    return render_template('resultados.html', tabelas=resultados.to_html(classes='table table-striped', index=False))

if __name__ == '__main__':
    app.run(debug=True)