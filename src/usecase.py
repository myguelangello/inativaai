import src.repository as repo
import src.gateway as gateway

class CollaboratorUseCase:
    def __init__(self):
        self.collaborator_repo = repo.CollaboratorRepository()

    def deactivate_collaborator(self):
        try:
            coll_exists, status_code = self.collaborator_repo.get_collaborator()
            if status_code != 200:
                return { "message": "Não houveram colaboradores desligados no período" }, status_code

            """ Deve receber um retorno com {"nm_pessoa_fisica: "", "nm_usuario": "", "dt_desligamento": ""} """
            users_tasy, status_code = self.collaborator_repo.comp_collaborator(coll_exists["deactivated_users"])
            if status_code != 200:
                return { "message": "Nenhum dos colaboradores desligados foi encontrado no Tasy" }, 404

            if users_tasy == []:
                return { 
                    "message": "Não há usuários para serem inativados no período", 
                    "deactivated_users": users_tasy
                }, status_code
            
            result, status_code = self.collaborator_repo.inativar_collaborator(users_tasy)

            return { 
                "message": result, 
                "deactivated_users": users_tasy 
            }, status_code
            
        except Exception as e:
            print(f"Error in deactivate_collaborator (usecase.py): {e}")
            return str(e), 500

class ServiceOrderUseCase:
    def __init__(self):
        self.collaborator_repo = repo.CollaboratorRepository()
        self.service_order_gateway = gateway.ServiceOrderGateway()
        # outro repository para enviar os dados
    
    def create_ad_deactivation_ticket(self):
        try:
            data, status_code = self.collaborator_repo.get_collaborator()
            if status_code != 200:
                return { "message": "Erro ao buscar colaboradores" }, status_code

            if not data.get("deactivated_users"):
                return { 
                    "message": "Não houveram colaboradores desligados para abertura de chamado" 
                }, 404
            
            formatted_data = ",\n".join([pessoa["nm_pessoa_fisica"] for pessoa in data["deactivated_users"]])
            data, status_code = self.service_order_gateway.create_ticket(formatted_data)

            if status_code != 200:
                return { "message": "Erro ao criar a ordem de serviço" }, status_code

            return {"message": f"Ordem de Serviço aberta com o Nº {data['nr_seq_os']}."}, status_code

        except Exception as e:
            print(f"Error in create_ad_deactivations_ticket (usecase.py): {e}")
            return str(e), 500