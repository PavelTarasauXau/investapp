"""add indexes and transaction trigger

Revision ID: 79d3d24fbf6a
Revises: 35e72adbc764
Create Date: 2026-05-13 01:48:59.162322

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79d3d24fbf6a'
down_revision: Union[str, Sequence[str], None] = '35e72adbc764'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE INDEX IF NOT EXISTS idx_assets_asset_type
    ON assets (asset_type);
    """)

    op.execute("""
    CREATE INDEX IF NOT EXISTS idx_stocks_sector
    ON stocks (sector);
    """)

    op.execute("""
    CREATE INDEX IF NOT EXISTS idx_transactions_type
    ON transactions (transaction_type);
    """)

    op.execute("""
    CREATE INDEX IF NOT EXISTS idx_transactions_portfolio_type
    ON transactions (portfolio_id, transaction_type);
    """)

    op.execute("""
    CREATE INDEX IF NOT EXISTS idx_portfolios_user_active
    ON portfolios (user_id, is_active);
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION check_sell_transaction_position()
    RETURNS TRIGGER AS $$
    DECLARE
        current_position NUMERIC(18, 4);
    BEGIN
        IF NEW.transaction_date > CURRENT_TIMESTAMP + INTERVAL '5 minutes' THEN
            RAISE EXCEPTION 'Transaction date cannot be in the future';
        END IF;

        IF NEW.transaction_type = 'sell' THEN
            SELECT COALESCE(SUM(
                CASE
                    WHEN transaction_type = 'buy' THEN quantity
                    WHEN transaction_type = 'sell' THEN -quantity
                    ELSE 0
                END
            ), 0)
            INTO current_position
            FROM transactions
            WHERE portfolio_id = NEW.portfolio_id
              AND asset_id = NEW.asset_id;

            IF NEW.quantity > current_position THEN
                RAISE EXCEPTION 'Cannot sell more assets than portfolio contains';
            END IF;
        END IF;

        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    DROP TRIGGER IF EXISTS trg_check_sell_transaction_position
    ON transactions;
    """)

    op.execute("""
    CREATE TRIGGER trg_check_sell_transaction_position
    BEFORE INSERT OR UPDATE ON transactions
    FOR EACH ROW
    EXECUTE FUNCTION check_sell_transaction_position();
    """)


def downgrade() -> None:
    op.execute("""
    DROP TRIGGER IF EXISTS trg_check_sell_transaction_position
    ON transactions;
    """)

    op.execute("""
    DROP FUNCTION IF EXISTS check_sell_transaction_position();
    """)

    op.execute("DROP INDEX IF EXISTS idx_portfolios_user_active;")
    op.execute("DROP INDEX IF EXISTS idx_transactions_portfolio_type;")
    op.execute("DROP INDEX IF EXISTS idx_transactions_type;")
    op.execute("DROP INDEX IF EXISTS idx_stocks_sector;")
    op.execute("DROP INDEX IF EXISTS idx_assets_asset_type;")