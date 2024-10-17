import asyncio

async def blackjack_task(var_name, conditions):
    await asyncio.sleep(1)  # Simulate a delay
    print(f"Evaluating {var_name} with conditions {conditions}")
    logic_handler.blackjack(var_name, conditions)

async def main():
    tasks = [
        blackjack_task("x", ["greater 10", "less 21", "divisible 3"]),
        blackjack_task("y", ["greater 2", "divisible 2"]),
        blackjack_task("z", ["greater 5", "divisible 1"])
    ]
    await asyncio.gather(*tasks)

asyncio.run(main())
