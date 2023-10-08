import pygame

class KeyData:
    def __init__(self) -> None:
        self.previous_key_state = {}
    
    def get_key_on_hold(self, key_code:int):
        keys = pygame.key.get_pressed()
        
        return keys[key_code]
    
    def get_key_on_keydown(self, key_code):
        keys = pygame.key.get_pressed()
        previous_state = self.previous_key_state.get(key_code, False)

        if keys[key_code] and not previous_state:
            self.previous_key_state[key_code] = True
            return True
        elif not keys[key_code]:
            self.previous_key_state[key_code] = False

        return False
            
        