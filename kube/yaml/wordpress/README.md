
* Create `namespace`
```
kubectl create namespace sl-wordpress
```
* Edit the file `wp-secrete` and then create it:
```
kubectl apply -f wp-secrete
```
* PV and PVC (Edit `hostPath` in pv.yml)
```
kubectl apply -f wp-pv.yml
kubectl apply -f wp-pvc.yml
```
* Deployment and Service:
```
kubectl apply -f wp-service.yml 
kubectl apply -f wp-deployment.yml 
```
* Get Service Url where `wordpress-service` is service name.
```
minikube service wordpress-service --url  
```