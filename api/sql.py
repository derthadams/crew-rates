season_list = """
    SELECT 1 as id, sq.uuid as uuid, sq.start_date as start_date, sq.end_date as end_date, 
        sq.title as season_title, sq.union_status as union_status, sq.genre as genre,
        sq.show_title as show_title, sq.show_uuid as show_uuid, sq.network_name as network_name, 
        sq.network_uuid as network_uuid, 
        JSONB_AGG(DISTINCT JSONB_BUILD_OBJECT(
            'name', sq.company_name,
            'uuid', sq.company_uuid)) as company_list,
            JSONB_AGG(DISTINCT sq.job_report) as job_reports 
    FROM (SELECT rates_season.uuid as uuid, rates_season.start_date as start_date, 
                    rates_season.end_date as end_date, 
                    rates_season.title as title, rates_season.union as union_status, 
                    rates_season.genre as genre, rates_show.title as show_title, 
                    rates_show.uuid as show_uuid, rates_network.name as network_name,
                    rates_network.uuid as network_uuid,
                    rates_company.name as company_name, rates_company.uuid as company_uuid,
                    JSONB_BUILD_OBJECT(
                        'job_title', JSONB_BUILD_OBJECT(
                                        'title', rates_jobtitle.title,
                                        'uuid', rates_jobtitle.uuid),
                        'reports', JSONB_AGG(   	
                            JSONB_BUILD_OBJECT(
                                'daily', rates_ratereport.final_daily, 
                                'hourly', rates_ratereport.final_hourly,
                                'guarantee', rates_ratereport.final_guarantee, 
                                'increase', rates_ratereport.percent_increase) 
                                ORDER BY rates_ratereport.final_daily)) AS job_report 
            FROM ((((((rates_season
            INNER JOIN rates_ratereport ON rates_season.id = rates_ratereport.season_id)
            INNER JOIN rates_jobtitle ON rates_jobtitle.id = rates_ratereport.job_title_id)
            INNER JOIN rates_show ON rates_season.show_id = rates_show.id)
            INNER JOIN rates_network ON rates_season.network_id = rates_network.id)
            INNER JOIN rates_season_companies on rates_season.id = rates_season_companies.season_id)
            INNER JOIN rates_company on rates_season_companies.company_id = rates_company.id)
            WHERE (%s = 0 OR (%s = 1 AND rates_season.start_date >= %s)) 
                AND (%s = 0 OR (%s = 1 AND rates_season.union = %s)) 
                AND (%s = 0 OR(%s = 1 AND rates_season.genre = %s))
GROUP BY rates_season.uuid, rates_season.start_date, rates_season.end_date, rates_season.title, 
            rates_season.union, rates_season.genre, rates_jobtitle.id, rates_show.title, 
            rates_show.uuid, rates_network.name, rates_network.uuid, rates_company.name, 
            rates_company.uuid) as sq
GROUP BY sq.uuid, sq.start_date, sq.end_date, sq.title, sq.union_status, sq.genre, sq.show_title, 
            sq.show_uuid, sq.network_name, sq.network_uuid
ORDER BY sq.start_date DESC;"""
