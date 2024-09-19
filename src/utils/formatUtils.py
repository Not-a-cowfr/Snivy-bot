def format_coins(value: float) -> str:
    suffixes = ['k', 'm', 'b', 't']
    for i, suffix in enumerate(suffixes, 1):
        unit = 1000 ** i
        if value < unit * 1000:
            return f'{value / unit:.1f}{suffix}'
    return str(value)