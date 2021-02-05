

shovelID = 0x0F39
pickaxeID = 0x0E86
beetle = 0x0000AF57

def smelt():
    Mobiles.FindBySerial(beetle)
    Player.HeadMessage(3,"found")
    types = [0x19B9,0x19B8,0x19BA,0x19B7]
    
    for t in Items.FindBySerial(Player.Backpack.Serial).Contains:
        if t.ItemID in types:
            Items.UseItem(t)
            Target.WaitForTarget(1000,False)
            Target.TargetExecute(beetle)
            Misc.Pause(1000)

Player.HeadMessage(5, "pickaxe")
Items.UseItemByID(pickaxeID, 0)
Target.WaitForTarget(1000, False)
#Target.TargetExecute(2577, 929 ,13)
Target.Last()
Misc.Pause(2000)
Player.HeadMessage(5, "shovel")
Items.UseItemByID(shovelID, 0)
Target.WaitForTarget(1000, False)
#Target.TargetExecute(2577, 929 ,13)
Target.Last()
Misc.Pause(2000)

if Player.Weight > (Player.MaxWeight*.9):
    smelt()