from git.git import Git

def run():
    git = Git('./test_folder')
    status = git.status()

    print(status)
    print(status.is_clean())

    git.add_all()

    git.commit('test commit')

    status = git.status()
    print(status)
    print(status.is_clean())

    print(git.get_current_branch())

if __name__ == "__main__":
    run()
