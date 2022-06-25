# Run instruction
- Configure resources in `config.json`
- Run container with `./run_containernet.sh`
- Inside container run `cd project && python3 ./containernet.py`
- After benchmarks, results are available in `results.csv` file

WARNING: If mininet deployment is stuck on creating switch, you probably need to install `openvswitch-switch`
```bash
# Ubuntu 20.04
sudo apt install openvswitch-switch
```

## DragonflyDB internal metrics
Metrics fo prometheus stack are available at `localhost:6379/metrics`. In order to run prometheus-grafana stack:
```
docker-compose -f grafana-compose.yaml up
```
`dashboard.json` contains simple dashboard to import in Grafana.

## Used benchmarks
DragonflyDB uses same API as Redis. We used `redis-benchmark` and `memtier_benchmark` tool to put it under stress [Blog post about redis-benchmark](https://www.digitalocean.com/community/tutorials/how-to-perform-redis-benchmark-tests)