import matplotlib.pyplot as plt

def load_data(path):
    with open(path) as f:
        return [float(line.strip()) * 1000 for line in f]  # seconds → ms

cold = load_data("benchmarks/data/cold.txt")
warm = load_data("benchmarks/data/warm.txt")

plt.figure()
plt.plot(cold, marker="o", label="Cold cache (MISS)")
plt.plot(warm, marker="o", label="Warm cache (HIT)")
plt.xlabel("Request number")
plt.ylabel("Response time (ms)")
plt.title("Nginx Cache Performance Comparison")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("benchmarks/graphs/cache_performance.png")
plt.show()
