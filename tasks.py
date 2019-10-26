#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following disclaimer
#    in the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of the  nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# --------------------------------------------------------------------------- #
# Imports
# --------------------------------------------------------------------------- #

import os
import glob
from invoke import task

from rir.loader import config

# --------------------------------------------------------------------------- #
# Settings
# --------------------------------------------------------------------------- #

PACKAGE_NAME = "rir"
DEPENDENCIES = "deps.txt"

REGISTRY_LOCK = "registry/repository"
REGISTRY_CACHE = "registry/cache"

# --------------------------------------------------------------------------- #
# Tasks
# --------------------------------------------------------------------------- #

@task
def create_cargo_registry(ctx, name):
    """ Create Registry  """
    ctx.run(f"cargo new {REGISTRY_LOCK}/{name}")

@task
def create_cargo_registry_pull(ctx, name):
    """ Create Registry  """
    ctx.run(f"cd {REGISTRY_LOCK}/{name}; git pull")

@task
def clone_repository_indexer(ctx):
    """ Create Registry  """
    for key, value in config['registry'].items():
        if not os.path.isdir(f"{REGISTRY_LOCK}/{key}"):
            ctx.run(f"git clone {value['url']} {REGISTRY_LOCK}/{key}")
        else:
            print(f"Updating {REGISTRY_LOCK}/{key}")
            ctx.run(f"cd {REGISTRY_LOCK}/{key} && git pull")
        create_cargo_generate_cache(ctx, name=key)


@task
def create_cargo_generate_cache(ctx, name):
    """ Create Registry  """
    ctx.run(f"cd  {REGISTRY_LOCK}/{name} && cargo fetch")

    ctx.run(f"cargo local-registry --sync {REGISTRY_LOCK}/{name}/Cargo.lock"
            f" {REGISTRY_CACHE}/{name}")

    ctx.run(f"cd {REGISTRY_CACHE}/{name}/index && git init"
        f"&& curl http://localhost:8080/api/v1/{name}/config > config.json"
        f"&& git add . && git commit -m 'Cache Update'")
@task
def deps(ctx):
    """ Install Dependencies """
    print("Installing Dependencies")
    ctx.run(f"pip3 install -r {DEPENDENCIES}")


@task
def docs(ctx):
    """ Live Documentation """
    print("Building Documentation")
    ctx.run(f"pdoc --http : {PACKAGE_NAME}")

@task
def lint(ctx):
    """ Running Lint """
    print("Lint Testing")
    files = glob.glob('*/**.py')
    ctx.run("pylint {}".format(' '.join(files)))

@task
def bump(ctx):
    """ Git Auto bumper by Branchname """
    branch = ctx.run("git rev-parse --abbrev-ref HEAD")
    if branch is "master":
        ctx.run("bumpversion minor")
    elif branch is "develop":
        ctx.run("bumpversion patch")
    elif branch is "release":
        ctx.run("bumpversion major")

# --------------------------------------------------------------------------- #
# END
# --------------------------------------------------------------------------- #

# EOF
