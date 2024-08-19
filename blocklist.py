"""
    This file exclusively houses the blocklist for JWT tokens, intended for importation by 
    the application and the logout resource. This allows for the addition of tokens to the 
    blocklist upon user logout.
"""

BLOCKLIST = set()