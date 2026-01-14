import src.usecase as usecase
from src.server.instance import server
app = server.app

@app.route('/', methods=['POST'])
def deactivate_collaborator():
    try:
        usecaseCol = usecase.CollaboratorUseCase()
        result, status_code = usecaseCol.deactivate_collaborator()

        return { 
            "message": result["message"], 
            "deactivated_users": result["deactivated_users"] 
        }, status_code

    except Exception as e:
        print(f"Error in '/' route function: {e}")
        return { 'message': 'Deu algum erro' }, 500

@app.route('/service-order/user-deactivation/chamadotasy', methods=['POST'])
def create_user_deactivations_service_order():
    try:
        usecase_ticket = usecase.ServiceOrderUseCase()
        data, status_code = usecase_ticket.create_ad_deactivation_ticket()
        print(data)
        return { "message": data["message"] }, status_code
    except Exception as e:
        print(f"Error in '/service-order/user-deactivation/chamadotasy' route function: {e}")
        return { 'message': 'Não foi possível abrir a solicitação por algum erro no servidor' }, 500

@app.route('/health', methods=['GET'])
def healthcheck():
    try:
        return { 'message': 'Está tudo ok!' }, 200
    except Exception as e:
        print(f"Error in '/health' route function: {e}")
        return { 'message': 'Deu algum erro' }, 500