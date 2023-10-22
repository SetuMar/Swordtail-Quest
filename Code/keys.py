import pygame

class KeyData:
    def __init__(self) -> None:
        self.previous_key_state = {}
        # previous keys and if they have been pressed
    
    def get_key_on_hold(self, key_code:int):
        keys = pygame.key.get_pressed()
        # get pressed keys
        
        return keys[key_code]
        # check if selected key is being pressed
    
    def get_key_on_keydown(self, key_code):
        keys = pygame.key.get_pressed()
        # get pressed keys
        previous_state = self.previous_key_state.get(key_code, False)
        # get the previous state of the key

        if keys[key_code] and not previous_state:
        # if the key is being pressed and the key hasn't been pressed yet
            self.previous_key_state[key_code] = True
            # set the state of pressed to true
            return True
            # return True
        elif not keys[key_code]:
        # if the key isn't pressed
            self.previous_key_state[key_code] = False
            # then set it's state to false
            
        return False
        # if the key is being held or hasn't been pressed yet return False
            
        