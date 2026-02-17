



# config to run the server n times if it fails
# config to inject information into the server such as ip address, mac address of the machine ...
# Decorator Factory
def configuration(*decorator_args,**decorator_kwargs):
    def logger(func):
        def wrapper(*args,**kwargs):
            merged_kwargs = {
                **kwargs,
                **decorator_kwargs
            }
            # run the function n number of times if it fails
            for i in range(decorator_args[0]):
                print("Attempting to run the Function",i+1)
                success = func(*args,**merged_kwargs)
                if success:
                    print("Function ran successfully")
                    break
                else:
                    print("Function Failed, retrying ...")
               
        return wrapper
    return logger

@configuration(2,mac_address=796567)
def server(ipaddr,port=8080,**kwargs)-> bool:
    if kwargs["mac_address"]:
        print(kwargs["mac_address"])
        print(f"Server Running in {ipaddr} on port {port}")
        return True
    else:
        return False


server("192.56.1.10")