from utils import *

class Output:
    def __init__(self, config):
        self.config = config

    def login_success(self, ip, username, password):
        msg = self.config['output']['login_success'].format(ip=ip, username=username, password=password)
        send_log("!", msg, 'green')

    def login_failed(self, ip, username, password):
        msg = self.config['output']['login_failed'].format(ip=ip, username=username, password=password)
        send_log("-", msg)

    def new_connection(self, ip):
        msg = self.config['output']['new_connection'].format(ip=ip)
        send_log("+", msg)

    def shutdown_server(self):
        msg = self.config['output']['shutdown_msg']
        send_log("#", msg)

    def startup(self, host, port):
        msg = self.config['output']['startup_msg'].format(host=host, port=port)
        send_log("*", msg)

    def no_channel(self, ip):
        msg = self.config['output']['no_channel_msg'].format(ip=ip)
        send_log("!", msg)

    def connection_error(self, ip, error, log_type="-"):
        msg = self.config['output']['connection_error_msg'].format(ip=ip, error=error)
        send_log(log_type, msg)

    def rsa_key_error(self, reason, log_type="x"):
        msg = self.config['output']['rsa_key_error'].format(reason=reason)
        send_log(log_type, msg)

    def rsa_key_loaded(self, path):
        msg = self.config['output']['rsa_key_loaded'].format(path=path)
        send_log("*", msg)

    def rsa_key_created(self, path):
        msg = self.config['output']['rsa_key_created'].format(path=path)
        send_log("+", msg)

    def run_command(self, ip, command):
        msg = self.config['output']['run_command'].format(ip=ip, command=command)
        send_log("#", msg)
        return msg

    def connection_closed(self, ip, reason="", log_type="-"):
        msg = self.config['output']['connection_closed_msg'].format(
            ip=ip,
            reason=f": {reason}" if reason else ""
        )
        send_log(log_type, msg)

