# Create the file
cat > startup-script.sh << 'EOF'
#!/bin/bash
# startup-script.sh for Compute Engine instance running Qdrant

# Update system packages
apt-get update
apt-get install -y docker.io docker-compose

# Start Docker service
systemctl start docker
systemctl enable docker

# Add current user to docker group
usermod -aG docker $USER

# Create directory for Qdrant data
mkdir -p /opt/qdrant/storage
mkdir -p /opt/qdrant/config

# Create Qdrant configuration file
cat > /opt/qdrant/config/production.yaml << EOCONF
log_level: INFO
storage:
  # Where to store all the data
  storage_path: /qdrant/storage

service:
  # Host to bind the service on
  host: 0.0.0.0
  # HTTP port
  http_port: 6333
  # gRPC port
  grpc_port: 6334

cluster:
  # Use disabled for single-node deployment
  enabled: false

# Telemetry settings
telemetry_disabled: true
EOCONF

# Create docker-compose file for Qdrant
cat > /opt/qdrant/docker-compose.yml << EOCOMP
version: '3.8'

services:
  qdrant:
    image: qdrant/qdrant:latest
    container_name: qdrant
    restart: always
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - ./storage:/qdrant/storage:z
      - ./config/production.yaml:/qdrant/config/production.yaml:ro
    environment:
      - QDRANT__SERVICE__HTTP_PORT=6333
      - QDRANT__SERVICE__GRPC_PORT=6334
EOCOMP

# Start Qdrant service
cd /opt/qdrant
docker-compose up -d

# Create a systemd service to ensure Qdrant starts on boot
cat > /etc/systemd/system/qdrant.service << EOSVC
[Unit]
Description=Qdrant Vector Database
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/qdrant
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOSVC

# Enable the service
systemctl enable qdrant.service
systemctl start qdrant.service

# Configure firewall to allow Qdrant ports
ufw allow 6333/tcp
ufw allow 6334/tcp

echo "Qdrant installation completed successfully!"
echo "Qdrant is running on ports 6333 (HTTP) and 6334 (gRPC)"
echo "Access the Qdrant dashboard at http://[EXTERNAL_IP]:6333/dashboard"
EOF

# Make it executable
chmod +x startup-script.sh