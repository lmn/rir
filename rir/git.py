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

import subprocess
from loader import Config

# --------------------------------------------------------------------------- #
# Shell Helper
# --------------------------------------------------------------------------- #

def run(command, std_in=None, popen_class=subprocess.Popen):
    """
    Command Shell Wrapper
    """
    proccess = popen_class(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE
    )
    if std_in:
        proccess.stdin.write(std_in)
    std_out, std_err = proccess.communicate()
    return_code = proccess.returncode

    return std_out, std_err, return_code

# --------------------------------------------------------------------------- #
# Class Git
# --------------------------------------------------------------------------- #

class Git(Config):
    """ Git Helper """
    def __init__(self):
        pass

    def git_upload_pack_adv(self, org, service):
        """ Get Upload Pack from Repository Refs """
        cmd = "git-upload-pack --stateless-rpc --advertise-refs {}/index".format(
            self.settings['registry'][org]['path']
        )

        git_repo_pack, _err, _rc = run(command=cmd.split())
        result = self.__service_data(service=service)
        result += git_repo_pack.decode()

        return result

    def git_upload_pack(self, org, msg):
        """ Get Upload Pack from Repository """
        cmd = "git-upload-pack --stateless-rpc {}/index".format(
            self.settings['registry'][org]['path']
        )
        result, _err, _rc = run(command=cmd.split(), std_in=msg)
        return result

    def __service_data(self, service):
        """ Generate Payload """
        packet = f'# service={service}\n'
        length = len(packet) + 4
        prefix = "{:04x}".format(length & 0xFFFF)
        result = prefix + packet + '0000'

        return result


# --------------------------------------------------------------------------- #
# END
# --------------------------------------------------------------------------- #

# EOF
