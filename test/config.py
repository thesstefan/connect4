import yaml

TEST_CONFIG_FILE_NAME = "test/test_config.yaml"

with open(TEST_CONFIG_FILE_NAME, "r") as stream:
    settings = yaml.safe_load(stream)
