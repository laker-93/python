from abc import ABC, abstractmethod

class AbsFlow(ABC):

    @abstractmethod
    def udp_mo(self, port, ppd_session=None):
        print("udp mo %d ppd %s" % (port, ppd_session))
        # This will cause a TypeError as Stream:udp_await() does not have a
        # ppd_session arg.
        self.udp_await(port, ppd_session=ppd_session)

        # Could do the following but it seems ugly.
        if ppd_session:
            self.udp_await(port, ppd_session=ppd_session)
        else:
            self.udp_await(port)

class Flow(AbsFlow):
    def udp_mo(self, port, ppd_session=None):
        super().udp_mo(port, ppd_session=ppd_session)

    def udp_await(self, port, ppd_session=None):
        print("flow udp await port %d ppd %s" % (port, ppd_session))

class Stream(AbsFlow):
    def udp_mo(self, port):
        super().udp_mo(port)

    # A 'Stream' knows nothing about ppd, so I want to avoid having
    # 'ppd_session' as an argument to this function.
    def udp_await(self, port):
        print("stream udp await %d" % port)

s = Stream()
s.udp_mo(3)

f = Flow()
f.udp_mo(3, "ppd")
