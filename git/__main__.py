from os import environ as env
import git

def run():
    git = git.Git('./test_folder', 'https://github.com/mascanio/test-priv.git', 'mascanio', env['token'])
    status = git.status()

    print(status)
    print(status.is_clean())

    git.add_all()

    git.commit('master')

    status = git.status()
    print(status)
    print(status.is_clean())

    print(git.get_current_branch())

    # print(git.push(git.get_current_branch()))
    # print(git.pull('dev', rebase=True))
    git.rebase_stash('master')

    status = git.status()
    print(status)
    print(status.is_clean())


if __name__ == "__main__":
    run()
