
def set_attributes(**kwargs):
    def decorator(method):
        for name, value in kwargs.items():
            setattr(method, name, value)
        return method
    return decorator
