import os
import json
import configparser


class Config:

    CONFIG_FOLDER_PATH = os.path.join(os.path.dirname(__file__), os.pardir)
    CONFIG_PATH = os.path.join(CONFIG_FOLDER_PATH, "config.ini")
    DEFAULT_CONFIG = {
        "connection": {
            "port_range_start": "10000",
            "port_range_end": "20000",
            "custom_messages": json.dumps([
                "Connect: ssh root@example.com -p {port}",
                "Dynamic port forward: ssh -D 9999 root@example.com -p {port} -t top"
            ]),
        }
    }

    def load(self):
        for configs in self._load_config().values():
            for config_key, config_value in configs.items():
                setattr(self, config_key, config_value)

    def _load_config(self):
        config_parser = configparser.ConfigParser()
        if config_parser.read(self.CONFIG_PATH):
            return config_parser
        return self._create_config()

    def _create_config(self):
        if not os.path.exists(self.CONFIG_FOLDER_PATH):
            os.makedirs(self.CONFIG_FOLDER_PATH)
        config_parser = configparser.ConfigParser()
        for section, configs in self.DEFAULT_CONFIG.items():
            config_parser[section] = {}
            for config_key, config_value in configs.items():
                config_parser[section][config_key] = config_value
        with open(self.CONFIG_PATH, 'w', encoding='utf-8') as f:
            config_parser.write(f)
        return config_parser


config = Config()
config.load()
