from .. import OHImports
logger = OHImports.oh.getLogger("EasyRule.OHTypes.Item")

from __convert import ToString, ToNumeric, ToTimestamp

class BaseItem:

    def __init__(self, ohitem = None):
        self.name   = None
        self.state  = None
        self.reprstr = ""
        self.ohitem = ohitem
        self.type = self.__class__.__name__

        if ohitem:
            self.name = str(ohitem.name)
            self.state = self.convertvalue(ohitem.state)

    def convertvalue(self, val):
        return ToString(val)

    def __repr__(self):
        return "{} (Type={}, State={}, {}ohitem=(...))".format( self.name, self.type, self.state, self.reprstr + ", " if self.reprstr != "" else "")

class ContactItem(BaseItem):
    def __init__(self, ohitem = None):
        BaseItem.__init__(self, ohitem)

        self.isOpen   = True if self.state == "OPEN"   else False
        self.isClosed = True if self.state == "CLOSED" else False
        self.reprstr = "isOpen={}, isClosed={}".format( str(self.isOpen), str(self.isClosed))

class SwitchItem(BaseItem):
    def __init__(self, ohitem = None):
        BaseItem.__init__(self, ohitem)

        self.isON  = True if self.state == "ON"  else False
        self.isOFF = True if self.state == "OFF" else False
        self.reprstr = "isON={}, isOFF={}".format( str(self.isON), str(self.isOFF))

class StringItem(BaseItem):
    def __init__(self, ohitem = None):
        BaseItem.__init__(self, ohitem)

class NumberItem(BaseItem):
    def __init__(self, ohitem = None):
        BaseItem.__init__(self, ohitem)

    def convertvalue(self, val):
        return ToNumeric(val)


class PercentItem(BaseItem):
    def __init__(self, ohitem = None):
        BaseItem.__init__(self, ohitem)

    def convertvalue(self, val):
        return ToNumeric(val)

class DimmerItem(BaseItem):
    def __init__(self, ohitem = None):
        BaseItem.__init__(self, ohitem)

    def convertvalue(self, val):
        return ToNumeric(val)

class DateTimeItem(BaseItem):
    def __init__(self, ohitem = None):
        BaseItem.__init__(self, ohitem)

    def convertvalue(self, val):
        return ToTimestamp(val)




def ConvertItem( ohitem):
    if ohitem is None:
        return None

    _type = str(type(ohitem))

    if _type == "<type 'org.openhab.core.library.items.NumberItem'>":
        return NumberItem(ohitem)
    elif _type == "<type 'org.openhab.core.library.items.StringItem'>":
        return StringItem(ohitem)
    elif _type == "<type 'org.openhab.core.library.items.PercentItem'>":
        return PercentItem(ohitem)
    elif _type == "<type 'org.openhab.core.library.items.ContactItem'>":
        return ContactItem(ohitem)
    elif _type == "<type 'org.openhab.core.library.items.DimmerItem'>":
        return DimmerItem(ohitem)
    elif _type == "<type 'org.openhab.core.library.items.SwitchItem'>":
        return SwitchItem(ohitem)
    elif _type == "<type 'org.openhab.core.library.items.DateTimeItem'>":
        return DateTimeItem(ohitem)

    logger.warning( "Unknown item type \"{}\"".format(_type))
    return BaseItem(ohitem)




