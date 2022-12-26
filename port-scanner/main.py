import asyncio
import time

'''
coroutine to scan a particular host's port - timeout of 3 seconds provided.
'''
async def port_scanner(host, port, timeout=5):                                                    
    coro = asyncio.open_connection(host, port)                                                      
    try:                                                      
        _, writer = await asyncio.wait_for(coro, timeout=timeout)
        writer.close()                                   
        return True                                                                                 
    except asyncio.TimeoutError:                                                                    
        return False

'''
Main coroutine that will call port_scanner coroutine
ports - iterable (range object) of ports to scan
'''
async def main(host, ports):
    print(f"scanning {host}")
    coros = [port_scanner(host, port) for port in ports]
    results = await asyncio.gather(*coros)
    for port, result in zip(ports, results):
        if result:
            print(f"{host}:{port} [OPEN]")

host = "python.org"
ports = range(443,444)

asyncio.run(main(host, ports))