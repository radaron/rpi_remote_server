# Rpi Remote server

## Installation

### Prerequisites
* rust
* libffi
* gcc
* openssl

### Install dependencies
```
make install
```

### Generate secret
```
make generate-secret
```

### Generate user
```
make add-user
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
ExecStart=${HOME}/.venv/bin/gunicorn
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

## Usage

### Start port forwarder
```
make forvard NAME=<NAME> PORT=<PORT>
```

### Check logs
```
journalctl -fu rpi-remote-server
```

## Development

### Install dev requirements

```
make install-dev
```

### Lint code
Backend
```
make lint
```
Frontend
```
cd frontend && pnpm lint
```

### Start dev
Backend
```
make start-dev
```
Frontend
```
cd frontend && pnpm start
```