# Importações FLASK =========
from flask import Flask, jsonify, request, url_for, render_template, redirect, flash, session
#============================

# Importações CLASSES =======
from models.cliente import Cliente
from models.produto import Produto
from models.entrada import PedidoEntrada
from models.fornecedor import Fornecedor
from models.cliente_cadastro import ClientesCadastro
#============================

# Importações E-MAIL ========
from email.mime.text import MIMEText # Texto no email
from email.mime.image import MIMEImage # Imagem no email
from email.mime.multipart import MIMEMultipart
import smtplib #Simple Mail Transfer Protocol - protocolo para enviar e-mail pela internet
#============================

# OUTRAS Importações ========
import random
from datetime import datetime
#============================

app = Flask(__name__)
app.secret_key = "Medstock_programa_de_estoque_123456"

#! = Feito pela -- Ana Beatriz // linha 1 a 526 𖹭.ᐟ

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

# TELA INICIAL ===============
@app.route("/inicial")
def tela_inicial():
    cliente_id = session.get("cliente_id")
    return render_template("tela_inicial.html", cliente = Cliente.seleciona_por_id(cliente_id)) 
#==============================================

# TELA HISTORICO DE FORNECEDOR ===============
@app.route("/historico/fornecedor")
def tela_historico_de_fornecedor():
    cliente_id = session.get("cliente_id")
    return render_template("tela_historico_de_fornecedor.html", fornecedor = Fornecedor.seleciona_tudo(order_by="nome_fornecedor"), cliente = Cliente.seleciona_por_id(cliente_id)) 
#==============================================

# TELA HISTORICO DE CLIENTE ===============
@app.route("/historico/cliente")
def tela_historico_de_cliente():
    cliente_id = session.get("cliente_id")
    return render_template("tela_historico_de_cliente.html", clientes = ClientesCadastro.seleciona_tudo(order_by="nome"), cliente = Cliente.seleciona_por_id(cliente_id)) 
#==============================================

# TELA CADASTRO DE FORNECEDOR ===============
@app.route("/cadastro/fornecedor")
def tela_cadastro_de_fornecedor():
    cliente_id = session.get("cliente_id")
    return render_template("tela_cadastro_de_fornecedor.html", cliente = Cliente.seleciona_por_id(cliente_id)) 
#==============================================

# TELA CLIENTES CADASTRO ===============
@app.route("/cadastro/clientescadastro")
def tela_clientes_cadastro():
    cliente_id = session.get("cliente_id")
    return render_template("tela_clientes_cadastro.html", cliente = Cliente.seleciona_por_id(cliente_id)) 
#==============================================

# TELA CADASTRO PRODUTO==============
@app.route("/cadastro/produto")
def tela_cadastro_produto():
    cliente_id = session.get("cliente_id")
    return render_template("tela_cadastro_produto.html", fornecedores = Fornecedor.seleciona_tudo(order_by="nome_fornecedor") , cliente = Cliente.seleciona_por_id(cliente_id), produto = None)
#==============================================

# TELA PRODUTO==============
@app.route("/produto")
def tela_produtos():
    cliente_id = session.get("cliente_id")
    produtos = Produto.seleciona_tudo(order_by="nome")
    for produto in produtos:
        produto["fornecedor"] = Fornecedor.seleciona_por_id(produto["fornecedor_id"])


    return render_template("tela_produtos.html", produtos=produtos, cliente = Cliente.seleciona_por_id(cliente_id))
#==============================================

# TELA ENTRADA==============
@app.route("/pedido/entrada")
def tela_entrada():
    cliente_id = session.get("cliente_id")
    #teste = PedidoEntrada.historico_entrada()
    #print("teste entradas", teste)
    return render_template("tela_entrada.html", entradas=PedidoEntrada.historico_entrada(), cliente = Cliente.seleciona_por_id(cliente_id))
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
    return redirect(url_for("tela_login"))
# ====================================

# Faz LOGIN CLIENTE ===============
@app.route("/cliente/login", methods=['POST'])
def fazer_login():
    email = request.form.get("email")
    senha = request.form.get("senha")

    cliente = Cliente.seleciona_por_email(email)

    if cliente and cliente["senha"] == senha:
        session["cliente_id"] = cliente["id"]
        flash("Login realizado com sucesso!", "success")
        return redirect(url_for("tela_inicial"))
    else:
        flash("Email ou senha inválidos!", "danger")
        return render_template("tela_login.html")

# -------------------------------------- CLIENTE FIM ------------------------------------------

# -------------------------------------- FORNECEDOR ------------------------------------------
#! GET FORM TELA DE CADASTRO FORNECEDOR ===============
def get_fornecedor_form_cadastro():
    return {
        "nome_fornecedor": request.form.get("nome_fornecedor").strip(),
        "cnpj": request.form.get("cnpj").strip(),
        "email": request.form.get("email").strip(),
    }
#==============================================

# POST SALVA FORNECEDOR ===============
@app.route("/fornecedor/salvar", methods=["POST"])
def salvar_fornecedor():
    dados = get_fornecedor_form_cadastro()
    fornecedor = Fornecedor(**dados)
    erros = fornecedor.validate()

    if erros:
        flash(erros[0], "danger")
        return render_template("tela_cadastro_de_fornecedor.html", fornecedor=dados) 

    try:
        fornecedor.insert()
        flash("Fornecedor cadastrado com sucesso.", "success")
        return redirect(url_for("tela_historico_de_fornecedor")) 
    except Exception as e:
            # Verifica se o erro é de entrada duplicada (código 1062 do MySQL)
        if "1062" in str(e):
            flash("CNPJ ou E-MAIL já cadastrado no sistema.", "danger")
        else:
            flash(f"Erro ao cadastrar Fornecedor: {e}", "danger")
        return render_template("tela_cadastro_de_fornecedor.html", fornecedor=dados) 
#==============================================

#! POST ATUALIZAR FORNECEDOR ======================
'''@app.route("/cliente/atualizar/<int:id>", methods=["POST"])
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
# ========================================='''

# DELETAR FORNECEDOR ==================
@app.route("/fornecedor/excluir/<int:id>")
def excluir_fornecedor(id):
    try:
        Fornecedor.deletar_fornecedor(id)
        flash("Fornecedor excluído com sucesso.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    except Exception as e:
        flash(f"Erro ao excluir Fornecedor: {e}", "danger")
    return redirect(url_for("tela_historico_de_fornecedor")) 
# ====================================

# -------------------------------------- FORNECEDOR FIM ------------------------------------------

# -------------------------------------- CLIENTE CADASTRO ------------------------------------------
#! GET FORM TELA DE CLIENTE CADASTRO ===============
def get_form_cliente_cadastro():
    return {
        "nome": request.form.get("nome").strip(),
        "cpf": request.form.get("cpf").strip(),
        "telefone": request.form.get("telefone").strip(),
        "cidade": request.form.get("cidade").strip(),
        "estado": request.form.get("estado").strip(),
        "cep": request.form.get("cep").strip(),
    }
#==============================================

#! POST SALVA CLIENTE CADASTRO ===============
@app.route("/clientescadastro/salvar", methods=["POST"])
def salvar_clientes_cadastro():
    dados = get_form_cliente_cadastro()
    clientes = ClientesCadastro(**dados)
    erros = clientes.validate()

    cliente_id = session.get("cliente_id")

    if erros:
        flash(erros[0], "danger")
        return render_template("tela_clientes_cadastro.html", clientes=dados, cliente = Cliente.seleciona_por_id(cliente_id)) #!

    try:
        clientes.insert()
        flash("Cliente cadastrado com sucesso!", "success")
        return redirect(url_for("tela_historico_de_cliente")) 
    except Exception as e:
            # Verifica se o erro é de entrada duplicada (código 1062 do MySQL)
        if "1062" in str(e):
            flash("CPF já cadastrado no sistema.", "danger")
        else:
            flash(f"Erro ao cadastrar Cliente: {e}", "danger")
        return render_template("tela_clientes_cadastro.html", clientes=dados, cliente = Cliente.seleciona_por_id(cliente_id)) 
#==============================================

#! POST ATUALIZAR FORNECEDOR ======================
'''@app.route("/cliente/atualizar/<int:id>", methods=["POST"])
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
# ========================================='''

# DELETAR FORNECEDOR ==================
@app.route("/clientescadastro/excluir/<int:id>")
def excluir_clientes_cadastro(id):
    try:
        ClientesCadastro.deletar_clientes_cadastro(id)
        flash("Cliente excluído com sucesso!", "danger")
    except ValueError as e:
        flash(str(e), "danger")
    except Exception as e:
        flash(f"Erro ao excluir Cliente: {e}", "danger")
    return redirect(url_for("tela_historico_de_cliente")) 
# ====================================

# -------------------------------------- CLIENTES CADASTRO FIM ------------------------------------------

#! -------------------------------------- ESQUECI A SENHA ------------------------------------------
#  Esqueci a senha ROTA===============
@app.route("/esqueci_a_senha", methods=["GET", "POST"])
def tela_esqueci_a_senha():
    if request.method == "POST":
        email = request.form.get("email")
        codigo = random.randint(100000, 999999)
        session["codigo_recuperacao"] = str(codigo)
        enviar_codigo_email(email, codigo)
        return redirect(url_for("verificar_codigo"))

    return render_template("tela_esqueci_a_senha.html")

# Verificar código ROTA=================
@app.route("/verificar_codigo", methods=["GET", "POST"])
def verificar_codigo():

    if request.method == "POST":
        codigo_digitado = request.form.get("codigo")
        codigo_salvo = session.get("codigo_recuperacao")
        if codigo_digitado == codigo_salvo:
            return "Código correto"
        else:
            return "Código inválido"
    return render_template("tela_verificar_codigo.html")

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
        "fornecedor_id": to_int(request.form.get("fornecedor_id", 1)),
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
    cliente_id = session.get("cliente_id")
    if not produto:
        flash("Produto não encontrado.", "danger")
        return redirect(url_for("tela_produtos"))
    return render_template("tela_cadastro_produto.html", cliente = Cliente.seleciona_por_id(cliente_id), produto=produto)
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
    data_campo = request.form.get("data_pedido")
    
    # Se o campo for vazio ou não selecionado gera a data/hora atual formatada para o MySQL
    if not data_campo or data_campo.strip() == "":
        data_pedido = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        data_pedido = data_campo
    return {
        #"produto_id": request.form.get("produto_id"),
        "data_pedido": data_pedido,
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

    pedido_padrao = {
        "data_pedido": datetime.now().strftime("%Y-%m-%dT%H:%M") # Formato correto para input do tipo datetime-local
    }

    return render_template("tela_cadastro_pedidos.html", produto=produto, tipo=tipo, pedido=pedido_padrao)

@app.route("/pedido/salvar/<int:produto_id>", methods=["POST"])
def salvar_pedido(produto_id):
    dados = get_pedido_form()
    #print("pedido", dados)
    produto = Produto() #Produto.seleciona_por_id(produto_id)
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
        dados["id"] = produto_id
        produto.upd_quantidade(produto_id, dados["quantidade"])
        flash("Pedido criado com sucesso.", "success")
        return redirect(url_for("tela_entrada"))
    except Exception as e:
        flash(f"Erro ao criar pedido: {e}", "danger")
        return render_template("tela_cadastro_pedidos.html")

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

#! = Feito pela -- Ana Beatriz // linha 1 a 642 𖹭.ᐟ

if __name__ == "__main__":
    app.run(debug=True)