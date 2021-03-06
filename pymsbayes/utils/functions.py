#! /usr/bin/env python

import sys
import os
import errno
import random
import string

from pymsbayes.utils import GLOBAL_RNG
from pymsbayes.fileio import process_file_arg

def mkdr(path):
    """
    Creates directory `path`, but suppresses error if `path` already exists.
    """
    try:
        os.makedirs(path)
    except OSError, e:
        if e.errno == errno.EEXIST:
            pass
        else:
            raise e

def mk_new_dir(path):
    attempt = -1
    while True:
        try:
            if attempt < 0:
                os.makedirs(path)
                return path
            else:
                p = path.rstrip(os.path.sep) + '-' + str(attempt)
                os.makedirs(p)
                return p
        except OSError, e:
            if e.errno == errno.EEXIST:
                attempt += 1
                continue
            else:
                raise e

def get_new_path(path, max_attempts = 1000):
    path = os.path.abspath(os.path.expandvars(os.path.expanduser(path)))
    if not os.path.exists(path):
        f = open(path, 'w')
        f.close()
        return path
    attempt = 0
    while True:
        p = '-'.join([path, str(attempt)])
        if not os.path.exists(p):
            f = open(p, 'w')
            f.close()
            return p
        if attempt >= max_attempts:
            raise Exception('failed to get unique path')
        attempt += 1

def get_sublist_greater_than(values, threshold):
    return [v for v in values if v > threshold]

def frange(start, stop, num_steps, include_end_point = False):
    inc = (float(stop - start) / num_steps)
    for i in range(num_steps):
        yield start + (i * inc)
    if include_end_point:
        yield stop

def random_str(length=8,
        char_pool=string.ascii_letters + string.digits):
    return ''.join(random.choice(char_pool) for i in range(length))

def get_random_int(rng = GLOBAL_RNG):
    return rng.randint(1, 999999999)

def get_indices_of_patterns(target_list, regex_list, sort=True):
    indices = []
    for regex in regex_list:
        indices.extend([i for i, e in enumerate(target_list) if regex.match(e)])
    if sort:
        return sorted(indices)
    return indices

def get_indices_of_strings(target_list, string_list, sort=True):
    indices = []
    for s in string_list:
        indices.extend([i for i, e in enumerate(target_list) if s.strip() == e.strip()])
    if sort:
        return sorted(indices)
    return indices
    
def list_splitter(l, n, by_size=False):
    """
    Returns generator that yields list `l` as `n` sublists, or as `n`-sized
    sublists if `by_size` is True.
    """
    if n < 1:
        raise StopIteration
    elif by_size:
        for i in range(0, len(l), n):
            yield l[i:i+n]
    else:
        if n > len(l):
            n = len(l)
        step_size = len(l)/int(n)
        if step_size < 1:
            step_size = 1
        # for i in range(0, len(l), step_size):
        #     yield l[i:i+step_size]
        i = -step_size
        for i in range(0, ((n-1)*step_size), step_size):
            yield l[i:i+step_size]
        yield l[i+step_size:]

def whereis(file_name):
    """
    Returns the first absolute path to `file_name` encountered in $PATH.
    Returns `None` if `file_name` is not found in $PATH.
    """
    paths = os.environ.get('PATH', '').split(':')
    for path in paths:
        abs_path = os.path.join(path, file_name)
        if os.path.exists(abs_path) and not os.path.isdir(abs_path):
            return abs_path
            break
    return None

def is_file(path):
    if not path:
        return False
    if not os.path.isfile(path):
        return False
    return True

def is_dir(path):
    if not path:
        return False
    if not os.path.isdir(path):
        return False
    return True

def is_executable(path):
    return is_file(path) and os.access(path, os.X_OK)

def which(exe):
    if is_executable(exe):
        return exe
    name = os.path.basename(exe)
    for p in os.environ['PATH'].split(os.pathsep):
        p = p.strip('"')
        exe_path = os.path.join(p, name)
        if is_executable(exe_path):
            return exe_path
    return None

def long_division(dividend, diviser):
    n, d = int(dividend), int(diviser)
    quotient = n / d
    remainder = n - (d * quotient)
    return quotient, remainder

def get_tolerance(num_prior_samples, num_posterior_samples):
    return num_posterior_samples / float(num_prior_samples)

def least_common_multiple(x):
    y = [i for i in x]
    while True:
        if len(set(y)) == 1:
            return y[0]
        min_index = y.index(min(y))
        y[min_index] += x[min_index]

