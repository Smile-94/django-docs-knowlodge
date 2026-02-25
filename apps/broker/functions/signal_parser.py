import logging
import re

logger = logging.getLogger(__name__)


def parse_signal(message: str):
    """
    Parse trading signal message.

    Example:
        BUY EURUSD [@1.0860 - Optional]
        SL 1.0850
        TP 1.0890
    """

    try:
        if not message or not isinstance(message, str):
            return {"valid": False, "error": "Empty message"}

        logger.info(f"INFO:-------->> Parsing signal message: {message}")

        # Remove starting & ending double quotes
        if message.startswith('"') and message.endswith('"'):
            message = message[1:-1].strip()

        # Remove starting & ending single quotes
        if message.startswith("'") and message.endswith("'"):
            message = message[1:-1].strip()

        lines = [line.strip() for line in message.split("\n") if line.strip()]
        if len(lines) < 2:
            logger.warning(f"WARNING:-------->> Incomplete signal data: {message}")
            return {"valid": False, "error": "Incomplete signal data"}

        # -------------------------
        # Parse First Line
        # -------------------------
        first_line = lines[0]

        pattern = r"^(BUY|SELL)\s+([A-Z]+)(?:\s*(?:\[@?([\d.]+)[^\]]*\]|@([\d.]+)))?$"
        match = re.match(pattern, first_line)

        if not match:
            logger.warning(f"WARNING:-------->> Invalid first line format: {first_line}")
            return {"valid": False, "error": "Invalid first line format"}

        action = match.group(1)
        instrument = match.group(2)
        price = match.group(3) or match.group(4)

        price = float(price) if price else None

        # -------------------------
        # Extract SL & TP
        # -------------------------
        sl = None
        tp = None

        for line in lines[1:]:
            upper = line.upper()

            if upper.startswith("SL"):
                try:
                    sl = float(line.split()[1])
                except (IndexError, ValueError):
                    logger.warning(f"WARNING:-------->> Invalid SL format: {line}")
                    return {"valid": False, "error": "Invalid SL format"}

            elif upper.startswith("TP"):
                try:
                    tp = float(line.split()[1])
                except (IndexError, ValueError):
                    logger.warning(f"WARNING:-------->> Invalid TP format: {line}")
                    return {"valid": False, "error": "Invalid TP format"}

        if sl is None:
            logger.warning(f"WARNING:-------->> SL not found in signal message: {message}")
            return {"valid": False, "error": "SL missing"}

        if tp is None:
            logger.warning(f"WARNING:-------->> TP not found in signal message: {message}")
            return {"valid": False, "error": "TP missing"}

        # -------------------------
        # Logical Validation
        # -------------------------
        if action == "BUY" and sl >= tp:
            logger.warning(f"WARNING:-------->> BUY signal with SL >= TP: {sl} >= {tp}")
            return {
                "valid": False,
                "error": "For BUY, SL must be lower than TP",
            }

        if action == "SELL" and sl <= tp:
            logger.warning(f"WARNING:-------->> SELL signal with SL <= TP: {sl} <= {tp}")
            return {
                "valid": False,
                "error": "For SELL, SL must be higher than TP",
            }

        return {
            "valid": True,
            "data": {
                "action": action,
                "instrument": instrument,
                "price": price,
                "stop_loss": sl,
                "take_profit": tp,
            },
        }

    except Exception as e:
        logger.error(f"ERROR:-------->> Unexpected error in parser_signal: {str(e)}")
        return {
            "valid": False,
            "error": f"Unexpected error: {str(e)}",
        }
