from django.db import connection
from django.shortcuts import redirect, render

from connect import dictfetchall, is_logged_in


def bolo_list(request):
    if not is_logged_in(request):
        return redirect('admin_login')

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                w.warrant_id,
                w.issue_date,
                c.criminal_id,
                c.name,
                c.age,
                c.gender,
                c.physical_description,
                c.sector_name,
                c.current_status,
                c.jail_name,
                c.jail_number,
                c.bounty_amount,
                c.is_repeat_offender
            FROM warrants_warrant w
            JOIN criminals_criminal c ON w.criminal_id = c.criminal_id
            WHERE
                w.status = 'Active'
                AND c.current_status <> 'IN_JAIL'
            ORDER BY
                c.bounty_amount DESC,
                c.is_repeat_offender DESC,
                w.issue_date DESC
            LIMIT 10
            """
        )
        bolos = dictfetchall(cursor)

        cursor.execute(
            """
            SELECT
                c.sector_name,
                COUNT(*) AS total
            FROM warrants_warrant w
            JOIN criminals_criminal c ON w.criminal_id = c.criminal_id
            WHERE
                w.status = 'Active'
                AND c.current_status <> 'IN_JAIL'
            GROUP BY c.sector_name
            ORDER BY total DESC, c.sector_name
            """
        )
        raw_sector_counts = dictfetchall(cursor)

    sector_palette = [
        '#c0392b',
        '#b45309',
        '#0f766e',
        '#2563eb',
        '#7c3aed',
        '#be123c',
        '#15803d',
        '#0891b2',
        '#9333ea',
        '#d97706',
        '#475569',
    ]

    max_count = max((row['total'] for row in raw_sector_counts), default=1)
    sector_graph = [
        {
            'key': row['sector_name'] or 'Unassigned',
            'label': row['sector_name'] or 'Unassigned',
            'count': row['total'],
            'width_percent': int((row['total'] / max_count) * 100) if max_count else 0,
            'color': sector_palette[index % len(sector_palette)],
        }
        for index, row in enumerate(raw_sector_counts)
    ]
    top_sector = sector_graph[0] if sector_graph else None
    total_on_lookout = sum(item['count'] for item in sector_graph)

    return render(request, 'warrants/bolo_list.html', {
        'bolos': bolos,
        'sector_graph': sector_graph,
        'total_bolos': total_on_lookout,
        'sector_count': len(sector_graph),
        'top_sector_name': top_sector['label'] if top_sector else 'N/A',
        'top_sector_total': top_sector['count'] if top_sector else 0,
    })
