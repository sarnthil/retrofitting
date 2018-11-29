import gzip
import math
import re
import sys
from collections import defaultdict
from copy import deepcopy

import click
import numpy as np

NUMBER = re.compile(r"\d+")
WORD_CHAR = re.compile(r"\w")


def normalize(word):
    if NUMBER.search(word.lower()):
        return "---num---"
    elif not WORD_CHAR.search(word):
        return "---punc---"
    else:
        return word.lower()


def read_word_vectors(filename):
    """Read all the word vectors and normalize them."""
    word_vectors = {}
    if filename.endswith(".gz"):
        opener = gzip.open
    else:
        opener = open
    with opener(filename, "r") as f:
        for line in f:
            line = line.strip().lower()
            word, *values = line.split()
            word_vectors[word] = np.zeros(len(values), dtype=float)
            for index, value in enumerate(values):
                word_vectors[word][index] = float(value)
                # normalize weight vector
            word_vectors[word] /= math.sqrt((word_vectors[word] ** 2).sum() + 1e-6)

        print("Vectors read from:", filename, file=sys.stderr)
        return word_vectors


def write_word_vectors(word_vectors, output):
    """Write word vectors to file."""
    print("\nWriting down the vectors in", output, file=sys.stderr)
    with open(output, "w") as f:
        for word, values in word_vectors.items():
            f.write(word + " ")
            for val in values:
                f.write("%.4f" % (val) + " ")
            f.write("\n")


def read_lexicon(filename):
    """Read the PPDB word relations as a dictionary."""
    lexicon = defaultdict(set)
    with open(filename) as f:
        for line in f:
            words = line.lower().strip().split()
            lexicon[normalize(words[0])].update(normalize(word) for word in words[1:])
    return lexicon


def retrofit(word_vectors, lexicon, iterations):
    """Retrofit word vectors to a lexicon."""
    new_word_vectors = deepcopy(word_vectors)
    wv_vocab = set(new_word_vectors.keys())
    loop_vocab = wv_vocab.intersection(set(lexicon.keys()))
    for i in range(iterations):
        print("iteration:", i + 1, " over ", iterations)
        # loop through every node also in ontology (else just use data estimate)
        for word in loop_vocab:
            word_neighbours = set(lexicon[word]).intersection(wv_vocab)
            num_neighbours = len(word_neighbours)
            # no neighbours, pass - use data estimate
            if num_neighbours == 0:
                continue
            # the weight of the data estimate if the number of neighbours
            new_vector = num_neighbours * word_vectors[word]
            # loop over neighbours and add to new vector (currently with weight 1)
            for pp_word in word_neighbours:
                new_vector += new_word_vectors[pp_word]
            new_word_vectors[word] = new_vector / (2 * num_neighbours)
    return new_word_vectors


@click.command()
@click.option(
    "-i",
    "--input",
    "input_",
    type=str,
    default=None,
    help="Input word vectors",
    required=True,
    show_default=True,
)
@click.option(
    "-l", "--lexicon", type=str, default=None, help="Lexicon file name", required=True
)
@click.option(
    "-o", "--output", type=str, help="Output word vectors", required=True, default=None
)
@click.option(
    "-n",
    "--iterations",
    required=True,
    type=int,
    default=10,
    help="Number of iterations",
    show_default=True,
)
def cli(input_, lexicon, output, iterations):
    """Blaaaaah"""
    word_vectors = read_word_vectors(input_)
    lexicon = read_lexicon(lexicon)
    new_word_vectors = retrofit(word_vectors, lexicon, iterations)
    write_word_vectors(new_word_vectors, output)


if __name__ == "__main__":
    cli()
