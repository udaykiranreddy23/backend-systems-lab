from queue import PriorityQueue, Empty
from threading import Thread, Event
from dataclasses import dataclass, field

@dataclass(order=True)
class Task:
    priority: int
    sequence: int
    fn: object = field(compare=False)
    args: tuple = field(default_factory=tuple, compare=False)
    kwargs: dict = field(default_factory=dict, compare=False)

class PriorityTaskQueue:
    def __init__(self, workers=2):
        if workers <= 0:
            raise ValueError("workers must be positive")
        self.queue = PriorityQueue()
        self.stop_event = Event()
        self.sequence = 0
        self.threads = []
        for i in range(workers):
            t = Thread(target=self._worker, name=f"worker-{i}", daemon=True)
            t.start()
            self.threads.append(t)

    def submit(self, fn, *args, priority=100, **kwargs):
        self.sequence += 1
        self.queue.put(Task(priority, self.sequence, fn, args, kwargs))

    def _worker(self):
        while not self.stop_event.is_set():
            try:
                task = self.queue.get(timeout=0.1)
            except Empty:
                continue
            try:
                task.fn(*task.args, **task.kwargs)
            finally:
                self.queue.task_done()

    def join(self):
        self.queue.join()

    def shutdown(self):
        self.stop_event.set()
        for t in self.threads:
            t.join(timeout=1)
