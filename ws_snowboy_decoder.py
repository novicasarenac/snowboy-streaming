import time
from snowboy import snowboydecoder


class WSHotwordDetector(snowboydecoder.HotwordDetector):

    def extend_buffer(self, data):
        self.ring_buffer.extend(data)
    
    def check_buffer(self):
        return True if len(self.ring_buffer._buf) > 4000 else False

    def perform_detection(self):
        data = self.ring_buffer.get()
        status = self.detector.RunDetection(data)
        
        return True if status > 0 else False
        