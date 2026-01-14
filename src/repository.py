import src.database as db
import src.querys.sql as sql
from sqlalchemy import text

class CollaboratorRepository:
    def __init__(self):
        pass

    def get_collaborator(self):
        try:
            lista = []
            with db.connect_fortesrh_db() as conn_fortes:
                result = conn_fortes.execute(text(sql.query_fortes))
                data = result.fetchall()
                if data:
                    for row in data:
                        lista.append({
                            "nr_cpf": row[0],
                            "dt_desligamento": row[1],
                            "dia_desligamento": row[2],
                            "nm_pessoa_fisica": row[3]
                        })
            lista = {
                "deactivated_users": lista
            }
            return lista, 200
        except Exception as e:
            print(f"Error in get_collaborator: {e}")
            return str(e), 500
        
    def comp_collaborator(self, users_fortes: list):
        try:
            users_tasy = []
            with db.connect_oracle_db() as conn_oracle:
                for row in users_fortes:

                    result = conn_oracle.execute(text(sql.query_oracle), {"NR_CPF": row["nr_cpf"]})
                    data = result.fetchall()
                    if data:
                        tasy_user = data[0]
                        users_tasy.append({
                            "nm_pessoa_fisica": row.get("nm_pessoa_fisica"),
                            "nm_usuario": tasy_user[1],
                            "dia_desligamento": row.get("dia_desligamento"),
                            "dt_desligamento": row.get("dt_desligamento"),
                            "tem_usuario": True,
                        })
                    else :
                        users_tasy.append({
                            "nm_pessoa_fisica": row.get("nm_pessoa_fisica"),
                            "nm_usuario": None,
                            "dia_desligamento": row.get("dia_desligamento"),
                            "dt_desligamento": row.get("dt_desligamento"),
                            "tem_usuario": False
                        })

            return users_tasy, 200
        except Exception as e:
            print(f"Error in comp_collaborator: {e}")
            return str(e), 500
        
    def inativar_collaborator(self, users: list):
        try:
            
            with db.connect_oracle_db() as conn_oracle:
                for row in users:
                    conn_oracle.execute(text(sql.query_oracle_inativar), {"NM_USUARIO": row["nm_usuario"]})
                    conn_oracle.execute(text(sql.query_oracle_insert_log), {"NM_USUARIO": row["nm_usuario"]})

                conn_oracle.commit() 
            return "Usuários inativados com sucesso!", 200

        except Exception as e:
            print(f"Error in inativar_collaborator: {e}")
            return str(e), 500
