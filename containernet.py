from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.clean import cleanup

import pandas
import json
import io
import itertools

from collections import defaultdict

def start_mininet(cpu, memory):
    cpu_period = 100000
    cpu_quota = int(cpu * cpu_period)
    mem_limit = int(memory)

    cleanup()
    net = Containernet(controller=Controller)
    net.addController('c0')


    db1 = net.addDocker(
        'db1',
        ip="10.0.0.251",
        dimage="dragonflydb",
        ports=[6379],
        port_bindings={6379:6379},
        dcmd=['dragonfly'],
        mem_limit=f"{mem_limit}m",
        cpu_period=cpu_period,
        cpu_quota=cpu_quota,
    )
    h1 = net.addDocker(
        'h1',
        ip='10.0.0.252',
        dimage='bench',
        ports=[8080],
        port_bindings={8080:8080},
    )
    s1 = net.addSwitch('s1')

    net.addLink(db1, s1)
    net.addLink(s1, h1)
    net.start()
    return net, h1, db1

with open("config.json") as conf:
    config = json.load(conf)
final_dict = defaultdict(lambda: [])

for cpu, memory in itertools.product(config['cpu'], config['memory']):
    net, h1, db1 = start_mininet(cpu, memory)
    print("==========================")
    print("TEST SUITE:")
    print(f"\tCPU: {cpu}")
    print(f"\tMemory: {memory}MB")
    print("==========================")
    
    # Crazy hax to run command through CLI since h1.cmd caused some time related problems
    CLI(net, script="./bench_scripts/redis.sh")
    rb_csv = h1.cmd(f"cat rb.csv")
    memtier_json = h1.cmd(f"cat mt.json")
    redis_res = pandas.read_csv(io.StringIO(rb_csv), index_col=0, header=None).T.to_dict('list')
    data = json.loads(memtier_json)
    data = {
        'CPU': [cpu],
        'Memory limit [MB]': [memory],
        'Requests per client': [data["run information"]["Requests per client"]],
        'Total duration': [data["ALL STATS"]["Runtime"]["Total duration"]],
        'Start time': [data["ALL STATS"]["Runtime"]["Start time"]],
        'Ops/sec': [data["ALL STATS"]["Sets"]["Ops/sec"]],
        'Average Latency': [data["ALL STATS"]["Sets"]["Average Latency"]],
        'Min Latency': [data["ALL STATS"]["Sets"]["Min Latency"]],
        'Max Latency': [data["ALL STATS"]["Sets"]["Max Latency"]],
        'KB/sec': [data["ALL STATS"]["Sets"]["KB/sec"]],
        **redis_res
    }
    for k, v in data.items():
        final_dict[k].append(v[0])
    net.stop()

df = pandas.DataFrame.from_dict(final_dict)
df.to_csv('result.csv', index=False, header=True)
