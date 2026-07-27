import datetime
import typing
import uuid
import time


class TimeInterval:
    def __init__(self, Mode: typing.Literal["Year", "Week", "Day", "Hour", "Minute"], StartTime: int, EndTime: int):
        self.Mode = Mode if Mode and Mode in ["Year", "Week", "Day", "Hour", "Minute"] else "Year"
        self.StartTime = StartTime if StartTime else -1
        self.EndTime = EndTime if EndTime else 100 ** 100

    def __bool__(self):
        if self.Mode == "Year": return self.StartTime <= time.time() <= self.EndTime
        if self.Mode == "Week": return self.StartTime <= time.time() - time.time() % (60 * 60 * 24 * 7) <= self.EndTime
        if self.Mode == "Day": return self.StartTime <= time.time() - time.time() % (60 * 60 * 24) <= self.EndTime
        if self.Mode == "Hour": return self.StartTime <= time.time() - time.time() % (60 * 60) <= self.EndTime
        if self.Mode == "Minute": return self.StartTime <= time.time() - time.time() % (60) <= self.EndTime
        return False

    def __dict__(self):
        return {"Mode": self.Mode, "StartTime": self.StartTime, "EndTime": self.EndTime}

    def __str__(self):
        return "<TimeInterval: MODE|[%s] STARTIME|[%s] ENDTIME|[%s]>" % (self.Mode, self.StartTime, self.EndTime)

    def __repr__(self):
        return self.__str__()


class LW3Task:
    def __init__(self, TaskUUID: str | None = None,
                 TaskName: str = "",
                 TaskType: str = "",
                 TaskStatus: str = "Running",
                 TaskCondition: str = "",
                 TaskAllowableErrorCount: int = None,
                 TaskDestroyImmediatelyUponCompletion: bool = False,
                 TaskExistsCalculation: TimeInterval = None,
                 TaskTimeCriticalParameters: float | str | None = "",
                 TaskCallBackVarDict: dict = {},
                 TaskCallBackDict: dict = {},
                 TaskCallBack: typing.Callable | None = None,
                 TaskLastExecutionTime: float = 0
                 ) -> None:
        self.TaskUUID: str = TaskUUID if TaskUUID else str(uuid.uuid4()).replace("-", "").upper()
        self.TaskName: str = TaskName
        self.TaskType: str = TaskType
        self.TaskStatus: str = TaskStatus
        self.TaskCondition: str | typing.Callable = TaskCondition
        self.TaskAllowableErrorCount: int = TaskAllowableErrorCount
        if TaskAllowableErrorCount is None:
            if TaskType == "Once": self.TaskAllowableErrorCount = 5
            if TaskType == "Interval": self.TaskAllowableErrorCount = 1
        self.TaskDestroyImmediatelyUponCompletion: bool = TaskDestroyImmediatelyUponCompletion
        self.TaskExistsCalculation: TimeInterval = TaskExistsCalculation
        self.TaskTimeCriticalParameters: float | str | None = TaskTimeCriticalParameters
        self.TaskCallBackVarDict: dict = TaskCallBackVarDict
        self.TaskCallBackDict: dict = TaskCallBackDict
        self.TaskCallBack: typing.Callable = TaskCallBack
        self.TaskLastExecutionTime: float = TaskLastExecutionTime

    def __dict__(self):
        return {"TaskUUID": self.TaskUUID,
                "TaskName": self.TaskName,
                "TaskType": self.TaskType,
                "TaskStatus": self.TaskStatus,
                "TaskCondition": self.TaskCondition,
                "TaskAllowableErrorCount": self.TaskAllowableErrorCount,
                "TaskDestroyImmediatelyUponCompletion": self.TaskDestroyImmediatelyUponCompletion,
                "TaskExistsCalculation": self.TaskExistsCalculation.__dict__(),
                "TaskTimeCriticalParameters": self.TaskTimeCriticalParameters,
                "TaskCallBackVarDict": self.TaskCallBackVarDict,
                "TaskCallBackDict": self.TaskCallBackDict,
                "TaskCallBack": str(self.TaskCallBack),
                "TaskLastExecutionTime": self.TaskLastExecutionTime
                }

    def __str__(self):
        return "<LW3Task: UUID|[%s] NAME|[%s] TYPE|[%s] STATUS|[%s]>" % (
            self.TaskUUID, self.TaskName, self.TaskType, self.TaskStatus)


class LW3TScheduler:
    def __init__(self, VarDict: dict, SleepTime: int = 0.01):
        self.VarDict: dict = VarDict
        self.Tasks: dict = {}
        self.SleepTime: int = SleepTime
        self._TaskKeys: list = ["TaskUUID",
                                "TaskName",
                                "TaskType",
                                "TaskStatus",
                                "TaskCondition",
                                "TaskAllowableErrorCount",
                                "TaskDestroyImmediatelyUponCompletion",
                                "TaskExistsCalculation",
                                "TaskTimeCriticalParameters",
                                "TaskCallBackVarDict",
                                "TaskCallBackDict",
                                "TaskCallBack",
                                "TaskLastExecutionTime"
                                ]
        self._TaskTypes: list = ["Once", "Interval", "Python"]
        self._TimeFormat: str = "%Y-%m-%d %H:%M:%S"

    def keep(self):
        while True:
            for TaskUUID in list(self.Tasks.keys()):
                TaskStructure = self.Tasks[TaskUUID]
                self._TryToRunTask(TaskStructure)
                if TaskStructure.TaskStatus == "Stopped" and TaskStructure.TaskDestroyImmediatelyUponCompletion:
                    self.RemoveTask(TaskUUID)
            time.sleep(self.SleepTime)

    def _VerifyTask(self, TaskStructure: LW3Task):
        TaskStructureDir = TaskStructure.__dict__()
        for i in self._TaskKeys:
            if i not in TaskStructureDir:
                return False
        if TaskStructure.TaskType not in self._TaskTypes:
            return False
        return True

    def _TryToRunTask(self, TaskStructure: LW3Task):
        if not self._VerifyTask(TaskStructure): return False
        if not TaskStructure.TaskExistsCalculation: return False
        if not self._IsAllowRunStatus(TaskStructure.TaskStatus): return False
        
        CurrentTime = time.time()
        
        if TaskStructure.TaskType == "Once":
            if type(TaskStructure.TaskTimeCriticalParameters) in (int, float) and abs(
                    TaskStructure.TaskTimeCriticalParameters - CurrentTime) < TaskStructure.TaskAllowableErrorCount:
                TaskStructure.TaskStatus = "Stopped"
                if TaskStructure.TaskCallBack: self._TryToEXECTask(TaskStructure)
        
        elif TaskStructure.TaskType == "Interval":
            if type(TaskStructure.TaskTimeCriticalParameters) in (int, float) and TaskStructure.TaskTimeCriticalParameters > 0:
                TimeSinceLastEXEC = CurrentTime - TaskStructure.TaskLastExecutionTime
                if TimeSinceLastEXEC >= TaskStructure.TaskTimeCriticalParameters:
                    TimeError = abs(TimeSinceLastEXEC - TaskStructure.TaskTimeCriticalParameters)
                    if TimeError <= TaskStructure.TaskAllowableErrorCount:
                        if TaskStructure.TaskCallBack: 
                            self._TryToEXECTask(TaskStructure)
                            TaskStructure.TaskLastExecutionTime = CurrentTime
        
        elif TaskStructure.TaskType == "PythonOnce":
            if TaskStructure.TaskCondition:
                if type(TaskStructure.TaskCondition) == str:
                    if eval(TaskStructure.TaskCondition, TaskStructure.TaskCallBackVarDict):
                        TaskStructure.TaskStatus = "Stopped"
                        if TaskStructure.TaskCallBack: self._TryToEXECTask(TaskStructure)
                elif callable(TaskStructure.TaskCondition):
                    if TaskStructure.TaskCondition(**TaskStructure.TaskCallBackDict):
                        if TaskStructure.TaskCallBack: self._TryToEXECTask(TaskStructure)
                        TaskStructure.TaskStatus = "Stopped"

        elif TaskStructure.TaskType == "Python":
            if TaskStructure.TaskCondition:
                if type(TaskStructure.TaskCondition) == str:
                    if eval(TaskStructure.TaskCondition, TaskStructure.TaskCallBackVarDict):
                        if TaskStructure.TaskCallBack: self._TryToEXECTask(TaskStructure)
                elif callable(TaskStructure.TaskCondition):
                    if TaskStructure.TaskCondition(**TaskStructure.TaskCallBackDict):
                        if TaskStructure.TaskCallBack: self._TryToEXECTask(TaskStructure)


    def _TryToEXECTask(self, TaskStructure: LW3Task):
        if type(TaskStructure.TaskCallBack) == str:
            exec(TaskStructure.TaskCallBack, TaskStructure.TaskCallBackVarDict)
        elif callable(TaskStructure.TaskCallBack):
            TaskStructure.TaskCallBack(**TaskStructure.TaskCallBackDict)

    def _IsAllowRunStatus(self, TaskStatus: str):
        if TaskStatus == "Running": return True
        return False

    def AddTask(self, TaskUUID: str | None = None,
                TaskName: str = "",
                TaskType: str = "",
                TaskStatus: str = "Running",
                TaskCondition: str | typing.Callable = "",
                TaskAllowableErrorCount: int = None,
                TaskDestroyImmediatelyUponCompletion: bool = False,
                TaskStartTime: float = None,
                TaskEndTime: float = None,
                TaskExistsCalculation: TimeInterval = None,
                TaskTimeCriticalParameters: float | str | None = "",
                TaskCallBackVarDict: dict = None,
                TaskCallBackDict: dict = None,
                TaskCallBack: typing.Callable = None
                ) -> str:
        if not TaskUUID: TaskUUID = str(uuid.uuid4()).replace("-", "").upper()
        else: TaskUUID = TaskUUID.replace("-", "").upper()
        if not TaskExistsCalculation: TaskExistsCalculation = TimeInterval("Year", TaskStartTime, TaskEndTime)
        if TaskCallBackVarDict is None: TaskCallBackVarDict = {}
        if TaskCallBackDict is None: TaskCallBackDict = {}
        
        # 对于Interval任务，设置初始执行时间为当前时间
        TaskLastExecutionTime = time.time() if TaskType == "Interval" else 0
        
        return self.AddTaskByTaskStructure(LW3Task(TaskUUID=TaskUUID,
                                                   TaskName=TaskName,
                                                   TaskType=TaskType,
                                                   TaskStatus=TaskStatus,
                                                   TaskCondition=TaskCondition,
                                                   TaskAllowableErrorCount=TaskAllowableErrorCount,
                                                   TaskDestroyImmediatelyUponCompletion=TaskDestroyImmediatelyUponCompletion,
                                                   TaskExistsCalculation=TaskExistsCalculation,
                                                   TaskTimeCriticalParameters=TaskTimeCriticalParameters,
                                                   TaskCallBackVarDict=TaskCallBackVarDict,
                                                   TaskCallBackDict=TaskCallBackDict,
                                                   TaskCallBack=TaskCallBack,
                                                   TaskLastExecutionTime=TaskLastExecutionTime))

    def AddTaskByTaskStructure(self, TaskStructure: LW3Task):
        if not self._VerifyTask(TaskStructure): return False
        if type(TaskStructure.TaskExistsCalculation) == dict: 
            TaskStructure.TaskExistsCalculation = TimeInterval(**TaskStructure.TaskExistsCalculation)
        self.Tasks[TaskStructure.TaskUUID] = TaskStructure
        return TaskStructure.TaskUUID

    def GetTask(self, TaskUUID: str) -> LW3Task | None:
        TaskUUID = TaskUUID.replace("-", "").upper()
        return self.Tasks.get(TaskUUID)

    def GetAllTasks(self) -> list:
        return list(self.Tasks.values())

    def StopTask(self, TaskUUID: str) -> bool:
        TaskUUID = TaskUUID.replace("-", "").upper()
        if TaskUUID in self.Tasks:
            self.Tasks[TaskUUID].TaskStatus = "Stopped"
            return True
        return False

    def PauseTask(self, TaskUUID: str) -> bool:
        TaskUUID = TaskUUID.replace("-", "").upper()
        if TaskUUID in self.Tasks:
            self.Tasks[TaskUUID].TaskStatus = "Paused"
            return True
        return False

    def RestartTask(self, TaskUUID: str) -> bool:
        TaskUUID = TaskUUID.replace("-", "").upper()
        if TaskUUID in self.Tasks:
            task = self.Tasks[TaskUUID]
            task.TaskStatus = "Running"
            # 重启Interval任务时重置上次执行时间
            if task.TaskType == "Interval":
                task.TaskLastExecutionTime = time.time()
            return True
        return False

    def RemoveTask(self, TaskUUID: str) -> bool:
        TaskUUID = TaskUUID.replace("-", "").upper()
        if TaskUUID in self.Tasks:
            del self.Tasks[TaskUUID]
            return True
        return False

    def ExportTasks(self) -> list:
        return [task.__dict__() for task in self.Tasks.values()]

    def ImportTasks(self, TasksData: list, AutoRestart: bool = False) -> bool:
        for task_data in TasksData:
            if "TaskExistsCalculation" in task_data and type(task_data["TaskExistsCalculation"]) == dict:
                task_data["TaskExistsCalculation"] = TimeInterval(**task_data["TaskExistsCalculation"])
            task = LW3Task(**task_data)
            if not AutoRestart and task.TaskStatus in ["Stopped", "Paused"]:
                task.TaskStatus = "Paused"
            self.AddTaskByTaskStructure(task)
        return True


if __name__ == "__main__":
    sch = LW3TScheduler(globals())
    TaskUUID = sch.AddTask(
        TaskName="TestInterval",
        TaskType="Interval",
        TaskTimeCriticalParameters=5,
        TaskAllowableErrorCount=1,
        TaskExistsCalculation=TimeInterval("Year", -1, -1),
        TaskCallBack=lambda: print(f"Interval Task Executed at {time.time()}"),
    )

    sch.AddTask(
        TaskName="TestOnce",
        TaskType="Once",
        TaskTimeCriticalParameters = time.time() + 10,
        TaskAllowableErrorCount=1,
        TaskExistsCalculation=TimeInterval("Year", -1, -1),
        TaskCallBack=lambda: print("One-time Task Executed"),
    )

    sch.AddTask(
        TaskName="Test无限",
        TaskType="Python",
        TaskCondition = lambda: True,
        TaskAllowableErrorCount=1,
        TaskExistsCalculation=TimeInterval("Year", -1, -1),
        TaskCallBack=lambda: print("One-time Task Executed 114514"),
    )
    
    sch.keep()