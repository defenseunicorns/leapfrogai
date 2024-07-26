# Queueing and High Traffic

## Table of Contents

- [Handling High Traffic](#Queueing-and-High-Traffic)
  - [Table of Contents](#table-of-contents)
  - [Status](#status)
  - [Background](#background)
  - [Decision](#decision)
  - [Rationale](#rationale)
  - [Alternatives](#alternatives)
  - [Related ADRs](#related-adrs)
  - [References](#references)

## Status

PROPOSED

## Context

LeapfrogAI needs to handle a large volume of inference, file upload, and embeddings requests. To ensure that we can manage this level of activity without significant performance degradation, we need to implement systems that prevent overwhelming or blocking by a large volume or single long-running task.

Adding a Queue management component can help create a more efficient request management system to deal with high request volumes of long-running tasks. However, it may introduce a significant level of complexity to the system, and we must weigh the options carefully.

Benefits of a Queue system for request processing:
- Allows the API to quickly respond even when the system is very busy.
- Prevents requests from being dropped or timing out.
- Allows resuming failed requests.
- Enables throttling of message processing rate.

## Decision

We have decided to implement a multi-tiered approach to address the queueing and high traffic challenges:

1. Address underlying bottlenecks in the system:
   - Optimize endpoint implementations, processing of long-running tasks, and indexing of files.
   - Reduce duplication of indexing efforts.
   - Scale horizontal/vertical resources as needed.

2. Implement a lightweight queueing solution using Supabase Realtime and FastAPI background tasks:
   - Utilize Supabase Realtime for task status updates (in-progress, complete, etc...) and basic queueing.
    - In the event of issues with Supabase Realtime, fallback to RedPanda.
   - Leverage FastAPI's background tasks to handle long running operations asynchronously in the background.

3. Prepare for future scaling by designing the system to easily integrate with a more robust queueing solution:
   - Design interfaces that can work with both our current lightweight solution and future, more robust options.
   - Do not attempt to push Supabase Realtime beyond its designed limits, instead plan to use RedPanda or RabbitMQ if those needs surface.

## Rationale
1. Addressing underlying bottlenecks:
   - This approach ensures we're not masking performance issues with a queueing system.
   - Optimizations can significantly improve system performance without adding complexity.

2. Lightweight solution (Supabase Realtime and FastAPI background tasks):
   - Leverages existing infrastructure (Supabase) reducing additional operational overhead.
   - FastAPI background tasks provide a simple way to handle asynchronous operations without introducing new dependencies.
   - This solution meets our current needs without over-engineering.

3. Preparation for future scaling:
   - Allows for easy transition to more robust solutions as the system grows.
   - Prevents lock-in to a solution that may not meet future needs.

We chose this approach over alternatives for a few reasons:
- This tiered approach allows us to start with a simple solution while preparing for future growth.
- Some alternatives are viable but would likely require significant additional setup and mx work to bring to the current environment.
  - The additional setup includes but is not limited to: new Zarf packages, updates to uds bundles, spikes to integrate with current app, resolving any permissions/hardening issues, more containers to add to ironbank/chainguard.
- When performing load testing on the system, the primary bottlenecks seem to be around the vectordb file indexing.
  - The issues related to this process should be able to be resolved by optimizations, a light amount of queueing, and background tasks.
  - Issues not related to indexing were primarily scalability issues. Which can be resolved via resource limits, throttling, improving horizontal and vertical scaling within the cluster.
- Authentication will be an issue for every solution except Supabase Realtime.

## Alternatives
Queueing Solutions Considered:
* RabbitMQ: Meets current and future needs.
  * Well maintained JS and Python libraries.
  * Requires additional, potentially significant integration work to bring into the k8s cluster.
* Supabase Realtime: Lightweight and already integrated, but may not meet all future queuing needs.
  * Well maintained JS and Python libraries.
  * Can listen directly to db transactions.
  * Already integrated with Supabase auth.
* Kafka: Powerful but too heavy for our current requirements.
  * Well maintained JS and Python libraries.
  * Requires additional, potentially significant integration work to bring into the k8s cluster.
* Celery: Good option for Python-based systems, but introduces additional dependencies.
  * Python library well maintained. JS library not well maintained.
* RedPanda: Accessible internally and provides a scalable solution.
  * Well maintained JS and Python libraries as it supports the same tooling as Kafka.
  * Zarf/UDS bundle already available.
* Custom Python solution: Flexible but requires significant unnecessary development effort given the tools already available.

## Related ADRs
* [0003-database](0003-database.md)

## References
1. Supabase Realtime Documentation: https://supabase.com/docs/guides/realtime
2. FastAPI Background Tasks: https://fastapi.tiangolo.com/tutorial/background-tasks/
3. Celery Documentation: https://docs.celeryq.dev/en/stable/
4. Kafka Documentation: https://kafka.apache.org/
5. RabbitMQ Documentation: https://www.rabbitmq.com/docs
6. RedPanda: https://docs.redpanda.com/docs/