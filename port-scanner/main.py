import asyncio

'''
coroutine to scan a particular host's port - timeout of 3 seconds provided.
'''
async def port_scanner(host, port, timeout=5):                                                    
    coro = asyncio.open_connection(host, port)                                                      
    try:
        _, writer = await asyncio.wait_for(coro, timeout=timeout)
        writer.close()
        return True, port
    except asyncio.TimeoutError:
        return False, port

'''
Main coroutine that will call port_scanner coroutine
ports - iterable (range object) of ports to scan
'''
async def main(host, ports):
    print(f"scanning {host}")
    coros = [port_scanner(host, port) for port in ports]
    '''
    When scanning an entire port range, we will hit the problem where we cross the limit of number of files opened in out OS (check ulimit -n).
    You can either increase this limit, or process these coroutines in batches. Either option works.
    Batching will be a little slower but will take care of larger number of ports that can't be taken care of in one shot.
    '''
    # asyncio.gather for getting all results before proceeding
    # results = await asyncio.gather(*coros)
    # for port, result in zip(ports, results):
    #     if result:
    #         print(f"{host}:{port} [OPEN]")

    # asyncio.as_completed for reacting to coroutines as and when they're completed
    # here timeout is not necessary
    for coro in asyncio.as_completed(coros):
        result, port = await coro
        if result:
            print(f"{host}:{port} [OPEN]")

host = "python.org"
ports = range(400,500)

asyncio.run(main(host, ports))