import os
import sys

# Bug 1: Mutable default argument
def add_user(username, users_list=[]):
    users_list.append(username)
    return users_list

# Bug 2: Resource leak (unclosed file) and division by zero risk
def calculate_ratio_from_file(filename, denominator):
    f = open(filename, "r")
    data = f.read()
    # If denominator is 0, this will crash
    # Also, the file 'f' is never closed if we crash here or finish execution
    ratio = len(data) / denominator
    return ratio

if __name__ == "__main__":
    print(add_user("alice"))
    print(add_user("bob"))  # Will output ['alice', 'bob'] instead of ['bob']
    
    # Division by zero risk
    print(calculate_ratio_from_file("requirements.txt", 0))
