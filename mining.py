import time
import sys
import math
import common
#    
from System.Collections.Generic import List
from System import Byte, Int32
#
MaxWeight = 520
#
import clr
clr.AddReference('System.Web.Extensions')
from System.Web.Script.Serialization import JavaScriptSerializer
#
Mining_Data_File = "Data/mining_data4.txt"
mining_data_file = open(Mining_Data_File, "r")
mining_data_json = mining_data_file.read()
locations = JavaScriptSerializer().Deserialize(mining_data_json, list)
mining_data_file.close()

PortableForge = 0
PortableForges = common.findRecursiveWithColor(Player.Backpack.Serial, [(0x0E32,  0x0489) ] )
if len(PortableForges) > 0:
    #Misc.SendMessage("Forges found")
    PortableForge = PortableForges[0]
#
IngotKey = 0
IngotKeys = common.findRecursiveWithColor(Player.Backpack.Serial, [(0x176B,  0x0014) ] )
if len(IngotKeys) > 0:
    #Misc.SendMessage("Ingot Key found")
    IngotKey = IngotKeys[0]
#
StoneKey = 0
StoneKeys = common.findRecursiveWithColor(Player.Backpack.Serial, [(0x176B,  0x0489) ] )
if len(StoneKeys) > 0:
    #Misc.SendMessage("Stone Key found")
    StoneKey = StoneKeys[0]
#
GemKey = 0
GemKeys = common.findRecursiveWithColor(Player.Backpack.Serial, [(0x176B,  0x0482) ] )
if len(GemKeys) > 0:
    #Misc.SendMessage("Gem Key found")
    GemKey = GemKeys[0]



Using_Garg = False

ore_locations = set()
for loc in locations:
    ore_locations.add( (loc[0], loc[1], loc[2]) )

def check_ore_locations(x, y):
    global ore_locations    
    for loc in ore_locations:
        if x == loc[0] and y == loc[1]:
            return loc[2]
    return None        
#
def update_ore_locations(x, y, color):
    global ore_locations
    # dont add locations that are already being mined with Garg pick
    global Using_Garg
    if Using_Garg:
        Misc.SendMessage("USING GARG")
        return
    if color == "Iron":
        return    
    locationData = check_ore_locations(x, y)
    if locationData == None or locationData == "Iron": 
        ore_locations.add( (x, y, color) )
        Misc.SendMessage("ADDED LOCATION for {}".format(color))
        mining_data_file = open(Mining_Data_File, "w")
        mining_data_file.write(JavaScriptSerializer().Serialize(ore_locations))
        mining_data_file.close()
#
# "Agapite", "Copper", "Valorite", "Ice", "Toxic", "Electrum",
Garg_Ore_Types = [
                  "Toxic",
                  "Electrum",
                  "Platinum" 
                 ]  
import re  
def check_use_garg():
    global Using_Garg 
    update = False
    journalEntry = None
    x = Player.Position.X / 8
    y = Player.Position.Y / 8 
    if Journal.Search("You put some"):
        journalEntry = Journal.GetLineText("You put some", False)
        groups = re. search('some\s+(.+)\sore', journalEntry)       
        if groups:               
            update_ore_locations(x, y, groups.group(1))
        else:
            Misc.SendMessage("NO GROPUPS!")    
    #
    ore_color = check_ore_locations(x, y)
    if ore_color in Garg_Ore_Types:
        Using_Garg = True
        Player.HeadMessage(9, "Use Garg to upgrade {}".format(ore_color))
        return True
    Using_Garg = False
    return False
    
Journal.Clear()
Packhorse = 0x40056C38

if Misc.CheckSharedValue("BagOfHolding"):
    BagOfHolding = Misc.ReadSharedValue("BagOfHolding")
else:
    BagOfHolding = 0x00  # PUT YOUR BOH ID HERE
                
shovelID = 0x0F39
pickaxeID = 0x0E86
waitForTarget = 5000
waitAfterMining = 2000
waitAfterPickAxe = 4000
pickaxe_spots = List[int] (( 0x136D, 0x1367, 0x136A)) 


def getVeins():
    findVeins = Items.Filter()
    findVeins.Enabled = True
    findVeins.OnGround = 1
    findVeins.Movable = False
    findVeins.RangeMin = -1
    findVeins.RangeMax = 2
    findVeins.Graphics = pickaxe_spots
    findVeins.Hues = List[int]((  ))
    findVeins.CheckIgnoreObject = True
    listVeins = Items.ApplyFilter(findVeins)
    return listVeins

#
MotionMap = {
             "North": (0, -1), 
             "Right": (+1, -1),
             "East": (+1, 0),
             "Down": (+1, +1),
             "South": (0, +1),
             "Left": (-1, +1),
             "West": (-1, 0),
             "Up": (-1, -1),
             } 
             
RotateMap = {
             "North": "Right", 
             "Right": "East",
             "East": "Down",
             "Down": "South",
             "South": "Left",
             "Left": "West",
             "West": "Up",
             "Up": "North"
             } 

CaveTiles = [ 0xae, 0x5, 0x3, 0xc1, 0xc2, 0xc3, 0xbd, 0x0016, 0x0017, 0x0018, 0x0019, 0x245, 0x246, 0x247, 0x248, 0x249, 0x22b, 0x22c, 0x22d, 0x22e, 0x22f ]    
SoilTiles = [0x73, 0x74, 0x75, 0x76,  0x77, 0x78]
#    
def MineSpot():
    direction = Player.Direction
    x_delta, y_delta = MotionMap[Player.Direction]
    x = Player.Position.X + x_delta
    y = Player.Position.Y + y_delta
    xStart = Player.Position.X
    yStart = Player.Position.Y
    #
    land_id = Statics.GetLandID(x, y, Player.Map)
    Misc.SendMessage("X: {} Y: {} LandID: 0x{:x} ImPassable: {}".format(x, y, land_id, Statics.GetLandFlag(land_id, "Impassable")))
    if Statics.GetLandFlag(land_id, "Impassable") or land_id in CaveTiles or True:
        Journal.Clear()
        retry = 0
        while True:
            if Player.Position.X != xStart:
                return
            if Player.Position.Y != yStart:
                return    
            if Journal.Search('There is no'):
                Player.HeadMessage(5, "DONE DONE")
                break
            if Journal.Search('no sand'):
                Player.HeadMessage(5, "DONE DONE")                
                break
            if Journal.Search('Target cannot be seen') or Journal.Search('You can\'t mine'):
                retry = retry + 1
                Misc.SendMessage("Retry: {} to find a mining spot".format(retry), 54)
                direction = RotateMap[direction]
                Misc.SendMessage("Try in the {} direction".format(direction), 54)
                x_delta, y_delta = MotionMap[direction]
                x = Player.Position.X + x_delta
                y = Player.Position.Y + y_delta
                xStart = Player.Position.X
                yStart = Player.Position.Y
                #
                Journal.Clear()
                Misc.Pause(500)
                if retry > 6:
                    break
            #
            tileinfo = Statics.GetStaticsLandInfo(x, y, Player.Map)
            if check_use_garg():
                if Items.BackpackCount(0x0E86, 0x076c) > 0:
                    Items.UseItemByID(0x0E86, 0x076c)
                elif Items.BackpackCount(0x0E85, 0x076c) > 0:    
                    Items.UseItemByID(0x0E85, 0x076c)
                else:
                    Player.HeadMessage(1, "NO GARG PICKS")
                    if Items.BackpackCount(0x0E86, 0) > 0:
                        Items.UseItemByID(0x0E86, -1)    
                    else:    
                        Items.UseItemByID(shovelID, -1)    
                Mobiles.Message (Player.Serial, 4, "Using Garg Axe")
            else:    
                if Items.BackpackCount(0x0E86, 0) > 0:
                    Items.UseItemByID(0x0E86, -1)    
                else:    
                    Items.UseItemByID(shovelID, -1) 
            Target.WaitForTarget(waitForTarget,False)                    
            tiles = Statics.GetStaticsTileInfo(x, y, Player.Map)
            #Misc.SendMessage("LandID: 0x{:x} #tiles{}".format(tileinfo.StaticID, len(tiles)), 5)
            if tileinfo.StaticID in CaveTiles and len(tiles) > 0:
                #Misc.SendMessage("StaticID: 0x{:x} #tiles{}".format(tiles[0].StaticID, len(tiles)), 5)
                Target.TargetExecute(x, y, tiles[0].StaticZ, tiles[0].StaticID)
            else:
                staticZ = Statics.GetLandZ(x, y, Player.Map)
                Target.TargetExecute(x, y, staticZ)
            Misc.Pause(waitAfterMining)
            on_me_filter = Mobiles.Filter()
            on_me_filter.Enabled = True
            on_me_filter.RangeMin = -1
            on_me_filter.RangeMax = 2
            on_me_filter.Bodies = List[int] ( [ 0x006F ] )
            on_me_filter.Notorieties = List[Byte](bytes([3,4,5,6]))
            up_close_enemies = Mobiles.ApplyFilter(on_me_filter)
            if len(up_close_enemies) > 0:
                Player.HeadMessage(2, "STOPPING FOR AGRO")
                Stop()
            if Player.WarMode == True:
                Stop()    
            if Target.HasTarget(): 
                Target.Cancel()                    
            CheckWeight()    
    listVeins = getVeins()
    if listVeins != None and len(listVeins) > 0:
        for vein in listVeins:
            while Items.FindBySerial(vein.Serial):
                Items.UseItemByID(pickaxeID,0)
                Target.WaitForTarget(waitForTarget,False)
                Target.TargetExecute(vein)
                Misc.Pause(waitAfterMining)
                CheckWeight()
            if Target.HasTarget(): 
                Target.Cancel()
            #tileinfo = Statics.GetStaticsTileInfo(Player.Position.X,Player.Position.Y, Player.Map)
            #if tileinfo.Count > 0:
            #    for tile in tileinfo:
            #    if tile.StaticID > 1340 and tile.StaticID < 1350 and tile.StaticZ == Player.Position.Z :

#
def StoreItems():
    if StoneKey:                 
        Misc.WaitForContext(StoneKey, 1000)
        Misc.ContextReply(StoneKey, "Refill from stock")        
    if GemKey:                 
        Misc.WaitForContext(GemKey, 1000)
        Misc.ContextReply(GemKey, "Refill from stock") 
    #    
    ORE = [0x19B7, 0x19B8, 0x19B9, 0x19Ba ]
    ores = common.findRecursive(Player.Backpack.Serial, ORE)
    for ore in ores: 
        propList = Items.GetPropStringList(ore)
        coal = False
        for prop in propList:
            if "Coal" in prop:
                coal = True
        #                    
        if PortableForge and ore.Hue != 0x0481 and not coal: # don't smelt plat
            Items.UseItem(ore.Serial)   
            Target.WaitForTarget(2000)
            if Target.HasTarget():                    
                Target.TargetExecute(PortableForge)                    
            else:    
                Items.Move(ore, BagOfHolding, 0)
            Misc.Pause(1000)
        else:    
            Items.Move(ore, BagOfHolding, 0)
            Misc.Pause(1000)
            
    OtherStorable = [ 0x1779, 0x11EA, 0x0F81,]
    others = common.findRecursive(Player.Backpack.Serial, OtherStorable)
    for other in others:             
        Items.Move(other, BagOfHolding, 0)
        Misc.Pause(1000)
    #
    if IngotKey:
        Misc.WaitForContext(IngotKey, 1000)
        Misc.ContextReply(IngotKey, "Refill from stock")        
    else:        
        # Move any ingots to BOH        
        for item in Player.Backpack.Contains:
            if item.ItemID == 0x1BF2:
                Items.Move(item, BagOfHolding, 0)    
#    
def CheckWeight():
    if Player.Weight < (Player.MaxWeight*.9) and Player.Weight < MaxWeight:
        return 0
    # 
    StoreItems()    
    #
    if Player.Weight < (Player.MaxWeight*.9) and Player.Weight < MaxWeight:
        return 0
    
    Player.HeadMessage(55, "Even after move I am over weight")
    Misc.SendMessage("Even after move I am over weight")
    Misc.SendMessage("STOPPING")
    sys.exit(99)        
                
def WeaponInHand():
    w_r = Player.GetItemOnLayer('RightHand')
    #Misc.SendMessage("right={}".format(w_r))
    w_l = Player.GetItemOnLayer('LeftHand')
    #Misc.SendMessage("left={}".format(w_l))
    if w_l != None: 
       weapon = w_l
    elif w_r != None:    
       weapon = w_r
    else:
       weapon = None       
    return weapon


CheckWeight()
MineSpot()
StoreItems()
    
