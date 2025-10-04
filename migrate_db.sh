#!/bin/bash
export FLASK_APP=app:create_migration_app

# Initialize migrations if not already done
if [ ! -f migrations/env.py ]; then
    echo "Initializing Flask-Migrate..."
    if [ -d migrations ]; then
        rm -rf migrations
    fi
    flask db init
    echo "✓ Migrations initialized"
fi

echo "Creating/updating migrations..."
flask db migrate
echo "Applying migrations to database..."
flask db upgrade
echo "✓ Database is up to date!"

