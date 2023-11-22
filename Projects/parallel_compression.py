import time
from joblib import Parallel, delayed
import os
import gzip
import lz4.frame
import shutil
import zstandard as zstd


def compress_gzip(i, j, n_clus, name, file_name):
    with open(f'./data/csv/{file_name}/{file_name}_{n_clus}_{name}_{i}_{j}.csv', 'rb') as f_in:
        if os.path.exists(f'./data/gzip/{file_name}/{file_name}_{n_clus}_{name}_{i}_{j}.gz'):
            os.remove(f'./data/gzip/{file_name}/{file_name}_{n_clus}_{name}_{i}_{j}.gz')
        with gzip.open(f'./data/gzip/{file_name}/{file_name}_{n_clus}_{name}_{i}_{j}.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

def compress_lz4(i, j, n_clus, name, file_name):
    with open(f'./data/csv/{file_name}/{file_name}_{n_clus}_{name}_{i}_{j}.csv', 'rb') as f_in:
        if os.path.exists(f'./data/lz4/{file_name}/{file_name}_{n_clus}_{name}_{i}_{j}.lz4'):
            os.remove(f'./data/lz4/{file_name}/{file_name}_{n_clus}_{name}_{i}_{j}.lz4')
        with lz4.frame.open(f'./data/lz4/{file_name}/{file_name}_{n_clus}_{name}_{i}_{j}.lz4', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

def compress_zstd(i, j, n_clus, name, file_name):
    with open(f'./data/csv/{file_name}/{file_name}_{n_clus}_{name}_{i}_{j}.csv', 'rb') as f_in:
        if os.path.exists(f'./data/zstd/{file_name}/{file_name}_{n_clus}_{name}_{i}_{j}.zst'):
            os.remove(f'./data/zstd/{file_name}/{file_name}_{n_clus}_{name}_{i}_{j}.zst')
        with zstd.open(f'./data/zstd/{file_name}/{file_name}_{n_clus}_{name}_{i}_{j}.zst', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def create_compression_tasks(format, n_clus, class_name, name, column):
    tasks = []
    for i in range(n_clus):
        for j in range(column):
            if format == 'gzip':
                if not os.path.exists(f'./data/gzip/{name}'):
                    os.makedirs(f'./data/gzip/{name}')
                tasks.append(delayed(compress_gzip)(i, j, n_clus, class_name, name))
            elif format == 'lz4':
                if not os.path.exists(f'./data/lz4/{name}'):
                    os.makedirs(f'./data/lz4/{name}')
                tasks.append(delayed(compress_lz4)(i, j, n_clus, class_name, name))
            elif format == 'zstd':
                if not os.path.exists(f'./data/zstd/{name}'):
                    os.makedirs(f'./data/zstd/{name}')
                tasks.append(delayed(compress_zstd)(i, j, n_clus, class_name, name))
    return tasks


def parallel_compression(format, n_clus, class_name, name, column, n_processes):
    tasks = create_compression_tasks(format, n_clus, class_name, name, column)
    compress_start_time = time.time()
    Parallel(n_jobs=n_processes)(tasks)
    compress_end_time = time.time()
    t_comp = compress_end_time - compress_start_time
    return t_comp