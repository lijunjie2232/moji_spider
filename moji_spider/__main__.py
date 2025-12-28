"""
Module allowing the package to be run with 'python -m moji_spider'
"""

from .main import main

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
