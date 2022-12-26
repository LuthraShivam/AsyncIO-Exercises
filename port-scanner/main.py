import asyncio

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

async def scanner(host, queue):
    while True:
        port = await queue.get()
        if not port:
            await queue.put(None)
            break
        if await port_scanner(host, port):
            print(f"{host}:{port} [OPEN]")
        queue.task_done()
'''
Main coroutine that will call port_scanner coroutine
ports - iterable (range object) of ports to scan
'''
async def main(host, ports, limit=500):
    print(f"scanning {host}")

    task_queue = asyncio.Queue()

    workers = [asyncio.create_task(scanner(host, task_queue)) for _ in range(limit)]

    for port in ports:
        await task_queue.put(port)
    
    await task_queue.join()

    await task_queue.put(None)

host = "python.org"
ports = range(1,500)

asyncio.run(main(host, ports))