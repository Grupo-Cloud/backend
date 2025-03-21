# NotebookLMini

## About

A simple chat application designed so you can chat with the contents of your documents. This chat app is composed
of multiple components, including but not limited to:

- A backend service written in FastAPI, running with a PostgreSQL relational database for keeping track of user data
- A frontend service written in React and shadcn for simple user interaction
- A Minio service that can store user documents such that they can always be queried and kept track of easily
- A Qdrant vector database that will let us sort through the user's documents and get information quickly and efficiently

## Deployment

To deploy the service, we have created a simple `docker-compose.yml`. This compose should work nicely as long as all environment variables
are filled properly. We supply an example .env file down below

```
JWT_SECRET_KEY='oXEvSSFm4-KJ_0TstrJ83IYVVPD36kgvSh-MJOQn4SvO3ZOxQU7ay6hf-r-ylrkqt8uhnYQP5OMrSa7v2GTMow' # Anything sufficiently random and long works well here
JWT_REFRESH_KEY= 'k9B8HmVBS49Ghasr70v7AUA6OLOaSoEwdu00sWkFsOcj4s6y8kxHBcqXB1jmnOwfQbcn_4S6WO2zfAmUEWgOJQ' # Anything sufficiently random and long works well here 
S3_HOST= 'minio:9000'
S3_ACCESS_KEY= 'MINIO'
S3_SECRET_KEY= 'MINIO123'
S3_SECURE= false
S3_TYPE= 'minio'
S3_DOCUMENT_BUCKET= 'documents'
QDRANT_HOST = 'qdrant'
QDRANT_PORT = 6333
QDRANT_COLLECTION_NAME = 'chunks'
GOOGLE_API_KEY=<Google API Key>
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_DB=database
POSTGRES_HOST=db
```

After creating the `.env` (or `.env.dev`) file in the working directory, please run

```
docker compose up -d
```

This will instantiate the application and let you access it fully. Frontend will be at `<INSERT URL>`, while the backend's documentation
and OpenAPI protocol specification can be found at `<INSERT URL>`.
