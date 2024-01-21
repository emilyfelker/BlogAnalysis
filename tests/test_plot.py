from BlogAnalysis.plot import create_scatter_plot, generate_mock_data
from matplotlib.pyplot import Figure


def test_create_scatter_plot():
    mock_data = generate_mock_data()
    figure, _ = create_scatter_plot(mock_data)
    assert isinstance(figure, Figure)


