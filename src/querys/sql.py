query_fortes = '''
SELECT
    a.cpf,
    TO_CHAR(a.datadesligamento, 'DD/MM/YYYY') AS data_desligamento,
    TO_CHAR(a.datadesligamento, 'DD') AS dia_desligamento,
    a.nome AS nm_pessoa_fisica
FROM colaborador a
WHERE 'w' = 'w'
  AND a.datadesligamento BETWEEN current_date - INTERVAL '10 week' AND current_date - INTERVAL '1 day'
ORDER BY a.nome ASC;
'''

query_oracle = '''
SELECT
    A.NM_PESSOA_FISICA NM_PESSOA_FISICA,
    B.NM_USUARIO NM_USUARIO
FROM PESSOA_FISICA A LEFT JOIN USUARIO B ON A.CD_PESSOA_FISICA = B.CD_PESSOA_FISICA
WHERE 1=1
AND A.NR_CPF = :NR_CPF
AND B.NM_USUARIO IS NOT NULL
AND B.IE_SITUACAO = 'A'
'''

query_oracle_inativar = '''
UPDATE USUARIO SET IE_SITUACAO = 'I',
    DT_ATUALIZACAO	= SYSDATE,
    DT_INATIVACAO	= SYSDATE,
    DS_OBSERVACAO = 'API INATIVAAI'
WHERE 1=1
AND NM_USUARIO = :NM_USUARIO
'''

query_oracle_insert_log = '''
INSERT INTO usuario_hist 
        (nr_sequencia,
        nm_usuario,
        nm_usuario_ref,
        ds_alteracao,
        dt_atualizacao)
VALUES  (usuario_hist_seq.NEXTVAL,
        'API INATIVAAI',
        :NM_USUARIO,
        'Usuário desligado',
        SYSDATE)
'''

query_fortes_to_ad = '''
SELECT
    a.nome,
    TO_CHAR(a.datadesligamento, 'DD/MM/YYYY') AS data_desligamento,
FROM colaborador a
WHERE 'w' = 'w'
  AND a.datadesligamento BETWEEN current_date - INTERVAL '1 week' AND current_date - INTERVAL '1 day';
'''
