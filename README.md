Here's a detailed breakdown of each step for the GaiaNet Docker setup:

### Step 1: **Copy Docker Files**
1. Copy the Docker setup from `docker_01` to `docker_03`:
   ```bash
   cp -r docker_01 docker_03
   ```

### Step 2: **Edit Docker Compose File**
1. Open the `docker-compose.yml` file in the `docker_03` directory:
   ```bash
   vi docker_03/docker-compose.yml
   ```
2. Change the `container_name` to `my-gaianet-app-03`:
   ```yaml
   container_name: my-gaianet-app-03
   ```

### Step 3: **Update Configuration in `entrypoint.sh`**
1. Open the `entrypoint.sh` file to change GaiaNet configuration URL:
   ```bash
   vi docker_03/entrypoint.sh
   ```
2. Modify the necessary configurations (e.g., GaiaNet URL or other parameters). Save the file when done.

### Step 4: **Build Docker Image and Start Container**
1. Navigate to the `docker_03` directory:
   ```bash
   cd docker_03
   ```
2. Build the Docker image without using the cache:
   ```bash
   sudo docker-compose up --build --no-cache
   ```
3. Start the container in detached mode:
   ```bash
   sudo docker-compose up -d
   ```
4. Check the container logs to ensure everything is running correctly:
   ```bash
   sudo docker logs my-gaianet-app-03 -f
   ```

### Step 5: **Download the CSV File**
1. Use `wget` to download the CSV file into the container or host machine:
   ```bash
   wget -O data.csv "https://data.cityofchicago.org/api/views/6irb-gasv/rows.csv?accessType=DOWNLOAD"
   ```
   This will save the CSV file as `data.csv` in the current directory.

### Step 6: **Access the Docker Container**
1. Start an interactive shell session inside the running Docker container:
   ```bash
   sudo docker exec -it my-gaianet-app-03 /bin/bash
   ```

### Step 7: **Insert Data into Qdrant Vector Database**
1. Inside the container, run the Python script to insert data into the Qdrant database:
   ```bash
   python3 import_data.py
   ```
   Make sure that `import_data.py` is properly set up to handle the CSV data and insert it into the Qdrant vector database.

---

These steps should guide you through the entire setup and execution of your GaiaNet Docker environment. 
