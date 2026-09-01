# Deploying the 珍丸茶室 Pearl & Co. scroll-world demo

Static site under `demo/`. No build step.

## Docker

```bash
docker build -t pearl-scroll-world:local -f deploy/Dockerfile .
docker run --rm -p 8080:80 pearl-scroll-world:local
# http://127.0.0.1:8080/
```

## Kubernetes / k3s

Manifests under `deploy/k8s/` are structurally valid (Namespace / Deployment / Service / Ingress).
This Cloud Agent environment has **no Docker socket and no reachable k3s API**, so live
`kubectl apply` cannot complete here — validate YAML locally, then apply on your cluster:

```bash
# structural check (no cluster required)
python3 -c "import yaml,glob; [yaml.safe_load_all(open(p)) for p in glob.glob('deploy/k8s/*.yaml')]"

kubectl apply -f deploy/k8s/namespace.yaml
kubectl apply -f deploy/k8s/deployment.yaml
kubectl apply -f deploy/k8s/service.yaml
# optional ingress (edit host first)
kubectl apply -f deploy/k8s/ingress.yaml
```

Build the image on a node that can pull/build, then load it into k3s (`k3s ctr images import` /
`docker save | k3s ctr images import`) so `pearl-scroll-world:local` resolves.

Check:

```bash
kubectl -n scroll-world get pods,svc,ingress
kubectl -n scroll-world port-forward svc/pearl-demo 8080:80
```

## Notes

- Prefer a CDN/object store with **byte-range** support for large MP4s; the engine still works without ranges via blob fetch.
- Replace placeholder `demo/assets/**` before a production launch (cream + accent stills / zoom loops).
