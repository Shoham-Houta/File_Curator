import os
import time
import magic
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from watchdog.observers import Observer
from threading import Timer

from rules import RuleEngine


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, rule_engine: RuleEngine, debounce_interval=1.0,):
        self.debounce_interval = debounce_interval
        self.debounce_timers = {}
        self.rule_engine = rule_engine

    def on_any_event(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return
        if event.event_type == "deleted":
            print(f"File Deleted: {event.src_path}")
            return

        path = event.src_path
        if path in self.debounce_timers:
            self.debounce_timers[path].cancel()
        timer = Timer(self.debounce_interval,self.process_event, args=(event,))
        self.debounce_timers[path] = timer
        timer.start()

    def process_event(self, event: FileSystemEvent) -> None:
        path = event.src_path
        if not os.path.exists(path):
            return
        try:
            file_description = magic.from_file(path, mime=True)
            log = self.rule_engine.evaluate(path, file_description)
            if log:
                print(f"Action Log: {log}")
        except FileNotFoundError:
            print(f"File not found: {path}")
            return
        
        if event.event_type == "created":
            print(f"File Created: {event.src_path}")
        elif event.event_type == "modified":
            print(f"File Modified: {event.src_path}")

        if path in self.debounce_timers:
            del self.debounce_timers[path]


def start_watcher(paths_to_watch: list[str]):
    rule_engine = RuleEngine()
    event_handler = FileChangeHandler(rule_engine)
    observer = Observer()
    for path_to_watch in paths_to_watch:
        observer.schedule(event_handler, path_to_watch, recursive=True)
        print(f"Watching for file changes in '{path_to_watch}' ...")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping watcher...")
        observer.stop()
    observer.join()


if __name__ == "__main__":
    start_watcher(["./data/watch_folder", "./data/documents", "./data/downloads", "./data/images"])
