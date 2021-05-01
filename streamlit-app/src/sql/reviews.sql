
WITH original_years AS ( 
  SELECT y.reviewid, MIN(y.year) original_year FROM "pitchfork-etl".years y GROUP BY y.reviewid 
  )

SELECT r.*, 
    COALESCE(y.original_year, r.pub_year) original_year,
    (CASE WHEN (r.title LIKE '%[%]%') or (y.original_year < r.pub_year) THEN 1 ELSE 0 END) reissue
    
FROM "pitchfork-etl".reviews r
INNER JOIN original_years y
    ON r.reviewid = y.reviewid;