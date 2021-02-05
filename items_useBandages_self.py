from glossary.colors import colors

bandages = Items.FindByID( 0x0E21, -1, Player.Backpack.Serial )

while bandages != None:
    #if bandages != None:
    if Player.Hits < Player.HitsMax:
        Items.UseItem( bandages )
        Target.WaitForTarget( 2000, False )
        Target.TargetExecute( Player.Serial )
        Misc.Pause(10000)
    else:
        Player.HeadMessage(5, 'HP full')
        Misc.Pause(5000)
    #    Player.HeadMessage( colors[ 'red' ], 'Out of bandages!' )
Player.HeadMessage( colors[ 'red' ], 'Out of bandages!' )