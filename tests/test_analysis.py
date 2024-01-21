import pytest
from datetime import date
from typing import Tuple
from BlogAnalysis.analysis import make_features, add_features_to_dataset, preview_features

sample_post1 = ("Title 1", date(2023, 1, 15), "This is the content of post 1")
sample_post2 = ("Title 2", date(2022, 5, 20), "This is the content of post 2")
sample_post3 = ("Title 3", date(2020, 1, 1), "This is the content of post 3")
sample_dataset = [sample_post1, sample_post2, sample_post3]


@pytest.mark.parametrize("post", sample_dataset)
def test_make_features(post: Tuple[str, date, str]):
    with pytest.raises(ValueError):
        make_features("This is just some text that someone wrote on a blog.")
    features = make_features(post)
    assert len(features) == 5, f"I expected 5 features but got {len(features)}"
    assert features["Number of Words"] == len(post[2].split())
    assert features["Day of Week"] == post[1].strftime("%A")
    assert features["Age of Emily"] == (post[1] - date(1991, 1, 9)).days / 365.25
