from Utilities  import  safe_start, safe_stop
from GUI        import  Application

if __name__ == "__main__" :
    
    safe_start()

    Application().mainloop()

    safe_stop()
