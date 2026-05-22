"""Simple DB management CLI for DealMind"""
import sys
from app.utils.database import init_db, drop_db


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m app.utils.manage_db init|drop")
        sys.exit(1)
    cmd = sys.argv[1].lower()
    if cmd == "init":
        print("Initializing database (create tables)...")
        init_db()
        print("Done.")
    elif cmd == "drop":
        confirm = input("Are you sure you want to DROP all tables? Type YES to confirm: ")
        if confirm == "YES":
            drop_db()
            print("Dropped all tables.")
        else:
            print("Aborted.")
    else:
        print("Unknown command", cmd)
        sys.exit(1)


if __name__ == "__main__":
    main()
