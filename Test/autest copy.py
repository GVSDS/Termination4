import uuid
import pytz
import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

class TaskScheduler:
    def __init__(self, ExecuteCallBack=None):
        # 设置时区为UTC-8
        self.timezone = pytz.timezone('Asia/Shanghai')
        # 初始化调度器
        self.scheduler = BackgroundScheduler(timezone=self.timezone)
        self.scheduler.start()
        # 任务数据存储
        self.task_dict = {}
        # 设置默认回调函数
        self.ExecuteCallBack = ExecuteCallBack or (lambda x, y, z: exec(y))
        # 配置日志
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger('TaskScheduler')

    def add_task(self, task_data: dict) -> bool:
        """添加新任务到调度器"""
        try:
            # 验证任务数据完整性
            required_fields = ['ETimeType', 'RTimeType', 'LTimeType', 'RCode']
            for field in required_fields:
                if field not in task_data:
                    raise ValueError(f"缺少必要字段: {field}")
            
            # 处理TaskUUID，没有则生成
            task_uuid = task_data.get('TaskUUID', str(uuid.uuid4()))
            if task_uuid in self.task_dict:
                raise ValueError(f"任务ID已存在: {task_uuid}")
            
            # 处理时间类型和时间值
            self._validate_time_fields(task_data)
            
            # 准备完整的任务数据
            full_task_data = {
                'TaskUUID': task_uuid,
                'TaskName': task_data.get('TaskName', f"Task_{task_uuid[:8]}"),
                'ETimeType': task_data['ETimeType'],
                'ETime': task_data.get('ETime'),
                'RTimeType': task_data['RTimeType'],
                'RTime': task_data.get('RTime'),
                'LTimeType': task_data['LTimeType'],
                'LTime': task_data.get('LTime'),
                'RCode': task_data['RCode'],
                'RType': task_data.get('RType', 'Python'),
                'working_status': False,  # 默认任务未激活
                'apscheduler_job_id': None,
                'creation_time': datetime.now(self.timezone).strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # 检查任务是否应该生效
            if self._should_task_be_active(full_task_data):
                full_task_data['working_status'] = True
                # 添加到调度器
                self._schedule_task(full_task_data)
            else:
                self.logger.info(f"任务 {task_uuid} 已添加但当前未激活")
            
            # 保存任务数据
            self.task_dict[task_uuid] = full_task_data
            return True
            
        except Exception as e:
            self.logger.error(f"添加任务失败: {str(e)}")
            return False

    def remove_task(self, task_uuid: str) -> bool:
        """从调度器中移除任务"""
        try:
            if task_uuid not in self.task_dict:
                return False
                
            task_data = self.task_dict[task_uuid]
            
            # 如果任务在调度器中，移除它
            if task_data['apscheduler_job_id'] and self.scheduler.get_job(task_data['apscheduler_job_id']):
                self.scheduler.remove_job(task_data['apscheduler_job_id'])
                
            # 从任务字典中删除
            del self.task_dict[task_uuid]
            return True
            
        except Exception as e:
            self.logger.error(f"移除任务失败: {str(e)}")
            return False

    def get_task(self, task_uuid: str) -> dict:
        """获取单个任务信息"""
        return self.task_dict.get(task_uuid)

    def list_tasks(self) -> dict:
        """列出所有任务"""
        return self.task_dict.copy()

    def shutdown(self):
        """关闭调度器"""
        self.scheduler.shutdown()

    def _validate_time_fields(self, task_data):
        """验证时间字段的有效性"""
        # 验证生效时间
        if task_data['ETimeType'] == '1':  # 具体时间
            if not task_data.get('ETime'):
                raise ValueError("ETimeType为1时需要提供ETime")
            self._parse_datetime(task_data['ETime'])
        elif task_data['ETimeType'] == '2':  # 每日时间
            if not task_data.get('ETime'):
                raise ValueError("ETimeType为2时需要提供ETime")
            self._parse_time(task_data['ETime'])
        elif task_data['ETimeType'] != '3':  # 永久生效
            raise ValueError("无效的ETimeType值")
            
        # 验证执行时间
        if task_data['RTimeType'] in ['1', '6', '7']:  # 具体时间/开机执行/开机延时执行
            if task_data['RTimeType'] == '1' and not task_data.get('RTime'):
                raise ValueError("RTimeType为1时需要提供RTime")
            if task_data['RTimeType'] == '1':
                self._parse_datetime(task_data['RTime'])
            if task_data['RTimeType'] == '7' and not task_data.get('RTime'):
                raise ValueError("RTimeType为7时需要提供RTime")
        elif task_data['RTimeType'] in ['2', '3', '4', '5']:  # 每日/每周/每月/间隔执行
            if not task_data.get('RTime'):
                raise ValueError(f"RTimeType为{task_data['RTimeType']}时需要提供RTime")
            if task_data['RTimeType'] == '2':  # 每日执行
                self._parse_time(task_data['RTime'])
            elif task_data['RTimeType'] == '3':  # 每周执行
                parts = task_data['RTime'].split(' ', 1)
                if len(parts) != 2:
                    raise ValueError("RTimeType为3时RTime格式应为'D HH:MM:SS'")
                day, time_str = parts
                if not day.isdigit() or int(day) not in range(1, 8):
                    raise ValueError("RTimeType为3时星期几必须是1-7之间的数字")
                self._parse_time(time_str)
            elif task_data['RTimeType'] == '4':  # 每月执行
                parts = task_data['RTime'].split(' ', 1)
                if len(parts) != 2:
                    raise ValueError("RTimeType为4时RTime格式应为'D HH:MM:SS'")
                day, time_str = parts
                if not day.isdigit() or int(day) not in range(1, 32):
                    raise ValueError("RTimeType为4时日期必须是1-31之间的数字")
                self._parse_time(time_str)
            elif task_data['RTimeType'] == '5':  # 间隔执行
                self._parse_time(task_data['RTime'])
        else:
            raise ValueError("无效的RTimeType值")
            
        # 验证失效时间
        if task_data['LTimeType'] == '1':  # 具体时间
            if not task_data.get('LTime'):
                raise ValueError("LTimeType为1时需要提供LTime")
            self._parse_datetime(task_data['LTime'])
        elif task_data['LTimeType'] == '2':  # 每日时间
            if not task_data.get('LTime'):
                raise ValueError("LTimeType为2时需要提供LTime")
            self._parse_time(task_data['LTime'])
        elif task_data['LTimeType'] != '3':  # 永久生效
            raise ValueError("无效的LTimeType值")

    def _should_task_be_active(self, task_data):
        """判断任务是否应该处于激活状态"""
        now = datetime.now(self.timezone)
        
        # 检查失效时间
        if task_data['LTimeType'] == '1':  # 具体时间失效
            ltime = self._parse_datetime(task_data['LTime'])
            if now > ltime:
                return False
        elif task_data['LTimeType'] == '2':  # 每日时间失效
            time_obj = self._parse_time(task_data['LTime'])
            ltime_today = datetime.combine(now.date(), time_obj.time())
            ltime_today = self.timezone.localize(ltime_today)
            if now > ltime_today:
                return False
                
        # 检查生效时间
        if task_data['ETimeType'] == '1':  # 具体时间生效
            etime = self._parse_datetime(task_data['ETime'])
            if now < etime:
                return False
        elif task_data['ETimeType'] == '2':  # 每日时间生效
            time_obj = self._parse_time(task_data['ETime'])
            etime_today = datetime.combine(now.date(), time_obj.time())
            etime_today = self.timezone.localize(etime_today)
            if now < etime_today:
                return False
                
        return True

    def _schedule_task(self, task_data):
        """将任务添加到调度器"""
        try:
            job_id = task_data['TaskUUID']
            task_name = task_data['TaskName']
            rcode = task_data['RCode']
            rtype = task_data['RType']
            
            # 根据执行时间类型创建不同的触发器
            if task_data['RTimeType'] == '1':  # 具体时间执行
                run_date = self._parse_datetime(task_data['RTime'])
                trigger = DateTrigger(run_date=run_date, timezone=self.timezone)
            elif task_data['RTimeType'] == '2':  # 每日执行
                time_parts = task_data['RTime'].split(':')
                hour, minute, second = map(int, time_parts)
                trigger = CronTrigger(hour=hour, minute=minute, second=second, timezone=self.timezone)
            elif task_data['RTimeType'] == '3':  # 每周执行
                day, time_str = task_data['RTime'].split(' ', 1)
                time_parts = time_str.split(':')
                hour, minute, second = map(int, time_parts)
                # 转换为APScheduler的星期格式 (0-6)
                day_of_week = str(int(day) - 1)
                trigger = CronTrigger(day_of_week=day_of_week, hour=hour, minute=minute, second=second, timezone=self.timezone)
            elif task_data['RTimeType'] == '4':  # 每月执行
                day, time_str = task_data['RTime'].split(' ', 1)
                time_parts = time_str.split(':')
                hour, minute, second = map(int, time_parts)
                trigger = CronTrigger(day=day, hour=hour, minute=minute, second=second, timezone=self.timezone)
            elif task_data['RTimeType'] == '5':  # 间隔执行
                time_parts = task_data['RTime'].split(':')
                hours = int(time_parts[0])
                minutes = int(time_parts[1])
                seconds = int(time_parts[2])
                total_seconds = hours * 3600 + minutes * 60 + seconds
                trigger = IntervalTrigger(seconds=total_seconds, timezone=self.timezone)
            elif task_data['RTimeType'] == '6':  # 开机执行
                # 立即执行一次
                self._execute_task(task_data)
                # 但不添加到调度器中，因为这种任务只执行一次
                return
            elif task_data['RTimeType'] == '7':  # 开机延时执行
                seconds = int(task_data['RTime'])
                run_date = datetime.now(self.timezone) + timedelta(seconds=seconds)
                trigger = DateTrigger(run_date=run_date, timezone=self.timezone)
            else:
                raise ValueError(f"不支持的RTimeType: {task_data['RTimeType']}")
            
            # 添加任务到调度器
            self.scheduler.add_job(
                func=self._execute_task_wrapper,
                trigger=trigger,
                args=[task_data],
                id=job_id,
                name=task_name,
                misfire_grace_time=3600  # 错过执行的宽限期（秒）
            )
            
            # 记录任务ID
            task_data['apscheduler_job_id'] = job_id
            self.logger.info(f"任务 {job_id} 已调度")
            
        except Exception as e:
            self.logger.error(f"调度任务失败: {str(e)}")
            # 如果调度失败，确保任务状态为未激活
            task_data['working_status'] = False

    def _execute_task_wrapper(self, task_data):
        """任务执行包装器，检查任务是否应该执行"""
        if self._should_task_be_active(task_data):
            self._execute_task(task_data)
        else:
            self.logger.info(f"任务 {task_data['TaskUUID']} 已失效，不执行")

    def _execute_task(self, task_data):
        """执行任务的实际方法"""
        try:
            self.logger.info(f"执行任务: {task_data['TaskName']} ({task_data['TaskUUID']})")
            # 调用回调函数执行任务代码
            self.ExecuteCallBack(task_data['TaskUUID'], task_data['RCode'], task_data['RType'])
        except Exception as e:
            self.logger.error(f"执行任务失败: {str(e)}")

    def _parse_datetime(self, datetime_str):
        """解析日期时间字符串"""
        try:
            # 尝试解析带时区的格式
            dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
            # 如果没有时区信息，添加本地时区
            if dt.tzinfo is None:
                dt = self.timezone.localize(dt)
            return dt
        except ValueError:
            # 尝试常见的日期时间格式
            for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S.%f'):
                try:
                    dt = datetime.strptime(datetime_str, fmt)
                    return self.timezone.localize(dt)
                except ValueError:
                    pass
            raise ValueError(f"无法解析日期时间: {datetime_str}")

    def _parse_time(self, time_str):
        """解析时间字符串"""
        try:
            time_obj = datetime.strptime(time_str, '%H:%M:%S')
            return time_obj
        except ValueError:
            raise ValueError(f"无法解析时间: {time_str}，格式应为'HH:MM:SS'")

# 继续对其测试，今天一定完成.idea里的任务！





"""
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
| '3' | 永久生效 | 无 | 不会失效 |"""





# 示例使用
if __name__ == "__main__":
    # 创建调度器实例
    scheduler = TaskScheduler()

    task1 = {
        'ETimeType': '1',
        'ETime': '2025-05-18 07:20:40',
        'RTimeType': '6',
        'RTime': '2025-05-18 07:22:50',
        'LTimeType': '1',
        'LTime': '2025-05-18 07:25:00',
        'RCode': 'print("HI")',
        'TaskName': 'HI_Expired'
    }
    
    # 添加任务
    scheduler.add_task(task1)
    
    # 列出所有任务
    print("\n所有任务:")
    for task_id, task in scheduler.list_tasks().items():
        print(f"ID: {task_id}, 名称: {task['TaskName']}, 状态: {'激活' if task['working_status'] else '未激活'}")
    
    # 保持主程序运行
    try:
        while True:
            pass
    except KeyboardInterrupt:
        scheduler.shutdown()
        print("\n调度器已关闭")