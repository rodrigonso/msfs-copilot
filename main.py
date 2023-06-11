import re
import nltk
from PyPDF2 import PdfReader

def read_PDF(file):
    reader = PdfReader(file)
    num_of_pages = len(reader.pages)

    page = reader.pages[0]
    text = page.extract_text()

    # print(text)
    return text


# There's an issue here where some of the checklist sections don't get properly split because they are in the same line as the item. may require manual fixing of this here (review)
def parse_PDF(text):
    result = []

    bullet_point = re.compile(r"\u2022")
    last_title_idx = 0

    lines = text.split('\n')
    curr = []

    regex = "^[A-Z ]*$"
    for idx, line in enumerate(lines):
        if (re.search(bullet_point, line)):
            res = line.strip()
            cleanString = re.sub(bullet_point, '', res)

            test = cleanString

            curr.append(test)   
        else:
            regex = "^[A-Z ]*$"
            test = bool(re.search(regex, line))
            if is_valid_token(line) and test:
                result.append({"name": lines[last_title_idx].strip(), "values": curr})
                last_title_idx = idx
                curr = []

    return result

def is_valid_token(token):
    return token and token.strip()

def is_upper(string):
    return string.isupper() and string.isalpha()

# def tokenize_Text(parsed):

    res = []

    for line in parsed:
        # print(parsed)
        res_line = {"q": "", "a": ""}

        l = 1
        r = 2

        # l = 1, r = 2
        # hey   there
        #   ^&
        has_seen_whitespace = False
        while (r < len(line) or l < r):
            left = line[l]
            right = line[r]

            if (not ' ' in right):
                # print(left, right)
                if has_seen_whitespace:
                    try:
                        res_line['q'] = line[0:(l+2)] # grabs the substring before whitespace
                        res_line['a'] = line[r:len(line)] # grabs the substring after whitespace
                    except:
                        print("soemthing went wrong", l, r)
                    break
                else:
                    l += 1
                    r += 1

            if (not ' ' in left) and (' ' in right):
                r += 1

                regex = "^(?=.*[A-Z])?(?=.*[0-9])?(?=.*[!@#$%^&*()_+])?$"
                curr_line = line[r:len(line)]
                is_of_interest = bool(re.search(r'\d', curr_line)) or is_upper(curr_line)

                print(is_of_interest, curr_line, r-l)
                has_seen_whitespace = (r - l >= 2) if True else False

        res.append(res_line)
        # print(res_line)
    # print(res)

def split_q_and_a(parsed):
    res = []

    for idx, line in enumerate(parsed):
        tokens = nltk.word_tokenize(line)
        
        q = ""
        a = ""

        for tk in tokens:
            regex = "^(?!.*[0-9])(?!.*[A-Z].*[A-Z].*[A-Z]).*$"
            is_q = bool(re.search(regex, tk))
            # print(tk, '-',is_q)
            if is_q:
                q += tk + " "
            else:
                a += tk + " "
        res.append({'q': q.strip(), 'a':a.strip()})
    return res


def rearrenge_tokens(values, section_name):
    res = []

    for idx, item in enumerate(values):
        curr = {'prompt': '', 'completion': ''}

        if idx == 0:
            curr['prompt'] = section_name # ask for title of the current checklist
            curr['completion'] = item['q'] # responds the prompt to the first question
        elif idx == len(values):
            curr['prompt'] = values[idx]['a'] # ask for the last answer of the current checklist
            curr['completion'] = section_name + 'COMPLETED' # responds with checklist completion
        else:
            curr['prompt'] = values[idx -1]['a'] # ask for the last answer we gave
            curr['completion'] = item['q'] # responds with the next checklist item

        res.append(curr)
    return res


def main():
    files = ["./test.pdf", "./test2.pdf", "./test3.pdf", "./test4.pdf", "./test5.pdf"]

    raw_data = read_PDF(files[1])
    reader = PdfReader(files[1])

    raw_data = []
    checklists = []
    total_of_data = 0

    for page in reader.pages:
        raw_data.append(page.extract_text())

    for data in raw_data:
        sections = parse_PDF(data)
        for section in sections:
            formatted = split_q_and_a(section['values'])
            res = rearrenge_tokens(formatted, section['name'])

            checklists.append({'section': section['name'], 'values': res})
            total_of_data += len(res)

    print(total_of_data)

if __name__ == "__main__":
    main()