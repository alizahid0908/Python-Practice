def announcer(f):
    def wrapper():
        print("About to run the function...")
        f()
        print("Funtion completeted")
    return wrapper

@announcer
def hello():
    print("Hello world")

hello()
