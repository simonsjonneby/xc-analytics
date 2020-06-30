ALTER TABLE athletes ADD COLUMN if not exists podiums integer;

UPDATE athletes SET podiums=b.podiums
FROM
      (
      SELECT  a.id, r.podiums, r.athlete_id
      FROM    athletes as a
              LEFT JOIN
              (
                -- Counts the number of wins of an athlete
                  SELECT athlete_id,count(athlete_id)*2 as podiums
                  FROM results
                  WHERE rank<=3
                  GROUP BY athlete_id
              ) AS r
        ON a.id = r.athlete_id
      ) as b
where athletes.id=b.id
;
