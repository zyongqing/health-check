import winrm
from health_check.logging import current_logger as logger

DEFAULT_PORT = 5985
LINE_END = "\r\n"


def execute(host, port, username, password, command, transport="basic"):
    client = winrm.Session(
        f"{host}:{port}",
        auth=(username, password),
        transport=transport,
        server_cert_validation="ignore",
    )

    try:
        result = client.run_ps(command)
        logger.debug("[%s:%s] execute: ok", host, port)

        exit_status = result.status_code
        logger.debug("exit status => %s", exit_status)

        stdout_payload = result.std_out.decode("GB18030")
        logger.debug("stdout payload =>\n%s<=end", stdout_payload)

        stderr_payload = result.std_err.decode("GB18030")
        logger.debug("stderr payload =>\n%s<=end", stderr_payload)

        return exit_status, stdout_payload.split(), stderr_payload.split()
    finally:
        logger.debug("[%s:%s] close: ok", host, port)
