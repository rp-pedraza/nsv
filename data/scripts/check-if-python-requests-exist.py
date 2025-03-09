#!/usr/bin/env python

try:
    import mymodule
    exit(0)
except ImportError as e:
    exit(1)
