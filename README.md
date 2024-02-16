# Blog Analysis with ChatGPT

## Introduction

This program analyzes a set of around 800 blog posts, mostly about my personal life, 
that I wrote between the ages of 15 and 21. My goal was 


## Features
- Feature 1: Description
- Feature 2: Description
- Feature 3: Description


## Usage

To get started with Project Name, run the following command:

```python
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
```

This scatterplot of Chat GPT's age estimate plotted against my actual age shows a posistive correlation between the two variables, with a few outliers:
![Scatterplot with linear regression line showing a positive correlation between age estimate and actual age](output/real_data_graphed.png "Actual Age vs. GPT Estimate")
The program could still be modified to see whether my age at the time of writing correlates better with simpler predictors like word count or difficulty, sentence length, or other measures of writing complexity.