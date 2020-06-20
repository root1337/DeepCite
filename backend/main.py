from flask import Flask, jsonify
from flask import request
import json
from tree import Tree
from controller import Claim, html_link, new_indention
import exceptions as errors
app = Flask(__name__)


exceptions = [errors.MalformedLink, errors.URLError, errors.EmptyWebsite, errors.ClaimNotInLink, errors.InvalidInput]

@app.route('/api/v1/deep_cite', methods=['GET', 'POST'])
def deep_cite():
# def deep_cite(claim, link):
    content = request.get_json()

    try:
        claim = sanitize_claim(content['claim'])
        link = sanitize_link(content['link'])
    except Exception as e:
        return jsonify({'error': 'Error 505: HTTP Verison Not Supported, hacker' })

    full_pre_json = {'error': 'none'}

    try:
        tree = Tree(link, claim)
        full_pre_json = {'results': tree.get_best_path()}
    # handles exceptions that arise
    except Exception as e:
        if check_instance(e):
            full_pre_json['error'] = str(e)
        else:
            # TODO: this should be better
            link = html_link('https://github.com/connorjoleary/DeepCite/issues')
            full_pre_json['error'] = str('Error 500: Internal Server Error ' + str(e) + "."  + \
                        new_indention("Please add your error to " + link + " with the corresponding claim and link."))
    
    return jsonify(full_pre_json)

def check_instance(e):
    for error in exceptions:
        if isinstance(e, error):
            return True
    return False

# sanitization and stripping of claim
def sanitize_claim(claim):
    sanitized = claim
    badstrings = [';','$','&&','../','<','>','%3C','%3E','\'','--','1,2','\x00','`','(',')','file://','input://', '\n', '\t']
    
    for bad in badstrings:
        if bad in sanitized:
            sanitized = sanitized.replace(bad, '')

    return sanitized.strip()

# sanitization of link
def sanitize_link(link):
    sanitized = link
    badstrings = [';','&&','../','<','>','--','1,2','`','(',')','input://', 'file://']
    
    for bad in badstrings:
        if bad in sanitized:
            sanitized = sanitized.replace(bad, '')

    return sanitized.strip()

if __name__ == "__main__":
    # deep_cite(**{"claim":"6 years after resigning, Nixon testified on behalf of former FBI assistant director Mark Felt at Felts own trial, and gave money to Felts defense fund. In 2005 Felt revealed he had been Deep Throat, Bob Woodwards source while breaking the Watergate scandal that led to Nixons resignation", "link":"https://www.reddit.com/r/todayilearned/comments/6bu1xc/til_nixon_sent_champagne_and_a_note_saying/"})
    app.run(host='0.0.0.0')
