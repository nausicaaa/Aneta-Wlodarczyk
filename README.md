###Aneta-Włodarczyk
simple HTTP server handling CRUD operations in Sanic

# Install requirements
pip install -r requirements.txt
pip install -e .

# Start server
python http_server/main.py

# Run tests
pytest http_server/tests/tests.py

# Setup database
docker pull postgres

docker-compose up

