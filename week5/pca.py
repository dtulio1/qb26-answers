#!/usr/bin/env python

import sys
import numpy
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def main():
    rapa_data = numpy.loadtxt('WT_NF_Rapa_counts.tsv')
    nf_data = numpy.loadtxt('WT_NF_Ctrl_counts.tsv')
    nf_rep_data = numpy.loadtxt('WT_NF_Ctrl_rep_counts.tsv')

    # The row and column names are stored in separate files. The sampling time and replicate can be extracted from the sample names
    genes = numpy.array([name.rstrip() for name in open('gene_names.txt')])
    sample_labels = numpy.array([name.rstrip().split('\t') for name in open('samples.txt')])
    times = numpy.array([int(time.split('_')[1]) for time, rep in sample_labels if rep == 1], numpy.int32)
    rep_times = numpy.array([int(time.split('_')[1]) for time, rep in sample_labels], numpy.int32)
    reps = numpy.array([int(rep.split('_')[1]) for time, rep in sample_labels], numpy.int32)
    
    #  Step 1.3: call PCA function on replicate data
    PCA_analysis(nf_rep_data, rep_times, reps, title = "Replicate PCA", fname = "replicate")

    # Step 2.1: Filter data
    # axis 1 computes time for each row
    means = numpy.mean(nf_data, axis = 1)
    stdev = numpy.std(nf_data, axis = 1)

    # filter for genes with mean > 0.85 and scaled std > 0.115
    filter = (means > 0.85) & ((stdev / means) > 0.115)

    # filter all 3 datasets
    # I passed throuhg each row, even though the assignment has [:, filter]
    # But it says our genes are in rows so I flipped it
    filtered_nf_data = nf_data[filter, :]
    filtered_rapa_data = rapa_data[filter, :]
    filtered_nf_rep_data = nf_rep_data[filter, :]

    # run PCA for 2.1
    PCA_analysis(filtered_nf_rep_data, rep_times, reps, title = "filtered", fname = "filtered")

    # For step 2.3: normalize the filtered data across time
    norm_nf_data = normalize_data(filtered_nf_data)
    norm_rapa_data = normalize_data(filtered_rapa_data)

    # find the time of peak expression (index of the largest value between all timepoints)
    peak = numpy.argmax(norm_nf_data, axis = 1)

    # PCA on each genes, color by time of peak expression
    pc1, pc2 = PCA_genes(norm_nf_data, peak, title = "Gene PCA", fname = "gene_pca")

    # Step 3.1: order expression times
    angle = numpy.arctan2(pc2, pc1)

    # Step 3.1: visualize ordered expression data
    plot_hm(norm_nf_data, xlabel = "time", ylabel = "genes", title = "Genes ordered by angle", orderby = angle, fname = "angle_ordered_heatmap")

    # Step 3.2: phase expression times and plot data
        # align using angles from control data
    aligned_nf_data = align_times(norm_nf_data, angle)

    # Step 3.2 - use heat map to plot
    plot_hm(aligned_nf_data, xlabel = "time", ylabel = "genes", title = "Phased expression", orderby = angle, fname = "phased_heatmap")

    # Step 3.3: Cluster data
    # First, align rapa data using angles from control data
    aligned_rapa_data = align_times(norm_rapa_data, angle)
    # Second, cluster the data with kmeans clustering
    kmeans = KMeans(n_clusters = 6, random_state = 42)
        # Next, fit model and predict labels in a single step
    groups = kmeans.fit_predict(numpy.concatenate((aligned_nf_data, aligned_rapa_data), axis = 1))

    # Step 3.4: Plot clustered data
        # Plot aligned control and rapa data, order and annotated by cluster
    plot_hm(aligned_nf_data, aligned_rapa_data, xlabel = "time", ylabel = "genes", title = "Clustered heatmap", orderby = groups, showgroups = True, fname = "clustered_heatmap" )

# step 1.2
# create a function that takes in rep data
def PCA_analysis(data, times, reps, title = "", fname = None):
    pca = PCA(random_state=42)
# transpose the matrix
# also train fit the PCA model
    pca_transpose = pca.fit_transform(data.T)
        # makes one row per sample
        # makes each column a PC
    pc1 = pca_transpose[:, 0]
    pc2 = pca_transpose[:, 1]

# plot the first and second pcs as a scatter plot
    plt.scatter(pc1, pc2, c=times, cmap = 'Set1', s=reps * 15)
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title(title)
    plt.savefig(fname)

    plt.show()

# step 2.2
# create a function to find and plot first 2 PCs
def PCA_genes(data, colors, title = "", fname = None):
    pca = PCA(random_state=42)
    pca_transform = pca.fit_transform(data)
    pc1 = pca_transform[:, 0]
    pc2 = pca_transform[:, 1]

    # scatter plot
    plt.scatter(pc1, pc2, c=colors, cmap = 'Set1')
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title(title)
    plt.savefig(fname)
    
    plt.show()

    # return coordinates for later use
    return pc1, pc2

def normalize_data(data):
    """
    Function to normalize data along the second axis of a 2D array.

    Parameters:
    -----------
    data : ndarray
           A 2D matrix containing sample data where the rows are samples and columns are features.

    Returns:
    --------
    norm_data : ndarray
                An array of the sample shape and data type as the original data with values normalized along the second axis.
    """
    norm_data = numpy.copy(data)
    norm_data -= numpy.mean(norm_data, axis=1, keepdims=True)
    norm_data /= numpy.std(norm_data, axis=1, keepdims=True)
    return norm_data

def plot_hm(*data, xlabel='', ylabel='', title='', orderby=None, showgroups=False, fname=None):
    """
    Function for plotting heatmap/matrix style data.

    Parameters:
    -----------
    data : ndarray(s)
           The array or arrays should be 2D with rows plotted along the y-axis and columns plotted along the x-axis.
           If multiple arrays are passed as positional arguments, they need to have the same number of rows.
    xlabel : str
           An x-axis label for the plotted data
    ylabel : str
           A y-axis label for the plotted data
    title : str
           A title to add above the plot
    orderby : ndarray
           A list of indices or group labels for ordering the data along the x-axis. If None, the data order is not changed
    showgroups : bool
           An indicator whether the group labels passed to `orderby` should be plotted as an additional color bar. Ignored if orderby is None.
    fname : str
           A file name to save the plot to. If None, the plot is only displayed but not saved.
    
    Returns:
    --------
    None
    """
    if orderby is None:
        order = numpy.arange(data[0].shape[0])
    else:
        order = numpy.argsort(orderby)
    if orderby is None or not showgroups:
        fig, ax = plt.subplots(1, len(data), figsize=(3, 15))
        if len(data) > 1:
            for i in range(len(data)):
                ax[i].imshow(data[i][order, :], aspect='auto')
                ax[i].set_xlabel(xlabel)
                if i > 0:
                    ax[i].set_yticks([])
            ax[0].set_ylabel(ylabel)
        else:
            ax.imshow(data[0][order, :], aspect='auto')
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
    else:
        groups = orderby[order]
        fig, ax = plt.subplots(1, len(data) + 1, width_ratios=[1] + [3] * len(data), figsize=(4, 15))
        if len(data) > 1:
            for i in range(len(data)):
                ax[i + 1].imshow(data[i][order, :], aspect='auto')
                ax[i + 1].set_xlabel(xlabel)
                ax[i + 1].set_ylabel('')
                ax[i + 1].set_yticks([])
        else:
            ax[-1].imshow(data[0][order, :], aspect='auto')
            ax[-1].set_xlabel(xlabel)
            ax[-1].set_ylabel('')
            ax[-1].set_yticks([])
        ax[-1].yaxis.tick_right()
        ax2 = ax[-1].twinx()
        ax2.set_ylabel(ylabel)
        ax[0].set_ylabel('group')
        ax[0].imshow(groups.reshape(-1, 1), aspect='auto')
        bounds = numpy.r_[0, numpy.where(groups[1:] != groups[:-1])[0] + 1, groups.shape[0]] - 0.5
        ax[0].set_yticks((bounds[:-1] + bounds[1:]) / 2)
        ax[0].set_yticklabels([str(i) for i in range(bounds.shape[0] - 1)])
        ax[0].set_xticks([])
    if title:
        plt.suptitle(title)
    if fname is not None:
        plt.savefig(fname, dpi=300, bbox_inches='tight')
    plt.show()


def align_times(data, angle):
    """
    This function takes a 2D matrix of data and a 1D matrix of angles (radians) and shifts data along the second axis (axis=1)
    to align all rows to have an effective angle of zero.

    Parameters:
    -----------
    data : ndarray
           A 2D matrix of data where each row is a sample and each column is a measurement in a cyclical cycle
    angle : ndarray
           A 1D matrix of data of a length equal to the number of rows in data. Angles should be in radians.
           
    Returns:
    --------
    aligned : ndarray
              A new array with data shifted along the second axis to align each row to have an angle of zero
    """
    n = data.shape[1]
    offsets = n - angle * n / (numpy.pi * 2)
    offsets[numpy.where(offsets < 0)] += n
    aligned = numpy.zeros_like(data)
    for i in range(data.shape[0]):
        aligned[i, :] = (numpy.roll(data[i, :], int(numpy.floor(offsets[i]))) * (numpy.ceil(offsets[i]) - offsets[i]) +
                         numpy.roll(data[i, :], int(numpy.ceil(offsets[i]))) * (offsets[i] - numpy.floor(offsets[i])))
    return aligned

# call main function
main()
