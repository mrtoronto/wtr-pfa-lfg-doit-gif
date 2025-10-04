import logging

logger = logging.getLogger('APP')

try:
    from main import app
except Exception as e:
    logger.error(f'Error importing app in wsgi.py: {e}')
    raise

if __name__ == "__main__":
    # For local development only
    app.run(host="localhost", port=4200, debug=True)

