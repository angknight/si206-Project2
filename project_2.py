# Your name: Angelina Knight
# Your student id: 41683569
# Your email: angiemk@umich.edu
# List who you worked with on this homework:

from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of book titles (as printed on the Goodreads website) 
    in the format given below. Make sure to strip() any newlines from the book titles.

    ['Book title 1', 'Book title 2'...]
    """
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), filename), "r") as file_content:
        file_string = file_content.read()
    soup = BeautifulSoup(file_string, "lxml")
    titles_list = []
    items = soup.find_all("a", class_="bookTitle")
    for item in items:
        titles_list.append(item.text.strip())
    return titles_list


def get_new_releases():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/genres/fantasy". Parse through the object and return a list of URLs for each
    of the books in the "NEW RELEASES TAGGED 'FANTASY'" section using the following format:

    ['https://www.goodreads.com/book/show/23106013-battle-ground', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and discard the rest.
    """
    url = "https://www.goodreads.com/genres/fantasy"
    content = requests.get(url)
    new_releases = []
    soup = BeautifulSoup(content.text, "lxml")
    table = soup.find("div", class_="bigBoxBody")
    tags = table.find_all("a")
    for tag in tags:
        href = tag["href"]
        if href.startswith("/book/show/"):
            new_releases.append(f"https://www.goodreads.com{href}")
    return new_releases


def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and star-rating. 
    This function should return a tuple in the following format:

    ('Some book title', 'the book's author', 'its star rating')

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and star rating.
    """
    info = requests.get(book_url)
    soup = BeautifulSoup(info.text, "lxml")
    title = soup.find("h1", class_="gr-h1 gr-h1--serif").text.strip()
    author = soup.find("a", class_="authorName").text
    rating = float(soup.find("span", itemprop="ratingValue").text.strip())
    return (title, author, rating)


def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2019"
    page in "best_books.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2019, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2019") 
    to your list of tuples.
    """
    root_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
    filename = os.path.join(root_path, filepath)
    with open(filename, "r") as file_content:
        file_string = file_content.read()
    
    soup = BeautifulSoup(file_string, "lxml")
    category_list = []
    content = soup.find_all("h4")
    for category in content:
        category_list.append(category.text.strip())

    title_list = []
    for div in soup.find_all('div', 'category__winnerImageContainer'):
        for img in div.find_all("img", alt=True):
            title_list.append(img["alt"])
    
    url_list = []
    urls = soup.find_all("div", "category clearFix")
    for url in urls:
        url_list.append(url.find("a")["href"])

    tup_list = []
    for category,title,url in zip(category_list, title_list, url_list):
        tup = (category, title, url)
        tup_list.append(tup)
    return tup_list


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by summarize_best_books()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Category", "Book title", and
    "URL", respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Category,Book title,URL
    Some category,Book1,url1
    Another category,Book2,url2
    Yet another category,Book3,url3

    This function should not return anything.
    """
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), filename), "w") as csv_content:
        csv_file = csv.writer(csv_content, delimiter=",")
        csv_file.writerow(["Category", "Book title", "URL"])
        for tup in data:
            csv_file.writerow(tup)

def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

class TestCases(unittest.TestCase):

    # call get_new_releases() and save it to a static variable: new_release_urls
    new_release_urls = get_new_releases()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        titles = get_titles_from_search_results("search_results.htm")
        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(titles), 20)
        # check that the variable you saved after calling the function is a list
        self.assertIsInstance(titles, list)
        # check that each title in the list is a string
        for title in titles:
            self.assertIsInstance(title, str)
        # check that the first title is correct (open search_results.htm and find it)
        self.assertEqual(titles[0],'Harry Potter and the Deathly Hallows (Harry Potter, #7)')
        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(titles[-1],'Harry Potter: The Prequel (Harry Potter, #0.5)')

    def test_get_new_releases(self):
        # check that TestCases.new_release_urls is a list
        self.assertIsInstance(TestCases.new_release_urls, list)
        # check that the length of TestCases.new_release_urls is correct (15 URLs)
        self.assertEqual(len(TestCases.new_release_urls), 15)
        # check that each URL in the TestCases.new_release_urls is a string
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        for url in TestCases.new_release_urls:
            self.assertIsInstance(url, str)
            self.assertTrue("https://www.goodreads.com/book/show/" in url)

    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        # for each URL in TestCases.new_release_urls
        summaries = []
        for url in TestCases.new_release_urls:
            #if url != 'https://www.goodreads.com/book/show/49247242-ring-shout':
            summaries.append(get_book_summary(url))
        # check that the number of book summaries is correct (15)
        self.assertEqual(len(summaries), 15)
            # check that each item in the list is a tuple
        for summary in summaries:
            self.assertIsInstance(summary, tuple)
            # check that each tuple has 3 elements
            self.assertEqual(len(summary), 3)
            # check that the first two elements in the tuple are string
            self.assertIsInstance(summary[0], str)
            self.assertIsInstance(summary[1], str)
            # check that the third element in the tuple, i.e. star-rating is a float
            self.assertIsInstance(summary[2], float)

    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        best_book_sums = summarize_best_books("best_books.htm")
        # check that we have the right number of best books (20)
        self.assertEqual(len(best_book_sums), 20)
            # assert each item in the list of best books is a tuple
        for tup in best_book_sums:
            self.assertIsInstance(tup, tuple)
            # check that each tuple has a length of 3
            self.assertEqual(len(tup), 3)
        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Testaments (The Handmaid's Tale, #2)", 'https://www.goodreads.com/choiceawards/best-fiction-books-2019'
        self.assertEqual(best_book_sums[0][0],'Fiction')
        self.assertEqual(best_book_sums[0][1],"The Testaments (The Handmaid's Tale, #2)")
        self.assertEqual(best_book_sums[0][2],'https://www.goodreads.com/choiceawards/best-fiction-books-2019')
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'A Beautiful Day in the Neighborhood: The Poetry of Mister Rogers', 'https://www.goodreads.com/choiceawards/best-picture-books-2019'
        self.assertEqual(best_book_sums[-1][0],'Picture Books')
        self.assertEqual(best_book_sums[-1][1],'A Beautiful Day in the Neighborhood: The Poetry of Mister Rogers')
        self.assertEqual(best_book_sums[-1][2],'https://www.goodreads.com/choiceawards/best-picture-books-2019')

    def test_write_csv(self):
        # call summarize_best_books on best_books.htm and save the result to a variable
        best_books = summarize_best_books("best_books.htm")
        # call write csv on the variable you saved
        write_csv(best_books, "test.csv")
        
        lst = []
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "test.csv"), "r") as testerfile:
            csv_reader = csv.reader(testerfile)
        # read in the csv that you wrote
            for elem in csv_reader:
                lst.append(elem)
        # check that there are 21 lines in the csv
        self.assertEqual(len(lst), 21)
        # check that the header row is correct
        self.assertEqual(lst[0], ["Category", "Book title", "URL"])
        # check that the next row is 'Fiction', "The Testaments (The Handmaid's Tale, #2)", 'https://www.goodreads.com/choiceawards/best-fiction-books-2019'
        self.assertEqual(lst[1], ["Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2019"])
        # check that the last row is 'Picture Books', 'A Beautiful Day in the Neighborhood: The Poetry of Mister Rogers', 'https://www.goodreads.com/choiceawards/best-picture-books-2019'
        self.assertEqual(lst[-1], ["Picture Books", "A Beautiful Day in the Neighborhood: The Poetry of Mister Rogers", "https://www.goodreads.com/choiceawards/best-picture-books-2019"])


if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)

