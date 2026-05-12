# Importações FLASK =========
from flask import Flask, jsonify, request, url_for, render_template, redirect, flash, session
#============================

# Importações CLASSES =======
from models.cliente import Cliente
from models.produto import Produto
from models.entrada import PedidoEntrada
#============================

# Importações E-MAIL ========
from email.mime.text import MIMEText # Texto no email
from email.mime.image import MIMEImage # Imagem no email
from email.mime.multipart import MIMEMultipart
import smtplib #Simple Mail Transfer Protocol - protocolo para enviar e-mail pela internet
#============================

# OUTRAS Importações ========
import random
#============================


app = Flask(__name__)
app.secret_key = "Medstock_programa_de_estoque_123456"

#! = Feito pela -- Ana Beatriz // linha 1 a 417

# TRANSFORMA DADOS ============
# inteiro
def to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

# decimal
def to_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default
# ===============================

# ======================= ROTAS =====================

# TELA DE CADASTRO ===============
@app.route("/")
def index():
    return render_template("tela_cadastro.html") 
#==============================================

# TELA DE LOGIN ===============
@app.route("/entrar")
def tela_login():
    return render_template("tela_login.html")
#==============================================

# TELA HOME ===============
@app.route("/home")
def tela_home():
    cliente_id = session.get("cliente_id")

    return render_template("tela_home.html", cliente = Cliente.seleciona_por_id(cliente_id))
#==============================================

# TELA CADASTRO PRODUTO==============
@app.route("/cadastro/produto")
def tela_cadastro_produto():
    cliente_id = session.get("cliente_id")
    return render_template("tela_cadastro_produto.html", cliente = Cliente.seleciona_por_id(cliente_id), produto = None)
#==============================================

# TELA PRODUTO==============
@app.route("/produto")
def tela_produtos():
    cliente_id = session.get("cliente_id")
    return render_template("tela_produtos.html", produtos = Produto.seleciona_tudo(order_by="nome"), cliente = Cliente.seleciona_por_id(cliente_id))
#==============================================

# TELA ENTRADA==============
@app.route("/pedido/entrada")
def tela_entrada():
    return render_template("tela_entrada.html", entrada=PedidoEntrada.encontra_tudo_com_produto())
#==============================================

# TELA SAIDA==============
@app.route("/pedido/saida")
def tela_saida():
    return render_template("tela_saida.html")
#==============================================

# TELA CADASTRO PEDIDOS==============
@app.route("/cadastro/pedido")
def tela_cadastro_pedidos():
    return render_template("tela_cadastro_pedidos.html", pedidos=PedidoEntrada.encontra_tudo_com_produto())
#==============================================

# TELA PERFIL DO USUARIO==============
@app.route("/perfil")
def tela_perfil_do_usuario():
    cliente_id = session.get("cliente_id")
    return render_template("tela_perfil_do_usuario.html", cliente = Cliente.seleciona_por_id(cliente_id))
#==============================================

# -------------------------------------- CLIENTE ------------------------------------------
# GET FORM TELA DE CADASTRO ===============
def get_cliente_form_cadastro():
    return {
        "nome": request.form.get("nome").strip(),
        "email": request.form.get("email").strip(),
        "cpf": request.form.get("cpf").strip(),
        "senha": request.form.get("senha").strip(),
    }
#==============================================

# POST SALVA CLIENTE ===============
@app.route("/cliente/salvar", methods=["POST"])
def salvar_cliente():
    dados = get_cliente_form_cadastro()
    cliente = Cliente(**dados)
    erros = cliente.validate()

    if erros:
            flash(erros[0], "danger")
            return render_template("tela_cadastro.html", cliente=dados)

    try:
        cliente.insert()
        flash("Cliente cadastrado com sucesso.", "success")
        return redirect(url_for("tela_login"))
    except Exception as e:
        # Verifica se o erro é de entrada duplicada (código 1062 do MySQL)
        if "1062" in str(e):
            flash("E-mail ou CPF já cadastrado no sistema.", "danger")
        else:
            flash(f"Erro ao cadastrar Cliente: {e}", "danger")
        return render_template("tela_cadastro.html", cliente=dados)
#==============================================

# POST ATUALIZAR CLIENTE ======================
@app.route("/cliente/atualizar/<int:id>", methods=["POST"])
def atualizar_cliente(id):
    dados = get_cliente_form_cadastro()
    cliente = Cliente(**dados)
    erros = cliente.validate()

    if erros:
        for erro in erros:
            flash(erro[0], "erro")
        dados["id"] = id
        return render_template("tela_cadastro.html", cliente=dados)

    try:
        if not Cliente.seleciona_por_id(id):
            flash("Cliente não encontrado.", "danger")
            return redirect(url_for("tela_login"))

        cliente.atualizar(id)
        flash("Cliente atualizado com sucesso.", "success")
        return redirect(url_for("tela_login"))
    except Exception as e:
        dados["id"] = id
        flash(f"Erro ao atualizar cliente: {e}", "danger")
        return render_template("tela_cadastro.html", cliente=dados)
# =========================================

# DELETAR CLIENTE ==================
@app.route("/cliente/excluir/<int:id>")
def excluir_cliente(id):
    try:
        Cliente.deletar_cliente(id)
        flash("Cliente excluído com sucesso.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    except Exception as e:
        flash(f"Erro ao excluir cliente: {e}", "danger")
    return redirect(url_for("tela_login")) #!
# ====================================

# Faz LOGIN CLIENTE ===============
@app.route("/cliente/login", methods=['POST'])
def fazer_login():
    email = request.form.get("email")
    senha = request.form.get("senha")


    cliente = Cliente.seleciona_por_email(email)

    if cliente["senha"] == senha:
        session["cliente_id"] = cliente["id"]
        flash("Login realizado com sucesso!", "success")
        return redirect(url_for("tela_home"))
    else:
        flash("Email ou senha inválidos!", "danger")
        return render_template("tela_login.html")

# -------------------------------------- CLIENTE FIM ------------------------------------------

#! -------------------------------------- ESQUECI A SENHA ------------------------------------------
#  Esqueci a senha ROTA===============
@app.route("/esqueci_a_senha", methods=["GET", "POST"])
def tela_esqueci_a_senha():
    if request.method == "POST":
        email = request.form.get("email")
        codigo = random.randint(100000, 999999)
        enviar_codigo_email(email, codigo)
        return  "Código enviado"

    return render_template("tela_esqueci_a_senha.html")

# Enviar Codigo E-MAIL =============
def enviar_codigo_email(destinatario, codigo):

    email_remetente = "medstock.sistema@gmail.com" 
    senha_app = "hahz uyzh eidq txts"

    mensagem = MIMEMultipart()

    mensagem["From"] = email_remetente
    mensagem["To"] = destinatario
    mensagem["Subject"] = "Código de recuperação MEDSTOCK"

    corpo = f"""
    <html>
        <body style="text-align:center;">

            <img src="cid:logo_medstock" width="200">

            <h2>Seu código de recuperação é:</h2>

            <h1>{codigo}</h1>

        </body>
    </html>
    """

    mensagem.attach(MIMEText(corpo, "html"))

    with open("static/img/medstock_logo_sf.png", "rb") as imagem:
        img = MIMEImage(imagem.read())
        img.add_header("Content-ID", "<logo_medstock>")
        mensagem.attach(img)

    servidor = smtplib.SMTP("smtp.gmail.com", 587) #"smtp.gmail.com" = servidor do Gmail - 587 = porta SMTP

    servidor.starttls()
    servidor.login(email_remetente, senha_app)
    servidor.send_message(mensagem)
    servidor.quit()
# -------------------------------------- ESQUECI A SENHA FIM ------------------------------------------

#! -------------------------------------- PRODUTO ------------------------------------------
# GET FORM TELA CADASTRO DE PRODUTO ===========
def get_produto_form_cadastro():
    return {
        "nome": request.form.get("nome", "").strip(),
        "quantidade_estoque": to_int(request.form.get("quantidade_estoque")),
        "categoria": request.form.get("categoria", "").strip(),
        "estoque_minimo": to_int(request.form.get("estoque_minimo")),
        "preco_custo": to_float(request.form.get("preco_custo")),
        "preco_venda": to_float(request.form.get("preco_venda")),   
    }
# ===============================


# POST SALVAR PRODUTO =======================
@app.route("/produto/salvar", methods=["POST"])
def salvar_produto():
    dados = get_produto_form_cadastro()
    produto = Produto(**dados)
    erros = produto.validate()

    if erros:
        for erro in erros:
            flash(erro[0], "danger")
        return render_template("formulario_produto.html", produto=dados)

    try:
        produto.insert()
        flash("Produto cadastrado com sucesso.", "success")
        return redirect(url_for("tela_produtos"))
    except Exception as e:
        # Verifica se o erro é de entrada duplicada (código 1062 do MySQL)
        if "1062" in str(e):
            flash("Produto já cadastrado.", "danger")
        else:
            flash(f"Erro ao cadastrar produto: {e}", "danger")
        return render_template("tela_cadastro_produto.html", produto=dados)
# ================================================

# POST ATUALIZAR PRODUTO ======================
@app.route("/produto/atualizar/<int:id>", methods=["POST"])
def atualizar_produto(id):
    dados = get_produto_form_cadastro()
    produto = Produto(**dados)
    erros = produto.validate()

    if erros:
        for erro in erros:
            flash(erro[0], "erro")
        dados["id"] = id
        return render_template("tela_produtos.html", produto=dados) 

    try:
        if not Produto.seleciona_por_id(id):
            flash("Produto não encontrado.", "erro")
            return redirect(url_for("tela_produtos"))

        produto.atualizar(id)
        flash("Produto atualizado com sucesso.", "success")
        return redirect(url_for("tela_produtos"))
    except Exception as e:
        dados["id"] = id
        flash(f"Erro ao atualizar produto: {e}", "danger")
        return render_template("tela_cadastro_produto.html", produto=dados)
# =========================================

# PUT EDITAR PRODUTO ==================
@app.route("/produto/editar/<int:id>")
def editar_produto(id):
    produto = Produto.seleciona_por_id(id)
    if not produto:
        flash("Produto não encontrado.", "danger")
        return redirect(url_for("tela_produtos"))
    return render_template("tela_cadastro_produto.html", produto=produto)
# ==============================

# DELETAR PRODUTO ==================
@app.route("/produto/excluir/<int:id>")
def excluir_produto(id):
    try:
        Produto.deletar_produto(id)
        flash("Produto excluído com sucesso.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    except Exception as e:
        flash(f"Erro ao excluir produto: {e}", "danger")
    return redirect(url_for("tela_produtos"))   
# ====================================
# -------------------------------------- PRODUTO FIM ------------------------------------------

#! -------------------------------------- PEDIDOS ------------------------------------------
# GET FORM TELA CADASTRO DE PEDIDOS ===========
def get_pedido_form():
    return {
        "produto_id": request.form.get("produto_id"),
        "data_pedido": request.form.get("data_pedido"),
        "valor_total": request.form.get("valor_total"),
        "observacao": request.form.get("observacao", "").strip(),
        "data_processamento": request.form.get("data_processamento"),
        "fornecedor_id": request.form.get("fornecedor_id")
    }

@app.route("/pedido/novo/<tipo>/<int:id>")
def novo_pedido(tipo, id):
    produto = Produto.seleciona_por_id(id)
    tipo = tipo.upper()

    if not produto:
        flash("Produto não encontrado.", "danger")
        return redirect(url_for("tela_produtos"))
    
    if tipo not in ["ENTRADA", "SAIDA"]:
        flash("Tipo de pedido inválido.", "erro")
        return redirect(url_for("tela_produtos"))

    return render_template("tela_cadastro_pedidos.html", produto=produto, tipo=tipo, pedido=None)


@app.route("/pedido/salvar/<int:produto_id>", methods=["POST"])
def salvar_pedido():
    dados = get_pedido_form()
    produto = Produto.seleciona_por_id(dados["produto_id"])
    entrada = PedidoEntrada(**dados)
    erros = entrada.validate()

    if not produto:
        flash("Produto não encontrado.", "erro")
        return redirect(url_for("tela_produtos"))

    if erros:
        for erro in erros:
            flash(erro, "erro")
        return render_template("tela_cadastro_pedidos.html", pedido=dados)
    
    try:
        entrada.insert()
        flash("Pedido criado com sucesso.", "success")
        return redirect(url_for("tela_entrada"))
    except Exception as e:
        flash(f"Erro ao criar pedido: {e}", "danger")
        return render_template("tela_cadastro_pedidos.html", produto=produto, tipo=dados["tipo"], pedido=dados)


@app.route("/pedido/processar/<int:id>")
def processar_pedido(id):
    try:
        mensagem = PedidoMovimentacao.processar(id)
        flash(mensagem, "sucesso")
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao processar pedido: {e}", "erro")
    return redirect(url_for("pedidos"))


@app.route("/pedido/cancelar/<int:id>")
def cancelar_pedido(id):
    try:
        mensagem = PedidoMovimentacao.cancelar(id)
        flash(mensagem, "sucesso")
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao cancelar pedido: {e}", "erro")
    return redirect(url_for("pedidos"))

#! = Feito pela -- Ana Beatriz // linha 1 a 417

'''usuarios = []
perfil = ["cliente", "fornercedor"]


# Fornecedores

fornecedor = []

@app.route("/fornecedor", methods=["POST"])
def cadastrar_fornecedor():
    dados = request.get_json()
    resposta = insert_fornecedor(dados)
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400


@app.route("/fornecedor/<int:idfornecedor>", methods=["GET"])
def listar_fornecedor(idfornecedor):
    resposta = read_fornecedor(idfornecedor)
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400


@app.route("/fornecedor/atualizar/<int:idfornecedor>", methods=["PUT"])
def atualizar_fornecedor(idfornecedor):
    dados = request.json
    dados['idfornecedor'] = idfornecedor
    resposta = update_fornecedor(dados)
    return jsonify(resposta), 200 if resposta.get('status') == 'sucesso' else 400

@app.route("/fornecedor/delete/<int:idfornecedor>", methods=["DELETE"])
def deletar_fornecedor(idfornecedor):
    resposta = delete_fornecedor(idfornecedor)
    return jsonify(resposta)

@app.route("/fornecedor/<int:indice>/pagto", methods=["GET"])
def listar_pagto(indice):
    if indice < len(fornecedor):
        return jsonify(fornecedor[indice].get("pagamento", {}))
    return jsonify({"erro": "Pagamento não encontrado"})


# Pagamentos

pagamento = []

@app.route("/pagamento", methods=["POST"])
def adicionar_pagamento():
    novo_pagamento = request.get_json()
    pagamentos = {
        "forma de pagamento": novo_pagamento["forma de pagamento"],
        "valor a ser pago": novo_pagamento["valor a ser pago"]
    }
    pagamento.append(pagamentos)
    return jsonify({"mensagem": "Pagamento adicionado com sucesso!"}), 201

@app.route("/pagamento", methods=["GET"])
def listar_pagamento():
    return jsonify(pagamento)

@app.route("/pagamento/<int:indice>", methods=["GET"])
def buscar_pagamento(indice):
    if indice < len(pagamento):
        return jsonify(pagamento[indice])
    return jsonify({"erro": "Pagamento não encontrado"}), 404

@app.route("/pagamento/<int:indice>", methods=["PUT"])
def atualizar_pagamento(indice):
    if indice < len(pagamento):
        dados = request.get_json()
        pagamento[indice].update(dados)
        return jsonify({"mensagem": "Pagamento atualizado com sucesso!"})
    return jsonify({"erro": "Pagamento não encontrado"}), 404

@app.route("/pagamento/<int:indice>", methods=["DELETE"])
def deletar_pagamento(indice):
    if indice < len(pagamento):
        pagamento.pop(indice)
        return jsonify({"mensagem": "Pagamento removido com sucesso!"})
    return jsonify({"erro": "Pagamento não encontrado"})



# Compras (entrada do fornecedor)

entrada = []

@app.route("/comprafornecedor", methods=["POST"])
def adicionar_entrada():
    nova_entrada = request.get_json()
    entradas = {
        "nome": nova_entrada["nome"],
        "quantidade": nova_entrada["quantidade"],
        "cnpj": nova_entrada["cnpj"]
    }
    
    res_nome = validar_nome_fornecedor(nova_entrada["nome"])
    res_quant = validar_quant_fornecedor(nova_entrada["quantidade"])
    res_cnpj = validar_cnpj(nova_entrada["cnpj"])

    
    entrada.append({"nome": res_nome, "quantidade": res_quant, "cnpj": res_cnpj})


    return jsonify({"nome": res_nome, "quantidade": res_quant}), 201

@app.route("/comprafornecedor", methods=["GET"])
def listar_entradas():
    return jsonify(entrada)

@app.route("/comprafornecedor/<int:indice>", methods=["GET"])
def buscar_entrada(indice):
    if indice < len(entrada):
        return jsonify(entrada[indice])
    return jsonify({"erro": "Entrada não encontrada"}), 404

@app.route("/comprafornecedor/<int:indice>", methods=["PUT"])
def atualizar_entrada(indice):
    if indice < len(entrada):
        dados = request.get_json()
        entrada[indice].update(dados)
        return jsonify({"mensagem": "Entrada atualizada com sucesso!"})
    return jsonify({"erro": "Entrada não encontrada"}), 404

@app.route("/comprafornecedor/<int:indice>", methods=["DELETE"])
def deletar_entrada(indice):
    if indice < len(entrada):
        entrada.pop(indice)
        return jsonify({"mensagem": "Entrada removida com sucesso!"})
    return jsonify({"erro": "Entrada não encontrada"}), 404


# Saídas (vendas)

saidas = []

@app.route("/saida", methods=["POST"])
def registrar_saida():
    nova_saida = request.get_json()
    saida = {
        "cliente": nova_saida.get("cliente"),
        "produtos": nova_saida.get("produtos", []),
        "pagamento": nova_saida.get("pagamento", {}),
        "valor_total": nova_saida.get("valor_total", 0.0)
    }
    saidas.append(saida)
    return jsonify({"mensagem": "Saída registrada com sucesso!"})

@app.route("/saida", methods=["GET"])
def listar_saidas():
    return jsonify(saidas)

@app.route("/saida/<int:indice>", methods=["PUT"])
def atualizar_saida(indice):
    if indice < len(saidas):
        dados = request.get_json()
        saidas[indice].update(dados)
        return jsonify({"mensagem": "Saída atualizada com sucesso!"})
    return jsonify({"erro": "Saída não encontrada"})

@app.route("/saida/<int:indice>", methods=["DELETE"])
def excluir_saida(indice):
    if indice < len(saidas):
        saidas.pop(indice)
        return jsonify({"mensagem": "Saída excluída com sucesso!"})
    return jsonify({"erro": "Saída não encontrada"})

@app.route("/saida/<int:indice>/produtos", methods=["GET"])
def get_produtos_saida(indice):
    if indice < len(saidas):
        return jsonify(saidas[indice].get("produtos", []))
    return jsonify({"erro": "Saída não encontrada"})

@app.route("/saida/<int:indice>/cliente", methods=["GET"])
def get_cliente_saida(indice):
    if indice < len(saidas):
        return jsonify(saidas[indice].get("cliente", {}))
    return jsonify({"erro": "Saída não encontrada"})

@app.route("/saida/<int:indice>/pagto", methods=["GET"])
def get_pagto_saida(indice):
    if indice < len(saidas):
        return jsonify(saidas[indice].get("pagamento", {}))
    return jsonify({"erro": "Saída não encontrada"})


# Movimentação de estoque

item = []

@app.route("/movimentacao", methods=["GET"])
def listar_item():
    return jsonify(item)

@app.route("/movimentacao", methods=["POST"])
def adicionar_item():
    novo_item = request.get_json()
    itens = {
        "nome": novo_item["nome"],
        "codigo": novo_item["codigo"],
        "quantidade": novo_item["quantidade"],
        "compra": novo_item["compra"],
        "venda": novo_item["venda"],
        "nome_entrada": novo_item["nome_entrada"],
        "quantidade_entrada": novo_item["quantidade_entrada"],
        "data_entrada": novo_item["data_entrada"],
        "fornecedor_e": novo_item["fornecedor_e"],
        "nome_saida": novo_item["nome_saida"],
        "quantidade_saida": novo_item["quantidade_saida"],
        "data_saida": novo_item["data_saida"],
        "fornecedor_s": novo_item["fornecedor_s"]
    }
    item.append(itens)
    return jsonify({"mensagem": "Item adicionado com sucesso!"})

@app.route("/movimentacao/<int:indice>", methods=["PUT"])
def atualizar_item(indice):
    if indice < len(item):
        dados = request.get_json()
        item[indice].update(dados)
        return jsonify({"mensagem": "Item atualizado com sucesso!"})
    return jsonify({"erro": "Item não encontrado"})

@app.route("/movimentacao/<int:indice>", methods=["DELETE"])
def deletar_item(indice):
    if indice < len(item):
        item.pop(indice)
        return jsonify({"mensagem": "Item deletado com sucesso!"})
    return jsonify({"erro": "Item não encontrado"})

@app.route("/movimentacao/produto/<int:indice>", methods=["GET"])
def consultar_item(indice):
    if indice < len(item):
        resultado = {"nome": item[indice]["nome"], "quantidade": item[indice]["quantidade"]}
        return jsonify(resultado)
    return jsonify({"erro": "Movimentação do item não encontrada"})

@app.route("/movimentacao/pedido/<int:indice>", methods=["GET"])
def visualizar_item(indice):
    if indice < len(item):
        resultado = {"compra": item[indice]["compra"], "venda": item[indice]["venda"]}
        return jsonify(resultado)
    return jsonify({"erro": "Pedido do item não encontrado"})

@app.route("/movimentacao/entrada/<int:indice>", methods=["GET"])
def registrar_entrada_item(indice):
    if indice < len(item):
        resultado = {
            "nome_entrada": item[indice]["nome_entrada"],
            "quantidade_entrada": item[indice]["quantidade_entrada"],
            "data_entrada": item[indice]["data_entrada"],
            "fornecedor_e": item[indice]["fornecedor_e"]
        }
        return jsonify(resultado)
    return jsonify({"erro": "Movimentação de entrada não encontrada"})

@app.route("/movimentacao/saida/<int:indice>", methods=["GET"])
def registrar_saida_item(indice):
    if indice < len(item):
        resultado = {
            "nome_saida": item[indice]["nome_saida"],
            "quantidade_saida": item[indice]["quantidade_saida"],
            "data_saida": item[indice]["data_saida"],
            "fornecedor_s": item[indice]["fornecedor_s"]
        }
        return jsonify(resultado)
    return jsonify({"erro": "Movimentação de saída não encontrada"})

# ITEM PEDIDO FORNECEDOR
item_pedido_fornecedor = []
@app.route("/item_pedido_fornecedor", methods=["POST"])
def adicionar_item_pfornecedor():
    dados = request.get_json()
    resposta = insert_item_pfornecedor(dados)
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

@app.route("/fornecedor/atualizar/<int:iditempedidofornecedor>", methods=["PUT"])
def atualizar_iditempedidofornecedor(iditempedidofornecedor):
    dados = request.json
    dados['iditempedidofornecedor'] = iditempedidofornecedor
    resposta = update_iditempedidofornecedor(dados)
    return jsonify(resposta), 200 if resposta.get('status') == 'sucesso' else 400

    
@app.route("/item_pedido_fornecedor/<int:indice>", methods=["GET"]) #quantidade INT NOT NULL, valor_unitario  pedido_cliente_idpedido_cliente  produto_idproduto  movimentacao_idmovimentacao,
def ler_item_pfornecedor(indice):
    if indice < len(item_pedido_fornecedor):
        return jsonify(item_pedido_fornecedor[indice])
    return jsonify({"erro": "Item pedido não encontrado"}), 404

@app.route("/item_pedido_fornecedor/delete/<int:indice>", methods=["DELETE"])
def deletar_item_pedidofor(indice):
    if indice < len(item_pedido_fornecedor):
        item_pedido_fornecedor.pop(indice)
        return jsonify({"mensagem": "Item removido com sucesso!"}), 201
    return jsonify({"erro": "Item não encontrado"}), 404

#===============================#

@app.route("/fornecedor/<int:idfornecedor>", methods=["GET"])
def listar_item_fornecedor(idfornecedor):
    resposta = read_fornecedor(idfornecedor)
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400


@app.route("/fornecedor/atualizar/<int:idfornecedor>", methods=["PUT"])
def atualizar_item_fornecedor(idfornecedor):
    dados = request.json
    dados['idfornecedor'] = idfornecedor
    resposta = update_fornecedor(dados)
    return jsonify(resposta), 200 if resposta.get('status') == 'sucesso' else 400

@app.route("/fornecedor/delete/<int:idfornecedor>", methods=["DELETE"])
def deletar_item_fornecedor(idfornecedor):
    resposta = delete_fornecedor(idfornecedor)
    return jsonify(resposta)

@app.route("/fornecedor/<int:indice>/pagto", methods=["GET"])
def listar_item_pagto(indice):
    if indice < len(fornecedor):
        return jsonify(fornecedor[indice].get("pagamento", {}))
    return jsonify({"erro": "Pagamento não encontrado"})

# ITEM PEDIDO CLIENTE
item_pedido_cliente = []
@app.route("/item_pedido_cliente", methods=["POST"])
def adicionar_item_pcliente():
    n = request.get_json()
    produtos.append(novo_produto)
    return jsonify({"mensagem": "Produto adicionado com sucesso"}), 201

@app.route("/item_pedido_cliente/<int:indice>", methods=["GET"]) #quantidade INT NOT NULL, valor_unitario  pedido_cliente_idpedido_cliente  produto_idproduto  movimentacao_idmovimentacao,
def ler_item_pcliente(indice):
    if indice < len(item_pedido_cliente):
        return jsonify(item_pedido_cliente[indice])
    return jsonify({"erro": "Item pedido não encontrado"}), 404

@app.route("/item_pedido_cliente/delete/<int:indice>", methods=["DELETE"])
def deletar_item_pedidocli(indice):
    if indice < len(item_pedido_cliente):
        item_pedido_cliente.pop(indice)
        return jsonify({"mensagem": "Item removido com sucesso!"}), 201
    return jsonify({"erro": "Item não encontrado"}), 404
'''
if __name__ == "__main__":
    app.run(debug=True)