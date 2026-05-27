CREATE SCHEMA IF NOT EXISTS pdv;

CREATE SEQUENCE pdv.categorias_id_seq START 1;
CREATE TABLE pdv.categorias (
    id INTEGER PRIMARY KEY DEFAULT nextval('pdv.categorias_id_seq'),
    nome VARCHAR(100) NOT NULL UNIQUE
);

CREATE SEQUENCE pdv.produtos_id_seq START 1;
CREATE TABLE pdv.produtos (
    id INTEGER PRIMARY KEY DEFAULT nextval('pdv.produtos_id_seq'),
    codigo_barras VARCHAR(20) NOT NULL UNIQUE,
    nome VARCHAR(200) NOT NULL,
    categoria_id INTEGER NOT NULL REFERENCES pdv.categorias (id),
    preco DECIMAL(10, 2) NOT NULL CHECK (preco > 0),
    ativo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE SEQUENCE pdv.formas_pagamento_id_seq START 1;
CREATE TABLE pdv.formas_pagamento (
    id INTEGER PRIMARY KEY DEFAULT nextval('pdv.formas_pagamento_id_seq'),
    nome VARCHAR(50) NOT NULL UNIQUE
);

CREATE SEQUENCE pdv.lojas_id_seq START 1;
CREATE TABLE pdv.lojas (
    id INTEGER PRIMARY KEY DEFAULT nextval('pdv.lojas_id_seq'),
    nome VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    uf CHAR(2) NOT NULL
);

CREATE SEQUENCE pdv.caixas_id_seq START 1;
CREATE TABLE pdv.caixas (
    id INTEGER PRIMARY KEY DEFAULT nextval('pdv.caixas_id_seq'),
    loja_id INTEGER NOT NULL REFERENCES pdv.lojas (id),
    numero INTEGER NOT NULL CHECK (numero > 0),
    UNIQUE (loja_id, numero)
);

CREATE SEQUENCE pdv.vendas_id_seq START 1;
CREATE TABLE pdv.vendas (
    id BIGINT PRIMARY KEY DEFAULT nextval('pdv.vendas_id_seq'),
    data_hora TIMESTAMPTZ NOT NULL,
    caixa_id INTEGER NOT NULL REFERENCES pdv.caixas (id),
    forma_pagamento_id INTEGER NOT NULL REFERENCES pdv.formas_pagamento (id),
    valor_total DECIMAL(12, 2) NOT NULL CHECK (valor_total >= 0),
    desconto DECIMAL(10, 2) NOT NULL DEFAULT 0 CHECK (desconto >= 0),
    status VARCHAR(20) NOT NULL DEFAULT 'concluida'
        CHECK (status IN ('concluida', 'cancelada'))
);

CREATE SEQUENCE pdv.itens_venda_id_seq START 1;
CREATE TABLE pdv.itens_venda (
    id BIGINT PRIMARY KEY DEFAULT nextval('pdv.itens_venda_id_seq'),
    venda_id BIGINT NOT NULL REFERENCES pdv.vendas (id),
    produto_id INTEGER NOT NULL REFERENCES pdv.produtos (id),
    quantidade DECIMAL(10, 3) NOT NULL CHECK (quantidade > 0),
    preco_unitario DECIMAL(10, 2) NOT NULL CHECK (preco_unitario > 0),
    subtotal DECIMAL(12, 2) NOT NULL CHECK (subtotal >= 0)
);

CREATE INDEX idx_vendas_data_hora ON pdv.vendas (data_hora);
CREATE INDEX idx_vendas_caixa_id ON pdv.vendas (caixa_id);
CREATE INDEX idx_vendas_forma_pagamento_id ON pdv.vendas (forma_pagamento_id);
CREATE INDEX idx_itens_venda_venda_id ON pdv.itens_venda (venda_id);
CREATE INDEX idx_itens_venda_produto_id ON pdv.itens_venda (produto_id);
CREATE INDEX idx_produtos_categoria_id ON pdv.produtos (categoria_id);

CREATE VIEW pdv.vw_vendas_detalhadas AS
SELECT
    v.id AS venda_id,
    v.data_hora,
    l.nome AS loja,
    l.cidade,
    l.uf,
    c.numero AS caixa,
    fp.nome AS forma_pagamento,
    v.valor_total,
    v.desconto,
    v.status,
    iv.id AS item_id,
    p.codigo_barras,
    p.nome AS produto,
    cat.nome AS categoria,
    iv.quantidade,
    iv.preco_unitario,
    iv.subtotal
FROM pdv.vendas v
JOIN pdv.caixas c ON c.id = v.caixa_id
JOIN pdv.lojas l ON l.id = c.loja_id
JOIN pdv.formas_pagamento fp ON fp.id = v.forma_pagamento_id
JOIN pdv.itens_venda iv ON iv.venda_id = v.id
JOIN pdv.produtos p ON p.id = iv.produto_id
JOIN pdv.categorias cat ON cat.id = p.categoria_id;
