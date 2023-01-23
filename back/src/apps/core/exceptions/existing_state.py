class ExistingStateException(Exception):
    """Если конфигурация на очередном шаге в точности повторит себя же на одном из более ранних шагов."""
    pass
