CREATE SCHEMA IF NOT EXISTS pdv;
SET search_path TO pdv, public;

CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    codigo_barras VARCHAR(20) NOT NULL UNIQUE,
    nome VARCHAR(200) NOT NULL,
    categoria_id INTEGER NOT NULL REFERENCES categorias (id),
    preco NUMERIC(10, 2) NOT NULL CHECK (preco > 0),
    ativo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE formas_pagamento (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE lojas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    uf CHAR(2) NOT NULL
);

CREATE TABLE caixas (
    id SERIAL PRIMARY KEY,
    loja_id INTEGER NOT NULL REFERENCES lojas (id),
    numero INTEGER NOT NULL CHECK (numero > 0),
    UNIQUE (loja_id, numero)
);

CREATE TABLE vendas (
    id BIGSERIAL PRIMARY KEY,
    data_hora TIMESTAMPTZ NOT NULL,
    caixa_id INTEGER NOT NULL REFERENCES caixas (id),
    forma_pagamento_id INTEGER NOT NULL REFERENCES formas_pagamento (id),
    valor_total NUMERIC(12, 2) NOT NULL CHECK (valor_total >= 0),
    desconto NUMERIC(10, 2) NOT NULL DEFAULT 0 CHECK (desconto >= 0),
    status VARCHAR(20) NOT NULL DEFAULT 'concluida'
        CHECK (status IN ('concluida', 'cancelada'))
);

CREATE TABLE itens_venda (
    id BIGSERIAL PRIMARY KEY,
    venda_id BIGINT NOT NULL REFERENCES vendas (id) ON DELETE CASCADE,
    produto_id INTEGER NOT NULL REFERENCES produtos (id),
    quantidade NUMERIC(10, 3) NOT NULL CHECK (quantidade > 0),
    preco_unitario NUMERIC(10, 2) NOT NULL CHECK (preco_unitario > 0),
    subtotal NUMERIC(12, 2) NOT NULL CHECK (subtotal >= 0)
);

CREATE INDEX idx_vendas_data_hora ON vendas (data_hora);
CREATE INDEX idx_vendas_caixa_id ON vendas (caixa_id);
CREATE INDEX idx_vendas_forma_pagamento_id ON vendas (forma_pagamento_id);
CREATE INDEX idx_itens_venda_venda_id ON itens_venda (venda_id);
CREATE INDEX idx_itens_venda_produto_id ON itens_venda (produto_id);
CREATE INDEX idx_produtos_categoria_id ON produtos (categoria_id);

CREATE VIEW vw_vendas_detalhadas AS
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
FROM vendas v
JOIN caixas c ON c.id = v.caixa_id
JOIN lojas l ON l.id = c.loja_id
JOIN formas_pagamento fp ON fp.id = v.forma_pagamento_id
JOIN itens_venda iv ON iv.venda_id = v.id
JOIN produtos p ON p.id = iv.produto_id
JOIN categorias cat ON cat.id = p.categoria_id;
