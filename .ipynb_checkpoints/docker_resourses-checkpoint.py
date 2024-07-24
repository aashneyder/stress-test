import subprocess
import time
import json
import matplotlib.pyplot as plt
from datetime import datetime

container_ids = ["7e195dbd8e49", "d90ed7fc193e"]
container_names = ["neon-api_neon-api", "ui_neon-ui"]
interval = 120

duration = 1300

data = {container_id: {"time": [], "cpu": [], "memory": []} for container_id in container_ids}

def get_docker_stats(container_ids):
    result = subprocess.run(
        ["docker", "stats", "--no-stream", "--format", "{{ json . }}"] + container_ids,
        capture_output=True,
        text=True
    )
    stats = result.stdout.strip().split("\n")
    return [json.loads(stat) for stat in stats]

def parse_cpu(value):
    return float(value.strip('%'))

def parse_memory(value):
    if value.endswith('GiB'):
        return float(value.strip('GiB')) 
    elif value.endswith('MiB'):
        return float(value.strip('MiB')) / 1024
    return float(value.strip('B')) / (1024 * 1024)

    
def main():
    start_time = time.time()
    while time.time() - start_time < duration:
        stats = get_docker_stats(container_ids)
        current_time = datetime.now().strftime("%H:%M:%S")
        
        for stat in stats:
            container_id = stat["ID"]
            data[container_id]["time"].append(current_time)
            data[container_id]["cpu"].append(parse_cpu(stat["CPUPerc"]))
            data[container_id]["memory"].append(parse_memory(stat["MemUsage"].split(' / ')[0]))
        
        time.sleep(interval)
    
    plt.figure(figsize=(20, 10))

    for i in range(len(container_ids)):
        plt.subplot(2, 1, 1)
        plt.plot(data[container_ids[i]]["time"], data[container_ids[i]]["cpu"], label=f'CPU {container_names[i]}')
        plt.ylabel('CPU Usage (%)')
        plt.xlabel('Time')
        plt.legend()

        plt.subplot(2, 1, 2)
        plt.plot(data[container_ids[i]]["time"], data[container_ids[i]]["memory"], label=f'Memory {container_names[i]}')
        plt.ylabel('Memory Usage (GB)')
        plt.xlabel('Time')
        plt.legend()

    plt.tight_layout()
    plt.savefig('docker_resourses_usage_neon.png')


if __name__ == "__main__":
    main()
