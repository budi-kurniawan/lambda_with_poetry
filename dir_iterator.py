from os import listdir
from os.path import isfile, join
import os
import asyncio
import aiofiles

class DirIterator():
    def __init__(self, mypath):
        self.files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        self.count = 0
        self.mypath = mypath

    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.count >= len(self.files):
            raise StopAsyncIteration
        file = join(self.mypath, self.files[self.count])
        content = None
        # async with aiofiles.open('filename', mode='r') as f:
        async with aiofiles.open(file, mode="r") as f:
            content = await f.read()
        self.count += 1
        return content

async def main():
    path = '__pycache__'
    path = 'test_dir'
    # path = '.'
    dir_iterator = DirIterator(path)
    async for f in dir_iterator:
        print(f)
        print("=============================")

if __name__ == '__main__':
    asyncio.run(main())
