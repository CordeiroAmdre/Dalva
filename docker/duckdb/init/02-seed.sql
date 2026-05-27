Static reference and sales data is loaded from Parquet files in `../parquet/`
during `uv run python -m dalva_backend.scripts.init_db`.

Parquet files (all static):
  categorias, formas_pagamento, lojas, caixas, produtos, vendas, itens_venda

Regenerate Parquet files after changing seed data:
  uv run python -m dalva_backend.scripts.build_parquet
