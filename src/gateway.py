import os
import requests
from dotenv import load_dotenv

load_dotenv()

""" Classe para abstrair acessos externos (APIs)"""
class ServiceOrderGateway:
    def __init__(self):
        # CARREGAR VARIÁVEIS DE AMBIENTE NECESSÁRIAS
        self.CHAMADOTASY_API_URL = os.getenv('CHAMADOTASY_API_URL')
        if not self.CHAMADOTASY_API_URL:
            raise ValueError("A variável de ambiente CHAMADOTASY_API_URL não está configurada.")

    def create_ticket(self, payload_data):
        try:
            # MONTAR REQUISIÇÃO PARA A API
            if payload_data.strip() == '':
                print("O payload não pode ser vazio")
                return {"message": "O payload não pode ser vazio"}, 500

            json_data = {
                "titulo_p": "Colaboradores desligados na última semana para inativação no AD",
                "ie_parado": "N", 
                "nm_usuario": "MYGUEL", 
                "nr_contato": "7272", 
                "nr_grupo_planej": "28", 
                "nr_grupo_trabalho": "28", 
                "nr_seq_equipamento": "203", 
                "nr_seq_localizacao": "78", 
                "descricao_p": f"Os seguintes colaboradores foram desligados nos últimos 7 dias, por favor verificar se possuem cadastro no AD para inativá-los \n {payload_data}", 
            }
            response = requests.post(f"{self.CHAMADOTASY_API_URL}/form/ajuste", json=json_data, headers={"Content-Type": "application/json"})

            response.raise_for_status()

            dados_json = response.json()
            return dados_json, 200

        except requests.exceptions.Timeout:
            print("Erro: O tempo limite da requisição foi excedido.")
            return str(e), response.status_code

        except requests.exceptions.ConnectionError:
            print("Erro: Não foi possível conectar ao servidor. Verifique sua conexão.")
            return str(e), response.status_code

        except requests.exceptions.HTTPError as e:
            print(f"Erro HTTP: {e}")
            return str(e), response.status_code

        except requests.exceptions.RequestException as e:
            print(f"Ocorreu um erro inesperado: {e}")
            return str(e), response.status_code

        except Exception as e:
            print(f"Error in gateway/create_ticket (gateway.py): {e}")
            return str(e), response.status_code