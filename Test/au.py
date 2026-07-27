from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import pytz
import logging
import uuid
import traceback
import typing
import random

def GUUID():
    return str(uuid.uuid3(uuid.NAMESPACE_DNS, str(random.randint(0, 10000000000000000000))))


class Task:
    """Task Type, Encapsulating Task Attributes And Behaviors."""
    
    def __init__(self, task_data: typing.Dict):
        """
        初始化任务
        :param task_data: 任务数据字典
        """
        self.task_data=task_data
        self.uuid = task_data.get('TaskUUID', GUUID())
        self.name = task_data.get('TaskName', 'Unnamed Task')
        self.e_time_type = task_data.get('ETimeType')
        self.e_time = task_data.get('ETime')
        self.r_time_type = task_data.get('RTimeType')
        self.r_time = task_data.get('RTime')
        self.r_code = task_data.get('RCode')
        self.r_type = task_data.get('RType')
        
        # 验证必要字段
        if not all([self.e_time_type, self.r_time_type, self.r_code]):
            raise ValueError("Missing Necessary Task Parameters")

    def is_effective(self) -> bool:
        """检查任务是否在生效时间内"""
        now = datetime.now(pytz.timezone('Asia/Shanghai'))
        
        try:
            if self.e_time_type == '1':  # 具体时间
                effective_time = datetime.strptime(self.e_time, '%Y-%m-%d %H:%M:%S')
                effective_time = pytz.timezone('Asia/Shanghai').localize(effective_time)
                return now >= effective_time
            
            elif self.e_time_type == '2':  # 每日执行时间
                hour, minute, second = map(int, self.e_time.split(':'))
                effective_time = now.replace(hour=hour, minute=minute, second=second)
                return now >= effective_time
            
            # 其他类型默认返回True
            return True
        except Exception as e:
            print(f"Failed To Check The Effective Time Of Task {self.uuid}: {e}")
            return False

    def create_trigger(self) -> typing.Optional[typing.Union[DateTrigger, CronTrigger, IntervalTrigger]]:
        """根据时间类型创建对应的触发器"""
        try:
            if self.r_time_type == '1':  # 具体时间
                return DateTrigger(run_date=datetime.strptime(self.r_time, '%Y-%m-%d %H:%M:%S'))
            
            elif self.r_time_type == '2':  # 每日执行时间
                hour, minute, second = map(int, self.r_time.split(':'))
                return CronTrigger(hour=hour, minute=minute, second=second)
            
            elif self.r_time_type == '3':  # 每周循环时间
                parts = self.r_time.split()
                day_of_week = parts[0]  # 1-7，1=周一
                hour, minute, second = map(int, parts[1].split(':'))
                return CronTrigger(day_of_week=day_of_week, hour=hour, minute=minute, second=second)
            
            elif self.r_time_type == '4':  # 月循环时间
                parts = self.r_time.split()
                day = parts[0]  # 1-31
                hour, minute, second = map(int, parts[1].split(':'))
                return CronTrigger(day=day, hour=hour, minute=minute, second=second)
            
            elif self.r_time_type == '5':  # 间隔时间
                hour, minute, second = map(int, self.r_time.split(':'))
                return IntervalTrigger(hours=hour, minutes=minute, seconds=second)
            
            elif self.r_time_type == '6':  # 开机时执行
                return None  # 已在调度器中特殊处理
            
            return None
        except Exception as e:
            print(f"Failed To Create Scheduler For Task {self.uuid} : {e}")
            return None


class TaskScheduler:
    """任务调度器类，管理所有任务的调度"""
    
    def __init__(self, ExecuteCallBack=lambda x, y, z: exec(y)):
        self.ExecuteCallBack=ExecuteCallBack
        """初始化调度器"""
        # 初始化调度器，使用上海时区
        self.scheduler = BackgroundScheduler(timezone=pytz.timezone('Asia/Shanghai'))
        self.scheduler.start()
        
        # 存储任务对象
        self.tasks: typing.Dict[str, Task] = {}
        
        # 添加事件监听
        self.scheduler.add_listener(self._job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    
    def _job_listener(self, event):
        """Task Execution Event Listener"""
        if event.code == EVENT_JOB_EXECUTED:
            print(f"Task {event.job_id} Executed Successfully")
        elif event.code == EVENT_JOB_ERROR:
            print(f"Task {event.job_id} Execution Failed: {event.exception}")

    def add_task(self, task_data: typing.Dict) -> bool:
        """
        Add Tasks To The Scheduler
        :param task_data: Task Data Dictionary
        :return: Was It Added Successfully?
        """
        try:
            task = Task(task_data)
            
            # 检查生效时间是否已过
            if not task.is_effective():
                print(f"Task {task.uuid} The Effective Date Has Passed.")
                return False
            
            # 处理开机执行的任务
            if task.r_time_type == '6':
                print(f"Immediately Execute The StartUp Task: {task.name}")
                self._execute_code(task_data, task.r_code, task.r_type)
                return True
            
            # 创建触发器
            trigger = task.create_trigger()
            if not trigger:
                print(f"Unable To Create A Trigger For Task: {task.uuid}")
                return False
            
            # 添加任务到调度器
            self.scheduler.add_job(
                self._execute_code,
                trigger=trigger,
                args=[task_data, task.r_code, task.r_type],
                id=task.uuid,
                name=task.name,
                misfire_grace_time=60,  # 允许60秒的延迟执行
            )
            
            # 存储任务对象
            self.tasks[task.uuid] = task
            print(f"Task {task.uuid} Has Been Added.")
            return True
            
        except Exception as e:
            print(f"Failed To Add Task: {e}")
            return False
    
    def remove_task(self, task_uuid: str) -> bool:
        """
        移除任务
        :param task_uuid: 任务UUID
        :return: 是否移除成功
        """
        if task_uuid not in self.tasks:
            print(f"任务 {task_uuid} 不存在")
            return False

        try:
            # 从调度器中移除
            try:
                self.scheduler.remove_job(task_uuid)
            except:
                pass

            # 从任务字典中移除
            del self.tasks[task_uuid]
            
            print(f"Task {task_uuid} Has Been Removed")
            return True
        except Exception as e:
            print(traceback.format_exc())
            print(f"Failed To Remove Task {task_uuid}: {e}")
            return False
    
    def get_task(self, task_uuid: str) -> typing.Optional[typing.Dict]:
        """
        获取任务信息
        :param task_uuid: 任务UUID
        :return: 任务信息字典或None
        """
        task = self.tasks.get(task_uuid)
        if not task:
            return None
        
        return {
            'TaskUUID': task.uuid,
            'TaskName': task.name,
            'ETimeType': task.e_time_type,
            'ETime': task.e_time,
            'RTimeType': task.r_time_type,
            'RTime': task.r_time,
            'RCode': task.r_code,
            'RType': task.r_type
        }
    
    def list_tasks(self) -> typing.Dict[str, typing.Dict]:
        """Get All Task Information"""
        return {uuid: self.get_task(uuid) for uuid in self.tasks}
    
    def _execute_code(self, task: dict, _code: str, _type: str):
        self.ExecuteCallBack(task, _code, _type)
    
    def shutdown(self):
        """关闭调度器"""
        self.scheduler.shutdown()
        print("Task Scheduler Has Been Closed.")
"""
请你使用python apscheduler做一个调度器，实现以下功能:

### 1. 初始化调度器
```python
scheduler = TaskScheduler(ExecuteCallBack=lambda x, y, z: exec(y))
```
- **参数**:
  - `ExecuteCallBack`: 任务执行时的回调函数，默认为直接执行Python代码
- **功能**: 创建后台调度器实例，使用UTC-8时区

### 2. 添加任务
```python
add_task(task_data: dict) -> bool
```
- **参数**:
  - `task_data`: 包含任务配置的字典，必须包含以下关键字段:
    - `ETimeType`: 生效时间类型
    - `ETime`: 生效时间
    - `RTimeType`: 执行时间类型
    - `RTime`: 执行时间
    - `LTimeType`: 失效时间类型
    - `LTime`: 失效时间
    - `RCode`: 要执行的代码
- **返回值**: 布尔值表示是否添加成功
- **功能**: 根据任务配置创建并调度任务

### 3. 移除任务
```python
remove_task(task_uuid: str) -> bool
```
- **参数**:
  - `task_uuid`: 要移除的任务ID
- **返回值**: 布尔值表示是否移除成功
- **功能**: 从调度器中移除指定任务

### 4. 获取单个任务信息
```python
get_task(task_uuid: str) -> Optional[dict]
```
- **参数**:
  - `task_uuid`: 要查询的任务ID
- **返回值**: 包含任务信息的字典或None
- **功能**: 获取指定任务的详细配置信息

### 5. 列出所有任务
```python
list_tasks() -> Dict[str, Dict]
```
- **返回值**: 字典格式的所有任务信息，键为任务ID
- **功能**: 获取当前所有已调度任务的列表

### 6. 关闭调度器
```python
shutdown()
```
- **功能**: 停止调度器运行，释放资源

## 任务配置参数详解

### 生效时间类型 (ETimeType)
| 值 | 类型 | ETime格式 | 描述 |
|----|------|-----------|------|
| '1' | 具体时间 | 'YYYY-MM-DD HH:MM:SS' | 在指定时间点后生效 |
| '2' | 每日时间 | 'HH:MM:SS' | 每天指定时间后生效 |
| '3' | 永久生效 | 无 | 永久生效 |

### 执行时间类型 (RTimeType)
| 值 | 类型 | RTime格式 | 描述 |
|----|------|-----------|------|
| '1' | 具体时间 | 'YYYY-MM-DD HH:MM:SS' | 在指定时间点执行一次 |
| '2' | 每日执行 | 'HH:MM:SS' | 每天固定时间执行 |
| '3' | 每周执行 | 'D HH:MM:SS' | 每周特定星期几执行 (1=周一) |
| '4' | 每月执行 | 'D HH:MM:SS' | 每月特定日期执行 |
| '5' | 间隔执行 | 'HH:MM:SS' | 按固定间隔重复执行 |
| '6' | 开机执行 | 无 | 调度器启动时立即执行 |
| '7' | 开机延时执行 | 'SS' | 调度器启动时等待一段时间执行 |

### 失效时间类型 (LTimeType)
| 值 | 类型 | LTime格式 | 描述 |
|----|------|-----------|------|
| '1' | 具体时间 | 'YYYY-MM-DD HH:MM:SS' | 在指定时间点失生效 |
| '2' | 每日时间 | 'HH:MM:SS' | 每天指定时间后失效 |
| '3' | 永久生效 | 无 | 不会失效 |

### 其他参数
- `TaskName`: 任务名称(可选)
- `TaskUUID`: 任务ID(可选，不提供会自动生成)
- `RCode`: 要执行的代码内容
- `RType`: 代码类型(Python/Shell等，直接提交给回调，不由调度器处理)

## 使用流程示例

1. 初始化调度器
2. 准备任务配置字典
3. 调用`add_task()`添加任务
4. (可选)使用`list_tasks()`查看任务
5. (可选)使用`remove_task()`删除任务
6. 程序结束时调用`shutdown()`关闭调度器

## 注意事项

注意除调度器外还有一个task_dict用于存储所有的task_data，格式{"UUID": task_data}，task_data也有相同的UUID，还有是否生效的标志working_status。

1. 所有时间都使用UTF-8时区（东八区）。
2. 任务ID(TaskUUID)必须唯一，不提供会自动生成。
3. 开机执行的任务(RTimeType='6')会立即执行，会被添加到调度器中，但是被设置为失效。
4. 调度器使用后台线程，主程序需要保持运行状态才能执行定时任务
5. 注意任务完成和失效后不要从调度器中移除任务，而是将属性设置为失效。
6. 如果是2345时间类型的任务则不可能失效。
7. 生效时间3和执行时间6还有失效时间3可以没有ETime和RTime和LTime（或者可以任意填写）。
8. 生效时间类型的优先级低于失效时间优先级，也就是即使生效时间为永久生效，如果设置了具体时间失效仍然会失效
9. 如果添加出错，允许返回错误信息，以便用户定位问题

使用以下作为示例
1:
'ETimeType': '3',
'RTimeType': '6',
'LTimeType': '1',
'LTime': '2025-05-18 03:16:00',
'RCode': 'print("HI")',
'TaskName': 'HI'
正常情况下这个示例由于已经过失效时间而被视为失效，会添加但是被设置为失效因此无法执行

2:
'ETimeType': '3',
'RTimeType': '6',
'LTimeType': '1',
'LTime': '2025-05-18 04:10:00',
'RCode': 'print("HI")',
'TaskName': 'HI'
正常情况下这个示例由于还没过失效时间而不被视为失效，会在添加的同时被执行

3:
'ETimeType': '1',
'ETime': '2025-05-18 07:20:40',
'RTimeType': '1',
'RTime': '2025-05-18 07:20:50',
'LTimeType': '1',
'LTime': '2025-05-18 07:25:00',
'RCode': 'print("HI")',
'TaskName': 'HI_Expired'
正常情况下这个示例由于还没到生效时间因此不被执行，但是仍然有效，因此到达生效时间和执行时间后才会执行，执行后会被设置为失效，执行前一直有效但不执行
但是注意，到达生效时间后不会立刻执行，而是继续等到执行时间才会继续执行，因此任务会在生效时间生效，并在执行时间执行，然后根据类型被选择是否设置为失效
如果未到达生效时间不应当被判断为失效，应当使用调度器设置在到达生效时间后自动生效，并在符合执行时间时执行！！！
如果未到达生效时间不应当被判断为失效，应当使用调度器设置在到达生效时间后自动生效，并在符合执行时间时执行！！！
如果未到达生效时间不应当被判断为失效，应当使用调度器设置在到达生效时间后自动生效，并在符合执行时间时执行！！！
如果未到达生效时间不应当被判断为失效，应当使用调度器设置在到达生效时间后自动生效，并在符合执行时间时执行！！！
如果未到达生效时间不应当被判断为失效，应当使用调度器设置在到达生效时间后自动生效，并在符合执行时间时执行！！！


4:
'ETimeType': '1',
'ETime': '2025-05-18 07:20:40',
'RTimeType': '6',
'LTimeType': '1',
'LTime': '2025-05-18 07:25:00',
'RCode': 'print("HI")',
'TaskName': 'HI_Expired'
该任务会在到达生效时间后立即执行，因为RTimeType为6开机执行，执行后会被设置为失效，如果当前时间超过失效时间后则不会执行，直接判断为失效"""