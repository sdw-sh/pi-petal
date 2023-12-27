parser = argparse.ArgumentParser("simple_example")
parser.add_argument(
    "counter", help="An integer will be increased by 1 and printed.", type=int
)
args = parser.parse_args()
print(args.counter + 1)
