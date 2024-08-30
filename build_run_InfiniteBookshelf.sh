
# Build the Docker image
docker build -f .devcontainer/Dockerfile_InfiniteBookshelf -t infinitebookshelf .

# Run the Docker container
docker run -d --name Dockerfile_InfiniteBookshelf -p 8501:8501 infinitebookshelf
