import sys


def process_option():
    if len(sys.argv) > 1:
        option = sys.argv[1]
        print(f"Processing option: {option}")
    else:
        print("No option provided")


if __name__ == "__main__":
    process_option()
