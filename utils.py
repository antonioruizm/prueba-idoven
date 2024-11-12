from typing import List

def zero_crossings(signal: List[int]) -> int:
    count = 0
    for i in range(1, len(signal)):
        if signal[i-1] * signal[i] < 0:
            count += 1
    return count
