import pytest

from dalva_backend.repositories.sql_validator import SqlValidationError, validate_readonly_sql


def test_select_allowed() -> None:
    validate_readonly_sql("SELECT id, nome FROM pdv.produtos WHERE ativo = true")


def test_with_cte_allowed() -> None:
    validate_readonly_sql(
        "WITH t AS (SELECT 1 AS x) SELECT x FROM t"
    )


def test_insert_blocked() -> None:
    with pytest.raises(SqlValidationError, match="Forbidden"):
        validate_readonly_sql("INSERT INTO pdv.produtos (nome) VALUES ('x')")


def test_delete_blocked() -> None:
    with pytest.raises(SqlValidationError, match="Forbidden"):
        validate_readonly_sql("DELETE FROM pdv.vendas WHERE id = 1")


def test_drop_blocked() -> None:
    with pytest.raises(SqlValidationError, match="Forbidden"):
        validate_readonly_sql("DROP TABLE pdv.produtos")


def test_multiple_statements_blocked() -> None:
    with pytest.raises(SqlValidationError, match="single"):
        validate_readonly_sql("SELECT 1; SELECT 2")
