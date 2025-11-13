#!/usr/bin/env python3
"""
Supabase Connection Diagnostic Tool
Quickly diagnose Supabase connection issues and provide actionable fixes
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from app.config import settings
from sqlalchemy import create_engine, text
import re

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def print_section(text):
    print(f"\n{'─'*70}")
    print(f"📋 {text}")
    print("─"*70)

def check_env_file():
    """Check if .env file exists and has correct configuration"""
    print_section("1. Checking Environment Configuration")

    env_path = Path(__file__).parent / ".env"

    if not env_path.exists():
        print("❌ .env file NOT FOUND")
        print("\n🔧 FIX:")
        print("   1. Copy .env.example to .env:")
        print("      cp backend/.env.example backend/.env")
        print("   2. Update DATABASE_URL with your Supabase connection string")
        return False

    print(f"✅ .env file exists at: {env_path}")

    # Read and check DATABASE_URL
    with open(env_path) as f:
        content = f.read()

    # Check if DATABASE_URL is set
    db_url_match = re.search(r'^DATABASE_URL=(.+)$', content, re.MULTILINE)

    if not db_url_match:
        print("❌ DATABASE_URL not found in .env")
        return False

    db_url = db_url_match.group(1).strip()

    # Check if it's SQLite or PostgreSQL
    if db_url.startswith('sqlite'):
        print("⚠️  Currently using SQLite (local file)")
        print(f"   DATABASE_URL={db_url}")
        print("\n🔧 To switch to Supabase:")
        print("   1. Uncomment the PostgreSQL DATABASE_URL line in .env")
        print("   2. Comment out or remove the SQLite line")
        print("   3. Make sure password is correct in the URL")
        return False

    elif db_url.startswith('postgresql'):
        print("✅ Configured for PostgreSQL/Supabase")

        # Obscure password for security
        obscured = re.sub(r':(.*?)@', ':****@', db_url)
        print(f"   DATABASE_URL={obscured[:80]}...")

        # Check for project reference
        if 'dhmwuixxxsxkyfjdblqu' in db_url:
            print("✅ Found project reference: dhmwuixxxsxkyfjdblqu")

        # Check for pooler (recommended)
        if 'pooler.supabase.com' in db_url:
            print("✅ Using connection pooling (recommended)")
        elif 'db.' in db_url and 'supabase.co' in db_url:
            print("⚠️  Using direct connection (pooling recommended)")

        return True

    else:
        print(f"❌ Unknown database type: {db_url[:30]}...")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    print_section("2. Checking Python Dependencies")

    try:
        import psycopg2
        print("✅ psycopg2 installed")
    except ImportError:
        print("❌ psycopg2 NOT installed")
        print("\n🔧 FIX:")
        print("   pip install psycopg2-binary")
        return False

    try:
        from sqlalchemy import __version__
        print(f"✅ SQLAlchemy installed (version {__version__})")
    except ImportError:
        print("❌ SQLAlchemy NOT installed")
        print("\n🔧 FIX:")
        print("   pip install -r backend/requirements.txt")
        return False

    return True

def test_connection():
    """Test actual database connection"""
    print_section("3. Testing Database Connection")

    db_url = settings.DATABASE_URL

    if db_url.startswith('sqlite'):
        print("⚠️  Skipping connection test (SQLite in use)")
        print("   Switch to PostgreSQL to test Supabase connection")
        return False

    try:
        print("🔌 Creating database engine...")
        engine = create_engine(db_url, pool_pre_ping=True)

        print("🔗 Attempting connection...")
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()[0]

            print("✅ CONNECTION SUCCESSFUL!")
            print(f"\n   PostgreSQL Version:")
            print(f"   {version[:100]}")

            # Check tables
            print("\n🗃️  Checking database tables...")
            result = connection.execute(text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """))

            tables = [row[0] for row in result.fetchall()]

            if tables:
                print(f"   ✅ Found {len(tables)} tables:")
                for table in tables:
                    # Count records
                    count_result = connection.execute(text(f"SELECT COUNT(*) FROM {table};"))
                    count = count_result.fetchone()[0]
                    print(f"      • {table:<20} ({count:>4} records)")
            else:
                print("   ⚠️  No tables found!")
                print("\n🔧 FIX:")
                print("   1. Run migration script in Supabase SQL Editor")
                print("      File: backend/supabase_migration.sql")
                print("   2. Seed database:")
                print("      python backend/seed_supabase.py")

            return True

    except Exception as e:
        print(f"❌ CONNECTION FAILED")
        print(f"\n   Error: {str(e)}")

        # Provide specific troubleshooting
        error_str = str(e).lower()

        print("\n🔧 TROUBLESHOOTING:")

        if 'password authentication failed' in error_str:
            print("   Issue: Incorrect database password")
            print("   Fix:")
            print("   1. Go to Supabase Dashboard → Settings → Database")
            print("   2. Click 'Reset database password'")
            print("   3. Update password in DATABASE_URL in .env")

        elif 'could not translate host name' in error_str or 'connection refused' in error_str:
            print("   Issue: Cannot reach Supabase server")
            print("   Fix:")
            print("   1. Check if Supabase project is paused")
            print("      Visit: https://supabase.com/dashboard")
            print("   2. Click 'Restore project' if paused")
            print("   3. Check internet connection")
            print("   4. Verify URL in DATABASE_URL is correct")

        elif 'timeout' in error_str:
            print("   Issue: Connection timeout")
            print("   Fix:")
            print("   1. Check firewall settings")
            print("   2. Try using VPN or different network")
            print("   3. Verify Supabase is not blocked")

        else:
            print("   1. Verify DATABASE_URL format in .env")
            print("   2. Check Supabase project status")
            print("   3. Review backend/test_supabase_connection.py for details")

        return False

def check_supabase_config():
    """Check Supabase-specific configuration"""
    print_section("4. Checking Supabase Configuration")

    if settings.SUPABASE_URL:
        print(f"✅ SUPABASE_URL: {settings.SUPABASE_URL}")
    else:
        print("⚠️  SUPABASE_URL not set in .env")
        print("   (Optional, only needed for Supabase Auth features)")

    if settings.SUPABASE_KEY:
        print(f"✅ SUPABASE_KEY: {settings.SUPABASE_KEY[:30]}...")
    else:
        print("⚠️  SUPABASE_KEY not set in .env")
        print("   (Optional, only needed for Supabase Auth features)")

    return True

def provide_summary(checks_passed):
    """Provide final summary and next steps"""
    print_header("DIAGNOSTIC SUMMARY")

    total_checks = len(checks_passed)
    passed = sum(checks_passed.values())

    print(f"Checks passed: {passed}/{total_checks}\n")

    for check, status in checks_passed.items():
        icon = "✅" if status else "❌"
        print(f"{icon} {check}")

    if all(checks_passed.values()):
        print("\n" + "🎉 "*20)
        print("\n✅ ALL CHECKS PASSED! Your Supabase connection is ready!")
        print("\n📝 Next steps:")
        print("   1. Start backend: python -m uvicorn app.main:app --reload")
        print("   2. Test API: http://localhost:8000/docs")
        print("   3. Start frontend: cd frontend && npm run dev")
        print("   4. Login: http://localhost:5173")
    else:
        print("\n" + "⚠️  "*20)
        print("\n❌ Some checks failed. Review the fixes above.")
        print("\n📝 Common quick fixes:")
        print("   1. Install dependencies: pip install -r backend/requirements.txt")
        print("   2. Check Supabase dashboard: https://supabase.com/dashboard")
        print("   3. Update .env with correct DATABASE_URL")
        print("   4. Test connection: python backend/test_supabase_connection.py")
        print("\n📖 Full reconnection guide:")
        print("   Open: SUPABASE_RECONNECTION_GUIDE.md")

def main():
    print_header("SUPABASE CONNECTION DIAGNOSTICS")
    print("This tool will check your Supabase setup and identify issues\n")

    checks = {}

    # Run all checks
    checks["Environment File (.env)"] = check_env_file()
    checks["Python Dependencies"] = check_dependencies()
    checks["Database Connection"] = test_connection()
    checks["Supabase Configuration"] = check_supabase_config()

    # Summary
    provide_summary(checks)

    print("\n")
    return 0 if all(checks.values()) else 1

if __name__ == "__main__":
    sys.exit(main())
