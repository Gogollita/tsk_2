import sys
import xml.etree.ElementTree as ET
from pathlib import Path


class Config:
    def __init__(self):
        self.package_name = ""
        self.repo_url = ""
        self.test_repo_mode = False
        self.output_file = "graph.png"
        self.ascii_tree_mode = False


def parse_bool(value):
    if value is None:
        return False
    value_str = str(value).strip().lower()
    if value_str in ('true', '1', 'yes'):
        return True
    elif value_str in ('false', '0', 'no'):
        return False
    raise ValueError(f"Invalid boolean value: {value}")


def load_config(config_path):
    try:
        tree = ET.parse(config_path)
        root = tree.getroot()

        config = Config()

        package_elem = root.find('package_name')
        if package_elem is None or not package_elem.text:
            raise ValueError("Missing required parameter: package_name")
        config.package_name = package_elem.text.strip()

        repo_elem = root.find('repository_url')
        if repo_elem is None or not repo_elem.text:
            raise ValueError("Missing required parameter: repository_url")
        config.repo_url = repo_elem.text.strip()

        test_mode_elem = root.find('test_repo_mode')
        if test_mode_elem is not None and test_mode_elem.text:
            config.test_repo_mode = parse_bool(test_mode_elem.text)

        output_elem = root.find('output_image')
        if output_elem is not None and output_elem.text:
            config.output_file = output_elem.text.strip()

        ascii_elem = root.find('ascii_tree_mode')
        if ascii_elem is not None and ascii_elem.text:
            config.ascii_tree_mode = parse_bool(ascii_elem.text)

        return config

    except ET.ParseError as e:
        print(f"Error parsing XML config: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading config: {e}")
        sys.exit(1)


def print_config(config):
    print("Configuration parameters:")
    print(f"  package_name: {config.package_name}")
    print(f"  repository_url: {config.repo_url}")
    print(f"  test_repo_mode: {config.test_repo_mode}")
    print(f"  output_image: {config.output_file}")
    print(f"  ascii_tree_mode: {config.ascii_tree_mode}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python Task1.py <config.xml>")
        print("Example: python Task1.py File.xml")
        sys.exit(1)

    config_path = Path(sys.argv[1])

    if not config_path.exists():
        print(f"Config file not found: {config_path}")
        sys.exit(1)

    config = load_config(config_path)
    print_config(config)


if __name__ == "__main__":
    main()