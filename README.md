# Namespace provisioner for Tanzu App Platform

This repo contains a function which will perform most(1) of the [provisioning for a developer namespace required by Tanzu Application Platform](https://docs.vmware.com/en/VMware-Tanzu-Application-Platform/1.1/tap/GUID-install-components.html#set-up-developer-namespaces-to-use-installed-packages-2).

(1) It does not populate a read-write developer registry credential (`registry-credential`). It could fill in a `secretgen-controller` secret for that, but then you'd be sharing the credential across namespaces. If you have a clever idea, feel free to file an issue or send a PR.

## Prerequisites

* [Tanzu Application Platform](https://docs.vmware.com/en/VMware-Tanzu-Application-Platform/1.1/tap/GUID-overview.html), version 1.1 or newer
* The [Functions workload](https://docs.vmware.com/en/VMware-Tanzu-Application-Platform/1.1/tap/GUID-workloads-using-functions.html) support loaded on your cluster
* [Metacontroller](https://metacontroller.github.io/metacontroller/guide/install.html#install-metacontroller-using-kustomize) installed on your cluster

## Installation

Install this function using the [deployment instructions for the functions workload](https://docs.vmware.com/en/VMware-Tanzu-Application-Platform/1.1/tap/GUID-workloads-using-functions.html#deploy-your-function-6). The configuration in this repo suggests installing in the `tap-support` namespace using the function name `annotate-tap-dev-ns`, but you can customize both of these parameters. Note that you'll need to _manually_ provision this namespace to bootstrap the process.

Once the function is running, apply the [`metacontroller.yaml`](./metacontroller.yaml) manifest, possibly customizing the `specs.hooks.sync.webhook.url` parameter to point to your deployed version of the function.

## Usage

As you can see from [`metacontroller.yaml`](./metacontroller.yaml#L11), the function will operate on namespaces labelled with the `tap.tanzu.vmware.com` label and any value. (The value of the label is not currently used.) To add this label to a namespace:

```bash
kubectl label ns $MY_NS tap.tanzu.vmware.com=yes
```

You can also do this via YAML using the normal `labels` field in `metadata`, but people seem to like command-line options.
