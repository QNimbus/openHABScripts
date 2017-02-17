"""
Created on Sun Jul  3 18:52:58 2016

@author: Sebastian
"""
from oh_globals import *

import time

import ScriptHelper as sh
reload(sh)

helper = sh.ScriptHelper("TEST")


helper.logerror("test")

MultiPlex0 = sh.MultiPlex( helper, "Multiplex0_String_Switch", { "ON": "Multiplex0_String_OUT_Proxy1", "OFF": "Multiplex0_String_OUT_Proxy2", "BLA": "Multiplex0_String_OUT_Proxy3"}, "Multiplex0_String_OUT", {"ON" : 0, "OFF" : 1, "BLA" : 0})
MultiPlex1 = sh.MultiPlex( helper, "Multiplex1_String_Switch", [ "Proxy1", "Proxy2", "Proxy3"], "Multiplex1_String_OUT", [0,1,0])


def getRules():
    mylist = helper.GetRules()

    print( "len: {}".format( len(mylist)))

    for k in mylist:
        print(k)
    
    return RuleSet( mylist)




TEST_RUN = 0
ERRORS = 0
PASSED = 0
logfile = []

def GetItemName( name):
    return "Multiplex{}_{}".format(TEST_RUN, name)

def log( string):
    global logfile
    logfile.append(string)


def AssertEqual(name, a,b):
    global ERRORS
    global PASSED
    if a == b:
        PASSED += 1
        log( "PASSED {:30s}: {} is {}".format(name, a,b))
    else:
        ERRORS += 1
        log( "FAILED {:30s}: {} is not {}".format(name, a,b))
    
def AssertItem( name, name1, state2):
    state1 = str(ItemRegistry.getItem( GetItemName(name1)).state)
    AssertEqual( name, state1, state2)

def AssertItems( name, name1, name2):
    state1 = str(ItemRegistry.getItem( GetItemName(name1)).state)
    state2 = str(ItemRegistry.getItem( GetItemName(name2)).state)
    AssertEqual( name, state1, state2)

def AssertOutput( name, item):
    AssertItems(name, "String_OUT", item)

def InitItems():
    print("-------------")
    log("")
    BusEvent.postUpdate( GetItemName("String_Switch"), "-")
    BusEvent.postUpdate( GetItemName("String_OUT_Proxy1"), "-")
    BusEvent.postUpdate( GetItemName("String_OUT_Proxy2"), "-")
    BusEvent.postUpdate( GetItemName("String_OUT_Proxy3"), "-")
    BusEvent.postUpdate( GetItemName("String_OUT"),    "-")
    time.sleep( 0.1)

def MultiPlexTest1():
    InitItems()
    
    BusEvent.postUpdate( GetItemName("String_Switch"), "ON" if TEST_RUN == 0 else "Proxy1")
    time.sleep( 0.1)

    BusEvent.sendCommand( GetItemName("String_OUT_Proxy1"), "TEST")    
    time.sleep( 0.1)

    AssertOutput("MultiPlexTest1", "String_OUT_Proxy1")

def MultiPlexTest2():
    InitItems()
    
    BusEvent.postUpdate( GetItemName("String_OUT_Proxy2"), "1234")

    BusEvent.postUpdate( GetItemName("String_Switch"), "OFF" if TEST_RUN == 0 else "Proxy2")
    time.sleep( 0.1)

    AssertOutput("MultiPlexTest2", "String_OUT_Proxy2")


def MultiPlexTest3():
    InitItems()
    BusEvent.postUpdate( GetItemName("String_Switch"), "ON" if TEST_RUN == 0 else "Proxy1")
    time.sleep( 0.1)
    
    BusEvent.sendCommand( GetItemName("String_OUT_Proxy1"), "TEST")

    AssertOutput("MultiPlexTest2", "String_OUT_Proxy1")

    
def MultiPlexTest4():
    InitItems()
    BusEvent.postUpdate( GetItemName("String_Switch"), "ON" if TEST_RUN == 0 else "Proxy1")
    BusEvent.postUpdate( GetItemName("String_OUT"), "ON")
    time.sleep( 0.2)
    AssertOutput("MultiPlexTest4", "String_OUT_Proxy1")

    BusEvent.postUpdate( GetItemName("String_Switch"), "OFF" if TEST_RUN == 0 else "Proxy2")
    time.sleep( 0.2)
    BusEvent.postUpdate( GetItemName("String_OUT"), "123")
    time.sleep( 0.2)
    AssertOutput("MultiPlexTest4", "String_OUT_Proxy2")


def MultiPlexTest5():
    InitItems()
    BusEvent.postUpdate( GetItemName("String_OUT_Proxy1"), "234")
    BusEvent.postUpdate( GetItemName("String_OUT_Proxy2"), "456")
    BusEvent.postUpdate( GetItemName("String_Switch"), "ON" if TEST_RUN == 0 else "Proxy1")
    time.sleep( 0.2)
    AssertOutput("MultiPlexTest5", "String_OUT_Proxy1")

    BusEvent.postUpdate( GetItemName("String_Switch"), "OFF" if TEST_RUN == 0 else "Proxy2")
    time.sleep( 0.2)
    AssertOutput("MultiPlexTest5", "String_OUT_Proxy2")
    
def MultiPlexTest6():
    InitItems()
    BusEvent.postUpdate( GetItemName("String_OUT_Proxy1"), "234")
    BusEvent.postUpdate( GetItemName("String_OUT_Proxy2"), "456")
    BusEvent.postUpdate( GetItemName("String_Switch"), "ON" if TEST_RUN == 0 else "Proxy1")
    time.sleep( 0.2)
    AssertOutput("MultiPlexTest6", "String_OUT_Proxy1")
    AssertItem( "MultiPlexTest6", "String_Switch", "ON" if TEST_RUN == 0 else "Proxy1")

    BusEvent.sendCommand( GetItemName("String_OUT_Proxy2"), "asdf")
    time.sleep( 0.2)
    AssertOutput("MultiPlexTest6", "String_OUT_Proxy2")
    AssertItem( "MultiPlexTest6", "String_Switch", "OFF" if TEST_RUN == 0 else "Proxy2")
    
    
    
def TestCases( bla):
    global TEST_RUN

    time.sleep( 1)

    log("")
    log("")
    log("")
    log("-----------------------------------------------------------------")
    log("Starting Tests")
    log("-----------------------------------------------------------------")
    
    for i in range(2):
        TEST_RUN = i
        MultiPlexTest1()
        MultiPlexTest2()
        MultiPlexTest3()
        MultiPlexTest4()
        MultiPlexTest5()
        MultiPlexTest6()
    
    #ItemRegistry.getItem( "Anwesend_Wohnung")
    log("")
    log("-----------------------------------------------------------------")
    log( "Passed: {}".format(PASSED))
    log( "Errors: {}".format(ERRORS))
    log("-----------------------------------------------------------------")
    
    for k in logfile:
        print(k)
    

from thread import start_new_thread
start_new_thread( TestCases, (0,))
