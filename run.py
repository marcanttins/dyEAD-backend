# run.py
from interfaces.http.app import create_app

# Cria a app Flask com configuração de ambiente (padrão 'dev')
app = create_app('dev')

if __name__ == '__main__':
    # Roda o servidor na porta 5000, modo debug conforme configuração
    app.run(host='localhost', port=5000)
