# Adapted from Hierarchical-Localization:
# https://github.com/cvg/Hierarchical-Localization

import logging
from collections import defaultdict
from pathlib import Path

import numpy as np

logger = logging.getLogger(__name__)

def parse_retrieval(path):
    retrieval = defaultdict(list)
    with open(path, "r") as f:
        for p in f.read().rstrip("\n").split("\n"):
            if len(p) == 0:
                continue
            q, r = p.split()
            retrieval[q].append(r)
    return dict(retrieval)


def names_to_pair(name0, name1, separator="/"):
    return separator.join((name0.replace("/", "-"), name1.replace("/", "-")))

def names_to_pair_old(name0, name1):
    return names_to_pair(name0, name1, separator="_")
