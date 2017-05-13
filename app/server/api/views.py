from django.http import JsonResponse
from django.forms.models import model_to_dict
import api.models as mdl
from meta import get_schema_instance

import logging
import json
logger = logging.getLogger('django')

# Create your views here.

def db_map_view(request):
    """returns the dbmap loaded on cache"""

    try:
        result = list()
        for scm in mdl.Schema.objects.all():
            r = model_to_dict(scm)

            r['tables'] = list()
            for tbl in scm.table_set.all():
                t_props = dict()
                data = list()
                if len(tbl.tablefield_set.all()) > 0:
                    data = [model_to_dict(tf) for tf in tbl.tablefield_set.all().order_by('-is_primary_key')]
                t_props["fields"] = data
                t = model_to_dict(tbl)
                t["props"] = t_props
                r['tables'].append(t)
            result.append(r)
        return JsonResponse(result, safe=False)
    except Exception as e:
        return JsonResponse({'success': False, 'err': str(e)})


def table_info(request, name=None):
    """Return the metadata of the requested table"""
    
    try:
        if name is None:
            return JsonResponse({'success': False, 'err': "Invalid table name"})

        t = mdl.Table.objects.filter(table_name=name)[0]

        if not t:   
            return JsonResponse({'success': False, 'err': "Table not found"})

        t_props = dict()
        data = list()
        if len(t.tablefield_set.all()) > 0:
            data = [model_to_dict(tf) for tf in t.tablefield_set.all().order_by('-is_primary_key')]
        t_props["fields"] = data
        this_tbl = model_to_dict(t)
        this_tbl["props"] = t_props

        return JsonResponse(this_tbl, safe=False)
    except Exception as e:
        return JsonResponse({'success': False, 'err': str(e)})


def  rebuild_db_map(request):
    """Collect the information of the observed database"""

    CACHE = None
    try:
        #TODO: recieve db and schemas from request? 
        db = "world"
        schemas = ["world"]
        with get_schema_instance("MY_SQL", db, schemas) as s:
            CACHE = s.tables

        mdl.Schema.objects.all().delete()
        log_d = dict()
        for scm in schemas:
            s = mdl.Schema.objects.create(schema_name=scm)
            #s.save()
            #s.refresh_from_db()

            for tbl in [CACHE[t] for t in CACHE if CACHE[t].db_schema==scm]:

                

                t = mdl.Table.objects.create(schema=s, table_name=tbl.name)
                for clm in tbl.columns:
                    d = {
                        'CHARACTER_MAXIMUM_LENGTH': tbl.columns[clm]._meta.CHARACTER_MAXIMUM_LENGTH,
                        'CHARACTER_OCTET_LENGTH': tbl.columns[clm]._meta.CHARACTER_OCTET_LENGTH,
                        'CHARACTER_SET_NAME': tbl.columns[clm]._meta.CHARACTER_SET_NAME,
                        'COLLATION_NAME': tbl.columns[clm]._meta.COLLATION_NAME,
                        'COLUMN_COMMENT': tbl.columns[clm]._meta.COLUMN_COMMENT,
                        'COLUMN_DEFAULT': tbl.columns[clm]._meta.COLUMN_DEFAULT,
                        'COLUMN_KEY': tbl.columns[clm]._meta.COLUMN_KEY,
                        'COLUMN_TYPE': tbl.columns[clm]._meta.COLUMN_TYPE,
                        'DATA_TYPE': tbl.columns[clm]._meta.DATA_TYPE,
                        'DATETIME_PRECISION': tbl.columns[clm]._meta.DATETIME_PRECISION,
                        'EXTRA': tbl.columns[clm]._meta.EXTRA,
                        'GENERATION_EXPRESSION': tbl.columns[clm]._meta.GENERATION_EXPRESSION,
                        'IS_NULLABLE': tbl.columns[clm]._meta.IS_NULLABLE,
                        'NUMERIC_PRECISION': tbl.columns[clm]._meta.NUMERIC_PRECISION,
                        'NUMERIC_SCALE': tbl.columns[clm]._meta.NUMERIC_SCALE,
                        'ORDINAL_POSITION': tbl.columns[clm]._meta.ORDINAL_POSITION,
                        'PRIVILEGES': tbl.columns[clm]._meta.PRIVILEGES
                    }
                    log_d[tbl.name+"."+clm] = d
                    mdl.TableField.objects.create(
                        table=t, 
                        field_name=clm, 
                        inner_type=tbl.columns[clm]._meta.COLUMN_TYPE,
                        allow_null=tbl.columns[clm]._meta.IS_NULLABLE=="YES",
                        is_primary_key= clm in tbl.pk
                    )

        with open('dump.json', 'w') as f:
            f.write(json.dumps(log_d, indent=4))
            
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'err': str(e)})


def tables_with_pks(request):
    """Return a list of the tables with their respective PKs"""

    try:
        result = list()
        for scm in mdl.Schema.objects.all():
            for tbl in scm.table_set.all():
                t = {"Table Name": tbl.table_name}
                t["Primary Keys"] = ", ".join([
                    f.field_name 
                    for f in 
                    tbl.tablefield_set.filter(is_primary_key=True).all()
                ])
                
                result.append(t)
        return JsonResponse(result, safe=False)
    except Exception as e:
        return JsonResponse({'success': False, 'err': str(e)})