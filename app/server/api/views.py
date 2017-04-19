from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import api.models as mdl
from meta import get_schema_instance

# Create your views here.

def db_map_view(request):
    """returns the dbmap loaded on cache"""

    result = list()
    for scm in mdl.Schema.objects.all():
        r = dict()
        r['name'] = scm.schema_name
        r['tables'] = list()
        for tbl in scm.table_set.all():
            r['tables'].append(
                {'name': tbl.table_name}
                )
        result.append(r)
    return JsonResponse(result, safe=False)

def  rebuild_db_map(request):

    CACHE = None
    
    #TODO: recieve db and schemas from request? 
    db = "world"
    schemas = ["world"]
    with get_schema_instance("MY_SQL", db, schemas) as s:
        CACHE = s.tables

    mdl.Schema.objects.all().delete()

    for scm in schemas:
        s = mdl.Schema.objects.create(schema_name=scm)
        #s.save()
        #s.refresh_from_db()

        for tbl in [CACHE[t] for t in CACHE if CACHE[t].db_schema==scm]:
            t = mdl.Table.objects.create(schema=s, table_name=tbl.name)
            #t.save()
    return JsonResponse({'success': True})
        
