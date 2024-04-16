#%%
"""
Testing preallocation vs. extension of array to store load profiles of
Result (on Johann's PC)

Preallocation_list_benchmark: 4.022432799999933
Extend_list_benchmark: 9.485812400000214
Preallocation_np_benchmark: 1.7216911999998956
Extend_np_benchmark: 32.18607789999987

-> use preallocation with numpy arrays
"""
import numpy as np

from time import perf_counter
nr_days = 365

nr_appliances = 50*20  # assume 50 users with each 20 appliances


day_profile_np = np.array([a*3 for a in range(1,1441)])
day_profile_list = [a*3 for a in range(1,1441)]


def preall_bench_np(day, nr_days):
    preall_list= np.zeros(nr_days * 1440)
    for i in range(nr_days):
        preall_list[i*1440:i*1440+1440] = day

    return preall_list

def preall_bench_list(day, nr_days):
    preall_list= nr_days * 1440*[None]
    for i in range(nr_days):
        preall_list[i*1440:i*1440+1440] = day

    return preall_list

def extend_bench_list(day, nr_days):
    empty_list = []
    for i in range(nr_days):
        empty_list.extend(day)

    return empty_list

def extend_bench_np(day, nr_days):
    empty_list = []
    for i in range(nr_days):
        empty_list.extend(day)

    return empty_list

start = perf_counter()
for i in range(nr_appliances):
    result = preall_bench_list(day_profile_list, nr_days)
print('Preallocation_list_benchmark: ' + str(perf_counter()-start))

start = perf_counter()
for i in range(nr_appliances):
    result_2 = extend_bench_list( day_profile_list, nr_days)
print('Extend_list_benchmark: ' + str(perf_counter()-start))

start = perf_counter()
for i in range(nr_appliances):
    result = preall_bench_np(day_profile_np, nr_days)
print('Preallocation_np_benchmark: ' + str(perf_counter()-start))

start = perf_counter()
for i in range(nr_appliances):
    result_2 = extend_bench_np(day_profile_np, nr_days)
print('Extend_np_benchmark: ' + str(perf_counter()-start))