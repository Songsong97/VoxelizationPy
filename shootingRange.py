import sys

def main():
    # print command line arguments

    s = [i for i in range(6)]

    p = [s[i + 3] - s[i] for i in range(3)]

    print(p)

if __name__ == "__main__":
    main()