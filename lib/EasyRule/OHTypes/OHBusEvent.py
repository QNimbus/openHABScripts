from ..OHImports import oh, BusEvent
logger = oh.getLogger("EasyRule.OHTypes.OHItemRegistry")


#primitive to String-Cast
class OHBusEvent():

    def sendCommand(self, itemName, val):

        if not isinstance( itemName, str):
            itemName = itemName.name
        if not isinstance( val, str):
            val = str(val)

        return BusEvent.sendCommand(itemName, val)

    def postUpdate(self, itemName, val):
        if not isinstance( itemName, str):
            itemName = itemName.name
        if not isinstance( val, str):
            val = str(val)

        return BusEvent.postUpdate(itemName, val)
