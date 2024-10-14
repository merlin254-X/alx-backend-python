#!/usr/bin/env python3
import asyncio
from typing import List
import random


async def wait_random(max_delay: int) -> float:
    """Wait for a random delay between 0 and max_delay and
    return the actual delay."""
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay


async def wait_n(n: int, max_delay: int) -> List[float]:
    """Spawn wait_random n times with the specified max_delay."""
    delays = []
    for _ in range(n):
        delays.append(await wait_random(max_delay))

    # Return the delays in ascending order without using sort()
    sorted_delays = []
    while delays:
        # Find the smallest delay and append it to sorted_delays
        smallest = min(delays)
        sorted_delays.append(smallest)
        delays.remove(smallest)

    return sorted_delays
