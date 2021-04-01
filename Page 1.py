from flask import Flask, render_template, Response, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


verhoeff_table_d = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 2, 3, 4, 0, 6, 7, 8, 9, 5),
    (2, 3, 4, 0, 1, 7, 8, 9, 5, 6),
    (3, 4, 0, 1, 2, 8, 9, 5, 6, 7),
    (4, 0, 1, 2, 3, 9, 5, 6, 7, 8),
    (5, 9, 8, 7, 6, 0, 4, 3, 2, 1),
    (6, 5, 9, 8, 7, 1, 0, 4, 3, 2),
    (7, 6, 5, 9, 8, 2, 1, 0, 4, 3),
    (8, 7, 6, 5, 9, 3, 2, 1, 0, 4),
    (9, 8, 7, 6, 5, 4, 3, 2, 1, 0))
verhoeff_table_p = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 5, 7, 6, 2, 8, 3, 0, 9, 4),
    (5, 8, 0, 3, 7, 9, 6, 1, 4, 2),
    (8, 9, 1, 6, 0, 4, 3, 5, 2, 7),
    (9, 4, 5, 3, 1, 2, 6, 8, 7, 0),
    (4, 2, 8, 6, 5, 7, 3, 9, 0, 1),
    (2, 7, 9, 3, 8, 0, 6, 4, 1, 5),
    (7, 0, 4, 6, 9, 1, 3, 2, 5, 8))
verhoeff_table_inv = (0, 4, 3, 2, 1, 5, 6, 7, 8, 9)


def calcsum(number):
    """For a given number returns a Verhoeff checksum digit"""
    c = 0
    for i, item in enumerate(reversed(str(number))):
        c = verhoeff_table_d[c][verhoeff_table_p[(i + 1) % 8][int(item)]]
    return verhoeff_table_inv[c]


def checksum(number):
    """For a given number generates a Verhoeff digit and
    returns number + digit"""
    c = 0
    for i, item in enumerate(reversed(str(number))):
        c = verhoeff_table_d[c][verhoeff_table_p[i % 8][int(item)]]
    return c


def generateVerhoeff(number):
    """For a given number returns number + Verhoeff checksum digit"""
    return "%s%s" % (number, calcsum(number))


def validateVerhoeff(number):
    """Validate Verhoeff checksummed number (checksum is last digit)"""
    return checksum(number) == 0


# Some tests and also usage examples
assert calcsum('75872') == 2
assert checksum('758722') == 0
assert calcsum('12345') == 1
assert checksum('123451') == 0
assert calcsum('142857') == 0
assert checksum('1428570') == 0
assert calcsum('123456789012') == 0
assert checksum('1234567890120') == 0
assert calcsum('8473643095483728456789') == 2
assert checksum('84736430954837284567892') == 0
assert generateVerhoeff('12345') == '123451'
assert validateVerhoeff('123451') == True
assert validateVerhoeff('122451') == False
assert validateVerhoeff('128451') == False


def Aadhaar_number():
    # text = request.form["Aadhaar_raw"]  # Read input data from HTML form
    text = request.form['input']
    text = text.lower()  # Convert the input data to lower case for better results
    all_text = text.split()  # Split the input data in single words
    # print(all_text)
    anum = ''  # Take an empty string
    result = []  # Take an empty list

    if 'aadhaar' in all_text or 'your' in all_text or 'g/male' in all_text:
        # print(all_text)
        res_list = list(filter(lambda x: all_text[x] == 'aadhaar', range(len(all_text))))  # index value of aadhaar
        # print(res_list)
        res_list1 = list(filter(lambda x: all_text[x] == 'your', range(len(all_text))))  # index value of your
        # print(res_list1)
        res_list2 = list(filter(lambda x: all_text[x] == 'g/male', range(len(all_text))))  # index value of g/male
        # print(res_list2)
        res_list1.extend(res_list2)
        # print(res_list1)
        res_list.extend(res_list1)
        res_list = list(set(res_list))  # all the index for aadhaar in one list
        # print('---->', res_list)
        for x in res_list:
            if (all_text[x + 1] == 'no.' and all_text[x + 2] == ':') or (
                    all_text[x + 1] == 'no'):  # checking the text for "no.", ":", "no"

                # if the above condition is satisfied then check the +3 index that must not be equal to your
                if all_text[x + 3] != 'your':
                    if all_text[x + 1] == 'no':
                        anum = all_text[x + 2] + all_text[x + 3] + all_text[x + 4]
                    else:
                        anum = all_text[x + 3] + all_text[x + 4] + all_text[x + 5]
                else:
                    anum = all_text[x + 5] + all_text[x + 6] + all_text[x + 7]
                anum = anum[:12]  # Take only 12 digits from index 0 to 11
                anum = anum.upper()
                anum = list(anum)
                if 'I' in anum:
                    anum[anum.index('I')] = '1'
                if 'Z' in anum:
                    anum[anum.index('Z')] = '2'
                if 'B' in anum:
                    anum[anum.index('B')] = '3'
                if 'O' in anum:
                    anum[anum.index('O')] = '0'
                a = ''
                # print(anum)
                for y in anum:
                    a += y
                # a.join(anum)
                result.append(a)

    else:
        for word in range(len(all_text)):
            if len(all_text[word]) == 4 and all_text[word].isdigit():
                if len(all_text) - word >= 3 and len(all_text[word + 1]) == 4 and len(all_text[word + 2]) == 4:
                    anum = all_text[word] + all_text[word + 1] + all_text[word + 2]
                    word += 3
                    anum = anum[:12]  # Take only 12 digits from index 0 to 11
                    anum = anum.upper()
                    anum = list(anum)
                    if 'I' in anum:
                        anum[anum.index('I')] = '1'
                    if 'Z' in anum:
                        anum[anum.index('Z')] = '2'
                    if 'B' in anum:
                        anum[anum.index('B')] = '3'
                    if 'O' in anum:
                        anum[anum.index('O')] = '0'
                    a = ''
                    # print(anum)
                    for y in anum:
                        a += y
                    # a.join(anum)
                    result.append(a)

    print(result)
    for r in result:
        print(r, ": ", validateVerhoeff(int(r)))
        if not validateVerhoeff(int(r)):
            result.remove(r)

    from collections import Counter  # import Counter for counting the repeated values of aadhaar no.
    # count_aadhaar = Counter(result)

    # Alternate method for counting
    count_aadhaar = {i: result.count(i) for i in result}
    # for key in count_aadhaar:
    #     print(key,count_aadhaar[key])
    print(count_aadhaar)

    return count_aadhaar


@app.route("/data", methods=["POST"])
def FindAadhaar():
    return Aadhaar_number()


app.run(debug=True)
