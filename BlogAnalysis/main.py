from BlogAnalysis.data import get_blogpost_dataset
from analysis import add_features_to_dataset, preview_features, show_summaries
from plot import create_scatter_plot

if __name__ == '__main__':

    dataset = get_blogpost_dataset("data/XangaBlogPosts")
    dataset_with_features = add_features_to_dataset(dataset)

    # Print post title, content preview (first 80 characters of post body), and features for each blog post
    preview_features(dataset_with_features)

    # Print just the ~5-word topic summary that ChatGPT generated for each blog post
    show_summaries(dataset_with_features)

    # Create graph of some feature against my age/over time
    create_scatter_plot(dataset_with_features,
                        y_variable="age_estimate",
                        title="Actual Age vs. GPT Estimate",
                        filename="output/real_data_graphed.png",
                        dpi=300)
