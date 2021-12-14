# Scalable-MNIST-on-Kubernetes
This is a course project repository for the class NYU CSCI-GA 3033 Special Topics: Cloud and Machine Learning


## 1 Kubernetes Clusters

### Login

```bash
# Log in to your IBM Cloud account
ibmcloud login -a cloud.ibm.com -r us-east -g 2021-fall-student-yk2516

# Set the Kubernetes context to your cluster for this terminal session.
ibmcloud ks cluster config --cluster c6hu044w0jh603bfh57g

```

### Deploy the Server on Kubernetes Cluster

#### server-all.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
    name: infer
    labels:
        app: api
spec:
    replicas: 3
    selector:
        matchLabels:
            app: api
    template:
        metadata:
            labels:
                app: api
        spec:
            containers:
                - name: infer
                  image: charllechen/mnist-k8s
                  ports:
                      - containerPort: 5000
---
apiVersion: v1
kind: Service
metadata:
  name: infer-end
spec:
  type: LoadBalancer
  selector:
    app: api
  ports:
  - name: my-balance
    protocol: TCP
    port: 5000
    targetPort: 5000
```

### Docker for Client

```bash
# Build docker images
docker build -f Dockerfile -t project2_client .

# Inspect docker images
docker images

# Tag the docker images
docker tag project2_client yilunkuang/project2-client:latest

# Push the image to dockerhub
docker push yilunkuang/project2-client:latest
```

### Deploy the Client on Kubernetes Cluster

#### client-job.yaml

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: request
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
      - image: yilunkuang/project2-client:latest
        name: client-request
        ports:
          - containerPort: 5000  
        volumeMounts:
        - name: my-volume
          mountPath: /mount-path
      volumes:
      - name: my-volume
        persistentVolumeClaim:
          claimName: mnist-app-pvc
```

#### Deployment Command

```bash
# (optional) If there are job requests
kubectl delete job request
kubectl apply -f client-job.yaml

# Check running status
kubectl get pods
kubectl get job
```

#### Debug

```bash
kubectl logs [POD_NAME]
# kubectl logs request--1-n8jtc
```

#### Go into the /mount-path/ directory to retrieve the file

```bash
kubectl exec -it my-deployment-86cf478d55-9qz9r -- bash
cd /mount-path/
cat sample.txt
```

## 2 NYU Greene GPU Cluster

### Server

```bash
ssh yk2516@greene.hpc.nyu.edu
cd /scratch/yk2516/
srun --nodes=1 --tasks-per-node=1 --cpus-per-task=1 --mem=32GB --time=3:00:00 --gres=gpu:1 --pty /bin/bash

singularity exec --nv --overlay $SCRATCH/overlay-50G-10M.ext3:ro /scratch/work/public/singularity/cuda10.1-cudnn7-devel-ubuntu18.04-20201207.sif /bin/bash

python server_gpu.py
```

### Client

```bash
# attempt to POST at the login node
curl -X POST -F 'image=@test.png' http://10.32.35.163:5000/inference

srun --nodes=1 --tasks-per-node=1 --cpus-per-task=1 --mem=32GB --time=2:00:00 --pty /bin/bash

python3 client_gpu.py > client_log.txt
```

## 3 Data Processing and Plotting

```bash
# Copy the files from NYU Greene HPC to local directory, and performs the following
cat [FOLDER_NAME]/100threads_10requests.txt | sed 's/thread .*//' | grep -Eo '[+-]?[0-9]+([.][0-9]+)?' > [FOLDER_NAME]/p100threads_10requests.txt
cat [FOLDER_NAME]/100threads_100requests.txt | sed 's/thread .*//' | grep -Eo '[+-]?[0-9]+([.][0-9]+)?' > [FOLDER_NAME]/p100threads_100requests.txt
cat [FOLDER_NAME]/100threads_1000requests.txt | sed 's/thread .*//' | grep -Eo '[+-]?[0-9]+([.][0-9]+)?' > [FOLDER_NAME]/p100threads_1000requests.txt
cat [FOLDER_NAME]/100threads_2000requests.txt | sed 's/thread .*//' | grep -Eo '[+-]?[0-9]+([.][0-9]+)?' > p100threads_2000requests.txt
cat [FOLDER_NAME]/100threads_4000requests.txt | sed 's/thread .*//' | grep -Eo '[+-]?[0-9]+([.][0-9]+)?' > p100threads_4000requests.txt
# Here [FOLDER_NAME] can be either kubernetes_data, kubernetes_data_3_workers, rtx8000_data, which corresponds to one CPU, three CPUs, and one GPU. 

# Run the code for plotting
python3 latency_plot.py
```
