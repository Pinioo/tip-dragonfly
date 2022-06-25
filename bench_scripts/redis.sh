h1 echo "Running redis-benchmark..."
h1 redis-benchmark -h db1 --csv > rb.csv
h1 echo "END"
h1 echo "Running memtier_benchmark..."
h1 memtier_benchmark -s db1 --json-out-file=mt.json
h1 echo "END"