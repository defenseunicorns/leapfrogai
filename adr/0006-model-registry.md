# Model Registry

## Table of Contents
- [Model Registry](#model-registry)
  - [Table of Contents](#table-of-contents)
  - [Status](#status)
  - [Context](#context)
  - [Decision](#decision)
  - [Rationale](#rationale)
  - [Alternatives](#alternatives)
    - [KServe](#kserve)
        - [KServe w/ S3 Buckets](#kserve-w-s3-buckets)
        - [KServe w/ OCI Registry](#kserve-w-oci-registry)
    - [Raw PVC Attachments](#raw-pvc-attachments)
  - [Related ADRs](#related-adrs)
  - [References](#references)

## Status
Proposed

## Context
GenerativeAI models are big. Because LeapfrogAI is designed to be deployable into AirGapped environments, we need to ensure that we are bringing the big GenerativeAI models with us. Currently, we are brining the AI models with us by backing them into our container images. For example, [we download synthia into our llama-cpp-python image](https://github.com/defenseunicorns/leapfrogai/blob/d1e42d9296f6e014ffbbcec2ba295443b1675567/packages/llama-cpp-python/Dockerfile#L15) and here we [download whisper](https://github.com/defenseunicorns/leapfrogai/blob/d1e42d9296f6e014ffbbcec2ba295443b1675567/packages/whisper/Dockerfile#L14) into our whisper image. Some of the models we are trying to use are large (several GBs).

The approach of 'baking in' the model weights to our images was a simple solution to our problem of needing to ensure we had the weights available to us, but not an ideal one.  Here are the fallbacks of this approach:
- We have large images that are harder to manage because of their size.
	- Pushing/pulling from GHCR takes more time.
	- Pushing large images to a Zarf Registry often [fails](https://github.com/defenseunicorns/zarf/issues/2104).
- We are unable to quickly/effectively use different models.
	- Wanting to try a different LLM involves rebuilding the entire image, instead of only changing the model at runtime.
- Larger images take longer to initialize within Kubernetes.
	- The initialization time of pods is increased because of time spent moving the containers OCI layers into the pod.

## Decision
While no decision has been made yet, I am leaning towards proposing we go with the simplest solution of using PVCs to manage our GenAI models.


## Rationale
N/A as no [Decision](#Decision) has been made yet.


## Alternatives

### KServe
While KServe is capable of doing a lot (inference, request batching, autoscaling, etc.), we are currently only going to be looking at its ability to assist in model storage and retrieval.

KServe uses a [Storage Container (initContainer)](https://kserve.github.io/website/master/modelserving/storage/storagecontainers/) to download the model during the Pods initialization. This initContainer downloads the model to a specified path for the application to use. This initContainers entire purpose is to abstract away the complexity of retrieving the model from your raw application. KServe supports several different potential sources for downloading. We will cover the options with the most potential below.

Pros of KServe Overall:
- KServe is a popular Open Source project which is a part of the KubeFlow ecosystem. This means we can likely leverage even more benefits in the near future.

Cons of KServe Overall:
- We are utilizing just a tiny piece of what KServe is, meaning we are adding a good amount of complexity for just that small piece.
- Solutions w/ KServe will need more cluster orchestration. We will either have to standup a [MinIO instance](https://github.com/defenseunicorns/uds-package-dependencies/blob/main/src/minio/zarf.yaml) or standup an [OCI Registry](https://github.com/defenseunicorns/uds-package-zot) within our cluster that we push our models to during deploy time.

##### KServe w/ S3 Buckets
[KServe S3 Docs](https://kserve.github.io/website/master/modelserving/storage/s3/s3/)
 One of the methods KServe natively supports is pulling models from an S3 bucket. [MinIO](https://min.io/docs/minio/kubernetes/upstream/) is an S3 compatible object store, meaning we can use MinIO for self-hosted and AirGapped environments and potentially use an AWS S3 bucket for online environments.

Pros of KServe w/ S3:
- Pretty easily adaptable to online/GovCloud s3 buckets
- Relatively simple to setup assuming you already have a managed instance of MinIO / AWS S3.

Cons of KServe w/ S3:
- Requires the local cluster have MinIO configured (OR requires access to upstream AWS S3 bucket that has been populated with the model)
- Hard to optimize re-deploys (If the model weights don't change we will likely still need to fully push the model to the bucket)

##### KServe w/ OCI Registry
[KServe OCI Docs](https://kserve.github.io/website/master/modelserving/storage/oci/)
KServe has an experimental feature in which they support using models that have been pushed to an OCI registry.


Pros of KServe w/ OCI Registry:
- Easy (free?) optimization of re-deploys. (If the model weights don't change, the OCI layers should be the same, so the push to the registry should complete a lot quicker)

Cons of KServe w/ OCI Registry:
- We might still have the same Zarf issue of [pushing large OCI artifacts to a registry](https://github.com/defenseunicorns/zarf/issues/2104)
- It is not immediately clear to me how we would push our OCI artifact into the registry.
	- Since populating the OCI registry will not use `kubectl` commands, Zarf does not expose any tools that will immediately help us with populating the OCI registry. We can likely put something together that will use [Zarf Actions](https://docs.zarf.dev/ref/actions/) but the future of Zarf Actions is a little shrouded as the Zarf teams moves to going GA so I am a little hesitant to hack together a solution until we see how the dust settles.
- KServe does not download and mount OCI artifacts the same way it does for the S3 artifacts. Instead, KServe uses an experiment feature that they're calling [Modelcars](https://kserve.github.io/website/master/modelserving/storage/oci/#enabling-modelcars)that runs the model as a sidecar that their [InferenceService](https://github.com/kserve/kserve/blob/ca691f728ac0fe6a711b2953a88abb1b3d532658/pkg/apis/serving/v1beta1/inference_service.go#L94) uses. This would require a good bit of rearchitecting on the LeapfrogAI end.

### Raw PVC Attachments
[k8s PVC Docs](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)

Maybe the simplest solution is the best solution? We can create a PersistantVolume for each model that gets populated during deploy time. This PersistantVolume will be mounted by all of the Pods that want to use that model.


Pros of PVC:
- Requires no new dependencies.
- Should have the shorted 'cold start' initialization time since Pods will only be mounting a PVC instead of pulling the model weights.


Cons of PVC:
- Hard to optimize re-deploys (If the model weights don't change) and benefit from caching.


## Related ADRs
N/A


## References
- [KServe Docs](https://kserve.github.io/website/latest/)
- [Zarf Docs](https://docs.zarf.dev/)
