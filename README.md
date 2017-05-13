#openHABScripts & EasyRule
This is a library for the JSR223 scripting engine on openHAB which is aiming to make the scripting with jython easier and less prone to errors.
This is also the home of EasyRule.


#Setup
- Add ```"-Dpython.path="configurations/scripts/lib""``` to the java args of openhab
- Copy the ```lib``` folder to ```configurations/scripts``` so all the files are in ```.../scripts/lib/```
- Create a new (Switch) item "Initialize" (name can be configured).
```Switch Initialize "Initialize"```

#How does this help me?
- It automatically creates the ```getRules()``` function. No need to manually track the created rules.
- It makes initializing rule variables very easy!
Just Drag and Drop the new Rule into the folder and the Initialize functions are called.
It even works during startup.
- Possibility to set openHAB back to a defined state.
Just change the initialization item to ON and everything will be as it is supposed to be.
No more posting states to items or calling functions manually.
One click/post and everything is like after startup.
- Small Rules can be created really convenient: 
```python
@EasyRule.ItemChanged("Itemname")
def MyRule1():
    BusEvent.postUpdate("Itemname", "0")
```
- It prints all the added rules in the logger window.
This makes searching for errors really easy.
````
+--------------------------------------------------------------------------------+
| Adding Rules:                                                                  |
|  - Rule1                                                                       |
|  - Rule2                                                                       |
|  - Rule3                                                                       |
+--------------------------------------------------------------------------------+
````
- It checks whether you have defined valid rule triggers:
````
+--------------------------------------------------------------------------------+
| Checking Rule1:                                                                |
|  - Found item 'MyItem1' for ChangedEventTrigger                                |
|  - Could not find item 'NonexistingItem1' for ChangedEventTrigger              |
| Rule 'Rule1' is not OK!                                                        |
+--------------------------------------------------------------------------------+
| Checking Rule2:                                                                |
|  - Found item 'MyItem2' for ChangedEventTrigger                                |
| Rule 'Rule2' is OK!                                                            |
+--------------------------------------------------------------------------------+
| Checking Rule3:                                                                |
|  - Found item MyItem3 for UpdatedEventTrigger                                  |
| Rule 'Rule3' is OK!                                                            |
+--------------------------------------------------------------------------------+
````

#How do I use it

```python
import EasyRule

#it is also recommended to create a helper item but not necessary
helper = EasyRule.ScriptHelper( "myScriptName")
```

#Simple Rules
Simple Rules are just small function calls. Create a function you like and just add the corresponding decorator:
```python
#Easy ItemChanged - Rule declaration.
@EasyRule.ItemChanged("Itemname")
def MyRule1():
    BusEvent.postUpdate("Itemname", "0")

#no need to use oh-vars for the trigger anymore
#the integer gets automatically converted to the corresponding type
@EasyRule.ItemChanged("NumberItem", None, 1)
def MyRule1Changed():
    BusEvent.postUpdate("NumberItem", "0")

#Easy ItemUpdated- Rule declaration.
@EasyRule.ItemUpdated("Itemname")
def MyRule2():
    BusEvent.postUpdate("Itemname", "0")

#Easy TimerTrigger- Rule declaration.
@EasyRule.TimerTrigger("Chron")
def MyRule3():
    BusEvent.postUpdate("Itemname", "0")
```

#Simple Rules with event
It is also possible to access the event-item. To achieve this just add a parameter to your function. 
```python
#Accessing the event-item is also possible:
@EasyRule.ItemChanged("TestString")
def MyRule1(event):
    print(event)

#Easy ItemUpdated- Rule declaration.
@EasyRule.ItemUpdated("TestString")
def MyRule2(event):
    print(event)
```

The variables of the event get automatically converted to the jython equivalent (DecimalType -> int/float, DateTime to float, StringType -> str). The above two rules produce the following output:
````
Event [triggerType=CHANGE, item=TestString (Type=StringItem, State=ON, ohitem=(...)), oldState=OFF, newState=ON, command=None, ohEvent=(...)]
Event [triggerType=UPDATE, item=TestString (Type=StringItem, State=ON, ohitem=(...)), oldState=None, newState=ON, command=None, ohEvent=(...)]
````
Accessing the original item is still possible. Just use the ohitem or ohEvent vars.
