class CustomMeta(type):
    def __new__(mcs, name, bases, classdict, **kwargs):
        custom_classdict = {(key if key.startswith("__") and key.endswith("__") else
                             ("custom_" + key)): value for key, value in classdict.items()}
        custom_classdict["__setattr__"] = mcs.custom_setattr
        cls = super().__new__(mcs, name, bases, custom_classdict, **kwargs)
        return cls

    def custom_setattr(cls, key, value):
        object.__setattr__(cls, (key if key.startswith("__") and key.endswith("__")
                                 else ("custom_" + key)), value)

    def __setattr__(cls, key, value):
        super().__setattr__((key if key.startswith("__") and key.endswith("__")
                             else ("custom_" + key)), value)
