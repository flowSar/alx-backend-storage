-- List all bands with Glam rock as their main style, ranked by their longevity

SELECT origin, SUM(fans) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;
