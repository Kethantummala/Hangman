import cx_Freeze

executables=[cx_Freeze.Executable("Hangman.py")]

cx_Freeze.setup(
    name="Play Hangman",
    options={"build_exe":{"packages":["pygame","screeninfo"]}},
    executables=executables
    )
