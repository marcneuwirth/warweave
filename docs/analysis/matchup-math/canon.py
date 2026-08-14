from sim2 import Cont, run, show
import sys

def C(n,k=1,tech=None): return Cont(n,k,tech)

print("### A. The eleven §28 canonical matchups, at natural squad scale (1 squad unless noted)\n")
show("1. Militia vs Direwolves",              [C('Militia')],   [C('Direwolves')])
show("1b. Militia x2 vs Direwolves (equal-ish gold)",[C('Militia',2)],[C('Direwolves')])
show("2. Militia vs Ember Mage",              [C('Militia')],   [C('EmberMage')])
show("3. Hunters vs Direwolves",              [C('Hunters')],   [C('Direwolves')])
show("4. Spear Guard vs Direwolves",          [C('SpearGuard')],[C('Direwolves')])
show("5. Spear Guard vs Troll",               [C('SpearGuard')],[C('Troll')])
show("5b. Spear Guard +Hooked vs Troll",      [C('SpearGuard',1,'HookedSpears')],[C('Troll')])
show("6. Longbowmen vs Troll",                [C('Longbowmen')],[C('Troll')])
show("6b. Longbowmen vs Troll +Stonehide",    [C('Longbowmen')],[C('Troll',1,'Stonehide')])
show("6c. Longbowmen +Bodkin vs Troll +Stonehide",[C('Longbowmen',1,'BodkinArrows')],[C('Troll',1,'Stonehide')])
show("7. Ember Mage vs Militia",              [C('EmberMage')], [C('Militia')])
show("7b. Ember Mage vs Militia x2",          [C('EmberMage')], [C('Militia',2)])
show("8. Ember Mage vs Troll",                [C('EmberMage')], [C('Troll')])
show("8b. Ember Mage +Focused vs Troll",      [C('EmberMage',1,'FocusedFlame')],[C('Troll')])
show("9. Frostcaller + Longbowmen vs Troll",  [C('Frostcaller'),C('Longbowmen')],[C('Troll')])
show("9b. Frostcaller+DeepFreeze + Longbow vs Troll",[C('Frostcaller',1,'DeepFreeze'),C('Longbowmen')],[C('Troll')])
show("9c. Longbowmen alone vs Troll (control)",[C('Longbowmen')],[C('Troll')])
print()
LINE = lambda: [C('SpearGuard'),C('Longbowmen')]          # 450g protected ranged line
show("10. Outriders x2 vs protected ranged line", [C('Outriders',2)], LINE())
show("10b. Outriders x2 +Javelin vs line",        [C('Outriders',2,'JavelinVolley')], LINE())
show("11. Direwolves x2 vs protected ranged line",[C('Direwolves',2)], LINE())
show("11b. Direwolves x2 vs UNprotected Longbow x2",[C('Direwolves',2)],[C('Longbowmen',2)])
show("11c. Direwolves x2 +Pack vs protected line",[C('Direwolves',2,'PackHunter')], LINE())

print("\n### B. Technology deltas (same matchup, tech on / off)\n")
tests=[
 ("Militia vs Direwolves",            ('Militia',1,None),('Direwolves',1,None)),
 ("Militia+Conscription vs Direwolves",('Militia',1,'Conscription'),('Direwolves',1,None)),
 ("Militia+Pitch vs Direwolves",      ('Militia',1,'PitchTorch'),('Direwolves',1,None)),
 ("Militia x4 vs Troll",              ('Militia',4,None),('Troll',1,None)),
 ("Militia x4 +Pitch vs Troll",       ('Militia',4,'PitchTorch'),('Troll',1,None)),
 ("Hunters x2 vs Direwolves",         ('Hunters',2,None),('Direwolves',1,None)),
 ("Hunters x2 +Rapid vs Direwolves",  ('Hunters',2,'RapidFire'),('Direwolves',1,None)),
 ("Hunters x2 +Loose vs Ember Mage",  ('Hunters',2,'LooseFormation'),('EmberMage',1,None)),
 ("Hunters x2 vs Ember Mage",         ('Hunters',2,None),('EmberMage',1,None)),
 ("SpearGuard vs Direwolves",         ('SpearGuard',1,None),('Direwolves',1,None)),
 ("SpearGuard+Phalanx vs Direwolves", ('SpearGuard',1,'Phalanx'),('Direwolves',1,None)),
 ("SpearGuard+Hooked vs Outriders",   ('SpearGuard',1,'HookedSpears'),('Outriders',1,None)),
 ("SpearGuard vs Outriders",          ('SpearGuard',1,None),('Outriders',1,None)),
 ("Longbowmen vs Militia x2",         ('Longbowmen',1,None),('Militia',2,None)),
 ("Longbowmen+Volley vs Militia x2",  ('Longbowmen',1,'VolleyFire'),('Militia',2,None)),
 ("EmberMage vs Militia x2",          ('EmberMage',1,None),('Militia',2,None)),
 ("EmberMage+Firestorm vs Militia x2",('EmberMage',1,'Firestorm'),('Militia',2,None)),
 ("Direwolves vs Longbowmen",         ('Direwolves',1,None),('Longbowmen',1,None)),
 ("Direwolves+Pounce vs Longbowmen",  ('Direwolves',1,'Pounce'),('Longbowmen',1,None)),
 ("Troll vs SpearGuard x1.5",         ('Troll',1,None),('SpearGuard',1.5,None)),
 ("Troll+Stonehide vs SpearGuard x1.5",('Troll',1,'Stonehide'),('SpearGuard',1.5,None)),
 ("Outriders vs Hunters",             ('Outriders',1,None),('Hunters',1,None)),
 ("Outriders+Flanking vs Hunters",    ('Outriders',1,'FlankingManeuver'),('Hunters',1,None)),
 ("Outriders+Javelin vs Hunters",     ('Outriders',1,'JavelinVolley'),('Hunters',1,None)),
]
for label,(an,ak,at),(bn,bk,bt) in tests:
    show(label,[C(an,ak,at)],[C(bn,bk,bt)])
