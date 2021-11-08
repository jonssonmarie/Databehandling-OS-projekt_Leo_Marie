"""
Uppgift 1 - Landstatistik

Ni får ett land tilldelat till er grupp. Börja med att anonymisera kolumnen med idrottarnas namn med
hashfunktionen SHA-256.
Undersök därefter hur det gått för landet i OS genom tiderna. Visualisera exempelvis:
de sporter landet fått flest medaljer i
antal medaljer per OS
histogram över åldrar
Skapa fler plots för att visualisera flera aspekter kring ert land och dess sportprestationer i O
"""
import pandas as pd
import numpy as np
from load_data import create_df

