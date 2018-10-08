## Pre-commit hook test
Check java code formatting before commit - use of java google formatter as pre-commit hook.

Rules: https://google.github.io/styleguide/javaguide.html

## How to
The hooks are all stored in the hooks subdirectory of the Git directory. In most projects, that’s .git/hooks.
Because .git/ is managed locally there is a need to set pre-commit hook by each user locally - could be replaced by script.

Execute:

    cp .run-google-java-format/pre-commit .git/hooks/
    chmod +x .git/hooks/pre-commit