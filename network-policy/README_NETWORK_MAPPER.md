# Network Mapper

> Process undergone to map connections in a cluster is described here

## Kubeshark

- not opensource
- costs money

## k8spacket

[k8spacket Github Link](https://github.com/k8spacket/k8spacket) 

- k8spacket used to map connections between pods
- did not work as expected
- each refresh of Grafana gave a new Diagram with different connections

## Otterize

### Network Mapper

- Network mapper used [k8s-network-mapper Docs](https://docs.otterize.com/features/network-mapping-network-policies/tutorials/k8s-network-mapper)

### Network Mapper Installation

Following commands installs the Network Mapper only.

- Linux CLI Installation

```
wget https://get.otterize.com/otterize-cli/v2.0.3/otterize_linux_x86_64.tar.gz
tar xf otterize_linux_x86_64.tar.gz
sudo cp otterize /usr/local/bin
```

- Helm Chart Installation

```
helm repo add otterize https://helm.otterize.com
helm repo update
helm install network-mapper otterize/network-mapper -n <namespace> --create-namespace --wait
```

- Traffic Mapping Command

```
otterize network-mapper visualize --mapper-namespace <mapper_namespace>  -n <namespace_to_map> -o <path_to_image>.png
```

### Intent-Based Access Control (IBAC)

> For Now Irrelevant

[IBAC Docs](https://docs.otterize.com/overview/intent-based-access-control)

- More research required
