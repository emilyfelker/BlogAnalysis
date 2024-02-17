from typing import Tuple, Any
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def create_scatter_plot(dataset, y_variable: str, title: str, filename=None, dpi=100, figsize=(8, 6)) -> Tuple[Figure, Any]:
    ages = [blogpost[-1]["age_of_emily"] for blogpost in dataset]
    y_data = [blogpost[-1][y_variable] for blogpost in dataset]

    # Filter out data points where y_data is NoneType
    filtered_data = [(age, y) for age, y in zip(ages, y_data) if y is not None and y < 100]

    # Unpack the filtered data
    ages_filtered, y_data_filtered = zip(*filtered_data)

    y_label = y_variable.replace("_", " ").title()

    plt.figure(figsize=figsize)
    plt.scatter(ages_filtered, y_data_filtered, marker='o', color='tab:purple', alpha=0.5, label='Blogpost')

    # Calculate the best-fit line
    slope, intercept = np.polyfit(ages_filtered, y_data_filtered, 1)
    # Create the best-fit line equation
    line_eq = f'Best Fit Line: y = {slope:.2f}x + {intercept:.2f}'
    # Plot the best-fit line
    plt.plot(ages_filtered, [slope * age + intercept for age in ages_filtered], color='black', label=line_eq)

    plt.xlabel('Actual Age (Years)')
    plt.ylabel(y_label)
    plt.title(title)

    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    if filename is not None:
        plt.savefig(filename, dpi=dpi)

    return plt.gcf(), plt


#  make mockup dataset
def generate_mock_data():
    data = []
    for _ in range(800):
        age_of_emily = random.uniform(15, 25)
        age_estimate_jitter = random.uniform(-7, 7)

        age_estimate = round(age_of_emily + age_estimate_jitter)

        data_dict = {
            "age_of_emily": age_of_emily,
            "age_estimate": age_estimate
        }

        tuple_data = ("PostTitle", "DatePlaceholder", data_dict)
        data.append(tuple_data)
    return data


if __name__ == "__main__":
    mock_data = generate_mock_data()
    figure, plt = create_scatter_plot(mock_data,
                                      y_variable="age_estimate",
                                      title="Actual Age vs. GPT Estimate (Mock Data)",
                                      filename="mock_data_graphed.png",
                                      dpi=150,
                                      figsize=(4.8, 3.6))
    plt.show()
