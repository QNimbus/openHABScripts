"""
Created on Sun Jul  3 18:52:58 2016

@author: Sebastian
"""
from oh_globals import *

import time

logger = oh.getLogger("ScriptHelper")


class ScriptHelper(Rule):
    
    def logerror( self, *args, **kwargs):
        self.logger.error(*args, **kwargs)
    def logwarn( self, *args, **kwargs):
        self.logger.warn(*args, **kwargs)
    def loginfo( self, *args, **kwargs):
        self.logger.info(*args, **kwargs)
    def logdebug( self, *args, **kwargs):
        self.logger.debug(*args, **kwargs)

    def __init__(self, logger_name, **kwargs):
        #init rule-class, no multi inheritance!
        #        super(self.__class__, self).__init__()
        Rule.__init__(self)
        
        self.logger = oh.getLogger( logger_name)        
        
        #init vars
        self.__rules  = []
        self.__rules.append(self)
        self.__init_item = "Initialize"
        
        #Vars for RuleCheck
        self.__intend_str = 80
        self.__TriggerCheckDone = False
        
        #optional args
        if "INIT_ITEM" in kwargs:
            self.__init_item = kwargs["INIT_ITEM"]
        
    #Called by EasyRule
    def _AddRule(self, my_rule):
        self.__rules.append( my_rule)

    #check if rule triggers are valid items
    def __CheckTriggers(self):
        
        #check if initialize item is available.
        # if not -> wait!
        if self.__ItemsAvailable() != True:
            return None

        #Do TriggerCheck only once!
        if self.__TriggerCheckDone:
            return None
        self.__TriggerCheckDone = True

        
        for rule in self.__rules:
            triggers = rule.getEventTrigger()
            self.loginfo("+{}+".format("-" * self.__intend_str))
            self.loginfo("| {:{width}s}|".format("Checking {}:".format(rule.__class__.__name__), width = self.__intend_str -1))
            
            ok = True

            for trigger in triggers:
                #get name
                trigger_name = str( trigger.getClass())
                trigger_name = trigger_name[trigger_name.rfind(".") + 1:-2]
                
                #these triggers do not have an item
                if (trigger_name == "StartupTrigger"    or
                    trigger_name == "ShutdownTrigger"   or
                    trigger_name == "TimerTrigger"):
                    continue
                
                #check if item exists
                item_name = str(trigger.getItem())
                if len(ItemRegistry.getItems( item_name)) != 1:
                    ok = False
                    self.logerror("| {:{width}s}|".format(" - Could not find item '{}' for {}".format(item_name, trigger_name), width = self.__intend_str -1))
                else:
                    self.loginfo("| {:{width}s}|".format(" - Found item '{}' for {}".format(item_name, trigger_name), width = self.__intend_str -1))
                    
                
            if ok:
                self.loginfo("| {:{width}s}|".format("Rule '{}' is OK!".format( rule.__class__.__name__), width = self.__intend_str -1))
            else:
                self.logerror("| {:{width}s}|".format("Rule '{}' is not OK!".format( rule.__class__.__name__), width = self.__intend_str -1))

        #checking done
        self.loginfo("+{}+".format("-" * self.__intend_str))
        return None
                
 

    def GetRules(self):

        #print Rule names
        self.loginfo("")
        self.loginfo("+{}+".format("-" * self.__intend_str))
        self.loginfo("| {:{width}s}|".format("Adding Rules:", width = self.__intend_str -1))
        for rule in self.__rules:
            self.loginfo("|  - {:{width}s}|".format(rule.__class__.__name__, width = self.__intend_str -4))
        self.loginfo("+{}+".format("-" * self.__intend_str))
        self.loginfo("")
        
        #check triggers
        self.__CheckTriggers()

        return self.__rules


    #so Jython doesn't generate an uncatchable exception
    def Initialize(self):
        self.__CheckTriggers()      

    def getEventTrigger(self):
        return [
            ChangedEventTrigger( self.__init_item, None, OnOffType.ON),
            ChangedEventTrigger( "aadf", None, OnOffType.ON),
            StartupTrigger()
        ]

    def __ItemsAvailable(self):
        if not len( ItemRegistry.getItems( self.__init_item)):
            return False
        
        if str(ItemRegistry.getItem( self.__init_item).state) == "Uninitialized":
            return False
        
        return True
        
    def execute(self, event):
        #Erst wenn ein item existiert soll initialisiert werden
        if self.__ItemsAvailable() != True:
            return None
        
        #initialize Classes        
        for k in self.__rules:
            try:
                k.Initialize()
            except Exception as e:
                logger.error( "{:20s} | Error: {}".format( "ScriptHelper", e))        
        

class EasyRule(Rule):
    def __init__(self, ScriptHelperClass, **kwargs):
        #init rule-class, no multi inheritance!
        Rule.__init__(self)
        
        #Add Rule
        ScriptHelperClass._AddRule(self)
        
    def Initialize(self):
        pass




















class __MultiPlex_RuleHelper(EasyRule):
    def __init__(self, ScriptHelperClass, RuleType, ItemName, ChangedFunction, CallData = {}):
        EasyRule.__init__(self, ScriptHelperClass)
        
        self.__type     = RuleType
        self.__name     = ItemName
        self.__calldata = CallData
        self.__function = ChangedFunction

    def getEventTrigger(self):
        if self.__type == "COMMAND":
            return [CommandEventTrigger( self.__name, None)]
        else:
            return [UpdatedEventTrigger( self.__name)]

    def execute(self, event):
        self.__function(event.item, self.__calldata) 



class MultiPlex(EasyRule):

    def ReceiveOutputUpdate( self, item, data):
        self.__logger.debug("ReceiveOutputUpdate: {}".format(item))
        
        if self.__input_item is None:
            self.__logger.debug("No input item!'".format())
            return None

        BusEvent.postUpdate( self.__input_item, str(item.state))
            

    def ReceiveCommand( self, item, data):
        self.__logger.debug("ReceiveCommand: {}".format(item))
        name  = str(item.name)
        state = str(item.state)
        
        self.__item_cache[name] = state
        
        priority = data["PRIORITY"]
        switch   = data["SWITCH_VALUE"]
        
        if name == self.__input_item:
            BusEvent.sendCommand( self.__output_item, state)

            #Refresh Switch item with higher priority            
            if priority > 0:
                BusEvent.postUpdate( self.__switch_item, switch)

        #Automatically switch to higher Priority item
        if priority > self.__input_prio:
            BusEvent.postUpdate( self.__switch_item, switch)


    def Initialize(self):
        self.__item_cache = {}
        self.__input_item = None
        
    def __init__(self, ScriptHelperClass, SwitchItem, SwitchedItems, OutputItem, Priorities = None, **kwargs):
        EasyRule.__init__(self, ScriptHelperClass)
        self.__logger = ScriptHelperClass.logger

        self.__switch_item = SwitchItem
        self.__output_item = OutputItem
        
        self.__item_cache = {}
        self.__input_item = None
        self.__input_prio = None
        
        self.__multiplex  = {}
        self.__priorities = {}
        if isinstance(SwitchedItems, dict):
            self.__multiplex = SwitchedItems
            for k in SwitchedItems:
                if Priorities is not None:
                    self.__priorities[k] = Priorities[k]
                else:
                    self.__priorities[k] = 0      
        elif isinstance(SwitchedItems, list):
            for i, k in enumerate(SwitchedItems):
                self.__multiplex[k] = self.__output_item + "_" + k
                if Priorities is not None:
                    self.__priorities[k] = Priorities[i]
                else:
                    self.__priorities[k] = 0
        else:
            self.__logger.error("Invalid Input Type for CMultiPlex: {}! Please use Dict or List".format(SwitchedItems))
            return None

        
        #Setup Rules
        self.__rules  = {}
        #Update Trigger
        self.__rules["ITEM_OUT"]    = __MultiPlex_RuleHelper(ScriptHelperClass, "UPDATE",  self.__output_item, self.ReceiveOutputUpdate)
        #Command Triggers
        for switch, item in self.__multiplex.items():
            self.__rules[item]  = __MultiPlex_RuleHelper(ScriptHelperClass, "COMMAND", item, self.ReceiveCommand, { "SWITCH_VALUE" : switch, "PRIORITY" : self.__priorities[switch]})
        
            

    def getEventTrigger(self):
        return [ChangedEventTrigger( self.__switch_item)]

    def execute(self, event):
        
        state = str(event.item.state)

        #unbekannter status
        if state not in self.__multiplex:
            self.__input_item  = None
            self.__logger.error("No output item defined for value '{}' of switch '{}'".format(state, self.__switch_item))
            return None

        self.__input_item  = self.__multiplex[state]
        self.__input_prio  = self.__priorities[state]

        #Check cache, else Item Registry
        if self.__input_item in self.__item_cache:
            BusEvent.sendCommand( self.__output_item, self.__item_cache[self.__input_item])
        else:
            new_state = str(ItemRegistry.getItem(self.__input_item).state)
            BusEvent.sendCommand( self.__output_item, new_state)

                    
        
