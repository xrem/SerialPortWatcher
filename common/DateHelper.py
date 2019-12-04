if __name__ == "__main__":
    raise ImportError()

from datetime import datetime as d

def getCurrentDate():
  t = d.today().timetuple()
  return '{:02}.{:02}.{:04} {:02}:{:02}:{:02}'.format (t[2], t[1], t[0], t[3], t[4], t[5])