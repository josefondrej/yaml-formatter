import yaml
from colorama import Fore, Style
from typing import Dict, List
import sys

VALUE_MAX_LEN = 100


def format_env_vars(env_vars: List, prefix: str = "") -> str:
    output = ""
    for env in env_vars:
        env_name = env["name"]
        env_value = env.get("value") or "valueFrom ..."
        if len(env_value) > VALUE_MAX_LEN:
            env_value = env_value[:VALUE_MAX_LEN] + "..."
        output += prefix + f"{Fore.LIGHTMAGENTA_EX}{env_name}{Style.RESET_ALL} = {env_value}\n"

    return output


def format_volume_mounts(volume_mounts: List, prefix: str = "") -> str:
    output = ""
    for volumeMount in volume_mounts:
        path = volumeMount["mountPath"]
        name = volumeMount["name"]
        output += prefix + f"{path} < {Fore.LIGHTMAGENTA_EX}{name}{Style.RESET_ALL}\n"

    return output


def format_container(container: Dict, prefix: str = "") -> str:
    image = container["image"]
    command = container.get("command") or "No command"

    output = ""
    output += prefix + f"{Fore.LIGHTCYAN_EX}Image:{Style.RESET_ALL} {image}\n"
    output += prefix + f"{Fore.LIGHTCYAN_EX}Command: {Style.RESET_ALL} {command}\n"

    output += prefix + f"{Fore.LIGHTCYAN_EX}Volume mounts: {Style.RESET_ALL}\n"
    output += format_volume_mounts(container["volumeMounts"], 2 * prefix)

    output += prefix + f"{Fore.LIGHTCYAN_EX}Envirnomental variables: {Style.RESET_ALL}\n"
    output += format_env_vars(container["env"], 2 * prefix)

    output += "\n"
    return output


def format_volume(volume: Dict, prefix: str = "") -> str:
    volume_name = volume["name"]

    output = ""
    output += prefix + f"{Fore.LIGHTMAGENTA_EX}{volume_name}{Style.RESET_ALL}"

    if volume.get("secret") is not None:
        volume_type = "secret"
        name = volume["secret"]["secretName"]

    if volume.get("configMap") is not None:
        volume_type = "configMap"
        name = volume["configMap"]["name"]

    output += f" < {name} [{volume_type}]\n"
    return output


def format_deploy(deploy: Dict, prefix: str = "") -> str:
    spec = deploy["spec"]
    containers = spec["containers"]
    init_containers = spec["initContainers"]
    volumes = spec["volumes"]

    output = ""
    for container in containers:
        container_name = container["name"]
        output += prefix + f"{Fore.LIGHTYELLOW_EX}CONTAINER{Style.RESET_ALL} [{container_name}]\n"
        output += format_container(container, prefix)

    for container in init_containers:
        container_name = container["name"]
        output += prefix + f"{Fore.LIGHTYELLOW_EX}INIT CONTAINER{Style.RESET_ALL} [{container_name}]\n"
        output += format_container(container, prefix)

    output += prefix + f"{Fore.LIGHTYELLOW_EX}VOLUMES{Style.RESET_ALL}\n"
    for volume in volumes:
        output += format_volume(volume, prefix)

    return output


if __name__ == "__main__":
    data = "".join(sys.stdin.readlines())
    deploy = yaml.safe_load(data)
    formatted_deploy = format_deploy(deploy, "    ")

    print(formatted_deploy)
