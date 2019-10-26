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

from bottle import Bottle, response, request, view

# Local
from git import Git

# Version
VERSION = 1

# --------------------------------------------------------------------------- #
# API Version 1
# --------------------------------------------------------------------------- #

app = Bottle()
git = Git()

# --------------------------------------------------------------------------- #
# Routes
# --------------------------------------------------------------------------- #

@app.get('/<org>/cargo')
@view('cargo')
def config(org):
    """ Get Configuration for Cargo """
    host = request.urlparts
    return dict(org=org, host=host)

@app.get('/<org>/config')
def repo(org):
    """ Get Configuration for Private Repository """
    host = request.urlparts
    dl = f"{host.scheme}://{host.netloc}/download/{org}/crates"
    api = f"{host.scheme}://{host.netloc}/api/v1/{org}"
    return dict(dl=dl, api=api)

@app.get('/<org>/info/refs')
def index(org):
    """ Get access git Refs"""
    service = request.query.service
    response.content_type = "application/x-git-upload-pack-advertisement"
    return git.git_upload_pack_adv(org, service)


@app.post('/<org>/git-upload-pack')
def git_upload_pack(org):
    """ Git Send Pack """
    response.content_type = "application/x-git-upload-pack-result"
    return git.git_upload_pack(org=org, msg=request.body.read())


@app.get('/status')
def status():
    """ Status API and Current Version """
    return dict(status='up', version=VERSION)

# --------------------------------------------------------------------------- #
# END
# --------------------------------------------------------------------------- #

# EOF
