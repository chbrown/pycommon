import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects


def int_histogram(data, min_value=None, max_value=None):
    '''
    >>> int_histogram([1, 1, 2, 4], 1, 4)
    (array([2, 1, 0, 1]), array([1, 2, 3, 4, 5]))
    >>> int_histogram([1, 1, 2, 4])
    (array([2, 1, 0, 1]), array([1, 2, 3, 4, 5]))
    '''
    data = np.array(data)
    if min_value is None:
        min_value = data.min()
    if max_value is None:
        max_value = data.max()
    bins = np.arange(min_value, max_value + 2)
    return np.histogram(data, bins=bins)


def plt_int_bar(counts, x, label_height=7, label_ha='center', label_va='bottom'):
    '''
    Args:
        counts: array of numbers
        x: an array of what each item in counts is counting (len(counts) == len(x))
    '''
    # counts has length == bins, xs has length == (bins + 1), since it includes the right edge
    fig, ax = plt.subplots()
    plt.bar(x, counts)
    ticks = [patch.get_x() + patch.get_width() / 2 for patch in ax.patches]
    ax.set_xticks(ticks)
    labels = x.astype(int)
    ax.set_xticklabels(labels)
    for patch, label in zip(ax.patches, counts):
        ax.text(patch.get_x() + patch.get_width() / 2, patch.get_height() + 3,
                label, ha=label_ha, va=label_va,
                path_effects=[PathEffects.withStroke(linewidth=4, foreground='w')])
    bottom, top = ax.get_ylim()
    ax.set_ylim(bottom, top + label_height)
    left, right = ax.get_xlim()
    ax.set_xlim(left - (1 - ax.patches[0].get_width()), right)
    return fig, ax


def plt_int_hist(data, title, min_value=None, max_value=None, label_height=7):
    hist, bin_edges = int_histogram(data, min_value=min_value, max_value=max_value)
    plt_int_bar(hist, bin_edges[:-1], label_height=label_height)
    plt.title(title)
