import os
import re
import json
import subprocess
from pathlib import Path
from typing import Any, Dict, AnyStr

from .common import get_platform
from .exceptions import NoEnvFoundError


class JsonParser(dict):
    def __init__(self, data: Dict = None):
        """Constructor

        :param data: Dictionary data to create json, defaults to None
        :type data: dict, optional
        """
        super().__init__(data or {})
        self.file_path = None

    @classmethod
    def load(cls, file_path: AnyStr):
        """Static method which reads existing json file and returns the instance

        :param file_path: json file path to read
        :type file_path: str
        :return: instance of the class having json data of the input file
        :rtype: JsonParser
        """
        with open(file_path, 'r') as f:
            jp = cls(data=json.load(f))
            jp.file_path = file_path
            return jp

    @classmethod
    def loads(cls, json_str: AnyStr):
        """Static method which reads the given json string and returns the instance

        :param json_str: json encoded string
        :type json_str: str
        :return: instance of the class having json data from the json sting
        :rtype: JsonParser
        """
        return cls(data=json.loads(json_str))

    def dump(self, file_path: AnyStr = None):
        """Exports the instance data to json file

        :param file_path: output json file path, defaults to None
        :type file_path: str, optional
        :raises ValueError: if file_path is null
        """
        self.file_path = file_path or self.file_path
        if not self.file_path:
            raise ValueError('No output json path given')

        # Create base directory
        base_dir = os.path.dirname(self.file_path)
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        with open(self.file_path, 'w') as f:
            json.dump(self, f, indent=4)

    def dumps(self):
        """Exports the instance data to json string

        :return: Json string data
        :rtype: str
        """
        return json.dumps(self, indent=4)


class EnvConfig(JsonParser):
    VAR_PATTERN = re.compile(r'\$\{([^}]+)\}')

    def __init__(self, data=None):
        """Constructor

        :param data: Dictionary data to create json, defaults to None
        :type data: dict, optional
        """
        super().__init__(data=data)

    def _resolve(self, value: Any, context: Dict[str, Any]) -> Any:
        if isinstance(value, str):
            return self._expand_string(value, context)
        elif isinstance(value, dict):
            return {k: self._resolve(v, context) for k, v in value.items()}
        elif isinstance(value, list):
            return [self._resolve(i, context) for i in value]
        else:
            return value

    def _expand_string(self, value: str, context: Dict[str, Any]) -> str:
        def replacer(match):
            var = match.group(1)
            # JSON key lookup (supports nested.key)
            try:
                keys = var.split(".")
                ref = context
                for key in keys:
                    ref = ref[key]
                if not (ref and isinstance(ref, (str, bytes))):
                    raise TypeError('Error')
                return self._expand_string(ref, context)
            except (KeyError, TypeError):
                return f"${{{var}}}"
        # Environment variable takes precedence over local value
        value = os.path.expandvars(value)
        return self.VAR_PATTERN.sub(replacer, value)

    def get_value(self, key: str, default=None) -> Any:
        value = self.get(key, default)
        return self._resolve(value, self)

    def __getitem__(self, key: str) -> Any:
        return self.get_value(key)


def get_envpref(envpref_path):
    envpref_path = Path(envpref_path)
    if envpref_path.exists():
        return JsonParser.load(envpref_path)
    envpref = JsonParser({})
    envpref.dump(envpref_path)
    return envpref


def manage_config(config):
    """Get/Set config of the environment

    :param config: Config of the environment
    :type config: EnvConfig
    """
    envs = get_envpref(config["envpref_path"])
    try:
        config_path = envs[config["env_name"]]
    except KeyError:
        raise NoEnvFoundError(f'Could not find comfyui environment: '
                              f'"{config["env_name"]}"')

    if config['edit']:
        system = get_platform()

        cmd = ['start', config_path]
        if system == 'Linux':
            cmd = ['xdg-open', config_path]
        elif system == 'Darwin':  # macOS
            cmd = ['open', config_path]
        # Open config file in text editor
        subprocess.Popen(cmd, shell=True)
        return

    print(config.dumps(), flush=True)
