#!/usr/bin/env python3
'''Task 2's module.
'''
import asyncio
import time

# Import wait_n from the correct file
wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    '''Computes the average runtime of wait_n.
    '''
    start_time = time.time()  # Record the start time
    asyncio.run(wait_n(n, max_delay))  # Run wait_n
    total_time = time.time() - start_time  # Calculate total elapsed time
    return total_time / n  # Return average time per coroutine
