from typing import List


def format_instance_description(instance_types: dict) -> List:
    """
    Generates a list of formatted instance descriptions from a dictionary of pod resource specifications.
    """
    formatted_list = []
    for instance, specs in instance_types.items():
        cpu = specs["cpu"]
        memory = specs["memory"]

        if memory.endswith("Gi"):
            memory_in_gb = int(memory[:-2])
            formatted_memory = f"{memory_in_gb} GB (RAM)"
        elif memory.endswith("Mi"):
            memory_in_mb = int(memory[:-2])
            formatted_memory = f"{memory_in_mb} MB (RAM)"

        description = f"{instance} {cpu} Cores, {formatted_memory}"
        formatted_list.append({instance: description})

    return formatted_list
