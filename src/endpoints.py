import json
import time

from flask import Flask, request, send_file
from flask_cors import CORS
from nlp_rake import Rake

from linkedin_test import Scraper
from text_classifier import NLPFilter

app = Flask(__name__,)
CORS(app)


@app.route('/')
def ok():
    return 'Ok'


@app.route("/getMindmap", methods=["POST"])
def get_mindmap():
    url = request.args.get('url')
    print(url)
    sections = ["About", "Activity", "Experience", "Education", "Volunteer experience", "Skills & endorsements",
                "Recommendations", "Accomplishments", "Interests", "Licenses & certifications"]
    # sections = ["About", "Experience", "Skills & endorsements", "Recommendations", "Accomplishments", "Interests"]
    scraper = Scraper(url)
    text_en = scraper.get_profile_data(sections)
    person_name = scraper.get_person_name()

    rake = Rake(min_chars=2, max_words=2)
    keywords = rake.apply(text_en)

    # for keyword in keywords:
    #     print(keyword)

    categories = NLPFilter().get_categories_names()
    predictions = NLPFilter().get_categories([key[0] for key in keywords])
    print(predictions)
    keywords_by_category = [[category, [pred[0] for pred in predictions if pred[1] == category and " " in pred[0]]] for
                            category in categories if category != "Other"]
    keywords_by_category.sort(key=lambda x: len(x[1]), reverse=True)

    # for prediction in predictions:
    #     print(prediction)

    print(person_name)
    categories_for_tree = []
    for i in range(len(keywords_by_category)):
        category = keywords_by_category[i]
        print(category[0], "(", len(category[1]), ")")
        number_of_results = int(len(category[1]) * 0.2)
        print("Showing", number_of_results, "results")
        if number_of_results != 0:
            keywords_for_category = []
            for j in range(0, number_of_results):
                keyword = category[1][j]
                print("\t" + keyword)
                keywords_for_category.append({"id": category[0].lower() + str(j), "topic": keyword})
            categories_for_tree.append({
                "id": category[0].lower(),
                "topic": category[0],
                "direction": "left" if i % 2 == 0 else "right",
                "children": keywords_for_category
            })
            print(categories_for_tree[-1])

    mind_map = {
        "meta": {
            "name": "jsMind remote",
            "author": "hizzgdev@163.com",
            "version": "0.2"
        },
        "format": "node_tree",
        "data": {
            "id": "root",
            "topic": person_name,
            "children": categories_for_tree
        }
    }

    mind_map = "var mind = " + json.dumps(mind_map) + ";"

    with open('../site/initialize_mindmap.js', 'w', encoding="utf8") as file:
        file.write(mind_map)

    return send_file('../site/initialize_mindmap.js', mimetype='text/javascript')


@app.route("/getIcebreakersLinkedin", methods=["GET"])
def get_tree_breakers():
    url = request.headers.get('url')
    print(url)
    scraper = Scraper(url)
    sections = ["About", "Activity", "Experience", "Education", "Volunteer experience", "Skills & endorsements",
                "Recommendations", "Accomplishments", "Interests", "Licenses & certifications"]
    text_en = scraper.get_profile_data(sections)
    person_name = scraper.get_person_name()
    print(person_name)
    #
    # rake = Rake(min_chars=2, max_words=2)
    # keywords = rake.apply(text_en)
    #
    # # for keyword in keywords:
    # #     print(keyword)
    #
    # categories = NLPFilter().get_categories_names()
    # predictions = NLPFilter().get_categories([key[0] for key in keywords])
    # print(predictions)
    # keywords_by_category = [[category, [pred[0] for pred in predictions if pred[1] == category and " " in pred[0]]] for
    #                         category in categories if category != "Other"]
    # keywords_by_category.sort(key=lambda x: len(x[1]), reverse=True)
    #
    # # for prediction in predictions:
    # #     print(prediction)
    #
    # categories_for_tree = []
    # for i in range(len(keywords_by_category)):
    #     category = keywords_by_category[i]
    #     print(category[0], "(", len(category[1]), ")")
    #     number_of_results = int(len(category[1]) * 0.2)
    #     print("Showing", number_of_results, "results")
    #     if number_of_results != 0:
    #         keywords_for_category = []
    #         for j in range(0, number_of_results):
    #             keyword = category[1][j]
    #             print("\t" + keyword)
    #             keywords_for_category.append({"id": category[0].lower() + str(j), "topic": keyword})
    #         categories_for_tree.append({
    #             "id": category[0].lower(),
    #             "topic": category[0],
    #             "direction": "left" if i % 2 == 0 else "right",
    #             "children": keywords_for_category
    #         })
    #         print(categories_for_tree[-1])

    breakers = {"data": [{"title": "Common Connections", "icebreakers": scraper.make_breakers_common_connections()},
                         {"title": "Work Experience", "icebreakers": scraper.make_breakers_experience()},
                         {"title": "Volunteering Experience",
                          "icebreakers": scraper.make_breakers_volunteering_experience()}]}

    return breakers


@app.route("/getNews", methods=["GET"])
def get_news():
    url = request.headers.get('url')
    print(url)
    scraper = Scraper(url)
    scraper.login()
    scraper.go_to_page(url)
    company_name = scraper.get_person_role()
    if len(company_name.split('at ')) > 1:
        company_name = company_name.split('at ')[1]
    print(company_name)
    scraper.go_to_page("https://www.google.com/")
    return {"data": scraper.search_news(company_name)}


@app.route("/getFunFacts", methods=["GET"])
def get_fun_facts():
    url = request.headers.get('url')
    print(url)
    # scraper = Scraper(url)
    #
    # scraper.login()
    # scraper.go_to_page(url)
    # person_name = scraper.get_person_name()
    # person_title = scraper.get_person_role()
    # person_role = scraper.get_person_role().split(" at ")[0]
    # print(person_name, person_title, person_role, sep="\t;\t")
    scraper = Scraper(url)
    lines = open("fun_facts_categories.csv", "r", encoding="utf-8").readlines()
    categories = [l.split(",")[0].lower() for l in lines[1:]]
    categories_words = [l.split(",")[1].lower() for l in lines[1:]]
    facts_links = [l.split(",")[2].lower() for l in lines[1:]]
    classifier = NLPFilter(True, 0.15, categories, categories_words, 1)
    scraper.login()
    links = scraper.get_profile_links()
    to_return = []
    for link in links:
        try:
            print(link)
            scraper.go_to_page(link)
            person_name = scraper.get_person_name()
            person_title = scraper.get_person_role()
            # person_role = scraper.get_person_role()
            person_role = scraper.get_person_role().split(" at ")[0]
            index = categories.index(classifier.get_category(person_role.lower())[1])
            scraper.go_to_page(facts_links[index])
            scraper.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(2)
            fun_fact = \
                str(scraper.driver.find_element_by_xpath("//div[contains(@class,'title')]/../h2").text).split(' (')[0]
            print(fun_fact)
            to_return.append({"name": str(person_name), "title": str(person_title), "category": str(
                classifier.get_category(person_role.lower())[1]), "fact": fun_fact})
        except:
            pass

    facts = {"data": to_return}

    return facts


if __name__ == '__main__':
    app.run(port=8000)
