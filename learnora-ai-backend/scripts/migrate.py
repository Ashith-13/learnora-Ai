"""
Database Migration Helper Script
Provides easy commands for Alembic migrations
"""
import asyncio
import sys
import os
import subprocess
from pathlib import Path

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings


class MigrationManager:
    """Handles database migrations using Alembic"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        
    def run_command(self, command: list) -> int:
        """Run a shell command"""
        try:
            result = subprocess.run(
                command,
                cwd=self.project_root,
                check=True,
                capture_output=True,
                text=True
            )
            print(result.stdout)
            return 0
        except subprocess.CalledProcessError as e:
            print(f"❌ Error: {e.stderr}")
            return 1
    
    def init_alembic(self):
        """Initialize Alembic (first time setup)"""
        print("=" * 50)
        print("🔧 Initializing Alembic...")
        print("=" * 50)
        
        alembic_dir = self.project_root / "alembic"
        if alembic_dir.exists():
            print("⚠️  Alembic already initialized!")
            response = input("Do you want to reinitialize? (y/n): ")
            if response.lower() != 'y':
                return
            
            # Backup existing alembic directory
            import shutil
            backup_dir = self.project_root / "alembic_backup"
            if backup_dir.exists():
                shutil.rmtree(backup_dir)
            shutil.move(str(alembic_dir), str(backup_dir))
            print("📦 Backed up existing alembic directory")
        
        result = self.run_command(["alembic", "init", "alembic"])
        if result == 0:
            print("\n✅ Alembic initialized successfully!")
            print("\n💡 Next steps:")
            print("   1. Update alembic.ini with your database URL")
            print("   2. Update alembic/env.py to import your models")
            print("   3. Run: python scripts/migrate.py create 'initial migration'")
    
    def create_migration(self, message: str):
        """Create a new migration"""
        print("=" * 50)
        print(f"📝 Creating migration: {message}")
        print("=" * 50)
        
        if not message:
            print("❌ Error: Migration message is required")
            print("Usage: python scripts/migrate.py create 'your message'")
            return
        
        result = self.run_command([
            "alembic", "revision", "--autogenerate", 
            "-m", message
        ])
        
        if result == 0:
            print("\n✅ Migration created successfully!")
            print("\n💡 Next steps:")
            print("   1. Review the migration file in alembic/versions/")
            print("   2. Run: python scripts/migrate.py upgrade")
    
    def upgrade(self, revision: str = "head"):
        """Upgrade database to a specific revision"""
        print("=" * 50)
        print(f"⬆️  Upgrading database to: {revision}")
        print("=" * 50)
        
        result = self.run_command(["alembic", "upgrade", revision])
        
        if result == 0:
            print("\n✅ Database upgraded successfully!")
    
    def downgrade(self, revision: str = "-1"):
        """Downgrade database to a specific revision"""
        print("=" * 50)
        print(f"⬇️  Downgrading database to: {revision}")
        print("=" * 50)
        
        confirm = input("⚠️  Are you sure you want to downgrade? (yes/no): ")
        if confirm.lower() != "yes":
            print("Cancelled.")
            return
        
        result = self.run_command(["alembic", "downgrade", revision])
        
        if result == 0:
            print("\n✅ Database downgraded successfully!")
    
    def current(self):
        """Show current migration revision"""
        print("=" * 50)
        print("📊 Current Migration Status")
        print("=" * 50)
        
        self.run_command(["alembic", "current"])
    
    def history(self):
        """Show migration history"""
        print("=" * 50)
        print("📜 Migration History")
        print("=" * 50)
        
        self.run_command(["alembic", "history", "--verbose"])
    
    def heads(self):
        """Show head revisions"""
        print("=" * 50)
        print("🎯 Head Revisions")
        print("=" * 50)
        
        self.run_command(["alembic", "heads"])
    
    def stamp(self, revision: str):
        """Stamp database with a specific revision without running migrations"""
        print("=" * 50)
        print(f"🏷️  Stamping database with revision: {revision}")
        print("=" * 50)
        
        confirm = input("⚠️  This will mark the database as being at this revision. Continue? (yes/no): ")
        if confirm.lower() != "yes":
            print("Cancelled.")
            return
        
        result = self.run_command(["alembic", "stamp", revision])
        
        if result == 0:
            print("\n✅ Database stamped successfully!")
    
    def show_help(self):
        """Show help message"""
        print("=" * 50)
        print("🗄️  Learnora AI - Database Migration Manager")
        print("=" * 50)
        print("\nUsage: python scripts/migrate.py [command] [args]")
        print("\nCommands:")
        print("  init                  - Initialize Alembic (first time setup)")
        print("  create 'message'      - Create a new migration")
        print("  upgrade [revision]    - Upgrade to a revision (default: head)")
        print("  downgrade [revision]  - Downgrade to a revision (default: -1)")
        print("  current               - Show current revision")
        print("  history               - Show migration history")
        print("  heads                 - Show head revisions")
        print("  stamp <revision>      - Stamp database with revision")
        print("  help                  - Show this help message")
        print("\nExamples:")
        print("  python scripts/migrate.py init")
        print("  python scripts/migrate.py create 'add user table'")
        print("  python scripts/migrate.py upgrade")
        print("  python scripts/migrate.py downgrade")
        print("  python scripts/migrate.py current")
        print("  python scripts/migrate.py history")
        print("\n💡 Tips:")
        print("  - Always review generated migrations before applying")
        print("  - Keep migration messages clear and descriptive")
        print("  - Test migrations in development before production")
        print("  - Backup your database before running migrations")


def main():
    """Main entry point"""
    manager = MigrationManager()
    
    if len(sys.argv) < 2:
        manager.show_help()
        return
    
    command = sys.argv[1].lower()
    
    try:
        if command == "init":
            manager.init_alembic()
        
        elif command == "create":
            if len(sys.argv) < 3:
                print("❌ Error: Migration message required")
                print("Usage: python scripts/migrate.py create 'your message'")
                return
            message = sys.argv[2]
            manager.create_migration(message)
        
        elif command == "upgrade":
            revision = sys.argv[2] if len(sys.argv) > 2 else "head"
            manager.upgrade(revision)
        
        elif command == "downgrade":
            revision = sys.argv[2] if len(sys.argv) > 2 else "-1"
            manager.downgrade(revision)
        
        elif command == "current":
            manager.current()
        
        elif command == "history":
            manager.history()
        
        elif command == "heads":
            manager.heads()
        
        elif command == "stamp":
            if len(sys.argv) < 3:
                print("❌ Error: Revision required")
                print("Usage: python scripts/migrate.py stamp <revision>")
                return
            revision = sys.argv[2]
            manager.stamp(revision)
        
        elif command == "help":
            manager.show_help()
        
        else:
            print(f"❌ Unknown command: {command}")
            print("\nRun 'python scripts/migrate.py help' for usage information")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()