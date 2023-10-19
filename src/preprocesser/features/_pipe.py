import time
import pandas as pd
from numpy.typing import ArrayLike
import multiprocessing as mp

from preprocesser.models import PreProcesser


def sequential_preprocessing(p: PreProcesser,
                             text_set: ArrayLike,
                             verbose=False) -> ArrayLike:
    """
    Preprocess a list of texts in sequential

    :p
        - Preprocesser class
    :text_text
        - Set of text that need to be mapped
    """

    if verbose:
        print("Total records of the dataset", len(text_set))

    df = pd.DataFrame({'text': text_set})
    t1 = time.time()
    df['text'] = df['text'].apply(p)
    t2 = time.time()

    if verbose:
        print("Time consuming Sequential Processing to process " +
              "the Dataset {0:.2f}s".format(round(t2-t1, 2)))
    return df['text'].values


def parallel_preprocessing(p: PreProcesser,
                           text_set: ArrayLike,
                           njobs: int = -1,
                           verbose=False) -> ArrayLike:
    """
    Preprocess a list of texts in parallel.
    The performance is evident when you deal with
    a big dataset of text.

    :p
        - Preprocesser class
    :text_text
        - Set of text that need to be mapped
    :njobs
        - Number of threds to be used. By default
        the value is -1, which mean it uses all the available threds.
    """

    if verbose:
        print("Total records of the dataset", len(text_set))

    df = pd.DataFrame({'text': text_set})
    processes = mp.cpu_count() if njobs == -1 else njobs
    processes = mp.cpu_count() if processes > mp.cpu_count() else processes
    t1 = time.time()
    with mp.Pool(processes=processes) as pool:
        df['text'] = pool.map(p, text_set)
    t2 = time.time()

    if verbose:
        print("Time consuming Parallel Processing to process " +
              "the Dataset {0:.2f}s".format(round(t2-t1, 2)))
    return df['text'].values
