"""Export static PDV seed datasets to Parquet files for DuckDB init."""

from __future__ import annotations

import argparse
import random
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

import duckdb

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_PARQUET_DIR = REPO_ROOT / "docker" / "duckdb" / "parquet"
SALES_SEED = 42
NUM_SALES = 2500
REFERENCE_NOW = datetime(2026, 5, 27, 12, 0, 0, tzinfo=timezone.utc)

CATEGORIAS = [
    (1, "Bebidas"),
    (2, "Padaria"),
    (3, "Mercearia"),
    (4, "Higiene"),
    (5, "Limpeza"),
    (6, "Frios e Laticínios"),
]

FORMAS_PAGAMENTO = [
    (1, "Dinheiro"),
    (2, "Cartão Débito"),
    (3, "Cartão Crédito"),
    (4, "PIX"),
]

LOJAS = [
    (1, "Mercado Central", "São Paulo", "SP"),
    (2, "Super PDV Norte", "Campinas", "SP"),
    (3, "Mini Mercado Sul", "Curitiba", "PR"),
]

PRODUTOS = [
    ("7891000100103", "Leite Integral 1L", 6, 4.89),
    ("7891000100202", "Iogurte Natural 170g", 6, 3.49),
    ("7891000100301", "Queijo Mussarela 200g", 6, 12.90),
    ("7891000100400", "Presunto Fatiado 200g", 6, 9.99),
    ("7891000100509", "Manteiga com Sal 200g", 6, 8.75),
    ("7891000100608", "Requeijão Cremoso 200g", 6, 7.45),
    ("7891000100707", "Pão Francês (un)", 2, 0.75),
    ("7891000100806", "Pão de Forma 500g", 2, 7.20),
    ("7891000100905", "Bolo de Chocolate (fatia)", 2, 4.50),
    ("7891000101002", "Croissant Manteiga", 2, 5.90),
    ("7891000101101", "Café Torrado 500g", 3, 18.90),
    ("7891000101200", "Arroz Branco 5kg", 3, 24.50),
    ("7891000101309", "Feijão Carioca 1kg", 3, 7.80),
    ("7891000101408", "Açúcar Cristal 1kg", 3, 4.20),
    ("7891000101507", "Óleo de Soja 900ml", 3, 6.99),
    ("7891000101606", "Macarrão Espaguete 500g", 3, 3.89),
    ("7891000101705", "Molho de Tomate 340g", 3, 2.99),
    ("7891000101804", "Sal Refinado 1kg", 3, 2.10),
    ("7891000101903", "Refrigerante Cola 2L", 1, 8.49),
    ("7891000102000", "Suco de Laranja 1L", 1, 6.75),
    ("7891000102109", "Água Mineral 1,5L", 1, 2.50),
    ("7891000102208", "Cerveja Lata 350ml", 1, 3.99),
    ("7891000102307", "Energético 250ml", 1, 9.90),
    ("7891000102406", "Chá Mate 1L", 1, 4.60),
    ("7891000102505", "Sabonete Líquido 250ml", 4, 11.90),
    ("7891000102604", "Shampoo 350ml", 4, 15.50),
    ("7891000102703", "Condicionador 350ml", 4, 16.90),
    ("7891000102802", "Pasta de Dente 90g", 4, 5.40),
    ("7891000102901", "Desodorante Aerosol", 4, 13.75),
    ("7891000103008", "Papel Higiênico 12 rolos", 4, 22.90),
    ("7891000103107", "Detergente Líquido 500ml", 5, 2.49),
    ("7891000103206", "Sabão em Pó 1kg", 5, 14.80),
    ("7891000103305", "Água Sanitária 1L", 5, 4.10),
    ("7891000103404", "Desinfetante 2L", 5, 9.50),
    ("7891000103503", "Esponja de Limpeza (3un)", 5, 6.20),
    ("7891000103602", "Biscoito Recheado 130g", 3, 3.25),
    ("7891000103701", "Achocolatado 400g", 3, 8.90),
    ("7891000103800", "Cereal Matinal 300g", 3, 12.40),
    ("7891000103909", "Barra de Cereal", 3, 2.80),
    ("7891000104006", "Banana Prata (kg)", 3, 5.99),
    ("7891000104105", "Maçã Gala (kg)", 3, 8.49),
    ("7891000104204", "Tomate (kg)", 3, 6.20),
    ("7891000104303", "Cebola (kg)", 3, 4.75),
    ("7891000104402", "Batata (kg)", 3, 5.10),
    ("7891000104501", "Ovos Brancos (dúzia)", 6, 10.90),
    ("7891000104600", "Margarina 500g", 6, 6.80),
    ("7891000104709", "Sorvete Pote 1,5L", 6, 19.90),
    ("7891000104808", "Whey Protein Bar", 3, 14.50),
    ("7891000104907", "Café Expresso (un)", 1, 4.00),
    ("7891000105004", "Salgadinho 150g", 3, 7.30),
]


def _caixas_rows() -> list[tuple[int, int, int]]:
    rows: list[tuple[int, int, int]] = []
    next_id = 1
    for loja_id in (1, 2, 3):
        for numero in (1, 2, 3):
            rows.append((next_id, loja_id, numero))
            next_id += 1
    return rows


def _produto_rows() -> list[tuple[int, str, str, int, float, bool]]:
    return [
        (idx, codigo, nome, cat_id, preco, True)
        for idx, (codigo, nome, cat_id, preco) in enumerate(PRODUTOS, start=1)
    ]


def _generate_sales() -> tuple[list[tuple], list[tuple]]:
    """Build static vendas and itens_venda rows with a fixed random seed."""
    random.seed(SALES_SEED)
    caixa_ids = [row[0] for row in _caixas_rows()]
    payment_ids = [row[0] for row in FORMAS_PAGAMENTO]
    products = [(row[0], row[2], row[4]) for row in _produto_rows()]

    vendas: list[tuple] = []
    itens: list[tuple] = []
    next_item_id = 1

    for venda_id in range(1, NUM_SALES + 1):
        days_back = random.random() * 90
        hour_offset = 8 + random.randint(0, 12)
        minute_offset = random.randint(0, 59)
        data_hora = REFERENCE_NOW - timedelta(
            days=days_back,
            hours=hour_offset,
            minutes=minute_offset,
        )
        caixa_id = random.choice(caixa_ids)
        forma_pagamento_id = random.choice(payment_ids)
        desconto = (
            round(Decimal(str(random.random() * 15)), 2)
            if random.random() < 0.12
            else Decimal("0")
        )
        status = "cancelada" if random.random() < 0.02 else "concluida"

        total = Decimal("0")
        num_items = 1 + random.randint(0, 6)
        for _ in range(num_items):
            produto_id, nome, preco = random.choice(products)
            preco_dec = Decimal(str(preco))
            if "(kg)" in nome:
                quantidade = Decimal(str(round(0.250 + random.random() * 1.750, 3)))
            elif "(un)" in nome or "(fatia)" in nome:
                quantidade = Decimal(str(1 + random.randint(0, 3)))
            else:
                quantidade = Decimal(str(1 + random.randint(0, 2)))
            subtotal = round(quantidade * preco_dec, 2)
            itens.append(
                (next_item_id, venda_id, produto_id, quantidade, preco_dec, subtotal)
            )
            next_item_id += 1
            total += subtotal

        valor_total = max(total - desconto, Decimal("0"))
        vendas.append(
            (
                venda_id,
                data_hora,
                caixa_id,
                forma_pagamento_id,
                valor_total,
                desconto,
                status,
            )
        )

    return vendas, itens


def build_parquet(output_dir: Path | None = None) -> Path:
    """Write static seed Parquet files used by init_db."""
    target = output_dir or DEFAULT_PARQUET_DIR
    target.mkdir(parents=True, exist_ok=True)

    conn = duckdb.connect()
    try:
        conn.execute("CREATE TABLE categorias (id INTEGER, nome VARCHAR)")
        conn.executemany("INSERT INTO categorias VALUES (?, ?)", CATEGORIAS)
        conn.execute(
            f"COPY categorias TO '{target / 'categorias.parquet'}' (FORMAT PARQUET)"
        )

        conn.execute("CREATE TABLE formas_pagamento (id INTEGER, nome VARCHAR)")
        conn.executemany("INSERT INTO formas_pagamento VALUES (?, ?)", FORMAS_PAGAMENTO)
        conn.execute(
            f"COPY formas_pagamento TO '{target / 'formas_pagamento.parquet'}' (FORMAT PARQUET)"
        )

        conn.execute(
            "CREATE TABLE lojas (id INTEGER, nome VARCHAR, cidade VARCHAR, uf CHAR(2))"
        )
        conn.executemany("INSERT INTO lojas VALUES (?, ?, ?, ?)", LOJAS)
        conn.execute(f"COPY lojas TO '{target / 'lojas.parquet'}' (FORMAT PARQUET)")

        caixas = _caixas_rows()
        conn.execute("CREATE TABLE caixas (id INTEGER, loja_id INTEGER, numero INTEGER)")
        conn.executemany("INSERT INTO caixas VALUES (?, ?, ?)", caixas)
        conn.execute(f"COPY caixas TO '{target / 'caixas.parquet'}' (FORMAT PARQUET)")

        produto_rows = _produto_rows()
        conn.execute(
            """
            CREATE TABLE produtos (
                id INTEGER,
                codigo_barras VARCHAR,
                nome VARCHAR,
                categoria_id INTEGER,
                preco DECIMAL(10, 2),
                ativo BOOLEAN
            )
            """
        )
        conn.executemany("INSERT INTO produtos VALUES (?, ?, ?, ?, ?, ?)", produto_rows)
        conn.execute(f"COPY produtos TO '{target / 'produtos.parquet'}' (FORMAT PARQUET)")

        vendas, itens = _generate_sales()
        conn.execute(
            """
            CREATE TABLE vendas (
                id BIGINT,
                data_hora TIMESTAMPTZ,
                caixa_id INTEGER,
                forma_pagamento_id INTEGER,
                valor_total DECIMAL(12, 2),
                desconto DECIMAL(10, 2),
                status VARCHAR
            )
            """
        )
        conn.executemany(
            """
            INSERT INTO vendas VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            vendas,
        )
        conn.execute(f"COPY vendas TO '{target / 'vendas.parquet'}' (FORMAT PARQUET)")

        conn.execute(
            """
            CREATE TABLE itens_venda (
                id BIGINT,
                venda_id BIGINT,
                produto_id INTEGER,
                quantidade DECIMAL(10, 3),
                preco_unitario DECIMAL(10, 2),
                subtotal DECIMAL(12, 2)
            )
            """
        )
        conn.executemany(
            "INSERT INTO itens_venda VALUES (?, ?, ?, ?, ?, ?)",
            itens,
        )
        conn.execute(
            f"COPY itens_venda TO '{target / 'itens_venda.parquet'}' (FORMAT PARQUET)"
        )
    finally:
        conn.close()

    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build static PDV Parquet seed files")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_PARQUET_DIR,
        help=f"Parquet output directory (default: {DEFAULT_PARQUET_DIR})",
    )
    args = parser.parse_args(argv)

    path = build_parquet(args.output_dir)
    print(f"Parquet seed files written to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
