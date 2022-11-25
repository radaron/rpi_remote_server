# Rpi Remote server

## Installation

### Prerequisites
* rust
* libffi
* poetry
* gcc
* openssl

### Poetry install
```
poetry install
```

### Generate secret
```
poetry run generate-secret
```

### Create service
```
cd <path of cloned repo>
```
```
echo "[Unit]
Description=rpi_remote server
After=multi-user.target
Conflicts=getty@tty1.service
[Service]
User=${USER}
Type=simple
Environment="LC_ALL=C.UTF-8"
Environment="LANG=C.UTF-8"
ExecStart=${HOME}/.local/bin/poetry run gunicorn
WorkingDirectory=$(pwd)
Restart=on-failure
[Install]
WantedBy=multi-user.target" | sudo tee /etc/systemd/system/rpi-remote-server.service
```
```
sudo systemctl daemon-reload
sudo systemctl enable rpi-remote-server.service
sudo systemctl start rpi-remote-server.service
```

## Generate user for manage
```
poetry run add-user
```

## Start port forwarder
```
poetry run forvard <PORT>
```