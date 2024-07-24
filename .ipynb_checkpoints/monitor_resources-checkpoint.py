import psutil
import time
import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import GPUtil

#interval_seconds = 5
def monitor_resources(duration_hours=0.33, output_file="resource_usage.json"):
    duration_seconds = duration_hours * 3600
    end_time = time.time() + duration_seconds
    data = []

    while time.time() < end_time:
        timestamp = datetime.now().isoformat()
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        
        # GPU usage
        gpus = GPUtil.getGPUs()
        gpus = [gpu for gpu in gpus if gpu.memoryTotal]
        gpu_usages = [gpu.load * 100 for gpu in gpus]  
        gpu_mem_usages = [gpu.memoryUsed / gpu.memoryTotal * 100 for gpu in gpus]  
        data_point = {
            "timestamp": timestamp,
            "cpu_usage (%)": cpu_usage,
            "memory_used (GB)": memory_info.used / (1024 ** 3),  
            "memory_total (GB)": memory_info.total / (1024 ** 3),  
            "gpu_usages (%)": gpu_usages,
            "gpu_mem_usages (%)": gpu_mem_usages
        }

        data.append(data_point)

        # Calculate and print the remaining time
        remaining_time = end_time - time.time()
        remaining_time_str = str(timedelta(seconds=int(remaining_time)))
        print(f"Time remaining: {remaining_time_str}")

        time.sleep(1)  

    with open(output_file, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Data collection complete. Data saved to {output_file}")

def plot_resource_usage(input_file="resource_usage.json"):
    with open(input_file, "r", encoding='utf-8') as f:
        data = json.load(f)

    timestamps = [datetime.fromisoformat(d["timestamp"]) for d in data]
    cpu_usage = [d["cpu_usage (%)"] for d in data]
    memory_used = [d["memory_used (GB)"] for d in data]  
    memory_total = data[0]["memory_total (GB)"]  
    gpu_usages = [sum(d["gpu_usages (%)"]) / len(d["gpu_usages (%)"]) if d["gpu_usages (%)"] else 0 for d in data]
    gpu_mem_usages = [sum(d["gpu_mem_usages (%)"]) / len(d["gpu_mem_usages (%)"]) if d["gpu_mem_usages (%)"] else 0 for d in data]

    plt.figure(figsize=(25, 15))

    # CPU usage
    plt.subplot(4, 1, 1)
    plt.plot(timestamps, cpu_usage, label="CPU Usage (%)")
    plt.xlabel("Time")
    plt.ylabel("CPU Usage (%)")
    plt.title("CPU Usage Over Time")
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    

    # Memory usage
    plt.subplot(4, 1, 2)
    plt.plot(timestamps, memory_used, label="Memory Used (GB)")
    #plt.axhline(y=memory_total, color='r', linestyle='--', label="Total Memory (GB)")
    plt.xlabel("Time")
    plt.ylabel("Memory Used (GB)")
    plt.title(f"Memory Usage Over Time (Total = {memory_total} GB)")
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    #plt.tight_layout()

    # GPU Usage
    plt.subplot(4, 1, 3)
    plt.plot(timestamps, gpu_usages, label="GPU Usage (%)")
    plt.xlabel("Time")
    plt.ylabel("Usage (%)")
    plt.title("GPU Usage Over Time")
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    #plt.tight_layout()


    # GPU Memory Usage
    plt.subplot(4, 1, 4)
    plt.plot(timestamps, gpu_mem_usages, label="GPU Memory Usage (%)")
    plt.xlabel("Time")
    plt.ylabel("Memory Usage (%)")
    plt.title("GPU Memory Usage Over Time")
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    plt.tight_layout()
    plt.savefig('resource_usage.png')

    
if __name__ == "__main__":
    
    monitor_resources()
    plot_resource_usage()
