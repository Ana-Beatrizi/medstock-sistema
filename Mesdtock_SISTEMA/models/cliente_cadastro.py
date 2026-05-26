from core.crud_base import Crudmedstock
from core.database import conectar_banco
from core.validador import Validador

#! = Feito pela -- Ana Beatriz // linha 1 a 45 𖹭.ᐟ

#============================ CLASSE CLIENTE CADASTRO =========================

class ClientesCadastro(Crudmedstock):
    table = "clientes_cadastro"
    fields = [
        "nome",
        "cpf",
        "telefone",
        "cidade",
        "estado",
        "cep"
    ]

    def __init__(self, nome, cpf, telefone, cidade, estado, cep):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.cidade = cidade
        self.estado = estado
        self.cep = cep

#=============================VALIDAÇÃO==============================
    def validate(self):
        erros = [
            Validador.obrigatorio(self.nome, "nome"),
            Validador.minimo_de_caracteres(self.nome, "nome", 3),
        ]
        return [erro for erro in erros if erro]
#===========================================================
    @classmethod
    def deletar_clientes_cadastro(cls, id):
        clientes_cadastro = cls.seleciona_por_id(id)
        if not clientes_cadastro:
            raise ValueError("Cliente não encontrado.")
        '''if cls.has_related_records(id): #! atencao
            raise ValueError("Não é possível excluir o produto porque ele possui pedidos ou movimentações vinculadas.")'''
        cls.delete(id)

#! = Feito pela -- Ana Beatriz // linha 1 a 45 𖹭.ᐟ