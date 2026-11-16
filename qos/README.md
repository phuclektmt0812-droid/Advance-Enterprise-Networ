# Quality of Service

## Objective
Prioritize real-time voice traffic across constrained WAN links while protecting other business applications.

## Design
- Identify and classify voice signaling and media traffic based on the selected lab endpoints.
- Mark traffic at a trusted boundary; do not blindly trust endpoint markings.
- Map markings to a documented queueing policy.
- Apply shaping/policing only where link rates and platform support are known.
- Preserve bandwidth for business-critical data and management traffic.
- Document the actual WAN bottleneck rate before tuning.

## Validation
Generate representative voice and data traffic, inspect policy counters, and compare behavior under congestion. Save policy output and test observations. Do not claim measurable voice quality improvements without corresponding measurements.

## Status
Design baseline; device-specific QoS commands and rates remain pending.
