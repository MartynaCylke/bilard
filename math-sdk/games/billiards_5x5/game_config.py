from typing import Dict, Tuple, List

NUM_REELS = 5
NUM_ROWS: List[int] = [5,5,5,5,5]

# 10 bil (kolory)
SYMBOLS = ["R","G","B","Y","O","W","Br","P","Te","Bk"]  # Bk=black

# Paytable (wg screena, w multipliers x bet)
TIER_L  = {"3":10, "4":50,  "5":100}   # 1.00, 0.50, 0.10
TIER_M1 = {"3":50, "4":150, "5":300}   # 3.00, 1.50, 0.50
TIER_M2 = {"3":100,"4":300, "5":600}   # 6.00, 3.00, 1.00
TIER_H  = {"3":200,"4":500, "5":1000}  # 10.00, 5.00, 2.00

TIERS = {"R":"L","G":"L","B":"L", "Y":"M1","O":"M1",
         "W":"M2","Br":"M2", "P":"H","Te":"H", "Bk":"H"}

def tier_table(t): return {"L":TIER_L,"M1":TIER_M1,"M2":TIER_M2,"H":TIER_H}[t]

PAYTABLE: Dict[Tuple[int,str], int] = {}
for s in SYMBOLS:
    t = tier_table(TIERS.get(s,"L"))
    for k in (3,4,5):
        PAYTABLE[(k, s)] = t[str(k)]

RTP_TARGET = 0.98
MODES = [("base", 1.0)]

# Jackpot (czarna bila, klaster >=4)
JACKPOT_TRIGGER_SYMBOL = "Bk"
JACKPOT_MIN_CLUSTER = 4
JACKPOT_MULTIPLIER = 2000

# Proste paski – optymalizator i tak doważy
REELSTRIPS: List[List[str]] = [["R","G","B","Y","O","W","Br","P","Te","Bk"] * 3 for _ in range(NUM_REELS)]
