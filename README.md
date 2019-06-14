# ternary

The code is related to the article preprint [Ternary quadratic forms representing arithmetic progressions](https://arxiv.org/abs/1906.02538) by T. Hejda a V. Kala.

## Description

There are two basic parts. First, `universal` is the script used in §3.1 of the article. Second, `count` is the script used in §3.3 and §3.4 of the article. The code used in §3.2 is not included.

## `universal`

Two files are needed from the repo: `universal.py` and `create_number_lists.sage`. If you do not have SageMath installed, you also need `number_lists.py`. How to run:

1. Run `create_number_lists.sage`. This will generate the file `number_lists.py`.
1. Check that `n_threads` at the beginning of `universal.py` matches the number of cores of your computer.
1. Run `universal.py`.
1. The output shows all primes the program computed, and the candidate forms, if there are any.

## `count`

Three files are needed from the repo: `count.cpp`, `count.sh` and `create_run_count.sage`. If you do not have SageMath installed, you also need `run_count.sh`. How to run:

1. Run `create_run_count.sage`. This will generate the file `run_count.sh`.
1. Make `run_count.sh` executable by `chmod +x run_count.sh`
1. Run `run_count.sh`.
1. The output is in files `c_<a>_<b>_<c>_<p>.txt`. If the file contains a line with `ZERO <n>`, this indicates that the form `<a,b,c*p>` is a candidate for a `(p,l)`-universal for `n` different `l`'s. This can be checked e.g. by `grep ZERO c_*.txt`.
