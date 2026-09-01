# Deploying the 珍丸茶室 Pearl & Co. scroll-world demo

Static site under `demo/`. No build step.

## Docker

```bash
docker build -t pearl-scroll-world:local -f deploy/Dockerfile .
docker run --rm -p 8080:80 pearl-scroll-world:local
# http://127.0.0.1:8080/
```

## Kubernetes / k3s

This environment has **no live k3s/kubectl cluster**. Manifests are ready to apply when you have one:

```bash
kubectl apply -f deploy/k8s/namespace.yaml
kubectl apply -f deploy/k8s/deployment.yaml
kubectl apply -f deploy/k8s/service.yaml
# optional ingress (edit host first)
kubectl apply -f deploy/k8s/ingress.yaml
```

Check:

```bash
kubectl -n scroll-world get pods,svc,ingress
kubectl -n scroll-world port-forward svc/pearl-demo 8080:80
```

## Notes

- Prefer a CDN/object store with **byte-range** support for large MP4s; the engine still works without ranges via blob fetch.
- Replace placeholder `demo/assets/**` before a production launch.
