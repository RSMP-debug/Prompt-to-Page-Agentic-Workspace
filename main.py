import argparse
import sys
import traceback

from agent.graph import agent


def main():
    parser = argparse.ArgumentParser(
        description="AI Software Engineer"
    )

    parser.add_argument(
        "--recursion-limit",
        "-r",
        type=int,
        default=100
    )

    args = parser.parse_args()

    try:
        user_prompt = input("Enter your project prompt: ").strip()

        result = agent.invoke(
            {"user_prompt": user_prompt},
            {"recursion_limit": args.recursion_limit}
        )

        print("\nGenerated Files:")

        generated_files = result.get("generated_files", {})

        for file_name in generated_files:
            print(f"✓ {file_name}")

        print("\nProject saved in generated_project/")

    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(0)

    except Exception:
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()