import winrm
from health_check.logging import current_logger as logger
from health_check.decorator import connection_cache

DEFAULT_PORT = 5985
LINE_END = "\r\n"


@connection_cache
def connect(host, port, username, password, **kwargs):
    client = winrm.Session(
        f"{host}:{port}",
        auth=(username, password),
        transport=kwargs.get("transport", "basic"),
        server_cert_validation="ignore",
    )
    logger.debug("[%s:%s] connect: ok", host, port)
    return client


def execute(host, port, username, password, command, **kwargs):
    client = connect(host, port, username, password, **kwargs)

    result = client.run_ps(command)
    logger.debug("[%s:%s] execute: ok", host, port)

    exit_status = result.status_code
    logger.debug("exit status => %s", exit_status)

    stdout_payload = result.std_out.decode("GB18030")
    logger.debug("stdout payload =>\n%s<=end", stdout_payload)

    stderr_payload = result.std_err.decode("GB18030")
    logger.debug("stderr payload =>\n%s<=end", stderr_payload)

    return exit_status, stdout_payload.split(), stderr_payload.split()
