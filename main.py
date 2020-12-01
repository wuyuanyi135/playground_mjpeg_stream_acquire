import os

import aiohttp
from aiohttp import client
import argparse
import asyncio


async def main():
    cnt = 0
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("-q", "--quiet", action="store_true")
    parser.add_argument("-o", "--output", default="./output")
    args = parser.parse_args()
    quiet = args.quiet
    os.makedirs(args.output, exist_ok=True)

    async with client.ClientSession() as session:
        resp = await session.request("get", args.url)
        reader = aiohttp.MultipartReader.from_response(resp)

        while True:
            part = await reader.next()
            if part is None:
                break
            data = await part.read(decode=False)
            with open(os.path.join(args.output, f"{cnt}.jpg"), "wb") as f:
                f.write(data)
            if not quiet:
                print(f"Count = {cnt}; size = {len(data)}")
            cnt += 1


if __name__ == '__main__':
    asyncio.run(main())
