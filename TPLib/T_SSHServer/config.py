import json
import os
import paramiko
import shutil
from getpass import getuser
from utils import *
from output import Output

CONFIG_DIR = "config"
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
SHELL_CONFIG_FILE = os.path.join(CONFIG_DIR, "shell.json")
RSA_KEY_PATH = os.path.join(CONFIG_DIR, "rsa_key.pem")
VHOME_DIR = os.path.join(".", "vdisk", "home")  # 虚拟home目录
VROOT_DIR = os.path.join(".", "vdisk", "root")  # 虚拟root目录
REAL_HOME_DIR = os.path.join(".", "home")  # 真实home目录模板
REAL_DEFAULT_HOME = os.path.join(REAL_HOME_DIR, "default")  # 默认home模板


def load_config():
    os.makedirs(CONFIG_DIR, exist_ok=True)

    # 默认配置
    default_config = {
        "settings": {
            "port": 22,
            "banner": "SSH-2.0-OpenSSH_9.6p1 Ubuntu-3ubuntu13.1",
            "hostname": "ubuntu"
        },
        "users": [
            {
                "username": "root",
                "password": "password",
                "home_dir": "root"
            },
            {
                "username": "ubuntu",
                "password": "password",
                "home_dir": "ubuntu"
            }
        ],
        "output": {
            "login_success": "{ip} - Successful login attempt | Username: {username} | Password: {password}",
            "login_failed": "{ip} - Failed login attempt | Username: {username} | Password: {password}",
            "new_connection": "{ip} - New SSH connection established",
            "no_channel_msg": "{ip} - SSH channel negotiation failed (timeout/protocol error)",
            "connection_closed_msg": "{ip} - Connection closed{reason}",
            "connection_error_msg": "{ip} - Connection error: {error}",
            "shutdown_msg": "Server - Shutting down honeypot service",
            "startup_msg": "Server - SSH Honeypot started on {host}:{port}",
            "rsa_key_error": "Server - Invalid RSA key detected: {reason}, generating new key",
            "rsa_key_loaded": "Server - Loaded existing RSA key from {path}",
            "rsa_key_created": "Server - Created new RSA key at {path}",
            "run_command": "{ip} - Executed command: {command}"
        }
    }

    default_shell_config = {
        "messages": {
            "motd": """Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-76-generic x86_64)

* Documentation:  https://help.ubuntu.com
* Management:     https://landscape.canonical.com
* Support:        https://ubuntu.com/advantage
{endl}""",
            "prompt": "{COLOR_USER}{username}@{hostname}:{COLOR_PATH}{path}{RESET}${space}",
            "root_prompt": "root@{hostname}:{path}#{space}"
        }
    }

    # 加载或创建主配置文件
    if not os.path.exists(CONFIG_FILE):
        send_log("+", f"Creating new config file: {CONFIG_FILE}")
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4)
        send_log("*", f"Server - Config file created: {CONFIG_FILE}")

    # 加载或创建shell配置文件
    if not os.path.exists(SHELL_CONFIG_FILE):
        send_log("+", f"Creating new shell config file: {SHELL_CONFIG_FILE}")
        with open(SHELL_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_shell_config, f, indent=4)
        send_log("*", f"Server - Shell config file created: {SHELL_CONFIG_FILE}")

    # 读取配置文件
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)

    with open(SHELL_CONFIG_FILE, 'r', encoding='utf-8') as f:
        shell_config = json.load(f)

    # 初始化虚拟磁盘
    try:
        # 删除旧的虚拟home目录
        if os.path.exists(VHOME_DIR):
            shutil.rmtree(VHOME_DIR)
            send_log("*", f"Removed old virtual home directory: {VHOME_DIR}")
        if os.path.exists(VROOT_DIR):
            shutil.rmtree(VROOT_DIR)
            send_log("*", f"Removed old virtual root directory: {VROOT_DIR}")

        # 确保真实home模板目录存在
        os.makedirs(REAL_HOME_DIR, exist_ok=True)
        os.makedirs(REAL_DEFAULT_HOME, exist_ok=True)

        # 为所有用户创建虚拟目录
        for user in config.get('users', []):
            username = user['username']
            is_root = username == 'root'

            # 确定虚拟目录路径
            vuser_home = VROOT_DIR if is_root else os.path.join(VHOME_DIR, username)
            os.makedirs(vuser_home, exist_ok=True)
            send_log("*", f"Created virtual home directory: {vuser_home}")

            # 确定要使用的模板目录
            home_dir = user.get('home_dir')
            template_dir = None

            if home_dir is not None:
                # 使用指定的home模板
                template_dir = os.path.join(REAL_HOME_DIR, home_dir)
            elif not is_root:
                # 非root用户默认使用default模板
                template_dir = REAL_DEFAULT_HOME

            # 如果模板目录存在，则复制内容
            if template_dir and os.path.exists(template_dir):
                for item in os.listdir(template_dir):
                    src = os.path.join(template_dir, item)
                    dst = os.path.join(vuser_home, item)
                    if os.path.isdir(src):
                        shutil.copytree(src, dst)
                    else:
                        shutil.copy2(src, dst)
                send_log("*", f"Copied home template files from {template_dir} to {vuser_home}")

    except Exception as e:
        send_log("x", f"Failed to initialize virtual home: {str(e)}")

    # 处理RSA密钥
    rsa_key = None
    if os.path.exists(RSA_KEY_PATH):
        try:
            rsa_key = paramiko.RSAKey(filename=RSA_KEY_PATH)
            Output(config).rsa_key_loaded(RSA_KEY_PATH)
        except Exception as e:
            Output(config).rsa_key_error(str(e))
            rsa_key = paramiko.RSAKey.generate(2048)
            rsa_key.write_private_key_file(RSA_KEY_PATH)
            Output(config).rsa_key_created(RSA_KEY_PATH)
    else:
        rsa_key = paramiko.RSAKey.generate(2048)
        rsa_key.write_private_key_file(RSA_KEY_PATH)
        Output(config).rsa_key_created(RSA_KEY_PATH)

    return config, shell_config, rsa_key