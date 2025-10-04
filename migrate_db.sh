#!/bin/bash
export FLASK_APP=app:create_migration_app
echo "Starting database migration..."
flask db migrate
echo "Database migration completed."
echo "Database upgrade..."
flask db upgrade
echo "Database upgrade completed."

