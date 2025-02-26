
class UserController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
    def getdata(self,ticker):
        return self.model.getdata(ticker)