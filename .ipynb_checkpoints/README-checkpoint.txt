# StressTest (Locust)


# Description
- ```locustfile.py``` - Locust file with tasks. Emulates user behavior.
- ```monitor_resources.py``` - Collect host resourse info.
- ```docker_resourses.py``` - Collect resourse info by docker container.
- ```convert_qa_logs.py``` - Convert logs to human readable format.

# Run
```
locust -f locustfile.py --host=http://ip:port --web-port 0000
python3 docker_resourses.py
python3 monitor_resources.py
```