import OHEvent
import OHItem
import OHItemRegistry
import __convert

reload(OHEvent)
reload(OHItem)
reload(OHItemRegistry)
reload(__convert)

from OHEvent import Event as Event
from OHEvent import ConvertItem as ConvertItem

from OHItemRegistry import OHItemRegistry as ItemRegistry