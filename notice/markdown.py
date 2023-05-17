from flask import Flask, request, jsonify
from database import Database
from celery import Celery

app = Flask(__name__)

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Create Markdown table
with Database() as conn:
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `markdown` (
              `id` int(11) NOT NULL AUTO_INCREMENT,
              `content` text NOT NULL,
              PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)
        conn.commit()

# Define Celery task
@celery.task
def save_markdown(markdown):
    conn = Database()
    with conn.cursor() as cursor:
        sql = "INSERT INTO `markdown` (`content`) VALUES (%s)"
        cursor.execute(sql, markdown)
        conn.commit()

# Define route handler
def save_markdown_handler():
    # Get POST request data
    markdown = request.form.get('markdown', '')
    # Call Celery task to process markdown data
    save_markdown.delay(markdown)
    save_markdown(markdown)
    # Return successful JSON response
    return jsonify({'success': True}), 200
