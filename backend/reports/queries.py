from django.db import connection


def _fetchall_as_dict(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def task_summary_report(region_id=None, days=30):
    sql = """
        SELECT
            COALESCE(r.name, 'Unassigned') AS region,
            t.priority,
            t.status,
            COUNT(t.id) AS task_count,
            SUM(
                CASE WHEN t.due_date < CURRENT_DATE
                          AND t.status NOT IN ('completed', 'cancelled')
                     THEN 1 ELSE 0 END
            ) AS overdue_count
        FROM tasks_task t
        LEFT JOIN users_region r ON t.region_id = r.id
        WHERE t.created_at >= NOW() - INTERVAL '{days} days'
          AND (%(region_id)s::int IS NULL OR t.region_id = %(region_id)s::int)
        GROUP BY r.name, t.priority, t.status
        ORDER BY r.name, t.priority, t.status;
    """.format(days=int(days))
    with connection.cursor() as cursor:
        cursor.execute(sql, {'region_id': region_id})
        return _fetchall_as_dict(cursor)


def agent_performance_report(region_id=None, team_id=None):
    sql = """
        SELECT
            u.id AS agent_id,
            u.username,
            u.first_name || ' ' || u.last_name AS full_name,
            tm.name AS team,
            rg.name AS region,
            COUNT(DISTINCT t.id) AS total_tasks_assigned,
            COUNT(DISTINCT CASE WHEN t.status = 'completed' THEN t.id END) AS tasks_completed,
            ROUND(
                COUNT(DISTINCT CASE WHEN t.status = 'completed' THEN t.id END)
                * 100.0 / NULLIF(COUNT(DISTINCT t.id), 0), 2
            ) AS task_completion_pct,
            COUNT(DISTINCT v.id) AS total_visits,
            COUNT(DISTINCT CASE WHEN v.outcome = 'successful' THEN v.id END) AS successful_visits,
            COUNT(DISTINCT CASE WHEN v.outcome = 'failed' THEN v.id END) AS failed_visits,
            ROUND(
                COUNT(DISTINCT CASE WHEN v.outcome = 'successful' THEN v.id END)
                * 100.0 / NULLIF(COUNT(DISTINCT v.id), 0), 2
            ) AS visit_success_pct,
            ROUND(AVG(EXTRACT(EPOCH FROM (v.completed_at - v.started_at)) / 60.0), 1) AS avg_visit_duration_min
        FROM users_user u
        LEFT JOIN tasks_task  t  ON t.assigned_to_id  = u.id
        LEFT JOIN visits_visit v  ON v.field_agent_id = u.id
        LEFT JOIN users_team  tm ON u.team_id   = tm.id
        LEFT JOIN users_region rg ON u.region_id = rg.id
        WHERE u.role = 'field_agent'
          AND u.is_active = TRUE
          AND (%(region_id)s::int IS NULL OR u.region_id = %(region_id)s::int)
          AND (%(team_id)s::int   IS NULL OR u.team_id   = %(team_id)s::int)
        GROUP BY u.id, u.username, u.first_name, u.last_name, tm.name, rg.name
        ORDER BY visit_success_pct DESC NULLS LAST, tasks_completed DESC;
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, {'region_id': region_id, 'team_id': team_id})
        return _fetchall_as_dict(cursor)


def visit_outcomes_report(region_id=None, days=90):
    sql = """
        SELECT
            DATE_TRUNC('week', v.started_at)::date AS week_start,
            COALESCE(v.outcome, 'pending')         AS outcome,
            COUNT(*)                               AS visit_count,
            ROUND(AVG(EXTRACT(EPOCH FROM (v.completed_at - v.started_at)) / 60.0), 1) AS avg_duration_min,
            ROUND(
                COUNT(*) * 100.0
                / SUM(COUNT(*)) OVER (PARTITION BY DATE_TRUNC('week', v.started_at)), 2
            ) AS pct_of_week
        FROM visits_visit v
        JOIN users_user u ON v.field_agent_id = u.id
        WHERE v.status      = 'completed'
          AND v.started_at >= NOW() - INTERVAL '{days} days'
          AND (%(region_id)s::int IS NULL OR u.region_id = %(region_id)s::int)
        GROUP BY DATE_TRUNC('week', v.started_at), v.outcome
        ORDER BY week_start DESC, visit_count DESC;
    """.format(days=int(days))
    with connection.cursor() as cursor:
        cursor.execute(sql, {'region_id': region_id})
        return _fetchall_as_dict(cursor)
