from sqlalchemy import inspect, text

from app import create_app
from app.extensions import db


app = create_app()


with app.app_context():
    inspector = inspect(db.engine)

    existing_columns = {
        column["name"]
        for column in inspector.get_columns("products")
    }

    with db.engine.begin() as connection:

        if "ratings_enabled" not in existing_columns:
            connection.execute(
                text(
                    """
                    ALTER TABLE products
                    ADD COLUMN ratings_enabled BOOLEAN
                    NOT NULL DEFAULT 1
                    """
                )
            )
            print("✅ تمت إضافة ratings_enabled")
        else:
            print("ℹ️ ratings_enabled موجود مسبقًا")

        if "comments_enabled" not in existing_columns:
            connection.execute(
                text(
                    """
                    ALTER TABLE products
                    ADD COLUMN comments_enabled BOOLEAN
                    NOT NULL DEFAULT 1
                    """
                )
            )
            print("✅ تمت إضافة comments_enabled")
        else:
            print("ℹ️ comments_enabled موجود مسبقًا")

    print("✅ انتهى تحديث جدول المنتجات")