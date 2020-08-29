
* CREATE ReplicaSet
```
kubectl create -f replicaset-definition.yml
```
* Get pods and replicaset
```
kubectl get replicaset
kubectl get pods
```
* Test replicaset, delete one of the `pod` and then get pods again.
```
kubectl delete pod <name-of-pod-from-replicaset>
kubectl get pods -o wide
```

### YAML

* Root level properties.
```yml
apiVersion: app/v1
kind: ReplicaSet
metadata:
spec:
```
* Name the ReplicaSet: `frontend`, add labels `app` and tier.
```yml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
    name: frontend
    labels:
        app: mywebsite
        tier: frontend
spec:
```
* ReplicaSet has 3 fields: `replicas`, `template` and `selector`. The number of `replicas` is 4
```yml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: frontend
  labels:
    app: mywebsite
    tier: frontend
spec:
    replicas: 4
    template:
    selector:
```
* Copy the contents of the `pod's yaml file` except for the `apiVersion` and `kind` and place it under the `template` section.
```yml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: frontend
  labels:
    app: mywebsite
    tier: frontend
spec:
  replicas: 4
  template:
    metadata:
      name: myapp-pod
      labels:
        app: myapp
    spec:
      containers:
        - name: nginx
          image: nginx
  selector:
```
* Add a property `matchLabels` under `selector` and copy the defined from `pod definition` under it.
```yml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: frontend
  labels:
    app: mywebsite
    tier: frontend
spec:
  replicas: 4
  template:
    metadata:
      name: myapp-pod
      labels:
        app: myapp
    spec:
      containers:
        - name: nginx
          image: nginx
  selector:
    matchLabels: 
        app: myapp
```