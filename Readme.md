# Rpi Remote server

## Installation
```
curl -sSL https://gist.githubusercontent.com/radaron/4a527ab6d75bbcdf1d619d0aeb2c6986/raw > install.sh
chmod +x install.sh
./install.sh
rm install.sh
```

## Generate user for manage
```
python -m tools.add_user
```

## Start port forwarder
```
python -m tools.forvard <PORT>
```