	-- Schema Medstock_db
	-- -----------------------------------------------------
	CREATE SCHEMA IF NOT EXISTS Medstock_db DEFAULT CHARACTER SET utf8 ;
	SHOW WARNINGS;
	USE Medstock_db ;

	-- ================= CLIENTE =================
	CREATE TABLE IF NOT EXISTS cliente (
	  id INT NOT NULL AUTO_INCREMENT,
	  nome VARCHAR(100) NOT NULL,
	  email VARCHAR(45) NOT NULL,
	  cpf CHAR(11) NOT NULL,
	  senha varchar(45) NOT NULL,
	  PRIMARY KEY (id),
	  UNIQUE (email),
	  UNIQUE (cpf)
	) ENGINE = InnoDB;

	-- ================= CLIENTE CADASTRADOS =================
	CREATE TABLE IF NOT EXISTS clientes_cadastro (
	 id INT NOT NULL AUTO_INCREMENT,
	 nome VARCHAR(100) NOT NULL,
	 cpf CHAR(11) UNIQUE,
	 telefone VARCHAR(20),
	 cidade VARCHAR(50),
	 estado CHAR(2),
	 cep CHAR(8),
	 PRIMARY KEY (id)
	) ENGINE=InnoDB;

	-- ================= PRODUTO =================
	CREATE TABLE IF NOT EXISTS produto (
	  id INT NOT NULL AUTO_INCREMENT,
	  fornecedor_id INT NOT NULL,
	  nome VARCHAR(100) NOT NULL,
	  quantidade_estoque INT NOT NULL DEFAULT 0,
	  categoria VARCHAR(100) NOT NULL,
	  estoque_minimo INT NOT NULL DEFAULT 0,
	  preco_custo DECIMAL(10,2) NOT NULL DEFAULT 0,
	  preco_venda DECIMAL(10,2) NOT NULL DEFAULT 0,
	  PRIMARY KEY (id),
	  CONSTRAINT fk_produto_fornecedor FOREIGN KEY (fornecedor_id) REFERENCES fornecedor (id)
	) ENGINE = InnoDB;


	-- ================= FORNECEDOR =================
	CREATE TABLE IF NOT EXISTS fornecedor (
	  id INT NOT NULL AUTO_INCREMENT,
	  nome_fornecedor VARCHAR(100) NOT NULL,
	  cnpj CHAR(14) NOT NULL,
	  email VARCHAR(50) NOT NULL,
	  PRIMARY KEY (id)
	) ENGINE = InnoDB;

	-- ================= MOVIMENTACAO =================
	CREATE TABLE IF NOT EXISTS movimentacao (
	  id INT NOT NULL AUTO_INCREMENT,
	  quantidade INT NULL,
	  data_mov DATETIME NULL,
	  idorigem INT NOT NULL,
	  tipo varchar(20) NOT Null,
	  produto_id INT NOT NULL,
	  PRIMARY KEY (id),
	  FOREIGN KEY (produto_id) REFERENCES produto (id)
	) ENGINE = InnoDB;


	-- ================= PEDIDO FORNECEDOR =================
	CREATE TABLE IF NOT EXISTS entrada (
	  id INT NOT NULL AUTO_INCREMENT,
	  data_pedido DATETIME NULL,
	  valor_total DECIMAL(10,2) NOT NULL,
	  observacao VARCHAR(255),
	  data_processamento DATETIME NULL,
	  fornecedor_id INT NOT NULL,
	  PRIMARY KEY (id),
	  FOREIGN KEY (fornecedor_id) REFERENCES fornecedor (id)
	) ENGINE = InnoDB;

	-- ================= ITEM PEDIDO FORNECEDOR =================
	CREATE TABLE IF NOT EXISTS item_pedido_fornecedor (
	  id INT NOT NULL AUTO_INCREMENT,
	  quantidade INT NULL,
	  valor_unitario DECIMAL(10,2) NULL,
	  entrada_id INT NOT NULL,
	  produto_id INT NOT NULL,
	  PRIMARY KEY (id),
	  FOREIGN KEY (entrada_id) REFERENCES entrada (id),
	  FOREIGN KEY (produto_id) REFERENCES produto (id)
	) ENGINE = InnoDB;

	-- ================= PEDIDO CLIENTE =================
	CREATE TABLE IF NOT EXISTS saida (
	  id INT NOT NULL AUTO_INCREMENT,
	  data_pedido DATETIME NOT NULL,
	  tipo VARCHAR(10) NOT NULL,
	  quantidade INT NOT NULL,
	  valor_total DECIMAL(10,2) NOT NULL,
	  observacao VARCHAR(255),
	  data_processamento DATETIME NULL,
	  cliente_id INT NOT NULL,
	  PRIMARY KEY (id),
	  FOREIGN KEY (cliente_id) REFERENCES cliente (id)
	) ENGINE = InnoDB;


	-- ================= ITEM PEDIDO CLIENTE =================
	CREATE TABLE IF NOT EXISTS item_pedido_cliente (
	  id INT NOT NULL AUTO_INCREMENT,
	  quantidade INT NULL,
	  valor_unitario DECIMAL(10,2) NULL,
	  saida_id INT NOT NULL,
	  produto_id INT NOT NULL,
	  PRIMARY KEY (id),
	  FOREIGN KEY (saida_id) REFERENCES saida (id),
	  FOREIGN KEY (produto_id) REFERENCES produto (id)
	) ENGINE = InnoDB;


	SHOW WARNINGS;

	select * from cliente;
	select * from produto;
	select * from entrada;
	select * from item_pedido_fornecedor;

	SET SQL_MODE=@OLD_SQL_MODE;
	SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
	SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;