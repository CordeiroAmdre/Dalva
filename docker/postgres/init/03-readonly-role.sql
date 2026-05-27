-- Read-only role for the PDV-AI SQL agent (defense in depth with app-level validation).
\set ON_ERROR_STOP on

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'pdv_readonly') THEN
        CREATE ROLE pdv_readonly LOGIN PASSWORD 'pdv_readonly';
    ELSE
        ALTER ROLE pdv_readonly WITH LOGIN PASSWORD 'pdv_readonly';
    END IF;
END
$$;

GRANT CONNECT ON DATABASE pdv_ai TO pdv_readonly;
GRANT USAGE ON SCHEMA pdv TO pdv_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA pdv TO pdv_readonly;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA pdv TO pdv_readonly;

ALTER DEFAULT PRIVILEGES IN SCHEMA pdv
    GRANT SELECT ON TABLES TO pdv_readonly;
