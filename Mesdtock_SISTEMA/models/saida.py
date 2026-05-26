from datetime import datetime
from core.crud_base import Crudmedstock
from core.database import conectar_banco
from core.validador import Validador
from models.produto import Produto

#from models.movimentacao import Movimentacao #! err

#! = Feito pela -- Ana Beatriz //  𖹭.ᐟ

#============================ CLASSE PEDIDO ENTRADA =========================
class PedidoSaida(Crudmedstock):
    table = "saida"
    fields = [
        "data_pedido",
        "valor_total",
        "observacao",
        "quantidade_pedido",
        "data_processamento",
        "clientes_cadastro_id",
        "produto_id"
    ]

    def __init__(self, data_pedido, valor_total, clientes_cadastro_id, produto_id, quantidade_pedido, observacao="", data_processamento=None):
        self.data_pedido = data_pedido or datetime.now()
        self.valor_total = valor_total
        self.clientes_cadastro_id = clientes_cadastro_id
        self.produto_id = produto_id
        self.observacao = observacao
        self.quantidade_pedido = quantidade_pedido
        self.data_processamento = data_processamento

#============================ VALIDAÇÃO =========================
    def validate(self):
        erros = [
            Validador.obrigatorio(self.quantidade_pedido, "quantidade_pedido"),
        ]
        return [erro for erro in erros if erro]

    @classmethod
    def encontra_tudo_com_produto(cls):
        conexao = conectar_banco.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = """
            SELECT * from saida 
            order by data_pedido desc
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def historico_saida(cls):
        conexao = conectar_banco.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = """
SELECT
    e.id,
    f.nome as cliente,
    p.nome,
    e.quantidade_pedido,
    e.valor_total,
    e.data_pedido
FROM saida e
JOIN clientes_cadastro f ON e.clientes_cadastro_id = f.id
JOIN produto p ON e.produto_id = p.id
ORDER BY e.data_pedido DESC
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def processar(cls, id):
        conexao = conectar_banco.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            conexao.start_transaction()

            cursor.execute("SELECT * FROM pedido_movimentacao WHERE id = %s FOR UPDATE", (id,))
            pedido = cursor.fetchone()
            if not pedido:
                raise ValueError("Pedido não encontrado.")

            if pedido["status"] != "PENDENTE":
                raise ValueError("Somente pedidos pendentes podem ser processados.")

            cursor.execute("SELECT * FROM produto WHERE id = %s FOR UPDATE", (pedido["produto_id"],))
            produto = cursor.fetchone()
            if not produto:
                raise ValueError("Produto não encontrado.")

            if pedido["tipo"] == "ENTRADA":
                nova_quantidade = produto["quantidade"] + pedido["quantidade"]
            elif pedido["tipo"] == "SAIDA":
                if pedido["quantidade"] > produto["quantidade"]:
                    raise ValueError("Estoque insuficiente para concluir a saída.")
                nova_quantidade = produto["quantidade"] - pedido["quantidade"]
            else:
                raise ValueError("Tipo de pedido inválido.")

            Produto.update_quantity(produto["id"], nova_quantidade, connection=conexao)

            mov = Movimentacao(produto["id"], pedido["tipo"], pedido["quantidade"])
            cursor.execute(
                """
                INSERT INTO movimentacao (produto_id, tipo_movimentacao, quantidade, data_movimentacao)
                VALUES (%s, %s, %s, %s)
                """,
                (mov.produto_id, mov.tipo_movimentacao, mov.quantidade, mov.data_movimentacao)
            )

            cursor.execute(
                """
                UPDATE pedido_movimentacao
                SET status = %s, data_processamento = %s
                WHERE id = %s
                """,
                ("CONCLUIDO", datetime.now(), id)
            )

            conexao.commit()
            return "Pedido processado com sucesso."
        except Exception:
            conexao.rollback()
            raise
        finally:
            cursor.close()
            conexao.close()
'''
    @classmethod
    def cancelar(cls, id):
        conexao = conectar_banco.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM entrada WHERE id = %s", (id,))
            pedido = cursor.fetchone()
            if not pedido:
                raise ValueError("Pedido não encontrado.")
            if pedido["status"] != "PENDENTE":
                raise ValueError("Somente pedidos pendentes podem ser cancelados.")

            cursor = conexao.cursor()
            cursor.execute(
                """
                UPDATE entrada
                SET status = %s, data_processamento = %s
                WHERE id = %s
                """,
                ("CANCELADO", datetime.now(), id)
            )
            conexao.commit()
            return "Pedido cancelado com sucesso."
        except Exception:
            conexao.rollback()
            raise
        finally:
            cursor.close()
            conexao.close()
'''