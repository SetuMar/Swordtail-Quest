def func(thing_to_say, do_you_wanna_say):
    if do_you_wanna_say:
        print(thing_to_say)
    
def function_caller(function):
    function()
    
function_caller(lambda: func("HELLO WORLD", True))