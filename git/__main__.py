from os import environ as env
from git.git import Git

def run():
    git = Git('./test_folder', 'mascanio', env['token'])
    status = git.status()

    print(status)
    print(status.is_clean())

    git.add_all()

    git.commit('master')

    status = git.status()
    print(status)
    print(status.is_clean())

    print(git.get_current_branch())

    # print(git.push('https://github.com/mascanio/test_wrapper.git', git.get_current_branch()))
    print(git.pull('https://github.com/mascanio/test_wrapper.git', 'dev', rebase=True))
    
    status = git.status()
    print(status)
    print(status.is_clean())


if __name__ == "__main__":
    run()
