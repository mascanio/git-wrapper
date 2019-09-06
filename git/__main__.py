from git.git import Git

def run():
    git = Git('.')
    status = git.status()

    print(status)
    print(status.is_clean())

if __name__ == "__main__":
    run()
