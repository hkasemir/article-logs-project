# Logs Analysis of a News Site
This project is an exploration of SQL and the wonder of relational databases!
We explore a DB with three tables, `articles`, `authors`, and `log` to find
interesting information about the popularity of articles, and how people are
accessing the site.

### To Run
This project is ideally run in a virtual machine using Vagrant and VirtualBox
with the following [Vagrant configuration](https://github.com/udacity/fullstack-nanodegree-vm)
and [SQL data for the news Database](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip).
To load the data, use the command `psql -d news -f newsdata.sql` when you have
the virtual machine running.

This program uses a few *views* to make the queries a bit simpler, set these up
by adding them via the `psql` terminal connected to the `news` DB in the VM:

## Views
### article_read_count:

```
CREATE VIEW article_read_count AS
SELECT title, COUNT(path) AS page_views
FROM log, articles
WHERE log.path LIKE CONCAT('%', articles.slug)
GROUP BY title
ORDER BY page_views DESC;
```

### error_counts:

```
CREATE VIEW error_counts AS
SELECT count(*) AS error_count, DATE_TRUNC('day', time) AS day
FROM log
WHERE status = '404 NOT FOUND'
GROUP BY day;
```

### ok_counts:

```
CREATE VIEW ok_counts AS
SELECT count(*) AS ok_count, DATE_TRUNC('day', time) AS day
FROM log
WHERE status = '200 OK'
GROUP BY day;
```

### error_percents:

```
CREATE VIEW error_percents AS
SELECT
  ok_count,
  error_count,
  TRUNC(error_count * 100 / TRUNC(ok_count + error_count, 1), 2) AS percent,
  ok_counts.day
FROM ok_counts, error_counts
WHERE ok_counts.day = error_counts.day
ORDER BY percent DESC;
```

## Getting Results
To get a printout of the data in your terminal, open up the vagrant ssh terminal
and run `python logs.py`.

et voila:
```
Articles with the most views:
    "Candidate is jerk, alleges rival" - 338647 views
    "Bears love berries, alleges bear" - 253801 views
    "Bad things gone, say good people" - 170098 views

Authors with the most reads:
    Ursula La Multa - 507594 views
    Rudolf von Treppenwitz - 423457 views
    Anonymous Contributor - 170098 views
    Markoff Chaney - 84557 views

Days with error rates in page views > 1%
    July 17, 2016 - 2.26% errors
```
