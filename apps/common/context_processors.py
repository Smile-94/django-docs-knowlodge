# apps/common/context_processors.py


def system_name(request):
    """
    Provide a default system name to all templates
    """
    return {"system_name": "Trade Broker"}
