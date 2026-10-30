def causal_mean(window):
    if not window:
        raise ValueError("empty")
    return sum(window) / len(window)
