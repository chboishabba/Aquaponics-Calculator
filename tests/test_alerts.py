from aquaponics.alerts import check_threshold

def test_check_threshold_levels():
    critical = check_threshold("pH", 9, 6, 8)
    assert critical.severity == "critical"
    warning = check_threshold("pH", 7.05, 7, 8)
    assert warning.severity == "warning"
    normal = check_threshold("pH", 7.5, 7, 8)
    assert normal.severity == "normal"
