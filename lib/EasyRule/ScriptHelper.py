from OHImports import Rule, oh, ItemRegistry, RuleSet, ChangedEventTrigger, StartupTrigger, OnOffType

from BaseRule import BaseRule as BaseRule


class ScriptHelper(BaseRule):
    InitializationItem = "Initialize"
    CheckTriggerItemsOnlyOnce = True

    def logerror(self, *args, **kwargs):
        self.logger.error(*args, **kwargs)

    def logwarn(self, *args, **kwargs):
        self.logger.warn(*args, **kwargs)

    def loginfo(self, *args, **kwargs):
        self.logger.info(*args, **kwargs)

    def logdebug(self, *args, **kwargs):
        self.logger.debug(*args, **kwargs)

    def __init__(self, logger_name, *args, **kwargs):

        # init rule-class, no multi inheritance!
        #        super(self.__class__, self).__init__()
        BaseRule.__init__(self, AddToHelper=False, *args, **kwargs)

        self.logname = logger_name
        self.logger = oh.getLogger(logger_name)

        # init vars
        self.__rules = []
        self.__rules.append(self)

        # Vars for RuleCheck
        self.__intend_str = 80
        self.__TriggerCheckDone = False

        # optional args
        if "INIT_ITEM" in kwargs:
            ScriptHelper.InitializationItem = kwargs["INIT_ITEM"]

    # Called by EasyRule
    def AddRule(self, my_rule):
        self.__rules.append(my_rule)

    # check if rule triggers are valid items
    def __CheckTriggers(self):
        if not self.__ItemAvailable():
            return None

        # Do TriggerCheck only once!
        if self.__TriggerCheckDone and ScriptHelper.CheckTriggerItemsOnlyOnce:
            return None
        self.__TriggerCheckDone = True

        for rule in self.__rules:
            #if we run this the scripthelper trigger is working
            #no need to check it
            if rule is self:
                continue

            triggers = rule.getEventTrigger()

            # check if name available, else classname
            name = rule.__dict__.get("name", rule.__class__.__name__)

            self.loginfo("+{}+".format("-" * self.__intend_str))
            self.loginfo("| {:{width}s}|".format("Checking {}:".format(name), width=self.__intend_str - 1))

            ok = True

            for trigger in triggers:
                # get name
                trigger_name = str(trigger.getClass())
                trigger_name = trigger_name[trigger_name.rfind(".") + 1:-2]

                # these triggers do not have an item
                if (trigger_name == "StartupTrigger" or
                            trigger_name == "ShutdownTrigger" or
                            trigger_name == "TimerTrigger"):
                    continue

                # check if item exists
                item_name = str(trigger.getItem())
                if len(ItemRegistry.getItems(item_name)) != 1:
                    ok = False
                    self.logerror(
                        "| {:{width}s}|".format(" - Could not find item '{}' for {}".format(item_name, trigger_name),
                                                width=self.__intend_str - 1))
                else:
                    self.loginfo("| {:{width}s}|".format(" - Found item '{}' for {}".format(item_name, trigger_name),
                                                         width=self.__intend_str - 1))

            if ok:
                self.loginfo("| {:{width}s}|".format("Rule '{}' is OK!".format(name), width=self.__intend_str - 1))
            else:
                self.logerror("| {:{width}s}|".format("Rule '{}' is not OK!".format(name), width=self.__intend_str - 1))

        # checking done
        self.loginfo("+{}+".format("-" * self.__intend_str))
        return None

    def GetRules(self):

        # print Rule names
        self.loginfo("")
        self.loginfo("+{}+".format("-" * self.__intend_str))
        self.loginfo("| {:{width}s}|".format("Adding Rules:", width=self.__intend_str - 1))
        for rule in self.__rules:
            #link specific logger to rule
            rule.logger = oh.getLogger("{:s}.{:s}".format(self.logname, rule.name))

            #print rulename
            self.loginfo("|  - {:{width}s}|".format(rule.name, width=self.__intend_str - 4))
        self.loginfo("+{}+".format("-" * self.__intend_str))
        self.loginfo("")

        # Check Triggers
        try:
            self.__CheckTriggers()
        except Exception as e:
            self.logerror("{}\n{}".format(e, traceback.format_exc()))
            raise e

        return RuleSet(self.__rules)

    def __ItemAvailable(self):
        # Erst wenn ein item existiert soll initialisiert werden
        if not len(ItemRegistry.getItems(ScriptHelper.InitializationItem)):
            return False
        if str(ItemRegistry.getItem(ScriptHelper.InitializationItem).state) == "Uninitialized":
            return False
        return True

    def getEventTrigger(self):
        return [
            ChangedEventTrigger(ScriptHelper.InitializationItem, None, OnOffType.ON),
            StartupTrigger()
        ]

    def Initialize(self):
        pass

    def execute(self, event):
        if not self.__ItemAvailable():
            return None

        # Check Triggers
        try:
            self.__CheckTriggers()
        except Exception as e:
            self.logerror("{}\n{}".format(e, traceback.format_exc()))
            raise e

        # initialize Classes
        for k in self.__rules:
            try:
                k.Initialize()
            except Exception as e:
                self.logger.error("{:20s} | Error: {}".format("ScriptHelper", e))
