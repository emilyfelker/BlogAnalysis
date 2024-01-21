from typing import Tuple, Any
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def create_scatter_plot(dataset, y_variable: str, title: str, filename=None, dpi=100) -> Tuple[Figure, Any]:
    ages = [blogpost[-1]["age_of_emily"] for blogpost in dataset]
    y_data = [blogpost[-1][y_variable] for blogpost in dataset]
    y_label = y_variable.replace("_", " ").title()

    plt.scatter(ages, y_data, marker='o', color='tab:purple', alpha=0.6, label='Blogposts')

    # Calculate the best-fit line
    slope, intercept = np.polyfit(ages, y_data, 1)
    # Create the best-fit line equation
    line_eq = f'Best Fit Line: y = {slope:.2f}x + {intercept:.2f}'
    # Plot the best-fit line
    plt.plot(ages, [slope * age + intercept for age in ages], color='black', label=line_eq)

    plt.xlabel('Actual Age (Years)')
    plt.ylabel(y_label)
    plt.title(title)

    plt.legend()
    plt.grid(True)

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
    figure, plt = create_scatter_plot(mock_data, "age_estimate", "Actual Age vs. GPT Estimate",
                                      "mock_data_graphed.png", 300)
    plt.show()
