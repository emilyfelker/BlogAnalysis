from data import get_blogpost_dataset
from analysis import add_features_to_dataset, preview_features
from plot import create_scatter_plot, plt

if __name__ == '__main__':

    dataset = get_blogpost_dataset("XangaBlogPosts", 1)
    dataset_with_features = add_features_to_dataset(dataset)
    preview_features(dataset_with_features)
    #figure, plt = create_scatter_plot(dataset_with_features, "real_data_graphed.png", 300)
