UPDATE athletes SET wins=b.wins
FROM
      (
      SELECT  a.id, r.wins, r.athlete_id
      FROM    athletes as a
              LEFT JOIN
              (
                -- Counts the number of wins of an athlete
                  SELECT athlete_id,count(athlete_id) as wins
                  FROM results
                  WHERE rank=1
                  GROUP BY athlete_id
              ) AS r
              ON a.id = r.athlete_id
      ) as b
where athletes.id=b.id
;
