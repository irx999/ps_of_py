import importlib
import logging
import os
from logging.handlers import RotatingFileHandler


class Logger:
    """
    日志类，用于创建和管理日志记录器

    usage:

    from modules.logger import Logger
    logger_instance = Logger(__name__, log_name="wr.log", debug_mode=True, notification=True, notificationFunction=None)
    logger_instance.debug("这是一个debug 的log信息")
    logger_instance.info("这是一个info 的log信息")
    logger_instance.warning("这是一个warning 的log信息")
    logger_instance.error("这是一个error 的log信息")
    logger_instance.critical("这是一个critical 的log信息")
    logger_instance.set_level(logging.DEBUG)  # 修改日志级别为DEBUG
    logger_instance.toggle_debug_mode(True)  # 开启debug模式
    """

    def __init__(
        self,
        name,
        log_name="wr",
        debug_mode=True,
        default_level="ERROR",
        notification=False,
        notificationFunction=None,
    ):
        self.name = name
        self.log_name = log_name
        self.debug_mode = debug_mode
        self.default_level = default_level
        self.notification = notification
        self.notificationFunction = notificationFunction
        self.logger = self._create_logger()

    def formatter(self, is_console=False):
        str = f"%(asctime)-20s - %(levelname)-7s -> {self.log_name:^8} <- %(file_lineno_fixed)s - %(funcName)s - %(message)s"
        str = "%(asctime)-20s - %(levelname)-4s %(file_lineno_fixed)s - %(message)s"
        return ColoredFormatter(str) if is_console else custom_formatter(str)

    def debug_notification(self):
        print(
            f"{self.log_name:<10}---Debug mode is \033[91m{str(self.debug_mode):^5}\033[0m, console_log_will_be_change"
        )

    def _create_logger(self) -> logging.Logger:
        # 获取log文件路径
        log_dir = os.path.join(os.getcwd(), "logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 创建logger
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.DEBUG)  # 设置基础日志级别为DEBUG

        # 创建一个滚动文件处理器，每个日志文件最大大小为5M，保存5个旧日志文件
        rf_handler = RotatingFileHandler(
            os.path.join(log_dir, self.log_name + ".log"),
            maxBytes=5 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )

        rf_handler.setFormatter(self.formatter())
        logger.addHandler(rf_handler)

        self.console_handler = None
        if self.debug_mode:
            # 如果debug模式打开，则输出到控制台
            self.debug_notification()
            self.console_handler = logging.StreamHandler()
            self.console_handler.setFormatter(self.formatter(True))
            logger.addHandler(self.console_handler)

        if self.notification and not self.debug_mode:
            # 如果错误类型是error，则发送邮件通知管理员
            notificatio_handler = NotificationHandler(self.notificationFunction)
            notificatio_handler.setFormatter(self.formatter(True))
            logger.addHandler(notificatio_handler)

        return logger

    def set_level(self, level):
        """Set the logging level."""
        self.logger.setLevel(level)
        self.default_level = level

    def toggle_debug_mode(self, enable):
        """Toggle debug mode on or off."""
        self.debug_mode = enable
        if enable and self.console_handler is None:
            # 如果要开启调试模式且当前没有控制台处理器
            self.debug_notification()
            self.console_handler = logging.StreamHandler()
            self.console_handler.setFormatter(self.formatter())
            self.logger.addHandler(self.console_handler)
            self.logger.setLevel(logging.DEBUG)  # 设置日志级别为DEBUG
        elif not enable and self.console_handler is not None:
            # 如果要关闭调试模式且当前有控制台处理器
            self.debug_notification()
            self.logger.removeHandler(self.console_handler)
            self.console_handler = None
            self.logger.setLevel(self.default_level)  # 恢复默认日志级别

    def __getattr__(self, attr):
        """Delegate attribute access to the internal logger."""
        return getattr(self.logger, attr)


class NotificationHandler(logging.Handler):
    """信息通知"""

    def __init__(self, notificationFunction):
        if notificationFunction is None:
            raise ValueError("notificationFunction cannot be None")
        self.notificationFunction = notificationFunction

    def emit(self, record):
        if record.levelno >= logging.ERROR:
            error_message = self.format(record)
            self.notificationFunction(error_message)


class custom_formatter(logging.Formatter):
    """自定义日志格式"""

    def format(self, record):
        file_lineno = f"[{record.filename}:{record.lineno}]"
        record.file_lineno_fixed = f"{file_lineno:^20}"  # 中对齐，占20字符
        record.funcName = f"{record.funcName:^20}"  # 左对齐，占20字符

        return super().format(record)


class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[94m",  # 蓝色
        "INFO": "\033[92m",  # 绿色
        "WARNING": "\033[93m",  # 黄色
        "ERROR": "\033[91m",  # 红色
        "CRITICAL": "\033[95m",  # 紫色
        "RESET": "\033[0m",  # 重置颜色，用于在日志文本后重置颜色，避免影响后续文本
    }

    def format(self, record):
        file_lineno = f"[{record.filename}:{record.lineno}]"
        record.file_lineno_fixed = f"{file_lineno:^20}"  # 中对齐，占20字符
        record.funcName = f"{record.funcName:^20}"  # 左对齐，占20字符

        log_level = record.levelname
        # 根据日志级别获取相应的颜色代码，如果找不到则使用重置颜色
        color_start = self.COLORS.get(log_level, self.COLORS["RESET"])
        # 获取重置颜色代码
        color_end = self.COLORS["RESET"]
        # 将颜色代码应用到日志级别上，以便在输出中显示颜色
        record.levelname = f"{color_start}{record.levelname:^10}{color_end}"

        return super().format(record)


def dingrobot(
    msg: list | str = "当你看到这个说明你没有填写msg",
    msgtype="text",
    access_token="",
    safe_word=">-<",
) -> bool:
    """
    钉钉机器人推送
    :param access_token: 钉钉机器人的access_token
    :param msg: 推送消息，可以是字符串或列表，列表第一个元素为标题，第二个元素为内容
    :param msgtype: 推送消息类型，可选值为text或markdown
    :return: bool
    """

    requests = importlib.import_module("requests")
    json = importlib.import_module("json")

    match msgtype:
        case "markdown":
            data = {
                "markdown": {"text": f"{safe_word}---{msg[1]}", "title": msg[0]},
                "msgtype": "markdown",
            }
        case _:
            data = {"text": {"content": f"{safe_word}---{msg}"}, "msgtype": "text"}
    headers = {"Content-Type": "application/json"}
    rebot_url = f"https://oapi.dingtalk.com/robot/send?access_token={access_token}"
    robot = requests.post(
        url=rebot_url, data=json.dumps(data), headers=headers, timeout=5
    )
    if robot.status_code != 200:
        return False
    return True


if __name__ == "__main__":
    logger_instance = Logger(__name__)
    logger_instance.debug(f"{__name__}123")  # 这行不会打印，因为默认不是DEBUG模式
    logger_instance.set_level("DEBUG")  # 修改日志级别为DEBUG
    logger_instance.debug(f"{__name__}123")  # 现在会打印
    logger_instance.toggle_debug_mode(False)  # 关闭debug模式
    logger_instance.debug(f"{__name__}123")  # 不会打印
    logger_instance.toggle_debug_mode(True)  # 开启debug模式
    logger_instance.set_level("INFO")  # 修改日志级别为DEBUG
    logger_instance.debug(f"{__name__}123")  # 再次打印
