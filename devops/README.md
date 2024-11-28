# eips.exposed Devops

## Helm

### Install new deployment

```bash
helm secrets install --dry-run --create-namespace -n eips eips devops/kubernetes/charts/eips \
    -f devops/kubernetes/charts/eips/values.yaml \
    -f devops/kubernetes/values/eips.yaml \
    -f devops/kubernetes/values/secrets.eips.enc.yaml
```

### Upgrade a deployment

```bash
helm secrets upgrade -n eips eips devops/kubernetes/charts/eips \
    -f devops/kubernetes/charts/eips/values.yaml \
    -f devops/kubernetes/values/eips.yaml \
    -f devops/kubernetes/values/secrets.eips.enc.yaml
```
