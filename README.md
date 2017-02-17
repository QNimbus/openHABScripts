# openHABScripts
This is a library for the JSR223 scripting engine on openHAB.

The goal of this project is to make the scripting with jython easier and less prone to errors.

#Usage
- Add ```"-Dpython.path="configurations/scripts/lib""``` to the java args of openhab
- Copy the ```lib``` folder to ```configurations/scripts``` so all the files are in ```.../scripts/lib/```
- When creating a new script start with
```python
import ScriptHelper as SH
helper = SH.ScriptHelper( "ModuleName")
```
- When creating a new rule do the following:
```python
class MyJSR223RuleName(SH.EasyRule):
    def __init__(self):
        #add this line or the lib won't work
        SH.EasyRule.__init__(self, helper)
        
        #define your variables here
        self.__myvariable = 0
    def Initialize(self):
        #initialize all your variables and required states here
        self.__myvariable = 0

#create an instance of the rule
#Note: this is different! Creating an instance is enough!
MyJSR223RuleName()
```
- At the End of the file do the following
```python
def getRules():
    return RuleSet(helper.GetRules() + [
        MyLegacyrule()
    ])
```
Note that all the rules with instances are automatically added.



#Why should I use this library?
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
|  - Could not find item 'NonexistingItem1' for ChangedEventTrigger               |
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
