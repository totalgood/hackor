def create_class(name, base_class):
    if not name in globals():
        class AnonymousClass(base_class):
            pass
        globals()[name] = AnonymousClass
    return globals()[name]
