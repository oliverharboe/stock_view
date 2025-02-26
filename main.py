from controllerv import UserController
from userv import UserView
from modelv import UserModel

def main():
    uv = UserView()
    um = UserModel()
    uc = UserController(um, uv)
    uv.setController(uc)
    uv.run()
    


if __name__ == "__main__":
    main()