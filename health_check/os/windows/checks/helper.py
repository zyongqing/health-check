import winrm

if __package__ == "":
    import logging

    logging.basicConfig(format="%(levelname)s\t%(asctime)s\t%(message)s")
    logger = logging.getLogger(__name__)
else:
    from health_check.utils.logging import current_logger as logger


def execute(host, port, username, password, command, transport="basic"):
    client = winrm.Session(
        "%s:%s" % (host, port),
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
        logger.debug("stdout payload => %s", stdout_payload)

        stderr_payload = result.std_err.decode("GB18030")
        logger.debug("stderr payload => %s", stderr_payload)

        return exit_status, stdout_payload, stderr_payload
    finally:
        logger.debug("[%s:%s] close: ok", host, port)
