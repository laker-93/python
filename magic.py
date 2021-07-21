 41         return f                                                                                                                                                                                                                             40     return decorator                                                                                                                                                                                                                         39                                                                                                                                                                                                                                              38 class Flow:                                                                                                                                                                                                                                  37     def __init__(self):                                                                                                                                                                                                                      36         print("I'm a flow")                                                                                                                                                                                                                  35 class DummyFlow(DummyObject):                                                                                                                                                                                                                34     proxied_class = Flow                                                                                                                                                                                                                     33                                                                                                                                                                                                                                              32 class CertusSE:                                                                                                                                                                                                                              31     def __init__(self):                                                                                                                                                                                                                      30         print("I'm a Certus SE")                                                                                                                                                                                                             29                                                                                                                                                                                                                                              28     @returns_dummy(DummyFlow)                                                                                                                                                                                                                27     def mo_data_flow(self):                                                                                                                                                                                                                  26         print("doing data flow things")                                                                                                                                                                                                      25         return "Thing"                                                                                                                                                                                                                       24                                                                                                                                                                                                                                              23     def another_method(self):                                                                                                                                                                                                                22         print("another certus se method")                                                                                                                                                                                                    21                                                                                                                                                                                                                                              20 class DummyCertusSE(DummyObject):                                                                                                                                                                                                            19     proxied_class = CertusSE                                                                                                                                                                                                                 18                                                                                                                                                                                                                                              17 class ANCTestCase():                                                                                                                                                                                                                         16     def __init__(self):                                                                                                                                                                                                                      15         print("I'm the testcase")                                                                                                                                                                                                            14                                                                                                                                                                                                                                              13     def CertusSE(self):                                                                                                                                                                                                                      12         certus_se = DummyCertusSE()                                                                                                                                                                                                          11         return certus_se                                                                                                                                                                                                                     10                                                                                                                                                                                                                                               9 test = ANCTestCase()                                                                                                                                                                                                                          8 bcx = test.CertusSE()                                                                                                                                                                                                                         7 obj = bcx.mo_data_flow                                                                                                                                                                                                                        6 print("invoking obj")                                                                                                                                                                                                                         5 obj()                                                                                                                                                                                                                                         4                                                                                                                                                                                                                                               3 #certus_se = CertusSE()                                                                                                                                                                                                                       2 #print(certus_se)                                                                                                                                                                                                                             1 #f = getattr(certus_se, 'another_method')                                                class DeferredValue():
    #def __init__(self, testcase, parent_dummy_obj, key, **kwargs):
    def __init__(self, source, key, **kwargs):
        print("I'm a deferred value, invoked from {} for key {} and with kwargs {}".format(source, key, kwargs))
        self.source = source
        self.key = key
        self.kwargs = kwargs
    def __call__(self, *args, **kwargs):
        print("an instance of DeferredValue is being called {}".format(self))
        call = DeferredCall(self.source, self.key, **self.kwargs)
        return call(*args, **kwargs)

    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        return "I'm a deferred value, invoked from {} for key {} and with kwargs {}".format(self.source, self.key, self.kwargs)

class DeferredCall(DeferredValue):
    #def __init__(self, testcase, dummy, target, child_dummy=None):
    def __init__(self, dummy, target, child_dummy=None):
        print("I'm a deferred call, invoked from {} for key {} with child_dummy {}".format(dummy, target, child_dummy))
        #super().__init__(testcase, dummy, target)
        super().__init__(dummy, target)

    def __call__(self, *args, **kwargs):
        print("an instance of DeferredCall is being called {}".format(self))
        # this DeferredCall which mocks a Future is added to the testcase's active list
        # once the body of the proxied object is run, this mock Future will be
        # resolved allowing the next mock Future to run on the active list.

    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        return "I'm a deferred call, invoked from {} for key {} and with kwargs {}".format(self.source, self.key, self.kwargs)

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
