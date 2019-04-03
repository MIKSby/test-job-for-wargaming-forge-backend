from cats_database import CatsDatabase


db = CatsDatabase(auth='dbname=wg_forge_db user=wg_forge '
                       'password=42a host=localhost port=5432')
colors = {}

for cat in db.get_cats():
    if cat[1] in colors:
        colors[cat[1]] += 1
    else:
        colors[cat[1]] = 1

for i in colors.keys():
    db.execute('INSERT INTO public.cat_colors_info(color, count) '
               'VALUES(%s, %s);', (i, colors[i]))
