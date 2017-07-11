class SpellType:
    TaxCollection = {
        'num': 1,
        'cost': 200,
        'time': 0
    }

    CallToArms = {
        'num': 2,
        'cost': 400,
        'time': 20
        };
        
    BloodFrenzy = {
        'num': 3,
        'cost': 600,
        'time': 0
        };
        
    GoblinsGreed = {
        'num': 4,
        'cost': 500,
        'time': 0
        };
        
    HellfireBlast = {
        'num': 4,
        'cost': 1000,
        'time': 0
        };

    FairyChanting = {
        'num': 4,
        'cost': 800,
        'time': 8
        };
    
class SpellMode:
    Disabled = 0;
    Syncronised = 1;
    Delay = 2;
    DelayedBurst = 3;