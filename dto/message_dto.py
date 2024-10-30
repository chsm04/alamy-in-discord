class MessageDTO:

    def __init__(self, uid, name, content):
        self.uid = uid
        self.name = name
        self.content = content
    
    # def greet(self):
    #     return f"Hello, {self.name}!"

# user = UserData(uid="user123", name="Alice", age=30)
# print(user.greet())  # 클래스 내 메서드로 접근 가능