# Libs usadas - INÍCIO
from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
# Libs usadas - FIM

app = Flask(__name__)

@app.route('/exchange_rate_tool', methods=['GET'])
def run_exchange_rate_tool():
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Diretório atual do meu ChromeDriver (em prod, vamos colocar numa env. var.)
    chrome_options.add_argument(f"executable_path=C:\\Users\\lucas\\Desktop\\chromedriver_win32\\chromedriver.exe")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Instrução para acessar o site alvo
        driver.get("https://dolarhoje.com/")

        # Timeout de 20s, atualmente a solução chega a 9.24s
        wait = WebDriverWait(driver, 20)

        # Caso a request não exceda 10s, inicia a busca
        try:
            # Busca diretamente pelo id 'nacional', que exibe o valor do dólar em real, dentro do input
            result = wait.until(EC.presence_of_element_located((By.ID, "nacional")))
            # Excessão para casos de timeout
        except TimeoutException:
            result = None

        # Decisor principal
        if result:
            # Caso 'nacional' retorne o valor em 'value', salvamos em 'current_usd_exchange_rate'
            current_usd_exchange_rate = result.get_attribute('value')

            response = {
                'usd_brl_exchange_rate': current_usd_exchange_rate,
                'success': True
            }

            return jsonify(response), 200
        else:
            # Caso 'nacional' não seja encontrado ou esteja vazio
            response = {
                'error': "Houve um erro ao obter a cotação do dólar.",
                'success': False
            }

            return jsonify(response), 400

    # Caso a operação falhe por algum motivo não previsto, exibe a mensagem de erro genérica
    except Exception:
        response = {
            'error': "Houve um erro sistêmico, por favor, tente novamente.",
            'success': False
        }

        return jsonify(response), 500

    # Encerra a busca até nova request
    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True)