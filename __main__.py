from safe import Safe


def main():
    app = Safe(fileName='umbilikus.txt')
    app.mainloop()

if __name__ == "__main__":
    main()
