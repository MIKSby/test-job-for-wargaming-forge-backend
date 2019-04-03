from collections import Counter
from statistics import mean, median

from cats_database import CatsDatabase


db = CatsDatabase(auth='dbname=wg_forge_db user=wg_forge '
                       'password=42a host=localhost port=5432')
cats = db.get_cats()

tails = [cat[2] for cat in cats]
whiskers = [cat[3] for cat in cats]


def calc_length_mean(data):
    return round(mean(data), 1)


def calc_length_median(data):
    return round(median(data), 1)


def calc_length_mode(data):
    return str({i[0] for i in Counter(data).most_common(2)})


db.execute('''INSERT INTO public.cats_stat(tail_length_mean, tail_length_median,
           tail_length_mode, whiskers_length_mean, whiskers_length_median,
           whiskers_length_mode) VALUES (%s, %s, %s, %s, %s, %s)''',
           (calc_length_mean(tails), calc_length_median(tails),
            calc_length_mode(tails), calc_length_mean(whiskers),
            calc_length_median(whiskers), calc_length_mode(whiskers)))
