# QoS Test Plan

| ID | Test | Expected Result | Evidence |
|---|---|---|---|
| QOS-01 | Voice classification | Intended voice traffic matches class | Class-map counters |
| QOS-02 | Marking policy | Trusted boundary applies expected marking | Packet/policy evidence |
| QOS-03 | Queueing under congestion | Voice class receives configured treatment | Queue/policy counters |
| QOS-04 | Non-voice traffic | Other classes retain configured service | Policy counters |
| QOS-05 | WAN interface policy | Policy is attached to intended interface/direction | Interface policy output |

## Execution Record
Record traffic generator, link rate, policy, observed counters and measured results. Do not claim voice quality improvement without measurements.
