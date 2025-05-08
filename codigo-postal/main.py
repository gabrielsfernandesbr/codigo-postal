from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>Consulta de CEP</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        input, button { padding: 8px; font-size: 16px; }
    </style>
</head>
<body>
    <h2>Consulta de CEP</h2>
    <form method="post">
        <label for="cep">Digite o CEP:</label>
        <input type="text" name="cep" required>
        <button type="submit">Buscar</button>
    </form>

    {% if data %}
        <h3>Resultado:</h3>
        <ul>
            <li><strong>CEP:</strong> {{ data['cep'] }}</li>
            <li><strong>Logradouro:</strong> {{ data['logradouro'] }}</li>
            <li><strong>Complemento:</strong> {{ data['complemento'] }}</li>
            <li><strong>Bairro:</strong> {{ data['bairro'] }}</li>
            <li><strong>Cidade:</strong> {{ data['localidade'] }}</li>
            <li><strong>Estado:</strong> {{ data['uf'] }}</li>
        </ul>
    {% elif error %}
        <p style="color: red;">{{ error }}</p>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    error = None

    if request.method == 'POST':
        cep = request.form['cep']
        try:
            url = f'https://viacep.com.br/ws/{cep}/json/'
            response = requests.get(url)
            if response.status_code == 200:
                json_data = response.json()
                if 'erro' not in json_data:
                    data = json_data
                else:
                    error = f"CEP {cep} não encontrado."
            else:
                error = "Erro ao consultar o serviço ViaCEP."
        except Exception as e:
            error = f"Ocorreu um erro: {e}"

    return render_template_string(HTML_TEMPLATE, data=data, error=error)

if __name__ == '__main__':
    app.run(debug=True)
