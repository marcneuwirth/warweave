import math, itertools, json

# ---- canonical post-hardening stats (#2 kernel, #3 mechanics, #9 elemental) ----
U = {
 'Militia':    dict(cost=100, n=8, hp=100, ar=0,  dmg=30,  cd=1.0,  rng=1.0,  typ='phys', spd=4.5, rad=0.4, front=4, ranks=2, sp=2.0, heavy=False, branch='Common', large=False),
 'Hunters':    dict(cost=150, n=5, hp=120, ar=0,  dmg=42,  cd=1.6,  rng=16.0, typ='phys', spd=4.0, rad=0.4, front=5, ranks=1, sp=2.0, heavy=False, branch='Common', large=False),
 'Outriders':  dict(cost=200, n=3, hp=260, ar=20, dmg=55,  cd=2.0,  rng=9.0,  typ='phys', spd=6.5, rad=0.8, front=3, ranks=1, sp=3.0, heavy=False, branch='Common', large=True, melee=1.2),
 'SpearGuard': dict(cost=200, n=6, hp=210, ar=30, dmg=48,  cd=1.5,  rng=2.2,  typ='phys', spd=4.5, rad=0.4, front=6, ranks=1, sp=2.0, heavy=False, branch='Military', large=False),
 'Longbowmen': dict(cost=250, n=5, hp=135, ar=0,  dmg=78,  cd=2.4,  rng=25.0, typ='phys', spd=4.0, rad=0.4, front=5, ranks=1, sp=2.0, heavy=True,  branch='Military', large=False),
 'EmberMage':  dict(cost=200, n=1, hp=360, ar=0,  dmg=95,  cd=2.25, rng=17.0, typ='magic',spd=4.0, rad=0.4, front=1, ranks=1, sp=2.0, heavy=False, branch='Magic', large=False),
 'Frostcaller':dict(cost=225, n=1, hp=390, ar=0,  dmg=45,  cd=1.8,  rng=18.0, typ='magic',spd=4.0, rad=0.4, front=1, ranks=1, sp=2.0, heavy=False, branch='Magic', large=False),
 'Direwolves': dict(cost=200, n=8, hp=125, ar=0,  dmg=34,  cd=0.9,  rng=1.0,  typ='phys', spd=7.5, rad=0.5, front=4, ranks=2, sp=2.0, heavy=False, branch='Beast', large=False),
 'Troll':      dict(cost=300, n=1, hp=1250,ar=25, dmg=105, cd=2.0,  rng=2.4,  typ='phys', spd=3.5, rad=1.2, front=1, ranks=1, sp=3.0, heavy=True,  branch='Beast', large=True, regen=25.0),
}
MELEE = {'Militia','Outriders','SpearGuard','Direwolves','Troll'}   # Outriders melee inside 3m

def armor_mult(armor, typ, pen=0.0, bypass=None):
    b = 0.5 if typ=='magic' else 0.0
    if bypass is not None: b = bypass
    eff = max(0.0, armor*(1.0-b) - pen)
    return 100.0/(100.0+eff)

def final_dmg(raw, target, typ, pen=0.0, delivery=1.0, defmods=()):
    d = raw*delivery*armor_mult(target['ar'], typ, pen)
    for m in defmods: d *= (1.0-m)
    return max(1.0, math.floor(d))

def frontage(u):
    return (u['front']-1)*u['sp'] + 2*u['rad']

def attacking_models(a, d):
    """models of squad a able to attack squad d simultaneously"""
    if a['n']==1: return 1
    if d['n']==1:
        # envelopment: ring circumference / collision arc
        R = d['rad'] + a['rad'] + a.get('melee', a['rng'] if a['rng']<5 else 0.0)
        if a['rng']>=5: return a['n']            # ranged, all fire
        cap = math.floor(2*math.pi*R/(2*a['rad']))
        return min(a['n'], cap)
    if a['rng']>=5: return a['n']                # ranged line, all fire
    reach = a.get('melee', a['rng'])
    # ranks that can reach: rank k needs reach >= (k-1)*spacing (surface-to-surface)
    ranks_ok = 1 + sum(1 for k in range(2, a['ranks']+1) if reach >= (k-1)*a['sp'])
    # lateral: contact width = defender frontage + 2*reach
    width = frontage(d) + 2*reach
    per_rank = min(a['front'], math.floor(width/a['sp'])+1)
    return min(a['n'], per_rank*ranks_ok)

def ttk(aname, dname, a_over=None, d_over=None, verbose=False):
    a = dict(U[aname]); d = dict(U[dname])
    if a_over: a.update(a_over)
    if d_over: d.update(d_over)
    per = final_dmg(a['dmg'], d, a['typ'], a.get('pen',0.0), a.get('delivery',1.0), a.get('defmods',()))
    hits = math.ceil(d['hp']/per)
    am = attacking_models(a, d)
    total_hits = hits*d['n']
    t = total_hits*a['cd']/am
    # regen credit
    regen = d.get('regen',0.0)*d.get('regenmult',1.0)
    dps = am*per/a['cd']
    net = dps - regen
    if regen>0:
        t = float('inf') if net<=0 else (d['hp']*d['n'])/net * (per*hits/d['hp'])
    eff = d['hp']/(per*hits)
    return dict(per=per, hits=hits, am=am, ttk=t, dps=dps, netdps=net, overkill_eff=eff)

if __name__=='__main__':
    names = list(U)
    print("=== per-model / squad reference ===")
    for k,v in U.items():
        print(f"{k:12s} cost{v['cost']:4d} n{v['n']:2d} hp{v['hp']:5d} ar{v['ar']:3d} dmg{v['dmg']:4d} cd{v['cd']:4.2f} "
              f"squadDPS(raw){v['n']*v['dmg']/v['cd']:7.1f} front{frontage(v):5.1f}m totHP{v['n']*v['hp']:5d}")
    
    print("\n=== equal-gold TTK matrix (seconds for ROW to wipe COLUMN, gold-normalized) ===")
    # equal gold: TTK = (cost_A/cost_B) * ttk_one_squad_of_A_vs_one_squad_of_B  -- since G/cost squads each side
    hdr = f"{'':12s}" + "".join(f"{n[:9]:>10s}" for n in names); print(hdr)
    M = {}
    for A in names:
        row = f"{A:12s}"
        for B in names:
            r = ttk(A,B)
            t = r['ttk']*(U[A]['cost']/U[B]['cost'])
            M[(A,B)] = t
            row += "      inf" .rjust(10) if math.isinf(t) else f"{t:10.1f}"
        print(row)
    
    print("\n=== equal-gold winner / margin (row TTK vs col TTK; ratio>1 = ROW loses) ===")
    print(f"{'':12s}" + "".join(f"{n[:9]:>10s}" for n in names))
    for A in names:
        row=f"{A:12s}"
        for B in names:
            ta, tb = M[(A,B)], M[(B,A)]
            if A==B: row+=f"{'--':>10s}"; continue
            if math.isinf(ta) and math.isinf(tb): row+=f"{'stall':>10s}"
            elif math.isinf(ta): row+=f"{'LOSS':>10s}"
            elif math.isinf(tb): row+=f"{'WIN':>10s}"
            else: row+=f"{ta/tb:10.2f}"
        print(row)
    
    print("\n=== damage-per-gold (squad DPS applied / cost) vs each armor tier ===")
    for tier,ar in [('0 armour',0),('20 (Outriders)',20),('25 (Troll)',25),('30 (SpearGuard)',30),('70 (Stonehide)',70)]:
        print(f"-- vs {tier}")
        for A in names:
            a=U[A]; per=final_dmg(a['dmg'], {'ar':ar}, a['typ'])
            print(f"   {A:12s} {a['n']*per/a['cd']:7.1f} dps  {a['n']*per/a['cd']/a['cost']:6.3f} dps/gold")
    
    print("\n=== effective-HP-per-gold ===")
    for A in names:
        a=U[A]; tot=a['n']*a['hp']
        ep = tot/armor_mult(a['ar'],'phys'); em = tot/armor_mult(a['ar'],'magic')
        print(f"{A:12s} rawHP{tot:5d}  eHP_phys{ep:7.0f} ({ep/a['cost']:5.2f}/g)  eHP_magic{em:7.0f} ({em/a['cost']:5.2f}/g)")
    
    print("\n=== attackingModels matrix (row attacker) ===")
    print(f"{'':12s}" + "".join(f"{n[:9]:>10s}" for n in names))
    for A in names:
        print(f"{A:12s}" + "".join(f"{attacking_models(U[A],U[B]):10d}" for B in names))
    
    print("\n=== overkill efficiency (row attacker into col target) ===")
    print(f"{'':12s}" + "".join(f"{n[:9]:>10s}" for n in names))
    for A in names:
        print(f"{A:12s}" + "".join(f"{ttk(A,B)['overkill_eff']*100:9.0f}%" for B in names))
    