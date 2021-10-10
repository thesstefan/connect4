import yaml

CONFIG_FILE_NAME = "config.yaml"

with open(CONFIG_FILE_NAME, "r") as stream:
    settings = yaml.safe_load(stream)
