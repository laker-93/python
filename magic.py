class DeferredValue():
    def __init__(self, source, key, **kwargs):
        print("I'm a deferred value, invoked from {} for key {} and with kwargs {}".format(source, key, kwargs))
        self.source = source
        self.key = key
        self.kwargs = kwargs
    def __call__(self, *args, **kwargs):
        print("an instance of DeferredValue is being called {}".format(self))
    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        return "I'm a deferred value, invoked from {} for key {} and with kwargs {}".format(self.source, self.key, self.kwargs)


class DummyObject():
    def __init__(self):
        print("I'm a DummyObject {}".format(self))
    def __getattr__(self, key):
        print("Getting attribute {} on {}".format(key, self))
        try:
            print("proxied class is {}".format(self.proxied_class))
            proxied_attr = getattr(self.proxied_class, key)
        except AttributeError:
            print("proxied class: {} has no attribute {}".format(self.proxied_class, key))
        else:
            print("got proxied_attr: {}".format(proxied_attr))
            if hasattr(proxied_attr, 'dummy_callable'):
                print("need to make another dummy object of type {} on {}".format(proxied_attr.dummy_callable, self))
                child_dummy = proxied_attr.dummy_callable()
            return DeferredValue(self, key, child_dummy=child_dummy)

def returns_dummy(cls):
    def decorator(f):
        print("decorating f: {}".format(f))
        f.dummy_callable = cls
        print("set dummy callable to {}".format(cls))
        return f
    return decorator

class Flow:
    def __init__(self):
        print("I'm a flow")

class DummyFlow(DummyObject):
    proxied_class = Flow

class CertusSE:
    def __init__(self):
        print("I'm a Certus SE")

    @returns_dummy(DummyFlow)
    def mo_data_flow(self):
        print("doing data flow things")
        return "Thing"

    def another_method(self):
        print("another certus se method")

class DummyCertusSE(DummyObject):
    proxied_class = CertusSE

class ANCTestCase():
    def __init__(self):
        print("I'm the testcase")

    def CertusSE(self):
        certus_se = DummyCertusSE()
        return certus_se

test = ANCTestCase()
bcx = test.CertusSE()
obj = bcx.mo_data_flow
print("invoking obj")
obj()

#certus_se = CertusSE()
#print(certus_se)
#f = getattr(certus_se, 'another_method')
#print(f)
