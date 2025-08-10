def tan_load_check(protein_feed_g: float, biofilter_cap_g: float):
    """Evaluate if the biofilter can handle TAN generated from protein feed.

    Approximately 9.2% of feed protein is converted to total ammonia nitrogen (TAN).
    This function estimates TAN load and compares it to the biofilter capacity.

    Args:
        protein_feed_g: Amount of protein feed provided (g).
        biofilter_cap_g: Biofilter capacity for TAN (g).

    Returns:
        A tuple ``(utilization_pct, within_capacity)`` where ``utilization_pct`` is
        the percentage of the biofilter capacity used and ``within_capacity``
        indicates whether the TAN load is within the biofilter's handling ability.
    """
    if biofilter_cap_g <= 0:
        raise ValueError("biofilter_cap_g must be positive")

    tan_produced = protein_feed_g * 0.092
    utilization_pct = (tan_produced / biofilter_cap_g) * 100
    return utilization_pct, utilization_pct <= 100
