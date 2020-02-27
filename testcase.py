import asyncio
from contextlib import contextmanager

@asyncio.coroutine
def chain_calls(l):
    print("chain_calls: got {} things in list".format(len(l)))
    for item in l:
        print("chain_calls: sleeping for 1")
        yield from asyncio.sleep(1)

class TestCase:
    def __init__(self, loop):
        self.active_list = []
        self.all_blocks = set()
        self.loop = loop

    @contextmanager
    def at(self, time):
        old_list = self.active_list
        print("lajp yielding to schedule_list, clear active_list from {}".format(old_list))
        self.active_list = []
        yield self.schedule_list(self.active_list, delay=time)
        print("lajp yielded to schedule_list, restore active_list to {}".format(old_list))
        self.active_list = old_list

    def schedule_list(self, l, delay):
        @asyncio.coroutine
        def runner():
            print("running and sleeping")
            yield from asyncio.sleep(1)
            print("waiting to have chained calls on {}".format(l))
            yield from chain_calls(l)
            print("finished chaining")
        print("scheduled with {} and delay".format(l, delay))
        list_task = self.loop.create_task(runner())
        print("add {} to all_blocks".format(list_task))
        self.all_blocks.add(list_task)
        return list_task

    def run_scheduled(self):
        print("run scheduled")
        @asyncio.coroutine
        def run():
            yield from asyncio.gather(*self.all_blocks)
            print("running all_blocks")

        run_task = self.loop.create_task(run())
        self.loop.run_until_complete(run_task)



a = 3
loop = asyncio.get_event_loop()
test = TestCase(loop)

with test.at(2) as setup:
    print("in body of {}".format(setup))
    test.active_list += ['new_thing']
    print("exiting {}".format(setup))

test.run_scheduled()
