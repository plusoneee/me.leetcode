## Kubernetes Basics
ref: [kubernetes.io](https://kubernetes.io/docs/tutorials/kubernetes-basics/)

### Cluster up and running 
* `minikube` version command:
```
minikube version
```

* Start the cluster command to start a virtual machine and a k8s cluster is running in that VM.
```
minikube start
```

### Cluster version

* To check if `kubectl` is installed:
```
kubectl version
```
1. `client version` is the `kubectl` version.
2. `server version` is `Kubernetes` version.

### Cluster details

* View the cluster details by running `kubectl cluster-info`:
```
kubectl cluster-info
```
* View the Nodes in the cluster
```
kubectl get nodes
```
This command shows all Nodes that can be used to host our applications and can see that its status is ready (to accept applications for deployment).

### Deploy an app

* Deploy first app on Kubernetes with `kubectl create deployment` command. Where `kubernetes-bootcamp` is the deployment name and `gcr.io/google-samples/kubernetes-bootcamp:v1` is app image location which include the full repository url for images. 
```
kubectl create deployment kubernetes-bootcamp --image=gcr.io/google-samples/kubernetes-bootcamp:v1
```
* This performed a few things:
    * searched for suitable Node where an instance of application could be run.
    * scheduled the application to run on the Node.
    * configured the cluster to reschedule the instance on new Node when needed.

* List deployments command:
```
kubectl get deployments 
```
- The `READY` column shows the ratio of `CURRENT` to DESIRED replicas, `CURRENT` is the number of replicas running nowm, `DESIRED` is the configured number of replicas.
- The `UP-TO_DATE` is the number of replicas that were updated to match the desired(confihured) state.
- The `AVAILABLE` state shows how many replicas are actually AVAILABLE to the users.

### View app

* Pods that are running indide Kubernetes are running on a private and isolated network, the `kubectl` command can create a proxy that will forward communications into the cluster-wide, private network.
```
kubectl proxy
```
or open a secound terminal windows run the proxy:
```
echo -e "\n\n\n\e[92mStarting Proxy. After starting it will not output a response. Please click the first Terminal Tab\n"; 
kubectl proxy
```
After command, We have a connection between `host` and the Kubernetes cluster. The proxy enables direct access to the API from these terminals. All those APIs through the proxy endpoint. For example  query the version through API LIKE `curl http://localhost:8001/version`. If `Connection refused`, ensure that the `kubectl proxy started above is running`.

* Get the `pod` name and store in the enviroment `POD_NAME`:
```
export POD_NAME=$(kubectl get pods -o go-template --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}')
echo $POD_NAME
```  
To see the output of application, run `curl http://localhost:8001/api/v1/namespaces/default/pods/$POD_NAME/proxy/`

### Explore app

* Use `kubectl get` command and look for existing Pods:
```
kubectl get pods
```
* To view what containers are inside that Pod and What images are used to build those containers run `describe pods` command:
```
kubectl describe pods
```
The `describe` command can be used to get detailed information about most of the kubernetes primitives: node, pods, deployments.

* Retrieve these logs using `kubectl logs` command:
```
kubectl logs $POD_NAME
```

### Executing command on the container
* Use the `exec` command and use the name of the `Pod` as a parameter. For example list the environment variables:
The name of the container can be omitted if only have a single container in the Pod.
```
kubectl exec $POD_NAME env
```
* Start a bash session in the Pod's container.
```
kubectl exec -ti $POD_NAME bash
```

### Create a new service
* List the current Services from cluster
```
kubectl get services
```
Service name `kubernetes` is created by default when minikube starts the cluster. 

* To create a new service and expose it to external traffic use the expose command with parameter `NodePort`.
```
kubectl expose deployment/kubernetes-bootcamp --type="NodePort" --port 8000
```
* Get service again, will see a running `service` call `kubernetes-bootcamp` which received a unique `cluster-IP`, an `internal port` and `external-IP`(the IP of the Node)
```
kubectl get services
```
* Create an enviroment variable call `NODE_PORT` that has the value of the `Node` post assigned:
```
export NODE_PORT=$(kubectl get services/kubernetes-bootcamp -o go-template='{{(index .spec.ports 0).nodePort}}')
```
* Test that app is exposed outsidee of the cluster using `curl`:the IP of the Node and externally exposed port:
```
curl $(minikube ip):$NODE_PORT
```

### Using labels
* The Deployment created automatically a label for Pod, see the name of the label use `describe deployment` command:
```
kubectl describe deployment
```
* Use the label to query list of Pods. Use the `kubectl get pods` commamd with `-l` and the label values:
```
kubectl get pods -l run=kubernetes-bootcamp
```
* list the existing services:
```
kubectl get services -l run=kubernetes-bootcamp
```
* Get the name of the Pod and store it in the `POD_NAME` enviroment variable:
```
export POD_NAME=$(kubectl get pods -o go-template --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}')
```
* To apply a new label we use the `label` command followed by the object type, object name and the new label (Here pinned the application version to the Pod):
```
kubectl label pod $POD_NAME app=v1
```
* Check with the `describe` command:
```
kubectl describe pods $POD_NAME
```
* Query the list of pods using the new label:
```
kubectl get pods -l app=v1
```

### Delete a service
* To delete `Services` use `delete service` command. Label can be used also here:
```
kubectl delete service -l run=kubernetes-bootcamp
```
* Confirm that the service was removed:
```
kubectl get services
```
* To confirm that route is not exposed anymore use `curl $(minikube ip):$NODE_PORT` command.
* Confirm that the app is still running inside the pod: 
```
kubectl exec -ti $POD_NAME curl localhost:8080
```

### Scaling a deplyment
* List deployments (should have one pod.):
```
kubectl get deployment
```
* Scale the Deployment to 4 replicas using `kubectl scale` command:
```
kubectl scale deployments/kubernetes-bootcamp --replicas=4
```
* List deployment once again, the change was applied now have 4 instances of the application availble:
```
kubectl get deployment
```
* Check if the number of Pods changed:
```
kubectl get pods -o wide
```
There are 4 `Pods` with different IP addresses. 
* The changed was registered in the Deployment events log. To check that use the `describe` command:
```
kubectl describe deployments/kubernetes-bootcamp
``` 
There are 4 `replicas` now.

### Load Balancing
* To find out the `exposed IP` and `Port` use the `describe services` command:
```
kubectl describe services/kubernetes-bootcamp
```
* Create an environment variable called `NODE_PORT` that has a value as the `Node port`:
```
export NODE_PORT=$(kubectl get services/kubernetes-bootcamp -o go-template='{{(index .spec.ports 0).nodePort}}')
```
* Use `curl` command to the exposed IP and port.
```
curl $(minikube ip):$NODE_PORT
```
Excute the command multiple times then we will see that hit a different `Pod` with every request. 


### Update App
* List `deployment` and list `Pods`:
```
kubectl get deployments
kubectl get pods
```
* To view the current image version of the app, run `describe` command against the `Pods` (look at the `Image` field):
```
kubectl describe pods
```
* To update the image of the application to version 2, use the `set image` command, followed by the `deployment name` and the new image version:
```
kubectl set image deployments/kubernetes-bootcamp kubernetes-bootcamp=jocatalin/kubernetes-bootcamp:v2
```
will see `kubectl set image deployments/kubernetes-bootcamp kubernetes-bootcamp=jocatalin/kubernetes-bootcamp:v2` in terminal.
* Check the status of the new Pods, and view the old one terminating with the get pods command:
```
kubectl get pods
```

### Verify update
* To find out the exposed IP and Port we can use `describe service`:
```
kubectl describe services/kubernetes-bootcamp
```
* Create an environment variable called `NODE_PORT` that has the value of the Node port assigned:
```
export NODE_PORT=$(kubectl get services/kubernetes-bootcamp -o go-template='{{(index .spec.ports 0).nodePort}}')
```
* `curl` to the the exposed IP and port:
```
curl $(minikube ip):$NODE_PORT
```
we see that all Pods are running the latest version (v2).
* The update can be confirmed also by running a rollout status command:
```
kubectl rollout status deployments/kubernetes-bootcamp
```
* To view the current image version of the app, run a describe command against the Pods (now version 2 of the app):
```
kubectl describe pods
```

### Rollback an update
* Let's perform another update, and deploy image tagged as `v10`:
```
kubectl set image deployments/kubernetes-bootcamp kubernetes-bootcamp=gcr.io/google-samples/kubernetes-bootcamp:v10
```
* Use `get deployments` to see the status of the deployment:
```
kubectl get deployments
```
* Somthings is wrong, do not have the desired number of Pods available. List Pods again and `describe` command on the `Pods` give more insights:
```
kubectl get pods
kubectl describe pods
```
* There is no image called `v10` in the repository. Roll back to previously working version use the `rollout` undo command:
```
kubectl rollout undo deployments/kubernetes-bootcamp
```
The `rollou`t command reverted the deployment to the previous known state (v2 of the image). List again the Pods and check again the image deployed:
```
kubectl get pods
kubectl describe pods
```

### Kubernetes Pods
`Pods` are the atomic unit on the Kubernetes platform. When we create a Deployment on K8s that Deployment creates Pods with containers inside them. A Pod is represents a group of one or more application containers (such as Docker), and some shared resources for those containers. Those resources include:
- Shared storage: Volumes.
- Networking: A unique cluster IP address.
- Information about how to run each container, such as the container image version or specific ports to use.

### Kubernetes Nodes
A Pod run on a `Node`. Each Node is managed by the Master. A Node can have multiple pods, and the K8s master automatically handles scheduling the pods across the Nodes in the cluster. The master is automatic scheduling  takes into account the available resouces on each Node.

- `kubectl get` - list resources.
- `kubectl describe` - show detailed information about a resource.
- `kubectl logs` - print the logs from a container in a pod.
- `kubectl exec` - execute a command on a container in a pod.


### Rolling Update
Rolling updates allow the following actions:
- Promote an application from one environment to another (via container image update).
- Rollback to previous versions.
- Continuous Integration and Continuous Delivery of applications with zero downtime.