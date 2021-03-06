#!/usr/bin/python

# This script reformats each file supplied on the command line according to
# the Google Java style (by calling out to the google-java-format program,
# https://github.com/google/google-java-format), but with improvements to
# the formatting of annotations in comments.

from __future__ import print_function
from distutils import spawn
import filecmp
import os
import stat
import subprocess
import sys
import tempfile

try:
    from urllib import urlretrieve  # python 2
except ImportError:
    from urllib.request import urlretrieve  # python 3

debug = False
# debug = True

script_dir = os.path.dirname(os.path.abspath(__file__))
# Rather than calling out to the shell, it would be better to
# call directly in Python.
fixup_py = os.path.join(script_dir, "fixup-google-java-format.py")

## To use an officially released version.
# Version 1.3 and earlier do not wrap line comments.
gjf_version = os.getenv("GJF_VERSION", "1.6")
gjf_snapshot = os.getenv("GJF_SNAPSHOT", "")
gjf_url_base = os.getenv("GJF_URL_BASE",
                         "https://github.com/google/google-java-format/releases/download/google-java-format-" + gjf_version + "/")
## To use a non-official version by default, because an official version is
## unusably buggy (like 1.1) or no new release has been made in a long time.
## Never change the file at a URL; make it unique by adding a date.
# gjf_version = "1.5"
# gjf_snapshot = "-SNAPSHOT-20171012"
# gjf_url_base = "http://types.cs.washington.edu/"
# gjf_url_base = "http://homes.cs.washington.edu/~mernst/tmp2/"

gjf_jar_name = "google-java-format-" + gjf_version + gjf_snapshot + "-all-deps.jar"
gjf_url = gjf_url_base + gjf_jar_name

# Set gjf_jar_path, or retrieve it if it doesn't appear locally. Does not update
# from remove path if remote is newer, so never change files on the server.
if os.path.isfile(os.path.join(script_dir, gjf_jar_name)):
    gjf_jar_path = os.path.join(script_dir, gjf_jar_name)
elif os.path.isfile(os.path.join(os.path.dirname(script_dir), "lib", gjf_jar_name)):
    gjf_jar_path = os.path.join(os.path.dirname(script_dir), "lib", gjf_jar_name)
else:
    gjf_jar_path = os.path.join(script_dir, gjf_jar_name)
    # print("retrieving " + gjf_url + " to " + gjf_jar_path)
    urlretrieve(gjf_url, gjf_jar_path)


# For some reason, the "git ls-files" must be run from the root.
# (I can run "git ls-files" from the command line in any directory.)
def under_git(dir, filename):
    """Return true if filename in dir is under git control."""
    if not spawn.find_executable("git"):
        if debug:
            print("no git executable found")
        return False
    FNULL = open(os.devnull, 'w')
    p = subprocess.Popen(["git", "ls-files", filename, "--error-unmatch"], cwd=dir, stdout=FNULL,
                         stderr=subprocess.STDOUT)
    p.wait()
    if debug:
        print("p.returncode", p.returncode)
    return p.returncode == 0


if debug:
    print("script_dir:", script_dir)
    print("fixup_py: ", fixup_py)
    print("gjf_jar_path: ", gjf_jar_path)

files = sys.argv[1:]
if len(files) == 0:
    print("run-google-java-format.py expects 1 or more filenames as arguments")
    sys.exit(1)

result = subprocess.call(["java", "-jar", gjf_jar_path, "--replace"] + files)
## This if statement used to be commented out, because google-java-format
## crashed a lot.  It seems more stable now.
# Don't stop if there was an error, because google-java-format won't munge
# files and we still want to run fixup-google-java-format.py.
if result != 0:
    print("Error when running google-java-format")
    sys.exit(result)

# Remove command-line arguments
files = [f for f in files if not f.startswith("-")]
# Exit if no files were supplied (maybe "--help" was supplied)
if not files:
    sys.exit(0)

if debug: print("Running fixup-google-java-format.py")
result = subprocess.call([fixup_py] + files)
if result != 0:
    print("Error when running fixup-google-java-format.py")
    sys.exit(result)
