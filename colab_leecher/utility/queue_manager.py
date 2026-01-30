# ⛏️ MiN3R × Colab Station | https://github.com/AdittyaMondal/MiN3R-Colab-Station
# Multi-task queue management system

import asyncio
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Any
from datetime import datetime
from uuid import uuid4


class TaskStatus(Enum):
    """Status of a task in the queue"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TaskItem:
    """Represents a single download/upload task"""
    task_id: str = field(default_factory=lambda: str(uuid4())[:8])
    source: List[str] = field(default_factory=list)
    mode: str = "leech"  # leech, mirror, dir-leech
    task_type: str = "normal"  # normal, zip, unzip, undzip
    ytdl: bool = False
    custom_name: str = ""
    zip_pswd: str = ""
    unzip_pswd: str = ""
    status: TaskStatus = TaskStatus.PENDING
    progress: float = 0.0
    progress_message: str = ""
    status_msg: Any = None  # Telegram message object
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: str = ""
    
    # Settings snapshot at task creation time
    stream_upload: bool = True
    caption_style: str = "code"
    convert_video: bool = True
    video_out: str = "mp4"


class TaskQueue:
    """Manages the task queue with add, get, cancel operations"""
    
    def __init__(self):
        self._queue: List[TaskItem] = []
        self._current_task: Optional[TaskItem] = None
        self._lock = asyncio.Lock()
        self._task_added_event = asyncio.Event()
        
    @property
    def current_task(self) -> Optional[TaskItem]:
        return self._current_task
    
    @current_task.setter  
    def current_task(self, task: Optional[TaskItem]):
        self._current_task = task
        
    @property
    def is_processing(self) -> bool:
        """Check if a task is currently being processed"""
        return self._current_task is not None and self._current_task.status == TaskStatus.RUNNING
    
    @property
    def pending_count(self) -> int:
        """Number of pending tasks in queue"""
        return len([t for t in self._queue if t.status == TaskStatus.PENDING])
    
    @property
    def all_tasks(self) -> List[TaskItem]:
        """Get all tasks including current"""
        tasks = []
        if self._current_task:
            tasks.append(self._current_task)
        tasks.extend(self._queue)
        return tasks
    
    async def add_task(
        self,
        source: List[str],
        mode: str,
        task_type: str,
        ytdl: bool = False,
        custom_name: str = "",
        zip_pswd: str = "",
        unzip_pswd: str = "",
        stream_upload: bool = True,
        caption_style: str = "code",
        convert_video: bool = True,
        video_out: str = "mp4"
    ) -> TaskItem:
        """Add a new task to the queue"""
        async with self._lock:
            task = TaskItem(
                source=source,
                mode=mode,
                task_type=task_type,
                ytdl=ytdl,
                custom_name=custom_name,
                zip_pswd=zip_pswd,
                unzip_pswd=unzip_pswd,
                stream_upload=stream_upload,
                caption_style=caption_style,
                convert_video=convert_video,
                video_out=video_out
            )
            self._queue.append(task)
            self._task_added_event.set()
            logging.info(f"Task {task.task_id} added to queue. Queue size: {len(self._queue)}")
            return task
    
    async def get_next_task(self) -> Optional[TaskItem]:
        """Get the next pending task from queue"""
        async with self._lock:
            for task in self._queue:
                if task.status == TaskStatus.PENDING:
                    self._queue.remove(task)
                    return task
            return None
    
    async def wait_for_task(self, timeout: float = None) -> bool:
        """Wait for a new task to be added"""
        self._task_added_event.clear()
        try:
            await asyncio.wait_for(self._task_added_event.wait(), timeout=timeout)
            return True
        except asyncio.TimeoutError:
            return False
    
    def get_task_by_id(self, task_id: str) -> Optional[TaskItem]:
        """Get a task by its ID"""
        if self._current_task and self._current_task.task_id == task_id:
            return self._current_task
        for task in self._queue:
            if task.task_id == task_id:
                return task
        return None
    
    def get_queue_position(self, task_id: str) -> int:
        """Get position of task in queue (1-indexed, 0 if not found or running)"""
        if self._current_task and self._current_task.task_id == task_id:
            return 0  # Currently running
        position = 1
        for task in self._queue:
            if task.task_id == task_id:
                return position
            if task.status == TaskStatus.PENDING:
                position += 1
        return -1  # Not found
    
    async def cancel_task(self, task_id: str) -> tuple[bool, str]:
        """Cancel a task by ID. Returns (success, message)"""
        async with self._lock:
            # Check if it's the current task
            if self._current_task and self._current_task.task_id == task_id:
                self._current_task.status = TaskStatus.CANCELLED
                return True, "Current task marked for cancellation"
            
            # Check queue
            for task in self._queue:
                if task.task_id == task_id:
                    if task.status == TaskStatus.PENDING:
                        task.status = TaskStatus.CANCELLED
                        self._queue.remove(task)
                        return True, f"Task {task_id} cancelled and removed from queue"
                    else:
                        return False, f"Task {task_id} cannot be cancelled (status: {task.status.value})"
            
            return False, f"Task {task_id} not found"
    
    def get_queue_status(self) -> str:
        """Get formatted queue status message"""
        if not self._current_task and not self._queue:
            return "📭 **Queue is empty**\n\nNo tasks running or pending."
        
        lines = ["📋 **Task Queue Status**\n"]
        
        if self._current_task:
            status_emoji = "🔄" if self._current_task.status == TaskStatus.RUNNING else "⏸️"
            progress = f"{self._current_task.progress:.1f}%" if self._current_task.progress > 0 else "Starting..."
            lines.append(f"{status_emoji} **Running:** `{self._current_task.task_id}`")
            lines.append(f"   └ {self._current_task.mode.upper()} | {progress}")
            lines.append("")
        
        pending_tasks = [t for t in self._queue if t.status == TaskStatus.PENDING]
        if pending_tasks:
            lines.append(f"⏳ **Pending ({len(pending_tasks)}):**")
            for i, task in enumerate(pending_tasks[:5], 1):  # Show max 5
                source_preview = task.source[0][:30] + "..." if len(task.source[0]) > 30 else task.source[0]
                lines.append(f"   {i}. `{task.task_id}` - {task.mode}")
            if len(pending_tasks) > 5:
                lines.append(f"   ... and {len(pending_tasks) - 5} more")
        
        return "\n".join(lines)


# Global task queue instance
task_queue = TaskQueue()


async def queue_worker():
    """Background worker that processes tasks from the queue"""
    from colab_leecher.utility.task_manager import execute_queued_task
    
    logging.info("Queue worker started")
    
    while True:
        try:
            # Wait for tasks if queue is empty
            if task_queue.pending_count == 0 and not task_queue.is_processing:
                logging.info("Queue worker waiting for tasks...")
                await task_queue.wait_for_task(timeout=60)
            
            # Get next task if not currently processing
            if not task_queue.is_processing:
                task = await task_queue.get_next_task()
                
                if task:
                    logging.info(f"Queue worker processing task: {task.task_id}")
                    task_queue.current_task = task
                    task.status = TaskStatus.RUNNING
                    task.started_at = datetime.now()
                    
                    try:
                        await execute_queued_task(task)
                        task.status = TaskStatus.COMPLETED
                        task.completed_at = datetime.now()
                        logging.info(f"Task {task.task_id} completed successfully")
                    except asyncio.CancelledError:
                        task.status = TaskStatus.CANCELLED
                        logging.info(f"Task {task.task_id} was cancelled")
                    except Exception as e:
                        task.status = TaskStatus.FAILED
                        task.error_message = str(e)
                        logging.error(f"Task {task.task_id} failed: {e}")
                    finally:
                        task_queue.current_task = None
            
            await asyncio.sleep(1)  # Small delay between checks
            
        except Exception as e:
            logging.error(f"Queue worker error: {e}")
            await asyncio.sleep(5)  # Wait before retrying on error
