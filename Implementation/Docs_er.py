import airbrake

logger = airbrake.getLogger(api_key="cb2a3a75073aac41efac1818747f2ac5", project_id= 171162)

try:
    1/0
except Exception:
    logger.exception("Bad math.")
print(logger)
