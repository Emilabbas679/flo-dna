from sqlalchemy import desc


def get_paginated_results(request, model, serializer, limit, page, search_query, **kwargs):
    query = model.query

    if search_query is not None:
        query = query.filter(search_query)

    if kwargs:
        for k, v in kwargs.items():
            f = {k: v}
            query = query.filter_by(**f)

    results = query.order_by(desc(model.updated)).paginate(page=page, per_page=limit)

    response = {
        'data': serializer.dump(results.items, many=True) or [],
        'total': results.total
    }

    if results.has_next:
        next_num = results.next_num
        response['next'] = {
            'next_page_number': next_num,
            'href': f'{request.base_url}?limit={limit}&page_number={next_num}'
        }

    return response
