from core.crud_base import Crudmedstock
from core.database import conectar_banco
from core.validador import Validador

# = Feito pela -- Ana Beatriz //

#============================ CLASSE FORNECEDOR =========================

class Fornecedor(Crudmedstock):
    table = "fornecedor"
    fields = [
        "nome_fornecedor",
        "cnpj",
        "email",
    ]

    def __init__(self, nome_fornecedor, cnpj, email):
        self.nome_fornecedor = nome_fornecedor
        self.cnpj = cnpj
        self.email = email

#=============================VALIDAÇÃO==============================
    def validate(self):
        erros = [
            Validador.obrigatorio(self.nome_fornecedor, "nome_fornecedor"),
            Validador.minimo_de_caracteres(self.nome_fornecedor, "nome_fornecedor", 3),
            Validador.valida_externa_email(self.email, "email", "22558|TvTq03AbZrLvC2Db5SLfeCW67P49qnQ3"),
        ]
        return [erro for erro in erros if erro]
#===========================================================
    @classmethod
    def deletar_fornecedor(cls, id):
        fornecedor = cls.seleciona_por_id(id)
        if not fornecedor:
            raise ValueError("Fornecedor não encontrado.")
        '''if cls.has_related_records(id): #! atencao
            raise ValueError("Não é possível excluir o produto porque ele possui pedidos ou movimentações vinculadas.")'''
        cls.delete(id)
