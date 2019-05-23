import yaml
from colorama import Fore, Style
from typing import Dict
import sys

VALUE_MAX_LEN = 100

def format_container(container: Dict, prefix: str = "", is_init: bool = False) -> str:
    output = ""
    container_flag = f"{Fore.YELLOW}INIT CONTAINER{Style.RESET_ALL}" if is_init else f"{Fore.YELLOW}CONTAINER{Style.RESET_ALL}"
    container_name = container["name"]
    image = container["image"]
    command = container.get("command") or "No command"
    output += prefix + f"{container_flag} [ {container_name} ]\n"
    output += prefix + f"{Fore.CYAN}Image:{Style.RESET_ALL} {image}\n"
    output += prefix + f"{Fore.CYAN}Command: {Style.RESET_ALL} {command}\n"

    output += prefix + f"{Fore.CYAN}Volume mounts: {Style.RESET_ALL}\n"
    for volumeMount in container["volumeMounts"]:
        path = volumeMount["mountPath"]
        name = volumeMount["name"]
        output += prefix + f"  {path} < {Fore.MAGENTA}{name}{Style.RESET_ALL}\n"

    output += prefix + f"{Fore.CYAN}Envirnomental variables: {Style.RESET_ALL}\n"
    for env in container["env"]:
        env_name = env["name"]
        env_value = env.get("value") or "valueFrom ..."
        if len(env_value) > VALUE_MAX_LEN:
            env_value = env_value[:VALUE_MAX_LEN] + "..."
        output += prefix + f"  {Fore.MAGENTA}{env_name}{Style.RESET_ALL} = {env_value}\n"

    output += "\n"
    return output

def format_volume(volume: Dict, prefix: str = "") -> str:
    output = ""
    volume_name = volume["name"]
    output += prefix + f"{Fore.GREEN}{volume_name}{Style.RESET_ALL}"

    if volume.get("secret") is not None:
        volume_type = "secret"
        name = volume["secret"]["secretName"]

    if volume.get("configMap") is not None:
        volume_type = "configMap"
        name = volume["configMap"]["name"]

    output += prefix + f" < {name} [{volume_type}]\n"
    return output


def format_deploy(deploy: Dict, prefix: str = "") -> str:
    spec = deploy["spec"]
    containers = spec["containers"]
    init_containers = spec["initContainers"]
    volumes = spec["volumes"]

    output = ""
    for container in containers:
        output += format_container(container, prefix)

    for container in init_containers:
        output += format_container(container, prefix, True)

    output += prefix + f"{Fore.YELLOW}VOLUMES{Style.RESET_ALL}\n"
    for volume in volumes:
        output += format_volume(volume, prefix)

    return output

if __name__ == "__main__":
    data = "".join(sys.stdin.readlines())
    deploy = yaml.safe_load(data)
    formatted_deploy = format_deploy(deploy, "  ")

    print(formatted_deploy)


