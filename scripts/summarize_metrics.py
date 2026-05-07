import csv
import sys

def summarize(csv_path):
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    if not rows:
        return None
    
    # Filter out rows with 0 tokens if they are at the beginning
    start_idx = 0
    while start_idx < len(rows) and float(rows[start_idx]['llamacpp:tokens_predicted_total']) == 0:
        start_idx += 1
    
    if start_idx == len(rows):
        return None
    
    first_row = rows[start_idx]
    last_row = rows[-1]
    
    duration = float(last_row['t']) - float(first_row['t'])
    tokens = float(last_row['llamacpp:tokens_predicted_total']) - float(first_row['llamacpp:tokens_predicted_total'])
    throughput = tokens / duration if duration > 0 else 0
    
    avg_kv = sum(float(r['llamacpp:kv_cache_usage_ratio']) for r in rows[start_idx:]) / (len(rows) - start_idx)
    
    return {
        "throughput": throughput,
        "avg_kv": avg_kv,
        "duration": duration,
        "tokens": tokens
    }

if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"Summary for {path}:")
        s = summarize(path)
        if s:
            print(f"  Throughput: {s['throughput']:.2f} tok/s")
            print(f"  Avg KV Usage: {s['avg_kv']*100:.1f}%")
        else:
            print("  No data")
