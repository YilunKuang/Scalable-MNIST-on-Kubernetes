import numpy as np
import matplotlib.pyplot as plt

cluster_type = ['kubernetes_data','kubernetes_data_3_workers','rtx8000_data']
file_type = ['p100threads_10requests.txt',
             'p100threads_100requests.txt',
             'p100threads_1000requests.txt',
             'p100threads_2000requests.txt',
             'p100threads_4000requests.txt']

lst_path = []
for i in range(len(cluster_type)):
    for j in range(len(file_type)):
        lst_path.append(cluster_type[i]+'/'+file_type[j])

lst_latency = []
for i in range(len(lst_path)):
    float_lst = []
    with open(lst_path[i],"r") as file:
        for line in file.readlines():
            float_lst.append(float(line))
        lst_latency.append(float_lst)

lst_mean = list(map(lambda x: np.mean(x), lst_latency))
lst_requests = [10, 100, 1000, 2000, 4000]
print(lst_mean)


# Visualize Raw
plt.figure()
for i in range(len(lst_requests)):
    plt.scatter(np.arange(1,101,1),lst_latency[i],c='C'+str(i),label='One CPU worker')
plt.xlabel("All 100 threads")
plt.ylabel("Time (sec)")
plt.title("Latency of all 100 threads for a single CPU node")
plt.show()

plt.figure()
for i in range(len(lst_requests)):
    plt.scatter(np.arange(1,101,1),lst_latency[i+5],c='C'+str(i),label='Three CPU worker')
plt.xlabel("All 100 threads")
plt.ylabel("Time (sec)")
plt.title("Latency of all 100 threads for three CPU nodes")
plt.show()

plt.figure()
for i in range(len(lst_requests)):
    plt.scatter(np.arange(1,101,1),lst_latency[i+10],c='C'+str(i),label='one GPU')
plt.xlabel("All 100 threads")
plt.ylabel("Time (sec)")
plt.title("Latency of all 100 threads for one GPU")
plt.show()

# Kubernetes Cluster | CPU vs. NYU Greene HPC | RTX8000
plt.figure()
plt.plot(lst_requests, lst_mean[:5])
plt.plot(lst_requests, lst_mean[5:10])
plt.plot(lst_requests, lst_mean[10:])
plt.scatter(lst_requests*len(cluster_type),lst_mean,c='r')
plt.xlabel("Numbers of requests per 100 threads")
plt.ylabel("Time (sec)")
plt.title("Comparison of Latency in the IBM Cloud Kubernetes Cluster vs. NYU Greene HPC")
plt.legend(['1 CPU nodes on Kubernetes','3 CPU nodes on Kubernetes''','One RTX8000 GPU'])
plt.show()

# Speedup
lst_speedup_one = np.divide(lst_mean[:5],lst_mean[10:])
lst_speedup_three = np.divide(lst_mean[5:10],lst_mean[10:])
plt.figure()
plt.plot(lst_requests, lst_speedup_one, c='C0')
plt.plot(lst_requests, lst_speedup_three,c='C1')
plt.xlabel("Numbers of requests per 100 threads")
plt.ylabel("Speedup (CPU time / GPU time)")
plt.title("Speedup of RTX8000 GPU over the IBM Cloud Kubernetes Cluster")
plt.legend(['one worker', 'three workers'])
plt.show()

