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
        response = None
        try:
            print("Entrou no gateway create_ticket")
            # MONTAR REQUISIÇÃO PARA A API
            if not payload_data or (isinstance(payload_data, str) and payload_data.strip() == ''):
                print("O payload não pode ser vazio")
                return {"message": "O payload não pode ser vazio"}, 400

            headers = {"Content-Type": "application/json"}
            json_data = {
                "titulo_p": "Colaboradores desligados na última semana para inativação no AD",
                "ie_parado": "N", 
                "nm_usuario": "MYGUEL", 
                "nr_contato": "7272", 
                "nr_grupo_planej": "28", 
                "nr_grupo_trabalho": "28", 
                "nr_seq_equipamento": "203", 
                "nr_seq_localizacao": "78", 
                "descricao_p": (
                    "Os seguintes colaboradores foram desligados nos últims 7 dias, "
                    "por favor verificar se possuem cadastro no AD para inativá-los \n" 
                    f"{payload_data}"
                ), 
            }
            response = requests.post(
                f"{self.CHAMADOTASY_API_URL}/form/ajuste", 
                json=json_data, 
                headers=headers
            )
            print("Resposta recebida da API de ChamadoTasy")
            response.raise_for_status()
            dados_json = response.json()

            return dados_json, response.status_code

        except requests.exceptions.Timeout:
            print("Erro: O tempo limite da requisição foi excedido.")
            return {"error": "O tempo limite da requisição foi excedido."}, response.status_code

        except requests.exceptions.ConnectionError:
            print("Erro: Não foi possível conectar ao servidor. Verifique sua conexão.")
            return {"error": "Falha de conexão com o servidor"}, response.status_code

        except requests.exceptions.HTTPError as e:
            print(f"Erro HTTP: {e}")
            return {"error": str(e)}, getattr(response, "status_code", 500)

        except requests.exceptions.RequestException as e:
            print(f"Ocorreu um erro inesperado: {e}")
            return {"error": str(e)}, getattr(response, "status_code", 500)

        except Exception as e:
            print(f"Error in gateway/create_ticket (gateway.py): {e}")
            return {"error": str(e)}, getattr(response, "status_code", 500)
