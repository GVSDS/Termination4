import paramiko
from paramiko import ServerInterface
from paramiko.common import AUTH_SUCCESSFUL, AUTH_FAILED, OPEN_SUCCEEDED, OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
import threading
from utils import *
from shell import HoneypotShell

class FakeSSHServer(ServerInterface):
    def __init__(self, config, client_ip):
        self.username = None
        self.password = None
        self.command = None
        self.config = config
        self.channel_ready = threading.Event()
        self.client_ip = client_ip

    def check_auth_password(self, username, password):
        self.username = username
        self.password = password

        for user in self.config['users']:
            if (username == user['username'] and
                    password == user['password']):
                print("login success", self.client_ip, username, password)
                return AUTH_SUCCESSFUL

        print("login failed", self.client_ip, username, password)
        return AUTH_FAILED

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return OPEN_SUCCEEDED
        return OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_shell_request(self, channel):
        self.channel_ready.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixel_width, pixel_height, modes):
        return True

    def check_channel_exec_request(self, channel, command):
        self.channel_ready.set()
        self.command = command.decode('utf-8')
        print("RUNCOMMAND: ", self.client_ip, self.command)
        return True

    def get_allowed_auths(self, username):
        return "password"

def handle_connection(client_sock, client_addr, config, shell_config, rsa_key):
    client_ip = client_addr[0]
    print("CON:", client_ip)

    transport = None
    channel = None

    try:
        transport = paramiko.Transport(client_sock)
        transport.local_version = config['settings']['banner']
        transport.add_server_key(rsa_key)
        server = FakeSSHServer(config, client_ip)

        try:
            transport.start_server(server=server)
            channel = transport.accept(60)
            transport.banner_timeout = 60
            transport.handshake_timeout = 30

        except paramiko.SSHException as e:
            print(client_ip, "Invalid SSH banner (possible telnet/HTTP/scan tool)", "-")
        except (ConnectionResetError, ConnectionError):
            print(client_ip, "Connection reset by peer", "-")
        except EOFError:
            print(client_ip, "Connection closed by client (possible telnet/HTTP/scan tool)", "-")
        except Exception as e:
            print("x", traceback_info())
            return

        if channel is None:
            print(client_ip)
            print(client_ip, "Timeout or Connection closed by client")
            return

        shell = HoneypotShell(channel, client_ip, config, shell_config, server)
        server.channel_ready.wait()
        if server.command is None:
            shell.run()
        else:
            shell.exec_command(server.command)

    except Exception as e:
        print("x", traceback_info())
    else:
        print(client_ip, "Client disconnected", "!")
    finally:
        if transport:
            transport.close()
