* CREATE `Pod` from `yaml` file:
```
kubectl create -f <yaml-file-path.yml>
```
* For example:
```
kubectl create -f pod-definition.yml
```
* Use `get pods` command check if Pod was created:
```
kubectl get pods
```
* DELETE `Pod`:
```
kubectl delete pods <name-of-pod>
```
