SET search_path TO pdv, public;

INSERT INTO categorias (nome) VALUES
    ('Bebidas'),
    ('Padaria'),
    ('Mercearia'),
    ('Higiene'),
    ('Limpeza'),
    ('Frios e Laticínios');

INSERT INTO formas_pagamento (nome) VALUES
    ('Dinheiro'),
    ('Cartão Débito'),
    ('Cartão Crédito'),
    ('PIX');

INSERT INTO lojas (nome, cidade, uf) VALUES
    ('Mercado Central', 'São Paulo', 'SP'),
    ('Super PDV Norte', 'Campinas', 'SP'),
    ('Mini Mercado Sul', 'Curitiba', 'PR');

INSERT INTO caixas (loja_id, numero)
SELECT l.id, gs.numero
FROM lojas l
CROSS JOIN generate_series(1, 3) AS gs (numero);

INSERT INTO produtos (codigo_barras, nome, categoria_id, preco) VALUES
    ('7891000100103', 'Leite Integral 1L', 6, 4.89),
    ('7891000100202', 'Iogurte Natural 170g', 6, 3.49),
    ('7891000100301', 'Queijo Mussarela 200g', 6, 12.90),
    ('7891000100400', 'Presunto Fatiado 200g', 6, 9.99),
    ('7891000100509', 'Manteiga com Sal 200g', 6, 8.75),
    ('7891000100608', 'Requeijão Cremoso 200g', 6, 7.45),
    ('7891000100707', 'Pão Francês (un)', 2, 0.75),
    ('7891000100806', 'Pão de Forma 500g', 2, 7.20),
    ('7891000100905', 'Bolo de Chocolate (fatia)', 2, 4.50),
    ('7891000101002', 'Croissant Manteiga', 2, 5.90),
    ('7891000101101', 'Café Torrado 500g', 3, 18.90),
    ('7891000101200', 'Arroz Branco 5kg', 3, 24.50),
    ('7891000101309', 'Feijão Carioca 1kg', 3, 7.80),
    ('7891000101408', 'Açúcar Cristal 1kg', 3, 4.20),
    ('7891000101507', 'Óleo de Soja 900ml', 3, 6.99),
    ('7891000101606', 'Macarrão Espaguete 500g', 3, 3.89),
    ('7891000101705', 'Molho de Tomate 340g', 3, 2.99),
    ('7891000101804', 'Sal Refinado 1kg', 3, 2.10),
    ('7891000101903', 'Refrigerante Cola 2L', 1, 8.49),
    ('7891000102000', 'Suco de Laranja 1L', 1, 6.75),
    ('7891000102109', 'Água Mineral 1,5L', 1, 2.50),
    ('7891000102208', 'Cerveja Lata 350ml', 1, 3.99),
    ('7891000102307', 'Energético 250ml', 1, 9.90),
    ('7891000102406', 'Chá Mate 1L', 1, 4.60),
    ('7891000102505', 'Sabonete Líquido 250ml', 4, 11.90),
    ('7891000102604', 'Shampoo 350ml', 4, 15.50),
    ('7891000102703', 'Condicionador 350ml', 4, 16.90),
    ('7891000102802', 'Pasta de Dente 90g', 4, 5.40),
    ('7891000102901', 'Desodorante Aerosol', 4, 13.75),
    ('7891000103008', 'Papel Higiênico 12 rolos', 4, 22.90),
    ('7891000103107', 'Detergente Líquido 500ml', 5, 2.49),
    ('7891000103206', 'Sabão em Pó 1kg', 5, 14.80),
    ('7891000103305', 'Água Sanitária 1L', 5, 4.10),
    ('7891000103404', 'Desinfetante 2L', 5, 9.50),
    ('7891000103503', 'Esponja de Limpeza (3un)', 5, 6.20),
    ('7891000103602', 'Biscoito Recheado 130g', 3, 3.25),
    ('7891000103701', 'Achocolatado 400g', 3, 8.90),
    ('7891000103800', 'Cereal Matinal 300g', 3, 12.40),
    ('7891000103909', 'Barra de Cereal', 3, 2.80),
    ('7891000104006', 'Banana Prata (kg)', 3, 5.99),
    ('7891000104105', 'Maçã Gala (kg)', 3, 8.49),
    ('7891000104204', 'Tomate (kg)', 3, 6.20),
    ('7891000104303', 'Cebola (kg)', 3, 4.75),
    ('7891000104402', 'Batata (kg)', 3, 5.10),
    ('7891000104501', 'Ovos Brancos (dúzia)', 6, 10.90),
    ('7891000104600', 'Margarina 500g', 6, 6.80),
    ('7891000104709', 'Sorvete Pote 1,5L', 6, 19.90),
    ('7891000104808', 'Whey Protein Bar', 3, 14.50),
    ('7891000104907', 'Café Expresso (un)', 1, 4.00),
    ('7891000105004', 'Salgadinho 150g', 3, 7.30);

INSERT INTO vendas (data_hora, caixa_id, forma_pagamento_id, valor_total, desconto, status)
SELECT
    NOW()
        - (random() * INTERVAL '90 days')
        - (random() * INTERVAL '1 day')
        + (
            (8 + floor(random() * 13)) * INTERVAL '1 hour'
            + floor(random() * 60) * INTERVAL '1 minute'
        ),
    1 + floor(random() * (SELECT COUNT(*) FROM caixas))::INTEGER,
    1 + floor(random() * (SELECT COUNT(*) FROM formas_pagamento))::INTEGER,
    0,
    CASE
        WHEN random() < 0.12 THEN round((random() * 15)::NUMERIC, 2)
        ELSE 0
    END,
    CASE
        WHEN random() < 0.02 THEN 'cancelada'
        ELSE 'concluida'
    END
FROM generate_series(1, 2500);

DO $$
DECLARE
    v_venda RECORD;
    v_num_itens INTEGER;
    v_produto RECORD;
    v_quantidade NUMERIC(10, 3);
    v_subtotal NUMERIC(12, 2);
    v_total NUMERIC(12, 2);
BEGIN
    FOR v_venda IN
        SELECT id, desconto, status
        FROM vendas
        WHERE valor_total = 0
    LOOP
        v_total := 0;
        v_num_itens := 1 + floor(random() * 7)::INTEGER;

        FOR i IN 1..v_num_itens LOOP
            SELECT id, nome, preco
            INTO v_produto
            FROM produtos
            WHERE ativo
            ORDER BY random()
            LIMIT 1;

            IF v_produto.nome LIKE '%(kg)' THEN
                v_quantidade := round((0.250 + random() * 1.750)::NUMERIC, 3);
            ELSIF v_produto.nome LIKE '%(un)%' OR v_produto.nome LIKE '%(fatia)%' THEN
                v_quantidade := 1 + floor(random() * 4)::INTEGER;
            ELSE
                v_quantidade := 1 + floor(random() * 3)::INTEGER;
            END IF;

            v_subtotal := round(v_quantidade * v_produto.preco, 2);

            INSERT INTO itens_venda (
                venda_id,
                produto_id,
                quantidade,
                preco_unitario,
                subtotal
            ) VALUES (
                v_venda.id,
                v_produto.id,
                v_quantidade,
                v_produto.preco,
                v_subtotal
            );

            v_total := v_total + v_subtotal;
        END LOOP;

        UPDATE vendas
        SET valor_total = GREATEST(v_total - v_venda.desconto, 0)
        WHERE id = v_venda.id;
    END LOOP;
END $$;

ANALYZE;
