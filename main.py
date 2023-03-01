"""
@Project, that enables for disabled people to be able to communicate with non-disabled people.

@Author: Emir Cetin Memis

@Contributors:
    - Ahmet Yildiz
    - Cem Baysal

@Date: 1/24/2023
"""

from Utilities  import  safe_start, safe_stop
from GUI        import  Application

if __name__ == "__main__" :
    
    safe_start()

    Application().mainloop()

    safe_stop()
