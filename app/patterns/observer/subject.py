from abc import ABC, abstractmethod

class Subject:
    """Subject class for Observer pattern - manages observers and notifications"""
    
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        """Attach an observer"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer):
        """Detach an observer"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, event_type, data):
        """Notify all observers of an event"""
        for observer in self._observers:
            observer.update(event_type, data)
