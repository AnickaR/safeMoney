import tkinter as Tk

class Safe(Tk.Tk):
    name = 'Safe'

    def __init__ (self, fileName):
      self.fileName = fileName
      super().__init__(className=self.name)

      self.money = {} # variable for memory money same in file
      self.loadMoney()

      self.title = 'Trezor'

      # entery for getting money
      vcmd = (self.register(self.validate), '%P')
      self.var_moneyOut = Tk.IntVar()
      self.ent_moneyOut = Tk.Entry(self, textvariable=self.var_moneyOut, validate='all', validatecommand=vcmd)
      self.ent_moneyOut.pack()

      self.btn_getMoney = Tk.Button(self, text='Sypej', command=self.actionGetMoney)
      self.btn_getMoney.pack()

      self.fm_showMoney = Tk.Frame(self)
      self.fm_showMoney.pack()

    
    def validate(self, value_if_allowed):
      if value_if_allowed:
          try:
              int(value_if_allowed)
              return True
          except ValueError:
              return False
      else:
          return False

    def loadMoney(self):
      safe = open(self.fileName, 'r')
      money = safe.readline().split('|')
      money = [v.split(' ') for v in money]
      money = {int(v[0]): int(v[1]) for v in money}
      self.money = money
      safe.close()
    
    def uploadMoney(self):
      safe = open(self.fileName, 'w')
      data = [[str(coin), str(count)] for coin, count in self.money.items()]
      for i, arr in enumerate(data):
        data[i] = ' '.join(arr)
      data = '|'.join(data)
      safe.write(data)
      safe.close()

    def actionGetMoney(self):
      getValue = self.var_moneyOut.get()
      got = {}
      moneyBefore = self.money
      for coin, count in self.money.items():
        for v in range(count):
          if (getValue - coin >= 0):
            # remove from money we want number of coin
            getValue -= coin
            self.money[coin] -= 1
            try:
              got[coin] += 1
            except:
              got[coin] = 1
      
      if (getValue != 0):
        self.money = moneyBefore
        print('V trezoru nemáte dostatek správných mincí pro tento výběr')
      else:
        self.uploadMoney()
        for child in self.fm_showMoney.winfo_children():
          child.destroy()
        for coin, count in got.items():
          Tk.Label(self.fm_showMoney, text=f"{str(count)} x {str(coin)}").pack()