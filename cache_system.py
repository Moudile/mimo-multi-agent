import json
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from collections import OrderedDict

class SmartCache:
    def __init__(self, max_size: int = 1000, ttl_hours: int = 24):
        self.cache = OrderedDict()
        self.max_size = max_size
        self.ttl = timedelta(hours=ttl_hours)
    
    def _get_key(self, prompt: str, model: str) -> str:
        return hashlib.md5(f"{prompt}:{model}".encode()).hexdigest()
    
    def get(self, prompt: str, model: str) -> Optional[Any]:
        key = self._get_key(prompt, model)
        
        if key in self.cache:
            entry = self.cache[key]
            if datetime.now() - entry["timestamp"] < self.ttl:
                self.cache.move_to_end(key)
                return entry["data"]
            else:
                del self.cache[key]
        
        return None
    
    def set(self, prompt: str, model: str, data: Any) -> None:
        key = self._get_key(prompt, model)
        
        if len(self.cache) >= self.max_size:
            self.cache.popitem(last=False)
        
        self.cache[key] = {
            "data": data,
            "timestamp": datetime.now()
        }
    
    def clear(self):
        self.cache.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "ttl_hours": self.ttl.total_seconds() / 3600
        }

class TaskQueue:
    def __init__(self, max_workers: int = 4):
        self.queue = []
        self.max_workers = max_workers
        self.running_tasks = set()
    
    def enqueue(self, task_id: str, task_data: Dict[str, Any]) -> None:
        self.queue.append({"task_id": task_id, **task_data})
    
    def dequeue(self) -> Optional[Dict[str, Any]]:
        if self.queue and len(self.running_tasks) < self.max_workers:
            task = self.queue.pop(0)
            self.running_tasks.add(task["task_id"])
            return task
        return None
    
    def complete(self, task_id: str) -> None:
        if task_id in self.running_tasks:
            self.running_tasks.remove(task_id)
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "pending": len(self.queue),
            "running": len(self.running_tasks),
            "max_workers": self.max_workers
        }