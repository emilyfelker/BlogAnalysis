from BlogAnalysis.data import get_blogpost_dataset
from analysis import add_features_to_dataset, preview_features, show_summaries
from plot import create_scatter_plot
from rag import generate_answer, ask_question

def demo_chatgpt_analysis():
    # Load dataset
    data = get_blogpost_dataset("data/XangaBlogPosts")

    # Add features to dataset
    dataset_with_features = add_features_to_dataset(data)

    # Print post title, content preview (first 80 characters of post body), and features for each blog post
    preview_features(dataset_with_features[:10])

    # Print just the ~5-word topic summary that ChatGPT generated for each blog post
    show_summaries(dataset_with_features[:10])

    # Create graph of some feature against my age/over time
    create_scatter_plot(dataset_with_features,
                        y_variable="age_estimate",
                        title="Actual Age vs. GPT Estimate",
                        filename="output/real_data_graphed.png",
                        dpi=250,
                        figsize=(6.4, 4.8))

def demo_rag():
    ask_question()
    # generate_answer("Emily's lovers?"))

if __name__ == '__main__':

    #demo_chatgpt_analysis()

    demo_rag()



