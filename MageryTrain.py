
def Meditate():  
    if not Player.BuffsExist('Meditation') and not Timer.Check('meditationTimer'):
        Misc.Pause(200)
        Player.HeadMessage(5, "Meditating")
        Player.UseSkill('Meditation')
        Timer.Create('meditationTimer', 8200)
        

if Player.GetSkillValue( 'Magery' ) < 50.0:
    if Player.Mana > 5:
        Spells.CastMagery("Wall of Stone")
        Target.WaitForTarget(2000, True)
        Target.Self()
    else:
        Meditate()
elif Player.GetSkillValue( 'Magery' ) < 62.8:
    if Player.Mana > 10:
        Spells.CastMagery("Mana Drain")
        Target.WaitForTarget(2000, True)
        Target.Self()
    else:
        Meditate()
elif Player.GetSkillValue( 'Magery' ) < 75.5:
    if Player.Mana > 20:
        Spells.CastMagery("Invisibility")
        Target.WaitForTarget(2000, True)
        Target.Self()
    else:
        Meditate()
elif Player.GetSkillValue( 'Magery' ) < 88.0:
    if Player.Mana > 40:
        Spells.CastMagery("Mana Vampire")
        Target.WaitForTarget(2000, True)
        Target.Self()
    else:
        Meditate()
else:
    if Player.Mana > 50:
        Spells.CastMagery("Air Elemental")
        Target.WaitForTarget(2000, True)
        Target.Self()
        if Player.Followers > 1:
            Player.ChatSay(5, "An Air Elemental Release")
            Misc.Pause(200)
    else:
        Meditate()

Misc.Pause(2000)

#if Player.Mana > spells.manaCost
#    Spells.CastMagery(spell)

    # Target the cast spell on the Player
#    Target.WaitForTarget( 2000, True )
#    Target.TargetExecute( Player.Serial )
#else:
#    Player.UseSkill( 'Meditation' )
#    Timer.Create( 'meditationTimer', meditationTimerMilliseconds )
#    Misc.Pause( 200 )
#    while Player.Mana < spell.manaCost + 1:
#        if not Player.BuffsExist( 'Meditation' ) and not Timer.Check( 'meditationTimer' ):
#            Player.UseSkill( 'Meditation' )
#            Timer.Create( 'meditationTimer', meditationTimerMilliseconds )
#        Misc.Pause( 200 )
                
#if Player.Mana > 10:
#    Spells.CastMagery("Greater Heal")
#    Target.WaitForTarget(5000, False)
#    Target.Self()
    
#Player.UseSkill("Meditation")    
#Misc.Pause(2000)
