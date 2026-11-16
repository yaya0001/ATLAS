from app.agent import create_agent


def main() -> None:
    task = input("Enter your prompt: ").strip()
    if not task:
        print("Please enter a prompt.")
        return

    state = create_agent().run(task)
    if state.status == "completed":
        print(f"\nATLAS: {state}")
    else:
        print(f"\nATLAS stopped with status: {state.status}.")


if __name__ == "__main__":
    main()