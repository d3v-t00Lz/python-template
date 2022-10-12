# NAME

pytemplate_cli

# SYNOPSIS

**pytemplate_cli** \[-h\] \[-c CONFIG\] {bar,foo,version} \...

# POSITIONAL ARGUMENTS

# COMMAND *\'pytemplate_cli* bar\'

usage: pytemplate_cli bar \[-h\] {baz} \...

A subcommand that does something

# SUBCOMMANDS *\'pytemplate_cli bar\'*

# COMMAND *\'pytemplate_cli* bar baz\'

usage: pytemplate_cli bar baz \[-h\]

It does something

# COMMAND *\'pytemplate_cli* foo\'

usage: pytemplate_cli foo \[-h\] \[-s SOMETHING\] \[-f\] foo

Do the foo thing

**foo**

:   Some required argument, in the format something:something:something

# OPTIONS *\'pytemplate_cli* foo\'

**-s** *SOMETHING*, **\--something** *SOMETHING*

:   Some integer number

**-f**, **\--force**

:   Foo no matter what

# COMMAND *\'pytemplate_cli* version\'

usage: pytemplate_cli version \[-h\]

Show the package version

# OPTIONS

**-c** *CONFIG*, **\--config** *CONFIG*

:   The path to a config file. Default values will be used if it does
    not exist.
