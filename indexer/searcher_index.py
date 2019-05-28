from indexer.db_manager import dbManager
import time


current_milli_time = lambda: int(round(time.time() * 1000))


def search_db(word):
    result = dbManager.find_word(word.lower())
    return result


def search(query):
    # time it
    millis = current_milli_time()

    terms = query.split(" ")
    results = []
    for word in terms:
        results.extend(search_db(word))

    # sort by freq
    results.sort(key=lambda x: x[2], reverse=True)

    # time it
    time_needed = current_milli_time() - millis

    # print the thing
    print("Results for query: \"" + query + "\"")
    print("Found results in " + str(time_needed) + " ms. \n")
    print("Displaying top 10:\n")
    print("  Frequencies".ljust(16, " ") + "|" + "  Document".ljust(80, " ") + "|" + "  Snippet")
    print("".ljust(16, "-") + "|" + "".ljust(80, "-") + "|" + "".ljust(80, "-"))

    for result in results[:10]:
        print(("  " + str(result[2])).ljust(16, " ") + "|" + ("  " + result[1]).ljust(80, " ") + "|  " +  result[4].replace("\n", "    . . .    "))


search("sistem spot")
