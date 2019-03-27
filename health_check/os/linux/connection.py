import paramiko
from health_check.logging import current_logger as logger
from health_check.decorator import connection_cache

DEFAULT_PORT = 22
LINE_END = "\n"


@connection_cache
def connect(host, port, username, password, **kwargs):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port, username, password, look_for_keys=False)
    logger.debug("[%s:%s] connect: ok", host, port)
    return client


def execute(host, port, username, password, command, **kwargs):
    client = connect(host, port, username, password)
    stdin, stdout, stderr = client.exec_command(command)
    logger.debug("[%s:%s] execute: ok", host, port)

    exit_status = stdout.channel.recv_exit_status()
    logger.debug("exit status => %s", exit_status)

    stdout_payload, stderr_payload = stdout.readlines(), stderr.readlines()
    logger.debug("stdout payload =>\n%s<=end", "".join(stdout_payload))
    logger.debug("stderr payload =>\n%s<=end", "".join(stderr_payload))

    return exit_status, stdout_payload, stderr_payload
