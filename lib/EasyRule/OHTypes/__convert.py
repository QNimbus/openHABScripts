from .. import OHImports
logger = OHImports.oh.getLogger("EasyRule.OHTypes.__convert")

def ToNumeric(javavar):
    if javavar is None:
        return None

    _str = str(javavar)
    try:
        return int(_str)
    except ValueError:
        try:
            return float(_str)
        except ValueError as e:
            logger.error("Error for '{}' : {}".format(javavar, e))
            raise e

def ToString(javavar):
    if javavar is None:
        return None
    return str(javavar)

def ToTimestamp(javavar):
    if javavar is None:
        return None
    return float( (OHImports.DateTimeType( str(javavar))).calendar.timeInMillis ) / 1000.0

