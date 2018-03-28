# Requirement 2

The following questions are considering group 1 (trace1.pcapng, trace2.pcapng, trace3.pcapng, trace4.pcapng and trace5.pcapng).

1. Determine the number of probes per “ttl” used in each trace file.

All 5 trace files used 3 probes per TTL.

2. Determine whether or not the sequence of intermediate routers is the same in different trace files

The sequence of the intermediate routers is not the same for all trace files. There are some slight differences.

3. If the sequence of intermediate routers is different in the five trace files, list the difference and explain why.

The first 11 intermediate IP addresses are the same for all 5 traces. The first 13 intermediate IP addresses are the same for traces 1, 3 and 4. Trace 2 flips the order of address 12 and 13. Trace 5 doesn't have 74.125.37.91 at all. Intermediate addresses 14, 15, 16 vary slightly, all following the form with 209.85. __ . __. Thre is likely a network of routers near the destination, with a changing optimal path for the traceroute. So when the traceroute is run the last 3 routers will be differ slightly. The differing IPs are likely quite similar due to being part of the same subnet.

4. If the sequence of intermediate routers is the same in the five trace files, draw a table to compare the RTTs of different traceroute attempts. From the result, which hop is likely to incur the maximum delay? Explain your conclusion.

    Average RTT for each TTL in milliseconds

| TTL | Trace 1 | Trace 2 | Trace 3 | Trace 4 | Trace 5 |
|----:|--------:|--------:|--------:|--------:|--------:|
|  1  |  11.37  |  11.39  |  11.69  |  11.21  |  11.3   |
|  2  |  16.85  |  15.93  |  15.73  |  15.71  |  16.69  |
|  3  |  16.01  |  15.45  |  16.31  |  15.42  |  17.48  |
|  4  |  17.56  |  17.71  |  17.16  |  16.69  |  18.25  |
|  5  |  18.36  |  16.88  |  17.91  |  17.44  |  19.01  |
|  6  |  11.86  |  11.64  |  12.11  |  11.52  |  11.92  |
|  7  |  13.51  |  13.43  |  14.41  |  13.59  |  13.54  |
|  8  |  14.10  |  50.24  |  15.18  |  14.01  |  18.52  |
|  9  |  18.23  |  16.79  |  18.09  |  16.93  |  16.71  |
| 10  |  16.91  |  17.58  |  18.86  |  18.18  |  17.96  |
| 11  |  19.43  |  19.22  |  20.10  |  19.43  |  19.33  |

Out of the first 11 intermediate IP addresses (which are the same across all 5 traces), I believe hop 10 -> 11 incurs the largest delay since the average RTT is clearly highest for the 5 traces. Some of the later hops may have larger average RTTs, but they cannot be compared since the IPs are not consistent for all traces.
