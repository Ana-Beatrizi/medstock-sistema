from core.crud_base import Crudmedstock
from core.database import conectar_banco
from core.validador import Validador

#! = Feito pela -- Ana Beatriz //  𖹭.ᐟ

#============================ CLASSE PRODUTO =========================

class Produto(Crudmedstock):
    table = "produto"
    fields = [
        "fornecedor_id",
        "nome",
        "quantidade_estoque",
        "categoria",
        "estoque_minimo",
        "preco_custo",
        "preco_venda",
    ]

    def __init__(self, fornecedor_id, nome, quantidade_estoque, categoria, estoque_minimo, preco_custo,
                 preco_venda,):
        self.fornecedor_id = fornecedor_id
        self.nome = nome
        self.quantidade_estoque = quantidade_estoque
        self.categoria = categoria
        self.estoque_minimo = estoque_minimo
        self.preco_custo = preco_custo
        self.preco_venda = preco_venda


#============================ VALIDAÇÃO =========================
    def validate(self):
        erros = [
            Validador.obrigatorio(self.nome, "nome"),
            Validador.nao_negativo(self.quantidade_estoque, "quantidade_estoque"),
            Validador.nao_negativo(self.preco_custo, "preço de custo"),
            Validador.nao_negativo(self.preco_venda, "preço de venda"),
            Validador.nao_negativo(self.estoque_minimo, "estoque_minimo"),
            Validador.obrigatorio(self.estoque_minimo, "estoque_minimo"),
        ]
        return [erro for erro in erros if erro]

    @classmethod
    def deletar_produto(cls, id):
        produto = cls.seleciona_por_id(id)
        if not produto:
            raise ValueError("Produto não encontrado.")
        '''if cls.has_related_records(id): #! atencao
            raise ValueError("Não é possível excluir o produto porque ele possui pedidos ou movimentações vinculadas.")'''
        cls.delete(id)

    @classmethod
    def upd_quantidade(cls, id, nova_quantidade, connection=None):
        conexao = connection or Database.connect()
        cursor = conexao.cursor()
        try:
            sql = "UPDATE produto SET quantidade = %s WHERE id = %s"
            cursor.execute(sql, (nova_quantidade, id))
            if connection is None:
                conexao.commit()
            return cursor.rowcount
        except Exception:
            if connection is None:
                conexao.rollback()
            raise
        finally:
            cursor.close()
            if connection is None:
                conexao.close()

'''
#! =================
#! err
    @classmethod
    def estoque_baixo(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM produto WHERE quantidade <= estoque_minimo ORDER BY nome"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def update_quantity(cls, id, nova_quantidade, connection=None):
        conexao = connection or Database.connect()
        cursor = conexao.cursor()
        try:
            sql = "UPDATE produto SET quantidade = %s WHERE id = %s"
            cursor.execute(sql, (nova_quantidade, id))
            if connection is None:
                conexao.commit()
            return cursor.rowcount
        except Exception:
            if connection is None:
                conexao.rollback()
            raise
        finally:
            cursor.close()
            if connection is None:
                conexao.close()

    @classmethod
    def has_related_records(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            queries = [
                "SELECT COUNT(*) FROM movimentacao WHERE produto_id = %s",
                "SELECT COUNT(*) FROM pedido_movimentacao WHERE produto_id = %s"
            ]
            total = 0
            for sql in queries:
                cursor.execute(sql, (id,))
                total += cursor.fetchone()[0]
            return total > 0
        finally:
            cursor.close()
            conexao.close()
'''