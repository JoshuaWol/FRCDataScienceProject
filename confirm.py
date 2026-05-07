def confirm(prompt:str = "Continue? [y/n]"):
    while True:
        answer = input(f"{prompt} [y/n]:").strip().lower()
        if answer in ('y', 'yes'):
            return True
        if answer in ("n", "no"):
            return False
        print("Please anser with either y or n to continue.")