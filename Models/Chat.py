class Role:
    SYS = "system"
    USER = "user"
    AGENT = "assistant"

class Chat:
    def __init__(self, system_message) -> None:
        self.sys = system_message
        self.messages = []
    
    def message(self, role, msg):
        self.messages.append( { "role": role, "content": msg } )
    
    def format(self):
        messages = self.messages.copy()

        if self.sys:
            messages.insert(-1, self.sys)
        
        return messages