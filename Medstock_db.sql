SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

CREATE SCHEMA IF NOT EXISTS Medstock_db DEFAULT CHARACTER SET utf8mb4;
USE Medstock_db;

-- ================= CLIENTE (usuários do sistema) =================
CREATE TABLE IF NOT EXISTS cliente (
  id INT NOT NULL AUTO_INCREMENT,
  nome VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL,
  cpf CHAR(11) NOT NULL,
  senha VARCHAR(250) NOT NULL,
  status VARCHAR(20) DEFAULT 'ativo',
  PRIMARY KEY (id),
  UNIQUE (email),
  UNIQUE (cpf)
) ENGINE = InnoDB;

-- ================= CLIENTES CADASTRADOS =================
CREATE TABLE IF NOT EXISTS clientes_cadastro (
  id INT NOT NULL AUTO_INCREMENT,
  nome VARCHAR(100) NOT NULL,
  cpf CHAR(11) UNIQUE,
  telefone VARCHAR(20),
  cidade VARCHAR(50),
  estado CHAR(2),
  cep CHAR(8),
  ativo BOOLEAN DEFAULT TRUE,
  PRIMARY KEY (id)
) ENGINE = InnoDB;

INSERT INTO clientes_cadastro (nome, cpf, telefone, cidade, estado, cep, ativo) VALUES
('João Carlos da Silva',     '52998224725', '(19)99876-1234', 'Itapira',      'SP', '13970000', TRUE),
('Maria Fernanda Souza',     '11144477735', '(19)99765-2345', 'Mogi Mirim',   'SP', '13800000', TRUE),
('Lucas Henrique Oliveira',  '12345678909', '(19)99654-3456', 'Itapira',      'SP', '13970120', TRUE),
('Ana Beatriz Costa',        '98765432100', '(19)99543-4567', 'Campinas',     'SP', '13010000', TRUE),
('Pedro Augusto Lima',       '16899535009', '(19)99432-5678', 'Jaguariúna',   'SP', '13820000', TRUE),
('Juliana Martins Rocha',    '39053344705', '(19)99321-6789', 'Amparo',       'SP', '13900000', TRUE),
('Ricardo Almeida Santos',   '71460238001', '(19)99210-7890', 'Mogi Guaçu',   'SP', '13840000', TRUE),
('Camila Pereira Gomes',     '15350946056', '(19)99123-8901', 'Estiva Gerbi', 'SP', '13857000', TRUE),
('Felipe Rodrigues Araújo',  '86288366757', '(19)99012-9012', 'Lindóia',      'SP', '13950000', TRUE),
('Patrícia Cristina Mendes', '29537914806', '(19)98901-0123', 'Serra Negra',  'SP', '13930000', TRUE);

-- ================= FORNECEDOR =================
CREATE TABLE IF NOT EXISTS fornecedor (
  id INT NOT NULL AUTO_INCREMENT,
  nome_fornecedor VARCHAR(100) NOT NULL,
  cnpj CHAR(14) NOT NULL,
  email VARCHAR(50) NOT NULL,
  ativo BOOLEAN DEFAULT TRUE,
  PRIMARY KEY (id),
  UNIQUE (cnpj)
) ENGINE = InnoDB;

INSERT INTO fornecedor (nome_fornecedor, cnpj, email, ativo) VALUES
('Cristália Produtos Químicos Farmacêuticos', '44734671000151', 'dac@cristalia.com.br', TRUE),
('Controll Pharma Comércio de Medicamentos', '11144448000103', 'contato@controllpharma.com.br', TRUE),
('M.G. Domingues Distribuidora de Medicamentos', '33735524000180', 'contato@mgdomingues.com.br', TRUE),
('Fontoveter Produtos Farmacêuticos e Cosméticos', '67310995000168', 'contato@fontoveter.com.br', TRUE),
('Gama Care Distribuidora', '12345678000101', 'contato@gamacare.com.br', TRUE),
('Horem Distribuidora Farmacêutica', '12345678000102', 'contato@horem.com.br', TRUE),
('Cadis Distribuidora Farmacêutica', '12345678000103', 'sac@grupocadis.com.br', TRUE),
('Quimion Distribuidora Farmacêutica', '12345678000104', 'contato@quimion.com.br', TRUE),
('SAMAPI Distribuidora Farmacêutica', '12345678000105', 'contato@samapi.com.br', TRUE),
('VenLife Distribuidora Farmacêutica', '12345678000106', 'contato@venlife.com.br', TRUE);

-- ================= PRODUTO =================
CREATE TABLE IF NOT EXISTS produto (
  id INT NOT NULL AUTO_INCREMENT,
  fornecedor_id INT NOT NULL,
  nome VARCHAR(100) NOT NULL,
  codigo_barras VARCHAR(14) NULL,
  marca VARCHAR(100) NULL,
  quantidade_estoque INT NOT NULL DEFAULT 0,
  categoria VARCHAR(100) NOT NULL,
  estoque_minimo INT NOT NULL DEFAULT 0,
  preco_custo DECIMAL(10,2) NOT NULL DEFAULT 0,
  preco_venda DECIMAL(10,2) NOT NULL DEFAULT 0,
  imagem VARCHAR(255) NULL,          -- nome do arquivo em static/uploads/produtos/ ou URL completa
  data_validade DATE NULL,
  tipo_medicamento ENUM('referencia','generico','similar','biologico','fitoterapico','outros') NOT NULL DEFAULT 'outros',
  tarja ENUM('preta','vermelha') NULL,                 -- NULL = isento
  tipo_receita ENUM('branca','azul','amarela') NULL,   -- NULL = não exige
  ativo BOOLEAN DEFAULT TRUE,
  PRIMARY KEY (id),
  UNIQUE KEY uq_produto_codigo_barras (codigo_barras),
  KEY idx_produto_categoria (categoria),
  KEY idx_produto_fornecedor (fornecedor_id),
  CONSTRAINT fk_produto_fornecedor FOREIGN KEY (fornecedor_id) REFERENCES fornecedor (id)
) ENGINE = InnoDB;

INSERT INTO produto
(fornecedor_id, nome, codigo_barras, marca, quantidade_estoque, categoria, estoque_minimo, preco_custo, preco_venda, imagem, data_validade, tipo_medicamento, tarja, tipo_receita, ativo)
VALUES
(1, 'Dipirona Sódica 500mg c/ 20 comprimidos', '7890000010009', 'EMS', 150, 'Analgésicos', 20, 3.50, 5.90, '01-dipirona-sodica-500mg.svg', '2028-03-31', 'generico', NULL, NULL, TRUE),
(2, 'Paracetamol 750mg c/ 20 comprimidos', '7890000010078', 'Neo Química', 180, 'Analgésicos', 20, 3.20, 5.90, '02-paracetamol-750mg.svg', '2028-01-31', 'generico', NULL, NULL, TRUE),
(3, 'Ibuprofeno 600mg c/ 10 comprimidos', '7890000010146', 'Medley', 120, 'Anti-inflamatórios', 15, 5.20, 8.90, '03-ibuprofeno-600mg.svg', '2027-11-30', 'generico', NULL, NULL, TRUE),
(4, 'Diclofenaco Sódico 50mg c/ 20 comprimidos', '7890000010214', 'Eurofarma', 110, 'Anti-inflamatórios', 15, 4.80, 7.90, '04-diclofenaco-sodico-50mg.svg', '2027-09-30', 'generico', NULL, NULL, TRUE),
(5, 'Amoxicilina 500mg c/ 21 cápsulas', '7890000010283', 'Eurofarma', 80, 'Antibióticos', 20, 12.50, 19.90, '05-amoxicilina-500mg.svg', '2027-06-30', 'generico', 'vermelha', 'branca', TRUE),
(6, 'Azitromicina 500mg c/ 3 comprimidos', '7890000010351', 'Medley', 70, 'Antibióticos', 10, 14.00, 22.90, '06-azitromicina-500mg.svg', '2027-04-30', 'generico', 'vermelha', 'branca', TRUE),
(7, 'Cefalexina 500mg c/ 8 cápsulas', '7890000010429', 'Teuto', 60, 'Antibióticos', 10, 11.00, 17.90, '07-cefalexina-500mg.svg', '2026-12-10', 'generico', 'vermelha', 'branca', TRUE),
(8, 'Loratadina 10mg c/ 12 comprimidos', '7890000010498', 'EMS', 100, 'Antialérgicos', 10, 4.80, 7.90, '08-loratadina-10mg.svg', '2028-02-29', 'generico', NULL, NULL, TRUE),
(9, 'Desloratadina 5mg c/ 10 comprimidos', '7890000010566', 'Germed', 70, 'Antialérgicos', 10, 7.50, 11.90, '09-desloratadina-5mg.svg', '2027-12-31', 'generico', NULL, NULL, TRUE),
(10, 'Fluconazol 150mg c/ 1 cápsula', '7890000010634', 'Neo Química', 60, 'Antifúngicos e Antivirais', 10, 5.90, 9.90, '10-fluconazol-150mg.svg', '2027-08-31', 'generico', NULL, NULL, TRUE),
(1, 'Aciclovir 200mg c/ 25 comprimidos', '7890000010702', 'Medley', 45, 'Antifúngicos e Antivirais', 8, 9.80, 15.90, '11-aciclovir-200mg.svg', '2027-05-31', 'generico', NULL, NULL, TRUE),
(2, 'Omeprazol 20mg c/ 28 cápsulas', '7890000010771', 'EMS', 140, 'Gastrointestinais', 20, 6.00, 9.90, '12-omeprazol-20mg.svg', '2027-10-31', 'generico', NULL, NULL, TRUE),
(3, 'Domperidona 10mg c/ 30 comprimidos', '7890000010849', 'Eurofarma', 12, 'Gastrointestinais', 15, 5.40, 8.90, '13-domperidona-10mg.svg', '2027-07-31', 'generico', NULL, NULL, TRUE),
(4, 'Sinvastatina 20mg c/ 30 comprimidos', '7890000010917', 'Medley', 90, 'Cardiovasculares', 15, 7.20, 11.90, '14-sinvastatina-20mg.svg', '2028-04-30', 'generico', NULL, NULL, TRUE),
(5, 'Ácido Acetilsalicílico 100mg c/ 30 comprimidos', '7890000010986', 'Neo Química', 100, 'Cardiovasculares', 15, 4.10, 6.90, '15-acido-acetilsalicilico-100mg.svg', '2027-07-31', 'generico', NULL, NULL, TRUE),
(6, 'Losartana Potássica 50mg c/ 30 comprimidos', '7890000011051', 'EMS', 130, 'Anti-hipertensivos', 20, 4.50, 7.90, '16-losartana-potassica-50mg.svg', '2028-05-31', 'generico', NULL, NULL, TRUE),
(7, 'Atenolol 50mg c/ 30 comprimidos', '7890000011129', 'Eurofarma', 95, 'Anti-hipertensivos', 15, 4.20, 6.90, '17-atenolol-50mg.svg', '2027-03-31', 'generico', NULL, NULL, TRUE),
(8, 'Anlodipino 5mg c/ 30 comprimidos', '7890000011198', 'Medley', 105, 'Anti-hipertensivos', 15, 3.90, 6.90, '18-anlodipino-5mg.svg', '2027-02-05', 'generico', NULL, NULL, TRUE),
(9, 'Metformina 850mg c/ 30 comprimidos', '7890000011266', 'EMS', 110, 'Antidiabéticos', 15, 5.50, 8.90, '19-metformina-850mg.svg', '2028-02-29', 'generico', NULL, NULL, TRUE),
(10, 'Glibenclamida 5mg c/ 30 comprimidos', '7890000011334', 'Germed', 50, 'Antidiabéticos', 10, 4.60, 7.90, '20-glibenclamida-5mg.svg', '2027-01-15', 'generico', NULL, NULL, TRUE),
(1, 'Salbutamol 100mcg/dose spray 200 doses', '7890000011402', 'Teuto', 45, 'Respiratórios', 8, 16.50, 26.90, '21-salbutamol-100mcg-dose.svg', '2027-09-30', 'generico', NULL, NULL, TRUE),
(2, 'Ambroxol 15mg/5ml xarope 120ml', '7890000011471', 'Neo Química', 60, 'Respiratórios', 10, 6.80, 10.90, '22-ambroxol-15mg-5ml.svg', '2027-05-31', 'generico', NULL, NULL, TRUE),
(3, 'Cetoconazol 2% creme 30g', '7890000011549', 'Eurofarma', 75, 'Dermatológicos', 10, 7.50, 11.90, '23-cetoconazol-2.svg', '2027-11-30', 'generico', NULL, NULL, TRUE),
(4, 'Prednisona 20mg c/ 10 comprimidos', '7890000011617', 'Medley', 60, 'Corticoides', 10, 6.20, 9.90, '24-prednisona-20mg.svg', '2027-08-31', 'generico', NULL, NULL, TRUE),
(5, 'Dexametasona 0,1% creme 10g', '7890000011686', 'EMS', 55, 'Corticoides', 8, 5.80, 9.90, '25-dexametasona-0-1.svg', '2026-11-28', 'generico', NULL, NULL, TRUE),
(6, 'Sertralina 50mg c/ 30 comprimidos', '7890000011754', 'Eurofarma', 70, 'Psiquiatria e Neurologia', 10, 9.50, 15.90, '26-sertralina-50mg.svg', '2027-10-31', 'generico', 'vermelha', 'branca', TRUE),
(7, 'Clonazepam 2mg c/ 30 comprimidos', '7890000011822', 'Medley', 40, 'Medicamentos Controlados', 8, 7.80, 12.90, '27-clonazepam-2mg.svg', '2027-06-30', 'generico', 'preta', 'azul', TRUE),
(8, 'Alprazolam 0,5mg c/ 30 comprimidos', '7890000011891', 'EMS', 5, 'Medicamentos Controlados', 8, 8.20, 13.90, '28-alprazolam-0-5mg.svg', '2027-04-30', 'generico', 'preta', 'azul', TRUE),
(9, 'Levotiroxina Sódica 50mcg c/ 30 comprimidos', '7890000011969', 'Eurofarma', 80, 'Endocrinologia', 10, 8.90, 14.90, '29-levotiroxina-sodica-50mcg.svg', '2028-01-31', 'generico', NULL, NULL, TRUE),
(10, 'Levonorgestrel 1,5mg c/ 1 comprimido', '7890000012034', 'Medley', 50, 'Ginecologia e Saúde da Mulher', 10, 7.90, 12.90, '30-levonorgestrel-1-5mg.svg', '2027-12-31', 'generico', NULL, NULL, TRUE),
(1, 'Cloridrato de Nafazolina 0,03% colírio 15ml', '7890000012102', 'EMS', 40, 'Oftalmológicos e Otológicos', 8, 6.40, 10.90, '31-cloridrato-de-nafazolina-0-03.svg', '2026-10-20', 'generico', NULL, NULL, TRUE),
(2, 'Vitamina C 1g c/ 10 efervescentes', '7890000012171', 'Neo Química', 90, 'Vitaminas e Suplementos', 10, 8.50, 13.90, '32-vitamina-c-1g.svg', '2028-03-31', 'generico', NULL, NULL, TRUE),
(3, 'Ácido Fólico 5mg c/ 30 comprimidos', '7890000012249', 'Teuto', 70, 'Vitaminas e Suplementos', 10, 4.20, 6.90, '33-acido-folico-5mg.svg', '2027-09-30', 'generico', NULL, NULL, TRUE),
(4, 'Paracetamol Gotas 200mg/ml frasco 15ml', '7890000012317', 'EMS', 85, 'Infantil e Bebês', 12, 4.90, 7.90, '34-paracetamol-gotas-200mg-ml.svg', '2027-07-31', 'generico', NULL, NULL, TRUE),
(5, 'Cloreto de Sódio 0,9% solução 500ml', '7890000012386', 'Eurofarma', 120, 'Materiais Hospitalares', 25, 3.80, 6.90, '35-cloreto-de-sodio-0-9.svg', '2028-06-30', 'generico', NULL, NULL, TRUE),
(6, 'Rivotril 2mg c/ 30 comprimidos', '7890000012454', 'Roche', 40, 'Medicamentos Controlados', 5, 18.00, 28.90, '36-rivotril-2mg.svg', '2027-06-30', 'referencia', 'preta', 'azul', TRUE),
(7, 'Aerolin 100mcg/dose spray 200 doses', '7890000012522', 'GSK', 60, 'Respiratórios', 10, 18.00, 28.90, '37-aerolin-100mcg-dose.svg', '2027-09-30', 'referencia', NULL, NULL, TRUE),
(8, 'Dorflex c/ 36 comprimidos', '7890000012591', 'Sanofi', 90, 'Analgésicos', 15, 14.50, 23.90, '38-dorflex.svg', '2027-12-31', 'referencia', NULL, NULL, TRUE),
(9, 'Vacina Influenza Tetravalente dose 0,5ml', '7890000012669', 'Sanofi Pasteur', 30, 'Vacinas', 5, 25.00, 39.90, '39-vacina-influenza-tetravalente.svg', '2027-01-30', 'biologico', NULL, NULL, TRUE),
(10, 'Vacina dT Adulto dose 0,5ml', '7890000012737', 'Butantan', 25, 'Vacinas', 5, 22.00, 35.90, '40-vacina-dt-adulto.svg', '2027-06-30', 'biologico', NULL, NULL, TRUE),
(1, 'Insulina Humana NPH 100UI/ml frasco 10ml', '7890000012805', 'Novo Nordisk', 20, 'Antidiabéticos', 5, 38.00, 60.90, '41-insulina-humana-nph-100ui-ml.svg', '2027-03-31', 'biologico', NULL, NULL, TRUE),
(2, 'Passiflora Incarnata 260mg c/ 20 cápsulas', '7890000012874', 'Herbarium', 45, 'Fitoterápicos', 8, 14.00, 22.90, '42-passiflora-incarnata-260mg.svg', '2027-10-31', 'fitoterapico', NULL, NULL, TRUE),
(3, 'Ginkgo Biloba 80mg c/ 30 comprimidos', '7890000012942', 'Herbarium', 40, 'Fitoterápicos', 8, 19.00, 30.90, '43-ginkgo-biloba-80mg.svg', '2027-08-31', 'fitoterapico', NULL, NULL, TRUE),
(4, 'Protetor Solar FPS 60 frasco 200ml', '7890000013017', 'Sundown', 35, 'Dermocosméticos', 8, 28.00, 44.90, '44-protetor-solar-fps-60.svg', '2027-12-31', 'outros', NULL, NULL, TRUE),
(5, 'Sabonete Líquido Antisséptico frasco 250ml', '7890000013086', 'Granado', 80, 'Higiene e Cuidados Pessoais', 12, 9.50, 15.90, '45-sabonete-liquido-antisseptico.svg', '2028-02-29', 'outros', NULL, NULL, TRUE),
(6, 'Pomada para Assaduras bisnaga 45g', '7890000013154', 'Cimed', 60, 'Infantil e Bebês', 10, 7.80, 12.90, '46-pomada-para-assaduras.svg', '2027-11-30', 'similar', NULL, NULL, TRUE),
(7, 'Curativo Adesivo c/ 40 unidades', '7890000013222', 'Cremer', 100, 'First Aid e Curativos', 15, 6.50, 10.90, '47-curativo-adesivo.svg', '2028-08-31', 'outros', NULL, NULL, TRUE),
(8, 'Luva Nitrílica caixa c/ 100 un.', '7890000013291', 'Descarpack', 200, 'EPIs', 20, 18.00, 28.90, '48-luva-nitrilica.svg', '2028-10-31', 'outros', NULL, NULL, TRUE),
(9, 'Seringa Descartável 10ml c/ agulha', '7890000013369', 'BD', 500, 'Materiais Hospitalares', 50, 0.80, 1.92, '49-seringa-descartavel-10ml.svg', '2029-01-31', 'outros', NULL, NULL, TRUE),
(10, 'Termômetro Digital clínico', '7890000013437', 'G-Tech', 40, 'Outros', 5, 12.00, 19.90, '50-termometro-digital.svg', NULL, 'outros', NULL, NULL, TRUE);


-- ================= ENTRADA (pedido ao fornecedor) =================
CREATE TABLE IF NOT EXISTS entrada (
  id INT NOT NULL AUTO_INCREMENT,
  data_pedido DATETIME NULL,
  valor_total DECIMAL(10,2) NOT NULL DEFAULT 0,
  observacao VARCHAR(255),
  quantidade_pedido INT NOT NULL DEFAULT 0,
  data_processamento DATETIME NULL,
  status ENUM('PENDENTE','PROCESSADO','CANCELADO') NOT NULL DEFAULT 'PENDENTE',
  fornecedor_id INT NOT NULL,
  produto_id INT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (produto_id) REFERENCES produto (id),
  FOREIGN KEY (fornecedor_id) REFERENCES fornecedor (id)
) ENGINE = InnoDB;

-- ================= SAIDA (pedido do cliente) =================
CREATE TABLE IF NOT EXISTS saida (
  id INT NOT NULL AUTO_INCREMENT,
  data_pedido DATETIME NULL,
  valor_total DECIMAL(10,2) NOT NULL DEFAULT 0,
  observacao VARCHAR(255),
  quantidade_pedido INT NOT NULL DEFAULT 0,
  data_processamento DATETIME NULL,
  status ENUM('PENDENTE','PROCESSADO','CANCELADO') NOT NULL DEFAULT 'PENDENTE',
  produto_id INT NOT NULL,
  clientes_cadastro_id INT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (produto_id) REFERENCES produto (id),
  FOREIGN KEY (clientes_cadastro_id) REFERENCES clientes_cadastro (id)
) ENGINE = InnoDB;

-- ================= MOVIMENTACAO =================
CREATE TABLE IF NOT EXISTS movimentacao (
  id INT NOT NULL AUTO_INCREMENT,
  tipo ENUM('ENTRADA','SAIDA') NOT NULL,
  quantidade INT NOT NULL,
  valor_total DECIMAL(10,2) NOT NULL,
  data_mov DATETIME NOT NULL,
  produto_id INT NOT NULL,
  fornecedor_id INT NULL,
  cliente_id INT NULL,
  entrada_id INT NULL,
  saida_id INT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (produto_id) REFERENCES produto (id),
  FOREIGN KEY (fornecedor_id) REFERENCES fornecedor (id),
  FOREIGN KEY (cliente_id) REFERENCES clientes_cadastro (id),
  FOREIGN KEY (entrada_id) REFERENCES entrada (id),
  FOREIGN KEY (saida_id) REFERENCES saida (id)
) ENGINE = InnoDB;

SHOW WARNINGS;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

SELECT * FROM cliente;
SELECT * FROM fornecedor;
SELECT * FROM produto;
SELECT * FROM entrada;