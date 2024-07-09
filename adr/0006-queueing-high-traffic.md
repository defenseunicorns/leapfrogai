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

LeapfrogAI has to be able to handle a large volume of inference, file upload, and embeddings requests. To ensure that we can handle this level of activity without significant performance degradation we need to have systems in place to prevent the system from being overwhelmed or blocked by any one task. 

## Decision
[Describe the decision made]

## Rationale
[Describe the potential consequences and impacts of the decision]

## Alternatives
Queueing
* RabbitMQ
* Supabase Realtime
* Kafka
* Custom Python solution

## Related ADRs
[List any related ADRs, if applicable]

## References
[List any references or resources used]