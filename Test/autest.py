import uuid
import pytz
from datetime import datetime, timedelta
from typing import Dict, Optional, Callable, Any
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.job import Job

class TaskScheduler:
    def __init__(self, ExecuteCallBack: Callable[[str, str, str], Any] = lambda x, y, z: exec(y)):
        """
        初始化调度器
        
        参数:
            ExecuteCallBack: 任务执行时的回调函数，默认为直接执行Python代码
        """
        self.scheduler = BackgroundScheduler(timezone=pytz.timezone('Asia/Shanghai'))  # UTC+8时区
        self.task_dict: Dict[str, Dict] = {}  # 存储所有任务数据
        self.ExecuteCallBack = ExecuteCallBack
        self.scheduler.start()
    
    def _generate_uuid(self) -> str:
        """生成唯一任务ID"""
        return str(uuid.uuid4())
    
    def _parse_time(self, time_str: str, time_format: str) -> datetime:
        """解析时间字符串为datetime对象"""
        return datetime.strptime(time_str, time_format).replace(tzinfo=pytz.timezone('Asia/Shanghai'))
    
    def _get_trigger(self, task_data: Dict) -> Any:
        """根据任务数据获取对应的触发器"""
        rtime_type = task_data['RTimeType']
        now = datetime.now(pytz.timezone('Asia/Shanghai'))
        
        if rtime_type == '1':  # 具体时间执行一次
            run_time = self._parse_time(task_data['RTime'], '%Y-%m-%d %H:%M:%S')
            return DateTrigger(run_date=run_time)
        
        elif rtime_type == '2':  # 每日固定时间执行
            hour, minute, second = map(int, task_data['RTime'].split(':'))
            return CronTrigger(hour=hour, minute=minute, second=second, timezone='Asia/Shanghai')
        
        elif rtime_type == '3':  # 每周特定星期几执行
            day_of_week, time_part = task_data['RTime'].split(' ', 1)
            hour, minute, second = map(int, time_part.split(':'))
            return CronTrigger(day_of_week=day_of_week, hour=hour, minute=minute, second=second, timezone='Asia/Shanghai')
        
        elif rtime_type == '4':  # 每月特定日期执行
            day, time_part = task_data['RTime'].split(' ', 1)
            hour, minute, second = map(int, time_part.split(':'))
            return CronTrigger(day=day, hour=hour, minute=minute, second=second, timezone='Asia/Shanghai')
        
        elif rtime_type == '5':  # 固定间隔执行
            hours, minutes, seconds = map(int, task_data['RTime'].split(':'))
            delta = timedelta(hours=hours, minutes=minutes, seconds=seconds)
            return IntervalTrigger(seconds=delta.total_seconds(), timezone='Asia/Shanghai')
        
        elif rtime_type == '6':  # 开机立即执行
            return DateTrigger(run_date=now)
        
        elif rtime_type == '7':  # 开机延时执行
            seconds = int(task_data['RTime'])
            return DateTrigger(run_date=now + timedelta(seconds=seconds))
        
        else:
            raise ValueError(f"未知的执行时间类型: {rtime_type}")
    
    def _check_task_valid(self, task_data: Dict) -> bool:
        """检查任务是否有效(未过期)"""
        now = datetime.now(pytz.timezone('Asia/Shanghai'))
        
        # 检查生效时间
        etime_type = task_data['ETimeType']
        if etime_type == '1':  # 具体时间生效
            effective_time = self._parse_time(task_data['ETime'], '%Y-%m-%d %H:%M:%S')
            if now < effective_time:
                return False
        elif etime_type == '2':  # 每日时间生效
            effective_time = self._parse_time(task_data['ETime'], '%H:%M:%S')
            now_time = now.time()
            if now_time < effective_time.time():
                return False
        
        # 检查失效时间
        ltime_type = task_data['LTimeType']
        if ltime_type == '1':  # 具体时间失效
            expire_time = self._parse_time(task_data['LTime'], '%Y-%m-%d %H:%M:%S')
            if now >= expire_time:
                return False
        elif ltime_type == '2':  # 每日时间失效
            expire_time = self._parse_time(task_data['LTime'], '%H:%M:%S')
            now_time = now.time()
            if now_time >= expire_time.time():
                return False
        
        return True
    
    def _execute_task(self, task_uuid: str):
        """执行任务的实际函数"""
        task_data = self.task_dict.get(task_uuid)
        if not task_data:
            return
        
        # 检查任务是否仍然有效
        if not self._check_task_valid(task_data):
            task_data['working_status'] = False
            return
        
        # 执行回调
        try:
            self.ExecuteCallBack(task_uuid, task_data['RCode'], task_data.get('RType', ''))
        except Exception as e:
            print(f"执行任务 {task_uuid} 时出错: {str(e)}")
        
        # 如果是一次性任务，执行后设置为失效
        if task_data['RTimeType'] in ['1', '6', '7']:
            task_data['working_status'] = False
    
    def add_task(self, task_data: Dict) -> bool:
        """
        添加任务到调度器
        
        参数:
            task_data: 包含任务配置的字典
            
        返回值:
            bool: 是否添加成功
        """
        try:
            # 验证必要字段
            required_fields = ['ETimeType', 'RTimeType', 'LTimeType', 'RCode']
            for field in required_fields:
                if field not in task_data:
                    raise ValueError(f"缺少必要字段: {field}")
            
            # 生成或使用提供的任务ID
            task_uuid = task_data.get('TaskUUID', self._generate_uuid())
            task_data['TaskUUID'] = task_uuid
            
            # 设置任务初始状态
            task_data['working_status'] = self._check_task_valid(task_data)
            
            # 如果任务已经失效，不添加到调度器
            if not task_data['working_status']:
                self.task_dict[task_uuid] = task_data
                return True
            
            # 获取触发器
            trigger = self._get_trigger(task_data)
            
            # 添加到调度器
            job = self.scheduler.add_job(
                self._execute_task,
                trigger=trigger,
                args=[task_uuid],
                id=task_uuid
            )
            
            # 存储任务数据
            self.task_dict[task_uuid] = task_data
            return True
            
        except Exception as e:
            print(f"添加任务失败: {str(e)}")
            return False
    
    def remove_task(self, task_uuid: str) -> bool:
        """
        从调度器中移除任务
        
        参数:
            task_uuid: 要移除的任务ID
            
        返回值:
            bool: 是否移除成功
        """
        if task_uuid not in self.task_dict:
            return False
        
        # 从调度器中移除
        self.scheduler.remove_job(task_uuid)
        
        # 从任务字典中移除
        del self.task_dict[task_uuid]
        return True
    
    def get_task(self, task_uuid: str) -> Optional[Dict]:
        """
        获取单个任务信息
        
        参数:
            task_uuid: 要查询的任务ID
            
        返回值:
            dict: 包含任务信息的字典或None
        """
        return self.task_dict.get(task_uuid)
    
    def list_tasks(self) -> Dict[str, Dict]:
        """
        列出所有任务
        
        返回值:
            dict: 所有任务信息的字典，键为任务ID
        """
        return self.task_dict.copy()
    
    def shutdown(self):
        """停止调度器运行，释放资源"""
        self.scheduler.shutdown(wait=True)

# 示例使用
if __name__ == "__main__":
    # 初始化调度器
    scheduler = TaskScheduler()
    
    # 示例1: 已过期的任务
    task1 = {
        'ETimeType': '3',
        'RTimeType': '6',
        'LTimeType': '1',
        'LTime': '2025-05-18 03:16:00',
        'RCode': 'print("HI from task1")',
        'TaskName': 'HI'
    }
    scheduler.add_task(task1)
    
    # 示例2: 未过期的任务（会立即执行）
    task2 = {
        'ETimeType': '3',
        'RTimeType': '6',
        'LTimeType': '1',
        'LTime': '2025-05-18 09:10:00',
        'RCode': 'print("HI from task2")',
        'TaskName': 'HI'
    }
    scheduler.add_task(task2)
    
    # 示例3: 未到生效时间的任务
    task3 = {
        'ETimeType': '1',
        'ETime': '2025-05-18 09:29:10',
        'RTimeType': '1',
        'RTime': '2025-05-18 09:29:20',
        'LTimeType': '1',
        'LTime': '2025-05-18 09:30:00',
        'RCode': 'print("HI from task3")',
        'TaskName': 'HI_Expired'
    }
    scheduler.add_task(task3)
    
    # 示例4: 到达生效时间后立即执行的任务
    task4 = {
        'ETimeType': '1',
        'ETime': '2025-05-18 07:20:40',
        'RTimeType': '6',
        'LTimeType': '1',
        'LTime': '2025-05-18 07:25:00',
        'RCode': 'print("HI from task4")',
        'TaskName': 'HI_Expired'
    }
    scheduler.add_task(task4)
    
    # 保持程序运行
    try:
        while True:
            pass
    except KeyboardInterrupt:
        scheduler.shutdown()