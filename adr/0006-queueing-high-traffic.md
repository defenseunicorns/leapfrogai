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

LeapfrogAI has to be able to handle a large volume of inference, file upload, and embeddings requests. To ensure that we can handle this level of activity without significant performance degradation we need to have systems in place to prevent the system from being overwhelmed or blocked by a large volume or a single long running task. 
Adding a Queue management component can help us create a more efficient request management system to deal with high request volumes of long-running tasks. However, it introduces a significant level of complexity to the system, and we must weigh the options carefully.

### Benefits of Queue system for request processing:
- Allows the Gateway to respond even when the back-end is very busy
- Prevents request from being dropped or timing out
- Allows resuming failed requests
- Allows to throttle message processing rate
## Decision
[Describe the decision made]

## Rationale
[Describe the potential consequences and impacts of the decision]

## Alternatives
Queueing
* RabbitMQ
* Supabase Realtime
* Kafka
* Celery
* Custom Python solution

## Related ADRs
[List any related ADRs, if applicable]

## References
[List any references or resources used]
