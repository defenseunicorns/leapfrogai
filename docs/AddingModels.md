# Adding a new Model

The [API Server](../api) has a dynamic discovery sidecar that mounts every configmap that has a label with a key `leapfrogai` in the `leapfrogai` namespace into the pod.  This allows models to be installed outside of the installation of the the leapfrogai platform.

The [Leapfrog Model Skeleton](https://github.com/defenseunicorns/leapfrog-model-skeleton) contains a chart that helps faciliate the creation of a model Zarf package.  To see how to use it, see some of the examples in the [models](../models/) folder