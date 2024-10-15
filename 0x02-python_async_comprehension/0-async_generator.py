#!/usr/bin/env python3
"""Task 0's module"""

import asyncio
import random


async def async_generator():
    """Asynchronously generates a random number between 0 and 10
    after 1 second, 10 times."""
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
