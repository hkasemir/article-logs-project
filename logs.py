#!/usr/bin/python2.7

import psycopg2


def get_most_popular_articles():
    """return top 3 most-read articles with their view counts"""

    connection = psycopg2.connect("dbname=news")
    cursor = connection.cursor()
    cursor.execute("""
      SELECT * FROM article_read_count
      LIMIT 3
    """)
    top_articles = cursor.fetchall()
    cursor.close()
    connection.close()
    return top_articles


def get_most_popular_authors():
    """return authors in order of most page views"""

    connection = psycopg2.connect("dbname=news")
    cursor = connection.cursor()
    cursor.execute("""
      SELECT name, SUM(page_views) AS total_views
      FROM authors, article_read_count, articles
      WHERE articles.author = authors.id
      AND articles.title = article_read_count.title
      GROUP BY name
      ORDER BY total_views DESC
    """)
    author_rank = cursor.fetchall()
    cursor.close()
    connection.close()
    return author_rank


def get_highest_error_days():
    """return day with the highest percentage of errors"""

    connection = psycopg2.connect("dbname=news")
    cursor = connection.cursor()
    cursor.execute("""
        SELECT percent, day
        FROM error_percents
        WHERE percent > 1
        ORDER BY percent DESC
    """)
    author_rank = cursor.fetchall()
    cursor.close()
    connection.close()
    return author_rank


def print_log_stats():
    """
        provide an overview listing of the most popular articles, authors,
        and any days with request error rates higher than 1%
    """
    popular_articles = get_most_popular_articles()
    print('\nArticles with the most views:')
    for title, view_count in popular_articles:
        print('    "%s" - %s views' % (title, view_count))

    popular_authors = get_most_popular_authors()
    print('\nAuthors with the most reads:')
    for author, read_count in popular_authors:
        print('    %s - %s views' % (author, read_count))

    error_days = get_highest_error_days()
    print('\nDays with error rates in page views > 1%')
    for percent, day in error_days:
        print('    %s - %s%% errors' % (day.strftime('%B %d, %Y'), percent))

print_log_stats()
