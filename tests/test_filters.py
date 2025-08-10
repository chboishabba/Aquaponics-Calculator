from aquaponics.filters import hampel_filter, ewma

def test_hampel_filter_removes_outlier():
    data = [1, 1, 1, 20, 1, 1, 1]
    filtered = hampel_filter(data, window_size=2, n_sigmas=3)
    assert filtered[3] == 1

def test_ewma_basic():
    data = [1, 2, 3]
    result = ewma(data, alpha=0.5)
    assert result == [1, 1.5, 2.25]
