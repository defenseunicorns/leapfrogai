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
- Allows the Gateway to respond even when the back-end is very busy
- Prevents requests from being dropped or timing out
- Allows resuming failed requests
- Enables throttling of message processing rate

## Decision

We have decided to implement a multi-tiered approach to address the queueing and high traffic challenges:

1. Address underlying bottlenecks in the system:
   - Optimize endpoint implementations, processing of long-running tasks, and indexing of files.
   - Reduce duplication of indexing efforts.
   - Scale horizontal/vertical resources as needed.

2. Implement a lightweight queueing solution using Supabase Realtime and FastAPI background tasks:
   - Utilize Supabase Realtime for real-time db updates and basic queueing
   - Leverage FastAPI's background tasks for handling non-blocking, asynchronous operations

3. Prepare for future scaling by designing the system to easily integrate with a more robust queueing solution:
   - Design interfaces that can work with both our current lightweight solution and future, more robust options
   - Do not attempt to push Supabase Realtime beyond its designed limits, instead plan to use RabbitMQ or Celery if those needs surface

## Rationale
1. Addressing underlying bottlenecks:
   - This approach ensures we're not masking performance issues with a queueing system
   - Optimizations can significantly improve system performance without adding complexity

2. Lightweight solution (Supabase Realtime and FastAPI background tasks):
   - Leverages existing infrastructure (Supabase) reducing additional operational overhead
   - FastAPI background tasks provide a simple way to handle asynchronous operations without introducing new dependencies
   - This solution meets our current needs without over-engineering

3. Preparation for future scaling:
   - Allows for easy transition to more robust solutions as the system grows
   - Prevents lock-in to a solution that may not meet future needs

We chose this approach over alternatives for several reasons:
- Kafka is considered too heavy for our current needs and would introduce unnecessary complexity
- A custom Python solution would require unnecessary development effort given the tools already available
- This tiered approach allows us to start with a simple solution while preparing for future growth

## Alternatives
Queueing Solutions Considered:
* RabbitMQ: Robust but potentially overkill for current needs
* Supabase Realtime: Lightweight and already integrated, but may not meet larger queuing needs
* Kafka: Powerful but too heavy for our current requirements
* Celery: Good option for Python-based systems, but introduces additional dependencies
* Custom Python solution: Flexible but requires significant development effort

## Related ADRs
[List any related ADRs, if applicable]

## References
1. Supabase Realtime Documentation: https://supabase.com/docs/guides/realtime
2. FastAPI Background Tasks: https://fastapi.tiangolo.com/tutorial/background-tasks/
3. Celery Documentation: https://docs.celeryq.dev/en/stable/
