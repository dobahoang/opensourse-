import asyncio

async def task_coro(value):
  # Simulate work (some may fail)
  if value % 2 == 0:
    raise ValueError(f"Task {value} failed!")
  await asyncio.sleep(value)
  print(f"Task {value} completed")

async def main():
  async with asyncio.TaskGroup() as group:
    # Create tasks (some may fail)
    for i in range(3):
      group.create_task(task_coro(i))

  # Tasks are automatically waited for when exiting the context manager

asyncio.run(main())
