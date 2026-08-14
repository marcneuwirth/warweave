import math
from mm import U, armor_mult, final_dmg, frontage, attacking_models

DT=0.02; GAP0=32.0; TIMEOUT=90.0

# ---- AoE catch (#11) -------------------------------------------------------
# #8 modelled splash as "the next k living models in the target contingent",
# with no spacing check, plus a flat aoe_res constant for Loose Formation.
# #11 ruled AoE catch is derived from formation spacing geometry instead:
# models on a lattice of pitch `sp` inside radius `r` is ~ pi*r^2/sp^2.
# Single-model squads catch nothing, and separate squads are never adjacent.
AOE_GEOM = True
VOLLEY_R = 1.5      # #11: "3m area" read as diameter; see AOE_R_CONVENTION

def splash_models(tgt, radius):
    if tgt['n'] <= 1:
        return 0
    if not AOE_GEOM:
        return min(tgt['n']-1, int(3.14159*radius*radius/4.0))
    sp = tgt['sp']
    return max(0, min(tgt['n']-1, int(3.14159*radius*radius/(sp*sp))))

class Cont:   # one contingent = k squads of one unit type, possibly with a tech
    def __init__(self, name, k=1, tech=None, over=None):
        self.name=name; self.k=k; self.tech=tech
        u=dict(U[name]); self.base=dict(u)
        if tech: u=apply_tech(u,tech)
        if over: u.update(over)
        self.u=u
        n=int(round(u['n']*k))
        self.hp0=u['hp']
        self.models=[float(u['hp'])]*n
        self.burn=[0.0]*n; self.chill=[0.0]*n; self.frozen=[0.0]*n; self.imm=[0.0]*n
        self.shield=[0.0]*n
        self.timers=[(i%7)*u['cd']/7.0 for i in range(n)]
        self.cost=u['cost']*k + (tech_cost(name,tech) if tech else 0)
        self.gold=self.cost
        self.first=[True]*n
        self.casts=[0]*n
        self.boulder_cd=[0.0]*n
        self.fa_cd=0.0
    def alive(self): return sum(1 for h in self.models if h>0)
    def tot(self): return sum(max(0.0,h) for h in self.models)
    def max(self): return self.hp0*len(self.models)

def tech_cost(name,tech):
    return 200 if U[name]['branch']=='Common' else 250

def apply_tech(u,t):
    u=dict(u)
    if t=='Conscription': u['n']+=3; u['hp']=round(u['hp']*0.85); u['dmg']=u['dmg']*0.90; u['front']=u['n']//2; u['ranks']=2
    elif t=='PitchTorch': u['pitch']=True
    elif t=='LooseFormation': u['sp']*=1.6; u['aoe_res']=0.20
    elif t=='RapidFire': u['cd']*=0.75; u['dmg']*=0.85
    elif t=='JavelinVolley': u['opening']=1.6; u['rng']=14.0
    elif t=='FlankingManeuver': u['flank']=0.30
    elif t=='Phalanx': u['sp']*=0.8; u['front_phys_res']=0.20
    elif t=='HookedSpears': u['hooked']=True; u['heavy']=True
    elif t=='BodkinArrows': u['pen']=60.0; u['dmg']*=0.90; u['heavy']=False
    elif t=='VolleyFire': u['cd']*=1.2; u['volley']=True
    elif t=='Firestorm': u['firestorm']=True
    elif t=='FocusedFlame': u['focused']=True
    elif t=='DeepFreeze': u['deepfreeze']=True
    elif t=='FrostArmor': u['frostarmor']=True
    elif t=='PackHunter': u['pack']=True
    elif t=='Pounce': u['pounce']=True
    elif t=='Stonehide': u['ar']+=45; u['spd']*=0.9
    elif t=='BoulderThrow': u['boulder']=True; u['rng']=13.0; u['dmg']=90; u['cd']=4.0; u['heavy']=True
    else: raise ValueError(t)
    return u

class Side:
    def __init__(self, conts, label):
        self.c=conts; self.label=label
        self.gold=sum(c.cost for c in conts)
    def alive(self): return sum(c.alive() for c in self.c)
    def rng(self): return max(c.u['rng'] for c in self.c if c.alive()>0) if self.alive() else 0
    def hp_pct(self):
        m=sum(c.max() for c in self.c); return 100.0*sum(c.tot() for c in self.c)/m if m else 0

def pick_target(side, attacker):
    """nearest living contingent; Direwolves prefer Backline (rng>=14) if exposed (no melee screen)"""
    live=[c for c in side.c if c.alive()>0]
    if not live: return None
    if attacker.name=='Direwolves':
        screen=any(c.u['rng']<9.0 for c in live)          # a melee-capable squad present = screened
        back=[c for c in live if c.u['rng']>=14.0]
        if back and not screen: return back[0]
    return live[0]

def run(sideA, sideB, gap0=GAP0, verbose=False):
    A=Side(sideA,'A'); B=Side(sideB,'B'); gap=gap0
    a_adv = A.rng() <= B.rng(); b_adv = B.rng() <= A.rng()
    t=0.0
    while t<TIMEOUT and A.alive()>0 and B.alive()>0:
        v=(max(c.u['spd'] for c in A.c if c.alive()>0) if a_adv else 0)+ \
          (max(c.u['spd'] for c in B.c if c.alive()>0) if b_adv else 0)
        if not (gap<=A.rng() and gap<=B.rng()):
            gap=max(0.0,gap-v*DT)
        for X,Y in ((A,B),(B,A)):
            for c in X.c:
                if c.alive()==0 or gap>c.u['rng']: continue
                tgt_c=pick_target(Y,c)
                if tgt_c is None: continue
                if c.u['rng']>=5.0: am=c.alive()
                else: am=min(c.alive(), int(round(attacking_models(c.u,tgt_c.u)*c.k)))
                idxs=[i for i,h in enumerate(c.models) if h>0][:am]
                for i in idxs:
                    c.timers[i]-=DT
                    if c.timers[i]>0: continue
                    c.timers[i]+=c.u['cd']
                    j=next((k for k,h in enumerate(tgt_c.models) if h>0),None)
                    if j is None: break
                    apply_attack(c,i,tgt_c,j,Y,am)
        for S in (A,B):
            fa=[c for c in S.c if c.u.get('frostarmor') and c.alive()>0]
            if fa:
                fa[0].fa_cd-=DT
                if fa[0].fa_cd<=0:
                    fa[0].fa_cd+=4.0
                    tgts=[c for c in S.c if c.alive()>0]
                    tgts.sort(key=lambda c: (not c.u.get('large'),))
                    tc2=tgts[0]
                    k=next((k for k,h in enumerate(tc2.models) if 0<h<tc2.hp0),None)
                    if k is not None: tc2.models[k]=min(tc2.hp0, tc2.models[k]+120.0)
            for c in S.c:
                for j,h in enumerate(c.models):
                    if h<=0: continue
                    if c.burn[j]>0: c.models[j]-=10.0*DT; c.burn[j]-=DT
                    for arr in (c.frozen,c.imm,c.chill):
                        if arr[j]>0: arr[j]-=DT
                    r=c.u.get('regen',0.0)
                    if r>0:
                        c.models[j]=min(c.hp0, c.models[j]+r*(0.25 if c.burn[j]>0 else 1.0)*DT)
        t+=DT
    win='A' if B.alive()==0 and A.alive()>0 else ('B' if A.alive()==0 and B.alive()>0 else 'TIMEOUT')
    return dict(t=round(t,1),win=win,a_hp=round(A.hp_pct()),b_hp=round(B.hp_pct()),
                a_alive=A.alive(),b_alive=B.alive(),a_gold=A.gold,b_gold=B.gold,
                a_adv=a_adv,b_adv=b_adv)

def apply_attack(c,i,tc,j,Yside,am):
    u=c.u; raw=u['dmg']; pool=0.0
    tgt=tc.u
    if u.get('hooked'): pool += 0.45 if tgt.get('large') else -0.10
    if u.get('pitch') and tgt['branch']=='Beast': pool += 0.30
    if u.get('focused') and tgt.get('large'): pool += 0.80
    if u.get('pack'): pool += min(0.32, 0.08*max(0,min(4,am-1)))
    if u.get('pounce') and c.first[i]: pool += 0.25; c.first[i]=False
    if u.get('opening') and c.first[i]: pool += 0.60; c.first[i]=False
    if tc.frozen[j]>0:
        if u['typ']=='magic': pool += 0.25
        elif u.get('heavy'): pool += 0.25
    delivery=1.0
    defm=[]
    if u['typ']=='phys' and tgt.get('front_phys_res'): defm.append(tgt['front_phys_res'])
    d=final_dmg(raw*(1+pool), tgt, u['typ'], u.get('pen',0.0), delivery, defm)
    tc.models[j]-=d
    if c.name=='EmberMage':
        tc.burn[j]=4.0
        c.casts[i]+=1
        storm = u.get('firestorm') and c.casts[i]%4==0
        rad = 5.0 if storm else (1.25 if u.get('focused') else 2.5)
        cap = splash_models(tgt, rad)
        if storm:
            for k2 in [k for k,h in enumerate(tc.models) if h>0 and k!=j][:cap]:
                tc.models[k2]-=final_dmg(raw*(1+pool)*0.70*(1-tgt.get('aoe_res',0.0)), tgt,'magic'); tc.burn[k2]=4.0
            cap=0
        ns=[k for k,h in enumerate(tc.models) if h>0 and k!=j][:cap]
        aoe = 1.0 if AOE_GEOM else 1-tgt.get('aoe_res',0.0)
        for k2 in ns:
            tc.models[k2]-=final_dmg(raw*(1+pool)*0.5*aoe, tgt,'magic'); tc.burn[k2]=4.0
    if u.get('pitch') and tgt['branch']=='Beast' and tgt.get('large'): tc.burn[j]=max(tc.burn[j],2.0)
    if u.get('volley'):
        aoe=1.0 if AOE_GEOM else 1-tgt.get('aoe_res',0.0)
        ns=[k for k,h in enumerate(tc.models) if h>0 and k!=j][:splash_models(tgt, VOLLEY_R)]
        for k2 in ns: tc.models[k2]-=final_dmg(raw*(1+pool)*0.5*aoe, tgt, u['typ'], u.get('pen',0.0))
    if c.name=='Frostcaller':
        fz = 1.25 if u.get('deepfreeze') else 0.75
        im = 1.75 if u.get('deepfreeze') else 1.25
        if tc.chill[j]>0 and tc.imm[j]<=0 and tc.frozen[j]<=0:
            tc.frozen[j]=fz; tc.imm[j]=fz+im
        tc.chill[j]=3.0

def show(label, A, B):
    r=run(A,B)
    w = {'A':A[0].name if r['win']=='A' else '', 'B':'', 'TIMEOUT':''}
    winner = 'LEFT' if r['win']=='A' else ('RIGHT' if r['win']=='B' else 'TIMEOUT')
    print(f"{label:52s} {winner:8s} t={r['t']:5.1f}s  L{r['a_gold']:5.0f}g@{r['a_hp']:3d}%  R{r['b_gold']:5.0f}g@{r['b_hp']:3d}%")
    return r
