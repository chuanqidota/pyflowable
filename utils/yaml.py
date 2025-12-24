from typing import Dict, Any

import yaml


def load_yaml_config(config_path: str) -> Dict[str, Any]:
    """加载 YAML 配置文件"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)
