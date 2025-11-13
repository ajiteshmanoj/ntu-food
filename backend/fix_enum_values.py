"""
Fix enum values in Supabase database
Converts uppercase enum names (STUDENT, STALL_OWNER, ADMIN) to lowercase values (student, stall_owner, admin)
"""

from sqlalchemy import create_engine, text
from app.config import settings

def fix_enum_values():
    engine = create_engine(settings.DATABASE_URL)

    with engine.connect() as conn:
        # Start a transaction
        trans = conn.begin()

        try:
            # Update user roles from uppercase to lowercase
            print("Updating user roles...")
            result = conn.execute(text("""
                UPDATE users
                SET role = CASE
                    WHEN role = 'STUDENT' THEN 'student'
                    WHEN role = 'STALL_OWNER' THEN 'stall_owner'
                    WHEN role = 'ADMIN' THEN 'admin'
                    ELSE role
                END
                WHERE role IN ('STUDENT', 'STALL_OWNER', 'ADMIN')
            """))

            print(f"✓ Updated {result.rowcount} user records")

            # Check if there are any other tables with enum issues
            print("\nVerifying all users have correct role values...")
            result = conn.execute(text("SELECT role, COUNT(*) FROM users GROUP BY role"))
            for row in result:
                print(f"  - {row[0]}: {row[1]} users")

            trans.commit()
            print("\n✓ All enum values have been fixed successfully!")

        except Exception as e:
            trans.rollback()
            print(f"✗ Error: {e}")
            raise

if __name__ == "__main__":
    fix_enum_values()
